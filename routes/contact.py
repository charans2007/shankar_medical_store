from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Enquiry, Shop
from utils import async_send_problem_notification
import re

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact_page():
    shop = Shop.query.first()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        message = request.form.get('message', '').strip()
        problem_type = request.form.get('problem_type', request.form.get('product_name', 'General Problem')).strip()
        
        # Validation
        errors = []
        if not name or len(name) < 2:
            errors.append("Please enter your full name (minimum 2 characters).")
        if not phone or len(re.sub(r'\D', '', phone)) < 7:
            errors.append("Please provide a valid contact phone or WhatsApp number.")
        if not message or len(message) < 5:
            errors.append("Please describe the problem or issue you experienced (minimum 5 characters).")
            
        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('contact.html', form_data=request.form)
            
        # Create enquiry record marked as a raised problem
        enquiry = Enquiry(
            name=name,
            phone=phone,
            message=message,
            product_name=f"[Problem: {problem_type}]" if problem_type else "[Problem Reported]",
            status='unread'
        )
        db.session.add(enquiry)
        db.session.commit()

        # Send notification to official store email (shankarhomeostores@gmail.com)
        shop_title = shop.name if shop else "Shankar Homoeo Stores"
        async_send_problem_notification(name, phone, problem_type, message, shop_title)
        
        flash("Thank you! Your enquiry has been sent to our pharmacy team. Your problem/issue has been registered and forwarded to our official email (shankarhomeostores@gmail.com) for prompt review.", "success")
        return redirect(url_for('contact.contact_page'))

    return render_template('contact.html')
