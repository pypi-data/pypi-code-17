import logging
import traceback
from pdbwebtemplate.core.business.user import UserWeb
from pdbwebtemplate.core.coreclassesweb import BaseHandlerAuthorized

class UpdateUserHandler(BaseHandlerAuthorized):
    def handle_auth_user(self, user, received_json_data):
        try:
            logging.debug('user %s', str(user))

            received_json_data['cpf'] = user.get('cpf')

            updated_user = UserWeb.update_user(received_json_data)

            self.session['user'] = updated_user
            self.response.set_status(200)
            self.response.write('{}')
        except Exception as e:
            if e.message == 'TOKEN_UNAUTHORIZED' or e.message == 'TOKEN_EXPIRED':
                self.response.set_status(401)
            elif str(e) == 'UNAUTHORIZED':
                self.response.set_status(400)
                self.response.write('USER_ALREADY_EXISTS')
            elif str(e) == 'USER_ALREADY_EXISTS' or str(e) == 'INVALID_PARAMETERS' or str(e) == 'NO_DATA_CHANGED':
                self.response.set_status(400)
                self.response.write(str(e))
            elif str(e) == 'INVALID_AGE':
                self.response.set_status(400)
                self.response.write('INVALID_AGE')
            else:
                err = traceback.print_exc()
                logging.critical('Exception: [%s]', err)
                logging.info('Error: [%s]', str(e))
                self.response.set_status(500)
                self.response.write('INTERNAL_ERROR')