from tstk.io import parsefastx,openfastx

compnt = {'A':'T','C':'G','G':'C','T':'A','N':'N'}

revcomp = lambda x: ''.join([compnt[B] for B in x][::-1])

def featurecountsdf(fname,allcolumns=False):
    import pandas as pd

    df = pd.read_table(fname,sep="\t",header=1) 
    if not allcolumns:
        cols = ["Geneid"] + [c for c in df.columns[df.columns.get_loc("Length"):]]
        df = df[cols]

    return df

def get_nreads_from_collapsed(fname):
        return sum(int(r[0].split("-")[1]) for r in parsefastx(openfastx(fname)[3]))

def get_aligned_nreads(fname,s="STAR"):
    ''' Gets counts of aligned reads from STAR output '''
    if s == "STAR":
        with open(fname) as f:
            nreads = {}
            for r in f:
                if "Number of input reads" in r:
                    nreads["input"] = int(r.split()[-1])
                elif "Uniquely mapped reads number" in r:
                    nreads["unique"] = int(r.split()[-1])
                elif "Number of reads mapped to multiple loci" in r:
                    nreads["mmap"] = int(r.split()[-1])
    else:
        raise ValueError("Unknown aligner '{}'".format(s))    

    return nreads
