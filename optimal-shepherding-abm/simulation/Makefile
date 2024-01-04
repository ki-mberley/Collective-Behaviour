# load the common configuration file
include ../config.mk

objs=herd.o
src=$(patsubst %.o,%.cc,$(objs))
execs=simulate

all: $(execs)

executables: $(execs)

# include the file dependencies
-include Makefile.dep

# a Makefile target to refresh the dependency file
depend: $(src)
	$(cxx) -MM $(src) >Makefile.dep

-include Makefile.dep

%.o: %.cc
	$(cxx) $(cflags) $(iflags) -c $<

# a Makefile target to remove all the built files
clean:
	rm -f $(objs) $(execs)

simulate: simulate.cc herd.o
	$(cxx) $(cflags) $(iflags) -o $@ $^ 


.PHONY: clean all executables depend
