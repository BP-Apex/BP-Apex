#!/usr/bin/python3
from collections import defaultdict
from cfg import *
import argparse
import sexpdata

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-out', default='cfg.out')
    parser.add_argument('-llvm', default='llvm.out')
    args = parser.parse_args()
    cfg = CFG()

    for l in open(args.llvm):
        x = sexpdata.loads(l)
        if x[0] == sexpdata.Symbol('BasicBlock'):
            block = CFGBlock(x[1], context=cfg)
        elif x[0] == sexpdata.Symbol('StoreInst'):
            block.btype = 2


    for l in open(args.llvm):
        x = sexpdata.loads(l)
        if x[0] == sexpdata.Symbol('BasicBlock'):
            pred = cfg[x[1]]
            for _succ in x[3:]:
                succ = cfg[_succ[1]]
                cfg.add_edge(pred, succ, 0)

                # CFGEdge(block, CFGRef(args.tag, succ[1]), 0))
            
    # # initialize
    # for n in cfg.blocks:
    #     n.succ = []
    #     n.pred = []
    # for e in cfg.edges:
    #     e.pred.succ.append(e)
    #     e.succ.pred.append(e)

    entries = [n for n in cfg.blocks if not n.pred]


    ## classify edges into tree, forward, cross, back
    for n in cfg.blocks:
        n.entry = n.exit = None
    for n in entries:
        dfs(n)

    ## set target of back edges as type 3 (loop)
    backedges = [e for e in cfg.edges if e.etype == BACK_EDGE]
    for e in backedges:
        e.succ.btype = 3

    # ## draw cfg into dot.0
    # draw_dot(cfg, "dot.1")

    ## compute ipdom
    for n in entries:
        compute_ipdom(n)

    # for n in entries:
    #     compute_idom(n)

    for n in entries:
        compute_pdf(n)

    # for n in cfg.blocks:
    #     n.pdom = sorted(n.pdom, key=lambda x: x.bid)
    #     n.pdf = sorted(n.pdf, key=lambda x: x.bid)

    # ## draw ipdom cfg into
    # draw_ipdom_dot(cfg, "dot.2")
    # draw_idom_dot(cfg, "dot.3")
    import pickle
    with open(args.out, 'wb') as f :
        pickle.dump(cfg, f)



def find_path(graph, src, dst, nodes):
    if src is dst:
        nodes.add(src)
        return True

    if src in nodes:
        return True

    p = [find_path(graph, succ, dst, nodes) for succ in graph[src]]
    if any(p):
        nodes.add(src)
        return True
    else:
        return False


_ctime = 0
def ctime():
    global _ctime
    _ctime += 1
    return _ctime


def dfs(n):
    n.entry = ctime()
    for e in n.succ:
        assert n == e.pred
        s = e.succ
        if s.entry is None:
            e.etype = 1
            dfs(s)
        elif s.exit is None:
            e.etype = 2
        elif s.entry > n.entry:
            e.etype = 3
        else:
            e.etype = 4
    n.exit = ctime()


def draw_dot(cfg, filename):
    f = open(filename, "w")
    f.write("digraph {\n")
    for b in cfg.blocks:
        if not b.succ:
            f.write("B%s [shape=rect];\n" % b.bid)
        if b.btype == 1:
            f.write("B%s [color=\"yellow\"];\n" % b.bid)
        if b.btype == 2:
            f.write("B%s [color=\"blue\"];\n" % b.bid)
        if b.btype == 3:
            f.write("B%s [color=\"red\"];\n" % b.bid)

    colors = {TREE_EDGE: 'black', BACK_EDGE: 'red', FWD_EDGE: 'green', CROSS_EDGE: 'blue'}
    for e in cfg.edges:
        p = e.pred
        s = e.succ
        f.write("B%s -> B%s [color=%s];\n" % (p.bid, s.bid, colors[e.etype]))
    f.write("}\n")


def draw_ipdom_dot(cfg, filename):
    f = open(filename, "w")
    f.write("digraph {\n")
    for b in cfg.blocks:
        if not b.succ:
            f.write("B%s [shape=rect];\n" % b.bid)
        if b.btype == 1:
            f.write("B%s [color=\"yellow\"];\n" % b.bid)
        if b.btype == 2:
            f.write("B%s [color=\"blue\"];\n" % b.bid)
        if b.btype == 3:
            f.write("B%s [color=\"red\"];\n" % b.bid)

    colors = {TREE_EDGE: 'black', BACK_EDGE: 'red', FWD_EDGE: 'green', CROSS_EDGE: 'blue'}
    for b in cfg.blocks:
        if b.ipdom:
            f.write("B%s -> B%s;\n" % (b.bid, b.ipdom.bid))
    f.write("}\n")


def draw_idom_dot(cfg, filename):
    f = open(filename, "w")
    f.write("digraph {\n")
    for b in cfg.blocks:
        if not b.succ:
            f.write("B%s [shape=rect];\n" % b.bid)
        if b.btype == 1:
            f.write("B%s [color=\"yellow\"];\n" % b.bid)
        if b.btype == 2:
            f.write("B%s [color=\"blue\"];\n" % b.bid)
        if b.btype == 3:
            f.write("B%s [color=\"red\"];\n" % b.bid)

    colors = {TREE_EDGE: 'black', BACK_EDGE: 'red', FWD_EDGE: 'green', CROSS_EDGE: 'blue'}
    for b in cfg.blocks:
        for d in b.dom:
            f.write("B%s -> B%s;\n" % (b.bid, d.bid))
    f.write("}\n")


def merge(nodes, edges):
    merges = defaultdict(list)
    while True:
        candidate = find_candidate(nodes)
        if candidate is None:
            break
        assert len(candidate.pred) == 1
        parent = next(iter(candidate.pred))
        merges[parent].append(candidate)

        parent.succ.remove(candidate)
        parent.succ.update(candidate.succ)
        for s in candidate.succ:
            s.pred.remove(candidate)
            s.pred.add(parent)
            
        del nodes[candidate.bb]
        if (parent.bb, candidate.bb) in edges:
            del edges[(parent.bb, candidate.bb)]

    return merges


def collect_cfg(entry):
    cfg = set() 
    queue = [entry]
    while queue:
        n = queue.pop()
        if n in cfg: continue
        cfg.add(n)
        queue.extend([e.succ for e in n.succ])
        queue.extend([e.pred for e in n.pred])

    assert len(cfg) == len(set(x.bid for x in cfg))
    return cfg


def compute_pdf(node):
    cfg = collect_cfg(node)
    for v in cfg:
        v.pdf = set()
    
    for n in cfg:
        for m in cfg:
            if n not in m.pdom: continue
            for z in m.pred:
                z = z.pred
                if n == z or n not in z.pdom:
                    n.pdf.add(z)


def compute_ipdom(node):
    cfg = collect_cfg(node)
    terminators = [n for n in cfg if not n.succ] 
    if len(terminators) == 0:
        print(node.bb)
        for n in cfg:
            print(n.bb, n.succ)
    assert len(terminators) == 1, len(terminators)

    t = terminators[0]
    for n in cfg:
        n.pdom = set(cfg)
    t.pdom = {t}

    queue = [e.pred for e in t.pred]
    while queue:
        n = queue.pop()
        k = len(n.pdom)
        for e in n.succ:
            s = e.succ
            n.pdom.intersection_update(s.pdom)
        n.pdom.add(n)
        if len(n.pdom) != k:
            queue.extend([e.pred for e in n.pred])

    for n in cfg: 
        n.ipdom = t
        for pdom in n.pdom:
            if pdom == n: continue
            if n.ipdom in pdom.pdom:
                n.ipdom = pdom


def compute_idom(node):
    cfg = collect_cfg(node)
    t = node
    for n in cfg:
        n.dom = set(cfg)
    t.dom = {t}

    queue = [e.succ for e in t.succ]
    while queue:
        n = queue.pop()
        k = len(n.dom)
        for e in n.pred:
            p = e.pred
            n.dom.intersection_update(p.dom)
        n.dom.add(n)
        if len(n.dom) != k:
            queue.extend([e.succ for e in n.succ])

    for n in cfg: 
        n.idom = t
        for dom in n.dom:
            if dom == n: continue  
            if n.idom in dom.dom:
                n.idom = dom


def removable(n):
    return n.btype == 1 and len(n.pred) == 1 and next(iter(n.pred)).btype != 3


def find_candidate(nodes):
    for n in nodes.values():
        if removable(n) and any(not removable(p) for p in n.pred):
            return n
    return None


if __name__ == '__main__':
    main()

