# Import all Flask utilities (request, session, render_template, etc.)
from flask import *
from functools import wraps  # For decorator wrapper functionality
import time  # For timing requests
import mysql.connector  # MySQL database connection
from werkzeug.security import generate_password_hash, check_password_hash  # Password hashing
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # JWT authentication


# Initialize Flask application
app = Flask(__name__)
# Set JWT secret key for token validation
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)  # Enable JWT support

# MySQL database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'inlamning_1'
}

# @app.before_request
# def start_timer():
#     g.start_time = time.time()
#     app.logger.info(f"Request started: {request.method} {request.path}")

# @app.after_request
# def log_request(response):
#     duration = time.time() - g.start_time
#     app.logger.info(f"Request ended: {request.method} {request.path} | Duration: {duration:.4f}s | Status: {response.status_code}")
#     return response

# Helper function to establish database connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Retrieve a user from the database by username
def get_user_from_db(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Return results as dictionaries

        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))  # Use parameterized query to prevent SQL injection
        user = cursor.fetchone()  # Get first result
        
        print(f"Fetched user from DB: {user}")
        return user
        
    except Exception as err:
        print(f"Error fetching user from DB: {err}")
        return None
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()



@app.route('/hash')
def hash_user_password_manual():
    # Route to hash a password (for testing/manual purposes)
    pwhash = generate_password_hash(request.args.get('p'))
    return pwhash

# Home page route - checks if user is already logged in
@app.route('/')
def home():
    return render_template("index.html")

# API login endpoint - returns JWT token for authenticated users
@app.route('/api/login', methods=['POST'])
def api_login():
    login_info = request.get_json(silent=True)  # Parse JSON request body

    username = login_info.get('username')
    password = login_info.get('password')

    user = get_user_from_db(username)

    # Verify credentials and generate JWT token
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid username or password"}), 401

# API endpoint to get all users - requires valid JWT token
@app.route('/api/users', methods=['GET'])
@jwt_required()
def users_api():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all users (excluding passwords)
    query = "SELECT id, username, name, email FROM users"
    cursor.execute(query)
    users_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(users_list)

# API endpoint to create a new user - requires valid JWT token
@app.route('/api/users', methods=['POST'])
@jwt_required()
def create_user_api():
    data = request.get_json(silent=True)
    # Validate required fields are present
    if data and "username" in data and "password" in data and "name" in data:
        username = data.get("username")
        name = data.get("name")
        password = data.get("password")
        hashed_password = generate_password_hash(password)  # Hash password

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            # Insert new user into database
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
        # Return 422 (Unprocessable Entity) if required fields missing
        return jsonify({"error": "Missing critical data field"}), 422

# API endpoint to get a specific user by ID - requires valid JWT token
@app.route('/api/users/<int:id>', methods=['GET'])
@jwt_required()
def users_by_id_api(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch user by ID (excluding password)
    query = "SELECT id, username, name, email FROM users WHERE id = %s"

    cursor.execute(query, (id,))

    user = cursor.fetchall()

    cursor.close()
    conn.close()
    # Return 404 if user not found
    if not user:
        print(f"User with ID {id} not found")
        return jsonify({"error": "Användaren hittades inte"}), 404
    return jsonify(user)

# API endpoint to update user information - requires valid JWT token
@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json(silent=True)
    print(f"Received data for update: {data}")

    name = data.get('name')
    username = data.get('username')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if user exists
        sql = """SELECT * FROM users WHERE id = %s"""
        cursor.execute(sql, (user_id,))
        user = cursor.fetchone()

        # Update user's name and username
        sql = """UPDATE users SET name = %s, username = %s WHERE id = %s"""

        cursor.execute(sql, (name, username, user_id))

        sql = """SELECT id, username, name, email FROM users WHERE id = %s"""
        cursor.execute(sql, (user_id,))
        user = cursor.fetchone()

        conn.commit()  # Save changes


        # Return 404 if user doesn't exist
        if not user:
            return jsonify({"error": "Användaren hittades inte"}), 404

        return jsonify({"message": "Användare uppdaterad", "user": user}), 200

    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": err}), 400
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

# API endpoint to get current authenticated user's info - requires valid JWT token
@app.route('/api/me', methods=['GET'])
@jwt_required()
def get_user_from_token():
    # Extract username from JWT token
    current_user = get_jwt_identity()
    print(f"curren user is {current_user}")
    user_info = get_user_from_db(current_user)
    user_info.pop('password', None)  # Remove password from response for security
    return jsonify(user_info), 200

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
