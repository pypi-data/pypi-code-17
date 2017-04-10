""" Test the OFF module, the underlying F2 storage engine:
    very basic Index lookup performance measurement
    Th. Estier - sept 2004
"""

import F2, time

OFF = F2.OFF

try:
	offStore = OFF.OFFStore('file:test_off.db')
	print("test_off: existing storage.")
except OFF.F2StorageError as e:
	OFF.db_root['F2_Signature'] = { }
	offStore = OFF.currentOFFStore
	print("test_off: empty storage.")

NB_VAL = 1000000   # one million 
print("creating function_1 (non reversed function) with {:,d} values.".format(NB_VAL))
f1 = OFF.AttributeStorage(4, is_reversed = False)
now = time.time()
for x in range(NB_VAL):
	f1[x] = x
f1[1] = -1
f1[10] = -1
f1[100] = -1
f1[1000] = -1
f1[10000] = -1
f1[100000] = -1
print("...took me %8.6f seconds" % (time.time()-now))

print("creating function_2 (with reversed function) with {:,d} values.".format(NB_VAL))
f2 = OFF.AttributeStorage(5, is_reversed = True)
now = time.time()
for x in range(NB_VAL):
	f2[x] = x
f2[1] = -1
f2[10] = -1
f2[100] = -1
f2[1000] = -1
f2[10000] = -1
f2[100000] = -1
print("...took me %8.6f seconds" % (time.time()-now))

print("Now let's close the OFF store.")
offStore.close()

print("\n...and let's open it again from the file system.")
offStore = OFF.OFFStore('file:test_off.db')

print("now looking for 6 values among {:,d} in f1 (non-reversed)...".format(NB_VAL))
now = time.time()
f1 = OFF.db_root[4]
res = f1.find(-1)
print("...took me %8.6f seconds" % (time.time()-now))
print("f1.find(-1) =", res)

print("now looking for 6 values among {:,d} in f2 (reversed)...".format(NB_VAL))
now = time.time()
f2 = OFF.db_root[5]
res = f2.find(-1)
print("...took me %8.6f seconds" % (time.time()-now))
print("f2.find(-1) =", res)

