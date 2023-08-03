from flask import request
from src.models.SensorsModel import Sensors as SensorsModel
from src.schemas.SensorsSchema import Sensors as SensorsSchema
from src import db
from src.errors.InvariantError import InvariantError
from src.models.HoneypotsModel import Honeypots as HoneypotsModel
from src.models.HoneypotSensorModel import HoneypotSensor as HoneypotSensorModel
from src.models.JobLogsModel import JobLogs as JobLogsModel
from src.models.SensorDashboardsModel import SensorDashboards as SensorDashboardsModel

import datetime as dt
import json
import aiohttp
import os
import requests

class SensorsService:
    def __init__(self):
        self.awx_url = os.getenv('AWX_BASE_URL')
        self.awx_token = os.getenv('AWX_ACCESS_TOKEN')
        self.awx_inventory_id = os.getenv('AWX_INVENTORY_ID')
        self.awx_workflow_job_id = os.getenv('AWX_WORKFLOW_JOB_TEMPLATE_ID')
        self.awx_url_header = {
            'Authorization': f'Bearer {self.awx_token}',
            'Content-Type': 'application/json'
        }
        self.kibana_url = os.getenv('KIBANA_BASE_URL')
        self.kibana_url_header = {
            'kbn-xsrf': 'true',
            'Content-Type': 'application/json'
        }
 
    def add_sensor(self, description, ip_address, honeypot, name, callback):
        sensor_schema = SensorsSchema()

        try:
            db.session.begin()

            check_sensor = SensorsModel.query.filter_by(ip_address = ip_address, status = True).first()

            if check_sensor:
                raise InvariantError(message="sensor already exist")

            new_sensor = SensorsModel(name = name, description = description, ip_address = ip_address, status = True, created_at = dt.datetime.now(), updated_at = dt.datetime.now())

            db.session.add(new_sensor)
            db.session.commit()
            
            callback(honeypot = honeypot, sensor_id = new_sensor.id, ip_address = ip_address, name = name)

            return sensor_schema.dump(new_sensor)

        except Exception as e:
            db.session.rollback()
            db.session.delete(new_sensor)
            db.session.commit()
            raise e
        
        finally:
            db.session.close()
                 
    async def list_all_sensors(self):
        sensors = (
            db.session.query(JobLogsModel.job_id, SensorsModel)
            .join(SensorsModel, JobLogsModel.sensor_id == SensorsModel.id)
            .filter(SensorsModel.status == True)
            .order_by(db.desc(JobLogsModel.created_at))
            .all()
        )

        results = []
        async with aiohttp.ClientSession() as session:
            for job_id, sensor in sensors:
                response = await session.get(f'{self.awx_url}/workflow_jobs/{job_id}/', headers=self.awx_url_header)
                job_list = {
                    'deployment_status': json.loads(await response.text())['status'],
                    'finished_at': dt.datetime.strptime(json.loads(await response.text())['finished'], '%Y-%m-%dT%H:%M:%S.%fZ') if json.loads(await response.text())['finished'] else None
                }
                sensor_schema = SensorsSchema()
                sensor_data = sensor_schema.dump(sensor)
                sensor_data['job_history'] = job_list

                results.append(sensor_data)
        
        return results
    
    async def get_one_sensor(self, id):
        sensor = self.check_sensor_exists(id)

        honeypot_info = (
            db.session
            .query(HoneypotsModel.id, HoneypotsModel.name)
            .join(HoneypotSensorModel)
            .join(SensorsModel)
            .filter(SensorsModel.id == sensor.id)
            .all()
        )

        query_job_history = (
            db.session
            .query(JobLogsModel.job_id, SensorsModel)
            .join(SensorsModel, JobLogsModel.sensor_id == SensorsModel.id)
            .filter(SensorsModel.id == sensor.id)
            .order_by(db.desc(JobLogsModel.created_at))
            .all()
        )

        dashbooard_url = (
            db.session
            .query(SensorDashboardsModel.dashboard_url)
            .filter(SensorDashboardsModel.sensor_id == sensor.id)
            .first()
        )

        job_history = []
        async with aiohttp.ClientSession() as session:
            for job_id, sensor in query_job_history:
                response = await session.get(f'{self.awx_url}/workflow_jobs/{job_id}/', headers=self.awx_url_header)
                job_list = {
                    'deployment_status': json.loads(await response.text())['status'],
                    'finished_at': dt.datetime.strptime(json.loads(await response.text())['finished'], '%Y-%m-%dT%H:%M:%S.%fZ') if json.loads(await response.text())['finished'] else None
                }
                job_history.append(job_list)

        honeypots = [{ 'id': id_, 'name': name} for id_, name in honeypot_info]  
            
        sensor_schema = SensorsSchema()
        sensor_data = sensor_schema.dump(sensor)
        sensor_data['honeypot'] = honeypots
        sensor_data['job_history'] = job_history
        sensor_data['dashboard_url'] = f'{self.kibana_url}{dashbooard_url[0]}' if dashbooard_url else '#'

        return sensor_data

    def edit_sensor(self, id, description, ip_address, name, honeypot, callback):
        try:
            db.session.begin()

            sensor = self.check_sensor_exists(id)

            old_ip_address = sensor.ip_address

            check_sensor = SensorsModel.query.filter_by(ip_address = ip_address, status = True).first()

            if check_sensor is not None and check_sensor.id != sensor.id:
                raise InvariantError(message="sensor already exist")
            
            dashboard_id = (
                db.session
                .query(SensorDashboardsModel.dashboard_id)
                .filter(SensorDashboardsModel.sensor_id == sensor.id)
                .first()
            )

            db.session.execute(db.update(SensorsModel).values({'name': name, 'description': description, 'ip_address': ip_address, 'updated_at': dt.datetime.now()}).where(SensorsModel.id == sensor.id))

            db.session.commit()
            callback(honeypot = honeypot, sensor_id = id, ip_address = ip_address, old_ip_address = old_ip_address, dashboard_id = dashboard_id[0] if dashboard_id else '', name = name)

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

            token = request.headers.get('Authorization')
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = os.getenv("SERVER_URL")
            response = requests.delete(f'{url}/honeypotsensor/{sensor.id}', headers=headers)

            if response.status_code == 500:
                raise Exception("server fail")
            
            # Delete host from AWX
            host_id = requests.get(url=(self.awx_url + f'/inventories/{self.awx_inventory_id}/hosts/?name={sensor.ip_address}'), headers=self.awx_url_header)

            payload = {
                'id': host_id.json()["results"][0]["id"],
                'disassociate': True
            }

            del_host = requests.post(url=(self.awx_url + f'/inventories/{self.awx_inventory_id}/hosts/'), headers=self.awx_url_header, json=payload)

            if del_host.status_code == 500:
                raise Exception("server fail")
            
            dashboard_id = (
                db.session
                .query(SensorDashboardsModel.dashboard_id)
                .filter(SensorDashboardsModel.sensor_id == sensor.id)
                .first()
            )

            # Delete kibana dashboard
            if dashboard_id:
                delete_dashboard = requests.delete(url=(self.kibana_url + f'/api/saved_objects/dashboard/{dashboard_id[0]}'), headers=self.kibana_url_header)
                if delete_dashboard.status_code == 500:
                    raise Exception("server fail")
                
                db.session.execute(db.delete(SensorDashboardsModel)
                                     .where(SensorDashboardsModel.sensor_id == sensor.id))

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e
        
        finally:
            db.session.close()

    def check_sensor_exists(self, id):
        sensor = SensorsModel.query.filter_by(id=id, status=True).first()
        
        if not sensor:
            raise InvariantError(message="sensor not exist")
        
        return sensor
    
    def execute_init_job(self, honeypot, sensor_id, ip_address, name):
        try:
            token = request.headers.get('Authorization')

            honeypotsensor_payload = {
                'sensor_id': sensor_id, 
                'honeypot': honeypot
            }
            job_payload = {
                'sensor_id': sensor_id,
                'ip_address': ip_address, 
                'honeypot': honeypot,
                'name': name
            }

            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = os.getenv("SERVER_URL")

            job_request = requests.post(f'{url}/ansible/jobs', json=job_payload, headers=headers)

            if job_request.status_code == 500:
                raise Exception("server fail")
            
            honeypot_request = requests.post(f'{url}/honeypotsensor', json=honeypotsensor_payload, headers=headers)
            
            if honeypot_request.status_code == 500:
                raise Exception("server fail")

        except Exception as e:
            raise e

    def execute_update_job(self, honeypot, sensor_id, ip_address, old_ip_address, dashboard_id, name):
        try:
            token = request.headers.get('Authorization')

            honeypotsensor_payload = {
                'sensor_id': sensor_id, 
                'honeypot': honeypot
            }
            job_payload = {
                'sensor_id': sensor_id,
                'ip_address': ip_address,
                'old_ip_address': old_ip_address, 
                'name': name,
                'dashboard_id': dashboard_id,
                'honeypot': honeypot
            }

            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = os.getenv("SERVER_URL")

            job_request = requests.put(f'{url}/ansible/jobs', json=job_payload, headers=headers)

            if job_request.status_code == 500:
                raise Exception("server fail")
            
            honeypot_request = requests.put(f'{url}/honeypotsensor', json=honeypotsensor_payload, headers=headers)
            
            if honeypot_request.status_code == 500:
                raise Exception("server fail")

        except Exception as e:
            raise e
        
    def get_logs(self, id):
        try:
            sensor = self.check_sensor_exists(id)
            latest_job = JobLogsModel.query.filter_by(sensor_id = sensor.id).order_by(db.desc(JobLogsModel.created_at)).first()
            
            token = request.headers.get('Authorization')

            host_payload = {
                'workflow_job_id': latest_job.job_id
            }

            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = os.getenv("SERVER_URL")

            response = requests.get(f'{url}/ansible/jobs/logs', json=host_payload, headers=headers, stream=True)

            if response.status_code == 500:
                raise Exception("server fail")
            
            modified_log = response.json()['data'].replace("monospace;", "monospace; \n  white-space: pre-wrap;").replace("body.ansi_back ", "").replace("font-size: 12px;", "")

            return {'finished': response.json()['finished'], 'data': modified_log }

        except Exception as e:
            raise e
        
    def relaunch_job(self, id):
        try:
            sensor = self.check_sensor_exists(id)
            latest_job = JobLogsModel.query.filter_by(sensor_id = sensor.id).order_by(db.desc(JobLogsModel.created_at)).first()
            
            token = request.headers.get('Authorization')

            host_payload = {
                'sensor_id': sensor.id,
                'workflow_job_id': latest_job.job_id
            }

            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = os.getenv("SERVER_URL")

            response = requests.post(f'{url}/ansible/jobs/relaunch', json=host_payload, headers=headers)

            if response.status_code == 500:
                raise Exception("server fail")

        except Exception as e:
            raise e
        
    def cancel_job(self, id):
        try:
            sensor = self.check_sensor_exists(id)
            latest_job = JobLogsModel.query.filter_by(sensor_id = sensor.id).order_by(db.desc(JobLogsModel.created_at)).first()
            
            token = request.headers.get('Authorization')

            host_payload = {
                'workflow_job_id': latest_job.job_id
            }

            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = os.getenv("SERVER_URL")

            response = requests.post(f'{url}/ansible/jobs/cancel', json=host_payload, headers=headers)

            if response.status_code == 500:
                raise Exception("server fail")

        except Exception as e:
            raise e