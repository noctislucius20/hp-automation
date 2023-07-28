import json
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.UsersModel import Users as UsersModel
from src.schemas.UsersSchema import UsersPost, UsersPut
from src.errors.InvariantError import InvariantError
from src.errors.AuthenticationError import AuthenticationError
from src.errors.AuthorizationError import AuthorizationError
from src import db

import datetime as dt
import secrets

class UsersService:
    def add_user(self, username, password, first_name, last_name):
        check_user = UsersModel.query.filter_by(username = username).first()

        user_schema = UsersPost()

        if not check_user:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = UsersModel(username = username, password = hashed_password, first_name = first_name, last_name = last_name, roles = 'user', status = True, created_at = dt.datetime.now(), updated_at = dt.datetime.now())

            db.session.add(new_user)
            db.session.commit()

            return user_schema.dump(new_user)
        
        if check_user.status == False:
            check_user.status = True
            check_user.password = generate_password_hash(password, method='sha256')
            check_user.created_at = dt.datetime.now()
            check_user.updated_at = dt.datetime.now()

            db.session.commit()

            return user_schema.dump(check_user)

        else:
            raise InvariantError(message="Username already exist")

    def list_all_users(self):
        users = UsersModel.query.filter_by(status=True).all()

        users_schema = UsersPut(many=True)
        
        return users_schema.dump(users)
    
    def get_one_user(self, username):
        user = self.check_user_existed(username)
        user_schema = UsersPut()

        return user_schema.dump(user)

    def edit_user(self, current_user, user_param, username, first_name, last_name, roles):
        user = self.check_user_existed(user_param)
        
        # username, first and last name only can be changed by its user
        if user.username != username:
            check_user = UsersModel.query.filter_by(username=username, status=True).first()
            if check_user:
                raise InvariantError(message="Username already exist")
            # if current_user.roles.value == 'admin' and current_user.username != user_param:
            if current_user.username != user_param:
                raise AuthorizationError(message="You don't have permission to change this user")

        if user.first_name != first_name or user.last_name != last_name:
            if current_user.username != user_param:
                raise AuthorizationError(message="You don't have permission to change this user")
            
        # roles only can be changed by admin
        if user.roles.value != roles:
            if current_user.roles.value != 'admin':
                raise AuthorizationError(message="You don't have permission to change this user")
      

        db.session.execute(db.update(UsersModel).values({'username': username, 'first_name': first_name, 'last_name': last_name, 'roles': roles, 'updated_at': dt.datetime.now()}).where(UsersModel.id == user.id))
        db.session.commit()

    def delete_user(self, username):
        user = self.check_user_existed(username)
        user.status = False

        db.session.commit()

    def change_password(self, user_param, current_user, password, new_password):
        user = self.check_user_existed(user_param)

        if password == None or new_password == None:
            raise InvariantError(message="password and new password must be filled")

        if current_user.roles.value == 'admin' and current_user.username != user_param:
            raise AuthorizationError(message="You don't have permission to change this password")
        
        match = check_password_hash(user.password, password)

        if not match:
            raise InvariantError(message="Password is not match with current password")
        
        user.password = generate_password_hash(new_password, method='sha256')
        user.updated_at = dt.datetime.now()

        db.session.commit()

    def reset_password(self, user_param, current_user):
        user = self.check_user_existed(user_param)

        if current_user.roles.value != 'admin':
            raise AuthorizationError(message="You don't have permission to change this password")

        random_password = secrets.token_hex(8)
        user.password = generate_password_hash(random_password, method='sha256')
        user.updated_at = dt.datetime.now()
 
        db.session.commit()

        return random_password

    def check_user_existed(self, username):
        user = UsersModel.query.filter_by(username=username, status=True).first()
    
        if not user:
            raise InvariantError(message="Username not exists")
        
        return user
        
    def verify_user_credential(self, username, password):
        user = UsersModel.query.filter_by(username=username, status=True).first()

        user_schema = UsersPost()

        if not user:
            raise AuthenticationError(message = 'Credential invalid')

        match = check_password_hash(user.password, password)

        if not match:
            raise AuthenticationError(message = 'Credential invalid')
        
        return user_schema.dump(user)
    
    def verify_user_access(self, id, username):
        user = UsersModel.query.filter_by(id=id, status=True).first()

        if not user:
            raise AuthenticationError(message = 'Credential invalid')
        
        if user.username != username:
            if user.roles.value != 'admin':
                raise AuthorizationError(message = "You don't have permission to do this action")
        
        return user
                
                