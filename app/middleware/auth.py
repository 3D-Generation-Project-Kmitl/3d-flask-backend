from functools import wraps
import jwt
from flask import request, abort
from flask import current_app

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "error": "Unauthorized"
            }, 401
        try:
            data = jwt.decode(token, current_app.config['AUTH_SECRET'], algorithms=["HS256"])
            user_id = request.args.get('id')
            if str(user_id)!=str(data['id']):
                return {
                    "message": "Access denied",
                    "error": "Unauthorized",
                }, 401
        except jwt.ExpiredSignatureError:
            return {
                "message": "Token is expired",
                "error": "Unauthorized"
            }, 401
        except Exception:
            return {
                "message": "Token is invalid",
                "error": "Unauthorized"
            }, 401
        return f(*args, **kwargs)
    
    return decorated