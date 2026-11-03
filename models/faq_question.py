from datetime import datetime, timezone
from models import db

class FaqQuestion(db.Model):
    """
    Model for questions submitted by visitors on the FAQ page.
    Admins can view and respond to these questions from the admin portal.
    """
    __tablename__ = 'faq_question'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(120), default='General Question')
    question = db.Column(db.Text, nullable=False)
    admin_response = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='pending', index=True) # 'pending', 'answered'
    is_public = db.Column(db.Boolean, default=True, index=True)
    responded_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'category': self.category,
            'question': self.question,
            'admin_response': self.admin_response,
            'status': self.status,
            'is_public': self.is_public,
            'responded_at': self.responded_at.strftime('%b %d, %Y %I:%M %p') if self.responded_at else '',
            'created_at': self.created_at.strftime('%b %d, %Y %I:%M %p') if self.created_at else ''
        }
