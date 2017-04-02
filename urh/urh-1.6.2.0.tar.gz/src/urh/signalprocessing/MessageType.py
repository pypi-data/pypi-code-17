import random
import uuid
import xml.etree.ElementTree as ET
from copy import deepcopy

from urh import constants
from urh.signalprocessing.FieldType import FieldType
from urh.signalprocessing.ProtocoLabel import ProtocolLabel
from urh.signalprocessing.Ruleset import Ruleset
from urh.util.Logger import logger


class MessageType(list):
    """
    A message type is a list of protocol fields.

    """

    __slots__ = ["name", "__id", "assigned_by_ruleset", "ruleset", "assigned_by_logic_analyzer"]

    def __init__(self, name: str, iterable=None, id=None, ruleset=None):
        iterable = iterable if iterable else []
        super().__init__(iterable)

        self.name = name
        self.__id = str(uuid.uuid4()) if id is None else id

        self.assigned_by_logic_analyzer = False
        self.assigned_by_ruleset = False
        self.ruleset = Ruleset() if ruleset is None else ruleset

    def __hash__(self):
        return hash(super)

    def __getitem__(self, index) -> ProtocolLabel:
        return super().__getitem__(index)

    def __repr__(self):
        return self.name + " " + super().__repr__()

    def __eq__(self, other):
        if isinstance(other, MessageType):
            return self.id == other.id
        else:
            return super().__eq__(other)

    @property
    def assign_manually(self):
        return not self.assigned_by_ruleset

    @property
    def id(self) -> str:
        return self.__id

    @property
    def unlabeled_ranges(self):
        """

        :rtype: list[(int,int)]
        """
        return self.__get_unlabeled_ranges_from_labels(self)

    @staticmethod
    def __get_unlabeled_ranges_from_labels(labels):
        """

        :type labels: list of ProtocolLabel
        :rtype: list[(int,int)]
        """
        start = 0
        result = []
        for lbl in labels:
            if lbl.start > start:
                result.append((start, lbl.start))
            start = lbl.end
        result.append((start, None))
        return result

    def unlabeled_ranges_with_other_mt(self, other_message_type):
        """

        :type other_message_type: MessageType
        :rtype: list[(int,int)]
        """
        labels = self + other_message_type
        labels.sort()
        return self.__get_unlabeled_ranges_from_labels(labels)

    def append(self, lbl: ProtocolLabel):
        super().append(lbl)
        self.sort()

    def add_protocol_label(self, start: int, end: int, name=None, color_ind=None,
                           auto_created=False, type: FieldType = None) -> ProtocolLabel:

        name = "" if not name else name
        used_colors = [p.color_index for p in self]
        avail_colors = [i for i, _ in enumerate(constants.LABEL_COLORS) if i not in used_colors]

        if color_ind is None:
            if len(avail_colors) > 0:
                color_ind = avail_colors[0]
            else:
                color_ind = random.randint(0, len(constants.LABEL_COLORS) - 1)

        proto_label = ProtocolLabel(name=name, start=start, end=end, color_index=color_ind,
                                    auto_created=auto_created, type=type)

        if proto_label not in self:
            self.append(proto_label)
            self.sort()

        return proto_label  # Return label to set editor focus after adding

    def add_label(self, lbl: ProtocolLabel, allow_overlapping=True):
        if allow_overlapping or not any(lbl.overlaps_with(l) for l in self):
            self.add_protocol_label(lbl.start, lbl.end, name=lbl.name, color_ind=lbl.color_index)

    def remove(self, lbl: ProtocolLabel):
        if lbl in self:
            super().remove(lbl)
        else:
            logger.warning(lbl.name + " is not in set, so cant be removed")

    def to_xml(self) -> ET.Element:
        result = ET.Element("message_type", attrib={"name": self.name, "id": self.id,
                                                    "assigned_by_ruleset": "1" if self.assigned_by_ruleset else "0",
                                                    "assigned_by_logic_analyzer": "1" if self.assigned_by_logic_analyzer else "0"})
        for lbl in self:
            result.append(lbl.to_xml(-1))

        result.append(self.ruleset.to_xml())

        return result

    @staticmethod
    def from_xml(tag: ET.Element):
        field_types_by_type_id = {ft.id: ft for ft in FieldType.load_from_xml()}

        name = tag.get("name", "blank")
        id = tag.get("id", None)
        assigned_by_ruleset = bool(int(tag.get("assigned_by_ruleset", 0)))
        assigned_by_logic_analyzer = bool(int(tag.get("assigned_by_logic_analyzer", 0)))
        labels = []
        for lbl_tag in tag.findall("label"):
            labels.append(ProtocolLabel.from_xml(lbl_tag, field_types_by_type_id=field_types_by_type_id))
        result = MessageType(name=name, iterable=labels, id=id, ruleset=Ruleset.from_xml(tag.find("ruleset")))
        result.assigned_by_ruleset = assigned_by_ruleset
        result.assigned_by_logic_analyzer = assigned_by_logic_analyzer

        return result

    def copy_for_fuzzing(self):
        result = deepcopy(self)
        for lbl in result:
            lbl.fuzz_values = []
            lbl.fuzz_created = True
        return result
