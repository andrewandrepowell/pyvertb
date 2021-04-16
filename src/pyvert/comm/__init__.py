from typing import Optional, Generic, TypeVar, Deque, Set
from abc import ABC, abstractmethod
from collections import deque
from asyncio import QueueEmpty
import cocotb
from cocotb.triggers import Event


class Process(ABC):
    """
    """

    def __init__(self, name: Optional[str] = None):
        for name, typ in self.__annotations__.items():
            setattr(self, name, typ())
        self._task = None

    def start(self) -> None:
        """
        """
        if self._task is not None:
            raise RuntimeError("task already started")
        self._task = cocotb.fork(self.run())

    def stop(self) -> None:
        """
        """
        if self._task is None:
            raise RuntimeError("task never started")
        self._task.kill()
        self._task = None

    @abstractmethod
    async def run(self) -> None:
        """
        """


T = TypeVar('T')


class Input(Generic[T]):

    def __init__(self):
        self._deque: Deque[T] = deque()
        self._put_event = Event()

    def send(self, value: T) -> None:
        """
        """
        self._deque.append(value)
        self._put_event.set()

    def __bool__(self) -> bool:
        return bool(self._deque)

    def recv_nowait(self) -> T:
        """
        """
        if self:
            return self._deque.popleft()
        raise QueueEmpty

    async def wait(self) -> None:
        """
        """
        while not self:
            self._put_event.clear()
            await self._put_event.wait()

    async def recv(self) -> T:
        """
        """
        await self.wait()
        return self._deque.popleft()


class Output(Generic[T]):
    """
    """

    def __init__(self):
        self._connections: Set[Input[T]] = set()

    def send(self, value: T) -> None:
        """
        """
        for c in self._connections:
            c.send(value)

    def connect(self, inp: Input[T]) -> None:
        """
        """
        self._connections.add(inp)