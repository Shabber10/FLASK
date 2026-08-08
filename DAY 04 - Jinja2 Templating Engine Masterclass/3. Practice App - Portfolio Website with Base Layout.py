# Day 04 Practice App: Rendering Templates with Context
from flask import Flask, render_template_string

app = Flask(__name__)

BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h2>User Roster (Total: {{ users|length }})</h2>
    <ul>
    {% for u in users %}
        <li><strong>{{ u.name|upper }}</strong> - Role: {{ u.role }}</li>
    {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def home():
    users_data = [
        {"name": "Alice", "role": "Admin"},
        {"name": "Bob", "role": "Developer"},
        {"name": "Charlie", "role": "Designer"}
    ]
    return render_template_string(BASE_TEMPLATE, title="Day 04 Jinja2", users=users_data)

if __name__ == '__main__':
    app.run(debug=True)
