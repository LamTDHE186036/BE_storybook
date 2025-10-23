from app.utils.response import api_response
from flask import Blueprint, request, jsonify
from app.services.cart_serviecs import CartService

class CartController:
    
    @staticmethod
    def get_cart(page, page_size, filters):
        try : 
            data, error = CartService.get_cart(page, page_size, filters=filters)
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
    def get_detail_cart(page, page_size, cart_id):
        try : 
            if cart_id is None :
                return api_response(
                    success=False,
                    message='cart_id is required',
                    status_code=400
                )
    
            data, error = CartService.get_detail_cart(page, page_size, cart_id)
            if error :
                return api_response(
                    success=False,
                    message=f'Error getting cart details: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Cart details retrieved successfully',
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
    def create_cart(request_data):
        try: 
            if not request_data or 'customer_id' not in request_data:
                return api_response(
                    success=False,
                    message='customer_id is required',
                    status_code=400
                )
        
            
            data, error = CartService.create_cart(request_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error creating cart: {error}',
                    status_code=500
                )
            
            return api_response(
                success=True,
                message='Cart created successfully',
                data=data,
                status_code=201
            )
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
    
    @staticmethod
    def update_cart(request_data): 
        try: 
            if not request_data or 'id' not in request_data:
                return api_response(
                    success=False,
                    message='cart id is required',
                    status_code=400
                )
            
            data, error = CartService.update_cart(request_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error updating cart: {error}',
                    status_code=500
                )
            
            return api_response(
                success=True,
                message='Cart updated successfully',
                data=data,
                status_code=200
            )
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
        
    @staticmethod
    def delete_cart(request_data: dict):
        try : 
            if not request_data or 'ids' not in request_data:
                return api_response(
                    success=False,
                    message='ids list is required',
                    status_code=400
                )
            ids = request_data.get('ids')
            if not isinstance(ids, list) : 
                return api_response(
                    success=False,
                    message='ids must be a list of integers',
                    status_code=400
                )
            
            data, error = CartService.delete_cart(ids)
            if error :
                return api_response(
                    success=False,
                    message=f'Error deleting carts: {error}',
                    status_code=500
                )
            
            return api_response(
                success=True,
                message='Carts deleted successfully',
                data=data,
                status_code=200
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
        
        
        
            