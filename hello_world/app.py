from flask import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, Te23D World!"


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
def loogin():
    return """<form action="/submit" method="post">
            <label for="name">name:</label>
            <input type="text" id="name" name="name"><br>
            <label for="pasword">pasword:</label>
            <input type="password" id="pasword" name="pasword"><br>
            <input type="checkbox" id="checkbox" name="checkbox"><label for="checkbox">do you accept cookies</label> <br>
            <input type="submit" value="Submit">
        </form>"""

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '')
    pasword = request.form.get('pasword', '')
    checkbox = request.form.get('checkbox', False)
    return f'Received via POST: {name}, {pasword},  Checkbox: {checkbox}'

if __name__ == '__main__':
    app.run(debug=True)
