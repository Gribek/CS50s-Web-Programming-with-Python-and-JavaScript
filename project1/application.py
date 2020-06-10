import os
import requests
from flask import Flask, session, render_template, request, redirect, \
    url_for, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

# Goodreads api key
API_KEY = 'd9cHhV5POr5Gvm21S6Hmsw'

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
    """Home page"""
    return render_template('index.html')


@app.route('/search', methods=('GET', 'POST'))
def search():
    """Search for the book"""

    if request.method == 'POST':

        # Get user input
        phrase = request.form.get('search').lower()
        column = request.form.get('column')
        error = None

        # Check user input
        if not phrase:
            error = 'Enter search phrase'
        elif column not in ['title', 'author', 'isbn']:
            error = 'Choose search option'

        # Search for books that match the query
        if error is None:
            sql = 'SELECT * FROM books where LOWER({}) LIKE :ph'.format(column)
            books = db.execute(sql, {'column': column, 'ph': f'%{phrase}%'})
            return render_template('search.html', books=books)

        flash(error)

    return render_template('search.html')


@app.route('/book_page/<int:book_id>')
def book_page(book_id):
    """Display information about the selected book"""

    # Get information about the book form database
    book = db.execute('SELECT * FROM books WHERE id = :id',
                      {'id': book_id}).fetchone()

    # Get reviews submitted by users
    reviews = db.execute('SELECT * FROM reviews WHERE book_id=:id',
                         {'id': book_id}).fetchall()

    # Get data form goodreads api
    result = requests.get('https://www.goodreads.com/book/review_counts.json',
                          params={'key': API_KEY, 'isbns': book.isbn})
    if result.status_code != 200:
        goodreads = None
    else:
        data = result.json()['books'][0]
        goodreads = data['average_rating'], data['work_ratings_count']

    return render_template('book_page.html', book=book, reviews=reviews,
                           goodreads=goodreads)


@app.route('/add_review/<int:book_id>', methods=('GET', 'POST'))
def add_review(book_id):
    """Add review about the selected book"""

    book = db.execute('SELECT * FROM books WHERE id = :id',
                      {'id': book_id}).fetchone()

    # Get user input
    if request.method == 'POST':
        rating = request.form.get('rating')
        opinion = request.form.get('opinion')
        error = None

        # Check user input
        if not rating:
            error = 'Rate the book'
        elif not opinion:
            error = 'Write down your opinion'

        # Check if user has not rated this book before
        check_rewiev = db.execute(
            'SELECT * FROM reviews WHERE book_id = :b_id AND user_id = :u_id',
            {'b_id': book.id, 'u_id': session['user_id']}).fetchone()
        if check_rewiev is not None:
            error = 'You have already submitted review for this book'

        # If no error save review to db
        if error is None:
            db.execute(
                'INSERT INTO reviews (rating, opinion, user_id, book_id) '
                'VALUES (:rating, :opinion, :user_id, :book_id)',
                {'rating': rating, 'opinion': opinion,
                 'user_id': session['user_id'], 'book_id': book.id})
            db.commit()
            return redirect(url_for('book_page', book_id=book.id))

        flash(error)

    return render_template('add_review.html', book=book)


@app.route('/app/<string:isbn>')
def goodreads_api(isbn):
    """Return data about the selected book in json format"""

    # Get book data form db
    book = db.execute('SELECT * FROM books WHERE isbn=:isbn',
                      {'isbn': isbn}).fetchone()

    # Make sure book exists in database
    if book is None:
        return jsonify({'error': 'ISBN not in database'}), 404

    # Get information about reviews from db
    review_count = db.execute('SELECT COUNT(*) FROM reviews where book_id=:id',
                              {'id': book.id}).fetchone()[0]
    avr_score = db.execute('SELECT AVG(rating) FROM reviews where book_id=:id',
                           {'id': book.id}).fetchone()[0]

    # Return the data in json format
    return jsonify({'title': book.title, 'author': book.author,
                    'year': book.year, 'isbn': book.isbn,
                    'review_count': review_count,
                    'average_score': float(avr_score)})


@app.route('/register', methods=('GET', 'POST'))
def register():
    """Register user"""

    # Get user input
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repeated_password = request.form.get('repeated_password')

        error = None

        # Check user input
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif password != repeated_password:
            error = 'Both passwords must be the same'
        elif db.execute('SELECT id FROM users WHERE username=:username',
                        {'username': username}).fetchone() is not None:
            error = f'Username {username} already exists'

        # Create new user if no error occurred
        if error is None:
            db.execute('INSERT INTO users (username, password) '
                       'VALUES (:username, :password)',
                       {'username': username,
                        'password': generate_password_hash(password)})
            db.commit()
            return redirect(url_for('login'))

        flash(error)

    return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Log user in"""

    # Get user input
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        # Make sure that username and password match
        user = db.execute('SELECT * FROM users WHERE username=:username',
                          {'username': username}).fetchone()
        if user is None or not check_password_hash(user['password'], password):
            error = 'Wrong username or password'

        # Log in user
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Log user out"""
    session.clear()
    return redirect(url_for('index'))
