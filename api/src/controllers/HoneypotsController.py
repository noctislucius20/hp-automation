from flask import Blueprint, request, make_response
from src.errors.ClientError import ClientError
from src.services.HoneypotsService import HoneypotsService
from src.schemas.HoneypotsSchema import Honeypots as HoneypotsSchema
from flask_marshmallow import exceptions
from src.tokenize.TokenManager import token_required

honeypot = Blueprint('honeypot', __name__)

@honeypot.route('/honeypots', methods=['POST'])
def create_honeypot():
    data = request.get_json()
    try:
        token_required()
        
        HoneypotsSchema().load(data=data)
        new_honeypot = HoneypotsService().add_honeypot(name=data.get('name'), description=data.get('description'))

        response = make_response({'status': 'success', 'message': 'new honeypot created', 'data': new_honeypot}, 201)
        return response
    
    except exceptions.ValidationError as e:
        response = make_response({'status': 'error', 'message': e.messages}, 400)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response

@honeypot.route('/honeypots', methods=['GET'])
def get_all_honeypots():
    try:
        token_required()

        honeypots = HoneypotsService().list_all_honeypots()

        response = make_response({'status': 'success', 'data': honeypots}, 200)
        return response
        
    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response

@honeypot.route('/honeypots/<id>', methods=['GET'])
def get_honeypot_by_id(id):
    try:
        token_required()

        honeypot = HoneypotsService().get_one_honeypot(id)

        response = make_response({'status': 'success', 'data': honeypot}, 200)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response
    
@honeypot.route('/honeypots/<id>', methods=['PUT'])
def update_honeypot_by_id(id):
    data = request.get_json()
    try:
        token_required()

        HoneypotsSchema().load(data=data)
        HoneypotsService().edit_honeypot(id=id, name=data.get('name'), description=data.get('description'))

        response = make_response({'status': 'success', 'message': 'honeypot successfully updated'}, 200)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response

@honeypot.route('/honeypots/<id>', methods=['DELETE'])
def delete_honeypot_by_id(id):
    try:
        token_required()

        HoneypotsService().delete_honeypot(id)
        response = make_response({'status': 'success', 'message': 'honeypot deleted successfully'}, 204)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response