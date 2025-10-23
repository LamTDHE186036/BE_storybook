from app.extension import db
from datetime import timezone, datetime


class Category(db.Model): 
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(255), nullable = False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc), onupdate= lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, default= None,  nullable=True)
    # askzdjsadf
    # kasjzhds
    def to_dict(self) : 
        
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }
        
        
        
    
    