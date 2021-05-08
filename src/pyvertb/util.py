from dataclasses import dataclass, field


class _RecordMetaclass(type):
    def __new__(typ, name, bases, dict):
        cls = super().__new__(typ, name, bases, dict)
        # hashability is necessary for records, frozen is necessary for hashability
        return dataclass(unsafe_hash=True, frozen=True)(cls)


class Record(metaclass=_RecordMetaclass):
    """
    Base class for record types

    Use Python attribute typing annotations to declare fields.
    Or use :func:`dataclasses.field` if you have more advanced needs.
    """


field = field


class MissingType:
    """Type of singleton MISSING"""

    def __repr__(self):
        return "MISSING"


MISSING = MissingType()
"""Use in place :value:`None` as an invalid value when :value:`None` is a valid value"""
