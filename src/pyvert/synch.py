from typing import Generic, TypeVar
from abc import ABC

from .process import Transaction


TransactionType = TypeVar('TransactionType', Transaction, covariant=True)


class SynchDriver(ABC, Generic[TransactionType]):
    """
    """

    def drive(self, trans: TransactionType) -> None:
        """
        """


class SynchMonitor(ABC, Generic[TransactionType]):
    """
    """

    def monitor(self) -> TransactionType:
        """
        """
