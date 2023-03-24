from src import ma

class Honeypots(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
        
    id = ma.Integer(required=False)
    name = ma.String(required=True)
    status = ma.Boolean(required=False)
    created_at = ma.DateTime(required=False)
    updated_at = ma.DateTime(required=False)
