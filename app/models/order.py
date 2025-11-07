from app.extension import db
from datetime import datetime, timezone
import json

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    price_before_discount = db.Column(db.Float, nullable=False)
    discount_code = db.Column(db.String(50), db.ForeignKey('discount.code'), nullable=True)
    total_price = db.Column(db.Float, nullable=False)    
    items = db.Column(db.Text, nullable=False)  # JSON string of items
    status = db.Column(db.String(50), nullable=False, default='pending')
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='unpaid')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        items_data = json.loads(self.items)
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'shipping_address': self.shipping_address,
            "price_before_discount": self.price_before_discount,
            'discount_code': self.discount_code,
            'total_price': self.total_price,
            'items': items_data,
            'status': self.status,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }
    
    



