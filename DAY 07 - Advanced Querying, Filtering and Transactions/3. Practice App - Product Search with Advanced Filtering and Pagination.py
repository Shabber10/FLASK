"""
===============================================================================
Day 07 Practice Script: Advanced Catalog Search, Filtering & Analytics
===============================================================================
This script demonstrates:
1. Multi-condition logical query building (`ilike` pattern matching, price ranges).
2. Dynamic result sorting by multiple attributes.
3. Pagination execution with `db.paginate()` helper objects.
4. Aggregations using `sqlalchemy.func` (`count`, `avg`, `max`, `group_by`).
5. Exposing an interactive search UI and a JSON analytics API.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Product Search with Advanced Filtering and Pagination.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day07-advanced-querying-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# =============================================================================
# 1. Product ORM Model Definition
# =============================================================================
class Product(db.Model):
    """ORM Model representing the 'products' database table."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=4.0)
    stock = db.Column(db.Integer, nullable=False, default=10)

    def to_dict(self):
        """Serializes model instance into a JSON dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "rating": self.rating,
            "stock": self.stock
        }


# Initialize DB Tables & Pre-seed Catalog Data
with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(Product)).scalars().first():
        print("🌱 Pre-seeding catalog products into SQLite database...")
        products_data = [
            # Electronics
            Product(name="Pro Wireless Mouse", category="Electronics", price=49.99, rating=4.5, stock=50),
            Product(name="Mechanical RGB Keyboard", category="Electronics", price=89.99, rating=4.7, stock=30),
            Product(name="Ultra HD 4K Monitor", category="Electronics", price=349.99, rating=4.8, stock=15),
            Product(name="Noise Canceling Headphones", category="Electronics", price=199.99, rating=4.6, stock=25),
            Product(name="USB-C Docking Station", category="Electronics", price=79.99, rating=4.2, stock=40),
            
            # Books
            Product(name="Mastering Flask Web Architecture", category="Books", price=39.99, rating=4.9, stock=100),
            Product(name="Python High Performance", category="Books", price=44.99, rating=4.7, stock=80),
            Product(name="Designing Data-Intensive Apps", category="Books", price=54.99, rating=5.0, stock=60),
            Product(name="Clean Architecture in Python", category="Books", price=34.99, rating=4.4, stock=45),
            
            # Apparel & Furniture
            Product(name="Developer Hoodie - Dark Mode", category="Apparel", price=59.99, rating=4.8, stock=70),
            Product(name="Binary Code Graphic Tee", category="Apparel", price=24.99, rating=4.3, stock=120),
            Product(name="Ergonomic Desk Chair", category="Furniture", price=299.99, rating=4.6, stock=10)
        ]
        db.session.add_all(products_data)
        db.session.commit()
        print("✅ Catalog data seeded successfully!")


# =============================================================================
# 2. HTML UI Template String
# =============================================================================
SEARCH_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 07 Catalog Search</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 30px; color: #333; }
        .card { max-width: 950px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
        .filter-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; background: #f8f9fa; padding: 15px; border-radius: 6px; border: 1px solid #e9ecef; }
        .filter-bar input, .filter-bar select { padding: 9px; border: 1px solid #ccc; border-radius: 4px; }
        .btn { background: #2980b9; color: white; border: none; padding: 9px 18px; border-radius: 4px; cursor: pointer; font-weight: bold; }
        .btn:hover { background: #21618c; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; border-bottom: 1px solid #e9ecef; text-align: left; }
        th { background: #34495e; color: white; }
        .pagination { display: flex; gap: 5px; margin-top: 20px; justify-content: center; }
        .page-link { padding: 8px 14px; border: 1px solid #ccc; text-decoration: none; color: #333; border-radius: 4px; font-weight: bold; }
        .page-link.active { background: #2980b9; color: white; border-color: #2980b9; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🔍 Product Catalog Search & Filtering (Day 07)</h2>

        <!-- Search & Filter Controls -->
        <form class="filter-bar" method="GET" action="/">
            <input type="text" name="q" placeholder="Search product name..." value="{{ query_params.q or '' }}">
            <select name="category">
                <option value="">All Categories</option>
                {% for cat in categories %}
                    <option value="{{ cat }}" {% if query_params.category == cat %}selected{% endif %}>{{ cat }}</option>
                {% endfor %}
            </select>
            <input type="number" step="0.01" name="min_price" placeholder="Min $" value="{{ query_params.min_price or '' }}">
            <input type="number" step="0.01" name="max_price" placeholder="Max $" value="{{ query_params.max_price or '' }}">
            <select name="sort">
                <option value="name_asc" {% if query_params.sort == 'name_asc' %}selected{% endif %}>Name (A-Z)</option>
                <option value="price_asc" {% if query_params.sort == 'price_asc' %}selected{% endif %}>Price (Low -> High)</option>
                <option value="price_desc" {% if query_params.sort == 'price_desc' %}selected{% endif %}>Price (High -> Low)</option>
                <option value="rating_desc" {% if query_params.sort == 'rating_desc' %}selected{% endif %}>Rating (Highest First)</option>
            </select>
            <button class="btn" type="submit">Filter Products</button>
        </form>

        <p>Showing Page <strong>{{ pagination.page }}</strong> of <strong>{{ pagination.pages }}</strong> (Total Results: {{ pagination.total }})</p>

        <!-- Product Results Table -->
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Product Name</th>
                    <th>Category</th>
                    <th>Price</th>
                    <th>Rating</th>
                    <th>Stock</th>
                </tr>
            </thead>
            <tbody>
                {% for p in pagination.items %}
                <tr>
                    <td>{{ p.id }}</td>
                    <td><strong>{{ p.name }}</strong></td>
                    <td>{{ p.category }}</td>
                    <td>${{ "%.2f"|format(p.price) }}</td>
                    <td>⭐ {{ p.rating }}</td>
                    <td>{{ p.stock }} units</td>
                </tr>
                {% else %}
                <tr><td colspan="6">No products match specified search criteria.</td></tr>
                {% endfor %}
            </tbody>
        </table>

        <!-- Pagination Controls -->
        <div class="pagination">
            {% if pagination.has_prev %}
                <a class="page-link" href="{{ url_for('index', page=pagination.prev_num, **query_params) }}">&laquo; Prev</a>
            {% endif %}

            {% for page_num in range(1, pagination.pages + 1) %}
                <a class="page-link {% if page_num == pagination.page %}active{% endif %}" href="{{ url_for('index', page=page_num, **query_params) }}">{{ page_num }}</a>
            {% endfor %}

            {% if pagination.has_next %}
                <a class="page-link" href="{{ url_for('index', page=pagination.next_num, **query_params) }}">Next &raquo;</a>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""


# =============================================================================
# 3. Route Handlers
# =============================================================================
@app.route('/')
def index():
    """Renders catalog search UI with dynamic filtering and pagination."""
    # Parse URL Query Parameters
    q = request.args.get('q', '', type=str).strip()
    category = request.args.get('category', '', type=str).strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'name_asc', type=str)
    page = request.args.get('page', 1, type=int)

    # 1. Base Select Query Statement
    stmt = db.select(Product)

    # 2. Dynamically Append Filters
    if q:
        # Case-insensitive partial pattern match
        stmt = stmt.where(Product.name.ilike(f"%{q}%"))
    if category:
        stmt = stmt.where(Product.category == category)
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)

    # 3. Apply Dynamic Sorting Rules
    if sort_by == 'price_asc':
        stmt = stmt.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        stmt = stmt.order_by(Product.price.desc())
    elif sort_by == 'rating_desc':
        stmt = stmt.order_by(Product.rating.desc())
    else:
        stmt = stmt.order_by(Product.name.asc())

    # 4. Execute Paginated Query (5 items per page)
    pagination = db.paginate(stmt, page=page, per_page=5, error_out=False)

    # 5. Fetch Distinct Categories for Filter Dropdown
    cat_stmt = db.select(Product.category).distinct()
    categories = db.session.execute(cat_stmt).scalars().all()

    query_params = {"q": q, "category": category, "min_price": min_price, "max_price": max_price, "sort": sort_by}

    return render_template_string(SEARCH_HTML, pagination=pagination, categories=categories, query_params=query_params)


@app.route('/api/stats')
def category_stats_api():
    """API Endpoint demonstrating SQL Aggregations and GROUP BY using func."""
    stmt = db.select(
        Product.category,
        func.count(Product.id).label('total_products'),
        func.avg(Product.price).label('average_price'),
        func.max(Product.price).label('highest_price')
    ).group_by(Product.category)

    results = db.session.execute(stmt).all()
    
    stats = []
    for r in results:
        stats.append({
            "category": r.category,
            "total_products": r.total_products,
            "average_price": round(r.average_price, 2),
            "highest_price": r.highest_price
        })

    return jsonify({"category_analytics": stats}), 200


# =============================================================================
# 4. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 07 Advanced Catalog Application...")
    print("🌐 Search UI at: http://127.0.0.1:5000/")
    print("📡 Analytics API at: http://127.0.0.1:5000/api/stats")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
