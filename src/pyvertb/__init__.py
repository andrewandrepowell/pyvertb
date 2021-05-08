from typing import (
    Generic,
    TypeVar,
    Optional,
    Iterator,
    Iterable,
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


T_co = TypeVar("T_co", covariant=True)


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
InTransactionType = TypeVar("TransactionType", bound=Transaction)
OutTransactionType = TypeVar("TransactionType", bound=Transaction)


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


class Scoreboard(Component):
    """ """

    def __init__(self):
        super().__init__()
        self._scorers: Set[Scorer] = set()

    def register_scorer(self, scorer: Scorer) -> None:
        """ """
        self._scorers.add(scorer)

    def deregister_scorer(self, scorer: Scorer) -> None:
        """ """
        self._scorers.remove(scorer)

    def scorers(self) -> Iterator[Scorer]:
        """ """
        return iter(self._scorers)


class Analyzer(Environment):
    """ """


class Stimulater(Environment):
    """ """
