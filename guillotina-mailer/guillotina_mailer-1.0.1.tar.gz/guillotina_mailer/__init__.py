# -*- coding: utf-8 -*-
from guillotina import configure

app_settings = {
    "mailer": {
        "default_sender": "foo@bar.com",
        "endpoints": {
            "default": {
                "type": "smtp",
                "host": "localhost",
                "port": 25
            }
        },
        "debug": False,
        "utility": "guillotina_mailer.utility.MailerUtility",
        "use_html2text": True,
        "domain": None
    }
}


configure.permission(id="mailer.SendMail", title="Request subscription")
configure.grant(permission="mailer.SendMail", role="guillotina.ContainerAdmin")


def includeme(root, settings):
    utility = settings.get('mailer', {}).get('utility',
                                             app_settings['mailer']['utility'])
    root.add_async_utility({
        "provides": "guillotina_mailer.interfaces.IMailer",
        "factory": utility,
        "settings": settings.get('mailer', {})
    }, loop=root.app.loop)

    configure.scan('guillotina_mailer.api')
