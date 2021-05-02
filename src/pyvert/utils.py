from dataclasses import dataclass, field


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


class MissingType:
    """Type of singleton MISSING"""

    def __repr__(self):
        return "MISSING"


MISSING = MissingType()
