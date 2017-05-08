import json
import logging
import traceback

from pdbwebtemplate.core.business.participationpromo import Participation
from pdbwebtemplate.core.configfile import ConfigFile
from pdbwebtemplate.core.coreclassesweb import BaseHandlerAuthorized


class ConsultParticipationHandler(BaseHandlerAuthorized):
    def handle_auth_user(self, user, received_json_data):
        try:

            settings = ConfigFile()
            user_param = settings.get_config_variable('promo', 'USER_IDENTIFIER_PARTICIPATION_PARAM_EXPECTED')
            params = {'iduser': user[user_param]}

            resp = Participation.execution('consult_numbers', params)
            self.response.write(json.dumps(resp))
        except Exception as e:
            if type(e).__name__ == 'HttpError':
                self.response.set_status(e.resp.status)
                self.response.write(e.message.upper())
            else:
                logging.critical('ERROR_HOTSITE_ON_CONSULTPARTICIPATION - HANDLER [%s]', traceback.print_exc())
                logging.critical('ERROR_EXCEPTION: %s', str(e))
                raise e