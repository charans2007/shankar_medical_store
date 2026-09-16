import os
from datetime import datetime
from flask import Flask, render_template, request
from config import Config
from models import db, Shop, Category
from utils import get_store_status, clean_phone_for_tel, clean_whatsapp_number, generate_whatsapp_link
from seed_data import seed_database

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure database directory exists
    db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database')
    os.makedirs(db_dir, exist_ok=True)

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

    # Global Context Processor: Makes shop info and live status available to all Jinja templates
    @app.context_processor
    def inject_global_shop_data():
        try:
            shop = Shop.query.first()
        except Exception:
            shop = None
            
        store_status = get_store_status(shop) if shop else {
            'is_open': False,
            'status_text': 'STATUS UNAVAILABLE',
            'status_class': 'status-closed',
            'badge_color': '#6b7280',
            'today_hours_text': Config.OPENING_HOURS,
            'sub_text': 'Check store hours'
        }

        # Categories for navigation dropdown
        try:
            nav_categories = Category.query.order_by(Category.display_order.asc()).all()
        except Exception:
            nav_categories = []

        # WhatsApp and Phone links for current shop
        whatsapp_num = shop.whatsapp if (shop and shop.whatsapp) else Config.WHATSAPP_NUMBER
        phone_num = shop.phone if (shop and shop.phone) else Config.PHONE_NUMBER
        doctor_phone_num = (shop.doctor_phone if (shop and getattr(shop, 'doctor_phone', None)) 
                            else Config.DOCTOR_CONSULTATION_PHONE)
        doctor_whatsapp_num = (shop.doctor_whatsapp if (shop and getattr(shop, 'doctor_whatsapp', None)) 
                              else Config.DOCTOR_CONSULTATION_WHATSAPP)
        shop_title = shop.name if (shop and shop.name) else Config.SHOP_NAME

        return {
            'shop': shop or Config,
            'store_status': store_status,
            'nav_categories': nav_categories,
            'clean_phone': clean_phone_for_tel(phone_num),
            'clean_whatsapp': clean_whatsapp_number(whatsapp_num),
            'doctor_phone': doctor_phone_num,
            'clean_doctor_phone': clean_phone_for_tel(doctor_phone_num),
            'doctor_whatsapp': doctor_whatsapp_num,
            'clean_doctor_whatsapp': clean_whatsapp_number(doctor_whatsapp_num),
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
        db.create_all()
        if not Shop.query.first():
            seed_database(app)

    return app

app = create_app()

if __name__ == '__main__':
    # Run development server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
