from contextlib import contextmanager
from abc import ABCMeta, abstractmethod
from copy import deepcopy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.ext.automap import automap_base

class Engine():
    def __init__(self, engine=None, driver=None, username=None, password=None, host=None, database=None, dialect="mysql", port=3306, echo=False, url=None):
        
        self.engine = None
        
        if engine is not None:
            from sqlalchemy.engine.base import Engine as SqlAlchemyEngine
            if not isinstance(engine, SqlAlchemyEngine):
                raise Exception('engine has to be instance of sqlalchemy.engine.base.Engine')
            self.engine = engine
            return

#         self.dialect = dialect
#         self.driver = driver
#         self.username = username
#         self.password = password
#         self.host = host
#         self.port = port
#         self.database = database
#         self.echo = echo
#         self.url = url
        
        kargs = deepcopy(locals())
        del kargs['self']
        self.build_engin(**kargs)
    
    def build_engin(self, **karg):
        if self.engine is not None:
            return 
        self.engine = create_engine(self.build_url(**karg), echo=karg['echo'])
        
    def build_url(self, **kargs):
        if kargs['url']:
            return kargs['url']
        url = "{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}".format(**kargs)
        return url

class PaginatedResultContainer():  
    
    def __init__(self, page, items):
        
        self.page = page
        self.items = items
        
class SessionAndMapperContainer():
    
    def __init__(self, session, mapper):
        
        self.mapper = mapper
        self.session = session

class SetupEngin():
    
    def __init__(self, config=None):
        
        self.engins = {}
        if config is not None:
            self.add_engins(config)
        return
    
    #def add_engin(self, name, driver=None, username=None, password=None, host=None, database=None, dialect="mysql", port=3306, echo=False, url=None):
    def add_engin(self, name, **kargs):
        
        self.engins[name] = Engine(**kargs)
        
    def add_engins(self, engin_list):
        
        if type(engin_list) is not type([]):
            raise TypeError('engins_list must be list')
        # if one config passed, make it duplicate.
        if len(engin_list) == 1:
            engin_list[0]['name'] = ReadWriteSessionContainer.MODE_WRITE
            engin_list.append(deepcopy(engin_list[0]))
            engin_list[1]['name'] = ReadWriteSessionContainer.MODE_READ
            
        for i in engin_list:
            self.add_engin(**i)
        return
    
    def test_engins(self):
        
        for n, e in self.engins.items():
            print('Connecting {name}...'.format(name=n))
            try:
                print(e.engine)
                e.engine.connect()
                print('Success')
            except Exception as exc:
                print('Connection test failed for {name}:{exeption}'.format(name=n, exeption=exc))
            pass
        
    def __getitem__(self, name):
        
        return self.engins[name].engine

class Session():
    def __init__(self, engines):
        self.engines = engines.engins
        self.sessions = {}
        
    def get_engines(self):
        return self.engines
    
    def get_engine(self, name):
        return self.engines[name]
    
    def __getitem__(self, name):
        if name in self.sessions:
            return self.sessions[name]
        return self.__build_session(name)
    
    def __build_session(self, name):
        if name not in self.engines:
            raise KeyError('Engin name {name} not found'.format(name=name)) 
        
        self.sessions[name] = sessionmaker(bind=self.engines[name].engine)()
        return self.sessions[name]
    
class BaseUtil():
    
    print_devider = ":"
    
    def __new__(cls, *args, **kargs):
        obj = object.__new__(cls)
        obj.add_event(object=obj)
        return obj
    
    def add_event(self, object=None):
        attrs = dir(object)
        for i in attrs:
            print(i)
            if i.startswith('__event_'):
                print(i)
        pass
    
    def get_columns(self):
        return self.__table__.columns._data.keys()
    
    def __repr__(self):
        columns = self.get_columns()
        output = ""
        for c in columns:
            output += c + self.print_devider + str(getattr(self, c)) + ","
        return output
 
class ReadWriteSessionContainer(): 
    
    MODE_READ = 'read'
    MODE_WRITE = 'write'
    
    read = None
    write = None
    
    engine = None
    
    
class ModelBase(metaclass = ABCMeta):
    
    @staticmethod
    def filter(*args):
        return args
    
    def __init__(self, *args, **kargs):
        
        if 'mapper' in kargs:
            self.__mapper__ = kargs['mapper']
        
        self.session = SetupModelBase.session
        self.instant_session = None
        
        self.mapper = None
        
        self.init(args, kargs)
    
    @abstractmethod
    def init(self, *args, **kargs):
        pass
        
    def get_mapper(self):
        
        return self.__mapper__
    
#     def get_session_with_mapper(self, mode=ReadWriteSessionContainer.MODE_READ):
#         
#         if mode == ReadWriteSessionContainer.MODE_READ:
#             return self.session.read.query(self.__mapper__)
#         if mode == ReadWriteSessionContainer.MODE_WRITE:
#             return self.session.write.query(self.__mapper__)
#         raise ValueError('Invalid session mode.')

#     def session_mode(self, mode):
#         if mode != ReadWriteSessionContainer.MODE_READ and mode !=  ReadWriteSessionContainer.MODE_WRITE:
#             raise ValueError('Invalid session mode.')
#         self.current_session_mode = mode
#         print(self.current_session_mode )
#         return self
    
    @contextmanager
    def session_mode(self, mode=None, session=None):
        
        if mode:
            self.instant_session = self.get_session(mode)
        elif session:
            self.instant_session = session
        else :
            raise ValueError('Invalid session')
        
        yield
        
        self.instant_session = None
#         if session_mode is not None:
#             return self.session_mode(session_mode)
    
    def get_session(self, mode=ReadWriteSessionContainer.MODE_READ, with_mapper=False):
        
        session = None
        if self.instant_session is not None:
            session = self.instant_session
        else:
            try:
                session = getattr(self.session, mode)
            except AttributeError as e:
                raise e
#         elif mode == ReadWriteSessionContainer.MODE_READ:
#             session =  self.session.read
#         elif mode == ReadWriteSessionContainer.MODE_WRITE:
#             session = self.session.write
#         else :
#             raise ValueError('Invalid session mode.')
        
        if not with_mapper:
            return session
        #return session object with mapper(session.query({MAPPER}))
        return session.query(self.get_mapper())
    
    def get_one(self,commit=True, with_session=False, filter=None, **kargs):
        
        session = self.get_session(ReadWriteSessionContainer.MODE_READ)
        mapper = self.__filter_factory(session, filter, kargs, 'first')
        result = self.__return(session, mapper, with_session)
        
        if commit or not with_session:
            session.commit()
            
        return result
    
    def get_all(self,commit=True, with_session=False, filter=None, **kargs):
        
        session = self.get_session(ReadWriteSessionContainer.MODE_READ)
        mapper = self.__filter_factory(session, filter, kargs, "all")
        result = self.__return(session, mapper, with_session)
        
        if commit or not with_session:
            session.commit()
            
        return result

    def __filter_factory(self, session, filter, kargs, method=None):

        if filter is not None:
            
            if not isinstance(filter, tuple):
                filter = (filter,)
            
            query = session.query(self.get_mapper()).filter(*filter)
        else:
            query = self.__build_filter(session.query(self.get_mapper()), kargs)
        
        if method is not None:
            mapper = getattr(query, method)()
            return mapper
        else:
            return query
        
    def paginate(self,query, perpage, page, page_range=5):
        
        from hdv_paginator import SQLAlchemy
        
        pgn = SQLAlchemy(perpage=perpage, page=page, page_range=page_range, item=query)
        return pgn.get_items()
        
#         total_rows = 0
#         if query is not None:
#             total_rows = query.count()
#         
#         from hdv_paginator import Paginator
#         
#         pgn = Paginator(perpage=perpage, page=page, page_range=page_range, total=total_rows)
#         
#         items = query.slice(pgn.page.item_index_in_current_page[0], pgn.page.item_index_in_current_page[1]+1).all()
#         
#         return PaginatedResultContainer(page=pgn.pag, items=items)

            
    def __build_filter(self, instance, params):
        
        if params is {}:
            return instance
        
        criterion = []
        for c, v in params.items():
            if type(v) is list :
                condition = self.__mapper__.__dict__[c].in_(v)
            else :
                condition = self.__mapper__.__dict__[c] == v
            criterion.append(condition)
            
        return instance.filter(*criterion)
    
    def __return(self,session, mapper, with_session=False):
        
        if not with_session:
            return mapper
        
        return SessionAndMapperContainer(mapper=mapper, session=session)

    def insert_or_update_if_exist(self,finding_keys, object=None, **kargs):
        
        if object:
            kargs = object.__dict__
        find = {k:kargs[k] for k in finding_keys}
        
        with self.session_mode(ReadWriteSessionContainer.MODE_WRITE):
            result = self.get_one(with_session=True, **find)
            if not result['mapper']:
                return self.insert(commit=True, **kargs)
            #update row
            new_values = {}
            if object:
                new_values = object.__dict__
            else:
                new_values = kargs;
                
            for k, v in new_values.items():
                setattr(result['mapper'], k, v)
            
            result['session'].commit()
    
    def delete(self, filter=None, **kargs):
        
        if filter is None and not kargs:
            raise ValueError("Empty argument cannot be accept")
        
        session = self.get_session(ReadWriteSessionContainer.MODE_WRITE)
        query = self.__filter_factory(session, filter, kargs)
        query.delete()
        session.commit()
        
        return True

    def update(self, update={}, filter=None, mappers_with_session=None, **kargs):
        
        if mappers_with_session is not None:
            return self.__update_mappers_with_session(update, mappers_with_session)
            
        session = self.get_session(ReadWriteSessionContainer.MODE_WRITE)
        
        if filter is not None:
            query = self.__filter_factory(session, filter, kargs)
            query.update(update)
            session.commit()
            return True
        
        rows = self.get_all(with_session=True, **kargs)
        
    def __update_mappers_with_session(self, update, mappers_with_session):
        
        session = mappers_with_session['session']
        mappers = mappers_with_session['mapper']
        
        if not isinstance(mappers, list):
            mappers = [mappers]
        
        for m in mappers:
            for c, v in update.items():
                setattr(m, c, v)
        
        session.commit()
        return mappers_with_session
        
    def insert_and_commit(self, mapper_object=None, **kargs):
        
        return self.insert(True, False, mapper_object, **kargs)
    
    def insert(self, commit=False, with_session=False, mapper_object=None, **kargs):
        
        session = self.get_session(ReadWriteSessionContainer.MODE_WRITE)
        
        #insert multiple mappers
        if isinstance(mapper_object, list):
            session.bulk_save_objects(mapper_object, return_defaults=True)
            mapper = mapper_object
        else:
            if  mapper_object:
                mapper = mapper_object
            else:
                mapper = self.get_mapper()(**kargs)
                
            session.add(mapper)
        
        if commit:
            if with_session:
                raise ValueError('Cannot return session instance after commit')
            session.commit()
            return mapper
        else:
            self.mapper = mapper
            return session
    
class SetupModelBase():
    
    initialized = False
    
    session = ReadWriteSessionContainer()
    automap_base = automap_base()
    
    @staticmethod
    def set_sessions(sessions, engine, prepare_automap=True):
        if sessions['read'] and sessions['write']:
            ReadWriteSessionContainer.read = sessions['read']
            ReadWriteSessionContainer.write = sessions['write']
        else :
            ReadWriteSessionContainer.read = ReadWriteSessionContainer.write = sessions
            
        ReadWriteSessionContainer.engine = engine
        #for automap meappers 
        if prepare_automap:
            SetupModelBase.automap_base.prepare(engine, reflect=True)
        
        SetupModelBase.initialized = True
    
    @staticmethod   
    def get_automap_base():
        if SetupModelBase.initialized:
            raise Exception('SetupModelBase.automap_base.prepare() has been called. Please call set_session_config()/set_sessions() method after SetupModelBase.automap_base()')
        return SetupModelBase.automap_base
        
    @staticmethod
    def set_session_config(config, engine=None):
        engines = SetupEngin(config)
        sessions = Session(engines)
        
        if engine is None:
            engine = sessions.engines['read'].engine
            
        if sessions['read'] and sessions['write']:
            SetupModelBase.set_sessions(
                                     {
                                      'read':sessions['read'],
                                      'write':sessions['write']
                                      },
                                     engine=engine
                                     )
        else:
            raise Exception('No read and write configuration found')
            
        
class SimpleSetup():     
    
#     tables = None
#     config = None
#     mappers = None
    
    def __init__(self, config, tables):
        
        self.tables = tables
        self.config = config
        self.session = None
        self.mappers = {}
        self.__create_mappers()
        self.__create_session()
        
    def __create_mappers(self):
        
        for t in self.tables:
            self.mappers[t] = self.__create_mapper_by_table_name(t)
        pass
    
    def __create_mapper_by_table_name(self, table):
        
        return type(table, (SetupModelBase.get_automap_base(),), {"__tablename__":table})
    
    def __create_session(self):
        
        SetupModelBase.set_session_config(self.config)
        self.session = SetupModelBase.session
    
    def get_mapper(self, name):
        
        return self.mappers[name]
    
    def get_session(self):
        
        return self.session
        
        
        