#!/usr/bin/env python


"""
./get_stats output_file lib_dir1 [,libdir2 [,libdirN]]

Gather stats (nb of reads) from input files and mapping and
remove-duplicates in a table.
"""


import re
import sys
import pysam
import os.path
import shlex
from subprocess import check_output
from glob import glob


class bowtie2statsError(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)


def get_bowtie2stats(file_):
    if not file_:
        return (None, None)

    with open(file_) as IN:
        lines = IN.readlines()
    
    reg_blank = re.compile(r'^$')
    regex = [
        # tuple (name of the retrieved number, pattern)
        ('tot',  r'^(\d+) reads(?:; of these:)?$'),
        ('p',    r'^  \d+ \([0-9\.]+%\) were (paired|unpaired); of these:$'),
        ('pc0',  r'^    (\d+) \([0-9\.]+%\) aligned concordantly 0 times$'),
        ('pc1',  r'^    (\d+) \([0-9\.]+%\) aligned concordantly exactly 1 time$'),
        ('pc2',  r'^    (\d+) \([0-9\.]+%\) aligned concordantly >1 times$'),
        ('_',    r'^    ----$'),
        ('pc0_2',r'^    (\d+) pairs aligned concordantly 0 times; of these:$'),
        ('pd1',  r'^      (\d+) \([0-9\.]+%\) aligned discordantly 1 time$'),
        ('pd2',  r'^      (\d+) \([0-9\.]+%\) aligned discordantly >1 times$'), #probably never happens
        ('_',   r'^    ----$'),
        ('s',   r'^    (\d+) pairs aligned 0 times concordantly or discordantly; of these:$'),
        ('sp',   r'^      (\d+) mates make up the pairs; of these:$'),
        ('s0',   r' {4,8}(\d+) \([0-9\.]+%\) aligned 0 times$'),
        ('s1',   r' {4,8}(\d+) \([0-9\.]+%\) aligned exactly 1 time$'),
        ('s2',   r' {4,8}(\d+) \([0-9\.]+%\) aligned >1 times$'),
        ('rate', r'^([0-9\.]+)% overall alignment rate$')]

    regex = [(name, re.compile(pattern)) for name,pattern in regex]
    matched = {}
    unmatched = []

    # read the file until it finds the first match of the expected message
    name0, reg0 = regex[0]
    
    if not lines:
        raise bowtie2statsError("File %s is empty." % file_)

    match0 = reg0.match(lines[0])
    while not match0 and len(lines)>1:
        if not reg_blank.match(lines[0]):
            unmatched += [lines.pop(0)]
        else:
            lines.pop(0)
        match0 = reg0.match(lines[0])
    if not match0:
        raise bowtie2statsError("File %s does not contain bowtie2 read counts." % file_)

    # then match lines in their expected order
    for name, reg in regex:
        match = reg.match(lines[0])
        if match:
            lines.pop(0)
            matched[name] = match.group(1) if name != '_' else match.group()
        else:
            matched[name] = 0  # to allow summing these names
    
    unmatched += lines  # lines should be empty if everything has matched

    if unmatched:
        unmatched = unmatched[:10] + [" + %s more..." %(len(unmatched)-10,)] if len(unmatched)>10 else unmatched
        sys.stderr.write("In %s those lines did not match:\n%s\n" %(file_, "\n".join(unmatched) ))

    tot = int(matched['tot'])
    if matched['p'] == 'paired':
        tot *= 2

    mapped  = int(matched['s1']) + int(matched['s2'])
    mapped += 2 * (int(matched['pc1']) + int(matched['pc2']))

    return tot, mapped



def get_readcount(bamfile, cmd="samtools view -c {}".format):
    if bamfile:
        readcount = check_output(shlex.split(cmd(bamfile)))
        return(int(readcount.rstrip("\n")), )
    else:
        return (None, )
    

def _get_readcount(bamfile):
    if bamfile:
        readcount = pysam.view("-c", bamfile)[0]
        return (int(readcount),)
    else:
        return (None,)


def grab_files(pattern, directories):
    for libdir in directories:
        found = glob(os.path.join(libdir, pattern))
        yield found[0] if found else None  # only keeps one file per directory


def make_lines(ttable, fields, func, fieldtuple, elemlist):
    lines = zip(*[func(e) for e in elemlist])
    for line, field in zip(lines, fieldtuple):
        if any(line):
            ttable[field] = line
            fields.append(field)


def gather_stats(output_file, directories, IDs=None):
    """IDs is a list of sample_lib names corresponding to the directories"""
    
    if not IDs:
        IDs = directories

    ttable = {"sample_lib": IDs}
    fields = ["sample_lib"]

    for trimmed_type in ['collapsed', 'paired', 'singles']:
        make_lines(ttable,
                   fields,
                   func = get_bowtie2stats,
                   fieldtuple = (trimmed_type+'.tot', trimmed_type+'.mapped'),
                   elemlist = list(grab_files('*.%s.bowtie2out.stats' % trimmed_type,
                                              directories)))
    
        make_lines(ttable,
                   fields,
                   func = get_readcount,
                   fieldtuple = (trimmed_type + '.no_dup',),
                   elemlist = list(grab_files(
                                   '*.%s.bowtie2out*.sorted.no_dup.bam' % trimmed_type,
                                              directories)))

    # compute totals if more than 1 trimmed_type
    for result_type in ['tot', 'mapped', 'no_dup']:
        fromfields = [t+result_type for t in ['collapsed.', 'paired.', 'singles.']]
        fromfields = [f for f in fromfields if ttable.get(f)]
        if len(fromfields) > 1:
            make_lines(ttable,
                       fields,
                       func = lambda tup :(sum(x for x in tup if not x is None),),
                       fieldtuple = ('sum.'+result_type,),
                       elemlist = zip(*(ttable[f] for f in fromfields)))
   
    with open(output_file, 'w') as OUT:
        OUT.write('\t'.join(fields) + '\n')
        for line in zip(*(ttable[field] for field in fields)):
            line = [str(count) for count in line]
            OUT.write("\t".join(line) + '\n')
    

if __name__ == '__main__':
    
    if len(sys.argv) > 2:
        output_file = sys.argv[1]
        directories = []
        for arg in sys.argv[2:]:
            directories.extend(glob(arg))

        gather_stats(output_file, directories)
    else:
        sys.exit(__doc__)

