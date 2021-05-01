from typing import Generic, TypeVar, Type

from .process import Transaction, Process, Output
from .synch import SynchMonitor


InterfaceType = TypeVar("TransactionType", Transaction, covariant=True)
TransactionType = TypeVar("TransactionType", Transaction, covariant=True)


class Monitor(Process, Generic[InterfaceType, TransactionType]):
    """ """

    output: Output[TransactionType]
    interface: Type[InterfaceType]


class BasicMonitor(Monitor[InterfaceType, TransactionType]):
    """ """

    @property
    def interface(self) -> InterfaceType:
        return self._synch_monitor.interface

    def __init__(self, synch_monitor: SynchMonitor[InterfaceType, TransactionType]):
        super().__init__()
        self.output = Output()
        self._synch_monitor = synch_monitor

    async def run(self):
        while True:
            trans = await self._synch_monitor.monitor()
            self.output.send(trans)
