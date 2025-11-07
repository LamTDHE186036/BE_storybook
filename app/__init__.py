# tạo __init__.py là trung tâm khởi tạo app, quản lý cấu hình, extensions, và kết nối tất cả module lại.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from .routes import register_routes
from dotenv import load_dotenv
import logging
from .configs.config import Config
from .extension import db, mail, migrate
from app.utils.middlewares import global_verify_token
from app.utils.scheduler import OrderNotificationScheduler 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Load biến môi trường từ file .env
load_dotenv()

def create_app() : 
    app = Flask(__name__)
    app.config.from_object(Config)
    try : 
        db.init_app(app)
        migrate.init_app(app,db)
        with app.app_context():
            db.engine.connect()
        logger.info("Database connection successful")
    except Exception as e:
        print(e)
        logger.error(f"Database connection failed: {e}")
        
    app.before_request(global_verify_token)
    register_routes(app)
    OrderNotificationScheduler.init_scheduler(app)
        
    return app 