from flask import Blueprint, request, make_response
from src.exceptions.ClientError import ClientError
from src.services.SensorsService import SensorsService
# from src.controllers.AuthController import token_required

sensor = Blueprint('sensor', __name__)

@sensor.route('/sensors', methods=['POST'])
def create_sensor():
    data = request.get_json()
    try:
        new_sensor = SensorsService().add_sensor(name=data.get('name'), ip_address=data.get('ip_address'), state=data.get('state'))

        response = make_response({'status': 'success', 'message': 'new sensor created', 'data': new_sensor})
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

@sensor.route('/sensors', methods=['GET'])
def get_all_sensors():
    sensors = SensorsService().list_all_sensors()

    response = make_response({'status': 'success', 'data': sensors})
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 200
    return response

@sensor.route('/sensors/<name>', methods=['GET'])
def get_sensor_by_sensorname(name):
    try:
        sensor = SensorsService().get_one_sensor(name)

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
    
@sensor.route('/sensors/<name>', methods=['PUT'])
def update_sensor_by_sensorname(name):
    data = request.get_json()
    try:
        SensorsService().edit_sensor(name=name, new_name=data.get('new_name'), ip_address=data.get('ip_address'), state=data.get('state'))

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

@sensor.route('/sensors', methods=['DELETE'])
def delete_sensor_by_sensorname():
    data = request.get_json()
    try:
        SensorsService().delete_sensor(name=data.get('name'))
        response = make_response({'status': 'success', 'message': 'sensor deleted successfully'})
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