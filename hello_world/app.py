from flask import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/user/<username>')
def show_user_profile(username):
    return f"User: {username}"

@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f"Search query: {query}"

@app.route('/add')
def add():
    a = request.args.get('a', default=0, type=int)
    b = request.args.get('b', default=0, type=int)
    return f"a + b = {a + b}"

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '')
    pasword = request.form.get('pasword', '')
    checkbox = request.form.get('checkbox', False)
    return f'Received via POST: {name}, {pasword},  Checkbox: {checkbox}'

TOOLS_INFO = [
    {"name": "hammer", "price": 9.99, "brand": "Acme", "stock": 12, "category": "hand tool"},
    {"name": "drill", "price": 49.99, "brand": "Bosch", "stock": 5, "category": "power tool", "battery": "18V"},
    {"name": "screwdriver_set", "price": 14.50, "brand": "Stanley", "stock": 20, "pieces": 10}
]

@app.route('/bob')
def bob():
    return render_template("bob.html", tools=TOOLS_INFO)

if __name__ == '__main__':
    app.run(debug=True)
