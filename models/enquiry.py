from datetime import datetime
from models import db

class Enquiry(db.Model):
    """
    Customer enquiry model for store contact and product availability enquiries.
    """
    __tablename__ = 'enquiry'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    product_name = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default='unread') # unread, read, replied
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'message': self.message,
            'product_name': self.product_name,
            'status': self.status,
            'created_at': self.created_at.strftime('%b %d, %Y %I:%M %p') if self.created_at else ''
        }
