import copy
import json
import logging
import traceback
from pdbwebtemplate.core.business.user import UserWeb
from pdbwebtemplate.core.coreclassesweb import BaseHandlerSession

class RegisterUserHandler(BaseHandlerSession):

    def handle(self, received_json_data, response_data):
        try:
            log_request = copy.deepcopy(received_json_data)

            if hasattr(log_request, 'password'):
                log_request.password = None

            logging.info('REGISTER REQUEST MADE WITH: '+str(log_request))
        except:
            pass

        has_error = True

        try:
            ip = self.request.remote_addr
            ### TODO: make this origin variable....
            origin = 'web'
            device = self.request.headers.get('User-Agent')

            received_json_data['origin'] = origin
            received_json_data['device'] = device
            received_json_data['ip'] = ip

            UserWeb.register(received_json_data)

            if received_json_data:
                received_json_data['identifier'] = received_json_data['cpf']

            self.session['user'] = received_json_data
            self.session['created'] = True
            has_error = False

        except Exception as e:
            if str(e) == 'INVALID_PARAMETERS':
                self.response.set_status(400)
                self.response.write('INVALID_PARAMETERS')
            elif str(e) == 'USER_ALREADY_EXISTS':
                self.response.set_status(400)
                self.response.write('USER_ALREADY_EXISTS')
            elif str(e) == 'EMAIL_ALREADY_USED':
                self.response.set_status(400)
                self.response.write('EMAIL_ALREADY_USED')
            elif str(e) == 'CPF_ALREADY_USED':
                self.response.set_status(400)
                self.response.write('CPF_ALREADY_USED')
            elif str(e) == 'SOCIALID_ALREADY_USED':
                self.response.set_status(400)
                self.response.write('SOCIALID_ALREADY_USED')
            elif str(e) == 'INVALID_PASSWORD_LENGTH':
                self.response.set_status(400)
                self.response.write('INVALID_PASSWORD_LENGTH')
            elif str(e) == 'INVALID_CHARSET':
                self.response.set_status(400)
                self.response.write('INVALID_CHARSET')
            elif str(e) == 'INVALID_AGE':
                self.response.set_status(400)
                self.response.write('INVALID_AGE')
            else:
                err = traceback.print_exc()
                logging.critical('Exception: [%s]', err)
                logging.info('Error: [%s]', str(e))
                self.response.set_status(500)
                self.response.write('INTERNAL_ERROR')

        ### OK RESPONSE....
        if not has_error:
            self.response.set_status(200)
            self.response.write(json.dumps(response_data))
