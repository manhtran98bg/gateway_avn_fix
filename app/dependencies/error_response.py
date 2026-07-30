from app.models.databases import User
from app import db
from flask import request
import base64
from flask_restx import reqparse, abort
from functools import wraps

auth_header = reqparse.RequestParser()
auth_header.add_argument('Authorization', location='headers', required=True, 
                         help='Authorization header is required', default='Basic YWRtaW46YWRtaW4=')

def login_required(f):
    @wraps(f)
    def wrapped_view(*args,**kwargs):
        auth = request.headers.get('Authorization')
        if not checkAuth(auth):
            return ({'message':'Unauthorized'}, 401)
        return f(*args,**kwargs)
    return wrapped_view

def requiredBody(f):
    @wraps(f)
    def wrapped_view(*args,**kwargs):
        body = request.get_json()
        if body == None:
            return badRequestError('Missing body in request')
        return f(*args,**kwargs)
    return wrapped_view

def checkAuth(auth: str)->bool:
    if isinstance(auth, str):
        _users = db.session.query(User).all()[0]
        db.session.close()
        return (auth == createToken(_users.username, _users.password))
    else:
        return False
    
def createToken(username: str, password: str)->str:
    b64Val = f'{username}:{password}'
    return f'Basic {base64.b64encode(b64Val.encode()).decode()}'
    
def badRequestError(desc: str)->any:
    response = abort(400, desc)
    return response