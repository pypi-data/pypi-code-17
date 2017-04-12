import subprocess
import argparse

def get_all_naked_disk():

    disks = []
    cmd = ["sudo", "fdisk", "-l"] 
    f = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell = False)
    err = f.stderr.read()
    for line in  err.splitlines():
        if -1 == line.find('/dev'):
            continue
        disk = line.split(' ')[1]
        disks.append(disk)

    return disks

def partition_disk(dev,dev_type=83):
    cmd_list = ["sudo","fdisk",dev]
    f = subprocess.Popen(cmd_list,stdin = subprocess.PIPE, \
            stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell = False)
    f.stdin.write("n\n")
    f.stdin.write("p\n")
    f.stdin.write("1\n")
    f.stdin.write("\n")
    f.stdin.write("\n")
    f.stdin.write("t\n")
    f.stdin.write("%s\n" % dev_type)
    f.stdin.write("w\n")

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", type=str, dest="dev",help="dev to partion")
    parser.add_argument("-t", "--type", type=str, dest="dev_type",help="dev type to partion",default="83")
    args = parser.parse_args()
    if args.dev is not None:
        partition_disk(args.dev,args.dev_type)
    else:
        for dev in get_all_naked_disk():
            partition_disk(dev,args.dev_type)


