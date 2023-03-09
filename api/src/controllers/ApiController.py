from flask import Blueprint, make_response

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def get_api_info():
    response = make_response({'description': 'API information', 'current_version': '/api/v1'})
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 200
    return response