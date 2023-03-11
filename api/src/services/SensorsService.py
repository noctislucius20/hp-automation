from src.models.SensorsModel import Sensors as SensorsModel
from src.schemas.SensorsSchema import Sensors as SensorsSchema
from src import db
from src.exceptions.InvariantError import InvariantError

import datetime as dt

class SensorsService:
    def add_sensor(self, name, ip_address, state):
        new_sensor = SensorsModel(name = name, ip_address = ip_address, state = state, status = True, created_at = dt.datetime.now(), updated_at = dt.datetime.now())

        db.session.add(new_sensor)
        db.session.commit()

        sensor_schema = SensorsSchema()

        return sensor_schema.dump(new_sensor)
        
    def list_all_sensors(self):
        sensors = SensorsModel.query.filter_by(status=True).all()
        sensors_schema = SensorsSchema(many=True)
        
        return sensors_schema.dump(sensors)
    
    def get_one_sensor(self, name):
        sensor = SensorsModel.query.filter_by(name=name, status=True).first()
        sensor_schema = SensorsSchema()

        if not sensor:
            raise InvariantError(message="sensor not exist")

        return sensor_schema.dump(sensor)

    def edit_sensor(self, name, ip_address, state, new_name):
        sensor = SensorsModel.query.filter_by(name=name, status=True).first()

        if not sensor:
            raise InvariantError(message="sensor not exist")
        
        db.session.execute(db.update(SensorsModel), {'id': sensor.id, 'name': new_name, 'ip_address': ip_address, 'state': state, 'updated_at': dt.datetime.now()})
        db.session.commit()

    def delete_sensor(self, name):
        sensor = SensorsModel.query.filter_by(name=name, status=True).first()

        if not sensor:
            raise InvariantError(message="sensor not exist")
        
        sensor.status = False

        db.session.commit()

    # def check_sensor_existed(self, name):
    #     sensor = SensorsModel.query.filter_by(sensorname=name, status=True).first()

    #     if sensor:
    #         raise InvariantError(message="sensor already exists")