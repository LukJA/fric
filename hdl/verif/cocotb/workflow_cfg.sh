# DO NOT REMOVE - CONFIGURE ENV FOR GH ACTIONS
# USERS CALL THE TOP-LEVEL SCRIPT BUT GH REQUIRES
# THIS DIRECTORY BECAUSE SOMETIMES WE CANT HAVE
# NICE THINGS

export COCOTB_TOP=$( realpath . )
export HDL_TOP=$( realpath $COCOTB_TOP/../.. )
export RTL_TOP=$( realpath $HDL_TOP/rtl )

export COCOTB_HDL_TIMEUNIT=1ns
export COCOTB_HDL_TIMEPRECISION=1ps

export TOPLEVEL_LANG=verilog
export SIM=verilator
export SIM_BUILD_ARGS="--trace --trace-fst --trace-structs --coverage"

if [ -f setup.user.sh ]; then source setup.user.sh ; fi
