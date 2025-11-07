from app.controllers.order_controller import OrderController
from flask import Blueprint, request, jsonify

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['GET'])
def get_orders():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    filters = {
        'id': request.args.get('id', type=int),
        'customer_id': request.args.get('customer_id', type=int)
    }
    
    return OrderController.get_orders(page, page_size, filters)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    return OrderController.create_order(data)

@order_bp.route('admin/orders', methods=['PATCH'])
def update_order():
    data = request.get_json()
    return OrderController.update_order(data)

@order_bp.route('/orders', methods=['PATCH'])
def update_order_shipping_address():
    data = request.get_json()
    return OrderController.update_order_shipping_address(data)

@order_bp.route('/orders', methods=['DELETE'])
def delete_order():
    request_data = request.get_json()
    return OrderController.delete_order(request_data)
