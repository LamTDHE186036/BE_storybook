from app.extension import db
from app.models.cart import Cart
from app.models.product_variants import ProductVariants
from app.models.cart_items import CartItems
from app.models.customer import Customer
from datetime import datetime, timezone
from math import ceil

class CartItemsService:
    @staticmethod
    def get_cart_items(page: int, page_size: int, filters: dict=None):
        try : 
            if page < 1 or page > 500 : 
                page = 1
            if page_size < 1 or page_size > 100 :
                page_size = 10
            query = db.session.query(CartItems).filter(CartItems.deleted_at.is_(None))
            
            if filters : 
                if filters.get('id') is not None : 
                    query = query.filter(CartItems.id == filters['id'])
                
                if filters.get('cart_id') is not None : 
                    query = query.filter(CartItems.cart_id == filters['cart_id'])
                
                if filters.get('product_variant_id') is not None : 
                    query = query.filter(CartItems.product_variant_id == filters['product_variant_id'])
                
            cart_items = query.paginate(
                                        page=page,
                                        per_page=page_size,
                                        error_out=False
            )
                        
            response_data = {
                'items' : [cart_item.to_dict() for cart_item in cart_items.items],
                'current_page' : cart_items.page,
                'total_pages' : ceil(cart_items.total / page_size),
                'total_items' : cart_items.total
            }           
            
            return response_data, None
        except Exception as e :
            return None, str(e)
        
    @staticmethod
    def create_cart_items(request_data: dict):
        try : 
            required_fields = ['customer_id', 'product_variant_id', 'quantity']
            for field in required_fields:
                if field not in request_data:
                    return None, f'Missing required field: {field}'
            
            customer_id = request_data['customer_id']
            product_variant_id = request_data['product_variant_id']
            quantity = request_data['quantity']
            
            customer = db.session.query(Customer).filter(
                Customer.id == customer_id,
                Customer.deleted_at.is_(None)
            ).first()
            if customer is None : 
                return None, 'Customer not found'
            
            product_variant = db.session.query(ProductVariants).filter(
                ProductVariants.id == product_variant_id,
                ProductVariants.deleted_at.is_(None)
            ).first()
            if product_variant is None : 
                return None, 'Product variant not found'
            
            cart = db.session.query(Cart).filter(
                Cart.customer_id == customer_id,    
                Cart.deleted_at.is_(None)
            ).first()
            if cart is None : 
                cart = Cart(
                    customer_id = customer_id,
                    status = 'active',
                    created_at = datetime.now(timezone.utc), 
                    updated_at = datetime.now(timezone.utc)
                )
                db.session.add(cart)
                db.session.commit()
                
            existing_cart_item = db.session.query(CartItems).filter(
                CartItems.cart_id == cart.id,
                CartItems.product_variant_id == product_variant_id,
                CartItems.deleted_at.is_(None)
            ).first()
            if existing_cart_item : 
                existing_cart_item.quantity += quantity
                existing_cart_item.updated_at = datetime.now(timezone.utc)
                db.session.commit()
                new_cart_item = existing_cart_item
            
            else : 
                new_cart_item = CartItems(
                    cart_id = cart.id,
                    product_variant_id = product_variant_id,
                    quantity = quantity,
                    created_at = datetime.now(timezone.utc),
                    updated_at = datetime.now(timezone.utc)
                )
                db.session.add(new_cart_item)
            
            cart.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            
            return new_cart_item.to_dict(), None
        
        except Exception as e :
            db.session.rollback()
            return None, str(e)
            
            
    @staticmethod
    def update_cart_items(request_data: dict):
        try : 
            if 'id' not in request_data : 
                return None, 'Missing cart item id'
            
            cart_item = db.session.query(CartItems).filter(
                CartItems.id == request_data['id'],
                CartItems.deleted_at.is_(None)
            ).first()
            if cart_item is None : 
                return None, 'Cart item not found'
            
            if 'quantity' in request_data : 
                cart_item.quantity += request_data['quantity']
            
            cart_item.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            
            cart = db.session.query(Cart).filter(
                Cart.id == cart_item.cart_id,
                Cart.deleted_at.is_(None)
            ).first()
            if cart : 
                cart.updated_at = datetime.now(timezone.utc)
                db.session.commit()
            
            return cart_item.to_dict(), None
        except Exception as e :
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def delete_cart_items(ids: list):
        try : 
            
            cart_items = db.session.query(CartItems).filter(
                CartItems.id.in_(ids),
                CartItems.deleted_at.is_(None)
            ).all()
            if not cart_items : 
                return None, 'No cart items found to delete'
            
            CartItems.query.filter(
                CartItems.id.in_(ids),
                CartItems.deleted_at.is_(None)
            ).update(
                {
                    'deleted_at': datetime.now(timezone.utc),
                    'updated_at': datetime.now(timezone.utc)
                },
                synchronize_session=False
            )
            
            db.session.commit()
            deleted_ids = [item.id for item in cart_items]
            return {'deleted_ids': deleted_ids}, None
            

            
            
        except Exception as e :
            db.session.rollback()
            return None, str(e)
            
            
            
        