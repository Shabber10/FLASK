# 🔐 Class Notes: Session Management in Flask

> **Class Reference**: Derived directly from *Final Session Management in Flask.docx*  
> **Topic**: Client-Side vs. Server-Side Sessions, Flask-Session (Filesystem), Database Authentication Flow (MySQL/SQLite), Session Lifetimes, and Secure Password Hashing.

---

## 🎯 1. Why Session Management?

* The Web communicates using **HTTP**, which is **stateless**.
* The server forgets the user after every request.
* To remember users across multiple pages (e.g. keep them logged in), we use **Session Management**.

### 💡 Definition of Session
> *"A session is used to store data temporarily on the server and remember the user when requests arrive from the browser."*

There are **2 main approaches in Flask**:
1. **Client-Side Session Management** (Default in Flask using signed cookies)
2. **Server-Side Session Management** (Using the `Flask-Session` extension with filesystem, database, or Redis)

---

## 🔹 2. Client-Side Session Management (Flask Default)

### What it means:
* Session data is stored directly in the browser inside a cookie named `session`.
* Flask **cryptographically signs and encodes** the cookie using `app.secret_key`.
* The browser stores the data, while the server creates and verifies the cryptographic signature.

```
┌──────────────┐                                       ┌──────────────┐
│   BROWSER    │                                       │ FLASK SERVER │
└──────┬───────┘                                       └──────┬───────┘
       │                                                      │
       │ 1. POST /login (username="admin")                    │
       ├─────────────────────────────────────────────────────>│
       │                                                      │ 2. session['username'] = 'admin'
       │                                                      │ 3. Serializes + Signs with secret_key
       │ 4. Set-Cookie: session=eJyrVkrOLS7...                │
       │<─────────────────────────────────────────────────────┤
       │                                                      │
       │ 5. GET /dashboard (sends Cookie: session=...)        │
       ├─────────────────────────────────────────────────────>│
       │                                                      │ 6. Verifies signature with secret_key
       │ 7. Returns "Welcome admin"                           │ 7. Reads session['username']
       │<─────────────────────────────────────────────────────┤
```

### Where is Data Stored?
| Location | Stored Data |
| :--- | :--- |
| **Browser** | Signed & Encrypted-like session payload cookie |
| **Server** | Only `SECRET_KEY` in memory / configuration |

### Security in Client-Side Sessions:
* ✔ **Tamper-Proof**: If a user attempts to edit cookie contents in DevTools, Flask detects signature mismatch and drops the session.
* ✔ **Key Revocation**: Changing `secret_key` instantly logs out all existing users.
* ⚠️ **Not Encrypted by Default**: Default client cookies are Base64 signed; users can inspect the plaintext fields. Never put passwords or confidential secrets inside `session`.

### 🧪 Basic Example:
```python
from flask import Flask, session

app = Flask(__name__)
app.secret_key = "abc123secretkey"

@app.route('/login')
def login():
    session['user'] = "admin"
    return "Logged in (Client-side)"

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome {session['user']}"
    return "Please log in first!"

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 🟢 3. Server-Side Session Management (Flask-Session)

### What it means:
* The actual session data (usernames, cart, roles) is stored **on the server** (Filesystem, Redis, or Database).
* The browser receives and stores **only a unique Session ID** in the cookie.
* Requires the `Flask-Session` extension (`pip install Flask-Session`).

```
┌──────────────┐            ┌──────────────┐            ┌────────────────────────┐
│   BROWSER    │            │ FLASK SERVER │            │ SERVER STORAGE / DISK  │
└──────┬───────┘            └──────┬───────┘            └───────────┬────────────┘
       │                           │                                │
       │ 1. POST /login            │                                │
       ├──────────────────────────>│ 2. Generates Session ID        │
       │                           │ 3. Writes session data ───────>│ (Saved to disk/Redis)
       │ 4. Set-Cookie:            │                                │
       │    session=uuid-1234      │                                │
       │<──────────────────────────┤                                │
       │                           │                                │
       │ 5. GET /dashboard         │                                │
       │    Cookie: uuid-1234      │                                │
       ├──────────────────────────>│ 6. Reads Session ID            │
       │                           │ 7. Fetches data from disk ────>│
       │                           │ 8. Receives {'user': 'admin'} <┤
       │ 9. Returns "Welcome"      │                                │
       │<──────────────────────────┤                                │
```

### Where is Data Stored?
| Location | Stored Data |
| :--- | :--- |
| **Browser** | Session ID string only (e.g. `xyz-789-uuid`) |
| **Server** (`flask_session/` or Redis) | Actual data (`username`, `cart`, `role`, `user_id`) |

### 🧪 Server-Side Filesystem Session Example:
```python
from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = "server_secret_key_123"

# Configure server-side session to store on local filesystem
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False

# Initialize the Flask-Session extension
Session(app)

@app.route('/login')
def login():
    session['user'] = "admin"
    return "Logged in (Server-side session active!)"

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if user:
        return f"Welcome to Server-Side Dashboard: {user}"
    return "Session not found. Please visit /login."

if __name__ == "__main__":
    app.run(debug=True)
```
> 📂 **What happens on disk?** When this runs, a `flask_session/` directory is automatically created on your server. Each active session creates a file containing that user's session data.

---

## 🗄️ 4. Full Database Login + Session System (MySQL / Database)

Here is the complete step-by-step implementation for database-backed authentication with session control:

### Step 1: Database Setup (MySQL)
```sql
CREATE DATABASE userdb;
USE userdb;

CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Insert sample user
INSERT INTO users(username, password) VALUES ("admin", "1234");
```

### Step 2: Application Code (`app.py`)
```python
from flask import Flask, render_template, request, redirect, session
import mysql.connector
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "mysecret123"

# Configure session expiration (2 minutes of inactivity)
app.permanent_session_lifetime = timedelta(minutes=2)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",        # Enter your MySQL password
        database="userdb"
    )

# ---------------------------------------
# LOGIN ROUTE (GET / POST)
# ---------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # session.permanent = True applies the timedelta expiry lifetime
            session.permanent = True
            session['username'] = username
            return redirect("/dashboard")
        else:
            return "Invalid Username or Password. Try Again!", 401

    return render_template("login.html")

# ---------------------------------------
# PROTECTED DASHBOARD ROUTE
# ---------------------------------------
@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        return render_template("dashboard.html", user=session['username'])
    else:
        # If user is not logged in, redirect to login page
        return redirect("/")

# ---------------------------------------
# LOGOUT ROUTE
# ---------------------------------------
@app.route("/logout")
def logout():
    # Remove user from session
    session.pop('username', None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
```

### Step 3: Templates

#### `templates/login.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login Page</h2>
    <form method="POST" action="/">
        <label>Username:</label>
        <input type="text" name="username" required><br><br>
        <label>Password:</label>
        <input type="password" name="password" required><br><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
```

#### `templates/dashboard.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body>
    <h2>Welcome {{ user }}!</h2>
    <p>Your session is active.</p>
    <a href="/logout">Logout</a>
</body>
</html>
```

---

## 🔒 5. Best Practice Upgrade: Secure Password Hashing

In production, **never store plaintext passwords** like `"1234"` in your database. Use `werkzeug.security`:

```python
from werkzeug.security import generate_password_hash, check_password_hash

# 1. When registering a user:
hashed_password = generate_password_hash("mysecretpassword", method='scrypt')
# Store `hashed_password` in DB

# 2. When user logs in:
# Fetch user row from DB by username
if user and check_password_hash(user['password'], entered_password):
    session['username'] = user['username']
    session.permanent = True
    return redirect('/dashboard')
else:
    return "Invalid credentials", 401
```

---

## 📊 6. Comparison Summary: Before vs. After Database & Session

| Feature | Hardcoded In-Memory | Database + Session |
| :--- | :--- | :--- |
| **Credentials** | Fixed in Python code | Stored in Database table |
| **User Count** | Single user only | Unlimited scalable users |
| **Session Control**| Manual check | Automatic Flask session with timeout |
| **Security** | Plaintext & insecure | Password hashing + cryptographically signed sessions |
