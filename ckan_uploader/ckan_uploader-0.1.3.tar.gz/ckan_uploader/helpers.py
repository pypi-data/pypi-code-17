# -*- coding: utf-8 -*-
from mimetypes import MimeTypes
from hashlib import md5


def list_of(_list, _class):
    """
    Chequea que la lista _list contenga elementos del mismo tipo, desciptos en _class.

    Args:
        - _list:
            - list().
            - Lista de elementos sobre la que se desea trabajar.
            - El argumento solo acepta objetos de class list.

        - _class:
            - Clase esperada en los elemntos de la lista.
            - admite que se chequee cualquier tipo, incuso, NoneType.

    Returns:
        - bool().
            - True: La  lista posee todos sus elementos de la clase _class
            - False: Al menos uno de los elementos no es de clase _class
    """
    if not isinstance(_list, list):
        raise TypeError('check_list_type() solo acepta type(_list)==list')
    return not False in [isinstance(element, _class) for element in _list]


def get_mimetype(_filename=None):
    """
    Retorna Mime Type de un archivo (_filename).
    Args:
    ====
        - _filename: Str(). path al archivo que se desea chequear.
    Require:
    =======
        - Python Builtin lib: mimetypes.
    Returns:
    =======
         - Str(). MimeType. Exito.
         - None: Fallo.
    """

    try:
        mime = MimeTypes()
        return mime.guess_type(_filename)[0]
    except TypeError:
        pass
    except IOError:
        pass


def build_hash(_filename):
    """
    Crear hash de recurso.
    Args:
    ====
        - _filename: Str(). Archivo sobre el cual se desea calcular HASH.
    Return:
    ======
         - Exito: Str() MD5-Hash.
         - Fallo: None.
    """

    hash_md5 = md5()
    try:
        with open(_filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except IOError:
        pass
