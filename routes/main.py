from flask import Blueprint, render_template, make_response, current_app, url_for, request, flash, redirect
from models import db, Shop, Category, Product, Consultation, Review, Enquiry
from utils import async_send_problem_notification
import re

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    categories = Category.query.order_by(Category.display_order.asc()).all()
    featured_products = Product.query.limit(8).all()
    return render_template('index.html', categories=categories, featured_products=featured_products)

@main_bp.route('/about')
def about():
    reviews = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).limit(4).all()
    return render_template('about.html', recent_reviews=reviews)

@main_bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        author_name = request.form.get('author_name', '').strip()
        rating_val = request.form.get('rating', '5').strip()
        comment = request.form.get('comment', '').strip()
        service_tag = request.form.get('service_tag', 'General Healthcare').strip()
        location = request.form.get('location', 'Malleswaram, Bengaluru').strip()

        errors = []
        if not author_name or len(author_name) < 2:
            errors.append("Please provide your name.")
        if not comment or len(comment) < 5:
            errors.append("Please write a few words about your experience (at least 5 characters).")
        try:
            rating = int(rating_val)
            if rating < 1 or rating > 5:
                rating = 5
        except (ValueError, TypeError):
            rating = 5

        if errors:
            for err in errors:
                flash(err, 'danger')
            reviews_list = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).all()
            return render_template('reviews.html', reviews=reviews_list, form_data=request.form)

        new_review = Review(
            author_name=author_name,
            rating=rating,
            comment=comment,
            service_tag=service_tag,
            reviewer_title="Verified Customer",
            location=location if location else "Bengaluru",
            is_approved=True
        )
        db.session.add(new_review)
        db.session.commit()

        flash(f"Thank you, {author_name}! Your review has been successfully received and added.", "success")
        return redirect(url_for('main.reviews') + '#customer-reviews')

    reviews_list = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).all()
    total_count = len(reviews_list)
    avg_rating = round(sum(r.rating for r in reviews_list) / total_count, 1) if total_count else 4.6
    
    # Calculate star distribution percentages
    star_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for r in reviews_list:
        if r.rating in star_counts:
            star_counts[r.rating] += 1
            
    star_pcts = {
        star: int((count / total_count) * 100) if total_count else 0
        for star, count in star_counts.items()
    }

    return render_template(
        'reviews.html',
        reviews=reviews_list,
        total_count=total_count,
        avg_rating=avg_rating,
        star_counts=star_counts,
        star_pcts=star_pcts
    )

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
        patient_name = request.form.get('patient_name', '').strip()
        phone = request.form.get('phone', '').strip()
        age = request.form.get('age', '').strip()
        gender = request.form.get('gender', 'Not Specified').strip()
        health_concern = request.form.get('health_concern', '').strip()
        consultation_mode = request.form.get('consultation_mode', 'WhatsApp Video/Audio').strip()
        preferred_time = request.form.get('preferred_time', 'Morning (10:00 AM - 01:00 PM)').strip()

        errors = []
        if not patient_name or len(patient_name) < 2:
            errors.append("Please enter the patient's full name.")
        if not phone or len(re.sub(r'\D', '', phone)) < 7:
            errors.append("Please provide a valid contact phone or WhatsApp number.")
        if not health_concern or len(health_concern) < 5:
            errors.append("Please describe your primary health concern or symptoms briefly.")

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('consultation.html', form_data=request.form)

        consultation = Consultation(
            patient_name=patient_name,
            phone=phone,
            age=age,
            gender=gender,
            health_concern=health_concern,
            consultation_mode=consultation_mode,
            preferred_time=preferred_time,
            status='pending'
        )
        db.session.add(consultation)
        db.session.commit()

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
            return render_template('faq.html', form_data=request.form)
            
        # Create enquiry record marked as a raised problem/question
        enquiry = Enquiry(
            name=name,
            phone=phone,
            message=message,
            product_name=f"[Problem: {problem_type}]" if problem_type else "[FAQ Problem/Question]",
            status='unread'
        )
        db.session.add(enquiry)
        db.session.commit()

        # Send notification to official store email (shankarhomeostores@gmail.com)
        shop_title = shop.name if shop else "Shankar Homoeo Stores"
        async_send_problem_notification(name, phone, problem_type, message, shop_title)
        
        flash("Thank you! Your problem/question has been registered and forwarded to our official email (shankarhomeostores@gmail.com) for prompt review.", "success")
        return redirect(url_for('main.faq'))

    return render_template('faq.html')

@main_bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Dynamically generate valid XML sitemap for local search engines."""
    pages = [
        {'loc': url_for('main.index', _external=True), 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': url_for('main.about', _external=True), 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': url_for('main.reviews', _external=True), 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': url_for('main.services', _external=True), 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': url_for('main.retail_wholesale', _external=True), 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': url_for('products.catalogue', _external=True), 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': url_for('main.location', _external=True), 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': url_for('contact.contact_page', _external=True), 'priority': '0.8', 'changefreq': 'monthly'},
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
