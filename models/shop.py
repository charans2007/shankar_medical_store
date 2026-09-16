from datetime import datetime
from models import db

class Shop(db.Model):
    """
    Shop configuration table holding the medical store's central details.
    Allows live updates from the admin dashboard without altering source code.
    """
    __tablename__ = 'shop'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, default='Shankar Homoeo Stores')
    tagline = db.Column(db.String(255), nullable=True, default='Your Trusted Homoeopathic & Medical Store')
    owner_name = db.Column(db.String(100), nullable=True, default='J D Shankar')
    phone = db.Column(db.String(20), nullable=False, default='+91 98866 61239')
    whatsapp = db.Column(db.String(20), nullable=False, default='919886661239')
    doctor_phone = db.Column(db.String(20), nullable=True, default='+91 95357 17958')
    doctor_whatsapp = db.Column(db.String(20), nullable=True, default='919535717958')
    email = db.Column(db.String(120), nullable=True, default='shankarhomeostores@gmail.com')
    
    # Address details
    address = db.Column(db.String(300), nullable=False, default='Shankar homoeo stores, opp to Kids kingdom, 7th Cross, Sampige Rd, Malleshwaram, Bengaluru, Karnataka 560003')
    area = db.Column(db.String(100), nullable=True, default='Malleswaram')
    city = db.Column(db.String(100), nullable=True, default='Bengaluru')
    state = db.Column(db.String(100), nullable=True, default='Karnataka')
    pincode = db.Column(db.String(20), nullable=True, default='560003')
    landmark = db.Column(db.String(200), nullable=True, default='Opposite to Kids Kingdom, Diagonally Opposite YES Bank')
    
    # Geo & Maps
    google_maps_url = db.Column(db.Text, nullable=True, default='https://www.google.com/maps/dir/?api=1&destination=Shankar+homoeo+stores,+opp+to+Kids+kingdom,+7th+Cross,+Sampige+Rd,+Malleshwaram,+Bengaluru,+Karnataka+560003')
    google_maps_embed_url = db.Column(db.Text, nullable=True, default='https://maps.google.com/maps?q=Shankar+homoeo+stores,+opp+to+Kids+kingdom,+7th+Cross,+Sampige+Rd,+Malleshwaram,+Bengaluru,+Karnataka+560003&t=&z=16&ie=UTF8&iwloc=&output=embed')
    latitude = db.Column(db.Float, nullable=True, default=12.9982562)
    longitude = db.Column(db.Float, nullable=True, default=77.5716692)
    
    # Schedule & Status
    opening_hours = db.Column(db.String(255), nullable=False, default='Monday - Saturday: 10:00 AM - 8:00 PM | Sunday: Closed')
    weekly_closure = db.Column(db.String(100), nullable=True, default='Sunday')
    weekday_open_time = db.Column(db.String(10), nullable=False, default='10:00')
    weekday_close_time = db.Column(db.String(10), nullable=False, default='20:00')
    sunday_open_time = db.Column(db.String(10), nullable=False, default='00:00')
    sunday_close_time = db.Column(db.String(10), nullable=False, default='00:00')
    is_sunday_closed = db.Column(db.Boolean, default=True)
    
    # Content & Branding
    description = db.Column(db.Text, nullable=True, default='Your trusted neighborhood medical store dispensing authentic medicines, healthcare essentials, wellness products, and personalized care.')
    logo_path = db.Column(db.String(255), nullable=True, default='/static/images/logo.svg')
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tagline': self.tagline,
            'owner_name': self.owner_name,
            'phone': self.phone,
            'whatsapp': self.whatsapp,
            'doctor_phone': self.doctor_phone,
            'doctor_whatsapp': self.doctor_whatsapp,
            'email': self.email,
            'address': self.address,
            'area': self.area,
            'city': self.city,
            'state': self.state,
            'pincode': self.pincode,
            'landmark': self.landmark,
            'google_maps_url': self.google_maps_url,
            'google_maps_embed_url': self.google_maps_embed_url,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'opening_hours': self.opening_hours,
            'weekly_closure': self.weekly_closure,
            'description': self.description,
            'logo_path': self.logo_path
        }
