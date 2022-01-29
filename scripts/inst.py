from llvmtype import *

class Val(Command):
    e0 = KWField()
    e1 = KWField()
    e2 = KWField()
    e3 = KWField()
    e4 = KWField()
    v = KWField()

    @property
    def value(self): return self.v


class Input(Command):
    seq = Field()
    value = Field()

    def __int__(self):
        return int(self.value)


class Instr(KeyCommand):
    vid = KeyField()
    vii = KeyField()
    src = KWField()
    loc = KWField()
    cdep = KWField()
    pdf = KWField()


class BBIns(Instr):
    terminator = KWField()


class OPIns(Instr):
    expr = KWField()

    def __int__(self):
        return int(self.expr.v)

    @property
    def value(self): return int(self)

    def as_code(self):
        if self.expr.e3.dependencies():
            return str(self.expr.e3)
        elif self.expr.e2.symbols():
            return str(self.expr.e3)
        else:
            return str(self.expr.v)

    def var_values(self):
        values = []
        for var in self.expr.e1.dependencies():
            # values.append('%s=%s' % (var.as_code(), var.expr.v))
            values.append((var.as_code(), var.expr.v))

        def _str_v(v): 
            if 48 <= v <= 57 or 65 <= v <= 90:
                return "%s('%s')" % (v, chr(v))
            return str(v)
        

        values = ['%s=%s' % (n, _str_v(v)) for n, v in values if v <=0x400000]
        return ', '.join(values)

    def values(self):
        values = []
        for var in self.expr.e1.dependencies():
            # values.append('%s=%s' % (var.as_code(), var.expr.v))
            values.append(var.expr.v)
        exprs = str(self.expr.e3).split()
        if len(exprs) >= 2:
            if exprs[1] == '<' or exprs[1] == '>=':
                values.append(1)
            elif exprs[1] == '<=' or exprs[1] == '>':
                values.append(2)
            elif exprs[1] == '==' or exprs[1] == '!=':
                values.append(3)
            try:
                values.append(int(exprs[2]))
            except:
                pass
            return values
        else:
            return exprs


class VVIns(OPIns):
    name = KWField()
    type = KWField()

    def as_code(self):
        return str(self.name)


class LDIns(OPIns):
    addr = KWField()

    def as_code(self):
        return str(self.addr.e3)


class ITIns(OPIns):
    addr = KWField()
    

class STIns(OPIns):
    addr = KWField()
    desc = KWField()

    def as_code(self):
        return '%s = %s' % (self.addr.e3, self.expr.e3)

    def var_values(self):
        values = []
        try:
            if isinstance(self.addr.e3.term, LDIns):
                # values.append('*%s=%s' % (self.addr.e3, self.expr.v))
                values.append(('*%s' % self.addr.e3, self.expr.v))
            else:
                # values.append('%s=%s' % (self.addr.e3, self.expr.v))
                values.append(('%s' % self.addr.e3, self.expr.v))
        except:
            # values.append('%s=%s' % (self.addr.e3, self.expr.v))
            values.append(('%s' % self.addr.e3, self.expr.v))
        for v2 in self.addr.e1.dependencies():
            if isinstance(v2, VVIns): continue
            # values.append('%s=%s' % (v2.as_code(), v2.expr.v))
            values.append(('%s' % v2.as_code(), v2.expr.v))
        
        for var in self.expr.e1.dependencies():
            # values.append('%s=%s' % (var.as_code(), var.expr.v))
            values.append(('%s' % var.as_code(), var.expr.v))
            if isinstance(var, VVIns): continue
            for v2 in var.addr.e1.dependencies():
                if isinstance(v2, VVIns): continue
                # values.append('%s=%s' % (v2.as_code(), v2.expr.v))
                values.append(('%s' % v2.as_code(), v2.expr.v))

        def _str_v(v): 
            if 48 <= v <= 57 or 65 <= v <= 90:
                return "%s('%s')" % (v, chr(v))
            return str(v)
        
        values = ['%s=%s' % (n, _str_v(v)) for n, v in values if v <=0x400000]
        return ', '.join(values)

    def values(self):
        values = []
        try:
            if isinstance(self.addr.e3.term, LDIns):
                # values.append('*%s=%s' % (self.addr.e3, self.expr.v))
                values.append((self.expr.v))
            else:
                # values.append('%s=%s' % (self.addr.e3, self.expr.v))
                values.append((self.expr.v))
        except:
            # values.append('%s=%s' % (self.addr.e3, self.expr.v))
            values.append((self.expr.v))
        for v2 in self.addr.e1.dependencies():
            if isinstance(v2, VVIns): continue
            # values.append('%s=%s' % (v2.as_code(), v2.expr.v))
            values.append((v2.expr.v))

        for var in self.expr.e1.dependencies():
            # values.append('%s=%s' % (var.as_code(), var.expr.v))
            values.append((var.expr.v))
            if isinstance(var, VVIns): continue
            for v2 in var.addr.e1.dependencies():
                if isinstance(v2, VVIns): continue
                # values.append('%s=%s' % (v2.as_code(), v2.expr.v))
                values.append((v2.expr.v))

        return values



class FNIns(OPIns):
    fname = KWField()
    fargs = KWField()
    
    def as_code(self):
        def _code(arg):
            try:
                return arg.as_code()
            except AttributeError:
                return str(arg)
        
        argstr = ', '.join(_code(a) for a in self.fargs)
        return '%s(%s)' % (self.fname, argstr)
    

class BRIns(OPIns):
    locT = KWField()
    locF = KWField()
    
    def as_code(self):
        if bool(self.expr.v):
            return 'if %s' % (self.expr.e3, )
        else:
            return 'if not %s' % (self.expr.e3, )

    def simplify(self):
        import z3
        import sexpdata
        e = self.expr.e2.as_z3()
        if not bool(self.expr.v):
            e = z3.Not(e)
        g = z3.Goal()
        g.add(e)

        t = z3.Tactic('ctx-solver-simplify')
        g = t(g)
        g = g[0]

        def sexpr_to_str(sexpr):
            if isinstance(sexpr, sexpdata.Symbol):
                return sexpr.value()
            elif isinstance(sexpr, list):
                fn, *op = [sexpr_to_str(o) for o in sexpr]
                if len(op) == 1:
                    return fn + ' ' + op[0]
                else:
                    fn = ' %s ' % (fn, )
                    return fn.join(op)
            elif isinstance(sexpr, int):
                if sexpr in (65, 90, 97, 122, 48, 57):
                    return "'%s'(%s)" % (chr(int(sexpr)), int(sexpr))
                else:
                    return str(int(sexpr))
            else:
                return str(sexpr)

        e = []
        for constraint in g:
            s = constraint.sexpr()
            s = sexpdata.loads(s)
            e.append(sexpr_to_str(s))

        return 'if ' + ' and '.join(e)


class LPIns(OPIns):
    pass


class PRINT(Instr):
    args = KWField()
    arge = KWField()
    argv = KWField()
    # argtypes = KWField()
    # args_e = KWField()

    def as_code(self):
        def tostr(l):
            s = ''
            for v in l:
                if v is None:
                    v = '*'
                elif v.value == 10:
                    v = '\\n'
                else:
                    v = chr(v.value)
                s += v
            return s

        s = tostr(self.arge[0])
        args = ['"%s"' % s] + [tostr(a) if isinstance(a, list) else a.as_code() for a in self.arge[1:]]
        
        
        # _arg = src[7:-2].strip()
        # _args = _arg.split(',')

        # args = [_args[0]] # + [a.as_code() for a in self.args[1:]]
        
        return 'printf(' + ', '.join(args) + ')'

    # ', '.join([a.as_code() for a in self.args])

    def str(self):
        pass

    def var_values(self):
        return ''


class Exec:
    def __init__(self, filename=None):
        from collections import OrderedDict
        self.exec = OrderedDict()
        self.root = Instr(0, 0, ipdom=0, context=self)
        if filename:
            self.load(filename)

    def __iter__(self):
        return iter(self.exec.values())

    def __getitem__(self, key):
        if key[0] == 'instr':
            key = key[1:]
        return self.exec[key]

    def __setitem__(self, key, val):
        if key[0] == 'instr':
            key = key[1:]
        self.exec[key] = val

    def load(self, filename):
        for line in open(filename):
            loads(line, context=self)
