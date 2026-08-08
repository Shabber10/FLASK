# Day 08 Practice App: Posts, Comments & Tags Relationship
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan', lazy='selectin')
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

with app.app_context():
    db.create_all()

@app.route('/demo')
def demo():
    p = Post(title="Day 08 Masterclass")
    c1 = Comment(body="Great lesson!", post=p)
    t1 = Tag(name="Flask")
    p.tags.append(t1)
    db.session.add(p)
    db.session.commit()
    return jsonify({"post": p.title, "comments_count": len(p.comments), "tags": [t.name for t in p.tags]})

if __name__ == '__main__':
    app.run(debug=True)
