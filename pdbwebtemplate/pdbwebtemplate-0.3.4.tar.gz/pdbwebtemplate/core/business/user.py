# -*- coding: latin-1 -*-

import re
from datetime import datetime
import logging
import json
from webapp2_extras import security
from webapp2_extras import auth
from pdbwebtemplate.core.business.util import Util
from pdbwebtemplate.core.configfile import ConfigFile
from pdbwebtemplate.core.connection import MySQL
from pdbwebtemplate.core.business.sendemail import SendEmail
from pdbwebtemplate.core.exceptions import UserInactivated


class UserWeb(object):
    # TODO: set it in config file....
    MANDATORY_PARAMS_INSERT = ['cpf', 'email', 'password', 'fullname', 'phone',
                               'dt_birthday', 'add_street', 'add_number', 'add_neighborhood',
                               'add_city', 'add_state', 'add_zipcode', 'aceitotermo']

    MANDATORY_PARAMS_UPDATE = ['cpf', 'add_street', 'add_number', 'add_neighborhood', 'dt_birthday']

    @classmethod
    def valid_age(cls, json_param):
        settings = ConfigFile()

        # TODO: set this name dt_birthday in config file
        min_age = settings.get_config_variable('site', 'MIN_AGE', True)

        if min_age and ('dt_birthday' in cls.MANDATORY_PARAMS_UPDATE):
            date_birth = datetime.strptime(json_param.get('dt_birthday'), '%d/%m/%Y')
            logging.debug('dateBirth: [%s]', str(date_birth))
            today = datetime.today()
            logging.debug('today: [%s]', str(today))
            age = today.year - date_birth.year - ((today.month, today.day) < (date_birth.month, date_birth.day))

            if min_age and age < int(min_age):
                raise Exception('INVALID_AGE')

    @classmethod
    def register(cls, json_param):
        validation_result = cls.validation(json_param)

        if validation_result == 'INVALID_PARAMETERS':
            raise Exception("INVALID_PARAMETERS")

        ### valid age....
        cls.valid_age(json_param)

        try:
            #TODO: set this param in config file....
            password = json_param.get('password')
            password = str(password)
        except Exception:
            logging.info('ERROR CHARACTER IN PASSWORD')
            raise Exception('INVALID_CHARSET')

        cls.validate_password(password)

        # TODO: it has to be done in hook
        cpf = re.sub("[^0-9]", "", str(json_param.get('cpf')))
        phone = re.sub("[^0-9]", "", str(json_param.get('phone')))
        celphone = re.sub("[^0-9]", "", str(json_param.get('celphone')))
        add_zipcode = re.sub("[^0-9]", "", str(json_param.get('add_zipcode')))
        social_type = json_param.get('social_type') if json_param.get('social_type') else None
        social_id = json_param.get('social_id') if json_param.get('social_id') else None
        social_info = json_param.get('social_info') if json_param.get('social_info') else None
        aceitotermo = 1 if json_param.get('aceitotermo') else 0
        aceitonoticias = 1 if json_param.get('aceitonoticias') else 0
        aceitoinfo = 1 if json_param.get('aceitoinfo') else 0
        email = json_param.get('email')

        if social_info:
            social_info = json.dumps(social_info)

        json_param['cpf'] = cpf
        json_param['phone'] = phone
        json_param['celphone'] = celphone
        json_param['add_zipcode'] = add_zipcode
        json_param['social_type'] = social_type
        json_param['social_id'] = social_id
        json_param['social_info'] = social_info
        json_param['aceitotermo'] = aceitotermo
        json_param['aceitonoticias'] = aceitonoticias
        json_param['aceitoinfo'] = aceitoinfo

        if email:
            email = email.lower()
            json_param['email'] = email

        #TODO: this params has be settled in config file....
        address_full = {
            "street": json_param.get('add_street'),
            "number": json_param.get('add_number'),
            "complement": json_param.get('add_complement'),
            "neighborhood": json_param.get('add_neighborhood')
        }
        address_full = json.dumps(address_full, ensure_ascii=False, encoding='latin-1')

        #TODO: dt_birthday and type of date has to be settled on config file
        date_object = datetime.strptime(json_param.get('dt_birthday'), '%d/%m/%Y')
        dt_birthday = date_object.strftime("%Y-%m-%d")
        json_param['dt_birthday'] = dt_birthday
        json_param['add_full'] = address_full

        # REMOVE UNECESSARY PARAM...
        del json_param['add_street']
        del json_param['add_number']
        del json_param['add_complement']
        del json_param['add_neighborhood']
        del json_param['emailconfirma']
        del json_param['passwordconf']

        created = cls.create_user_store(json_param)

        if not created:
            raise Exception('USER_ALREADY_EXISTS')
        try:
            ### TODO: review this method... maybe using hook
            ### TODO: param have to be on file....
            name = json_param.get('fullname').encode('latin-1')
            email = json_param.get('email').lower()

            cls.send_mail(name, email)
        except Exception as e:
            logging.critical('ERROR_SENDING_EMAIL_REGISTER %s', str(e))

        return created

    @classmethod
    def send_mail(cls, name, email):
        settings = ConfigFile()
        register_template_id = settings.get_config_variable('email', 'REGISTER_TEMPLATE_ID', True)
        sender_email = settings.get_config_variable('email', 'EMAIL_SENDER', True)
        name_email = settings.get_config_variable('email', 'REGISTER_EMAIL_NAME', True)

        email_substitution_tags = {
            'nome': name,
            'email': email
        }

        email_info = {
            'from_email': sender_email,
            'from_email_name': name_email.decode('utf-8', 'replace'),
            'to_email': email,
            'subject': '',
            'main_content': '<html></html>',
            'template_id': register_template_id,
            'email_substitution_tags': email_substitution_tags
        }

        SendEmail.send_email(email_info)

    @classmethod
    def validation(cls, params):
        for param in cls.MANDATORY_PARAMS_INSERT:
            if not params.get(param):
                return 'INVALID_PARAMETERS'

    @classmethod
    def validate_password(cls, password):
        settings = ConfigFile()
        __PASSWORD_MIN_LENGTH = int(settings.get_config_variable('register', 'PASSWORD_MIN_LENGTH', True))
        Util.validate_password(password, __PASSWORD_MIN_LENGTH)

    @classmethod
    def create_user_store(cls, json):

        try:
            if 'password' in json:
                password = security.generate_password_hash(json.get('password'), length=12)
                json['password'] = password
            else:
                raise Exception('NO_PASSWORD_PROVIDED')

            #TODO: it may be moved to some library....
            query = 'insert into user ('
            list_param = []
            values = 'values ('

            for param in json:
                if len(list_param) == 0:
                    query += param
                    values += '%s'
                else:
                    query += ', {}'.format(param)
                    values += ', %s'

                list_param.append(json.get(param))

            ### QUERY IS READY
            query = '{}) {})'.format(query, values)

            conn = MySQL.get_connection(3)
            conn.autocommit(True)
            cursor = conn.cursor()
            result = cursor.execute(query, list_param)

            cursor.close()
            conn.close()
            return result

        except Exception as e:
            if e.__class__.__name__ == 'IntegrityError':
                error, info = e.args
                if 'unique_email' in info:
                    raise Exception('EMAIL_ALREADY_USED')
                if 'unique_cpf' in info:
                    raise Exception('CPF_ALREADY_USED')
                if 'unique_socialid' in info:
                    raise Exception('SOCIALID_ALREADY_USED')
                raise e
            else:
                raise e

    @classmethod
    def update_user(cls, json_param):
        if not json_param:
            raise Exception("INVALID_PARAMETERS")

        for par in cls.MANDATORY_PARAMS_UPDATE:
            if not json_param.get(par):
                raise Exception("INVALID_PARAMETERS")

        cls.valid_age(json_param)

        # TODO: dt_birthday and type of date has to be settled on config file
        if json_param.get('dt_birthday'):
            date_object = datetime.strptime(json_param.get('dt_birthday'), '%d/%m/%Y')
            dt_birthday = date_object.strftime("%Y-%m-%d")
            json_param['dt_birthday'] = dt_birthday

        cpf = json_param.get('cpf')

        if json_param.get('email'):
            del json_param['email']
        if json_param.get('cpf'):
            del json_param['cpf']

        address_full = {
            "street": json_param.get('add_street'),
            "number": json_param.get('add_number'),
            "complement": json_param.get('add_complement'),
            "neighborhood": json_param.get('add_neighborhood')
        }

        if json_param.get('phone'):
            json_param['phone'] = re.sub("[^0-9]", "", str(json_param.get('phone')))
        if json_param.get('celphone'):
            json_param['celphone'] = re.sub("[^0-9]", "", str(json_param.get('celphone')))
        if json_param.get('add_zipcode'):
            json_param['add_zipcode'] = re.sub("[^0-9]", "", str(json_param.get('add_zipcode')))

        json_param['add_full'] = json.dumps(address_full, ensure_ascii=False, encoding='latin-1')

        try:
            del json_param['add_street']
            del json_param['add_number']
            del json_param['add_complement']
            del json_param['add_neighborhood']
        except:
            pass

        if cls.update_user_store(cpf, json_param):
            ret_user = cls.get_by_filter(cpf)
        else:
            raise Exception('NO_DATA_CHANGED')

        return ret_user

    @classmethod
    def update_user_store(cls, cpf, json_param):
        query = 'update user set'
        list_param = []

        for param in json_param:
            if len(list_param) == 0:
                query += ' {} = %s'.format(param)
            else:
                query += ', {} = %s'.format(param)

            list_param.append(json_param.get(param))

        ### QUERY IS READY
        query += ' where cpf = %s'
        list_param.append(cpf)

        conn = MySQL.get_connection(3)
        conn.autocommit(True)
        cursor = conn.cursor()
        result = cursor.execute(query, list_param)

        cursor.close()
        conn.close()

        if result == 1:
            return True
        else:
            return False

    @classmethod
    def update_email_store(cls, cpf, email):
        query = 'update user set email = %s where cpf = %s'

        conn = MySQL.get_connection(3)
        conn.autocommit(True)
        cursor = conn.cursor()
        result = cursor.execute(query, [email, cpf])

        cursor.close()
        conn.close()

        if result == 1:
            return True
        else:
            return False

    @classmethod
    def get_by_filter(cls, cpf=None, email=None, id=None):
        conn = MySQL.get_connection(3)
        cursor = conn.cursor()
        query = ''
        params = []
        if cpf:
            query = 'select * from user where cpf = %s'
            params.append(cpf)
        elif email:
            query = 'select * from user where email = %s'
            params.append(email)
        elif id:
            query = 'select * from user where id = %s'
            params.append(id)

        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(result) < 1:
            raise Exception('USER_NOT_FOUND')

        result = result[0]

        return cls.mount_user_from_db(result)

    @classmethod
    def mount_user_from_db(cls, result_set):
        address = json.loads(result_set[16], encoding='latin-1')
        dt_birthday = result_set[6].strftime("%d/%m/%Y")
        dt_created = ''
        dt_updated = ''
        if result_set[14]:
            dt_created = result_set[14].isoformat()
        if result_set[15]:
            dt_updated = result_set[15].isoformat()

        user = {
            'id': result_set[0],
            'cpf': result_set[1],
            'fullname': result_set[2].decode('latin-1'),
            'email': result_set[3].decode('latin-1'),
            'phone': result_set[4],
            'celphone': result_set[5],
            'dt_birthday': dt_birthday,
            'password': result_set[7],
            'social_type': result_set[8] if result_set[8] else "",
            'social_id': result_set[9] if result_set[9] else "",
            'dt_created': dt_created,
            'dt_updated': dt_updated,
            'add_street': address.get('street'),
            'add_number': address.get('number'),
            'add_complement': address.get('complement') if address.get('complement') else "",
            'add_neighborhood': address.get('neighborhood'),
            'add_city': result_set[17].decode('latin-1'),
            'add_state': result_set[18],
            'add_zipcode': result_set[19],
            'active': result_set[20]
        }

        return user

    @classmethod
    def update_email(cls, iduser, email):

        if not iduser:
            raise Exception('INVALID_HEADER_PARAMETERS')
        if not email:
            raise Exception('INVALID_PARAMETERS')
        try:
            resp = cls.update_email_store(iduser, email)
            if resp:
                return True
            else:
                raise Exception('NO_DATA_CHANGED')
        except Exception as e:
            if e.__class__.__name__ == 'IntegrityError':
                error, info = e.args
                if 'unique_email' in info:
                    raise Exception('EMAIL_ALREADY_USED')
                raise e
            else:
                raise e

    @classmethod
    def change_password(cls, cpf, newpass):
        conn = MySQL.get_connection(3)
        cursor = conn.cursor()
        password = security.generate_password_hash(newpass, length=12)

        query = 'update user set password = %s where cpf = %s'
        result = cursor.execute(query, (password, cpf))
        conn.commit()
        cursor.close()
        conn.close()

        if result == 1:
            return result
        else:
            return False

    @classmethod
    def get_by_auth_password(cls, auth_id, password):

        conn = MySQL.get_connection(3)
        cursor = conn.cursor()

        query = 'select * from user where cpf = %s'
        cursor.execute(query, [auth_id])
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(result) > 0:
            result = result[0]
            user = cls.mount_user_from_db(result)

            if user.get('active') == 0:
                raise UserInactivated()

            if not security.check_password_hash(password, user['password']):
                raise auth.InvalidPasswordError()

            del user['password']
            return user
        else:
            raise auth.InvalidAuthIdError()

    @classmethod
    def get_by_social(cls, social_id, social_type):

        conn = MySQL.get_connection(3)
        cursor = conn.cursor()

        query = 'select * from user where social_id = %s and social_type = %s limit 1'
        cursor.execute(query, [social_id, social_type])
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(result) > 0:
            result = result[0]
            user = cls.mount_user_from_db(result)

            if user.get('active') == 0:
                raise UserInactivated()

            del user['password']
            return user
        else:
            raise auth.InvalidAuthIdError()