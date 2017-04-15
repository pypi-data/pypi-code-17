ptable_data = {
    "H": "Hydrogen",
    "O": "Oxygen",
    "Zn": "Zink"}
 
def get_name(symb):
    return ptable_data.get(symb, None)
 
def get_symb(name):
    for item in ptable_data:
        if ptable_data[item] == name:
            return item
    return None
