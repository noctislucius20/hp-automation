from flask import Blueprint, request, make_response
from src.errors.ClientError import ClientError
from src.schemas import AuthenticationsSchema
from src.services.UsersService import UsersService
from src.services.AuthenticationsService import AuthenticationsService
from src.tokenize import TokenManager
from flask_marshmallow import exceptions

auth = Blueprint('auth', __name__)

@auth.route('/auth', methods=['POST'])
def add_token():
    data = request.get_json()
    try:
        AuthenticationsSchema.AuthenticationsPost().load(data)
        id = UsersService().verify_user_credential(data.get('username'), data.get('password'))

        access_token = TokenManager.TokenManager().generate_access_token(id)
        refresh_token = TokenManager.TokenManager().generate_refresh_token(id)

        AuthenticationsService().add_refresh_token(refresh_token)

        response = make_response({'status': 'success', 'message': 'authentication added successfully', 'data': {'access_token': access_token, 'refresh_token': refresh_token}})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 201
        return response

    except exceptions.ValidationError as e:
        response = make_response({'status': 'error', 'message': e.messages})
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json'
        return response
    
    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]})
        response.status_code = e.status_code
        response.headers['Content-Type'] = 'application/json'
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'})
        response.status_code = 500
        response.headers['Content-Type'] = 'application/json'
        return response


@auth.route('/auth', methods=['PUT'])
def update_token():
    data = request.get_json()
    try:
        AuthenticationsSchema.AuthenticationsPut().load(data)
        AuthenticationsService().verify_refresh_token(data.get('refresh_token'))
        id = TokenManager.TokenManager().verify_refresh_token(data.get('refresh_token'))

        access_token = TokenManager.TokenManager().generate_access_token(id)

        response = make_response({'status': 'success', 'message': 'access token updated', 'data': access_token})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200
        return response
        
    except exceptions.ValidationError as e:
        response = make_response({'status': 'error', 'message': e.messages})
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json'
        return response
    
    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]})
        response.status_code = e.status_code
        response.headers['Content-Type'] = 'application/json'
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'})
        response.status_code = 500
        response.headers['Content-Type'] = 'application/json'
        return response
    
@auth.route('/auth', methods=['DELETE'])
def delete_token():
    data = request.get_json()
    try:
        AuthenticationsSchema.AuthenticationsDelete().load(data)
        AuthenticationsService().verify_refresh_token(data.get('refresh_token'))
        AuthenticationsService().delete_refresh_token(data.get('refresh_token'))

        response = make_response({'status': 'success', 'message': 'access token deleted successfully'})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 204
        return response

    except exceptions.ValidationError as e:
        response = make_response({'status': 'error', 'message': e.messages})
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json'
        return response
    
    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]})
        response.status_code = e.status_code
        response.headers['Content-Type'] = 'application/json'
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'})
        response.status_code = 500
        response.headers['Content-Type'] = 'application/json'
        return response
