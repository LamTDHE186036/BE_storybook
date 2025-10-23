# tạo __init__.py là trung tâm khởi tạo app, quản lý cấu hình, extensions, và kết nối tất cả module lại.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from .routes import register_routes
from dotenv import load_dotenv
import logging
from .configs.config import Config
from .extension import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Load biến môi trường từ file .env
load_dotenv()

def create_app() : 
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    try : 
        db.init_app(app)
        with app.app_context():
            db.engine.connect()
        logger.info("Database connection successful")
        from app.utils.middlewares import verify_token
        @app.before_request
        def before_request_handler():
            return verify_token()
        register_routes(app)
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        
    return app 