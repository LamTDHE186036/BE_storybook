from flask import Flask, jsonify, request, json
from app.services.category_services import CategoryService
from app.utils.response import api_response


class CategoryController:
    
    @staticmethod
    def get_category(page:int, page_size: int, filters: dict, include_children: bool): 
        try : 
            data, error = CategoryService.get_category(page, page_size, filters=filters, include_children=include_children)
            
            
            if error : 
                return api_response(
                    success=False,
                    message=f'Error getting categories: {error}',
                    status_code=500
                )
            return api_response(
                success=True,   
                message='Categories retrieved successfully',
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
    def create_category(request_data): 
        print(json.dumps(request_data, indent=2, ensure_ascii=False))
        try : 
            required_fields = ['name', 'description', 'slug', 'parent_id']
            for field in required_fields :
                if field not in request_data : 
                    return api_response(
                        success=False, 
                        message=f'Missing required field: {field}', 
                        status_code=400
                    )
            data, error = CategoryService.create_category(request_data)
            if error : 
                return api_response(
                    success=False,
                    message=f'Error creating category: {error}',
                    status_code=500
                )
            return api_response(
                success=True,   
                message='Category created successfully',
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
    def update_category(category_id: int, request_data):
        try : 
            if not category_id or category_id < 1 : 
                return api_response(
                    success=False,
                    message='Invalid category ID',
                    status_code=400
                )
            if not request_data : 
                return api_response(
                    success=False,
                    message='No data provided for update',
                    status_code=400
                )
            data, error = CategoryService.update_category(category_id, request_data)
            if error :
                return api_response(
                    success=False,
                    message=f'Error updating category: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Category updated successfully',
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
    def delete_category(request_data): 
        try: 
            if not request_data or 'ids' not in request_data:
                return api_response(
                    success=False,
                    message="No category IDs provided for deletion",
                    status_code=400
                )
            ids = request_data.get('ids')
            if not isinstance(ids, list) or not ids : 
                return api_response(
                    success=False,
                    message="Invalid category IDs format. It should be a non-empty list.",
                    status_code=400
                )
            
            data, error = CategoryService.delete_category(ids)
            if error :
                return api_response(
                    success=False,
                    message=f"Error deleting categories: {error}",
                    status_code=500
                )
                
            deleted_count = len(data.get('deleted_categories', []))
            failed_count = len(data.get('failed_deletions', []))
            
            if deleted_count == 0 and failed_count > 0:
                # Không xóa được category nào
                return api_response(
                    success=False,
                    message=f"Failed to delete all {failed_count} categories",
                    data=data,
                    status_code=400
                )
            elif deleted_count > 0 and failed_count > 0:
                # Xóa được một số, một số thất bại
                return api_response(
                    success=True,
                    message=f"Successfully deleted {deleted_count} categories, {failed_count} failed",
                    data=data,
                    status_code=200
                )
            else:
                # Xóa thành công tất cả
                return api_response(
                    success=True,
                    message=f"Successfully deleted all {deleted_count} categories",
                    data=data,
                    status_code=200
                )
            
        except Exception as e :
            return api_response(
                success=False,
                message=f"Internal server error: {str(e)}",
                status_code=500
            )