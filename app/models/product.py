from flask import Flask, jsonify, request, json
from app.extension import db
from datetime import timezone, datetime

class Product(db.Model): 
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(255), nullable = False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc), onupdate= lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, default= None,  nullable=True)
    
    def to_dict(self) : 
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'author': self.author,
            'description': self.description,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }