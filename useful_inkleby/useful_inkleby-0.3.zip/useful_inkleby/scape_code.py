'''
Created on Jul 5, 2016

@author: Alex
'''

from files import QuickGrid
from data.postcode import valid_uk_postcode

def combine():
    root = QuickGrid().open("E:\\wfdata\\Public Register 01 06 2016.xls",tab=0)
    
    
    for x in range(1,565):# 
        print x
        additional = QuickGrid().open("E:\\wfdata\\Public Register 01 06 2016.xls",tab=x)
        root.data.extend(additional.data)
        
    root.save("E:\\wfdata\\Merged.xls")
    
    
def expand():
    
    ql = QuickGrid().open("E:\\wfdata\\Merged.xls")
    
    ql.header.extend(["road","town","postcode","landlord gender"])
    
    for r in ql:
        
        address = r["property address"].split(",")
        postcode = address[-1].strip()
        if len(address) > 2:
            town = address[-2].strip()
        print address
        if len(address) > 3:
            street = " ".join(address[-3].strip().split(" ")[1:])
        title = r["licence holder"].split(" ")[0].lower()
        if valid_uk_postcode(postcode):
            r.append(street)
            r.append(town)
            r.append(postcode)
        else:
            r.append("")
            r.append("")
            r.append("")
        if title == "mr":
            gender = "Male"
        elif title in ["miss","mrs","ms"]:
            gender = "Female"
        else:
            gender = "Unknown"
        r.append(gender)
        
    
    
    ql.save("E:\\wfdata\\Expanded.xls")

#combine()
expand()