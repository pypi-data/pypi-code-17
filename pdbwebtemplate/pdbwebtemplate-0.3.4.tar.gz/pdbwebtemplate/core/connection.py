'''
Created on May 28, 2016

@author: everton
'''
import os
import logging
import MySQLdb
import time

class MySQL(object):

    @classmethod
    def get_connection(cls, retry=1):
        try:
            if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
                logging.info('GAE_DB')
                logging.debug('PROJECT [%s], INSTANCE[%s] - USER [%s] - PASS [%s], SCHEMA [%s]',
                              os.getenv('CLOUDSQL_PROJECT'),
                              os.getenv('CLOUDSQL_INSTANCE'),
                              os.getenv('CLOUDSQL_USER'),
                              os.getenv('CLOUDSQL_PASS'),
                              os.getenv('CLOUDSQL_SCHEMA'))

                unix_socket = '/cloudsql/{}:{}'.format(os.getenv('CLOUDSQL_PROJECT'),
                                                       os.getenv('CLOUDSQL_INSTANCE'))

                logging.info('Opening connection')
                db = MySQLdb.connect(unix_socket=unix_socket, user=os.getenv('CLOUDSQL_USER'),
                                     passwd=os.getenv('CLOUDSQL_PASS', ''), db=os.getenv('CLOUDSQL_SCHEMA'))

            else:
                logging.info('LOCAL_DB')
                db = MySQLdb.connect(host=os.getenv('DBDEV_HOST'),
                                     user=os.getenv('DBDEV_USER'),
                                     passwd=os.getenv('DBDEV_PASS', ''),
                                     db=os.getenv('DBDEV_SCHEMA'))

            return db

        except Exception as e:
            if e and retry <= 3:
                time.sleep(2)
                logging.info('RETRY_IS: %s', str(retry))
                return cls.get_connection(retry+1)
            else:
                logging.critical('ERROR_GETTING_CONNECTION_AFTER_RETRY: %s', str(e))
                logging.info('CONNECTION_RETRY_WAS: %s', str(retry))
            raise e
