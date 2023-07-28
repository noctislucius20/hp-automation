from src import ma

class AuthenticationsPost(ma.SQLAlchemySchema):
    class Meta:
        ordered = True

    username = ma.String(required=True)
    password = ma.String(required=True)

class AuthenticationsPut(ma.SQLAlchemySchema):
    username = ma.String(required=True)
    roles = ma.String(required=True)
    refresh_token = ma.String(required=True)

class AuthenticationsDelete(ma.SQLAlchemySchema):
    refresh_token = ma.String(required=True)