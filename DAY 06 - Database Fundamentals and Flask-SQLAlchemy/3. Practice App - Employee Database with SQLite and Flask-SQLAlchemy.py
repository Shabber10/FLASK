"""
===============================================================================
Day 06 Practice Application: Employee & Student Database with Flask-SQLAlchemy
===============================================================================
Demonstrates complete Object-Relational Mapping (ORM) and CRUD operations in Flask
using `Flask-SQLAlchemy` and SQLite (zero-config, portable).

Features Demonstrated:
1. Setting up Flask-SQLAlchemy with SQLite database URI (`sqlite:///company.db`).
2. Defining the `Employee` model with constraints, types, and serialization.
3. Automatically creating tables via `db.create_all()` inside app context.
4. Performing all 4 CRUD operations:
   - CREATE: `POST /api/employees` or form submission
   - READ: `GET /api/employees` and `GET /api/employees/<id>`
   - UPDATE: `PUT /api/employees/<id>`
   - DELETE: `DELETE /api/employees/<id>`
5. Interactive Web Portal Dashboard rendering `templates/index.html`.
"""

import os
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

app = Flask(__name__)

# =============================================================================
# STEP 1: Database Configuration & Extension Initialization
# =============================================================================
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'day06-database-masterclass-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'sqlite:///' + os.path.join(basedir, 'company.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# =============================================================================
# STEP 2: Model Definition (Employee Table)
# =============================================================================
class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    department = db.Column(db.String(50), nullable=False, default="Engineering")
    salary = db.Column(db.Float, nullable=False, default=50000.0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "salary": self.salary,
            "is_active": self.is_active,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }


# =============================================================================
# STEP 3: Database Initialization & Seeding Helper
# =============================================================================
def init_database():
    """Initializes tables and seeds initial demo data."""
    with app.app_context():
        db.create_all()
        # Seed demo data if database is empty
        if not Employee.query.first():
            demo_employees = [
                Employee(name="Alice Johnson", email="alice@enterprise.dev", department="Engineering", salary=85000.0),
                Employee(name="Bob Smith", email="bob@enterprise.dev", department="Marketing", salary=62000.0),
                Employee(name="Charlie Lee", email="charlie@enterprise.dev", department="Finance", salary=75000.0)
            ]
            db.session.add_all(demo_employees)
            db.session.commit()
            print("✓ Database initialized with sample employees.")


# =============================================================================
# STEP 4: REST API CRUD Endpoints
# =============================================================================

# 1. READ ALL: GET /api/employees
@app.route('/api/employees', methods=['GET'])
def api_get_employees():
    stmt = select(Employee).order_by(Employee.id.asc())
    employees = db.session.execute(stmt).scalars().all()
    return jsonify({
        "status": "success",
        "total": len(employees),
        "employees": [e.to_dict() for e in employees]
    }), 200


# 2. READ ONE: GET /api/employees/<id>
@app.route('/api/employees/<int:emp_id>', methods=['GET'])
def api_get_employee(emp_id):
    employee = db.session.get(Employee, emp_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"status": "success", "employee": employee.to_dict()}), 200


# 3. CREATE: POST /api/employees
@app.route('/api/employees', methods=['POST'])
def api_create_employee():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    department = data.get('department', 'Engineering')
    salary = float(data.get('salary', 50000))

    if not name or not email:
        return jsonify({"error": "Validation Error", "message": "Name and email are required"}), 422

    # Check for existing email
    existing = Employee.query.filter_by(email=email).first()
    if existing:
        return jsonify({"error": "Conflict", "message": "Email already exists"}), 409

    new_emp = Employee(name=name, email=email, department=department, salary=salary)
    db.session.add(new_emp)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Employee created successfully",
        "employee": new_emp.to_dict()
    }), 201


# 4. UPDATE: PUT /api/employees/<id>
@app.route('/api/employees/<int:emp_id>', methods=['PUT', 'PATCH'])
def api_update_employee(emp_id):
    employee = db.session.get(Employee, emp_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json() or {}
    if 'name' in data:
        employee.name = data['name']
    if 'email' in data:
        employee.email = data['email']
    if 'department' in data:
        employee.department = data['department']
    if 'salary' in data:
        employee.salary = float(data['salary'])
    if 'is_active' in data:
        employee.is_active = bool(data['is_active'])

    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "Employee updated successfully",
        "employee": employee.to_dict()
    }), 200


# 5. DELETE: DELETE /api/employees/<id>
@app.route('/api/employees/<int:emp_id>', methods=['DELETE'])
def api_delete_employee(emp_id):
    employee = db.session.get(Employee, emp_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    db.session.delete(employee)
    db.session.commit()
    return jsonify({
        "status": "success",
        "message": f"Employee #{emp_id} deleted successfully"
    }), 200


# =============================================================================
# STEP 5: Interactive Web UI Dashboard
# =============================================================================
@app.route('/', methods=['GET'])
def index():
    employees = Employee.query.order_by(Employee.id.asc()).all()
    return render_template('index.html', employees=employees)


if __name__ == '__main__':
    init_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
