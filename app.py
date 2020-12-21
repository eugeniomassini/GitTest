from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_mail import Mail, Message


app = Flask(__name__)

app.config['SECRET_KEY'] = 'kncjdiejdsfmsdasldfjwqop'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///website.db'
app.config['SQLALCHEMY_COMMIT_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # recommendation from pycharm

#Email configuration
app.config['MAIL_SERVER'] ='smtp.mail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['EMAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']

db = SQLAlchemy(app) # database object
bcrypt = Bcrypt(app)
mail_object = Mail(app) # mail object

from model import User, Role
from form import ConsumerRegForm, loginForm


# Send mail for confirmation of the registration
def send_mail(to, subject, template, **kwargs):
    msg = Message(subject,
                  recipients=[to],
                  sender=app.config['MAIL_USERNAME'])
    print(msg)
    msg.html = render_template('welcome-mail.html', **kwargs) #TODO modify welcome-mail.html
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
    db.session.add_all([role_supplier, role_consumer, role_admin])
    db.session.commit()


@app.route('/registerdb',methods=['POST','GET'])
def regiterPagedb():
    name=None
    registerForm=ConsumerRegForm()
    if registerForm.validate_on_submit():
        name=registerForm.name.data
        session['name']=registerForm.name.data
        session['email']=registerForm.email.data
        password_2 = bcrypt.generate_password_hash(registerForm.password.data).encode('utf-8')
        newuser = User(name=registerForm.name.data,
                       username=registerForm.email.data,
                       password=registerForm.password.data, role_id=2)
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register-db.html',registerForm=registerForm,name_website='SQL Registration to IS 2020 Platform',name=name)




@app.route('/signin')
def login():
    return render_template('signin.html')

# Consumer registration in db
@app.route('/register', methods=['POST', 'GET'])
def consumer_reg():
    name=None
    registerForm=ConsumerRegForm()
    if registerForm.validate_on_submit():
        name=registerForm.name.data
        session['name']=registerForm.name.data
        session['email']=registerForm.email.data
        password_2 = bcrypt.generate_password_hash(registerForm.password.data).encode('utf-8')
        newuser = User(name=registerForm.name.data,
                       username=registerForm.email.data,
                       password=password_2,
                       role_id=2)
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('post_layout')) #TODO create post_layout.html
    return render_template('register.html', registerForm=registerForm, name=name)




#session login

def login():
    login_form = loginForm()
    if login_form.validate_on_submit():
        user_info = User.query.filter_by(username=login_form.username.data).first()
        if user_info and bcrypt.check_password_hash(user_info.password, login_form.password.data):
            session['user_id'] = user_info.id
            session['name'] = user_info.name
            session['email'] = user_info.username
            session['role_id'] = user_info.role_id
            return redirect('dashboard') #TODO create dashboard

    return render_template('login.html', login_form=login_form) #TODO create login.html


# session logout

def logout():
    session.clear()
    return redirect(url_for('post_layout')) #TODO create post_layout.html



# Error 404 and 500 handlers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'),500


@app.route('/testHome')
def testHomepage():
    return render_template('Homepage.html')

@app.route('/reg-c')
def signupC():
    return render_template('signup-consumer.html')

if __name__ == '__main__':
    app.run()
