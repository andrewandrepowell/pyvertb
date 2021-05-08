from typing import TypeVar
from pyvertb import SynchDriver, SynchMonitor, Driver, Monitor, Interface, Transaction


InterfaceType = TypeVar("InterfaceType", bound=Interface)
TransactionType = TypeVar("TransactionType", bound=Transaction)
InTransactionType = TypeVar("TransactionType", bound=Transaction)
OutTransactionType = TypeVar("TransactionType", bound=Transaction)


class BasicDriver(Driver[InterfaceType, InTransactionType, OutTransactionType]):
    """ """

    @property
    def interface(self) -> InterfaceType:
        return self._synch_driver.interface

    def __init__(
        self,
        synch_driver: SynchDriver[InterfaceType, InTransactionType, OutTransactionType],
    ):
        super().__init__()
        self._synch_driver = synch_driver

    async def run(self):
        while True:
            trans = await self.input.recv()
            self._synch_driver.drive(trans)


class BasicMonitor(Monitor[InterfaceType, TransactionType]):
    """ """

    @property
    def interface(self) -> InterfaceType:
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
