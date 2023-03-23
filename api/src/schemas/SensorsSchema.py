from src import ma

class Sensors(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
        fields = ('id', 'ip_address', 'description', 'status', 'created_at', 'updated_at')
  
    