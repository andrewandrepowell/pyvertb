import typing

import cocotb
from cocotb.triggers import RisingEdge, Timer

import pyvertb.cocotb_compat as compat
from pyvertb import Interface, SynchDriver, Transaction


async def clock(clk, half_period):
    while True:
        clk.value = 1
        await half_period
        clk.value = 0
        await half_period


class FifoTransaction(Transaction):
    data: typing.Union[typing.Any, typing.Dict[str, typing.Any]]


class FifoInterface(Interface):
    clk: compat.LogicHandle
    ready: compat.LogicHandle
    valid: compat.LogicHandle
    data: typing.Union[compat.ObjectHandle, typing.Dict[str, compat.ObjectHandle]]


class FifoWrSynchDriver(SynchDriver[FifoInterface, FifoTransaction, None]):

    in_transaction_type = FifoTransaction
    out_transaction_type = None

    def __init__(self, interface):
        self.interface = interface
        self.interface.valid.setimmediate(0)

    async def drive(self, trans):
        pass


class FifoRdSynchDriver(SynchDriver[FifoInterface, None, FifoTransaction]):

    in_transaction_type = None
    out_transaction_type = FifoTransaction

    def __init__(self, interface):
        self.interface = interface
        self.interface.ready.setimmediate(0)

    async def drive(self, trans=None):
        pass


@cocotb.test()
async def test(_):
    cocotb.fork(clock(cocotb.top.clk, Timer(5, "ns")))
    cocotb.top.rst.value = 1
    cocotb.top.valid_in.value = 0
    cocotb.top.ready_in.value = 0
    await Timer(20, "ns")
    cocotb.top.rst.value = 0
    await RisingEdge(cocotb.top.clk)
