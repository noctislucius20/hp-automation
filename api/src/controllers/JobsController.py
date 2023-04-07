from flask import Blueprint, make_response, request
from src.errors.ClientError import ClientError
from src.services.JobsService import JobsService
from src.tokenize.TokenManager import token_required


jobs = Blueprint('jobs', __name__)

@jobs.route('/jobs', methods=['POST'])
@token_required
def run_jobs():
   data = request.get_json()
   try:
      jobs_service = JobsService()
      jobs_service.add_host(ip_address=data.get('ip_address'))
      jobs_service.run_starter_job(ip_address=data.get('ip_address'), honeypot=data.get('honeypot'))
      
      response = make_response({'status': 'success', 'message': 'job started'})
      response.status_code = 200
      response.headers['Content-Type'] = 'application/json'
      return response 

   except ClientError as e:
      response = make_response({'status': 'error', 'message': e.args[0]})
      response.status_code = e.status_code
      response.headers['Content-Type'] = 'application/json'
      return response

   except:
      #server error 
      response = make_response({'status': 'error', 'message': 'server fail'})
      response.status_code = 500
      response.headers['Content-Type'] = 'application/json'
      return response
