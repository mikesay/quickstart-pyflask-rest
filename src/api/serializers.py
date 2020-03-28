# -*- coding: UTF-8 -*-
from flask_restplus import fields
from api.restplus import api

####################################################
# Restful API data model for Compiler Warning info #
####################################################

api_job = api.model('APIJob', {
    'id': fields.Integer(readOnly=True, description='Jenkins job id'),
    'name': fields.String(readOnly=True, description='Jenkins job name'),
    'job_type': fields.String(readOnly=True, required=False, default="ci", description='Jenkins job type: ci,deploy,smoke_test,santity_test,function_test,dynamic_test'),
    'display': fields.Boolean(readOnly=True, required=False, default=True, description='Whether to display job')
})

api_jobs = api.model('APIJobs', {
    'total_count': fields.Integer(readOnly=True, default=0, description='Total job counts'),
    'page': fields.Integer(readOnly=True, default=-1, description='The current page number of jobs'),
    'per_page': fields.Integer(readOnly=True, default=-1, description='Job count of one page'),
    'api_job_items': fields.List(fields.Nested(api_job), readOnly=True, description='Job records')
})
