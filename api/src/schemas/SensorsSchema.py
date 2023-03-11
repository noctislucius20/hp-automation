from src import ma

class Sensors(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
        fields = ('name', 'ip_address', 'state', 'status', 'created_at', 'updated_at')
  
    