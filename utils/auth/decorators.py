from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request

from utils.http.responses import Response


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if claims["role"] == "admin":
                return fn(*args, **kwargs)
            else:
                return Response.get_message(403, message="Forbidden")

        return decorator

    return wrapper
