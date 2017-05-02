# -*- coding: utf-8 -*-

"""
    raas_v2.raasv2_client

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""
from .decorators import lazy_property
from .controllers.accounts_controller import AccountsController
from .controllers.orders_controller import OrdersController
from .controllers.catalog_controller import CatalogController
from .controllers.exchange_rates_controller import ExchangeRatesController
from .controllers.status_controller import StatusController
from .controllers.customers_controller import CustomersController
from .configuration import Configuration

class RaaSV2Client(object):

    @lazy_property
    def accounts(self):
        return AccountsController()

    @lazy_property
    def orders(self):
        return OrdersController()

    @lazy_property
    def catalog(self):
        return CatalogController()

    @lazy_property
    def exchange_rates(self):
        return ExchangeRatesController()

    @lazy_property
    def status(self):
        return StatusController()

    @lazy_property
    def customers(self):
        return CustomersController()


    def __init__(self, 
                 platform_name = 'QAPlatform2',
                 platform_key = 'apYPfT6HNONpDRUj3CLGWYt7gvIHONpDRUYPfT6Hj'):
        if platform_name != None:
            Configuration.platform_name = platform_name
        if platform_key != None:
            Configuration.platform_key = platform_key


