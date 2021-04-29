from typing import Generic, TypeVar

from .process import Transaction, Process, Output
from .synch import SynchMonitor


TransactionType = TypeVar('TransactionType', Transaction, covariant=True)


class Monitor(Process, Generic[TransactionType]):
    """
    """
    output: Output[TransactionType]


class BasicMonitor(Monitor[TransactionType]):
    """
    """

    def __init__(self, synch_monitor: SynchMonitor[TransactionType]):
        super().__init__()
        self.output = Output()
        self._synch_monitor = synch_monitor

    async def run(self):
        while True:
            trans = await self._synch_monitor.monitor()
            self.output.send(trans)
