#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "util.h"

static void *check_alloc(void *p)
{
    if (!p) {
        fprintf(stderr, "fatal: out of memory\n");
        exit(1);
    }
    return p;
}

void *xmalloc(size_t n)
{
    return check_alloc(malloc(n));
}

void *xcalloc(size_t nmemb, size_t size)
{
    return check_alloc(calloc(nmemb, size));
}

char *xstrdup(const char *s)
{
    size_t n = strlen(s) + 1;
    char *copy = xmalloc(n);

    memcpy(copy, s, n);
    return copy;
}
