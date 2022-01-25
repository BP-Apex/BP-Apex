#!/usr/bin/python3
from llvm import *
from command import *
from common import *
from expr import *
import argparse
import model
import sys
from collections import defaultdict
import pickle
def print_object(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

sys.setrecursionlimit(10000)

mem = defaultdict(lambda: None)
desc = None

class CDEP:
    __slots__ = 'bb', 'ipdom'
    def __init__(self, bb, ipdom):
        self.bb = bb
        self.ipdom = ipdom
    def __repr__(self):
        return 'BB%s %s' % (self.bb.vid, self.ipdom)


class CALL:
    __slots__ = 'name', 'args', 'prevBB', 'currBB', 'retins'
    def __init__(self, name, args, prevBB, currBB):
        self.name = name
        self.args = args
        self.prevBB = prevBB
        self.currBB = currBB
        self.retins = None
    def __repr__(self):
        return 'CALL(%s)' % \
            (' '.join(str(arg) for arg in self.args), )
 

class LLVMVisitor:
    def initializeVar(self, instr, addr, type, value):
        from itertools import count
        assert isinstance(value, (list, int))

        if isinstance(type, TypeArray):
            if not isinstance(value, list):
                value = [value]
            elem = type.elemType 
            size = elem.type_size()
            for _a, _v in zip(count(addr, size), value):
                self.initializeVar(instr, _a, elem, _v)

        elif isinstance(type, TypeStruct):
            assert isinstance(value, list)
            for _m, _v in zip(type.members(), value):
                self.initializeVar(instr, addr + _m.offset, _m.type, _v)

        else:
            assert isinstance(type, (TypePointer, TypeInt))
            execute(ITIns, instr,
                    addr=makeval(addr), expr=makeval(value))

    def visitGlobalVar(self, instr, value, flag):
        assert isinstance(instr.vtype, TypePointer)
        self.initializeVar(instr, value, instr.vtype.elemType, instr.initial)

        execute(VVIns, instr,
                name=instr.vname, type=instr.vtype,
                expr=makeval(value))
        
    def visitAllocaInst(self, instr, value, flag):
        execute(VVIns, instr,
                name=instr.vname, type=instr.vtype,
                expr=makeval(value))

    def visitBasicBlock(self, instr, value, flag):
        global prevBB, currBB, cdepstack
        
        if currBB is not None:
            cdepstack.append(currBB)
        while cdepstack and cdepstack[-1].ipdom == instr.vid:
            cdepstack.pop()
        
        BB = execute(BBIns, instr, cdep=cdepstack[-1], ipdom=instr.ipdom,
                     pdf=instr.pdf)
        prevBB, currBB = currBB, BB
        if prevBB:
            prevBB.next = currBB
        currBB.prev = prevBB

    def visitStoreInst(self, instr, value, flag):
        waddr = resolve(instr.waddr)
        vexpr = resolve(instr.value)
        if vexpr is not None:
            execute(STIns, instr,
                    addr=makeval(waddr), expr=makeval(vexpr, value))


    def visitLoadInst(self, instr, value, flag):
        raddr = resolve(instr.raddr)
        vexpr = mem[raddr.value]
        execute(LDIns, instr,
                addr=makeval(raddr), expr=makeval(vexpr, value))

    def visitCallInst(self, instr, value, flag):
        if flag == 1:
            self.enterCallInst(instr, value)
        else:
            self.leaveCallInst(instr, value)

    def enterCallInst(self, instr, value):
        global prevBB, currBB
        name = instr.func.temp.fname
        args = [resolve(arg.param) for arg in instr.args]
        callstack.append(CALL(name, args, prevBB, currBB))
        prevBB, currBB = None, None

    def leaveCallInst(self, instr, value):
        global prevBB, currBB
        call = callstack.pop()
        
        prevBB, currBB = call.prevBB, call.currBB
        vexpr = call.retins
        if vexpr:
            execute(OPIns, instr, expr=makeval(vexpr, value))
        else:
            model.run(call.name, instr, value, call.args)

    def visitReturnInst(self, instr, value, flag):
        vexpr = resolve(instr.value)
        I = execute(OPIns, instr, expr=makeval(vexpr, value))
        callstack[-1].retins = I

    def visitBranchInst(self, instr, value, flag):
        vexpr = resolve(instr.cond)
        execute(BRIns, instr, expr=makeval(vexpr, value),
                locT=instr.targets[0].temp.dbg.lineno, locF=instr.targets[1].temp.dbg.lineno)

    def visitGetPtrInst(self, instr, value, flag):
        base = resolve(instr.base)
        idxs = [resolve(i) for i in instr.idxs]
        vexpr = _list('ptr', base, *idxs)
        execute(OPIns, instr, expr=makeval(vexpr, value))

    def visitCastInst(self, instr, value, flag):
        vexpr = resolve(instr.value)
        if int(vexpr) != value:
            vexpr = _list('-', vexpr, value - int(vexpr))
        execute(OPIns, instr, expr=makeval(vexpr, value))

    def visitBinopInst(self, instr, value, flag):
        binop = opcodes[instr.opcode]
        opers = [resolve(o) for o in instr.operands]
        vexpr = _list(binop, *opers)
        execute(OPIns, instr, expr=makeval(vexpr, value))

    def visitCmpInst(self, instr, value, flag):
        cmpop = opcodes[instr.opcode]
        opers = [resolve(o) for o in instr.operands]
        vexpr = _list(cmpop, *opers)
        execute(OPIns, instr, expr=makeval(vexpr, value))

    def visitSwitchInst(self, instr, value, flag):
        vexpr = resolve(instr.cond)
        execute(BRIns, instr,
                expr=makeval(vexpr, value))

    def visitSelectInst(self, instr, value, flag):
        errs("ERR: SELECT at %d: %s" % (instr.vid, instr.dbg.fetch()))
        assert False

    
    def visitPhiInst(self, instr, value, flag):
        cases = dict((c.block.temp.vid, c.value) for c in instr.cases)
        dfd=cases[prevBB.vid]
        vexpr = resolve(cases[prevBB.vid])
        execute(OPIns, instr, 
                expr=makeval(vexpr, value))




def main():
    from collections import defaultdict
    parser = argparse.ArgumentParser()
    parser.add_argument('-out', required=True)
    # parser.add_argument('-tag', required=True)
    parser.add_argument('-cfg', required=True)
    parser.add_argument('-llvm', default='~/dachuang/apex/A/llvm.out')
    parser.add_argument('-exec', default='~/dachuang/apex/A/exec.out')
    parser.add_argument('-args', default='~/dachuang/apex/A/args.out')
    parser.add_argument('-vars', default='~/dachuang/apex/A/vars.out')
    args = parser.parse_args()

    global log, reg, mem, var, program, \
        cdepstack, callstack, exectrace, \
        prevBB, currBB
    log = open('symb.log', 'w')
    reg = defaultdict(lambda: None)
    # mem = defaultdict(lambda: None)
    var = {}
    program = None
    cdepstack = []
    callstack = []
    exectrace = []
    E = Exec()
    prevBB = None
    # currBB = BBIns(0, 0, ipdom=0)
    currBB = E.root
    currBB.terminator = currBB
    with open(args.cfg, 'rb') as f:
        cfg = pickle.load(f)

    program = LLVMProg()
    program.load(args.llvm)
    program.set_cfg(cfg)

    visitor = LLVMVisitor()

    callstack.append(CALL('main', [None, None], None, None))
    for instr in program:
        instr.vii = 1

    from itertools import chain
    input_seq = 1
    for addr, value in chain(read_args(args.args), read_args(args.vars)):
        mem[addr] = Input(input_seq, value)
        input_seq += 1
    model.set_argument(read_args(args.args))

    from sexpdata import loads
    for line in open(args.exec):
        e = loads(line)
        vid, val, flag = e[1:4]
        try:
            program[vid].accept(visitor, val, flag)
        except model.SymbExecException as e:
            print_symberror(program[vid], e.args)
            sys.exit(1)
            
        except Exception as e:
            errs('ERROR at %d: %s' % (vid, program[vid]))
            raise

    last = program[vid]
    if not isinstance(last, ReturnInst) and \
       not (isinstance(last, CallInst) and last.func.fname == 'exit'):
        print_symberror(last,
                        ["program terminated unexpectedly at the following location",
                         exectrace[-1].var_values()])
        sys.exit(1)

    
    # E = Exec()
    for I in exectrace:
        if isinstance(I, BBIns): continue
        if I.cdep is None: I.cdep = E.root
        # assert I.cdep is not None, (I.vid, I)
        # assert not isinstance(I.cdep, BBIns), (I.vid, I)
        

        I.pdf = I.bb.pdf
        k = (I.vid, I.vii)
        E[k] = I

       
    f = open(args.out + '.xxx', "w")
    for I in exectrace:
        if not isinstance(I, BBIns):
    #         I.pdf = I.bb.pdf
            f.write(str(I) + "\n")
    f.close()

    f = open(args.out, 'wb')
    pickle.dump(E, f, protocol=pickle.HIGHEST_PROTOCOL)
    f.close()

def print_symberror(stmt, msgs):
    f1 = open("symberror.out", "w")
    f2 = open("src.c", "r")
    print(stmt)
    from itertools import count
    for l, n in zip(f2, count(1)):
        l = l.rstrip()
        if n == stmt.dbg.lineno:
            for msg in msgs:
                f1.write('--- // <<<< ' + msg + ' >>>>\n')
            f1.write('--- ')
            if l[:4] == '    ':
                l = l[4:]
            else:
                l = l.lstrip()
            f1.write(l)
            f1.write("    // (WRONG)\n")
        else:
            f1.write(l)
            f1.write("\n")
    f1.close()
    f2.close()
    sys.exit(1)



def read_args(filename):
    try:
        for l in open(filename):
            l = l.split()
            if not l:
                continue
            yield int(l[0], 16), int(l[1])
    except FileNotFoundError:
        pass


def execute(cls, instr, **kwargs):
    global currBB, exectrace, desc
    source = (instr.dbg and instr.dbg.fetch()) or None
    lineno = (instr.dbg and instr.dbg.lineno) or 0
    I = cls(instr.vid, instr.vii,
            src=source, loc=lineno, bb=currBB, **kwargs)
    reg[I.vid] = I
    instr.vii += 1

    if isinstance(I, BBIns):
        I.bb = I
    else:
        I.cdep = I.bb.cdep.terminator

    if instr.vii > 10000:
        raise model.SymbExecException(
            "There are too many iterations",
            "Check whether the condition of loop having this statement is correct")

    if isinstance(I, STIns):
        I.desc = desc

    if isinstance(I, (STIns, ITIns)):
        mem[I.addr.value] = I

    if isinstance(I, BRIns):
        currBB.terminator = I

    exectrace.append(I)
    return I


def makeval(e0, v=None):
    if isinstance(e0, int):
        assert v is None or e0 == v or e0 & 0xffffffff == v & 0xffffffff, (e0, v)
        v = e0
    elif isinstance(e0, (Input, OPIns)):
        # assert v is None or \
        #        e0.value == v or e0.value & 0xffffffff == v & 0xffffffff or abs(e0.value) + abs(v) == 0x100000000, \
        #        (e0.value, v, e0)
        v = e0.value
    elif isinstance(e0, list):
        assert v is not None
    else:
        # assert False, type(e0)
        assert v is not None
        return Val(e0=expr(v), e1=expr(v), e2=expr(v), e3=expr(v), e4=expr(v), v=v)
        
    if isinstance(e0, list):
        e0 = expr(*e0)
    else:
        e0 = expr(e0)
    e1 = expand1(e0)
    e2 = expand2(e0)
    e3 = expand3(e0)
    e4 = expand4(e0)
    return Val(e0=e0, e1=e1, e2=e2, e3=e3, e4=e4, v=v)


def resolve(llvm):
    if isinstance(llvm, IRef):
        id = llvm.temp.vid
        if id == -1:
            return None
        return reg[id]
    elif isinstance(llvm, Arg):
        return callstack[-1].args[llvm.argno]
    else:
        return llvm


def isinternal(addr):
    return 0xa0000000 <= addr < 0xb0000000 or addr in var


if __name__ == '__main__':
    model.symbexec = sys.modules[__name__]
    model.initialize(execute, makeval, mem)
    main()
