
from .ORGElement import * 
class ORGListItem(ORGElement):
    
    def __init__(self, title):
        self.title = title

    def parse(lines):
        """
        Returns new object with this element which is trying to parse 
    
        lines: list of lines to parse
    
        returns: tuple (ORGElement or its child, remaining_lines)
    
        remaining_lines - list of lines that are not parsed
    
        if parsing cannot be done then (None, lines) is returned 
        """
        if len(lines) == 0:
            return (None, lines)
        if len(lines[0].strip()) < 2:
            return (None, lines)
        if (lines[0].strip())[:2] == "+ ":
            return (ORGListItem((lines[0].strip())[2:]), lines[1:])
        else:
            return (None, lines)

    def getType(self):
        """
        Returns one of types listed above
        """
        return ORGElement.ELEMENT_TYPE_LIST_ITEM

    def getText(self):
        return self.title


    def getOutput(self):
        """
        Returns representation of the element in a org-mode format.
        """
        return "+ " + self.getText()
