from app.models.product import Product
from app.models.category import Category
from app.models.product_category import ProductCategory
from app.models.product_variants import ProductVariants
from app.services.product_variants_services import ProductVariantsService
from app.extension import db
from math import ceil
import json
from datetime import datetime, timezone

class ProductService:
    @staticmethod
    def get_products(page: int, page_size: int, filters: dict=None):
        try: 
            if page < 1 or page > 500 : 
                page = 1
            if page_size < 1 or page_size > 100 : 
                page_size = 10
            
            query = Product.query.filter(Product.deleted_at.is_(None))
            
            if filters : 
                if filters.get('name') is not None : 
                    query = query.filter(Product.name.ilike(f'%{filters["name"]}%'))
                    
                if filters.get('slug') is not None : 
                    query = query.filter(Product.slug == filters['slug'])
                
                if filters.get('id') is not None : 
                    query = query.filter(Product.id == filters['id'])
            
            

            products = query.paginate(
                                        page=page,
                                        per_page=page_size, 
                                        error_out=False
            )
            
            items = []
            for product in products.items: 
                category_ids = list(
                    db.session.scalars(
                        db.select(ProductCategory.category_id).where(
                            ProductCategory.product_id == product.id
                        )
                    )
                )
                product_dict = product.to_dict()
                product_dict['category_ids'] = category_ids
                items.append(product_dict)

            response_data = {
                'items': items,
                'pagination': {
                    'currentPage': page,
                    'pageSize': page_size,
                    'totalPages': ceil(products.total / page_size),
                    'totalItems': products.total
                }
            }
            return response_data, None
        except Exception as e :
            return None, str(e)
    
    @staticmethod
    def get_category_by_product(page: int, page_size: int, product_id: int):
        try: 
            if page < 1 or page > 500 : 
                page = 1    
            if page_size < 1 or page_size > 100 :
                page_size = 10
            
            product = db.session.get(Product, product_id)
            if not product or product.deleted_at is not None:
                return None, "Product not found"
            
            query = (
                        db.session.query(Category.id, Category.name, Category.slug)
                        .join(ProductCategory)
                        .filter(
                            ProductCategory.product_id == product_id,
                            Category.deleted_at.is_(None)
                        )
                    )
        
        
            categories = query.paginate(
                                        page=page,
                                        per_page=page_size,
                                        error_out=False
                                        )
            
    
    
    
            items = [

                        {"id": c[0], "name": c[1], "slug": c[2]}
                        for c in categories
                    ]
            response_data = {
                "product_name": product.name,
                'items': items,
                'pagination': {
                    'currentPage': page,
                    'pageSize': page_size,
                    'totalPages': ceil(categories.total / page_size),
                    'totalItems': categories.total}
            }       
            return response_data, None
            
        
        except Exception as e :
            return None, str(e)
            
            

    @staticmethod
    def create_product(product_data: dict):
        try: 
            category_ids = product_data.get('category_ids')
            if not category_ids or not isinstance(category_ids, list) or len(category_ids) == 0:
                return None, "Category IDs are required and must be a non-empty list."
            
            valid_categories_ids = list(
                db.session.scalars( #scalars() sẽ trả về một generator gồm các giá trị cột duy nhất
                    db.select(Category.id).where(
                        Category.id.in_(category_ids),
                        Category.deleted_at.is_(None)
                       )
                    )
                )
            
            Added_IDs = f'{valid_categories_ids}'

            
            if not valid_categories_ids or len(valid_categories_ids) == 0:
                return None, "No valid categories found for the provided IDs."
            
            
            
            new_product = Product(
                name=product_data.get('name'),
                slug=product_data.get('slug'),
                author=product_data.get('author'),
                description=product_data.get('description'),
                quantity=product_data.get('quantity'),
                image_url=product_data.get('image_url')
            )
            
            db.session.add(new_product)
            db.session.flush()  # Ensure new_product.id is available
            db.session.bulk_insert_mappings( #Bulk insert nhiều records vào bảng ProductCategory cùng lúc
                ProductCategory,
                [{'product_id': new_product.id, 'category_id': category_id} for category_id in valid_categories_ids]
            )
            db.session.commit()
            result = new_product.to_dict()
            result['Added_Category_IDs'] = Added_IDs
            return result, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update_product(product_id: int, product_data: dict):
        try:
            product = db.session.get(Product, product_id)
            if not product or product.deleted_at is not None:
                return None, "Product not found"
            
            allowed_fields = ['name', 'slug', 'author', 'description', 'image_url', 'category_ids']
            updated_fields = []
            
            for field in allowed_fields:
                if field in product_data:
                    if field == 'category_ids':
                        category_ids = product_data.get('category_ids')
                        if not isinstance(category_ids, list) or len(category_ids) == 0:
                            return None, "category_ids must be a non-empty list"
                        valid_categories_ids = list(
                            db.session.scalars( #scalars() sẽ trả về một generator gồm các giá trị cột duy nhất
                                db.select(Category.id).where(
                                    Category.id.in_(category_ids),
                                    Category.deleted_at.is_(None)
                                    )
                                )
                            )
                        if not valid_categories_ids or len(valid_categories_ids) == 0:
                            return None, "No valid categories found for the provided IDs."
                        
                        current_categories_ids = list(
                            db.session.scalars( #scalars() sẽ trả về một generator gồm các giá trị cột duy nhất
                                db.select(ProductCategory.category_id).where(
                                    ProductCategory.product_id == product_id
                                    )
                                )
                            )
                        
                        to_add = set(valid_categories_ids) - set(current_categories_ids) #phần tử có trong valid_categories_ids nhưng không có trong current_categories_ids
                        to_remove = set(current_categories_ids) - set(valid_categories_ids)
                        
                        
                        
                        # Xóa các liên kết không còn
                        if to_remove:
                            db.session.query(ProductCategory).filter(
                                ProductCategory.product_id == product_id,
                                ProductCategory.category_id.in_(to_remove)
                            ).delete(synchronize_session=False)

                        # Thêm các liên kết mới
                        if to_add:
                            db.session.bulk_insert_mappings(
                                ProductCategory,
                                [{'product_id': product_id, 'category_id': category_id} for category_id in to_add]
                            )

                        updated_fields.append('category_ids')
                
                    else : 
                        setattr(product, field, product_data[field])
                        updated_fields.append(field)
                        
            db.session.commit()
            response_data = product.to_dict()
            response_data['updatedFields'] = updated_fields
            return response_data, None
                        
                        
        except Exception as e:
                db.session.rollback()
                return None, str(e)                
            
          
    @staticmethod              
    def delete_product(ids: list):
        try: 
            products= Product.query.filter(Product.id.in_(ids), Product.deleted_at.is_(None)).all()
            if not products : 
                return None, "No products found to delete"
            
            deleted_products = []
            
            product_ids = [product.id for product in products]
            Product.query.filter(Product.id.in_(product_ids), Product.deleted_at.is_(None)).update(
                {Product.deleted_at: datetime.now(timezone.utc)}, synchronize_session=False
            )
            
            db.session.query(ProductCategory).filter(ProductCategory.product_id.in_(product_ids)).delete(synchronize_session=False)
            
            variant_ids = list(
                db.session.scalars( #scalars() sẽ trả về một generator gồm các giá trị cột duy nhất
                    db.select(ProductVariants.id).where(
                        ProductVariants.product_id.in_(product_ids),
                        ProductVariants.deleted_at.is_(None)
                       )
                    )
                )
            if variant_ids and len(variant_ids) > 0 :
                ProductVariantsService.delete_variants(variant_ids)

            deleted_products = [{'id': p.id} for p in products]

            db.session.commit()
            response_data = {
                'deleted_products': deleted_products
            }
            return response_data, None
        except Exception as e : 
            db.session.rollback()
            return None, str(e)                
            
            
            
            