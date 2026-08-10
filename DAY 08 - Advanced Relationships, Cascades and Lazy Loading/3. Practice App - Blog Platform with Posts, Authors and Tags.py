"""
===============================================================================
Day 08 Practice Script: Multi-Model Blog Platform with Complex Relationships
===============================================================================
This script demonstrates:
1. One-to-Many relationships with cascade delete orphans (Posts -> Comments).
2. Many-to-Many relationships via secondary association table (Posts <-> Tags).
3. Eager loading using `selectinload()` to eliminate N+1 query problems.
4. Dynamic relationship querying with `lazy='dynamic'`.
5. Web UI & REST API for Authors, Posts, Comments, and Tags.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Blog Platform with Posts, Authors and Tags.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import datetime
from flask import Flask, jsonify, request, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import selectinload, joinedload

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day08-relationships-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# =============================================================================
# 1. Association Table for Many-to-Many (Posts <-> Tags)
# =============================================================================
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)


# =============================================================================
# 2. ORM Models
# =============================================================================
class User(db.Model):
    """ORM Model representing Blog Authors."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # One-to-Many: User -> Posts
    posts = db.relationship('Post', backref='author', lazy='selectin')


class Tag(db.Model):
    """ORM Model representing Article Tags."""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)


class Post(db.Model):
    """ORM Model representing Blog Posts."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # One-to-Many: Post -> Comments (With Cascade Delete-Orphan!)
    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan', lazy='selectin')
    
    # Many-to-Many: Post <-> Tags via post_tags junction table
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'), lazy='selectin')

    def to_dict(self):
        """Serializes model instance to JSON dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author.username if self.author else None,
            "comments_count": len(self.comments),
            "tags": [t.name for t in self.tags],
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class Comment(db.Model):
    """ORM Model representing Article Comments."""
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(50), nullable=False, default="Anonymous")
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)


# Initialize Tables & Pre-seed Initial Sample Data
with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(User)).scalars().first():
        print("🌱 Pre-seeding Blog platform data into SQLite database...")
        u1 = User(username="tech_writer", email="writer@blog.com")
        t1 = Tag(name="Flask")
        t2 = Tag(name="Python")
        t3 = Tag(name="SQLAlchemy")
        
        p1 = Post(title="Mastering Relational Mappings in Flask", content="Deep dive into ORM relationships, cascades, and eager loading...", author=u1)
        p1.tags.extend([t1, t2, t3])
        
        c1 = Comment(body="Outstanding article on cascades!", author_name="DevAlice", post=p1)
        c2 = Comment(body="Helped me fix my N+1 query issue.", author_name="DevBob", post=p1)
        
        db.session.add_all([u1, t1, t2, t3, p1, c1, c2])
        db.session.commit()
        print("✅ Sample blog data seeded successfully!")


# =============================================================================
# 3. HTML UI Template String
# =============================================================================
BLOG_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 08 Blog Platform</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 30px; color: #333; }
        .card { max-width: 800px; margin: 0 auto 20px auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
        h2 { color: #2c3e50; margin-top: 0; }
        .tag { background: #8e44ad; color: white; padding: 4px 10px; border-radius: 4px; font-size: 0.85em; font-weight: bold; margin-right: 5px; }
        .comment-box { background: #f8f9fa; padding: 12px; border-left: 4px solid #3498db; margin-top: 10px; font-size: 0.9em; border-radius: 4px; }
        .meta { color: #7f8c8d; font-size: 0.85em; }
        .btn-danger { background: #e74c3c; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 0.85em; font-weight: bold; }
        .btn-danger:hover { background: #c0392b; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📝 Blog Engine - Relationship & Cascade Demo (Day 08)</h2>
        <p>Demonstrating One-to-Many, Many-to-Many, and Cascade Delete-Orphan behavior.</p>
    </div>

    {% for p in posts %}
    <div class="card">
        <h3>{{ p.title }}</h3>
        <p class="meta">By <strong>{{ p.author.username }}</strong> on {{ p.created_at.strftime("%b %d, %Y") }}</p>

        <p>{{ p.content }}</p>

        <div style="margin-bottom: 15px;">
            <strong>Tags:</strong>
            {% for t in p.tags %}
                <span class="tag">{{ t.name }}</span>
            {% endfor %}
        </div>

        <h4>Comments ({{ p.comments|length }}) <a class="btn-danger" href="/posts/delete/{{ p.id }}">Delete Post (Triggers Cascade)</a></h4>
        {% for c in p.comments %}
            <div class="comment-box">
                <strong>{{ c.author_name }}:</strong> {{ c.body }}
            </div>
        {% else %}
            <p class="meta">No comments yet.</p>
        {% endfor %}
    </div>
    {% endfor %}
</body>
</html>
"""


# =============================================================================
# 4. Route Handlers
# =============================================================================
@app.route('/')
def index():
    """Eager loads comments and tags using selectinload to prevent N+1 query problems."""
    stmt = db.select(Post).options(selectinload(Post.comments), selectinload(Post.tags)).order_by(Post.id.desc())
    posts = db.session.execute(stmt).scalars().all()
    return render_template_string(BLOG_HTML, posts=posts)


@app.route('/posts/delete/<int:post_id>')
def delete_post(post_id):
    """Deletes Post, automatically triggering cascade delete for associated Comments."""
    post = db.session.get(Post, post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/api/posts')
def api_posts():
    """API Endpoint returning posts and nested relationships as JSON."""
    stmt = db.select(Post).options(selectinload(Post.comments), selectinload(Post.tags))
    posts = db.session.execute(stmt).scalars().all()
    return jsonify([p.to_dict() for p in posts]), 200


# =============================================================================
# 5. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 08 Blog Platform Application...")
    print("🌐 Open Blog UI at: http://127.0.0.1:5000/")
    print("📡 Test REST API at: http://127.0.0.1:5000/api/posts")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
