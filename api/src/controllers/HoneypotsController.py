from flask import Blueprint, request, make_response
from src.errors.ClientError import ClientError
from src.services.HoneypotsService import HoneypotsService
from src.schemas.HoneypotsSchema import Honeypots as HoneypotsSchema
from flask_marshmallow import exceptions
from src.tokenize.TokenManager import token_required

honeypot = Blueprint('honeypot', __name__)

@honeypot.route('/honeypots', methods=['POST'])
@token_required
def create_honeypot():
    data = request.get_json()
    try:
        HoneypotsSchema().load(data=data)
        new_honeypot = HoneypotsService().add_honeypot(name=data.get('name'))

        response = make_response({'status': 'success', 'message': 'new honeypot created', 'data': new_honeypot})
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

@honeypot.route('/honeypots', methods=['GET'])
@token_required
def get_all_honeypots():
    honeypots = HoneypotsService().list_all_honeypots()

    response = make_response({'status': 'success', 'data': honeypots})
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 200
    return response

@honeypot.route('/honeypots/<id>', methods=['GET'])
@token_required
def get_honeypot_by_id(id):
    try:
        honeypot = HoneypotsService().get_one_honeypot(id)

        response = make_response({'status': 'success', 'data': honeypot})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200
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
    
@honeypot.route('/honeypots/<id>', methods=['PUT'])
@token_required
def update_honeypot_by_id(id):
    data = request.get_json()
    try:
        HoneypotsSchema().load(data=data)
        HoneypotsService().edit_honeypot(id=id, name=data.get('name'))

        response = make_response({'status': 'success', 'message': 'honeypot successfully updated'})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200
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

@honeypot.route('/honeypots/<id>', methods=['DELETE'])
@token_required
def delete_honeypot_by_id(id):
    try:
        HoneypotsService().delete_honeypot(id)
        response = make_response({'status': 'success', 'message': 'honeypot deleted successfully'})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 204
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