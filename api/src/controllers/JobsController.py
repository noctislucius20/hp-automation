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
      jobs_service.run_job(ip_address=data.get('ip_address'), honeypot=data.get('honeypot'))
      
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
      jobs_service.run_job(ip_address=data.get('ip_address'), honeypot=data.get('honeypot'))
      
      response = make_response({'status': 'success', 'message': 'job updated'}, 200)
      return response 

   except ClientError as e:
      response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
      return response

   except:
      #server error 
      response = make_response({'status': 'error', 'message': 'server fail'}, 500)
      return response

@jobs.route('/jobs/logs', methods=['GET'])
def get_job_log():
   data = request.get_json()
   try:

      jobs_service = JobsService()
      job_logs = jobs_service.get_log(ip_address=data.get('ip_address'))
      
      response = make_response({'status': 'success', 'message': 'job logs retrieved', 'data': job_logs}, 200)
      return response 

   except ClientError as e:
      response = make_response({'status': 'error', 'message': e.args[0]}, e.status_code)
      return response

   except:
      #server error 
      response = make_response({'status': 'error', 'message': 'server fail'}, 500)
      return response