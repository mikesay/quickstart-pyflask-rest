# -*- coding: UTF-8 -*-
'''
Created on Feb 19, 2019

@author: mikezhang
'''
#!/usr/bin/env python
from utils.common_utils import LogUtil, BasicError
from utils.api_error import ServerError, NotFoundError, BadRequestError

logger = LogUtil.get_named_logger(__name__)

class JenkinsJobSVC(object):
    '''
    classdocs
    '''
    def get_jobs(self, page=None, per_page=None, display=True, job_type="ci"):
        try:
            rdata = {'total_count':50, 'page':page, 'per_page':per_page, 'api_job_items':[]}

            for i in range(50):
                item = {
                        'id': i,
                        'name': "{}_{}".format("quickstart-pyflask-rest", i),
                        'job_type': job_type,
                        'display': display
                }

                rdata['api_job_items'].append(item)

            return rdata
        except BasicError:
            raise
        except Exception as err:
            raise ServerError(errormsg=err.message, cause=err)

    def get_job_by_id(self, job_id):
        try:
            return {
                    'id': job_id,
                    'name': "{}_{}".format("quickstart-pyflask-rest", job_id),
                    'job_type': "ci",
                    'display': True
            }

        except BasicError:
            raise
        except Exception as err:
            raise ServerError(errormsg=err.message, cause=err)

    def register_new_job(self, data):
        try:
            job_id = 20
            item = {
                'name': data["name"],
                'job_type': data["job_type"],
                'display': data["display"]
            }

            logger.info("The new job {} with generated id {} and type {} is added".format(item['name'], job_id, item['job_type']))
            return job_id

        except BasicError:
            raise
        except Exception as err:
            raise ServerError(errormsg=err.message, cause=err)

    def update_job(self, job_id, data):
        try:
            item = {
                'name': data["name"],
                'job_type': data["job_type"],
                'display': data["display"]
            }

            logger.info("Job {} with id {} and type {} was updated".format(item['name'], job_id, item['job_type']))

        except BasicError:
            raise
        except Exception as err:
            raise ServerError(errormsg=err.message, cause=err)

if __name__ == '__main__':
    pass