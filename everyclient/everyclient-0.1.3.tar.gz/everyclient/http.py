# -*- coding: utf-8 -*-
from urllib3 import (
    exceptions,
    PoolManager,
    Timeout,
    Retry,
    )
from certifi import where
from json import (
    loads,
    dumps
    )


class HTTP:
    retries = 5
    redirects = 2
    timeout = 120
    read = None
    domain = 'https://api.every-sense.com'
    port = 8001
    headers = {'Content-Type': 'application/json;charset=utf-8'}

    _conn = PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=where(),
        timeout=Timeout(connect=timeout, read=read),
        retries=Retry(connect=retries, redirect=redirects)
        )

    def request(self, api_method, body):
        url = self.domain + ':' + str(self.port) + '/' + api_method
        try:
            req = self._conn.urlopen(
                'POST',
                url,
                headers=self.headers,
                body=dumps(body),
                )
            res = loads(req.data.decode('utf-8'))
            return res
        except exceptions.MaxRetryError as e:
            res = {
                'code': -40,
                'reason': 'Max retry (%s) exceeded ' % self.retries
            }
            return res
        except exceptions.ConnectTimeoutError as e:
            res = {
                'code': -30,
                'reason': 'Connection timeout (%s sec)' % self.timeout
            }
            return res
        except Exception as e:
            raise e
        finally:
            req.release_conn()
