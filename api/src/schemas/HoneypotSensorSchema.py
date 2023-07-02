from src import ma
from src.schemas.HoneypotsSchema import Honeypots as HoneypotsSchema

class PostHoneypotSensor(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
  
    id = ma.Integer(required=False)
    honeypot = ma.List(ma.Nested(HoneypotsSchema), required=True, load_only=True)
    sensor_id = ma.Integer(required=True)
    created_at = ma.DateTime(required=False)
    updated_at = ma.DateTime(required=False)

class GetHoneypotSensor(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
  
    id = ma.Integer(required=True)
    honeypot_id = ma.Integer(required=True)
    sensor_id = ma.Integer(required=True)
    created_at = ma.DateTime(required=False)
    updated_at = ma.DateTime(required=False)

class PutHoneypotSensor(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
  
    id = ma.Integer(required=False)
    honeypot = ma.List(ma.Nested(HoneypotsSchema), required=True, load_only=True)
    sensor_id = ma.Integer(required=True)
    created_at = ma.DateTime(required=False)
    updated_at = ma.DateTime(required=False)