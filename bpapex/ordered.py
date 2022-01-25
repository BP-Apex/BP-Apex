#!/usr/bin/python3
from collections import OrderedDict, MutableSet


class OrderedSet(OrderedDict, MutableSet):
    def __init__(self, *iterables):
        super(OrderedSet, self).__init__()
        self.update(*iterables)

    def update(self, *args, **kwargs):
        if kwargs:
            raise TypeError("update() takes no keyword arguments")
        for s in args:
            for e in s:
                self.add(e)

    def add(self, elem):
        self[elem] = None

    def discard(self, elem):
        self.pop(elem, None)

    def __le__(self, other):
        return all(e in other for e in self)

    def __lt__(self, other):
        return self <= other and self != other

    def __ge__(self, other):
        return all(e in self for e in other)

    def __gt__(self, other):
        return self >= other and self != other

    def __repr__(self):
        return 'OrderedSet([%s])' % (', '.join(map(repr, self.keys())))

    def __str__(self):
        return '{%s}' % (', '.join(map(repr, self.keys())))

    difference = property(lambda self: self.__sub__)
    difference_update = property(lambda self: self.__isub__)
    intersection = property(lambda self: self.__and__)
    intersection_update = property(lambda self: self.__iand__)
    issubset = property(lambda self: self.__le__)
    issuperset = property(lambda self: self.__ge__)
    symmetric_difference = property(lambda self: self.__xor__)
    symmetric_difference_update = property(lambda self: self.__ixor__)
    union = property(lambda self: self.__or__)


class OrderedNamespace(object):
    def __init__(self):
        super(OrderedNamespace, self).__setattr__('_odict', OrderedDict())

    def __getattr__(self, key):
        odict = super(OrderedNamespace, self).__getattribute__('_odict')
        if key in odict:
            return odict[key]
        return super(OrderedNamespace, self).__getattribute__(key)

    def __setattr__(self, key, val):
        self._odict[key] = val

    def __hasattr__(self, key):
        return key in self._odict

    def __delattr__(self, key):
        del self._odict[key]

    @property
    def __dict__(self):
        return self._odict
