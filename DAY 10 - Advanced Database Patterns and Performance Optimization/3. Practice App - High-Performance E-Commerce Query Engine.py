"""
Day 10 Practice Application: High-Performance E-Commerce Query Engine
=====================================================================
This application demonstrates:
1. Creating single-column and composite multi-column indexes on models.
2. Defining hybrid properties (@hybrid_property) for Python/SQL calculations.
3. Executing raw SQL queries safely with text() and bound parameters.
4. Profiling SQL query execution count and latency via event listeners.
5. Configuring connection pool settings with pool_pre_ping=True.
"""

import time
from flask import Flask, jsonify, request, render_template_string, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, text, Index
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.engine import Engine
from sqlalchemy.orm import selectinload

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day10-performance-optimization-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce_performance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 1800,
    'pool_pre_ping': True
}

db = SQLAlchemy(app)

# Track total queries executed per HTTP request
query_audit_log = []

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    latency_ms = (time.time() - context._query_start_time) * 1000
    query_audit_log.append({
        "sql": str(statement).strip(),
        "latency_ms": round(latency_ms, 3)
    })


# ------------------------------------------------------------------------------
# 1. Models with Composite Indexes & Hybrid Properties
# ------------------------------------------------------------------------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    orders = db.relationship('Order', backref='user', lazy='selectin')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='COMPLETED')
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan', lazy='selectin')

    # Composite Multi-Column Index
    __table_args__ = (
        Index('idx_order_user_status', 'user_id', 'status'),
    )


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), index=True, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Hybrid Property: Python & SQL calculation
    @hybrid_property
    def line_total(self):
        return self.unit_price * self.quantity

    @line_total.expression
    def line_total(cls):
        return cls.unit_price * cls.quantity


# Initialize Database & Seed Benchmark Data
with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(User)).scalars().first():
        u1 = User(username="alice_dev", email="alice@test.com")
        u2 = User(username="bob_dev", email="bob@test.com")
        
        o1 = Order(order_number="ORD-10001", user=u1, status="COMPLETED")
        i1 = OrderItem(product_name="Mechanical Keyboard", unit_price=89.99, quantity=2, order=o1)
        i2 = OrderItem(product_name="Wireless Mouse", unit_price=49.99, quantity=1, order=o1)

        o2 = Order(order_number="ORD-10002", user=u2, status="COMPLETED")
        i3 = OrderItem(product_name="4K Monitor", unit_price=399.99, quantity=1, order=o2)

        db.session.add_all([u1, u2, o1, o2, i1, i2, i3])
        db.session.commit()


# Reset Query Audit Log before each request
@app.before_request
def clear_query_log():
    query_audit_log.clear()


# ------------------------------------------------------------------------------
# 2. HTML Diagnostic Dashboard Template
# ------------------------------------------------------------------------------
PERF_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 10 Performance Optimization Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
        .card { max-width: 900px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .sql-box { background: #1a202c; color: #63b3ed; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 0.85em; margin-bottom: 10px; overflow-x: auto; }
        .badge { background: #319795; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.85em; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background: #2d3748; color: white; }
    </style>
</head>
<body>
    <div class="card">
        <h2>⚡ High-Performance Query Diagnostics (Day 10)</h2>
        <p>Demonstrating Hybrid Attributes, Bound Raw SQL, and Real-Time Event Listener Query Profiling.</p>

        <h3>Order Summaries (Hybrid Property Calculations)</h3>
        <table>
            <thead>
                <tr>
                    <th>Order #</th>
                    <th>Customer</th>
                    <th>Status</th>
                    <th>Line Items Total (Hybrid Computed)</th>
                </tr>
            </thead>
            <tbody>
                {% for o in orders %}
                <tr>
                    <td><strong>{{ o.order_number }}</strong></td>
                    <td>{{ o.user.username }}</td>
                    <td><span class="badge">{{ o.status }}</span></td>
                    <td>${{ "%.2f"|format(o.items|sum(attribute='line_total')) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <h3>Executed SQL Query Profiler (Total SQL Queries: {{ queries|length }})</h3>
        {% for q in queries %}
            <div class="sql-box">
                [Latency: {{ q.latency_ms }}ms] -- {{ q.sql }}
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 3. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    stmt = db.select(Order).options(selectinload(Order.user), selectinload(Order.items))
    orders = db.session.execute(stmt).scalars().all()
    return render_template_string(PERF_HTML, orders=orders, queries=list(query_audit_log))

@app.route('/api/raw-sql')
def raw_sql_api():
    """Demonstrates executing raw SQL queries safely with bound parameters."""
    raw_query = text("""
        SELECT u.username, o.order_number, SUM(i.unit_price * i.quantity) as order_total
        FROM users u
        JOIN orders o ON u.id = o.user_id
        JOIN order_items i ON o.id = i.order_id
        WHERE o.status = :status
        GROUP BY o.id
    """)
    results = db.session.execute(raw_query, {"status": "COMPLETED"}).all()
    
    data = []
    for r in results:
        data.append({
            "username": r.username,
            "order_number": r.order_number,
            "order_total": round(r.order_total, 2)
        })

    return jsonify({
        "query_results": data,
        "queries_executed": list(query_audit_log)
    })


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 10 Performance Optimization Application...")
    print("Dashboard UI at http://127.0.0.1:5000/")
    print("Raw SQL API at http://127.0.0.1:5000/api/raw-sql")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
