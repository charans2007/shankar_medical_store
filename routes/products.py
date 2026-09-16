from flask import Blueprint, render_template, request, jsonify, abort
from models import Product, Category, Shop
from utils import generate_whatsapp_link

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def catalogue():
    """
    Searchable product catalogue for in-store inventory discovery and WhatsApp availability enquiry.
    Strictly NOT an e-commerce store (no cart, no checkout, no delivery).
    """
    category_slug = request.args.get('category', '').strip()
    search_query = request.args.get('q', '').strip()
    availability_filter = request.args.get('availability', '').strip()
    
    query = Product.query
    
    selected_category = None
    if category_slug:
        selected_category = Category.query.filter_by(slug=category_slug).first()
        if selected_category:
            query = query.filter(Product.category_id == selected_category.id)
            
    if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
            (Product.name.ilike(search_filter)) |
            (Product.brand.ilike(search_filter)) |
            (Product.description.ilike(search_filter))
        )
        
    if availability_filter:
        query = query.filter(Product.availability == availability_filter)
        
    products = query.order_by(Product.name.asc()).all()
    categories = Category.query.order_by(Category.display_order.asc()).all()
    
    return render_template(
        'products.html',
        products=products,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query,
        availability_filter=availability_filter,
        total_results=len(products)
    )

@products_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    """Product detailed specification view with WhatsApp availability enquiry trigger."""
    product = Product.query.get_or_404(product_id)
    shop = Shop.query.first()
    shop_name = shop.name if shop else "Shankar Homoeo Stores"
    whatsapp_number = shop.whatsapp if shop else "919886661239"
    
    whatsapp_url = generate_whatsapp_link(
        whatsapp_number=whatsapp_number,
        product_name=product.name,
        shop_name=shop_name,
        message_type='availability'
    )
    
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(4).all()
    
    return render_template(
        'product_details.html',
        product=product,
        whatsapp_url=whatsapp_url,
        related_products=related_products
    )

@products_bp.route('/api/products/search')
def api_search():
    """Fast JSON endpoint for real-time frontend search filtering and suggestions."""
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify({'results': []})
        
    search_term = f"%{q}%"
    matches = Product.query.filter(
        (Product.name.ilike(search_term)) |
        (Product.brand.ilike(search_term)) |
        (Product.description.ilike(search_term))
    ).limit(8).all()
    
    results = []
    for item in matches:
        results.append({
            'id': item.id,
            'name': item.name,
            'category': item.category.name if item.category else '',
            'brand': item.brand or '',
            'availability': item.availability,
            'pack_size': item.pack_size or '',
            'url': f"/products/{item.id}"
        })
        
    return jsonify({'results': results})
