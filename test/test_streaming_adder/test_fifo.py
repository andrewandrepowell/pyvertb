import cocotb
from cocotb.triggers import Timer, RisingEdge


async def clock(clk, half_period):
    while True:
        clk.value = 1
        await half_period
        clk.value = 0
        await half_period


@cocotb.test()
async def test(_):
    cocotb.fork(clock(cocotb.top.clk, Timer(5, "ns")))
    cocotb.top.rst.value = 1
    cocotb.top.valid_in.value = 0
    cocotb.top.ready_in.value = 0
    await Timer(20, "ns")
    cocotb.top.rst.value = 0
    await RisingEdge(cocotb.top.clk)
    # write in
    await RisingEdge(cocotb.top.clk)
    cocotb.top.valid_in.value = 1
    for i in range(8):
        assert cocotb.top.ready_out.value == 1
        cocotb.top.data_in.value = i
        await RisingEdge(cocotb.top.clk)
    cocotb.top.valid_in.value = 0
    # ensure full
    await RisingEdge(cocotb.top.clk)
    assert cocotb.top.ready_out.value == 0
    # read out
    await RisingEdge(cocotb.top.clk)
    cocotb.top.ready_in.value = 1
    for i in range(8):
        assert cocotb.top.valid_out.value == 1
        await RisingEdge(cocotb.top.clk)
        assert cocotb.top.data_out.value == i
    cocotb.top.ready_in.value = 0
    # ensure empty
    await RisingEdge(cocotb.top.clk)
    assert cocotb.top.valid_out.value == 0
