from typing import Generic, TypeVar, Type
from abc import abstractmethod
from pyvertb.comm import Transaction, Process, Input, Output
from pyvertb.types import Record


class Interface(Record):
    """ """


InterfaceType = TypeVar("InterfaceType", Interface, covariant=True)
TransactionType = TypeVar("TransactionType", Transaction, covariant=True)


class SynchDriver(Generic[InterfaceType, TransactionType]):
    """ """

    interface: Type[InterfaceType]

    @abstractmethod
    def drive(self, trans: TransactionType) -> None:
        """ """


class SynchMonitor(Generic[TransactionType]):
    """ """

    interface: Type[InterfaceType]

    @abstractmethod
    def monitor(self) -> TransactionType:
        """ """


class Driver(Process, Generic[InterfaceType, TransactionType]):
    """ """

    input: Input[TransactionType]
    interface: Type[InterfaceType]


class BasicDriver(Driver[InterfaceType, TransactionType]):
    """ """

    @property
    def interface(self) -> InterfaceType:
        return self._synch_driver.interface

    def __init__(
        self,
        synch_driver: SynchDriver[InterfaceType, TransactionType],
    ):
        super().__init__()
        self._synch_driver = synch_driver

    async def run(self):
        while True:
            trans = await self.input.recv()
            self._synch_driver.drive(trans)


class Monitor(Process, Generic[InterfaceType, TransactionType]):
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
