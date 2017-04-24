import json
import logging
import traceback

from pdbwebtemplate.core.business.password import ChangePasswordBusiness
from pdbwebtemplate.core.business.user import UserWeb
from pdbwebtemplate.core.coreclassesweb import BaseHandlerSession

class ChangePasswordHandler(BaseHandlerSession):
    def handle(self, received_json_data, response_data):
        try:
            has_error = True
            try:
                ChangePasswordBusiness.validate_password(received_json_data.get('password'))
                has_error = False
                logging.info('PASSWORD WAS VALIDATED WITH SUCCESS')
            except:
                #TODO: make it dinamic
                self.redirect('/recuperarsenhaerro1')

            if not has_error:
                if self.session.get('user_id'):
                    UserWeb.change_password(self.session.get('user_id'), received_json_data.get('password'))
                    self.response.set_status(200)
                    self.response.write(json.dumps(response_data))
                else:
                    logging.info('USER TRYING TO RESET WITH EXPIRED SESSION (post)')
                    logging.info('SESSION: %s', str(self.session))
                    self.response.set_status(400)
                    self.response.write("EXPIRED_SESSION_UPDATE_PASSWORD")

        except Exception as e:
            logging.critical("ERROR DURING RESET PASSWORD (post): %s", traceback.print_exc())
            logging.critical("ERROR DURING RESET PASSWORD (post): %s", e.message)
            # TODO: make it dinamic
            self.redirect('/recuperarsenhaerro')

    def get(self):
        self.redirect('/')
