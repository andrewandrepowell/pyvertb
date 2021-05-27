SOURCES := fifo_top.vhd fifo.vhd util.vhd
TOPLEVEL := fifo_top
MODULE := test_fifo
COMMON_ARGS := --std=08
COCOTB_ARGS := --vpi=$(shell cocotb-config --lib-name-path vpi ghdl)
RUN_ARGS := --vcd=output.vcd


all:
	ghdl -i $(COMMON_ARGS) $(SOURCES)
	ghdl -m $(COMMON_ARGS) $(TOPLEVEL)
	MODULE=$(MODULE) TOPLEVEL=$(TOPLEVEL) COCOTB_REDUCED_LOG_FMT=1 \
	ghdl -r $(COMMON_ARGS) $(TOPLEVEL) $(COCOTB_ARGS) $(RUN_ARGS)


clean::
	ghdl remove
	@rm -f output.vcd
	@rm -f results.xml
