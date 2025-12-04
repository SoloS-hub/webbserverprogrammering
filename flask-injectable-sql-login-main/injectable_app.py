from flask import Flask, render_template, request, session
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'webbserv_injection_demo',
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Fel vid anslutning till MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Vulnerable login endpoint intentionally concatenating SQL."""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        connection = get_db_connection()
        if connection is None:
            return "Databasanslutning misslyckades", 500

        try:
            cursor = connection.cursor(dictionary=True)

            # INTENTIONALLY VULNERABLE: unsafely interpolate user input into SQL
            query = (
                "SELECT * FROM users WHERE username = '" + username + "' "
                "AND password = '" + password + "'"
            )
            print(f"Executing query: {query}")  # For debugging purposes
            cursor.execute(query)
            user = cursor.fetchone()

            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['name'] = user['name']
                return f'Inloggning lyckades! Välkommen, {user["name"]}! <a href="/logout">Logga ut</a>'
            else:
                return ('Ogiltigt användarnamn eller lösenord', 401)

        except Error as e:
            print(f"Databasfel: {e}")
            return "Databasfel inträffade", 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/logout')
def logout():
    session.clear()
    return 'Du har loggats ut.'

if __name__ == '__main__':
    app.run(debug=True)
