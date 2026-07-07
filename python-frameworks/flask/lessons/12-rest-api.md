# 🌐 REST API with Flask-RESTful
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Build RESTful APIs with resources, request parsing, marshalling.

## Install

```bash
pip install flask-restful
```

## Basic Setup

```python
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
```

## Resources

Resources are classes with methods for each HTTP verb.

```python
class ItemResource(Resource):
    def get(self, item_id):
        item = store.get(item_id)
        if not item:
            return {"error": "Not found"}, 404
        return {"item": item}

    def put(self, item_id):
        data = request.get_json()
        item = store.update(item_id, data)
        if not item:
            return {"error": "Not found"}, 404
        return {"item": item}

    def delete(self, item_id):
        if not store.delete(item_id):
            return {"error": "Not found"}, 404
        return {"message": "Deleted"}
```

## Adding Resources

```python
api.add_resource(ItemListResource, "/api/items")
api.add_resource(ItemResource, "/api/items/<int:item_id>")
api.add_resource(StatsResource, "/api/stats")
```

## Request Parsing

```python
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True, help="Name is required")
parser.add_argument("price", type=float, default=0.0)
parser.add_argument("category", type=str, default="general")

class ItemListResource(Resource):
    def post(self):
        args = parser.parse_args()
        item = store.create(args)
        return {"item": item, "message": "Created"}, 201
```

## Response Marshalling

```python
from flask_restful import fields, marshal_with

item_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "price": fields.Float,
    "category": fields.String,
}

class ItemResource(Resource):
    @marshal_with(item_fields)
    def get(self, item_id):
        item = store.get(item_id)
        if not item:
            abort(404)
        return item
```

<!-- 🤔 Return status codes as the second value in a tuple: `return data, 201`. -->

## Run the Code

```bash
python code/12-rest-api.py
```
