# -*- coding:utf-8 -*-                                                         #

#===============================================================================
# Copyright (C) 2017 Dariusz L. Leonarski
# All Rights Reserved
# This software is protected under the terms of the proprietary license.
#===============================================================================

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .const import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
#from .const import *

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
                     .filter(role__in=RoleStored.active_only.all()) \
                     .filter(Q(inactive_till__isnull=True) |
                             Q(inactive_till__isnull=False, inactive_till__lt=timezone.now()))


class AuthzRole(models.Model):
    """Role is a sort of privilige"""
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


class AuthzGrant(models.Model):
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
                                      related_name="as_authz_trustee",
                                      limit_choices_to=trustee_choices)
    trustee_objid = models.PositiveIntegerField()
    trustee = GenericForeignKey('trustee_ctype', 'trustee_objid')

    target_ctype = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="as_authz_target", limit_choices_to=target_choices)
    target_objid = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ctype', 'target_objid')

    role = models.ForeignKey(AuthzRole, on_delete=models.CASCADE)
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


class AuthzHandler:
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


class RoleFull(AuthzHandler):
    name = "allrights_except"
    title = "Supervisor (limited)"
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


class AuthzRegistry(object):

    def __init__(self):
        self._implementation_map = {}  # {name:implementation}

    def __str__(self):
        return "Role Registry"

    def register(self, role_implementation_class):
        #print("registry.register %s" % role_implementation_class)

        instance = role_implementation_class()
        role_name = instance.name

        if role_name in list(self._implementation_map.keys()):
            print(("Warning: role %s already in registry with implementation: %s" %
                   (role_name, self._implementation_map[role_name])))
        self._implementation_map[role_name] = instance

    def get_implementation(self, role_name):
        return self._implementation_map.get(role_name, None)
    get = get_implementation

    def __iter__(self):
        for name, implementation in list(self._implementation_map.items()):
            yield (name, implementation)


authz_registry = AuthzRegistry()
