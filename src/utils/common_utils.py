# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
import json
from abc import ABCMeta, abstractmethod
from Crypto.Cipher import AES #@UnresolvedImport
from binascii import b2a_hex, a2b_hex

class BasicError(Exception):
    __metaclass__ = ABCMeta
    def __init__(self, errormsg, cause=None, errorcode=400):
        self._errormsg = errormsg
        self._cause = cause
        self._errorcode = errorcode
    
    def __str__(self):
        return self.stack_error
 
    def __repr__(self):
        return self.stack_error
    
    @property
    def stack_error(self):
        stack_error = ""
        if(self._cause):
            if(isinstance(self._cause, BasicError)):
                stack_error = self._cause.stack_error
            else:
                stack_error = "[Error class]: " + self._cause.__class__.__name__ + \
                            "\n[Error Message]:\n" + str(self._cause)
        
        stack_error = self.error + "\n\nCaused by => \n\n" + stack_error
        return stack_error
         
    @property
    def error(self):
        value = "[Error class]: " + self.__class__.__name__ + \
                "\n[Error Message]:\n" + self._errormsg
        return value
    
    @property
    def error_code(self):
        return self._errorcode

class LogUtil(object):
    @classmethod
    def init_root_logger(cls, log_name="", log_to_file=True, log_to_console=True):
        # create logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if(log_to_console):
            # create console handler and set level to debug
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            
            # add formatter to ch
            ch.setFormatter(formatter)
            
            # add ch to logger
            logger.addHandler(ch)
        
        if(log_to_file):
            # create rotate file handler and set level to debug
            #
            if(not os.path.exists("logs")):
                os.mkdir("logs")
    
            log_fname = "logs" + os.path.sep + "root.log" if log_name == "" else "logs{0}{1}.log".format(os.path.sep, log_name)
            rfh = RotatingFileHandler(log_fname, maxBytes=10485760, backupCount=5)
            rfh.setLevel(logging.DEBUG)
            
            # add formatter to rfh
            rfh.setFormatter(formatter)
            
            # add rfh to logger
            logger.addHandler(rfh)
    
    @classmethod 
    def get_root_logger(cls):
        return logging.getLogger()
    
    @classmethod
    def get_named_logger(cls, name):
        logger = logging.getLogger(name)
        root_logger = LogUtil.get_root_logger()
        if(len(root_logger.handlers) <= 0):
            logger.addHandler(logging.NullHandler())
            
        return logger

logger_name = "utils.common_utils" if __name__ == "__main__" else __name__
logger = LogUtil.get_named_logger(logger_name)

class FileManager(object):
    __metaclass__ = ABCMeta

    def __init__(self, file_path):
        self._file_path = file_path
    
    @abstractmethod   
    def read(self):
        pass

    @abstractmethod
    def write(self, data):
        pass

class TextFileManager(FileManager):
    def read(self):
        try:
            with open(self._file_path, "r+") as fp:
                return fp.read()
        except  IOError as ioe:
            err_msg = "{0}::{1} - IOError: [Errno {2} ] {3} : {4}".format(self.__class__.__name__, 
                                                                            "read", 
                                                                            str(ioe.errno), 
                                                                            ioe.strerror, 
                                                                            ioe.filename)
            logger.error(err_msg)
            raise BasicError(err_msg, ioe)
        except Exception as err:
            err_msg = "{0}::{1} - IOError: [Errno {2} ] {3}".format(self.__class__.__name__, 
                                                                            "read", 
                                                                            str(err.errno), 
                                                                            err.message)
            logger.error(err_msg)
            raise BasicError(err_msg, err)
        
    def write(self, data):
        try:
            with open(self._file_path, "w+") as fp:
                return fp.write(data)
        except  IOError as ioe:
            err_msg = "{0}::{1} - IOError: [Errno {2} ] {3} : {4}".format(self.__class__.__name__, 
                                                                            "write", 
                                                                            str(ioe.errno), 
                                                                            ioe.strerror, 
                                                                            ioe.filename)
            logger.error(err_msg)
            raise BasicError(err_msg, ioe)
        except Exception as err:
            err_msg = "{0}::{1} - IOError: [Errno {2} ] {3}".format(self.__class__.__name__, 
                                                                            "write", 
                                                                            str(err.errno), 
                                                                            err.message)
            logger.error(err_msg)
            raise BasicError(err_msg, err)

class JSONFileManager(TextFileManager):
    def read(self):
        fc = TextFileManager.read(self)
        return json.loads(fc)
    
    def write(self, data):
        pass
    
    def writes(self, dict_value):
        try:
            with open(self._file_path, "w+") as fp:
                json.dump(dict_value, fp)
        except  IOError as ioe:
            err_msg = "{0}::{1} - IOError: [Errno {2} ] {3} : {4}".format(self.__class__.__name__, 
                                                                            "read", 
                                                                            str(ioe.errno), 
                                                                            ioe.strerror, 
                                                                            ioe.filename)
            logger.error(err_msg)
            raise BasicError(err_msg, ioe)
        except Exception as err:
            err_msg = "{0}::{1} - IOError: [Errno {2} ] {3}".format(self.__class__.__name__, 
                                                                            "read", 
                                                                            str(err.errno), 
                                                                            err.message)
            logger.error(err_msg)
            raise BasicError(err_msg, err)
    
class EasyRequests(object):
    class EasyHttpBasicAuth(HTTPBasicAuth):
        def __init__(self, username, password):
            HTTPBasicAuth.__init__(self, username, password)
            
    class EasyHTTPDigestAuth(HTTPDigestAuth):
        def __init__(self, username, password):
            HTTPDigestAuth.__init__(self, username, password)

    def __init__(self, auth = None, ssl_verify=False, timeout=120, **kargs):
        self._session = requests.Session()
        self._session.auth = auth
        self.verify = ssl_verify
        self.timeout = timeout
    
    def get_back_binary(self, url, data = None, json = None):
        resp = self._session.get(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.content

    def get_back_json(self, url, data = None, json = None):
        """
        :param data: (optional) Dictionary, bytes, or file-like object to send
            in the body of the :class:`EasyRequests`.
        :param json: (optional) json to send in the body of the
            :class:`EasyRequests`.
        """
        resp = self._session.get(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.json()
    
    def get_back_xml(self, url, data = None, json = None):
        pass
    
    def get_back_text(self, url,  data = None, json = None):
        resp = self._session.get(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.text
    
    def post_back_binary(self, url, data = None, json = None):
        resp = self._session.post(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.content

    def post_back_json(self, url, data = None, json = None):
        resp = self._session.post(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.json()
    
    def post_back_xml(self, url, data = None, json = None):
        pass
    
    def post_back_text(self, url,  data = None, json = None):
        resp = self._session.post(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.text
    
    def post_back_status(self, url,  data = None, json = None):
        resp = self._session.post(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return True
    
    def patch_back_binary(self, url, data = None, json = None):
        resp = self._session.patch(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.content

    def patch_back_json(self, url, data = None, json = None):
        resp = self._session.patch(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.json()
    
    def patch_back_xml(self, url, data = None, json = None):
        pass
    
    def patch_back_text(self, url,  data = None, json = None):
        resp = self._session.patch(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.text
    
    def patch_back_status(self, url,  data = None, json = None):
        resp = self._session.patch(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return True

    def put_back_binary(self, url, data = None, json = None):
        resp = self._session.put(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.content

    def put_back_json(self, url, data = None, json = None):
        resp = self._session.put(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.json()
    
    def put_back_xml(self, url, data = None, json = None):
        pass
    
    def put_back_text(self, url,  data = None, json = None):
        resp = self._session.put(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return resp.text
    
    def put_back_status(self, url,  data = None, json = None):
        resp = self._session.put(url, verify=self.verify, timeout=self.timeout, data = data, json = json)
        if(not resp.ok):
            resp.raise_for_status()
            
        return True   

    def delete_back_status(self, url,  **kwargs):
        if(kwargs and len(kwargs) > 0):
            resp = self._session.delete(url, kwargs, verify=self.verify, timeout=self.timeout)
        else:
            resp = self._session.delete(url, verify=self.verify, timeout=self.timeout)
            
        if(not resp.ok):
            resp.raise_for_status()
            
        return True


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs): #@NoSelf
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#Python2
class CommonConfig(object):
    def __init__(self):
        json_fmanager = JSONFileManager("conf{0}devops_utils.json".format(os.path.sep))
        self._config = json_fmanager.read()
    
    def check_config_section(self, module_name):
        if(module_name not in self._config):
            raise BasicError("{0}:{1} - configure file doesn't include section {2}".format(self.__class__.__name__, 
                                                                                           "check_config_section", 
                                                                                           module_name))

    @property
    def config(self):
        return self._config
    
class Crypter():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
        self.key_length = 16 # It must be 16 (*AES-128*), 24 (*AES-192*), or 32 (*AES-256*) bytes long. 
     
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        count = len(text)
        if(count % self.key_length != 0) :
                add = self.key_length - (count % self.key_length)
        else:
            add = 0

        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)
     
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

__all__ = ['LogUtil', 'CommonConfig', 'BasicError']

if __name__ == "__main__":
    LogUtil.init_root_logger("LogUtil")
    try:
        CommonConfig()
    except BasicError as berr:
        logger.error(berr.stack_error)
        sys.exit(1)
    except Exception as err:
        logger.error(err.message)
        