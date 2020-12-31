from flask import Flask, render_template, session, redirect, url_for, abort
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

# import classes from model
from model import User, Role, Consumer, Supplier, Review, ShoppingCart, Order, OrderLines, Message
from form import ConsumerRegForm, SupplierRegForm, loginForm


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
def hello_world():
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
    db.session.add_all([role_supplier, role_consumer, role_admin])  # premade user for
    db.session.commit()


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
        new_consumer = Consumer(consumer_email=registerForm.email.data,
                                consumer_name=registerForm.name.data,
                                consumer_surname=registerForm.familyname.data,
                                consumer_address=registerForm.address.data,
                                consumer_phone=registerForm.phone.data)
        # TODO insert information also in consumer's table
        db.session.add(new_user)
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
        new_supplier = Supplier(supplier_email=registerForm.email.data,
                                supplier_name=registerForm.name.data,
                                supplier_address=registerForm.address.data,
                                supplier_phone=registerForm.phone.data,
                                piva=registerForm.piva.data,
                                description=registerForm.description.data)
        # TODO insert information in supplier's table
        db.session.add(user_info)
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


@app.route('/user/<username>') # TODO change it to ID
def consumer(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@app.route('/dashboard')
def dashboard():
    if session.get('email'):
        name = session.get('name')
        return render_template('dashboard.html', name=name)
    else:
        return redirect(url_for('login'))


# session logout

def logout():
    session.clear()
    return redirect(url_for('post_layout'))  # TODO create post_layout.html


@app.route('/testHome')
def testHomepage():
    return render_template('Homepage.html')


# Error 404 and 500 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
