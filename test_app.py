"""
Comprehensive Automated Test Suite for Medicare Medical Shop Website.
Tests all public routes, search API, contact submission, admin authentication, and inventory CRUD.
"""

import unittest
from app import create_app
from models import db, Shop, Product, Category, Enquiry, AdminUser
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test_secret_key'

class MedicalShopTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_01_public_pages(self):
        """Verify all public facing pages render with HTTP 200."""
        routes = ['/', '/about', '/reviews', '/services', '/retail-wholesale', '/products', '/location', '/faq', '/contact', '/doctor-consultation']
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Failed on route {route}")
            self.assertIn(b'Shankar Homoeo Stores', response.data)

        # Check retail & wholesale specific content
        res_rw = self.client.get('/retail-wholesale')
        self.assertIn(b'20+ Years of Experience as Distributor in Retail and Wholesale', res_rw.data)

        # Check home page specific hero content
        res_home = self.client.get('/')
        self.assertIn(b'Your Trusted', res_home.data)
        self.assertIn(b'Free Doctor Consultation', res_home.data)

    def test_02_seo_endpoints(self):
        """Verify sitemap.xml and robots.txt are served correctly."""
        # Sitemap
        res_sitemap = self.client.get('/sitemap.xml')
        self.assertEqual(res_sitemap.status_code, 200)
        self.assertIn(b'<urlset', res_sitemap.data)

        # Robots
        res_robots = self.client.get('/robots.txt')
        self.assertEqual(res_robots.status_code, 200)
        self.assertIn(b'Disallow: /admin/', res_robots.data)

    def test_03_404_error_page(self):
        """Verify custom 404 page is rendered for non-existent paths."""
        response = self.client.get('/non-existent-page-url-xyz')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 - Page Not Found', response.data)

    def test_04_product_search_api(self):
        """Verify the live search JSON API returns matching items."""
        response = self.client.get('/api/products/search?q=Paracetamol')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('results', json_data)
        self.assertTrue(len(json_data['results']) >= 1)
        self.assertIn('Paracetamol', json_data['results'][0]['name'])

    def test_05_product_details_page(self):
        """Verify product detail view loads and includes WhatsApp link with pre-filled message."""
        import html
        product = Product.query.first()
        self.assertIsNotNone(product)
        
        response = self.client.get(f'/products/{product.id}')
        self.assertEqual(response.status_code, 200)
        escaped_name = html.escape(product.name).encode()
        self.assertIn(escaped_name, response.data)
        self.assertIn(b'wa.me', response.data)

    def test_06_contact_enquiry_form(self):
        """Verify submitting the contact form persists an enquiry to the database."""
        form_data = {
            'name': 'Anita Sharma',
            'phone': '+91 91234 56789',
            'message': 'Do you have digital thermometers in stock today?',
            'product_name': 'Digital Clinical Thermometer'
        }
        response = self.client.post('/contact', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thank you! Your enquiry has been sent', response.data)

        # Verify DB entry
        enquiry = Enquiry.query.filter_by(name='Anita Sharma').first()
        self.assertIsNotNone(enquiry)
        self.assertEqual(enquiry.phone, '+91 91234 56789')
        self.assertEqual(enquiry.status, 'unread')

    def test_07_admin_auth_and_dashboard(self):
        """Verify admin session authentication and protected dashboard."""
        # Unauthorized access redirects to login
        res_unauth = self.client.get('/admin/dashboard')
        self.assertEqual(res_unauth.status_code, 302)
        self.assertIn('/admin/login', res_unauth.headers['Location'])

        # Failed login
        res_fail = self.client.post('/admin/login', data={'username': 'admin', 'password': 'wrongpassword'})
        self.assertEqual(res_fail.status_code, 200)
        self.assertIn(b'Invalid admin credentials', res_fail.data)

        # Successful login
        res_login = self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b'Pharmacy Dashboard', res_login.data)

        # Access dashboard while authenticated
        res_dash = self.client.get('/admin/dashboard')
        self.assertEqual(res_dash.status_code, 200)
        self.assertIn(b'Total Products', res_dash.data)

        # Logout
        res_logout = self.client.get('/admin/logout', follow_redirects=True)
        self.assertEqual(res_logout.status_code, 200)
        self.assertIn(b'Staff Admin Login', res_logout.data)

    def test_08_admin_product_crud(self):
        """Verify admin can add, edit, and delete products."""
        # Login first
        self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'})
        category = Category.query.first()

        # Add product
        new_prod_data = {
            'name': 'Test Vitamin C 500mg Chewable',
            'category_id': category.id,
            'brand': 'HealthBrand',
            'pack_size': 'Bottle of 30',
            'dosage_form': 'Tablet',
            'availability': 'In Stock',
            'description': 'Daily antioxidant support.'
        }
        res_add = self.client.post('/admin/products/add', data=new_prod_data, follow_redirects=True)
        self.assertEqual(res_add.status_code, 200)

        created_prod = Product.query.filter_by(name='Test Vitamin C 500mg Chewable').first()
        self.assertIsNotNone(created_prod)

        # Edit product
        edit_data = {
            'name': 'Test Vitamin C 500mg Chewable (Updated)',
            'category_id': category.id,
            'brand': 'HealthBrand Pro',
            'pack_size': 'Bottle of 60',
            'dosage_form': 'Tablet',
            'availability': 'Limited Stock',
            'description': 'Updated formulation.'
        }
        res_edit = self.client.post(f'/admin/products/edit/{created_prod.id}', data=edit_data, follow_redirects=True)
        self.assertEqual(res_edit.status_code, 200)

        updated_prod = Product.query.get(created_prod.id)
        self.assertEqual(updated_prod.name, 'Test Vitamin C 500mg Chewable (Updated)')
        self.assertEqual(updated_prod.availability, 'Limited Stock')

        # Delete product
        res_del = self.client.post(f'/admin/products/delete/{created_prod.id}', follow_redirects=True)
        self.assertEqual(res_del.status_code, 200)
        self.assertIsNone(Product.query.get(created_prod.id))

    def test_09_admin_settings_update(self):
        """Verify admin can update shop configurations."""
        self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'})
        
        settings_data = {
            'name': 'Sanjeevani Medical Store',
            'tagline': 'Trusted Health Care Since 2010',
            'owner_name': 'Dr. Sharma',
            'phone': '+919876543210',
            'whatsapp': '919876543210',
            'email': 'sanjeevani@example.com',
            'address': 'Shop 12, Market Complex, Indiranagar',
            'area': 'Indiranagar',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'pincode': '560038',
            'landmark': 'Opposite Metro Station',
            'google_maps_url': 'https://maps.google.com/?q=pharmacy',
            'google_maps_embed_url': 'https://maps.google.com/maps?q=pharmacy&output=embed',
            'latitude': '12.9784',
            'longitude': '77.6408',
            'opening_hours': 'Mon-Sat: 8:00 AM - 10:30 PM | Sun: 9:00 AM - 3:00 PM',
            'weekly_closure': 'None',
            'weekday_open_time': '08:00',
            'weekday_close_time': '22:30',
            'sunday_open_time': '09:00',
            'sunday_close_time': '15:00',
            'description': 'Your community pharmacy in Indiranagar.'
        }
        res = self.client.post('/admin/settings', data=settings_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        shop = Shop.query.first()
        self.assertEqual(shop.name, 'Sanjeevani Medical Store')
        self.assertEqual(shop.city, 'Bengaluru')

    def test_10_reviews_page(self):
        """Verify dedicated reviews page renders, accepts customer review submissions, and admin lists reviews."""
        # 1. GET reviews page
        response = self.client.get('/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Customer Reviews &amp; Testimonials', response.data)
        self.assertIn(b'Submit a Review', response.data)

        # 2. POST submit customer review
        review_data = {
            'author_name': 'Kavita Menon',
            'rating': '5',
            'comment': 'Exceptional service and quick response for Dr. Reckeweg drops availability in Malleswaram.',
            'service_tag': 'German Dilutions & Medicines',
            'location': 'Malleswaram 8th Cross'
        }
        res_post = self.client.post('/reviews', data=review_data, follow_redirects=True)
        self.assertEqual(res_post.status_code, 200)
        self.assertIn(b'Your review has been successfully received and added', res_post.data)
        self.assertIn(b'Kavita Menon', res_post.data)
        self.assertIn(b'Exceptional service and quick response', res_post.data)

        # 3. Admin view reviews
        self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'})
        res_admin = self.client.get('/admin/reviews')
        self.assertEqual(res_admin.status_code, 200)
        self.assertIn(b'Kavita Menon', res_admin.data)

if __name__ == '__main__':
    unittest.main()
