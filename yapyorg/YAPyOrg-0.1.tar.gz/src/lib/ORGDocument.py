

from .ORGBlock import *
from .ORGElement import *
from .ORGList import *
from .ORGMacro import *
from .ORGSection import *
from .ORGTable import *
from .ORGText import *
from .ORGEmptyLine import * 

class ORGDocument(object):
    
    def __init__(self, elements):
        self.elements = elements

    def getElements(self):
        return self.elements

    def parseElement(lines):
        """
        lines: list of lines

        Returns: (element, remaining_lines)
        """
        elem, lines = ORGEmptyLine.parse(lines)
        if elem != None:
            return (elem, lines)

        elem, lines = ORGSection.parse(lines)
        if elem != None:
            return (elem, lines)
        
        #elem, lines = ORGBlock.parse(lines)
        #if elem != None:
        #    return (elem, lines)
        
        elem, lines = ORGList.parse(lines)
        if elem != None:
            return (elem, lines)
        
        #elem, lines = ORGMacro.parse(lines)
        #if elem != None:
        #    return (elem, lines)
        
        #elem, lines = ORGTable.parse(lines)
        #if elem != None:
        #    return (elem, lines)
        
        elem, lines = ORGText.parse(lines)
        if elem != None:
            return (elem, lines)
        
        return (None, lines)

    def parse(lines):
        res = []
        elem, lines = ORGDocument.parseElement(lines)
        while elem != None:
            if elem.getType() != ORGElement.ELEMENT_TYPE_EMPTY_LINE:
                res.append(elem)
            elem, lines = ORGDocument.parseElement(lines)
        return ORGDocument(res)

    def createTree(self, level=0):
        """
        level: level above which creation stops

        Returns: (root, remaining_elements)
        """
        root = ORGSection("", level=0)
        elems = self.elements
        while len(elems) > 0:
            elem = elems[0]
            if elem.getType() != ORGElement.ELEMENT_TYPE_SECTION:
                root.addElement(elem)
                elems = elems[1:]
            else:
                if elem.getLevel() > level:
                    child, elems = ORGDocument(elems[1:]).createTree(level=elem.getLevel())
                    for e in child.getElements():
                        elem.addElement(e)
                    for s in child.getSubSections():
                        elem.addSubSection(s)
                    root.addSubSection(elem)
                else:
                    return (root, elems)
        return (root, elems)
    
    def getOutput(self):
        """
        Returns representation of the element in a org-mode format.
        """
        lines = []
        for e in self.elements:
            lines.append(e.getOutput())
        return "\n".join(lines)
