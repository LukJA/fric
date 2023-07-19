ifndef COCOTB_TOP
  $(error COCOTB_TOP (top level path) not set! Run verif/cocotb/setup.sh first)
endif

TOPLEVEL_LANG = verilog
VERILOG_SOURCES ?= $(shell find $(RTL_TOP) -type f -name '*.sv')

$(info $$VERILOG_SOURCES is [${VERILOG_SOURCES}])

COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

# sim can be overwritten if needed, add EXTRA_ARGS in the below if block
SIM ?= verilator

ifeq ($(SIM),verilator)
	EXTRA_ARGS += --trace --trace-structs --coverage
endif

include $(shell cocotb-config --makefiles)/Makefile.sim
