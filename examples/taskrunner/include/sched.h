#ifndef TR_SCHED_H
#define TR_SCHED_H

#include "queue.h"
#include "task.h"

#define SCHED_PRIO_MAX  10
#define SCHED_MAX_RETRY 2

typedef struct sched {
    queue_t queue;
    int submitted;
    int completed;
    int failed;
    int retried;
} sched_t;

void sched_init(sched_t *s);
int sched_submit(sched_t *s, task_t *t);
int sched_run_once(sched_t *s);
void sched_drain(sched_t *s);

#endif
