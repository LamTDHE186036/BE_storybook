from app.extension import db
from flask import Blueprint, request, jsonify
from app.controllers.product_controller import ProductController

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    filters = {
        'name' : request.args.get('name', type=str),
        'slug' : request.args.get('slug', type=str),
        'id'    : request.args.get('id', type=int)
    }
    return ProductController.get_products(page, page_size, filters)

@product_bp.route('/products/<int:product_id>/categories', methods=['GET'])
def get_category_by_product( product_id):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    return ProductController.get_category_by_product(page, page_size,product_id)

@product_bp.route('/admin/products', methods=['POST'])
def create_product():
    request_data = request.get_json()
    return ProductController.create_product(request_data)

@product_bp.route('/admin/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    request_data = request.get_json()
    return ProductController.update_product(product_id, request_data)

@product_bp.route('/admin/products', methods=['DELETE'])
def delete_product():
    request_data = request.get_json()
    return ProductController.delete_product(request_data)

