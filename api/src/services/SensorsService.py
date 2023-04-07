from src.models.SensorsModel import Sensors as SensorsModel
from src.schemas.SensorsSchema import Sensors as SensorsSchema
from src import db
from src.errors.InvariantError import InvariantError

import datetime as dt
import json
import aiohttp
import os
import asyncio

class SensorsService:
    def add_sensor(self, description, ip_address, honeypot, callback):
        check_sensor = SensorsModel.query.filter_by(ip_address = ip_address).first()

        sensor_schema = SensorsSchema()

        if not check_sensor:
            new_sensor = SensorsModel(description = description, ip_address = ip_address, status = True, created_at = dt.datetime.now(), updated_at = dt.datetime.now())

            db.session.add(new_sensor)
            db.session.commit()
    
            result = sensor_schema.dump(new_sensor)

            asyncio.run(callback(honeypot = honeypot, sensor_id = new_sensor.id, ip_address = ip_address))

            return result

        if check_sensor.status == False:
            check_sensor.status = True
            check_sensor.description = description
            check_sensor.created_at = dt.datetime.now()
            check_sensor.updated_at = dt.datetime.now()

            db.session.commit()


            asyncio.run(callback(honeypot, check_sensor.id, ip_address))

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
    
    async def call_api(self, honeypot, sensor_id, ip_address):
        honeypotsensor_payload = {'sensor_id': sensor_id, 'honeypot': honeypot}
        job_payload = {'ip_address': ip_address, 'honeypot': honeypot}
    
        async with aiohttp.ClientSession() as session:
            headers = {'Content-Type': 'application/json'}
            url = os.getenv("SERVER_URL")
            await session.post(url=f'{url}/ansible/jobs', json=job_payload, headers=headers)
            await session.post(url=f'{url}/honeypotsensor', json=honeypotsensor_payload, headers=headers)
