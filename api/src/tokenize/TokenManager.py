from src.errors.InvariantError import InvariantError
from functools import wraps
from flask import request, make_response

import jwt
import os
import datetime as dt
import json


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            token = request.headers.get('Authorization').replace('Bearer ', '')
            jwt.decode(token, os.getenv('ACCESS_TOKEN_KEY'), algorithms='HS256', verify=True)

        except Exception as e:
            return make_response({'status': 'error', 'message': e.args[0]}, 403)
        
        return f(*args, **kwargs)

    return decorator

class TokenManager:
    def generate_access_token(self, payload):
        return jwt.encode({'id': payload, 'exp': dt.datetime.utcnow() + dt.timedelta(seconds=int(os.getenv('ACCESS_TOKEN_AGE')))}, os.getenv('ACCESS_TOKEN_KEY'))
    
    def generate_refresh_token(self, payload):
        return jwt.encode({'id': payload}, os.getenv('REFRESH_TOKEN_KEY'))
    
    def verify_refresh_token(self, refresh_token):
        try:
            return jwt.decode(refresh_token, os.getenv('REFRESH_TOKEN_KEY'), algorithms='HS256', verify=True)

        except:
            raise InvariantError(message='refresh token invalid')