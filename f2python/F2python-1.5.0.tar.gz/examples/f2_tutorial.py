""" The complete set of python instructions in the F2 tutorial
    
    These are all the instructions of the Section 3 of the documentation,
    "Section 3 Using F2: a short introduction"
    
    usage: $ python f2_tutorial.py [storage_URL]

     You can execute this script with the URL of a F2 Data store as 1st argument.
     Th. Estier - sept 2005 to dec 2014
"""
import F2, sys

db_URL = 'file:root.db'
if len(sys.argv) > 1:
	db_URL = sys.argv[1]

f2 = F2.connect(db_URL)

print(f2.String, f2.Int, f2.CLASS, f2.Attribute)

D = f2.class_create(className='Department', database='test',
                    schema={'name': f2.String})
print("D =", D)
market = D.create(name='Marketing')
print("market =", market, " market.name =", market.name)

P = f2.class_create(className = 'Person', database='test', 
              schema={'firstname': f2.String,
                      'lastname' : f2.String})

print("P =", P)
                
E = f2.class_create(className = 'Employee', database='test',
        superClass = P,
        schema={'work_in': (f2.Department, 1, '*'),
                'manager':  f2.Person})
print("E =", E)

joe =           P.create(firstname='Joe', lastname='Cool')
larry = f2.Person.create(firstname='Larry', lastname='Ellison')
print("(larry.firstname, larry.lastname) =", (larry.firstname, larry.lastname))

larry.firstname = 'Lawrence'

linus = f2.Employee.create(firstname='Linus', 
                           lastname='Torvald',
                           manager = larry,
                           work_in = market)

print("linus.work_in.name = ", linus.work_in.name)
print("linus.manager.firstname = ", linus.manager.firstname)

try:
	print("linus.manager.work_in = ")
	print(linus.manager.work_in)
except:
    print("Oops... Lawrence is not an employee yet.")
                            
larry = f2.Employee.enter(larry)
larry.work_in = market

print("larry.work_in.name =", larry.work_in.name)

print("linus.manager.work_in == linus.work_in =>", linus.manager.work_in == linus.work_in)

for attr in f2.Employee.all_attributes():
    a = attr.attributeName
    print(a, '-->', getattr(larry, a))

print("P( work_in = market ) =>", P( work_in = market ))
print("E( work_in = market ) =>", E( work_in = market ))

print("Now let's add proper keys to these tuple classes:")
f2.add_key(f2.Person, 'firstname', 'lastname')
f2.add_key(f2.Department, 'name')

print("P( work_in = market ) =>", P( work_in = market ))
print("E( work_in = market ) =>", E( work_in = market ))

print("P( work_in = market ).firstname =>", P(work_in = market).firstname)
print("E( work_in = market ).firstname =>", E(work_in = market).firstname)



f2.close()


