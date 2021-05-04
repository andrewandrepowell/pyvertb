from typing import (
    Generic,
    TypeVar,
    Optional,
    Iterator,
    Iterable,
    Deque,
    AsyncIterator,
    Set,
)
from abc import ABC, abstractmethod
from collections import deque
from asyncio import QueueEmpty

import pyvert.cocotb_compat as compat
from pyvert.util import Record


class Transaction(Record):
    """
    Base class for a Transaction types.

    Transactions represents an atomic change in state in a system.


    Usage:
    .. code-block:: python3

    """


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


T_co = TypeVar("T_co", covariant=True)


class Source(AsyncIterator[T_co]):
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
    def recv_nowait(self) -> T_co:
        """ """

    async def recv(self) -> T_co:
        """ """
        await self.available()
        return self.recv_nowait()

    def __aiter__(self) -> AsyncIterator[T_co]:
        return self

    async def __anext__(self) -> T_co:
        return await self.recv()


class Sink(Generic[T_co]):
    """ """

    @abstractmethod
    def send(self, value: T_co) -> None:
        """ """


class Input(Source[T_co]):
    """ """

    def __init__(self, source: Optional[Source[T_co]] = None):
        self._source = source

    def connect(self, source: Source[T_co]) -> None:
        if self._source is not None:
            raise ConnectionError("Already connected")
        self._source = source

    def disconnect(self) -> Source[T_co]:
        if self._source is None:
            raise ConnectionError("Never connected")
        res, self._source = self._source, None
        return res

    def is_available(self):
        if self._source is None:
            raise ConnectionError("Never connected")
        return self._source.is_available()

    async def available(self):
        if self._source is None:
            raise ConnectionError("Never connected")
        await self._source.available()

    def recv_nowait(self):
        if self._source is None:
            raise ConnectionError("Never connected")
        return self._source.recv_nowait()


class Output(Sink[T_co]):
    """ """

    def __init__(self, sink: Optional[Sink[T_co]] = None):
        self._sink = sink

    def connect(self, sink: Sink[T_co]) -> None:
        if self._sink is not None:
            raise ConnectionError("Already connected")
        self._sink = sink

    def disconnect(self) -> Sink[T_co]:
        if self._sink is None:
            raise ConnectionError("Never connected")
        res, self._sink = self._sink, None
        return res

    def send(self, value):
        if self._sink is None:
            raise ConnectionError("Never connected")
        self._source.send(value)


class Channel(Sink[T_co], Source[T_co]):
    """ """

    def __init__(self, init: Optional[Iterable[T_co]] = None):
        super().__init__()
        self._deque: Deque[T_co] = deque(init)
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


def connect(source: Output[T_co], sink: Input[T_co]) -> None:
    """ """
    c = Channel[T_co]()
    source.connect(c)
    sink.connect(c)


class System:
    """ """

    def __init__(self):
        super().__init__()
        self._processes: Set[Process] = set()

    def register_process(self, process: Process) -> None:
        """ """
        self._processes.add(process)

    def deregister_process(self, process: Process) -> None:
        """ """
        self._processes.remove(process)

    def processes(self) -> Iterator[Process]:
        """ """
        return iter(self._processes)
