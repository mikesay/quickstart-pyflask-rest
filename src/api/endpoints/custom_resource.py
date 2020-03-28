# -*- coding: UTF-8 -*-
'''
Created on Feb 16, 2019

@author: mikezhang
'''
from flask import request
from flask_restplus import Resource
from flask_restplus.model import ModelBase
from utils.api_error import BadRequestError

class CustomResource(Resource):
    def validate_payload(self, func):
        Resource.validate_payload(self, func)

        if getattr(func, '__apidoc__', False) is not False:
            doc = func.__apidoc__
            validate = doc.get('validate', None)
            validate = validate if validate is not None else self.api._validate
            if validate:
                for expect in doc.get('expect', []):
                    # TODO: handle third party handlers
                    if isinstance(expect, list) and len(expect) == 1:
                        if isinstance(expect[0], ModelBase):
                            self._validate(expect[0], collection=True)
                    if isinstance(expect, ModelBase):
                        self._validate(expect, collection=False)
                        
    def _validate(self, expect, collection=False):
        '''
        :param ModelBase expect: the expected model for the input payload
        :param bool collection: False if a single object of a resource is
        expected, True if a collection of objects of a resource is expected.
        '''
        # TODO: proper content negotiation
        data = request.get_json()
        if collection:
            data = data if isinstance(data, list) else [data]
            for obj in data:
                self._validate_key_exist(obj, expect)
        else:
            self._validate_key_exist(data, expect)
            
    def _validate_key_exist(self, data, api_model):
        for key in api_model:
            if api_model[key].required and key not in data:
                raise BadRequestError("Required field {} missing".format(key))

if __name__ == '__main__':
    pass