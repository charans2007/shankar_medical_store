from models import db

class Category(db.Model):
    """
    Product categories e.g. Prescription Medicines, OTC Medicines, First Aid, etc.
    """
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    icon = db.Column(db.String(50), nullable=True, default='capsules')
    display_order = db.Column(db.Integer, default=0)

    # Relationships
    products = db.relationship('Product', backref='category', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'icon': self.icon,
            'product_count': len(self.products)
        }
