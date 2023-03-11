from flask import Blueprint, request, make_response
from src.errors.ClientError import ClientError
from src.services.HoneypotsService import HoneypotsService
# from src.controllers.AuthController import token_required

honeypot = Blueprint('honeypot', __name__)

@honeypot.route('/honeypots', methods=['POST'])
def create_honeypot():
    data = request.get_json()
    try:
        new_honeypot = HoneypotsService().add_honeypot(name=data.get('name'))

        response = make_response({'status': 'success', 'message': 'new honeypot created', 'data': new_honeypot})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 201
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.message})
        response.status_code = e.statusCode
        response.headers['Content-Type'] = 'application/json'
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'})
        response.status_code = 500
        response.headers['Content-Type'] = 'application/json'
        return response

@honeypot.route('/honeypots', methods=['GET'])
def get_all_honeypots():
    honeypots = HoneypotsService().list_all_honeypots()

    response = make_response({'status': 'success', 'data': honeypots})
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 200
    return response

@honeypot.route('/honeypots/<name>', methods=['GET'])
def get_honeypot_by_honeypotname(name):
    try:
        honeypot = HoneypotsService().get_one_honeypot(name)

        response = make_response({'status': 'success', 'data': honeypot})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.message})
        response.status_code = e.statusCode
        response.headers['Content-Type'] = 'application/json'
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'})
        response.status_code = 500
        response.headers['Content-Type'] = 'application/json'
        return response
    
@honeypot.route('/honeypots/<name>', methods=['PUT'])
def update_honeypot_by_honeypotname(name):
    data = request.get_json()
    try:
        HoneypotsService().edit_honeypot(name=name, new_name=data.get('new_name'))

        response = make_response({'status': 'success', 'message': 'honeypot successfully updated'})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.message})
        response.status_code = e.statusCode
        response.headers['Content-Type'] = 'application/json'
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'})
        response.status_code = 500
        response.headers['Content-Type'] = 'application/json'
        return response

@honeypot.route('/honeypots', methods=['DELETE'])
def delete_honeypot_by_honeypotname():
    data = request.get_json()
    try:
        HoneypotsService().delete_honeypot(name=data.get('name'))
        response = make_response({'status': 'success', 'message': 'honeypot deleted successfully'})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.message})
        response.status_code = e.statusCode
        response.headers['Content-Type'] = 'application/json'
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'})
        response.status_code = 500
        response.headers['Content-Type'] = 'application/json'
        return response