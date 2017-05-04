from dwell.RAD.deprecated import deprecated

def new1():
    print("new1")

@deprecated
def dep1():
    print ("dep1")

@deprecated(message="new message.")
def dep2():
    print ("dep2")

@deprecated(message="new message.", replacement=new1)
def dep3():
    print ("dep2")

@deprecated(replacement=new1)
def dep4():
    print ("dep3")
#
@deprecated(replacement=new1, use_replacement=True)
def dep5():
    print ("dep4")

print("Running dep1")
dep1()
print("Running dep2")
dep2()
print("Running dep3")
dep3()
print("Running dep4")
dep4()
print("Running dep5")
dep5()
print("Running new1")
new1()
