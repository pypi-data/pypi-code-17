
"""
this is an automator to run pytest.

"""

json_layout = """  file: pytester.json required.
{ "app": <path to application folder within project "."?>,
  "tests": <path to tests within project (not used yet)>",
  "options" : {
      <optname>:{"help":<help text>, "opt":<option>},
      ....  repeat for each option
           }
}"""
import sys
import pytest, os

from objdict import ObjDict, JsonDecodeError

def printhelp(parms):
    if not 'options' in parms or not parms.options:
        print("No options available, edit pytester.json")
    else:
        print("\n options are:-")
        for key, optn in parms.options.items():
            print("{}: {}".format(key, optn.help))

def pytester(argv, config="pytester.json"):
    """main function does all the work"""
    print("python", sys.version)
    try:
        with open(config) as f:
            txt = f.read()
    except FileNotFoundError:
        print(json_layout)
        return None

    if not txt:
        print("file empty?")
    else:
        try:
            parms = ObjDict(txt)
        except JsonDecodeError:
            print("oops" + txt)
    
    #import pdb; pdb.set_trace()     
    cdir = os.listdir()
    if  "app" in parms and parms.app in cdir:
        print('chdir')
        os.chdir(parms.app)
    #print(os.listdir('.'))

    #sys.path.append('.')

    testargs = [] #['pytest']
    #if debuging
    testargs += ['--pdb', '--maxfail=1']
    #now the test_pages

    if len(argv) > 1:
        a1 = argv[1]
        if 'options' in parms and a1 in parms.options:
            test = parms.options[a1].opt 
            #'./tests/test_ObjDict.py::TestInstance__json__::test_dict_subobj_to_json'
            testargs.append(test)
        else:
            printhelp(parms)
            return

    try:
        pytest.main(testargs)
    except BaseException as ex:
        print('Pytest returned:', ex)

