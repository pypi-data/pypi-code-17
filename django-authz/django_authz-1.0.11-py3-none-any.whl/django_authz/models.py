# -*- coding:utf-8 -*-                                                         #

#===============================================================================
# Copyright (C) 2017 Dariusz L. Leonarski
# All Rights Reserved
# This software is protected under the terms of the proprietary license.
#===============================================================================

import sys

from django.apps import apps
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
#from .const import *


#from .const import *
from .utils import force_to_model, get_model_full_name

TEXT_SHORT_LENGTH = 40
TEXT_MEDIUM_LENGTH = 100
TEXT_LONG_LENGTH = 500


def Q_ored(*items):
    q = None
    for item in items:
        app_label, model_name = item.split(".", 1)
        if q is None:
            q = Q(app_label=app_label, model=model_name)
        else:
            q |= Q(app_label=app_label, model=model_name)
    return q


class _ActiveRoleManager(models.Manager):

    def get_queryset(self):
        return super(_ActiveRoleManager, self).get_queryset().filter(active=True, implemented=True)


class _ActiveGrantManager(models.Manager):
    def get_queryset(self):
        return super(_ActiveGrantManager, self) \
                     .get_queryset() \
                     .filter(role__in=Role.active_only.all()) \
                     .filter(Q(inactive_till__isnull=True) |
                             Q(inactive_till__isnull=False, inactive_till__lt=timezone.now()))


class Role(models.Model):
    """Role as an entry in a database."""
    """Role's logic is expressed by RoleHandler. Association is done by Role.name == RoleHandler.name"""
    name = models.CharField(max_length=TEXT_SHORT_LENGTH, verbose_name="Name", unique=True)
    """ System use name"""
    title = models.CharField(max_length=TEXT_MEDIUM_LENGTH, verbose_name="Title", help_text="Human readable name")
    """ Human readable name"""

    description = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    implemented = models.BooleanField(default=False)

    objects = models.Manager()
    active_only = _ActiveRoleManager()

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ('name',)

    def __str__(self):
        return self.title if self.title else self.name

    def get_handler(self):
        return authz_registry.get(self.name)


class Grant(models.Model):
    class Meta:
        unique_together = ('trustee_ctype', 'trustee_objid', 'target_ctype', 'target_objid', 'role')

    try:
        trustee_choices = Q_ored(*settings.AUTHZ_TRUSTEE_MODELS)
    except:
        trustee_choices = Q_ored(settings.AUTH_USER_MODEL, "auth.group")

    try:
        target_choices = Q_ored(*settings.AUTHZ_TARGET_MODELS)
    except:
        target_choices = Q()
    #print("Trustee choices: %s" % str(trustee_choices))
    #print("Target choices: %s" % str(target_choices))
    #trustee_choices = Q(app_label=authz_user_app_label, model=authz_user_model_name)| Q(app_label="auth", \
    #model="group") #ContentType.objects
    #target_choices = Q(app_label="partner", model="partner")| Q(app_label="pearson", model="customer")
    #target_choices = ContentType.objects # app_label="partner", model="partner")| Q(app_label="pearson", \
    # model="customer")
    trustee_ctype = models.ForeignKey(ContentType,
                                      on_delete=models.CASCADE,
                                      related_name="as_grant_trustee",
                                      limit_choices_to=trustee_choices)
    trustee_objid = models.PositiveIntegerField()
    trustee = GenericForeignKey('trustee_ctype', 'trustee_objid')

    target_ctype = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="as_grant_target", limit_choices_to=target_choices)
    target_objid = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ctype', 'target_objid')

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    reason = models.CharField(max_length=TEXT_MEDIUM_LENGTH, default="unknown")
    inactive_till = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()
    active_only = _ActiveGrantManager()

    def __str__(self):
        return("%s as %s" % (self.trustee, self.role))

    @classmethod
    def exists(cls, trustee, target, role_name):
        if trustee is None or target is None:
            return False
        trustee_ct = ContentType.objects.get(app_label=trustee._meta.app_label, model=trustee._meta.model_name)
        target_ct = ContentType.objects.get(app_label=target._meta.app_label, model=target._meta.model_name)
        return cls.objects.filter(trustee_ctype=trustee_ct, trustee_objid=trustee.id,
                                         target_ctype=target_ct, target_objid=target.id,
                                         role__name=role_name).exists()

    @classmethod
    def exists_target(cls, trustee, role_name):
        if trustee is None:
            return False
        trustee_ct = ContentType.objects.get(app_label=trustee._meta.app_label, model=trustee._meta.model_name)
        return cls.objects.filter(trustee_ctype=trustee_ct, trustee_objid=trustee.id,
                                  target_objid__isnull=False,
                                  role__name=role_name).exists()

################################################################################
# Role Implementations(s)
################################################################################


class RoleHandler:
    """ Role Implementation"""
    name = "authz_norights"
    title = "No Rights at all"
    description = "No rights anywhere"

    may_add_models = []
    cant_add_models = []

    may_delete_models = []
    cant_delete_models = []

    may_change_models = []
    cant_change_models = []

    may_access_modules = []
    cant_access_modules = []

    def __init__(self, name="", title="", description=""):
        if name:
            self.name = name
        if title:
            self.title = title
        if description:
            self.description = description

    def has_module_permission(self, app_label):
        """ app_label is expected be a string """
        return app_label in self.may_access_modules and app_label not in self.cant_access_modules

    def has_add_model_permission(self, model):
        """ model is expected be a name or instance of a specific model"""
        """ fullname means app_label.model_name"""
        full_model_name = get_model_full_name(model)
        rv = full_model_name in self.may_add_models and full_model_name not in self.cant_add_models
        #if rv:
        #    print ("found %s in %s" % (fname,self.may_change_models))
        return rv

    def has_change_model_permission(self, model):
        """ model is expected be a name or instance of a specific model"""
        """ fullname means app_label.model_name"""
        full_model_name = get_model_full_name(model)
        rv = full_model_name in self.may_change_models and full_model_name not in self.cant_change_models
        #if rv:
        #    print ("found %s in %s" % (fname,self.may_change_models))
        return rv

    def has_delete_model_permission(self, model):
        """ model is expected be a name or instance of a specific model"""
        """ fullname means app_label.model_name"""
        full_model_name = get_model_full_name(model)
        rv = full_model_name in self.may_delete_models and full_model_name not in self.cant_delete_models
        #if rv:
        #    print ("found %s in %s" % (fname,self.may_change_models))
        return rv

    def has_change_instance_permission(self, obj, targets):
        return False

    def has_delete_instance_permission(self, obj, targets):
        return False

    def get_queryset(self, model, directly_assigned):
        model = force_to_model(model)
        return model.objects.none()

    def dump(self):
        rv = {'add': set(),
              'upd': set(),
              'del': set(),
              'acc': set(),
             }
        for app_label, models in list(apps.all_models.items()):
            for model in list(models.values()):
                #print("%s models:%s " % (app_label,model))
                if self.has_module_permission(model):
                    rv['acc'].add(model._meta.app_label)

                if self.has_add_model_permission(model):
                    rv['add'].add(model._meta.model_name)
                if self.has_delete_model_permission(model):
                    rv['del'].add(model._meta.model_name)
                if self.has_change_model_permission(model):
                    rv['upd'].add(model._meta.model_name)
        out = ""
        for key in ['add', 'upd', 'del', 'acc']:
            rv[key] = [item for item in rv[key]]
            rv[key].sort()
        out = "\n".join(["%s: %s" % (key, rv[key]) for key in ['acc', 'add', 'upd', 'del'] if rv[key]])
        return out


class EmptyRole(RoleHandler):
    """White & Black lists are taken into account """
    name = "allrights_except"
    title = "Supervisor (limited, without priviliges stated here)"
    description = "Any rights anywwhere"


class LimitedRole(RoleHandler):
    """Only Black lists are taken into account """
    name = "allrights_except"
    title = "Supervisor (limited, without priviliges stated here)"
    description = "Any rights anywwhere"

    def has_module_permission(self, app_label):
        """ app_label is expected be a string """
        return app_label not in self.cant_access_modules

    def has_add_model_permission(self, model):
        """ model is expected be a name or instance of a specific model"""
        """ fullname means app_label.model_name"""
        full_model_name = get_model_full_name(model)
        rv = full_model_name not in self.cant_add_models
        #if rv:
        #    print ("found %s in %s" % (fname,self.may_change_models))
        return rv

    def has_change_model_permission(self, model):
        """ model is expected be a name or instance of a specific model"""
        """ fullname means app_label.model_name"""
        full_model_name = get_model_full_name(model)
        rv = full_model_name not in self.cant_change_models
        #if rv:
        #    print ("found %s in %s" % (fname,self.may_change_models))
        return rv

    def has_delete_model_permission(self, model):
        """ model is expected be a name or instance of a specific model"""
        """ fullname means app_label.model_name"""
        full_model_name = get_model_full_name(model)
        rv = full_model_name not in self.cant_delete_models
        #if rv:
        #    print ("found %s in %s" % (fname,self.may_change_models))
        return rv

    def has_change_instance_permission(self, obj, targets):
        return False

    def has_delete_instance_permission(self, obj, targets):
        return False

    def get_queryset(self, model, directly_assigned):
        model = force_to_model(model)
        return model.objects.none()


class _AuthzRegistry(object):

    def __init__(self):
        self._handlers_map = {}  # {name:implementation}

    def __str__(self):
        return "Role Registry: %s" % self._handlers_map

    def register(self, role_handler_class):
        instance = role_handler_class()
        role_name = instance.name

        if role_name in list(self._handlers_map.keys()):
            raise AssertionError("Warning: role named %s already in registry with implementation: %s" %
                   (role_name, self._handlers_map[role_name]))
        self._handlers_map[role_name] = instance

    def get_handler(self, role_name):
        return self._handlers_map.get(role_name, EmptyRole())

    def __iter__(self):
        for name, handler in list(self._handlers_map.items()):
            yield (name, handler)

authz_registry = _AuthzRegistry()


class AuthzInfo(object):
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
            for assignment in Grant.active_only.filter(trustee_objid=trustee.id):
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

    def get_handlers(self):
        rv = []
        for role_name in self.get_role_names():
            impl = authz_registry.get_handler(role_name)
            if impl is not None:
                rv.append(impl)
        #print("role implementations: %s" % rv)
        return rv

    def get_queryset(self, model):
        #print("authz get qset")
        model = force_to_model(model)
        qset = model.objects.none()
        for role_name in list(self._roles.keys()):
            impl = authz_registry.get_handler(role_name)
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
        for impl in self.get_handlers():
            if impl.has_module_permission(model):
                rv = True
                break
        #if rv:
        #    print("Authz: May %s access module labeled %s? %s" % (self,label,rv))
        return rv

    def has_add_permission(self, model):
        model = force_to_model(model)
        for impl in self.get_handlers():
            if impl.has_add_model_permission(model):
                return True
        return False

    def has_change_model_permission(self, model):
        model = force_to_model(model)
        for impl in self.get_handlers():
            if impl.has_change_model_permission(model):
                return True
        return False

    def has_delete_model_permission(self, model):
        model = force_to_model(model)
        for impl in self.get_handlers():
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
