# SV COCO MakeFile
.DEFAULT_GOAL := testdff

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = 	$(shell pwd)/sv/*.sv 

# Verilator
SIM=verilator
EXTRA_ARGS += --trace-fst --trace-structs --coverage
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

# Unit Test Targets
testdff:
	$(MAKE) sim MODULE=test_dff TOPLEVEL=dff

testposit:
	$(MAKE) sim MODULE=test_posit_adder TOPLEVEL=posit_adder

include $(shell cocotb-config --makefiles)/Makefile.sim

