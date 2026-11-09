#ifndef TR_QUEUE_H
#define TR_QUEUE_H

#include "task.h"

typedef struct queue {
    task_t *head;
    int len;
} queue_t;

void queue_init(queue_t *q);
void queue_push(queue_t *q, task_t *t);
task_t *queue_pop(queue_t *q);
int queue_len(const queue_t *q);

#endif
