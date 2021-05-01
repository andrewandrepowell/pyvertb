from typing import Generic, TypeVar, Deque, Set, Optional, Iterator, Union
from abc import ABC, abstractmethod
from collections import deque
from asyncio import QueueEmpty

import cocotb
from cocotb.triggers import Event
from cocotb.decorators import RunningTask

from .types import Record


class Transaction(Record):
    """ """


class Process(ABC):
    """ """

    def __init__(self):
        super().__init__()
        self._task: Optional[RunningTask] = None

    def start(self) -> None:
        """ """
        if self._task is not None:
            raise RuntimeError("task already started")
        self._task = cocotb.fork(self.run())

    def stop(self) -> None:
        """ """
        if self._task is None:
            raise RuntimeError("task never started")
        self._task.kill()
        self._task = None

    @abstractmethod
    async def run(self) -> None:
        """ """


QueueEmpty = QueueEmpty


T = TypeVar("T")


class Sink(Generic[T]):
    """ """

    def send(self, value: T) -> None:
        """ """


class Source(Generic[T]):
    """ """

    def available(self) -> bool:
        """ """

    def recv_nowait(self) -> T:
        """ """

    async def wait(self) -> None:
        """ """

    async def recv(self) -> T:
        """ """

    def connect(self, inp: Sink[T]) -> None:
        """ """


class Input(Sink[T]):
    """ """

    def available(self) -> bool:
        """ """

    def recv_nowait(self) -> T:
        """ """

    async def wait(self) -> None:
        """ """

    async def recv(self) -> T:
        """ """


class Output(Source[T]):
    """ """

    def __init__(self):
        super().__init__()

    def send(self, value: T) -> None:
        """ """


class Sequence(Source[T]):
    """ """

    def __init__(self, it: Iterator[T]):
        super().__init__()
