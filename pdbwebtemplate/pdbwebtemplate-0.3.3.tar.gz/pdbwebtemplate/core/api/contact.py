# -*- coding: latin-1 -*-
import json
import logging
import traceback

from pdbwebtemplate.core.business.contact import ContactService
from pdbwebtemplate.core.coreclassesweb import BaseHandlerSession


class ContactHandler(BaseHandlerSession):
    def handle(self, received_json_data, _):
        try:
            response = ContactService.send_contact_email(self, received_json_data)
            self.response.write(json.dumps({'status': response}))
        except Exception as e:
            traceback.format_exc()
            logging.critical('Error sending contact')
            traceback.print_exc()
            raise e