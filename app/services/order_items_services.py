from app.extension import db
from app.models.order_items import OrderItems
from app.models.product_variants import ProductVariants
from app.models.order import Order
from math import ceil

class OrderItemsService:
    
    @staticmethod
    def get_order_items(page, per_page, filters: dict = None):
        try:
            if page < 1 or page > 500 : 
                page = 1
            if per_page < 1 or per_page > 100 :
                per_page = 10
            
            query = db.session.query(OrderItems).filter(OrderItems.deleted_at.is_(None))
            
            if filters :
                if filters.get('id') :
                    query = query.filter(OrderItems.id == filters['id'])
                
                if filters.get('order_id') :
                    query = query.filter(OrderItems.order_id == filters['order_id'])
                
                if filters.get('product_variant_id') :
                    query = query.filter(OrderItems.product_variant_id == filters['product_variant_id'])
            
            order_items = query.paginate(
                page=page,  
                per_page=per_page,
                error_out=False
            )
            
            response_data = {
                'items': [item.to_dict() for item in order_items.items],
                'pagination': {
                    'currentPage': page,
                    'pageSize': per_page,
                    'totalPages': ceil(order_items.total / per_page),
                    'totalItems': order_items.total
                }
            }
            return response_data, None
        except Exception as e:
            return None, str(e)
        
        
    