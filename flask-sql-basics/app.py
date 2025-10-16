from flask import Flask, render_template, request, redirect, url_for
import os
import mysql.connector # den här modulen behövs för att skapa en databasanslutning

app = Flask(__name__)

# Denna databas konfigurationsdata kan också lagras i environmentvariabler 
# för bättre säkerhet.

# enklast
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'classicmodels'
}

# säkrare
# DB_CONFIG = {
#     'host': os.getenv('DB_HOST', 'localhost'),
#     'user': os.getenv('DB_USER', 'root'),
#     'password': os.getenv('DB_PASSWORD', ''),
#     'database': os.getenv('DB_NAME', 'classicmodels'),
# }

def get_db_connection():
    """
    Skapar en databasanslutning och returnerar den.
    """
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def product_lines():
    conn = get_db_connection()
    # Skapar en cursor för att köra SQL-frågor
    cursor = conn.cursor(dictionary=True)
    # Hämtar alla productlines
    cursor.execute('SELECT productLine, textDescription FROM productlines')
    lines = cursor.fetchall()
    cursor.close()
    conn.close()
    # renderar en mall med alla productlines
    return render_template('product_lines.html', lines=lines)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    product_line = request.args.get('product_line', '')
    if request.method == 'POST':
        productCode = request.form['productCode']
        productName = request.form['productName']
        productLine = request.form['productLine']
        productScale = request.form['productScale']
        productVendor = request.form['productVendor']
        productDescription = request.form['productDescription']
        quantityInStock = request.form['quantityInStock']
        buyPrice = request.form['buyPrice']
        MSRP = request.form['MSRP']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO products (productCode, productName, productLine, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (productCode, productName, productLine, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('products', product_line=productLine))
    return render_template('add_product.html', productLine=product_line)

@app.route('/products/<product_line>')
def products(product_line):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Hämtar alla produkter för en given productline
    cursor.execute('SELECT productCode, productName, productLine FROM products WHERE productLine = %s', (product_line,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    # renderar en mall med alla produkter
    return render_template('products.html', products=products, product_line=product_line)

# Denna route hanterar tillägg av anställda
@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        jobTitle = request.form['jobTitle']
        employee_number = request.form['employeeNumber']
        conn = get_db_connection()
        cursor = conn.cursor()
        # INSERT lägger till en rad med en ny anställd i tabellen employees
        cursor.execute(
            """
            INSERT INTO employees (firstName, lastName, email, jobTitle, officeCode, reportsTo, employeeNumber)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (firstName, lastName, email, jobTitle, 1, None, employee_number)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('employees'))
    return render_template('add_employee.html')

@app.route('/employees')
def employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Hämtar alla anställda
    cursor.execute('SELECT employeeNumber, firstName, lastName, email, jobTitle FROM employees')
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    # renderar en mall med alla anställda
    return render_template('employees.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)