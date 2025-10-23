from app.utils.response import api_response
from app.services.post_category_services import PostCategoryService

class PostCategoryController:
    
    @staticmethod
    def get_post_categories(page, page_size, filters: dict = None):
        try: 
            
            
            data, error = PostCategoryService.get_post_categories(page, page_size, filters)
            if error:
                return api_response(
                    success=False,
                    message=f'Error getting post categories: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Post categories retrieved successfully',
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
    def get_posts_by_category(page, page_size, slug):
        try:
            data, error = PostCategoryService.get_posts_by_category(page, page_size, slug)
            
            if error:
                return api_response(
                    success=False,
                    message=f'Error getting posts by category: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Posts by category retrieved successfully',
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
    def create_post_category(request_data):
        try:
            data, error = PostCategoryService.create_post_category(request_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error creating post category: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Post category created successfully',
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
    def update_post_category(request_data):
        try:
            data, error = PostCategoryService.update_post_category(request_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error updating post category: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Post category updated successfully',
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
    def delete_post_category(request_data):
        try:
            data, error = PostCategoryService.delete_post_category(request_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error deleting post category: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Post category deleted successfully',
                data=data,
                status_code=200
            )
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )