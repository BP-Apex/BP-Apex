from llvmtype import *

opcodes = {1:'==',2:'>',3:'>=',4:'<',5:'<=',8:'+', 9:['float','+'], 10:'-', 11:['float','-'], 12:'*', 13:['float','*'], 14:'/', 15:'/', 16:['float','/'], 17:'%', 18:'%', 19:['float','%'],
           20:'<<', 21:'>>', 22:'>>', 23:'&&', 24:'||', 25:'^',
           32:'=', 33:'!=', 34:'>', 35:'>=', 36:'<', 37:'<=',
           38:'>', 39:'>=', 40:'<', 41:'<=',42:'!='}

class Arg(Command):
    argno = Field()


class IRef(Ref):
    def __init__(self, key, context=None):
        super().__init__('llvm', key, context=context)


class DBG(Command):
    fname = Field()
    lineno = Field()
    column = Field()

    def fetch(self):
        from linecache import getline
        if self.fname and self.lineno:
            line = getline(self.fname, self.lineno).rstrip()
            return "%s: %s" % (self.lineno, line)
        else:
            return None


@cmdfunc
def LocalVar(vid, vname, vtype, context=None):
    alloc = context[vid]
    alloc.vname = vname
    alloc.vtype = TypePointer(vtype)


class LLVM(KeyCommand):
    vid = KeyField()
    dbg = Field()


class GlobalVar(LLVM):
    vname = Field()
    vtype = Field()
    initial = Field()


class Function(LLVM):
    fname = Field()
    rtype = Field()
    args = MultiField()


class FuncParam(Command):
    param = Field()
    pname = Field()
    ptype = Field()


class BasicBlock(LLVM):
    successors = MultiField()


class LLVMInst(LLVM):
    pass


class AllocaInst(LLVMInst):
    vname = Field()
    vtype = Field()


class CallInst(LLVMInst):
    func = Field()
    args = MultiField()


class CallParam(Command):
    param = Field()
    ptype = Field()


class CastInst(LLVMInst):
    ftype = Field()
    ttype = Field()
    value = Field()


class CmpInst(LLVMInst):
    opcode = Field()
    operands = MultiField()


class BinopInst(LLVMInst):
    opcode = Field()
    operands = MultiField()


class StoreInst(LLVMInst):
    waddr = Field()
    value = Field()


class LoadInst(LLVMInst):
    raddr = Field()


class SelectInst(LLVMInst):
    cond = Field()
    Tval = Field()
    Fval = Field()


class GetPtrInst(LLVMInst):
    base = Field()
    idxs = MultiField()


class BranchInst(LLVMInst):
    cond = Field()
    targets = MultiField()


class ReturnInst(LLVMInst):
    value = Field()


class PhiInst(LLVMInst):
    cases = MultiField()


class PhiCase(Command):
    value = Field()
    block = Field()


class SwitchInst(LLVMInst):
    cond = Field()
    cases = MultiField()


class SwitchCase(Command):
    value = Field()
    target = Field()


class LLVMProg:
    def __init__(self):
        from collections import OrderedDict
        self.instrs = OrderedDict()

    def __iter__(self):
        return iter(self.instrs.values())

    def __setitem__(self, key, elem): 
        if isinstance(key, tuple):
            key = key[1]
        self.instrs[key] = elem

    def __getitem__(self, key):
        if isinstance(key, tuple):
            key = key[1]
        try:
            return self.instrs[key]
        except:
            return None
        #     for x in self.instrs.items():
        #         print(x)
            #print("tmp store inst:", key)

    def load(self, filename):
        empty_dbgs = []
        currB = None
        for line in open(filename):
            instr = loads(line, context=self)
            if instr:
                if getattr(instr, 'dbg', None):
                    for _ins in empty_dbgs:
                        _ins.dbg = instr.dbg
                    empty_dbgs = []
                elif isinstance(instr, BasicBlock):
                    empty_dbgs.append(instr)

                if isinstance(instr, BasicBlock):
                    currB = instr
                elif isinstance(instr, (ReturnInst, BranchInst, SwitchInst)):
                    currB.terminator = instr

    def set_cfg(self, cfg):
        for block in cfg.blocks:
            self[block.bid].ipdom = block.ipdom.bid
            self[block.bid].pdf = [self[b.bid].terminator.vid for b in block.pdf]

    def loadcfg(self, filename):
        from cfg import CFG
        cfg = CFG()
        cfg.load(filename)
        self.set_cfg(cfg)
