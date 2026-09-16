from datetime import datetime
from models import db

class Product(db.Model):
    """
    Product model for physical store catalogue browsing and availability enquiries.
    NOTE: E-commerce actions (cart, checkout, payment, delivery) are strictly prohibited.
    """
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    brand = db.Column(db.String(100), nullable=True)
    pack_size = db.Column(db.String(80), nullable=True) # e.g., 'Strip of 10 Tablets', '100 ml Bottle'
    dosage_form = db.Column(db.String(50), nullable=True) # Tablet, Syrup, Ointment, Device, etc.
    requires_prescription = db.Column(db.Boolean, default=False)
    
    # Availability status values: 'Available', 'In Stock', 'Limited Stock', 'Out of Stock', 'Availability Varies'
    availability = db.Column(db.String(50), nullable=False, default='Availability Varies')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else '',
            'category_slug': self.category.slug if self.category else '',
            'description': self.description,
            'brand': self.brand,
            'pack_size': self.pack_size,
            'dosage_form': self.dosage_form,
            'requires_prescription': self.requires_prescription,
            'availability': self.availability,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else ''
        }
