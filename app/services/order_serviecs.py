from app.extension import db
from app.models.discount import Discount
from app.models.order import Order
from app.models.order_items import OrderItems
from app.models.product_variants import ProductVariants
from datetime import datetime, timezone
import json


class OrderService:
    
    @staticmethod
    def get_orders(page: int, page_size: int, filters: dict=None):
        try : 
            if page < 1 or page > 500 : 
                page = 1
            if page_size < 1 or page_size > 100 :
                page_size = 10
            
            query = db.session.query(Order).filter(Order.deleted_at.is_(None))
            
            if filters :
                if filters.get('id') :
                    query = query.filter(Order.id == filters['id'])
                
                if filters.get('customer_id') :
                    query = query.filter(Order.customer_id == filters['customer_id'])
            
            orders = query.paginate(
                        page=page,
                        per_page=page_size,
                        error_out=False
            )
        
            response_data = {
                'items': [order.to_dict() for order in orders.items],
                'pagination': {
                    'currentPage': page,
                    'pageSize': page_size,
                    'totalPages': (orders.total + page_size - 1) // page_size,
                    'totalItems': orders.total
                }
            }
            return response_data, None
        except Exception as e :
            return None, str(e)
    @staticmethod
    def create_order(data: dict):
        try : 
            required_fields = ['customer_id','shipping_address','discount_code','items','status','payment_status','payment_method']
            for field in required_fields :
                if field not in data :
                    return None, f'Missing required field: {field}'
            if not isinstance(data['items'], list) or len(data['items']) == 0 :
                return None, 'Order must contain at least one item'
            
            price_before_discount = sum(item.get('price', 0) * item.get('quantity', 1) for item in data['items'])
            
            discount_code = data.get('discount_code') or None
            discount_value = 0.0
            
            if discount_code :
                discount = db.session.query(Discount).filter(
                    Discount.code == discount_code,
                    Discount.deleted_at.is_(None),
                    Discount.start_date <= datetime.now(timezone.utc),
                    Discount.end_date >= datetime.now(timezone.utc)
                ).first()
                
                if not discount :
                    return None, 'Invalid or expired discount code'
                
                if discount.min_order_value and price_before_discount < discount.min_order_value :
                    return None, f'Order does not meet the minimum value for this discount: {discount.min_order_value}'
                
                if discount.usage_limit is not None:
                    if discount.usage_limit <= 0:
                        return None, 'Discount code usage limit reached'
                    else:
                        discount.usage_limit -= 1

                
                if discount.discount_type == 'percentage' :
                    discount_value = (discount.discount_value / 100) * price_before_discount
                elif discount.discount_type == 'fixed' :
                    discount_value = discount.discount_value
                
                if discount_value > price_before_discount :
                    discount_value = price_before_discount
                
                db.session.add(discount)
                db.session.flush()
                
            total_price = price_before_discount - discount_value
            
            order = Order(
                customer_id = data['customer_id'],
                shipping_address = data['shipping_address'],
                items = json.dumps(data['items']),
                discount_code = discount_code,
                price_before_discount = price_before_discount,
                total_price = total_price,
                status = data['status'],
                payment_status = data['payment_status'],
                payment_method = data['payment_method']
            )
            
            db.session.add(order)
            db.session.flush()
            
            order_items = []
            for item in data['items'] :
                order_item = OrderItems(
                    order_id = order.id,
                    product_variant_id = item.get('product_variant_id'),
                    quantity = item.get('quantity', 1),
                )
                order_items.append(order_item)
                db.session.add(order_item)
            
            db.session.commit()
            return order.to_dict(), None
    
        except Exception as e :
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_order(data: dict):
        try : 
            if 'id' not in data :
                return None, 'id is required'
            
            order = db.session.query(Order).filter(
                Order.id == data['id'],
                Order.deleted_at.is_(None) 
            ).first()
            
            if order is None :
                return None, 'Order not found'
            
            old_status = order.status
            
            updatable_fields = ['shipping_address','status']
            for field in updatable_fields: 
                if field in data :
                    setattr(order, field, data[field])
                    
            if old_status != 'shipped' and order.status == 'shipped' :
                order_items = db.session.query(OrderItems).filter(
                    OrderItems.order_id == order.id,
                    OrderItems.deleted_at.is_(None)
                ).all()
                
                for item in order_items :
                    product_variant = db.session.query(ProductVariants).filter(
                        ProductVariants.id == item.product_variant_id,
                        ProductVariants.deleted_at.is_(None)
                    ).first()
                    
                    if product_variant :
                        if product_variant.quantity < item.quantity :
                            return None, f'Insufficient stock for product variant ID {product_variant.id}'
                        
                        product_variant.quantity -= item.quantity
                        product_variant.quantity_ordered += item.quantity
                        if product_variant.quantity == 0 :
                            product_variant.status = 'out_of_stock'
                        db.session.add(product_variant)
                
            db.session.add(order)
            db.session.commit()
            return order.to_dict(), None
        except Exception as e :
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def delete_order(ids: list):
        try : 
            if not ids or not isinstance(ids, list) :
                return None, 'ids must be a non-empty list'
            
            orders = db.session.query(Order).filter(
                Order.id.in_(ids),
                Order.deleted_at.is_(None)
            ).all() 
            
            if not orders :
                return None, 'No orders found to delete'
            
            Order.query.filter(
                Order.id.in_(ids),
                Order.deleted_at.is_(None)
            ).update(
                {Order.deleted_at: datetime.now(timezone.utc)},
                {Order.updated_at: datetime.now(timezone.utc)},
                synchronize_session=False
            )   
            
            delete_ids = [order.id for order in orders]
            db.session.commit()
            return {'deleted_ids': delete_ids}, None
        except Exception as e :
            db.session.rollback()
            return None, str(e)
        
        
        