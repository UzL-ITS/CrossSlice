#include <stdlib.h>
#include <string.h>

#include "kv.h"
#include "util.h"

static unsigned long hash_key(const char *key)
{
    unsigned long h = 5381;
    int c;

    while ((c = *key++))
        h = ((h << 5) + h) + (unsigned long)c;
    return h;
}

/* Linear probing: returns the slot holding key, or the first free slot. */
static int find_slot(const kv_store *s, const char *key)
{
    int idx = (int)(hash_key(key) % (unsigned long)s->cap);
    int i;

    for (i = 0; i < s->cap; i++) {
        kv_entry *e = &s->entries[(idx + i) % s->cap];

        if (!e->in_use || strcmp(e->key, key) == 0)
            return (idx + i) % s->cap;
    }
    return -1;
}

static int kv_grow(kv_store *s)
{
    kv_entry *old_entries = s->entries;
    int old_cap = s->cap;
    int i;

    s->cap = old_cap * 2;
    s->count = 0;
    s->entries = xcalloc((size_t)s->cap, sizeof(kv_entry));
    for (i = 0; i < old_cap; i++) {
        kv_entry *e = &old_entries[i];

        if (e->in_use) {
            kv_put(s, e->key, e->value);
            free(e->value);
        }
    }
    free(old_entries);
    return KV_OK;
}

kv_store *kv_create(void)
{
    kv_store *s = xmalloc(sizeof(kv_store));

    s->cap = KV_INITIAL_CAP;
    s->count = 0;
    s->entries = xcalloc(KV_INITIAL_CAP, sizeof(kv_entry));
    return s;
}

int kv_put(kv_store *s, const char *key, const char *value)
{
    size_t key_len = strlen(key);
    kv_entry *e;
    int idx;

    if (key_len >= KV_MAX_KEY_LEN)
        return KV_ERR_KEYLEN;
    if (2 * (s->count + 1) > s->cap)
        kv_grow(s);
    idx = find_slot(s, key);
    if (idx < 0)
        return KV_ERR_NOMEM;
    e = &s->entries[idx];
    if (!e->in_use) {
        memcpy(e->key, key, key_len + 1);
        e->in_use = 1;
        s->count++;
    } else {
        free(e->value);
    }
    e->value = xstrdup(value);
    return KV_OK;
}

int kv_get(kv_store *s, const char *key, const char **out_value)
{
    int idx = find_slot(s, key);

    if (idx < 0 || !s->entries[idx].in_use) {
        *out_value = NULL;
        return KV_ERR_NOTFOUND;
    }
    *out_value = s->entries[idx].value;
    return KV_OK;
}

int kv_remove(kv_store *s, const char *key)
{
    int idx = find_slot(s, key);

    if (idx < 0 || !s->entries[idx].in_use)
        return KV_ERR_NOTFOUND;
    free(s->entries[idx].value);
    s->entries[idx].value = NULL;
    s->entries[idx].in_use = 0;
    s->count--;
    return KV_OK;
}

void kv_destroy(kv_store *s)
{
    int i;

    for (i = 0; i < s->cap; i++)
        if (s->entries[i].in_use)
            free(s->entries[i].value);
    free(s->entries);
    free(s);
}
