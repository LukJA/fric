# fric
Finite-Response-Impulse-Computer

### Usage
For 32 bit free modelsim, get a 32 conda python and cocotb enviroment. Unit tests are all defined and called by the msim makefile

For Icarus/Verilator, SV support is limited, but the standard makefile can be used.

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