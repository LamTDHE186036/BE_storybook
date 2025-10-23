from app.extension import db
from datetime import timezone, datetime

class OrderItems(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True )
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc), onupdate= lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, default= None,  nullable=True)
    
    def to_dict(self) : 
        
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_variant_id': self.product_variant_id,
            'quantity': self.quantity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }
    
    