export COCOTB_TOP=$( cd $(dirname -- "$0") && pwd -P )
echo COCOTB_TOP: $COCOTB_TOP
export RTL_TOP=$( cd $COCOTB_TOP/../../rtl && pwd -P)
echo RTL_TOP: $RTL_TOP

export COCOTB_HDL_TIMEUNIT=1ns
export COCOTB_HDL_TIMEPRECISION=1ps

export TOPLEVEL_LANG=verilog
export VERILOG_SOURCES=$(find ${RTL_TOP} -type f -name '*.sv')

export SIM=verilator
