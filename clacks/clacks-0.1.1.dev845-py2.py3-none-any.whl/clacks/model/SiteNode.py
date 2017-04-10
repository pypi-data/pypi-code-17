#!/usr/bin/env python3

"""SiteNode class definition."""
# pylint: disable=no-member

import re
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        func, literal, select, text)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import (ColumnProperty, aliased, backref, column_property,
                            relationship, validates, with_polymorphic)

from ..db import db
from ..tools import all_subclasses
from .Base import Base
from .Grant import Grant


class SiteNode(Base):

    """Base class for any node of site structure tree"""

    __tablename__ = 'links'
    # Unfortunately we aren't there yet:
    # __table_args__ = (
    #     UniqueConstraint('_parent', 'position'),
    #    )

    id = Column(Integer, primary_key=True)
    linkName = Column('title', String)
    _parent = Column('_parent', ForeignKey('links.id', onupdate='CASCADE',
                                           ondelete='CASCADE', deferrable=True))
    _position = Column('position', Integer,
                       server_default=text("currval(('links_id_seq'::text)::regclass)"))
    visible = Column(Boolean)
    lang = Column(String(8))  # ForeignKey('languages.iso_code'))
    type = Column(String(32))
    placement = Column('placement', String(32))
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now())

    _editGrant = Column('edit_grant', ForeignKey('grants_dictionary.id', onupdate='CASCADE',
                                                 ondelete='SET NULL', deferrable=True))
    _viewGrant = Column('view_grant', ForeignKey('grants_dictionary.id', onupdate='CASCADE',
                                                 ondelete='SET NULL', deferrable=True))
    _addNodeGrant = Column('add_node_grant', ForeignKey('grants_dictionary.id', onupdate='CASCADE',
                                                        ondelete='SET NULL', deferrable=True))

    editGrant = relationship('Grant', foreign_keys=[_editGrant])
    viewGrant = relationship('Grant', foreign_keys=[_viewGrant])
    addNodeGrant = relationship('Grant', foreign_keys=[_addNodeGrant])

    __mapper_args__ = {'polymorphic_on': type}

    _parentObj = relationship('SiteNode',
                              remote_side='SiteNode.id',
                              backref=backref('childNodes',
                                              order_by='SiteNode._position',
                                              collection_class=ordering_list('_position')))

    # alternative relationship if subquery usage matters and speed counts
    childNodesQuery = relationship('SiteNode',
                                   lazy='dynamic',
                                   remote_side='SiteNode._parent',
                                   order_by='SiteNode._position')

    def viewGranted(self, user):
        """check if given user can view this node"""
        if not self.viewGrant:
            return self.parent.viewGranted(user) if self.parent else True

        if self.viewGrant.name == 'ANONYMOUS':
            return True
        elif not user:
            return False
        else:
            return user.granted(self.viewGrant)

    def editGranted(self, user):
        """check if given user can view this node"""
        # anonymous editions are not allowed no matter what
        if not user:
            return False

        if not self.editGrant and self.parent:
            return self.parent.editGranted(user)

        # by default only SITE_ADMIN has edition rights; if it is given to
        # 'ANONYMOUS' it is probably by some mistake so let's prevent it
        if not self.editGrant or self.editGrant.name == 'ANONYMOUS':
            return user.granted('SITE_ADMIN')
        else:
            return user.granted(self.editGrant)

    def addNodeGranted(self, user):
        """check if given user can add new node to this one"""
        # anonymous additions are not allowed no matter what
        if not user:
            return False

        if not self.addNodeGrant and self.parent:
            return self.parent.addNodeGranted(user)

        # by default only SITE_ADMIN has edition rights; if it is given to
        # 'ANONYMOUS' it is probably by some mistake so let's prevent it
        if not self.addNodeGrant or self.addNodeGrant.name == 'ANONYMOUS':
            return user.granted('SITE_ADMIN')
        else:
            return user.granted(self.addNodeGrant)

    def __init__(self, **kwargs):
        # for some reason ordering_list has problems with setting parent in constructor
        if 'parent' in kwargs:
            raise ValueError('setting parent from constructor not supported yet')
        if 'placement' in kwargs:
            raise ValueError('setting placement from constructor not supported yet')
        super().__init__(**kwargs)

    def delete(self):
        """ safe removal function applying some additional cleanups
        """
        db.expire_all()
        for node in self.childNodes:
            node.delete()
        for control in self.controls:
            control.delete(wholePage=True)
        db.delete(self)
        db.flush()
        self.reorder()

    @hybrid_property
    def position(self):
        """ position attribute is read only, as changes should be done
        indirectly by manipulating parent object's childNodes property
        """
        return self._position

    @validates('placement')
    def validate_placement(self, key, placement):  # pylint: disable=unused-argument
        """Validate if placement is among allowed ones."""
        if (placement is not None) and (placement not in self.placements()):
            raise ValueError('Given placement not allowed for this node (%s): %r' %
                             (self.linkName, placement))
        return placement

    @hybrid_property
    def parent(self):
        """Return parent node."""
        return self._parentObj

    @parent.setter
    def parent(self, parent):
        """Set parent node."""
        if self._parentObj != parent:
            if not isinstance(parent, SiteNode):
                raise ValueError('Unsupported class of parent node')
            parent.childNodes.append(self)
            placements = list(self.placements().keys())
            if self.placement not in placements:
                self.placement = placements[0] if len(placements) == 1 else None
            self.refreshSubtree()

    def linkNameCut(self, dlen):
        """Return link name reduced to length given"""
        if len(self.linkName) <= dlen:
            return self.linkName
        short = re.sub(r'^(.*)\W(.*)$', r'\1', self.linkName[:dlen-2], flags=re.UNICODE)
        return (short if len(short) else self.linkName[:dlen-3])+'...'

    @staticmethod
    def reorder(parent=None):
        """Normalize link position numbers
        across the whole table or for the given parent node
        (its left for emergency use only, as current code
        should always produce normalized values)
        """

        # UPDATE links SET position=t1.newpos FROM (
        #     SELECT id, row_number() OVER (
        #         PARTITION BY _parent ORDER BY position) AS newpos FROM links) AS t1
        #   WHERE links.id = t1.id AND links._parent=:parent

        sq = (select((SiteNode.id, func.row_number()
                      .over(partition_by="_parent", order_by="position")
                      .label('pos')))
              .alias('foo'))

        query = db.query(SiteNode).filter(SiteNode.id == sq.columns.id)

        if parent:
            query = query.filter(SiteNode._parent == parent.id)

        query.update({SiteNode.position: sq.columns.pos-1})
        db.flush()

    def copyTo(self, node):
        """ returns a new node being cloned from this one
        with all controls cloned as well and parent set to the argument given
        """
        result = type(self)(**{
            c.key: getattr(self, c.key)
            for c in self.__mapper__.iterate_properties
            if (isinstance(c, ColumnProperty) and
                all(isinstance(b, Column) for b in c.columns) and
                c.key not in ['id', '_parent', '_position', 'placement'])})
        db.flush()
        node.childNodes.append(result)

        for ctrl in self.controls:
            result.controls.append(ctrl.clone())
            db.flush()

        try:
            result.placement = self.placement
        except ValueError:
            placements = result.placements().keys()
            result.placement = placements[0] if len(placements) == 1 else None

        db.flush()
        return result

    def deepCopyTo(self, node):
        """Clone whole subtree of the site to the new location."""
        newnode = self.copyTo(node)

        for child in self.childNodes:
            child.deepCopyTo(newnode)

        return newnode

    def refreshSubtree(self):
        """Walk whole stubtree calling itself on each node,
        it's needed by PageNode and its derivatives which specialize
        it to actually do something useful like rebuilding urls
        """
        for child in self.childNodes:
            child.refreshSubtree()

    def export(self):
        """return JSON compatible dictionary of node state."""
        result = {attr: getattr(self, attr) for attr in
                  ['id', 'linkName', 'visible', 'lang', 'type',
                   'placement', 'childNodesCount', '_parent', 'position']}
        result.update({g: getattr(self, g).name if getattr(self, g) else ''
                       for g in ['editGrant', 'viewGrant', 'addNodeGrant']})
        return result

    def update(self, items):
        """Update object's attributes from dictionary"""
        parent = self.parent
        for key in items.keys():
            if key in ['linkName', 'visible', 'placement']:
                setattr(self, key, items[key])
            if key in ['editGrant', 'viewGrant', 'addNodeGrant']:
                setattr(self, key, Grant.get(items[key])
                        if items[key] else None)

        if ('position' in items) and (int(items['position']) != self.position):
            newpos = int(items['position'])  # just in case
            if newpos > self.position:
                newpos -= 1  # needed with parent.childNodes.pop()

            parent.childNodes.remove(self)
            parent.childNodes.insert(newpos, self)
            db.flush()

        if ('_parent' in items) and (items['_parent'] != self._parent):
            raise NotImplementedError()

        self.modified = func.now()
        db.flush()

    @property
    def parents(self):
        """Generator over parent objects"""
        while self.parent:
            yield self.parent
            self = self.parent

    def _placementPath(self):
        """Construct full placement path in as config compatible string."""
        return ':'+':'.join([a.placement or 'none' for a in list(self.parents)[::-1]])

    def placements(self):
        """Returns list of placements this node can be set to.

        It's obtained by comparing node placement path built from
        parent nodes placements with config file entries, namely their
        parent-allow lists of regular expressions and "supports" lists
        containing page types. "supports" can be negated by placing "!"
        as one of elements or missing or empty to allow any node type.
        """

        from gtcms.core import cfg

        allPlacements = cfg.get('page', 'placements', default=None)
        myPath = self._placementPath()

        return {
            key: val.get('name', '[%s]' % key)
            for key, val in allPlacements.items()
            if (any(re.search(regex+'$', myPath)
                    for regex in val['parent-allow']) and
                (((self.type in val.get('supports', [])) != ("!" in val.get('supports', []))) or
                 'supports' not in val))}

    def getMenuTree(self, placements, maxdepth=None, visible=True):
        """Return dictionary of {'node': SiteNode, 'children': []} dicts
        for a given criteria keyed on SiteNode.id.

        Function generates part of site tree based on given criteria
        @arg placements - iterable of page types (locations)
        If first element is sole '!', then works as negation.
        @arg maxdepth depth of generated tree, unlimited if set to None
        @arg visible select only nodes with visible attribute set to a given value
        (if None, select all nodes), @default True
        """

        basequery = db.query(SiteNode.id.label('id'), literal(1).label('depth'))\
                      .filter_by(id=self.id)\
                      .cte(name='base', recursive=True)
        basealias = aliased(basequery, name='base2')
        unionquery = db.query(SiteNode.id.label('id'), (basealias.c.depth+1).label('depth'))\
                       .filter(SiteNode._parent == basealias.c.id)

        if maxdepth:
            unionquery = unionquery.filter(basealias.c.depth < maxdepth)

        if visible is not None:
            unionquery = unionquery.filter(SiteNode.visible == visible)

        if placements:
            if placements[0] == '!':
                unionquery = unionquery.filter(SiteNode.placement.notin_(placements[1:]))
            else:
                unionquery = unionquery.filter(SiteNode.placement.in_(placements))

        unionalias = aliased(basequery.union_all(unionquery), name='nodeids')

        query = db.query(with_polymorphic(SiteNode, SiteNode.__subclasses__()))\
                  .join(unionalias, SiteNode.id == unionalias.c.id)\
                  .order_by(unionalias.c.depth, SiteNode._position)
        nodes = query.all()
        byid = {node.id: [] for node in nodes}
        for node in nodes:
            if node != self:
                byid[node._parent].append(node)

        return byid

    def getAppendableControls(self):
        """return all Contols and their placements appendable to this SiteNode."""
        from .Control import Control
        result = ({'control': ctrl,
                   'placements': ctrl.getAppendablePlacements(self)}
                  for ctrl in all_subclasses(Control))
        return [r for r in result if r['placements'] != []]


__sntable = SiteNode.__table__.alias()
SiteNode.childNodesCount = \
    column_property(select([func.count(__sntable.c._parent)],
                           __sntable.c._parent == SiteNode.id).correlate(SiteNode.__table__),
                    deferred=True)
