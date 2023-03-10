from werkzeug.security import generate_password_hash, check_password_hash
from src.models.UsersModel import Users as UsersModel
from src.schemas.UsersSchema import Users as UsersSchema
from src import db
from src.exceptions.InvariantError import InvariantError

import datetime as dt

class UsersService:
    def add_user(self, username, password, first_name, last_name):
        self.check_user_existed(username)
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = UsersModel(username = username, password = hashed_password, first_name = first_name, last_name = last_name, roles = 'user', status = True, created_at = dt.datetime.now(), updated_at = dt.datetime.now())

        db.session.add(new_user)
        db.session.commit()

        user_schema = UsersSchema()

        return user_schema.dump(new_user)
    
    def check_user_existed(self, username):
        user = UsersModel.query.filter_by(username=username, status=True).first()

        if user:
            raise InvariantError(message="user already exists")
        
    def list_all_users(self):
        users = UsersModel.query.filter_by(status=True).all()
        users_schema = UsersSchema(many=True)
        
        return users_schema.dump(users)
    
    def get_one_user(self, username):
        user = UsersModel.query.filter_by(username=username, status=True).first()
        user_schema = UsersSchema()

        if not user:
            raise InvariantError(message="user not exist")

        return user_schema.dump(user)

    def edit_user(self, username, first_name, last_name, password, new_password, new_username):
        user = UsersModel.query.filter_by(username=username, status=True).first()

        if not user:
            raise InvariantError(message="user not exist")
        
        check_pass = check_password_hash(user.password, password)

        if not check_pass:
            raise InvariantError(message='password invalid')
        
        if user.username != new_username:
            self.check_user_existed(new_username)

        user.username = new_username if new_username != None and new_username != '' else user.username
        user.first_name = first_name if first_name != None and first_name != '' else user.first_name
        user.last_name = last_name if last_name != None and last_name != '' else user.last_name
        user.password = generate_password_hash(new_password, method='sha256') if new_password != None and new_password != '' else user.password
        user.updated_at = dt.dt.now() 

        db.session.commit()

    def delete_user(self, username):
        user = UsersModel.query.filter_by(username=username, status=True).first()

        if not user:
            raise InvariantError(message="user not exist")
        
        user.status = False

        db.session.commit()

