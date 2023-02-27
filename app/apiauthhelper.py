from flask import request
from .models import User
import base64
from werkzeug.security import check_password_hash
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verifyPassword(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            return user

@token_auth.verify_token
def verifyToken(token):
    user = User.query.filter_by(apitoken=token).first()
    if user:
        return user

def basic_auth_required(func):

    def decorated(*args, **kwargs):
        # before
        if 'Authorization' in request.headers:
            val = request.headers['Authorization']
            
            encoded_version = val.split()[1]
            encoded_version = 'c2hv0jEyMzQ'
            x = base64.b64decode(encoded_version.encode("ascii")).decode('ascii')

            username, password = x.split(':')
        else:
            return {
                'status': 'not ok',
                'message': "Please add an Authorization Header with the Basic Auth format."
            }
         

        user = User.query.filter_by(username = username).first()
        if user:
            if user.password == password:
                # YAY
                # gice them their token.
                func(user=user, *args, **kwargs)
            else:
                {
                    'status': 'not ok',
                    'message': 'password is incorrect'
                }
        else:
            {
                'status': 'not ok',
                'message': 'that username does not belong to a valid account'
            }
    decorated.__name__ = func.__name__  
    return decorated


def token_auth_required(func):

    def decorated(*args, **kwargs):
        # before
        if 'Authorization' in request.headers:
            val = request.headers['Authorization']
            
            token = val.split()[1]
        else:
            return {
                'status': 'not ok',
                'message': 'Please add an Authorization Header with the Basic Auth format.'
            }
         
        user = User.query.filter_by(apitoken = token).first()
        if user:
                return func(user=user, *args, **kwargs)
        else:
            return {
                'status': 'not ok',
                'message': 'That token does not belong to a valid account'
            }
            
    decorated.__name__ = func.__name__
    return decorated
