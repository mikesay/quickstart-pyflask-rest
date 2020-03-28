# -*- coding: UTF-8 -*-
from flask_restplus import reqparse
from flask_restplus.inputs import boolean

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, help='Page number', location='values')
pagination_arguments.add_argument('per_page', type=int, required=False, help='Results per page {error_msg}', location='values')

get_jobs_arguments = pagination_arguments.copy()
get_jobs_arguments.add_argument('display', type=boolean, required=False, help='Get displayed jobs', location='values')
get_jobs_arguments.add_argument('job_type', required=False, help='Get jobs of specified job_type', location='values')