from src import ma
from flask_marshmallow import exceptions
from src.schemas.HoneypotsSchema import Honeypots as HoneypotsSchema
import ipaddress

def validate_ipv4(ip):
    try:
        ipaddress.ip_address(ip)
    except:
        raise exceptions.ValidationError('Invalid IP address.')

class Sensors(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
        
    id = ma.Integer(required = False)
    ip_address = ma.String(validate = validate_ipv4, required=True)
    name = ma.String(required=False)
    description = ma.String(required=False)
    deployment_status = ma.String(required=False)
    finished_at = ma.DateTime(required=False)
    dashboard_url = ma.String(required=False)
    status = ma.Boolean(required=False)
    created_at = ma.DateTime(required=False)
    updated_at = ma.DateTime(required=False)
    honeypot = ma.List(ma.Nested(HoneypotsSchema), required=True, load_only=True)