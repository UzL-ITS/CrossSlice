#include <stdio.h>

#include "sched.h"
#include "task.h"
#include "log.h"

static int work_ok(void *arg)
{
    (void)arg;
    return 0;
}

static int work_flaky(void *arg)
{
    int *countdown = arg;

    if (*countdown > 0) {
        (*countdown)--;
        return -1;
    }
    return 0;
}

int main(void)
{
    sched_t sched;
    int flaky_failures = 2;
    int i;

    log_set_level(LOG_LEVEL_INFO);
    sched_init(&sched);

    for (i = 0; i < 3; i++)
        sched_submit(&sched, task_create(i, "steady", 1, work_ok, NULL));
    sched_submit(&sched,
                 task_create(99, "flaky", 5, work_flaky, &flaky_failures));

    sched_drain(&sched);

    printf("submitted=%d completed=%d failed=%d retried=%d\n",
           sched.submitted, sched.completed, sched.failed, sched.retried);
    return 0;
}
