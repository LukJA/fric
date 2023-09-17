# Howdy there cowboy!
# Welcome to the Python virtual environment setup script.
# Luke this one's just for you :)

# print warning if running on Linux
if [ "$(uname -s)" = "Linux" ]; then
    echo On Debian based systems, python3-venv must be installed
    echo Run sudo apt install python3.10-venv
fi

# create environment in ./env
# you can change this path if you want, so long as it's in .gitignore
envpath="env"

# only create environment if it doesn't exist
if [ -d "$envpath" ]; then
    # actiavet only
    echo "Found environment $envpath, activating..."
    source "$envpath/bin/activate"
else
    echo "Creating virtual environment in $envpath..."
    python3 -m venv "$envpath"

    echo "Activating environment..."
    source "$envpath/bin/activate"

    # install requirements
    echo "Installing Python requirements..."
    python3 -m pip install -q --upgrade pip
    python3 -m pip install -q -r requirements.txt
fi

echo
echo "Virtual environment setup complete!"

echo 
echo "Installing env variables"
export HDL_TOP=$( realpath ./hdl )
export RTL_TOP="$HDL_TOP/rtl"
export COCOTB_TOP="$HDL_TOP/verif/cocotb"
echo "Environment activated"
echo
