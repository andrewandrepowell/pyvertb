from typing import (
    Generic,
    TypeVar,
    Optional,
    Iterator,
    Deque,
    AsyncIterator,
    Set,
    Type,
)
from abc import ABC, abstractmethod
from collections import deque
from asyncio import QueueEmpty

import pyvertb.cocotb_compat as compat
from pyvertb.util import Record


T = TypeVar("T")


class Transaction(Record):
    """ """


class Component(ABC):
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


class Sink(Generic[T]):
    """ """

    @abstractmethod
    def send(self, value: T) -> None:
        """ """


class Channel(Sink[T], Source[T]):
    """ """

    def __init__(self):
        super().__init__()
        self._deque: Deque[T] = deque()
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


class Environment:
    """ """

    def __init__(self):
        super().__init__()
        self._processes: Set[Component] = set()

    def register_process(self, process: Component) -> None:
        """ """
        self._processes.add(process)

    def deregister_process(self, process: Component) -> None:
        """ """
        self._processes.remove(process)

    def processes(self) -> Iterator[Component]:
        """ """
        return iter(self._processes)


class Interface(Record):
    """ """


InterfaceType = TypeVar("InterfaceType", bound=Interface)
TransactionType = TypeVar("TransactionType", bound=Transaction)
InTransactionType = TypeVar("InTransactionType", bound=Transaction)
OutTransactionType = TypeVar("OutTransactionType", bound=Transaction)


class SynchDriver(Generic[InterfaceType, InTransactionType, OutTransactionType]):
    """ """

    interface: Type[InterfaceType]

    @abstractmethod
    def drive(self, trans: InTransactionType) -> OutTransactionType:
        """ """


class SynchMonitor(Generic[InterfaceType, TransactionType]):
    """ """

    interface: Type[InterfaceType]

    @abstractmethod
    def monitor(self) -> TransactionType:
        """ """


class Driver(Component, Generic[InterfaceType, InTransactionType, OutTransactionType]):
    """ """

    input: Source[InTransactionType]
    output: Sink[OutTransactionType]
    interface: Type[InterfaceType]


class Monitor(Component, Generic[InterfaceType, TransactionType]):
    """ """

    output: Sink[TransactionType]
    interface: InterfaceType


class Model(Component):
    """ """


class Scorer(Component):
    """ """


ScorerType = TypeVar("ScorerType")


class Scoreboard(Component, Generic[ScorerType]):
    """ """

    def __init__(self):
        super().__init__()
        self._scorers: Set[ScorerType] = set()

    def register_scorer(self, scorer: ScorerType) -> None:
        """ """
        self._scorers.add(scorer)

    def deregister_scorer(self, scorer: ScorerType) -> None:
        """ """
        self._scorers.remove(scorer)

    def scorers(self) -> Iterator[ScorerType]:
        """ """
        return iter(self._scorers)


class Analyzer(Environment):
    """ """


class Stimulater(Environment):
    """ """
