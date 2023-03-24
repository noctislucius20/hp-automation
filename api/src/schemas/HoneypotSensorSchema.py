from src import ma

class HoneypotSensor(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
  
    id = ma.Integer(required=False)
    honeypot_id = ma.Integer(required=True)
    sensor_id = ma.Integer(required=True)
    status = ma.Boolean(required=False)
    created_at = ma.DateTime(required=False)
    updated_at = ma.DateTime(required=False)
