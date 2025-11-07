# # backend/app/utils/auth_middleware.py
# from functools import wraps
# from flask import request, jsonify
# import jwt
# import os

# SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")

# def token_required(f):
#     """Protect routes using JWT Authorization header."""
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         if "Authorization" in request.headers:
#             parts = request.headers["Authorization"].split(" ")
#             if len(parts) == 2 and parts[0].lower() == "bearer":
#                 token = parts[1]

#         if not token:
#             return jsonify({"error": "Token is missing!"}), 401

#         try:
#             jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         except Exception as e:
#             return jsonify({"error": "Invalid or expired token", "details": str(e)}), 401

#         return f(*args, **kwargs)
#     return decorated





# backend/app/utils/auth_middleware.py
from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    """Protect routes using JWT Authorization header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # ✅ Extract Bearer token
        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split(" ")
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            # ✅ Get SECRET_KEY dynamically from the current Flask app
            secret_key = current_app.config.get("JWT_SECRET_KEY", "supersecretkey")

            # ✅ Decode using the same key used by Flask-JWT-Extended
            jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({"error": "Invalid or expired token", "details": str(e)}), 401
        except Exception as e:
            return jsonify({"error": "Token verification failed", "details": str(e)}), 401

        return f(*args, **kwargs)
    return decorated
