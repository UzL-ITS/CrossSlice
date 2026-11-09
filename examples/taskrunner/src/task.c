#include <stdlib.h>
#include <string.h>

#include "task.h"
#include "log.h"
#include "util.h"

task_t *task_create(int id, const char *name, int priority,
                    task_fn fn, void *arg)
{
    task_t *t = xmalloc(sizeof(task_t));

    t->id = id;
    strncpy(t->name, name, TASK_NAME_MAX - 1);
    t->name[TASK_NAME_MAX - 1] = '\0';
    t->priority = priority;
    t->state = TASK_PENDING;
    t->attempts = 0;
    t->fn = fn;
    t->arg = arg;
    t->next = NULL;
    return t;
}

int task_execute(task_t *t)
{
    int rc;

    t->attempts++;
    rc = t->fn(t->arg);
    if (rc == 0) {
        t->state = TASK_DONE;
    } else {
        t->state = TASK_FAILED;
        LOG_ERROR("task %d (%s) failed with %d", t->id, t->name, rc);
    }
    return rc;
}

void task_free(task_t *t)
{
    free(t);
}
