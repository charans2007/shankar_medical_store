import os
from datetime import datetime
from flask import Flask, render_template, request
from sqlalchemy import event
from sqlalchemy.engine import Engine
from config import Config, is_vercel
from models import db, Shop, Category
from utils import get_store_status, clean_phone_for_tel, clean_whatsapp_number, generate_whatsapp_link, get_cached_value
from seed_data import seed_database

# Optimize SQLite for High Concurrency (WAL locally, Memory pragma for serverless/Vercel)
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if hasattr(dbapi_connection, 'cursor'):
        try:
            cursor = dbapi_connection.cursor()
            if not is_vercel:
                cursor.execute("PRAGMA journal_mode=WAL")
            else:
                cursor.execute("PRAGMA journal_mode=MEMORY")
            cursor.execute("PRAGMA busy_timeout=30000")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.execute("PRAGMA cache_size=-64000")
            cursor.execute("PRAGMA temp_store=MEMORY")
            cursor.close()
        except Exception:
            pass

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, 'templates'),
        static_folder=os.path.join(BASE_DIR, 'static'),
        static_url_path='/static'
    )
    app.config.from_object(config_class)

    # Ensure database directory exists if writable (e.g. locally)
    try:
        db_dir = os.path.join(BASE_DIR, 'database')
        os.makedirs(db_dir, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from routes.main import main_bp
    from routes.products import products_bp
    from routes.contact import contact_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)

    # Global Context Processor: High-concurrency cached shop info and live status
    @app.context_processor
    def inject_global_shop_data():
        def fetch_shop():
            try:
                return Shop.query.first()
            except Exception:
                return None

        def fetch_categories():
            try:
                return Category.query.order_by(Category.display_order.asc()).all()
            except Exception:
                return []

        shop = get_cached_value('global_shop', 60, fetch_shop)
        nav_categories = get_cached_value('global_categories', 60, fetch_categories)

        store_status = get_store_status(shop) if shop else {
            'is_open': False,
            'status_text': 'STATUS UNAVAILABLE',
            'status_class': 'status-closed',
            'badge_color': '#6b7280',
            'today_hours_text': Config.OPENING_HOURS,
            'sub_text': 'Check store hours'
        }

        # WhatsApp and Phone links for current shop
        whatsapp_num = shop.whatsapp if (shop and shop.whatsapp) else Config.WHATSAPP_NUMBER
        phone_num = shop.phone if (shop and shop.phone) else Config.PHONE_NUMBER
        
        # Free Doctor Consultation (Online Tele-Health): 9535717958
        doctor_phone_num = (shop.doctor_phone if (shop and getattr(shop, 'doctor_phone', None)) 
                            else Config.DOCTOR_CONSULTATION_PHONE)
        doctor_whatsapp_num = (shop.doctor_whatsapp if (shop and getattr(shop, 'doctor_whatsapp', None)) 
                              else Config.DOCTOR_CONSULTATION_WHATSAPP)
        
        # Physical Doctor Consultant (In-Person / Homeolaya): 8050604747
        physical_doctor_phone_num = (shop.physical_store_phone if (shop and getattr(shop, 'physical_store_phone', None))
                                     else getattr(Config, 'PHYSICAL_DOCTOR_PHONE', '+91 80506 04747'))
        physical_doctor_whatsapp_num = (shop.physical_store_whatsapp if (shop and getattr(shop, 'physical_store_whatsapp', None))
                                       else getattr(Config, 'PHYSICAL_DOCTOR_WHATSAPP', '918050604747'))
        
        shop_title = shop.name if (shop and shop.name) else Config.SHOP_NAME

        return {
            'shop': shop or Config,
            'store_status': store_status,
            'nav_categories': nav_categories,
            'clean_phone': clean_phone_for_tel(phone_num),
            'clean_whatsapp': clean_whatsapp_number(whatsapp_num),
            # Free Doctor Consultation (Online) - ONLY 9535717958
            'doctor_phone': doctor_phone_num,
            'clean_doctor_phone': clean_phone_for_tel(doctor_phone_num),
            'doctor_whatsapp': doctor_whatsapp_num,
            'clean_doctor_whatsapp': clean_whatsapp_number(doctor_whatsapp_num),
            # Physical Doctor Consultant (In-Store / Dr. Komala GR) - ONLY 8050604747
            'physical_doctor_phone': physical_doctor_phone_num,
            'clean_physical_doctor_phone': clean_phone_for_tel(physical_doctor_phone_num),
            'physical_doctor_whatsapp': physical_doctor_whatsapp_num,
            'clean_physical_doctor_whatsapp': clean_whatsapp_number(physical_doctor_whatsapp_num),
            'header_whatsapp_url': generate_whatsapp_link(whatsapp_num, shop_name=shop_title, message_type='general'),
            'current_year': datetime.now().year,
            'generate_whatsapp_link': generate_whatsapp_link
        }

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    # CLI command for seeding
    @app.cli.command("seed-db")
    def seed_db_command():
        """CLI command to initialize tables and seed default shop and product data."""
        seed_database(app)

    # Auto-initialize and seed database on first run
    with app.app_context():
        try:
            db.create_all()
            if not Shop.query.first():
                seed_database(app)
        except Exception as e:
            app.logger.warning(f"Database initialization notice: {e}")

    return app

app = create_app()

if __name__ == '__main__':
    # Run development server
    port = int(os.environ.get('PORT', 5000))
    try:
        app.run(host='127.0.0.1', port=port, debug=True)
    except (KeyboardInterrupt, SystemExit):
        print("\n[*] Local server stopped cleanly.")
