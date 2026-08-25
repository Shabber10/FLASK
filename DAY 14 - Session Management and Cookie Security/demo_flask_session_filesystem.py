"""
===============================================================================
Day 14 Demo: Server-Side Session Management with Flask-Session (Filesystem)
===============================================================================
Topic: Demonstrating Server-Side Sessions as covered in class notes:
- Using Flask-Session extension
- app.config["SESSION_TYPE"] = "filesystem"
- Session data stored on server disk in `flask_session/`
- Browser cookie holds only a unique encrypted Session ID

How to Run:
1. python "demo_flask_session_filesystem.py"
2. Open in browser: http://127.0.0.1:5000/
"""

import os
from flask import Flask, session, render_template_string, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.secret_key = "abc123secretkey-day14"

# Configure server-side session
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flask_session")
app.config["SESSION_PERMANENT"] = False

# Initialize Flask-Session extension
Session(app)

INDEX_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Day 14 - Server-Side Filesystem Session Demo</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0f172a;
            color: #f8fafc;
            padding: 2rem;
            max-width: 650px;
            margin: 0 auto;
        }
        .card {
            background: #1e293b;
            padding: 1.5rem;
            border-radius: 0.75rem;
            border: 1px solid #334155;
            margin-bottom: 1.5rem;
        }
        h2 { color: #38bdf8; margin-top: 0; }
        .val { color: #34d399; font-weight: bold; }
        a.btn {
            display: inline-block;
            background: #38bdf8;
            color: #0f172a;
            padding: 0.5rem 1rem;
            text-decoration: none;
            border-radius: 0.375rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        a.btn-danger {
            background: #f87171;
            color: #0f172a;
        }
        code { background: #0f172a; padding: 0.2rem 0.4rem; border-radius: 0.25rem; color: #f472b6; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🟢 Server-Side Session Management (Flask-Session)</h2>
        {% if user %}
            <p>Status: <span class="val">Logged In</span></p>
            <p>Active User: <span class="val">{{ user }}</span></p>
            <p>Session Role: <span class="val">{{ role }}</span></p>
            <p>Items in Cart: <span class="val">{{ cart_count }} items</span></p>
        {% else %}
            <p>Status: <span style="color:#f87171;">Guest (Not Logged In)</span></p>
        {% endif %}
    </div>

    <div class="card">
        <h3>Actions:</h3>
        <p>
            {% if not user %}
                <a href="/login?user=admin" class="btn">Login as 'admin'</a>
                <a href="/login?user=Jani" class="btn">Login as 'Jani'</a>
            {% else %}
                <a href="/dashboard" class="btn">Go to /dashboard</a>
                <a href="/add_cart" class="btn">Add Item to Cart</a>
                <a href="/logout" class="btn btn-danger">Logout (Clear Session)</a>
            {% endif %}
        </p>
        <p><a href="/" class="btn" style="background:#64748b; color:white;">↻ Refresh Status</a></p>
    </div>

    <div class="card">
        <h3>Server Storage Inspection:</h3>
        <p>Session files stored on server disk in: <code>{{ session_dir }}</code></p>
        <p>Active Session Files count: <strong>{{ file_count }}</strong></p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    user = session.get('user')
    role = session.get('role', 'Standard')
    cart = session.get('cart', [])
    session_dir = app.config["SESSION_FILE_DIR"]
    
    file_count = 0
    if os.path.exists(session_dir):
        file_count = len([f for f in os.listdir(session_dir) if os.path.isfile(os.path.join(session_dir, f))])

    return render_template_string(
        INDEX_PAGE,
        user=user,
        role=role,
        cart_count=len(cart),
        session_dir=session_dir,
        file_count=file_count
    )

@app.route('/login')
def login():
    username = request.args.get('user', 'admin') if 'request' in globals() else 'admin'
    from flask import request as req
    user = req.args.get('user', 'admin')
    
    # Store data in server session
    session['user'] = user
    session['role'] = 'Administrator' if user == 'admin' else 'Student'
    session['cart'] = ['Flask Book', 'Python Course']
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))
    return f"""
    <html><body style='background:#0f172a;color:#f8fafc;font-family:sans-serif;padding:2rem;'>
        <h2>Welcome to Protected Dashboard, {user}!</h2>
        <p>Your session is stored securely in the server filesystem.</p>
        <p><a href='/' style='color:#38bdf8;'>← Home</a> | <a href='/logout' style='color:#f87171;'>Logout</a></p>
    </body></html>
    """

@app.route('/add_cart')
def add_cart():
    if 'cart' not in session:
        session['cart'] = []
    cart = session['cart']
    cart.append(f"Product #{len(cart) + 1}")
    session['cart'] = cart
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    # Clear session data on the server
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
