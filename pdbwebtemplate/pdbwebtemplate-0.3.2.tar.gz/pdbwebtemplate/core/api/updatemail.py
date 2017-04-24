import json
import logging
import traceback

from pdbwebtemplate.core.business.user import UserWeb
from pdbwebtemplate.core.configfile import ConfigFile
from pdbwebtemplate.core.coreclassesweb import BaseHandlerAuthorized



class UpdateUserEmailHandler(BaseHandlerAuthorized):
    def handle_auth_user(self, user, received_json_data):
        try:
            settings = ConfigFile()
            user_param = settings.get_config_variable('site', 'USER_IDENTIFIER_PARAM')

            action = UserWeb.update_email(user[user_param], received_json_data['email'])

            if action:
                user['email'] = received_json_data['email']
                self.session['user'] = user
                self.response.set_status(200)
                self.response.write(json.dumps({}))
            else:
                raise Exception('NO_DATA_CHANGED')

        except Exception as e:
            if e.message == 'TOKEN_UNAUTHORIZED':
                self.response.set_status(401)
            elif str(e) == 'INVALID_HEADER_PARAMETERS':
                self.response.set_status(401)
                self.response.write('INVALID_HEADER_PARAMETERS')
            elif str(e) == 'INVALID_PARAMETERS':
                self.response.set_status(400)
                self.response.write('INVALID_PARAMETERS')
            elif str(e) == 'NO_DATA_CHANGED':
                self.response.set_status(400)
                self.response.write('NO_DATA_CHANGED')
            elif str(e) == 'EMAIL_ALREADY_USED':
                self.response.set_status(400)
                self.response.write('EMAIL_ALREADY_USED')
            else:
                traceback.print_exc()
                logging.critical('Exception: updating email')
                logging.info('Error: [%s]', str(e))
                self.response.set_status(500)
                self.response.write('INTERNAL_ERROR')