from typing import (
    Coroutine,
    Any,
    TypeVar,
    AsyncIterable,
    AsyncIterator,
    List,
    Awaitable,
    Tuple,
)

from asyncio import CancelledError, InvalidStateError

from cocotb.handle import (
    SimHandleBase,
    HierarchyObject,
    HierarchyArrayObject,
    NonHierarchyIndexableObject,
    ModifiableObject,
    IntegerObject,
    EnumObject,
    StringObject,
    RealObject,
)
from cocotb import fork
from cocotb.triggers import PythonTrigger, Event, First
from cocotb.decorators import RunningTask
import cocotb.outcomes


T = TypeVar("T")


Object = SimHandleBase
"""
"""

Scope = HierarchyObject
"""
"""

ScopeArray = HierarchyArrayObject
"""
"""

Logic = ModifiableObject
"""
"""

Array = NonHierarchyIndexableObject
"""
"""

Record = HierarchyObject
"""
"""

Integer = IntegerObject
"""
"""

Enum = EnumObject
"""
"""

String = StringObject
"""
"""

Real = RealObject
"""
"""


class Forever(PythonTrigger):
    """ """

    def prime(self, callback):
        super().prime()
        # do nothing, let it hang


Task = RunningTask
"""
"""


def create_task(coro: Coroutine) -> Task:
    """ """
    return cocotb.fork(coro)


def cancel_task(task: Task) -> None:
    """ """
    task.kill()


def task_is_done(task: Task) -> None:
    """ """
    return task._finished


def task_was_canceled(task: Task) -> bool:
    """ """
    if not task._finished:
        return False
    try:
        task.retval
    except CancelledError:
        return True
    return False


def task_result(task: Task) -> Any:
    """ """
    if not task._finished:
        raise InvalidStateError
    return task.retval


Event = Event
"""
"""


def aiter(aiterable: AsyncIterable[T]) -> AsyncIterator[T]:
    return aiterable.__aiter__()


async def anext(aiterator: AsyncIterator[T]) -> T:
    return await aiterator.__anext__()


async def azip(*aiterables: AsyncIterable[T]) -> AsyncIterable[List[T]]:
    aiterators = [aiter(ait) for ait in aiterables]
    while True:
        yield [await anext(ait) for ait in aiterators]


async def select(*awaitables: Awaitable[T]) -> Tuple[int, T]:
    async def waiter(idx: int, awaitable: Awaitable) -> Tuple[int, T]:
        return idx, await awaitable

    wait_tasks = [fork(waiter(i, aw)) for i, aw in enumerate(awaitables)]
    idx, res = await First(wait_tasks)
    for wait_task in wait_tasks:
        wait_task.kill()
    return idx, res
