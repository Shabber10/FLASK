"""
===============================================================================
Day 04 Practice Script: Jinja2 Masterclass & Portfolio Roster Engine
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Rendering real HTML template files using `render_template('index.html')`.
2. STEP 2: Registering custom Jinja filters (`currency`, `short_date`).
3. STEP 3: Registering custom Jinja tests (`is premium`).
4. STEP 4: Passing dynamic Python list data to template loops.
5. STEP 5: Injecting global variables into templates via `@app.context_processor`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Portfolio Website with Base Layout.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import datetime
from flask import Flask, render_template

app = Flask(__name__)
app.config['SITE_NAME'] = 'Enterprise Portfolio Engine'


# =============================================================================
# STEP 2 & 3: Custom Jinja Filters & Tests Registration
# =============================================================================

@app.template_filter('currency')
def currency_filter(amount):
    """
    Step 2a Custom Filter: Formats raw float values into currency strings ($85.50).
    Used in Jinja2 template as: {{ dev.hourly_rate|currency }}
    """
    return f"${amount:,.2f}"


@app.template_filter('short_date')
def short_date_filter(dt_str):
    """
    Step 2b Custom Filter: Formats YYYY-MM-DD strings into friendly dates (Mar 15, 2024).
    Used in Jinja2 template as: {{ dev.joined|short_date }}
    """
    dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
    return dt.strftime("%b %d, %Y")


@app.template_test('premium')
def is_premium(tier):
    """
    Step 3 Custom Test: Evaluates if a user account tier is premium (returns True/False).
    Used in Jinja2 template as: {% if tier is premium %}
    """
    return str(tier).lower() in ['pro', 'enterprise', 'vip']


# =============================================================================
# STEP 5: Global Template Context Processor
# =============================================================================

@app.context_processor
def inject_global_year():
    """
    Step 5: Injects current year globally into template footers across the app.
    """
    return {
        'current_year': datetime.datetime.now().year,
        'platform_name': app.config['SITE_NAME']
    }


# =============================================================================
# STEP 1 & 4: Route Handlers & Template Rendering
# =============================================================================

@app.route('/')
def index():
    """
    Step 1 & 4: Renders developer roster using templates/index.html file.
    Flask automatically searches the local templates/ directory for index.html!
    """
    developers = [
        {"name": "alice smith", "role": "Fullstack Engineer", "hourly_rate": 85.50, "joined": "2024-03-15", "tier": "Pro"},
        {"name": "bob jones", "role": "DevOps Architect", "hourly_rate": 110.00, "joined": "2023-11-01", "tier": "Enterprise"},
        {"name": "charlie brown", "role": "Frontend Designer", "hourly_rate": 65.00, "joined": "2025-01-20", "tier": "Standard"}
    ]
    return render_template('index.html', developers=developers)


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 04 Jinja2 Masterclass Application...")
    print("🌐 Open browser at: http://127.0.0.1:5000/")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
