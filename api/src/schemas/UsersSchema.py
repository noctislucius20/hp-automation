from src import ma
from src.models.UsersModel import UserEnum

class Users(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
        fields = ('username', 'first_name', 'last_name', 'roles', 'status', 'created_at', 'updated_at')
  
    roles = ma.Enum(enum=UserEnum, by_value=True)
    