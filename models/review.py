from datetime import datetime, timezone
from models import db

class Review(db.Model):
    """
    Customer Review model for storing customer feedback and ratings.
    """
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    comment = db.Column(db.Text, nullable=False)
    service_tag = db.Column(db.String(100), default='General Visit') # German Dilutions, Doctor Consultation, Customer Service, etc.
    reviewer_title = db.Column(db.String(100), default='Verified Customer') # Local Resident, Malleswaram Guide, etc.
    location = db.Column(db.String(100), default='Malleswaram, Bengaluru')
    is_approved = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'author_name': self.author_name,
            'rating': self.rating,
            'comment': self.comment,
            'service_tag': self.service_tag,
            'reviewer_title': self.reviewer_title,
            'location': self.location,
            'is_approved': self.is_approved,
            'created_at': self.created_at.strftime('%b %d, %Y') if self.created_at else ''
        }
