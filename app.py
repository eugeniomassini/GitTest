from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
@app.route('/homepage')
def homepage():
    return render_template('base.html')

@app.route('/signin')
def login():
    return render_template('signin.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/testHome')
def testHomepage():
    return render_template('Homepage.html')

@app.route('/reg-c')
def signupC():
    return render_template('signup-consumer.html')

if __name__ == '__main__':
    app.run()
