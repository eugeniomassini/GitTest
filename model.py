class Consumer(db.Model):
    _tablename_='Consumers'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(25),nullable=False)
    surname = db.Column(db.String(25),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(15),nullable=False)
    email = db.Column(db.String(25),unique=True,index=True)
    password = db.Column(db.String(15),nullable=False)
    orders = db.relationship('Order',backref='consumer')
    reviews = db.relatioship('Review',backref='consumer',lazy='dynamic')

class Supplier(db.Model):
    _tablename_='Suppliers'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(15),nullable=False)
    name = db.Column(db.String(25),nullable=False)
    piva = db.Column(db.String(11),nullable=False)
    description = db.Column(db.Text,nullable=True)
    email = db.Column(db.String(25),unique=True,index=True)
    password = db.Column(db.String(15),nullable=False)
    products = db.relationship('Product',backref='supplier')
    reviews = db.relationship('Review',backref='supplier',lazy='dynamic')

class Product(db.Model):
    _tablename_='Products'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer,db.ForeignKey('Suppliers.id'))
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.String(20),nullable=False)
    certificate = db.Column(db.Boolean)
    lines = db.relationship('OrderLines',backref='product')

class Order(db.Model):
    _tablename_='Orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10),nullable=False)
    consumer_id = db.Column(db.Integer,db.ForeignKey('Consumers.id'))
    amount = db.Column(db.Float,nullable=False)
    pickup = db.Column(db.Boolean)
    lines = db.relationship('OrderLines',backref='order')

class OrderLines(db.Model):
    _tablename_='Orders Lines'
    id = db.Column(db.Integer, primarykey=True)
    order_id = db.Column(db.Integer,db.ForeignKey('Orders.id'))
    product_id = db.Column(db.Integer,db.ForeignKey('Products.id'))
    supplier_id = db.Column(db.Integer,db.ForeignKey('Suppliers.id'))
    quantity = db.Column(db.Integer,nullable=False)

class Review(db.Model):
    _tablename_='Reviews'
    id = db.Column(db.Integer,primary_key=True)
    consumer_id = db.Column(db.Integer,db.ForeignKey('Consumers.id'))
    supplier_id = db.Column(db.Integer,db.ForeignKey('Supplier.id'))
    body = db.Column(db.Text,nullable=False)
    bodyhtml = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    score = db.Column(db.Integer)
    disabled = db.Column(db.Boolean)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i', 'strong']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))

db.event.listen(Comment.body, 'set', Comment.on_changed_body)

class Message(db.Model):
    id = db.Column(db.Integer, primarykey=True)
    name = db.Column(db.String(25))
    surname = db.Column(db.String(25))
    email = db.Column(db.String(25))
    request = db.Column(db.Text)
    supplier = db.Column(db.Boolean)