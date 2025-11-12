from flask import Flask, render_template
import mysql.connector


app = Flask(__name__)

app.secret_key = 'your_secret_key'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'un_global_goals'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM goals"
    cursor.execute(query)
    goals = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('home.html', goals=goals)

@app.route('/goals/<id>')
def view_goal(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM targets WHERE goal_id = %s"
    cursor.execute(query, (id,))
    targets = cursor.fetchall()
    
    query = "SELECT * FROM goals WHERE id = %s"
    cursor.execute(query, (id,))
    goal = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('goal.html', targets=targets, goal=goal)

if __name__ == '__main__':
    app.run(debug=True)
