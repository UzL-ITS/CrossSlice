#ifndef TR_UTIL_H
#define TR_UTIL_H

#include <stddef.h>

void *xmalloc(size_t n);
char *xstrdup(const char *s);
void die(const char *msg);

#endif
