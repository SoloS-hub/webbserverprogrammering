from flask import *
import os
import json

app = Flask(__name__)

app.secret_key = 'your_secret_key'

users = {
}

with open('users.json') as f:
    users = json.load(f)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f"Search query: {query}"

@app.route('/add')
def add():
    a = request.args.get('a', default=0, type=int)
    b = request.args.get('b', default=0, type=int)
    return f"a + b = {a + b}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if users.get(username) == password:
            session['username'] = username
            return render_template("profile.html", username=session['username'])
        return 'Invalid username or password'
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username in users:
            return 'Username already exists'
        users[username] = password
        json.dump(users, open('users.json', 'w'))
        return redirect(url_for('login'))
    return render_template("create_account.html")

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template("profile.html", username=session['username'])
    return redirect(url_for('login'))

TOOLS_INFO = [
    {"name": "hammer", "price": 9.99, "brand": "Acme", "stock": 12, "category": "hand tool"},
    {"name": "drill", "price": 49.99, "brand": "Bosch", "stock": 5, "category": "power tool", "battery": "18V"},
    {"name": "screwdriver_set", "price": 14.50, "brand": "Stanley", "stock": 20, "pieces": 10}
]

@app.route('/bob')
def bob():
    return render_template("bob.html", tools=TOOLS_INFO)

@app.route('/view_users')
def view_users():
    return render_template("users.html", users=users.keys())
list(users.keys())


if __name__ == '__main__':
    app.run(debug=True)
