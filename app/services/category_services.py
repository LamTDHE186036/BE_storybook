from app.models.category import Category
from app.models.product_category import ProductCategory
from app.extension import db
from math import ceil
import json
from datetime import datetime, timezone

class CategoryService :
    
    @staticmethod
    def get_category(page: int, page_size: int, filters: dict=None, include_children: bool=False): 
        try : 
            if page < 1 or page > 500 : 
                page = 1
            if page_size < 1 or page_size > 100 : 
                page_size = 10  
            
            query = Category.query.filter(Category.deleted_at.is_(None))
            
            if filters : 
                if filters.get('name') is not None : 
                    query = query.filter(Category.name.ilike(f'%{filters["name"]}%'))
                    
                if filters.get('id') is not None : 
                    query = query.filter(Category.id == filters['id'])
                    
                if filters.get('slug') is not None : 
                    query = query.filter(Category.slug == filters['slug'])
            
                    
            categories = query.paginate(
                                        page=page,
                                        per_page=page_size, 
                                        error_out=False
                                        )
            
            items = []
            for item in categories.items :
                item_dict = item.to_dict()
                if include_children :
                    children = Category.query.filter_by(parent_id=item.id).all()
                    item_dict['children'] = [child.to_dict() for child in children]
                items.append(item_dict)
            
            response_data = {
                'items': items,
                'pagination': {
                    'currentPage': page,
                    'pageSize': page_size,
                    'totalPages': ceil(categories.total / page_size),
                    'totalItems': categories.total
                }
            }
            
            
            
            return response_data, None
                   
        except Exception as e :
            return None, str(e)
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def create_category(category_data: dict):
        try: 
            new_category = Category(
                name=category_data.get('name'),
                description=category_data.get('description'),
                slug=category_data.get('slug'),
                parent_id=category_data.get('parent_id')
            )
            
            db.session.add(new_category)
            db.session.commit()
            
            return new_category.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_category(category_id: int, category_data: dict):
        
        try:
            category = Category.query.get(category_id)
            if not category or category.deleted_at is not None:
                return None, "Category not found"
            
            allow_fields = ['name', 'description', 'slug', 'parent_id']
            updated_fields = []
            
            for field in allow_fields:
                if field in category_data:
                    setattr(category, field, category_data[field])
                    updated_fields.append(field)  
                
            if not updated_fields:
                return None, "No valid fields to update"
            
            db.session.commit()
            
            response_data = category.to_dict()
            response_data['updatedFields'] = updated_fields
            return response_data, None
        
        except Exception as e:
                db.session.rollback()
                return None, str(e)
            
    @staticmethod
    def delete_category(ids: list): 
        try: 
            categories= Category.query.filter(Category.id.in_(ids), Category.deleted_at.is_(None)).all()
            if not categories : 
                return None, "No categories found to delete"
            
            deleted_categories = []
            failed_deletions = []
            
            for category in categories :
                children_count = Category.query.filter(Category.parent_id==category.id, Category.deleted_at.is_(None)).count()
                if children_count > 0 :
                    failed_deletions.append({
                        'id': category.id,
                        'name': category.name,
                        'reason': 'Category has sub-categories. Delete children first.'
                    })
                    continue # Bỏ qua category này, không xóa
                
                
                product_count = db.session.query(ProductCategory).filter(ProductCategory.category_id==category.id).count()
                if product_count > 0 :
                    failed_deletions.append({
                        'id': category.id,
                        'name': category.name,
                        'reason': 'Category is associated with products'
                    })
                    continue
                
                
                deleted_categories.append(category)
                category.deleted_at = datetime.now(timezone.utc)
                
            db.session.commit()
            
            response_data = {
                'deleted_categories': [cat.to_dict() for cat in deleted_categories],
                'failed_deletions': failed_deletions
            }
            return response_data, None
                  
        except Exception as e :
            db.session.rollback()
            return None, str(e)
            
            
            
            
            