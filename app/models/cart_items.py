from app.extension import db   
from datetime import timezone, datetime

class CartItems(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True )
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_variant_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc), onupdate= lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, default= None,  nullable=True)
    
    def to_dict(self) : 
        
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product_variant_id': self.product_variant_id,
            'quantity': self.quantity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }
