# SV COCO MakeFile

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(shell pwd)/dff.sv
TOPLEVEL = signed_add
MODULE = test_dff

# Verilator
SIM=verilator
EXTRA_ARGS += --trace-fst --trace-structs --coverage

include $(shell cocotb-config --makefiles)/Makefile.sim

