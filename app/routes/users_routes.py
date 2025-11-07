from flask import Blueprint, request, jsonify
from app.controllers.users_controller import UsersController

users_bp = Blueprint('users', __name__)


@users_bp.route('/admin/register', methods=['POST'])
def register():
    response_data = request.get_json()
    return UsersController.register(response_data)

@users_bp.route('/login', methods=['POST'])
def login():
    response_data = request.get_json()
    return UsersController.login(response_data)

@users_bp.route('/admin/users', methods=['GET'])
def get_users():
    return UsersController.get_users()

@users_bp.route('/admin/update-users', methods=['PATCH'])
def update_user():
    response_data = request.get_json()
    return UsersController.update_user(response_data)

@users_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return UsersController.delete_user(user_id)

@users_bp.route('/admin/users', methods=['DELETE'])
def delete_multiple_users():
    response_data = request.get_json()
    return UsersController.delete_multiple_users(response_data)


@users_bp.route('/forgot-password', methods=['POST'])
def forgot_password() : 
    response_data = request.get_json()
    return UsersController.forgot_password(response_data)

@users_bp.route('/confirm-otp', methods=['POST'])
def confirm_otp() : 
    response_data = request.get_json()
    return UsersController.confirm_otp(response_data)

@users_bp.route('/admin/reset-password', methods=['POST'])
def reset_password() :
    response_data = request.get_json()
    return UsersController.reset_password(response_data)
