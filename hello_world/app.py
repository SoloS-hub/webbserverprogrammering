from flask import *
import os
import json

app = Flask(__name__)

app.secret_key = 'your_secret_key'

users = {}

with open('users.json', "r") as f:
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
            user_file = os.path.join("user_data", f"{session['username']}.json")
            if os.path.exists(user_file):
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
            return render_template("profile.html", username=session['username'], user_data=user_data)
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
        # create a user file in user_data folder
        save_users(username)
        return redirect(url_for('login'))
    return render_template("create_account.html")

def save_users(username):
    with open(os.path.join("static/user_template.json"), 'r') as f:
        user_data = json.load(f)
    with open(os.path.join("user_data", f"{username}.json"), 'w') as f:
        user_data['username'] = username
        json.dump(user_data, f)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        about_me = request.form.get('about_me', '')
        # return f"Name: {name}, Email: {email}, About Me: {about_me}"
        user_file = os.path.join("user_data", f"{session['username']}.json")
        if os.path.exists(user_file):
            with open(user_file, 'r') as f:
                user_data = json.load(f)
            user_data['name'] = name
            user_data['email'] = email
            user_data['about_me'] = about_me
            with open(user_file, 'w') as f:
                json.dump(user_data, f)
    if 'username' in session:
        user_file = os.path.join("user_data", f"{session['username']}.json")
        if os.path.exists(user_file):
            with open(user_file, 'r') as f:
                user_data = json.load(f)
        return render_template("profile.html", username=session['username'], user_data=user_data)
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


if __name__ == '__main__':
    app.run(debug=True)
