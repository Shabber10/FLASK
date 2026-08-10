"""
===============================================================================
Day 04 Practice Script: Jinja2 Masterclass & Portfolio Roster Engine
===============================================================================
This script demonstrates:
1. Template inheritance with base layouts, content blocks, and extends.
2. Registering and calling custom Jinja2 filters (`currency`, `short_date`).
3. Registering and using custom Jinja2 tests (`is premium`).
4. Defining and invoking Jinja2 macros for reusable status badges.
5. Using loop context variables (`loop.index`, `loop.cycle`).

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Portfolio Website with Base Layout.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import datetime
from flask import Flask, render_template_string

app = Flask(__name__)

# =============================================================================
# 1. Custom Jinja Filters & Tests Registration
# =============================================================================

@app.template_filter('currency')
def currency_filter(amount):
    """Custom Filter: Formats raw float values into currency strings ($85.50)."""
    return f"${amount:,.2f}"


@app.template_filter('short_date')
def short_date_filter(dt_str):
    """Custom Filter: Formats YYYY-MM-DD strings into friendly dates (Mar 15, 2024)."""
    dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
    return dt.strftime("%b %d, %Y")


@app.template_test('premium')
def is_premium(tier):
    """Custom Test: Evaluates if a user account tier is premium (returns True/False)."""
    return str(tier).lower() in ['pro', 'enterprise', 'vip']


# =============================================================================
# 2. Template Definitions (Simulating Modular Jinja Template Files)
# =============================================================================

# Master Base Skeleton Template (Simulates base.html)
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Portfolio Roster Engine{% endblock %}</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background: #f8f9fa; color: #333; }
        .navbar { background: #2c3e50; padding: 18px 30px; color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .container { max-width: 950px; margin: 30px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .row-even { background-color: #ffffff; }
        .row-odd { background-color: #f8f9fa; }
        .badge { padding: 5px 10px; border-radius: 4px; font-size: 0.75em; color: white; font-weight: bold; }
        .badge-pro { background: #8e44ad; }
        .badge-std { background: #7f8c8d; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #e9ecef; }
        th { background-color: #e9ecef; }
    </style>
    {% block styles %}{% endblock %}
</head>
<body>
    <div class="navbar">
        <h2>🚀 Day 04: Jinja2 Masterclass Roster Engine</h2>
    </div>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    {% block footer %}
    <div style="text-align:center; padding: 20px; color: #7f8c8d; font-size: 0.9em;">
        <p>&copy; {{ current_year }} Enterprise Portfolio Engine | All Rights Reserved</p>
    </div>
    {% endblock %}
</body>
</html>
"""

# Child Template Extending Base Layout (Simulates index.html)
INDEX_TEMPLATE = """
{% extends base_template %}

{# Jinja2 Macro: Render Badge Component #}
{% macro render_badge(tier) %}
    {% if tier is premium %}
        <span class="badge badge-pro">PRO TIER</span>
    {% else %}
        <span class="badge badge-std">STANDARD</span>
    {% endif %}
{% endmacro %}

{% block title %}Developer Roster - Jinja2 Masterclass{% endblock %}

{% block content %}
    <h2>Registered Developers (Total: {{ developers|length }})</h2>
    
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Developer Name</th>
                <th>Role</th>
                <th>Hourly Rate</th>
                <th>Joined Date</th>
                <th>Membership Tier</th>
            </tr>
        </thead>
        <tbody>
        {% for dev in developers %}
            <tr class="{{ loop.cycle('row-even', 'row-odd') }}">
                <td>{{ loop.index }}</td>
                <td><strong>{{ dev.name|title }}</strong></td>
                <td>{{ dev.role }}</td>
                <td>{{ dev.hourly_rate|currency }} / hr</td>
                <td>{{ dev.joined|short_date }}</td>
                <td>{{ render_badge(dev.tier) }}</td>
            </tr>
        {% else %}
            <tr><td colspan="6">No developers registered in system.</td></tr>
        {% endfor %}
        </tbody>
    </table>
{% endblock %}
"""


# =============================================================================
# 3. Context Processor & Route Handlers
# =============================================================================

@app.context_processor
def inject_global_year():
    """Injects current year globally into template footers."""
    return {'current_year': datetime.datetime.now().year}


@app.route('/')
def index():
    """Renders developer roster using Jinja2 inheritance, filters, and macros."""
    devs = [
        {"name": "alice smith", "role": "Fullstack Engineer", "hourly_rate": 85.50, "joined": "2024-03-15", "tier": "Pro"},
        {"name": "bob jones", "role": "DevOps Architect", "hourly_rate": 110.00, "joined": "2023-11-01", "tier": "Enterprise"},
        {"name": "charlie brown", "role": "Frontend Designer", "hourly_rate": 65.00, "joined": "2025-01-20", "tier": "Standard"}
    ]
    return render_template_string(INDEX_TEMPLATE, base_template=BASE_TEMPLATE, developers=devs)


# =============================================================================
# 4. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 04 Jinja2 Masterclass Application...")
    print("🌐 Open browser at: http://127.0.0.1:5000/")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
