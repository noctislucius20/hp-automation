from flask import Blueprint, request, make_response
from src.errors.ClientError import ClientError
from src.services.HoneypotSensorService import HoneypotSensorService
from src.schemas.HoneypotSensorSchema import PostHoneypotSensor, GetHoneypotSensor, PutHoneypotSensor
from flask_marshmallow import exceptions
from src.tokenize.TokenManager import token_required

honeypotsensor = Blueprint('honeypotsensor', __name__)

@honeypotsensor.route('/honeypotsensor', methods=['POST'])
def create_honeypotsensor():
    data = request.get_json()
    try:
        token_required()

        PostHoneypotSensor().load(data=data)
        honeypotsensor_svc = HoneypotSensorService()
        honeypotsensor = honeypotsensor_svc.add_honeypotsensor(honeypot=data.get('honeypot'), sensor_id=data.get('sensor_id'))

        response = make_response({'status': 'success', 'message': 'new honeypotsensor created', 'data': honeypotsensor}, 201)
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


@honeypotsensor.route('/honeypotsensor', methods=['PUT'])
def update_honeypotsensor():
    data = request.get_json()
    try:
        token_required()

        PutHoneypotSensor().load(data=data)
        honeypotsensor_svc = HoneypotSensorService()
        honeypotsensor_svc.update_honeypotsensor(sensor_id=data.get('sensor_id'), honeypot=data.get('honeypot'))

        response = make_response({'status': 'success', 'message': 'honeypotsensor updated successfully'}, 200)
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

@honeypotsensor.route('/honeypotsensor/<id>', methods=['DELETE'])
def delete_honeypotsensor_by_id(id):
    try:
        token_required()

        HoneypotSensorService().delete_honeypotsensor(id=id)
        response = make_response({'status': 'success', 'message': 'honeypotsensor deleted successfully'}, 204)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response