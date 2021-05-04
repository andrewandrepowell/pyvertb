from typing import Iterator, Union, TypeVar, Type, MutableSet, MutableSequence
from asyncio import QueueEmpty

from pyvertb.comm import Source, Sink
from pyvertb.util import MISSING, MissingType
import pyvertb.cocotb_compat as compat


T_co = TypeVar("T_co", covariant=True)


class IteratorSource(Source[T_co]):
    """ """

    def __init__(self, it: Iterator[T_co]):
        self._it = it
        self._lookahead: Union[MissingType, T_co] = MISSING

    def is_available(self) -> bool:
        if self._lookahead is not MISSING:
            return True
        try:
            self._lookahead = next(self._it)
        except StopIteration:
            return False
        return True

    async def available(self):
        if self.is_available():
            return
        await compat.Forever()

    def recv_nowait(self):
        if self._lookahead is not MISSING:
            res, self._lookahead = self._lookahead, MISSING
            return res
        try:
            return next(self._it)
        except StopIteration:
            raise QueueEmpty from None


class SequenceSink(Sink[T_co]):
    """ """

    def __init__(self, cls: Type[MutableSequence[T_co]]):
        self.value = cls()

    def send(self, value):
        self.value.append(value)


class SetSink(Sink[T_co]):
    """ """

    def __init__(self, cls: Type[MutableSet[T_co]]):
        self.value = cls()

    def send(self, value):
        self.value.add(value)


class NullSink(Sink[T_co]):
    """ """

    def send(self, value):
        pass
