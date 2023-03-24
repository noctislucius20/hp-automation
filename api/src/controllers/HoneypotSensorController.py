from flask import Blueprint, request, make_response
from src.errors.ClientError import ClientError
from src.services.HoneypotSensorService import HoneypotSensorService
from src.schemas.HoneypotSensorSchema import HoneypotSensor as HoneypotSensorSchema
from flask_marshmallow import exceptions
# from src.controllers.AuthController import token_required

honeypotsensor = Blueprint('honeypotsensor', __name__)

@honeypotsensor.route('/honeypotsensor', methods=['POST'])
def create_honeypotsensor():
    data = request.get_json()
    try:
        HoneypotSensorSchema().load(data=data)
        new_honeypotsensor = HoneypotSensorService().add_honeypotsensor(honeypot_id=data.get('honeypot_id'), sensor_id=data.get('sensor_id'), status=data.get('status'))

        response = make_response({'status': 'success', 'message': 'new honeypotsensor created', 'data': new_honeypotsensor})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 201
        return response

    except exceptions.ValidationError as e:
        response = make_response({'status': 'error', 'message': e.messages})
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json'
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

@honeypotsensor.route('/honeypotsensor', methods=['DELETE'])
def delete_honeypotsensor_by_id():
    data = request.get_json()
    try:
        HoneypotSensorService().delete_honeypotsensor(honeypot_id=data.get('honeypot_id'), sensor_id=data.get('sensor_id'))
        response = make_response({'status': 'success', 'message': 'honeypotsensor deleted successfully'})
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