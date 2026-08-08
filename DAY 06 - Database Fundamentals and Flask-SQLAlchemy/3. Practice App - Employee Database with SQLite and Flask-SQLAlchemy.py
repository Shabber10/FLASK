# Day 06 Practice App: Employee Management System
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    emp = Employee(name=data['name'], department=data['department'], salary=data['salary'])
    db.session.add(emp)
    db.session.commit()
    return jsonify({"id": emp.id, "name": emp.name}), 201

@app.route('/employees', methods=['GET'])
def list_employees():
    emps = Employee.query.all()
    return jsonify([{"id": e.id, "name": e.name, "dept": e.department, "salary": e.salary} for e in emps])

if __name__ == '__main__':
    app.run(debug=True)
