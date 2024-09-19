import os
from flask import request
from functools import wraps

API_KEY = os.getenv('API_KEY')

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('x-api-key')
        if key and key == API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 401
    return decorated