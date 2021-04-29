from typing import Set, Iterator

from .process import Process


class System:
    """
    """

    def __init__(self):
        self._processes: Set[Process]

    def register_process(self, p: Process) -> None:
        """
        """
        self._processes.add(p)

    def deregister_process(self, p: Process) -> None:
        """
        """
        self._processes.remove(p)

    def processes(self) -> Iterator[Process]:
        """
        """
        return iter(self._processes)
