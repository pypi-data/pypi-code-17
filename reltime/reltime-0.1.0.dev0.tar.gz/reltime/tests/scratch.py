import re
rel_day = "(today|yesterday|tomorrow|tonight|tonite)"
reg3 = re.compile(rel_day, re.IGNORECASE)
print str(reg3)