from flask import Blueprint, request, jsonify
from app.controllers.users_controller import UsersController
from app.utils.middlewares import register_required

users_bp = Blueprint('users', __name__)


@users_bp.route('/admin/register', methods=['POST'])
def register():
    response_data = request.get_json()
    return UsersController.register(response_data)

@users_bp.route('/login', methods=['POST'])
def login():
    response_data = request.get_json()
    return UsersController.login(response_data)
