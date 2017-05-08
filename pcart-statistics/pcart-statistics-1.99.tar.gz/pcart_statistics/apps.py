from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PCartStatisticsConfig(AppConfig):
    name = 'pcart_statistics'
    verbose_name = _('Statistics')

    def ready(self):
        from pcart_catalog.signals import product_page_visit
        from .listeners import product_page_visit_listener
        product_page_visit.connect(product_page_visit_listener)
