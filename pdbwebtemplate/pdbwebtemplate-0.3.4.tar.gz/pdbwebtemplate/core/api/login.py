from pdbwebtemplate.core.api.loginbase import LoginBase
from pdbwebtemplate.core.business.login import LoginService


class LoginUserHandler(LoginBase):

    @classmethod
    def get_class_handle(cls):
        return LoginService