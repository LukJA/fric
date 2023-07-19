ifndef COCOTB_TOP
  $(error COCOTB_TOP (top level cocotb path) not set! \
  	Run `source verif/cocotb/setup.sh` first)
endif

ifndef RTL_TOP
  $(error RTL_TOP (top level RTL path) not set! \
  	Run `source verif/cocotb/setup.sh` first)
endif
