#!/usr/bin/python3
from command import *

class TypeCommand(Command):
    def resolve_name(self, base, idxs):
        assert len(idxs) == 0, (base, idxs)
        return base

    def resolve_type(self, idxs):
        assert len(idxs) == 0, (idxs, )
        return self

class TypePointer(TypeCommand):
    elemType = Field()

    def resolve_name(self, base, idxs):
        if not idxs: return base
        if idxs[0][0] == 0:
            base = '(*%s)' % (base, )
        else:
            base = '%s[%s]' % (base, idxs[0][1])
        return self.elemType.resolve_name(base, idxs[1:])

    def resolve_type(self, idxs):
        if not idxs: return self
        return self.elemType.resolve_type(idxs[1:])

    def type_size(self):
        return 8


class TypeArray(TypeCommand):
    elemType = Field()
    size = Field()

    def resolve_name(self, base, idxs):
        if not idxs: return base
        base = '%s[%s]' % (base, idxs[0][1])
        return self.elemType.resolve_name(base, idxs[1:])

    def resolve_type(self, idxs):
        if not idxs: return self
        return self.elemType.resolve_type(idxs[1:])

    def type_size(self):
        return self.elemType.type_size() * self.size


class TypeInt(TypeCommand):
    width = Field()

    def type_size(self):
        return self.width // 8

class TypeFloat(TypeCommand):
    width = Field()

    def type_size(self):
        return self.width // 8

class TypeDouble(TypeCommand):
    width = Field()

    def type_size(self):
        return self.width // 16


class TypeStruct(TypeCommand):
    name = Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.name)
        self.layout = DefTypeStruct.find(self.name)
        self.composite_type = CompositeType.find(self.dbg_name)

    @property
    def dbg_name(self):
        idx = self.name.find('.')
        if idx >= 0:
            return self.name[idx+1:]
        return self.name

    def resolve_name(self, base, idxs):
        if not idxs: return base
        member = self.composite_type.members[idxs[0][0]]
        base = '%s.%s' % (base, member.mname)
        return member.mtype.resolve_name(base, idxs[1:])

    def resolve_type(self, idxs):
        if not idxs: return self
        member = self.composite_type.members[idxs[0][0]]
        return member.mtype.resolve_type(idxs[1:])

    def members(self):
        return self.layout.members 


class StructCommand(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        type(self)._instances_.append(self)

    @classmethod
    def find(cls, name):
        for i in cls._instances_:
            if i.name == name:
                return i
        raise ValueError(name + ' not found')


class DefTypeStruct(StructCommand): 
    _instances_ = []
    name = Field()
    members = MultiField()


class DefTypeStructMember(Command):
    type = Field()
    offset = Field()


class TypeVoid(Command):
    pass


class CompositeType(StructCommand):
    _instances_ = []
    name = Field()
    members = MultiField()


class CompositeMember(Command):
    name = Field()
    type = Field()
