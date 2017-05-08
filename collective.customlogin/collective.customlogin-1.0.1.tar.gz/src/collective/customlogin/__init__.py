from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService import registerMultiPlugin

from collective.customlogin import plugin

try:
    registerMultiPlugin(plugin.CustomLogin.meta_type)
except RuntimeError:
    # ignore exceptions on re-registering the plugin
    pass


def initialize(context):
    context.registerClass(
        plugin.CustomLogin,
        permission=add_user_folders,
        constructors=(plugin.manage_addCustomLoginForm,
                      plugin.manage_addCustomLogin),
        visibility=None,
        icon=""
    )
