# -*- coding: latin-1 -*-
from core.external_auth.externalauth import ExternalAuth
from core.services.basepromo.base_request import BaseRequest

class Participation(object):

    @classmethod
    def execution(cls, method, params):
        """ CENTRAL METHOD
        :param method: The method to be called
        :param params: Dict with the service params
        :return: Service body response
        """
        if method == 'participation_pincode':
            return cls.participation_pincode(params)
        if method == 'consult_numbers':
            return cls.consult_numbers(params)

    @classmethod
    def participation_pincode(cls, params):
        service = ExternalAuth.get_pdbcontest_service()
        return BaseRequest.execute_service(service.requestnumbers().requestnumbers().put(body=params))

    @classmethod
    def create_purchase(cls, params):
        service = ExternalAuth.get_pdbcontest_service()
        return BaseRequest.execute_service(service.purchasepromo().savepurchase().put(body=params))

    @classmethod
    def consult_numbers(cls, params):
        service = ExternalAuth.get_pdbcontest_service()
        return BaseRequest.execute_service(
            service.querynumbers().querynumbers().get(user_id=params['iduser'], channel='all'), 3)