"""
Day 01 Practice Script - Basic Flask Application & Render Template Demo
Run using: python "3. Practice Script - Hello World and Basic Commands.py"
"""

from flask import Flask, render_template

# Initialize Flask application instance
app = Flask(__name__)
print("Flask App Instance Initialized:", app)

# 1. Home route returning text
@app.route('/')
def home():
    return "Hello from /home route! Jani Basha Shaik Hyderabad! Aha!"

# 2. Static route returning simple HTML string
@app.route('/course')
def courses():
    return "<h1>I am going to buy an HTML course!</h1>"

# 3. Dynamic route capturing parameters
@app.route('/course/<name>')
def coursename(name):
    return f"Your course name is: <strong>{name}</strong>"

# 4. Route rendering template 'home.html'
@app.route('/render-home')
def render_home_page():
    return render_template('home.html')

# 5. Route rendering template 'index.html'
@app.route('/render-index')
def render_index_page():
    return render_template('index.html')

if __name__ == '__main__':
    print("Starting Flask Development Server on http://127.0.0.1:5000")
    app.run(debug=True)
