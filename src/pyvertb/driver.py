from typing import TypeVar

from pyvertb import Driver, Interface, SynchDriver, Transaction

InterfaceType = TypeVar("InterfaceType", bound=Interface)
InTransactionType = TypeVar("InTransactionType", bound=Transaction)
OutTransactionType = TypeVar("OutTransactionType", bound=Transaction)


class BasicDriver(Driver[InterfaceType, InTransactionType, OutTransactionType]):
    """ """

    @property
    def interface(self):
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
