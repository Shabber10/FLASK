"""
===============================================================================
Day 14 Demo: Client-Side State Management with Cookies
===============================================================================
Topic: Demonstrating Cookies in Flask as covered in class notes:
- Why HTTP is stateless
- Setting cookies with make_response and res.set_cookie()
- Reading cookies with request.cookies.get()
- Cookie lifetime (max_age) and deleting cookies

How to Run:
1. python "demo_cookies_state_management.py"
2. Open in browser: http://127.0.0.1:5000/
"""

from flask import Flask, make_response, request, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Day 14 - Cookies State Management Demo</title>
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
        <h2>🍪 Client-Side State Management (Cookies)</h2>
        <p>Current Cookie <code>username</code> value: <span class="val">{{ username }}</span></p>
        <p>Current UI Theme preference: <span class="val">{{ theme }}</span></p>
    </div>

    <div class="card">
        <h3>Try Actions:</h3>
        <p>
            <a href="/set_cookie?name=Jani" class="btn">Set Cookie (username='Jani')</a>
            <a href="/set_cookie?name=Admin" class="btn">Set Cookie (username='Admin')</a>
            <a href="/set_theme?theme=Dark" class="btn">Set Theme ('Dark')</a>
            <a href="/set_theme?theme=Light" class="btn">Set Theme ('Light')</a>
            <a href="/clear_cookie" class="btn btn-danger">Clear Cookies</a>
        </p>
        <p><a href="/" class="btn" style="background:#64748b; color:white;">↻ Refresh Page</a></p>
    </div>

    <div class="card">
        <h3>How it works:</h3>
        <ul>
            <li><strong>set_cookie():</strong> <code>res = make_response(...); res.set_cookie('username', 'Jani')</code></li>
            <li><strong>request.cookies:</strong> <code>user = request.cookies.get('username')</code></li>
            <li><strong>Browser Storage:</strong> Data is stored in your browser's cookie storage (~4KB limit).</li>
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    username = request.cookies.get('username', 'Not Set (Guest)')
    theme = request.cookies.get('theme', 'System Default')
    return render_template_string(HTML_PAGE, username=username, theme=theme)

@app.route('/set_cookie')
def set_cookie():
    name = request.args.get('name', 'Jani')
    res = make_response(f"<html><body style='background:#0f172a;color:#f8fafc;font-family:sans-serif;padding:2rem;'><h3>Cookie 'username' set to '{name}'!</h3><p><a href='/' style='color:#38bdf8;'>← Back to Home</a></p></body></html>")
    # Setting cookie in browser (valid for 1 day)
    res.set_cookie("username", name, max_age=60 * 60 * 24, httponly=False)
    return res

@app.route('/set_theme')
def set_theme():
    theme = request.args.get('theme', 'Dark')
    res = make_response(f"<html><body style='background:#0f172a;color:#f8fafc;font-family:sans-serif;padding:2rem;'><h3>Theme cookie set to '{theme}'!</h3><p><a href='/' style='color:#38bdf8;'>← Back to Home</a></p></body></html>")
    res.set_cookie("theme", theme, max_age=60 * 60 * 24 * 7)
    return res

@app.route('/get_cookie')
def get_cookie():
    user = request.cookies.get("username", "No Cookie Found")
    return f"Cookie Value = {user}"

@app.route('/clear_cookie')
def clear_cookie():
    res = make_response(f"<html><body style='background:#0f172a;color:#f8fafc;font-family:sans-serif;padding:2rem;'><h3>Cookies cleared!</h3><p><a href='/' style='color:#38bdf8;'>← Back to Home</a></p></body></html>")
    res.delete_cookie('username')
    res.delete_cookie('theme')
    return res

if __name__ == "__main__":
    app.run(debug=True, port=5000)
