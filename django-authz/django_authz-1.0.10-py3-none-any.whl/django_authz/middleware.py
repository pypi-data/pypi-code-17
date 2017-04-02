from django.contrib.auth.models import AbstractUser
from .models import AuthzInfo


class CollectRolesFromRequest:

    def process_request(self, request):
        """ Add authz_explict_roles dictionary to request object"""
        trustees = []
        user = request.user
        if isinstance(user, AbstractUser):
            trustees.append(user)
            trustees += [g for g in user.groups.all()]
        request.authz = AuthzInfo(*trustees)
