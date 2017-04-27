def parsearguments():
    import argparse,sys

    epilog = """============================== Alea jacta est =============================="""
    parser = argparse.ArgumentParser(epilog=epilog,formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('INFNAME',help="Path to the xam or fastx file containing the reads")
    parser.add_argument('OUTFNAME',help="Output file name (fasta only).")
    parser.add_argument('--minreads',help="Minimum number of reads for a sequence to be reported.",type=int,default=1)

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    return(vars(parser.parse_args()))

def main():
    from tstk.io import openfastx,parsefastx
    from tstk.common import revcomp
    import pysam
    import sys,collections,os

    args = parsearguments()

    INFNAME = args["INFNAME"]
    OUTFNAME = args["OUTFNAME"]

    fpathnoext, fext = os.path.splitext(INFNAME)

    if fext in [".bam",".sam"]:
        entries = [entry for entry in pysam.AlignmentFile(INFNAME,"rb") if dict(entry.get_tags())["HI"] == 1]# only get the first entry in case of multi-mappers
        entries = [revcomp(str(e.seq)) if e.is_reverse else str(e.seq) for e in entries]
        counter = collections.Counter(entries) #only include one hit from the multi mappers
    else:
        fpathnoext,fext,ftype,fh = openfastx(INFNAME)
        seqs = [str(seq) for name,seq,qual in parsefastx(fh)]
        counter = collections.Counter(seqs)
        fh.close()

    if OUTFNAME.endswith(".csv"):
        ofh = open(OUTFNAME,"w")
    else:
        ofpathnoext,ofext,oftype,ofh = openfastx(OUTFNAME.replace("fastq","fasta"),mode='wt')

    seqid = 1
    for seq in counter.most_common():
        seqstr = seq[0]
        nreads = int(seq[1])
        if nreads < args["minreads"]:
            break
        if OUTFNAME.endswith(".csv"):
            ofh.write("{}\t{}\n".format(nreads,seqstr))
        else:
            ofh.write(">{}-{}\n{}\n".format(seqid,nreads,seqstr))
        seqid += 1

    ofh.close()

if __name__ == "__main__":

    main()
