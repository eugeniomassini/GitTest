from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kncjdiejdsfmsdasldfjwqop'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///website.db'
app.config['SQLALCHEMY_COMMIT_TEARDOWN']=True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from model import User, Role
from form import ConsumerRegForm, loginForm



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
@app.route('/homepage')
def homepage():
    return render_template('index.html')


@app.before_first_request
def setup():
    db.drop_all()
    db.create_all()
    role_supplier = Role(name='Supplier')
    role_consumer = Role(name='Consumer')
    role_admin = Role(name='Admin')
    db.session.add_all([role_supplier,role_consumer,role_admin])
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
        session['name']=registerForm.name.data
        session['email']=registerForm.email.data
        user_info = User(name=registerForm.name.data,
                        username=registerForm.email.data,
                        password=registerForm.password.data,
                        role_id=2  #Consumer is 2nd role
                        )
        db.session.add(user_info)
        db.session.commit()


        # name=registerForm.name.data
    return render_template('register.html', registerForm=registerForm, name=name)




if __name__ == '__main__':
    app.run()
