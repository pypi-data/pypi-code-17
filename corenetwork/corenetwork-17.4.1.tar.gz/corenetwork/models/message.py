"""
Copyright (C) 2014-2017 cloudover.io ltd.
This file is part of the CloudOver.org project

Licensee holding a valid commercial license for this software may
use it in accordance with the terms of the license agreement
between cloudover.io ltd. and the licensee.

Alternatively you may use this software under following terms of
GNU Affero GPL v3 license:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. For details contact
with the cloudover.io company: https://cloudover.io/


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.


You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.db import models
from corenetwork.models.tag import Tag

class Message(models.Model):
    message = models.TextField()
    function = models.TextField()
    exception = models.TextField(default='', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    installation_id = models.CharField(max_length=60, help_text='System installation id (different for each corenetwork installation)')

    class Meta:
        app_label = 'corenetwork'

    @property
    def tag_list(self):
        return ', '.join([t.name for t in self.tags.all()])

    @property
    def has_exception(self):
        return self.exception is not None and self.exception != ''

    def __str__(self):
        prefix = '%s %s' % (self.date, self.function)
        prefix_tab = 40 - len(prefix)
        if prefix_tab < 0:
            prefix_tab = 0
        tab_prefix = ' ' * prefix_tab

        tags = ','.join([str(t) for t in self.tags.all()])
        tags_tab = 30 - len(tags)
        if tags_tab < 0:
            tags_tab = 0
        tab_tags = ' ' * tags_tab

        log = '\033[37m%s\033[0m %s \033[32m%s\033[0m%s %s' % (prefix, tab_prefix, tags, tab_tags, self.message)

        if self.exception is not None and self.exception != '':
            log = log + '\n\033[31m' + self.exception + '\033[0m'
        return log