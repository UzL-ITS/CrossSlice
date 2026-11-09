#include <stddef.h>

#include "sched.h"
#include "log.h"

static int validate_task(const task_t *t)
{
    if (!t || !t->fn)
        return -1;
    if (t->priority < 0 || t->priority > SCHED_PRIO_MAX)
        return -1;
    if (t->name[0] == '\0')
        return -1;
    return 0;
}

static void handle_result(sched_t *s, task_t *t, int rc)
{
    if (rc == 0) {
        s->completed++;
        LOG_INFO("task %d (%s) done", t->id, t->name);
        task_free(t);
        return;
    }
    if (t->attempts <= SCHED_MAX_RETRY) {
        s->retried++;
        LOG_WARN("task %d (%s) retry %d", t->id, t->name, t->attempts);
        queue_push(&s->queue, t);
        return;
    }
    s->failed++;
    task_free(t);
}

void sched_init(sched_t *s)
{
    queue_init(&s->queue);
    s->submitted = 0;
    s->completed = 0;
    s->failed = 0;
    s->retried = 0;
}

int sched_submit(sched_t *s, task_t *t)
{
    if (validate_task(t) != 0) {
        LOG_ERROR("rejecting invalid task");
        return -1;
    }
    queue_push(&s->queue, t);
    s->submitted++;
    LOG_INFO("submitted task %d (%s) prio %d", t->id, t->name, t->priority);
    return 0;
}

int sched_run_once(sched_t *s)
{
    task_t *t = queue_pop(&s->queue);
    int rc;

    if (!t)
        return -1;
    rc = task_execute(t);
    handle_result(s, t, rc);
    return 0;
}

void sched_drain(sched_t *s)
{
    while (queue_len(&s->queue) > 0)
        sched_run_once(s);
}
