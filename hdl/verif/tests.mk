# howdy there cowboy, you're now entering the wild wild west of GNU make!

# this is a really hacky (read: bad) way of getting basic key/value pairs
# out of makefiles so we can define a test suite more easily
# (i.e. it's not ideal to have to add a new make target for each file)

# to add a target, simply define two variables:
#   MODULE_{test_name} := test_name
#   TOPLEVEL_{test_name} := test_hdl
# where {test_name} is the name of your test (make target)
# and test_hdl is the name of the rtl file

# dff
MODULE_dff   	    := test_dff
TOPLEVEL_dff 	    := dff

# posit
MODULE_posit     	:= test_posit_adder
TOPLEVEL_posit 		:= posit_adder

# clz
MODULE_clz   		:= test_clz
TOPLEVEL_clz 		:= count_lead_zero

# clo
MODULE_clo   		:= test_clo
TOPLEVEL_clo 		:= count_lead_one

# ffo
MODULE_ffo   		:= test_ffo
TOPLEVEL_ffo 		:= find_first_one

# ffno
MODULE_ffno   		:= test_ffno
TOPLEVEL_ffno 		:= find_first_n_ones

# decoder
MODULE_decoder   	:= test_decoder
TOPLEVEL_decoder 	:= format_decoder
