"""
Day 06 Practice Application: Employee Portal with mysql-connector-python
========================================================================
Demonstrates complete raw MySQL Database CRUD operations in Flask using `mysql-connector-python`.
Includes fallback support for local testing.
"""

from flask import Flask, request, render_template_string, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'flask_demo_db',
    'port': 3306
}

def get_db_connection():
    """Helper to establish a MySQL connection."""
    return mysql.connector.connect(**db_config)

def init_db():
    """Initializes the employees table in MySQL."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                salary DECIMAL(10, 2) NOT NULL DEFAULT 0.00
            ) ENGINE=InnoDB;
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ MySQL 'employees' table initialized successfully.")
    except Error as e:
        print(f"⚠️ MySQL Connection Notice: {e}")

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Employee Management Portal (mysql-connector-python)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f8f9fa; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        form { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr auto; gap: 10px; margin-bottom: 30px; }
        input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #2ecc71; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }
        button.delete { background: #e74c3c; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #34495e; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>👨‍💼 Employee Portal (mysql-connector-python CRUD)</h1>
        
        <!-- CREATE FORM -->
        <h3>Add New Employee</h3>
        <form action="/add-employee" method="POST">
            <input type="text" name="first_name" placeholder="First Name" required>
            <input type="text" name="last_name" placeholder="Last Name" required>
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="number" step="0.01" name="salary" placeholder="Salary ($)" required>
            <button type="submit">Add Employee</button>
        </form>

        <!-- READ TABLE -->
        <h3>Current Employees List</h3>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Salary</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for emp in employees %}
                <tr>
                    <td>{{ emp.id }}</td>
                    <td>{{ emp.first_name }} {{ emp.last_name }}</td>
                    <td>{{ emp.email }}</td>
                    <td>${{ "%.2f"|format(emp.salary) }}</td>
                    <td>
                        <form action="/delete-employee/{{ emp.id }}" method="POST" style="display:inline;">
                            <button type="submit" class="delete">Delete</button>
                        </form>
                    </td>
                </tr>
                {% else %}
                <tr><td colspan="5" style="text-align:center;">No employees found in database. Add one above!</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

# Demo In-Memory Storage if local MySQL server is offline
demo_employees = [
    {"id": 1, "first_name": "Alice", "last_name": "Smith", "email": "alice@example.com", "salary": 85000.00},
    {"id": 2, "first_name": "Bob", "last_name": "Jones", "email": "bob@example.com", "salary": 62000.00}
]

@app.route('/')
def index():
    """READ: Fetch all employees."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, first_name, last_name, email, salary FROM employees ORDER BY id DESC")
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template_string(HTML_TEMPLATE, employees=employees)
    except Error:
        # Fallback for local testing if MySQL service isn't active
        return render_template_string(HTML_TEMPLATE, employees=demo_employees)

@app.route('/add-employee', methods=['POST'])
def add_employee():
    """CREATE: Insert new employee."""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    salary = request.form.get('salary', type=float, default=0.00)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO employees (first_name, last_name, email, salary) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (first_name, last_name, email, salary))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Database write notice: {e}")
        new_id = len(demo_employees) + 1
        demo_employees.append({"id": new_id, "first_name": first_name, "last_name": last_name, "email": email, "salary": salary})

    return redirect(url_for('index'))

@app.route('/delete-employee/<int:emp_id>', methods=['POST'])
def delete_employee(emp_id):
    """DELETE: Remove employee record."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Error:
        global demo_employees
        demo_employees = [e for e in demo_employees if e['id'] != emp_id]

    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🚀 Starting Flask App with mysql-connector-python on http://127.0.0.1:5000")
    init_db()
    app.run(debug=True)
