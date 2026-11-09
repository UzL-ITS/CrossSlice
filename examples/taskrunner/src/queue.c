#include <stddef.h>

#include "queue.h"

/* Higher priority first; FIFO among equals. */
static int task_before(const task_t *a, const task_t *b)
{
    return a->priority > b->priority;
}

void queue_init(queue_t *q)
{
    q->head = NULL;
    q->len = 0;
}

void queue_push(queue_t *q, task_t *t)
{
    task_t **link = &q->head;

    while (*link && !task_before(t, *link))
        link = &(*link)->next;
    t->next = *link;
    *link = t;
    q->len++;
}

task_t *queue_pop(queue_t *q)
{
    task_t *t = q->head;

    if (!t)
        return NULL;
    q->head = t->next;
    t->next = NULL;
    q->len--;
    return t;
}

int queue_len(const queue_t *q)
{
    return q->len;
}
