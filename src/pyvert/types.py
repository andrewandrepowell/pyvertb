from dataclasses import dataclass, field


from cocotb.handle import (
    SimHandleBase,
    HierarchyObject,
    HierarchyArrayObject,
    NonHierarchyIndexableObject,
    ModifiableObject,
    IntegerObject,
    EnumObject,
    StringObject,
    RealObject,
)


Object = SimHandleBase
"""
"""

Scope = HierarchyObject
"""
"""

ScopeArray = HierarchyArrayObject
"""
"""

Logic = ModifiableObject
"""
"""

Array = NonHierarchyIndexableObject
"""
"""

Record = HierarchyObject
"""
"""

Integer = IntegerObject
"""
"""

Enum = EnumObject
"""
"""

String = StringObject
"""
"""

Real = RealObject
"""
"""


class _RecordMetaclass(type):

    def __new__(typ, name, bases, dict):
        cls = super().__new__(typ, name, bases, dict)
        return dataclass(unsafe_hash=True, frozen=True)(cls)


class Record(metaclass=_RecordMetaclass):
    """
    Base class for record types

    Use Python attribute typing anontations to declare fields
    """


field = field
