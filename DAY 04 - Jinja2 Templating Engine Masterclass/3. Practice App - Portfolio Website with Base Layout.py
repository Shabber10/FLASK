"""
Day 04 Practice Application: Jinja2 Masterclass & Portfolio Engine
===================================================================
This application demonstrates:
1. Template inheritance with base layouts, content blocks, and super().
2. Defining & calling custom Jinja2 filters and tests.
3. Defining & invoking Jinja2 macros for UI components.
4. Using loop context variables (loop.index, loop.cycle).
5. Safe HTML rendering & autoescaping protections.
"""

from flask import Flask, render_template_string
import datetime

app = Flask(__name__)

# ------------------------------------------------------------------------------
# 1. Register Custom Filters and Tests
# ------------------------------------------------------------------------------
@app.template_filter('currency')
def currency_filter(amount):
    return f"${amount:,.2f}"

@app.template_filter('short_date')
def short_date_filter(dt_str):
    dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
    return dt.strftime("%b %d, %Y")

@app.template_test('premium')
def is_premium(tier):
    return tier.lower() in ['pro', 'enterprise', 'vip']


# ------------------------------------------------------------------------------
# 2. Template Definitions (Simulating Modular Jinja Templates)
# ------------------------------------------------------------------------------
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Portfolio Engine{% endblock %}</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background: #f8f9fa; }
        .navbar { background: #2c3e50; padding: 15px; color: white; }
        .container { max-width: 900px; margin: 30px auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .row-even { background-color: #ffffff; }
        .row-odd { background-color: #f2f4f7; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: white; font-weight: bold; }
        .badge-pro { background: #9b59b6; }
        .badge-std { background: #7f8c8d; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
    </style>
    {% block styles %}{% endblock %}
</head>
<body>
    <div class="navbar">
        <strong>🚀 Day 04: Jinja2 Masterclass Portfolio Engine</strong>
    </div>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    {% block footer %}
    <div style="text-align:center; padding: 15px; color: #7f8c8d;">
        <p>&copy; {{ current_year }} Portfolio Engine | All Rights Reserved</p>
    </div>
    {% endblock %}
</body>
</html>
"""

INDEX_TEMPLATE = """
{% extends base_template %}

{% macro render_badge(tier) %}
    {% if tier is premium %}
        <span class="badge badge-pro">PRO TIER</span>
    {% else %}
        <span class="badge badge-std">STANDARD</span>
    {% endif %}
{% endmacro %}

{% block title %}Developer Roster - Jinja2 Masterclass{% endblock %}

{% block content %}
    <h2>Developer Portfolio Roster (Total: {{ developers|length }})</h2>
    
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Developer Name</th>
                <th>Role</th>
                <th>Rate</th>
                <th>Joined Date</th>
                <th>Account Status</th>
            </tr>
        </thead>
        <tbody>
        {% for dev in developers %}
            <li-row class="{{ loop.cycle('row-even', 'row-odd') }}">
                <tr>
                    <td>{{ loop.index }}</td>
                    <td><strong>{{ dev.name|title }}</strong></td>
                    <td>{{ dev.role }}</td>
                    <td>{{ dev.hourly_rate|currency }} / hr</td>
                    <td>{{ dev.joined|short_date }}</td>
                    <td>{{ render_badge(dev.tier) }}</td>
                </tr>
            </li-row>
        {% else %}
            <tr><td colspan="6">No developers registered.</td></tr>
        {% endfor %}
        </tbody>
    </table>
{% endblock %}
"""


# ------------------------------------------------------------------------------
# 3. Context Processor & Route Handlers
# ------------------------------------------------------------------------------
@app.context_processor
def inject_global_year():
    return {'current_year': datetime.datetime.now().year}

@app.route('/')
def index():
    devs = [
        {"name": "alice smith", "role": "Fullstack Engineer", "hourly_rate": 85.50, "joined": "2024-03-15", "tier": "Pro"},
        {"name": "bob jones", "role": "DevOps Architect", "hourly_rate": 110.00, "joined": "2023-11-01", "tier": "Enterprise"},
        {"name": "charlie brown", "role": "Frontend Designer", "hourly_rate": 65.00, "joined": "2025-01-20", "tier": "Standard"}
    ]
    return render_template_string(INDEX_TEMPLATE, base_template=BASE_TEMPLATE, developers=devs)


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 04 Jinja2 Masterclass Application...")
    print("Test endpoint at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
