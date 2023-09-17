import os
import sys
import inspect
from pathlib import Path

from cocotb.runner import get_runner


# Acquire environment variables

_ENV_RTL_TOP = os.getenv("RTL_TOP")
_ENV_COCOTB_TOP = os.getenv("COCOTB_TOP")

if _ENV_RTL_TOP is None:
    raise EnvironmentError("Incorrect config, RTL_TOP not set!")

if _ENV_COCOTB_TOP is None:
    raise EnvironmentError("Incorrect config, COCOTB_TOP not set!")

COCOTB_TOP = Path(str(_ENV_COCOTB_TOP))

RTL_TOP = Path(_ENV_RTL_TOP)
SRC_TOP = RTL_TOP / 'src'
INC_TOP = RTL_TOP / 'include'


_default_sim = "verilator"
_default_sim_args = [
    "--trace",
    "--trace-fst",
    "--trace-structs",
    "--coverage"
]

# TODO: include these env vars in class
# export COCOTB_HDL_TIMEUNIT=1ns
# export COCOTB_HDL_TIMEPRECISION=1ps

class TestWrapper():
    __test__ = False
    
    def __init__(self, *,
                 src=None,
                 inc=[INC_TOP],
                 toplevel,
                 sim=_default_sim,
                 sim_args=_default_sim_args):
        
        self.runner = get_runner(sim)

        if src is None:
            src_files = SRC_TOP.resolve().glob('**/*.sv')
        elif isinstance(src, list):
            src_files = []
            for src_dir in src:
                src_path = ( SRC_TOP / src_dir ).resolve()
                src_files.extend( src_path.glob('**/*.sv') )
        else:
            src_path = ( SRC_TOP / src ).resolve()

            src_files = src_path.glob('**/*.sv')
        
        self.runner.build(
            always=True,
            verilog_sources=src_files,
            includes=inc,
            hdl_toplevel=toplevel,
            build_args=sim_args,
            build_dir=str( COCOTB_TOP / f'sim_build/{toplevel}' )
        )

        self._toplevel = toplevel

    def test(self, search_path: str):
        caller_path = Path((inspect.stack()[1])[1])
        caller_dir = caller_path.parent
        full_path = (caller_dir / search_path).resolve()

        modules = full_path.glob(
            '**/cocotb_test_*.py'
        )

        for module_path in modules:
            folder_path = str(module_path.parent)
            module_name = module_path.stem

            print("DEBUG:", folder_path, module_name)

            sys.path.append(folder_path)

            self.runner.test(
                hdl_toplevel=self._toplevel,
                test_module=module_name
            )

            sys.path.remove(folder_path)

