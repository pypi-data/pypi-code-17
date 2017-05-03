
import weakref
from collections import deque
from joker.aligner.calculate import Aligner
from joker.aligner.submatrix import load_submat


__version__ = '0.0.2'


# cache a few aligners
_aligners_d = weakref.WeakValueDictionary()
_aligners_q = deque([], 1024)


def create_aligner(submat='blosum60', rho=13):
    return Aligner.from_submatr(*load_submat(submat), rho=rho)


def get_aligner(submat='blosum60', rho=13):
    key = submat, rho
    try:
        return _aligners_d[key]
    except KeyError:
        pass
    a = create_aligner(submat=submat, rho=rho)
    _aligners_d[key] = a
    _aligners_q.append(a)
    return a


def align_simple(iseq, jseq, submat='blosum60', rho=13):
    aligner = get_aligner(submat=submat, rho=rho)
    score, iseq, jseq = aligner.align(iseq, jseq, backtrack=True)
    mseq = Aligner.make_match_string(iseq, jseq)
    return score, iseq.decode(), jseq.decode(), mseq.decode()


def compute_score(iseq, jseq, submat='blosum60', rho=13):
    aligner = get_aligner(submat=submat, rho=rho)
    return aligner.align(iseq, jseq, backtrack=False)[0]
