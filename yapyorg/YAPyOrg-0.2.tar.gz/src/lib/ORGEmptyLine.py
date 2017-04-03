
from .ORGElement import * 


class ORGEmptyLine(ORGElement):
    

    def parse(lines):
        if len(lines) > 0:
            if lines[0].strip() == "":
                return (ORGEmptyLine(), lines[1:])
            else:
                return (None, lines)
        else:
            return (None, lines)

    def getType(self):
        """
        Returns one of types listed above
        """
        return ORGElement.ELEMENT_TYPE_EMPTY_LINE
    
    def getOutput(self):
        """
        Returns representation of the element in a org-mode format.
        """
        return ""
