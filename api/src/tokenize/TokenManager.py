import json
from src.errors.InvariantError import InvariantError
from src.errors.AuthorizationError import AuthorizationError
from functools import wraps
from flask import request, make_response

import jwt
import os
import datetime as dt


def token_required():
    try:
        token = None

        if not 'Authorization' in request.headers:
            raise AuthorizationError(message='Token is missing')
        
        token = request.headers.get('Authorization').replace('Bearer ', '')
        user = jwt.decode(token, os.getenv('ACCESS_TOKEN_KEY'), algorithms='HS256', verify=True)
        return user

    except Exception as e:
        raise AuthorizationError(message = e.args[0])

class TokenManager:
    def generate_access_token(self, payload):
        return jwt.encode({'id': payload['id'], 'username': payload['username'], 'roles': payload['roles'], 'exp': dt.datetime.utcnow() + dt.timedelta(seconds=int(os.getenv('ACCESS_TOKEN_AGE')))}, os.getenv('ACCESS_TOKEN_KEY'))
    
    def generate_refresh_token(self, payload):
        return jwt.encode({'id': payload['id'], 'username': payload['username'], 'roles': payload['roles'], 'exp': dt.datetime.utcnow() + dt.timedelta(seconds=int(os.getenv('REFRESH_TOKEN_AGE')))}, os.getenv('REFRESH_TOKEN_KEY'))
    
    def verify_refresh_token(self, refresh_token):
        try:
            user = jwt.decode(refresh_token, os.getenv('REFRESH_TOKEN_KEY'), algorithms='HS256', verify=True)
            return user

        except:
            raise InvariantError(message='refresh token invalid')