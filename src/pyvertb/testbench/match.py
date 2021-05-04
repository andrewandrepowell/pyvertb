from typing import TypeVar, Generic, Set
import operator

from pyvertb.communication import Transaction, Source
from pyvertb.testbench import Scorer, Scoreboard
import pyvertb.cocotb_compat as compat


TransactionType = TypeVar("TransactionType", bound=Transaction)


class Matcher(Scorer, Generic[TransactionType]):
    """ """

    expected: Source[TransactionType]
    actual: Source[TransactionType]
    total: int
    mismatched: int
    matched: int
    match_event: compat.Event

    match = operator.eq
    """ """


class OrderedMatcher(Matcher[TransactionType]):
    """ """

    def __init__(
        self, expected: Source[TransactionType], actual: Source[TransactionType]
    ):
        self.expected = expected
        self.actual = actual
        self.mismatched = 0
        self.matched = 0
        self.match_event = compat.Event()

    @property
    def total(self):
        return self.matched + self.mismatched

    async def run(self):
        while True:
            async for actual, expected in compat.azip(self.actual, self.expected):
                if self.match(actual, expected):
                    self.matched += 1
                else:
                    self.mismatched += 1
                self.match_event.set()


class UnorderedMatcher(Matcher[TransactionType]):
    """ """

    def __init__(
        self, expected: Source[TransactionType], actual: Source[TransactionType]
    ):
        self.expected = expected
        self.actual = actual
        self.matched = 0
        self.match_event = compat.Event()
        self._expected_queue: Set[TransactionType] = set()
        self._actual_queue: Set[TransactionType] = set()

    @property
    def total(self):
        return self.matched + self.mismatched

    @property
    def mismatched(self):
        return max(len(self._expected_queue), len(self._actual_queue))

    async def run(self):
        while True:
            which = await compat.select(
                (self.expected.available(), self.actual.available())
            )
            if which == 0:
                self._expected_queue.add(self.expected.recv_nowait())
            else:
                self._actual_queue.add(self.actual.recv_nowait())
            if self.match is operator.eq:
                common = self._actual_queue & self._expected_queue
            else:
                common: Set[TransactionType] = set()
                for actual in self._actual_queue:
                    for expected in self._expected_queue:
                        if self.match(actual, expected):
                            common.add(actual)
            self.matched += len(common)
            self._actual_queue -= common
            self._expected_queue -= common
            self.match_event.set()


class MatchScoreboard(Scoreboard):
    """ """

    def is_passing(self) -> bool:
        return all(scorer.mismatched == 0 for scorer in self.scorers())

    async def run(self):
        # we don't need to do any aggregation here
        pass
