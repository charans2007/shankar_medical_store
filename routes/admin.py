import functools
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models import db, AdminUser, Product, Category, Enquiry, Shop, Consultation, Review

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(view):
    """Decorator to require authenticated admin session."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the pharmacy administration dashboard.', 'warning')
            return redirect(url_for('admin.login', next=request.url))
        return view(**kwargs)
    return wrapped_view

# ----------------- AUTHENTICATION -----------------

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('admin.dashboard'))
        else:
            flash('Invalid admin credentials. Please verify username and password.', 'danger')
            
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been securely logged out.', 'info')
    return redirect(url_for('admin.login'))

# ----------------- DASHBOARD -----------------

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_products = Product.query.count()
    available_products = Product.query.filter(Product.availability.in_(['In Stock', 'Available'])).count()
    out_of_stock_products = Product.query.filter_by(availability='Out of Stock').count()
    total_enquiries = Enquiry.query.count()
    unread_enquiries = Enquiry.query.filter_by(status='unread').count()
    total_consultations = Consultation.query.count()
    pending_consultations = Consultation.query.filter_by(status='pending').count()
    
    recent_enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).limit(6).all()
    recent_consultations = Consultation.query.order_by(Consultation.created_at.desc()).limit(6).all()
    recent_products = Product.query.order_by(Product.updated_at.desc()).limit(6).all()
    
    return render_template(
        'admin/dashboard.html',
        total_products=total_products,
        available_products=available_products,
        out_of_stock_products=out_of_stock_products,
        total_enquiries=total_enquiries,
        unread_enquiries=unread_enquiries,
        total_consultations=total_consultations,
        pending_consultations=pending_consultations,
        recent_enquiries=recent_enquiries,
        recent_consultations=recent_consultations,
        recent_products=recent_products
    )

# ----------------- PRODUCT MANAGEMENT -----------------

@admin_bp.route('/products')
@admin_required
def products():
    category_id = request.args.get('category_id', type=int)
    availability = request.args.get('availability', '').strip()
    search = request.args.get('q', '').strip()
    
    query = Product.query
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if availability:
        query = query.filter(Product.availability == availability)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
        
    product_list = query.order_by(Product.name.asc()).all()
    categories = Category.query.order_by(Category.name.asc()).all()
    
    return render_template(
        'admin/products.html',
        products=product_list,
        categories=categories,
        selected_category_id=category_id,
        selected_availability=availability,
        search=search
    )

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    categories = Category.query.order_by(Category.name.asc()).all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category_id = request.form.get('category_id', type=int)
        brand = request.form.get('brand', '').strip()
        pack_size = request.form.get('pack_size', '').strip()
        dosage_form = request.form.get('dosage_form', '').strip()
        availability = request.form.get('availability', 'In Stock')
        requires_prescription = bool(request.form.get('requires_prescription'))
        description = request.form.get('description', '').strip()
        
        if not name or not category_id:
            flash('Product name and category are required.', 'danger')
            return render_template('admin/add_product.html', categories=categories, form_data=request.form)
            
        new_prod = Product(
            name=name,
            category_id=category_id,
            brand=brand,
            pack_size=pack_size,
            dosage_form=dosage_form,
            availability=availability,
            requires_prescription=requires_prescription,
            description=description
        )
        db.session.add(new_prod)
        db.session.commit()
        flash(f'Product "{name}" added successfully to the store catalogue.', 'success')
        return redirect(url_for('admin.products'))
        
    return render_template('admin/add_product.html', categories=categories)

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    categories = Category.query.order_by(Category.name.asc()).all()
    
    if request.method == 'POST':
        product.name = request.form.get('name', '').strip()
        product.category_id = request.form.get('category_id', type=int)
        product.brand = request.form.get('brand', '').strip()
        product.pack_size = request.form.get('pack_size', '').strip()
        product.dosage_form = request.form.get('dosage_form', '').strip()
        product.availability = request.form.get('availability', 'In Stock')
        product.requires_prescription = bool(request.form.get('requires_prescription'))
        product.description = request.form.get('description', '').strip()
        
        if not product.name or not product.category_id:
            flash('Product name and category are required.', 'danger')
            return render_template('admin/edit_product.html', product=product, categories=categories)
            
        db.session.commit()
        flash(f'Product "{product.name}" updated successfully.', 'success')
        return redirect(url_for('admin.products'))
        
    return render_template('admin/edit_product.html', product=product, categories=categories)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    p_name = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f'Product "{p_name}" removed from catalogue.', 'info')
    return redirect(url_for('admin.products'))

# ----------------- CATEGORY MANAGEMENT -----------------

@admin_bp.route('/categories', methods=['GET', 'POST'])
@admin_required
def categories():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            name = request.form.get('name', '').strip()
            slug = request.form.get('slug', '').strip().lower().replace(' ', '-')
            description = request.form.get('description', '').strip()
            icon = request.form.get('icon', 'capsules').strip()
            
            if not name or not slug:
                flash('Category name and slug are required.', 'danger')
            else:
                existing = Category.query.filter((Category.name == name) | (Category.slug == slug)).first()
                if existing:
                    flash('A category with that name or slug already exists.', 'warning')
                else:
                    cat = Category(name=name, slug=slug, description=description, icon=icon)
                    db.session.add(cat)
                    db.session.commit()
                    flash(f'Category "{name}" created.', 'success')
            return redirect(url_for('admin.categories'))

        elif action == 'edit':
            category_id = request.form.get('category_id', type=int)
            cat = Category.query.get_or_404(category_id)
            cat.name = request.form.get('name', '').strip()
            cat.description = request.form.get('description', '').strip()
            cat.icon = request.form.get('icon', 'capsules').strip()
            db.session.commit()
            flash(f'Category "{cat.name}" updated.', 'success')
            return redirect(url_for('admin.categories'))

    cat_list = Category.query.order_by(Category.display_order.asc()).all()
    return render_template('admin/categories.html', categories=cat_list)

@admin_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@admin_required
def delete_category(category_id):
    cat = Category.query.get_or_404(category_id)
    c_name = cat.name
    db.session.delete(cat)
    db.session.commit()
    flash(f'Category "{c_name}" deleted.', 'info')
    return redirect(url_for('admin.categories'))

# ----------------- ENQUIRIES -----------------

@admin_bp.route('/enquiries')
@admin_required
def enquiries():
    enquiry_list = Enquiry.query.order_by(Enquiry.created_at.desc()).all()
    return render_template('admin/enquiries.html', enquiries=enquiry_list)

@admin_bp.route('/enquiries/<int:enquiry_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_enquiry_status(enquiry_id):
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    enquiry.status = 'read' if enquiry.status == 'unread' else 'unread'
    db.session.commit()
    flash(f'Enquiry from {enquiry.name} marked as {enquiry.status}.', 'info')
    return redirect(url_for('admin.enquiries'))

@admin_bp.route('/enquiries/<int:enquiry_id>/delete', methods=['POST'])
@admin_required
def delete_enquiry(enquiry_id):
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    db.session.delete(enquiry)
    db.session.commit()
    flash('Enquiry deleted.', 'info')
    return redirect(url_for('admin.enquiries'))

# ----------------- DOCTOR CONSULTATIONS -----------------

@admin_bp.route('/consultations')
@admin_required
def consultations():
    consultation_list = Consultation.query.order_by(Consultation.created_at.desc()).all()
    return render_template('admin/consultations.html', consultations=consultation_list)

@admin_bp.route('/consultations/<int:consultation_id>/status', methods=['POST'])
@admin_required
def update_consultation_status(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    new_status = request.form.get('status', 'confirmed')
    consultation.status = new_status
    db.session.commit()
    flash(f'Consultation for {consultation.patient_name} marked as {new_status}.', 'info')
    return redirect(url_for('admin.consultations'))

@admin_bp.route('/consultations/<int:consultation_id>/delete', methods=['POST'])
@admin_required
def delete_consultation(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    db.session.delete(consultation)
    db.session.commit()
    flash('Consultation booking deleted.', 'info')
    return redirect(url_for('admin.consultations'))

# ----------------- SHOP SETTINGS -----------------

@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    shop = Shop.query.first()
    if not shop:
        shop = Shop()
        db.session.add(shop)
        db.session.commit()

    if request.method == 'POST':
        shop.name = request.form.get('name', shop.name).strip()
        shop.tagline = request.form.get('tagline', shop.tagline).strip()
        shop.owner_name = request.form.get('owner_name', shop.owner_name).strip()
        shop.phone = request.form.get('phone', shop.phone).strip()
        shop.whatsapp = request.form.get('whatsapp', shop.whatsapp).strip()
        shop.doctor_phone = request.form.get('doctor_phone', getattr(shop, 'doctor_phone', '+91 95357 17958')).strip()
        shop.doctor_whatsapp = request.form.get('doctor_whatsapp', getattr(shop, 'doctor_whatsapp', '919535717958')).strip()
        shop.email = request.form.get('email', shop.email).strip()
        shop.address = request.form.get('address', shop.address).strip()
        shop.area = request.form.get('area', shop.area).strip()
        shop.city = request.form.get('city', shop.city).strip()
        shop.state = request.form.get('state', shop.state).strip()
        shop.pincode = request.form.get('pincode', shop.pincode).strip()
        shop.landmark = request.form.get('landmark', shop.landmark).strip()
        shop.google_maps_url = request.form.get('google_maps_url', shop.google_maps_url).strip()
        shop.google_maps_embed_url = request.form.get('google_maps_embed_url', shop.google_maps_embed_url).strip()
        
        try:
            shop.latitude = float(request.form.get('latitude', shop.latitude))
            shop.longitude = float(request.form.get('longitude', shop.longitude))
        except (ValueError, TypeError):
            pass

        shop.opening_hours = request.form.get('opening_hours', shop.opening_hours).strip()
        shop.weekly_closure = request.form.get('weekly_closure', shop.weekly_closure).strip()
        shop.weekday_open_time = request.form.get('weekday_open_time', shop.weekday_open_time).strip()
        shop.weekday_close_time = request.form.get('weekday_close_time', shop.weekday_close_time).strip()
        shop.sunday_open_time = request.form.get('sunday_open_time', shop.sunday_open_time).strip()
        shop.sunday_close_time = request.form.get('sunday_close_time', shop.sunday_close_time).strip()
        shop.is_sunday_closed = bool(request.form.get('is_sunday_closed'))
        shop.description = request.form.get('description', shop.description).strip()
        
        db.session.commit()
        flash('Shop information updated successfully! Changes will appear throughout the website.', 'success')
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html', shop=shop)

# ----------------- REVIEW MANAGEMENT -----------------

@admin_bp.route('/reviews')
@admin_required
def reviews():
    all_reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('admin/reviews.html', reviews=all_reviews)

@admin_bp.route('/reviews/delete/<int:review_id>', methods=['POST'])
@admin_required
def delete_review(review_id):
    rev = Review.query.get_or_404(review_id)
    db.session.delete(rev)
    db.session.commit()
    flash('Customer review deleted successfully.', 'info')
    return redirect(url_for('admin.reviews'))
