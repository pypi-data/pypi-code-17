# -*- coding: latin-1 -*-
import os
import re

from pdbwebtemplate.core.business.sendemail import SendEmail
from pdbwebtemplate.core.business.user import UserWeb
from pdbwebtemplate.core.configfile import ConfigFile
from pdbwebtemplate.core.models.userndb import UserNdb

class ForgotPasswordService(object):
    @classmethod
    def request_recover(cls, cpf):
        if not cpf:
            raise Exception('InvalidParameters')

        cpf = re.sub("[^0-9]", "", str(cpf))

        user = UserWeb.get_by_filter(cpf)

        if not user:
            raise Exception('UserNotFound')

        settings = ConfigFile()

        forgot_template_id = settings.get_config_variable('email', 'FORGOTPASS_TEMPLATE_ID', True)
        email_name = settings.get_config_variable('email', 'FORGOTPASS_EMAIL_NAME')
        from_email = settings.get_config_variable('email', 'EMAIL_SENDER')

        environment = os.environ['ENVIRONMENT']
        path = ''

        if environment == 'PROD':
            path = settings.get_config_variable('environment', 'PROD_PATH', True)
        elif environment == 'DEV':
            path = settings.get_config_variable('environment', 'DEV_PATH', True)

        signup_token = UserNdb.create_signup_token(user['id'])

        email_vars = {'link': path+'/recuperarsenha?token='+signup_token,
                      'nome': user['fullname'].encode('latin-1')}

        email_info = {}
        email_info['from_email'] = from_email
        email_info['from_email_name'] = email_name.decode('utf-8', 'replace')
        email_info['to_email'] = str(user['email'])
        email_info['subject'] = ''
        email_info['main_content'] = "<html></html>"
        email_info['template_id'] = forgot_template_id
        email_info['email_substitution_tags'] = email_vars

        SendEmail.send_email(email_info)

        return {'email': user['email']}