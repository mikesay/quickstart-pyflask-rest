# -*- coding: UTF-8 -*-
import functools
from flask import url_for
from flask_restplus import Api, abort
from utils.common_utils import LogUtil
from utils.api_error import ServerError, BadRequestError, NotFoundError

logger = LogUtil.get_named_logger(__name__)

class Custom_API(Api):
    @property
    def specs_url(self):
        '''
        The Swagger specifications absolute url (ie. `swagger.json`)
        Overwrite the one from Api to set _external value to False, so that it will return relative path.
        
        :rtype: str
        '''
        return url_for(self.endpoint('specs'), _external=False)

api = Custom_API(version='1.0', title='Sample API',
          description='Sample APIs for quickstart project\.')

def error_handler(f):
    @functools.wraps(f)
    def wrapper(*args, **kargs):
        try:
            return f(*args, **kargs)
        except BadRequestError as brerr:
            logger.error(brerr.stack_error)
            abort(400, brerr.stack_error)
        except NotFoundError as nfrerr:
            logger.error(nfrerr.stack_error)
            abort(404, nfrerr.stack_error)
        except ServerError as serr:
            logger.error(serr.stack_error)
            abort(500, serr.stack_error)
        except Exception as err:
            logger.error(err.message)
            abort(500, err.message)
            
    return wrapper