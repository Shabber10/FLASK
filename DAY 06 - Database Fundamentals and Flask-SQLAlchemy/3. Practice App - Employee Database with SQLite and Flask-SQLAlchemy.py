"""
===============================================================================
Day 06 Practice Script: Employee Directory Database Application
===============================================================================
This script demonstrates:
1. Setting up an SQLite database connection using Flask-SQLAlchemy 3.x.
2. Defining ORM Model classes (`Employee`) with column data types and constraints.
3. Performing CRUD operations using modern SQLAlchemy 2.0 syntax (`db.select()`, `db.session.get()`).
4. Implementing transaction safety using `db.session.rollback()`.
5. Exposing both a web UI and a RESTful JSON API.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Employee Database with SQLite and Flask-SQLAlchemy.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import datetime
from flask import Flask, jsonify, request, render_template_string, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day06-sqlalchemy-masterclass-secret'
# Configure local SQLite database file path (stored inside instance/ or working dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy extension instance
db = SQLAlchemy(app)


# =============================================================================
# 1. Employee ORM Model Definition
# =============================================================================
class Employee(db.Model):
    """ORM Model representing the 'employees' database table."""
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    department = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        """Helper method to serialize model instance to a JSON dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "salary": self.salary,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


# Automatically create SQL tables & pre-seed initial sample data on app startup
with app.app_context():
    db.create_all()
    
    # Check if table is empty using SQLAlchemy 2.0 select statement
    first_record = db.session.execute(db.select(Employee)).scalars().first()
    if not first_record:
        print("🌱 Pre-seeding initial employee records into SQLite database...")
        sample_emps = [
            Employee(name="Alice Smith", email="alice@company.com", department="Engineering", salary=85000.0),
            Employee(name="Bob Jones", email="bob@company.com", department="Marketing", salary=62000.0),
            Employee(name="Charlie Brown", email="charlie@company.com", department="Sales", salary=71000.0)
        ]
        db.session.add_all(sample_emps)
        db.session.commit()
        print("✅ Sample data pre-seeded successfully!")


# =============================================================================
# 2. HTML UI Template String
# =============================================================================
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 06 Employee Directory</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 30px; background: #f4f6f9; color: #333; }
        .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); max-width: 850px; margin: auto; }
        h2 { color: #2c3e50; margin-top: 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; border-bottom: 1px solid #e9ecef; text-align: left; }
        th { background-color: #2c3e50; color: white; }
        .btn { background: #27ae60; color: white; padding: 10px 16px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
        .btn:hover { background: #219150; }
        .form-inline { display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }
        .form-inline input { padding: 10px; border: 1px solid #ccc; border-radius: 4px; flex: 1; min-width: 150px; }
        .delete-btn { color: #e74c3c; font-weight: bold; text-decoration: none; }
        .delete-btn:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📊 Employee Directory System (Day 06)</h2>

        <!-- Form for Adding New Employees -->
        <form class="form-inline" method="POST" action="/employees/add">
            <input type="text" name="name" placeholder="Full Name" required>
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="text" name="department" placeholder="Department" required>
            <input type="number" step="0.01" name="salary" placeholder="Salary ($)" required>
            <button class="btn" type="submit">Add Employee</button>
        </form>

        <!-- Table Displaying Database Rows -->
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Department</th>
                    <th>Salary</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for e in employees %}
                <tr>
                    <td>{{ e.id }}</td>
                    <td><strong>{{ e.name }}</strong></td>
                    <td>{{ e.email }}</td>
                    <td>{{ e.department }}</td>
                    <td>${{ "%.2f"|format(e.salary) }}</td>
                    <td><a class="delete-btn" href="/employees/delete/{{ e.id }}">Delete</a></td>
                </tr>
                {% else %}
                <tr><td colspan="6">No employees found in database.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""


# =============================================================================
# 3. Web UI Routes (HTML)
# =============================================================================
@app.route('/')
def index():
    """Renders HTML Employee Directory listing all employees."""
    stmt = db.select(Employee).order_by(Employee.id.desc())
    emps = db.session.execute(stmt).scalars().all()
    return render_template_string(INDEX_HTML, employees=emps)


@app.route('/employees/add', methods=['POST'])
def add_employee_form():
    """Handles HTML Form Submission to create a new Employee record."""
    try:
        emp = Employee(
            name=request.form['name'],
            email=request.form['email'],
            department=request.form['department'],
            salary=float(request.form['salary'])
        )
        db.session.add(emp)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"❌ [DB ERROR] Rollback triggered: {e}")
        
    return redirect(url_for('index'))


@app.route('/employees/delete/<int:emp_id>')
def delete_employee_form(emp_id):
    """Deletes an Employee record by Primary Key ID."""
    emp = db.session.get(Employee, emp_id)
    if emp:
        db.session.delete(emp)
        db.session.commit()
    return redirect(url_for('index'))


# =============================================================================
# 4. RESTful JSON API Routes
# =============================================================================
@app.route('/api/employees', methods=['GET'])
def list_employees_api():
    """API Endpoint returning all employees as JSON."""
    stmt = db.select(Employee).order_by(Employee.id)
    emps = db.session.execute(stmt).scalars().all()
    return jsonify([e.to_dict() for e in emps]), 200


@app.route('/api/employees', methods=['POST'])
def create_employee_api():
    """API Endpoint creating a new employee from JSON payload."""
    data = request.get_json(silent=True) or {}
    if not all(k in data for k in ('name', 'email', 'department', 'salary')):
        return jsonify({"error": "Bad Request", "message": "Missing required fields"}), 400

    try:
        emp = Employee(
            name=data['name'],
            email=data['email'],
            department=data['department'],
            salary=float(data['salary'])
        )
        db.session.add(emp)
        db.session.commit()
        return jsonify(emp.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database Error", "message": str(e)}), 400


# =============================================================================
# 5. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 06 Employee Directory Application...")
    print("🌐 Open Web UI at: http://127.0.0.1:5000/")
    print("📡 Test REST API at: http://127.0.0.1:5000/api/employees")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
