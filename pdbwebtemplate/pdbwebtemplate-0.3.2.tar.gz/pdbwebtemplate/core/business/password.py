import logging
import traceback
from pdbwebtemplate.core.services.helper.util import Util

from pdbwebtemplate.core.configfile import ConfigFile
from pdbwebtemplate.core.models.userndb import UserNdb
from pdbwebtemplate.core.services.models.usertoken import UserToken

class ChangePasswordBusiness(object):
    @classmethod
    def check_change_pass_attempt(cls, context, page):
        token = context.request.get('token')

        if token and page == 'recuperarsenha':
            try:
                cls.save_token(context, token)
            except:
                page = 'recuperarsenhaerro'
                return page

        elif not token and page == 'recuperarsenha':
            page = 'recuperarsenhaerro'
            return page
        else:
            return page

        return page

    @classmethod
    def save_token(cls, self, token):
        try:

            try:
                user_id, parsed_token = Util.parse_token_dot(token)
            except:
                raise Exception('InvalidToken')

            UserToken().validate_token(token)
            user, temp = UserNdb.get_by_auth_token(int(user_id), parsed_token, 'signup')

            if not user:
                raise Exception('InvalidToken')

            self.session['user_id'] = user['cpf']
            logging.debug('SESSION CREATED FOR RESET PASSWORD: %s', str(self.session))

        except Exception as e:
            self.session['user'] = None
            if e.message == 'InvalidToken' or e.message == 'TOKEN_UNAUTHORIZED' or e.message == 'TOKEN_EXPIRED':
                logging.warn('Normal condition in reset password %s', e.message)
            else:
                logging.critical("ERROR DURING RESET PASSWORD (save_token): %s", traceback.print_exc())
                logging.critical("ERROR DURING RESET PASSWORD (save_token): %s", e.message)

            raise e

    @classmethod
    def validate_password(cls, password):
        settings = ConfigFile()
        __PASSWORD_MIN_LENGTH = int(settings.get_config_variable('register', 'PASSWORD_MIN_LENGTH', True))
        Util.validate_password(password, __PASSWORD_MIN_LENGTH)