from app.extension import db
from app.models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.jwt_ultis import JWTUtils
from datetime import datetime, timezone

class UsersServices:
    @staticmethod
    def register(response_data):
        try:
            if not response_data : 
                return None, 'No data provided'
            
            role = response_data.get('role')
            user_name = response_data.get('user_name')
            password = response_data.get('password')
            
            if not user_name or not password or not role:
                return None, 'Missing required fields'
            
            existing_user = User.query.filter_by(user_name=user_name, deleted_at=None).first()
            if existing_user:
                return None, 'User with this email already exists'
            
            password_hash = generate_password_hash(password)
            
            new_user = User(
                role=role,
                user_name=user_name, 
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
                role=user.role
                )
            
            return token, None
        
        except Exception as e:
            return None, str(e)
        
            
                                                                            