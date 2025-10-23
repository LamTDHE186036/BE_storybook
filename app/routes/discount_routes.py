from flask import Blueprint, request, jsonify
from app.controllers.discount_controller import DiscountController

discount_bp = Blueprint('discount', __name__)


@discount_bp.route('/discounts', methods=['GET'])
def get_discount():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    filters = {
        'code': request.args.get('code', type=str),
        'id': request.args.get('id', type=int)
    }
    
    return DiscountController.get_discount(page, page_size, filters)


@discount_bp.route('/admin/discounts', methods=['POST'])
def create_discount():
    data = request.get_json()
    return DiscountController.create_discount(data)


@discount_bp.route('/admin/discounts', methods=['PATCH'])
def update_discount():
    data = request.get_json()
    return DiscountController.update_discount(data) 

@discount_bp.route('/admin/discounts', methods=['DELETE'])
def delete_discount():
    request_data = request.get_json()
    return DiscountController.delete_discount(request_data)

