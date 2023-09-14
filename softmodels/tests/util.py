from pyposit import PyPosit, PyPositConfig


cfg_71 = PyPositConfig(n_bits=7, es=1)

def pyposit_71_from_float(f):
    # handy utility function
    return PyPosit.from_float(cfg_71, f)
