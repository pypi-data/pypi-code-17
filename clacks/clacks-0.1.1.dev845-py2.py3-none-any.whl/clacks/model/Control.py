#!/usr/bin/env python3

"""Control base class."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import backref, relationship

from ..core import ROOTPATH, cfg
from ..db import db
from ..tools import all_subclasses, json, parse_decorated_json
from .Base import Base
from .ControlProperty import ControlProperty


class Control(Base):

    """Control base class."""

    __tablename__ = 'controls'

    id = Column(Integer, primary_key=True)
    _class = Column('class', String(32))
    _page = Column(ForeignKey('links.id', onupdate='CASCADE', ondelete='CASCADE'))
    placement = Column(String(16))
    _priority = Column('priority', Integer)
    dynamic = Column(Boolean, server_default='true')
    enabled = Column(Boolean, server_default='true')
    page = relationship('SiteNode',
                        foreign_keys=[_page],
                        backref=backref('controls', order_by=_priority,
                                        cascade="save-update, merge, delete",
                                        collection_class=ordering_list('_priority')))

    # properties are obsolete and shouldn't be used anymore
    properties = association_proxy('_properties', 'value',
                                   creator=lambda k, v: ControlProperty(name=k, value=v))
    data = Column(JSONB)

    __mapper_args__ = {'polymorphic_on': _class}

    _settings = {}

    editMode = 'IFrame'  # other supported values: None, 'ControlPane'

    def delete(self, wholePage=False):  # pylint: disable=unused-argument
        """Simple stub for safe control removal that may be overriden by subclasses as needed.

        @wholePage says whether control is removed alone or as part of whole page removal
        """
        db.delete(self)
        db.flush()

    @classmethod
    def controlName(cls):
        """Returns control name, needs to be implemented by subclasses."""
        raise NotImplementedError('Method not implemented for class %s', (cls.__name__,))

    @property
    def name(self):
        """ By default shows controlName() but may be customized
        to give more informations about control's contents """

        return self.controlName()

    def getValue(self, name):
        """ temporary solution for a problem of additional control properties
        needed until migration to hstore will be possible """

        found = [a for a in self.properties if a.name == name]
        return found[0].value if found else None

    def export(self):
        """Return JSON compatible dictionary of object state."""
        result = {}
        result.update(self.properties)
        result.update({attr: getattr(self, attr) for attr in
                       ['id', 'name', '_page', 'placement', '_class', '_priority', 'dynamic',
                        'editMode', 'enabled', ]})
        return result

    def update(self, args):
        """Simple update, needs to be extended in subclasses."""
        if 'enabled' in args:
            self.enabled = bool(args['enabled'])

    def clone(self):
        """ smart cloning """
        newone = self.__class__(placement=self.placement,
                                dynamic=self.dynamic,
                                enabled=self.enabled)
        newone.properties = self.properties
        return newone

    def startup(self, node):
        """Called before any .fetch(placement) is called
        to allow additional preparations that would be too costly for
        the constructor
        @arg node - PageNode for which control is about to be rendered,
        may be different than one from database relation, as control may
        be rendered from PageMeta
        """
        self.contextPage = node  # pylint: disable=attribute-defined-outside-init

    @property
    def placements(self):
        """Default placement definition (matches most subclasses needs)
        """
        return [self.placement]

    @classmethod
    def getIdentity(cls):
        """return class identity as stored in database (currently class name
        with …Control stripped out)."""
        return cls.__mapper_args__['polymorphic_identity'] \
            if 'polymorphic_identity' in cls.__mapper_args__ else None

    @classmethod
    def getAppendablePlacements(cls, node):
        """return list of placements to which this control can be added
        for a given SiteNode"""

        from .SiteNode import SiteNode

        settings = cls._settings

        if settings.get('one-per-page', False) and \
           any(isinstance(p, cls) for p in node.controls):
            return ()

        if settings.get('one-per-language', False) and \
           db.query(Control).join(SiteNode).filter(SiteNode.lang == node.lang,
                                                   Control._class == cls.getIdentity()).count():
            return ()

        # pylint: disable=too-many-boolean-expressions
        if (settings.get('node-types', None) is not None and
            (list(settings['node-types']) == [] or
             (settings['node-types'][0] == '!' and node.type in settings['node-types']) or
             (settings['node-types'][0] != '!' and node.type not in settings['node-types']))):
            return ()

        # no default, each control needs to have this entry in config
        return cfg.get('controls', 'placements', cls.getIdentity()) if cls.getIdentity() else ()

    @classmethod
    def setDefaultPlacements(cls):
        """generate automatic configuration containing default placements for controls missing ones,
        based on cls._settings dictionary.

        This method is called from bin/update script.
        It is implemented this way, to allow defaults to change of new deployments without risk
        of breaking old projects.
        """
        config = None
        cfgpath = ROOTPATH/'config/_automatic.json'
        for ctrl in all_subclasses(cls):
            if cfg.get('controls', 'placements', ctrl.getIdentity(), default=None) is None and \
               'default-placements' in ctrl._settings:
                if not config:
                    if cfgpath.is_file():
                        with cfgpath.open() as fp:
                            config = parse_decorated_json(fp.read())
                    else:
                        config = {}
                    if 'controls' not in config:
                        config['controls'] = {}
                    if 'placements' not in config['controls']:
                        config['controls']['placements'] = {}
                config['controls']['placements'][ctrl.getIdentity()] = \
                    ctrl._settings['default-placements']

        if config:
            with cfgpath.open('w') as fh:
                fh.write("//-*- js -*-\n"
                         "// this file is automatically created by update script\n"
                         "// it's contents need to be moved to _common.json\n"
                         "var dummy = ")
                json.dump(config, fh, indent=4, sort_keys=True, ensure_ascii=False)
                fh.write(';\n')
