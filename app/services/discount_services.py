from app.extension import db
from app.models.discount import Discount
from datetime import datetime, timezone
from math import ceil

class DiscountService:
    @staticmethod
    def get_discount(page: int, page_size: int, filters: dict=None):
        try : 
            if page < 1 or page > 500 : 
                page = 1 
            if page_size < 1 or page_size > 100 :
                page_size = 10 
            
            query = db.session.query(Discount).filter(Discount.deleted_at.is_(None))
            
            if filters :
                if filters.get('code') :
                    query = query.filter(Discount.code.ilike(f"%{filters['code']}%"))
                
                if filters.get('id') :
                    query = query.filter(Discount.id == filters['id'])
            
            discounts = query.paginate(
                        page=page,
                        per_page=page_size,
                        error_out=False
            )
            
            response_data = {
                'items': [discount.to_dict() for discount in discounts.items],
                'pagination': {
                    'currentPage': page,
                    'pageSize': page_size,
                    'totalPages': ceil(discounts.total / page_size),
                    'totalItems': discounts.total
                }
            }
            
            return response_data, None
        except Exception as e :
            return None, str(e)
        
    
    @staticmethod
    def create_discount(discount_data: dict):
        try : 
            required_fields = ['code', 'discount_type', 'discount_value', 'min_order_value', 'start_date', 'end_date', 'usage_limit']
            for field in required_fields :
                if field not in discount_data :
                    return None, f'Missing required field: {field}'
            
            existing_discount = db.session.query(Discount).filter(
                Discount.code == discount_data['code'],
                Discount.deleted_at.is_(None)
            ).first()
            if existing_discount :
                return None, 'Discount code already exists'
            
            new_discount = Discount(
                code=discount_data['code'],
                discount_type=discount_data['discount_type'],
                discount_value=discount_data['discount_value'],
                min_order_value=discount_data.get('min_order_value'),
                start_date=datetime.fromisoformat(discount_data['start_date']),
                end_date=datetime.fromisoformat(discount_data['end_date']),
                usage_limit=discount_data.get('usage_limit')
            )
            
            db.session.add(new_discount)
            db.session.commit()
            
            return new_discount.to_dict(), None
        except Exception as e :
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def update_discount(discount_data: dict):
        try : 
            if 'id' not in discount_data :
                return None, 'id is required'
            
            discount = db.session.query(Discount).filter(
                Discount.id == discount_data['id'],
                Discount.deleted_at.is_(None)
            ).first()
            if discount is None :
                return None, 'Discount not found'
            
            updatable_fields = [ 'discount_value', 'min_order_value', 'start_date', 'end_date', 'usage_limit']
            for field in updatable_fields: 
                if field in discount_data :
                    if field in ['start_date', 'end_date']:
                        setattr(discount, field, datetime.fromisoformat(discount_data[field]))
                    else:
                        setattr(discount, field, discount_data[field])
            
            discount.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            return discount.to_dict(), None
        except Exception as e :
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_discount(ids: list):
        try :
            discounts = db.session.query(Discount).filter(
                Discount.id.in_(ids),
                Discount.deleted_at.is_(None)
            ).all()
            if not discounts :
                return None, 'No discounts found to delete'
            
            db.session.query(Discount).filter(
                Discount.id.in_(ids),
                Discount.deleted_at.is_(None)
            ).update(
                {Discount.deleted_at: datetime.now(timezone.utc)},
                synchronize_session=False)
            
            discounts_deleted = [discount.to_dict() for discount in discounts]
            discounts_deleted_info = {'deleted_ids': [discount.id for discount in discounts]}
            discounts_deleted.append(discounts_deleted_info)
            
            db.session.commit()
            
            return discounts_deleted, None
            
        except Exception as e :
            db.session.rollback()
            return None, str(e)