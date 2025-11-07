import os 
from datetime import datetime, timedelta, timezone
from flask import request 
import jwt
from dotenv import load_dotenv

load_dotenv()

class JWTUtils:
    @staticmethod
    def encode_access_token(user_id:int,user_name:str, role:str, email:str, **kwargs):
        
        secret_key = os.getenv("SECRET_KEY")
        issued_at = datetime.now(timezone.utc)
        expiration = issued_at + timedelta(seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600)))
        
        payload = {
            'user_id' : user_id,
            'sub': user_name,
            "role" : role,
            "email" : email,
            "iat" : int(issued_at.timestamp()),
            "exp" : int(expiration.timestamp())
            }
        
        payload.update(kwargs)
        
        token = jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
        
        return token
    
    @staticmethod
    def decode_access_token(token:str):
        try : 
            secret_key = os.getenv("SECRET_KEY")
            
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=['HS256']
            )
            
            return payload, None

        except jwt.ExpiredSignatureError:
            return None, 'Token has expired'
        
        except jwt.InvalidTokenError:
            return None, 'Invalid token'
        
        except Exception as e:
            return None, str(e)
   
    @staticmethod
    def get_token_from_request():
        auth_header = request.headers.get('Authorization')
        if not auth_header : 
            return None, 'Authorization header is missing'
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None, 'Invalid Authorization header format.'
        
        return parts[1], None
    
        
            
             
        
        
        
        
        
    
    
    
