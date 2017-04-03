from django.db import models


class IPLocation(models.Model):
    id = models.AutoField(primary_key=True)
    ip_from = models.PositiveIntegerField(default=0, db_index=True)
    ip_to = models.PositiveIntegerField(default=0, db_index=True)
    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=64)

    class Meta(object):
        db_table = 'ip_location'
