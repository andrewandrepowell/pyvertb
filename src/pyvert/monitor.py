from typing import Generic, TypeVar

from pyvert.comm import Transaction, Process, Source
from pyvert.interface import Interface
from pyvert.synch import SynchMonitor


InterfaceType = TypeVar("InterfaceType", Interface, covariant=True)
TransactionType = TypeVar("TransactionType", Transaction, covariant=True)


class Monitor(Process, Generic[InterfaceType, TransactionType]):
    """ """

    output: Source[TransactionType]
    interface: InterfaceType


class BasicMonitor(Monitor[InterfaceType, TransactionType]):
    """ """

    @property
    def output(self) -> Source[TransactionType]:
        return self._output

    @property
    def interface(self) -> InterfaceType:
        return self._synch_monitor.interface

    def __init__(
        self,
        output: Source[TransactionType],
        synch_monitor: SynchMonitor[InterfaceType, TransactionType],
    ):
        super().__init__()
        self._output = output
        self._synch_monitor = synch_monitor

    async def run(self):
        while True:
            trans = await self._synch_monitor.monitor()
            self._output.send(trans)
