from typing import Set, Iterator

from pyvertb.communication import Component, Environment


class Analyzer(Environment):
    """ """


class Stimulater(Environment):
    """ """


class Scorer(Component):
    """ """


class Model(Component):
    """ """


class Scoreboard(Component):
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
