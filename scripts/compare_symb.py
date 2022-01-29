#!/usr/bin/python3
from common import *

from itertools import product
import z3
import time

ncheck = 0
npairs = 0
check_err_idx = 0
z3_timeout = 100

def compare_symb(symbA, symbB):
    global processed
    cmpins_list = []
    z3.set_param(timeout=z3_timeout)

    import pickle
    execA = pickle.load(open(symbA, 'rb'))
    execB = pickle.load(open(symbB, 'rb'))

    tmp = sys.stdout
    # sys.stdout = open(compare_log, "w")
    sys.stdout = None
    # fout = open(cmpins, "w")
    fout = None

    listSTA = [I for I in execA if isinstance(I, STIns)]
    listSTB = [I for I in execB if isinstance(I, STIns)]

    listBRA = [I for I in execA if isinstance(I, BRIns)]
    listBRB = [I for I in execB if isinstance(I, BRIns)]

    cAs = len(listSTA)
    cBs = len(listSTB)
    cAb = len(listBRA)
    cBb = len(listBRB)
    total = cAs * cBs + cAb * cBb
    processed = 0

    
    for I1, I2 in product(listSTA, listSTB):
        try:
            if I1.value != I2.value:
                c = 0
            else:
                c = compare(I1, I2)

        except:
            c = 0
        Print(fout,cmpins_list, I1, I2, c)
        processed += 1

    for I1, I2 in product(listBRA, listBRB):
        try:
            c = compare(I1, I2)
        except:
            c = 0
        Print(fout,cmpins_list, I1, I2, c)
        processed += 1

    sys.stdout = tmp
    return cmpins_list

def Print(fout, cmpins_list, I1, I2, b):
    if not b: return
    global npairs
    npairs += 1
    cmpins_list.append([I1.vid, I1.vii, I2.vid, I2.vii, b])
    # fout.write("%s %s %s %s %s\n" % (I1.vid, I1.vii, I2.vid, I2.vii, b))

def expand_expr(expr):
    if isinstance(expr, list):
        return [expr[0]] + [expand_expr(op) for op in expr[1:]]
    if isinstance(expr, (int, LDIns)):
        return expr
    if isinstance(expr, Instr):
        return expand_expr(expr.v_expr)

def expr_to_str(expr):
    if expr is None:
        return 'None'

    if isinstance(expr, list):
        if len(expr) > 2:
            return '(%s)' % ((' ' + expr[0] + ' ').join([expr_to_str(op) for op in expr[1:]]), ) 
        else:
            return '(%s%s)' % (expr[0], expr_to_str(expr[1]))
    if isinstance(expr, int):
        return str(expr)
    if isinstance(expr, LDIns):
        return str(expr.vname)
    assert False, ("wrong expr", type(expr), expr)
    
def expr_to_z3(expr):
    import operator as op
    from functools import reduce
    op_to_func = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
                  '%': op.mod, '&&': z3.And, '||': z3.Or, '^': op.xor,
                  '=': op.eq, '!=': op.ne, '>': op.gt, '>=': op.ge,
                  '<': op.lt, '<=': op.le, 'ptr': op.add,
                  '!': op.not_}

    if isinstance(expr, list):
        fn = op_to_func[expr[0]]

        if len(expr) == 2:
            return fn(expr[1])
        else:
            op = [expr_to_z3(e) for e in expr[1:]]
            return reduce(fn, op)
    if isinstance(expr, str):
        return z3.Int(expr)
    return expr

def compare(I1, I2):
    global ncheck, check_err_idx, processed
    print("\n\n== COMPARE ({I1.vid} {I1.vii}) - ({I2.vid}, {I2.vii})".format_map(locals()))

    symbols1 = I1.expr.e2.symbols()
    symbols2 = I2.expr.e2.symbols()
    print("symbol",symbols1,symbols2)
    if symbols1 != symbols2:
        print("UNMATCH SYMBS", symbols1, symbols2)
        return 0

    symbols = symbols1
    if isinstance(I1, STIns) and isinstance(I2, STIns):
        if I1.value != I2.value:
            return 0

    # if isinstance(I1, BRIns) and isinstance(I2, BRIns):
    #     if not symbols:
    #         return 0
        
    #if not symbols:
    #    if I1.value != I2.value:
    #        # print("VALUE NOT MATCH", I1.value, I2.value)
    #        return 0

    def simplify(e):
        if isinstance(e, z3.ExprRef):
            return z3.simplify(e)
        return e

    e1 = simplify(I1.expr.e2.as_z3())
    print('e1 ', e1)
    e2 = simplify(I2.expr.e2.as_z3())
    print('e2 ', e2)


    symbs1 = I1.expr.e2.symbols()
    symbs2 = I2.expr.e2.symbols()

    # try:
    #     print (e1.sexpr())
    # except:
    #     print (e1)

    # try:
    #     print (e2.sexpr())
    # except:
    #     print (e2)
    
    # e1 = simplify(expr_to_z3(I1.expr.expr1))
    # e2 = simplify(expr_to_z3(I2.expr.expr1))
    # symbs1 = get_symbs(I1.expr.expr1)
    # symbs2 = get_symbs(I2.expr.expr1)
    print('solver')

    s = z3.Solver()
    # import os
    # if os.path.exists("../precond"):
    #     for l in open("../precond"):
    #         print(loads(l))
    #         s.add(expr_to_z3(loads(l)))
    
    print('solver2')

    if symbs1 != symbs2:
        print("UNMATCH SYMBS", symbs1, symbs2)
        return 0

    # sys.stdout.flush()
    print('solver3')
    #
    # if isinstance(e1, bool) or isinstance(e2, bool):
    #     print("EITHER e1 is bool or e2 is bool")
    #     return 0

    # if isinstance(I1, STIns) and isinstance(I2, STIns):
    #     if (I1.s_type == 'i') ^ (I2.s_type == 'i'):
    #         print("EITHER I1 is important or I2 is important, not both")
    #         print(I1.s_type, I2.s_type)
    #         return 0
    #     if (I1.s_type == 'i') and (I2.s_type == 'i'):
    #         if I1.w_addr != I2.w_addr:
    #             print("BOTH important and address is different")
    #             print(I1.w_addr, I2.w_addr)
    #             return 0

    print('xx')
    print(e1, e2)
    print(type(e1), type(e2))

    print('yy')

    if isinstance(e1, z3.BoolRef) and isinstance(e2, z3.BoolRef):
        print('bool')
        if I1.value != I2.value:
            e2 = z3.Not(e2)
        s.add(e1 != e2)

        try:
            ncheck += 1
            # print("CHECKING bool ")
            # s1 = str(z3.simplify(e1))
            # s2 = str(z3.simplify(e2))
            # print(e1, s1)
            # print(e2, s2)

            _t0 = time.perf_counter()
            # s.set(timeout=z3_timeout)
            s.set('timeout', z3_timeout)
            r = s.check()
            _t1 = time.perf_counter()
            # ftime.write("time: %s\n" % (_t1 - _t0))
            # ftime.write("   " + s1 + "\n")
            # ftime.write("   " + s2 + "\n")
            # print('Check result: ', r)

        except Exception as e:
            check_err_idx += 1
            errs("ERROR %s in %s, %s" % (e, I1.expr, I2.expr))
            r = z3.sat
        
        if r == z3.unsat:
            return 1
        else:
            return 0

    if isinstance(e1, (z3.ArithRef, int, float)) and isinstance(e2, (z3.ArithRef, int, float)):
        print('arith')
        if I1.value != I2.value:
            print("VALUE NOT MATCH", I1.value, I2.value)
            return 0
        # if (not isinstance(I1.v_expr_expand, list)) or (not isinstance(I2.v_expr_expand, list)):
        #     print("I1 or I2 simple")
        #     return 0
        
        if isinstance(e1, (int, float)) and isinstance(e2, (int, float)):
            return 3
        if isinstance(e1, z3.ArithRef) and isinstance(e2, z3.ArithRef):
            s.add(e1 != e2)
            # for symb in symbs1:
            #     s.add(z3.Int(symb) != 0)
            try:
                ncheck += 1
                # print("CHECKING int ")
                s1 = str(z3.simplify(e1))
                s2 = str(z3.simplify(e2))
                # print(e1, s1)
                # print(e2, s2)

                _t0 = time.perf_counter()
                # s.set(timeout=z3_timeout)
                s.set('timeout', z3_timeout)
                r = s.check()
                _t1 = time.perf_counter()
                # ftime.write("time: %s\n" % (_t1 - _t0))
                # ftime.write("   " + s1 + "\n")
                # ftime.write("   " + s2 + "\n")
                # print('Check result: ', r)

            except Exception as e:
                check_err_idx += 1
                print("ERROR ", e, " in ", e1, e2, type(e1), type(e2))
                r = z3.sat
            if r == z3.unsat:
                return 4
            else:
                return 0
        assert False
        return 0
