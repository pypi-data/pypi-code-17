import subprocess
from ecscli import runCmd
from ecscli import main_parser
import common
import sys
import json

from test_common import *
import datetime

######################################################################
##  
## 
######################################################################
def pSilent(s, silent=True):
    if not silent:  
        print(s)   


######################################################################
##
##
######################################################################
def createTemplate(divider='|'):
    template = "{0:20}"+divider+"{1:35}"+divider+"{2:10}"+divider+"{3:10}"+divider+"{4:10}"+divider+"{5:10}"+divider+"{6:10}"+divider+"{7:10}"+divider+"{8:35}"
    return template


######################################################################
##
##
######################################################################
def printReport(report, units):
    template = createTemplate('|')
    str0 = template.format('','','','','CURRENT', 'CURRENT', 'VARRAY', 'VARRAY', 'VARRAY')

    rightNow = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:00Z')
    with open('billingreport_'+rightNow+'.txt', 'w') as fp:
        size = 'SIZE ('+units+')'
        str = template.format('NAMESPACE', 'BUCKET', 'CREATED', 'DELETED', 'OBJECT CNT', size, 'FREE', 'PROVSIONED', 'ID')
        pSilent(str0, False)
        pSilent(str, False)
        fp.write(str0 +'\n')
        fp.write(str +'\n')

        for r in report:
            str = template.format(*r)
            pSilent(str, False)
            fp.write(str +'\n')


######################################################################
# get the capacity of the vpool
######################################################################
def capacity_info(billing_result, silent=False):
    results = {}

    vpool_id = billing_result['vpool_id']

    #first get the virtual array mappings of the vpool/replicationGroup that this bucket belongs to
    sys.argv = ["", "objectvpool", "show", "-id", vpool_id]
    result = runCmd()
    pSilent(result, silent)

    vMappings = result['varrayMappings']
    for vMap in vMappings:
        vMapName = vMap['name']
        vMapId = vMap['value']

        print('Getting the capacity of vArray ' + vMapName)
        sys.argv = ["", "capacity", "-vId", vMapId]
        result = runCmd()
        results[vMapId] = result
        pSilent(result, silent)

    return results


######################################################################
# "2017-04-19T17:55Z"
######################################################################
def sample_namespace_and_bucket(theNs=None, theBucket=None, units="GB", startTime=None):
    rightNow = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:00Z')
    print('rightNow = ' + rightNow)

    '''
    if startTime is None:
        try:
            with open('lastRun.json', 'r') as lr:
                lastRunResults = json.load(lr)
        except:
            print('Could not use last run')
            return
    '''

    sys.argv = ["", "billing", "sample", "-ns", theNs, "-bucket", theBucket, "-st", startTime, "-et", rightNow, "-u", units]
    result = runCmd()

    '''
    with open('billingsample.json', 'w') as fp:
        json.dump(result, fp, indent=4)
    '''
    return result

######################################################################
##  
##  
######################################################################
def show_billing_info(theNs='ben_namespace', theBucket='aadad2489cf04390b99aaf89fe96cde4', units='MB', startTime='2017-04-12T17:55Z'):
    print('Entered show_billing_info namespace: ' + theNs + ' bucket: ' + theBucket )
    report = []

    resultStr = sample_namespace_and_bucket(theNs, theBucket, units, startTime)
    result = json.loads(resultStr)
    capacity_results = capacity_info(result, True)

    ns = result['namespace']
    b = result['name']
    c = result['objects_created']
    d = result['objects_deleted']
    to = result['total_objects']
    ts = result['total_size']
    bucketLine = [ns, b, c, d, to, ts]

    iter = 0
    for k, v in capacity_results.iteritems():
        if (iter == 0):
            output = bucketLine 
        else:
            output = ['','','','','','']

        value = json.loads(v)
        fr = value['totalFree_gb']
        pr = value['totalProvisioned_gb']
        output.append(fr)
        output.append(pr)
        output.append(k)
        iter = iter+1
        report.append(output)
    return (report, units)


######################################################################
##
##
######################################################################
def getObjectUserNamespace(objectUser='ben'):
    sys.argv = ["", "objectuser", "list", "-uid", objectUser]
    result = runCmd()
    ns = result['namespace']
    return ns


######################################################################
##
##
######################################################################
def getBucketsWithOwner(theOwner='ben', startTime='2017-04-12T17:55Z', units='GB'):
    print('Entered getBucketsWithOwner with owner: ' + theOwner)
    ownerReport = []

    #first get the namespace that the object user belongs to
    theNs = getObjectUserNamespace(theOwner)
    print('RETRIEVED NS:' + theNs)

    sys.argv = ["", "bucket", "list", "-ns", theNs]
    result = runCmd()
    buckets = result['object_bucket']
    for b in buckets:
        if b['owner'] == theOwner:
            bName = b['name']
            report, units = show_billing_info(theNs, bName , 'MB', startTime)
            ownerReport.extend(report)

    return ownerReport,units

######################################################################
##  
##  
######################################################################
def authit(configProfile='51-root', password='ChangeMe'):
    print('Entered authit')
    p = subprocess.Popen( 'python ecscli.py config set -pf ' + configProfile, shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)


    p = subprocess.Popen( 'python ecscli.py authenticate', shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    p.communicate(password)
    print('pretty sure we are authorized')


######################################################################
##  
##  
######################################################################
if __name__ == "__main__":
    authit()

    if (len(sys.argv) > 1):
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(sys.argv[1])

        if (len(sys.argv) > 2):
            funcArgs = sys.argv[2:]
            report,units = method(*funcArgs)
        else:
            report, units = method()

    else:
        report, units = show_billing_info()

    printReport(report, units)

