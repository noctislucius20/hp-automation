from src import ma

class AuthenticationsPost(ma.SQLAlchemySchema):
    class Meta:
        ordered = True

    username = ma.String(required=True)
    password = ma.String(required=True)

class AuthenticationsPut(ma.SQLAlchemySchema):
    refresh_token = ma.String(required=True)

class AuthenticationsDelete(ma.SQLAlchemySchema):
    refresh_token = ma.String(required=True)