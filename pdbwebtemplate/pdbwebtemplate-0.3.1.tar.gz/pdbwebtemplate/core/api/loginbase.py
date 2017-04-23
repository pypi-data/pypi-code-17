import json
import logging
import traceback

from pdbwebtemplate.core.coreclassesweb import BaseHandlerSession
from pdbwebtemplate.core.exceptions import InvalidParameters, UserInactivated, InternalServerError
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError


class LoginBase(BaseHandlerSession):
    def handle(self, received_json_data, _):
        try:
            service = self.get_class_handle()
            service.validate_request(received_json_data)
            login_data = service.login(received_json_data)
            login_resp = {
                'user_data': login_data['user_data']
            }

            ### SAVE IN SESSION..
            self.session['user'] = login_resp['user_data']

            self.response.set_status(200)
            self.response.write(json.dumps(login_resp))

        except Exception as e:
            if isinstance(e, InvalidAuthIdError):
                self.response.set_status(404)
                self.response.write("USER_NOT_FOUND")
            elif isinstance(e, InvalidPasswordError):
                self.response.set_status(400)
                self.response.write("INVALID_PASSWORD")
            elif isinstance(e, InvalidParameters):
                self.response.set_status(400)
                self.response.write("INVALID_PARAMETERS")
            elif isinstance(e, UserInactivated):
                self.response.set_status(400)
                self.response.write("USER_INACTIVATED")
            else:
                stacktrace = traceback.format_exc()
                logging.critical("Error during login!! %s", stacktrace)
                self.response.set_status(500)
                self.response.write(InternalServerError.get_json_response500(str(e)))

    @classmethod
    def get_class_handle(cls):
        raise NotImplemented

class LogoutUserHandler(BaseHandlerSession):
    def handle(self, _, __):
        self.clear_cache()
        self.session['user'] = None
        self.redirect("/")