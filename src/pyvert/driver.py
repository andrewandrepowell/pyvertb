from typing import Generic, TypeVar

from .process import Transaction, Process, Input
from .synch import SynchDriver


TransactionType = TypeVar('TransactionType', Transaction, covariant=True)


class Driver(Process, Generic[TransactionType]):
    """
    """
    input: Input[TransactionType]


class BasicDriver(Driver[TransactionType]):
    """
    """

    def __init__(self, synch_driver: SynchDriver[TransactionType]):
        super().__init__()
        self.input = Input()
        self._synch_driver = synch_driver

    async def run(self):
        while True:
            trans = await self.input.recv()
            self._synch_driver.drive(trans)
