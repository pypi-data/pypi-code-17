# -*- coding: latin-1 -*-
import logging
import re

class Util(object):

    @staticmethod
    def clear_cpf(cpf):
        return re.sub("[^0-9]", "", cpf)

    @staticmethod
    def is_cpf(cpf):
        reg = re.compile('[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}')
        return bool(reg.match(cpf))

    @staticmethod
    def parse_token(token):
        values = token.split('.auth.')
        return values[0], values[2]

    @staticmethod
    def __parse_data(value):
        if value.__class__.__name__ == 'datetime':
            value = value.strftime('%Y-%m-%d')
        return value

    @staticmethod
    def parse_token_dot(token):
        values = token.split('.')
        return values[0], values[2]

    @staticmethod
    def hide_email_part(email):
        try:
            part_email = email.split('@')
            hidden_string = ''
            size = len(part_email[0])
            count = 0

            while count < size:
                if count < (size / 2):
                    hidden_string = hidden_string + '*'
                else:
                    hidden_string = hidden_string + part_email[0][count]
                count += 1

            return hidden_string + '@' + part_email[1]
        except:
            return ''

    @staticmethod
    def format_cpf(cpf):
        # adjust CPF
        cpf = str(cpf).zfill(11)
        return "%s.%s.%s-%s" % (cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])

    @staticmethod
    def get_first_name(fullname):
        firstname = ''
        try:
            firstname = fullname.split()[0]
        except Exception as e:
            logging.warn('Error %s', str(e))
        return firstname

    @staticmethod
    def get_last_name(fullname):
        lastname = ''
        try:
            index = 0
            for part in fullname.split():
                if index > 0:
                    if index > 1:
                        lastname += ' '
                    lastname += part
                index += 1
        except Exception as e:
            logging.warn('Error %s', str(e))

        return lastname

    @classmethod
    def validate_password(cls, password, max_length):
        ### CHECK IF PASSWORD HAS ANY SPECIAL CHARS.....
        if len(password) < max_length:
            raise Exception("INVALID_PASSWORD_LENGTH")

        if not password or not password.isalnum():
            raise Exception('INVALID_CHARSET')

    @classmethod
    def hide_email_part(cls, email):
        try:
            part_email = email.split('@')
            hidden_string = ''
            size = len(part_email[0])
            count = 0
            while count < size:
                if count < (size / 2):
                    hidden_string += '*'
                else:
                    hidden_string += part_email[0][count]
                count += 1
            return hidden_string + '@' + part_email[1]
        except:
            return ''