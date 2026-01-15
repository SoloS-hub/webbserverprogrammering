# Importing Necessary Modules
from flask import *
app = Flask(__name__)

# Create a Main route here
@app.route('/')
def input():
    return render_template('Temp.html')
  
# Create other routes here. 
# host/passing will be the website link
@app.route('/passing', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        result = request.form
        
        # Send result data to result_data HTML file
        return render_template("result_data.html", result=result)


# main route to start with
if __name__ == '__main__':
    app.run(debug=True)