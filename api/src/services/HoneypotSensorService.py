from src.models.HoneypotSensorModel import HoneypotSensor as HoneypotSensorModel
from src.schemas.HoneypotSensorSchema import HoneypotSensor as HoneypotSensorSchema
from src import db
from src.errors.InvariantError import InvariantError

import datetime as dt

class HoneypotSensorService:
    def add_honeypotsensor(self, honeypot_id, sensor_id):
        new_honeypotsensor = HoneypotSensorModel(honeypot_id = honeypot_id, sensor_id = sensor_id, status = True, created_at = dt.datetime.now(), updated_at = dt.datetime.now())

        db.session.add(new_honeypotsensor)
        db.session.commit()

        honeypotsensor_schema = HoneypotSensorSchema()

        return honeypotsensor_schema.dump(new_honeypotsensor)

    def delete_honeypotsensor(self, honeypot_id, sensor_id):
        honeypotsensor = HoneypotSensorModel.query.filter_by(honeypot_id = honeypot_id, sensor_id = sensor_id, status=True).first()

        if not honeypotsensor:
            raise InvariantError(message="honeypotsensor not exist")
        
        honeypotsensor.status = False

        db.session.commit()