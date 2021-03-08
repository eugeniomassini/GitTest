from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] = 'kncjdiejdsfmsdasldfjwqop'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # recommendation from pycharm

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.mail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['EMAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']

db = SQLAlchemy(app)  # database object
bcrypt = Bcrypt(app)  # to encrypt the use password
mail_object = Mail(app)  # mail object

from model import User, Role, Consumer, Supplier, Review, ShoppingCart, Order, OrderLines, Message
from form import ConsumerRegForm, SupplierRegForm, loginForm, researchForm


# Send mail for confirmation of the registration
def send_mail(to, subject, template, **kwargs):
    msg = Message(subject,
                  recipients=[to],
                  sender=app.config['MAIL_USERNAME'])
    print(msg)
    msg.html = render_template('welcome-mail.html', **kwargs)  # TODO modify welcome-mail.html
    mail_object.send(msg)


# Send mail for confirmation of the registration for suppliers
def send_mail_supp(to, subject, template, **kwargs):
    msg = Message(subject,
                  recipients=[to],
                  sender=app.config['MAIL_USERNAME'])
    print(msg)
    msg.html = render_template('supplier-mail.html', **kwargs)  # TODO modify supplier-mail.html
    mail_object.send(msg)


@app.route('/')
def helloworld():
    return 'Hello World!'


@app.route('/index')
@app.route('/homepage')
def homepage():
    return render_template('base.html')


@app.before_first_request
def setup_db():
    db.drop_all()
    db.create_all()
    role_supplier = Role(name='Supplier')
    role_consumer = Role(name='Consumer')
    role_admin = Role(name='Admin')
    db.session.add_all([role_supplier, role_consumer, role_admin])
    db.session.commit()

# Following lines only to pre-insert some users in the database without filling the form each time
    password1 = bcrypt.generate_password_hash('12345678').encode('utf-8')
    user_info = User(name='Fruit & Vegetables',
                     email='s289100@studenti.polito.it',
                     password=password1,
                     roleid=1)
    db.session.add(user_info)
    db.session.commit()
    user_info = User.query.filter_by(email='s289100@studenti.polito.it').first()
    session['user_id'] = user_info.id
    new_supplier = Supplier(id=user_info.id,
                            supplier_name='Fruit & Vegetables',
                            supplier_address='Torino',
                            supplier_phone='0123456789',
                            piva='000000',
                            description='Local & Fresh Food')
    db.session.add(new_supplier)
    db.session.commit()
    password2 = bcrypt.generate_password_hash('12345678').encode('utf-8')
    user_info = User(name='Organic Food',
                     email='s222585@studenti.polito.it',
                     password=password2,
                     roleid=1)
    db.session.add(user_info)
    db.session.commit()
    user_info = User.query.filter_by(email='s222585@studenti.polito.it').first()
    session['user_id'] = user_info.id
    new_supplier = Supplier(id=user_info.id,
                            supplier_name='Organic Food',
                            supplier_address='Milano',
                            supplier_phone='1234567890',
                            piva='222222',
                            description='Local & Fresh Vegetables')
    db.session.add(new_supplier)
    db.session.commit()
    password3 = bcrypt.generate_password_hash('12345678').encode('utf-8')
    new_user = User(name='Elisa',
                    email='elisa.vassallo.24@gmail.com',
                    password=password3,
                    roleid=2)
    db.session.add(new_user)
    db.session.commit()
    user_info = User.query.filter_by(email='elisa.vassallo.24@gmail.com').first()
    session['user_id'] = user_info.id
    new_consumer = Consumer(id=user_info.id,
                            consumer_name='Elisa',
                            consumer_surname='Vassallo',
                            consumer_address='Torino',
                            consumer_phone='0123456789')
    db.session.add(new_consumer)
    db.session.commit()
    password3 = bcrypt.generate_password_hash('12345678').encode('utf-8')
    user_info = User(name='Organic Vegetables',
                     email='s222589@studenti.polito.it',
                     password=password3,
                     roleid=1)
    db.session.add(user_info)
    db.session.commit()
    user_info = User.query.filter_by(email='s222589@studenti.polito.it').first()
    session['user_id'] = user_info.id
    new_supplier = Supplier(id=user_info.id,
                            supplier_name='Organic Vegetables',
                            supplier_address='Torino',
                            supplier_phone='2345678901',
                            piva='333333',
                            description='Local Food')
    db.session.add(new_supplier)
    db.session.commit()
# End of lines for pre-filling

# Consumer registration in db
@app.route('/register/consumer', methods=['POST', 'GET'])
def consumer_reg():
    name = None
    registerForm = ConsumerRegForm()
    if registerForm.validate_on_submit():
        name = registerForm.name.data
        session['name'] = registerForm.name.data
        session['email'] = registerForm.email.data
        password_2 = bcrypt.generate_password_hash(registerForm.password.data).encode('utf-8')
        new_user = User(name=registerForm.name.data,
                        email=registerForm.email.data,
                        password=password_2,
                        roleid=2)
        db.session.add(new_user)
        db.session.commit()
        user_info = User.query.filter_by(email=registerForm.email.data).first()
        session['user_id'] = user_info.id
        new_consumer = Consumer(id=user_info.id,
                                consumer_name=registerForm.name.data,
                                consumer_surname=registerForm.familyname.data,
                                consumer_address=registerForm.address.data,
                                consumer_phone=registerForm.phone.data)
        db.session.add(new_consumer)
        db.session.commit()

        # send welcome email
        send_mail(registerForm.email.data,
                  'You have registered successfully',
                  'mail',
                  name=registerForm.name.data,
                  email=registerForm.email.data,
                  password=registerForm.password.data)

        return redirect(url_for('login'))  # TODO create post_layout.html or choose where to go
    return render_template('signup-consumer.html', registerForm=registerForm, name=name)


# Supplier registration in db
@app.route('/register/supplier', methods=['POST', 'GET'])
def supplier_reg():
    name = None
    registerForm = SupplierRegForm()
    if registerForm.validate_on_submit():
        name = registerForm.name.data
        session['name'] = registerForm.name.data
        session['email'] = registerForm.email.data
        password_2 = bcrypt.generate_password_hash(registerForm.password.data).encode('utf-8')
        user_info = User(name=registerForm.name.data,
                         email=registerForm.email.data,
                         password=password_2,
                         roleid=1)
        db.session.add(user_info)
        db.session.commit()
        user_info = User.query.filter_by(email=registerForm.email.data).first()
        session['user_id'] = user_info.id
        new_supplier = Supplier(id=user_info.id,
                                supplier_name=registerForm.name.data,
                                supplier_address=registerForm.address.data,
                                supplier_phone=registerForm.phone.data,
                                piva=registerForm.piva.data,
                                description=registerForm.description.data)
        db.session.add(new_supplier)
        db.session.commit()

        # send welcome email
        send_mail_supp(registerForm.email.data,
                       'You have registered successfully',
                       'mail',
                       name=registerForm.name.data,
                       email=registerForm.email.data,
                       password=registerForm.password.data)

        return redirect(url_for('login'))  # TODO create post_layout.html
    return render_template('signup-supplier.html', registerForm=registerForm, name=name)


# session login
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = loginForm()
    if login_form.validate_on_submit():
        user_info = User.query.filter_by(email=login_form.email.data).first()
        if user_info and bcrypt.check_password_hash(user_info.password, login_form.password.data):
            session['user_id'] = user_info.id
            session['name'] = user_info.name
            session['email'] = user_info.email
            session['role_id'] = user_info.role_id
        return redirect('dashboard')  # TODO create dashboard.html
    return render_template('signin.html', login_form=login_form)


@app.route('/dashboard')
def dashboard():
    if session.get('email'):
        name=session.get('name')
        return render_template('dashboard.html',name=name)
    else:
        return redirect(url_for('login'))


# session logout

def logout():
    session.clear()
    return redirect(url_for('post_layout'))  # TODO create post_layout.html


@app.route('/testHome')
def testHomepage():
    return render_template('Homepage.html')


@app.route('/testresearch', methods=['POST', 'GET'])
def testResearch():
    research_form = researchForm()
    if research_form.validate_on_submit():
        city = research_form.city.data
        session['city'] = research_form.city.data
        #suppliers = Supplier.query.filter_by(supplier_address=city).all()
        #locals_ids = [supplier.id for supplier in suppliers]
        #localsuppliers = Supplier.query.filter(Supplier.id.in_(locals_ids)).all()
        #dropname = db.engine.execute("SELECT * FROM SUPPLIER WHERE SUPPLIER_ADDRESS LIKE 'city' ORDER BY id")
        #suppliers = dropname.fetchall
        #cur.execute=(dropname, ('%'+research_form.city.data+'%',))
        #flash('Showing result for: ' + research_form.city.data, 'success')
        return redirect(url_for('testResults', city=city))
    #else:
        #flash('Search again', 'danger')
    return render_template('research.html', research_form=research_form)



@app.route('/testres', methods=['GET'])
def testResults():
    city = request.args.get('city')
    suppliers = Supplier.query.filter_by(supplier_address=city).all()
    locals_ids = [supplier.id for supplier in suppliers]
    localsuppliers = Supplier.query.filter(Supplier.id.in_(locals_ids)).all()
    if localsuppliers is None:
        return redirect(url_for('page_not_found'))
    return render_template('results.html', localsuppliers=localsuppliers)


# Error 404 and 500 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
