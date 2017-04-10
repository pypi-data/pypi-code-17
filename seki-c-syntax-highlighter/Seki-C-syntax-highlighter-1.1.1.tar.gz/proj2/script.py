import subprocess
import sys

#useless
flist = [
#test4 is the first with --format
'error-parameter.fmt',
'error-size.fmt',
'error-color.fmt',
'error-re.fmt',
'empty',
'basic-parameter.fmt',
'basic-parameter.fmt',
'basic-parameter.fmt',
'basic-re.fmt',
'special-re.fmt',
'special-symbols.fmt',
'negation.fmt',
'multiple.fmt',
'spaces.fmt',
'empty',
'overlap.fmt',
're.fmt',
'example.fmt',
'c.fmt'
]

#useless
ilist = [
#test2 begins with --input
    'nonexistent',
    'empty',
    'empty',
    'empty',
    'empty',
    'empty',
    'basic-parameter.in',
    'basic-parameter.in',
    'basic-parameter.in',
    'basic-re.in',
    'special-re.in',
    'special-symbols.in',
    'negation.in',
    'multiple.in',
    'multiple.in',
    'newlines.in',
    'overlap.in',
    'special-symbols.in',
    'example.in',
    'cprog.c'
]
#useless
elist = [
1,2,3,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
]


for i in range(1,23):
    test = "test" + ("0" if i <= 9 else "") + str(i) + ".err"
    test1 = "test" + ("0" if i <= 9 else "") + str(i) + ".out"
    test2 = "!test" + ("0" if i <= 9 else "") + str(i) + ".!!!"
    subprocess.call(["rm", test, test1, test2])


subprocess.call(["rm", "mycode", "myout", "myerr"])
subprocess.call(["bash", "_stud_tests.sh"])


output = open("myerr", "w+")
for i in range(1,23):
    output.write("\t\t*** TEST {} ***\n".format(i))
    output.flush()
    
    test = "test" + ("0" if i <= 9 else "") + str(i) + ".err"
    testref = "ref-out/test" + ("0" if i <= 9 else "") + str(i) + ".err"
    print(test + " " + testref)
    subprocess.call(["diff", "-Nau", test, testref], stdout=output)
    
    output.write("PASSED!!!")
    output.write("\n\n\n")
output.close()

output = open("myout", "w+")
for i in range(1,23):
    output.write("\t\t*** TEST {} ***\n".format(i))
    output.flush()
    test = "test" + ("0" if i <= 9 else "") + str(i) + ".out"
    testref = "ref-out/test" + ("0" if i <= 9 else "") + str(i) + ".out"
    print(test + " " + testref)
    subprocess.call(["diff", "-Nu", test, testref], stdout=output)
    
    output.write("PASSED!!!")
    output.write("\n\n\n")
output.close()


output = open("mycode", "w+")
for i in range(1,23):
    output.write("\t\t*** TEST {} ***\n".format(i))
    output.flush()
    
    test = "test" + ("0" if i <= 9 else "") + str(i) + ".!!!"
    testref = "ref-out/test" + ("0" if i <= 9 else "") + str(i) + ".!!!"
    print(test + " " + testref)
    subprocess.call(["diff", "-Nau", test, testref], stdout=output)
    output.write("PASSED!!!")
    
    output.write("\n\n\n")
output.close()




