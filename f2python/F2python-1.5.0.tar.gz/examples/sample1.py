""" test.py
"""
import sys, F2

db_url = 'file:root.db'
if len(sys.argv) > 1:
	db_url = sys.argv[1]
f2 = F2.connect(db_url)

P = f2.CLASS(className = 'Person')
E = f2.CLASS(className = 'Employee')

if P:
	print("Class Person seems to already exist")
	P = P[0]
	joe = P(firstname='joe') or P.create(firstname='joe')
	toto = P(firstname='toto')
	if not toto:
		E = E[0]
		toto = E.create(firstname='toto', manager=joe)
else:
	print("Create a class Person")
	P = f2.class_create('Person', schema={'firstname':f2.String})
	print("P =", P)
	print("Create a sub-class Employee of Person")
	E = f2.class_create('Employee', superClass=P, schema={'manager':P})
	print("E =", E)
	joe = P.create(firstname='joe')
	toto = E.create(firstname='toto', manager=joe)
	
print("All persons:", P().firstname)
print("All employees:", E().firstname)
	
try:
	D = f2.Department
	print("Class Department seems to already exist")
	marketing = D(name='Marketing')
	if not marketing:
		marketing = D.create(name = 'Marketing')
except:
	print("Create a class Department")
	D = f2.class_create('Department', schema = {'name':f2.String })
	work = f2.Attribute.create(attributeName = 'work_in', 
	                           domainClass = P, 
	                           rangeClass = D)
	marketing = D.create(name = 'Marketing')

print("Initially, Joe worked in:", joe.work_in)
joe.work_in = marketing
print("Now, Joe works in:", joe.work_in.name)

allMetaK = f2.CLASS.all_subclasses()
print("all meta K = ", allMetaK)

allPs = P.all_subclasses()
print("all kind of persons =", allPs)

print("now trying to remove department marketing...")
f2.Department.leave(marketing)

print("Now Class Department is:", D().name)
print("... then persons are:", P().firstname)
print("... and employees are:", E().firstname)

print("Now joe.work_in = ", joe.work_in, "and toto works for:", toto.manager.firstname)

print("Lets change a little things: build a new department (finance)")
finance = D.create(name = 'Finance')
print("finance = ", finance)
joe.work_in = finance

print("and lets assign minimum cardinality to some attributes: Employee.manager and Person.work_in")
F2.new_F2_Attribute('manager', f2.Employee).minCard = 1
F2.new_F2_Attribute('work_in', f2.Person).minCard = 1

print("...and lets try again !")

print("joe works in:", joe.work_in)
print("toto works for joe is:", (toto.manager == joe))

D.leave(finance)
print("Now Class Department is:", D().name)
print("... then persons are:", P().firstname)
print("... and employees are:", E().firstname)


print("Now making the test repeatable by deleting these classes")
f2.CLASS.leave(D); 
f2.CLASS.leave(P); 
f2.CLASS.leave(E)
print("Done, closing")
f2.close()
