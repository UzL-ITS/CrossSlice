CC     ?= cc
CFLAGS ?= -Wall -Wextra -O2

kvcli: kv.c util.c main.c
	$(CC) $(CFLAGS) -o $@ kv.c util.c main.c

clean:
	rm -f kvcli

.PHONY: clean
