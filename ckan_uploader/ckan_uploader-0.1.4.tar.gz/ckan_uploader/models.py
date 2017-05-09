# -*- coding: utf-8 -*-


class Errs(object):
    """
    Minima clase para contener errores.
    """

    def __init__(self,
                 _description='',
                 _type='',
                 _context=''):
        import arrow
        for v in [_description, _type, _context]:
            if not isinstance(v, (str, unicode)):
                raise TypeError('La clase del argumento {} no es aceptable'.format(v))
            if len(v) == 0:
                raise ValueError('Todos los argumentos son requeridos, {_v},'
                                 ' no puede ser len({_v})==0'.format(_v=v))
        self.description = _description
        self.type = _type
        self.context = _context
        self.timestamp = arrow.now()

    def __str__(self):
        """
        Imprime en formato READABLE los datos del error.

        Args:
            - None.

        Returns:
            - str().
        """
        return '{ts}: {etype}: {context}: {desc}.'.format(ts=self.timestamp.format('YYYY-MM-DDTHH:mm:ss'),
                                                          etype=self.type.upper(),
                                                          context=self.context,
                                                          desc=self.description)


class MyLogger(object):
    """
    Manejo de Logs Mediante version extendida de logging.
    """

    def __init__(self, logger_name='', log_level='DEBUG'):
        """
        Init de la clase.

        Args:
            - logger_name:
                - Str().
                - No puede ser un string vacio.

            - log_level:
                - Str().
                - No puede ser un string vacio.
                - Solo se adminten cuatro valores posibles: DEBUG, INFO, ERROR, CRITICAL.
        """
        import logging
        # log types.
        self.llevels = {
            'DEBUG': logging.DEBUG,
            'ERROR': logging.ERROR,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'CRITICAL': logging.CRITICAL,
            'NOTSET': logging.NOTSET}

        # log List.
        self.errs = []

        # Validaciones de Argumentos.
        # Chequeo clase.
        for v in [logger_name, log_level]:
            if not isinstance(v, (unicode, str)):
                raise TypeError('El Argumento {}, requiere ser de tipo: str o unicode.'.format(v))

        # Chequeo contenido.
        if len(logger_name) == 0:
            raise ValueError('El Argumento logger_name, no puede ser un String vacio.')

        # Chequeo de contenido.
        if log_level.upper() not in self.llevels.keys():
            raise ValueError('\"{}\", no es un valor aceptado para \"log_level\".')

        # Creo instancia de logging
        logging.basicConfig(level=self.llevels[log_level.upper()])
        self.log_level = log_level
        self.logg_inst = logging.getLogger(logger_name)

    def error(self, msg='', _context='UNKNOW'):
        self.__save_err(_msg=msg, _context=_context, _type='error')
        self.logg_inst.error(msg)

    def warning(self, msg='', _context='UNKNOW'):
        self.__save_err(_msg=msg, _context=_context, _type='warning')
        self.logg_inst.warning(msg)

    def info(self, msg='', _context='UNKNOW'):
        self.__save_err(_msg=msg, _context=_context, _type='info')
        self.logg_inst.info(msg)

    def debug(self, msg='', _context='UNKNOW'):
        self.__save_err(_msg=msg, _context=_context, _type='debug')
        self.logg_inst.debug(msg)

    def critical(self, msg='', _context='UNKNOW'):
        self.__save_err(_msg=msg, _context=_context, _type='critical')
        self.logg_inst.critical(msg)

    def __save_err(self, _msg, _type, _context):
        """
        Agrega el error ocurrido a la lista de errors.

        Args:
            - _msg: Str(). Mensaje de error.
            - _type: Str(). Tipo de error.
            - _context: Str(). Contexto en el cual ocurrio el error.

        Returns:
            - None.
        """
        self.errs.append(Errs(
            _description=_msg,
            _type=_type,
            _context=_context))

    def get_logs(self, _filter_by_type=''):
        """
        Devuelve lista de errores ocurridos.

        Args:
            _filter_by_type: Str(). Tipo de error.
        Return:
             - list().
        """
        err_list = []
        if not (_filter_by_type, str, unicode):
            raise TypeError('El Argumento _filter_by, requiere ser de tipo str o unicode.')
        if _filter_by_type.upper() in self.llevels.keys():
            # Retorno valores filtrados
            for e in self.errs:
                if e.type.upper() == _filter_by_type.upper():
                    err_list.append(e)
        elif _filter_by_type == '':
            # Retorno todos
            err_list = self.errs
        return err_list


class CKANElement(object):
    """Clase generica para contener elementos elementos de CKAN."""

    def __init__(self, _required_keys=None, datadict=None, _forced_keys=None, context='dataset'):
        if not isinstance(_required_keys, list):
            raise TypeError('El argumento \"_required_keys\" requiere ser de tipo \"list\"')
        if context.lower() not in ['distribution', 'dataset']:
            raise ValueError('No es posible seleccionar el contexto deseado [{}]'.format(context))
        self.required_keys = _required_keys
        self.context = context
        self._load(datadict, _forced_keys)

    def _load(self, datadict=None, _forced_keys=None):
        # Chequeo que dataset sea un Diccionario.
        if not isinstance(datadict, dict):
            raise TypeError("El argumento \"datadict\" debe ser un diccionario.")
        # Chequeo que dataset posea todas las claves que
        # requiero para crear una instancia de Dataset
        for rk in self.required_keys:
            # Si la clave requerida, no existe dentro de "datadict"
            # salgo con una exception KeyError.
            if rk not in datadict.keys():
                raise KeyError('{context}: La clave: \"{rk}\", es requerida.'.format(rk=rk,
                                                                                     context=self.context))
            else:
                # si la clave existe, la agrego.
                setattr(self, rk, datadict[rk])
        if None not in [_forced_keys] and isinstance(_forced_keys, dict):
            for k, v in _forced_keys.items():
                setattr(self, k, v)


class Distribution(CKANElement):
    """Clase contenedora para Distributions."""

    def __init__(self, datadict=None, _file=None):
        required_keys = ["state", "license_id",
                         "description", "name", "url"]
        fk = {}
        if isinstance(_file, (str, unicode)):
            import os
            import helpers
            if os.path.exists(_file):
                fn = os.path.abspath(_file)
                fk.update({'file': fn,
                           'mimetype': helpers.get_mimetype(fn),
                           'size': os.path.getsize(fn),
                           'hash': helpers.build_hash(fn),
                           })
        fk.update({'package_id': ''})
        super(Distribution, self).__init__(_required_keys=required_keys,
                                           datadict=datadict,
                                           _forced_keys=fk,
                                           context='distribution')


class Dataset(CKANElement):
    """Clase contenedora para Datasets."""

    def __init__(self, datadict=None, _distributions=None, _distribution_literal=False):
        import helpers
        required_keys = ["license_title", "maintainer", "private",
                         "maintainer_email", "author", "author_email",
                         "state", "type", "groups", "license_id",
                         "owner_org", "url", "notes", "owner_org",
                         "license_url", "isopen", "title", "title", "name"]
        if not _distribution_literal:
            if _distributions:
                if isinstance(_distributions, Distribution):
                    _distributions = [_distributions]
                elif isinstance(_distributions, list):
                    import helpers
                    if not helpers.list_of(_distributions, Distribution):
                        raise TypeError('Las distribuciones provistas, no son de tipo Distribution...')
                else:
                    _distributions = []
            else:
                _distributions = []
        elif not isinstance(_distributions, list) \
                or not helpers.list_of(_distributions, dict):
            raise TypeError('Las distrubuciones \"literales\", solo pueden ser de clase list.')
        super(Dataset, self).__init__(_required_keys=required_keys,
                                      datadict=datadict,
                                      _forced_keys={'resources': _distributions,
                                                    'package_id': ''})


