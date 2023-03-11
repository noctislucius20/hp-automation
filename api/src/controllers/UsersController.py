from flask import Blueprint, request, make_response
from src.exceptions.ClientError import ClientError
from src.services.UsersService import UsersService
# from src.controllers.AuthController import token_required

user = Blueprint('user', __name__)

@user.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        new_user = UsersService().add_user(username=data.get('username'), password=data.get('password'), first_name=data.get('first_name'), last_name=data.get('last_name'))

        response = make_response({'status': 'success', 'message': 'new user created', 'data': new_user})
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

@user.route('/users', methods=['GET'])
def get_all_users():
    users = UsersService().list_all_users()

    response = make_response({'status': 'success', 'data': users})
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 200
    return response

@user.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):
    try:
        user = UsersService().get_one_user(username)

        response = make_response({'status': 'success', 'data': user})
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
    
@user.route('/users/<username>', methods=['PUT'])
def update_user_by_username(username):
    data = request.get_json()
    try:
        UsersService().edit_user(username=username, first_name=data.get('first_name'), last_name=data.get('last_name'), new_username=data.get('new_username'))

        response = make_response({'status': 'success', 'message': 'user successfully updated'})
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

@user.route('/users', methods=['DELETE'])
def delete_user_by_username():
    data = request.get_json()
    try:
        UsersService().delete_user(username=data.get('username'))
        response = make_response({'status': 'success', 'message': 'user deleted successfully'})
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