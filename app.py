from flask import Flask, render_template, session, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy
#from flask_bcrypt import Bcrypt

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('homepage.html')

@app.route('/results')
def research_results():
    return render_template('results.html')

@app.route('/reg-c')
def signupC():
    return render_template('signup-supplier.html')

if __name__ == '__main__':
    app.run()
