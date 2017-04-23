from pdbwebtemplate.core.api.loginbase import LoginBase
from pdbwebtemplate.core.business.login import LoginSocialService


class LoginUserSocialHandler(LoginBase):

    @classmethod
    def get_class_handle(cls):
        return LoginSocialService