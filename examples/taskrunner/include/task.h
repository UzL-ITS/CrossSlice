#ifndef TR_TASK_H
#define TR_TASK_H

#define TASK_NAME_MAX 32

#define TASK_PENDING 0
#define TASK_DONE    1
#define TASK_FAILED  2

typedef int (*task_fn)(void *arg);

typedef struct task {
    int id;
    char name[TASK_NAME_MAX];
    int priority;
    int state;
    int attempts;
    task_fn fn;
    void *arg;
    struct task *next;
} task_t;

task_t *task_create(int id, const char *name, int priority,
                    task_fn fn, void *arg);
int task_execute(task_t *t);
void task_free(task_t *t);

#endif
