"""
Day 13 Practice Application: RESTful Articles & Authors API Engine
==================================================================
This application demonstrates:
1. Building class-based REST resources with Flask-RESTful (Resource).
2. Data serialization & deserialization using Marshmallow schemas.
3. Enforcing schema payload validation with Marshmallow validators.
4. Implementing standard HTTP REST verbs (GET, POST, PUT, PATCH, DELETE).
5. Returning explicit HTTP status codes (200, 201, 204, 400, 404, 422).
"""

from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day13-restful-api-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rest_articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)


# ------------------------------------------------------------------------------
# 1. ORM Models
# ------------------------------------------------------------------------------
class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    articles = db.relationship('Article', backref='author', lazy=True, cascade='all, delete-orphan')


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='published')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)


# Initialize Database & Seed Sample Records
with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(Author)).scalars().first():
        a1 = Author(name="Jane Doe", email="jane@techblog.com")
        p1 = Article(title="Building Scalable REST APIs with Flask-RESTful", content="RESTful design patterns...", author=a1)
        p2 = Article(title="Marshmallow Data Validation Masterclass", content="Data schemas...", author=a1)
        db.session.add_all([a1, p1, p2])
        db.session.commit()


# ------------------------------------------------------------------------------
# 2. Marshmallow Schemas
# ------------------------------------------------------------------------------
class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)

class ArticleSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=5, max=200))
    content = fields.Str(required=True)
    status = fields.Str(validate=validate.OneOf(['draft', 'published', 'archived']))
    created_at = fields.DateTime(dump_only=True)
    author_id = fields.Int(required=True)
    author = fields.Nested(AuthorSchema, dump_only=True)

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


# ------------------------------------------------------------------------------
# 3. Flask-RESTful Resources
# ------------------------------------------------------------------------------
class AuthorListResource(Resource):
    def get(self):
        authors = db.session.execute(db.select(Author)).scalars().all()
        return authors_schema.dump(authors), 200

    def post(self):
        payload = request.get_json(silent=True) or {}
        try:
            data = author_schema.load(payload)
        except ValidationError as err:
            return {"error": "Validation Error", "messages": err.messages}, 422

        author = Author(**data)
        db.session.add(author)
        db.session.commit()
        return author_schema.dump(author), 201


class ArticleListResource(Resource):
    def get(self):
        articles = db.session.execute(db.select(Article)).scalars().all()
        return articles_schema.dump(articles), 200

    def post(self):
        payload = request.get_json(silent=True) or {}
        try:
            data = article_schema.load(payload)
        except ValidationError as err:
            return {"error": "Validation Error", "messages": err.messages}, 422

        if not db.session.get(Author, data['author_id']):
            return {"error": "Bad Request", "message": f"Author ID {data['author_id']} not found."}, 400

        article = Article(**data)
        db.session.add(article)
        db.session.commit()
        return article_schema.dump(article), 201


class ArticleDetailResource(Resource):
    def get(self, article_id):
        article = db.session.get(Article, article_id)
        if not article:
            return {"error": "Not Found", "message": f"Article ID {article_id} does not exist."}, 404
        return article_schema.dump(article), 200

    def put(self, article_id):
        article = db.session.get(Article, article_id)
        if not article:
            return {"error": "Not Found", "message": f"Article ID {article_id} does not exist."}, 404

        payload = request.get_json(silent=True) or {}
        try:
            data = article_schema.load(payload)
        except ValidationError as err:
            return {"error": "Validation Error", "messages": err.messages}, 422

        article.title = data['title']
        article.content = data['content']
        article.status = data.get('status', 'published')
        article.author_id = data['author_id']
        db.session.commit()
        return article_schema.dump(article), 200

    def delete(self, article_id):
        article = db.session.get(Article, article_id)
        if not article:
            return {"error": "Not Found", "message": f"Article ID {article_id} does not exist."}, 404

        db.session.delete(article)
        db.session.commit()
        return '', 204


# Register Resources on Api
api.add_resource(AuthorListResource, '/api/authors')
api.add_resource(ArticleListResource, '/api/articles')
api.add_resource(ArticleDetailResource, '/api/articles/<int:article_id>')


# ------------------------------------------------------------------------------
# 4. Interactive Web Tester UI
# ------------------------------------------------------------------------------
TESTER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 13 REST API Tester</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
        .card { max-width: 850px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .endpoint { background: #2d3748; color: #63b3ed; padding: 12px; border-radius: 6px; font-family: monospace; margin-bottom: 10px; }
        .badge { padding: 4px 8px; border-radius: 4px; color: white; font-weight: bold; font-size: 0.85em; }
        .get { background: #27ae60; }
        .post { background: #e67e22; }
        .put { background: #2980b9; }
        .delete { background: #c0392b; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 RESTful API & Marshmallow Engine (Day 13)</h2>
        <p>Active REST API Resource Endpoints:</p>

        <div class="endpoint"><span class="badge get">GET</span> <a href="/api/authors" style="color:#63b3ed;">/api/authors</a> - List Authors</div>
        <div class="endpoint"><span class="badge post">POST</span> /api/authors - Create Author (JSON)</div>
        <div class="endpoint"><span class="badge get">GET</span> <a href="/api/articles" style="color:#63b3ed;">/api/articles</a> - List Articles with Nested Authors</div>
        <div class="endpoint"><span class="badge post">POST</span> /api/articles - Create Article (Validated via Marshmallow)</div>
        <div class="endpoint"><span class="badge get">GET</span> <a href="/api/articles/1" style="color:#63b3ed;">/api/articles/1</a> - Get Article #1 Detail</div>
        <div class="endpoint"><span class="badge put">PUT</span> /api/articles/1 - Replace Article #1 Payload</div>
        <div class="endpoint"><span class="badge delete">DELETE</span> /api/articles/1 - Remove Article #1 (204 No Content)</div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(TESTER_HTML)


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 13 RESTful API Application...")
    print("Web Dashboard at http://127.0.0.1:5000/")
    print("API Authors at http://127.0.0.1:5000/api/authors")
    print("API Articles at http://127.0.0.1:5000/api/articles")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
