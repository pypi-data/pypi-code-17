# -*- coding: latin-1 -*-
from core.services.basepromo.base_request import BaseRequest
from core.external_auth.externalauth import ExternalAuth

class Extract(object):

    @staticmethod
    def consult_extract(user):
        if user:
            service = ExternalAuth.get_pdbcontest_service()
            response = BaseRequest.handle_execute_serv(service.purchasepromo().purchaseprod().get(user=user), 3)
            return response

    @staticmethod
    def delete_item(user, item):
        service = ExternalAuth.get_pdbcontest_service()
        return BaseRequest.handle_execute_serv(service.purchasepromo().purchaseprod().delete(user=user,
                                                                                             id_item=item), 3)