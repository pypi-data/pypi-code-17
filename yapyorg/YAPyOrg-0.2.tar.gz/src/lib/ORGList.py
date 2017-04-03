
from .ORGElement import * 
from .ORGListItem import * 

class ORGList(ORGElement):
    
    def __init__(self):
        self.items = []

    def parse(lines):
            """
            Returns new object with this element which is trying to parse 
        
            lines: list of lines to parse
        
            returns: tuple (ORGElement or its child, remaining_lines)
        
            remaining_lines - list of lines that are not parsed
        
            if parsing cannot be done then (None, lines) is returned 
            """
            item, lines = ORGListItem.parse(lines)
            l = ORGList()
            while item != None:
                l.addItem(item)
                item, lines = ORGListItem.parse(lines)
            if l.itemCount() > 0:
                return (l, lines)
            else:
                return (None, lines)

    def getType(self):
        """
        Returns one of types listed above
        """
        return ORGElement.ELEMENT_TYPE_LIST

    def itemCount(self):
        return len(self.items)

    def addItem(self, item):
        self.items.append(item)

    def getItems(self):
        return self.items
    
    def getOutput(self):
        """
        Returns representation of the element in a org-mode format.
        """
        items = []
        for item in self.getItems():
            items.append("+ " + item.getText())
        return "\n".join(items)
            
