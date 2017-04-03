
from .ORGElement import * 
from .ORGTableRow import * 

class ORGTable(ORGElement):
    
    def __init__(self):
        self.rows = []
    
    def addRow(self, row):
        self.rows.append(row)

    def getRows(self):
        return self.rows

    def parse(lines):
        if len(lines) == 0:
            return (None, lines)
        table = ORGTable()
        (row, lines) = ORGTableRow.parse(lines)
        if row == None or row.getType() != ORGElement.ELEMENT_TYPE_TABLE_ROW:
            return (None, lines)
        if len(lines) > 0:
            curr = lines[0]
            heading = True
            for c in curr:
                if c != "-":
                    heading = False
                    break
            if heading:
                row.setHeading()
                lines = lines[1:]
        while row != None and row.getType() == ORGElement.ELEMENT_TYPE_TABLE_ROW:
            table.addRow(row)
            (row, lines) = ORGTableRow.parse(lines)
        return (table, lines)


    def getType(self):
        return ORGElement.ELEMENT_TYPE_TABLE

    def getOutput(self):
        s = ""
        for r in self.rows:
            s += r.getOutput()
        return s
