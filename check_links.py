"""
Link and Asset Verification Script for Shankar Homoeo Stores Web Platform.
Checks all public routes, static assets, and endpoints to ensure zero 404/500 errors.
"""

import os
import re
import sys

# Ensure root directory is in sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app
from models import Product, Category, Shop

def check_all_links():
    app = create_app()
    client = app.test_client()

    print("=" * 70)
    print(" SHANKAR HOMOEO STORES - AUTOMATED LINK & ASSET HEALTH CHECK")
    print("=" * 70)

    routes_to_test = [
        '/',
        '/about',
        '/reviews',
        '/services',
        '/retail-wholesale',
        '/doctor-consultation',
        '/location',
        '/faq',
        '/products',
        '/contact',
        '/sitemap.xml',
        '/robots.txt',
        '/admin/login'
    ]

    with app.app_context():
        # Add categories
        for cat in Category.query.all():
            routes_to_test.append(f'/products/category/{cat.slug}')

        # Add products
        for prod in Product.query.limit(10).all():
            routes_to_test.append(f'/products/{prod.id}')

    tested_count = 0
    failures = []
    static_assets_checked = set()
    missing_assets = []

    print(f"\n[*] Testing {len(routes_to_test)} application routes...")
    for route in routes_to_test:
        tested_count += 1
        try:
            res = client.get(route)
            if res.status_code in (200, 302):
                print(f"  [PASS] {res.status_code} - {route}")
            else:
                print(f"  [FAIL] {res.status_code} - {route}")
                failures.append((route, res.status_code))

            # Scan HTML responses for static assets (/static/...)
            if res.content_type and 'text/html' in res.content_type:
                html = res.data.decode('utf-8', errors='ignore')
                asset_matches = re.findall(r'["\'](/static/[^"\'?#\s]+)', html)
                for asset in asset_matches:
                    if asset not in static_assets_checked:
                        static_assets_checked.add(asset)
                        rel_path = asset.replace('/static/', '', 1)
                        local_path = os.path.join(BASE_DIR, 'static', rel_path.replace('/', os.sep))
                        if not os.path.exists(local_path):
                            missing_assets.append((route, asset))

        except Exception as e:
            print(f"  [EXC]  {route}: {e}")
            failures.append((route, str(e)))

    print("\n" + "=" * 70)
    print(" HEALTH CHECK RESULTS")
    print("=" * 70)
    print(f" Routes Tested:         {tested_count}")
    print(f" Route Failures:        {len(failures)}")
    print(f" Static Assets Checked: {len(static_assets_checked)}")
    print(f" Missing Static Files:  {len(missing_assets)}")

    if failures:
        print("\n[!] ROUTE ERRORS:")
        for route, status in failures:
            print(f"   * {route} -> {status}")

    if missing_assets:
        print("\n[!] MISSING ASSETS FOUND IN PAGES:")
        for page, asset in missing_assets:
            print(f"   * Found on {page}: {asset}")

    if not failures and not missing_assets:
        print("\n [SUCCESS] All application routes and static assets verified OK! (100% HEALTHY)\n")
        return 0
    else:
        print("\n [WARNING] Some issues were detected.\n")
        return 1

if __name__ == '__main__':
    exit_code = check_all_links()
    sys.exit(exit_code)

