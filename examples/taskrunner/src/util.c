#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "util.h"

void die(const char *msg)
{
    fprintf(stderr, "fatal: %s\n", msg);
    exit(1);
}

void *xmalloc(size_t n)
{
    void *p = malloc(n);

    if (!p)
        die("out of memory");
    return p;
}

char *xstrdup(const char *s)
{
    size_t n = strlen(s) + 1;
    char *copy = xmalloc(n);

    memcpy(copy, s, n);
    return copy;
}
