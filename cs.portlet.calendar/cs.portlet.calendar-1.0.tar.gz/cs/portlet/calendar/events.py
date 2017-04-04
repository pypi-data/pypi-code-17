from Acquisition import aq_inner
from DateTime import DateTime
from plone import api
from Products.Five.browser import BrowserView

import json


class CSPortletCalendarEvents(BrowserView):
    def __call__(self):
        context = aq_inner(self.context)
        start = self.request.get('start')
        end = self.request.get('end')
        dt_start = DateTime(start).asdatetime().date()
        dt_end = DateTime(end).asdatetime().date()
        items = api.content.find(
            portal_type='Event',
            start={'query': (dt_start, dt_end), 'range': 'min:max'},
            container=context,
        )
        return json.dumps(self.decorate_events(items))

    def decorate_events(self, events):
        items = []
        for eventbrain in events:
            event = eventbrain.getObject()
            decorated = {}
            decorated['id'] = eventbrain.UID
            decorated['start'] = DateTime(eventbrain.start).ISO8601()
            decorated['end'] = DateTime(eventbrain.end).ISO8601()
            decorated['description'] = event.title
            decorated['url'] = event.absolute_url()
            items.append(decorated)
        return items
