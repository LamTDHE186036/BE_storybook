from datetime import datetime, timezone
from app.extension import db

class ProductVariants(db.Model):
    __tablename__ = 'product_variants'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.Float, default=0.0)
    quantity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='active')  # 'active', 'out_of_stock', 'inactive'
    quantity_ordered = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'name': self.name,
            'slug': self.slug,
            'price': self.price,
            'quantity': self.quantity,
            "status": self.status,
            'quantity_ordered': self.quantity_ordered,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            
        }