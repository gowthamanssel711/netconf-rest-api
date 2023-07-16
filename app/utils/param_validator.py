from functools import wraps
from flask import request, jsonify

def validate_params(required_params):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.method =="GET":
                params = request.args
            if request.method =="POST" or "DELETE":
                params = list(request.get_json().keys())
            missing_params = [param for param in required_params if param not in params]
            if missing_params:
                error_message = f"Missing required parameters: {', '.join(missing_params)}"
                return jsonify(error=error_message), 400

            return func(*args, **kwargs)

        return wrapper

    return decorator