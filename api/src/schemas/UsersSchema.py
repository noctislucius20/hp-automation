from src import ma
from src.models.UsersModel import UserEnum

class UsersPost(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
    
    id = ma.Integer(required=False)
    username = ma.String(required=True)
    first_name = ma.String(required=False)
    last_name = ma.String(required=False)
    password = ma.String(required=False)
    roles = ma.Enum(enum=UserEnum, by_value=True, required=False)
    status = ma.Boolean(required=False)
    created_at = ma.DateTime(required=False)
    updated_at = ma.DateTime(required=False)
    
class UsersPut(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
    
    username = ma.String(required=False)
    first_name = ma.String(required=False)
    last_name = ma.String(required=False)
    roles = ma.Enum(enum=UserEnum, by_value=True, required=False)
    created_at = ma.DateTime(required=False)
    updated_at = ma.DateTime(required=False)