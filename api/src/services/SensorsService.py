from src.models.SensorsModel import Sensors as SensorsModel
from src.schemas.SensorsSchema import Sensors as SensorsSchema
from src import db
from src.errors.InvariantError import InvariantError

import datetime as dt
import json

class SensorsService:
    def add_sensor(self, description, ip_address):
        check_sensor = SensorsModel.query.filter_by(ip_address = ip_address).first()

        sensor_schema = SensorsSchema()

        if not check_sensor:
            new_sensor = SensorsModel(description = description, ip_address = ip_address, status = True, created_at = dt.datetime.now(), updated_at = dt.datetime.now())

            db.session.add(new_sensor)
            db.session.commit()
            return sensor_schema.dump(new_sensor)

        if check_sensor.status == False:
            check_sensor.status = True
            check_sensor.created_at = dt.datetime.now()
            check_sensor.updated_at = dt.datetime.now()

            db.session.commit()
            return sensor_schema.dump(check_sensor)
      
        else:
            raise InvariantError(message="sensor already exist")
        
    def list_all_sensors(self):
        sensors = SensorsModel.query.filter_by(status=True).all()

        sensors_schema = SensorsSchema(many=True)
        
        return sensors_schema.dump(sensors)
    
    def get_one_sensor(self, id):
        sensor = self.check_sensor_exists(id)

        sensor_schema = SensorsSchema()

        return sensor_schema.dump(sensor)

    def edit_sensor(self, id, description, ip_address):
        sensor = self.check_sensor_exists(id)

        if not sensor.ip_address != ip_address:
            db.session.execute(db.update(SensorsModel), {'id': sensor.id, 'description': description, 'updated_at': dt.datetime.now()})
            db.session.commit()
            return 0
        
        check_sensor = SensorsModel.query.filter_by(ip_address = ip_address).first()

        if check_sensor:
            raise InvariantError(message="sensor already exist")
        
        db.session.execute(db.update(SensorsModel), {'id': sensor.id, 'description': description, 'ip_address': ip_address, 'updated_at': dt.datetime.now()})
        db.session.commit()
     
    def delete_sensor(self, id):
        sensor = self.check_sensor_exists(id)
        sensor.status = False

        db.session.commit()
    
    def check_sensor_exists(self, id):
        sensor = SensorsModel.query.filter_by(id=id, status=True).first()
        
        if not sensor:
            raise InvariantError(message="sensor not exist")
        
        return sensor