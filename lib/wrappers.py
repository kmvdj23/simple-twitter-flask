import json
from functools import wraps
from flask import redirect, url_for, request, jsonify
from flask_login import current_user


def token_required(func):
    @wraps(func)
    def has_token(*args, **kwargs):
        if 'auth_token' in request.headers:
            return func(*args, **kwargs)
        else:
            data = {
                'message' : 'token is missing'
            }
            return jsonify(data)
    return
