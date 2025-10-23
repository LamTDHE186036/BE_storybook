from flask import Flask, Blueprint, request
from app.controllers.product_variants_controller import ProductVariantsController

product_variants_bp = Blueprint('product_variants', __name__)


@product_variants_bp.route('/product_variants', methods=['GET'])
def get_product_variants():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    filters = {
        'name' : request.args.get('name', type=str), 
        'slug' : request.args.get('slug', type=str),
        'product_id' : request.args.get('product_id', type=int),
        'min_price' : request.args.get('min_price', type=float),
        'max_price' : request.args.get('max_price', type=float),
    }
    
    return ProductVariantsController.get_product_variants(page, page_size, filters)

@product_variants_bp.route('/product_variants/<int:variant_id>', methods=['GET'])
def get_product_by_variant(variant_id):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    return ProductVariantsController.get_product_by_variant(variant_id, page, page_size)
    


@product_variants_bp.route('/admin/product_variants', methods=['POST'])
def create_product_variant():
    request_data = request.get_json()
    return ProductVariantsController.create_product_variant(request_data)

@product_variants_bp.route('/admin/product_variants/<int:variant_id>', methods=['PATCH'])
def update_product_variant(variant_id):
    request_data = request.get_json()
    return ProductVariantsController.update_product_variant(variant_id, request_data)
    
@product_variants_bp.route('/admin/product_variants', methods=['DELETE'])
def delete_variants(): 
    request_data = request.get_json()
    return ProductVariantsController.delete_variants(request_data)
