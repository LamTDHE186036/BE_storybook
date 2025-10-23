from flask import Blueprint
from app.controllers.post_category_controller import PostCategoryController
from flask import request

post_category_bp = Blueprint('post_category', __name__)

@post_category_bp.route('/post_categories', methods=['GET'])
def get_post_categories():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    filters = {
        'id': request.args.get('id'),
        'slug': request.args.get('slug')
    }
    
    return PostCategoryController.get_post_categories(page, page_size, filters)

@post_category_bp.route('/post_categories/<string:slug>/posts', methods=['GET'])
def get_post_by_category(slug):
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    
    return PostCategoryController.get_posts_by_category(page, page_size, slug)

@post_category_bp.route('/admin/post_categories', methods=['POST'])
def create_post_category():
    request_data = request.get_json()
    return PostCategoryController.create_post_category(request_data)


@post_category_bp.route('/admin/post_categories', methods=['PATCH'])
def update_post_category():
    request_data = request.get_json()
    return PostCategoryController.update_post_category(request_data) 


@post_category_bp.route('/admin/post_categories', methods=['DELETE'])
def delete_post_category():
    request_data = request.get_json()
    return PostCategoryController.delete_post_category(request_data)  


