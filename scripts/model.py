from inst import *
from itertools import takewhile
from functools import reduce
import operator
import itertools

__all__ = ['run']
__functions__ = {}

input_seq = 0


class SymbExecException(Exception):
    pass


_count = itertools.count
def count(x):
    return _count(int(x))


def register(func):
    __functions__[func.__name__] = func
    return func


def initialize(_execute, _makeval, _mem):
    global execute, makeval, mem
    # execute = symbexec.execute
    # makeval = symbexec.makeval
    execute = _execute
    makeval = _makeval
    mem = _mem


def set_argument(args):
    from itertools import count
    global input_variables
    input_variables = [(addr, Input(seq, value)) \
                       for (addr, value), seq in zip(args, count(1))]
    

def run(function, instr, value, args):
    if function in __functions__:
        __functions__[function](instr, args, value)
    else:
        # print ('default', function)
        execute(OPIns, instr, expr=makeval(value))


def as_list(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        return list(f(*args, **kwargs))
    return wrapped


def as_str(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        return ''.join(f(*args, **kwargs))
    return wrapped


def readmems(ptr, size=None):
    global mem
    # mem = symbexec.mem
    if size is None:
        r = count(int(ptr))
        #print('if the size is None, r is', r)
    else:
        r = range(int(ptr), int(ptr) + int(size))
    #for m, n in mem.items():
        #print('m is ',m,'n is', n.as_code())
    for p, i in zip(r, count(0)):
        m = mem[p]
        #print('in readmems the m is', m)
        if m is None:
            try:
                #print('the m is None')
                e3 = ptr.expr.e3
                if e3.fn == 'ptr' and e3.op[1] == 0 and e3.op[2] == 0:
                    ptr = e3.op[0].term
            except AttributeError:
                pass
            
            raise SymbExecException(
                "Use uninitialized value",
                "%s[%s] is not initialized" % (ptr.as_code(), i),
                "This may happen because you are missing terminating null character '\\0'")
        yield m
        

@as_list
def cstr(ptr, size=None, ending=False):
    for m in readmems(ptr, size):
        if int(m) == 0:
            if ending:
                yield(m)
            return
        yield(m)


@as_str
def _str(s):
    for c in s:
        c = int(c)
        if c == 10:
            yield('\\n')
        else:
            # print('in _str, c is', chr(c))
            yield(chr(c))


class PArg:
    def __init__(self, type, idx):
        self.type = type
        self.idx = idx


def _printf(fmt):
    i = 0
    f = False
    for c in fmt:
        if f:
            if int(c) == ord('%'):
                yield c
            else:
                yield PArg(chr(int(c)), i)
                i += 1
                f = False
        elif int(c) == ord('%'):
            f = True


@register
def printf(instr, args, value):
    fmt = cstr(args[0])
    arge, argv = [fmt], [_str(fmt)]
    
    for c in _printf(fmt):
        if isinstance(c, PArg):
            a = args[c.idx + 1]
            # print('ctype is ',c.type)
            if c.type == 'd' or c.type == 'i' or c.type == 'u':
                arge.append(a)
                argv.append(int(a))
            elif c.type == 's':
                s = cstr(a)
                #print(_str(s))
                arge.append(s)
                argv.append(_str(s))
            elif c.type == 'c':
                #print('in model.py the a is', a.value)
                arge.append(a)
                argv.append(chr(int(a)))
            elif c.type == 'f':
                # print('in model.py the float a is',float(a.value))
                arge.append(a)
                argv.append(float(a.value))
            elif c.type == 'l':
                # print('in model.py the double a is',a)
                arge.append(a)
                argv.append(float(a.value))
   
    execute(PRINT, instr, args=args, arge=arge, argv=argv)


@register
def INTERNAL_ARRAY(instr, args, value):
    pass


@register
def INTERNAL_VARIABLE(instr, args, value):
    pass


def _pow(x, y):
    _x, _y = signed(x), signed(y)
    if _y < 0:
        desc = ["The second argument of pow() is negative"]
        if isinstance(y, Instr):
            desc.append(y.var_values())
        
        raise SymbExecException(*desc)
    elif _y == 0:
        return 1
    elif _y == 1:
        return x
    else:
        return ['*'] + ([x] * _y)


def _atoi(ptr, base):
    def digit(d):
        v = int(d)
        if 48 <= v <= 57:
            return ['-', d, 48], v - 48
        if 65 <= v <= 90:
            return ['-', d, 55], v - 55
        if 97 <= v <= 122:
            return ['-', d, 87], v - 87
        return None

    s = cstr(ptr)
    b = int(base)
    negative = False
    if int(s[0]) == 45: # -
        negative = True
        s = s[1:]
    s = list(takewhile(operator.truth, map(digit, s)))
    s.reverse()

    vexpr = [['*', d, _pow(base, r)] for (d, _), r in zip(s, count(0))]
    value = [d * (b ** r) for (_, d), r in zip(s, count(0))]

    if not vexpr:
        vexpr = 0
    elif len(vexpr) > 1:
        vexpr = ['+'] + vexpr
    else:
        vexpr = vexpr[0]

    if value:
        value = reduce(operator.add, value)
    else:
        value = 0

    if negative:
        vexpr = ['*', -1, vexpr]
        value *= -1

    return vexpr, value, len(s)


@register
def atoi(instr, args, value):
    vexpr, _, _ = _atoi(args[0], 10)
    execute(FNIns, instr, expr=makeval(vexpr, value),
            fname='atoi', fargs=args)


def _strlen(ptr):
    return len(cstr(ptr))
    

def _strcpy(instr, dst, src, size=None):
    global mem
    # mem = symbexec.mem
    if size is None:
        l = _strlen(src)
    else:
        l = min(_strlen(src), size)
    if int(src) + l >= int(dst) and int(dst) + l >= int(src):
        raise SymbExecException("source overlaps destination")
    
    for d, s in zip(count(dst), cstr(src, size, True)):
        execute(STIns, instr, expr=makeval(s), addr=makeval(d))
        # mem[d] = s


@register
def strlen(instr, args, value):
    execute(FNIns, instr, expr=makeval(value),
            fname="strlen", fargs=args)

        
@register
def strdup(instr, args, value):
    _strcpy(instr, value, args[0])
    execute(OPIns, instr, expr=makeval(value))


@register
def strcat(instr, args, value):
    dst, src = args
    off = len(cstr(dst))
    _strcpy(instr, int(dst) + off, src)
    execute(OPIns, instr, expr=makeval(args[0], value))


@register
def strcpy(instr, args, value):
    dst, src = args
    _strcpy(instr, dst, src)
    execute(OPIns, instr, expr=makeval(args[0], value))


@register
def strchr(instr, args, value):
    string, char = args
    char = int(char)
    for c, p in zip(cstr(string), count(0)):
        if int(c) == char:
            execute(FNIns, instr, expr=makeval(['+', string, p], value),
                    fname='strchr', fargs=args)
            return
    else:
        execute(FNIns, instr, expr=makeval(0, value),
                fname='strchr', fargs=args)


@register
def strrchr(instr, args, value):
    string, char = args
    char = int(char)
    for c, p in reversed(list(zip(cstr(string), count(0)))):
        if int(c) == char:
            execute(OPIns, instr, expr=makeval(['+', string, p], value))
            return
    else:
        execute(OPIns, instr, expr=makeval(0, value))


@register
def strcmp(instr, args, value):
    execute(FNIns, instr, expr=makeval(value),
            fname="strcmp", fargs=args)


@register
def strtol(instr, args, value):
    vexpr, _, endp = _atoi(args[0], args[2])

    if int(args[1]) != 0:
        execute(STIns, instr,
                expr=makeval(['+', args[0], endp], int(args[0]) + endp),
                addr=makeval(args[1]))

    execute(OPIns, instr, expr=makeval(vexpr, value))


@register
def strncat(instr, args, value):
    dst, src, size = args
    off = len(cstr(dst, size))
    _strcpy(instr, int(dst) + off, src, int(size) - off)
    execute(OPIns, instr, expr=makeval(args[0], value))



def _memcpy(dst, src, size):
    global mem
    # mem = symbexec.mem
    for d, s in zip(count(int(dst)), readmems(src, int(size))):
        mem[d] = s

        
def _memset(dst, c, size):
    global mem
    # mem = symbexec.mem
    dst, size = int(dst), int(size)
    for d in range(dst, dst + size):
        mem[d] = c


@register
def memcpy(instr, args, value):
    dst, src, size = args
    _memcpy(dst, src, size)
    execute(OPIns, instr, expr=makeval(args[0], value))


@register
def memset(instr, args, value):
    dst, c, size = args
    _memset(dst, c, size)
    execute(OPIns, instr, expr=makeval(args[0], value))


@register
def llvm_memset(instr, args, value):
    dst, c, size, _, _ = args
    _memset(dst, c, size)


@register
def llvm_memcpy(instr, args, value):
    dst, src, size, _, _ = args
    _memcpy(dst, src, size)


@register
def sscanf(instr, args, value):
    fmtstr = _str(cstr(args[1]))
    if fmtstr == '%d':
        vexpr, value, _ = _atoi(args[0], 10)
        execute(STIns, instr, expr=makeval(vexpr, value),
                addr=makeval(args[2]))
    else:
        assert False, fmtstr


@register
def DESCRIPTION(instr, args, value):
    descstr = _str(cstr(args[0]))
    symbexec.desc = descstr


@register
def END_DESCRIPTION(instr, args, value):
    symbexec.desc = None


def _int2str(n, b, symbols='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        return (_int2str(n//b, b, symbols) if n >= b else "") + symbols[n%b] 


def _itoa(instr, ptr, val, n, radix, lower=False):
    i = 0
    if n < 0:
        execute(STIns, instr,
                expr=makeval(ord('-')),
                addr=makeval(['ptr', ptr, i], int(ptr) + i))
        n = -n
        i += 1

    s = _int2str(n, radix)
    for l, c in reversed(list(zip(count(0), reversed(s)))):
        if lower:
            c = c.lower()
        x = (n // (radix ** l)) % radix
        e = ['%', ['/', val, radix ** l], radix]
        if x < 10:
            x += ord('0')
            e = ['+', e, ord('0')]
        elif lower:
            x += ord('a') - 10
            e = ['+', e, ord('a') - 10]
        else:
            x += ord('A') - 10
            e = ['+', e, ord('A') - 10]

        assert x == ord(c), (x, c)
        execute(STIns, instr,
                expr=makeval(e, ord(c)),
                addr=makeval(['ptr', ptr, i], int(ptr) + i))
        i += 1
    return i


@register
def sprintf(instr, args, value):
    global mem
    # mem = symbexec.mem
    dst = args[0]
    fmt = cstr(args[1])
    idx = 0
    
    for c in _printf(fmt):
        if isinstance(c, PArg):
            a = args[c.idx + 2]
            if c.type == 'd':
                off = _itoa(instr, dst, a, signed(a), 10)
                idx += off
                
            elif c.type == 'x':
                off = _itoa(instr, dst, a, signed(a), 16, lower=True)
                idx += off

            elif c.type == 'X':
                off = _itoa(instr, dst, a, signed(a), 16)
                idx += off

            elif c.type == 's':
                for src in cstr(a):
                    execute(STIns, instr,
                            expr=makeval(src),
                            addr=makeval(['ptr', dst, idx], int(dst) + idx))
                    idx += 1

            elif c.type == 'c':
                execute(STIns, instr,
                        expr=makeval(a),
                        addr=makeval(['ptr', dst, idx], int(dst) + idx))
                idx += 1
        else:
            execute(STIns, instr,
                    expr=makeval(c),
                    addr=makeval(['ptr', dst, idx], int(dst) + idx))
            idx += 1

    execute(STIns, instr,
            expr=makeval(0),
            addr=makeval(['ptr', dst, idx], int(dst) + idx))
    execute(OPIns, instr, expr=makeval(value))


@register
def isalpha(instr, args, value):
    execute(FNIns, instr, expr=makeval(value),
            fname='isalpha', fargs=args)


@register
def isdigit(instr, args, value):
    execute(FNIns, instr, expr=makeval(value),
            fname='isdigit', fargs=args)


@register
def isspace(instr, args, value):
    execute(FNIns, instr, expr=makeval(value),
            fname='isspace', fargs=args)


@register
def toupper(instr, args, value):
    c = args[0]
    v = int(c)
    if 97 <= v <= 122:
        vexpr = ['-', c, 32]
    else:
        vexpr = c
    execute(OPIns, instr, expr=makeval(vexpr, value))
        

@register
def tolower(instr, args, value):
    c = args[0]
    v = int(c)
    if 65 <= v <= 90:
        vexpr = ['+', c, 32]
    else:
        vexpr = c
    execute(OPIns, instr, expr=makeval(vexpr, value))


@register
def abs(instr, args, value):
    v = args[0]
    if signed(v) >= 0:
        execute(FNIns, instr, expr=makeval(v, value),
                fname='abs', fargs=args)
    else:
        execute(FNIns, instr, expr=makeval(['-', 0, v], value),
                fname='abs', fargs=args)
    

@register
def pow(instr, args, value):
    vexpr = _pow(args[0], args[1])
    execute(FNIns, instr, expr=makeval(vexpr, value),
            fname='pow', fargs=args)
    

def signed(v):
    v = int(v)
    if v <= 0x7fffffff:
        return v
    else:
        return -((~v & 0xffffffff) + 1)


@register
def INPUT_VARIABLE(instr, args, value):
    global input_seq, input_variables
    input_seq += 1
    V = input_variables[input_seq - 1]
    assert int(args[0]) == V[0]

    execute(STIns, instr, expr=makeval(V[1]), addr=makeval(args[0]))


@register
def INPUT_MATRIX(instr, args, value):
    global input_seq, input_variables 

    base = int(args[0])
    row = int(args[1])
    col = int(args[2])
    m = int(args[3])
    n = int(args[4])

    for i in range(m):
        for j in range(n):
            input_seq += 1
            V = input_variables[input_seq - 1]
            execute(STIns, instr, expr=makeval(V[1]),
                    addr=makeval(V[0]))



@register
def INPUT_STRING(instr, args, value):
    global input_seq, input_variables

    for i in count(0):
        input_seq += 1
        V = input_variables[input_seq - 1]
        assert int(args[0]) + i == V[0]
        execute(STIns, instr, expr=makeval(V[1]), addr=makeval(['ptr', args[0], i], int(args[0]) + i))

        if int(V[1]) == 0:
            break


@register
def INPUT_CHAR(instr, args, value):
    global input_seq, input_variables
    input_seq += 1

    V = input_variables[input_seq - 1]
    assert int(args[0]) == V[0]
    
    execute(STIns, instr, expr=makeval(V[1]), addr=makeval(args[0]))
    execute(OPIns, instr, expr=makeval(value))

    
