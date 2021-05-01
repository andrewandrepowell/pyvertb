from typing import Generic, TypeVar, Type

from .process import Transaction, Process, Input
from .synch import SynchDriver


InterfaceType = TypeVar("TransactionType", Transaction, covariant=True)
TransactionType = TypeVar("TransactionType", Transaction, covariant=True)


class Driver(Process, Generic[InterfaceType, TransactionType]):
    """ """

    input: Input[TransactionType]
    interface: Type[InterfaceType]


class BasicDriver(Driver[InterfaceType, TransactionType]):
    """ """

    @property
    def interface(self) -> InterfaceType:
        return self._synch_driver.interface

    def __init__(self, synch_driver: SynchDriver[InterfaceType, TransactionType]):
        super().__init__()
        self.input = Input()
        self._synch_driver = synch_driver

    async def run(self):
        while True:
            trans = await self.input.recv()
            self._synch_driver.drive(trans)
