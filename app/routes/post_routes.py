from flask import Blueprint, request, jsonify
from app.controllers.post_controller import PostController  

post_bp = Blueprint('post', __name__)

@post_bp.route('/posts', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    filters = {
        'id': request.args.get('id'),
        'sllug': request.args.get('slug'),
        'name': request.args.get('name')
    }
    return PostController.get_posts(page, page_size, filters)


@post_bp.route('/admin/posts', methods=['POST'])
def create_post():
    response_data = request.get_json()
    return PostController.create_post(response_data)

@post_bp.route('/admin/posts', methods=['PATCH'])
def update_post():
    response_data = request.get_json()
    return PostController.update_post(response_data)


@post_bp.route('/admin/posts', methods=['DELETE'])
def delete_post():
    response_data = request.get_json()
    return PostController.delete_post(response_data)



    