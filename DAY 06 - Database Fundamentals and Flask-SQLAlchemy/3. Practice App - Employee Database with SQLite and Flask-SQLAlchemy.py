"""
===============================================================================
Day 06 Practice Script: Employee Directory Database Application
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Setting up SQLite database connection and defining `Employee(db.Model)`.
2. STEP 2: Creating SQL tables (`db.create_all()`) and pre-seeding initial data in `app.app_context()`.
3. STEP 3: Querying database rows using SQLAlchemy 2.0 syntax (`db.select()`, `scalars().all()`).
4. STEP 4: Handling HTML form insertion with transaction safety (`db.session.rollback()`).
5. STEP 5: Deleting database rows by Primary Key ID (`db.session.delete()`).
6. STEP 6: Exposing RESTful JSON API endpoints (`/api/employees`).

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Employee Database with SQLite and Flask-SQLAlchemy.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day06-sqlalchemy-masterclass-secret'
# Configure local SQLite database file path (stored as instance/employees.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy extension instance
db = SQLAlchemy(app)


# =============================================================================
# STEP 1: Employee ORM Model Definition
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


# =============================================================================
# STEP 2: Database Initialization & Initial Data Seeding
# =============================================================================

with app.app_context():
    # Creates all tables defined by db.Model classes if they do not exist
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
# STEP 3 & 4 & 5: Web UI Routes (HTML via render_template)
# =============================================================================

@app.route('/')
def index():
    """
    Step 3: Renders HTML Employee Directory querying all database rows.
    Uses modern SQLAlchemy 2.0 syntax: db.select(Employee).order_by(...)
    """
    stmt = db.select(Employee).order_by(Employee.id.desc())
    emps = db.session.execute(stmt).scalars().all()
    return render_template('employees.html', employees=emps)


@app.route('/employees/add', methods=['POST'])
def add_employee_form():
    """
    Step 4: Form submission handler with transaction rollback safety.
    """
    try:
        emp = Employee(
            name=request.form['name'],
            email=request.form['email'],
            department=request.form['department'],
            salary=float(request.form['salary'])
        )
        db.session.add(emp)
        db.session.commit()
        flash(f"Employee '{emp.name}' added successfully!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"❌ [DB ERROR] Rollback triggered: {e}")
        flash("Failed to add employee. Email address may already be in use.", "danger")
        
    return redirect(url_for('index'))


@app.route('/employees/delete/<int:emp_id>')
def delete_employee_form(emp_id):
    """
    Step 5: Deleting an Employee record by Primary Key ID.
    Uses db.session.get(Employee, emp_id)
    """
    emp = db.session.get(Employee, emp_id)
    if emp:
        db.session.delete(emp)
        db.session.commit()
        flash(f"Employee #{emp_id} deleted successfully.", "success")
    return redirect(url_for('index'))


# =============================================================================
# STEP 6: RESTful JSON API Endpoints
# =============================================================================

@app.route('/api/employees', methods=['GET'])
def list_employees_api():
    """Step 6a: API Endpoint returning all employees as JSON."""
    stmt = db.select(Employee).order_by(Employee.id)
    emps = db.session.execute(stmt).scalars().all()
    return jsonify([e.to_dict() for e in emps]), 200


@app.route('/api/employees', methods=['POST'])
def create_employee_api():
    """Step 6b: API Endpoint creating a new employee from JSON payload."""
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
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 06 Employee Directory Application...")
    print("🌐 Open Web UI at: http://127.0.0.1:5000/")
    print("📡 Test REST API at: http://127.0.0.1:5000/api/employees")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
