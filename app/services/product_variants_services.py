from app.models.product_variants import ProductVariants
from app.models.product import Product
from app.extension import db
from math import ceil
import json
from datetime import datetime, timezone


class ProductVariantsService :
    
    @staticmethod
    def get_product_variants(page: int, page_size: int, filters: dict=None): 
        try : 
            if page < 1 or page > 500 : 
                page = 1
            if page_size < 1 or page_size > 100 : 
                page_size = 10  
            
            query = ProductVariants.query.filter(ProductVariants.deleted_at.is_(None))
            
            if filters : 
                if filters.get('name') is not None : 
                    query = query.filter(ProductVariants.name.ilike(f'%{filters["name"]}%'))
                    
                if filters.get('slug') is not None : 
                    query = query.filter(ProductVariants.slug == filters['slug'])
                    
                if filters.get('product_id') is not None : 
                    query = query.filter(ProductVariants.product_id == filters['product_id'])
                
                if filters.get('min_price') is not None or filters.get('max_price') is not None :    
                    min_price = filters.get('min_price')
                    max_price = filters.get('max_price')
                    if min_price is not None and max_price is not None:
                        query = query.filter(ProductVariants.price.between(min_price, max_price))
                        
                    elif min_price is not None and max_price is None:
                        query = query.filter(ProductVariants.price >= min_price)
                        
                    elif min_price is None and max_price is not None:
                        query = query.filter(ProductVariants.price <= max_price)
                        
                
                    
            product_variants = query.paginate(
                                        page=page,
                                        per_page=page_size, 
                                        error_out=False
                                        )
            
            items = [item.to_dict() for item in product_variants.items]
            
            response_data = {
                'items': items,
                'pagination': {
                    'currentPage': page,
                    'pageSize': page_size,
                    'totalPages': ceil(product_variants.total / page_size),
                    'totalItems': product_variants.total
                }
            }
            
            
            
            return response_data, None
                   
        except Exception as e :
            return None, str(e)
        
    @staticmethod
    def get_product_by_variant(variant_id: int, page: int, page_size: int):
        try:
            if page < 1 or page > 500:
                page = 1
            if page_size < 1 or page_size > 100:
                page_size = 10  
            
            variant = db.session.get(ProductVariants, variant_id)
            if not variant or variant.deleted_at is not None:
                return None, "Product variant not found"
            
            product_id = variant.product_id
            
            query = db.session.query(Product.id, Product.name, Product.slug).filter(
                Product.id == product_id,   
                Product.deleted_at.is_(None)
            )
                        
            products = query.paginate(
                                        page=page,
                                        per_page=page_size, 
                                        error_out=False
                                        )
            
            items = [{'id': item.id, 'name': item.name, 'slug': item.slug} for item in products.items]
            
            response_data = {
                "variant": variant.name,
                'items': items,
                'pagination': {
                    'currentPage': page,
                    'pageSize': page_size,
                    'totalPages': ceil(products.total / page_size),
                    'totalItems': products.total
                }
            }
            
            return response_data, None
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def create_product_variant(product_variants_data: dict): 
        try: 
            product_id = product_variants_data.get('product_id')
            if not product_id : 
                return None, "Product ID is required."
            
            valid_product = db.session.get(Product, product_id)
            if not valid_product or valid_product.deleted_at is not None:
                return None, "No valid product found for the provided ID."
            
            new_product_variants = ProductVariants(
                name = product_variants_data.get('name'),
                product_id = product_variants_data.get('product_id'),
                slug = product_variants_data.get('slug'),
                price = product_variants_data.get('price'),
                quantity = product_variants_data.get('quantity', 0),
                status = product_variants_data.get('status', 'active'),
                quantity_ordered = product_variants_data.get('quantity_ordered', 0),
                image_url = product_variants_data.get('image_url')
            )
            
            db.session.add(new_product_variants)
            db.session.commit()
            return new_product_variants.to_dict(), None
            
            
            
        except Exception as e :
            return None, str(e)
        
    @staticmethod
    def update_product_variant(variant_id: int, update_data: dict):
        try: 
            variant = db.session.get(ProductVariants, variant_id)
            if not variant or variant.deleted_at is not None:
                return None, "Product variant not found"
            
            allowed_fields = [ 'product_id', 'name', 'slug', 'price','status', 'quantity', 'quantity_ordered', 'image_url']
            updated_fields = []
            for field in allowed_fields: 
                if field in update_data: 
                    if field == 'product_id':
                        new_product_id = update_data.get('product_id')
                        valid_product = db.session.get(Product, new_product_id)
                        if not valid_product or valid_product.deleted_at is not None:
                            return None, "No valid product found for the provided ID."
                        setattr(variant, field, new_product_id)
                        updated_fields.append(field)
                    elif field == 'quantity':
                        new_quantity = update_data.get('quantity')
                        if new_quantity <= 0 : 
                            variant.status = 'out_of_stock'
                        else : 
                            variant.status = update_data.get('status', 'active')
                            
                        setattr(variant, field, new_quantity)
                        updated_fields.append(field)
                    else:
                        setattr(variant, field, update_data.get(field))
                        updated_fields.append(field)
                    
            db.session.commit()
            response_data = variant.to_dict()
            response_data['updated_fields'] = updated_fields
            return response_data, None
        except Exception as e :
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_status(product_variant: ProductVariants):
        if product_variant.quantity <= 0:
            return 'out_of_stock'
        elif product_variant.deleted_at is not None or product_variant.status == 'inactive':
            return 'inactive'
        else:
            return 'active'
        
        
    
    @staticmethod
    def delete_variants(variant_ids: list):
        try: 
            variants = ProductVariants.query.filter(ProductVariants.id.in_(variant_ids), ProductVariants.deleted_at.is_(None)).all()
            if not variants or len(variants) == 0:
                return None, "No valid product variants found for the provided IDs."
            
            deleted_variants =[]
            ProductVariants.query.filter(ProductVariants.id.in_(variant_ids), ProductVariants.deleted_at.is_(None)).update(
                {ProductVariants.deleted_at: datetime.now(timezone.utc)},
                synchronize_session=False
            )
            # db.session.flush()  # đẩy thay đổi lên session để các object reflect deleted_at
            db.session.commit()
            
            for variant in variants:
                variant.status = 'inactive'
                deleted_variants.append({'id': variant.id})

            
            
            db.session.commit()
            response_data = {
                'deleted_variants': deleted_variants
            }   
            return response_data, None
        except Exception as e :
            db.session.rollback()
            return None, str(e) 
                
            
        