from src.models.HoneypotsModel import Honeypots as HoneypotsModel
from src.schemas.HoneypotsSchema import Honeypots as HoneypotsSchema
from src import db
from src.errors.InvariantError import InvariantError

import datetime as dt

class HoneypotsService:
    def add_honeypot(self, name, description):
        honeypot_schema = HoneypotsSchema()
        try:
            db.session.begin()

            check_honeypot = HoneypotsModel.query.filter_by(name = name, status = True).first()
    
            if check_honeypot:
                raise InvariantError(message="honeypot already exist")

            new_honeypot = HoneypotsModel(name = name, description = description, status = True, created_at = dt.datetime.now(), updated_at = dt.datetime.now())
        
            db.session.add(new_honeypot)
            db.session.commit()

            return honeypot_schema.dump(new_honeypot)
        
        except Exception as e:
            db.session.rollback()
            raise e
        
        finally:
            db.session.close()

    def list_all_honeypots(self):
        honeypots = HoneypotsModel.query.filter_by(status=True).all()

        honeypots_schema = HoneypotsSchema(many=True)
        
        return honeypots_schema.dump(honeypots)
    
    def get_one_honeypot(self, id):
        honeypot = self.check_honeypot_exists(id)

        honeypot_schema = HoneypotsSchema()

        return honeypot_schema.dump(honeypot)

    def edit_honeypot(self, id, name, description):
        try: 
            db.session.begin()
            
            honeypot = self.check_honeypot_exists(id)

            check_honeypot = HoneypotsModel.query.filter_by(name = name, status = True).first()

            if check_honeypot is not None and check_honeypot.id != honeypot.id:
                raise InvariantError(message="honeypot already exist")

            db.session.execute(db.update(HoneypotsModel).values({'name': name, 'description': description, 'updated_at': dt.datetime.now()}).where(HoneypotsModel.id == honeypot.id))

            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            raise e
        
        finally:
            db.session.close()
            
    def delete_honeypot(self, id):
        try:
            db.session.begin()

            honeypot = self.check_honeypot_exists(id)

            db.session.execute(db.update(HoneypotsModel).values({'status': False, 'updated_at': dt.datetime.now()}).where(HoneypotsModel.id == honeypot.id))

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e
        
        finally:
            db.session.close()

    def check_honeypot_exists(self, id):
        honeypot = HoneypotsModel.query.filter_by(id=id, status=True).first()
        
        if not honeypot:
            raise InvariantError(message="honeypot not exist")
        
        return honeypot