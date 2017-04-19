import requests
from fnexchange.core.plugins import AbstractPlugin


class SlackPlugin(AbstractPlugin):
    def post_message(self, payload):
        elements = payload["elements"]
        pretext = getattr(self.config, 'pretext', None)
        title = getattr(self.config, 'title', 'Security Notification')

        attachments = []
        for element in elements:
            attachment = {
                'title': title,
                'fields': [{'title': k, 'value': v, 'short': True} for k, v in element.items()]
            }
            if pretext:
                attachment['pretext'] = pretext
            attachments.append(attachment)

        success = False
        try:
            response = requests.post(self.config.url, json={'attachments': attachments})
            success = response.status_code == 200
        except:
            pass

        return {
            'metadata': {
                'success': success
            },
            'elements': elements  # return the same thing back
        }
