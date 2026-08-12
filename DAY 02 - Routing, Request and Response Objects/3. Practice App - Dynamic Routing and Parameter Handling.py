"""
===============================================================================
Day 02 Practice Script: Dynamic Routing, Redirection & Request Handling
===============================================================================
This script starts from pure zero basics for beginner developers.

What this script demonstrates step-by-step:
1. STEP 1: Basic static route handlers (`/`, `/admin`).
2. STEP 2: Conditional routing: Hardcoded `redirect()` vs Dynamic `url_for()`.
3. STEP 3: Built-in URL path converters (`<string>`, `<int>`, `<path>`).
4. STEP 4: Extracting query string parameters (`request.args`) & `abort(404)`.
5. STEP 5: Handling POST payloads, custom HTTP headers, and cookies (`make_response`).
6. STEP 6 (ADVANCED - OPTIONAL): Registering a custom Regex Converter on `app.url_map`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Dynamic Routing and Parameter Handling.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from flask import Flask, request, jsonify, make_response, redirect, url_for, abort

app = Flask(__name__)

# Simulated in-memory database
user_database = {
    1: {"username": "shabber", "role": "developer"},
    2: {"username": "admin", "role": "administrator"}
}


# =============================================================================
# STEP 1: Basic Static Routes
# =============================================================================

@app.route('/')
def home():
    """
    Step 1a: Home Page Endpoint ('/')
    """
    return """
    <h2>Welcome to Day 02: Flask Routing & Redirection Masterclass</h2>
    <p>Test the beginner routes below:</p>
    <ul>
        <li><a href="/admin">Admin Dashboard (<code>/admin</code>)</a></li>
        <li><a href="/user/shabber">User Route: Shabber (<code>/user/shabber</code>)</a></li>
        <li><a href="/user/admin">Conditional Redirect Test: Admin (<code>/user/admin</code>)</a></li>
        <li><a href="/hello/John">Dynamic Redirect Test: Hello (<code>/hello/John</code>)</a></li>
        <li><a href="/profile/1">Converter Route: Integer ID 1 (<code>/profile/1</code>)</a></li>
        <li><a href="/search?q=flask&page=1">Query Params Search (<code>/search?q=flask&page=1</code>)</a></li>
    </ul>
    """


@app.route('/admin')
def admin():
    """
    Step 1b: Admin Dashboard Endpoint ('/admin')
    """
    return "<h2 style='color: green;'>Welcome to the Secret Admin Dashboard! 🛡️</h2>"


# =============================================================================
# STEP 2: Conditional Redirection: Hardcoded vs Dynamic `url_for()`
# =============================================================================

@app.route('/user/<name>')
def user(name):
    """
    Step 2a: Dynamic Route with Conditional Redirection
    If name is 'admin', redirect directly to the admin dashboard!
    """
    if name == 'admin':
        # Hardcoded Redirect Example: redirect('/admin')
        # Dynamic url_for Redirect Example (BEST PRACTICE):
        return redirect(url_for('admin'))
    else:
        return f"<h3>User Profile Page</h3><p>Your name is: <strong>{name}</strong></p>"


@app.route('/hello/<name>')
def hello(name):
    """
    Step 2b: Redirection passing dynamic arguments to another route via url_for()
    Navigating to /hello/John automatically redirects to /user/John!
    """
    return redirect(url_for('user', name=name))


# =============================================================================
# STEP 3: Built-in URL Path Converters
# =============================================================================

@app.route('/profile/<int:user_id>')
def get_user_profile(user_id):
    """
    Step 3a: Integer Converter (<int:user_id>)
    Ensures user_id is automatically converted into a Python int.
    """
    user_info = user_database.get(user_id)
    if not user_info:
        # Halt execution and return 404 Not Found
        abort(404, description=f"User ID {user_id} does not exist.")
    
    return jsonify({
        "status": "success",
        "user_id": user_id,
        "profile": user_info
    }), 200


@app.route('/files/<path:file_path>')
def view_file_path(file_path):
    """
    Step 3b: Path Converter (<path:file_path>)
    Matches strings that contain forward slashes (e.g. /files/docs/2026/report.pdf).
    """
    return f"<h3>File Viewer</h3><p>Viewing file path: <code>{file_path}</code></p>"


# =============================================================================
# STEP 4: Query Parameters & Aborting Requests
# =============================================================================

@app.route('/search')
def search():
    """
    Step 4: Extracting Query String Parameters (`request.args`)
    Example URL: http://127.0.0.1:5000/search?q=flask&page=1
    """
    query = request.args.get('q', default='', type=str)
    page = request.args.get('page', default=1, type=int)
    
    if not query:
        return jsonify({"error": "Bad Request", "message": "Query parameter 'q' is required."}), 400
        
    return jsonify({
        "search_query": query,
        "page_number": page,
        "results": [f"Result 1 for '{query}'", f"Result 2 for '{query}'"]
    }), 200


# =============================================================================
# STEP 5: Handling POST Requests & Explicit Responses (`make_response`)
# =============================================================================

@app.route('/api/login', methods=['POST'])
def login():
    """
    Step 5: POST Endpoint receiving JSON payload and building response with cookies
    """
    data = request.get_json(silent=True) or request.form.to_dict()
    
    if not data or not data.get('username'):
        return jsonify({"error": "Missing username in request payload"}), 400
        
    response_payload = {
        "status": "authenticated",
        "user": data.get('username')
    }
    
    # Wrap response explicitly to add custom headers and cookies
    resp = make_response(jsonify(response_payload), 200)
    resp.headers['X-Auth-Token-Issued'] = 'True'
    resp.set_cookie('session_id', 'xyz-secure-token-99', httponly=True)
    
    return resp


# =============================================================================
# STEP 6 (OPTIONAL / ADVANCED): Custom Regex URL Converter
# =============================================================================
# NOTE FOR BEGINNERS: Built-in converters (int, str, path) are enough for 95% of apps!
# This custom regex converter is included only as an advanced bonus topic.

from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super().__init__(url_map)
        self.regex = items[0]

# Register custom regex converter on Flask's url_map
app.url_map.converters['regex'] = RegexConverter

@app.route('/product/<regex(r"PRD-\\d{4}"):sku>')
def get_product(sku):
    return jsonify({"product_sku": sku, "status": "available"}), 200


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 02 Dynamic Routing Practice Application...")
    print("🌐 Open browser at: http://127.0.0.1:5000/")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
