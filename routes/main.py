from flask import Blueprint, render_template, make_response, current_app, url_for, request, flash, redirect, jsonify

from models import db, Shop, Category, Product, Consultation, Enquiry, FaqQuestion

from utils import async_send_problem_notification, clean_phone_for_tel

from config import Config

import re

main_bp = Blueprint('main', __name__)

@main_bp.route('/')

def index():

    categories = Category.query.order_by(Category.display_order.asc()).all()

    featured_products = Product.query.limit(8).all()

    return render_template('index.html', categories=categories, featured_products=featured_products)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/services')

def services():

    categories = Category.query.order_by(Category.display_order.asc()).all()

    return render_template('services.html', categories=categories)

@main_bp.route('/retail-wholesale')

def retail_wholesale():

    shop = Shop.query.first()

    categories = Category.query.order_by(Category.display_order.asc()).all()

    return render_template('retail_wholesale.html', shop=shop, categories=categories)

@main_bp.route('/doctor-consultation', methods=['GET', 'POST'])

def doctor_consultation():

    shop = Shop.query.first()

    if request.method == 'POST':

        is_ajax = request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        payload = request.get_json(silent=True) if request.is_json else request.form

        patient_name = (payload.get('patient_name') or '').strip()

        phone = (payload.get('phone') or '').strip()

        address = (payload.get('address') or '').strip()

        age = (payload.get('age') or '').strip()

        gender = (payload.get('gender') or 'Not Specified').strip()

        health_concern = (payload.get('health_concern') or '').strip()

        consultation_mode = (payload.get('consultation_mode') or 'WhatsApp Video/Audio').strip()

        preferred_date = (payload.get('preferred_date') or '').strip()

        preferred_time = (payload.get('preferred_time') or 'Morning (10:00 AM - 01:00 PM)').strip()

        errors = []

        if not patient_name or len(patient_name) < 2:

            errors.append("Please enter the patient's full name.")

        if not phone or len(re.sub(r'\D', '', phone)) < 7:

            errors.append("Please provide a valid contact phone or WhatsApp number.")

        if not health_concern:

            health_concern = 'Online Doctor Consultation Call'

        if errors:

            if is_ajax:

                return jsonify({'success': False, 'message': errors[0], 'errors': errors}), 400

            for err in errors:

                flash(err, 'danger')

            return render_template('consultation.html', form_data=payload)

        consultation = Consultation(

            patient_name=patient_name,

            phone=phone,

            address=address if address else None,

            age=age if age else None,

            gender=gender,

            health_concern=health_concern,

            consultation_mode=consultation_mode,

            preferred_date=preferred_date if preferred_date else None,

            preferred_time=preferred_time,

            status='pending'

        )

        db.session.add(consultation)

        db.session.commit()

        doctor_phone_raw = shop.doctor_phone if (shop and getattr(shop, 'doctor_phone', None)) else Config.DOCTOR_CONSULTATION_PHONE

        doctor_call_url = clean_phone_for_tel(doctor_phone_raw)

        if is_ajax:

            return jsonify({

                'success': True,

                'message': 'Your Free Doctor Consultation request has been received!',

                'call_url': doctor_call_url,

                'consultation_id': consultation.id

            })

        flash("Your Free Doctor Consultation request has been received! Our consulting doctor/clinic coordinator will contact you shortly to confirm your consultation slot.", "success")

        return redirect(url_for('main.doctor_consultation'))

    return render_template('consultation.html')

@main_bp.route('/location')

def location():

    return render_template('location.html')

@main_bp.route('/faq', methods=['GET', 'POST'])

def faq():

    shop = Shop.query.first()

    

    if request.method == 'POST':

        name = request.form.get('name', '').strip()

        phone = request.form.get('phone', '').strip()

        message = request.form.get('message', '').strip()

        problem_type = request.form.get('problem_type', 'General Problem / Question').strip()

        

        # Validation

        errors = []

        if not name or len(name) < 2:

            errors.append("Please enter your full name (minimum 2 characters).")

        if not phone or len(re.sub(r'\D', '', phone)) < 7:

            errors.append("Please provide a valid contact phone or WhatsApp number.")

        if not message or len(message) < 5:

            errors.append("Please describe the problem or question in detail (minimum 5 characters).")

            

        if errors:

            for err in errors:

                flash(err, 'danger')

            answered_faqs = FaqQuestion.query.filter_by(is_public=True, status='answered').order_by(FaqQuestion.responded_at.desc()).all()

            return render_template('faq.html', form_data=request.form, answered_faqs=answered_faqs)

            

        # Create enquiry record marked as a raised problem/question

        enquiry = Enquiry(

            name=name,

            phone=phone,

            message=message,

            product_name=f"[Problem: {problem_type}]" if problem_type else "[FAQ Problem/Question]",

            status='unread'

        )

        db.session.add(enquiry)

        # Also create FaqQuestion so admin can review and respond via admin portal

        email = request.form.get('email', '').strip()

        faq_q = FaqQuestion(

            name=name,

            phone=phone,

            email=email if email else None,

            category=problem_type if problem_type else 'General Question',

            question=message,

            status='pending',

            is_public=True

        )

        db.session.add(faq_q)

        db.session.commit()

        # Send notification to official store email (shankarhomeostores@gmail.com)

        shop_title = shop.name if shop else "Shankar Homoeo Stores"

        async_send_problem_notification(name, phone, problem_type, message, shop_title)

        

        flash("Thank you! Your question has been registered and forwarded to our official email (shankarhomeostores@gmail.com) for prompt review.", "success")

        return redirect(url_for('main.faq'))

    answered_faqs = FaqQuestion.query.filter_by(is_public=True, status='answered').order_by(FaqQuestion.responded_at.desc()).all()

    return render_template('faq.html', answered_faqs=answered_faqs)

@main_bp.route('/sitemap.xml', methods=['GET'])

def sitemap():

    """Dynamically generate valid XML sitemap for local search engines."""

    pages = [

        {'loc': url_for('main.index', _external=True), 'priority': '1.0', 'changefreq': 'daily'},

        {'loc': url_for('main.about', _external=True), 'priority': '0.8', 'changefreq': 'monthly'},

        {'loc': url_for('main.services', _external=True), 'priority': '0.8', 'changefreq': 'monthly'},

        {'loc': url_for('main.retail_wholesale', _external=True), 'priority': '0.9', 'changefreq': 'weekly'},

        {'loc': url_for('products.catalogue', _external=True), 'priority': '0.9', 'changefreq': 'daily'},

        {'loc': url_for('main.location', _external=True), 'priority': '0.9', 'changefreq': 'weekly'},

        {'loc': url_for('contact.contact_page', _external=True), 'priority': '0.8', 'changefreq': 'monthly'},

        {'loc': url_for('main.doctor_consultation', _external=True), 'priority': '0.9', 'changefreq': 'weekly'},

        {'loc': url_for('main.faq', _external=True), 'priority': '0.7', 'changefreq': 'monthly'},

    ]

    

    # Add product detail pages

    products = Product.query.all()

    for product in products:

        pages.append({

            'loc': url_for('products.product_detail', product_id=product.id, _external=True),

            'priority': '0.7',

            'changefreq': 'weekly'

        })

    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>']

    sitemap_xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:

        sitemap_xml.append('  <url>')

        sitemap_xml.append(f"    <loc>{page['loc']}</loc>")

        sitemap_xml.append(f"    <changefreq>{page['changefreq']}</changefreq>")

        sitemap_xml.append(f"    <priority>{page['priority']}</priority>")

        sitemap_xml.append('  </url>')

    sitemap_xml.append('</urlset>')

    response = make_response('\n'.join(sitemap_xml))

    response.headers['Content-Type'] = 'application/xml'

    return response

@main_bp.route('/robots.txt', methods=['GET'])

def robots():

    """Standard robots.txt allowing search engines while keeping admin portal private."""

    sitemap_url = url_for('main.sitemap', _external=True)

    content = f"""User-agent: *

Disallow: /admin/

Disallow: /api/

Sitemap: {sitemap_url}

"""

    response = make_response(content)

    response.headers['Content-Type'] = 'text/plain'

    return response

