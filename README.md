<p align="center">
	<img width="300px" src="logo/logo_prototype_2.png">
	<h1 align="center">
        <b>F</b>inite
        <b>R</b>esponse
        <b>I</b>mpulse
        <b>C</b>omputer
    </h1>
</p>

## Usage
```bash
# Construct Environment
source setup.sh
# Run
cd hdl/verif/cocotb
pytest
```


## Simulation Notes

### Icarus
Icarus is free and functional, but only supports a minimal subset of the SystemVerilog syntax (e.g. no array reduction operators).

### Verilator
Verilator is fast, but smashes the hierarchy for debugging, and seems to fail to properly generate recursive modules with multiple levels e.g. that used in the leading ones and zeroes detectors.

### Modelsim-Intel
Intel quartus modelsim is free and includes a GUI, but the free version is 32-bit, and is therefore incompatible with the 64-bit default python.

```bash
$ conda create -n py3_32
$ conda activate py3_32
$ conda config --env --set subdir linux-32
$ conda install python=3 gxx_linux-32
$ pip install cocotb
$ pip install pytest
```