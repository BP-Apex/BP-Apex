#!/usr/bin/python3
from compare_symb import compare_symb
from common import *
from itertools import product
import factorgraph as fg
import numpy as np
import os
THERSHOLD = 0.6
CERTAIN = [1 / 100, 99 / 100]
MEDIAN = [1 / 2, 1 / 2]
ALL = 'all'
FS = 'fs'
FL = 'fl'
FCD = 'fcd'
FDD = 'fdd'
FD = 'fd'

class Align(object):

    def __init__(self, symba, symbb, verbose=0, executepath='tmp', evidence=None, positive_v=9/10, negative_v=1/10,
                 positive_dep=0.6, negative_dep=0.4, iter=3, dis=2, mode='all'):
        self.verbose = verbose
        self.executepath = executepath

        self.symba = symba
        self.symbb = symbb

        self.parama = self.load_params(self.symba)
        self.paramb = self.load_params(self.symbb)

        self.evidence = evidence

        self.cback = {}
        self.dback = {}

        self.positiona = {}
        self.positionb = {}
        self.mark_position()

        self.positive_v = positive_v
        self.negative_v = negative_v
        self.positive_dep = positive_dep
        self.negative_dep = negative_dep
        self.iter = iter
        self.dis = dis
        self.offset = 0.15
        self.mode = mode

    @log_func()
    def align(self):
        # comapre symb values
        self.cmpinslist = compare_symb(self.symba, self.symbb)

        # symbol execution result
        self.symbexec = self.get_symbexec()

        record = time.time()

        # seqence alignment
        self.seq_alignments = self.seq_align()

        # initial alignment
        self.initial_alignments = self.initial_align()

        # belief propagation alignment
        self.bp_alignments = self.bp_align()

        self.bp_time = time.time() - record

        js = self.dump_result(self.bp_alignments)
        self.debug(js)
        print('\nResult is shown in tmp/res.json')
        return self.bp_alignments, js

    def get_precision_recall_f_score(self, res):
        try:
            precision = len(set(res).intersection(self.evidence)) / len(set(res))
        except ZeroDivisionError:
            precision = 0

        recall = len(set(res).intersection(self.evidence)) / len(self.evidence)

        try:
            f_score = 2 * (precision * recall) / (precision + recall)
        except ZeroDivisionError:
            f_score = 0

        return precision, recall, f_score

    def dump_result(self, alignments):
        js = {}
        js['time'] = self.bp_time

        res = ["{0} {1}".format(alignment[0].s, alignment[1].s) for alignment in alignments if
               isinstance(alignment[0], (STIns, BRIns))]

        js['alignment'] = res
        js['symb_wrong'] = len(self.parama.seq)
        js['symb_correct'] = len(self.paramb.seq)
        js['loc_wrong'] = self.parama.loc
        js['loc_correct'] = self.paramb.loc

        if self.evidence is not None and len(self.evidence) > 0:
            precision, recall, f_score = self.get_precision_recall_f_score(res)
            js['precision'] = precision
            js['recall'] = recall
            js['f_score'] = f_score
            js['not_aligned'] = [_ for _ in self.evidence if _ not in set(res).intersection(self.evidence)]
            js['false_aligned'] = [_ for _ in res if _ not in set(res).intersection(self.evidence) and _ in res]

        return js

    def copy(self, tocopy):
        return [I for I in tocopy]

    def bp_align(self):
        bp_alignments = self.copy(self.initial_alignments)

        for i in range(1, self.iter + 1):
            bp_alignments = self.refine(bp_alignments, i)

        bp_alignments = self.filter(bp_alignments)

        return bp_alignments

    def add_rv(self, var):
        if var not in self._rvs:
            self._rvs.add(var)
            new_variable = self.G.rv(var, 2)
            self.str_rv_map[var] = new_variable

    def add_factor(self, var, varlist, p):
        if var not in self._factors:
            self._factors.add(var)
            l = []
            for v in varlist:
                l.append(self.str_rv_map[v])

            self.G.factor(l, potential=np.array(p))

    def refine(self, old_alignments, cur_range):
        if old_alignments is None or len(old_alignments) == 0:
            return []

        self._rvs = set()
        self._factors = set()
        self.str_pair_map = {}
        self.str_rv_map = {}
        self.G = fg.Graph()

        # Assign probability to old alignments
        self.assign_prob(old_alignments)

        # propagate probaility to dependences
        self.propagate(old_alignments, cur_range)

        # Run belief propagation
        self.G.lbp(normalize=True)

        new_alignments = self.extract()

        return new_alignments

    def extract(self):
        tuples = self.G.rv_marginals(None, True)
        new_alignments = []

        for rv, marg in tuples:
            pair = self.str_pair_map[str(rv)]
            I1 = pair[0]
            I2 = pair[1]

            if marg[1] > THERSHOLD:
                new_alignments.append([I1, I2, [marg[0], marg[1]]])
        new_alignments.sort(key=lambda x: (x[0].s, x[1].s))

        return new_alignments

    def propagate(self, alignments, n):
        worklist = []
        workset = set()
        for alignment in alignments:
            worklist.append([(alignment[0], alignment[1]), 1])

        count = 0

        while len(worklist) > 0:
            [instance, distance] = worklist.pop(0)

            if not isinstance(instance[0], type(instance[1])):
                continue

            ddeps, cdeps = self.apply_rule(instance, n)
            count += 1
            if distance <= self.dis:
                for (i, j) in ddeps:
                   if (i, j) not in workset:
                       worklist.append([(i, j), distance + 1])
                       workset.add((i, j))

                for (i, j) in cdeps:
                   if (i, j) not in workset:
                       worklist.append([(i, j), distance + 1])
                       workset.add((i, j))


    def apply_rule(self, instance, distance):
        assert instance != None

        # fS
        if self.mode != FS:
            self.add_fS(instance)

        ddeps, cdeps = self.get_deps(instance[0], instance[1], distance)

        # fDD
        if self.mode != FDD and self.mode != FD:
            fDD_variables = [instance] + list(ddeps)
            self.add_fD(fDD_variables, type='data')

        # fCD
        if self.mode != FCD and self.mode != FD:
            fCD_variables = [instance] + list(cdeps)
            self.add_fD(fCD_variables, type='control')

        # fL
        if self.mode != FL:
            self.add_fL(instance)

        return ddeps, cdeps

    def assign_prob(self, alignments):
        for I1, I2, p in alignments:
            var = self.gen_rv((I1, I2))
            self.add_rv(var)
            self.add_factor(var, [var], p)

    def add_fL(self, variable):
        I1 = variable[0]
        I2 = variable[1]

        if not (isinstance(I1, (STIns, BRIns)) and isinstance(I2, (STIns, BRIns))):
            return

        v = self.gen_rv((I1, I2))
        self.add_rv(v)
        v_ff = v + ' l'

        import re
        partten_while = re.compile(r'while\s*[(].*[)]')
        partten_for = re.compile(r'for\s*[(].*;.*;.*[)]')

        if I1.src and I2.src and ((re.search(partten_while, I1.src) and re.search(partten_while, I2.src)) or
                                  (re.search(partten_for, I1.src) and re.search(partten_for, I2.src)) or
                                  (re.search(partten_while, I1.src) and re.search(partten_for, I2.src)) or
                                  (re.search(partten_for, I1.src) and re.search(partten_while, I2.src))
        ):
            self.add_factor(v_ff, [v], CERTAIN)

    def add_fS(self, variable):
        I1 = variable[0]
        I2 = variable[1]

        if not (isinstance(I1, (STIns, BRIns)) and isinstance(I2, (STIns, BRIns))):
            return

        v = self.gen_rv((I1, I2))
        self.add_rv(v)

        v_fs = v + ' s'

        symbs1 = I1.values()
        symbs2 = I2.values()

        high = [self.negative_v, self.positive_v]
        low = [self.positive_v, self.negative_v]

        # STIns
        if isinstance(I1, STIns) and isinstance(I2, STIns):
            if len(symbs1) > 0 and len(symbs2) > 0:
                if symbs1 == symbs2:
                    self.add_factor(v_fs, [v], high)
                elif I1.value != I2.value:
                    self.add_factor(v_fs, [v], low)
            elif I1.expr.v != I2.expr.v:
                self.add_factor(v_fs, [v], low)

        # BRIns
        elif isinstance(I1, BRIns) and isinstance(I2, BRIns):
            s1 = sorted(I1.values())
            s2 = sorted(I2.values())
            if s1 == s2:
                self.add_factor(v_fs, [v], high)
            elif len([_ for _ in s1 if _ in s2]) == 0:
                self.add_factor(v_fs, [v], low)

    def add_fD(self, variables, type=''):
        if len(variables) == 1:
            return
        values = self.get_value(variables)
        vars = [self.gen_rv(pair) for pair in variables]

        var = ''
        for v in vars:
            var += v + ' '
            self.add_rv(v)
        var += type

        self.add_factor(var, vars, values)

    def get_value(self, variables):
        counts = 1 << (len(variables) - 1)
        values = [self.negative_dep] * int(counts + 1) + [self.positive_dep] * int(counts - 1)

        while len(values) > 2:
            res = []
            for i in range(0, len(values), 2):
                l = [values[i], values[i + 1]]
                res.append(l)
            values = res

        return values

    def filter(self, alignments):
        res = [[alignments[0][0], alignments[0][1], alignments[0][2]]]
        residues = []

        for x in alignments[1:]:
            cur_left = x[0]
            cur_right = x[1]
            cur_prob = x[2][1]

            if cur_left.s > res[-1][0].s:
                if cur_right.s > res[-1][1].s:
                    res.append(x)
                else:
                    i = 1

                    while i <= len(res) and res[-i][1].s >= cur_right.s:
                        last_prob = res[-i][2][1]
                        if last_prob >= cur_prob:
                            break
                        i += 1

                    # not found
                    else:
                        i -= 1

                        while i:
                            residues.append(res[-1])
                            res.remove(res[-1])
                            i -= 1

                        res.append(x)
            else:
                if x[2][1] > res[-1][2][1]:
                    residues.append(res[-1])
                    res[-1] = x

        probability = 1
        for key in res:
            probability  = min(key[2][1], probability)

        # add residues
        residues.sort(key=lambda x: (x[0].s, x[1].s))
        index = 1
        for residue in residues:
            for i in range(index, len(res)):
                if residue[0].s < res[i][0].s and residue[1].s < res[i][1].s and \
                        residue[0].s > res[i - 1][0].s and residue[1].s > res[i - 1][1].s and \
                        residue[2][1] >= probability:
                    res.append(residue)
                    index = i
                    break

        res.sort(key=lambda x: (x[0].s, x[1].s))

        result = []
        for key in res:
            result.append([key[0], key[1], key[2]])

        return result

    def initial_align(self):
        initial_alignments = []

        for I1, I2 in self.seq_alignments:
            if I1.src and I2.src:
                symbols1 = I1.expr.e2.symbols()
                symbols2 = I2.expr.e2.symbols()

                if len(symbols1) > 0 and len(symbols2) > 0 and symbols1 == symbols2:
                    initial_alignments.append([I1, I2, CERTAIN])
                else:
                    initial_alignments.append([I1, I2, MEDIAN])


        seqA = self.parama.seq
        seqB = self.paramb.seq

        # PRINT instances
        pA = [I for I in seqA if isinstance(I, PRINT)]
        pB = [I for I in seqB if isinstance(I, PRINT)]

        from itertools import count
        for I1, I2, idx in zip(pA, pB, count(0)):
            if I1.argv[0] != I2.argv[0] or len(I1.argv) != len(I2.argv):
                break
            for v1, v2, vidx in zip(I1.argv[1:], I2.argv[1:], count(1)):
                if v1 != v2:
                    # inside found
                    break
            else:
                # inside not found
                initial_alignments.append([I1, I2, CERTAIN])
                continue
            # found
            break

        return initial_alignments

    def gen_rv(self, pair):
        I1 = pair[0]
        I2 = pair[1]

        s = str(I1.s) + ' ' + str(I2.s)
        self.str_pair_map[s] = pair
        return s

    def get_symbexec(self):
        symbexec = set()

        for l in self.cmpinslist:
            v1, i1, v2, i2, flag = l
            symbexec.add((self.parama.exec[(v1, i1)], self.paramb.exec[(v2, i2)]))
        return symbexec

    def seq_align(self):
        alignments = []
        exclude = set(alignments)

        result = self.score_board(lambda n1, n2: self.score(n1, n2, self.symbexec, exclude))

        for i, n1, j, n2, b in result:
            if b:
                alignments.append((n1, n2))

        return alignments

    def score_board(self, score):
        from itertools import count

        seq1 = [0] + self.parama.seq
        seq2 = [0] + self.paramb.seq

        T = [[0 for __ in seq2] for _ in seq1]
        U = [[0 for __ in seq2] for _ in seq1]

        for i, n1 in zip(count(0), seq1):
            for j, n2 in zip(count(0), seq2):
                if i == 0:
                    T[i][j] = 0
                    U[i][j] = 0
                elif j == 0:
                    T[i][j] = 0
                    U[i][j] = 0
                else:
                    s = score(n1, n2)

                    T[i][j], U[i][j] = max(
                        (T[i - 1][j - 1] + s, 2),  # match
                        (T[i - 1][j], 3),  # delete
                        (T[i][j - 1], 4))  # insert

                    if U[i][j] == 2 and s > 0: U[i][j] = 1  # select

        align = list(self.iter_align(seq1, seq2, U))
        align.reverse()
        return align

    def score(self, n1, n2, C, exclude=None):
        if (n1, n2) in C:
            if exclude and (n1, n2) in exclude:
                return 0
            return 2
        else:
            return -1

    def iter_align(self, seq1, seq2, U):
        i = len(seq1) - 1
        j = len(seq2) - 1

        while i > 0 and j > 0:
            if U[i][j] == 1:
                yield (i, seq1[i], j, seq2[j], True)
                i -= 1
                j -= 1
            elif U[i][j] == 2:
                yield (i, seq1[i], j, seq2[j], False)
                i -= 1
                j -= 1
            elif U[i][j] == 3:
                yield (i, seq1[i], 0, None, False)
                i -= 1
            elif U[i][j] == 4:
                yield (0, None, j, seq2[j], False)
                j -= 1

        while j > 0:
            yield (0, None, j, seq2[j], False)
            j -= 1

        while i > 0:
            yield (i, seq1[i], 0, None, False)
            i -= 1

    def get_deps(self, left, right, n):
        def _add_pair(pair, deps):
            i = pair[0]
            j = pair[1]
            if i in self.positiona and j in self.positionb and abs(self.positiona[i] - self.positionb[j]) < self.offset:
                deps.add((i, j))

        search1 = set()
        search2 = set()
        search3 = set()
        search4 = set()

        self.get_ddep_within_n(search1, left, n)
        self.get_ddep_within_n(search2, right, n)
        self.get_cdep_within_n(search3, left, n)
        self.get_cdep_within_n(search4, right, n)

        ddeps = set()
        for i, j in product(search1, search2):
            _add_pair((i, j), ddeps)

        cdeps = set()
        for i, j in product(search3, search4):
            _add_pair((i, j), cdeps)

        return ddeps, cdeps

    def list_to_map(self, list):
        map = {}

        for pair in list:
            if pair[0] not in map:
                map[pair[0]] = [pair[1]]
            else:
                map[pair[0]].append(pair[1])

        return map

    def get_ddep_within_n(self, search, I, n):
        if isinstance(I, PRINT):
            return
        queue = [(I, 0)]

        while queue:
            (instance, dis) = queue.pop(0)
            if dis < n:
                for d in instance.expr.e0.dependencies():
                    if isinstance(d, STIns):
                        search.add(d)
                    queue.append((d, dis + 1))

    def get_cdep_within_n(self, search, I, n):
        if I is None:
            return
        cdep = I.cdep
        while cdep and n > 0:
            if isinstance(cdep, (STIns, BRIns)):
                n -= 1
                search.add(cdep)
            cdep = cdep.cdep

    def mark_position(self):
        len_of_a = len(self.parama.seq)
        for i in range(len_of_a):
            self.positiona[self.parama.seq[i]] = (i + 1) / len_of_a

        len_of_b = len(self.paramb.seq)
        for i in range(len_of_b):
            self.positionb[self.paramb.seq[i]] = (i + 1) / len_of_b

    def load_params(self, symbfile):
        from itertools import count
        import pickle
        f = open(symbfile, 'rb')
        exec = pickle.load(f)
        f.close()

        loc = 0
        seq = []
        printins = []

        for I, s in zip(exec, count(1)):
            I.s = s
            I.flag = 0
            I.indent = -1
            I.location = None
            I.cdchild = []
            if hasattr(I, 'loc') and I.loc:
                loc = max(loc, I.loc)

            if isinstance(I, (STIns, BRIns, PRINT)) and I.vid != 0 and I.loc > 0:
                seq.append(I)
                if isinstance(I, PRINT):
                    printins.append(I)

        return Param(exec, loc, seq, printins)

    def debug(self, msg, *args):
        '''
        Prints debug message if verbose mode on.
        '''
        if self.verbose:
            debug(msg, *args)