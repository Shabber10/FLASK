# Day 10 Practice App: Dual Database Binds & Raw SQL
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_primary.db'
app.config['SQLALCHEMY_BINDS'] = {
    'audit': 'sqlite:///app_audit.db'
}

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)

class AuditLog(db.Model):
    __bind_key__ = 'audit'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/raw-query')
def raw_query():
    result = db.session.execute(text("SELECT 1 AS alive")).fetchone()
    return jsonify({"raw_result": result.alive})

if __name__ == '__main__':
    app.run(debug=True)
