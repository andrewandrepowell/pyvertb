from typing import Set, Iterator

from pyvert.comm import Process


class System:
    """ """

    def __init__(self):
        super().__init__()
        self._processes: Set[Process] = set()

    def register_process(self, process: Process) -> None:
        """ """
        self._processes.add(process)

    def deregister_process(self, process: Process) -> None:
        """ """
        self._processes.remove(process)

    def processes(self) -> Iterator[Process]:
        """ """
        return iter(self._processes)


class Analysis(System):
    """ """


class Stimulus(System):
    """ """
