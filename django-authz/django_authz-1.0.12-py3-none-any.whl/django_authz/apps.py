from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class AuthzConfig(AppConfig):
    name = 'authz'
    verbose_name = _("Django Authorization Module")

    def ready(self):
        from .models import Role, Grant, Handler
        from .registry import authz_registry

        #  Collect roles from authz_registry and ensure corresponding RoleStored exist
        for  role_name, role_impl in list(authz_registry._implementation_map.items()):
            #print("reg: %s %s" % (role_name,role_impl))
            try:
                role, is_new = RoleStored.objects.get_or_create(name=role_name)
            except Exception as e:
                print(("Error: %s" % e))
                continue

            #print("%6s %s:%s " % ("IS NEW" if is_new else "",role_name,role_impl))
            if is_new:
                role.title = role_impl.title
                role.description = role_impl.description
                role.save()

        # For each Role in RoleStored ensure corresponding implementation exists
        # Or mark role as not implemented
        # TRY EXCEPT is because "ready" method is called twice
        # and during one of the passes exception occures
        try:
            #print("App ready. registry2=%s" % authz_registry._implementation_map)
            #print("App ready. stored count=%s" % RoleStored.objects.count())
            for role_stored in RoleStored.objects.all():
                #print("impl for %s is: %s" % (role_stored.name,i))
                if not isinstance(authz_registry.get_implementation(role_stored.name), RoleImplementation):
                    #print("Warning :role %s has no implementation. Empty Role presumed" % role_stored.short_name)
                    role_stored.implemented = False
                else:
                    role_stored.implemented = True
                    role_stored.details = authz_registry.get_implementation(role_stored.name).dump()
                role_stored.save()

            #print("Authz Reg is:\n %s" % pprint.pformat(authz_registry.role_implementations,indent=2,compact=True))
        except Exception as e:
            #print("error: %s" % e)
            pass
        #print("Authz Registry is:\n %s" % pprint.pformat(authz_registry._implementation_map,indent=2,compact=True))
        #from importlib import import_module
        #m = import_module('app_partner.roles')
        #exec("import app_partner.roles",globals())
        #__import__('app_partner.roles')

        from django.apps import apps
        from django.contrib.contenttypes.models import ContentType
        #print("AUTH USER MODEL NAME: %s" % settings.AUTH_USER_MODEL)
        from django.contrib.auth.models import Group
        authz_user_model = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
        #print("AUTH USER MODEL: %s" % authz_user_model)
        from django.contrib.contenttypes.fields import GenericRelation

        authz_user_model.authz_targets = GenericRelation(RoleAssignment, related_query_name='authz_trustees')
        Group.authz_targets = GenericRelation(RoleAssignment, related_query_name='authz_trustees')
        from django.db.models import Q
        try:
            q = ContentType.objects.none()
            for item in settings.AUTHZ_TARGET_MODELS:
                app_label, model_name = item.lower().split(".")
                q |= Q(app_label=app_label, model=model_name)
                #print("added %s.%s" % (app_label,model_name))
            RoleAssignment.target_choices = q
            #RoleAssignment.target_ctype.get_limit_choices_to = q
        except Exception as e:
            print(e)
