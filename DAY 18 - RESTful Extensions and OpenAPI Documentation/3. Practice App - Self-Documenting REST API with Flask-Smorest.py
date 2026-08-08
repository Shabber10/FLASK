# Day 18 Practice App: Flask-RESTful Resource Dispatching
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

todos = {1: "Master Flask Routing", 2: "Master Marshmallow Schemas"}

class TodoResource(Resource):
    def get(self, todo_id):
        if todo_id not in todos:
            return {"error": "Todo item not found"}, 404
        return {"id": todo_id, "task": todos[todo_id]}
        
    def delete(self, todo_id):
        if todo_id in todos:
            del todos[todo_id]
            return "", 204
        return {"error": "Not found"}, 404

api.add_resource(TodoResource, '/todos/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
