from app.extension import db
from app.models.post_category import PostCategory
from app.models.post import Post
from datetime import datetime, timezone
from math import ceil

class PostCategoryService:
    
    @staticmethod
    def get_post_categories(page, page_size, filters: dict = None):
        try:
            if page < 1 or page > 500 : 
                page = 1
            if page_size < 1 or page_size > 100 :
                page_size = 10
            
            query = db.session.query(PostCategory).filter(PostCategory.deleted_at.is_(None))
            
            if filters :
                if filters.get('id') :
                    query = query.filter(PostCategory.id == filters['id'])
                if filters.get('slug') :
                    query = query.filter(PostCategory.slug == filters['slug'])
                
            post_categories = query.paginate(
                page=page,
                per_page=page_size,
                error_out=False
            )
            response_data = {
                'items': [category.to_dict() for category in post_categories.items],
                'pagination': {
                    'currentPage': page,
                    'pageSize': page_size,
                    'totalPages': ceil(post_categories.total / page_size),
                    'totalItems': post_categories.total
                }
            }
            return response_data, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_posts_by_category(page, page_size, slug):
        try : 
            if page < 1 or page > 500 : 
                page = 1
            if page_size < 1 or page_size > 100 :
                page_size = 10
            
            category = db.session.query(PostCategory).filter(
                PostCategory.slug == slug,
                PostCategory.deleted_at.is_(None)
            ).first()
            
            if not category :
                return None, 'Post category not found'
            
            query = db.session.query(Post).filter(
                Post.post_category_id == category.id,
                Post.deleted_at.is_(None)
            )
            
            posts = query.paginate(
                page=page,
                per_page=page_size,
                error_out=False
            )
            
            response_data = {
                'items': [post.to_dict() for post in posts.items],
                'pagination': {
                    'currentPage': page,
                    'pageSize': page_size,
                    'totalPages': ceil(posts.total / page_size),
                    'totalItems': posts.total
                }
            }
            return response_data, None
        except Exception as e:
            return None, str(e)
        
    
    @staticmethod
    def create_post_category(request_data):
        try :
            if not request_data : 
                return None, 'Invalid request data'
            
            fields_required = ['name',"description",'slug']
            for field in fields_required :
                if field not in request_data :
                    return None, f'Missing required field: {field}'
                
            new_category = PostCategory(
                name=request_data['name'],
                description=request_data['description'],
                slug=request_data['slug']
            )
            
            db.session.add(new_category)
            db.session.commit()
            
            return new_category.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    
    @staticmethod
    def update_post_category(request_data):
        try :
            if not request_data : 
                return None, 'Invalid request data'
            
            if 'id' not in request_data :
                return None, 'Missing required field: id'
            
            category = db.session.query(PostCategory).filter(
                PostCategory.id == request_data['id'],
                PostCategory.deleted_at.is_(None)
            ).first()
            
            if not category :
                return None, 'Post category not found'
            
            updatable_fields = ['name','description','slug']
            for field in updatable_fields :
                if field in request_data :
                    setattr(category, field, request_data[field])
            db.session.add(category)
            db.session.commit()
            return category.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    
    @staticmethod
    def delete_post_category(request_data):
        
        try :
            if not request_data : 
                return None, 'Invalid request data'
            
            ids = request_data.get('ids')
            if not ids or not isinstance(ids, list) :
                return None, 'ids must be a list of post category IDs to delete'
            
            categories = db.session.query(PostCategory).filter(
                PostCategory.id.in_(ids),
                PostCategory.deleted_at.is_(None)
            ).all()
        
            if not categories :
                return None, 'No post categories found to delete'
            
            posts = db.session.query(Post).filter(
                Post.post_category_id.in_(ids),
                Post.deleted_at.is_(None)
            ).all()
            if posts :
                return None, 'Cannot delete post categories that have associated posts'
            
            
            db.session.query(PostCategory).filter(
                PostCategory.id.in_(ids),
                PostCategory.deleted_at.is_(None)
            ).update(
                {PostCategory.deleted_at: datetime.now(timezone.utc)},
                synchronize_session=False
            )

            deleted_ids = [category.id for category in categories]
            db.session.commit()
            
            return {'deleted_ids': deleted_ids}, None
        except Exception as e :
            db.session.rollback()
            return None, str(e)
        
        
        