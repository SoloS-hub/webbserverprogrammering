from flask import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/subpage')
def subpage():
    return render_template("subpage.html", header="Subpage Header", content="This is the subpage content.")

@app.route('/test')
def test():
    return render_template("subpage.html", header="Test Page Header", content="This is the test page content.")

@app.route('/test2')
def test2():
    return render_template("subpage.html", header="Test2 Page Header", content="This is the test2 page content.")

print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)