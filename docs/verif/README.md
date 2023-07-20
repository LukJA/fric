<img width="100px" align=right src="../../logo/logo_prototype_2.png">

# A Brief Introduction to fric's Verification Methodology

fric supports two main verification platforms: python-based verification
with cocotb, and traditional systemverilog testbenches with modelsim.

## cocotb

cocotb is a great tool for quickly and easily constructing testbenches based on
python models. The entire test suite has been integrated with pytest for easy
test aggregation, and also GitHub actions for CI/CD.

### Getting Started

The basic flow for running the cocotb test suite is as follows:
```bash
cd hdl/verif/cocotb
source setup.sh
pytest
```
This is a massive abstraction that runs a complex array of scripts to test
each model; however integrating new tests into this system is quite
straightforward.

As tests are aggregated with pytest, we rely on pytest's discoverability rules
to find tests to run: running `pytest` from any folder will recursively
search for any python files named `test_*.py` or `*_test.py`, and execute
each function with these files named `test_*` or `*_test` (the same naming
convention as the files themselves, minus the file extension) as an individual
test. Therefore, adding a file within the `tests/` folder following this
convention will add tests to the suite. For consistency, the `test_*`
convention should be followed within this repo.

The convention at the time of writing is to structure test groups, e.g. by
function or by module, into folders at the top level of the `cocotb/tests/`
folder. Scripts should be able to account for further levels of nesting within
this, for example arithmetic tests could be structured as follows:
```
cocotb/
  |
  +-- tests/
       |
       +-- arithmetic/
       |     |
       |     +-- add/
       |     |     |
       |     |     +-- test_add.py
       |     |     |
       |     |     +-- add_1/cocotb_test_add_1.py
       |     |     |
       |     |     +-- add_2/cocotb_test_add_2.py
       |     |
       |     +-- sub/
       |           |
       |           +-- test_sub.py
       |           |
       |           +-- sub_1/cocotb_test_sub_1.py
       |           |
       |           +-- sub_2/cocotb_test_sub_2.py
       |
       +-- other/
             |
             +-- test_other.py
             .
             .
             .
```

As apparent in this example, the `test_*.py` file should call a set of
cocotb test modules, following the usual syntax, from within separate
sub-folders within the test suite (i.e. at the same level as `test_*.py`).
To maintain consistence, these cocotb test modules should be named as
`cocotb_test_*.py` to highlight their purpose and distinguish them from
library functions.

It may be necessary to instantiate a testbench for your tests, for example
where an interface is used in a module. This testbench should be named
`*_tb.sv`, with an appropriate module name in place of the wildcard, and
included in the same folder as the `cocotb_test_*.py` file.

### Constructing a Test Suite

Guidelines as to how to construct and structure your cocotb tests can be found
in the cocotb documentation. Structing the test suite top-level script
(`test_*.py`), however, warrants further explanation.

Test files follow a similar format, replicated below:

```python
import sys, os

try:
    from cocotb_setup import *
except ModuleNotFoundError:
    sys.exit("Error: incorrect configuration! "
             "Please run `source setup.sh` from verif/cocotb.")


CWD = os.path.dirname(os.path.realpath(__file__))

###############################################################################

def test_example():
    cocotb_test_module(
        src=[
            ...
        ],

        toplevel="toplevel_module_name",

        modulepath=f"{CWD}/path/to/module",
        modules=[
            ...
        ]
    )

...
```

Text above the divider is boilerplate: this simply imports the correct
environment variables and functions from the infrastructure. This will raise
an error if `source setup.sh` has not been run: running this file instantiates
many necessary environment variables, including the path to `cocotb_setup.py`
(which provides `cocotb_test_module`, amongst other things).

Below the divider is an example test, once again named following the `test_*`
convention. All tests should defer to their cocotb implementations for complex
logic etc, and use this function only for instantiation. It should serve merely
as a mapping between test modules, their top-level sv modules, and related
source files.

Therefore, it should suffice to copy the template above (and examples from
existing test suites) to produce new files. The variables COCOTB_TOP
(`hdl/verif/cocotb/`) and RTL_TOP (`hdl/rtl/`) are useful when referencing
test and source files, respectively.

### Running a Sub-set of Tests

Should you wish to run only the tests for some modules, you can simply pass the
folder path that you wish to test to pytest, for example:
```bash
pytest tests/arithmetic/
```
will run only the `test_*.py` files found recursively within this folder.
Following the above example, this would execute tests in `test_add.py` and
`test_sub.py` but not `test_other.py` nor any other tests not shown.

### Viewing Results

Pytest reports pass/fail results with module-level granularity, and within
the text logs for each is a test-level scoreboard. For further debugging,
waves are generated with each pass.

Results are all contained within the `sim_build` folder at the
top level (this is guaranteed by code within `cocotb_test_module`).
The folder structure within should mirror that of the `tests/` folder,
and within each module's named folder are two important files: `dump.vcd`,
containing waves, and `coverage.dat`, containing test coverage information.

### Peeking under the hood

To understand how and why this structure works, let's first discuss the
design philosophy behind it. Cocotb allows for, in effect, each toplevel to map
to multiple 'modules', which each contain multiple tests. Thematic or
functional separation of tests, therefore, makes sense with this modular
structure: one such module may contain a set of tests for one particular
behaviour, while another may contain a wholly different set of tests for
logically different behaviour.

At a higher level in the heirarchy, pytest draws distinction between test files
(i.e. `test_*.py`) and the tests within (once again, a many to one mapping).
To unify these two trees, each test file summarises the tests for a logical
group or block of the rtl (for example, the deocder, or arithmetic functions),
while each test within runs a cocotb test suite for an individual toplevel,
which itself may have multiple test modules. To summarise in tree form:
```
pytest
    |
    +- test_suite_1.py (one logical test suite)
    |   |
    |   +- test_toplevel_1 --> toplevel_1 (one sv module)
    |   |   |
    |   |   +- cocotb_test_1_1.py --> toplevel_1 function 1 tests
    |   |   |
    |   |   +- cocotb_test_1_2.py --> toplevel_1 function 2 tests
    |   |
    |   +- test_toplevel_2 --> toplevel_2 (another sv module)
    |       |
    |       +- cocotb_test_2_1.py --> toplevel_2 function 1 tests
    |       |
    |       +- cocotb_test_2_2.py --> toplevel_2 function 2 tests
    |
    +- test_suite_2.py (another logical test suite)
        |
        .
        .
        .
```
This isn't the clearest tree: the structure is inherently confusing because
there are so many levels of abstraction. We might need to find a better way
in future.

Having discussed the idea behind the structure, let's now discuss
implementation.

Configuration currently relies on environment variables: they are individaully
configurable, global, and can easily be varied between local runs without
committing hard changes to files.

The shell script `setup.sh` simply defines some key paths and configuration
variables for use by python or other build processes. The definitions in
here can easily be overwritten by re-defining variables in `setup.user.sh`,
which is called at the end of `setup.sh`'s execution.

As discussed above, calling `pytest` will execute the `test_*` functions in
any test files found. Each of these files should execute some simple
boilerplate code, and the test functions within should each execute a call to
`cocotb_test_module`. `cocotb_setup` is a module found in `hdl/verif/cocotb`
which defines `cocotb_test_module` and imports many environment variables into
python; the aforementioned boilerplate code simply tries to import this file,
and terminates execution if the shell environment is incorrectly configured.
This works because `setup.sh` adds `hdl/verif/cocotb` to `PYTHONPATH`, allowing
the module to be discovered by a python script placed anywhere. Likewise,
defining shorthand path variables in `setup.sh` makes locating files from
within arbitrarily-nested test folders much easier.

The variable definitions in `cocotb_setup` are fairly self-explanatory.
`cocotb_test_module` is the core test function which instantiates and executes
a runner, which cocotb uses to execute modules. Each call instantiates a new
runner for a single toplevel (and one or more test modules), however a call to
runner could be globally shared within a test suite.

`cocotb_test_module` takes four arguments:
- `src`: a list of verilog source files to compile
- `toplevel`: the name of the toplevel sv module to test
- `modulepath`: the absolute path of the test folder
- `modules`: a list of python cocotb test modules

The `subpath` variable is defined from `modulepath`, and is used to create
the sim_build folder heirarchy. Beyond this, the only non-standard code is to
add `modulepath` to the system PYTHONPATH, in order to make the modules
discoverable by cocotb.

With this complexity abstracted by the function, all it takes is one function
call with the right information to add a cocotb test suite to pytest.

### Integration with GitHub Actions

All of this is run through GitHub actions on every push to provide CI/CD.
Currently, this uses macOS 13 as only homebrew provides a straightforward
installation of verilator 5, which is required for SystemVerilog.


## modelsim

### ```modelsim is not currently implemented```
