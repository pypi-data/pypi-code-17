import pprint
from django.apps import apps
from .decorators import authz_role_implementation
from .utils import force_to_model, get_model_full_name, get_role_implementation, wlist_blist

@authz_role_implementation
