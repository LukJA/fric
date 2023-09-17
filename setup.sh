# Howdy there cowboy!
# Welcome to the Python virtual environment setup script.
# Luke this one's just for you :)

echo On Debian based systems, python3-venv must be installed
echo Run sudo apt install python3.10-venv

# create environment in ./env
# you can change this path if you want, so long as it's in .gitignore
if [ ! -d "env" ]; then
    echo "Creating virtual environment in ./env..."
    python3 -m venv env
fi

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
export HDL_TOP=$( realpath ./hdl )
export RTL_TOP="$HDL_TOP/rtl"
export COCOTB_TOP="$HDL_TOP/verif/cocotb"
echo "Environment activated"
echo
