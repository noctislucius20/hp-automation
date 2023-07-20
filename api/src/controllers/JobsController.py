import asyncio
from flask import Blueprint, make_response, request
from src.errors.ClientError import ClientError
from src.services.JobsService import JobsService
from src.tokenize.TokenManager import token_required


jobs = Blueprint('jobs', __name__)

@jobs.route('/jobs', methods=['POST'])
def run_jobs():
   data = request.get_json()
   try:
      token_required()

      jobs_service = JobsService()
      jobs_service.add_host(ip_address=data.get('ip_address'))
      jobs_service.run_job(sensor_id=data.get('sensor_id'), ip_address=data.get('ip_address'), honeypot=data.get('honeypot'), name=data.get('name'), dashboard_id='', method='POST')
      
      response = make_response({'status': 'success', 'message': 'job started'}, 200)
      return response

   except ClientError as e:
      response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
      return response

   except:
      #server error 
      response = make_response({'status': 'error', 'message': 'server fail'}, 500)
      return response
   
@jobs.route('/jobs', methods=['PUT'])
def update_jobs():
   data = request.get_json()
   try:
      token_required()

      jobs_service = JobsService()
      jobs_service.update_host(ip_address=data.get('ip_address'), old_ip_address=data.get('old_ip_address'))
      jobs_service.run_job(sensor_id=data.get('sensor_id'), ip_address=data.get('ip_address'), honeypot=data.get('honeypot'), name=data.get('name'), dashboard_id=data.get('dashboard_id'), method='PUT')
      
      response = make_response({'status': 'success', 'message': 'job updated'}, 200)
      return response 

   except ClientError as e:
      response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
      return response

   except:
      #server error 
      response = make_response({'status': 'error', 'message': 'server fail'}, 500)
      return response

# @jobs.route('/jobs', methods=['GET'])
# def get_jobs():
#    data = request.get_json()
#    try:
#       token_required()

#       jobs_service = JobsService()
#       job_status = jobs_service.get_job_status(latest_job=data.get('latest_job'))
      
#       response = make_response({'status': 'success', 'message': 'jobs retrieved', 'job_status': job_status}, 200)
#       return response 

#    except ClientError as e:
#       response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
#       return response

#    except:
#       #server error 
#       response = make_response({'status': 'error', 'message': 'server fail'}, 500)
#       return response

@jobs.route('/jobs/logs', methods=['GET'])
def get_job_log():
   data = request.get_json()
   try:

      jobs_service = JobsService()
      job_logs = asyncio.run(jobs_service.get_log(workflow_job_id=data.get('workflow_job_id')))
      
      response = make_response({'status': 'success', 'message': 'job logs retrieved', 'finished':job_logs['finished'], 'data': job_logs['logs']}, 200)
      return response 

   except ClientError as e:
      response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
      return response

   except:
      #server error 
      response = make_response({'status': 'error', 'message': 'server fail'}, 500)
      return response
   
@jobs.route('/jobs/relaunch', methods=['POST'])
def relaunch_job():
   data = request.get_json()
   try:
      token_required()

      jobs_service = JobsService()
      jobs_service.relaunch_job(workflow_job_id=data.get('workflow_job_id'), sensor_id=data.get('sensor_id'))
      
      response = make_response({'status': 'success', 'message': 'job relaunched'}, 200)
      return response 

   except ClientError as e:
      response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
      return response

   except:
      #server error 
      response = make_response({'status': 'error', 'message': 'server fail'}, 500)
      return response
   
@jobs.route('/jobs/cancel', methods=['POST'])
def cancel_job():
   data = request.get_json()
   try:
      token_required()

      jobs_service = JobsService()
      jobs_service.cancel_job(workflow_job_id=data.get('workflow_job_id'))
      
      response = make_response({'status': 'success', 'message': 'job cancelled'}, 200)
      return response 

   except ClientError as e:
      response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
      return response

   except:
      #server error 
      response = make_response({'status': 'error', 'message': 'server fail'}, 500)
      return response