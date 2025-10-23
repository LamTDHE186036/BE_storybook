from app.extension import db
from datetime import timezone, datetime

class Cart(db.Model):
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True )
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='active')
    created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc), onupdate= lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, default= None,  nullable=True)
    
    def to_dict(self) : 
        
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            "status" : self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }