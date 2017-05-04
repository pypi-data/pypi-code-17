__version__ = '0.0.1'


def translate(seq, tid=1, trim_aster=False):
    """
    :param seq: 
    :param tid: translate table id
    :param trim_aster: 
    """
    from joker.bioinfo.translation import CodonTable
    return CodonTable.load(tid).translate(seq, trim_aster=trim_aster)


def revcompl(seq, typ='dna'):
    """
    :param seq: 
    :param typ: 'dna' or 'rna'
    """
    from joker.bioinfo.replication import Transcoder
    typ = typ.lower()
    assert typ in {'dna', 'rna'}
    tc = Transcoder.load('revcompl_{}'.format(typ))
    return tc.transcode(seq).decode()
