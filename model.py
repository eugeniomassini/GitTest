from datetime import datetime

from app import db

class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('Role.id'))
    type = db.Column(db.String(30))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __repr__(self):
        return "<User %r>" % self.name

class Role (db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing
    name = db.Column(db.String(20), nullable=False)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name

class Consumer (db.Model):
    id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True) # Auto-incrementing
    consumer_name = db.Column(db.String(50), nullable=False)
    consumer_surname = db.Column(db.String(50), nullable=False)
    consumer_address = db.Column(db.String(50), nullable=False)
    cosumer_phone = db.Column(db.String(12), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'consumer',
    }

class Supplier (db.Model):
    id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True) # Auto-incrementing
    supplier_name = db.Column(db.String(50), nullable=False)
    supplier_address = db.Column(db.String(50), nullable=False)
    supplier_phone = db.Column(db.String(12), nullable=False)
    piva = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'supplier',
    }

class Review (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consumer_id = db.Column(db.Integer, db.ForeignKey('Consumer.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('Supplier.id'))
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Product (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('Supplier.id'))
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    certificate = db.Column(db.Boolean)

class ShoppingCart (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    numberofproducts = db.Column(db.Integer)
    consumer_id = db.Column(db.Integer, db.ForeignKey('Consumer.id'))

class Order (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, )
    date = db.Column(db.Date)
    amount = db.Column(db.Float)
    pickup = db.Column(db.Boolean)
    consumer_id = db.Column(db.Integer, db.ForeignKey('Consumer.id'))

class OrderLines (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('Supplier.id'))
    quantity = db.Column(db.Integer)

class Message (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    request = db.Column(db.Text, nullable=False)
    supplier = db.Column(db.Boolean)