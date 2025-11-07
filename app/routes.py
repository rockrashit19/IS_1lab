from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User
from markupsafe import escape

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/data", methods=["GET"])
@jwt_required()
def get_data():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    sample = [
        {"id": 1, "title": "Public post 1", "content": escape("Hello <script>alert(1)</script> from user data")},
        {"id": 2, "title": "Public post 2", "content": escape("This content is safe to render in client")}
    ]
    return jsonify({
        "user": {"id": user.id, "username": escape(user.username)},
        "data": sample
    })
