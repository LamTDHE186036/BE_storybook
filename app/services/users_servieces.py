from app.extension import db, mail 
from app.models.users import User
from app.models.otp import OTP
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.jwt_ultis import JWTUtils
from app.services.otp_mail_services import EmailService
from datetime import datetime, timezone
from flask import g


class UsersServices:
    @staticmethod
    def register(response_data):
        try:
            if not response_data : 
                return None, 'No data provided'
            
            current_user = g.get("current_user")
            if not current_user or current_user.get("role") != "manager":
                return None, 'Not manager. Permission denied'
            
            
            role = response_data.get('role')
            user_name = response_data.get('user_name')
            email = response_data.get("email")
            password = response_data.get('password')
            
            
            if not user_name or not password or not role:
                return None, 'Missing required fields'
            
            existing_user = User.query.filter_by(user_name=user_name, deleted_at=None).first()
            if existing_user:
                return None, 'User already exists'
            
            password_hash = generate_password_hash(password)
            
            new_user = User(
                role=role,
                user_name=user_name, 
                email = email,
                password_hash=password_hash
                )
            db.session.add(new_user)
            db.session.commit()
            
            return new_user.to_dict(), None
        
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def login(response_data):
        try : 
            if not response_data : 
                return None, 'No data provided'
            
            user_name = response_data.get('user_name')
            password = response_data.get('password')

            
            if not user_name or not password :
                return None, 'Missing required fields'
            
            user = db.session.query(User).filter(
                User.user_name == user_name,
                User.deleted_at.is_(None)
            ).first()
            
            if not user or not check_password_hash(user.password_hash, password):
                return None, 'Invalid username or password'
            
            token = JWTUtils.encode_access_token(
                user_id = user.id,
                user_name=user.user_name, 
                email = user.email,
                role=user.role
                )
            
            return token, None
        
        except Exception as e:
            return None, str(e)
            
            
            
        
    
    @staticmethod
    def get_users():
        try : 
            current_user = g.get("current_user")
            if not current_user or current_user.get("role") != "manager":
                return None, 'Not manager. Permission denied'
            
            users = User.query.filter_by(deleted_at=None).all()
            users_list = [user.to_dict() for user in users]
            
            return users_list, None
        
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def update_user(response_data):
        try:
            if not response_data : 
                return None, 'No data provided'
            
            current_user = g.get("current_user")
            if not current_user : 
                return None, 'Authentication required'
            
            user_id = response_data.get('id')
            current_password = response_data.get('current_password')
            new_email = response_data.get('new_email')
            new_password = response_data.get('new_password')
            
            if not user_id :
                return None, 'User ID is required'
             
            if not current_password : 
                return None, 'Current password is required'
            
            if current_user.get('id') != user_id :
                return None, 'You can only update your own account'
            
            user = db.session.query(User).filter(
                User.id == user_id,
                User.deleted_at.is_(None)
            ).first()
            
            if not user :
                return None, 'User not found'
            
            if not check_password_hash(user.password_hash, current_password):
                return None, 'Current password is incorrect'
            
            if not new_email and not new_password :
                return None, 'No new data provided for update'
            
            if new_email :
                existing_email = User.query.filter(
                    User.email == new_email,
                    User.id != user_id,
                    User.deleted_at.is_(None)
                ).first()
                if existing_email :
                    return None, 'Email already in use'
                user.email = new_email
                
            if new_password :
                if check_password_hash(user.password_hash, new_password):
                    return None, 'New password must be different from the current password'
                user.password_hash = generate_password_hash(new_password)
                
            user.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            
            return user.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def delete_user(user_id):
        try:
            if not user_id :
                return None, 'User ID is required'
            
            current_user = g.get("current_user")
            if not current_user : 
                return None, 'Authentication required'
            
            current_role = current_user.get("role")
            current_id = current_user.get("id")
            
            # Chỉ được xóa tài khoản của chính mình
            if current_id != user_id : 
                return None, "You can only delete your own account"
            
            user = db.session.query(User).filter(
                User.id == user_id,
                User.deleted_at.is_(None)
            ).first()
            
            if not user :
                return None, 'User not found'
            
            # Nếu là manager, kiểm tra còn manager khác không
            if user.role == "manager":
                manager_count = db.session.query(User).filter(
                    User.role == "manager",
                    User.deleted_at.is_(None),
                    User.id != user_id
                ).count()
                
                if manager_count == 0 :
                    return None, 'Cannot delete the last manager account. System must have at least one manager.'
            
            # Soft delete
            user.deleted_at = datetime.now(timezone.utc)
            user.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            
            return {
                'id': user.id,
                'user_name': user.user_name,
                'role': user.role
            }, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
                    
                    
                    
    @staticmethod
    def delete_multiple_users(response_data):
        """Manager có thể xóa nhiều người, nhưng không được xóa chính mình"""
        try:
            if not response_data or 'ids' not in response_data:
                return None, 'No data provided'
            
            user_ids = response_data.get("ids")
            if not user_ids or not isinstance(user_ids, list):
                return None, 'A list of user IDs is required'

            current_user = g.get("current_user")
            if not current_user:
                return None, 'Authentication required'

            current_role = current_user.get("role")
            current_id = current_user.get("id")

            if current_role != "manager":
                return None, 'Permission denied: only manager can delete multiple users'

            if current_id in user_ids:
                user_ids = [uid for uid in user_ids if uid != current_id]
                
                if not user_ids:
                    return None, 'You cannot delete your own account'
                
            users_to_delete = db.session.query(User).filter(
                User.id.in_(user_ids),
                User.deleted_at.is_(None)
            ).all()
            
            if not users_to_delete:
                return None, 'No valid users found to delete'
            
            db.session.query(User).filter(
            User.id.in_([user.id for user in users_to_delete]),
            User.deleted_at.is_(None)
            ).update(
                {
                    User.deleted_at: datetime.now(timezone.utc),
                    User.updated_at: datetime.now(timezone.utc)
                },
                synchronize_session=False
                    )
            
            db.session.commit()
            
            deleted_users_info = [
                {
                    'id': user.id,
                    'user_name': user.user_name,
                    'role': user.role
                } for user in users_to_delete
            ]
            
            return deleted_users_info, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
            

            
    @staticmethod
    def forgot_password(response_data):

        try:
            if not response_data : 
                return None, 'No data provided'
            
            email = response_data.get('email')
            if not email :
                return None, 'Email is required'
            
            user = db.session.query(User).filter(
                User.email == email,
                User.deleted_at.is_(None)
            ).first()
            
            if not user :
                return None, 'User with this email not found'
            
            
            success, error = EmailService.send_otp_email(email)
            if not success : 
                return None, f'Failed to send OTP email: {error}'
            
            return {
                'email': email,
                'message': 'OTP has been sent to your email'
            }, None
            
        except Exception as e:
            print(e)
            return None, str(e)
        
        
        
    @staticmethod
    def confirm_otp(response_data):
        try:
            if not response_data : 
                return None, 'No data provided'
            
            email = response_data.get('email')
            otp_code = response_data.get('otp_code')
            
            if not email or not otp_code :
                return None, 'Missing required fields'
            
            user = db.session.query(User).filter(
                User.email == email,
                User.deleted_at.is_(None)
            ).first()
        
            if not user :
                return None, 'User with this email not found'
            
            is_valid, error = EmailService.verify_otp(email, otp_code)
            
            if not is_valid : 
                return None, f'OTP verification failed: {error}'
            
            token = JWTUtils.encode_access_token(
                user_id=user.id,
                email=user.email,
                user_name=user.user_name, 
                role=user.role
            )
            
            return {
                'message': 'OTP verified successfully',
                'otp_token': token
            }, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        


    
    @staticmethod
    def reset_password(response_data):
        try: 
            if not response_data:
                return None, 'No data provided'
            
            new_password = response_data.get('new_password')
            
            if not new_password:
                return None, 'Missing new_password field'
            
            # Validate password length
            if len(new_password) < 6:
                return None, 'Password must be at least 6 characters'
            
            current_user = g.get("current_user")
            
            if not current_user:
                return None, 'Authentication required'
            
            current_id = current_user.get("id")
            user = db.session.query(User).filter(
                User.id == current_id,
                User.deleted_at.is_(None)
            ).first()
            if not user:
                return None, 'User not found'
            
            db.session.query(User).filter(
                User.id == current_id,
                User.deleted_at.is_(None)
            ).update(
                {
                    User.password_hash: generate_password_hash(new_password),
                    User.updated_at: datetime.now(timezone.utc)
                },
                synchronize_session=False
            )
            
            db.session.commit()
            return {
                'id': user.id,
                'user_name': user.user_name,
                'email': user.email,
                'role': user.role,
                'message': 'Password has been reset successfully'
            }, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
            
            
            