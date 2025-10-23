from app.extension import db
from datetime import datetime, timezone

class Discount(db.Model):
    
    __tablename__ = 'discount'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_type = db.Column(db.String(20), nullable=False)  # e.g., 'percentage', 'fixed'
    discount_value = db.Column(db.Float, nullable=False)
    min_order_value = db.Column(db.Float, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    usage_limit = db.Column(db.Integer, nullable=True)  # Total number of times the discount can be used
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'discount_type': self.discount_type,
            'discount_value': self.discount_value,
            'min_order_value': self.min_order_value,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'usage_limit': self.usage_limit,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat()  if self.deleted_at else None
        }
        
        
