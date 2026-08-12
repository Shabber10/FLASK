"""
===============================================================================
Day 10 Practice Script: Dual Database Binds & Raw SQL Architecture
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Setting up multiple database connection binds (`SQLALCHEMY_BINDS`).
2. STEP 2: Binding ORM models to specific database files (`__bind_key__`).
3. STEP 3: Initializing tables across ALL binds & pre-seeding initial data in `app.app_context()`.
4. STEP 4: Web UI dashboard route handler (`/`) using `render_template('index.html')`.
5. STEP 5: Safe execution of Raw SQL queries using `sqlalchemy.text()` and bound parameters.
6. STEP 6: Retrieving secondary database engine objects using `db.get_engine()`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Dual Database Architecture with Primary and Analytics Binds.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day10-multidb-secret-key'

# =============================================================================
# STEP 1: Configure Primary & Secondary Database Binds
# =============================================================================

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
# STEP 2: Primary & Secondary ORM Models (__bind_key__)
# =============================================================================

class User(db.Model):
    """Primary DB Model representing Users (Stored in app_primary.db)."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='user', lazy='selectin')


class Order(db.Model):
    """Primary DB Model representing Financial Orders (Stored in app_primary.db)."""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class AuditLog(db.Model):
    """Audit DB Model representing System Event Logs (Stored in app_audit.db)."""
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


# =============================================================================
# STEP 3: Database Creation & Data Pre-seeding
# =============================================================================

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
# STEP 4: Dual Database Dashboard Route Handler (HTML via render_template)
# =============================================================================

@app.route('/')
def index():
    """
    Step 4: Renders HTML UI fetching data from both Primary and Audit databases.
    Uses templates/index.html file.
    """
    users = db.session.execute(db.select(User)).scalars().all()
    logs = db.session.execute(db.select(AuditLog).order_by(AuditLog.id.desc())).scalars().all()
    return render_template('index.html', users=users, logs=logs)


# =============================================================================
# STEP 5: Safe Parameterized Raw SQL Execution Endpoint
# =============================================================================

@app.route('/api/raw-sql')
def raw_sql_demo():
    """
    Step 5: Demonstrates SAFE Raw SQL execution with text() and bound parameters.
    """
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
# STEP 6: Engine Inspection & Connection Pool Helper
# =============================================================================

def inspect_database_engines():
    """Step 6: Inspects active database engine objects for binds."""
    with app.app_context():
        primary_engine = db.engine
        audit_engine = db.get_engine(bind='audit')
        print(f"ℹ️ Primary DB Engine Driver: {primary_engine.driver}")
        print(f"ℹ️ Audit DB Engine Driver: {audit_engine.driver}")


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    inspect_database_engines()
    print("=" * 75)
    print("🚀 Starting Day 10 Dual Database Application...")
    print("🌐 Open Web Dashboard at: http://127.0.0.1:5000/")
    print("📡 Test Raw SQL API at: http://127.0.0.1:5000/api/raw-sql")
    print("📡 Test Audit Logs API at: http://127.0.0.1:5000/api/audit-logs")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
