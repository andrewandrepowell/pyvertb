from typing import TypeVar

from pyvertb import Interface, Monitor, SynchMonitor, Transaction

InterfaceType = TypeVar("InterfaceType", bound=Interface)
TransactionType = TypeVar("TransactionType", bound=Transaction)


class BasicMonitor(Monitor[InterfaceType, TransactionType]):
    """ """

    @property
    def interface(self):
        return self._synch_monitor.interface

    def __init__(
        self,
        synch_monitor: SynchMonitor[InterfaceType, TransactionType],
    ):
        super().__init__()
        self._synch_monitor = synch_monitor

    async def run(self):
        while True:
            trans = await self._synch_monitor.monitor()
            self._output.send(trans)
