import aiohttp
from src.errors.InvariantError import InvariantError
from src.models.JobLogsModel import JobLogs as JobLogsModel
from src import db
from src import socketio

import os
import json
import requests
import asyncio
import datetime as dt

class JobsService:    
    def __init__(self):
        self.awx_url = os.getenv('AWX_BASE_URL')
        self.awx_token = os.getenv('AWX_ACCESS_TOKEN')
        self.awx_inventory_id = os.getenv('AWX_INVENTORY_ID')
        self.awx_workflow_job_id = os.getenv('AWX_WORKFLOW_JOB_TEMPLATE_ID')
        self.awx_workflow_update_job_id = os.getenv('AWX_WORKFLOW_UPDATE_JOB_TEMPLATE_ID')
        self.awx_url_header = {
            'Authorization': f'Bearer {self.awx_token}',
            'Content-Type': 'application/json'
        }
 
    def add_host(self, ip_address):   
        try:
            host_var = {
                'ansible_user': '{{ sensor_user }}',
                'ansible_become_pass': '{{ sensor_pass }}'
            }
    
            payload = {
                'name': ip_address,
                'description': 'honeypot',
                'variables': str(host_var)
            }
    
            requests.post(url=(self.awx_url + f'/inventories/{self.awx_inventory_id}/hosts/'), headers=self.awx_url_header, data=json.dumps(payload))
    
        except Exception as e:
            raise e

        # if response.status_code != 201:
        #     raise InvariantError(message=str(response.json()))
        

    def update_host(self, ip_address, old_ip_address):
        try:
            host_var = {
                'ansible_user': '{{ honeypot_user }}',
                'ansible_become_pass': '{{ honeypot_pass }}'
            }
    
            payload = {
                'name': ip_address,
                'description': 'honeypot',
                'variables': str(host_var)
            }
            
            host_id = requests.get(url=(self.awx_url + f'/inventories/{self.awx_inventory_id}/hosts/?name={old_ip_address}'), headers=self.awx_url_header)

            requests.put(url=(self.awx_url + f'/hosts/{host_id.json()["results"][0]["id"]}/'), headers=self.awx_url_header, json=payload)
        
        except Exception as e:
            raise e

    def run_job(self, ip_address, honeypot, sensor_id, name, dashboard_id, method):
        try:
            hp_list = [hp['name'].lower() for hp in honeypot]

            extra_vars = {
                'ip_address': ip_address,
                'hp_list': ', '.join(hp_list),
                'sensor_name': name,
                'dashboard_id': dashboard_id,
                'method': method
            }
    
            payload = {
                'extra_vars': str(extra_vars)
            }

            if method == 'POST':
                response = requests.post(url=(self.awx_url + f'/workflow_job_templates/{self.awx_workflow_job_id}/launch/'), headers=self.awx_url_header, data=json.dumps(payload))

            if method == 'PUT':
                response = requests.post(url=(self.awx_url + f'/workflow_job_templates/{self.awx_workflow_update_job_id}/launch/'), headers=self.awx_url_header, data=json.dumps(payload))
            
            job_logs = JobLogsModel(sensor_id=sensor_id, job_id=response.json()['workflow_job'], job_url=(self.awx_url + (f'{response.json()["url"]}').replace('api/v2/', '')), created_at=dt.datetime.now()) 
            db.session.add(job_logs)
            db.session.commit()

            json.dumps(response.json())
            
        except Exception as e:
            raise e

    def relaunch_job(self, workflow_job_id, sensor_id):
        try:
            response = requests.post(url=(self.awx_url + f'/workflow_jobs/{workflow_job_id}/relaunch/'), headers=self.awx_url_header)

            job_logs = JobLogsModel(sensor_id=sensor_id, job_id=response.json()['id'], job_url=(self.awx_url + (f'{response.json()["url"]}').replace('api/v2/', '')), created_at=dt.datetime.now())
            db.session.add(job_logs)
            db.session.commit()

            json.dumps(response.json())
            
        except Exception as e:
            raise e
        
    def cancel_job(self, workflow_job_id):
        try:
            requests.post(url=(self.awx_url + f'/workflow_jobs/{workflow_job_id}/cancel/'), headers=self.awx_url_header)
            
            return 0
        except Exception as e:
            raise e

    # def get_job_status(self, latest_job):
    #     try:
    #         response = requests.get(url=(self.awx_url + f'/workflow_jobs/{latest_job}/'), headers=self.awx_url_header)
    #         return response.json()['status']
        
    #     except Exception as e:
    #         raise e
        
    async def get_log(self, workflow_job_id):
        try:
            check_running = requests.get(url=(self.awx_url + f'/workflow_jobs/{workflow_job_id}/'), headers=self.awx_url_header).json()

            job_list = requests.get(url=(self.awx_url + f'/workflow_jobs/{workflow_job_id}/workflow_nodes/'), headers=self.awx_url_header).json()

            job_ids = sorted([str(job["summary_fields"]["job"]["id"]) for job in job_list['results'] if 'job' in job["summary_fields"]], key=int)

            del job_ids[0]

            results = []
            async with aiohttp.ClientSession() as session:
                for job_id in job_ids:
                    response = await session.get(url=(self.awx_url + f'/jobs/{job_id}/stdout/?format=html'), headers=self.awx_url_header)
                    results.append(await response.text())

            new_result = '<br/><div style="color: #ffae00">=================== End of this step. Start a new job ===================</div><br/>'.join(results)

            # response = requests.get(url=(self.awx_url + f'/jobs/{job_id[-1]}/stdout/?format=html'), headers=self.awx_url_header)
            return {'finished': True if check_running['finished'] is not None else False, 'logs': new_result.replace("#161b1f", "#BEBEBE")}
        
        except Exception as e:
            raise e