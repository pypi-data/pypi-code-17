import pprint
from django.apps import apps
from .decorators import authz_role_implementation
from .utils import force_to_model, get_model_full_name, get_role_implementation, wlist_blist


@authz_role_implementation
class TestRole1(AuthzHandler):
    name = "test_role_1"
    title = "Testing role one"
    description = "Just fortesting purposes"

    def __init__(self):
        super(TestRole1, self).__init__()
