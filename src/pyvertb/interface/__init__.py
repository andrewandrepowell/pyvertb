from typing import Generic, TypeVar, Type
from abc import abstractmethod
from pyvertb.communication import Transaction, Component, Input, Output
from pyvertb.util import Record


class Interface(Record):
    """ """


InterfaceType = TypeVar("InterfaceType", bound=Interface)
TransactionType = TypeVar("TransactionType", bound=Transaction)
InTransactionType = TypeVar("TransactionType", bound=Transaction)
OutTransactionType = TypeVar("TransactionType", bound=Transaction)


class SynchDriver(Generic[InterfaceType, InTransactionType, OutTransactionType]):
    """ """

    interface: Type[InterfaceType]

    @abstractmethod
    def drive(self, trans: InTransactionType) -> OutTransactionType:
        """ """


class SynchMonitor(Generic[InterfaceType, TransactionType]):
    """ """

    interface: Type[InterfaceType]

    @abstractmethod
    def monitor(self) -> TransactionType:
        """ """


class Driver(Component, Generic[InterfaceType, InTransactionType, OutTransactionType]):
    """ """

    input: Input[InTransactionType]
    output: Output[OutTransactionType]
    interface: Type[InterfaceType]


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


class Monitor(Component, Generic[InterfaceType, TransactionType]):
    """ """

    output: Output[TransactionType]
    interface: InterfaceType


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
