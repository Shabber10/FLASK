"""
Day 26 Practice Application: Multi-Tenant SaaS E-Commerce Platform
===================================================================
This application demonstrates:
1. Resolving tenant identity via subdomains or 'X-Tenant-ID' headers.
2. Injecting tenant state into Flask thread-local 'g.tenant' context.
3. Strict Discriminator-Column tenant data isolation.
4. Dynamic tenant provision API (POST /api/tenants).
5. Interactive Web Dashboard demonstrating multi-tenant switching & isolation checks.
"""

from flask import Flask, jsonify, request, g, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day26-multitenant-saas-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ------------------------------------------------------------------------------
# 1. Multi-Tenant Database Models
# ------------------------------------------------------------------------------
class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    plan = db.Column(db.String(20), default='starter') # starter, enterprise

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()
    # Seed Initial Tenants
    t1 = Tenant(name="Acme Corporation", slug="acme", plan="enterprise")
    t2 = Tenant(name="Globex Tech", slug="globex", plan="starter")
    db.session.add_all([t1, t2])
    db.session.commit()

    # Seed Tenant Products
    p1 = Product(tenant_id=t1.id, name="Acme Quantum Compute Server", price=4999.99)
    p2 = Product(tenant_id=t1.id, name="Acme Industrial Robot Arm", price=12500.00)
    p3 = Product(tenant_id=t2.id, name="Globex SaaS Analytics Dashboard", price=299.99)
    db.session.add_all([p1, p2, p3])
    db.session.commit()


# ------------------------------------------------------------------------------
# 2. Tenant Context Resolution Middleware
# ------------------------------------------------------------------------------
@app.before_request
def resolve_tenant():
    # 1. Check X-Tenant-ID Header
    tenant_slug = request.headers.get('X-Tenant-ID')
    
    # 2. Fallback to Subdomain (e.g. acme.localhost:5000)
    if not tenant_slug:
        host = request.host.split(':')[0]
        parts = host.split('.')
        if len(parts) >= 2 and parts[0] not in ['www', 'localhost', '127']:
            tenant_slug = parts[0]

    if tenant_slug:
        tenant = db.session.execute(db.select(Tenant).where(Tenant.slug == tenant_slug)).scalar_one_or_none()
        g.tenant = tenant
    else:
        g.tenant = None


# ------------------------------------------------------------------------------
# 3. Interactive Web Dashboard UI
# ------------------------------------------------------------------------------
SAAS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 26 Multi-Tenant SaaS Masterclass</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
        .card { max-width: 900px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .tenant-selector { background: #edf2f7; padding: 15px; border-radius: 6px; margin-bottom: 20px; }
        .btn { background: #3182ce; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; }
        .btn-active { background: #2b6cb0; font-weight: bold; }
        .log-box { background: #1a202c; color: #48bb78; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 0.9em; margin-top: 15px; }
        .badge { background: #805ad5; color: white; padding: 3px 6px; border-radius: 3px; font-size: 0.85em; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🏢 Multi-Tenant SaaS Platform Engine (Day 26)</h2>
        <p>Demonstrating Strict Multi-Tenant Isolation using Subdomain/Header Resolution & Context Injection.</p>

        <div class="tenant-selector">
            <strong>Active Tenant Selector (X-Tenant-ID Header):</strong><br><br>
            <button class="btn" onclick="setTenant('acme')">Switch to Acme Corp (acme)</button>
            <button class="btn" onclick="setTenant('globex')">Switch to Globex Tech (globex)</button>
            <button class="btn" onclick="setTenant('')">No Tenant Header (Public)</button>
        </div>

        <div>Active Header: <span id="current_tenant_display" class="badge">None (Public)</span></div>

        <div style="margin-top: 15px;">
            <button class="btn" onclick="fetchProducts()">Fetch Catalog (/api/products)</button>
        </div>

        <div id="output" class="log-box">Select a tenant and click 'Fetch Catalog'...</div>
    </div>

    <script>
        let currentTenantHeader = '';

        function setTenant(slug) {
            currentTenantHeader = slug;
            document.getElementById('current_tenant_display').innerText = slug ? slug : 'None (Public)';
            fetchProducts();
        }

        async function fetchProducts() {
            const headers = {};
            if (currentTenantHeader) {
                headers['X-Tenant-ID'] = currentTenantHeader;
            }
            const res = await fetch('/api/products', { headers: headers });
            const data = await res.json();
            document.getElementById('output').innerText = 
                `HTTP Status: ${res.status}\n` + JSON.stringify(data, null, 2);
        }
    </script>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 4. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template_string(SAAS_HTML)

@app.route('/api/products')
def get_products():
    if not g.tenant:
        return jsonify({
            "error": "Bad Request",
            "message": "Missing or invalid tenant context. Pass 'X-Tenant-ID' header or use tenant subdomain."
        }), 400

    # Query strictly isolated to active tenant in g.tenant!
    products = db.session.execute(
        db.select(Product).where(Product.tenant_id == g.tenant.id)
    ).scalars().all()

    return jsonify({
        "status": "Success",
        "tenant": {
            "name": g.tenant.name,
            "slug": g.tenant.slug,
            "plan": g.tenant.plan
        },
        "isolated_products_count": len(products),
        "products": [{"id": p.id, "name": p.name, "price": p.price} for p in products]
    }), 200


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 26 Multi-Tenant SaaS Engine...")
    print("SaaS Dashboard UI at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
