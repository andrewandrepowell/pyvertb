from typing import MutableSequence, MutableSet, Type, TypeVar

from pyvertb import Sink

T = TypeVar("T")


class SequenceSink(Sink[T]):
    """ """

    def __init__(self, cls: Type[MutableSequence[T]]):
        self.value = cls()

    def send(self, value):
        self.value.append(value)


class SetSink(Sink[T]):
    """ """

    def __init__(self, cls: Type[MutableSet[T]]):
        self.value = cls()

    def send(self, value):
        self.value.add(value)


class NullSink(Sink[T]):
    """ """

    def send(self, value):
        pass
