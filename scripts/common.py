import sys
import time
from inst import *
from functools import wraps

DEBUG_DEST = sys.stderr
ERROR_DEST = sys.stderr

def parseargs(argvs):
    '''
    Simple argument parser
    '''
    args = []
    kwargs = {}

    nextopt = None

    for arg in argvs:
        if nextopt:
            kwargs[nextopt] = arg
            nextopt = None

        elif arg.startswith('--'):
            nextopt = arg[2:]

        elif arg.startswith('-'):
            kwargs[arg[1:]] = True

        else:
            args.append(arg)

    return args, kwargs

def debug(msg, *args):
    if args:
        msg %= tuple(args)
    print('[debug] %s' % (msg,), file=DEBUG_DEST)

def log_func():
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            print('-'*20)
            print('# Func: %s' % func.__name__)
            begin = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print('\n## Cost time: %.2fs'% (end - begin))
            print('-'*20)
            return result

        return wrapped_function

    return logging_decorator

class Param(object):
    def __init__(self, exec, loc, seq, printins):
        self.exec = exec
        self.loc = loc
        self.seq = seq
        self.printins = printins

def depth(I):
    if I is None:
        return -1
    if I.cdep is None:
        return 0
    else:
        return depth(I.cdep) + 1