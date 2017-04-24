# -*- coding: latin-1 -*-
from core.services.basepromo.base_request import BaseRequest
from core.external_auth.externalauth import ExternalAuth

class Consult(object):
    @staticmethod
    def consult_numbers(user):
        if user:
            service = ExternalAuth.get_pdbcontest_service()
            return BaseRequest.handle_execute_serv(service.querynumbers().querynumbers().get(user_id=user, channel='all'), 3)

    @staticmethod
    def consult_cnpj(cnpj):
        if cnpj:
            service = ExternalAuth.get_pdbcontest_service()
            return BaseRequest.handle_execute_serv(service.purchasepromo().checkcnpj().get(cnpj=cnpj), 3)