from typing import (
    Generic,
    TypeVar,
    Optional,
    Iterator,
    Deque,
    AsyncIterator,
    Set,
    Type,
    Tuple,
)
from abc import ABC, abstractmethod
from collections import deque
from asyncio import QueueEmpty

import pyvertb.cocotb_compat as compat
from pyvertb.util import Record


T = TypeVar("T")


class Component(ABC):
    """ """

    @abstractmethod
    def start(self) -> None:
        """ """

    @abstractmethod
    def stop(self) -> None:
        """ """


class Process(Component):
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


class Module(Component):
    """ """

    def sub_components(self) -> Iterator[Tuple[str, Component]]:
        for name, obj in dir(self).items():
            if isinstance(obj, Component):
                yield name, obj

    def start(self) -> None:
        for _, c in self.sub_components():
            c.start()

    def stop(self) -> None:
        for _, c in self.sub_components():
            c.stop()


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


class Interface(Record):
    """ """


class Transaction(Record):
    """
    Base class for all transaction types.

    Transactions represent a single occurence of an observable "event".
    Transactions can represent anything; including, but not limited to:
    * An AXI Stream, List, or Full Transaction
    * An interrupt occuring
    * A change in state

    Transactions don't necessarily have to have associated data, but many do.
    For example, a transaction for an interupt occuring typically won't have
    associated data; but an AXI Full Transaction will contain a lot of data.
    """


InterfaceType = TypeVar("InterfaceType", bound=Interface)
TransactionType = TypeVar("TransactionType", bound=Transaction)
InTransactionType = TypeVar("InTransactionType", bound=Transaction)
OutTransactionType = TypeVar("OutTransactionType", bound=Transaction)


class SynchDriver(
    Component, Generic[InterfaceType, InTransactionType, OutTransactionType]
):
    """ """

    interface: InterfaceType
    in_transaction_type: Type[InTransactionType]
    out_transaction_type: Type[OutTransactionType]

    @abstractmethod
    def drive(self, trans: InTransactionType) -> OutTransactionType:
        """ """


class SynchMonitor(Component, Generic[InterfaceType, TransactionType]):
    """ """

    interface: InterfaceType
    transaction_type: Type[TransactionType]

    @abstractmethod
    def monitor(self) -> TransactionType:
        """ """


class Driver(Process, Generic[InterfaceType, InTransactionType, OutTransactionType]):
    """ """

    input: Source[InTransactionType]
    output: Sink[OutTransactionType]
    interface: Type[InterfaceType]


class Monitor(Process, Generic[InterfaceType, TransactionType]):
    """ """

    output: Sink[TransactionType]
    interface: InterfaceType


class Model(Process):
    """ """


class Scorer(Process):
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


class Analyzer(Module):
    """ """


class Stimulater(Module):
    """ """
