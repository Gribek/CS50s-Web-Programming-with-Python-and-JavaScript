import os

from flask import Flask, session, render_template, request, redirect, \
    url_for, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

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


@app.route('/search', methods=('GET', 'POST'))
def search():
    """Search for the book"""

    if request.method == 'POST':

        phrase = request.form.get('search').lower()
        column = request.form.get('column')
        error = None
        print(phrase, column)

        if not phrase:
            error = 'Enter search phrase'
        elif column not in ['title', 'author', 'isbn']:
            error = 'Choose search option'

        if error is None:
            sql = 'SELECT * FROM books where LOWER({}) LIKE :ph'.format(column)
            books = db.execute(sql, {'column': column, 'ph': f'%{phrase}%'})
            return render_template('search.html', books=books)

        flash(error)

    return render_template('search.html')


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


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Log user in"""

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        user = db.execute('SELECT * FROM users WHERE username=:username',
                          {'username': username}).fetchone()
        if user is None or not check_password_hash(user['password'], password):
            error = 'Wrong username or password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
