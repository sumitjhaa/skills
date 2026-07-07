"""Flask vs Django comparison — runnable Flask app."""
from flask import Flask, request, jsonify

app = Flask(__name__)

items: list[dict] = []
counter = 0


@app.route("/")
def home():
    return jsonify({"service": "Flask API", "version": "1.0", "items_count": len(items)})


@app.route("/items", methods=["GET"])
def list_items():
    return jsonify(items)


@app.route("/items", methods=["POST"])
def create_item():
    global counter
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "name and price required"}), 400
    counter += 1
    item = {"id": counter, "name": data["name"], "price": data["price"]}
    items.append(item)
    return jsonify(item), 201


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id: int):
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(item)


if __name__ == "__main__":
    print("=== Flask API ===")
    for rule in app.url_map.iter_rules():
        if rule.endpoint != "static":
            methods = ",".join(rule.methods - {"HEAD", "OPTIONS"})
            print(f"  {methods} {rule.rule}")
    print("\nRun with: flask run  (or: python 10-17-flask-django.py)")
    print("Then: curl http://localhost:5000/")
    app.run(debug=True, port=5000)
