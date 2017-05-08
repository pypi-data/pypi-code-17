import logging
import re
from pdbwebtemplate.core.business.user import UserWeb
from pdbwebtemplate.core.business.util import Util
from pdbwebtemplate.core.exceptions import InvalidParameters


class LoginService(object):
    @staticmethod
    def validate_request(user):
        if not user.get('cpf') or not user.get('password'):
            raise InvalidParameters

    @staticmethod
    def login(user):
        login_data = {}
        if Util.is_cpf(user['cpf']):
            user['cpf'] = Util.clear_cpf(user['cpf'])

        user['cpf'] = re.sub("[^0-9]", "", str(user['cpf']))
        logging.info('Getting user with id: %s', user['cpf'])

        user = UserWeb.get_by_auth_password(user['cpf'], user['password'])

        logging.info('user_data: %s', user)

        login_data['user_id'] = user.get('cpf')
        login_data['user_data'] = user

        return login_data

class LoginSocialService(object):
    @staticmethod
    def validate_request(user):
        if not user.get('social_id') or not user.get('social_type'):
            raise InvalidParameters

    @staticmethod
    def login(user):
        login_data = {}

        user = UserWeb.get_by_social(user['social_id'], user['social_type'])

        logging.info('user_data: %s', user)

        login_data['user_id'] = user.get('cpf')
        login_data['user_data'] = user

        return login_data