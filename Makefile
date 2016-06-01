
all: sample

sample:	sample.o

%.o:	%.c
	$(CC) -O2 -o $@ -c $<
