from __init__ import __version__
import logging
import datetime
from flask import Flask, redirect, url_for, render_template, request, session, flash

# simple log
logger_name = 'app'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
# location w.r.t. working directory that calls this Flask app
hdler = logging.FileHandler(f'{logger_name}.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hdler.setFormatter(formatter)
logger.addHandler(hdler)

app = Flask(__name__)

# secret key for session
# set the secret key to some random bytes
# keep this really secret!
# set session lifetime if needed, defaults to 31 days
app.secret_key = b'_r@nd0m'
app.permanent_session_lifetime = datetime.timedelta(days=7)


# simple endpoint
@app.get('/')
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


# learning GET/POST
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        session['user'] = user
        return redirect(url_for('user'))
    else:
        if 'user' in session.keys():
            return redirect(url_for('user'))
        return render_template('login.html')

@app.get('/user')
def user():
    if 'user' in session:
        user = session['user'] 
        return render_template('user.html', user=user)
    else:
        return redirect(url_for('login'))

@app.get('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        session.pop('user', None)
        flash(f'You have been logged out, {user}!', category='info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    logger.debug(f'Running version {__version__}')
    app.run(debug=True, port=5000)