from flask import request, g
from app.utils.jwt_ultis import JWTUtils
from app.extension import db
from app.utils.response import api_response
from app.models.users import User

ADMIN_ROUTES = [
    "/api/admin",
    "/auth/admin",
]

def is_admin_route(path: str) -> bool:
    """Kiểm tra xem route hiện tại có phải là route admin không"""
    return any(path.startswith(r) for r in ADMIN_ROUTES)


def global_verify_token():
    """Middleware chạy trước mỗi request để kiểm tra token cho các route admin"""
     # print(f"Middleware chạy cho route: {request.path}")

    
    if not is_admin_route(request.path):
        # Nếu không phải route admin thì cho qua
        # print("Không phải admin route → bỏ qua kiểm tra token")
        return None
    
    try:
        # Lấy token từ header
        token, error = JWTUtils.get_token_from_request()
        if error:
            return api_response(
                success=False,
                message="Authorization token is missing",
                status_code=401
            )

        # Giải mã token
        payload, error = JWTUtils.decode_access_token(token)
        if error:
            return api_response(
                success=False,
                message=error,
                status_code=401
            )

        # Kiểm tra user tồn tại
        user = db.session.query(User).filter(
            User.id == payload["user_id"],
            User.deleted_at.is_(None)
        ).first()

        if not user:
            return api_response(
                success=False,
                message="User not found or deleted",
                status_code=404
            )

        # Lưu user vào context
        g.current_user = {
            "id": user.id,
            "user_name": user.user_name,
            "role": user.role,
            "email": user.email,
            "payload": payload
        }
        # print(" Là admin route → kiểm tra token.")
        return None

    except Exception as e:
        return api_response(
            success=False,
            message=f"Token validation error: {str(e)}",
            status_code=500
        )
