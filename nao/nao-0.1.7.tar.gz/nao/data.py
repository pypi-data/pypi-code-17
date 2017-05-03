
import numpy as np
import decimal as dec

import itertools

from inspect import isclass, getmro

from . import logger, benchmark, odict

from sqlalchemy.types import DateTime, Date
from sqlalchemy.types import Integer, BigInteger, Float, Numeric, Boolean, Enum
from sqlalchemy.types import String, Text, Unicode, UnicodeText
from sqlalchemy.schema import Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declared_attr

log = logger(__name__)


# TODO need to centralize resource loading (query and Excel)
# to ensure data integrity


class LoaderError(Exception): pass

class LoadableMixin(object):
    """
    This is the Basic mixin that performs loading functionality

    This should be created similarly to declarative base otherwise
    shared among all model classes in the same interpreter process

    """
    __loader__ = None  #: override class attribute in subclasses
    __loader_args__ = {} #: loading arguments shared by subclasses

    @classmethod
    def load(cls, params=None, ranges=None):
        """
        """
        metadata = get_metadata(cls)

        for pars in cls._parse_ranges(ranges, params):

            s = cls._get_session(pars, metadata)

            res = cls._load(pars)

            s.bulk_insert_mappings(c, res)

            s.commit()
            s.close()


    @classmethod
    @benchmark
    def load_all(cls, params=None, ranges=None):
        """

        `params`
        These params are used to prepare sql-statements 


        `ranges`
        Used to iterate through ranges (preferably an `odict`)
        """
        # TODO somehow stop relying on table names

        loader_classes, metadata = sorted_subclasses(cls)
        log.debug("loader classes: {}".format(loader_classes))
        log.debug("metadata: {}".format(metadata))

        for pars in cls._parse_ranges(ranges, params):

            s = cls._get_session(pars, metadata)

            cache = cls._load_all(loader_classes, pars)

            # bulk insert chould operate separately by the cache
            for key, res in cache.items():
                c = loader_classes[key]
                s.bulk_insert_mappings(c, res)

            s.commit()
        
            # TODO implement row-by-row insert for debugging
            # for row in res:
            #     s.bulk_insert_mappings(self.cls, [row])
            #     s.commit()
            s.close()


    @classmethod
    def _load(cls, params=None):
        """
        Get classes, no ranges, no session
        
        return cls objects loaded from engine

        """
        # TODO use only __loader__args__ instead
        if isinstance(cls.__loader__, Loader):
            # delegate task to loader object
            log.debug('Loading for model class: {}'.format(cls))

            return cls.__loader__.load(cls, params)

        else:
            # rasie some more sensible error
            log.info("{} is not loadable!".format(cls))
        


    @classmethod
    def _load_all(cls, loader_classes, params):
        """
        Get classes, no ranges, no session

        Implement implicit foreign keys
        """
        # TODO use cache only if there is implicit foreign
        cache = odict()
        implicit_foreign = []

        for tname, klass in loader_classes.items():

            # relies on _load here
            log.debug("Loading classes for {} and {}".format(tname, klass))
            res = klass._load(params)

            cache[tname] = res

            for r in inspect(klass).relationships:

                # TODO what if related class is not in loader classes
                rtbl = r.target.name

                # check if target allows imlicit foreign key addition
                if (
                    rtbl in loader_classes and
                    issubclass(loader_classes[rtbl], ImplicitForeignMixin)
                    ):
                    # target should already exist in the cache because of sorted_tables
                    implicit_foreign.append((klass, r))
                    

            # TODO For DiffLoader check existence here
            # New (add new items with insert_date)
            # Match (implicit records should drop, others update_date)
            # Delete (no actual deletion only delete_date)


        # making implicit foregin key happen
        # TODO many to many??? association proxies???
        # TODO not null howto?

        log.debug("Searching implicit foreign keys...")

        def get_index(table, keys):
            """
            TODO might implement caching of indices here
            """
            index = []
            for row in cache[table.name]:
                index.append(tuple([row[k] for k in keys]))
            return index

        for klass, relation in implicit_foreign:
            # source is the table with foreign_keys to target

            fks, pks = tuple(zip(*[(l.name, r.name) for l, r in relation.local_remote_pairs]))
            # print(fks, pks)
            # target is accepting new records with implicit_foreign flag
            target_index = get_index(relation.target, pks)
            # print(target_index)
            target_class = loader_classes[relation.target.name]

            for row in cache[klass.__tablename__]:
                ind = tuple([row[k] for k in fks])
                if any([i is None for i in ind]): continue

                # print(ind)
                if ind not in target_index:

                    log.warning("Implicit Foreign {} ({}) from table {}".format(
                        relation.target.name,
                        ", ".join([str(i) for i in ind]),
                        klass.__tablename__
                    ))

                    new_row = dict((k,v) for k,v in zip(pks, ind))
                    new_row[IMPLICIT_FOREIGN] = True
                    cache[relation.target.name].append(new_row)

                    # update target_index
                    target_index.append(ind)
                    # target_class.add_implicit_foreign(ind) # return a dict...

            # read all data from klass and check if already in target_data

        return cache


    @classmethod
    def _parse_ranges(cls, ranges, params):

        if ranges is not None:

            names, iterables = ranges.keys(), ranges.values()

            # initialize all parameters once with a Carthesian product
            prod = itertools.product(*iterables)

            for vector in prod:
                
                d = dict(zip(names, vector))

                log.info("LOADING values: {}".format(d))

                p = params.copy()
                p.update(d)


                log.debug("loading params: {}".format(p))
                yield p


        # simply loading with params
        else:
            log.debug("loading params: {}".format(p))
            yield params



    @classmethod
    def _parse_data(cls, data,
        return_raw_dict=True,
        position_based=True,
        only_one_row=False,
        ):
        """
        returns a list of dicts

        validated and coerced to the corresponding model
        """

        # TODO remove columns with special usage
        columns = cls.__table__.columns
        log.debug("Parsing column {}".format(columns))

        res = []

        if only_one_row:
            data = [data]

        # TODO if slow then pandas might use some C magic for this but I doubt (should check)
        i, j = 0, 0  # if the resultproxy has no rows...

        for i,row in enumerate(data):
            # allow extra columns at the end with default values or null
            if position_based and len(row) > len(columns):
                raise ValueError("Degenarate raw (col count mismatch)")

            new_row = {}

            # log.debug("The {} raw row: {}".format(i, row))

            for j,col in enumerate(columns):

                if position_based:
                    # it is OK to have extra columns at the end
                    if j >= len(row): break
                    val = row[j]

                elif col.name in row:
                    # name based could have extra rows anywhere
                    val = row[col.name]
                else:
                    log.warning("Column {} missing for row {}".format(col.name, i))
                    continue

                if val is not None:
                    try:
                        val = cls._parse_value(val, col)
                    except:
                        log.error("row {}, col {}, value [{}], type {}".format(i, j, row[j], type(row[j])))
                        log.error("COLUMN {} ({}) pk: {}".format(col.name, col.type, col.primary_key))
                        raise

                # log.debug("Value parsed for {}: {}".format(col.name, val))
                new_row[col.name] = val

            if return_raw_dict:
                res.append(new_row)
            else:
                res.append(cls(**new_row))

        log.debug("Parsed {} rows with {} columns".format(i+1, j+1))

        if only_one_row:
            return res[0]
        else:
            return res


    @staticmethod
    def _parse_value(val, col):

        # TODO check foreign keys for uniqueness and no None!
        # if c.foreign_keys:
        #     log.debug("Foreign keys for {} are {}".format(c.name, c.foreign_keys))

        # TODO think about primary key column check
        # TODO think about unique constraint check

        # determine numerical input types
        raw_numeric_types = (int, dec.Decimal, float)

        # SQLalchemy types categorized
        numeric_types = (Integer, BigInteger, Numeric, Float)
        date_types = (Date, DateTime)
        string_types = (String, Unicode, Text, UnicodeText)
        bool_types = (Boolean, )

        # very lazy approach to bool casting
        true_vals = (True, 'Y', 'I', 1, '1')  
        # false_vals = (False, 'N', 'N', 0, '0')

        # numeric types only go to numeric types
        if isinstance(val, raw_numeric_types):
            if isinstance(col.type, numeric_types):
                pass
                # TODO check for possible precision loss
                # log.debug("Casting numeric to numeric")
                # val = dec.Decimal(str(val)) OR let the engine do that :)

            elif isinstance(col.type, string_types):
                log.warning("Casting numeric to string")
                orig = val
                val = str(val)
                if col.type.length is not None and len(val) > col.type.length:
                    val = val[:col.type.length]
                    # remove unnecessary end zeros...
                    if orig != type(orig)(val):
                        raise ValueError("COLUMN {} would have been truncated {}".format(col.name, val))


            else:
                raise ValueError("Casting numeric to non-numeric!")

        # str and anything except for numeric and None
        else: 
            if isinstance(col.type, date_types):
                val = pd.to_datetime(val)
                # TODO stp using pd
                # TODO unrealistic date (what is realistic? (today +/- 120 years)
            # series.between(left, right)

            elif isinstance(col.type, numeric_types):
                # Everything casted to Decimal to avoid precision problems, only one conversion occurs at the SQL side
                if val.startswith('0'):
                    log.warning("Converting '0' starting strig to numeric")
                # check dtypes and issue warnings
                val = dec.Decimal(val)

            elif isinstance(col.type, string_types):
                val = val.strip()
                # callback mechanism for maximum string length in column! (self._callback_string_length)
                # check string and unicode columns length attribute
                if col.type.length is not None and len(val) > col.type.length:
                    raise ValueError("COLUMN {} would have been truncated {}".format(col.name, val))


            elif isinstance(col.type, bool_types):
                val = val in true_vals

        return val


    @staticmethod
    def _get_session(params, metadata):

        te = params.pop('target_engine', None) or metadata.bind

        if not te:
            raise ValueError("no target engine")

        log.debug('Target engine: {}'.format(te))
        
        return sessionmaker(bind=te)()


IMPLICIT_FOREIGN = 'implicit_foreign'

class ImplicitForeignMixin(LoadableMixin):
    """
    This class is mainly an indicator to initiate
    impliciet loading mechanism based on the foreign keys
    of other `Loadable` classes of the same `LoadableBase`.

    Adds a `Column` by the name defined in `IMPLICIT_FOREIGN`
    constant.
    """


def anon(cls):
    return None


# TODO remove column from load iteration!
# PATCH using `declared_attr` moves it to the end otherwise
# `column_instance._create_order` defines or need to flag mixin
# columns otherwise


setattr(ImplicitForeignMixin, IMPLICIT_FOREIGN, declared_attr(lambda cls: Column(Boolean, default=False)))


def sorted_subclasses(cls):
    """
    the collecting mechanism is that the classes
    should be inherited from the caller

    TODO change that they should inherit from
    Base and have a __loader__ attribute
    create Base.metadata.load_all() somehow
    """

    # get all subclasses that should have a __tablename__:
    lst = odict()

    for c in subclasses(cls):
        print('scls', c)
        if hasattr(c, '__tablename__'):
            lst[c.__tablename__] = last_cls = c
            

    # get metadata
    metadata = get_metadata(last_cls)
    
    loader_classes = odict()

    if metadata:
        for t in metadata.sorted_tables:
            if t.name in lst:
                loader_classes[t.name] = lst[t.name]

        return loader_classes, metadata

    else:
        raise ValueError("No metadata found :(")


def subclasses(cls):
    for subclass in cls.__subclasses__():
        yield subclass
        yield from subclasses(subclass)


def get_metadata(cls):
    """
    _declared_class_registry might be safer...
    """
    for c in cls.__mro__:
        print('mro', c)
        if hasattr(c, 'metadata'):
            return c.metadata



import pandas as pd  # TODO REMOVE pandas dependency!


class Loader(object):
    """
    Base class for all the loading functionality

    This could be an abstract base clas
    """
    pass


class ParamLoader(Loader):
    
    def __init__(self, **kwds):
        """
        """
        self.kwds = kwds


    def load(self, model_class, params):

        self._get_config(model_class, params)

        self.model_class = model_class
        self.table = model_class.__table__

        # debug usually from load or load_all call
        self.debug = self.cfg.pop('debug', False)

        self.tbl = model_class.__table__
        # log.debug(tbl)

        # call class specific loader mechanism
        return self._load()


    def _get_config(self, cls, params):
        x = cls.__loader_args__.copy()
        x.update(self.kwds)
        x.update(params)
        self.cfg = x




class SQLLoader(ParamLoader):


    @staticmethod
    def prepare_sql(sql, **params):
        sql = sql.strip()
        if sql.endswith(';'): sql = sql[:-1]
        sql = sql.format(**params)
        return sql


    def _load(self):

        cfg = self.cfg
        # get engine
        engine = cfg.get('source_engine')

        # INFO no defaults needed as if there is it should be in the
        # SQL (otherwise a cfg called params could be used)
        sql = cfg.get('load_sql')
        # create prepare sql class which use parameter inclusion
        # might wanna check sqlalchemy syntax for that!
        sql = self.prepare_sql(sql, **cfg)
        # log.debug(sql)
        
        # read sql
        res = self.model_class._parse_data(engine.execute(sql))
        # res = self._read_sql_slow(sql, engine)

        # search duplicates
        if self.debug:

            import pandas as pd

            df = pd.DataFrame(res)
            pks = [c.name for c in self.table.columns if c.primary_key]
            log.debug("primary key: {}".format(pks))
            dpl = df.duplicated(subset=pks, keep=False)
            if dpl.any():
                log.debug("DUPLICATE: {}".format(df.duplicated(subset=pks).any()))
                df[dpl].to_csv('dupidup.csv')
                # TODO make output filename more sane

        # TODO add callback mechanism for other tables
        # for c in self.cls.__table__.columns:
        #     if c.foreign_keys:
        #         log.debug("Foreign keys for {} are {}".format(c.name, c.foreign_keys))

        return res


    


class ExcelLoader(ParamLoader):
    

    def _load(self):
        """
        Excel load mechanism using pandas for quick implementation
        """

        return

        cfg = self.cfg

        path = cfg.get('path')
        sheet = cfg.get('sheet', None)
        cols = cfg.get('columns', None)


        import pandas as pd

        xl = pd.ExcelFile(path)
        # print(xl.sheet_names)

        df = xl.parse(sheet if sheet is not None else 0)

        # filter by cols here

        users = df.to_dict(orient='records')

        groups = {}

        ret = []

        def get_group(name):
            if name not in groups:
                groups[name] = Group(name=name)
            
            return groups[name]

        for u in users:

            c = dict(
                login_ldap = u['id'],
                email = u['email'],
                name_first = u['first'],
                name_last = u['last'],
                name_title = u['title'],
                name_nick = u['nick'],
                name_hanzi = u['hanzi'],
                tele_ext = str(u['ext']),
                tele_mobile = u['mobile'],
                # name_nick = u['nick'] if u['nick'] else None,
                )

            # c = cls(**c)

            # Membership(c, get_group(u['department']), u['order'])

            ret.append(c)

        return ret

class DiffLoader(ParamLoader):
    pass


class SQLDiffLoader(SQLLoader, DiffLoader):
    """
    Search for new items based on primary key

    Auto-add functionality if pk is missing
    (tricky it should be used from other table loaders!!!)
    TODO

    TODO Implement callback functionality to add missing entities
    """












#############################################################
# OLD LOADER based on Pandas
# It was not working mainly due to mixed types row handling difficulties

# @benchmark
# def _parse_sql(self, sql, engine):
#     """
#     TODO not in use anymore
    
#     Cannot be significantly faster as it is necessary to read data into memory
#     for conversions
#     """
#     # coerce_float=False ensures all dtypes are object_
#     with benchmark("Reading data into memory..."):
#         df = pd.read_sql(sql, engine, coerce_float=False)

#     # TODO create own describe based on pandas
#     # show more sophisticated data
#     log.debug("Describing dataframe before conversion:")
#     log.debug(df.describe(include='all'))

#     log.debug("Datatypes of dataframe:")
#     log.debug(df.dtypes)

#     # print(df)

#     col_names = [c.name for c in self.cls.__table__.columns]
#     df.columns = col_names
#     # TODO check compatibility of dimensions

#     index = []
#     for i, c in enumerate(self.cls.__table__.columns):

#         log.debug("COLUMN {} ({}) pk: {}".format(c.name, c.type, c.primary_key))
#         # df[c.name] = df[c.name].astype(str)

#         col = df[c.name] # working with one col at a time
#         col = col[pd.notnull(col)] # working with not None only

#         print(col)

#         # TODO check foreign keys for uniqueness and no None!
#         if c.foreign_keys:
#             log.debug("Foreign keys for {} are {}".format(c.name, c.foreign_keys))


#         if isinstance(c.type, (Date, DateTime)):
#             col = pd.to_datetime(col)
#             # TODO unrealistic date (what is realistic? (today +/- 120)
#             # series.between(left, right)

#         elif isinstance(c.type, (Integer, BigInteger, Numeric, Float)):
#             # Everything casted to Decimal to avoid precision problems, only one conversion occurs at the SQL side
#             if col.str.startswith('0').any():
#                 log.warning("Converting '0' starting strig to numeric")
#             # check dtypes and issue warnings
#             col = col.astype(dec.Decimal)
#             # pd.to_numeric(df[c.name], errors='coerce')  
#             # df.ix(pd.notnull(df[c.name]), c.name).astype(dec.Decimal) #
#             # df[c.name].replace(pd.nan, None, inplace=True)

#         elif isinstance(c.type, (String, Text, Unicode, UnicodeText)):
#             col = col.str.strip()
#             mx = col.str.len().max()  # .map(len).max() is quicker a bit
#             log.debug("COLUMN {} max length: {}".format(c.name, mx))
#             # check string and unicode columns length attribute
#             if mx > c.type.length:
#                 raise ValueError("COLUMN {} would have been truncated".format(c.name))


#         elif isinstance(c.type, (Boolean, )):
#             col = col.astype('bool')  # remove none!
#             # Allow Y-N, 0-1, True-False conversion explicitly

#         #   print(i.enums)

#         df[c.name] = col # write back parsed col
        

#     # to_numeric introduce np.nan -> monkey-patch:
#     # df = df.where(pd.notnull(df), None) # notnull selects the elements NOT replaced
#     # TODO move this to to_dict somehow as in a simple dict no np.nan should occur...

#     # show more sophisticated data
#     log.debug("Describing dataframe after conversion:")
#     log.debug(df.describe(include='all'))

#     log.debug("Datatypes of dataframe:")
#     log.debug(df.dtypes)

#     # print(df)
        
#     # convert to dictionary works only without using index
#     # df.set_index(index, inplace=True)

#     # custom df.to_dict
#     res = []
#     for df_row in df.itertuples():
#         r = {}
#         for i,c in enumerate(col_names):
#             r[c] = df_row[i]
#         res.append(r)

#     return res

#     # return df.to_dict(orient='records')  # avoid indices for this operation!
