from flask import Blueprint, jsonify, request
from db import mongo
from bson.objectid import ObjectId

user_bp = Blueprint("user", __name__)

# Helper function to clean ObjectId (Convert ObjectId to string in a MongoDB document.)
def clean_document(doc):
    if isinstance(doc, dict):
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return doc


# GET All Users
@user_bp.route("/", methods=["GET"])
def get_users():
    users = mongo.db.users.find()
    users = list(users)
    data = [clean_document(user) for user in users]
    return jsonify(data), 200


# GET User by ID
@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
    return jsonify(user) if user else ("User not found", 404)


# POST Create a User
@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    result = mongo.db.users.insert_one(data)
    return jsonify({"message": "User created", "id": str(result.inserted_id)}), 201


# PUT Update User (Full Update)
@user_bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    success = mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    return jsonify({"message": "User updated"}) if success else ("Update failed", 400)


# DELETE User
@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"message": "User deleted"}) if success else ("Delete failed", 400)
