"""
===============================================================================
Day 07 Practice Script: Advanced Catalog Search, Filtering & Analytics
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Setting up catalog model (`Product`) and pre-seeding sample data.
2. STEP 2: Pattern matching (`ilike`) and numerical range filtering (`>=`, `<=`).
3. STEP 3: Logical operators (`and_`, `or_`, `not_`) and dynamic result sorting (`order_by`).
4. STEP 4: Paginated query execution using `db.paginate()` helper objects.
5. STEP 5: SQL aggregations (`func.count`, `func.avg`, `func.max`, `group_by`) via JSON API.
6. STEP 6 (ADVANCED - OPTIONAL): Nested transactions and savepoints (`db.session.begin_nested()`).

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Product Search with Advanced Filtering and Pagination.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day07-advanced-querying-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# =============================================================================
# STEP 1: Product ORM Model Definition & Pre-seeding
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


# Initialize DB Tables & Pre-seed Catalog Data inside app_context
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
# STEP 2 & 3 & 4: Search, Filtering, Sorting & Pagination View Handler
# =============================================================================

@app.route('/')
def index():
    """
    Renders catalog search UI using templates/products.html with dynamic filtering and pagination.
    """
    # Parse URL Query Parameters
    q = request.args.get('q', '', type=str).strip()
    category = request.args.get('category', '', type=str).strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'name_asc', type=str)
    page = request.args.get('page', 1, type=int)

    # 1. Base Select Query Statement
    stmt = db.select(Product)

    # 2. Step 2: Dynamically Append Filters
    if q:
        # Case-insensitive partial pattern match
        stmt = stmt.where(Product.name.ilike(f"%{q}%"))
    if category:
        stmt = stmt.where(Product.category == category)
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)

    # 3. Step 3: Apply Dynamic Sorting Rules
    if sort_by == 'price_asc':
        stmt = stmt.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        stmt = stmt.order_by(Product.price.desc())
    elif sort_by == 'rating_desc':
        stmt = stmt.order_by(Product.rating.desc())
    else:
        stmt = stmt.order_by(Product.name.asc())

    # 4. Step 4: Execute Paginated Query (5 items per page)
    pagination = db.paginate(stmt, page=page, per_page=5, error_out=False)

    # 5. Fetch Distinct Categories for Filter Dropdown
    cat_stmt = db.select(Product.category).distinct()
    categories = db.session.execute(cat_stmt).scalars().all()

    query_params = {"q": q, "category": category, "min_price": min_price, "max_price": max_price, "sort": sort_by}

    return render_template('products.html', pagination=pagination, categories=categories, query_params=query_params)


# =============================================================================
# STEP 5: SQL Aggregations & Analytics API
# =============================================================================

@app.route('/api/stats')
def category_stats_api():
    """
    Step 5: API Endpoint demonstrating SQL Aggregations and GROUP BY using func.
    """
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
# STEP 6 (OPTIONAL / ADVANCED): Savepoints & Nested Transactions Demo
# =============================================================================

def run_savepoint_demo():
    """Demonstrates creating savepoints with db.session.begin_nested()"""
    with app.app_context():
        try:
            # Savepoint (Nested Transaction Checkpoint)
            savepoint = db.session.begin_nested()
            temp_p = Product(name="Temp Test Item", category="Electronics", price=1.0)
            db.session.add(temp_p)
            db.session.flush()
            # Rollback only to savepoint
            savepoint.rollback()
            db.session.commit()
            print("✅ Savepoint demo executed successfully (temp item rolled back).")
        except Exception as e:
            db.session.rollback()


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    run_savepoint_demo()
    print("=" * 75)
    print("🚀 Starting Day 07 Advanced Catalog Application...")
    print("🌐 Search UI at: http://127.0.0.1:5000/")
    print("📡 Analytics API at: http://127.0.0.1:5000/api/stats")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
