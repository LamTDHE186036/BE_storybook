from app.extension import db
from app.models.post import Post
from app.models.post_category import PostCategory
from datetime import datetime, timezone
from math import ceil

class PostService:
    @staticmethod
    def get_posts(page, page_size, filters):
        try:
            if page < 1 or page > 100:
                page = 1 
            if page_size < 1 or page_size > 100:
                page_size = 10
            
            query = db.session.query(Post).filter(Post.deleted_at.is_(None))
            
            if filters:
                if filters.get('id') is not None:
                    query = query.filter(Post.id == filters['id'])
                if filters.get('slug') is not None:
                    query = query.filter(Post.slug.ilike(f"%{filters['slug']}%"))
                if filters.get('name') is not None:
                    query = query.filter(Post.name.ilike(f"%{filters['name']}%"))
                
            posts = query.paginate(
                page=page,
                per_page=page_size,
                error_out=False
            )
            
            response_data = {
                'items': [post.to_dict() for post in posts.items],
                'current_page': posts.page,
                'total_pages': ceil(posts.total / page_size),
                'total_items': posts.total
            }
            return response_data, None
        except Exception as e:
            return None, str(e)
        
        
    @staticmethod
    def create_post(data: dict):
        try:
            required_fields = ["post_category_id", "name", "slug", "content", "url_image"]
            for field in required_fields:
                if field not in data:
                    return None, f'Missing required field: {field}'
            
            post_category = db.session.query(PostCategory).filter(
                PostCategory.id == data['post_category_id'],
                PostCategory.deleted_at.is_(None)
            ).first()
            if not post_category:
                return None, 'Invalid post_category_id'
            
            new_post = Post(
                post_category_id=data['post_category_id'],
                name=data['name'],
                slug=data['slug'],
                content=data['content'],
                url_image=data['url_image']
            )
            db.session.add(new_post)
            db.session.commit()
            return new_post.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def update_post(data: dict):
        try : 
            if not data or 'id' not in data:
                return None, 'Missing post id for update'
            
            post = db.session.query(Post).filter(
                Post.id == data['id'],
                Post.deleted_at.is_(None)
            ).first()
            
            if not post :
                return None, 'Post not found'
            
      
            if 'post_category_id' in data :
                post_category = db.session.query(PostCategory).filter(
                    PostCategory.id == data['post_category_id'],
                    PostCategory.deleted_at.is_(None)
                ).first()
                if not post_category:
                    return None, 'Invalid post_category_id'
            
            fields_updatable = ['post_category_id', 'name', 'slug', 'content', 'url_image']
            for field in fields_updatable :
                if field in data :
                    setattr(post, field, data[field])
                    
            post.updated_at = datetime.now(timezone.utc)
                
            db.session.commit()
            return post.to_dict(), None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
            
            

    @staticmethod
    def delete_post(data: dict):
        
        try :
            if not data or 'ids' not in data:
                return None, 'Missing post id for deletion'
            
            ids = data.get('ids')
            if not isinstance(ids, list) or not ids:
                return None, 'ids must be a non-empty list'
            
            posts = db.session.query(Post).filter(
                Post.id.in_(ids),
                Post.deleted_at.is_(None)
            ).all()
            if not posts :
                return None, 'No posts found to delete'
            db.session.query(Post).filter(
                Post.id.in_(ids),
                Post.deleted_at.is_(None)
            ).update(
                {Post.deleted_at: datetime.now(timezone.utc),
                 Post.updated_at: datetime.now(timezone.utc)},
                synchronize_session=False
            )
            
            deleted_ids = [post.id for post in posts]
            db.session.commit()
            return {'deleted_ids': deleted_ids }, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
            