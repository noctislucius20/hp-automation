from src.models.HoneypotsModel import Honeypots as HoneypotsModel
from src.schemas.HoneypotsSchema import Honeypots as HoneypotsSchema
from src import db
from src.errors.InvariantError import InvariantError

import datetime as dt

class HoneypotsService:
    def add_honeypot(self, name):
        new_honeypot = HoneypotsModel(name = name, status = True, created_at = dt.datetime.now(), updated_at = dt.datetime.now())

        db.session.add(new_honeypot)
        db.session.commit()

        honeypot_schema = HoneypotsSchema()

        return honeypot_schema.dump(new_honeypot)
        
    def list_all_honeypots(self):
        honeypots = HoneypotsModel.query.filter_by(status=True).all()
        honeypots_schema = HoneypotsSchema(many=True)
        
        return honeypots_schema.dump(honeypots)
    
    def get_one_honeypot(self, name):
        honeypot = HoneypotsModel.query.filter_by(name=name, status=True).first()
        honeypot_schema = HoneypotsSchema()

        if not honeypot:
            raise InvariantError(message="honeypot not exist")

        return honeypot_schema.dump(honeypot)

    def edit_honeypot(self, name, new_name):
        honeypot = HoneypotsModel.query.filter_by(name=name, status=True).first()

        if not honeypot:
            raise InvariantError(message="honeypot not exist")
        
        db.session.execute(db.update(HoneypotsModel), {'id': honeypot.id, 'name': new_name, 'updated_at': dt.datetime.now()})
        db.session.commit()

    def delete_honeypot(self, name):
        honeypot = HoneypotsModel.query.filter_by(name=name, status=True).first()

        if not honeypot:
            raise InvariantError(message="honeypot not exist")
        
        honeypot.status = False

        db.session.commit()