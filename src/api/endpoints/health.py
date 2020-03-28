# -*- coding: UTF-8 -*-
from flask_restplus import Resource
from flask import request
from api.serializers import api_jobs, api_job
from api.parsers import get_jobs_arguments
from api.restplus import api, error_handler
from utils.common_utils import LogUtil
from service import jenkins_job_svc

logger = LogUtil.get_named_logger(__name__)

ns = api.namespace('health', description='Return health status')

###################################################
# Get jenkins jobs                                #
################################################### 

@ns.route('')
@api.response(200, 'Everything is ok!')
@api.response(201, 'Update job successfully!')
@api.response(400, 'Bad request!')
@api.response(404, 'Job not found!')
@api.response(500, 'Server error!')
class Health(Resource):
    @ns.doc('Return health status')
    @error_handler
    def get(self):
        """
        Get health information.
        """
        return "", 200
        