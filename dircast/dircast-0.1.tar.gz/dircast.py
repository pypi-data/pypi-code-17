import gc
import os
import sys
import lzma
import hashlib
__version__ = '0.1'
PI = 0
EM = 1
EN = 2
ES = 3
EC1 = 4
EC2 = 5

class Cast:

    def __init__(self):
        self.cast = []

    def get_path_by_index(self, ei, ri=-1):
        if ei < 0:
            return ''
        if ei > len(self.cast) - 1:
            return ''
        path = self.cast[ei][EN]
        while True:
            ei = self.cast[ei][PI]
            if ei == ri:
                break
            else:
                path = os.path.join(self.cast[ei][EN], path)
        return path

    def get_index_by_path(self, path, ri=-1):
        apath = path.split(os.sep)
        pi = ri
        si = 0
        found = True
        for i in range(0, len(apath)):
            if not found: break
            found = False
            for ei in range(si, len(self.cast)):
                if self.cast[ei][PI] == pi and self.cast[ei][EN] == apath[i]:
                    if i == len(apath) - 1:
                        return ei
                    else:
                        pi = ei
                        si = ei + 1
                        found = True
                        break
        return -1

    def get_subs(self, pi, em='fd', recursive=False):
        ia = []
        if pi > len(self.cast) - 1:
            return ia
        if self.cast[pi][EM] != 'd':
            return ia
        for ei in range(0, len(self.cast)):
            if self.cast[ei][PI] == pi:
                if self.cast[ei][EM] in em:
                    ia.append(ei)
        if recursive:
            i = 0
            while True:
                if i == len(ia):
                    break
                else:
                    pi = ia[i]
                    for ei in range(pi + 1, len(self.cast)):
                        if self.cast[ei][PI] == pi:
                            if self.cast[ei][EM] in em:
                                ia.append(ei)
                i += 1
        return ia

    def make_cast_by_dir(self, path_to_dir, indicate='no'):
        self.cast = []
        gc.collect()
        if not os.path.isdir(path_to_dir) or os.path.islink(path_to_dir):
            return
        abs_path_to_dir = os.path.abspath(path_to_dir)
        self.cast.append(
            [-1, 'd', os.path.basename(abs_path_to_dir), 0, '', ''])
        i = 0
        progress(indicate, 'scan: ' + str(i))
        es_total = 0
        es_current = 0
        for root, dirs, files in os.walk(abs_path_to_dir):
            pi = self.get_index_by_path(
                os.path.relpath(root, os.path.dirname(abs_path_to_dir)))
            for d in dirs:
                self.cast.append([pi, 'd', d, 0, '', ''])
                i += 1
                progress(indicate, 'scan: ' + str(i))
            for f in files:
                es = os.lstat(os.path.join(root, f)).st_size
                es_total += es
                self.cast.append([pi, 'f', f, es, '', ''])
                i += 1
                progress(indicate, 'scan: ' + str(i))
        progress(indicate, 'scan: ' + str(i) + ' done\n')
        progress(indicate, 'calc: ' + str(es_current))
        for x in range(0, len(self.cast)):
            if self.cast[x][EM] == 'f':
                absfname = os.path.join(abs_path_to_dir,
                    self.get_path_by_index(x, 0))
                cs1 = hashlib.md5()
                cs2 = hashlib.sha256()
                with open(absfname, mode='rb') as fr:
                    while True:
                        data = fr.read(2047)
                        es_current += len(data)
                        if len(data) == 0: break
                        cs1.update(data)
                        cs2.update(data)
                        del data
                self.cast[x][EC1] = cs1.hexdigest()
                self.cast[x][EC2] = cs2.hexdigest()
                gc.collect()
            progress(indicate,
                'calc: ' + str(int(es_current * 99 / es_total)) + '%')
        for x in range(len(self.cast) - 1, -1, -1):
            if self.cast[x][EM] == 'd':
                es = 0
                ec1 = 0
                ec2 = 0
                for y in range(x + 1, len(self.cast)):
                    if self.cast[y][PI] == x:
                        es += self.cast[y][ES]
                        if self.cast[y][EM] == 'd':
                            ec1 += self.cast[y][EC1] + 1
                            ec2 += self.cast[y][EC2]
                        else:
                            ec2 += 1
                self.cast[x][ES] = es
                self.cast[x][EC1] = ec1
                self.cast[x][EC2] = ec2
        progress(indicate, 'calc: 100% done\n')

    def save_in_file(self, filename):
        with lzma.open(filename, 'w') as f:
            for ei in range(0, len(self.cast)):
                f.write(bytes(' / '.join([str(e) for e in self.cast[ei]]) +
                    '\n', 'utf-8'))

    def load_from_file(self, filename):
        self.cast = []
        lines = ''
        with lzma.open(filename, 'r') as f:
            lines = str(f.read(), 'utf-8')
        if lines != '':
            for line in lines.split('\n'):
                if line == '': continue
                a = line.split(' / ')
                self.cast.append([int(a[0]), a[1], a[2], int(a[3]),
                    a[4] if a[1] == 'f' else int(a[4]),
                    a[5] if a[1] == 'f' else int(a[5])])

    def is_empty_dir(self, ei):
        if ei < len(self.cast):
            if self.cast[ei][EM] == 'd':
                if self.cast[ei][ES] == 0:
                    if self.cast[ei][EC1] == 0:
                        if self.cast[ei][EC2] == 0:
                            return True
        return False

    def is_sub(self, ei, pi):
        if ei < 1:
            return 0
        if ei > len(self.cast) - 1:
            return 0
        if pi < 0:
            return 0
        if pi > len(self.cast) - 1:
            return 0
        if ei <= pi:
            return 0
        if self.cast[pi][EM] != 'd':
            return 0
        i = 1
        _ei = ei
        while True:
            if self.cast[_ei][PI] == pi:
                return i
            else:
                _ei = self.cast[_ei][PI]
                if _ei == 0:
                    return 0
                else:
                    i += 1

    def is_subs(self, aei, api):
        if len(aei) > len(api):
            return False
        _api = api.copy()
        subs = []
        for i in range(0, len(aei)):
            subs.append(False)
            for j in range(0, len(_api)):
                if self.is_sub(aei[i], _api[j]) != 0:
                    subs[i] = True
                    _api.pop(j)
                    break
        if sum(subs) == len(subs):
            return True
        else:
            return False

def compare_check_values(e1, e2):
    if e1[EM] == e2[EM]:
        if e1[ES] == e2[ES] and e1[EC1] == e2[EC1] and e1[EC2] == e2[EC2]:
            return True
        else:
            return False
    else:
        return False

def compare_casts(cast1, cast2, ei1=0, ei2=0, indicate='no'):
    retval = {'cres':'', 'lres':[]}
    progress(indicate, 'compare...')
    if cast1.cast[ei1][EM] != cast2.cast[ei2][EM]:
        retval['cres'] = 'fd'
    else:
        if cast1.cast[ei1][EM] == 'f':
            if compare_check_values(cast1.cast[ei1], cast2.cast[ei2]):
                retval['cres'] = 'eq'
            else:
                retval['cres'] = 'ne'
        else:
            ia1 = cast1.get_subs(ei1, recursive=True)
            ia2 = cast2.get_subs(ei2, recursive=True)
            max = len(ia1)
            while True:
                if len(ia1) == 0:
                    break
                path1 = cast1.get_path_by_index(ia1[0], ri=ei1)
                index2 = cast2.get_index_by_path(path1, ri=ei2)
                if index2 != -1:
                    if compare_check_values(cast1.cast[ia1[0]], cast2.cast[index2]):
                        retval['lres'].append([3, ia1[0], index2])
                    else:
                        retval['lres'].append([0, ia1[0], index2])
                else:
                    retval['lres'].append([1, ia1[0], index2])
                ia1.pop(0)
                if index2 != -1:
                    ia2.remove(index2)
                progress(indicate,
                    'compare: ' + str(int((max - len(ia1)) * 99 / max)) + '%')
            for i in range(0, len(ia2)):
                retval['lres'].append([2, -1, ia2[i]])
            c = [0, 0, 0, 0]
            for i in range(0, len(retval['lres'])):
                cr = retval['lres'][i][0]
                c[cr] += 1
            if len(retval['lres']) == 0:
                retval['cres'] = 'eq'
            elif c[0] == 0 and c[1] == 0 and c[2] == 0 and c[3] != 0:
                retval['cres'] = 'eq'
            elif (c[1] != 0 or c[2] != 0) and c[0] == 0 and c[3] == 0:
                retval['cres'] = 'ne'
            else:
                retval['cres'] = 'pd'
    progress(indicate, 'compare: 100% done\n')
    return retval

def find_equal_dirs_in_cast(cast, ignore_empty=True, indicate='no'):
    retval = []
    progress(indicate, 'search: 0%')
    for x in range(1, len(cast.cast)):
        if cast.cast[x][EM] == 'd':
            earlier = False
            for i in range(0, len(retval)):
                if x in retval[i]:
                    earlier = True
                    break
            if earlier:
                continue
            if cast.is_empty_dir(x) and ignore_empty:
                continue
            dup = []
            for y in range(x + 1, len(cast.cast)):
                if cast.cast[y][EM] == 'd':
                    if compare_check_values(cast.cast[x], cast.cast[y]):
                        cr = compare_casts(cast, cast, x, y)
                        if cr['cres'] == 'eq':
                            if len(dup) == 0:
                                dup.append(x)
                            dup.append(y)
            if len(dup) != 0:
                if len(retval) == 0:
                    retval.append(dup)
                else:
                    is_subs = False
                    for i in range(0, len(retval)):
                        if cast.is_subs(dup, retval[i]):
                            is_subs = True
                            break
                    if not is_subs:
                        retval.append(dup)
        progress(indicate,
                'search: ' + str(int(x * 99 / (len(cast.cast) - 1))) + '%')
    for i in range(1, len(retval)):
        pos = i
        for j in range(i - 1, -1, -1):
            if cast.cast[retval[i][0]][ES] > cast.cast[retval[j][0]][ES]:
                pos = j
            else:
                break
        if pos != i:
            retval.insert(pos, retval.pop(i))
    progress(indicate, 'search: 100% done\n')
    return retval

def progress(indicate, value):
    if indicate == 'cl':
        print('\r' + value, end='')

def do_cl():
    if sys.argv[1] == 'makecast':
        if len(sys.argv) != 4:
            print('Incorrect command line.')
            quit()
        cst = Cast()
        cst.make_cast_by_dir(sys.argv[2], indicate='cl')
        cst.save_in_file(sys.argv[3])
    elif sys.argv[1] == 'compare':
        if len(sys.argv) != 5:
            print('Incorrect command line.')
            quit()
        cst1 = Cast()
        if os.path.isdir(sys.argv[2]):
            cst1.make_cast_by_dir(sys.argv[2], indicate='cl')
        else:
            if sys.argv[2].endswith('.dircast'):
                cst1.load_from_file(sys.argv[2])
            else:
                print('Incorrect command line.')
                quit()
        cst2 = Cast()
        if os.path.isdir(sys.argv[3]):
            cst2.make_cast_by_dir(sys.argv[3], indicate='cl')
        else:
            if sys.argv[3].endswith('.dircast'):
                cst2.load_from_file(sys.argv[3])
            else:
                print('Incorrect command line.')
                quit()
        cr = compare_casts(cst1, cst2, indicate='cl')
        with open(sys.argv[4], mode='wt', encoding='utf-8') as f:
            f.write(cr['cres'] + '\n\n')
            for x in range(0, len(cr['lres'])):
                f.write(str(cr['lres'][x][0]) + '\n')
                if cr['lres'][x][0] != 2:
                    f.write(cst1.get_path_by_index(cr['lres'][x][1]) + '\n')
                if cr['lres'][x][0] != 1:
                    f.write(cst2.get_path_by_index(cr['lres'][x][2]) + '\n')
                f.write('\n')
    elif sys.argv[1] == 'dupdirs':
        if len(sys.argv) != 4:
            print('Incorrect command line.')
            quit()
        cst = Cast()
        if os.path.isdir(sys.argv[2]):
            cst.make_cast_by_dir(sys.argv[2], indicate='cl')
        else:
            if sys.argv[2].endswith('.dircast'):
                cst.load_from_file(sys.argv[2])
            else:
                print('Incorrect command line.')
                quit()
        dups = find_equal_dirs_in_cast(cst, indicate='cl')
        with open(sys.argv[3], mode='wt', encoding='utf-8') as f:
            for x in range(0, len(dups)):
                f.write(str(cst.cast[dups[x][0]][ES]) + '\n')
                for y in range(0, len(dups[x])):
                    f.write(cst.get_path_by_index(dups[x][y]) + '\n')
                f.write('\n')
    elif sys.argv[1] == 'browse':
        if len(sys.argv) != 4:
            print('Incorrect command line.')
            quit()
        cst = Cast()
        cst.load_from_file(sys.argv[2])
        with open(sys.argv[3], mode='wt', encoding='utf-8') as f:
            for ei in range(0, len(cst.cast)):
                f.write(str(ei) + ':\t' +
                    '\t'.join([str(e) for e in cst.cast[ei]]) + '\n')
    else:
        print('Incorrect command line.')
        quit()

def do_gui():
    pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        do_cl()
