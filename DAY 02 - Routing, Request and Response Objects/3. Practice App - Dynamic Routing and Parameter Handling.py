"""
Day 02 Practice App - Dynamic Routing, Converters, Parameters, Form Data, JSON & Redirection
Run using: python "3. Practice App - Dynamic Routing and Parameter Handling.py"
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.routing import BaseConverter

# 1. Custom URL Converter for Even Numbers
class EvenNumberConverter(BaseConverter):
    def to_python(self, value):
        val = int(value)
        if val % 2 != 0:
            raise ValueError()  # 404 Not Found if odd
        return val

app = Flask(__name__)
# Register custom converter
app.url_map.converters['even'] = EvenNumberConverter

# In-memory RAM Data
users = [
    {'id': 1, "name": "ramu", "age": 23},
    {'id': 2, "name": "harish", "age": 19}
]

# -------------------------------------------------------------
# 1. QUERY PARAMETERS - request.args (GET)
# -------------------------------------------------------------
@app.route('/query')
def query_demo():
    name = request.args.get('name', 'guest')
    age = request.args.get('age')
    a = request.args.get('a', type=float, default=1)
    b = request.args.get('b', type=int, default=1)
    fruits = request.args.getlist('f')
    
    return jsonify({
        'name': name,
        'age': f'age is {age} ',
        'add': a + b,
        'fruitslist': fruits,
        'raw_data': str(request.args),
        'as_dict': request.args.to_dict(),
        'as_dict_with_lists': request.args.to_dict(flat=False)
    })

# -------------------------------------------------------------
# 2. FORM DATA & TEMPLATE RENDERING - request.form (POST)
# -------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        course = request.form.get('course')
        return render_template('success.html', username=username, email=email, course=course)
    
    return render_template('register.html')

# -------------------------------------------------------------
# 3. JSON DATA & REST APIs - request.get_json() (POST/PUT/DELETE)
# -------------------------------------------------------------
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.get_json()
    new_user = {
        'id': len(users) + 1,
        'name': data.get('name'),
        'age': data.get('age')
    }
    users.append(new_user)
    return jsonify({"message": "Student added successfully!", "user": new_user}), 201

@app.route('/updateuser/<int:uid>', methods=['PUT'])
def update_user(uid):
    data = request.get_json()
    new_age = data.get('age')
    
    for user in users:
        if user['id'] == uid:
            user['age'] = new_age
            return jsonify({"message": f"user data with id {uid} updated successfully", "updated_data": users})
            
    return jsonify({"message": f"user id {uid} is not found..."}), 404

@app.route('/deleteuser/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    for index, user in enumerate(users):
        if user['id'] == uid:
            users.pop(index)
            return jsonify({
                "message": f"user data with id {uid} deleted successfully",
                "updated_data": users
            }), 200
            
    return jsonify({"message": f"user id {uid} is not found..."}), 404

@app.route('/reset', methods=['GET'])
def reset_data():
    global users
    users = [
        {'id': 1, "name": "ramu", "age": 23},
        {'id': 2, "name": "harish", "age": 19}
    ]
    return jsonify({"message": "data reset successful", "users": users})

# -------------------------------------------------------------
# 4. DYNAMIC ROUTING & URL CONVERTERS
# -------------------------------------------------------------
@app.route('/user/<string:name>')
def user_profile(name):
    return f"Hello {name}, welcome to Flask dynamic routing!"

@app.route('/sum/<int:a>/<int:b>')
def sum_numbers(a, b):
    return f"The sum of {a} and {b} is: {a + b}"

@app.route('/even/<even:num>')
def check_even(num):
    return f"Validated even number: {num}"

# -------------------------------------------------------------
# 5. REDIRECTION USING url_for()
# -------------------------------------------------------------
@app.route('/stuall')
def studentall():
    # Navigates dynamically using function name 'register'
    return redirect(url_for('register'))

if __name__ == '__main__':
    print("Starting Day 02 Flask App on http://127.0.0.1:5000")
    app.run(debug=True)
