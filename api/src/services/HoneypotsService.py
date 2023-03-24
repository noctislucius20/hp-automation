from src.models.HoneypotsModel import Honeypots as HoneypotsModel
from src.schemas.HoneypotsSchema import Honeypots as HoneypotsSchema
from src import db
from src.errors.InvariantError import InvariantError

import datetime as dt

class HoneypotsService:
    def add_honeypot(self, name):
        check_honeypot = HoneypotsModel.query.filter_by(name = name).first()

        honeypot_schema = HoneypotsSchema()

        if not check_honeypot:
            new_honeypot = HoneypotsModel(name = name, status = True, created_at = dt.datetime.now(), updated_at = dt.datetime.now())

            db.session.add(new_honeypot)
            db.session.commit()

            return honeypot_schema.dump(new_honeypot)

        if check_honeypot.status == False:
            check_honeypot.status = True
            check_honeypot.created_at = dt.datetime.now()
            check_honeypot.updated_at = dt.datetime.now()

            db.session.commit()

            return honeypot_schema.dump(check_honeypot)
      
        else:
            raise InvariantError(message="honeypot already exist")
        
    def list_all_honeypots(self):
        honeypots = HoneypotsModel.query.filter_by(status=True).all()

        honeypots_schema = HoneypotsSchema(many=True)
        
        return honeypots_schema.dump(honeypots)
    
    def get_one_honeypot(self, id):
        honeypot = self.check_honeypot_exists(id)

        honeypot_schema = HoneypotsSchema()

        return honeypot_schema.dump(honeypot)

    def edit_honeypot(self, id, name):
        honeypot = self.check_honeypot_exists(id)

        if not honeypot.name != name:
            return 0
        
        check_honeypot = HoneypotsModel.query.filter_by(name = name).first()

        if check_honeypot:
            raise InvariantError(message="honeypot already exist")
        
        db.session.execute(db.update(HoneypotsModel), {'id': honeypot.id, 'name': name, 'updated_at': dt.datetime.now()})
        db.session.commit()

    def delete_honeypot(self, id):
        honeypot = self.check_honeypot_exists(id)
        honeypot.status = False

        db.session.commit()

    def check_honeypot_exists(self, id):
        honeypot = HoneypotsModel.query.filter_by(id=id, status=True).first()
        
        if not honeypot:
            raise InvariantError(message="honeypot not exist")
        
        return honeypot