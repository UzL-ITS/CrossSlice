#include <stdarg.h>
#include <stdio.h>

#include "log.h"

static int current_level = LOG_LEVEL_INFO;

static const char *level_name(int level)
{
    if (level == LOG_LEVEL_ERROR)
        return "ERROR";
    if (level == LOG_LEVEL_WARN)
        return "WARN";
    return "INFO";
}

void log_set_level(int level)
{
    current_level = level;
}

void log_msg(int level, const char *fmt, ...)
{
    va_list ap;

    if (level < current_level)
        return;
    fprintf(stderr, "[%s] ", level_name(level));
    va_start(ap, fmt);
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    fputc('\n', stderr);
}
