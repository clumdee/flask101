from __init__ import __version__
import os
import datetime
from flask import Flask, redirect, url_for, render_template, request, session, flash
from logger import logger
from db import db, Users


app = Flask(__name__)

# secret key for session
# set the secret key to some random bytes
# keep this really secret!
# set session lifetime if needed, defaults to 31 days
app.secret_key = b'_r@nd0m'
app.permanent_session_lifetime = datetime.timedelta(days=7)

# prepare to init database
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # optional, suppress noti


# initialize SQLAlchemy object
db.app = app
db.init_app(app)


# simple endpoint
@app.get('/')
@app.get('/home')
def home():
    logger.debug('calling home')
    # return 'This is a home page'
    content = dict()
    return render_template('index.html', content=content)

# pass part of URL as an argument
# @app.get('/<name>-<lastname>')
# def user(name, lastname):
#     # return f'Hello {name}!'
#     content = {'name':name, 'lastname':lastname}
#     return render_template('index.html', content=content)

# straight redirect / redirect with url_for
@app.get('/admin')
def admin():
    # return redirect('/not-you')
    return redirect(url_for('user', name='not admin'))

# view Users table
@app.route('/view')
def view():
    return render_template('view.html', values=Users.query.all())

# learning GET/POST
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        session['user'] = user

        # check if a user exists and retrieve their email
        # create a new user record with NULL email if not exists
        found_user = Users.query.filter_by(name=user).first()
        if found_user:
            session['email'] = found_user.email
        else:
            usr = Users(user, None)
            db.session.add(usr)
            db.session.commit()

        flash('Login successful!')
        return redirect(url_for('user'))
    else:
        if 'user' in session.keys():
            flash('Already logged in!')
            return redirect(url_for('user'))
        return render_template('login.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'user' in session:
        user = session['user'] 
        
        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email

            # save user's email to database
            found_user = Users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()

            flash('Email was saved!')
        else:
            if 'email' in session:
                email = session['email']
            else:
                email = None

        return render_template('user.html', user=user, email=email)
    else:
        flash('You are not logged in!')
        return redirect(url_for('login'))

@app.get('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        session.pop('user', None)
        session.pop('email', None)
        flash(f'You have been logged out, {user}!', category='info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    logger.debug(f'Running version {__version__}')
    # create (or read existing) database before start
    db.create_all()
    app.run(debug=True, port=5000)