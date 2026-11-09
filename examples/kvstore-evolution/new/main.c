#include <stdio.h>
#include <string.h>

#include "kv.h"

/* Tiny line-based REPL: set <k> <v> | get <k> | del <k> | quit */
int main(void)
{
    kv_store *store = kv_create();
    char line[256], key[256], value[256];

    while (fgets(line, sizeof(line), stdin)) {
        if (sscanf(line, "set %255s %255s", key, value) == 2) {
            if (kv_put(store, key, value) == KV_OK)
                printf("ok\n");
            else
                printf("error\n");
        } else if (sscanf(line, "get %255s", key) == 1) {
            const char *v;

            if (kv_get(store, key, &v) == KV_OK)
                printf("%s\n", v);
            else
                printf("(not found)\n");
        } else if (sscanf(line, "del %255s", key) == 1) {
            printf(kv_remove(store, key) == KV_OK ? "ok\n" : "(not found)\n");
        } else if (strncmp(line, "quit", 4) == 0) {
            break;
        }
    }
    kv_destroy(store);
    return 0;
}
