import logging
import os
import traceback
from pdbwebtemplate.core.business.sendemail import SendEmail
from pdbwebtemplate.core.configfile import ConfigFile
from pdbwebtemplate.core.models.storemailcontact import StoreEmailContact


class ContactService(object):
    @classmethod
    def send_contact_email(cls, handle, data):
        logging.info('CONTACT_EMAIL_SENT_WITH: [%s]', str(data))

        try:
            settings = ConfigFile()
            service_email_receiver = settings.get_config_variable('email', 'CONTACT_EMAIL_RECEIVER')

            if not data.get('fullname') or not data.get('phone_number') or not data.get('email') or \
                    not data.get('subject') or not data.get('message') or not data.get('cpf'):
                raise Exception('INVALID_PARAMETERS')

            environment = os.environ['ENVIRONMENT']

            if 'DEV' == environment:
                service_email_receiver = 'dev@promodebolso.com.br'
                #else:
                #service_email_receiver = 'contato@promocaotorratorra.com.br'

            contact_email_name = settings.get_config_variable('email', 'CONTACT_EMAIL_NAME')
            contact_email_sender = data.get('email')

            email_info = {}
            email_info['from_email'] = contact_email_sender
            email_info['from_email_name'] = contact_email_name.decode('utf-8', 'replace')
            email_info['to_email'] = service_email_receiver
            email_info['subject'] = data.get('fullname')
            email_info['main_content'] = "<html></html>"
            email_info['template_id'] = settings.get_config_variable('email', 'CONTACT_TEMPLATE_ID')

            email_substitution_tags = {}

            #TODO: it has to be flexiable...
            email_substitution_tags['name'] = data.get('fullname').encode('latin-1', 'replace')
            email_substitution_tags['cell'] = data.get('phone_number')
            email_substitution_tags['email'] = data.get('email').encode('latin-1', 'replace')
            email_substitution_tags['subject'] = data.get('subject').encode('latin-1', 'replace')
            email_substitution_tags['message'] = data.get('message').encode('latin-1', 'replace')
            email_substitution_tags['cpf'] = data.get('cpf')

            email_info['email_substitution_tags'] = email_substitution_tags

            cls.store_email(data, service_email_receiver)

            response = SendEmail.send_email(email_info)

            if response:
                return 'EMAIL_SENT'
            else:
                return 'EMAIL_NOT_SENT'

        except Exception as e:
            if str(e) == 'INVALID_PARAMETERS':
                handle.response.set_status(400)
            else:
                settings = ConfigFile()
                service_email_receiver = settings.get_config_variable('email', 'CONTACT_EMAIL_RECEIVER')
                cls.store_email(data, service_email_receiver)
                traceback.print_exc()
                logging.critical('ERROR SENDING EMAIL: %s', traceback.print_exc())
                raise e

    @classmethod
    def store_email(cls, data, receiver):
        ### TODO: id should be using a queue....
        try:
            promoname = os.environ['PROMO_NAME']
            sender_name = data.get('fullname')
            message = data.get('message')
            StoreEmailContact(sender_name=sender_name,
                              sender_id=data.get('cpf'),
                              sender_phone=data.get('phone_number'),
                              sender_email=data.get('email'),
                              subject=data.get('subject'),
                              message=message,
                              receiver_email=receiver,
                              namespace=promoname).put()
        except:
            traceback.print_exc()
            logging.critical('ERROR STORING EMAIL: %s', traceback.print_exc())
