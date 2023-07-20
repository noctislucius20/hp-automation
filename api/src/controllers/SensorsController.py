import asyncio
from time import sleep
from flask import Blueprint, request, make_response, jsonify
from src import socketio
from src.utils.MappingRequest import mapping_data
from src.errors.ClientError import ClientError
from src.services.SensorsService import SensorsService
from src.schemas.SensorsSchema import Sensors as SensorsSchema
from flask_marshmallow import exceptions

from src.tokenize.TokenManager import token_required

sensor = Blueprint('sensor', __name__)

@sensor.route('/sensors', methods=['POST'])
def create_sensor():
    data = request.get_json()
    try:
        token_required()

        data = mapping_data(data)

        SensorsSchema().load(data=data)
        sensor_svc = SensorsService()
        sensor_svc.add_sensor(ip_address=data.get('ip_address'), description=data.get('description'), honeypot=data.get('honeypot'), name=data.get('name'), callback=sensor_svc.execute_init_job)

        response = make_response({'status': 'success', 'message': 'new sensor created'}, 201)
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

@sensor.route('/sensors', methods=['GET'])
def get_all_sensors():
    try:
        token_required()

        sensors = asyncio.run(SensorsService().list_all_sensors())

        response = make_response({'status': 'success', 'data': sensors}, 200)
        return response
    
    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response

@sensor.route('/sensors/<id>', methods=['GET'])
def get_sensor_by_id(id):
    try:
        token_required()

        sensor = asyncio.run(SensorsService().get_one_sensor(id))

        response = make_response({'status': 'success', 'data': sensor}, 200)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response
    
@sensor.route('/sensors/<id>', methods=['PUT'])
def update_sensor_by_id(id):
    data = request.get_json()
    try:
        token_required()

        data = mapping_data(data)

        SensorsSchema().load(data=data)

        sensor_svc = SensorsService()
        sensor_svc.edit_sensor(id=id, ip_address=data.get('ip_address'), name=data.get('name'), description=data.get('description'), honeypot=data.get('honeypot'), callback=sensor_svc.execute_update_job)

        response = make_response({'status': 'success', 'message': 'sensor successfully updated'}, 200)
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

@sensor.route('/sensors/<id>', methods=['DELETE'])
def delete_sensor_by_id(id):
    try:
        SensorsService().delete_sensor(id=id)
        response = make_response({'status': 'success', 'message': 'sensor deleted successfully'}, 204)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response
    
@sensor.route('/sensors/<id>/logs', methods=['GET'])
def get_logs_by_sensor_id(id):
    try:
        token_required()
        
        logs = SensorsService().get_logs(id)

        if logs['finished'] == False:
            socketio.emit('logs', logs['data'])
            socketio.sleep(1)
            return {'status': 'success'} 

        return make_response({'status': 'success', 'data': logs['data']}, 200)
        
    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response

@sensor.route('/sensors/<id>/relaunch', methods=['POST'])
def relaunch_sensor_job(id):
    try:
        token_required()

        SensorsService().relaunch_job(id)

        response = make_response({'status': 'success', 'message': 'job relaunched'}, 200)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response

@sensor.route('/sensors/<id>/cancel', methods=['POST'])
def cancel_sensor_job(id):
    try:
        token_required()

        SensorsService().cancel_job(id)

        response = make_response({'status': 'success', 'message': 'job cancelled'}, 200)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response

@socketio.on('disconnect')
def close_connection():
    print('Client disconnected')