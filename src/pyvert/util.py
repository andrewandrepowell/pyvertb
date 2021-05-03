from typing import TypeVar, Optional
from dataclasses import dataclass, field
import sys


T = TypeVar('T')


def public(api: T, name: Optional[str] = None) -> T:
    if name is None:
        name = api.__name__
    sys.modules[api.__module__].__all__.append(name)
    return api


public(public)


class _RecordMetaclass(type):
    def __new__(typ, name, bases, dict):
        cls = super().__new__(typ, name, bases, dict)
        # hashability is necessary for records, frozen is necessary for hashability
        return dataclass(unsafe_hash=True, frozen=True)(cls)


@public
class Record(metaclass=_RecordMetaclass):
    """
    Base class for record types

    Use Python attribute typing annotations to declare fields.
    Or use :func:`dataclasses.field` if you have more advanced needs.
    """


field = public(field, 'field')


@public
class MissingType:
    """Type of singleton MISSING"""

    def __repr__(self):
        return "MISSING"


MISSING = public(MissingType(), 'MISSING')
"""Use in place :value:`None` as an invalid value where :value:`None` is a valid value"""
