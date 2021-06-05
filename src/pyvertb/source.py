from asyncio import QueueEmpty
from typing import Iterator, TypeVar, Union

import pyvertb.cocotb_compat as compat
from pyvertb import Source
from pyvertb.util import MISSING, MissingType

T = TypeVar("T")


class IteratorSource(Source[T]):
    """ """

    def __init__(self, it: Iterator[T]):
        self._it = it
        self._lookahead: Union[MissingType, T] = MISSING

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
