from typing import Generic, TypeVar, Type
from abc import ABC

from pyvert.comm import Transaction


InterfaceType = TypeVar("TransactionType", Transaction, covariant=True)
TransactionType = TypeVar("TransactionType", Transaction, covariant=True)


class SynchMonitor(ABC, Generic[TransactionType]):
    """ """

    interface: Type[InterfaceType]

    def monitor(self) -> TransactionType:
        """ """
