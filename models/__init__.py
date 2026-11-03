import os
import sys

# Ensure root directory is always on sys.path for IDE and runtime resolution
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.shop import Shop
from models.category import Category
from models.product import Product
from models.enquiry import Enquiry
from models.admin_user import AdminUser
from models.consultation import Consultation
from models.review import Review
from models.faq_question import FaqQuestion

__all__ = ['db', 'Shop', 'Category', 'Product', 'Enquiry', 'AdminUser', 'Consultation', 'Review', 'FaqQuestion']
