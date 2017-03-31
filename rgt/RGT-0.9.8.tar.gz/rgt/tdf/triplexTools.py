# Python Libraries
from __future__ import print_function
import os
import sys
import pysam
import shutil
import pickle
from ctypes import *
from collections import *
import natsort as natsort_ob

# Local Libraries
import numpy
numpy.seterr(divide='ignore', invalid='ignore')
import matplotlib
from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MaxNLocator


# Distal Libraries
from rgt.SequenceSet import SequenceSet
from rgt.viz.plotTools import output_array
from rgt.GenomicRegion import GenomicRegion
from RNADNABindingSet import RNADNABindingSet
from rgt.GenomicRegionSet import GenomicRegionSet
from rgt.motifanalysis.Statistics import multiple_test_correction
from rgt.Util import SequenceType, Html, ConfigurationFile, GenomeData, Library_path

# Color code for all analysis
target_color = "mediumblue"
nontarget_color = "darkgrey"
sig_color = "powderblue"

####################################################################################
####################################################################################

def print2(summary, string):
    """ Show the message on the console and also save in summary. """
    print(string)
    summary.append(string)


def output_summary(summary, directory, filename):
    """Save the summary log file into the defined directory"""
    pd = os.path.join(dir, directory)
    try:
        os.stat(pd)
    except:
        os.mkdir(pd)
    if summary:
        with open(os.path.join(pd, filename), 'w') as f:
            print("********* RGT Triplex: Summary information *********",
                  file=f)
            for s in summary:
                print(s, file=f)


def check_dir(path):
    """Check the availability of the given directory and creat it"""
    try: os.stat(path)
    except:
        try: os.mkdir(path)
        except: pass


def try_int(s):
    "Convert to integer if possible."
    try:
        return int(s)
    except:
        return s


def natsort_key(s):
    "Used internally to get a tuple by which s is sorted."
    import re
    return map(try_int, re.findall(r'(\d+|\D+)', s))


def natcmp(a, b):
    "Natural string comparison, case sensitive."
    return cmp(natsort_key(a), natsort_key(b))


def natcasecmp(a, b):
    "Natural string comparison, ignores case."
    return natcmp(a.lower(), b.lower())


def natsort(seq, cmp=natcmp):
    "In-place natural string sort."
    seq.sort(cmp)


def natsorted(seq, cmp=natcmp):
    "Returns a copy of seq, sorted by natural string sort."
    import copy
    temp = copy.copy(seq)
    natsort(temp, cmp)
    return temp


def list_all_index(path, link_d=None):
    """Creat an 'index.html' in the defined directory """

    dirname = os.path.basename(path)

    if link_d:
        pass
    else:
        link_d = {"List": "index.html"}

    html = Html(name="Directory: " + dirname, links_dict=link_d,
                fig_rpath="./style", fig_dir=os.path.join(path, "style"),
                RGT_header=False, other_logo="TDF", homepage="../index.html")

    html.add_heading("All experiments in: " + dirname + "/")

    data_table = []
    type_list = 'sssssssssssssssssss'
    col_size_list = [20] * 20
    c = 0

    header_list = ["No.", "Experiments", "RNA", "Closest genes",
                   "Exon", "Length", "Expression*",
                   "Norm DBS*",
                   "Norm DBD*",  "No sig. DBD",
                   "Organism", "Target region",
                   "Rank*"]

    profile_f = open(os.path.join(path, "profile.txt"), 'r')
    profile = {}
    for line in profile_f:
        line = line.strip()
        line = line.split("\t")
        if line[0] == "Experiment": continue
        elif len(line) > 5: profile[line[0]] = line[1:]
    profile_f.close()

    # sig_list = []

    for i, exp in enumerate(profile.keys()):
        c += 1
        if profile[exp][10] == "-":
            new_line = [str(c), exp, profile[exp][0]]
        else:
            new_line = [str(c),
                        '<a href="' + os.path.join(exp, "index.html") + \
                        '">' + exp + "</a>", profile[exp][0]]
        new_line += [ profile[exp][12],#3 close genes
                      profile[exp][1], #4 exon
                      profile[exp][2], #5 length
                      profile[exp][13] ]#6 exp

        if float(profile[exp][11]) < 0.05:
            new_line += [ profile[exp][6], #7 norm DBS
                          profile[exp][8], #8 norm DBD
                          profile[exp][9]] #9 sig DBD
                          # profile[exp][10], #10 Top DBD
                          # "<font color=\"red\">" + \
                          # profile[exp][11] + "</font>"]
            # sig_list.append(True)
        else:
            new_line += [str(0),  # 7 norm DBS
                         str(0),  # 8 norm DBD
                         profile[exp][9]]  # 9 sig DBD
                         # profile[exp][10],  # 10 Top DBD
                         # profile[exp][11]]
            # sig_list.append(False)

        new_line += [ profile[exp][4], profile[exp][5] ]

        data_table.append(new_line)

    rank_dbd = len(data_table) - rank_array([float(x[8]) for x in data_table])
    rank_dbs = len(data_table) - rank_array([float(x[7]) for x in data_table])

    rank_exp = len(data_table) - rank_array([0 if x[6] == "n.a." else float(x[6]) for x in data_table ])

    rank_sum = [x + y + z for x, y, z  in zip(rank_dbd, rank_dbs, rank_exp)]

    nd = [ d + [str(rank_sum[i])] for i, d in enumerate(data_table) ]

    nd = natsort_ob.natsorted(nd, key=lambda x: x[-1])
    html.add_zebra_table(header_list, col_size_list, type_list, nd,
                         align=10, cell_align="left", sortable=True)

    html.add_fixed_rank_sortable()
    html.write(os.path.join(path, "index.html"))


def revise_index(root):
    "Revise other index.html in the same project"

    dir_list = {}
    plist = {}
    for item in os.listdir(root):
        h = os.path.join(root, item, "index.html")
        pro = os.path.join(root, item, "profile.txt")
        if os.path.isfile(pro):
            dir_list[os.path.basename(item)] = "../" + item + "/index.html"
            plist[os.path.basename(item)] = h
    dir_list = OrderedDict(sorted(dir_list.items()))
    # print(dir_list)
    for d, p in plist.iteritems():
        list_all_index(path=os.path.dirname(p),
                       link_d=dir_list)

def update_profile(dirpath, expression, name_list=None):
    header_list = ["Experiment", "RNA_names", "Tag", "Organism", "Target_region", "No_sig_DBDs",
                   "Top_DBD", "p-value", "closest_genes"]
    profiles = []
    pro = os.path.join(dirpath, "profile.txt")
    if not os.path.isfile(pro):
        print("There is no profile.txt in this directory.")
        return

    if expression:
        gene_exp = {}
        with open(expression) as f:
            for line in f:
                l = line.strip().split()
                gene_exp[l[0].partition(".")[0]] = l[1]
        profile_temp = []
        with open(pro) as f:
            for line in f:
                if not line.startswith("Experiment"):
                    l = line.strip().split("\t")
                    if len(l) == 12:
                        profile_temp.append(l + [gene_exp[l[0]]])
        with open(pro, "w") as f:
            h = ["Experiment", "RNA_names", "exon", "length",
                 "Tag", "Organism", "Target_region",
                 "Norm_DBS", "Norm_DBS_on_sig_DBD",
                 "Norm_DBD", "No_sig_DBDs", "Top_DBD",
                 "p-value", "closest_genes", "expression"]
            print("\t".join(h), file=f)
            for line in profile_temp:
                print("\t".join(line), file=f)
    if name_list:
        pass
    else:
        for item in os.listdir(dirpath):
            stat = os.path.join(dirpath, item, "stat.txt")
            summary = os.path.join(dirpath, item, "summary.txt")
            if os.path.isfile(stat) and os.path.isfile(summary):
                with open(stat) as f:
                    for line in f:
                        l = line.strip().split()
                        if l[0] == "name":
                            each_name = l[1]
                            each_tag = l[1].split("_")[-1]
                        if l[0] == "genome": each_organism = l[1]
                        if l[0] == "DBD_sig": each_DBD_sig = l[1]
                        if l[0] == "p_value": each_p_value = l[1]
                with open(summary) as g:
                    for line in g:
                        if "rgt-TDF" in line and " -de " in line:
                            l = line.strip().split()
                            each_target_region = os.path.basename(l[l.index("-de") + 1])
                profiles.append([item,each_name,each_tag,each_organism,each_target_region,
                                 each_DBD_sig,"n.a.",each_p_value,"-"])

    with open(pro, "w") as f:
        print("\t".join(header_list), file=f)
        for line in profiles:
            print("\t".join(line), file=f)


def gen_heatmap(path):
    """Generate the heatmap to show the sig RNA in among conditions"""

    def fmt(x, pos):
        # a, b = '{:.0e}'.format(x).split('e')
        # b = int(b)
        # return r'${} \times 10^{{{}}}$'.format(a, b)
        a = -numpy.log10(x)
        return '{:.0f}'.format(a)

    matrix = OrderedDict()
    rnas = []
    for item in os.listdir(path):
        # print(item)
        # print(os.path.isdir(os.path.join(path,item)))
        if not os.path.isdir(os.path.join(path, item)): continue
        if item == "style": continue
        # if item == "index.html": continue
        matrix[item] = {}
        pro = os.path.join(path, item, "profile.txt")
        with open(pro) as f:
            for line in f:
                line = line.strip().split("\t")
                if line[0] == "Experiment": continue
                if line[6] == "-": continue
                matrix[item][line[0]] = float(line[7])
                rnas.append(line[0])
    rnas = list(set(rnas))
    # rnas.sort()

    # Convert into array
    ar = []
    exps = natsorted(matrix.keys())
    rnas = natsorted(rnas)
    # print(exps)
    for exp in exps:
        row = []
        for rna in rnas:
            try:
                row.append(matrix[exp][rna])
            except:
                row.append(1)
        ar.append(row)
    ar = numpy.array(ar)
    ar = numpy.transpose(ar)

    # print(ar.shape)
    data = ar[~numpy.all(ar == 1, axis=1)]
    # print(data.shape)


    fig = plt.figure(figsize=(len(matrix.keys()) * 1.5, len(rnas) * 2.5))
    # fig = plt.figure()
    # ax1 = fig.add_axes([0.09,0.2,0.2,0.6])
    # Y = sch.linkage(data, method='single')
    # Z1 = sch.dendrogram(Y, orientation='right')
    # ax1.set_xticks([])
    # ax1.set_yticks([])

    # Compute and plot second dendrogram.
    # ax2 = fig.add_axes([0.3, 1.1, 0.55,0.04])
    # Y = sch.linkage(data.T, method='single')
    # Z2 = sch.dendrogram(Y)
    # ax2.set_xticks([])
    # ax2.set_yticks([])
    bounds = []
    for n in range(-8, 0):
        # print(10**n)
        bounds.append(10 ** n)
    norm = colors.BoundaryNorm(bounds, plt.cm.YlOrRd_r.N)

    # Plot distance matrix.
    axmatrix = fig.add_axes([0.1, 0.2, 0.8, 0.6])
    # axmatrix = fig.add_axes()
    # idx1 = Z1['leaves']
    # idx2 = Z2['leaves']
    # data = data[idx1,:]
    # data = data[:,idx2]
    im = axmatrix.matshow(data, aspect='auto', origin='lower', cmap=plt.cm.YlOrRd_r, norm=norm)

    axmatrix.set_xticks(range(data.shape[1]))
    axmatrix.set_xticklabels(exps, minor=False, ha="left")
    axmatrix.xaxis.set_label_position('top')
    axmatrix.xaxis.tick_top()
    plt.xticks(rotation=40, fontsize=10)

    axmatrix.set_yticks(range(data.shape[0]))
    axmatrix.set_yticklabels(rnas, minor=False)
    # axmatrix.set_yticklabels( [ rnas[i] for i in idx1 ], minor=False)
    axmatrix.yaxis.set_label_position('right')
    axmatrix.yaxis.tick_right()
    plt.yticks(rotation=0, fontsize=10)
    # axmatrix.tight_layout()

    # Plot colorbar.
    axcolor = fig.add_axes([0.1, 0.1, 0.8, 0.02])

    plt.colorbar(im, cax=axcolor, orientation='horizontal', norm=norm,
                 boundaries=bounds, ticks=bounds, format=matplotlib.ticker.FuncFormatter(fmt))
    axcolor.set_xlabel('p value (-log10)')
    lmats = ar.tolist()
    for i, r in enumerate(rnas):
        lmats[i] = [r] + [str(x) for x in lmats[i]]
    lmats = [["p-value"] + exps] + lmats

    output_array(array=lmats, directory=path, folder="", filename='matrix_p.txt')
    # os.path.join(path,'matrix_p.txt'), lmats, delimiter='\t')
    try:
        fig.savefig(os.path.join(path, 'condition_lncRNA_dendrogram.png'))
        fig.savefig(os.path.join(path, 'condition_lncRNA_dendrogram.pdf'), format="pdf")
    except:
        pass


def generate_rna_exp_pv_table(root, multi_corr=True):
    "Generate p value table for Experiments vs RNA in the same project"

    nested_dict = lambda: defaultdict(nested_dict)
    # nested_dict = lambda: defaultdict(lambda: 'n.a.')

    data = nested_dict()
    rnas = []

    for item in os.listdir(root):
        pro = os.path.join(root, item, "profile.txt")
        if os.path.isfile(pro):
            with open(pro) as f:
                for line in f:
                    if line.startswith("Experiment"):
                        continue
                    else:
                        line = line.strip().split("\t")
                        data[item][line[0]] = float(line[7])
                        rnas.append(line[0])

    exp_list = sorted(data.keys())
    rnas = sorted(list(set(rnas)))

    pvs = []
    for rna in rnas:
        for exp in exp_list:
            if data[exp][rna]: pvs.append(data[exp][rna])
    if multi_corr:
        reject, pvals_corrected = multiple_test_correction(pvs, alpha=0.05, method='indep')
    else:
        pvals_corrected = pvs

    with open(os.path.join(root, "table_exp_rna_pv.txt"), "w") as t:
        print("\t".join(["RNA_ID"] + exp_list), file=t)
        i = 0
        for rna in rnas:
            newline = [rna]
            for exp in exp_list:
                if data[exp][rna]:
                    newline.append(str(pvals_corrected[i]))
                    i += 1
                else:
                    newline.append("n.a.")
            print("\t".join(newline), file=t)


def value2str(value):
    if (isinstance(value,str)):
        try: value = float(value)
        except: return value
    if value == 0: return "0"
    if(isinstance(value,int)): return str(value)
    elif(isinstance(value,float)):
        if abs(value) >= 1000: 
            try: r = "{}".format(int(value))
            except: r = "Inf"
        elif 1000 > abs(value) > 10: r = "{:.1f}".format(value)
        elif 10 > abs(value) >= 1: r = "{:.2f}".format(value)
        elif 1 > abs(value) >= 0.05: r = "{:.2f}".format(value)
        elif 0.05 > abs(value) > 0.0001: r = "{:.4f}".format(value)
        else: r = "{:.1e}".format(value)
        return r


def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]


def random_each(input):
    """Return the counts of DNA Binding sites with randomization
    For multiprocessing. 
    Input contains:
    0       1               2                3     4              5          6                    
    str(i), self.rna_fasta, self.dna_region, temp, self.organism, self.rbss, str(marks.count(i)),
    number, rna,            region,          temp, organism,      rbss,      number of mark

    7  8  9  10  11  12  13  14  15          16                 17
    l, e, c, fr, fm, of, mf, rm, filter_bed, self.genome_path,  par
    """
    import sys
    # Filter BED file
    if input[15]:
        random = input[2].random_regions(organism=input[4], multiply_factor=1,
                                         overlap_result=True, overlap_input=True,
                                         chrom_X=True, chrom_M=False, filter_path=input[15])
    else:
        random = input[2].random_regions(organism=input[4], multiply_factor=1,
                                         overlap_result=True, overlap_input=True,
                                         chrom_X=True, chrom_M=False)
    
    txp = find_triplex(rna_fasta=input[1], dna_region=random, temp=input[3],
                       organism=input[4], prefix=str(input[0]), remove_temp=True,
                       l=int(input[7]), e=int(input[8]), c=input[9], fr=input[10],
                       fm=input[11], of=input[12], mf=input[13], rm=input[14],
                       par=input[17], genome_path=input[16],
                       dna_fine_posi=False)

    txp.merge_rbs(rbss=input[5], rm_duplicate=True)

    txpf = find_triplex(rna_fasta=input[1], dna_region=random, temp=input[3], 
                       organism=input[4], prefix=str(input[0]), remove_temp=True, 
                       l=int(input[7]), e=int(input[8]),  c=input[9], fr=input[10], 
                       fm=input[11], of=input[12], mf=input[13], rm=input[14], 
                       par=input[17], genome_path=input[16],
                       dna_fine_posi=True)

    txpf.merge_rbs(rbss=input[5], rm_duplicate=True)
    sys.stdout.flush()
    print("".join(["="]*int(input[6])), end="")

    return [ [len(tr) for tr in txp.merged_dict.values() ], [len(dbss) for dbss in txpf.merged_dict.values()] ]


def get_sequence(dir, filename, regions, genome_path):
    """
    Fetch sequence into FASTA file according to the given BED file
    """
    genome = pysam.Fastafile(genome_path)
    with open(os.path.join(dir, filename), 'w') as output:
        for region in regions:
            if "_" not in region.chrom:
                print(">"+ region.toString(), file=output)
                print(genome.fetch(region.chrom, max(0, region.initial), region.final), file=output)


def find_triplex(rna_fasta, dna_region, temp, organism, l, e, dna_fine_posi, genome_path, prefix="", remove_temp=False, 
                 c=None, fr=None, fm=None, of=None, mf=None, rm=None, par=""):
    """Given a GenomicRegionSet to run Triplexator and return the RNADNABindingSet"""
    
    # Generate FASTA 
    get_sequence(dir=temp, filename="dna_"+prefix+".fa", regions=dna_region, genome_path=genome_path)

    # Triplexator
    run_triplexator(ss=rna_fasta, ds=os.path.join(temp,"dna_"+prefix+".fa"), 
                    output=os.path.join(temp, "dna_"+prefix+".txp"), 
                    l=l, e=e, c=c, fr=fr, fm=fm, of=of, mf=mf, rm=rm, par=par)
    # Read txp
    txp = RNADNABindingSet("dna")
    txp.read_txp(os.path.join(temp, "dna_"+prefix+".txp"), dna_fine_posi=dna_fine_posi)
    txp.remove_duplicates()

    if remove_temp:
        os.remove(os.path.join(temp,"dna_"+prefix+".fa"))
        os.remove(os.path.join(temp,"dna_"+prefix+".txp"))

    return txp

def run_triplexator(ss, ds, output, l=None, e=None, c=None, fr=None, fm=None, of=None, mf=None, rm=None, par=""):
    """Perform Triplexator"""
    #triplexator_path = check_triplexator_path()
    # triplexator -ss -ds -l 15 -e 20 -c 2 -fr off -fm 0 -of 1 -rm
    triclass = Library_path()
    triplex_lib_path = triclass.get_triplexator()
    triplex_lib  = cdll.LoadLibrary(triplex_lib_path)

    arguments = ""
    if ss: arguments += "-ss "+ss+" "
    if ds: arguments += "-ds "+ds+" "
    if l: arguments += "-l "+str(l)+" "
    if e: arguments += "-e "+str(e)+" "
    if c: arguments += "-c "+str(c)+" "
    if fr: arguments += "-fr "+fr+" "
    if fm: arguments += "-fm "+str(fm)+" "
    if of: arguments += "-of "+str(of)+" "
    if mf: arguments += "-mf "
    if rm: arguments += "-rm "+str(rm)+" "
    # arguments += "--bit-parallel "
    if par != "":
        par = par.replace('_'," ")
        par = "-" + par
        arguments += par+" "
    
    arguments += "-o "+ os.path.basename(output) + " -od " + os.path.dirname(output)

    arg_strings  = arguments.split(' ')
    arg_ptr      = (c_char_p * (len(arg_strings) + 1))()

    arg_ptr[0] = "triplexator"  # to simulate calling from cmd line
    for i, s in enumerate(arg_strings):
        arg_ptr[i + 1] = s
    
    triplex_lib.pyTriplexator(len(arg_strings) + 1, arg_ptr)
    os.remove(os.path.join(output + ".summary"))
    os.remove(os.path.join(output + ".log"))


def read_ac(path, cut_off, rnalen):
    """Read the RNA accessibility file and output its positions and values

    The file should be a simple table with two columns:
    The first column is the position and the second one is the value
    '#' will be skipped

    """
    access = []
    with open(path) as f:
        i = 0
        while i < rnalen:
            for line in f:
                line = line.split()
                if not line: continue
                elif line[0][0] == "#": continue
                elif len(line) < 2: continue
                else:
                    v = line[1]
                    if v == "NA": 
                        access.append(0)
                    else: 
                        try: v = 2**(-float(v))
                        except: continue
                        if v >= cut_off:
                            access.append(1)
                        else:
                            access.append(0)
                    i += 1
    return access

def region_link_internet(organism, region):
    ani = None
    if organism == "hg19":
        ani = "human"
    elif organism == "hg38":
        ani = "human"
    elif organism == "mm9":
        ani = "mouse"
    if ani:
        region_link = "".join(['<a href="http://genome.ucsc.edu/cgi-bin/hgTracks?db=', organism,
                               "&position=", region.chrom, "%3A", str(region.initial), "-",
                               str(region.final), '" style="text-align:left" target="_blank">',
                               region.toString(space=True), '</a>'])
    else:
        if organism == "tair10":
            region_link = "".join(
                ['<a href="http://tairvm17.tacc.utexas.edu/cgi-bin/gb2/gbrowse/arabidopsis/?name=',
                 region.chrom, "%3A", str(region.initial), "..", str(region.final),
                 '" target="_blank">',
                 region.toString(space=True), '</a>'])
        else:
            region_link = region.toString(space=True)
    return region_link


def split_gene_name(gene_name, org):
    
    if gene_name == None:
        return ""
    if gene_name[0:2] == "chr":
        return gene_name

    if org=="hg19": ani = "human"
    elif org=="hg38": ani = "human"
    elif org=="mm9": ani = "mouse"
    else: ani = None

    if not ani:
        if org == "tair10":
            p1 = "".join(['<a href="https://www.arabidopsis.org/servlets/TairObject?name=', gene_name,
                          '&type=locus" target="_blank">', gene_name, '</a>' ])
            return p1
        else:
            return gene_name
    else:    
        p1 = '<a href="http://genome.ucsc.edu/cgi-bin/hgTracks?org='+ani+\
             "&db="+org+"&singleSearch=knownCanonical&position="
        p2 = '" style="text-align:left" target="_blank">'
        p3 = '</a>'

        if ":" in gene_name:
            genes = gene_name.split(":")
            genes = list(set(genes))
            result = []
            c = 0
            for i, g in enumerate(genes):
                if "(" in g:
                    d = g.partition('(')[2].partition(')')[0]
                    g = g.partition('(')[0]
                    if "-" in d:
                        result.insert(0, p1+g+p2+g+p3+"("+d+")")
                    else:
                        result.append(p1+g+p2+g+p3+"("+d+")")
                else:
                    c += 1
                    if c < 6:
                        result.append(p1 + g + p2 + g + p3)

            result = ",".join(result)

        elif gene_name == ".":
            result = "none"

        else:
            if "(" in gene_name:
                d = gene_name.partition('(')[2].partition(')')[0]
                g = gene_name.partition('(')[0]
                result = p1+g+p2+g+p3+"("+d+")"
            else:
                result = p1+gene_name+p2+gene_name+p3
        
        return result


def lineplot(txp, rnalen, rnaname, dirp, sig_region, cut_off, log, ylabel, linelabel, 
             filename, ac=None, showpa=False, exons=None):
    # Plotting
    f, ax = plt.subplots(1, 1, dpi=300, figsize=(6,4))
    
    # Extract data points
    x = range(rnalen)
    #print(rnalen)
    if log:
        all_y = [1] * rnalen
        p_y = [1] * rnalen
        a_y = [1] * rnalen
    else:
        all_y = [0] * rnalen
        p_y = [0] * rnalen
        a_y = [0] * rnalen

    txp.remove_duplicates_by_dbs()
    for rd in txp:
        #print(str(rd.rna.initial), str(rd.rna.final))
        if rd.rna.orientation == "P":
            for i in range(rd.rna.initial, rd.rna.final):
                p_y[i] += 1
                all_y[i] += 1
        if rd.rna.orientation == "A":
            for i in range(rd.rna.initial, rd.rna.final):
                a_y[i] += 1
                all_y[i] += 1
    # Log
    if log:
        all_y = numpy.log(all_y)
        p_y = numpy.log(p_y)
        a_y = numpy.log(a_y)
        max_y = max(all_y)+0.5
        min_y = 1
        ylabel += "(log10)"
    else:
        max_y = float(max(all_y) * 1.1)
        min_y = 0

    if ac:
        min_y = float(max_y*(-0.09))
    
    
    # Plotting
    for rbs in sig_region:
        rect = patches.Rectangle(xy=(rbs.initial,0), width=len(rbs), height=max_y, facecolor=sig_color, 
                                 edgecolor="none", alpha=0.5, lw=None, label="Significant DBD")
        ax.add_patch(rect)
    
    lw = 1.5
    if showpa:
        ax.plot(x, all_y, color=target_color, alpha=1, lw=lw, label="Parallel + Anti-parallel")
        ax.plot(x, p_y, color="purple", alpha=1, lw=lw, label="Parallel")
        ax.plot(x, a_y, color="dimgrey", alpha=.8, lw=lw, label="Anti-parallel")
    else:
        ax.plot(x, all_y, color="mediumblue", alpha=1, lw=lw, label=linelabel)

    # RNA accessbility
    if ac:
        n_value = read_ac(ac, cut_off, rnalen=rnalen)
        drawing = False
        for i in x:
            if n_value[i] > 0:
                if drawing:
                    continue
                else:
                    last_i = i
                    drawing = True
            elif drawing:
                pac = ax.add_patch(patches.Rectangle((last_i, min_y), i-last_i, -min_y,
                                   hatch='///', fill=False, snap=False, linewidth=0, label="RNA accessibility"))
                drawing = False
            else:
                continue

    # Legend
    handles, labels = ax.get_legend_handles_labels()
    legend_h = []
    legend_l = []
    for uniqlabel in uniq(labels):
        legend_h.append(handles[labels.index(uniqlabel)])
        legend_l.append(uniqlabel)
    ax.legend(legend_h, legend_l, 
              bbox_to_anchor=(0., 1.02, 1., .102), loc=2, mode="expand", borderaxespad=0., 
              prop={'size':9}, ncol=3)

    # XY axis
    ax.set_xlim(left=0, right=rnalen )
    ax.set_ylim( [min_y, max_y] ) 
    for tick in ax.xaxis.get_major_ticks(): tick.label.set_fontsize(9) 
    for tick in ax.yaxis.get_major_ticks(): tick.label.set_fontsize(9) 
    ax.set_xlabel(rnaname+" sequence (bp)", fontsize=9)
    
    ax.set_ylabel(ylabel,fontsize=9, rotation=90)
    
    if None:
        if exons and len(exons) > 1:
            w = 0
            i = 0
            h = (max_y - min_y)*0.02

            for exon in exons:
                l = abs(exon[2] - exon[1])
                
                #print([i,l,w])
                #ax.axvline(x=w, color="gray", alpha=0.5, zorder=100)
                if i % 2 == 0:
                    rect = matplotlib.patches.Rectangle((w,max_y-h),l,h, color="moccasin")
                else:
                    rect = matplotlib.patches.Rectangle((w,max_y-h),l,h, color="gold")
                ax.add_patch(rect)
                i += 1
                w += l
            ax.text(rnalen*0.01, max_y-2*h, "exon boundaries", fontsize=5, color='black')

    f.tight_layout(pad=1.08, h_pad=None, w_pad=None)

    f.savefig(os.path.join(dirp, filename), facecolor='w', edgecolor='w',  
              bbox_extra_artists=(plt.gci()), bbox_inches='tight', dpi=300)
    # PDF
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(12) 
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    ax.xaxis.label.set_size(14)
    ax.yaxis.label.set_size(14) 
    ax.legend(legend_h, legend_l, 
              bbox_to_anchor=(0., 1.02, 1., .102), loc=2, mode="expand", borderaxespad=0., 
              prop={'size':12}, ncol=3)
    pp = PdfPages(os.path.splitext(os.path.join(dirp,filename))[0] +'.pdf')
    pp.savefig(f,  bbox_inches='tight') # bbox_extra_artists=(plt.gci()),
    pp.close()

def load_dump(path, filename):
    file = open(os.path.join(path,filename),'r')
    object = pickle.load(file)
    file.close()
    print("\tLoading from file: "+filename)
    return object

def dump(object, path, filename):
    file = open(os.path.join(path,filename),'wb')
    pickle.dump(object,file)
    file.close()
    print("\tDump to file: "+filename)

def check_triplexator_path():
    try:
        cf = ConfigurationFile()
        with open(os.path.join(cf.data_dir,"triplexator_path.txt")) as f:
            l = f.readline()
            l = l.strip("\n")
            return l
    except:
        print("Please define the path to Triplexator by command: rgt-TDF triplexator -path <PATH>")
        sys.exit(1)
    
def rna_associated_gene(rna_regions, name, organism):
    if rna_regions:
        s = [ rna_regions[0][0], min([e[1] for e in rna_regions]), 
              max([e[2] for e in rna_regions]), rna_regions[0][3] ]
        g = GenomicRegionSet("RNA associated genes")
        g.add( GenomicRegion(chrom=s[0], initial=s[1], final=s[2], name=name, orientation=s[3]) )
        asso_genes = g.gene_association(organism=organism, promoterLength=1000, show_dis=True)

        genes = asso_genes[0].name.split(":")
        closest_genes = []
        for n in genes:
            if name not in n: closest_genes.append(n)
        closest_genes = set(closest_genes)

        if len(closest_genes) == 0:
            return "."
        else:
            return ":".join(closest_genes)
    else:
        return "."

def rank_array(a):
    try:
        a = numpy.array(a)
    except:
        a = numpy.array([float(b) for b in a])
    sa = numpy.searchsorted(numpy.sort(a), a)
    return sa

def dbd_regions(exons, sig_region, rna_name, output,out_file=False, temp=None, fasta=True):
    """Generate the BED file of significant DBD regions and FASTA file of the sequences"""
    if len(sig_region) == 0:
        return
    #print(self.rna_regions)
    if not exons:
        pass
    else:
        dbd = GenomicRegionSet("DBD")
        dbdmap = {}
        if len(exons) == 1:
            print("## Warning: No information of exons in the given RNA sequence, the DBD position may be problematic. ")
        for rbs in sig_region:
            loop = True

            if exons[0][3] == "-":
                while loop:
                    cf = 0
                    for exon in exons:
                        #print(exon)

                        l = abs(exon[2] - exon[1])
                        tail = cf + l

                        if cf <= rbs.initial <=  tail:
                            dbdstart = exon[2] - rbs.initial + cf
                            
                            if rbs.final <= tail: 
                                #print("1")
                                dbdend = exon[2] - rbs.final + cf
                                if dbdstart > dbdend: dbdstart, dbdend = dbdend, dbdstart
                                dbd.add( GenomicRegion(chrom=exons[0][0], 
                                                       initial=dbdstart, final=dbdend, 
                                                       orientation=exons[0][3], 
                                                       name=str(rbs.initial)+"-"+str(rbs.final) ) )
                                dbdmap[str(rbs)] = dbd[-1].toString() + " strand:-"
                                loop = False
                                break
                            elif rbs.final > tail:

                                subtract = l + cf - rbs.initial
                                #print("2")
                                #print("Subtract: "+str(subtract))
                                if dbdstart > exon[1]: dbdstart, exon[1] = exon[1], dbdstart
                                dbd.add( GenomicRegion(chrom=exons[0][0], 
                                                       initial=dbdstart, final=exon[1], 
                                                       orientation=exons[0][3], 
                                                       name=str(rbs.initial)+"-"+str(rbs.initial+subtract)+"_split1" ) )
                        
                        elif rbs.initial < cf and rbs.final <= tail: 
                            #print("3")
                            dbdstart = exon[2]
                            dbdend = exon[2] - rbs.final + rbs.initial + subtract
                            if dbdstart > dbdend: dbdstart, dbdend = dbdend, dbdstart
                            dbd.add( GenomicRegion(chrom=exons[0][0], 
                                                   initial=dbdstart, final=dbdend, 
                                                   orientation=exons[0][3], 
                                                   name=str(cf)+"-"+str(rbs.final)+"_split2" ) )
                            dbdmap[str(rbs)] = dbd[-2].toString() + " & " + dbd[-1].toString() + " strand:-"
                            loop = False
                            break

                        elif rbs.initial > tail:
                            pass

                        cf += l
                        
                    loop = False
            else:

                while loop:
                    cf = 0
                    for exon in exons:
                        #print(exon)
                        l = exon[2] - exon[1]
                        tail = cf + l
                        #print("cf:   " + str(cf))
                        #print("tail: " + str(tail) )
                        if cf <= rbs.initial <=  tail:
                            dbdstart = exon[1] + rbs.initial - cf
                            
                            if rbs.final <= tail: 
                                #print("1")
                                dbdend = exon[1] + rbs.final -cf
                                dbd.add( GenomicRegion(chrom=exons[0][0], 
                                                       initial=dbdstart, final=dbdend, 
                                                       orientation=exons[0][3], 
                                                       name=str(rbs.initial)+"-"+str(rbs.final) ) )
                                dbdmap[str(rbs)] = dbd[-1].toString() + " strand:+"
                                loop = False
                                break
                            elif rbs.final > tail:

                                subtract = l + cf - rbs.initial
                                #print("2")
                                #print("Subtract: "+str(subtract))
                                dbd.add( GenomicRegion(chrom=exons[0][0], 
                                                       initial=dbdstart, final=exon[2], 
                                                       orientation=exons[0][3], 
                                                       name=str(rbs.initial)+"-"+str(rbs.initial+subtract)+"_split1" ) )

                        elif rbs.initial < cf and rbs.final <= tail: 
                            #print("3")
                            dbdstart = exon[1]
                            dbdend = exon[1] + rbs.final - rbs.initial - subtract
                            dbd.add( GenomicRegion(chrom=exons[0][0], 
                                                   initial=dbdstart, final=dbdend, 
                                                   orientation=exons[0][3], 
                                                   name=str(cf)+"-"+str(rbs.final)+"_split2" ) )
                            dbdmap[str(rbs)] = dbd[-2].toString() + " & " + dbd[-1].toString() + " strand:+"
                            loop = False
                            break

                        elif rbs.initial > tail:
                            pass

                        cf += l
                        
                    loop = False
        if not out_file:
            dbd.write_bed(filename=os.path.join(output, "DBD_"+rna_name+".bed"))
        else:
            # print(dbd)
            # print(dbd.sequences[0])
            dbd.write_bed(filename=output)
    # FASTA
    if fasta:
        #print(dbdmap)
        if not out_file:
            seq = pysam.Fastafile(os.path.join(output,"rna_temp.fa"))
            fasta_f = os.path.join(output, "DBD_"+rna_name+".fa")
        else:
            seq = pysam.Fastafile(os.path.join(temp,"rna_temp.fa"))
            fasta_f = output+".fa"

        with open(fasta_f, 'w') as fasta:
            for rbs in sig_region:
                print(">"+ rna_name +":"+str(rbs.initial)+"-"+str(rbs.final), file=fasta)
                s = seq.fetch(rbs.chrom, max(0, rbs.initial), rbs.final)
                for ss in [s[i:i + 80] for i in range(0, len(s), 80)]:
                    print(ss, file=fasta)

def connect_rna(rna, temp, rna_name):
    """Generate FASTA file merging all exons and return the number of exons and sequence length"""
    seq = ""
    exons = 0
    with open(rna) as f:
        for line in f:
            if line.startswith(">"):
                exons += 1
            else:
                line = line.strip()
                seq += line

    with open(os.path.join(temp,"rna_temp.fa"), "w") as r:
        print(">"+rna_name, file=r)
        for s in [seq[i:i + 80] for i in range(0, len(seq), 80)]:
            print(s, file=r)
    return [exons, len(seq)]

def get_dbss(input_BED,output_BED,rna_fasta,output_rbss,organism,l,e,c,fr,fm,of,mf,rm,temp):
    regions = GenomicRegionSet("Target")
    regions.read_bed(input_BED)
    regions.gene_association(organism=organism, show_dis=True)

    connect_rna(rna_fasta, temp=temp, rna_name="RNA")
    rnas = SequenceSet(name="rna", seq_type=SequenceType.RNA)
    rnas.read_fasta(os.path.join(temp,"rna_temp.fa"))
    rna_regions = get_rna_region_str(os.path.join(temp,rna_fasta))
    # print(rna_regions)
    genome = GenomeData(organism)
    genome_path = genome.get_genome()
    txp = find_triplex(rna_fasta=rna_fasta, dna_region=regions, 
                       temp=temp, organism=organism, remove_temp=False,
                       l=l, e=e, c=c, fr=fr, fm=fm, of=of, mf=mf, genome_path=genome_path,
                       prefix="targeted_region", dna_fine_posi=True)

    print("Total binding events:\t",str(len(txp)))
    txp.write_bed(output_BED)
    txp.write_txp(filename=output_BED.replace(".bed",".txp"))
    rbss = txp.get_rbs()
    dbd_regions(exons=rna_regions, sig_region=rbss, rna_name="rna", output=output_rbss, 
                out_file=True, temp=temp, fasta=False)
    # print(rbss.sequences)
    # print(len(rbss))
    # rbss.write_bed(output_rbss)

def get_rna_region_str(rna):
    """Getting the rna region from the information header with the pattern:
            REGION_chr3_51978050_51983935_-_
        or  chr3:51978050-51983935 -    """
    rna_regions = []
    with open(rna) as f:
        for line in f:
            if line[0] == ">":
                line = line.strip()
                # Loci
                if "REGION" in line:
                    l = line.split()
                    for i, e in enumerate(l):
                        if "REGION" in e:
                            e = e.split("_")
                            #print(e)
                            try:
                                r = [e[1], int(e[2]), int(e[3]), e[4]]
                            except:
                                r = [e[1], int(e[3]), int(e[4]), e[5]]
                
                elif "chr" in line:
                    try:
                        l = line.partition("chr")[2]
                        chrom = "chr" + l.partition(":")[0]
                        start = int(l.partition(":")[2].partition("-")[0])
                        end = int(l.partition(":")[2].partition("-")[2].split()[0])
                        sign = l.partition(":")[2].partition("-")[2].split()[1]
                        if sign == "+" or sign == "-" or sign == ".":
                            r = [chrom, start, end, sign]
                        elif "strand" in line:
                            s = l.partition("strand=")[2][0]
                            r = [chrom, start, end, s]
                        else:
                            print(line)
                    except:
                        break

                else:
                    r = []
                # Score
                if "score" in line:
                    ss = line.partition("score")[2].partition("=")[2]
                    score = float(ss.split()[0])
                    r.append(score)
                if r:
                    rna_regions.append(r)
    # if rna_regions:
    #     rna_regions.sort(key=lambda x: x[1])
    #     if rna_regions[0][3] == "-":
    #         rna_regions = rna_regions[::-1]

    return rna_regions


def no_binding_response(args, rna_regions, rna_name, organism, stat, expression):
    print("*** Find no DBD having DBS with cutoff = "+str(args.ccf))

    pro_path = os.path.join(os.path.dirname(args.o), "profile.txt")
    exp = os.path.basename(args.o)
    try:
        if args.de:
            tar = args.de
        else:
            tar = args.bed
    except:
        tar = args.bed
    stat["DBD_all"] = 0
    stat["DBSs_target_all"] = 0
    stat["DBSs_target_DBD_sig"] = 0

    save_profile(rna_regions=rna_regions, rna_name=rna_name,
                 organism=organism, output=args.o, bed=args.bed,
                 geneset=tar, stat=stat, topDBD=["-", 1], sig_DBD=[],
                 expression=expression)

    revise_index(root=os.path.dirname(os.path.dirname(args.o)))
    shutil.rmtree(args.o)
    sys.exit(1)

def write_stat(stat, filename):
    """Write the statistics into file"""
    order_stat = ["name", "genome", "exons", "seq_length",
                  "target_regions", "background_regions",
                  "DBD_all", "DBD_sig",
                  "DBSs_target_all", "DBSs_target_DBD_sig",
                  "DBSs_background_all", "DBSs_background_DBD_sig", "p_value"]
    with open(filename, "w") as f:
        for k in order_stat:
            try:
                print("\t".join([k,stat[k]]), file=f)
            except:
                continue

def integrate_stat(path):
    """Integrate all statistics within a directory"""
    base = os.path.basename(path)
    order_stat = ["name", "genome", "exons", "seq_length",
                  "target_regions", "background_regions",
                  "DBD_all", "DBD_sig",
                  "DBSs_target_all", "DBSs_target_DBD_sig",
                  "DBSs_background_all", "DBSs_background_DBD_sig", "p_value"]
    nested_dict = lambda: defaultdict(nested_dict)
    data = nested_dict()

    for item in os.listdir(path):
        pro = os.path.join(path, item, "stat.txt")
        if os.path.isfile(pro):
            with open(pro) as f:
                for line in f:
                    l = line.split()
                    data[item][l[0]] = l[1]
    with open(os.path.join(path,"statistics_"+base+".txt"), "w") as g:
        print("\t".join(order_stat), file=g)

        for item in data.keys():
            print("\t".join([data[item][o] for o in order_stat]), file=g)

def merge_DBD_regions(path):
    """Merge all available DBD regions in BED format. """

    for t in os.listdir(path):
        if os.path.isdir(os.path.join(path, t)):
            dbd_pool = GenomicRegionSet(t)
            for rna in os.listdir(os.path.join(path,t)):
                f = os.path.join(path, t, rna, "DBD_"+rna+".bed")
                if os.path.exists(f):
                    dbd = GenomicRegionSet(rna)
                    dbd.read_bed(f)
                    for r in dbd: r.name = rna+"_"+r.name
                    dbd_pool.combine(dbd)
            dbd_pool.write_bed(os.path.join(path, t, "DBD_"+t+".bed"))


def save_profile(rna_regions, rna_name, organism, output, bed,\
                 stat, topDBD, sig_DBD, expression, geneset=None):
    """Save statistics for comparison with other results"""

    pro_path = os.path.join(os.path.dirname(output), "profile.txt")
    exp = os.path.basename(output)
    # tag = os.path.basename(os.path.dirname(rnafile))
    if geneset:
        tar_reg = os.path.basename(geneset)
    else:
        tar_reg = os.path.basename(bed)
    # RNA name with region
    # if rna_regions:
    #     exon = str(len(rna_regions))
    # else:
    #     exon = "-"
    # rna = self.rna_name
    # RNA associated genes
    r_genes = rna_associated_gene(rna_regions=rna_regions, name=rna_name, organism=organism)

    newlines = []

    this_rna = [exp, rna_name, stat["exons"], stat["seq_length"],
                output.split("_")[-1], organism, tar_reg,
                value2str(float(stat["DBSs_target_all"])/int(stat["seq_length"])*1000),
                value2str(float(stat["DBSs_target_DBD_sig"])/int(stat["seq_length"])*1000),
                value2str(float(stat["DBD_all"])/int(stat["seq_length"])*1000), str(len(sig_DBD)),
                topDBD[0], value2str(topDBD[1]), r_genes, value2str(expression)]
    # try:
    if os.path.isfile(pro_path):
        with open(pro_path, 'r') as f:
            new_exp = True
            for line in f:
                line = line.strip()
                line = line.split("\t")
                if line[0] == exp:
                    newlines.append(this_rna)
                    new_exp = False
                elif line[0] == "Experiment":
                    continue
                else:
                    newlines.append(line)
            if new_exp:
                newlines.append(this_rna)
    else:
        newlines.append(this_rna)

    try: newlines.sort(key=lambda x: float(x[12]))
    except: pass
    newlines = [["Experiment", "RNA_names", "exon", "length",
                 "Tag", "Organism", "Target_region",
                 "Norm_DBS", "Norm_DBS_on_sig_DBD",
                 "Norm_DBD", "No_sig_DBDs", "Top_DBD",
                 "p-value", "closest_genes", "expression"]] + newlines

    with open(pro_path, 'w') as f:
        for lines in newlines:
            print("\t".join(lines), file=f)