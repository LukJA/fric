# THIS FILE MUST BE RUN FROM THE CURRENT DIRECTORY
# IT DOES NOT WORK OTHERWISE

# IT IS CONFIGURED THIS WAY BECAUSE GITHUB ACTIONS IS A PAIN
# (it runs all scripts from some weird temp directory)

# the below corrects the path if run like e.g. source ../setup.sh
# but this doesn't work with gh actions so instead just source the script
# from the same dir.

# export COCOTB_TOP=$( cd $(dirname -- "$0") && pwd -P )

export COCOTB_TOP=$( realpath . )
export HDL_TOP=$( realpath $COCOTB_TOP/../.. )
export RTL_TOP=$( realpath $HDL_TOP/rtl )

# FIXME: These need to be included in the runner
export COCOTB_HDL_TIMEUNIT=1ns
export COCOTB_HDL_TIMEPRECISION=1ps

export TOPLEVEL_LANG=verilog
# export VERILOG_SOURCES=$(find ${RTL_TOP} -type f -name '*.sv')

export SIM=verilator
export SIM_BUILD_ARGS="--trace --coverage"

export PYTHONPATH="${COCOTB_TOP}:${PYTHONPATH}"
