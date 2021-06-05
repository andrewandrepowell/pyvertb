from typing import Awaitable, Callable

from pyvertb import Module, Process


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
