from app.utils.response import api_response
from app.services.order_serviecs import OrderService

class OrderController:
    
    @staticmethod
    def get_orders(page: int, page_size: int, filters: dict=None):
        try : 
            data, error = OrderService.get_orders(page, page_size, filters=filters)
            if error : 
                return api_response(
                    success=False,
                    message=f'Error getting orders: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Orders retrieved successfully',
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
    def create_order(data: dict):
        try : 
            if not data :
                return api_response(
                    success=False,
                    message='No input data provided',
                    status_code=400
                )
            data, error = OrderService.create_order(data)
            if error : 
                return api_response(
                    success=False,
                    message=f'Error creating order: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Order created successfully',   
                data = data,
                status_code=201
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code= 500
            )
    
    @staticmethod
    def update_order(data: dict):
        try : 
            if not data :
                return api_response(
                    success=False,
                    message='No input data provided',
                    status_code=400
                )
            data, error = OrderService.update_order(data)
            if error : 
                return api_response(
                    success=False,
                    message=f'Error updating order: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Order updated successfully',   
                data = data,
                status_code=200
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code= 500
            )

    @staticmethod
    def delete_order(request_data: dict):
        try : 
            if not request_data or 'ids' not in request_data :     
                return api_response(
                    success=False,
                    message='No input data provided or ids missing',
                    status_code=400
                )
            ids = request_data['ids']
            data, error = OrderService.delete_order(ids)
            if error : 
                return api_response(
                    success=False,
                    message=f'Error deleting orders: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Orders deleted successfully',   
                data = data,
                status_code=200
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code= 500
            )