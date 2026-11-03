from datetime import datetime, timezone
from models import db

class Consultation(db.Model):
    """
    Model for booking Free Online & In-Store Consultations with Professional Doctors.
    """
    __tablename__ = 'consultation'

    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    age = db.Column(db.String(10), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    health_concern = db.Column(db.Text, nullable=False)
    consultation_mode = db.Column(db.String(50), default='WhatsApp Video/Audio') # WhatsApp, Phone, In-Person
    preferred_date = db.Column(db.String(50), nullable=True) # e.g. '2026-09-19' or 'Today'
    preferred_time = db.Column(db.String(80), default='Morning (10:00 AM - 01:00 PM)')
    status = db.Column(db.String(30), default='pending', index=True) # pending, confirmed, completed, cancelled
    doctor_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_name': self.patient_name,
            'phone': self.phone,
            'address': self.address,
            'age': self.age,
            'gender': self.gender,
            'health_concern': self.health_concern,
            'consultation_mode': self.consultation_mode,
            'preferred_date': self.preferred_date,
            'preferred_time': self.preferred_time,
            'status': self.status,
            'doctor_notes': self.doctor_notes,
            'created_at': self.created_at.strftime('%b %d, %Y %I:%M %p') if self.created_at else ''
        }
