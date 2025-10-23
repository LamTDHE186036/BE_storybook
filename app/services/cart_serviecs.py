from flask import Blueprint, request, jsonify
from app.extension import db
from app.models.cart import Cart
from app.models.product_variants import ProductVariants 
from app.models.cart_items import CartItems
from app.models.customer import Customer
from datetime import datetime, timezone
from math import ceil

class CartService:
    
    @staticmethod
    def get_cart(page: int, page_size: int, filters: dict=None):
        try : 
            if page < 1 or page > 500 : 
                page = 1
            if page_size < 1 or page_size > 100 :
                page_size = 10
            query = db.session.query(Cart).filter(Cart.deleted_at.is_(None))
            
            if filters : 
                if filters.get('id') is not None : 
                    query = query.filter(Cart.id == filters['id'])
                
                if filters.get('customer_id') is not None : 
                    query = query.filter(Cart.customer_id == filters['customer_id'])
                
            carts = query.paginate(
                                        page=page,
                                        per_page=page_size,
                                        error_out=False
            )
                        
            response_data = {
                'items' : [cart.to_dict() for cart in carts.items],
                'current_page' : carts.page,
                'total_pages' : ceil(carts.total / page_size),
                'total_items' : carts.total
            }           
            
            return response_data, None
        except Exception as e :
            return None, str(e)
        
    
    @staticmethod
    def get_detail_cart(page: int, page_size: int, cart_id: int):
        
        try: 
            if page < 1 or page > 500 : 
                page = 1
            if page_size < 1 or page_size > 100 :
                page_size = 10
            
            cart = db.session.query(Cart).filter(
                Cart.id == cart_id,
                Cart.deleted_at.is_(None)
            ).first()
            
            
            
            if cart is None : 
                return None, 'Cart not found'
            
            products = db.session.query(
                ProductVariants.image_url, ProductVariants.name, ProductVariants.price, ProductVariants.status, CartItems.id, CartItems.quantity
            ).join(
                ProductVariants, CartItems.product_variant_id == ProductVariants.id
            ).filter(
                CartItems.cart_id == cart_id,
            ).all()
            
            products_list = []
            for product in products :
                product_dict = {
                    'image_url' : product.image_url,
                    'name' : product.name,
                    'price' : product.price,
                    'status' : product.status,
                    'quantity_select' : product.quantity,
                    'cart_item_id' : product.id
                }
                products_list.append(product_dict)
            
            response_data = {
                "items" : cart.to_dict(),
                "products" : products_list,
                'current_page' : page,
                'total_pages' : 1,
                'total_items' : 1
            }
            return response_data, None
        except Exception as e :
            return None, str(e)
    
    
    @staticmethod
    def create_cart(response_data: dict):
        try: 
            required_fields = ['customer_id', 'status']
            for field in required_fields : 
                if field not in response_data : 
                    return None, f'Missing required field: {field}'
            
            customer = db.session.query(Customer).filter(
                Customer.id == response_data['customer_id'],
                Customer.deleted_at.is_(None)
            ).first()
            if customer is None : 
                return None, 'Customer not found'
            
            existing_cart = db.session.query(Cart).filter(
                Cart.customer_id == response_data['customer_id'],
                Cart.deleted_at.is_(None)
            ).first()
            if existing_cart is not None : 
                return None, 'Cart for this customer already exists'
            
            new_cart = Cart(
                customer_id = response_data['customer_id'],
                status = response_data['status'],
                created_at = datetime.now(timezone.utc),
                updated_at = datetime.now(timezone.utc)
            )
            db.session.add(new_cart)
            db.session.commit()
            
            return new_cart.to_dict(), None
        
        except Exception as e :
            db.session.rollback()
            return None, str(e)
                
                

    @staticmethod
    def update_cart(request_data: dict):
        try: 
            if 'id' not in request_data : 
                return None, 'Missing cart id'
            
            cart = db.session.query(Cart).filter(
                Cart.id == request_data['id'],
                Cart.deleted_at.is_(None)
            ).first()
            
            if cart is None : 
                return None, 'Cart not found'
            
            allow_fields = ['status']
            updated_fields = []
            
            for field in allow_fields : 
                if field in request_data : 
                    setattr(cart, field, request_data[field])
                    updated_fields.append(field)
                    
            if not updated_fields : 
                return None, 'No valid fields to update'
            
            cart.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            
            response_data = cart.to_dict()
            response_data['updatedFields'] = updated_fields
            return response_data, None
        except Exception as e :
            db.session.rollback()
            return None, str(e)
    
    
    @staticmethod
    def delete_cart(ids: list):
        try: 
            carts = db.session.query(Cart).filter(
                Cart.id.in_(ids),
                Cart.deleted_at.is_(None)
            ).all()
            
            if not carts : 
                return None, 'No carts found to delete'
            
            
            Cart.query.filter(Cart.id.in_(ids), Cart.deleted_at.is_(None)).update(
                {Cart.deleted_at: datetime.now(timezone.utc)},
                synchronize_session=False
            )
            
            
            db.session.commit()
            deleted_ids = [cart.id for cart in carts]
            return {'deleted_ids': deleted_ids}, None
        except Exception as e :
            db.session.rollback()
            return None, str(e)
    
    
        
        
        
            
            
             
               
            