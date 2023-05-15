from src.models.HoneypotSensorModel import HoneypotSensor as HoneypotSensorModel
from src.schemas.HoneypotSensorSchema import GetHoneypotSensor as GetHoneypotSensorSchema
from src import db
from src.errors.InvariantError import InvariantError


import os
import requests
import datetime as dt
import json

class HoneypotSensorService:
    def add_honeypotsensor(self, honeypot, sensor_id):
        # Check if any honeypot sensors already exist for this sensor ID
        if HoneypotSensorModel.query.filter_by(sensor_id=sensor_id).first() is not None:
            raise InvariantError(message='Honeypot sensor already exists')
        
        # Create new honeypot sensor instances and add them to the database
        honeypot_sensor = [HoneypotSensorModel(honeypot_id=hp['id'], sensor_id=sensor_id, created_at=dt.datetime.now(), updated_at=dt.datetime.now()) for hp in honeypot]
        db.session.bulk_save_objects(honeypot_sensor)
        db.session.commit()
        
        # Retrieve the newly created honeypot sensor instances and return them as JSON
        result = HoneypotSensorModel.query.filter_by(sensor_id=sensor_id).all()
        return GetHoneypotSensorSchema().dump(result)

    def update_honeypotsensor(self, honeypot, sensor_id):
        # Get existing honeypot sensors for this sensor_id
        existing_sensors = HoneypotSensorModel.query.filter_by(sensor_id=sensor_id).all()
        
        # Keep track of ids that should remain after updating
        new_ids = set(hp['id'] for hp in honeypot)
        existing_ids = set(hs.honeypot_id for hs in existing_sensors)
        ids_to_keep = new_ids.intersection(existing_ids)
        
        # Remove instances that are no longer needed
        for sensor in existing_sensors:
            if sensor.honeypot_id not in ids_to_keep:
                db.session.delete(sensor)
        
        # Add new sensors
        honeypot_sensor = [HoneypotSensorModel(honeypot_id=hp['id'], sensor_id=sensor_id, created_at=dt.datetime.now(), updated_at=dt.datetime.now()) for hp in honeypot]
        
        try:
            db.session.bulk_save_objects(honeypot_sensor)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception("Failed to save honeypot sensors.")

    def delete_honeypotsensor(self, id):
        honeypotsensor = HoneypotSensorModel.query.filter_by(id = id).first()

        if not honeypotsensor:
            raise InvariantError(message="honeypotsensor not exist")

        HoneypotSensorModel.query.filter_by(honeypot_id = honeypotsensor.honeypot_id).delete()

        db.session.commit()

        