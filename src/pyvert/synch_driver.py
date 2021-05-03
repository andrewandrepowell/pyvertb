from typing import Generic, TypeVar, Type
from abc import ABC

from pyvert.comm import Transaction


InterfaceType = TypeVar("TransactionType", Transaction, covariant=True)
TransactionType = TypeVar("TransactionType", Transaction, covariant=True)


class SynchDriver(ABC, Generic[InterfaceType, TransactionType]):
    """ """

    interface: Type[InterfaceType]

    def drive(self, trans: TransactionType) -> None:
        """ """
