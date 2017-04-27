from Bio import SeqIO
from Bio.Seq import Seq
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import glob,os,math,sys,json,pysam,operator

#pd.options.display.mpl_style = 'default'

#TODO: add strand to the gbk processor (for plotting the subfeatures)
#TODO add ability to plot subfeatures as bars under the x axis

def parsearguments():
    epilog = """============================== Alea jacta est =============================="""
    parser = argparse.ArgumentParser(epilog=epilog,formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('ALNFILE',help="bam/sam format alignment file")
    parser.add_argument('FEATURESFILE',help="File from which to extract the features (gbk/ape or bed)")
    parser.add_argument('OUTDIR',help="Output directory")
    parser.add_argument('--outprefix',help="Prefix for the output file names",default="")
    parser.add_argument('--features',help="Comma separated list of features to extract")
    parser.add_argument('--normfeat',help="Name of the subfeature to normalise all reads to")
    parser.add_argument('--normnreads',help="Normalise to the total number of aligned reads (per library)",action="store_true")
    parser.add_argument('--normval',help="Normalisation factor",default=None,type=float) #TODO improve behaviour
    parser.add_argument('--stranded', help="Generate a stranded plot", action="store_true")
    parser.add_argument('--binsize', help="Bin size to use for the histogram", type=int,default=10)
    parser.add_argument('--offsetup',help="Portion of sequence to show after the feature. Accepts a number (e.g. 1000) of nts, or a length multiplier (e.g. 1.5x)",default="0")
    parser.add_argument('--offsetdown',help="Portion of sequence to show before the feature. Accepts a number (e.g. 1000) of nts, or a length multiplier (e.g. 1.5x)",default="0")
    parser.add_argument('--log', help="Generate the y axis in log scale", action="store_true")
    parser.add_argument('--mmapweight', help="Weight the reads by the number of times it maps.", action="store_true")
    parser.add_argument('--nmaps', help="Maximum number of multi maps a read can have and still be counted", type=int, default=1)
    parser.add_argument('--length', help="Restrict counted reads to this length", type=int, default=None)
    parser.add_argument('--5pnt', help="Restrict counted reads to the ones with this 5p nt", default=None)
    parser.add_argument('--ylims',metavar='N,N',help="Limits for the y axis, comma separated (lower,upper)")

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    return(vars(parser.parse_args()))

def processbed(fname,featnames=None):
    features = []

    with open(fname, "rU") as f:
        for r in f:
            row = r.split()
            chrname = row[0]
            start = int(row[1])
            end = int(row[2])
            name = row[3]
            strand = row[5]
            if not featnames or name in featnames:
                features.append({"strand":strand,"name":name,"chr":chrname,"start":start,"end":end,"subfeatures":[]})

    return(features)

def processgbk(fname,featnames=None):
    features = []

    records = SeqIO.parse(open(fname, "rU"), "gb")
    for record in records:
        if not featnames or (record.name in featnames or record.id in featnames):
            subfeatures = [] 
            for subfeature in record.features:
                f = {}
                f["start"] = int(subfeature.location.start)
                f["end"] = int(subfeature.location.end)
                f["label"] = subfeature.qualifiers["label"][0]
                if "color" in subfeature.qualifiers:
                    f["color"] = subfeature.qualifiers["color"][0]
                if "fwcolor" in subfeature.qualifiers:
                    f["fwcolor"] = subfeature.qualifiers["fwcolor"][0]
                if "rvcolor" in subfeature.qualifiers:
                    f["rvcolor"] = subfeature.qualifiers["rvcolor"][0]
                subfeatures.append(f)
            features.append({"name":record.name,"start":1,"end":len(record.seq),"subfeatures":subfeatures})

    return(features)

def checkfilters(r,length,nt5p,nmaps):
    length = False if length and len(r.seq) != length else True
    if r.is_reverse:
        seq = Seq(r.seq)
        seq = seq.reverse_complement()
    else:
        seq = r.seq
    nt = False if nt5p and seq[0] != nt5p else True
    try:
        mult = True if dict(r.get_tags())["NH"] <= nmaps else False
    except KeyError:
        print("WARNING: NH tag not present. Ignoring multi-mapper restriction")
        mult = True
    return mult and length and nt

def fhist(fname,feature,offsetup=0,offsetdown=0,normfeat=None,normnreads=False,normval=None,binsize=1,stranded=False,length=None,nt5p=None,nmaps=1,mmapweight=False):
    read_weights_fw = read_weights_rv = None

    bamfile = pysam.AlignmentFile(fname)

    reflen = feature["end"] - feature["start"]

    nbins = int(reflen/binsize)

    if offsetup and "x" in offsetup:
        offsetup = int(reflen * float(offsetup.replace("x","")))
    else:
        offsetup = int(offsetup)

    if offsetdown and "x" in offsetdown:
        offsetdown = int(reflen * float(offsetdown.replace("x","")))
    else:
        offsetdown = int(offsetdown)

    reflen += offsetdown + offsetup

    try:
        refname = feature["name"]
    except KeyError:
        refname = feature["id"]

    try:
        featname = feature["chr"]
    except KeyError:
        featname = feature["name"]

    if normfeat:
        for sf in feature["subfeatures"]:
            if sf["label"] == normfeat:
                normfeat = sf

    start = feature["start"]-offsetdown
    end = feature["end"]+offsetup

    if stranded:
        read_starts_fw = [read.reference_start + offsetdown - feature["start"] + 2 for read in bamfile.fetch(featname,start,end,multiple_iterators=True) if checkfilters(read,length=length,nmaps=nmaps,nt5p=nt5p) and not read.is_reverse]
        read_starts_rv = [read.reference_start + offsetdown - feature["start"] + 2 for read in bamfile.fetch(featname,start,end,multiple_iterators=True) if checkfilters(read,length=length,nmaps=nmaps,nt5p=nt5p) and read.is_reverse]

        if mmapweight:
            try:
                read_weights_fw = [1/dict(read.get_tags())["NH"] for read in bamfile.fetch(featname,start,end,multiple_iterators=True) if checkfilters(read,length=length,nmaps=nmaps,nt5p=nt5p) and not read.is_reverse]
                read_weights_rv = [1/dict(read.get_tags())["NH"] for read in bamfile.fetch(featname,start,end,multiple_iterators=True) if checkfilters(read,length=length,nmaps=nmaps,nt5p=nt5p) and read.is_reverse]
            except KeyError: # no multimapper info in the bamfile
                read_weights_fw = [1 for read in bamfile.fetch(featname,start,end,multiple_iterators=True) if checkfilters(read,length=length,nmaps=nmaps,nt5p=nt5p) and not read.is_reverse]
                read_weights_rv = [1 for read in bamfile.fetch(featname,start,end,multiple_iterators=True) if checkfilters(read,length=length,nmaps=nmaps,nt5p=nt5p) and read.is_reverse]
    else:
        read_starts_fw = [read.reference_start + offsetdown - feature["start"] + 2 for read in bamfile.fetch(featname,start,end,multiple_iterators=True) if checkfilters(read,length=length,nmaps=nmaps,nt5p=nt5p)]
        read_starts_rv = [0 for read in bamfile.fetch(featname,start,end,multiple_iterators=True)]

        if mmapweight:
            try:
                read_weights_fw = [1/dict(read.get_tags())["NH"] for read in bamfile.fetch(featname,start,end,multiple_iterators=True) if checkfilters(read,length=length,nmaps=nmaps,nt5p=nt5p)]
            except KeyError:
                read_weights_fw = [1 for read in bamfile.fetch(featname,start,end,multiple_iterators=True) if checkfilters(read,length=length,nmaps=nmaps,nt5p=nt5p)]

            read_weights_rv = [1 for read in bamfile.fetch(featname,start,end,multiple_iterators=True)]

    counts_fw,bins_fw = np.histogram(np.array(read_starts_fw),bins=nbins,range=(0,reflen),weights=read_weights_fw)
    counts_rv,bins_rv = np.histogram(np.array(read_starts_rv),bins=nbins,range=(0,reflen),weights=read_weights_rv)

    if stranded:
        counts_rv *= -1

    if not stranded or sum(counts_fw) > sum(counts_rv): #which bins to use when calculating width, etc
        refbins = bins_fw
    else:
        refbins = bins_rv

    #TODO: improve this logic. They are not mutually exclusive at the argument level
    if normval:
        counts_fw = counts_fw / normval
        counts_rv = counts_rv / normval
    elif normnreads:
        try:
            nalnreads = sum(1/dict(read.get_tags())["NH"] for read in bamfile.fetch(featname,start,end,multiple_iterators=True))
        except KeyError:
            nalnreads = sum(1 for read in bamfile.fetch(featname,start,end,multiple_iterators=True))

        counts_fw = counts_fw / nalnreads
        counts_rv = counts_rv / nalnreads
    elif normfeat:
        tmp = sum(r >= normfeat["start"] and r <= normfeat["end"] for r in read_starts_fw)
        tmp += sum(r >= normfeat["start"] and r <= normfeat["end"] for r in read_starts_rv)
        counts_fw = counts_fw / tmp
        counts_rv = counts_rv / tmp

    width = (refbins[1] - refbins[0])
    center = (refbins[:-1] + refbins[1:]) / 2

    counts = {"fw":counts_fw}
    if counts_rv.any():
        counts["rv"] = counts_rv

    return counts,refbins,center,width,feature
        
def plot(counts,refbins,center,width,feature,fheight=6,fwidth=14,ylims=(-1,1),title=""):
    if "rv" not in counts:
        stranded = False
    else:
        stranded = True
    
    reflen = feature["end"] - feature["start"]
    
    counts_fw = counts["fw"]
    counts_rv = counts["rv"]
    
    miny,maxy = ylims
    
    if max(counts_fw) > ylims[1]:
        maxy = max(counts_fw)
    if stranded and min(counts_rv) < ylims[0]:
        miny = min(counts_rv)

    if stranded:
        fwcolordef = "blue"
    else:
        fwcolordef = "black"
    rvcolordef = "red"

    fig, ax = plt.subplots(figsize=(fwidth,fheight))
    fwax = ax.bar(center, counts_fw, align='center', width=width)
    if stranded:
        rvax = ax.bar(center, counts_rv, align='center', width=width)

    for (bin_start,patch) in zip(refbins,fwax.patches):
        patch.set_edgecolor("none")
        patch.set_color(fwcolordef)
        if "subfeatures" in feature:
            for sf in feature["subfeatures"]:
                try:
                    fwcolor = sf["fwcolor"]
                except KeyError:
                    try:
                        fwcolor = sf["color"]
                    except KeyError:
                        if stranded:
                            fwcolor = "blue"
                        else:
                            fwcolor = "black"

                if bin_start >= sf["start"] and bin_start < sf["end"]:
                    patch.set_color(fwcolor)
                    break

    if stranded:
        for (bin_start,patch) in zip(refbins,rvax.patches):
            patch.set_edgecolor("none")
            patch.set_color(rvcolordef)
            if "subfeatures" in feature:
                for sf in feature["subfeatures"]:
                    try:
                        rvcolor = sf["rvcolor"]
                    except KeyError:
                        try:
                            rvcolor = sf["color"]
                        except KeyError:
                            rvcolor = "red"

                    if bin_start >= sf["start"] and bin_start < sf["end"]:
                        patch.set_color(rvcolor)
                        break

    ax.set_title(title)
    ax.set_xlim(0,reflen)
    ax.set_ylim(miny,maxy)

    return(fig)

if __name__ == "__main__":
    import argparse,sys
    from common import *

    args = parsearguments()

    if args["features"]:
        featlist = args["features"].split(",")
    else:
        featlist = None

    featsfname = args["FEATURESFILE"]

    fext = os.path.splitext(featsfname)[1]

    if fext in [".gbk",".gb",".ape"]:
        features = processgbk(featsfname,featnames=featlist)
    elif fext == ".bed":
        features = processbed(featsfname,featnames=featlist)
    else:
        raise ValueError("Could not identify features file type from extension {}".format(fext))

    if args["ylims"]:
        ylims = [int(y) for y in args["ylims"].split(",")]
    else:
        ylims = (-1,1)

    for feature in features:

        try:
            counts,refbins,center,width,feature = fhist(args["ALNFILE"],feature,offsetup=args["offsetup"],offsetdown=args["offsetdown"],normfeat=args["normfeat"],stranded=args["stranded"],normnreads=args["normnreads"],normval=args["normval"],binsize=args["binsize"],length=args["length"],nt5p=args["5pnt"],nmaps=args["nmaps"],mmapweight=args["mmapweight"])

            fig = plot(counts,refbins,center,width,feature,title=args["ALNFILE"],ylims=ylims)

            fig.savefig(args["ALNFILE"].replace(".bam","_featurehist_{}.svg".format(feature["name"])))
        except:
            print("ERROR: something went wrong with {}. Skipping".format(feature))
