#ifndef KV_H
#define KV_H

#define KV_INITIAL_CAP 8
#define KV_MAX_KEY_LEN 64

#define KV_OK           0
#define KV_ERR_NOMEM   -1
#define KV_ERR_NOTFOUND -2
#define KV_ERR_KEYLEN  -3

typedef struct kv_entry {
    char key[KV_MAX_KEY_LEN];
    char *value;
    int in_use;
} kv_entry;

typedef struct kv_store {
    kv_entry *entries;
    int cap;
    int count;
} kv_store;

kv_store *kv_create(void);
int kv_put(kv_store *s, const char *key, const char *value);
int kv_get(kv_store *s, const char *key, const char **out_value);
int kv_remove(kv_store *s, const char *key);
void kv_destroy(kv_store *s);

#endif
