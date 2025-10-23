from flask import Flask, Blueprint, request
from app.services.product_variants_services import ProductVariantsService
from app.utils.response import api_response


class ProductVariantsController:
    
    @staticmethod
    def get_product_variants(page:int, page_size: int, filters: dict): 
        try : 
            data, error = ProductVariantsService.get_product_variants(page, page_size, filters=filters)
            
            
            if error : 
                return api_response(
                    success=False,
                    message=f'Error getting product varients: {error}',
                    status_code=500
                )
            return api_response(
                success=True,   
                message='Product varients retrieved successfully',
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
    def get_product_by_variant(variant_id: int, page: int, page_size: int):
        try:
            if not variant_id or variant_id <= 0:
                return api_response(
                    success=False,
                    message="Invalid variant ID.",
                    status_code=400
                )       
                
            data, error = ProductVariantsService.get_product_by_variant(variant_id, page, page_size)
            if error:
                return api_response(
                    success=False,
                    message=f"Error retrieving product by variant: {error}",
                    status_code=500
                )
            
            return api_response(
                success=True,
                message="Product retrieved successfully by variant.",
                data=data,
                status_code=200
            )
        
        except Exception as e:
            return api_response(
                success=False,
                message=f"Internal server error: {str(e)}",
                status_code=500
            )
    
    @staticmethod
    def create_product_variant(request_data: dict):
        try : 
            required_fields = ['product_id','name', 'slug', 'price', 'quantity', "status", 'quantity_ordered', 'image_url']
            for filed in required_fields : 
                if filed not in request_data : 
                    return api_response(
                        success=False, 
                        message=f'Missing required field: {filed}', 
                        status_code= 400
                    )
        
            data, error = ProductVariantsService.create_product_variant(request_data)
            if error : 
                return api_response(
                    success=False,
                    message=f'Error creating product varient: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Product varient created successfully',
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
    def update_product_variant(variant_id: int, request_data: dict):
        try:
            if not variant_id or variant_id <= 0:
                return api_response(
                    success=False,
                    message="Invalid variant ID.",
                    status_code=400
                )       
                
            if not request_data or not isinstance(request_data, dict):
                return api_response(
                    success=False,
                    message="Request data must be a valid dictionary.",
                    status_code=400
                )
                
            data, error = ProductVariantsService.update_product_variant(variant_id, request_data)
            if error:
                return api_response(
                    success=False,
                    message=f"Error updating product variant: {error}",
                    status_code=500
                )
            
            return api_response(
                success=True,
                message="Product variant updated successfully.",
                data=data,
                status_code=200
            )
        
        except Exception as e:
            return api_response(
                success=False,
                message=f"Internal server error: {str(e)}",
                status_code=500
            )
        
    @staticmethod
    def delete_variants(request_data: dict): 
        try:
            if not request_data or 'ids' not in request_data : 
                return api_response(
                    success=False, 
                    message="Request data must contain 'ids' field.", 
                    status_code=400
                )
                
            ids = request_data.get('ids')
            if not isinstance(ids, list) or len(ids) == 0 : 
                return api_response(
                    success=False,
                    message="'ids' must be a non-empty list.",
                    status_code=400
                )
            
            data, error = ProductVariantsService.delete_variants(ids)
            if error : 
                return api_response(
                    success=False, 
                    message=f"Error deleting product variants: {error}", 
                    status_code=500
                )
            return api_response(
                success=True,   
                message="Product variants deleted successfully.",
                data=data,
                status_code=200
            )
            
        except Exception as e : 
            return api_response(
                success=False, 
                message=f"Internal server error: {str(e)}", 
                status_code=500
            )
            
            