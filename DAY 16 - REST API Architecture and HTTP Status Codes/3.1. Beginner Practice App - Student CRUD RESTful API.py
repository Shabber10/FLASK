"""
================================================================================
CLASS NOTES PRACTICAL APPLICATION: STUDENT CRUD RESTful API WITH STATUS CODES
================================================================================
Goal: A crystal-clear, zero-dependency, beginner-friendly RESTful API in Flask.

Concepts Demonstrated Step-by-Step:
1. REST Resource Endpoints: Using clean plural nouns (/students, /students/<id>).
2. Proper HTTP Methods: GET (read), POST (create), PUT (update), DELETE (remove).
3. HTTP Status Codes:
   - 200 OK: Data retrieved or updated successfully.
   - 201 Created: New student added.
   - 204 No Content: Student deleted (or 200 with confirmation).
   - 400 Bad Request: Missing or malformed JSON payload.
   - 404 Not Found: Student ID does not exist.
   - 409 Conflict: Duplicate email or roll number already exists.
   - 422 Unprocessable Content: Invalid data values (e.g. empty name, invalid age).
4. jsonify(): Clean, industry-standard JSON response generation.
5. request.get_json(): Extracting JSON request payload safely.

How to Run:
1. In your terminal, run:
   python "3.1. Beginner Practice App - Student CRUD RESTful API.py"
2. Open your browser or Postman at: http://127.0.0.1:5000/
================================================================================
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# ------------------------------------------------------------------------------
# In-Memory Database (Simulating a database table of Students)
# ------------------------------------------------------------------------------
students_db = {
    101: {"id": 101, "name": "Rahul Sharma", "email": "rahul@example.com", "age": 21, "course": "Computer Science"},
    102: {"id": 102, "name": "Priya Patel", "email": "priya@example.com", "age": 22, "course": "Data Science"},
    103: {"id": 103, "name": "Amit Kumar", "email": "amit@example.com", "age": 20, "course": "Information Technology"}
}


# ------------------------------------------------------------------------------
# Helper Validation Functions
# ------------------------------------------------------------------------------
def is_email_taken(email, exclude_id=None):
    """Check if an email already exists in the database."""
    for s_id, s in students_db.items():
        if s["email"].lower() == email.lower() and s_id != exclude_id:
            return True
    return False


# ------------------------------------------------------------------------------
# 1. Root & Documentation Route
# ------------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    """Welcome and quick API guide."""
    return jsonify({
        "message": "Welcome to the Student CRUD RESTful API!",
        "version": "1.0",
        "endpoints": {
            "GET /students": "List all students (Status 200)",
            "GET /students/<id>": "Get details of single student (Status 200 or 404)",
            "POST /students": "Create a new student (Status 201, 400, 409, 422)",
            "PUT /students/<id>": "Update an existing student (Status 200, 404, 422)",
            "DELETE /students/<id>": "Delete a student (Status 200 or 204, 404)"
        }
    }), 200


# ------------------------------------------------------------------------------
# 2. GET /students - Fetch All Students
# ------------------------------------------------------------------------------
@app.route("/students", methods=["GET"])
def get_all_students():
    """
    HTTP Method: GET
    Success Code: 200 OK
    Real-Life Analogy: Waiter brings the menu / list of dishes.
    """
    students_list = list(students_db.values())
    return jsonify({
        "success": True,
        "count": len(students_list),
        "data": students_list
    }), 200


# ------------------------------------------------------------------------------
# 3. GET /students/<int:student_id> - Fetch Single Student
# ------------------------------------------------------------------------------
@app.route("/students/<int:student_id>", methods=["GET"])
def get_single_student(student_id):
    """
    HTTP Method: GET
    Success Code: 200 OK
    Error Code: 404 Not Found (if student ID doesn't exist)
    Real-Life Analogy: Asking the library for book number #999.
    """
    student = students_db.get(student_id)
    if not student:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Student with ID {student_id} does not exist."
        }), 404

    return jsonify({
        "success": True,
        "data": student
    }), 200


# ------------------------------------------------------------------------------
# 4. POST /students - Create New Student
# ------------------------------------------------------------------------------
@app.route("/students", methods=["POST"])
def create_student():
    """
    HTTP Method: POST
    Success Code: 201 Created
    Error Codes:
      - 400 Bad Request (Missing JSON payload)
      - 409 Conflict (Duplicate email)
      - 422 Unprocessable Content (Validation failed on name or age)
    Real-Life Analogy: Registering a new Gmail account.
    """
    data = request.get_json()

    # 400 Bad Request: Missing or malformed JSON
    if not data or not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": "Invalid or missing JSON payload."
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    age = data.get("age")
    course = data.get("course", "General Studies").strip()

    # 422 Unprocessable Content: Data validation checks
    if not name:
        return jsonify({
            "success": False,
            "error": "Unprocessable Content",
            "message": "Student 'name' is required and cannot be empty."
        }), 422

    if not email or "@" not in email:
        return jsonify({
            "success": False,
            "error": "Unprocessable Content",
            "message": "A valid 'email' address is required."
        }), 422

    if age is not None:
        try:
            age = int(age)
            if age <= 0 or age > 120:
                raise ValueError()
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "error": "Unprocessable Content",
                "message": "Field 'age' must be a valid positive integer."
            }), 422
    else:
        age = 18

    # 409 Conflict: Email already registered
    if is_email_taken(email):
        return jsonify({
            "success": False,
            "error": "Conflict",
            "message": f"Email '{email}' is already registered in the system."
        }), 409

    # Generate new ID
    new_id = max(students_db.keys(), default=100) + 1
    new_student = {
        "id": new_id,
        "name": name,
        "email": email,
        "age": age,
        "course": course
    }
    students_db[new_id] = new_student

    # Return 201 Created
    return jsonify({
        "success": True,
        "message": "Student created successfully.",
        "data": new_student
    }), 201


# ------------------------------------------------------------------------------
# 5. PUT /students/<int:student_id> - Update Existing Student
# ------------------------------------------------------------------------------
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    HTTP Method: PUT
    Success Code: 200 OK
    Error Codes:
      - 400 Bad Request (Missing JSON payload)
      - 404 Not Found (Student doesn't exist)
      - 409 Conflict (Email taken by someone else)
      - 422 Unprocessable Content (Validation failed)
    """
    if student_id not in students_db:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Student with ID {student_id} does not exist."
        }), 404

    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": "Invalid or missing JSON payload."
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    age = data.get("age")
    course = data.get("course", "").strip()

    if not name:
        return jsonify({
            "success": False,
            "error": "Unprocessable Content",
            "message": "Student 'name' cannot be empty."
        }), 422

    if email and is_email_taken(email, exclude_id=student_id):
        return jsonify({
            "success": False,
            "error": "Conflict",
            "message": f"Email '{email}' is already taken by another student."
        }), 409

    # Update fields
    student = students_db[student_id]
    student["name"] = name
    if email:
        student["email"] = email
    if age is not None:
        student["age"] = int(age)
    if course:
        student["course"] = course

    return jsonify({
        "success": True,
        "message": f"Student #{student_id} updated successfully.",
        "data": student
    }), 200


# ------------------------------------------------------------------------------
# 6. DELETE /students/<int:student_id> - Delete Student
# ------------------------------------------------------------------------------
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    HTTP Method: DELETE
    Success Code: 200 OK (with confirmation message) or 204 No Content
    Error Code: 404 Not Found
    Real-Life Analogy: Throwing paper into the trash can.
    """
    if student_id not in students_db:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Student with ID {student_id} does not exist."
        }), 404

    deleted_student = students_db.pop(student_id)
    return jsonify({
        "success": True,
        "message": f"Student #{student_id} ({deleted_student['name']}) has been deleted successfully."
    }), 200


# ------------------------------------------------------------------------------
# Self-Test Verification Suite
# ------------------------------------------------------------------------------
def run_self_tests():
    """Runs automated verification tests using Flask test client."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE FOR STUDENT CRUD RESTful API")
    print("=" * 70)

    client = app.test_client()

    # Test 1: GET /students (200 OK)
    res = client.get("/students")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    print("[+] TEST 1 PASSED: GET /students -> 200 OK (Count:", res.json["count"], ")")

    # Test 2: POST /students (201 Created)
    new_data = {"name": "Kiran Varma", "email": "kiran.varma@example.com", "age": 23, "course": "Cyber Security"}
    res = client.post("/students", json=new_data)
    assert res.status_code == 201, f"Expected 201, got {res.status_code}"
    created_id = res.json["data"]["id"]
    print(f"[+] TEST 2 PASSED: POST /students -> 201 Created (New ID: {created_id})")

    # Test 3: POST /students with Duplicate Email (409 Conflict)
    res = client.post("/students", json=new_data)
    assert res.status_code == 409, f"Expected 409, got {res.status_code}"
    print("[+] TEST 3 PASSED: Duplicate email -> 409 Conflict")

    # Test 4: POST /students with Invalid Age (422 Unprocessable Content)
    res = client.post("/students", json={"name": "Test", "email": "test@test.com", "age": -5})
    assert res.status_code == 422, f"Expected 422, got {res.status_code}"
    print("[+] TEST 4 PASSED: Invalid age -> 422 Unprocessable Content")

    # Test 5: GET /students/<id> (200 OK)
    res = client.get(f"/students/{created_id}")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    print(f"[+] TEST 5 PASSED: GET /students/{created_id} -> 200 OK")

    # Test 6: PUT /students/<id> (200 OK)
    res = client.put(f"/students/{created_id}", json={"name": "Kiran Varma Updated", "email": "kiran.varma@example.com"})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    print(f"[+] TEST 6 PASSED: PUT /students/{created_id} -> 200 OK")

    # Test 7: DELETE /students/<id> (200 OK)
    res = client.delete(f"/students/{created_id}")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    print(f"[+] TEST 7 PASSED: DELETE /students/{created_id} -> 200 OK")

    # Test 8: GET /students/<id> after delete (404 Not Found)
    res = client.get(f"/students/{created_id}")
    assert res.status_code == 404, f"Expected 404, got {res.status_code}"
    print(f"[+] TEST 8 PASSED: GET /students/{created_id} after deletion -> 404 Not Found")

    print("=" * 70)
    print("ALL 8 SELF-TESTS COMPLETED SUCCESSFULLY! REST API IS 100% FUNCTIONAL.")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv or "-t" in sys.argv:
        run_self_tests()
    else:
        print("Starting Flask Student CRUD RESTful API Server...")
        print("Run with '--test' to execute automated test checks.")
        app.run(debug=True, port=5000)
