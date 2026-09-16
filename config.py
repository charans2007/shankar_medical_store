import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, 'database')
os.makedirs(DB_DIR, exist_ok=True)
DEFAULT_DB_PATH = os.path.join(DB_DIR, 'medical_shop.db').replace('\\', '/')

raw_db_url = os.environ.get('DATABASE_URL')
if not raw_db_url or raw_db_url.strip() == 'sqlite:///database/medical_shop.db':
    DATABASE_URI = f"sqlite:///{DEFAULT_DB_PATH}"
else:
    DATABASE_URI = raw_db_url

class Config:
    """Central configuration for the Medical Shop Application."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_medical_store_fallback_secret_key_2026')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security: Cookie settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Admin default credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    # Optional Google Maps API Key
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')

    # Central Shop Configuration
    SHOP_NAME = os.environ.get('SHOP_NAME', 'Shankar Homoeo Stores')
    SHOP_TAGLINE = os.environ.get('SHOP_TAGLINE', 'Your Trusted Homoeopathic & Medical Store')
    OWNER_NAME = os.environ.get('OWNER_NAME', 'J D Shankar')
    PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '+91 98866 61239')
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '919886661239')
    DOCTOR_CONSULTATION_PHONE = os.environ.get('DOCTOR_CONSULTATION_PHONE', '+91 95357 17958')
    DOCTOR_CONSULTATION_WHATSAPP = os.environ.get('DOCTOR_CONSULTATION_WHATSAPP', '919535717958')
    EMAIL = os.environ.get('EMAIL', 'shankarhomeostores@gmail.com')
    FULL_ADDRESS = os.environ.get('FULL_ADDRESS', 'Shankar homoeo stores, opp to Kids kingdom, 7th Cross, Sampige Rd, Malleshwaram, Bengaluru, Karnataka 560003')
    AREA = os.environ.get('AREA', 'Malleswaram')
    CITY = os.environ.get('CITY', 'Bengaluru')
    STATE = os.environ.get('STATE', 'Karnataka')
    PINCODE = os.environ.get('PINCODE', '560003')
    GOOGLE_MAPS_URL = os.environ.get('GOOGLE_MAPS_URL', 'https://www.google.com/maps/dir/?api=1&destination=Shankar+homoeo+stores,+opp+to+Kids+kingdom,+7th+Cross,+Sampige+Rd,+Malleshwaram,+Bengaluru,+Karnataka+560003')
    LATITUDE = float(os.environ.get('LATITUDE', '12.9982562'))
    LONGITUDE = float(os.environ.get('LONGITUDE', '77.5716692'))
    OPENING_HOURS = os.environ.get('OPENING_HOURS', 'Monday - Saturday: 10:00 AM - 8:00 PM | Sunday: Closed')
    WEEKLY_CLOSURE = os.environ.get('WEEKLY_CLOSURE', 'Sunday')
    SHOP_DESCRIPTION = os.environ.get('SHOP_DESCRIPTION', 'Your trusted neighborhood medical store dispensing authentic medicines, healthcare essentials, wellness products, and personalized care.')
    SHOP_LOGO = os.environ.get('SHOP_LOGO', '/static/images/logo.svg')

    # Weekly timing config for dynamic open/closed calculation
    # Store standard daily opening and closing hours (24-hour format)
    # 0 = Monday, 6 = Sunday
    DAILY_SCHEDULE = {
        0: {'open': '10:00', 'close': '20:00', 'closed': False}, # Mon
        1: {'open': '10:00', 'close': '20:00', 'closed': False}, # Tue
        2: {'open': '10:00', 'close': '20:00', 'closed': False}, # Wed
        3: {'open': '10:00', 'close': '20:00', 'closed': False}, # Thu
        4: {'open': '10:00', 'close': '20:00', 'closed': False}, # Fri
        5: {'open': '10:00', 'close': '20:00', 'closed': False}, # Sat
        6: {'open': '00:00', 'close': '00:00', 'closed': True},  # Sun
    }
