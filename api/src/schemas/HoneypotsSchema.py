from src import ma

class Honeypots(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
        fields = ('id', 'name', 'status', 'created_at', 'updated_at')
  
    