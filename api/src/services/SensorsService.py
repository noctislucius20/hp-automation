from flask import request
from src.models.SensorsModel import Sensors as SensorsModel
from src.schemas.SensorsSchema import Sensors as SensorsSchema
from src import db
from src.errors.InvariantError import InvariantError
from src.models.HoneypotsModel import Honeypots as HoneypotsModel
from src.models.HoneypotSensorModel import HoneypotSensor as HoneypotSensorModel

import datetime as dt
import json
import aiohttp
import os
import asyncio
import requests

class SensorsService:
    def add_sensor(self, description, ip_address, honeypot, name, callback):
        sensor_schema = SensorsSchema()

        try:
            db.session.begin()

            check_sensor = SensorsModel.query.filter_by(ip_address = ip_address, status = True).first()

            if check_sensor:
                raise InvariantError(message="sensor already exist")

            new_sensor = SensorsModel(name = name, description = description, ip_address = ip_address, status = True, created_at = dt.datetime.now(), updated_at = dt.datetime.now())

            db.session.add(new_sensor)
            db.session.flush()
            
            callback(honeypot = honeypot, sensor_id = new_sensor.id, ip_address = ip_address)
            # asyncio.run(callback(honeypot = honeypot, sensor_id = new_sensor.id, ip_address = ip_address))
            return sensor_schema.dump(new_sensor)

        except Exception as e:
            db.session.rollback()
            db.session.delete(new_sensor)
            db.session.commit()
            raise e
        
        finally:
            db.session.close()
                 
    def list_all_sensors(self):
        sensors = SensorsModel.query.filter_by(status=True).all()

        sensors_schema = SensorsSchema(many=True)
        
        return sensors_schema.dump(sensors)
    
    def get_one_sensor(self, id):
        sensor = self.check_sensor_exists(id)

        query = (
            db.session
            .query(HoneypotsModel.id, HoneypotsModel.name)
            .join(HoneypotSensorModel)
            .join(SensorsModel)
            .filter(SensorsModel.id == sensor.id)
        )
        
        honeypot_info = query.all() 
        
        honeypots = [{ 'id': id_, 'name': name} for id_, name in honeypot_info]  
        
        print(honeypots)
        
        sensor_schema = SensorsSchema()
        sensor_data = sensor_schema.dump(sensor)
        sensor_data['honeypot'] = honeypots  

        return sensor_data

    def edit_sensor(self, id, description, ip_address, name, honeypot, callback):
        try:
            db.session.begin()

            sensor = self.check_sensor_exists(id)

            old_ip_address = sensor.ip_address

            check_sensor = SensorsModel.query.filter_by(ip_address = ip_address, status = True).first()

            if check_sensor is not None and check_sensor.id != sensor.id:
                raise InvariantError(message="sensor already exist")

            db.session.execute(db.update(SensorsModel).values({'name': name, 'description': description, 'ip_address': ip_address, 'updated_at': dt.datetime.now()}).where(SensorsModel.id == sensor.id))

            db.session.flush()
            # TODO: run job to update sensor in ansible
            callback(honeypot = honeypot, sensor_id = id, ip_address = ip_address, old_ip_address = old_ip_address)

        except Exception as e:
            db.session.rollback()
            raise e
        
        finally:
            db.session.close()

    def delete_sensor(self, id):
        try:
            db.session.begin()

            sensor = self.check_sensor_exists(id)

            db.session.execute(db.update(SensorsModel).values({'status': False, 'updated_at': dt.datetime.now()}).where(SensorsModel.id == sensor.id))

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e
        
        finally:
            db.session.close()

    def get_logs(self, id):
        try:
            sensor = self.check_sensor_exists(id)
            
            token = request.headers.get('Authorization')

            host_payload = {
                'ip_address': sensor.ip_address
            }

            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = os.getenv("SERVER_URL")

            response = requests.get(f'{url}/ansible/jobs/logs', json=host_payload, headers=headers, stream=True)

            if response.status_code == 500:
                raise Exception("server fail")
            
            new_response = response.text.replace("monospace;", "monospace; \\n  white-space: pre-wrap;").replace("body.ansi_back ", "").replace("font-size: 12px;", "")
            return new_response

        except Exception as e:
            raise e
    
    def check_sensor_exists(self, id):
        sensor = SensorsModel.query.filter_by(id=id, status=True).first()
        
        if not sensor:
            raise InvariantError(message="sensor not exist")
        
        return sensor
    
    def execute_init_job(self, honeypot, sensor_id, ip_address):
        try:
            token = request.headers.get('Authorization')

            honeypotsensor_payload = {
                'sensor_id': sensor_id, 
                'honeypot': honeypot
            }
            job_payload = {
                'ip_address': ip_address, 
                'honeypot': honeypot
            }

            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = os.getenv("SERVER_URL")

            job_request = requests.post(f'{url}/ansible/jobs', json=job_payload, headers=headers)

            if job_request.status_code == 500:
                raise Exception("server fail")
            
            db.session.commit()

            honeypot_request = requests.post(f'{url}/honeypotsensor', json=honeypotsensor_payload, headers=headers)
            
            if honeypot_request.status_code == 500:
                raise Exception("server fail")

        except Exception as e:
            raise e

    def execute_update_job(self, honeypot, sensor_id, ip_address, old_ip_address):
        try:
            token = request.headers.get('Authorization')

            honeypotsensor_payload = {
                'sensor_id': sensor_id, 
                'honeypot': honeypot
            }
            job_payload = {
                'ip_address': ip_address,
                'old_ip_address': old_ip_address, 
                'honeypot': honeypot
            }

            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = os.getenv("SERVER_URL")

            job_request = requests.put(f'{url}/ansible/jobs', json=job_payload, headers=headers)

            if job_request.status_code == 500:
                raise Exception("server fail")
            
            db.session.commit()

            honeypot_request = requests.put(f'{url}/honeypotsensor', json=honeypotsensor_payload, headers=headers)
            
            if honeypot_request.status_code == 500:
                raise Exception("server fail")

        except Exception as e:
            raise e
        
   
        
