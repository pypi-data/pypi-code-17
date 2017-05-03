import sys

reload(sys)
sys.setdefaultencoding('utf8')


class CKANUploader(object):
    def __init__(self,
                 ckan_url='',
                 ckan_api_key='',
                 dp_user='',
                 dp_pass='',
                 dp_host='http://localhost',
                 dp_port='8800'):
        """
        Inicializacion del Modulo CKANUploader

        Args:
        ====
            ckan_api_key: Str().
                    - Este campo no puede ser vacio. len(obj) == 0
                    - API-KEY de CKAN para realizar tareas dentro de CKAN
                      Se requiere que el usuario propietario de la API-KEY tenga permisos.
                      de actualizacion y carga de activos de datos.

            ckan_url: Str().
                     - Este campo no puede ser vacio, len(obj) == 0.
                     - URL al portal de datos.

        """
        import ckanapi
        from models import MyLogger
        if False in [isinstance(arg, (str, unicode)) for arg in self.__init__.__code__.co_varnames]:
            raise TypeError
        if 0 in [len(ckan_api_key), len(ckan_url)]:
            # Si alguno de los argumentos provistos es de logitud 0
            # "suelto" una exception ValueError
            raise ValueError('Los Argumentos [\'ckan_url\',\'ckan_api_key\']')
        self.host_url = ckan_url
        self.api_key = ckan_api_key
        self.ua = 'ckanuploader/1.0 (+https://github.com/datosgobar/ckanuploader)'

        self.log = MyLogger(logger_name='{}.controller'.format(__name__),
                            log_level='INFO')
        self.my_remote_ckan = ckanapi.RemoteCKAN(self.host_url, apikey=self.api_key, user_agent=self.ua)
        dp_con_vars = [dp_user, dp_pass, dp_host, dp_port]
        self.dp_available = 0 not in [len(v) for v in dp_con_vars]
        if self.dp_available:
            self.dp_host = dp_host
            self.dp_user = dp_user
            self.dp_pass = dp_pass
            self.dp_port = dp_port
            self.dp_url = '{host}{port}'.format(host=dp_host,
                                                port=':{}'.format(dp_port) if dp_port != '80' else '')

    def exists(self, id_or_name='', search_for_datasets=True):
        """
        Chequea la existencia de un Dataset o un recurso.

        Args:
        ====
            - id_or_name: str(). ID o Nombre del objeto que se requiere chequear.
                          Para datasets, se admite que se use Name o ID, mientras que para
                          distribuciones, solo se podra buscar mediante ID.

            - search_for_datasets: bool(). FLAG,
                - True: Se busca un Dataset.
                - False: Se busca un distribucion.
                - default: True(Busqueda para datasets)

        Returns:
        =======
            - bool():
                - True: Existe el objeto buscado.
                - False: No existe el objeto buscado.
        """
        # Si el tipo de los argumentos provistos no es el esperado,
        # salgo con una exception TypeError.
        if not isinstance(id_or_name, (str, unicode)) or not isinstance(search_for_datasets, bool):
            raise TypeError

        # Si id_or_name es una cadena vacia, salgo con un exception ValueError.
        if len(id_or_name) == 0:
            raise ValueError('El argumento id_or_name no puede ser de len()==0')
        # Si el flag search_for_datasets == True, busco sobre los datasets.
        if search_for_datasets:
            avalailable_datasets = self.my_remote_ckan.action.package_list()
            return id_or_name in avalailable_datasets
        else:
            # Considero que estoy buscando una distribution
            all_distributions = self.get_all_distrubutions()
            dist_by_ids = [_id for _id in all_distributions.keys()]
            dist_by_names = [self._render_name(all_distributions[_id]) for _id in all_distributions.keys()]
            return id_or_name in dist_by_ids or id_or_name in dist_by_names

    def _render_name(self, title=None, _encoding='utf-8'):
        """
        Formatea cadenas de textos a formato de nombres para ckan.

        Este metodo aplica las siguientes transformaciones:
        - Cambiar espacios por guiones medios.
        - Toda la frase en minusculas.
        - Quita caracteres que no sean alfanumericos.

        Args:
            - name: str() o unicode().
        Returns:
            - str:
        """
        import re
        import unicodedata

        def strip_accents(text):
            """Quitar acentos."""
            try:
                try:
                    text = unicode(text, _encoding)
                except NameError:
                    pass
                text = unicodedata.normalize('NFD', text)
                text = text.encode('ascii', 'ignore')
                text = text.decode("utf-8")
            except Exception as e:
                self.log.debug(str(e))
            return str(text)

        text = strip_accents(title.lower())
        text = re.sub('[ ]+', '-', text)
        text = re.sub('[^0-9a-zA-Z_-]', '', text)
        return text

    def create_dataset(self, dataset=None):
        """
        Crea un nuevo dataset en un CKAN remoto.

        Args:
             - dataset:
        Returns:
             - TODO.
        """
        from ckanapi import NotAuthorized, ValidationError, NotFound
        from models import Dataset
        status = False
        if not isinstance(dataset, Dataset):
            raise TypeError
        try:
            dataset.name = self._render_name(dataset.title)
            dataset.groups = self.build_groups(dataset.groups)
            self.my_remote_ckan.action.package_create(**dataset.__dict__)
            status = True
        except NotAuthorized:
            self.log.error('No posee los permisos requeridos para crear el dataset {}.'
                           ''.format(dataset.title))
        except ValidationError:
            self.log.error('No es posible crear el dataset \"{}\", el mismo ya existe.'
                           ''.format(dataset.title))
        except NotFound:
            self.log.error('No es posible crear el dataset \"{}\", alguno de los datos '
                           'provistos no existen.')

        return status

    def update_dataset(self, dataset=None):
        """
        Actualizar Datasets o Distribuciones.

        Args:
            - dataset: Dataset().
        """
        from models import Dataset
        from ckanapi import NotAuthorized, ValidationError
        if not isinstance(dataset, Dataset):
            raise TypeError
        status = False
        update_this_dataset = dataset.__dict__
        unrequired_keys = ['required_keys', 'context']
        for k in unrequired_keys:
            if k in update_this_dataset.keys():
                del update_this_dataset[k]
        try:
            update_this_dataset['name'] = self._render_name(dataset.title)
            update_this_dataset['groups'] = self.build_groups(dataset.groups)
            self.my_remote_ckan.action.package_update(**update_this_dataset)
            status = True
        except NotAuthorized:
            self.log.error('No posee los permisos requeridos para crear el dataset {}.'
                           ''.format(dataset.title))
        except ValidationError:
            self.log.error('No es posible crear el dataset \"{}\", el mismo ya existe.'
                           ''.format(dataset.title))
        return status

    def get_distributions(self, id_or_name=None, all_platform=False):
        """
        Retona lista de distribuciones contenidas dentro de un Dataset.

        Args:
            - id_or_name:
                - Str().
                - ID o NAME de un dataset.
                - Si id_or_name no es unicode o str, sale con una exception TypeError.
                - Si el id_or_name no existe dentro de la plataforma, sale con una Exception ValueError.
        Returns:
            - List()
        """
        # Validaciones de campos:
        if not isinstance(id_or_name, (str, unicode)) or \
                not isinstance(all_platform, bool):
            err_msg = 'Los Argumentos provistos no son validos...'
            self.log.error(err_msg)
            raise TypeError(err_msg)
        # Chequeo que exista el dataset seleccionado.
        if not self.exists(id_or_name=id_or_name):
            err_msg = 'No existe Dataset con ID o NAME == {}'.format(id_or_name)
            self.log.error(err_msg)
            raise ValueError(err_msg)

    def get_all_distrubutions(self):
        """
        Diccionario de distrubuciones disponibles en el CKAN remoto: self.ckan_url.

        Args:
        ====
            - None.

        Returns:
        ========
            - dict().
        """
        distributions = {}
        all_datasets = self.my_remote_ckan.action.package_list()
        for dataset in all_datasets:
            ds_dist = self.my_remote_ckan.call_action('package_show', {'id': dataset})
            ds_dist = ds_dist['resources']
            for d in ds_dist:
                distributions.update({d['id']: d['name']})
        return distributions

    @staticmethod
    def diff_datasets(dataset_a=None, dataset_b=None):
        """
        Compara dos datasets y retorna la diferencia aditiva de ambos.

        Cuando se realiza la diferencia, el valor que prevalece es el de
        dataset_b.

        Args:
        ====
            - dataset_a:
                - Dataset().
                - Solo admite ser de tipo Dataset().

            - dataset_b:
                - Dataset().
                - Solo admite ser de tipo Dataset().

        Returns:
        =======
            - Dataset().

        Exceptions:
        ==========
            TypeError:
                - Uno o ambos argumentos, no son de clase Dataset.
        """
        from models import Dataset
        for v in [dataset_a, dataset_b]:
            if not isinstance(v, Dataset):
                raise TypeError('Para comparar los datasets ambos deben ser de clase Dataset.')
        diff_ds = {}
        omit_this_keys = ['required_keys', 'context']
        for k, v in dataset_a.__dict__.items():
            if k not in omit_this_keys:
                if v != dataset_b.__dict__[k]:
                    diff_ds.update({k: dataset_b.__dict__[k] if len(dataset_b.__dict__[k]) > 0 else v})
                else:
                    diff_ds.update({k: v})
        return Dataset(datadict=diff_ds,
                       _distributions=dataset_a.__dict__['resources'],
                       _distribution_literal=True)

    def freeze_dataset(self, id_or_name):
        """
        Crea una imagen temporal del contenido de un dataset.

        Args:
        ====
            - id_or_name:
                - str().
                - Id o Nombre del dataset que deseo freezar.
        Returns:
        =======
            - Dataset: Si el objeto es localizable & "Freezable".

        Exceptions:
        ==========
            - ValueError:
                - id_or_name esta unicode o str pero es del len == 0.
            - TypeError:
                - id_or_name no es un str o unicode.
        """
        from models import Dataset
        stored_dataset = self.retrieve_dataset_metadata(id_or_name)
        if stored_dataset:
            freezed_dataset = {"license_title": stored_dataset['license_title'],
                               "maintainer": stored_dataset['maintainer'],
                               "private": stored_dataset['private'],
                               "maintainer_email": stored_dataset['maintainer_email'],
                               "id": stored_dataset['id'],
                               "owner_org": stored_dataset['owner_org'],
                               "author": stored_dataset['author'],
                               "isopen": stored_dataset['isopen'],
                               "author_email": stored_dataset['author_email'],
                               "state": stored_dataset['state'],
                               "license_id": stored_dataset['license_id'],
                               "type": stored_dataset['type'],
                               "groups": [g['name'] for g in stored_dataset['groups']],
                               "creator_user_id": stored_dataset['creator_user_id'],
                               "name": stored_dataset['name'],
                               "url": stored_dataset['url'],
                               "notes": stored_dataset['notes'],
                               "title": stored_dataset['title'],
                               "license_url": stored_dataset['license_url']}
            return Dataset(datadict=freezed_dataset,
                           _distribution_literal=True,
                           _distributions=stored_dataset['resources'])

    def get_datasets_list(self, only_names=True):
        """
        Obtener lista de Datasets y Recursos remotos.

        Args:
            - only_names = bool(). FLAG.
                            - True: Lista con solo los nombres de los dataset de self.ckan_url.
                            - False: Lista con todos los datos de los dataset de self.ckan_url.

        Returns:
        ========
            - list().
                - len(list) == 0: No existen datos.
                - len(list) == n, lista de n datasets.

        Exceptions:
        ==========
            - TypeError:
                - only_names no es de clase bool.
        """
        if not isinstance(only_names, bool):
            err_msg = 'El agumento \"only_names\" requiere ser de tipo \"bool\".'
            self.log.error(err_msg)
            raise TypeError(err_msg)
        if only_names:
            return self.my_remote_ckan.action.package_list()
        else:
            return self.my_remote_ckan.action.package_search()['results']

    def get_resource_id(self, name=''):
        """
        Obtener el ID de un recurso.

        Args:
            - name:
                - str().
                - No admite len()==0.

        Returns:
             - None: No existe el recurso.
             - Str(). Id de recurso.
        """
        all_distributions = self.get_all_distrubutions()
        all_distributions_ids = [_id for _id in all_distributions.keys()]
        all_distributions_name = [self._render_name(n) for n in all_distributions.values()]
        fixed_name = self._render_name(name)
        if fixed_name in all_distributions_name:
            _index = all_distributions_name.index(fixed_name)
            return all_distributions_ids[_index]

    def retrieve_dataset_metadata(self, id_or_name=None):
        """
        Retorna metadata de un dataset.

        Args:
        ====
            - id_or_name: str(). nombre o id del dataset requerido

        Returns:
        =======
            - dict():
            - None: No existe el recurso.

        Exceptions:
        ==========
            - TypeError:
                - id_or_name no es de clase str o unicode.
        """
        if not isinstance(id_or_name, (unicode, str)):
            raise TypeError
        try:
            ds = self.my_remote_ckan.call_action('package_show',
                                                 data_dict={'id': id_or_name})
            return ds
        except Exception as e:
            self.log.error(e)

    def clean_all_views(self, resource_id):
        """
        Elimina las vistas creadas para un recurso de id==resource_id.
        Args:
            - resource_id:
                - str|unicode.
                - not None.
                - Not len(resource_id) == 0.
        """
        import ckanapi
        try:
            resource_views = self.my_remote_ckan.call_action('esource_view_list',
                                                             {'id': resource_id})
            for view in resource_views:
                view_id = view['result']['id']
                if self.my_remote_ckan.call_action('resource_view_delete',
                                                   {'id':view_id}):
                    pass
                else:
                    self.log.warning('No fue posible eliminar la vista: \'{}\''
                                     ' del recurso \'{}\'.'.format(view_id,
                                                                   resource_id))
        except ckanapi.ValidationError:
            self.log.error('resource_id invalido({})'.format(resource_id))
            return False

        except ckanapi.NotFound:
            self.log.warning('No se encontraron vistas para el recurso:\'{}\''.format(resource_id))
            return False

    def build_groups(self, groups=None, _selected_keys=None):
        """Formatea los grupos para poder incluirlos dentro de la creacion | actualizacion de los datasets."""
        fixed_groups = []
        if not isinstance(groups, list):
            raise TypeError('El argumento \"groups\" requiere ser una lista.')
        if None in [_selected_keys]:
            required_keys = ['id']
        elif isinstance(_selected_keys, list):
            required_keys = _selected_keys
        else:
            err_msg = 'El Argumento \"_selected_keys\" no puede ser \"{}\"'.format(type(_selected_keys))
            self.log.error(err_msg)
            raise TypeError(err_msg)
        platform_groups_list = self.my_remote_ckan.action.group_list()
        if False in [True for g in groups if g in platform_groups_list]:
            err_msg = 'No esposible seleccionar el grupo especifico.'
            self.log.error(err_msg)
            raise ValueError(err_msg)
        for g in groups:
            mg = self.my_remote_ckan.call_action('group_show', data_dict={'id': g})
            fix_me = {}
            for rk in required_keys:
                fix_me.update({rk: mg[rk]})
            fixed_groups.append(fix_me)
        return fixed_groups

    def _push_distribution(self,
                           _d=None,
                           update=False,
                           only_metadata=False,
                           _views=True):
        """
        Carga a CKAN una distribucion.

        Returns:
             - bool.
                - True, exito al salvar la distribucion.
                - False, ocurrio un fallo al salvar la distribucion.

        """
        from ckanapi.errors import CKANAPIError, NotFound, NotAuthorized, ValidationError

        def get_dp_status(_resource_id=''):
            from requests.auth import HTTPBasicAuth
            from requests.exceptions import ConnectionError, Timeout, ReadTimeout
            import requests
            try:
                with requests.Session() as s:
                    # Iniciamos la session
                    dp_host = self.dp_url
                    s.get(url='{}/login'.format(dp_host),
                          auth=HTTPBasicAuth(self.dp_user, self.dp_pass))
                    jobs_list = s.get(url='{host}/job'.format(host=dp_host)).json()['list']
                    for job in jobs_list:
                        job_url = '{host}{uri}'.format(host=dp_host, uri=job)
                        json_response = s.get(job_url).json()
                        if json_response['metadata']['resource_id'] == _resource_id:
                            return json_response['status'] != 'pending'
            except ConnectionError:
                self.log.critical('Imposible establecer conexion con el host:{}.'.format(self.dp_host))
                raise ConnectionError
            except (Timeout, ReadTimeout):
                self.log.critical('Tiempo de espera superado.')
                raise Timeout

        def remove_from_datastore(resource_id, gtrys=0):
            """Remueve un recurdo del datastore."""
            try:
                import time
                trys = 0
                while not get_dp_status(_resource_id=resource_id) and trys > 10000:
                    trys += 1
                    time.sleep(1)
                if trys > 100:
                    self.log.warning('El servicio remoto de Datapusher no parece estar funcionando...')
                try:
                    ds_action = self.my_remote_ckan.call_action('datastore_delete', {'resource_id': resource_id,
                                                                                     'force': True})
                    return {u'resource_id': unicode(resource_id)} == ds_action
                except CKANAPIError as ckan_api_msg:
                    # print 'CKAN Err:', ckan_api_msg
                    # time.sleep(1)
                    gtrys += 1
                    if gtrys < 500:
                        time.sleep(1)
                        remove_from_datastore(resource_id, gtrys=gtrys)
                    else:
                        self.log.warning('Es imposible quitar este recurso del datastore, no existe...')
                        return True
                return False
            except Exception as e:
                self.log.error('Ocurrio un error en la limpieza de recursos...\n error:{}'.format(e))

        from models import Distribution
        status = False
        if not isinstance(_d, Distribution):
            raise TypeError('Distrubucion invalida.')
        _dis = _d.__dict__
        _dis.update({'name': _d.name,
                     'description': _d.description.decode('utf-8')})
        invalid_args = ['required_keys', 'context']
        for ia in invalid_args:
            try:
                del _dis[ia]
            except KeyError:
                pass
        import os
        push_upload = 'file' in _d.__dict__.keys()
        if push_upload:
            # Metodo UPLOAD.
            _dis.update({'upload': open(_d.file, 'rb'),
                         'url_type': 'upload',
                         'url': os.path.basename(_d.file)})

        else:
            # Metodo 'LINK'
            self.log.info('Push method: LINK')
            _dis.update({'url': _dis['url'],
                         'url_type': 'link'})
        r = False
        try:
            if update:
                _dis.update({'id': self.get_resource_id(name=_dis['name'])})
                r = self.my_remote_ckan.action.resource_update(**_dis)
            else:
                r = self.my_remote_ckan.action.resource_create(**_dis)
            if r:
                status = True

        except NotAuthorized:
            self.log.critical('No posee permisos para actualizar|crear distribuciones.')
        except ValidationError, e:
            self.log.critical('No es posible actualizar|crear la/las distribuciones con la data provista.')
            self.log.critical('CKAN Err: {}.'.format(e))
        except NotFound:
            self.log.critical('No es posible actualizar|crear la/las distribuciones,'
                              ' la informacion provista, no existe')
        if False not in [only_metadata, status, not push_upload]:
            if self.dp_available:
                self.log.info('Limpiando recurso: {}.'.format(r['id']))
                if remove_from_datastore(resource_id=r['id']):
                    status = True
                    self.log.info('hecho!')
                else:
                    self.log.critical('Ocurrio un fallo al limpiar el recurso \"{}\".'.format(r['id']))
            else:
                msg = '\n###########################ERROR###################################\n' \
                      '# Imposible utilizar esta funcion, configuracion no disponible.   #\n' \
                      '# Para utilizar la funcion de \"solo salvar metadata\" es requerido #\n' \
                      '# que configures previamente tu datapusher user:pass@host:port.   #\n' \
                      '###########################ERROR###################################\n'
                raise Exception(msg)
        if _views:
            self.clean_all_views(r['id'])
        return status

    def save(self, _obj=None,
             only_metadata=False,
             _views=True):
        """
        Guarda un _obj dentro de CKAN.

        Si el _obj existe, lo actualiza, si no, lo creo.
        De la misma manera son tratadas las distribuciones que el mismo contenga.

        Args:
            - _obj: _obj(). Objeto de que se desea salvar.
            - only_metadata: bool(). Pushear solo metadata.
            - _views: bool(). Flag. Mantener vistas remotas o eliminar.
        Returns:
             - bool():
                - True se salvo correctamente el _obj.
                - False: Fallo la carga del _obj.
        """
        from models import Dataset, Distribution
        ds_status = False
        dis_status = False
        distributions = []
        if type(_obj) not in [Dataset, list, Distribution]:
            raise TypeError
        if isinstance(_obj, list):
            # Si es una lista, solo voy a intentar salvar los
            #  que son instancias de la clase _obj.
            for o in _obj:
                if isinstance(o, (Dataset, Distribution)):
                    self.save(_obj=o,
                              only_metadata=only_metadata,
                              _views=_views)
                else:
                    # Si _obj[n] no es _obj o Distribution lo omito.
                    self.log.info('Se omite {} por no ser una instancia de '
                                  '_obj() o de Distribution.'.format(o))
        if isinstance(_obj, Dataset):
            if 'resources' in _obj.__dict__.keys():
                distributions = _obj.resources
                _obj.resources = []
            else:
                dis_status = True
            ds_name = self._render_name(title=_obj.title)

            try:
                ds_name = ds_name.decode('utf-8 ')
            except UnicodeEncodeError:
                pass

            if self.exists(id_or_name=ds_name):
                # Actualizo el _obj.
                self.log.info('El _obj \"{}\" existe, por tanto, se actualizara.'.format(ds_name))
                # Antes de actualizar debo bajar toda la metadata del dataset,
                # para que no se sobre escriba de manera erroenea el mismo al
                # realizar el update.
                ds_remote = self.freeze_dataset(ds_name)
                if self.update_dataset(dataset=self.diff_datasets(ds_remote, _obj)):
                    self.log.info('_obj \"{}\" actualizado correctamente.'.format(ds_name))
                    ds_status = True
            else:
                # Caso contrario, lo creo.
                self.log.info('El _obj \"{d}\" no existe. Creando _obj \"{d}\"...'.format(d=ds_name))
                if self.create_dataset(dataset=_obj):
                    self.log.info('_obj \"{}\" fue creado con exito.'.format(ds_name))
                    ds_status = True
            if len(distributions) > 0:
                self.log.info('Guardando distribuciones({})...'.format(len(distributions)))
                for d in distributions:
                    d.package_id = ds_name
                    self.save(_obj=d,
                              only_metadata=only_metadata,
                              _views=_views)
            return ds_status
        import helpers
        if isinstance(_obj, Distribution):
            if isinstance(_obj, Distribution):
                dist_name = _obj.name
                self.log.info('Salvando Distribucion \"{}\".'.format(dist_name))
                if self.exists(id_or_name=self._render_name(dist_name), search_for_datasets=False):
                    self.log.info('Actualizando distribucion \"{}\".'.format(dist_name))
                    if self._push_distribution(_d=_obj,
                                               only_metadata=only_metadata,
                                               _views=_views,
                                               update=True):
                        dis_status = True
                else:
                    self.log.info(
                        'La distribucion \"%s\" no existe, creando nueva distribucion.' % dist_name)
                    if self._push_distribution(_d=_obj,
                                               only_metadata=only_metadata,
                                               _views=_views):
                        dis_status = True
        elif helpers.list_of(_obj, Distribution):
            for m in _obj.__dict__.keys():
                self.save(m, only_metadata=only_metadata, _views=_views)
        return dis_status and ds_status
