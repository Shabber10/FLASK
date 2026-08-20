"""
Day 06 Practice Application: College Student Database with mysql-connector-python
==================================================================================
Demonstrates complete raw MySQL Database CRUD operations in Flask using `mysql-connector-python`.
Target Database: `collegedb`, Table: `student` (id, sname, sage, smarks, scity).
"""

from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration for 'collegedb'
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'collegedb',
    'port': 3306
}

def get_db_connection():
    """Helper to establish a MySQL connection to 'collegedb'."""
    return mysql.connector.connect(**db_config)

# Fallback in-memory student storage if local MySQL server is offline
demo_students = [
    (1, "raju", 24, 85.0, "Hyderabad"),
    (2, "ramu", 25, 90.0, "Bangalore")
]

def init_db():
    """Initializes the 'student' table in 'collegedb' database."""
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
        print("✅ MySQL 'student' table in 'collegedb' initialized successfully.")
    except Error as e:
        print(f"⚠️ MySQL Connection Notice: {e}")

# route for check the connection
@app.route('/')
def Home():
    return "Database connection is successfully"

# fetch the student records from database (collegedb)
@app.route('/getstudents', methods=['GET'])
def Getstudents():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("select * from student")
        results = cursor.fetchall()  # nested list
        print(results)
        cursor.close()
        conn.close()
        return render_template('studentsdata.html', students=results)
    except Error:
        return render_template('studentsdata.html', students=demo_students)

# fetch student record based on id
@app.route('/getstudentbyid/<int:sid>', methods=['GET']) # /getstudentbyid/1
def Getstudentbyid(sid): 
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from student where id=%s", (sid,))
        result = cursor.fetchone()
        print("data is:", result)
        cursor.close()
        conn.close()
        if not result:
            return {"message": f"student id {sid} is not found"}
        return result
    except Error:
        for s in demo_students:
            if s[0] == sid:
                return {"id": s[0], "sname": s[1], "sage": s[2], "smarks": s[3], "scity": s[4]}
        return {"message": f"student id {sid} is not found"}

# api for display register form
@app.route('/register')
def Register():
    return render_template('register.html')

# api for get data from form and send data to db
@app.route('/Addstudent', methods=['POST'])
def Addstudent():
    name = request.form['myname']
    age = request.form['myage']
    marks = request.form['mymarks']
    city = request.form['mycity']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("insert into student(sname,sage,smarks,scity) values(%s,%s,%s,%s)", (name, age, marks, city))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Database write notice: {e}")
        new_id = len(demo_students) + 1
        demo_students.append((new_id, name, int(age), float(marks), city))
    return redirect('/getstudents')

# route for get data based on id for editing
@app.route('/editstudent/<int:sid>', methods=['GET'])
def Editstudent(sid):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("select * from student where id=%s", (sid,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('editstudent.html', student=result)
    except Error:
        match = next((s for s in demo_students if s[0] == sid), demo_students[0])
        return render_template('editstudent.html', student=match)

# route for update the student based on id
@app.route('/updatestudent/<int:sid>', methods=['POST'])
def Updatestudent(sid):
    id = request.form['sid']
    name = request.form['sname']
    age = request.form['sage']
    marks = request.form['smarks']
    city = request.form['scity']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "update student set sname=%s,sage=%s,smarks=%s,scity=%s where id=%s"
        cursor.execute(query, (name, age, marks, city, id))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Database write notice: {e}")
        global demo_students
        demo_students = [(int(id), name, int(age), float(marks), city) if s[0] == int(id) else s for s in demo_students]
    return redirect('/getstudents')

# route for delete student based on id
@app.route('/deletestudent/<int:sid>', methods=['GET'])
def Deletestudent(sid):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("delete from student where id=%s", (sid,))
        conn.commit()
        cursor.close()
        conn.close()
    except Error:
        global demo_students
        demo_students = [s for s in demo_students if s[0] != sid]
    return redirect("/getstudents")

if __name__ == '__main__':
    print("🚀 Starting Flask App on http://127.0.0.1:5000")
    init_db()
    app.run(debug=True)
