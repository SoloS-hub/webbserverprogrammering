from flask import *
from functools import wraps
import time
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'your_secret_key'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'inlamning_1'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def start_timer():
    g.start_time = time.time()
    app.logger.info(f"Request started: {request.method} {request.path}")

@app.after_request
def log_request(response):
    duration = time.time() - g.start_time
    app.logger.info(f"Request ended: {request.method} {request.path} | Duration: {duration:.4f}s | Status: {response.status_code}")
    return response

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_user_from_db(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


@app.route('/hash')
def hash_user_password_manual():
    pwhash = generate_password_hash(request.args.get('p'))
    return pwhash

@app.route('/')
def home():
    if 'username' in session:
        return render_template("index.html", user_authenticated=True)
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        user = get_user_from_db(username)

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Login successful')
            return render_template("profile.html", username=session['username'], user_data=user)
        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for('home'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        hashed_password = generate_password_hash(password)

        user = get_user_from_db(username)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if user:
            flash('Username already exists')
            return redirect(url_for('create_account'))
        
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template("create_account.html")


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        about_me = request.form.get('about_me', '')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "UPDATE `users` SET `name`=%s,`email`=%s WHERE `username`=%s"
        cursor.execute(query, (name, email, session['username']))
        conn.commit()
        cursor.close()
        conn.close()
    
    user = get_user_from_db(session['username'])

    return render_template("profile.html", username=session['username'], user_data=user)


if __name__ == '__main__':
    app.run(debug=True)
