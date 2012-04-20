LDFLAGS=-luuid 

CFLAGS=-g -I/usr/include/python2.7

all: test uuid.o


clean:
	rm -rf test *.o *~ *.pyc
