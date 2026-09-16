from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.shop import Shop
from models.category import Category
from models.product import Product
from models.enquiry import Enquiry
from models.admin_user import AdminUser
from models.consultation import Consultation
from models.review import Review

__all__ = ['db', 'Shop', 'Category', 'Product', 'Enquiry', 'AdminUser', 'Consultation', 'Review']
