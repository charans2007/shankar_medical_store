# 🏥 Medicare - Physical Medical Store & Pharmacy Website

A modern, responsive, full-stack website built for local physical medical shops and retail pharmacies.

> **IMPORTANT ARCHITECTURAL RULE:**  
> This platform is **strictly designed for a PHYSICAL STORE ONLY**. It does **NOT** offer online medicine ordering, delivery, shopping carts, or online payment gateways. Instead, it enables local customers to:
> **Discover Store & Inventory &rarr; Check Live Status &rarr; Enquire on WhatsApp/Phone &rarr; Get GPS Directions &rarr; Visit the Physical Store**.

---

## 🌟 Key Features

- **Centralized Configuration:** All shop contact details, name, tagline, address, phone numbers, and timings are managed in one central place and can be live-edited via the Admin Dashboard.
- **Dynamic Live Store Status:** Real-time calculation showing **🟢 OPEN NOW** or **🔴 CLOSED** with today's operating hours and weekly holiday management.
- **WhatsApp Click-to-Chat Integration:** One-click pre-filled availability enquiries (`"Hello, I would like to enquire about the availability of [PRODUCT] at [SHOP]..."`).
- **Direct Phone Integration:** Standard `tel:` links for immediate connection with the pharmacy counter.
- **Google Maps Integration:** Embedded store map with instant "Get Directions" navigation.
- **Searchable Product Catalogue:** Instant client-side search and category filtering with stock badges (`In Stock`, `Limited Stock`, `Out of Stock`, `Availability Varies`).
- **Prescription Safety Disclaimers:** Explicit notices warning patients against self-medication and mandating registered doctor prescriptions for scheduled drugs.
- **Mobile-First Responsive Layout:** Includes a fixed mobile bottom action bar:  
  `[ 📞 Call ]  [ 💬 WhatsApp ]  [ 📍 Directions ]`
- **Secure Admin Portal:** Session-authenticated dashboard with hashed passwords (`Werkzeug`), product management (CRUD), category management, customer enquiry inbox, and live shop configuration.
- **Local SEO & Schema.org:** JSON-LD structured data for `Pharmacy`, automated dynamic `sitemap.xml`, and search-engine optimized `robots.txt`.

---

## 💻 Technology Stack

- **Backend:** Python 3.10+, Flask
- **Database & ORM:** SQLite, Flask-SQLAlchemy
- **Frontend:** HTML5, Modern Vanilla CSS3 (Custom design system), Vanilla JavaScript (No heavy frameworks)
- **Security:** Werkzeug password hashing, secure session cookies, input validation

---

## 📁 Project Architecture

```text
medicalshopWEB/
├── app.py                     # Application factory & entry point
├── config.py                  # Central configuration with placeholders
├── seed_data.py               # Database initialization & demo data seeder
├── utils.py                   # Dynamic open/closed status & WhatsApp URL generator
├── requirements.txt           # Python dependencies
├── README.md                  # Complete documentation
├── .env.example               # Environment variables template
├── .env                       # Local environment variables
├── .gitignore                 # Git ignore rules
│
├── database/
│   └── medical_shop.db        # SQLite database
│
├── models/                    # SQLAlchemy database models
│   ├── __init__.py            # Database instance & model exports
│   ├── shop.py                # Central store settings model
│   ├── category.py            # Product categories model
│   ├── product.py             # Product catalogue model
│   ├── enquiry.py             # Customer enquiries model
│   └── admin_user.py          # Admin credentials model (hashed passwords)
│
├── routes/                    # Flask blueprints
│   ├── __init__.py
│   ├── main.py                # Public pages (Home, About, Services, Location, FAQ, SEO)
│   ├── products.py            # Catalogue, Product details, Live Search JSON API
│   ├── contact.py             # Contact form & enquiry persistence
│   └── admin.py               # Admin auth, dashboard, inventory CRUD, settings
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Base layout with SEO, navbar, mobile bottom bar, footer
│   ├── index.html             # Homepage with Hero, Live Status, Categories, Reviews
│   ├── about.html             # Store philosophy, pharmacist info, store profile
│   ├── services.html          # In-store dispensing and healthcare services
│   ├── products.html          # Product catalogue with live search and filter pills
│   ├── product_details.html   # Detailed product view with WhatsApp enquiry
│   ├── contact.html           # Contact details and customer enquiry form
│   ├── location.html          # Dedicated Google Maps & directions page
│   ├── faq.html               # Configurable physical store FAQs
│   ├── 404.html               # Custom 404 error page
│   ├── 500.html               # Custom 500 server error page
│   │
│   └── admin/                 # Protected Admin Portal templates
│       ├── base_admin.html    # Admin layout with sidebar navigation
│       ├── login.html         # Secure login screen
│       ├── dashboard.html     # Inventory stats & recent enquiries
│       ├── products.html      # Product management table with filters
│       ├── add_product.html   # Add new product form
│       ├── edit_product.html  # Edit existing product form
│       ├── categories.html    # Category management
│       ├── enquiries.html     # Customer enquiries table with mark-as-read
│       └── settings.html      # Live shop profile & timings editor
│
├── static/
│   ├── css/
│   │   ├── style.css          # Main responsive healthcare stylesheet
│   │   └── admin.css          # Admin portal stylesheet
│   ├── js/
│   │   ├── main.js            # Mobile drawer, FAQ accordions, flash alerts
│   │   ├── products.js        # Real-time search filter
│   │   └── admin.js           # Delete confirmation prompts
│   ├── images/
│   │   └── logo.svg           # Scalable medical cross brand logo
│   └── favicon/
│       └── favicon.svg        # Medical store browser favicon
│
└── seo/
    ├── sitemap.xml            # Static SEO sitemap
    └── robots.txt             # Crawl directives
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or newer
- `pip` package manager

### 2. Environment Setup
Copy the example environment file:
```bash
cp .env.example .env
```
Inside `.env`, you can customize the default values:
- `SECRET_KEY`: Random secret string for session security.
- `ADMIN_USERNAME`: Default admin username (default: `admin`).
- `ADMIN_PASSWORD`: Default admin password (default: `admin123`).
- Initial placeholders for `SHOP_NAME`, `PHONE_NUMBER`, `WHATSAPP_NUMBER`, etc.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup & Seeding
The database tables and initial demo data are automatically created upon running the app for the first time. To manually re-seed the database at any point, run:
```bash
flask seed-db
```
*(Or in Python: `python -c "from app import app; from seed_data import seed_database; seed_database(app)"`)*

### 5. Run Locally
Start the Flask development server:
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 🔐 Staff Admin Access

- **Admin Login URL:** `http://127.0.0.1:5000/admin/login`
- **Default Username:** `admin`
- **Default Password:** `admin123`

*Note: You can change the admin password or username in `.env` before first seeding, or directly through the database.*

### In the Admin Panel, staff can:
1. **View Dashboard:** Stock counts, out-of-stock items, unread customer enquiries.
2. **Product Management:** Add new medicines/devices, edit details, set Rx prescription requirement, and update availability status (`In Stock`, `Limited Stock`, `Availability Varies`, `Out of Stock`).
3. **Category Management:** Add, edit, or delete product categories.
4. **Customer Enquiries:** View messages submitted by visitors, toggle read/unread status, or click to call back.
5. **Shop Settings:** Update shop name, phone numbers, WhatsApp number, full address, Google Maps URL, and weekday/Sunday operating hours live without restarting the server!

---

## 📍 Connecting to Google Business Profile

This website is engineered to complement the shop's Google Business Profile:

1. **Log in to Google Business Profile Manager:** Go to [business.google.com](https://business.google.com).
2. **Ensure NAP Consistency (Name, Address, Phone):** Ensure the **Shop Name**, **Address**, and **Phone Number** match exactly between your Google Business Profile and this website's settings.
3. **Add Website URL:** In Google Business Profile under **Edit Profile &rarr; Contact &rarr; Website**, paste your live website domain (e.g. `https://your-medical-store.com`).
4. **Embed Google Maps Pin:**
   - In Google Maps, search for your pharmacy.
   - Click **Share &rarr; Embed a map &rarr; Copy HTML**.
   - Extract the `src="..."` URL from the iframe and paste it into **Admin Dashboard &rarr; Shop Settings &rarr; Google Maps Embed URL**.
   - Copy the short share link into **Google Maps Directions URL**.
5. **Customer Reviews:** As customers leave authentic reviews on Google, you can feature their verified feedback on the website.

---

## 🌐 Production Deployment

To run in production on Ubuntu / Linux / VPS:
1. Use Gunicorn as the WSGI HTTP Server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```
2. Configure Nginx as a reverse proxy:
   ```nginx
   server {
       listen 80;
       server_name your-medical-store.com www.your-medical-store.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
3. Secure with free SSL certificate using Let's Encrypt Certbot:
   ```bash
   sudo certbot --nginx -d your-medical-store.com -d www.your-medical-store.com
   ```
