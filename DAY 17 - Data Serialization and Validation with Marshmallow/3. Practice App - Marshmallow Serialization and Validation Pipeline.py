"""
===============================================================================
Day 17 Practice Script: Marshmallow Serialization & Validation Pipeline
===============================================================================
This script demonstrates:
1. Defining Marshmallow Schemas (`AuthorSchema`, `BookSchema`).
2. Serializing SQLAlchemy models to JSON using `schema.dump()`.
3. Deserializing and validating incoming JSON request payloads using `schema.load()`.
4. Custom validation rules (`@validates('price')`, `@validates('isbn')`).
5. Nested relationship serialization (`fields.Nested(BookSchema, many=True)`).
6. Capturing `ValidationError` exceptions and returning HTTP 422 JSON error responses.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Marshmallow Serialization and Validation Pipeline.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import datetime
from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate, validates, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day17-marshmallow-masterclass-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///day17_books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)


# =============================================================================
# 1. SQLAlchemy ORM Models
# =============================================================================
class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    books = db.relationship('Book', backref='author', lazy=True, cascade='all, delete-orphan')


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    published_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)


# =============================================================================
# 2. Marshmallow Schemas for Validation & Serialization
# =============================================================================
class BookSchema(Schema):
    """Schema for validating and serializing Book records."""
    id = fields.Int(dump_only=True)                                     # Output response only
    title = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    isbn = fields.Str(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=0.99, max=999.99))
    published_year = fields.Int(required=True, validate=validate.Range(min=1900, max=2026))
    author_id = fields.Int(required=True)

    @validates('isbn')
    def validate_isbn_format(self, value):
        """Custom validation method checking ISBN length."""
        cleaned_isbn = value.replace('-', '')
        if len(cleaned_isbn) not in [10, 13]:
            raise ValidationError("ISBN must be a valid 10 or 13-digit number format.")


class AuthorSchema(Schema):
    """Schema for serializing Author records with nested books."""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    
    # One-to-Many Nested Relationship Serialization
    books = fields.Nested(BookSchema, many=True, dump_only=True)


book_schema = BookSchema()
books_schema = BookSchema(many=True)
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


# Seed initial database records if empty
with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(Author)).scalars().first():
        a1 = Author(name="Shabber Hussain", email="shabber@flaskmastery.dev")
        b1 = Book(title="Flask Architecture & Engineering", isbn="978-1-23456-789-0", price=39.99, published_year=2025, author=a1)
        b2 = Book(title="Mastering Microservices with Flask", isbn="978-0-98765-432-1", price=45.50, published_year=2026, author=a1)
        db.session.add_all([a1, b1, b2])
        db.session.commit()


# =============================================================================
# 3. REST API Endpoints Utilizing Marshmallow Schemas
# =============================================================================

# GET /api/v1/authors - Serializes list of authors with nested books
@app.route('/api/v1/authors', methods=['GET'])
def get_authors():
    authors = db.session.execute(db.select(Author)).scalars().all()
    # Dump SQLAlchemy list into JSON dict using Marshmallow
    return jsonify({
        "status": "success",
        "data": authors_schema.dump(authors)
    }), 200


# GET /api/v1/books - Serializes list of books
@app.route('/api/v1/books', methods=['GET'])
def get_books():
    books = db.session.execute(db.select(Book)).scalars().all()
    return jsonify({
        "status": "success",
        "data": books_schema.dump(books)
    }), 200


# POST /api/v1/books - Deserializes and Validates incoming JSON
@app.route('/api/v1/books', methods=['POST'])
def create_book():
    json_payload = request.get_json() or {}

    try:
        # Load and Validate incoming JSON using Marshmallow Schema!
        validated_data = book_schema.load(json_payload)
    except ValidationError as err:
        # Catch validation error and return HTTP 422 Unprocessable Entity
        return jsonify({
            "error": {
                "code": 422,
                "type": "UNPROCESSABLE_ENTITY",
                "message": "Marshmallow validation failed.",
                "details": err.messages
            }
        }), 422

    # Check if author exists
    author = db.session.get(Author, validated_data['author_id'])
    if not author:
        return jsonify({
            "error": {"code": 404, "message": f"Author with ID {validated_data['author_id']} not found."}
        }), 404

    # Create Book ORM instance from validated data
    new_book = Book(
        title=validated_data['title'],
        isbn=validated_data['isbn'],
        price=validated_data['price'],
        published_year=validated_data['published_year'],
        author_id=validated_data['author_id']
    )
    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Book created successfully",
        "data": book_schema.dump(new_book)
    }), 201


# =============================================================================
# 4. Interactive Web UI Dashboard
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 17 Marshmallow Pipeline</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #8e44ad; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🍡 Marshmallow Serialization & Validation Pipeline (Day 17)</h2>
                <p>Data Validation Engine Active: <span class="badge">Marshmallow 3.x</span></p>

                <h3>API Endpoints:</h3>
                <ul>
                    <li><code>GET /api/v1/authors</code> -> Serializes authors with nested books</li>
                    <li><code>GET /api/v1/books</code> -> Serializes all books list</li>
                    <li><code>POST /api/v1/books</code> -> Validates incoming JSON and handles 422 errors</li>
                </ul>

                <p style="margin-top: 25px;">
                    <a href="/api/v1/authors">Inspect GET /api/v1/authors JSON</a> | 
                    <a href="/api/v1/books">Inspect GET /api/v1/books JSON</a>
                </p>
            </div>
        </body>
        </html>
    """)


# =============================================================================
# 5. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 17 Marshmallow Pipeline Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("📡 Authors API at: http://127.0.0.1:5000/api/v1/authors")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
