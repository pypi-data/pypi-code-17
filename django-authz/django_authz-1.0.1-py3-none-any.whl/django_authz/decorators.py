from .models import authz_registry


def authz_role_implementation(role_impl_class):
    authz_registry.register(role_impl_class)
    return role_impl_class


def authz_role_definition(name, title, description):
    authz_registry.register(None, name, title, description)


def authz_modeladmin(cls):
    inner_has_add_permission = cls.has_add_permission
    inner_has_change_permission = cls.has_change_permission
    inner_has_delete_permission = cls.has_delete_permission
    inner_has_module_permission = cls.has_module_permission
    inner_get_actions = cls.get_actions
    inner_get_inline_instances = cls.get_inline_instances
    inner_get_fieldsets = cls.get_fieldsets

    def get_queryset(self, request):
        # Remember about: inner_get_queryset(request)
        return  request.authz.get_queryset(self.model)

    def has_add_permission(self, request):
        return inner_has_add_permission(self, request) or request.authz.has_add_permission(self.model)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return inner_has_change_permission(self, request, obj) or \
                   request.authz.has_change_model_permission(self.model)
        else:
            return inner_has_change_permission(self, request, obj) or request.authz.has_change_instance_permission(obj)

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return inner_has_delete_permission(self, request, obj) or \
                   request.authz.has_delete_model_permission(self.model)
        else:
            return inner_has_delete_permission(self, request, obj) or \
            request.authz.has_delete_instance_permission(obj)

    def has_module_permission(self, request):
        return inner_has_module_permission(self, request) or request.authz.has_module_permission(self.model)

    def get_actions(self, request):
        actions = inner_get_actions(self, request)
        if not self.has_delete_permission(request):
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_inline_instances(self, request, obj=None):
        return inner_get_inline_instances(self, request, obj)

    def get_fieldsets(self, request, obj=None):
        return inner_get_fieldsets(self, request, obj)

    cls.get_queryset = get_queryset
    cls.has_add_permission = has_add_permission
    cls.has_change_permission = has_change_permission
    cls.has_delete_permission = has_delete_permission
    cls.has_module_permission = has_module_permission
    cls.get_actions = get_actions
    cls.get_inline_instances = get_inline_instances
    cls.get_fieldsets = get_fieldsets
    return cls
