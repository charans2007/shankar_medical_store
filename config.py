import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Check if running in Vercel Serverless environment (where filesystem outside /tmp is read-only)
is_vercel = (
    os.environ.get('VERCEL') == '1' or
    bool(os.environ.get('VERCEL_ENV')) or
    bool(os.environ.get('NOW_REGION')) or
    bool(os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))
)

if is_vercel:
    import tempfile
    DB_DIR = tempfile.gettempdir()
    DEFAULT_DB_PATH = os.path.join(DB_DIR, 'medical_shop.db').replace('\\', '/')
    bundled_db_path = os.path.join(BASE_DIR, 'database', 'medical_shop.db')
    if not os.path.exists(DEFAULT_DB_PATH) and os.path.exists(bundled_db_path):
        import shutil
        try:
            shutil.copy2(bundled_db_path, DEFAULT_DB_PATH)
        except Exception:
            pass
else:
    DB_DIR = os.path.join(BASE_DIR, 'database')
    try:
        os.makedirs(DB_DIR, exist_ok=True)
    except OSError:
        pass
    DEFAULT_DB_PATH = os.path.join(DB_DIR, 'medical_shop.db').replace('\\', '/')

raw_db_url = os.environ.get('DATABASE_URL')
if not raw_db_url or raw_db_url.strip() in ('sqlite:///database/medical_shop.db', 'sqlite:///medical_shop.db'):
    DATABASE_URI = f"sqlite:///{DEFAULT_DB_PATH}"
else:
    # Handle postgres:// to postgresql:// dialect translation for SQLAlchemy
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URI = raw_db_url

class Config:
    """Central configuration for the Medical Shop Application."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_medical_store_fallback_secret_key_2026')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # High-Concurrency Database Engine Options (SQLite 30s timeout, non-blocking connection pool)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'connect_args': {
            'timeout': 30,
            'check_same_thread': False
        }
    }
    
    # Static asset caching (1 day) to reduce I/O under multi-user concurrency
    SEND_FILE_MAX_AGE_DEFAULT = 86400
    
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
    # General Store & Pharmacy Desk Phone & WhatsApp (Orders / Medicine availability)
    PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '+91 98866 61239')
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '919886661239')
    
    # Physical Store Details (Homeolaya)
    PHYSICAL_STORE_NAME = os.environ.get('PHYSICAL_STORE_NAME', 'Homeolaya')
    
    # Physical Doctor Consultant (Dr. Komala GR @ Homeolaya) - ONLY 8050604747
    PHYSICAL_DOCTOR_PHONE = os.environ.get('PHYSICAL_DOCTOR_PHONE', '+91 80506 04747')
    PHYSICAL_DOCTOR_WHATSAPP = os.environ.get('PHYSICAL_DOCTOR_WHATSAPP', '918050604747')
    PHYSICAL_STORE_PHONE = os.environ.get('PHYSICAL_STORE_PHONE', '+91 80506 04747')
    PHYSICAL_STORE_WHATSAPP = os.environ.get('PHYSICAL_STORE_WHATSAPP', '918050604747')
    
    # Free Doctor Consultations (Online Tele-health Doctor) - ONLY 9535717958
    DOCTOR_CONSULTATION_PHONE = os.environ.get('DOCTOR_CONSULTATION_PHONE', '+91 95357 17958')
    DOCTOR_CONSULTATION_WHATSAPP = os.environ.get('DOCTOR_CONSULTATION_WHATSAPP', '919535717958')
    EMAIL = os.environ.get('EMAIL', 'shankarhomeostores@gmail.com')
    
    # Main Store Address (Shankar Homoeo Stores - Malleshwaram)
    FULL_ADDRESS = os.environ.get('FULL_ADDRESS', 'opp to Kids kingdom, 7th Cross, Sampige Rd, Malleshwaram, Bengaluru, Karnataka 560003')
    AREA = os.environ.get('AREA', 'Malleshwaram')
    CITY = os.environ.get('CITY', 'Bengaluru')
    STATE = os.environ.get('STATE', 'Karnataka')
    PINCODE = os.environ.get('PINCODE', '560003')
    LANDMARK = os.environ.get('LANDMARK', 'opp to Kids kingdom')
    GOOGLE_MAPS_URL = os.environ.get('GOOGLE_MAPS_URL', 'https://www.google.com/maps/dir/?api=1&destination=Kids+Kingdom,+7th+Cross,+Sampige+Rd,+Malleshwaram,+Bengaluru,+Karnataka+560003')
    GOOGLE_MAPS_EMBED_URL = os.environ.get('GOOGLE_MAPS_EMBED_URL', 'https://maps.google.com/maps?q=opp+to+Kids+kingdom,+7th+Cross,+Sampige+Rd,+Malleshwaram,+Bengaluru,+Karnataka+560003&t=&z=16&ie=UTF8&iwloc=&output=embed')
    LATITUDE = float(os.environ.get('LATITUDE', '13.0035'))
    LONGITUDE = float(os.environ.get('LONGITUDE', '77.5701'))

    # Physical Store Details (Homeolaya - Vidyaranyapura)
    PHYSICAL_STORE_NAME = os.environ.get('PHYSICAL_STORE_NAME', 'Homeolaya')
    PHYSICAL_STORE_ADDRESS = os.environ.get('PHYSICAL_STORE_ADDRESS', 'Homeolaya, Suvarna Complex, 706/1, Vidyaranyapura Main Rd, near BWSSB Office & Canara Bank Stop, near Hyderabadi Bawarchi, BEL Layout, Vidyaranyapura, Bengaluru, Karnataka 560097')
    PHYSICAL_STORE_LANDMARK = os.environ.get('PHYSICAL_STORE_LANDMARK', 'Near BWSSB Office & Canara Bank Stop, Near Hyderabadi Bawarchi')
    PHYSICAL_STORE_AREA = os.environ.get('PHYSICAL_STORE_AREA', 'Vidyaranyapura')
    PHYSICAL_STORE_PINCODE = os.environ.get('PHYSICAL_STORE_PINCODE', '560097')
    PHYSICAL_STORE_MAPS_URL = os.environ.get('PHYSICAL_STORE_MAPS_URL', 'https://www.google.com/maps/dir/?api=1&destination=Homeolaya,+Suvarna+Complex,+706/1,+Vidyaranyapura+Main+Rd,+near+BWSSB+Office+%26+Canara+Bank+Stop,+near+Hyderabadi+Bawarchi,+BEL+Layout,+Vidyaranyapura,+Bengaluru,+Karnataka+560097')
    PHYSICAL_STORE_MAPS_EMBED_URL = os.environ.get('PHYSICAL_STORE_MAPS_EMBED_URL', 'https://maps.google.com/maps?q=Homeolaya,+Suvarna+Complex,+706/1,+Vidyaranyapura+Main+Rd,+BEL+Layout,+Vidyaranyapura,+Bengaluru,+Karnataka+560097&t=&z=16&ie=UTF8&iwloc=&output=embed')
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
