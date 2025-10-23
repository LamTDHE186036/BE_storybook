from app.utils.response import api_response
from app.services.cart_serviecs import CartService
from app.services.cart_items_services import CartItemsService

class CartItemsController:
    
    @staticmethod
    def get_cart_items(page, page_size, filters):
        try : 
            data, error = CartItemsService.get_cart_items(page, page_size, filters=filters)
            if error :
                return api_response(
                    success=False,
                    message=f'Error getting cart items: {error}',
                    status_code=500
                )
            return api_response(
                success=True,   
                message='Cart items retrieved successfully',
                data=data,
                status_code=200    
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
            
    
    @staticmethod
    def create_cart_items(request_data):
        try : 
            if not request_data or "customer_id" not in request_data: 
                return api_response(
                    success=False,
                    message='Request data is required',
                    status_code=400
                )
            data, error = CartItemsService.create_cart_items(request_data)
            if error :
                return api_response(
                    success=False,
                    message=f'Error creating cart items: {error}',
                    status_code=500
                )
            return api_response(
                success=True,

                message='Cart items created successfully',
                data=data,      
                status_code=201
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
        
    @staticmethod
    def update_cart_items(request_data):
        try : 
            if not request_data or "id" not in request_data: 
                return api_response(
                    success=False,
                    message='Request data is required',
                    status_code=400
                )
            data, error = CartItemsService.update_cart_items(request_data)
            if error :
                return api_response(
                    success=False,
                    message=f'Error updating cart items: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Cart items updated successfully',
                data=data,      
                status_code=200
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )   
    
    @staticmethod
    def delete_cart_items(request_data):
        try : 
            if not request_data or "ids" not in request_data: 
                return api_response(
                    success=False,
                    message='ids list is required',
                    status_code=400
                )
            ids = request_data.get('ids')
            if not isinstance(ids, list):
                    return api_response(
                        success=False,
                        message='ids must be a list of integers',
                        status_code=400
                    )   
            data, error = CartItemsService.delete_cart_items(ids)
            if error :
                return api_response(
                    success=False,
                    message=f'Error deleting cart items: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Cart items deleted successfully',
                data=data,      
                status_code=200
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
            
           
    
    

