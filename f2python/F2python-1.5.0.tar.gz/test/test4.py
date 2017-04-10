"""test4.py
   do help isolate a vicious bug in OFF.
   
   If you can't find anything wrong executing this script it's because
   you are working on a version where the bug is corrected !
   If you find some bug then it's a regression ! Then please contact F2 developpers.
"""
import sys

db_url = 'rpc:127.0.0.1:8081'
# db_url = 'file:root.db'
if len(sys.argv) > 1:
	db_url = sys.argv[1]

import F2
db = F2.connect(db_url)

P = db.CLASS(className = 'Person')

if P:
	print("Class Person seems to already exist")
	P = P[0]
	E = db.Employee
else:
	print("Create a class Person")
	P = db.class_create('Person', database='test', 
	        schema={'name':db.String})
	print("P =", P)
	print("Create a sub-class Employee of Person")
	E = db.class_create('Employee', superClass=P, database='test',
	       schema={'manager':P})
	print("E =", E)

theBoss = P.create(name='Zebigboss')

print("1) create 10 employees")
for i in range(1,11):
	e = E.create(name='Mr %d' % i, manager=theBoss)
	if i % 5 == 0:
		e.name = 'Titi'

print("2) Let's look for employee(s) called 'Titi'...")
titis = E(name = 'Titi')
print("'found", len(titis), "of them.")
for e in titis:
	print("-", e, e.name)

print("3) Now let's optimize: index the reverse function of attribute 'name' ")
attribut_name = db.Attribute(attributeName='name', domainClass=P)[0]
attribut_name.set_reverse_function()

print("4) Let's look for employee(s) called 'Titi'...")
titis = E(name = 'Titi')
print("'found", len(titis), "of them.")
for e in titis:
	print("-", e, e.name)

print("4.2) let's close and re-open the db")
db.close(commit_needed=True)
db = F2.connect(db_url)
P = db.Person
E = db.Employee


print("5) create 10 more employees")
for i in range(1,11):
	e = E.create(name='Mr %d' % i, manager=theBoss)
	if i % 5 == 0:
		e.name = 'Titi'

print("6) Let's look for employee(s) called 'Titi'...")
titis = E(name = 'Titi')
print("'found", len(titis), "of them.")
for e in titis:
	print("-", e, e.name)

print("7) now to verify: full scan lookup:")
for p in P():
	print(p, "is called", p.name)

db.close()
