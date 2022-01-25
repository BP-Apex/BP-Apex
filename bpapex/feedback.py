from itertools import count
from common import *
from inst import *

CORRECT = 'correct'

class Feedback(object):
    def __init__(self, parama=None, paramb=None, alignments=None, verbose=0, executepath='tmp'):
        global VERBOSE, EXECUTEPATH

        self.alignments = alignments
        self.verbose = verbose
        self.executepath = executepath

        self.parama = parama
        self.paramb = paramb

        self.is_exit = False

    @log_func()
    def feedback(self):
        # critical instance
        feed = self.get_criteria()

        if self.is_exit:
            print('Result\n' + feed)
            return feed

        # make slices
        seqA, seqB = self.make_slices()

        # filter
        sA, sB = self.filter(seqA, seqB)

        # generate feedback
        feed = self.gen_feed(sA, sB, feed)

        print('Result\n' + feed)

        return feed

    def get_info(self, I, align_but_not_match):
        info = ''
        if isinstance(I, STIns):
            info = 'src: %s\tvalue: %s\texecution: %dth' % (I.src, I.var_values(), I.vii)
            if I in align_but_not_match and align_but_not_match[I] is not None:
                info += '\n* Should produce value: %s' % (align_but_not_match[I].var_values())

        if isinstance(I, BRIns):
            info = 'src: %s\tvalue: %s\texecution: %dth' % (I.src, I.value, I.vii)
            if I in align_but_not_match:
                info += '\n* Should have take anthor branch.'
        return info

    def gen_feed(self, sA, sB, err_feed):
        feed = ''
        vida = set()
        vidb = set()
        if len(sA) > 0:
            feed += 'Should not\n'

            _dict = {}
            for p in self.align_but_not_match:
                if p[0] is not None:
                    _dict[p[0]] = p[1]

            for I in sA:
                if I.vid not in vida:
                    vida.add(I.vid)
                    feed += self.get_info(I, _dict) + '\n'

        if len(sB) > 0:
            feed += '\nShould have\n'

            _dict = {}
            for p in self.align_but_not_match:
                if p[1] is not None:
                    _dict[p[1]] = p[0]

            for I in sB:
                if I.vid not in vidb:
                    vidb.add(I.vid)
                    feed += self.get_info(I, _dict) + '\n'

        if len(err_feed) > 0:
            feed += '\nShould print\n'
            feed += err_feed

        return feed

    def depth(self, I):
        if I is None:
            return -1
        if I.cdep is None:
            return 0
        else:
            return self.depth(I.cdep) + 1

    def filter(self, seqA, seqB):
        alignments = self.alignments
        self.alignments_in_slice = []

        aliA = [l[0] for l in alignments]
        aliB = [l[1] for l in alignments]
        vidA = dict((l[0].vid, l[1].vid) for l in alignments)
        vidB = dict((l[1].vid, l[0].vid) for l in alignments)

        depw = self.depth(self.error_print)
        depc = self.depth(self.correct_print)

        sA = self.filter_ali(aliA, depw, seqA)
        sB = self.filter_ali(aliB, depc, seqB)

        self.align_but_not_match = []

        for i in sA:
            if i.vid in vidA:
                for j in sB:
                    if j.vid == vidA[i.vid]:
                        self.align_but_not_match.append((i, j))
                        break

        for i in sA:
            if i.vid in vidA:
                self.align_but_not_match.append((i, None))

        for i in sB:
            if i.vid in vidB:
                self.align_but_not_match.append((None, i))

        return sA, sB

    def filter_ali(self, ali, dep, seq):

        short = []
        for s in seq:
            depth_of_s = self.depth(s)
            if depth_of_s == dep - 1:
                short.append(s)
        whitelist = [_ for _ in short if _ not in ali]

        index = -1
        for i in range(len(seq)):
            if seq[i] in ali:
                index = i
        index += 1
        res = []
        for i in range(len(seq)):
            if i < index and seq[i] in whitelist or i >= index:
                res.append(seq[i])
        return res

    def get_criteria(self):
        seqA = self.parama.seq
        seqB = self.paramb.seq
        criteriaA = None
        criteriaB = None

        # PRINT instances
        pA = [I for I in seqA if isinstance(I, PRINT)]
        pB = [I for I in seqB if isinstance(I, PRINT)]

        wrong_var = 0
        right_var = 0

        for Ia, Ib, idx in zip(pA, pB, count(0)):
            if Ia.argv[0] != Ib.argv[0] or len(Ia.argv) != len(Ib.argv):
                criteriaidx = [idx]
            for v1, v2, vidx in zip(Ia.argv[1:], Ib.argv[1:], count(1)):
                if v1 != v2:
                    wrong_var = v1
                    right_var = v2
                    criteriaidx = [idx, vidx]
                    # inside found
                    break
            else:
                # inside not found
                continue
            # found
            break

        # not found
        else:
            if len(pA) == len(pB):
                self.is_exit = True
                return CORRECT
            elif len(pA) > len(pB):
                lastP = pA[len(pB) - 1]
                self.is_exit = True
                return self.exit(lastP)
            else:
                criteriaA = None
                criteriaB = pB[len(pA)]
                criteriaidx = []


        self.error_print = pA[int(criteriaidx[0])] if len(criteriaidx) > 0 else None
        self.correct_print = pB[int(criteriaidx[0])] if len(criteriaidx) > 0 else pB[len(pA)]

        if len(criteriaidx) == 1:
            criteriaA = self.error_print
            criteriaB = self.correct_print
        elif len(criteriaidx) > 1:
            i2 = int(criteriaidx[1])
            criteriaA = self.error_print.arge[i2]
            criteriaB = self.correct_print.arge[i2]

            if isinstance(criteriaA, list) and isinstance(criteriaB, list):
                for cA, cB in zip(criteriaA, criteriaB):
                    if cA.value != cB.value:
                        criteriaA = cA
                        criteriaB = cB
                        break
                # not found
                else:
                    assert len(criteriaA) != len(criteriaB)
                    minlen = min(len(criteriaA), len(criteriaB))
                    if minlen < len(criteriaA):
                        criteriaA = criteriaA[minlen]
                        criteriaB = None
                    else:
                        criteriaB = criteriaB[minlen]
                        criteriaA = None

        # assert criteriaA, criteriaB
        feed = self.wrong_print(self.error_print, self.correct_print, right_var, wrong_var)

        # Get the instances (STIns and BRIns) that are directly depended by PRINT instance
        if isinstance(criteriaA, (OPIns, PRINT)):
            criteriaA = [_I for _I in self.dependency_of(criteriaA) if isinstance(_I, (STIns, BRIns))]
        if isinstance(criteriaB, (OPIns, PRINT)):
            criteriaB = [_I for _I in self.dependency_of(criteriaB) if isinstance(_I, (STIns, BRIns))]

        self.criteriaA = criteriaA
        self.criteriaB = criteriaB

        return feed

    def make_slices(self):
        seqA = self.make_slice(self.parama.seq, self.criteriaA)
        seqB = self.make_slice(self.paramb.seq, self.criteriaB)
        return seqA, seqB

    def make_slice(self, seq, criteria):
        try:
            criteria = set(criteria)
        except TypeError:
            criteria = {criteria}

        execset = set(seq)
        criteria = set(I for I in criteria if I and I in execset)

        for I in reversed(seq):
            if I in criteria:
                criteria.update(_ for _ in self.dependency_of(I) if _ in execset)

        return sorted(criteria, key=lambda I: I.s)


    def dependency_of(self, I):
        def _dep_of(I):
            if not isinstance(I, OPIns):
                return []
            if isinstance(I, STIns):
                return [I]

            deps = I.expr.e0.dependencies()
            if deps:
                deps = [_dep_of(d) for d in deps]
                return set().union(*deps)
            else:
                return []

        dependencies = set()
        if I.cdep:
            dependencies.add(I.cdep)

        if isinstance(I, OPIns):
            for d in I.expr.e0.dependencies():
                dependencies.update(_dep_of(d))

        return dependencies

    def wrong_print(self, criteriaA, criteriaB, rv, wv):
        if criteriaA is not None:
            return 'When \'%s\' at %dth execution, you should have output %s, instead of %s.' % (
            criteriaA.src, criteriaA.vii, str(rv), str(wv))
        elif criteriaB is not None:
            return 'You should have output {1}.'.format(criteriaB.src, criteriaB.argv)

    def exit(self, instance):
        return 'After \'%s\' at _%dth execution, you should have exit.' % (instance.src, instance.vii)

    def debug(self, msg, *args):
        '''
        Prints debug message if verbose mode on.
        '''
        if VERBOSE:
            debug(msg, *args)