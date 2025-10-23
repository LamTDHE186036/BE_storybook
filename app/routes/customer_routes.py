from flask import Blueprint, render_template, request, jsonify
from app.controllers.customer_controller import CustomerController

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customers', methods=['GET'])
def get_customers():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    filters = {
        'id'   : request.args.get('id', type=int)
    }
    return CustomerController.get_customers(page, page_size, filters)

@customer_bp.route('/admin/customers', methods=['POST'])
def create_customer():
    request_data = request.get_json()
    return CustomerController.create_customer(request_data)

@customer_bp.route('/admin/customers', methods=['PATCH'])
def update_customer():
    request_data = request.get_json()
    return CustomerController.update_customer(request_data)
