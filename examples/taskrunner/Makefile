CC      ?= cc
CFLAGS  ?= -Wall -Wextra -O2
CFLAGS  += -Iinclude

SRC = src/log.c src/util.c src/task.c src/queue.c src/sched.c src/main.c

taskrunner: $(SRC)
	$(CC) $(CFLAGS) -o $@ $(SRC)

clean:
	rm -f taskrunner

.PHONY: clean
