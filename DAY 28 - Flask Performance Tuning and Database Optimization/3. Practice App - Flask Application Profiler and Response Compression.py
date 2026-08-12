"""
===============================================================================
Day 28 Practice Script: Flask Performance Tuning & Database Optimization
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: ORM Models (`Author` 1 <---> N `Book`).
2. STEP 2: Intercepting and auditing SQL queries via SQLAlchemy engine event listeners.
3. STEP 3: In-memory database seeding routine (50 authors and 250 books).
4. STEP 4: REST API endpoints comparing Eager Loading (`joinedload()`) vs Lazy Loading N+1 Query Trap.
5. STEP 5: Interactive Web UI Performance Benchmark Dashboard rendering `templates/index.html`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Flask Application Profiler and Response Compression.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
from flask import Flask, jsonify, g, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_compress import Compress

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day28-performance-masterclass-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Compress(app)  # Enables transparent Gzip response compression


# =============================================================================
# STEP 1: ORM Models (Author 1 <---> N Book)
# =============================================================================
class Author(db.Model):
    """Step 1a: Author entity model."""
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy='select')


class Book(db.Model):
    """Step 1b: Book entity model."""
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)


# =============================================================================
# STEP 2: SQL Query Counter & Event Listener Middleware
# =============================================================================
@app.before_request
def start_query_tracker():
    """Step 2a: Initializes query counter and request timer."""
    g.query_count = 0
    g.start_time = time.time()


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, execmany):
    """Step 2b: Intercepts SQL engine execution and increments counter."""
    if hasattr(g, 'query_count'):
        g.query_count += 1


@app.after_request
def inject_performance_headers(response):
    """Step 2c: Injects performance headers into HTTP response."""
    if hasattr(g, 'start_time') and hasattr(g, 'query_count'):
        elapsed_ms = round((time.time() - g.start_time) * 1000, 2)
        response.headers['X-Query-Count'] = str(g.query_count)
        response.headers['X-Response-Time-MS'] = f"{elapsed_ms}ms"
    return response


# =============================================================================
# STEP 3: Database Seeding Routine
# =============================================================================
def seed_database():
    """Step 3: Populates in-memory database with 50 authors and 250 books."""
    with app.app_context():
        db.create_all()
        if Author.query.count() == 0:
            print("🌱 Seeding database with 50 Authors and 250 Books...")
            authors_list = []
            for i in range(1, 51):
                author = Author(name=f"Author #{i}")
                db.session.add(author)
                authors_list.append(author)
            db.session.commit()

            for author in authors_list:
                for j in range(1, 6):
                    book = Book(title=f"Book '{j}' by {author.name}", author_id=author.id)
                    db.session.add(book)
            db.session.commit()
            print("✅ Database seeding complete!")


seed_database()


# =============================================================================
# STEP 4: REST API Benchmark Endpoints (N+1 vs Eager vs Gzip)
# =============================================================================

# GET /api/v1/slow-authors -> UNOPTIMIZED N+1 Query Trap (51 SQL Queries!)
@app.route('/api/v1/slow-authors', methods=['GET'])
def get_slow_authors():
    """Step 4a: Unoptimized lazy loading route executing 51 database queries."""
    authors = Author.query.all()
    result = []
    for a in authors:
        book_titles = [b.title for b in a.books]  # Lazy loading triggers query per author!
        result.append({"author_id": a.id, "name": a.name, "books_count": len(book_titles)})

    return jsonify({
        "status": "success",
        "mode": "UNOPTIMIZED (Lazy Loading N+1 Trap)",
        "sql_queries_executed": g.query_count,
        "authors_count": len(result),
        "data": result
    }), 200


# GET /api/v1/fast-authors -> OPTIMIZED Eager Loading (1 SQL Query!)
@app.route('/api/v1/fast-authors', methods=['GET'])
def get_fast_authors():
    """Step 4b: Optimized eager loading route executing 1 single SQL JOIN query."""
    authors = Author.query.options(joinedload(Author.books)).all()
    result = []
    for a in authors:
        book_titles = [b.title for b in a.books]  # In-memory access, NO additional SQL!
        result.append({"author_id": a.id, "name": a.name, "books_count": len(book_titles)})

    return jsonify({
        "status": "success",
        "mode": "OPTIMIZED (joinedload Eager Loading)",
        "sql_queries_executed": g.query_count,
        "authors_count": len(result),
        "data": result
    }), 200


# GET /api/v1/large-payload -> Demonstrates Gzip Payload Compression
@app.route('/api/v1/large-payload', methods=['GET'])
def get_large_payload():
    """Step 4c: Returns 5,000 items compressed using Gzip."""
    large_dataset = [
        {"id": i, "sku": f"PROD-SKU-{i:05d}", "description": "High performance dataset payload compression test item"}
        for i in range(5000)
    ]
    return jsonify({
        "status": "success",
        "mode": "Gzip Compressed Response",
        "items_count": len(large_dataset),
        "items": large_dataset
    }), 200


# =============================================================================
# STEP 5: Interactive Web UI Dashboard Route Handler (render_template)
# =============================================================================
@app.route('/')
def home():
    """Step 5: Renders templates/index.html dashboard."""
    return render_template('index.html')


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 28 Performance Tuning Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🔴 Slow N+1 Route at: http://127.0.0.1:5000/api/v1/slow-authors")
    print("🟢 Fast Eager Route at: http://127.0.0.1:5000/api/v1/fast-authors")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
