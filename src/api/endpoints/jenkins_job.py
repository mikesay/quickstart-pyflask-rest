# -*- coding: UTF-8 -*-
from flask_restplus import Resource
from flask import request
from api.serializers import api_jobs, api_job
from api.parsers import get_jobs_arguments
from api.restplus import api, error_handler
from utils.common_utils import LogUtil
from service import jenkins_job_svc

logger = LogUtil.get_named_logger(__name__)

ns = api.namespace('jobs', description='Manage Jenkins Jobs')

###################################################
# Get jenkins jobs                                #
################################################### 

@ns.route('/<int:job_id>')
@api.response(200, 'Everything is ok!')
@api.response(201, 'Update job successfully!')
@api.response(400, 'Bad request!')
@api.response(404, 'Job not found!')
@api.response(500, 'Server error!')
class JenkinsJob(Resource):
    @ns.doc('Get job by id')
    @api.marshal_with(api_job)
    @error_handler
    def get(self, job_id):
        """
        Get job by id.
        """
        jb_svc = jenkins_job_svc.JenkinsJobSVC()
        return jb_svc.get_job_by_id(job_id), 200

    @ns.doc('Update job')
    @api.expect(api_job, validate=True)
    @error_handler
    def patch(self, job_id):
        """
        Update job.
        """
        data = request.json
        jb_svc = jenkins_job_svc.JenkinsJobSVC()
        jb_svc.update_job(job_id, data)
        return 'Update job successfully', 201

@ns.route('')
@api.response(200, 'Everything is ok!')
@api.response(400, 'Bad request!')
@api.response(404, 'Not found!')
@api.response(500, 'Server error!')
class JenkinsJobCollection(Resource):
    @ns.doc('Get all jobs')
    @api.marshal_with(api_jobs)
    @error_handler
    def get(self):
        """
        Get all jobs.
        jobs?page=1&per_page=50&display=true&job_type=ci
        """
        args = get_jobs_arguments.parse_args()
        
        display = args['display']
        if(display == None):
            display = True

        job_type = args['job_type']
        if(job_type == None):
            job_type = "ci"

        page = args["page"]
        per_page = args["per_page"]
            
        jb_svc = jenkins_job_svc.JenkinsJobSVC()
        return jb_svc.get_jobs(display=display, job_type=job_type, page=page, per_page=per_page), 200

    @ns.doc('Register new job')
    @api.expect(api_job, validate=True)
    @error_handler
    def post(self):
        """
        Register new job.
        """
        data = request.json
        jb_svc = jenkins_job_svc.JenkinsJobSVC()
        job_id = jb_svc.register_new_job(data)
        logger.info("New job with id {} added!".format(job_id))
        return 'Register job successfully', 201
        