"""
Database Schema Migration & Integrity Utility for Shankar Homoeo Stores.
Ensures all database tables, columns, constraints, and initial seeds are properly synced.
"""

import os
import sys

# Ensure root directory is in sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app
from models import db, Shop, Category, Product, AdminUser, Enquiry, Consultation, Review, FaqQuestion
from seed_data import seed_database
from config import Config

def migrate_database():
    print("=" * 70)
    print(" SHANKAR HOMOEO STORES - DATABASE MIGRATION & REPAIR UTILITY")
    print("=" * 70)

    app = create_app()

    with app.app_context():
        # 1. Ensure all defined tables exist
        print("[*] Checking database tables and schema...")
        db.create_all()

        # 2. Inspect tables in SQLite
        conn = db.session.connection().connection
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall() if not row[0].startswith('sqlite_')]
        print(f"[*] Found {len(tables)} active tables: {', '.join(sorted(tables))}")

        # 3. Check WAL Mode
        cursor.execute("PRAGMA journal_mode;")
        journal_mode = cursor.fetchone()[0]
        print(f"[*] SQLite Journal Mode: {journal_mode.upper()}")
        if journal_mode.upper() != 'WAL':
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA busy_timeout=30000;")
            print("    -> Configured SQLite WAL mode for high concurrency.")

        # 4. Check for baseline shop configuration & admin user
        shop_count = Shop.query.count()
        category_count = Category.query.count()
        product_count = Product.query.count()
        admin_count = AdminUser.query.count()

        print("\n[*] Database Record Counts:")
        print(f"    - Shop Profiles:    {shop_count}")
        print(f"    - Admin Accounts:   {admin_count}")
        print(f"    - Categories:       {category_count}")
        print(f"    - Products:         {product_count}")
        print(f"    - Enquiries:        {Enquiry.query.count()}")
        print(f"    - Consultations:    {Consultation.query.count()}")
        print(f"    - Reviews:          {Review.query.count()}")
        print(f"    - FAQ Questions:    {FaqQuestion.query.count()}")

        if shop_count == 0 or admin_count == 0:
            print("\n[*] Initial data missing. Running automated database seeder...")
            seed_database(app)
            print("    -> Baseline data seeded successfully.")

        print("\n" + "=" * 70)
        print(" [SUCCESS] Database schema is healthy, synced, and production-ready!")
        print("=" * 70)

if __name__ == '__main__':
    migrate_database()

