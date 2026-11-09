# Fix-task transcript — kvstore @ 353554d523f6 — openrouter:mock/model @ xhigh

- Hint given: function `kv_put`
- Real fix: 6 changed lines

```diff
diff --git a/kv.c b/kv.c
index 44a0cab..b462c94 100644
--- a/kv.c
+++ b/kv.c
@@ -62,9 +62,12 @@ kv_store *kv_create(void)
 
 int kv_put(kv_store *s, const char *key, const char *value)
 {
+    size_t key_len = strlen(key);
     kv_entry *e;
     int idx;
 
+    if (key_len >= KV_MAX_KEY_LEN)
+        return KV_ERR_KEYLEN;
     if (2 * (s->count + 1) > s->cap)
         kv_grow(s);
     idx = find_slot(s, key);
@@ -72,7 +75,7 @@ int kv_put(kv_store *s, const char *key, const char *value)
         return KV_ERR_NOMEM;
     e = &s->entries[idx];
     if (!e->in_use) {
-        strcpy(e->key, key);
+        memcpy(e->key, key, key_len + 1);
         e->in_use = 1;
         s->count++;
     } else {
diff --git a/kv.h b/kv.h
index 93868a6..2d8e3e9 100644
--- a/kv.h
+++ b/kv.h
@@ -7,6 +7,7 @@
 #define KV_OK           0
 #define KV_ERR_NOMEM   -1
 #define KV_ERR_NOTFOUND -2
+#define KV_ERR_KEYLEN  -3
 
 typedef struct kv_entry {
     char key[KV_MAX_KEY_LEN];

```

## Self-navigation arm (generic file tools)

### Turn 1  _(tok 100+20, stop=tool_use)_

**Reasoning:** let me read

- `read_file(path=kv.c, version=old, start_line=60, end_line=85)` →

```
kv.c lines 60-85 of 120
   60|     return s;
   61| }
   62| 
   63| int kv_put(kv_store *s, const char *key, const char *value)
   64| {
   65|     kv_entry *e;
   66|     int idx;
   67| 
   68|     if (2 * (s->count + 1) > s->cap)
   69|         kv_grow(s);
   70|     idx = find_slot(s, key);
   71|     if (idx < 0)
   72|         return KV_ERR_NOMEM;
   73|     e = &s->entries[idx];
   74|     if (!e->in_use) {
   75|         strcpy(e->key, key);
   76|         e->in_use = 1;
   77|         s->count++;
   78|     } else {
   79|         free(e->value);
   80|     }
   81|     e->value = xstrdup(value);
   82|     return KV_OK;
   83| }
   84| 
   85| int kv_get(kv_store *s, const char *key, const char **out_value)
```

### Turn 2  _(tok 100+20, stop=tool_use)_

- **submit_fix** → `{"root_cause": "strcpy overflow", "patch": "--- a/kv.c\n+++ b/kv.c\n@@\n-strcpy\n+strncpy", "files_touched": ["kv.c"], "confidence_overall": "high"}`

**Judge:** `{"root_cause_match": "correct", "fix_quality": "equivalent", "rationale": "mock", "score": 2}`

