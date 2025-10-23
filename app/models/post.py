from app.extension import db
from datetime import datetime, timezone


class Post(db.Model):
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    post_category_id = db.Column(db.Integer, db.ForeignKey('post_category.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    url_image = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_category_id': self.post_category_id,
            'name': self.name,
            'content': self.content,
            'url_image': self.url_image,
            'slug': self.slug,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }
        
        