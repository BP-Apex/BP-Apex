from command import *
from collections import OrderedDict

__all__ = ['CFGBlock', 'CFGEdge', 'CFG', 'TREE_EDGE', 'BACK_EDGE', 'FWD_EDGE', 'CROSS_EDGE']

TREE_EDGE=1
BACK_EDGE=2
FWD_EDGE=3
CROSS_EDGE=4

class CFGBlock(KeyCommand):
    bid   = KeyField()
    btype = KWField(1)
    pdom  = KWField()
    ipdom = KWField()
    succ  = KWField(list)
    pred  = KWField(list)
    pdf   = KWField()

class CFGEdge(Command):
    pred  = Field()
    succ  = Field()
    etype = Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pred.succ.append(self)
        self.succ.pred.append(self)

class CFG:
    def __init__(self):
        self._blocks = OrderedDict()
        self._edges = []

    def __getitem__(self, bid):
        return self._blocks[bid]

    def __setitem__(self, key, block):
        if key[0] == 'cfgblock':
            key = key[1]
        self._blocks[key] = block

    blocks = property(lambda self: self._blocks.values())
    edges = property(lambda self: self._edges)

    def add_edge(self, pred, succ, etype):
        self._edges.append(CFGEdge(pred, succ, etype))

    def dump(self, filename):
        from sexpdata import dumps
        f = open(filename, "w")
        for b in self.blocks:
            f.write(dumps(encode(b)))
            f.write("\n")
        for e in self.edges:
            f.write(dumps(encode(e)))
            f.write("\n")
        f.close()

    def load(self, filename):
        from sexpdata import loads
        f = open(filename)
        for l in f:
            self.add(decode(loads(l)))
        f.close() 
