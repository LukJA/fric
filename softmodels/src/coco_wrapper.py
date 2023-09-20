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

COCOTB_TOP = Path(_ENV_COCOTB_TOP)

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

def cocotb_test_wrapper(
        *,
        src=None,
        inc=[INC_TOP],
        toplevel,
        sim=_default_sim,
        sim_args=_default_sim_args,
        test_search_path='.'):
    """Utility function for easier cocotb testing.

    See docs/verif/README.md for more info.

    Args:
        src:              [str] - source file paths to search for .sv files
        inc:              [str] - include directories (passed straight to -I)
        toplevel:         str   - the name of the top-level module
        sim:              str   - the simulator to use
        sim_args:         [str] - any arguments to pass to the simulator
        test_search_path: str   - path to recursively search for test modules

    Returns:
        None
    """

    runner = get_runner(sim)

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

    prev_stack = inspect.stack()[1]
    test_name = prev_stack.function
    test_module = Path(prev_stack[1]).stem

    build_dir = str(COCOTB_TOP / f'sim_build/{test_module}/{test_name}')
    
    runner.build(
        always=True,
        verilog_sources=src_files, # type: ignore
        includes=inc,
        hdl_toplevel=toplevel,
        build_args=sim_args,
        build_dir=build_dir
    )

    caller_path = Path(prev_stack[1])
    caller_dir = caller_path.parent
    full_path = (caller_dir / test_search_path).resolve()

    modules = full_path.glob(
        '**/cocotb_test_*.py'
    )

    for module_path in modules:
        folder_path = str(module_path.parent)
        module_name = module_path.stem

        print("DEBUG:", folder_path, module_name)

        sys.path.append(folder_path)

        runner.test(
            hdl_toplevel=toplevel,
            test_module=module_name
        )

        sys.path.remove(folder_path)
