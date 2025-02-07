from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = { 'message': "Login successful!" }
    return jsonify(data), 200

@auth_bp.route("/register", methods=["POST"])
def register():
    data = { 'message': "Registration successful!" }
    return jsonify(data), 200