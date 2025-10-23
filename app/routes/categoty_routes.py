from flask import Flask, Blueprint, request
from app.controllers.category_controller import CategoryController

category_bp = Blueprint('category', __name__)


@category_bp.route('/categories', methods=['GET'])
def get_category():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    filters = {
        'name' : request.args.get('name', type=str), 
        'id' : request.args.get('id', type=int), 
        'slug' : request.args.get('slug', type=str)
    }
    
    include_children = request.args.get('include_children', 'false').lower() == 'true'
    
    return CategoryController.get_category(page, page_size, filters, include_children)
    

@category_bp.route('/admin/categories', methods=['POST'])
def create_category():
    request_data = request.get_json()
    return CategoryController.create_category(request_data)

@category_bp.route('/admin/categories/<int:category_id>', methods=['PATCH'])
def update_category(category_id: int):
    request_data = request.get_json()
    return CategoryController.update_category(category_id, request_data)

@category_bp.route('/admin/categories', methods=['DELETE'])
def delete_category():
    request_data = request.get_json()
    return CategoryController.delete_category(request_data)             