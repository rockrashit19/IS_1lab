from flask import Blueprint, request, jsonify
from .database import db
from .models import User
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token
from markupsafe import escape

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    email = (data.get("email") or "").strip() or None

    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400

    existing = User.query.filter_by(username=username).first()
    if existing:
        return jsonify({"msg": "user exists"}), 409

    password_hash = bcrypt.hash(password)
    user = User(username=username, password_hash=password_hash, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "user created", "user": {"username": escape(username), "email": escape(email) if email else None}}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.verify(password, user.password_hash):
        return jsonify({"msg": "bad credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token, "user": {"username": escape(user.username), "email": escape(user.email) if user.email else None}}), 200
