# Howdy there cowboy!
# Welcome to the Python virtual environment setup script.
# Luke this one's just for you :)

echo On Debian based systems, python3-venv must be installed
echo Run sudo apt install python3.10-venv

# create environment in ./env
# you can change this path if you want, so long as it's in .gitignore
echo "Creating virtual environment in ./env..."
python3 -m venv env

# install requirements
echo "Activating environment..."
source env/bin/activate

# install requirements
echo "Installing python requirements..."
python3 -m pip install -q --upgrade pip
python3 -m pip install -q -r requirements.txt

echo
echo "Virtual environment setup complete!"

echo 
echo "Installing env variables"
export COCOTB_TOP=$( realpath ./hdl/verif/cocotb )
export HDL_TOP=$( realpath $COCOTB_TOP/../.. )
export RTL_TOP=$( realpath $HDL_TOP/rtl )

export COCOTB_HDL_TIMEUNIT=1ns
export COCOTB_HDL_TIMEPRECISION=1ps
export TOPLEVEL_LANG=verilog
export SIM=verilator
export SIM_BUILD_ARGS="--trace --trace-fst --trace-structs --coverage"
echo "Environment activated"
echo
