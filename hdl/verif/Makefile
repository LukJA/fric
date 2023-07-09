# SV COCO MakeFile
.DEFAULT_GOAL := testdff

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = ../rtl/*.sv

# Verilator
SIM=verilator
# EXTRA_ARGS += -Isv
# EXTRA_ARGS += --trace --trace-depth 5 --trace-structs --coverage
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

include tests/tests.mk

cocotb:
	rm -f -r out/$(TEST)
	$(MAKE) sim MODULE=$(MODULE_$(TEST)) TOPLEVEL=$(TOPLEVEL_$(TEST))

include $(shell cocotb-config --makefiles)/Makefile.sim
