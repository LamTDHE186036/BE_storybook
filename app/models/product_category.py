from datetime import datetime, timezone
from app.extension import db

class ProductCategory(db.Model):
    __tablename__ = 'product_category'

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'category_id': self.category_id,
        }
