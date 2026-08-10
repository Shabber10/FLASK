"""
Day 06 Practice Application: Employee Database Management System
================================================================
This application demonstrates:
1. Setting up SQLite database with Flask-SQLAlchemy 3.x.
2. Defining ORM Models with data constraints and default values.
3. Performing CRUD operations using SQLAlchemy 2.0 db.select() syntax.
4. Implementing transaction safety with db.session.rollback().
5. Exposing both HTML UI and RESTful JSON API endpoints.
"""

from flask import Flask, jsonify, request, render_template_string, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day06-sqlalchemy-masterclass-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ------------------------------------------------------------------------------
# 1. Employee ORM Model Definition
# ------------------------------------------------------------------------------
class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    department = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "salary": self.salary,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


# Initialize Tables & Pre-seed Data
with app.app_context():
    db.create_all()
    # Pre-seed initial employees if table is empty
    if not db.session.execute(db.select(Employee)).scalars().first():
        sample_emps = [
            Employee(name="Alice Smith", email="alice@company.com", department="Engineering", salary=85000.0),
            Employee(name="Bob Jones", email="bob@company.com", department="Marketing", salary=62000.0),
            Employee(name="Charlie Brown", email="charlie@company.com", department="Sales", salary=71000.0)
        ]
        db.session.add_all(sample_emps)
        db.session.commit()


# ------------------------------------------------------------------------------
# 2. HTML UI Template String
# ------------------------------------------------------------------------------
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 06 Employee Directory</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; background: #f4f6f9; }
        .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); max-width: 800px; margin: auto; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background-color: #2c3e50; color: white; }
        .btn { background: #27ae60; color: white; padding: 8px 15px; border: none; border-radius: 4px; text-decoration: none; cursor: pointer; }
        .form-inline { display: flex; gap: 10px; margin-top: 15px; }
        .form-inline input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; flex: 1; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📊 Employee Management System (Day 06)</h2>

        <form class="form-inline" method="POST" action="/employees/add">
            <input type="text" name="name" placeholder="Full Name" required>
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="text" name="department" placeholder="Department" required>
            <input type="number" step="0.01" name="salary" placeholder="Salary" required>
            <button class="btn" type="submit">Add Employee</button>
        </form>

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
                    <td><a href="/employees/delete/{{ e.id }}" style="color:red;">Delete</a></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 3. Web UI Routes
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    stmt = db.select(Employee).order_by(Employee.id.desc())
    emps = db.session.execute(stmt).scalars().all()
    return render_template_string(INDEX_HTML, employees=emps)

@app.route('/employees/add', methods=['POST'])
def add_employee_form():
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
        print(f"Error adding employee: {e}")
    return redirect(url_for('index'))

@app.route('/employees/delete/<int:emp_id>')
def delete_employee_form(emp_id):
    emp = db.session.get(Employee, emp_id)
    if emp:
        db.session.delete(emp)
        db.session.commit()
    return redirect(url_for('index'))


# ------------------------------------------------------------------------------
# 4. RESTful JSON API Routes
# ------------------------------------------------------------------------------
@app.route('/api/employees', methods=['GET'])
def list_employees_api():
    stmt = db.select(Employee).order_by(Employee.id)
    emps = db.session.execute(stmt).scalars().all()
    return jsonify([e.to_dict() for e in emps])

@app.route('/api/employees', methods=['POST'])
def create_employee_api():
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


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 06 Employee Directory Application...")
    print("Test UI at http://127.0.0.1:5000/")
    print("Test API at http://127.0.0.1:5000/api/employees")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
