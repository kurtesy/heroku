from functools import wraps
from flask import request, abort, make_response, jsonify
from config import dev


def require_appkey(api_call):
    @wraps(api_call)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == dev.APP_API_KEY:
            return api_call(*args, **kwargs)
        else:
            abort(
                make_response(
                    jsonify({
                        "status": "ERROR",
                        "errorCode": "auth-error"
                    }), 401))
    return decorated_function
