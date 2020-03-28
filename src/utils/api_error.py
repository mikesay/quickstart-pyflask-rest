# -*- coding: UTF-8 -*-
'''
Created on Feb 14, 2019

@author: mikezhang
'''
#!/usr/bin/env python

from common_utils import BasicError

class BadRequestError(BasicError):
    def __init__(self, errormsg, cause=None):
        BasicError.__init__(self, errormsg=errormsg, cause=cause, errorcode=400)
        
class NotFoundError(BasicError):
    def __init__(self, errormsg, cause=None):
        BasicError.__init__(self, errormsg=errormsg, cause=cause, errorcode=404)

class ServerError(BasicError):
    def __init__(self, errormsg, cause=None):
        BasicError.__init__(self, errormsg=errormsg, cause=cause, errorcode=500)
        