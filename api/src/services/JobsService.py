from src.errors.InvariantError import InvariantError

import os
import json
import requests
import asyncio

class JobsService:    
    def __init__(self):
        self.awx_url = os.getenv('AWX_BASE_URL')
        self.awx_token = os.getenv('AWX_ACCESS_TOKEN')
        self.awx_inventory_id = os.getenv('AWX_INVENTORY_ID')
        self.awx_workflow_job_id = os.getenv('AWX_WORKFLOW_JOB_TEMPLATE_ID')
        self.awx_url_header = {
            'Authorization': f'Bearer {self.awx_token}',
            'Content-Type': 'application/json'
        }
 
    def add_host(self, ip_address):      
        host_var = {
            'ansible_user': '{{ honeypot_user }}',
            'ansible_become_pass': '{{ honeypot_pass }}'
        }

        payload = {
            'name': ip_address,
            'description': 'honeypot',
            'variables': str(host_var)
        }

        response = requests.post(url=(self.awx_url + f'/inventories/{self.awx_inventory_id}/hosts/'), headers=self.awx_url_header, data=json.dumps(payload))

        print(json.dumps(response.json()))

        # if response.status_code != 201:
        #     raise InvariantError(message=str(response.json()))
        
    def run_starter_job(self, ip_address, honeypot):
        hp_list = [hp['name'].lower() for hp in honeypot if hp['status']]

        extra_vars = {
            'ip_address': ip_address,
            'hp_list': ', '.join(hp_list)
        }

        payload = {
            'extra_vars': str(extra_vars)
        }

        response = requests.post(url=(self.awx_url + f'/workflow_job_templates/{self.awx_workflow_job_id}/launch/'), headers=self.awx_url_header, data=json.dumps(payload))
        
        print(json.dumps(response.json()))     
    
    # async def run_deploy_honeypot_job(self, honeypot):
    #     try:
    #         job_map = {
    #             'cowrie': 'AWX_JOB_TEMPLATE_COWRIE_ID',
    #             'dionaea': 'AWX_JOB_TEMPLATE_DIONAEA_ID',
    #             'honeytrap': 'AWX_JOB_TEMPLATE_HONEYTRAP_ID',
    #             'rdpy': 'AWX_JOB_TEMPLATE_RDPY_ID',
    #             'elasticpot': 'AWX_JOB_TEMPLATE_ELASTICPOT_ID',
    #             'gridpot': 'AWX_JOB_TEMPLATE_GRIDPOT_ID'
    #         }

    #         for hp in honeypot:
    #             hp_lower = hp['name'].lower()
    #             if hp_lower in job_map and hp['status'] == True:
    #                 job_template = os.getenv(job_map[hp_lower])
    #                 response = requests.post(url=(self.awx_url + f'/job_templates/{job_template}/launch/'), headers=self.awx_url_header)

    #                 print(response.json())

    #     except Exception as e:
    #         raise e
        


