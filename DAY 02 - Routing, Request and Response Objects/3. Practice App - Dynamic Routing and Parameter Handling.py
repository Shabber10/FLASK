# Day 02 Practice App: Dynamic Routing & Request Inspection
from flask import Flask, request, jsonify, make_response
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super().__init__(url_map)
        self.regex = items[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

@app.route('/product/<regex(r"[a-z]{3}-\d{4}"):code>')
def get_product(code):
    return jsonify({"product_code": code, "category": "electronics"})

@app.route('/api/search', methods=['GET', 'POST'])
def search_handler():
    if request.method == 'GET':
        query = request.args.get('q', 'default')
        page = request.args.get('page', 1, type=int)
        return jsonify({"method": "GET", "query": query, "page": page})
    else:
        payload = request.get_json(silent=True) or request.form.to_dict()
        resp = make_response(jsonify({"method": "POST", "data": payload}), 201)
        resp.headers['X-API-Status'] = 'Processed'
        return resp

if __name__ == '__main__':
    app.run(debug=True)
