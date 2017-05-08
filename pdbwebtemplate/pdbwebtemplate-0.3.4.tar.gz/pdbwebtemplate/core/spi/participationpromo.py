import json
import logging
import traceback

from pdbwebtemplate.core.business.participationpromo import Participation
from pdbwebtemplate.core.configfile import ConfigFile
from pdbwebtemplate.core.coreclassesweb import BaseHandlerAuthorized


class ParticipationHandler(BaseHandlerAuthorized):

    def handle_auth_user(self, user, received_json_data):
        try:
            settings = ConfigFile()
            expected_fields = settings.get_config_variable('promo', 'PARTICIPATION_PINCODE_PARAMS_EXPECTED', 'array')
            user_param = settings.get_config_variable('promo', 'USER_IDENTIFIER_PARTICIPATION_PARAM_EXPECTED')

            for field in expected_fields:
                if not received_json_data.get(field):
                    self.request_print_status(400, 'INVALID_PARAMETERS')
                    return
            params = {
                'user_id': user[user_param],
                "pincode": received_json_data['pincode'],
                "extra_info": "{}"
            }

            resp = Participation.execution('participation_pincode', params)
            self.response.write(json.dumps(resp))
        except Exception as e:
            if str(e) == 'INVALID_PARAMETERS':
                self.response.set_status(400)
                self.response.write('INVALID_PARAMETERS')
            if type(e).__name__ == 'HttpError':
                self.response.set_status(e.resp.status)
                self.response.write(e.message.upper())
            else:
                logging.critical('ERROR_HOTSITE_ON_PARTICIPATION - HANDLER [%s]', traceback.print_exc())
                logging.critical('ERROR_EXCEPTION: %s', str(e))
                raise e

