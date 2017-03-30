
class ORGElement:
    
    ELEMENT_TYPE_SECTION = 1
    ELEMENT_TYPE_LIST = 2
    ELEMENT_TYPE_TEXT = 3
    ELEMENT_TYPE_BLOCK = 4
    ELEMENT_TYPE_MACRO = 5
    ELEMENT_TYPE_TABLE = 6
    ELEMENT_TYPE_LIST_ITEM = 7
    ELEMENT_TYPE_EMPTY_LINE = 8

    def parse(lines):
        """
        Returns new object with this element which is trying to parse 
    
        lines: list of lines to parse
    
        returns: tuple (ORGElement or its child, remaining_lines)
    
        remaining_lines - list of lines that are not parsed
    
        if parsing cannot be done then (None, lines) is returned 
        """
        pass

    def getType(self):
        """
        Returns one of types listed above
        """
        return None

    def getOutput(self):
        """
        Returns representation of the element in a org-mode format.
        """
        return ""
