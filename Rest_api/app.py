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
    print(f"Fetched user from DB: {user}")
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

@app.route('/users')
def users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, username, name, email FROM users"
    cursor.execute(query)
    users_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("users.html", users=users_list)

@app.route('/users/<int:id>')
def users_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, username, name, email FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    user = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("users.html", users=user)

@app.route('/api/users', methods=['GET'])
def users_api():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, username, name, email FROM users"
    cursor.execute(query)
    users_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users_list)

@app.route('/api/users', methods=['POST'])
def create_user_api():
    data = request.get_json(silent=True)
    if data and "username" in data and "password" in data and "name" in data:
        username = data.get("username")
        name = data.get("name")
        password = data.get("password")
        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = "INSERT INTO users (`username`, `password`, `name`) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, hashed_password, name))
            conn.commit()
            cursor.close()
            conn.close()
            user = get_user_from_db(username)
            return jsonify({"id": cursor.lastrowid, "status": "User created", "user": user}), 201
        
        except Exception as err:
            print(f"Error: {err}")
            return jsonify({"error": "Something went wrong. Sorry!"}), 500
    else:
        return jsonify({"error": "Missing critical data field"}), 422

@app.route('/api/users/<int:id>', methods=['GET'])
def users_by_id_api(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, username, name, email FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    user = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(user)

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json(silent=True)
    print(f"Received data for update: {data}")

    name = data.get('name')
    username = data.get('username')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if cursor.rowcount == 0:
            return jsonify({"error": "Användaren hittades inte"}), 404
        
        sql = """UPDATE users SET name = %s, username = %s WHERE id = %s"""

        cursor.execute(sql, (name, username, user_id))
    
        conn.commit()
    
        cursor.close()
        conn.close()

        return jsonify({"message": "Användare uppdaterad", "id": user_id}), 200

    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": err}), 400


if __name__ == '__main__':
    app.run(debug=True)
