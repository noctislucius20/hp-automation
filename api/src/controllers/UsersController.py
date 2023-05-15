from flask import Blueprint, request, make_response
from src.errors.ClientError import ClientError
from src.services.UsersService import UsersService
from src.schemas.UsersSchema import UsersPost, UsersPut
from src.utils.MappingRequest import mapping_data
from src.tokenize.TokenManager import token_required
from flask_marshmallow import exceptions

user = Blueprint('user', __name__)

@user.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        data = mapping_data(data)
        UsersPost().load(data=data)
        result = UsersService().add_user(username=data.get('username'), password=data.get('password'), first_name=data.get('first_name'), last_name=data.get('last_name'))

        response = make_response({'status': 'success', 'message': 'new user created', 'data': result}, 201)
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

@user.route('/users', methods=['GET'])
def get_all_users():
    try:
        id = token_required()
    
        user = UsersService()
        user.verify_user_access(id=id['id'], username=None)
        
        result = user.list_all_users()
    
        response = make_response({'status': 'success', 'data': result}, 200)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response
    
@user.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):
    try:
        id = token_required()

        user = UsersService()
        user.verify_user_access(id=id['id'], username=username)

        result = user.get_one_user(username)

        response = make_response({'status': 'success', 'data': result}, 200)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response
    
@user.route('/users/<username>', methods=['PUT'])
def update_user_by_username(username):
    data = request.get_json()
    try:
        id = token_required()
        data = mapping_data(data)

        UsersPut().load(data=data)

        user = UsersService()
        current_user = user.verify_user_access(id=id['id'], username=username)
        user.edit_user(user_param=username, current_user=current_user, username=data.get('username'), first_name=data.get('first_name'), last_name=data.get('last_name'), roles=data.get('roles'))

        response = make_response({'status': 'success', 'message': 'user successfully updated'}, 200)
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

@user.route('/users/<username>', methods=['DELETE'])
def delete_user_by_username(username):
    try:
        id = token_required()

        user = UsersService()
        user.verify_user_access(id=id, username=username)
        user.delete_user(username=username)

        response = make_response({'status': 'success', 'message': 'user deleted successfully'}, 204)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response
    
@user.route('/users/<username>/change-password', methods=['PUT'])
def update_user_password_by_username(username):
    data = request.get_json()
    try:
        id = token_required()

        user = UsersService()
        current_user = user.verify_user_access(id=id, username=username)
        result = user.change_password(user_param=username, current_user=current_user, password=data.get('password'), new_password=data.get('new_password'))

        response = make_response({'status': 'success', 'message': 'user password successfully updated', 'data': result}, 200)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response
    
@user.route('/users/<username>/reset-password', methods=['PUT'])
def reset_user_password_by_username(username):
    try:
        id = token_required()

        user = UsersService()
        current_user = user.verify_user_access(id=id, username=username)
        result = user.reset_password(user_param=username, current_user=current_user)

        response = make_response({'status': 'success', 'message': 'user password successfully reset', 'data': result}, 200)
        return response

    except ClientError as e:
        response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
        return response

    except:
        #server error 
        response = make_response({'status': 'error', 'message': 'server fail'}, 500)
        return response