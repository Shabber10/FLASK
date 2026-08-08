# Day 07 Practice App: Advanced Filtering & Pagination
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/search')
def search():
    cat = request.args.get('category')
    max_price = request.args.get('max_price', type=float)
    page = request.args.get('page', 1, type=int)
    
    stmt = db.select(Product)
    if cat:
        stmt = stmt.filter(Product.category == cat)
    if max_price:
        stmt = stmt.filter(Product.price <= max_price)
        
    pagination = db.paginate(stmt, page=page, per_page=5, error_out=False)
    
    return jsonify({
        "products": [{"id": p.id, "name": p.name, "price": p.price} for p in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    })

if __name__ == '__main__':
    app.run(debug=True)
