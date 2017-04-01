# Middleware

import pprint

import sys
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from .models import RoleAssignment
from .utils import force_to_model
from .registry import authz_registry
from django.contrib.auth.models import AbstractUser, Group
from .authz import Authz

class CollectRolesFromRequest:
    def process_request(self,request):
        """ Add authz_explict_roles dictionary to request object"""
        trustees = []
        extra_roles = []
        user = request.user
        #print("request user=%s" % user)
        if isinstance(user,AbstractUser):
            trustees.append(user)
            #print("User %s added" % user)
            trustees += [g for g in user.groups.all()]
            if user.is_superuser:
                extra_roles = ['authz_allrights']
        #print("Request trustees = %s extra_roles=%s" % (trustees,extra_roles))
        request.authz = Authz(*trustees,extra_roles=extra_roles)
