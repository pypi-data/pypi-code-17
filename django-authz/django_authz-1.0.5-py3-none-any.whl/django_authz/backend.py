# -*- coding:utf-8 -*-                                                         #

#===============================================================================
# Copyright (C) 2017 Pearson Central Europe
# All Rights Reserved
# This software is protected under the terms of the proprietary license.
#===============================================================================

import time
from middleware.globalrequest import Request
from authz.registry import authz_registry
from authz.authz import Authz


def calculate_permission(usr, perm, obj=None):
    authz = AuthzCache.get(usr)
    authz.dump()

    if "." not in perm:
        rv = perm in authz.may_acc
    else:
        app, tail = perm.split(".", 1)
        print("app=%s tail=%s" % (app, tail))
        op, model = tail.split("_", 1)
        model = ".".join([app, model])
        print("op=%s model=%s" % (op, model))
        rv = True
    print("CALC PERM: %s %s %s=%s" % (usr, perm, obj, rv))
    return rv


class AuthzCache:
    _cache = {}
    _max_age = 60  # second(s)

    @classmethod
    def get(cls, usr):
        now = time.time()
        rv, tstamp = cls._cache.get(usr, (None, -1.0))
        if rv is not None and now - tstamp <= cls._max_age:
            return rv
        rv = Authz(usr)
        cls._cache[usr] = (rv, now)
        return rv


class PermCache:
    _cache = {}
    _max_age = 60  # second(s)

    @classmethod
    def get(cls, usr, perm, obj=None):
        now = time.time()
        rv, tstamp = cls._cache.get(usr, {}).get(perm, {}).get(obj, (False, -1.0))
        if now - tstamp <= cls._max_age:
            return rv
        rv = calculate_permission(usr, perm, obj=obj)
        cls._cache.setdefault(usr, {}).setdefault(perm, {})[obj] = (rv, now)
        return rv


class AuthBackend(object):


    def authenticate(self, username=None, password=None):
        #print("AUTHZ_BACK Authenticate: %s %s" % (username, "***password***"))
        return None

    def get_user_permissions(self, user_obj, obj=None):
        print("AUTHZ_BACK USR PERM: %s %s" % (user_obj, obj))
        """
        Returns a set of permission strings the user `user_obj` has from their
        `user_permissions`.
        """
        return set()  # self._get_permissions(user_obj, obj, 'user')

    def get_group_permissions(self, user_obj, obj=None):
        print("AUTHZ_BACK GRP PERM: %s %s" % (user_obj, obj))
        """
        Returns a set of permission strings the user `user_obj` has from the
        groups they belong.
        """
        return set()  # self._get_permissions(user_obj, obj, 'group')

    def get_all_permissions(self, user_obj, obj=None):
        print("AUTHZ_BACK ALL PERM: %s %s" % (user_obj, obj))
        if not user_obj.is_active or user_obj.is_anonymous() or obj is not None:
            return set()
        return set()

    def has_perm(self, user, perm, obj=None, **kwargs):
        rv = PermCache.get(user, perm, obj=obj)
        #print("AUTHZ_BACK HAS PERM: %s %s %s = %s" % (user, perm, obj, rv))
        return rv


        try:
            if False:
                authz = Request().authz
                app, tail = perm.split(".", 1)
                #print("app=%s tail=%s" % (app, tail))
                op, model = tail.split("_", 1)
                model = ".".join([app, model])
                #print("op=%s model=%s" % (op, model))
                if op == "add":
                    rv = authz.may_add2(model)
                elif op == "change":
                    rv = authz.may_change(model, obj)
                elif op == "delete":
                    rv = authz.may_delete(model, obj)
                else:
                    rv = False
        except Exception as e:
            print("AUTHZ_BACK HAS PERM: User=%s Perm=%s Obj=%s error=%s" % (user, perm, obj, e))
            rv = False
        rv = AuthBackend._perm_cache_put(user, perm, obj, rv)
        #AuthBackend._perm_cache_dump()

    def has_module_perms(self, user, app_label):
        rv = PermCache.get(user, app_label)
        #print("AUTHZ_BACK HAS MOD PERMS: %s %s = %s" % (user, app_label, rv))
        return rv

    def get_user(self, user_id):
        #print("AUTHZ_BACK GET USER: %s" % user_id)
        # Do nothing here - superclass will do what needed
        return None

