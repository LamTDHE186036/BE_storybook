from app.utils.response import api_response
from app.services.post_services import PostService

class PostController:
    @staticmethod
    def get_posts(page, page_size, filters) : 
        try: 
            data, error = PostService.get_posts(page, page_size, filters)
        
            if error:
                return api_response(
                    success=False,
                    message=error,
                    status_code=400
                )
            return api_response(
                success=True,
                message='Posts retrieved successfully',
                data=data,
                status_code=200
            )
        except Exception as e:
            return api_response(
                success=False,
                message=str(e),
                status_code=500
            )
            
    
    @staticmethod
    def create_post(response_data):
        try : 
            data, error = PostService.create_post(response_data)
            if error:
                return api_response(
                    success=False,
                    message=error,
                    status_code=400
                )
            return api_response(
                success=True,
                message='Post created successfully',
                data=data,
                status_code=201
            )
        except Exception as e:
            return api_response(
                success=False,
                message=str(e),
                status_code=500
            )
    
    
    @staticmethod
    def update_post(response_data):
        try : 
            data, error = PostService.update_post(response_data)
            if error:
                return api_response(
                    success=False,
                    message=error,
                    status_code=400
                )
            return api_response(
                success=True,
                message='Post updated successfully',
                data=data,
                status_code=200
            )
        except Exception as e:
            return api_response(
                success=False,
                message=str(e),
                status_code=500
            )
    
    
    @staticmethod
    def delete_post(response_data):
        try : 
            data, error = PostService.delete_post(response_data)
            if error:
                return api_response(
                    success=False,
                    message=error,
                    status_code=400
                )
            return api_response(
                success=True,
                message='Post deleted successfully',
                data=data,
                status_code=200
            )
        except Exception as e:
            return api_response(
                success=False,
                message=str(e),
                status_code=500
            )
        
            