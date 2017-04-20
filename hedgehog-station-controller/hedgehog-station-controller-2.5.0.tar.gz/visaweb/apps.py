from __future__ import unicode_literals

from django.apps import AppConfig

import assetadapter


class VisawebConfig(AppConfig):
    name = 'visaweb'
    verbose_name = "Visaweb Application"

    def ready(self):
        from visaweb.models import Asset
        import visaweb

        asset_list = Asset.objects.all()
        mapping = {}
        for a in asset_list:
            mapping[a.alias] = a.address
        visaweb.client.alias(mapping)
        pass