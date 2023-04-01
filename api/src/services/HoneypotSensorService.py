from src.models.HoneypotSensorModel import HoneypotSensor as HoneypotSensorModel
from src.schemas.HoneypotSensorSchema import HoneypotSensor as HoneypotSensorSchema
from src import db
from src.errors.InvariantError import InvariantError


import os
import requests
import datetime as dt
import json

class HoneypotSensorService:
    def add_honeypotsensor(self, honeypot, sensor_id):
        check_honeypotsensor = HoneypotSensorModel.query.filter_by(sensor_id = sensor_id).all()

        if check_honeypotsensor:
            raise InvariantError(message='honeypotsensor already exist')
        
        honeypot_sensor = []
        for hp in honeypot:
            honeypot_sensor.append(HoneypotSensorModel(honeypot_id = hp['id'], sensor_id = sensor_id, status = hp['status'], created_at = dt.datetime.now(), updated_at = dt.datetime.now()))

        db.session.bulk_save_objects(honeypot_sensor)
        db.session.commit()

        result = HoneypotSensorModel.query.filter_by(sensor_id = sensor_id).all()
        
        return json.dumps({'data': result})

    def delete_honeypotsensor(self, id):
        honeypotsensor = HoneypotSensorModel.query.filter_by(id = id).first()

        if not honeypotsensor:
            raise InvariantError(message="honeypotsensor not exist")

        HoneypotSensorModel.query.filter_by(honeypot_id = honeypotsensor.honeypot_id).delete()

        db.session.commit()

        