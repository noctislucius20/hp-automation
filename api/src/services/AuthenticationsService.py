from src.models.AuthenticationsModel import Authentications as AuthenticationsModel
from src.errors.InvariantError import InvariantError
from src import db

class AuthenticationsService:
    def add_refresh_token(self, token):
        new_refresh_token = AuthenticationsModel(token = token)

        db.session.add(new_refresh_token)
        db.session.commit()

    def verify_refresh_token(self,token):
        check = AuthenticationsModel.query.filter_by(token = token).first()

        if not check:
            raise InvariantError(message= "refresh token is not valid")

    def delete_refresh_token(self, token):
        refresh_token = AuthenticationsModel.query.filter_by(token = token).first()

        db.session.delete(refresh_token)
        db.session.commit()