from src import ma
from src.schemas.HoneypotsSchema import Honeypots as HoneypotsSchema

class HoneypotSensor(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
  
    id = ma.Integer(required=False)
    honeypot = ma.List(ma.Nested(HoneypotsSchema), required=True, load_only=True)
    sensor_id = ma.Integer(required=True)
    status = ma.Boolean(required=False)
    created_at = ma.DateTime(required=False)
    updated_at = ma.DateTime(required=False)
