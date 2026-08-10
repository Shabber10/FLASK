"""
===============================================================================
Day 28 Practice Script: Flask Performance Tuning & Database Optimization
===============================================================================
This script demonstrates:
1. SQLAlchemy Eager Loading (`joinedload()`) vs Lazy Loading N+1 Query Trap.
2. Intercepting and auditing SQL queries via SQLAlchemy engine event listeners.
3. Transparent HTTP response compression using `Flask-Compress`.
4. Performance timing headers (`X-Query-Count`, `X-Response-Time-MS`).
5. Interactive Web UI Performance Benchmark Dashboard.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Flask Application Profiler and Response Compression.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
from flask import Flask, jsonify, g, request, render_template_string
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
# 1. ORM Models (Author 1 <---> N Book)
# =============================================================================
class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy='select')


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)


# =============================================================================
# 2. SQL Query Counter & Event Listener Middleware
# =============================================================================
@app.before_request
def start_query_tracker():
    g.query_count = 0
    g.start_time = time.time()


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, execmany):
    if hasattr(g, 'query_count'):
        g.query_count += 1


@app.after_request
def inject_performance_headers(response):
    if hasattr(g, 'start_time') and hasattr(g, 'query_count'):
        elapsed_ms = round((time.time() - g.start_time) * 1000, 2)
        response.headers['X-Query-Count'] = str(g.query_count)
        response.headers['X-Response-Time-MS'] = f"{elapsed_ms}ms"
    return response


# =============================================================================
# 3. Database Seeding Routine
# =============================================================================
def seed_database():
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
# 4. REST API Benchmark Endpoints
# =============================================================================

# GET /api/v1/slow-authors -> UNOPTIMIZED N+1 Query Trap (51 SQL Queries!)
@app.route('/api/v1/slow-authors', methods=['GET'])
def get_slow_authors():
    # ❌ Triggers 1 Query for Authors + 50 Individual Queries for Books = 51 Queries!
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
    # ✅ Triggers 1 Single SQL LEFT OUTER JOIN Query!
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
# 5. Interactive Web UI Performance Benchmark Dashboard
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 28 Performance Tuning Masterclass</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 850px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #27ae60; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
                .btn { display: inline-block; background: #27ae60; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-right: 10px; border: none; cursor: pointer; }
                .btn-danger { background: #c0392b; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
                .metric { font-size: 24px; font-weight: bold; color: #e74c3c; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>⚡ Performance Tuning & Database Optimization (Day 28)</h2>
                <p>Optimization Suite: <span class="badge">Eager Loading & Flask-Compress Active</span></p>

                <p>Compare N+1 Lazy Loading vs joinedload Eager Loading performance across 50 authors and 250 books:</p>

                <p>
                    <button class="btn btn-danger" onclick="runBenchmark('/api/v1/slow-authors')">🔴 Run Unoptimized N+1 Query Route (51 Queries)</button>
                    <button class="btn" onclick="runBenchmark('/api/v1/fast-authors')">🟢 Run Eager Loaded Route (1 Query)</button>
                    <button class="btn" style="background:#8e44ad;" onclick="runBenchmark('/api/v1/large-payload')">📦 Test Gzip Payload (5,000 Items)</button>
                </p>

                <h3>Live Performance Telemetry:</h3>
                <div id="output" style="background: #1e1e1e; color: #00ff00; padding: 15px; border-radius: 5px; font-family: monospace; min-height: 120px;">
                    Click a benchmark button above to test database query latency...
                </div>

                <script>
                    function runBenchmark(url) {
                        const out = document.getElementById('output');
                        out.innerHTML = "Fetching '" + url + "'... Please wait...";

                        fetch(url)
                        .then(res => {
                            const queryCount = res.headers.get('X-Query-Count');
                            const timeMs = res.headers.get('X-Response-Time-MS');
                            const encoding = res.headers.get('Content-Encoding') || 'identity';

                            return res.json().then(data => ({ data, queryCount, timeMs, encoding }));
                        })
                        .then(item => {
                            out.innerHTML = "STATUS 200 OK!<br>" +
                                "Mode: <strong>" + item.data.mode + "</strong><br>" +
                                "SQL Queries Executed: <span class='metric'>" + item.queryCount + "</span><br>" +
                                "Response Latency Header: <span class='metric'>" + item.timeMs + "</span><br>" +
                                "Content-Encoding: <strong>" + item.encoding + "</strong>";
                        });
                    }
                </script>
            </div>
        </body>
        </html>
    """)


# =============================================================================
# 6. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 28 Performance Tuning Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🔴 Slow N+1 Route at: http://127.0.0.1:5000/api/v1/slow-authors")
    print("🟢 Fast Eager Route at: http://127.0.0.1:5000/api/v1/fast-authors")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
