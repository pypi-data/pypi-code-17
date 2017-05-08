import json
import logging
import traceback
from pdbwebtemplate.core.business.forgotpassword import ForgotPasswordService
from pdbwebtemplate.core.business.util import Util
from pdbwebtemplate.core.coreclassesweb import BaseHandler

class ForgotPasswordHandler(BaseHandler):

    def handle(self, received_json_data, _):
        try:
            if received_json_data.get('cpf'):
                response = ForgotPasswordService.request_recover(received_json_data.get('cpf'))
                forgot_password = {
                    'email':  Util.hide_email_part(response.get('email'))
                }
                self.response.set_status(200)
                self.response.write(json.dumps(forgot_password))
            else:
                raise Exception('InvalidParameters')

        except Exception as e:
            if str(e) == 'USER_NOT_FOUND':
                self.response.set_status(404)
                self.response.write('USER_NOT_FOUND')
            elif str(e) == 'InvalidParameters':
                self.response.set_status(400)
                self.response.write('INVALID_PARAMETERS')
            else:
                logging.critical('Exception: [%s]', traceback.print_exc())
                logging.info('Error: [%s]', str(e))
                self.response.set_status(500)
                self.response.write('INTERNAL_ERROR')