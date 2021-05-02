from typing import Generic, TypeVar, Type

from pyvert.comm import Transaction, Process, Sink
from pyvert.synch import SynchDriver
from pyvert.interface import Interface


InterfaceType = TypeVar("InterfaceType", Interface, covariant=True)
TransactionType = TypeVar("TransactionType", Transaction, covariant=True)


class Driver(Process, Generic[InterfaceType, TransactionType]):
    """ """

    input: Sink[TransactionType]
    interface: Type[InterfaceType]


class BasicDriver(Driver[InterfaceType, TransactionType]):
    """ """

    @property
    def interface(self) -> InterfaceType:
        return self._synch_driver.interface

    def __init__(
        self,
        input: Sink[TransactionType],
        synch_driver: SynchDriver[InterfaceType, TransactionType],
    ):
        super().__init__()
        self.input = input
        self._synch_driver = synch_driver

    async def run(self):
        while True:
            trans = await self.input.recv()
            self._synch_driver.drive(trans)
