# -*- coding: latin-1 -*-
'''
Created on Sep 11, 2016

@author: richard
'''
import logging
import json
import traceback
from googleapiclient import errors


class BaseRequest(object):
    '''
    Base class for request
    '''
    @staticmethod
    def execute_service(service, retries=0):

        try:
            return service.execute(num_retries=retries)
        except errors.HttpError as e:
            content = json.loads(e.content)
            content = content['error']
            if content['code'] == 400:
                err_str = content['message']
                e.message = err_str
                raise e
            if content['code'] == 404:
                err_str = 'NotFound'
                e.message = err_str
                raise e
            else:
                logging.critical('ERROR_HOTSITE - HANDLING_HTTP_ERROR: %s', traceback.print_exc())
                raise Exception
        except Exception as e:
            logging.critical('ERROR_SERVICE_EXECUTION %s', traceback.print_exc())
            raise e