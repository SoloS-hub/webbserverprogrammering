from flask import *
from functools import wraps
import time
import mysql.connector

app = Flask(__name__)

app.secret_key = 'your_secret_key'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)


@app.before_request
def start_timer():
    g.start_time = time.time()
    app.logger.info(f"Request started: {request.method} {request.path}")

@app.after_request
def log_request(response):
    duration = time.time() - g.start_time
    app.logger.info(f"Request ended: {request.method} {request.path} | Duration: {duration:.4f}s | Status: {response.status_code}")
    return response

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'inlamning_1'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

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

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        query = "SELECT username, name, email FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and user['password'] == password:
            session['username'] = username
            flash('Login successful')
            return render_template("profile.html", username=session['username'], user_data=user_data)
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
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        if user:
            flash('Username already exists')
            return redirect(url_for('create_account'))
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
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
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT username, name, email FROM users WHERE username = %s"
        cursor.execute(query, (session['username'],))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template("profile.html", username=session['username'], user_data=user_data)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
