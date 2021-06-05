from abc import ABC, abstractmethod
from asyncio import QueueEmpty, QueueFull
from collections import deque
from typing import (AsyncIterator, Deque, Generic, Iterator, Optional, Set,
                    Tuple, Type, TypeVar)

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


class ReceiveFailed(QueueEmpty):
    """ """


class SendFailed(QueueFull):
    """ """


class Source(AsyncIterator[T]):
    """ """

    @abstractmethod
    def recv_is_ready(self) -> bool:
        """ """

    @abstractmethod
    async def recv_ready(self) -> None:
        """ """

    @abstractmethod
    def try_recv(self) -> T:
        """ """
        if self.recv_is_ready():
            return self._recv()
        raise ReceiveFailed

    async def recv(self) -> T:
        """ """
        await self.recv_ready()
        return self._recv()

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        return await self.recv()


class Sink(Generic[T]):
    """ """

    @abstractmethod
    def send_is_ready(self) -> bool:
        """ """

    @abstractmethod
    async def send_ready(self) -> None:
        """ """

    @abstractmethod
    def _send(self, value: T) -> None:
        """ """

    def try_send(self, value: T) -> None:
        """ """
        if self.send_is_ready():
            self._send(value)
        raise SendFailed

    async def send(self, value: T):
        """ """
        await self.send_ready()
        self._send(value)


class Channel(Sink[T], Source[T]):
    """ """

    def __init__(self, *, depth: int = 0):
        super().__init__()
        self._deque: Deque[T] = deque()
        self._send_event = compat.Event()

    def recv_is_ready(self) -> bool:
        return len(self._deque) != 0

    async def recv_ready(self) -> None:
        while not self.recv_is_ready():
            self._send_event.clear()
            await self._send_event.wait()

    def _recv(self) -> T:
        return self._deque.popleft()

    def send_is_ready(self) -> bool:
        return True

    async def send_ready(self) -> None:
        return

    def _send(self, value: T) -> None:
        self._deque.append(value)
        self._send_event.set()


class Signal(Sink[T], Source[T]):
    """ """

    def __init__(self):
        self._value: Optional[T] = None
        self._send_event = compat.Event()
        self._recv_event = compat.Event()

    def recv_is_ready(self) -> bool:
        return self._send_event.is_set()

    async def recv_ready(self) -> None:
        while not self.recv_is_ready():
            self._send_event.clear()
            await self._send_event.wait()

    def try_recv(self) -> T:
        if self.recv_is_ready():
            self._recv_event.set()
            return self._value
        raise ReceiveFailed

    async def recv(self) -> T:
        await self.recv_ready()
        self._recv_event.set()
        self._send_event.clear()
        return self._value

    def send_is_ready(self) -> bool:
        return self._recv_event.is_set()

    async def send_ready(self) -> None:
        while not self.send_is_ready():
            self._recv_event.clear()
            await self._recv_event.wait()

    def try_send(self, value: T) -> None:
        if self.recv_is_ready():
            self._value = value
            self._send_event.set()
            return
        raise SendFailed

    async def send(self, value: T) -> None:
        await self.send_is_ready()
        self._value = value
        self._send_event.set()
        self._recv_event.clear()


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
