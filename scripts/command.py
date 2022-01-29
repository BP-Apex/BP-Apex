#!/usr/bin/python3
import sys
sys.path.append('../scripts/lib')
import lazy_object_proxy

__all__ = ['Field', 'MultiField', 'KeyField', 'KWField',
           'Command', 'KeyCommand', 'Ref', 'Reference', 'cmdfunc',
           'decode', 'encode', 'loads', 'dumps','errs','_tuple','_list']



class uniquedict(dict):
    def __setitem__(self, key, elem):
        if key in self:
            raise KeyError('%r exists' % (key, ))
        super().__setitem__(key, elem)

__command__ = uniquedict()
__context__ = uniquedict()


def cmdfunc(func, name=None):
    if not name:
        name = func.__name__
    __command__[name.lower()] = func
    return func

def errs(*args):
    import sys
    sys.stderr.write(' '.join(str(a) for a in args))
    sys.stderr.write('\n')

def _tuple(*args):
    return tuple(args)

def _list(*args):
    return list(args)

@cmdfunc
def List(*args, **kwargs):
    return list(args)

class Field:
    sequence = 0
    __slots__ = ('seqn', 'name', 'argn')
    def __init__(self):
        Field.sequence += 1
        self.seqn = Field.sequence
        self.name = ''
        self.argn = 0

    def __call__(self, args, kwargs):
        return args[self.argn]

    def __repr__(self):
        return '<Field %s %s %s>' % (self.seqn, self.name, self.argn)


class MultiField(Field):
    __slots__ = ('size', )
    def __init__(self, size=0):
        super().__init__()
        self.size = size

    def __call__(self, args, kwargs):
        if self.size:
            return list(args[self.argn:self.argn + self.size])
        else:
            return list(args[self.argn:])


class KWField(Field):
    __slots__ = ('default', )
    def __init__(self, default=None):
        super().__init__()
        self.default = default

    def __call__(self, args, kwargs):
        if callable(self.default):
            default = self.default()
        else:
            default = self.default
        return kwargs.get(self.name, default)


class KeyField(Field): pass


class MetaCommand(type):
    def __new__(mcs, name, bases, attrs):
        from itertools import count, chain
        # single inheritance between command
        _bases = [cls for cls in bases if isinstance(cls, MetaCommand)]
        assert len(_bases) <= 1

        base_command = next(iter(_bases), None)
        base_members = getattr(base_command, '__members__', [])
        members = [attr for attr in attrs.items() if isinstance(attr[1], Field)]
        members = sorted(members, key=lambda item: item[1].seqn)
        for (fnm, fld), argn in zip(members, count(len(base_members))):
            fld.name, fld.argn = fnm, argn
        members = base_members + [fld for fnm, fld in members]
        command = attrs.get('__command__', name)
        classkey = None
        if base_command and base_command.__name__ == 'KeyCommand':
            classkey = command.lower()
        else:
            classkey = getattr(base_command, '__classkey__', None)

        attrs['__members__'] = members
        attrs['__command__'] = command
        attrs['__classkey__'] = classkey

        cls = super().__new__(mcs, name, bases, attrs)
        __command__[command.lower()] = cls
        return cls


class Command(metaclass=MetaCommand):
    def __init__(self, *args, **kwargs):
        for field in type(self).__members__:
            setattr(self, field.name, field(args, kwargs))
        fieldnames = set(f.name for f in type(self).__members__)
        for key, val in kwargs.items():
            if key not in fieldnames:
                setattr(self, key, val)
        
    def __repr__(self):
        from sexpdata import dumps
        return dumps(encode(self))

    def accept(self, visitor, *args):
        fn = getattr(visitor, 'visit' + self.__class__.__name__)
        return fn(self, *args)

class temp(Command):
    pass

class Ref(Command):
    __key__ = Field()
    
    def __init__(self, cls, *key, context=__context__):
        cls = cls.lower()
        key = _tuple(cls, *key)
        Command.__init__(self, key)
        self.temp = lazy_object_proxy.Proxy(lambda: context[self.__key__])

Reference = Ref
        

class KeyCommand(Command):
    def __init__(self, *args, context=__context__, **kwargs):
        super().__init__(*args, **kwargs)
        context[self.__key__] = self

    @property
    def __key__(self):
        cls = self.__class__.__classkey__
        key = [getattr(self, fld.name) for fld in type(self).__members__
               if isinstance(fld, KeyField)]
        return _tuple(cls, *key)


def decode(sexpr, context=__context__):
    if isinstance(sexpr, list):
        if sexpr:
            cmd, *args = sexpr
            cmd = decode_cmd(cmd)
            args, kwargs = decode_arg(args, context)
            
            return cmd(*args, **kwargs)
        else:
            return None
    else:
        return sexpr


def decode_cmd(cmd):
    from sexpdata import Symbol
    assert isinstance(cmd, Symbol)
    cmd = cmd.value().lower()
    return __command__[cmd]


def decode_arg(lst, context):
    from sexpdata import Symbol
    args = []
    kwargs = {'context': context}
    idx = 0
    while idx < len(lst):
        arg = lst[idx]
        if isinstance(arg, Symbol) and arg.value()[0] == ':':
            name = arg.value()[1:]
            arg = decode(lst[idx + 1], context)
            kwargs[name] = arg
            idx += 2
        else:
            arg = decode(arg, context)
            args.append(arg)
            idx += 1
    return args, kwargs


def loads(s, context=__context__):
    import sexpdata
    return decode(sexpdata.loads(s), context)


def encode(obj, with_ref=False):
    from sexpdata import Symbol as Sym
    if obj is None:
        return []
    elif with_ref and isinstance(obj, KeyCommand):
        return _list(Sym('ref'), *encode_arg(obj.__key__, with_ref))
    elif isinstance(obj, Command):
        return _list(Sym(obj.__class__.__command__), \
                     *encode_positional_args(obj)) + encode_keyword_args(obj)
    elif hasattr(obj, 'encode_'):
        return obj.encode_()
    elif isinstance(obj, (int, str, float)):
        return obj
    elif isinstance(obj, (list, set, tuple)):
        return _list(Sym('list'), *encode_arg(obj, with_ref))
    else:
        assert False, ("unknown type", type(obj))


def encode_arg(arg, with_ref):
    assert isinstance(arg, (list, set, tuple))
    return [encode(obj, with_ref=with_ref) for obj in arg]


def encode_positional_args(obj):
    positionals = [f for f in obj.__members__ if not isinstance(f, KWField)]
    encoded = []
    for field in positionals:
        encoded.append(encode(getattr(obj, field.name), with_ref=True))
    return encoded
    

def encode_keyword_args(obj):
    from sexpdata import Symbol
    keywords = [f for f in obj.__members__ if isinstance(f, KWField)]
    encoded = []
    for field in keywords:
        encoded.extend([Symbol(':' + field.name),
                        encode(getattr(obj, field.name), with_ref=True)])
    return encoded


def dumps(obj):
    import sexpdata
    return sexpdata.dumps(encode(obj))

