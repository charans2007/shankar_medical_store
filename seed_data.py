import os
from models import db, Shop, Category, Product, AdminUser, Enquiry, Review
from config import Config

def seed_database(app):
    """Seed the database with default shop configuration, categories, and sample demo products."""
    with app.app_context():
        db.create_all()

        # 1. Initialize Shop Configuration if not present
        shop = Shop.query.first()
        if not shop:
            shop = Shop(
                name=Config.SHOP_NAME,
                tagline=Config.SHOP_TAGLINE,
                owner_name=Config.OWNER_NAME,
                phone=Config.PHONE_NUMBER,
                whatsapp=Config.WHATSAPP_NUMBER,
                email=Config.EMAIL,
                address=Config.FULL_ADDRESS,
                area=Config.AREA,
                city=Config.CITY,
                state=Config.STATE,
                pincode=Config.PINCODE,
                landmark='Near City Central Hospital / Bus Stand',
                google_maps_url=Config.GOOGLE_MAPS_URL,
                google_maps_embed_url='https://maps.google.com/maps?q=pharmacy&t=&z=15&ie=UTF8&iwloc=&output=embed',
                latitude=Config.LATITUDE,
                longitude=Config.LONGITUDE,
                opening_hours=Config.OPENING_HOURS,
                weekly_closure=Config.WEEKLY_CLOSURE,
                weekday_open_time='08:00',
                weekday_close_time='22:00',
                sunday_open_time='09:00',
                sunday_close_time='14:00',
                is_sunday_closed=False,
                description=Config.SHOP_DESCRIPTION,
                logo_path='/static/images/logo.svg'
            )
            db.session.add(shop)

        # 2. Seed Categories
        categories_data = [
            {"name": "Prescription Medicines", "slug": "prescription-medicines", "icon": "prescription", "description": "Authentic branded and generic prescription drugs dispensed against valid doctor prescriptions.", "order": 1},
            {"name": "Homoeopathic Dilutions", "slug": "homoeopathic-dilutions", "icon": "droplet", "description": "Authentic homoeopathic potencies (30C, 200C, 1M) prepared in pure dispensing alcohol.", "order": 2},
            {"name": "Mother Tinctures (Q)", "slug": "mother-tinctures", "icon": "flask", "description": "Concentrated herbal homoeopathic mother tinctures from SBL, Schwabe, and Dr. Reckeweg.", "order": 3},
            {"name": "Biochemic Tissue Salts", "slug": "biochemic-tissue-salts", "icon": "pills", "description": "Schuessler biochemic tissue remedies and combinations (6X, 12X).", "order": 4},
            {"name": "Speciality Drops & Tonics", "slug": "speciality-drops-tonics", "icon": "heart-pulse", "description": "Renowned German and Indian homoeopathic formulations, cough syrups, and health tonics.", "order": 5},
            {"name": "OTC Medicines", "slug": "otc-medicines", "icon": "pills", "description": "Safe over-the-counter pain relief, fever relievers, cough syrups, and digestive health remedies.", "order": 6},
            {"name": "First Aid", "slug": "first-aid", "icon": "first-aid", "description": "Bandages, antiseptics, sterile gauze, burn relief, surgical tapes, and emergency first aid supplies.", "order": 7},
            {"name": "Baby Care", "slug": "baby-care", "icon": "baby", "description": "Infant formula, gentle baby cleansers, diaper rash creams, feeding essentials, and baby hygiene.", "order": 8},
            {"name": "Personal Care", "slug": "personal-care", "icon": "spa", "description": "Skin and hair care, oral hygiene, dermatological lotions, antiseptic washes, and hand sanitizers.", "order": 9},
            {"name": "Vitamins & Wellness", "slug": "vitamins-wellness", "icon": "heart-pulse", "description": "Multivitamins, calcium supplements, omega-3 oils, immunity boosters, and herbal supplements.", "order": 10},
            {"name": "Medical Equipment", "slug": "medical-equipment", "icon": "stethoscope", "description": "Digital thermometers, BP monitors, pulse oximeters, vaporizers, and mobility aids.", "order": 11},
            {"name": "Diabetes Care", "slug": "diabetes-care", "icon": "droplet", "description": "Blood glucose monitoring meters, test strips, lancets, diabetic foot care, and sugar substitutes.", "order": 12},
            {"name": "Healthcare Products", "slug": "healthcare-products", "icon": "shield-check", "description": "Protective masks, hot water bottles, orthopedic braces, compression socks, and wellness aids.", "order": 13}
        ]

        category_map = {}
        for cat in categories_data:
            existing = Category.query.filter_by(slug=cat['slug']).first()
            if not existing:
                cat_obj = Category(
                    name=cat['name'],
                    slug=cat['slug'],
                    icon=cat['icon'],
                    description=cat['description'],
                    display_order=cat['order']
                )
                db.session.add(cat_obj)
                db.session.flush()
                category_map[cat['slug']] = cat_obj
            else:
                category_map[cat['slug']] = existing

        # 3. Seed Clearly Labeled Demo Products if catalogue is empty
        if Product.query.count() == 0:
            demo_products = [
                # Prescription Medicines
                {
                    "name": "[DEMO] Amoxicillin & Potassium Clavulanate 625mg",
                    "category": "prescription-medicines",
                    "brand": "Generic/Branded",
                    "pack_size": "Strip of 10 Tablets",
                    "dosage_form": "Tablet",
                    "requires_prescription": True,
                    "availability": "In Stock",
                    "description": "Broad-spectrum antibacterial formulation. Strictly dispensed upon presentation of a valid doctor's prescription."
                },
                {
                    "name": "[DEMO] Telmisartan 40mg",
                    "category": "prescription-medicines",
                    "brand": "Standard Healthcare",
                    "pack_size": "Strip of 15 Tablets",
                    "dosage_form": "Tablet",
                    "requires_prescription": True,
                    "availability": "In Stock",
                    "description": "Blood pressure management therapy. Requires a valid doctor's prescription for dispensing."
                },
                {
                    "name": "[DEMO] Atorvastatin 10mg",
                    "category": "prescription-medicines",
                    "brand": "PharmaCore",
                    "pack_size": "Strip of 10 Tablets",
                    "dosage_form": "Tablet",
                    "requires_prescription": True,
                    "availability": "In Stock",
                    "description": "Lipid-lowering medication. Valid doctor prescription required."
                },
                # OTC Medicines
                {
                    "name": "[DEMO] Paracetamol 650mg Fast Action",
                    "category": "otc-medicines",
                    "brand": "Reliable Care",
                    "pack_size": "Strip of 15 Tablets",
                    "dosage_form": "Tablet",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Widely used fever reducer and mild to moderate pain relief formulation."
                },
                {
                    "name": "[DEMO] Cough & Throat Lozenges (Menthol & Honey)",
                    "category": "otc-medicines",
                    "brand": "HerbaRelief",
                    "pack_size": "Pack of 24 Lozenges",
                    "dosage_form": "Lozenges",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Soothing throat drops for mild cough and irritated throat relief."
                },
                {
                    "name": "[DEMO] Antacid Oral Suspension Mint Flavour",
                    "category": "otc-medicines",
                    "brand": "GasRelief",
                    "pack_size": "200 ml Bottle",
                    "dosage_form": "Syrup",
                    "requires_prescription": False,
                    "availability": "Limited Stock",
                    "description": "Fast-acting relief from acidity, heartburn, and gas discomfort."
                },
                # First Aid
                {
                    "name": "[DEMO] Antiseptic Liquid (Povidone Iodine 5%)",
                    "category": "first-aid",
                    "brand": "SafeHeal",
                    "pack_size": "100 ml Bottle",
                    "dosage_form": "Liquid Antiseptic",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Topical antiseptic solution for minor cuts, grazes, and wound disinfection."
                },
                {
                    "name": "[DEMO] Sterile Cotton Gauze Swabs (7.5cm x 7.5cm)",
                    "category": "first-aid",
                    "brand": "MedGauze",
                    "pack_size": "Pack of 10 Pouches",
                    "dosage_form": "Surgical Dressing",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Sterilized 100% absorbent cotton gauze pads for wound dressing."
                },
                {
                    "name": "[DEMO] Waterproof Adhesive Bandages Assorted",
                    "category": "first-aid",
                    "brand": "QuickBand",
                    "pack_size": "Box of 50 Bandages",
                    "dosage_form": "Adhesive Strip",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Breathable, flexible, waterproof protection for minor everyday cuts and scrapes."
                },
                # Baby Care
                {
                    "name": "[DEMO] Pediatric Zinc Oxide Diaper Rash Cream",
                    "category": "baby-care",
                    "brand": "BabyCare Plus",
                    "pack_size": "75g Tube",
                    "dosage_form": "Ointment",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Protective barrier cream enriched with soothing zinc oxide and vitamin E."
                },
                {
                    "name": "[DEMO] Tear-Free Gentle Baby Wash & Shampoo",
                    "category": "baby-care",
                    "brand": "PureBaby",
                    "pack_size": "200 ml Bottle",
                    "dosage_form": "Liquid Wash",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Hypoallergenic, pH-balanced gentle daily cleanser for sensitive baby skin."
                },
                # Personal Care
                {
                    "name": "[DEMO] Dermatological Moisturizing Lotion with Ceramides",
                    "category": "personal-care",
                    "brand": "DermaShield",
                    "pack_size": "250 ml Pump Bottle",
                    "dosage_form": "Lotion",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Non-greasy, intense hydrating body lotion for dry and sensitive skin."
                },
                {
                    "name": "[DEMO] Medicated Anti-Dandruff Shampoo (Ketoconazole 2%)",
                    "category": "personal-care",
                    "brand": "ScalpGuard",
                    "pack_size": "100 ml Bottle",
                    "dosage_form": "Shampoo",
                    "requires_prescription": False,
                    "availability": "Availability Varies",
                    "description": "Targeted anti-dandruff and itchy scalp treatment shampoo."
                },
                # Vitamins & Wellness
                {
                    "name": "[DEMO] Daily Multivitamin & Mineral Formula",
                    "category": "vitamins-wellness",
                    "brand": "VitaVital",
                    "pack_size": "Bottle of 60 Tablets",
                    "dosage_form": "Tablet",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Comprehensive blend of essential vitamins A, C, D3, B-Complex and zinc for everyday vitality."
                },
                {
                    "name": "[DEMO] Calcium 500mg + Vitamin D3 Chewable",
                    "category": "vitamins-wellness",
                    "brand": "BoneStrong",
                    "pack_size": "Bottle of 30 Tablets",
                    "dosage_form": "Chewable Tablet",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Essential bone mineral supplement promoting bone density and calcium absorption."
                },
                # Medical Equipment
                {
                    "name": "[DEMO] Digital Blood Pressure Monitor with Auto-Inflation",
                    "category": "medical-equipment",
                    "brand": "AccuCheck Health",
                    "pack_size": "Single Unit Kit with Cuff",
                    "dosage_form": "Digital Device",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Accurate upper-arm automatic BP monitor with WHO blood pressure indicator and memory storage."
                },
                {
                    "name": "[DEMO] Fingertip Pulse Oximeter with OLED Display",
                    "category": "medical-equipment",
                    "brand": "OxyPulse",
                    "pack_size": "Single Unit with Lanyard",
                    "dosage_form": "Digital Device",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Fast and precise real-time SpO2 oxygen saturation and pulse rate measurement."
                },
                {
                    "name": "[DEMO] Digital Clinical Thermometer (Waterproof)",
                    "category": "medical-equipment",
                    "brand": "ThermoSafe",
                    "pack_size": "Single Unit with Case",
                    "dosage_form": "Device",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "High-precision 10-second oral, underarm, and rectal temperature reading with fever alarm."
                },
                # Diabetes Care
                {
                    "name": "[DEMO] Blood Glucose Monitoring System with 25 Test Strips",
                    "category": "diabetes-care",
                    "brand": "GlucoTrack",
                    "pack_size": "Complete Starter Kit",
                    "dosage_form": "Monitoring Kit",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Compact glucometer requiring tiny blood sample, providing reliable results in 5 seconds."
                },
                {
                    "name": "[DEMO] Sterile Blood Lancets 30G",
                    "category": "diabetes-care",
                    "brand": "MicroPrick",
                    "pack_size": "Box of 100 Lancets",
                    "dosage_form": "Lancet",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Ultra-fine silicon-coated lancets for gentle, virtually painless blood sampling."
                },
                # Healthcare Products
                {
                    "name": "[DEMO] 3-Ply Surgical Face Masks (BFE > 99%)",
                    "category": "healthcare-products",
                    "brand": "MediShield",
                    "pack_size": "Box of 50 Masks",
                    "dosage_form": "Protective Mask",
                    "requires_prescription": False,
                    "availability": "In Stock",
                    "description": "Certified high-filtration 3-ply disposable protective face masks with comfortable ear loops."
                },
                {
                    "name": "[DEMO] Orthopedic Lumbar Support Belt",
                    "category": "healthcare-products",
                    "brand": "OrthoRelief",
                    "pack_size": "Medium Size (Adjustable)",
                    "dosage_form": "Support Brace",
                    "requires_prescription": False,
                    "availability": "Availability Varies",
                    "description": "Ergonomic back support brace providing firm compression and spine stabilization."
                }
            ]

            for p in demo_products:
                cat_slug = p['category']
                if cat_slug in category_map:
                    product = Product(
                        name=p['name'],
                        category_id=category_map[cat_slug].id,
                        brand=p['brand'],
                        pack_size=p['pack_size'],
                        dosage_form=p['dosage_form'],
                        requires_prescription=p['requires_prescription'],
                        availability=p['availability'],
                        description=p['description']
                    )
                    db.session.add(product)

        # 4. Seed Admin User
        admin_user = AdminUser.query.filter_by(username=Config.ADMIN_USERNAME).first()
        if not admin_user:
            admin_user = AdminUser(username=Config.ADMIN_USERNAME)
            admin_user.set_password(Config.ADMIN_PASSWORD)
            db.session.add(admin_user)

        # 5. Seed Demo Enquiry
        if Enquiry.query.count() == 0:
            demo_enquiry = Enquiry(
                name="[DEMO] Ramesh Kumar",
                phone="+919876500000",
                message="[DEMO] Hello, do you have Blood Glucose Test Strips in stock today? I will visit this evening.",
                product_name="[DEMO] Blood Glucose Monitoring System with 25 Test Strips",
                status="unread"
            )
            db.session.add(demo_enquiry)

        # 6. Seed Initial Customer Reviews
        if Review.query.count() == 0:
            initial_reviews = [
                Review(
                    author_name="Venkatesh R.",
                    rating=5,
                    comment="One of the best homoeopathic stores in Malleswaram, Bangalore. They have almost every medicine you need, including rare German dilutions from Dr. Reckeweg and Schwabe that are hard to find elsewhere. Highly knowledgeable and courteous staff.",
                    service_tag="German Dilutions & Medicines",
                    reviewer_title="Local Guide",
                    location="Malleswaram, Bengaluru",
                    is_approved=True
                ),
                Review(
                    author_name="Dr. Priya N.",
                    rating=5,
                    comment="Very reliable homoeo pharmacy. The doctor consultation is extremely helpful and patient. They explain dosages clearly and all medicines are 100% authentic with sealed packaging. Recommended for anyone looking for holistic healthcare in Malleswaram.",
                    service_tag="Doctor Consultation",
                    reviewer_title="Malleswaram Resident",
                    location="Malleswaram, Bengaluru",
                    is_approved=True
                ),
                Review(
                    author_name="Satish Kumar",
                    rating=5,
                    comment="Been visiting Shankar Homoeo Stores on 7th Cross Sampige Road for years. Excellent stock of mother tinctures, dilutions, and biochemic combinations. The owner is very patient and explains the exact potency and bottle seal integrity.",
                    service_tag="Mother Tinctures",
                    reviewer_title="Local Resident",
                    location="7th Cross, Malleswaram",
                    is_approved=True
                ),
                Review(
                    author_name="Meenakshi Sundaram",
                    rating=5,
                    comment="Prompt service and very polite staff. I contacted them on WhatsApp beforehand to check availability of a specific Schwabe dilution and they confirmed within minutes with the price. Saved me a lot of travel time. 5 stars!",
                    service_tag="Customer Service & WhatsApp",
                    reviewer_title="Bengaluru Resident",
                    location="Bengaluru",
                    is_approved=True
                ),
                Review(
                    author_name="Rajesh Gopinath",
                    rating=5,
                    comment="Dr. Silaiezhil and the consulting homoeopaths provide genuine, caring diagnosis. My mother had chronic knee joint stiffness and their homoeopathic remedies brought immense relief without side effects. Shankar Homoeo Stores is truly a gem in Malleswaram.",
                    service_tag="Doctor Consultation",
                    reviewer_title="Verified Patient",
                    location="Bengaluru",
                    is_approved=True
                ),
                Review(
                    author_name="Ananya Mahesh",
                    rating=4,
                    comment="Good collection of SBL and Dr. Reckeweg drops. Store is located conveniently on 7th cross opposite Kids Kingdom. Can get a bit crowded on Saturday evenings, but the staff handles orders swiftly and accurately.",
                    service_tag="German Dilutions & Medicines",
                    reviewer_title="Local Resident",
                    location="Malleswaram",
                    is_approved=True
                ),
                Review(
                    author_name="Kishore Sharma",
                    rating=5,
                    comment="Always fresh medicines and all potencies available (30C, 200C, 1M, Q tinctures). The store maintains proper temperature and hygienic dispensing standards. Best place for homoeopathic needs in North Bangalore.",
                    service_tag="German Dilutions & Medicines",
                    reviewer_title="Local Guide",
                    location="North Bangalore",
                    is_approved=True
                ),
                Review(
                    author_name="Deepa Lakshmi",
                    rating=5,
                    comment="Had an online consultation for allergic rhinitis and sinusitis with their doctor. Very courteous and systematic questioning. The suggested homoeopathic treatment worked wonders. Very thankful to Shankar Homoeo Stores!",
                    service_tag="Doctor Consultation",
                    reviewer_title="Verified Patient",
                    location="Bengaluru",
                    is_approved=True
                ),
                Review(
                    author_name="Suresh K.",
                    rating=4,
                    comment="Very authentic medicines at reasonable prices. Even if a particular dilution is out of stock, they arrange it quickly or notify you on phone. Reliable neighborhood medical store.",
                    service_tag="Store Availability",
                    reviewer_title="Local Resident",
                    location="Malleswaram",
                    is_approved=True
                )
            ]
            for rev in initial_reviews:
                db.session.add(rev)

        db.session.commit()
        print("Database seeded successfully with initial configuration and demo data.")
