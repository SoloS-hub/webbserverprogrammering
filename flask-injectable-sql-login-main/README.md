# Flask SQL Injection Demonstration

⚠️ **WARNING**: This application contains **intentional security vulnerabilities** for educational purposes only. **DO NOT** use this code in production or deploy it on public servers.

## Purpose
This is a vulnerable Flask login application designed to demonstrate SQL injection attacks. The application intentionally uses unsafe SQL query construction to allow students to understand and practice identifying SQL injection vulnerabilities.

## What is SQL Injection?
SQL injection is a web security vulnerability that allows an attacker to interfere with database queries. By injecting malicious SQL code through user input, attackers can:
- Bypass authentication
- Access unauthorized data
- Modify or delete database records
- Execute administrative operations on the database

## Setup Instructions

### 1. Install Required Packages
```bash
pip install -r requirements.txt
```

### 2. Setup MySQL Database
1. Make sure MySQL server is running on your localhost
2. Run the SQL script to create the database and table:
   - Open MySQL command line or phpMyAdmin
   - Execute the SQL commands from `database_setup.sql`
   - This will create a database called `webbserv_injection_demo` with a `users` table and sample users

### 3. Configure Database Connection
Edit `injectable_app.py` and update the `DB_CONFIG` dictionary with your MySQL credentials:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Your MySQL username
    'password': '',  # Your MySQL password
    'database': 'webbserv_injection_demo'
}
```

### 4. Run the Application
```bash
python injectable_app.py
```

The application will run on `http://127.0.0.1:5000`

## Test Users
The database includes five test users:
- Username: `admin`, Password: `admin123`
- Username: `user1`, Password: `password`
- Username: `john_doe`, Password: `secure123`
- Username: `jane_smith`, Password: `mypass456`
- Username: `bob_wilson`, Password: `bobpass789`

## SQL Injection Examples
See `injections.txt` for example SQL injection payloads. Try these in the login form to see how SQL injection works:

## The Vulnerability
The vulnerable code in `injectable_app.py` directly concatenates user input into SQL queries:

```python
query = (
    "SELECT * FROM users WHERE username = '" + username + "' "
    "AND password = '" + password + "'"
)
```

This allows attackers to break out of the string context and inject arbitrary SQL code.

