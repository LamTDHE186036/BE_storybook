from flask import Blueprint, render_template, request, jsonify
from .categoty_routes import category_bp
from .product_routes import product_bp
from .product_variants_routes import product_variants_bp
from .cart_routes import cart_bp
from .cart_items_routes import cart_itenms_bp
from .customer_routes import customer_bp
from .order_routes import order_bp
from .order_items_routes import order_items_bp
from .discount_routes import discount_bp
from .post_category_routes import post_category_bp
from .post_routes import post_bp
from .users_routes import users_bp

def register_routes(app) :
    app.register_blueprint(category_bp, url_prefix='/api')
    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(product_variants_bp, url_prefix='/api')
    app.register_blueprint(cart_bp, url_prefix='/api')
    app.register_blueprint(cart_itenms_bp, url_prefix='/api')
    app.register_blueprint(customer_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')
    app.register_blueprint(order_items_bp, url_prefix='/api')
    app.register_blueprint(discount_bp, url_prefix='/api')
    app.register_blueprint(post_category_bp, url_prefix='/api')
    app.register_blueprint(post_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/auth')
    