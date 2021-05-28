from typing import Callable, Awaitable
from pyvertb import Process, Module


def process(func: Callable[[None], Awaitable[None]]) -> Process:
    """ """

    class _(Process):
        run = func

    return _()


def module(func: Callable[[Module], None]) -> Module:
    """ """
    m = Module()
    func(m)
    return m
