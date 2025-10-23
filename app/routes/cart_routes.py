from flask import Blueprint, request, jsonify
from app.controllers.cart_controller import CartController

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    filters = {
        'id'   : request.args.get('id', type=int),
        'customer_id' : request.args.get('customer_id', type=int)
    }
    
    return CartController.get_cart(page, page_size, filters)



@cart_bp.route('/cart/<int:cart_id>', methods=['GET'])
def get_detail_cart(cart_id: int):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    return CartController.get_detail_cart(page, page_size, cart_id)


@cart_bp.route('/admin/cart', methods=['POST'])
def create_cart():
    request_data = request.get_json()
    return CartController.create_cart(request_data)


@cart_bp.route('/admin/cart', methods=['PATCH'])
def update_cart():
    request_data = request.get_json()
    return CartController.update_cart(request_data)

@cart_bp.route('/admin/cart', methods=['DELETE'])
def delete_cart():
    request_data = request.get_json()
    return CartController.delete_cart(request_data)





    