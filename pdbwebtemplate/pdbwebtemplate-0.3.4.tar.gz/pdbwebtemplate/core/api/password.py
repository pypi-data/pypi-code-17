import json
import logging
import traceback

from pdbwebtemplate.core.business.password import ChangePasswordBusiness
from pdbwebtemplate.core.business.user import UserWeb
from pdbwebtemplate.core.coreclassesweb import BaseHandlerSession


class ChangePasswordHandler(BaseHandlerSession):
    def handle(self, received_json_data, response_data):
        try:

            try:
                str(received_json_data.get('password'))
            except Exception:
                logging.info('ERROR CHARACTER IN PASSWORD')
                raise Exception('INVALID_CHARSET')

            ChangePasswordBusiness.validate_password(received_json_data.get('password'))

            logging.info('PASSWORD WAS VALIDATED WITH SUCCESS')

            if self.session.get('user_id'):
                UserWeb.change_password(self.session.get('user_id'), received_json_data.get('password'))
                self.session['password_changed'] = True
                self.response.set_status(200)
                self.response.write(json.dumps(response_data))
            else:
                logging.info('USER TRYING TO RESET WITH EXPIRED SESSION (post)')
                logging.info('SESSION: %s', str(self.session))
                self.response.set_status(400)
                self.response.write("EXPIRED_SESSION_UPDATE_PASSWORD")

        except Exception as e:
            if str(e) == 'INVALID_CHARSET':
                self.response.set_status(400)
                self.response.write('INVALID_CHARSET')
                return
            else:
                logging.critical("ERROR DURING RESET PASSWORD (post): %s", traceback.print_exc())
                logging.critical("ERROR DURING RESET PASSWORD (post): %s", e.message)
                # TODO: make it dinamic
                self.redirect('/recuperarsenhaerro')

    def get(self):
        self.redirect('/')
