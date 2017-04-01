from django.apps import apps
from django.db import models

from .utils import RequestRoles, force_to_model

def has_request_system_role(request,role_short_name):
    return role_short_name in request.authz_explicit_roles['system']

def has_request_model_role(request,role_short_name,*models):
    return (role_short_name,model) in request.authz_explicit_roles['model']

def has_request_instance_role(request,role__short_name,instance):
    return (role_short_name,instance) in request.authz_explicit_roles['instance']

def has_request_queryset_role(request,role__short_name,queryset):
    for instance in queryset.all():
        if (role_short_name,instance) in request.authz_explicit_roles['instance']:
            return True
    return False

"""


    _impl = None

    @property
    def impl(self):
        if self._impl is None:
            self._impl = _role_map[self.short_name]()
        return self._impl

    def __str__(self):
        return self.descr_name

    def get_implementation(self):
        return _role_map[self.short_name]

    def filter_qset(self,model,qset,request):
        return qset

    @classmethod
    def sync_from_code(cls):
        super_role = None
        for key,role_class in _role_map.items():
            role,is_new = Role.objects.get_or_create(short_name=key)
            if is_new:
                role.descr_name = role.impl.descr_name
                role.description = role.impl.__doc__
            role.details = role.impl.get_details()
            role.save()
            for obj in role.impl.default_members():
                role.assign_to(usr_grp=obj,reason="by default")

    def assign_to(self,usr_grp,target=None,reason=None):
        ra = RoleAssignment(usr_grp=usr_grp,target=target,role=self,reason=reason)
        ra.save()

    def may_create_model(self,model):
        return model in matching_models(*self.impl.priviliges['create'])

    def may_delete_model(self,model):
        return model in matching_models(*self.impl.priviliges['delete'])

    def may_delete_model(self,model):
        return model in matching_models(*self.impl.priviliges['delete'])

class RoleImplementation:
    def get_details(self):
        return mark_safe(json.dumps(self.priviliges,indent=4).replace(" ","&nbsp;").replace("\n","<br>\n"))

    def default_members(self):
        for obj in []:
            yield obj

    def filter_qset(self,model,qset,request):
        # By default return query set unchanged
        return qset

    applies_to_none  = True         # Systemwide - not related to specific type or instance
    applies_to_type  = False        # May be assigned to type of objects
    applies_to_inst   = False        # May be assigned to the specific object's instance


@register('testing_role')
class RoleTest(AuthzRole):
    pass











class AuthzModel(models.Model):
    roles = {}
    @classmethod
    def get_authz_queryset(cls,request):
        qset = cls.objects
        Q_seq = None
        ctype = ConentType.objects.get_for_moel(cls)
        tmp = {}
        for assigned in [a for a in list(request.authz_explicit_roles['instance']) if a[1] == ctype]:
            role_item = tmp.setdefault(assigned[0],{})
            role_item.setdefault('assigned',[]).append(assigned[2])
        for a_role_name,a_ctype,a_objid in assigned:
            if a_role_name not in cls.roles.keys() or a_ctype != ctype:
                continue
            obj_id.append(a_objid)
            for browse_condition in cls.roles['browse']:
                if browse_condition == 'explicit':
                    qset = qs.filter(id__in = obj_id)

        return qset if Q_seq is None else qset.filter(Q_seq)

    #def is_user_in_model_role(self,role_short_name,user







    roles = ('role_creator'),('role_manager','partner','group__customer__partner_id')
    model_add = {'role_creator':{}}
    model_delete = {'role_manager': {}}
    model_change = model_delete
    model_browse = {'role_manager':{}}


    model_roles = ('each_role_manager',)
    inst_roles =  {
                    'this_role_manager':{''}
                  }

    def is_user_in_model_role(self,role_name,user):
        model = self.model
        return RoleAssignment.active_only.filter(role__short_name=role_name,
                                                 usr_grp=user,
                                                 target_ctype=model,
                                                 target_objid__isnull=True)\
                                         .exists()

    def is_user_this_role_manager(self,user):
        return RoleAssignment.active_only.filter(role='this_role_manager',
                                                 usr_grp=user,
                                                 target=self)\
                                         .exists()

    """



"""
class Rights:
        add_model = True
        del_model = True
        upd_model = True
        browse = True
        def __init__(self,model):
            self.model = model
"""