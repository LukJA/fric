# SV COCO MakeFile
.DEFAULT_GOAL := testdff

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = 	$(shell pwd)/sv/*.sv

# Verilator
SIM=verilator
# EXTRA_ARGS += -Isv
# EXTRA_ARGS += --trace --trace-depth 5 --trace-structs --coverage
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

# Unit Test Targets
testdff: 
	rm -f -r sim_build
	$(MAKE) sim MODULE=test_dff TOPLEVEL=dff

testposit:
	rm -f -r sim_build
	$(MAKE) sim MODULE=test_posit_adder TOPLEVEL=posit_adder

testclz:
	rm -f -r sim_build
	$(MAKE) sim MODULE=test_clz TOPLEVEL=count_lead_zero

testclo:
	rm -f -r sim_build
	$(MAKE) sim MODULE=test_clo TOPLEVEL=count_lead_one

testffo:
	rm -f -r sim_build
	$(MAKE) sim MODULE=test_ffo TOPLEVEL=find_first_one

testffno:
	rm -f -r sim_build
	$(MAKE) sim MODULE=test_ffno TOPLEVEL=find_first_n_ones

testcl: testclo testclz

testdecoder:
	rm -f -r sim_build
	$(MAKE) sim MODULE=test_decoder TOPLEVEL=format_decoder

include $(shell cocotb-config --makefiles)/Makefile.sim

