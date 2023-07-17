.DEFAULT_GOAL := test_pe_2

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = \
	$(shell pwd)/../../../rtl/posit/*.sv \
	$(shell pwd)/../../../rtl/decode/posit32_count_regime.sv \
	$(shell pwd)/../../../rtl/decode/util/*.sv \

SIM=verilator
EXTRA_ARGS += --trace
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

include $(shell cocotb-config --makefiles)/Makefile.sim

test_pe_2:
	rm -rf sim_build
	$(MAKE) sim MODULE=test_count_regime TOPLEVEL=posit32_regime_tb
