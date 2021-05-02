from typing import Set, Iterator

from pyvert.comm import Process
from pyvert.scorer import Scorer


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


class MatchScoreboard(Scoreboard):
    """ """

    def is_passing(self) -> bool:
        return all(scorer.mismatched == 0 for scorer in self.scorers())

    async def run(self):
        # we don't need to do any aggregation here
        pass
