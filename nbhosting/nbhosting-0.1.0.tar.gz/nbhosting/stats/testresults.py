# parse the output of test-images

import re



def read_test(f):
    result = []
    for line in f:
        if line.startswith


def read_tests(filenames):
    result = []
    for filename in filenames:
        paths = [ "/root/nbhosting/sctipts/tests", "."]
        for path in paths:
            fullname = os.path.join(path, filename)
            try:
                with open(fullname) as f:
                    result += read_test(f)
                break
        print("input {filename} not found".format(**locals()))
    return result
                        
