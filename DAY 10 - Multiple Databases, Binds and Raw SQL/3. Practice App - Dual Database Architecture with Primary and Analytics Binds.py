"""
===============================================================================
Day 10 Practice Script: Dual Database Binds & Raw SQL Architecture
===============================================================================
This script demonstrates:
1. Setting up multiple database connection binds (`SQLALCHEMY_BINDS`).
2. Binding ORM models to specific database files (`__bind_key__`).
3. Safe execution of Raw SQL queries using `sqlalchemy.text()` and bound parameters.
4. Performing transactions across multiple database engines.
5. Exposing an interactive dual-DB management UI and REST API.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Dual Database Architecture with Primary and Analytics Binds.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import datetime
from flask import Flask, jsonify, request, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day10-multidb-secret-key'

# Primary Database Connection URI (Stores Core Users & Orders)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_primary.db'

# Secondary Database Binds (Stores Audit System Logs)
app.config['SQLALCHEMY_BINDS'] = {
    'audit': 'sqlite:///app_audit.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy extension instance
db = SQLAlchemy(app)


# =============================================================================
# 1. Primary Database ORM Models (primary.db)
# =============================================================================
class User(db.Model):
    """Primary DB Model representing Users."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='user', lazy='selectin')


class Order(db.Model):
    """Primary DB Model representing Financial Orders."""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# =============================================================================
# 2. Secondary Database ORM Model (audit.db)
# =============================================================================
class AuditLog(db.Model):
    """Audit DB Model representing System Event Logs."""
    __tablename__ = 'audit_logs'
    __bind_key__ = 'audit'  # Explicitly bound to app_audit.db!

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(150), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "event": self.event,
            "user_identity": self.user_identity,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }


# Initialize tables across ALL binds & pre-seed initial data
with app.app_context():
    # db.create_all() creates tables in both primary.db and audit.db!
    db.create_all()

    if not db.session.execute(db.select(User)).scalars().first():
        print("🌱 Pre-seeding data in Primary and Audit databases...")
        u1 = User(username="alice_dev", email="alice@dev.com")
        u2 = User(username="bob_admin", email="bob@admin.com")
        db.session.add_all([u1, u2])
        db.session.flush()

        o1 = Order(item_name="Mechanical Keyboard", amount=120.00, user=u1)
        o2 = Order(item_name="USB-C Hub", amount=45.00, user=u1)
        o3 = Order(item_name="4K Monitor", amount=350.00, user=u2)
        db.session.add_all([o1, o2, o3])

        log1 = AuditLog(event="DATABASE_INITIALIZED", user_identity="SYSTEM")
        log2 = AuditLog(event="USER_CREATED", user_identity="alice_dev")
        db.session.add_all([log1, log2])

        db.session.commit()
        print("✅ Dual databases pre-seeded successfully!")


# =============================================================================
# 3. HTML UI Template String
# =============================================================================
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 10 Dual Database Binds</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 30px; color: #333; }
        .grid { display: flex; gap: 20px; max-width: 1000px; margin: auto; }
        .card { flex: 1; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
        h2 { color: #2c3e50; margin-top: 0; }
        .badge { background: #27ae60; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
        .badge-audit { background: #e67e22; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
        th { background: #34495e; color: white; }
    </style>
</head>
<body>
    <div style="max-width: 1000px; margin: 0 auto 20px auto;">
        <h2>🔀 Dual Database Binds & Raw SQL Demo (Day 10)</h2>
    </div>

    <div class="grid">
        <!-- Card 1: Primary Database -->
        <div class="card">
            <h3><span class="badge">Primary DB</span> Users & Orders</h3>
            <table>
                <thead>
                    <tr><th>User</th><th>Orders</th></tr>
                </thead>
                <tbody>
                    {% for u in users %}
                    <tr>
                        <td><strong>{{ u.username }}</strong></td>
                        <td>
                            {% for o in u.orders %}
                                • {{ o.item_name }} (${{ "%.2f"|format(o.amount) }})<br>
                            {% endfor %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <!-- Card 2: Audit Database -->
        <div class="card">
            <h3><span class="badge-audit">Audit DB</span> System Logs</h3>
            <table>
                <thead>
                    <tr><th>Event</th><th>User</th><th>Time</th></tr>
                </thead>
                <tbody>
                    {% for log in logs %}
                    <tr>
                        <td>{{ log.event }}</td>
                        <td><strong>{{ log.user_identity }}</strong></td>
                        <td>{{ log.timestamp.strftime("%H:%M:%S") }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""


# =============================================================================
# 4. Route Handlers
# =============================================================================
@app.route('/')
def index():
    """Renders HTML UI fetching data from both Primary and Audit databases."""
    users = db.session.execute(db.select(User)).scalars().all()
    logs = db.session.execute(db.select(AuditLog).order_by(AuditLog.id.desc())).scalars().all()
    return render_template_string(INDEX_HTML, users=users, logs=logs)


@app.route('/api/raw-sql')
def raw_sql_demo():
    """Demonstrates SAFE Raw SQL execution with text() and bound parameters."""
    min_amount = request.args.get('min_amount', 50.0, type=float)

    # SAFE: Wrapped in text() using :min_val parameter binding
    raw_query = text("""
        SELECT u.username, o.item_name, o.amount 
        FROM users u 
        JOIN orders o ON u.id = o.user_id 
        WHERE o.amount >= :min_val 
        ORDER BY o.amount DESC
    """)

    result = db.session.execute(raw_query, {"min_val": min_amount}).fetchall()

    orders_list = [
        {"username": row.username, "item_name": row.item_name, "amount": row.amount}
        for row in result
    ]

    return jsonify({"filter_min_amount": min_amount, "results": orders_list}), 200


@app.route('/api/audit-logs')
def list_audit_logs():
    """API Endpoint fetching logs from secondary audit database."""
    stmt = db.select(AuditLog).order_by(AuditLog.id.desc())
    logs = db.session.execute(stmt).scalars().all()
    return jsonify([l.to_dict() for l in logs]), 200


# =============================================================================
# 5. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 10 Dual Database Application...")
    print("🌐 Open Web UI at: http://127.0.0.1:5000/")
    print("📡 Test Raw SQL API at: http://127.0.0.1:5000/api/raw-sql")
    print("📡 Test Audit Logs API at: http://127.0.0.1:5000/api/audit-logs")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
