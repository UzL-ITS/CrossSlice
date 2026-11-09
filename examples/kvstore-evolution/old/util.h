#ifndef KV_UTIL_H
#define KV_UTIL_H

#include <stddef.h>

void *xmalloc(size_t n);
void *xcalloc(size_t nmemb, size_t size);
char *xstrdup(const char *s);

#endif
