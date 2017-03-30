
from .ORGElement import * 



class ORGText(ORGElement):

    def __init__(self, text):
        self.text = text.strip() 

    def getText(self):
        return self.text

    def parse(lines):
        """
        Returns new object with this element which is trying to parse 
    
        lines: list of lines to parse
    
        returns: tuple (ORGElement or its child, remaining_lines)
    
        remaining_lines - list of lines that are not parsed
    
        if parsing cannot be done then (None, lines) is returned 
        """
        i = 0
        text = ""
        while i < len(lines) and len(lines[i]) > 0 and not lines[i][0] in "<+*|":
            text = text + lines[i] + " "
            i = i + 1
        if text != "":
            return (ORGText(text), lines[i:])
        else:
            return (None, lines)


    def getType(self):
        """
        Returns one of types listed above
        """
        return ORGElement.ELEMENT_TYPE_TEXT
    
    def getOutput(self):
        """
        Returns representation of the element in a org-mode format.
        """
        return self.getText()
