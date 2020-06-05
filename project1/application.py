import os

from flask import Flask, session, render_template, request, redirect, url_for, \
    flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    return 'Project 1: TODO'


@app.route('/register', methods=('GET', 'POST'))
def register():
    """Register user"""

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repeated_password = request.form.get('repeated_password')

        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif password != repeated_password:
            error = 'Both passwords must be the same'
        elif db.execute('SELECT id FROM users WHERE username=:username',
                        {'username': username}).fetchone() is not None:
            error = f'Username {username} already exists'

        if error is None:
            db.execute('INSERT INTO users (username, password) '
                       'VALUES (:username, :password)',
                       {'username': username,
                        'password': generate_password_hash(password)})
            db.commit()
            return redirect(url_for('index'))

        flash(error)

    return render_template('register.html')
