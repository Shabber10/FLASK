"""
===============================================================================
Day 14 Demo: Full Database Login & Session Expiration System
===============================================================================
Topic: Database-Backed Authentication + Session Management from class notes:
- User login with database validation
- session.permanent = True with app.permanent_session_lifetime = timedelta(minutes=2)
- Protected /dashboard route checking 'username' in session
- /logout route with session.pop('username', None)
- Modern templates: login.html and dashboard.html
- Supports both SQLite (zero-config default) and MySQL database connections!

How to Run:
1. python "demo_database_session_auth.py"
2. Open in browser: http://127.0.0.1:5000/
3. Sign in with:
   - Username: admin
   - Password: 1234
"""

import os
import sqlite3
from datetime import timedelta
from flask import Flask, render_template, request, redirect, session, url_for

# Optional MySQL connector import
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

app = Flask(__name__, template_folder="templates")
app.secret_key = "mysecret123-day14-db-session"

# Configure session expiration (2 minutes of inactivity)
app.permanent_session_lifetime = timedelta(minutes=2)

# =============================================================================
# Database Configuration & Helper
# Set USE_MYSQL = True if you have MySQL running locally with 'userdb' database
# =============================================================================
USE_MYSQL = False
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "userdb.sqlite")

def init_sqlite_db():
    """Initializes local SQLite database and seeds default admin user."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # Seed sample user if empty
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', '1234')")
        cursor.execute("INSERT INTO users (username, password) VALUES ('jani', 'pass123')")
        conn.commit()
    conn.close()

def get_user_from_db(username, password):
    """Fetches user matching username and password from active database."""
    if USE_MYSQL and MYSQL_AVAILABLE:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",        # Enter your MySQL password here
            database="userdb"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    else:
        # SQLite Fallback (Zero setup required)
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

# Initialize SQLite database upon startup
init_sqlite_db()

# -----------------------------------------------------------------------------
# LOGIN ROUTE (GET / POST)
# -----------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = get_user_from_db(username, password)

        if user:
            # session.permanent = True enables the 2-minute lifetime expiry
            session.permanent = True
            # Store username in session
            session['username'] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid Username or Password. Try Again!"

    # If already logged in, redirect straight to dashboard
    if 'username' in session:
        return redirect(url_for("dashboard"))

    return render_template("login.html", error=error)

# -----------------------------------------------------------------------------
# DASHBOARD ROUTE (Protected)
# -----------------------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    # Check if user is logged in
    if 'username' in session:
        return render_template("dashboard.html", user=session['username'])
    else:
        # If session is empty -> redirect to login
        return redirect(url_for("login"))

# -----------------------------------------------------------------------------
# LOGOUT ROUTE
# -----------------------------------------------------------------------------
@app.route("/logout")
def logout():
    # Remove user from session -> logs out user
    session.pop('username', None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" Day 14 Database & Session Auth Demo Running!")
    print(" Open: http://127.0.0.1:5000/")
    print(" Credentials -> User: 'admin' | Password: '1234'")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)
