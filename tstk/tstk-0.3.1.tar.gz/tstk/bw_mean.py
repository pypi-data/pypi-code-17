import os
import sys
import shlex
import subprocess

fnames = [f for f in sys.argv[1].split(",") if f != '']
outdir = sys.argv[2]
ofname_root = sys.argv[3]
fchrsizes = sys.argv[4]
try:
    mean = "-mean" if sys.argv[5] == "mean" else ""
except IndexError:
    mean = ""

fnames_bw = []

for fname in fnames:
    fname_root,fname_ext = os.path.splitext(os.path.basename(fname))
    fname_sorted = "{}/{}.sorted{}".format(outdir,fname_root,fname_ext)
    fname_bw = "{}/{}.bw".format(outdir,fname_root)
    fnames_bw.append(fname_bw)

    cmd = "/nfs/users/nfs_t/tdd/software/bedtools2/bin/sortBed -i {}".format(fname)
    print(cmd)

    p1 = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    with open(fname_sorted,"wb") as ofh:
        ofh.write(p1.stdout.read())

    cmd = "/nfs/users/nfs_t/tdd/lustre/pipette/binx/kentUtils/bin/bedGraphToBigWig {} {} {}".format(fname_sorted,fchrsizes,fname_bw)
    print(cmd)
    p1 = subprocess.run(shlex.split(cmd))

ofname_bg = "{}.bg".format(ofname_root)
ofname_bg_sorted = "{}.sorted.bg".format(ofname_root)
ofname_bw = "{}.bw".format(ofname_root)
 
cmd = "/nfs/users/nfs_t/tdd/lustre/pipette/binx/kentUtils/bin/bigWigMerge {} {} {}/{}".format(mean," ".join(fnames_bw),outdir,ofname_bg)
print(cmd)
p1 = subprocess.run(shlex.split(cmd))

cmd = "/nfs/users/nfs_t/tdd/lustre/pipette/binx/bedtools/2.26.0/sortBed -i {}/{}".format(outdir,ofname_bg)
print(cmd)
p1 = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
with open("{}/{}".format(outdir,ofname_bg_sorted),"wb") as ofh:
    ofh.write(p1.stdout.read())

cmd = "/nfs/users/nfs_t/tdd/lustre/pipette/binx/kentUtils/bin/bedGraphToBigWig {outdir}/{bg} {fchr} {outdir}/{bw}".format(fchr=fchrsizes,outdir=outdir,bg=ofname_bg_sorted,bw=ofname_bw)
print(cmd)
p1 = subprocess.run(shlex.split(cmd))
