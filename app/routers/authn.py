from flask_restx import Namespace, Resource, fields
from flask import request
from app.dependencies.error_response import abort, createToken, checkAuth
from app.internal.yaml_loader import PI_SERIAL_NUMBER

__NS_URL = 'authn'
authn = Namespace(__NS_URL.capitalize(), description=f'APIs for {__NS_URL}', path=f'/{__NS_URL}')
authn_request_body = authn.model("Authn Request Body",{
    'username': fields.String(description='username'),
    'password': fields.String(description='password'),
})
token_response = authn.model("Token Response",{
    'token': fields.String(description='token response'),
    'gateway_id': fields.String(description='id of gateway'),
})
@authn.route('/')
class AuthnAPI(Resource):
    @authn.expect(authn_request_body)
    @authn.marshal_with(token_response)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        token = createToken(username, password)
        if checkAuth(token):
            return {
                'token': token,
                'gateway_id': PI_SERIAL_NUMBER
            }
        else:
            return abort(401, 'Unauthorized')