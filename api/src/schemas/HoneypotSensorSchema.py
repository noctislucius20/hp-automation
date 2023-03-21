from src import ma

class HoneypotSensor(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
        fields = ('honeypot_id', 'sensor_id', 'status', 'created_at', 'updated_at')
  
    