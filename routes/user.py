from flask import Blueprint, jsonify, request
from flasgger import swag_from

user_bp = Blueprint("user", __name__)

users = [
    {"id": 1, "name": "Arjun Khetia", "email": "arjunkhetia@gmail.com"},
    {"id": 2, "name": "Pranshu Khetia", "email": "pranshukhetia@gmail.com"},
]


# GET All Users
@user_bp.route("/", methods=["GET"])
@swag_from({
    "tags": ["User"],
    "summary": "Get all users",
    "responses": {
        "200": {"description": "A list of users"}
    }
})
# @jwt_required()
def get_users():
    return jsonify(users), 200


# GET User by ID
@user_bp.route("/<int:user_id>", methods=["GET"])
@swag_from({
    "tags": ["User"],
    "summary": "Get a user by ID",
    "parameters": [
        {"name": "user_id", "in": "path", "type": "integer", "required": True}
    ],
    "responses": {
        "200": {"description": "User found"},
        "404": {"description": "User not found"}
    }
})
# @jwt_required()
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    return (jsonify(user), 200) if user else (jsonify({"message": "User not found"}), 404)


# POST Create a User
@user_bp.route("/", methods=["POST"])
@swag_from({
    "tags": ["User"],
    "summary": "Create a new user",
    "parameters": [
        {"name": "body", "in": "body", "required": True, "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"}
            }
        }}
    ],
    "responses": {
        "201": {"description": "User created"},
        "400": {"description": "Invalid input"}
    }
})
# @jwt_required()
def create_user():
    data = request.get_json()
    if "name" not in data or "email" not in data:
        return jsonify({"message": "Invalid input"}), 400

    new_user = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
    users.append(new_user)
    return jsonify(new_user), 201


# PUT Update User (Full Update)
@user_bp.route("/<int:user_id>", methods=["PUT"])
@swag_from({
    "tags": ["User"],
    "summary": "Update a user completely",
    "parameters": [
        {"name": "user_id", "in": "path", "type": "integer", "required": True},
        {"name": "body", "in": "body", "required": True, "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"}
            }
        }}
    ],
    "responses": {
        "200": {"description": "User updated"},
        "404": {"description": "User not found"}
    }
})
# @jwt_required()
def update_user(user_id):
    data = request.get_json()
    user = next((u for u in users if u["id"] == user_id), None)
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    user["name"] = data["name"]
    user["email"] = data["email"]
    return jsonify(user), 200


# PATCH Update User (Partial Update)
@user_bp.route("/<int:user_id>", methods=["PATCH"])
@swag_from({
    "tags": ["User"],
    "summary": "Partially update a user",
    "parameters": [
        {"name": "user_id", "in": "path", "type": "integer", "required": True},
        {"name": "body", "in": "body", "required": True, "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"}
            }
        }}
    ],
    "responses": {
        "200": {"description": "User updated"},
        "404": {"description": "User not found"}
    }
})
# @jwt_required()
def patch_user(user_id):
    data = request.get_json()
    user = next((u for u in users if u["id"] == user_id), None)
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        user["email"] = data["email"]

    return jsonify(user), 200


# DELETE User
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@swag_from({
    "tags": ["User"],
    "summary": "Delete a user",
    "parameters": [
        {"name": "user_id", "in": "path", "type": "integer", "required": True}
    ],
    "responses": {
        "200": {"description": "User deleted"},
        "404": {"description": "User not found"}
    }
})
# @jwt_required()
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "User deleted"}), 200
