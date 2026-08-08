# Day 17 Practice App: Marshmallow Schema Pipeline
from flask import Flask, jsonify, request
from marshmallow import Schema, fields, validate, ValidationError

app = Flask(__name__)

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=2))
    author = fields.Str(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=0.99))

book_schema = BookSchema()
books_schema = BookSchema(many=True)

books_db = [{"id": 1, "title": "Flask Deep Dive", "author": "Shabber", "price": 29.99}]

@app.route('/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'GET':
        return jsonify(books_schema.dump(books_db))
        
    try:
        data = book_schema.load(request.json or {})
        data['id'] = len(books_db) + 1
        books_db.append(data)
        return jsonify(book_schema.dump(data)), 201
    except ValidationError as err:
        return jsonify({"validation_errors": err.messages}), 400

if __name__ == '__main__':
    app.run(debug=True)
