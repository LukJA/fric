# SV COCO MakeFile
.DEFAULT_GOAL := testdff

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(shell pwd)/../rtl/*.sv

# Verilator
SIM=verilator
# EXTRA_ARGS += -Isv
# EXTRA_ARGS += --trace --trace-depth 5 --trace-structs --coverage
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

include $(shell cocotb-config --makefiles)/Makefile.sim
include tests.mk

cocotb:
	# in theory this supports multiple modules running on a single toplevel
	# doing this with the tests.mk system is harder but perhaps the best way
	# is to use a more complex make import system with subdirectories per
	# toplevel
	#
	# e.g. TOPLEVEL_1 has a TL_1 subdirectory which contains:
	#  - a makefile which imports boilerplate
	#  - all the test_xxx.py files for that toplevel
	# then TOPLEVEL_2 has the same in TL_2
	# and in the parent there's some config.mk etc to import
	
	rm -f -r sim_build
	$(MAKE) sim MODULE=$(MODULE_$(TEST)) TOPLEVEL=$(TOPLEVEL_$(TEST))
