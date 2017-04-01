class AuthzModelMixin(object):
    @classmethod
    def authz_may_add_to_model(cls,request):
        return request.authz.may_add_to_model(cls)

    @classmethod
    def authz_may_upd_model(cls,request):
        return request.authz.may_upd_model(cls)

    @classmethod
    def authz_may_del_from_model(cls,request):
        return request.authz.may_del_from_model(cls)

    @classmethod
    def authz_may_access_module(cls,request):
        return request.authz.may_access_model(cls)

    @classmethod
    def authz_get_queryset(cls,request):
        rv = cls.objects.none()
        for role in request.authz.get_roles():
            rv |= role.get_queryset(request,cls)
        #print("authz queryset=%s" % rv)
        return rv

    def authz_may_upd_instance(self,request):
        for impl in request.authz.get_roles():
            if impl.may_upd_instance(request,self):
                return True
        return False

    def authz_may_del_instance(self,request):
        for impl in request.authz.get_roles():
            if impl.may_del_instance(request,self):
                return True
        return False
