"""
===============================================================================
Day 17 Practice Script: Marshmallow Serialization & Validation Pipeline
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Defining SQLAlchemy ORM models (`Author`, `Book`).
2. STEP 2: Defining Marshmallow Schemas (`BookSchema`, `AuthorSchema`) with `fields.Nested` and `@validates('isbn')`.
3. STEP 3: Seeding initial database records.
4. STEP 4: Serializing SQLAlchemy models to JSON using `schema.dump()` (`GET /api/v1/authors`, `GET /api/v1/books`).
5. STEP 5: Deserializing and validating incoming JSON request payloads using `schema.load()` and handling `ValidationError` (422).
6. STEP 6: Interactive Web UI pipeline tester dashboard rendering `templates/index.html`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Marshmallow Serialization and Validation Pipeline.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import datetime
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate, validates, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day17-marshmallow-masterclass-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///day17_books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)


# =============================================================================
# STEP 1: SQLAlchemy ORM Models
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
# STEP 2: Marshmallow Schemas for Validation & Serialization
# =============================================================================
class BookSchema(Schema):
    """Step 2a: Schema for validating and serializing Book records."""
    id = fields.Int(dump_only=True)                                     # Output response only
    title = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    isbn = fields.Str(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=0.99, max=999.99))
    published_year = fields.Int(required=True, validate=validate.Range(min=1900, max=2026))
    author_id = fields.Int(required=True)

    @validates('isbn')
    def validate_isbn_format(self, value):
        """Step 2b: Custom validation method checking ISBN length."""
        cleaned_isbn = value.replace('-', '')
        if len(cleaned_isbn) not in [10, 13]:
            raise ValidationError("ISBN must be a valid 10 or 13-digit number format.")


class AuthorSchema(Schema):
    """Step 2c: Schema for serializing Author records with nested books."""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    
    # One-to-Many Nested Relationship Serialization
    books = fields.Nested(BookSchema, many=True, dump_only=True)


book_schema = BookSchema()
books_schema = BookSchema(many=True)
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


# =============================================================================
# STEP 3: Initial Database Seeding
# =============================================================================
with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(Author)).scalars().first():
        a1 = Author(name="Shabber Hussain", email="shabber@flaskmastery.dev")
        b1 = Book(title="Flask Architecture & Engineering", isbn="978-1-23456-789-0", price=39.99, published_year=2025, author=a1)
        b2 = Book(title="Mastering Microservices with Flask", isbn="978-0-98765-432-1", price=45.50, published_year=2026, author=a1)
        db.session.add_all([a1, b1, b2])
        db.session.commit()


# =============================================================================
# STEP 4: GET REST API Endpoints Utilizing schema.dump()
# =============================================================================

# GET /api/v1/authors - Serializes list of authors with nested books
@app.route('/api/v1/authors', methods=['GET'])
def get_authors():
    """Step 4a: Dumps SQLAlchemy list into JSON dict using Marshmallow."""
    authors = db.session.execute(db.select(Author)).scalars().all()
    return jsonify({
        "status": "success",
        "data": authors_schema.dump(authors)
    }), 200


# GET /api/v1/books - Serializes list of books
@app.route('/api/v1/books', methods=['GET'])
def get_books():
    """Step 4b: Dumps all books list."""
    books = db.session.execute(db.select(Book)).scalars().all()
    return jsonify({
        "status": "success",
        "data": books_schema.dump(books)
    }), 200


# =============================================================================
# STEP 5: POST Endpoint Utilizing schema.load() & Handling ValidationError
# =============================================================================
@app.route('/api/v1/books', methods=['POST'])
def create_book():
    """Step 5: Loads and Validates incoming JSON using Marshmallow Schema."""
    json_payload = request.get_json() or {}

    try:
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
# STEP 6: Interactive Web UI Dashboard Route Handler (render_template)
# =============================================================================
@app.route('/')
def home():
    """Step 6: Renders templates/index.html dashboard."""
    return render_template('index.html')


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 17 Marshmallow Pipeline Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("📡 Authors API at: http://127.0.0.1:5000/api/v1/authors")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
