# -*- coding: latin-1 -*-
import sendgrid
from sendgrid.helpers.mail import *
from sendgrid import *
import logging
import traceback
from pdbwebtemplate.core.configfile import ConfigFile

class SendEmail(object):

    @staticmethod
    def send_email(email_info):
        try:
            settings = ConfigFile()
            SEND_GRID_KEY = settings.get_config_variable('email', 'SERVICE_KEY')

            from_email = Email(email_info['from_email'], email_info['from_email_name'])
            to_email = Email(email_info['to_email'].encode('utf-8'))
            subject = str(email_info['subject'].encode('utf-8'))
            content = str(email_info['main_content'])
            template_id = str(email_info['template_id'])
            email_substitution_tags = email_info.get('email_substitution_tags')

            sg = sendgrid.SendGridAPIClient(apikey=str(SEND_GRID_KEY))
            personalization = Personalization()
            personalization.add_to(to_email)

            if email_substitution_tags:
                for key, value in email_substitution_tags.iteritems():
                    pkey = '%{}%'.format(key)
                    pvalue = u'{}'.format(value.decode('latin-1'))
                    personalization.add_substitution(Substitution(pkey, pvalue))

            content = Content("text/html", content)
            mail = Mail()

            #TODO: adapt sendgrid....

            mail.set_from(from_email)
            mail.add_personalization(personalization)
            mail.set_subject(subject)
            mail.add_content(content)
            mail.set_template_id(template_id)

            sg.client.mail.send.post(request_body=mail.get())
            return True

        except Exception as e:
            logging.critical('EMAIL_CONFIG_ERROR: [%s]', traceback.print_exc())
            logging.critical('ERROR_MESSAGE: [$s]', str(e))
            raise e