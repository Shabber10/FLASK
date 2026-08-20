"""
Day 06 Practice Application: College Student Management Portal with mysql-connector-python
==========================================================================================
Demonstrates complete raw MySQL Database CRUD operations in Flask using `mysql-connector-python`.
Uses the 'college' database and 'student' table (sname, sage, smarks, scity).
Includes manual form input and random student data generation.
"""

from flask import Flask, request, render_template_string, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import Error
import random

app = Flask(__name__)

# MySQL Database Configuration for 'college' database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'college',
    'port': 3306
}

def get_db_connection():
    """Helper to establish a MySQL connection to the 'college' database."""
    return mysql.connector.connect(**db_config)

def init_db():
    """Initializes the 'student' table in the 'college' database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sname VARCHAR(100) NOT NULL,
                sage INT NOT NULL,
                smarks DECIMAL(5, 2) NOT NULL,
                scity VARCHAR(100) NOT NULL
            ) ENGINE=InnoDB;
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ MySQL 'student' table in 'college' database initialized successfully.")
    except Error as e:
        print(f"⚠️ MySQL Connection Notice: {e}")

# HTML Template with Form and Random Data Generator
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>College Student Management Portal (mysql-connector-python)</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f4f7f6; color: #333; }
        .container { max-width: 950px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 12px; font-size: 26px; }
        .actions-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 15px; }
        form.add-form { display: grid; grid-template-columns: 2fr 1fr 1fr 1.5fr auto; gap: 10px; width: 100%; background: #f8f9fa; padding: 15px; border-radius: 6px; border: 1px solid #e9ecef; }
        input { padding: 10px; border: 1px solid #ced4da; border-radius: 5px; font-size: 14px; }
        button { background: #2ecc71; color: white; border: none; padding: 10px 18px; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 14px; transition: background 0.2s; }
        button:hover { background: #27ae60; }
        button.btn-random { background: #8e44ad; }
        button.btn-random:hover { background: #732d91; }
        button.delete { background: #e74c3c; padding: 6px 12px; font-size: 12px; }
        button.delete:hover { background: #c0392b; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 14px; text-align: left; border-bottom: 1px solid #e9ecef; }
        th { background: #34495e; color: white; font-weight: 600; }
        tr:hover { background-color: #f1f2f6; }
        .badge { background: #3498db; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; }
        .card-header { display: flex; justify-content: space-between; align-items: center; margin-top: 25px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 College Student Portal (MySQL `college.student`)</h1>
        
        <!-- CREATE FORM (MANUAL INPUT) -->
        <h3>Add New Student Manually</h3>
        <form class="add-form" action="/add-student" method="POST">
            <input type="text" name="sname" placeholder="Student Name (sname)" required>
            <input type="number" name="sage" placeholder="Age (sage)" min="15" max="100" required>
            <input type="number" step="0.01" name="smarks" placeholder="Marks (smarks)" min="0" max="100" required>
            <input type="text" name="scity" placeholder="City (scity)" required>
            <button type="submit">Add Student</button>
        </form>

        <!-- RANDOM VALUE GENERATOR BUTTON -->
        <div class="card-header">
            <h3>Registered Students List</h3>
            <form action="/add-random-student" method="POST" style="display:inline;">
                <button type="submit" class="btn-random">🎲 Generate & Insert Random Student</button>
            </form>
        </div>

        <!-- READ TABLE -->
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Student Name (sname)</th>
                    <th>Age (sage)</th>
                    <th>Marks (smarks)</th>
                    <th>City (scity)</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for std in students %}
                <tr>
                    <td><span class="badge">#{{ std.id }}</span></td>
                    <td><strong>{{ std.sname }}</strong></td>
                    <td>{{ std.sage }} yrs</td>
                    <td>{{ "%.2f"|format(std.smarks) }}</td>
                    <td>📍 {{ std.scity }}</td>
                    <td>
                        <form action="/delete-student/{{ std.id }}" method="POST" style="display:inline;">
                            <button type="submit" class="delete">Delete</button>
                        </form>
                    </td>
                </tr>
                {% else %}
                <tr><td colspan="6" style="text-align:center; padding: 25px; color: #7f8c8d;">No students found in `college.student` database. Add one manually or click 'Generate & Insert Random Student'!</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

# Demo In-Memory Storage if local MySQL server is offline
demo_students = [
    {"id": 1, "sname": "Aarav Sharma", "sage": 20, "smarks": 88.50, "scity": "Mumbai"},
    {"id": 2, "sname": "Ananya Verma", "sage": 21, "smarks": 92.00, "scity": "Delhi"},
    {"id": 3, "sname": "Rohan Mehta", "sage": 19, "smarks": 75.25, "scity": "Bangalore"}
]

# Lists for Random Student Generation
RANDOM_NAMES = ["Vikram Singh", "Neha Gupta", "Priya Patel", "Karan Malhotra", "Riya Sen", "Amitabh Das", "Sneha Rao", "Rahul Joshi"]
RANDOM_CITIES = ["Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad", "Jaipur", "Ahmedabad", "Kolkata", "Chennai"]

@app.route('/')
def index():
    """READ: Fetch all students from the 'student' table in 'college' database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, sname, sage, smarks, scity FROM student ORDER BY id DESC")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template_string(HTML_TEMPLATE, students=students)
    except Error:
        # Fallback for local testing if MySQL service isn't active
        return render_template_string(HTML_TEMPLATE, students=demo_students)

@app.route('/add-student', methods=['POST'])
def add_student():
    """CREATE: Insert new student manually from form."""
    sname = request.form.get('sname')
    sage = request.form.get('sage', type=int)
    smarks = request.form.get('smarks', type=float)
    scity = request.form.get('scity')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO student (sname, sage, smarks, scity) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (sname, sage, smarks, scity))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Database write notice: {e}")
        new_id = len(demo_students) + 1
        demo_students.append({"id": new_id, "sname": sname, "sage": sage, "smarks": smarks, "scity": scity})

    return redirect(url_for('index'))

@app.route('/add-random-student', methods=['POST'])
def add_random_student():
    """CREATE: Insert random student data into MySQL."""
    sname = random.choice(RANDOM_NAMES)
    sage = random.randint(18, 24)
    smarks = round(random.uniform(50.0, 99.0), 2)
    scity = random.choice(RANDOM_CITIES)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO student (sname, sage, smarks, scity) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (sname, sage, smarks, scity))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Database random insert notice: {e}")
        new_id = len(demo_students) + 1
        demo_students.append({"id": new_id, "sname": sname, "sage": sage, "smarks": smarks, "scity": scity})

    return redirect(url_for('index'))

@app.route('/delete-student/<int:std_id>', methods=['POST'])
def delete_student(std_id):
    """DELETE: Remove student record."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE id = %s", (std_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Error:
        global demo_students
        demo_students = [s for s in demo_students if s['id'] != std_id]

    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🚀 Starting College Student Portal on http://127.0.0.1:5000")
    init_db()
    app.run(debug=True)

