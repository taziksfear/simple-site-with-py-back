from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

JSON_FILE = 'users.json'

def load_users():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(JSON_FILE, 'w') as file:
        json.dump(users, file, indent=4)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = load_users()
    return jsonify(users)

@app.route('/api/users/<int:user_id>/objects', methods=['POST'])
def update_objects(user_id):
    data = request.json
    action = data.get("action")
    object_name = data.get("name")
    count = data.get("count")

    users = load_users()
    user = next((user for user in users if user["userId"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    obj = next((obj for obj in user["objects"] if obj["name"] == object_name), None)
    if not obj:
        return jsonify({"error": "Object not found"}), 404

    if action == "buy":
        obj["count"] += count
    elif action == "sell":
        if obj["count"] < count:
            return jsonify({"error": "Not enough objects to sell"}), 400
        obj["count"] -= count
    else:
        return jsonify({"error": "Invalid action"}), 400

    save_users(users)

    return jsonify({"message": "Object count updated", "user": user})

if __name__ == '__main__':
    app.run(debug=True)
