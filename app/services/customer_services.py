from app.extension import db
from app.models.cart import Cart
from app.models.product_variants import ProductVariants
from app.models.cart_items import CartItems
from app.models.customer import Customer
from datetime import datetime, timezone
from math import ceil

class CustomerService:
    @staticmethod
    def get_customers(page: int, page_size: int, filters: dict=None):
        try : 
            if page < 1 or page > 500 : 
                page = 1
            if page_size < 1 or page_size > 100 :
                page_size = 10
            query = db.session.query(Customer).filter(Customer.deleted_at.is_(None))
            
            if filters : 
                if filters.get('id') is not None : 
                    query = query.filter(Customer.id == filters['id'])
                
            customers = query.paginate(
                                        page=page,
                                        per_page=page_size,
                                        error_out=False
            )
                        
            response_data = {
                'items' : [customer.to_dict() for customer in customers.items],
                'current_page' : customers.page,
                'total_pages' : ceil(customers.total / page_size),
                'total_items' : customers.total
            }           
            
            return response_data, None
        except Exception as e :
            return None, str(e)
        
    
    @staticmethod
    def create_customer(request_data: dict):
        try : 
            required_fields = ['name','address', 'phone_number', 'email']
            for field in required_fields :
                if field not in request_data :
                    return None, f'{field} is required'
            new_customer = Customer(
                name = request_data['name'],
                address = request_data['address'],
                phone_number = request_data['phone_number'],
                email = request_data['email']
            )
            if 'customer_tier' in request_data :
                new_customer.customer_tier = request_data['customer_tier']
            db.session.add(new_customer)
            db.session.commit()
            return new_customer.to_dict(), None
        except Exception as e :
            db.session.rollback()
            return None, str(e)
    
    
    @staticmethod
    def update_customer(request_data: dict):
        try : 
            if 'id' not in request_data :
                return None, 'id is required'
            customer = db.session.query(Customer).filter(
                Customer.id == request_data['id'],
                Customer.deleted_at.is_(None)
            ).first()
            if customer is None :
                return None, 'Customer not found'
            
            updatable_fields = ['name','address', 'phone_number', 'email', 'customer_tier']
            for field in updatable_fields :
                if field in request_data :
                    setattr(customer, field, request_data[field])
                    
            customer.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            return customer.to_dict(), None
        except Exception as e :
            db.session.rollback()
            return None, str(e)
