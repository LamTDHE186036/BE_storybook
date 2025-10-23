from app.utils.response import api_response
from app.services.discount_services import DiscountService

class DiscountController:
    
    @staticmethod
    def get_discount(page: int, page_size: int, filters: dict):
        try : 
            data, error = DiscountService.get_discount(page, page_size, filters=filters)
            if error : 
                return api_response(
                    success=False,
                    message=f'Error getting discounts: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Discounts retrieved successfully',
                data = data,
                status_code= 200
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code= 500
            )
            
    @staticmethod
    def create_discount(discount_data: dict):
        try : 
            if not discount_data :
                return api_response(
                    success=False,
                    message='No data provided',
                    status_code=400
                )
            data, error = DiscountService.create_discount(discount_data)
            if error : 
                return api_response(
                    success=False,
                    message=f'Error creating discount: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Discount created successfully',
                data = data,    
                status_code= 201
            )
        except Exception as e : 
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code= 500
            )
    
    @staticmethod
    def update_discount(discount_data: dict):
        try : 
            if not discount_data :
                return api_response(
                    success=False,
                    message='No data provided',
                    status_code=400
                )
            data, error = DiscountService.update_discount(discount_data)
            if error : 
                return api_response(
                    success=False,
                    message=f'Error updating discount: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Discount updated successfully',
                data = data,    
                status_code= 200
            )
        except Exception as e : 
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code= 500
            )
    
    @staticmethod
    def delete_discount(request_data: dict):
        try : 
            
            if not request_data or 'ids' not in request_data   :
                return api_response(
                    success=False,
                    message='No ids provided',
                    status_code=400
                )
            ids = request_data['ids']
            if not isinstance(ids, list)  : 
                return api_response(
                    success=False,
                    message='ids must be a list',
                    status_code=400
                )
            
            data, error = DiscountService.delete_discount(ids)
            if error : 
                return api_response(
                    success=False,
                    message=f'Error deleting discount: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Discount deleted successfully',
                data = data,    
                status_code= 200
            )
        except Exception as e : 
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code= 500
            )    
            