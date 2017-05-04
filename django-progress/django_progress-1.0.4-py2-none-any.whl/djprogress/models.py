from django.db import models

import datetime

class Progress(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    current = models.IntegerField(default=0)
    total = models.IntegerField(default=100)
    eta = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, db_index=True)
    parent = models.ForeignKey('Progress', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    exception = models.TextField(blank=True)
    
    class Meta:
        verbose_name = u'progress'
        verbose_name_plural = u'progresses'

    def __unicode__(self):
        return u'%s: %d/%d' % (self.name, self.current, self.total)
    
    def is_just_now_updated(self):
        return (datetime.datetime.now() - self.last_updated).seconds < 7

