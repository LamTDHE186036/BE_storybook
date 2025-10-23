from functools import wraps
from flask import request, jsonify, g
from app.utils.jwt_ultis import JWTUtils
from app.extension import db
from app.utils.response import api_response
import os
import json
import jwt
from app.models.users import User

ADMIN_ROUTES = [
    "/api/admin",
    "/auth/admin",
]

def is_admin_route(path: str) -> bool:
    for admin_route in ADMIN_ROUTES:
        if path.startswith(admin_route):
            return True
    return False

    
def verify_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin_route(request.path):
            return api_response(
                success=False,
                message="Access denied! Only admin can access this route.",
                status_code=403
            )
        try:
            #  Lấy token
            token , error = JWTUtils.get_token_from_request()
            if error:
                return api_response(
                    success=False,
                    message=error,
                    status_code=401
                )
            # Giải mã token
            payload , error = JWTUtils.decode_access_token(token)
            if error:
                return api_response(
                    success=False,
                    message=error,
                    status_code=401
                )
            user = db.session.query(User).filter(
                User.id == payload['user_id'],
                User.deleted_at.is_(None)
            ).first()
            if not user:
                return api_response(
                    success=False,
                    message='User not found or has been deleted',
                    status_code=401
            )
            g.current_user = {
                'id': user.id,
                'user_name': user.user_name,
                'role': user.role,
                'payload': payload
            }    
        except Exception as e:
            print(e)
            return api_response(
                success=False,
                message="Token is missing!",
                status_code=401
            )
        return f(*args, **kwargs)
    return decorated_function




            
            
            
            
        
        
        

            
        