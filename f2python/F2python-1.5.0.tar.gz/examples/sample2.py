""" An example showing the syntax for declaring a simple schema using the
    short circuit function "class_create".
    Th. Estier - sept 2004
"""
import sys
import F2

db_url = 'file:root.db'
if len(sys.argv) > 1:
    db_url = sys.argv[1]

f2 = F2.connect(db_url)

D = f2.class_create(className='Department', database='test',
          schema={'name': f2.String})

P = f2.class_create(className='Person', database='test',
              schema={'firstname': f2.String,
                      'lastname' : f2.String})

E = f2.class_create(className='Employee', database='test',
              superClass=P,
              schema={'work_in' : (f2.Department, 1, 'N'),
                      'manager' : f2.Person})

# let's print this schema:

for C in (f2.Person, f2.Employee, f2.Department):
    print("class", C.className)
    for attr in C.all_attributes():
        if attr.visibility == 1:
            print("    ", attr.attributeName, ':', attr.rangeClass.className, end=' ')
            if attr.minCard != F2.F2_NULL or attr.maxCard != F2.F2_NULL:
                print(attr.minCard, '..', attr.maxCard)
            else:
                print()

f2.close()
