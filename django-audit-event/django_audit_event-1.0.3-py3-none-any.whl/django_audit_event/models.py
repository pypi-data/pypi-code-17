from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

try:
    from django.contrib.gis.geoip2 import GeoIP2
    geoip_support = True
except Exception as e:
    geoip_support = False
    print("Warning: no GEOIP support.")
    print(("Error during import GeoIP2: %s" % e))

import uuid


def new_uuid():
    return str(uuid.uuid4())


def discover_crequest():
    try:
        from crequest.middleware import CrequestMiddleware

        def real_crequest():
            return CrequestMiddleware.get_request()
        rv = real_crequest
    except ImportError:

        def fake_crequest():
            return None
        rv = fake_crequest
    return rv


Request = discover_crequest()


################################################################################
# Constatnts
################################################################################

class C:
    """ Just a container for a few constatnts"""
    TEXT_SHORT_LENGTH = 50
    TEXT_MEDIUM_LENGTH = 100
    TEXT_LONG_LENGTH = 1024

    # Suggested Outcome Names (set of possible outcome values is not limited to those below only).
    OUT_SUCCESS = "success"
    OUT_FAILURE = "failure"
    OUT_DENIAL = "denial"
    OUT_INTERRUPT = "interrupt"
    OUT_FINISH = 'finish'
    OUT_START = 'start'

    # Severity Levels
    SEV_DEBUG = 0
    SEV_INFO = 10
    SEV_WARN = 20
    SEV_ERROR = 30
    SEV_CRITICAL = 40


################################################################################
#                                                                              #
#                                   Event                                      #
#                                                                              #
################################################################################
class AuditEvent(models.Model):
    class Meta:
        verbose_name = _('Audit Event')
        verbose_name_plural = _('Audit Events')

    ############################################################################
    # Persistent properties
    ############################################################################
    name = models.CharField(max_length=C.TEXT_LONG_LENGTH, null=True, default='', verbose_name=_("Event Name"))
    uuid = models.CharField(max_length=36, default=new_uuid, unique=True)
    outcome = models.CharField(max_length=C.TEXT_SHORT_LENGTH, verbose_name=_("Outcome code"))

    tstamp_beg = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=_("Begin Time Stamp"))
    tstamp_end = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=_("End Time Stamp"))
    duration = models.PositiveIntegerField(default=0)

    severity = models.SmallIntegerField(default=C.SEV_INFO, verbose_name=_("Severity"))

    initiator_name = models.CharField(max_length=C.TEXT_MEDIUM_LENGTH, null=True, blank=True)
    initiator_id = models.CharField(max_length=C.TEXT_MEDIUM_LENGTH, null=True, blank=True)

    target_name = models.CharField(max_length=C.TEXT_MEDIUM_LENGTH, null=True, blank=True)
    target_id = models.CharField(max_length=C.TEXT_MEDIUM_LENGTH, null=True, blank=True)

    details = models.TextField(_("Details"), null=True)
    error_msg = models.CharField(max_length=C.TEXT_MEDIUM_LENGTH, null=True, blank=True)
    comment = models.TextField(_("Comment"), null=True)

    src_ip_addr = models.CharField(null=True, max_length=C.TEXT_SHORT_LENGTH, verbose_name=_("Source IP"))
    src_city = models.CharField(max_length=C.TEXT_MEDIUM_LENGTH, null=True, blank=True)
    src_country = models.CharField(max_length=C.TEXT_MEDIUM_LENGTH, null=True, blank=True)
    src_latitude = models.FloatField(null=True, blank=True)
    src_longitude = models.FloatField(null=True, blank=True)

    ############################################################################
    # Instance Level Methods
    ############################################################################
    def __str__(self):
        return "%s %s %s" % (self.name, self.tstamp_beg, self.outcome)

    def save(self, *args, **kwargs):
        self.duration = (self.tstamp_end - self.tstamp_beg).total_seconds()
        super(AuditEvent, self).save(*args, **kwargs)

    def update(self, **kwargs):
        for key, val in list(kwargs.items()):
            setattr(self, key, val)
        self.tstamp_end = timezone.now()
        self.save()

    ############################################################################
    # Class Level Methods
    ############################################################################
    @classmethod
    def _store(cls, evt_name, level, **kwargs):
        kwargs.update(dict(name=evt_name, severity=level))
        event = cls(**kwargs)

        request = Request()
        if request is not None:
            if 'initiator_name' not in kwargs and request.user:
                event.initiator_name = request.user.username
            if 'initiator_id' not in kwargs and request.user:
                event.initiator_id = request.user.id
            event.src_ip_addr = request.META.get('HTTP_X_FORWARDED_FOR', '')
            if not event.src_ip_addr:
                event.src_ip_addr = request.META.get('REMOTE_ADDR', 'localhost')
            if geoip_support:
                try:
                    g = GeoIP2()
                    c = g.city(event.src_ip_addr)
                    event.src_city = c['city']
                    event.src_country = c['country_name']
                    event.src_latitude = c['latitude']
                    event.src_longitude = c['longitude']
                except:
                    # Ignore if failed
                    pass
        event.save()
        return event

    @classmethod
    def info(cls, evt_name, **kwargs):
        return cls._store(evt_name, C.SEV_INFO, **kwargs)

    @classmethod
    def warn(cls, evt_name, **kwargs):
        return cls._store(evt_name, C.SEV_WARN, **kwargs)

    @classmethod
    def error(cls, evt_name, **kwargs):
        return cls._store(evt_name, C.SEV_ERROR, **kwargs)

    @classmethod
    def critical(cls, evt_name, **kwargs):
        return cls._store(evt_name, C.SEV_CRITICAL, **kwargs)

    @classmethod
    def given(cls, evt_name, severity, **kwargs):
        return cls._store(evt_name, severity, **kwargs)

    @classmethod
    def clean_too_old(cls, days):
        pass
