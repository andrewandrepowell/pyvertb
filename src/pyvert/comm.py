from typing import (
    Generic,
    TypeVar,
    Type,
    Optional,
    Union,
    Iterator,
    Iterable,
    Deque,
    MutableSequence,
    MutableSet,
    AsyncIterator,
)
from abc import ABC, abstractmethod
from collections import deque
from asyncio import QueueEmpty

import pyvert.cocotb_compat as compat
from pyvert.util import MISSING, MissingType


class Process(ABC):
    """ """

    def __init__(self):
        super().__init__()
        self._task: Optional[compat.Task] = None

    def start(self) -> None:
        """ """
        if self._task is not None:
            raise RuntimeError("task already started")
        self._task = compat.create_task(self.run())

    def stop(self) -> None:
        """ """
        if self._task is None:
            raise RuntimeError("task never started")
        compat.cancel_task(self._task)
        self._task = None

    @abstractmethod
    async def run(self) -> None:
        """ """


T = TypeVar("T")


class Sink(Generic[T]):
    """ """

    @abstractmethod
    def send(self, value: T) -> None:
        """ """


class Source(AsyncIterator[T]):
    """ """

    @abstractmethod
    def is_available(self) -> bool:
        """ """

    def __bool__(self) -> bool:
        return self.is_available()

    @abstractmethod
    async def available(self) -> None:
        """ """

    @abstractmethod
    def recv_nowait(self) -> T:
        """ """

    async def recv(self) -> T:
        """ """
        await self.available()
        return self.recv_nowait()

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        return await self.recv()


class Channel(Sink[T], Source[T]):
    """ """

    def __init__(self, init: Optional[Iterable[T]] = None):
        super().__init__()
        self._deque: Deque[T] = deque(init)
        self._send_event = compat.Event()

    def send(self, value):
        self._deque.append(value)
        self._send_event.set()

    def is_available(self):
        return bool(self._deque)

    async def available(self):
        while not self.is_available():
            self._send_event.clear()
            await self._send_event.wait()

    def recv_nowait(self):
        try:
            return self._deque.popleft()
        except IndexError:
            raise QueueEmpty from None


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


class SequenceSink(Sink[T]):
    """ """

    def __init__(self, cls: Type[MutableSequence[T]]):
        self.value = cls()

    def send(self, value):
        self.value.append(value)


class SetSink(Sink[T]):
    def __init__(self, cls: Type[MutableSet[T]]):
        self.value = cls()

    def send(self, value):
        self.value.add(value)


class NullSink(Sink[T]):
    def send(self, value):
        pass
