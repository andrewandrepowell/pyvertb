from typing import Set, Iterator

from pyvertb.comm import Process, System


class Analysis(System):
    """ """


class Stimulus(System):
    """ """


class Scorer(Process):
    """ """


class Model(Process):
    """ """


class Scoreboard(Process):
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
