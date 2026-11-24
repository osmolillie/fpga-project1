SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES = $(CURDIR)/../rtl/counter.sv
COCOTB_TOPLEVEL = counter
COCOTB_TEST_MODULES = test_counter

COMPILE_ARGS += -g2012

include $(shell cocotb-config --makefiles)/Makefile.sim
