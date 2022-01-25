import z3
import operator as op
from inst import *
from sexpdata import Symbol as Sym
from command import *
from ordered import OrderedSet

__all__ = ['expr', 'expand1', 'expand2', 'expand3', 'expand4']

__oper__ = {'+': op.add, '-': op.sub, '*': op.mul,
            '%': op.mod, '/': op.truediv,
            '&&': z3.And, '||': z3.Or, '^': z3.Xor,
            '=': op.eq, '!=': op.ne, '!': z3.Not,
            '>': op.gt, '>=': op.ge, '<': op.lt, '<=': op.le,
            'ptr': op.add}

__flip__ = {'=': '!=', '!=': '=',
            '>': '<=', '>=': '<', '<': '>=', '<=': '>'}


@cmdfunc
def expr(*args, **kwargs):
    if len(args) == 1:
        term = args[0]
        if isinstance(term, int):
            return CONST(term)
        elif isinstance(term, float):
            return CONST_FLOAT(term)
        elif isinstance(term, Input):
            return ITERM(term)
        elif isinstance(term, OPIns):
            return OTERM(term)
        elif isinstance(term, (EXPR, ITERM, OTERM, CONST)):
            return term
        elif isinstance(term, list):
            return expr(*term)
        else:
            assert False, type(term)
    else:
        fn, *op = args
        op = [expr(o) for o in op]
        return EXPR(fn, *op)


def expand1(e):
    return e.expand(1)


def expand2(e):
    return e.expand(2)


def expand3(e):
    return e.expand(3)


def expand4(e):
    return e.expand(4)


class EXPR:
    def __init__(self, *expr):
        self.fn, *self.op = list(expr)

    def __repr__(self):
        # print('in __repr__')
        # print('fn is ', self.fn)
        if self.fn == 'ptr':
            if len(self.op) > 2 and self.op[1] == 0:
                return str(self.op[0]) + ''.join('[' + str(o)  + ']' for o in self.op[2:])
            else:
                return str(self.op[0]) + ''.join('[' + str(o)  + ']' for o in self.op[1:])
        fn = self.fn    
        if len(self.fn) == 2:
            fn = self.fn[1]
        if len(self.op) == 1:
            return fn + str(self.op[0])
        else:
            return (' ' + fn + ' ').join([str(o) for o in self.op])

    def encode_(self):
        return _list(Sym('expr'), self.fn) + [o.encode_() for o in self.op]

    def expand(self, lvl):
        op = [e.expand(lvl) for e in self.op]
        return EXPR(self.fn, *op)

    def as_z3(self):
        fn = __oper__[self.fn]
        op = [e.as_z3() for e in self.op]
        if self.fn == '^':
            if isinstance(op[0], int) and op[0] == -1:
                op[0] = True
            if isinstance(op[1], int) and op[1] == -1:
                op[1] = True

        if len(op) > 2:
            from functools import reduce
            return reduce(fn, op)
        else:
            return fn(*op)

    def symbols(self):
        return set(sym for o in self.op for sym in o.symbols())

    def dependencies(self):
        from itertools import chain
        return OrderedSet(chain.from_iterable(o.dependencies() for o in self.op))


class ITERM:
    def __init__(self, term):
        assert isinstance(term, Input)
        self.term = term

    def __repr__(self):
        return 'I%s' % (self.term.seq, )

    def encode_(self):
        return [Sym('expr'), encode(self.term, True)]

    def expand(self, lvl):
        return self

    def as_z3(self):
        return z3.Int('I%s' % (self.term.seq, ))

    def symbols(self):
        return {'I%s' % (self.term.seq, )}

    def dependencies(self):
        return set()


class OTERM:
    def __init__(self, term):
        assert isinstance(term, OPIns)
        self.term = term

    def __repr__(self):
        try:
            return self.term.as_code()
        except:
            return '<OTERM.>'
        
        # if isinstance(self.term, VVIns):
        #     return str(self.term.name)
        # elif isinstance(self.term, LDIns):
        #     return str(self.term.addr.e1)
        # else:
        #     return '<OTERM>'

    def encode_(self):
        return [Sym('expr'), encode(self.term, True)]

    def expand(self, lvl):
        if lvl == 1 and isinstance(self.term, (VVIns, LDIns)):
            return self
        if lvl == 3 and isinstance(self.term, (VVIns, LDIns, FNIns)):
            return self
        if lvl == 4 and isinstance(self.term, (VVIns, STIns)):
            return self
        e = self.term.expr
        return getattr(e, 'e%d' % lvl)

    def as_z3(self):
        assert isinstance(self.term, (VVIns, LDIns)), type(self.term)
        return z3.Int(str(self))

    def symbols(self):
        if isinstance(self.term, VVIns):
            pass
        elif isinstance(self.term, LDIns):
            return self.term.expr.e3.symbols()
        elif isinstance(self.term, FNIns):
            return set(sym for arg in self.term.fargs for sym in arg.expr.e3.symbols())
        else:
            assert False
        return set()

    def dependencies(self):
        return {self.term}


class CONST(int):
    def encode_(self):
        return [Sym('expr'), self]
    
    def expand(self, lvl):
        return self
    
    def as_z3(self):
        return int(self)

    def symbols(self):
        return set()

    def dependencies(self):
        return set()
class CONST_FLOAT(float):
    def encode_(self):
        return [Sym('expr'), self]
    
    def expand(self, lvl):
        return self
    
    def as_z3(self):
        return float(self)

    def symbols(self):
        return set()

    def dependencies(self):
        return set()
