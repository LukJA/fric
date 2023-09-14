# Howdy there cowboy!
# Welcome to the Python virtual environment setup script.
# Luke this one's just for you :)

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
echo "Remember, if you want to do verif, you'll have to run:"
echo " $ cd hdl/verif/cocotb && source setup.sh |"
echo
echo "It's is an unfortunate consequence of github's weird directory structure."
echo "(I'll look into it...)"
echo
