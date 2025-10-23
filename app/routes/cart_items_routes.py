from flask import Blueprint, request, jsonify
from app.controllers.cart_items_controller import CartItemsController


cart_itenms_bp = Blueprint('cart_items', __name__)

@cart_itenms_bp.route('/cart_items', methods=['GET'])
def get_cart_items():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    filters = {
        'id'   : request.args.get('id', type=int),
        'cart_id' : request.args.get('cart_id', type=int),
        'product_variant_id' : request.args.get('product_variant_id', type=int)
    }
    return CartItemsController.get_cart_items(page, page_size, filters)

@cart_itenms_bp.route('/admin/cart_items', methods=['POST'])
def create_cart_items():
    request_data = request.get_json()
    return CartItemsController.create_cart_items(request_data)

@cart_itenms_bp.route('/admin/cart_items', methods=['PATCH'])
def update_cart_items():
    request_data = request.get_json()
    return CartItemsController.update_cart_items(request_data)

@cart_itenms_bp.route('/admin/cart_items', methods=['DELETE'])
def delete_cart_items():
    request_data = request.get_json()
    return CartItemsController.delete_cart_items(request_data)
