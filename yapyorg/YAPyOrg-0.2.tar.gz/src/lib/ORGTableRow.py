
from .ORGElement import * 
class ORGTableRow(ORGElement):
    
    def __init__(self, items, heading=False):
        self.heading = heading
        self.items = items

    def isHeading(self):
        return self.heading

    def parse(lines):
        if len(lines) == 0:
            return (None, lines)
        current = lines[0]
        if current == "":
            return (None, lines)
        if current[0] == "|":
            items = current.split("|")[1:-1]
            res = []
            for item in items:
                res.append(item.strip())
            return (ORGTableRow(res), lines[1:])
        else:
            return (None, lines)

    def getItems(self):
        return self.items

    def setHeading(self):
        self.heading = True

    def getType(self):
        return ORGElement.ELEMENT_TYPE_TABLE_ROW

    def getOutput(self):
        H = ""
        s = "| " + " | ".join(self.items) + " |"
        if self.heading:
            H = len(s)*"-" + "\n"
        return s + "\n" + H
