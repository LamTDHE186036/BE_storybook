from app.utils.response import api_response
from app.services.order_items_services import OrderItemsService

class OrderItemsController:
    @staticmethod
    def get_order_items(page, per_page, filters: dict = None):
        try:
            
            data, error = OrderItemsService.get_order_items(page, per_page, filters=filters)
            if error:
                return api_response(
                    success=False,
                    message=f'Error getting order items: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Order items retrieved successfully',
                data=data,
                status_code=200
            )
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
            