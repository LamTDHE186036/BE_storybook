from flask import Blueprint, request, jsonify
from app.controllers.order_items_controller import OrderItemsController

order_items_bp = Blueprint('order_items', __name__)

@order_items_bp.route('/order_items', methods=['GET'])
def get_order_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    filters = {
        'id': request.args.get('id', type=int),
        'order_id': request.args.get('order_id', type=int),
        'product_variant_id': request.args.get('product_variant_id', type=int),
    }
    
    return OrderItemsController.get_order_items(page, per_page, filters)



