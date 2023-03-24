from flask import Blueprint, request, make_response, jsonify
from src.errors.ClientError import ClientError
from src.services.SensorsService import SensorsService
from src.schemas.SensorsSchema import Sensors as SensorsSchema
from flask_marshmallow import exceptions

import requests
import json
import os
# from src.controllers.AuthController import token_required

sensor = Blueprint('sensor', __name__)

@sensor.route('/sensors', methods=['POST'])
def create_sensor():
    data = request.get_json()
    try:
        SensorsSchema().load(data=data)
        new_sensor = SensorsService().add_sensor(ip_address=data.get('ip_address'), description=data.get('description'))
        # new_job = requests.post(url=f'{os.getenv("SERVER_URL")}/ansible/jobs', data=json.dumps(new_sensor), headers={'Content-Type': 'application/json'})

        response = make_response({'status': 'success', 'message': 'new sensor created', 'data': new_sensor})
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

@sensor.route('/sensors', methods=['GET'])
def get_all_sensors():
    sensors = SensorsService().list_all_sensors()

    response = make_response({'status': 'success', 'data': sensors})
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 200
    return response

@sensor.route('/sensors/<id>', methods=['GET'])
def get_sensor_by_id(id):
    try:
        sensor = SensorsService().get_one_sensor(id)

        response = make_response({'status': 'success', 'data': sensor})
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
    
@sensor.route('/sensors/<id>', methods=['PUT'])
def update_sensor_by_id(id):
    data = request.get_json()
    try:
        SensorsSchema().load(data=data)
        SensorsService().edit_sensor(id=id, ip_address=data.get('ip_address'), description=data.get('description'))

        response = make_response({'status': 'success', 'message': 'sensor successfully updated'})
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

@sensor.route('/sensors/<id>', methods=['DELETE'])
def delete_sensor_by_id(id):
    try:
        SensorsService().delete_sensor(id=id)
        response = make_response({'status': 'success', 'message': 'sensor deleted successfully'})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 204
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