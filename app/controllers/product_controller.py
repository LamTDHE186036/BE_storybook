from flask import Flask, jsonify, request, json
from app.services.product_services import ProductService
from app.utils.response import api_response
from app.extension import db

class ProductController:
    
    @staticmethod
    def get_products(page: int, page_size: int, filters: dict): 
        try : 
            data, error = ProductService.get_products(page, page_size, filters=filters)
            
            if error : 
                return api_response(
                    success=False,
                    message=f'Error getting products: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Products retrieved successfully',
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
    def get_category_by_product(page: int, page_size: int, product_id: int):

        if not product_id or product_id < 1 : 
            return api_response(
                success=False,
                message='Invalid product ID',
                status_code=400
            )
        try : 
            data, error = ProductService.get_category_by_product(page, page_size, product_id)
            if error :
                return api_response(
                    success=False,
                    message=f'Error getting categories for product: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Categories retrieved successfully',
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
    def create_product(request_data):   
        try: 
            required_fields = ['name', 'slug','author', 'description', 'image_url', 'category_ids']
            for field in required_fields:
                if field not in request_data:
                    return api_response(
                        success=False,
                        message=f'Missing required field: {field}',
                        status_code=400
                    )
            
            category_ids = request_data.get('category_ids')
            
            if not isinstance(category_ids, list): 
                return api_response(
                    success=False,
                    message='category_ids must be a non-empty list',
                    status_code=400
                )
            
            data, error = ProductService.create_product(request_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error creating product: {error}',
                    status_code=500
                )
                
            return api_response(
                success=True,
                message=f'Product created successfully',
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
    def update_product(product_id: int, request_data):
        if not product_id or product_id < 1 : 
            return api_response(
                success=False,
                message='Invalid product ID',
                status_code=400
            )
        if not request_data : 
            return api_response(
                success=False,
                message='No data provided for update',
                status_code=400
            )
        try : 
            data, error = ProductService.update_product(product_id, request_data)
            if error :
                return api_response(
                    success=False,
                    message=f'Error updating product: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Product updated successfully',
                data=data,
                status_code=200
            )   
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
    
    def delete_product(request_data):
        try : 
            if not request_data or 'ids' not in request_data:
                return api_response(
                    success=False,
                    message='No product IDs provided for deletion',
                    status_code=400
                )
            ids = request_data.get('ids')
            if not isinstance(ids, list) or len(ids) == 0:
                return api_response(
                    success=False,
                    message='ids must be a non-empty list',
                    status_code=400
                )
            data, error = ProductService.delete_product(ids)
            if error :
                return api_response(
                    success=False,
                    message=f'Error deleting products: {error}',
                    status_code=500
                )
            
            return api_response(
                success=True,
                message=f"Successfully deleted categories",
                data=data,
                status_code=200
            )
                
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
        
        