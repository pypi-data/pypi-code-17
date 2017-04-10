#!/usr/bin/env python3

"""Tag class."""

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from .Base import Base

control_tags = Table(
    'tags2controls', Base.metadata,
    Column('_tag', ForeignKey('tags.id', onupdate='CASCADE', ondelete='CASCADE'),
           primary_key=True),
    Column('_control', ForeignKey('controls.id', onupdate='CASCADE', ondelete='CASCADE'),
           primary_key=True)
)


class Tag(Base):
    """Tag class."""

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    comment = Column(Text)

    controls = relationship('Control', secondary=control_tags,
                            backref=backref("tags",
                                            collection_class=attribute_mapped_collection('name')))

"""
class Tag {

    public static function addTagToControl(Tag $tag, GtControl $control) {
        // how about writing real OO code?
        return self::addToControlById($tag, $control->getId());
    }

    public static function addTagToControlById(Tag $tag, $controlid) {
        // how about writing real OO code?
        return PgDB::set('tags2controls',
                         ['_tag' => $tag->id,
                          '_control' => $controlid],
                         ['_tag' => $tag->id,
                          '_control' => $controlid]);
    }

    public function addToControl(GtControl $control) {
        return self::addTagToControl($this, $control);
    }

    public function addToControlById($controlid) {
        return self::addTagToControlById($this, $controlid);
    }

    public static function setControlTags(Gtcontrol $control, $tags) {
        if (!is_array($tags)) {
            $tags = explode(',', $tags);
        }

        PgDB::execute('DELETE FROM tags2controls WHERE _control=?', $control->getId());
        foreach($tags as $tag) {
            if (!($tag instanceof Tag)) {
                $tag = trim($tag);
                if ($tag == '') {
                    continue;
                }
                $tag = new Tag($tag);
            }
            $stuff = ['_tag' => $tag->id,
                      '_control' => $control->getId()];
            PgDB::set('tags2controls', $stuff, $stuff);
        }
    }


}
"""  # pylint: disable=pointless-string-statement
