import cocotb
import pytest
from cocotbext_ver.comm import Process, Input, Output, QueueEmpty


@cocotb.test()
async def test_comm(_):

    class MyProcess(Process):
        a: Input[str]
        b: Output[int]

        async def run(self):
            while True:
                val = await self.a.recv()
                self.b.send(int(val))

    p = MyProcess()
    k = Input()
    p.b.connect(k)

    p.start()
    with pytest.raises(RuntimeError):
        p.start()

    with pytest.raises(QueueEmpty):
        k.recv_nowait()

    p.a.send("1")
    assert await k.recv() == 1

    p.a.send("123567")
    await k.wait()
    assert k.recv_nowait() == 123567

    p.stop()
    with pytest.raises(RuntimeError):
        p.stop()
