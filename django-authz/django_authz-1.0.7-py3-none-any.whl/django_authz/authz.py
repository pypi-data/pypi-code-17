'''
Documentation, License etc.

@package django_authz
'''
import sys
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from .utils import force_to_model
from .registry import authz_registry
from .models import RoleAssignment


class Authz(object):

    def __init__(self, *trustees):
        self.trustees = trustees
        self._roles = {}   # {name:{model:[target,...]))
        self._targets = set()
        self.may_add = set()
        self.may_upd = set()
        self.may_del = set()
        self.may_acc = set()

        #print("Authz(%s,%s)" % (trustees,extra_roles))
        for trustee in trustees:
            for assignment in RoleAssignment.active_only.filter(trustee_objid=trustee.id):
                #print("found assignment for trustee %s and active role %s" % (trustee,assignment.role.name))
                role_name = assignment.role.name
                _role_item = self._roles.setdefault(role_name, {})

                target_model = ContentType.objects.get(pk=assignment.target_ctype.pk).model_class() \
                                if assignment.target_ctype is not None else None
                target_obj = assignment.target if assignment.target is not None else None

                if target_model:
                    targets = _role_item.setdefault(target_model, [])
                    if target_obj:
                        #print("\nFound target object: %s %s" % (self,target_obj))
                        targets.append(target_obj)
                        self._targets.add(target_obj)
        #print("Authz request for %s:\n %s\n" % (trustees, pprint.pformat(self._roles,indent=2)))
        #self.dump()
        for app_label, models in list(apps.all_models.items()):
            for model in list(models.values()):
                #print("%s models:%s " % (app_label,model))
                if self.has_module_permission(model):
                    self.may_acc.add(model._meta.app_label)

                if self.has_add_permission(model):
                    self.may_add.add(model)
                if self.has_delete_model_permission(model):
                    self.may_del.add(model)
                if self.has_change_model_permission(model):
                    self.may_upd.add(model)

    def dump(self):
        print(("Add: %s" % self.may_add))
        print(("Del: %s" % self.may_del))
        print(("Upd: %s" % self.may_upd))
        print(("Acc: %s" % self.may_acc))
        for role_name, models in list(self._roles.items()):
            for model, targets in list(models.items()):
                if targets:
                    print (("targets for %s: %s" % (role_name, targets)))

    def has_role(self, role_name):
        return role_name in list(self._roles.keys())

    def has_model(self, model):
        for _role_item in list(self._roles.values()):
            if model in list(_role_item.keys()):
                return True
        return False

    def get_role_names(self):
        return list(self._roles.keys())

    def get_implementations(self):
        rv = []
        for role_name in self.get_role_names():
            impl = authz_registry.get_implementation(role_name)
            if impl is not None:
                rv.append(impl)
        #print("role implementations: %s" % rv)
        return rv

    def get_queryset(self, model):
        #print("authz get qset")
        model = force_to_model(model)
        qset = model.objects.none()
        for role_name in list(self._roles.keys()):
            impl = authz_registry.get(role_name)
            if impl is None:
                continue
            tmp = impl.get_queryset(model, self._targets)
            qset |= tmp
        #print("in authz for role %s qset=%s"  % (self,qset))
        return qset

    def get_role_targets(self, role_name):
        rv = []
        for model_targets in list(self._roles[role_name].values()):
            rv += model_targets
        return list(set(rv))

    def get_target_id_list(self, role_implementation, model):
        model = force_to_model(model)
        #print("looking for targets of role:%s model:%s " % (role_implementation,model))
        #print("by roles=%s" % self.by_roles)
        #print("GET ASSIGNED in %s" % self)
        try:
            targets = self.by_roles[role_implementation][model]
        except:
            print((sys.exc_info()[1]))
            targets = []
        return [target.id for target in targets]

    def has_module_permission(self, model):
        model = force_to_model(model)
        rv = False
        for impl in self.get_implementations():
            if impl.has_module_permission(model):
                rv = True
                break
        #if rv:
        #    print("Authz: May %s access module labeled %s? %s" % (self,label,rv))
        return rv

    def has_add_permission(self, model):
        model = force_to_model(model)
        for impl in self.get_implementations():
            if impl.has_add_permission(model):
                return True
        return False

    def has_change_model_permission(self, model):
        model = force_to_model(model)
        for impl in self.get_implementations():
            if impl.has_change_model_permission(model):
                return True
        return False

    def has_delete_model_permission(self, model):
        model = force_to_model(model)
        for impl in self.get_implementations():
            if impl.has_delete_model_permission(model):
                return True
        return False

    def has_change_instance_permission(self, obj):
        for role_name in list(self._roles.keys()):
            impl = authz_registry.get(role_name)
            if impl is None:
                continue
            if impl.has_change_instance_permission(obj, self.get_role_targets(role_name)):
                return True
        return False

    def has_delete_instance_permission(self, obj):
        return False
        for role_name in list(self._roles.keys()):
            impl = authz_registry.get(role_name)
            if impl is None:
                continue
            if impl.has_delete_instance_permission(obj, self.get_role_targets(role_name)):
                return True
        return False
