# Impact-analysis transcript — php-src @ f2b371e747d2 — openrouter:deepseek/deepseek-v4-pro

- target: `phar_parse_url` (ext/phar/stream.c), arity 4->5
- truth: [['ext/phar/dirstream.c', 'phar_wrapper_mkdir'], ['ext/phar/dirstream.c', 'phar_wrapper_open_dir'], ['ext/phar/dirstream.c', 'phar_wrapper_rmdir'], ['ext/phar/stream.c', 'phar_wrapper_open_url'], ['ext/phar/stream.c', 'phar_wrapper_rename'], ['ext/phar/stream.c', 'phar_wrapper_stat'], ['ext/phar/stream.c', 'phar_wrapper_unlink']]

## Self-navigation arm

### Turn 1  _(tok 902+114, stop=tool_use)_

**Reasoning:** The user wants me to find all call sites of `phar_parse_url` in the repository. I need to search for calls to this function, excluding its definition and prototypes/comments. Let me grep for it.

- `grep(pattern=phar_parse_url\s*\(, version=old)` →

```
12 matches
ext/phar/dirstream.c:250:	php_url *resource = phar_parse_url(wrapper, path, mode, options);
ext/phar/dirstream.c:360:	if ((resource = phar_parse_url(wrapper, url_from, "w", options)) == NULL) {
ext/phar/dirstream.c:484:	php_url *resource = phar_parse_url(wrapper, url, "w", options);
ext/phar/dirstream.h:25:php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options);
ext/phar/phar.c:2200: * This is used by phar_parse_url()
ext/phar/stream.c:58:php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options) /* {{{ */
ext/phar/stream.c:169:	php_url *resource = phar_parse_url(wrapper, path, mode, options);
ext/phar/stream.c:560:	php_url *resource = phar_parse_url(wrapper, url, "r", flags|PHP_STREAM_URL_STAT_QUIET);
ext/phar/stream.c:663:	php_url *resource = phar_parse_url(wrapper, url, "rb", options);
ext/phar/stream.c:733:	php_url *resource_from = phar_parse_url(wrapper, url_from, "wb", options|PHP_STREAM_URL_STAT_QUIET);
ext/phar/stream.c:746:	php_url *resource_to = phar_parse_url(wrapper, url_to, "wb", options|PHP_STREAM_URL_STAT_QUIET);
ext/phar/stream.h:21:php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options);
```

### Turn 2  _(tok 1450+768, stop=tool_use)_

**Reasoning:** Let me analyze the matches:

1. `ext/phar/dirstream.c:250` - call inside some function
2. `ext/phar/dirstream.c:360` - call inside some function
3. `ext/phar/dirstream.c:484` - call inside some function
4. `ext/phar/dirstream.h:25` - prototype (exclude)
5. `ext/phar/phar.c:2200` - comment (exclude)
6. `ext/phar/stream.c:58` - definition (exclude)
7. `ext/phar/stream.c:169` - call inside some function
8. `ext/phar/stream.c:560` - call inside some function
9. `ext/phar/stream.c:663` - call inside some function
10. `ext/phar/stream.c:733` - call inside some function
11. `ext/phar/stream.c:746` - call inside some function
12. `ext/phar/stream.h:21` - prototype (exclude)

So I need to find the enclosing function for each call site. Let me look at each file.

**Says:** I need to identify the enclosing functions for each call site. Let me examine the relevant lines in context.

- `read_file(path=ext/phar/dirstream.c, start_line=240, end_line=255)` →

```
ext/phar/dirstream.c lines 240-255 of 580
  240| }
  241| /* }}}*/
  242| 
  243| /**
  244|  * Open a directory handle within a phar archive
  245|  */
  246| php_stream *phar_wrapper_open_dir(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /* {{{ */
  247| {
  248| 	char *error;
  249| 
  250| 	php_url *resource = phar_parse_url(wrapper, path, mode, options);
  251| 	if (!resource) {
  252| 		php_stream_wrapper_log_error(wrapper, options, "phar url \"%s\" is unknown", path);
  253| 		return NULL;
  254| 	}
  255| 
```

- `read_file(path=ext/phar/dirstream.c, start_line=350, end_line=365)` →

```
ext/phar/dirstream.c lines 350-365 of 580
  350| 
  351| 	phar_archive_data *phar = phar_get_archive(ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL);
  352| 
  353| 	zend_string_release_ex(arch, false);
  354| 
  355| 	if (PHAR_G(readonly) && (!phar || !phar->is_data)) {
  356| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\", write operations disabled", url_from);
  357| 		return 0;
  358| 	}
  359| 
  360| 	if ((resource = phar_parse_url(wrapper, url_from, "w", options)) == NULL) {
  361| 		return 0;
  362| 	}
  363| 
  364| 	/* we must have at the very least phar://alias.phar/internalfile.php */
  365| 	if (!resource->scheme || !resource->host || !resource->path) {
```

- `read_file(path=ext/phar/dirstream.c, start_line=474, end_line=490)` →

```
ext/phar/dirstream.c lines 474-490 of 580
  474| 
  475| 	phar_archive_data *phar = phar_get_archive(ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL);
  476| 
  477| 	zend_string_release_ex(arch, false);
  478| 
  479| 	if (PHAR_G(readonly) && (!phar || !phar->is_data)) {
  480| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot rmdir directory \"%s\", write operations disabled", url);
  481| 		return 0;
  482| 	}
  483| 
  484| 	php_url *resource = phar_parse_url(wrapper, url, "w", options);
  485| 	if (!resource) {
  486| 		return 0;
  487| 	}
  488| 
  489| 	/* we must have at the very least phar://alias.phar/internalfile.php */
  490| 	if (!resource->scheme || !resource->host || !resource->path) {
```

- `read_file(path=ext/phar/stream.c, start_line=159, end_line=175)` →

```
ext/phar/stream.c lines 159-175 of 947
  159| static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /* {{{ */
  160| {
  161| 	phar_archive_data *phar;
  162| 	phar_entry_data *idata;
  163| 	char *internal_file;
  164| 	char *error;
  165| 	HashTable *pharcontext;
  166| 	php_stream *fpf;
  167| 	zval *pzoption, *metadata;
  168| 
  169| 	php_url *resource = phar_parse_url(wrapper, path, mode, options);
  170| 	if (!resource) {
  171| 		return NULL;
  172| 	}
  173| 
  174| 	/* we must have at the very least phar://alias.phar/internalfile.php */
  175| 	if (!resource->scheme || !resource->host || !resource->path) {
```

- `read_file(path=ext/phar/stream.c, start_line=550, end_line=565)` →

```
ext/phar/stream.c lines 550-565 of 947
  550| 
  551| /**
  552|  * Stream wrapper stat implementation of stat()
  553|  */
  554| static int phar_wrapper_stat(php_stream_wrapper *wrapper, const char *url, int flags,
  555| 				  php_stream_statbuf *ssb, php_stream_context *context) /* {{{ */
  556| {
  557| 	char *internal_file;
  558| 	size_t internal_file_len;
  559| 
  560| 	php_url *resource = phar_parse_url(wrapper, url, "r", flags|PHP_STREAM_URL_STAT_QUIET);
  561| 	if (!resource) {
  562| 		return FAILURE;
  563| 	}
  564| 
  565| 	/* we must have at the very least phar://alias.phar/internalfile.php */
```

- `read_file(path=ext/phar/stream.c, start_line=653, end_line=668)` →

```
ext/phar/stream.c lines 653-668 of 947
  653| 
  654| /**
  655|  * Unlink a file within a phar archive
  656|  */
  657| static int phar_wrapper_unlink(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
  658| {
  659| 	char *internal_file, *error;
  660| 	size_t internal_file_len;
  661| 	phar_entry_data *idata;
  662| 
  663| 	php_url *resource = phar_parse_url(wrapper, url, "rb", options);
  664| 	if (!resource) {
  665| 		php_stream_wrapper_log_error(wrapper, options, "phar error: unlink failed");
  666| 		return 0;
  667| 	}
  668| 
```

- `read_file(path=ext/phar/stream.c, start_line=723, end_line=750)` →

```
ext/phar/stream.c lines 723-750 of 947
  723| /* }}} */
  724| 
  725| static int phar_wrapper_rename(php_stream_wrapper *wrapper, const char *url_from, const char *url_to, int options, php_stream_context *context) /* {{{ */
  726| {
  727| 	char *error;
  728| 	bool is_dir = false;
  729| 	bool is_modified = false;
  730| 
  731| 	error = NULL;
  732| 
  733| 	php_url *resource_from = phar_parse_url(wrapper, url_from, "wb", options|PHP_STREAM_URL_STAT_QUIET);
  734| 	if (!resource_from) {
  735| 		php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\": invalid or non-writable url \"%s\"", url_from, url_to, url_from);
  736| 		return 0;
  737| 	}
  738| 
  739| 	phar_archive_data *pfrom = phar_get_archive(ZSTR_VAL(resource_from->host), ZSTR_LEN(resource_from->host), NULL, 0, NULL);
  740| 	if (PHAR_G(readonly) && (!pfrom || !pfrom->is_data)) {
  741| 		php_url_free(resource_from);
  742| 		php_error_docref(NULL, E_WARNING, "phar error: Write operations disabled by the php.ini setting phar.readonly");
  743| 		return 0;
  744| 	}
  745| 
  746| 	php_url *resource_to = phar_parse_url(wrapper, url_to, "wb", options|PHP_STREAM_URL_STAT_QUIET);
  747| 	if (!resource_to) {
  748| 		php_url_free(resource_from);
  749| 		php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\": invalid or non-writable url \"%s\"", url_from, url_to, url_to);
  750| 		return 0;
```

### Turn 3  _(tok 4256+108, stop=tool_use)_

**Reasoning:** Now let me also check the enclosing functions for the dirstream.c calls at lines 360 and 484.

- `read_file(end_line=330, path=ext/phar/dirstream.c, start_line=310)` →

```
ext/phar/dirstream.c lines 310-330 of 580
  310| 			php_url_free(resource);
  311| 			return ret;
  312| 		}
  313| 		ret = phar_make_dirstream(internal_file, internal_file_len, &phar->manifest);
  314| 		php_url_free(resource);
  315| 		return ret;
  316| 	} else {
  317| 		zend_string *str_key;
  318| 
  319| 		/* search for directory */
  320| 		ZEND_HASH_MAP_FOREACH_STR_KEY(&phar->manifest, str_key) {
  321| 			if (zend_string_starts_with_cstr(str_key, internal_file, internal_file_len)) {
  322| 				/* directory found */
  323| 				ret = phar_make_dirstream(internal_file, internal_file_len, &phar->manifest);
  324| 				php_url_free(resource);
  325| 				return ret;
  326| 			}
  327| 		} ZEND_HASH_FOREACH_END();
  328| 	}
  329| 
  330| 	php_url_free(resource);
```

### Turn 4  _(tok 4647+85, stop=tool_use)_

- `read_file(end_line=310, path=ext/phar/dirstream.c, start_line=280)` →

```
ext/phar/dirstream.c lines 280-310 of 580
  280| 			efree(error);
  281| 		} else {
  282| 			php_stream_wrapper_log_error(wrapper, options, "phar file \"%s\" is unknown", ZSTR_VAL(resource->host));
  283| 		}
  284| 		php_url_free(resource);
  285| 		return NULL;
  286| 	}
  287| 
  288| 	if (zend_string_equals(resource->path, ZSTR_CHAR('/'))) {
  289| 		/* root directory requested */
  290| 		php_url_free(resource);
  291| 		return phar_make_dirstream("/", strlen("/"), &phar->manifest);
  292| 	}
  293| 
  294| 	if (!HT_IS_INITIALIZED(&phar->manifest)) {
  295| 		php_url_free(resource);
  296| 		return NULL;
  297| 	}
  298| 
  299| 	const char *internal_file = ZSTR_VAL(resource->path) + 1; /* strip leading "/" */
  300| 	size_t internal_file_len = ZSTR_LEN(resource->path) - 1;
  301| 	const phar_entry_info *entry = zend_hash_str_find_ptr(&phar->manifest, internal_file, internal_file_len);
  302| 	php_stream *ret;
  303| 
  304| 	if (NULL != entry && !entry->is_dir) {
  305| 		php_url_free(resource);
  306| 		return NULL;
  307| 	} else if (entry && entry->is_dir) {
  308| 		if (entry->is_mounted) {
  309| 			ret = php_stream_opendir(entry->tmp, options, context);
  310| 			php_url_free(resource);
```

### Turn 5  _(tok 5166+117, stop=tool_use)_

**Reasoning:** Now let me also confirm the enclosing function for dirstream.c:360 and :484.

For dirstream.c:360 - let me look above.

- `read_file(end_line=340, path=ext/phar/dirstream.c, start_line=333)` →

```
ext/phar/dirstream.c lines 333-340 of 580
  333| /* }}} */
  334| 
  335| /**
  336|  * Make a new directory within a phar archive
  337|  */
  338| int phar_wrapper_mkdir(php_stream_wrapper *wrapper, const char *url_from, int mode, int options, php_stream_context *context) /* {{{ */
  339| {
  340| 	phar_entry_info entry;
```

### Turn 6  _(tok 5399+85, stop=tool_use)_

- `read_file(end_line=470, path=ext/phar/dirstream.c, start_line=461)` →

```
ext/phar/dirstream.c lines 461-470 of 580
  461| /**
  462|  * Remove a directory within a phar archive
  463|  */
  464| int phar_wrapper_rmdir(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
  465| {
  466| 	char *error;
  467| 
  468| 	/* pre-readonly check, we need to know if this is a data phar */
  469| 	zend_string *arch = phar_split_fname(url, strlen(url), NULL, 2, 2);
  470| 	if (!arch) {
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 7  _(tok 5667+575, stop=tool_use, forced)_

**Reasoning:** Let me compile the list of call sites:

1. `ext/phar/dirstream.c:250` — function `phar_wrapper_open_dir`
2. `ext/phar/dirstream.c:360` — function `phar_wrapper_mkdir`
3. `ext/phar/dirstream.c:484` — function `phar_wrapper_rmdir`
4. `ext/phar/stream.c:169` — function `phar_wrapper_open_url`
5. `ext/phar/stream.c:560` — function `phar_wrapper_stat`
6. `ext/phar/stream.c:663` — function `phar_wrapper_unlink`
7. `ext/phar/stream.c:733` — function `phar_wrapper_rename`
8. `ext/phar/stream.c:746` — function `phar_wrapper_rename` (same function, second call)

So the unique enclosing functions are:

1. `phar_wrapper_open_dir` — `ext/phar/dirstream.c`
2. `phar_wrapper_mkdir` — `ext/phar/dirstream.c`
3. `phar_wrapper_rmdir` — `ext/phar/dirstream.c`
4. `phar_wrapper_open_url` — `ext/phar/stream.c`
5. `phar_wrapper_stat` — `ext/phar/stream.c`
6. `phar_wrapper_unlink` — `ext/phar/stream.c`
7. `phar_wrapper_rename` — `ext/phar/stream.c`

That's 7 callers. Let me submit.

- **submit_callers** → `{"callers": [{"function": "phar_wrapper_open_dir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_stat", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_unlink", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_rename", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2743+105, stop=tool_use)_

**Reasoning:** We need find all call sites of phar_parse_url in repository. Need list every function that calls it, enclosing function name and file. We can use grep and semantic tools. Let's search.

- `grep(pattern=phar_parse_url, version=old)` →

```
12 matches
ext/phar/dirstream.c:250:	php_url *resource = phar_parse_url(wrapper, path, mode, options);
ext/phar/dirstream.c:360:	if ((resource = phar_parse_url(wrapper, url_from, "w", options)) == NULL) {
ext/phar/dirstream.c:484:	php_url *resource = phar_parse_url(wrapper, url, "w", options);
ext/phar/dirstream.h:25:php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options);
ext/phar/phar.c:2200: * This is used by phar_parse_url()
ext/phar/stream.c:58:php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options) /* {{{ */
ext/phar/stream.c:169:	php_url *resource = phar_parse_url(wrapper, path, mode, options);
ext/phar/stream.c:560:	php_url *resource = phar_parse_url(wrapper, url, "r", flags|PHP_STREAM_URL_STAT_QUIET);
ext/phar/stream.c:663:	php_url *resource = phar_parse_url(wrapper, url, "rb", options);
ext/phar/stream.c:733:	php_url *resource_from = phar_parse_url(wrapper, url_from, "wb", options|PHP_STREAM_URL_STAT_QUIET);
ext/phar/stream.c:746:	php_url *resource_to = phar_parse_url(wrapper, url_to, "wb", options|PHP_STREAM_URL_STAT_QUIET);
ext/phar/stream.h:21:php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options);
```

### Turn 2  _(tok 3283+338, stop=tool_use)_

**Reasoning:** Need identify enclosing function for each call site. Matches in dirstream.c lines 250, 360, 484; stream.c lines 169, 560, 663, 733, 746. Prototypes dirstream.h, stream.h ignore. phar.c comment ignore. Definition stream.c:58 ignore. Need functions containing lines.

Let's get context or grep function definitions. Use grep for function definitions in those files.

- `grep(pattern=^(PHP_FUNCTION|static |php_stream|php_url|int |void |char |p, path_glob=ext/phar/dirstream.c, version=old)` →

```
10 matches
ext/phar/dirstream.c:37:static int phar_dir_close(php_stream *stream, int close_handle)  /* {{{ */
ext/phar/dirstream.c:54:static int phar_dir_seek(php_stream *stream, zend_off_t offset, int whence, zend_off_t *newoffset) /* {{{ */
ext/phar/dirstream.c:86:static ssize_t phar_dir_read(php_stream *stream, char *buf, size_t count) /* {{{ */
ext/phar/dirstream.c:118:static ssize_t phar_dir_write(php_stream *stream, const char *buf, size_t count) /* {{{ */
ext/phar/dirstream.c:127:static int phar_dir_flush(php_stream *stream) /* {{{ */
ext/phar/dirstream.c:136:static int phar_compare_dir_name(Bucket *f, Bucket *s)  /* {{{ */
ext/phar/dirstream.c:149:static php_stream *phar_make_dirstream(const char *dir, size_t dirlen, const HashTable *manifest) /* {{{ */
ext/phar/dirstream.c:246:php_stream *phar_wrapper_open_dir(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_
ext/phar/dirstream.c:338:int phar_wrapper_mkdir(php_stream_wrapper *wrapper, const char *url_from, int mode, int options, php_stream_context *context) /* {{{ */
ext/phar/dirstream.c:464:int phar_wrapper_rmdir(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
```

- `grep(pattern=^(PHP_FUNCTION|static |php_stream|php_url|int |void |char |p, path_glob=ext/phar/stream.c, version=old)` →

```
12 matches
ext/phar/stream.c:58:php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options) /* {{{ */
ext/phar/stream.c:159:static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STR
ext/phar/stream.c:349:static int phar_stream_close(php_stream *stream, int close_handle) /* {{{ */
ext/phar/stream.c:363:static ssize_t phar_stream_read(php_stream *stream, char *buf, size_t count) /* {{{ */
ext/phar/stream.c:394:static int phar_stream_seek(php_stream *stream, zend_off_t offset, int whence, zend_off_t *newoffset) /* {{{ */
ext/phar/stream.c:438:static ssize_t phar_stream_write(php_stream *stream, const char *buf, size_t count) /* {{{ */
ext/phar/stream.c:461:static int phar_stream_flush(php_stream *stream) /* {{{ */
ext/phar/stream.c:485:static void phar_dostat(const phar_archive_data *phar, const phar_entry_info *data, php_stream_statbuf *ssb, bool is_temp_dir)
ext/phar/stream.c:537:static int phar_stream_stat(php_stream *stream, php_stream_statbuf *ssb) /* {{{ */
ext/phar/stream.c:554:static int phar_wrapper_stat(php_stream_wrapper *wrapper, const char *url, int flags,
ext/phar/stream.c:657:static int phar_wrapper_unlink(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
ext/phar/stream.c:725:static int phar_wrapper_rename(php_stream_wrapper *wrapper, const char *url_from, const char *url_to, int options, php_stream_context *context) /* {{{ */
```

### Turn 3  _(tok 4524+765, stop=tool_use)_

**Reasoning:** Matches align:
dirstream.c 250 in phar_wrapper_open_dir (starts 246)
360 in phar_wrapper_mkdir (338)
484 in phar_wrapper_rmdir (464)
stream.c 169 in phar_wrapper_open_url (159)
560 in phar_wrapper_stat (554)
663 in phar_wrapper_unlink (657)
733,746 in phar_wrapper_rename (725)

Need ensure no other call sites missed due multiline/macros. grep found all textual occurrences. But could be through macros? phar_parse_url only textual. We have 8 call sites. Need list every function. Could submit. But let's verify line 250 etc maybe multiple functions? Let's use get_context_at for each line? Or read function lines. But we already know. Should ensure no call at stream.c:560 is within phar_wrapper_stat and not phar_stream_stat. get_context_at for confidence.

- `get_context_at(file=ext/phar/dirstream.c, line=250, version=old)` →

```
phar_wrapper_open_dir — ext/phar/dirstream.c:246 [function] php_stream *phar_wrapper_open_dir(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /*
  reads: mode, options, path, wrapper; writes: -; returns: return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return phar_make_dirstream("/", strlen("/"), &phar->manifest);

SLICE around line 250 (def-use, level 2; '>' marks the seed):
php_stream *phar_wrapper_open_dir(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /* {
   char *error;
>  php_url *resource = phar_parse_url(wrapper, path, mode, options);
   if(!resource) {
   ...
   }
   if(!resource->scheme || !resource->host || !resource->path) {
     if(resource->host && !resource->path) {
       php_stream_wrapper_log_error(wrapper, options, "phar error: no directory in \"%s\", must have at least phar://%s/ for root directory(always use full path to a new phar)", path, ZSTR_VAL(resource->host));
       php_url_free(resource);
   ...
     }
     php_url_free(resource);
   ...
   }
   if(!zend_string_equals_literal_ci(resource->scheme, "phar")) {
     php_url_free(resource);
   ...
   }
   ...
   const phar_archive_data *phar = phar_get_archive(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error);
   if(!phar) {
     if(error) {
   ...
     } else {
       php_stream_wrapper_log_error(wrapper, options, "phar file \"%s\" is unknown", ZSTR_VAL(resource->host));
     }
     php_url_free(resource);
   ...
   }
   if(zend_string_equals(resource->path, ZSTR_CHAR('/'))) {
     php_url_free(resource);
     return phar_make_dirstream("/", strlen("/"), &phar->manifest);
   }
   if(!HT_IS_INITIALIZED(&phar->manifest)) {
     php_url_free(resource);
   ...
   }
   const char *internal_file = ZSTR_VAL(resource->path)+ 1;
   size_t internal_file_len = ZSTR_LEN(resource->path)- 1;
   const phar_entry_info *entry = zend_hash_str_find_ptr(&phar->manifest, internal_file, internal_file_len);
   ...
   if(NULL != entry && !entry->is_dir) {
     php_url_free(resource);
   ...
   } else if(entry && entry->is_dir) {
     if(entry->is_mounted) {
       ret = php_stream_opendir(entry->tmp, options, context);
       php_url_free(resource);
       return ret;
     }
     ret = phar_make_dirstream(internal_file, internal_file_len, &phar->manifest);
     php_url_free(resource);
     return ret;
   } else {
     zend_string *str_key;
     ZEND_HASH_MAP_FOREACH_STR_KEY(&phar->manifest, str_key)
       if(zend_string_starts_with_cstr(str_key, internal_file, internal_file_len)) {
         ret = phar_make_dirstream(internal_file, internal_file_len, &phar->manifest);
         php_url_free(resource);
         return ret;
   ...
       }
   }
   php_url_free(resource);
   ...
}

CALLEES (18):
  phar_parse_url (ext/phar/stream.c:58): reads filename, mode, options, wrapper; writes -; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  php_stream_wrapper_log_error (main/streams/streams.c:242): reads fmt, options, wrapper; writes -; returns -
  php_url_free (ext/standard/url.c:28): reads theurl; writes -; returns -
  phar_request_initialize (ext/phar/phar.c:3369): reads -; writes -; returns -
  phar_get_archive (ext/phar/util.c:946): reads alias, alias_len, error, fname, fname_len; writes error*; returns return NULL; | return archive; | return NULL; | return archive; | return NULL; | return archive;
  phar_make_dirstream (ext/phar/dirstream.c:149): reads dir, dirlen, manifest; writes -; returns return php_stream_alloc(&phar_dir_ops, data, NULL, "r"); | return php_stream_alloc(&phar_dir_ops, data, NULL, "r"); | return php_stream_alloc(&phar_dir_ops, data, NULL, "r");
  zend_string_equals (Zend/zend_string.h:395): reads s1, s2; writes -; returns return s1 == s2 || zend_string_equal_content(s1, s2);
  ZSTR_CHAR (Zend/zend_string.h:110): reads c; writes -; returns return zend_one_char_string[c];
  zend_hash_str_find_ptr (Zend/zend_hash.h:915): reads ht, len, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  zend_string_starts_with_cstr (Zend/zend_string.h:409): reads prefix, prefix_length, str; writes -; returns return ZSTR_LEN(str)>= prefix_length && !memcmp(ZSTR_VAL(str), prefix, prefix_length);
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  zend_string_equals_literal_ci [macro]: #define zend_string_equals_literal_ci(str, c) \
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  HT_IS_INITIALIZED [macro]: #define HT_IS_INITIALIZED(ht) \
  ZEND_HASH_FOREACH_END [macro]: #define ZEND_HASH_FOREACH_END() \
  ZEND_HASH_MAP_FOREACH_STR_KEY [macro]: #define ZEND_HASH_MAP_FOREACH_STR_KEY(ht, _key) \
  php_stream_opendir [macro]: #define php_stream_opendir(path, options, context) _php_stream_opendir((path), (options), (context) STREAMS_CC)

CALLERS (0):
```

- `get_context_at(file=ext/phar/dirstream.c, line=360, version=old)` →

```
phar_wrapper_mkdir — ext/phar/dirstream.c:338 [function] int phar_wrapper_mkdir(php_stream_wrapper *wrapper, const char *url_from, int mode, int options, php_stream_context *context) /*
  reads: options, url_from, wrapper; writes: -; returns: return 0; | return 0; | return 0; | return 0; | return 0; | return 0;

SLICE around line 360 (def-use, level 2; '>' marks the seed):
int phar_wrapper_mkdir(php_stream_wrapper *wrapper, const char *url_from, int mode, int options, php_stream_context *context) /* {
   ...
   char *error;
   php_url *resource = NULL;
   ...
>  if((resource = phar_parse_url(wrapper, url_from, "w", options))== NULL) {
     return 0;
   }
   if(!resource->scheme || !resource->host || !resource->path) {
     php_url_free(resource);
   ...
   }
   if(!zend_string_equals_literal_ci(resource->scheme, "phar")) {
     php_url_free(resource);
   ...
   }
   phar = phar_get_archive(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error);
   if(!phar) {
     php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", error retrieving phar information: %s", ZSTR_VAL(resource->path)+ 1, ZSTR_VAL(resource->host), error);
   ...
     php_url_free(resource);
   ...
   }
   phar_entry_info *e = phar_get_entry_info_dir(phar, ZSTR_VAL(resource->path)+ 1, ZSTR_LEN(resource->path)- 1, 2, &error, true);
   if(e) {
     if(e->is_temp_dir) {
       zend_string_efree(e->filename);
       efree(e);
     }
     php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", directory already exists", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host));
     php_url_free(resource);
   ...
   }
   if(error) {
     php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", %s", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host), error);
   ...
     php_url_free(resource);
   ...
   }
   if(phar_get_entry_info_dir(phar, ZSTR_VAL(resource->path)+ 1, ZSTR_LEN(resource->path)- 1, 0, &error, true)) {
     php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", file already exists", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host));
     php_url_free(resource);
   ...
   }
   if(error) {
     php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", %s", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host), error);
   ...
     php_url_free(resource);
   ...
   }
   memset((void *)&entry, 0, sizeof(phar_entry_info));
   if(phar->is_zip) {
   ...
   }
   entry.filename = zend_string_init(ZSTR_VAL(resource->path)+ 1, ZSTR_LEN(resource->path)- 1, false);
   if(phar->is_tar) {
   ...
   }
   php_url_free(resource);
   ...
   entry.phar = phar;
   ...
   entry.old_flags = PHAR_ENT_PERM_DEF_DIR;
   void *had_been_added = zend_hash_add_mem(&phar->manifest, entry.filename, &entry, sizeof(phar_entry_info));
   if(!had_been_added) {
     php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", adding to manifest failed", ZSTR_VAL(entry.filename), ZSTR_VAL(phar->fname));
     zend_string_efree(entry.filename);
   ...
   }
   phar_flush(phar, &error);
   if(error) {
     php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", %s", ZSTR_VAL(entry.filename), ZSTR_VAL(phar->fname), error);
     zend_hash_del(&phar->manifest, entry.filename);
   ...
   }
   phar_add_virtual_dirs(phar, ZSTR_VAL(entry.filename), ZSTR_LEN(entry.filename));
   ...
}

CALLEES (18):
  phar_split_fname (ext/phar/phar.c:2277): reads entry, executable, filename, filename_len, for_create; writes -; returns return phar_split_fname_ex(filename, filename_len, entry, executable, for_create, NULL);
  php_stream_wrapper_log_error (main/streams/streams.c:242): reads fmt, options, wrapper; writes -; returns -
  phar_get_archive (ext/phar/util.c:946): reads alias, alias_len, error, fname, fname_len; writes error*; returns return NULL; | return archive; | return NULL; | return archive; | return NULL; | return archive;
  zend_string_release_ex (Zend/zend_string.h:359): reads persistent, s; writes -; returns -
  phar_parse_url (ext/phar/stream.c:58): reads filename, mode, options, wrapper; writes -; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  php_url_free (ext/standard/url.c:28): reads theurl; writes -; returns -
  phar_get_entry_info_dir (ext/phar/util.c:1169): reads dir, error, path, path_len, phar, security; writes error*, phar*; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  zend_string_efree (Zend/zend_string.h:342): reads s; writes -; returns -
  zend_string_init (Zend/zend_string.h:202): reads len, persistent, str; writes -; returns return ret;
  zend_hash_add_mem (Zend/zend_hash.h:741): reads ht, key, pData, size; writes -; returns return Z_PTR_P(zv); | return NULL;
  phar_flush (ext/phar/phar.c:2493): reads error, phar; writes -; returns return phar_flush_ex(phar, NULL, false, error);
  zend_hash_del (Zend/zend_hash.c:1549): reads ht, key; writes -; returns return SUCCESS; | return FAILURE;
  phar_add_virtual_dirs (ext/phar/util.c:1962): reads filename, filename_len, phar; writes phar*; returns -
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  zend_string_equals_literal_ci [macro]: #define zend_string_equals_literal_ci(str, c) \
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  not defined in this repository: PHAR_G

CALLERS (0):
```

- `get_context_at(file=ext/phar/dirstream.c, line=484, version=old)` →

```
phar_wrapper_rmdir — ext/phar/dirstream.c:464 [function] int phar_wrapper_rmdir(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /*
  reads: options, url, wrapper; writes: -; returns: return 0; | return 0; | return 0; | return 0; | return 0; | return 0;

SLICE around line 484 (def-use, level 2; '>' marks the seed):
int phar_wrapper_rmdir(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {
   char *error;
   ...
>  php_url *resource = phar_parse_url(wrapper, url, "w", options);
   if(!resource) {
   ...
   }
   if(!resource->scheme || !resource->host || !resource->path) {
     php_url_free(resource);
   ...
   }
   if(!zend_string_equals_literal_ci(resource->scheme, "phar")) {
     php_url_free(resource);
   ...
   }
   phar = phar_get_archive(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error);
   if(!phar) {
     php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\" in phar \"%s\", error retrieving phar information: %s", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host), error);
   ...
     php_url_free(resource);
   ...
   }
   size_t path_len = ZSTR_LEN(resource->path)- 1;
   phar_entry_info *entry = phar_get_entry_info_dir(phar, ZSTR_VAL(resource->path)+ 1, path_len, 2, &error, true);
   if(!entry) {
     if(error) {
       php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\" in phar \"%s\", %s", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host), error);
   ...
     } else {
       php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\" in phar \"%s\", directory does not exist", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host));
     }
     php_url_free(resource);
   ...
   }
   if(!entry->is_deleted) {
     zend_string *str_key;
     ZEND_HASH_MAP_FOREACH_STR_KEY(&phar->manifest, str_key)
       if(zend_string_starts_with_cstr(str_key, ZSTR_VAL(resource->path)+1, path_len)&& IS_SLASH(ZSTR_VAL(str_key)[path_len])) {
   ...
         if(entry->is_temp_dir) {
           zend_string_efree(entry->filename);
           efree(entry);
         }
         php_url_free(resource);
   ...
       }
   ...
     ZEND_HASH_MAP_FOREACH_STR_KEY(&phar->virtual_dirs, str_key)
   ...
       if(zend_string_starts_with_cstr(str_key, ZSTR_VAL(resource->path)+1, path_len)&& IS_SLASH(ZSTR_VAL(str_key)[path_len])) {
   ...
         if(entry->is_temp_dir) {
           zend_string_efree(entry->filename);
           efree(entry);
         }
         php_url_free(resource);
   ...
       }
   }
   if(entry->is_temp_dir) {
     zend_hash_str_del(&phar->virtual_dirs, ZSTR_VAL(resource->path)+1, path_len);
     zend_string_efree(entry->filename);
     efree(entry);
   } else {
     entry->is_deleted = 1;
     entry->is_modified = 1;
     phar_flush(phar, &error);
     if(error) {
       php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\" in phar \"%s\", %s", ZSTR_VAL(entry->filename), ZSTR_VAL(phar->fname), error);
       php_url_free(resource);
   ...
     }
   }
   php_url_free(resource);
   ...
}

CALLEES (20):
  phar_split_fname (ext/phar/phar.c:2277): reads entry, executable, filename, filename_len, for_create; writes -; returns return phar_split_fname_ex(filename, filename_len, entry, executable, for_create, NULL);
  php_stream_wrapper_log_error (main/streams/streams.c:242): reads fmt, options, wrapper; writes -; returns -
  phar_get_archive (ext/phar/util.c:946): reads alias, alias_len, error, fname, fname_len; writes error*; returns return NULL; | return archive; | return NULL; | return archive; | return NULL; | return archive;
  zend_string_release_ex (Zend/zend_string.h:359): reads persistent, s; writes -; returns -
  phar_parse_url (ext/phar/stream.c:58): reads filename, mode, options, wrapper; writes -; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  php_url_free (ext/standard/url.c:28): reads theurl; writes -; returns -
  phar_get_entry_info_dir (ext/phar/util.c:1169): reads dir, error, path, path_len, phar, security; writes error*, phar*; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  zend_string_efree (Zend/zend_string.h:342): reads s; writes -; returns -
  zend_string_starts_with_cstr (Zend/zend_string.h:409): reads prefix, prefix_length, str; writes -; returns return ZSTR_LEN(str)>= prefix_length && !memcmp(ZSTR_VAL(str), prefix, prefix_length);
  phar_flush (ext/phar/phar.c:2493): reads error, phar; writes -; returns return phar_flush_ex(phar, NULL, false, error);
  zend_hash_str_del (Zend/zend_hash.c:1676): reads ht, len, str; writes -; returns return SUCCESS; | return FAILURE;
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  zend_string_equals_literal_ci [macro]: #define zend_string_equals_literal_ci(str, c) \
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZEND_HASH_FOREACH_END [macro]: #define ZEND_HASH_FOREACH_END() \
  IS_SLASH [macro (1 of 2 definitions)]: #define IS_SLASH(c) ((c) == '/')
  ZEND_ASSERT [macro (1 of 3 definitions)]: # define ZEND_ASSERT(c) ZEND_ASSUME(c)
  ZEND_HASH_MAP_FOREACH_STR_KEY [macro]: #define ZEND_HASH_MAP_FOREACH_STR_KEY(ht, _key) \
  not defined in this repository: PHAR_G

CALLERS (0):
```

- `get_context_at(file=ext/phar/stream.c, line=169, version=old)` →

```
phar_wrapper_open_url — ext/phar/stream.c:159 [function] static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /*
  reads: mode, opened_path, options, path, wrapper; writes: opened_path*; returns: return NULL; | return NULL; | return NULL; | return NULL; | return fpf; | return NULL;

SLICE around line 169 (def-use, level 2; '>' marks the seed):
static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /* {
   ...
   phar_entry_data *idata;
   ...
   char *error;
   ...
>  php_url *resource = phar_parse_url(wrapper, path, mode, options);
   if(!resource) {
   ...
   }
   if(!resource->scheme || !resource->host || !resource->path) {
     php_url_free(resource);
   ...
   }
   if(!zend_string_equals_literal_ci(resource->scheme, "phar")) {
     php_url_free(resource);
   ...
   }
   ...
   internal_file = estrndup(ZSTR_VAL(resource->path)+ 1, ZSTR_LEN(resource->path)- 1);
   if(mode[0] == 'w' ||(mode[0] == 'r' && mode[1] == '+')) {
     if(NULL ==(idata = phar_get_or_create_entry_data(resource->host, internal_file, strlen(internal_file), mode, 0, &error, true, time(NULL)))) {
       if(error) {
   ...
       } else {
         php_stream_wrapper_log_error(wrapper, options, "phar error: file \"%s\" could not be created in phar \"%s\"", internal_file, ZSTR_VAL(resource->host));
       }
       efree(internal_file);
       php_url_free(resource);
   ...
     }
     fpf = php_stream_alloc(&phar_ops, idata, NULL, mode);
     php_url_free(resource);
     efree(internal_file);
     if(context && Z_TYPE(context->options)!= IS_UNDEF &&(pzoption = zend_hash_str_find_ind(HASH_OF(&context->options), "phar", sizeof("phar")-1))!= NULL) {
       pharcontext = HASH_OF(pzoption);
       if(idata->internal_file->uncompressed_filesize == 0 && idata->internal_file->compressed_filesize == 0 &&(pzoption = zend_hash_str_find_ind(pharcontext, "compress", sizeof("compress")-1))!= NULL && Z_TYPE_P(pzoption)== IS_LONG &&(Z_LVAL_P(pzoption)& ~PHAR_ENT_COMPRESSION_MASK)== 0) {
         idata->internal_file->flags &= ~PHAR_ENT_COMPRESSION_MASK;
         idata->internal_file->flags |= Z_LVAL_P(pzoption);
       }
       if((pzoption = zend_hash_str_find_ind(pharcontext, "metadata", sizeof("metadata")-1))!= NULL) {
         phar_metadata_tracker_free(&idata->internal_file->metadata_tracker, idata->internal_file->is_persistent);
         metadata = pzoption;
         ZVAL_COPY_DEREF(&idata->internal_file->metadata_tracker.val, metadata);
         idata->phar->is_modified = true;
       }
     }
     if(opened_path) {
       *opened_path = zend_strpprintf_unchecked(MAXPATHLEN, "phar://%S/%S", idata->phar->fname, idata->internal_file->filename);
     }
     return fpf;
   } else {
     if(!*internal_file &&(options & STREAM_OPEN_FOR_INCLUDE)) {
       phar = phar_get_archive(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, NULL);
       if(!phar) {
         php_stream_wrapper_log_error(wrapper, options, "file %s is not a valid phar archive", ZSTR_VAL(resource->host));
         efree(internal_file);
         php_url_free(resource);
   ...
       }
       if(phar->is_tar || phar->is_zip) {
         if((FAILURE == phar_get_entry_data(&idata, resource->host, ".phar/stub.php", sizeof(".phar/stub.php")-1, "r", 0, &error, false))|| !idata) {
   ...
         }
         efree(internal_file);
         if(opened_path) {
           *opened_path = zend_string_copy(phar->fname);
         }
         php_url_free(resource);
   ...
       } else {
         php_stream *stream = phar_get_pharfp(phar);
         if(stream == NULL) {
           stream = phar_open_archive_fp(phar);
           if(UNEXPECTED(!stream)) {
             php_stream_wrapper_log_error(wrapper, options, "phar error: could not reopen phar \"%s\"", ZSTR_VAL(resource->host));
             efree(internal_file);
             php_url_free(resource);
   ...
           }
         }
   ...
         entry =(phar_entry_info *)ecalloc(1, sizeof(phar_entry_info));
   ...
         entry->phar = phar;
   ...
         entry->compressed_filesize = entry->uncompressed_filesize = phar->halt_offset;
         entry->is_crc_checked = 1;
         idata =(phar_entry_data *)ecalloc(1, sizeof(phar_entry_data));
         idata->fp = stream;
         idata->phar = phar;
         idata->internal_file = entry;
         if(!phar->is_persistent) {
           ++(entry->phar->refcount);
         }
   ...
         php_url_free(resource);
         if(opened_path) {
           *opened_path = zend_string_copy(phar->fname);
         }
         efree(internal_file);
   ...
       }
     }
     if((FAILURE == phar_get_entry_data(&idata, resource->host, internal_file, strlen(internal_file), "r", 0, &error, false))|| !idata) {
   ...
       if(error) {
   ...
       } else {
         php_stream_wrapper_log_error(wrapper, options, "phar error: \"%s\" is not a file in phar \"%s\"", internal_file, ZSTR_VAL(resource->host));
       }
       efree(internal_file);
       php_url_free(resource);
   ...
     }
   }
   php_url_free(resource);
   #ifdef ...
   fprintf(stderr, "Pharname: %s\n", ZSTR_VAL(idata->phar->fname));
   fprintf(stderr, "Filename: %s\n", internal_file);
   fprintf(stderr, "Entry: %s\n", ZSTR_VAL(idata->internal_file->filename));
   fprintf(stderr, "Size: %u\n", idata->internal_file->uncompressed_filesize);
   fprintf(stderr, "Compressed: %u\n", idata->internal_file->flags);
   #endif
   if(!idata->internal_file->is_crc_checked && phar_postprocess_file(idata, idata->internal_file->crc32, &error, 2)!= SUCCESS) {
   ...
     phar_entry_delref(idata);
     efree(internal_file);
   ...
   }
   if(!PHAR_G(cwd_init)&&(options & STREAM_OPEN_FOR_INCLUDE)) {
     const char *entry = ZSTR_VAL(idata->internal_file->filename), *cwd;
   ...
     if((idata->phar->is_tar || idata->phar->is_zip)&& zend_string_equals_literal(idata->internal_file->filename, ".phar/stub.php")) {
   ...
     } else if((cwd = strrchr(entry, '/'))) {
       PHAR_G(cwd_len)= cwd - entry;
       PHAR_G(cwd)= estrndup(entry, PHAR_G(cwd_len));
     } else {
   ...
       PHAR_G(cwd)= NULL;
     }
   }
   if(opened_path) {
     *opened_path = zend_strpprintf_unchecked(MAXPATHLEN, "phar://%S/%S", idata->phar->fname, idata->internal_file->filename);
   }
   efree(internal_file);
   ...
   fpf = php_stream_alloc(&phar_ops, idata, NULL, mode);
   return fpf;
}

CALLEES (32):
  phar_parse_url (ext/phar/stream.c:58): reads filename, mode, options, wrapper; writes -; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  php_stream_wrapper_log_error (main/streams/streams.c:242): reads fmt, options, wrapper; writes -; returns -
  php_url_free (ext/standard/url.c:28): reads theurl; writes -; returns -
  phar_request_initialize (ext/phar/phar.c:3369): reads -; writes -; returns -
  phar_get_entry_data (ext/phar/util.c:452): reads allow_dir, error, fname, mode, path, path_len, ret, security; writes error*, ret*; returns return FAILURE; | return FAILURE; | return FAILURE; | return SUCCESS; | return FAILURE; | return SUCCESS;
  zend_string_copy (Zend/zend_string.h:222): reads s; writes -; returns return s;
  ZSTR_EMPTY_ALLOC (Zend/zend_string.h:106): reads -; writes -; returns return zend_empty_string;
  phar_open_archive_fp (ext/phar/util.c:702): reads phar; writes -; returns return stream; | return NULL; | return stream;
  phar_get_pharfp (ext/phar/phar_internal.h:306): reads phar; writes -; returns return phar->fp; | return PHAR_G(cached_fp)[phar->phar_pos].fp;
  phar_get_archive (ext/phar/util.c:946): reads alias, alias_len, error, fname, fname_len; writes error*; returns return NULL; | return archive; | return NULL; | return archive; | return NULL; | return archive;
  zend_strpprintf_unchecked (Zend/zend.c:367): reads format, max_len; writes -; returns return str;
  phar_metadata_tracker_free (ext/phar/phar.c:642): reads persistent, tracker; writes tracker*; returns -
  zend_hash_str_find_ind (Zend/zend_hash.h:457): reads ht, len, str; writes -; returns return(zv && Z_TYPE_P(zv)== IS_INDIRECT)?((Z_TYPE_P(Z_INDIRECT_P(zv))!= IS_UNDEF)? Z_INDIRECT_P(zv): NULL): zv;
  phar_get_or_create_entry_data (ext/phar/util.c:597): reads allow_dir, error, fname, mode, path, path_len, security, timestamp; writes error*; returns return NULL; | return NULL; | return ret; | return NULL; | return NULL; | return NULL;
  phar_entry_delref (ext/phar/phar.c:397): reads idata; writes -; returns -
  phar_postprocess_file (ext/phar/phar.c:2338): reads crc32, error, idata, process_zip; writes error*, idata*; returns return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return SUCCESS; | return SUCCESS;
  zend_string_equals_literal_ci [macro]: #define zend_string_equals_literal_ci(str, c) \
  estrndup [macro]: #define estrndup(s, length) _estrndup((s), (length) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ecalloc [macro]: #define ecalloc(nmemb, size) _ecalloc((nmemb), (size) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  UNEXPECTED [macro (1 of 4 definitions)]: # define UNEXPECTED(condition) (condition)
  ZVAL_COPY_DEREF [macro]: #define ZVAL_COPY_DEREF(z, v) do { \
  Z_LVAL_P [macro]: #define Z_LVAL_P(zval_p) Z_LVAL(*(zval_p))
  Z_TYPE_P [macro]: #define Z_TYPE_P(zval_p) Z_TYPE(*(zval_p))
  HASH_OF [macro]: #define HASH_OF(p) (Z_TYPE_P(p)==IS_ARRAY ? Z_ARRVAL_P(p) : ((Z_TYPE_P(p)==IS_OBJECT ? Z_OBJ_HT_P(p)->get_properties(Z_OBJ_P(p)) : NULL)))
  Z_TYPE [macro]: #define Z_TYPE(zval) zval_get_type(&(zval))
  php_stream_alloc [macro]: #define php_stream_alloc(ops, thisptr, persistent_id, mode) _php_stream_alloc((ops), (thisptr), (persistent_id), (mode) STREAMS_CC)
  zend_string_equals_literal [macro]: #define zend_string_equals_literal(str, literal) \
  not defined in this repository: PHAR_G, strrchr

CALLERS (0):
```

- `get_context_at(file=ext/phar/stream.c, line=560, version=old)` →

```
phar_wrapper_stat — ext/phar/stream.c:554 [function] static int phar_wrapper_stat(php_stream_wrapper *wrapper, const char *url, int flags, php_stream_statbuf *ssb, php_stream_context *context) /*
  reads: flags, ssb, url, wrapper; writes: -; returns: return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return SUCCESS; | return FAILURE;

SLICE around line 560 (def-use, level 2; '>' marks the seed):
static int phar_wrapper_stat(php_stream_wrapper *wrapper, const char *url, int flags, php_stream_statbuf *ssb, php_stream_context *context) /* {
   ...
>  php_url *resource = phar_parse_url(wrapper, url, "r", flags|PHP_STREAM_URL_STAT_QUIET);
   if(!resource) {
   ...
   }
   if(!resource->scheme || !resource->host || !resource->path) {
     php_url_free(resource);
   ...
   }
   if(!zend_string_equals_literal_ci(resource->scheme, "phar")) {
     php_url_free(resource);
   ...
   }
   ...
   internal_file = ZSTR_VAL(resource->path)+ 1;
   phar_archive_data *phar = phar_get_archive(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, NULL);
   if(!phar) {
     php_url_free(resource);
   ...
   }
   if(*internal_file == '\0') {
     phar_dostat(phar, NULL, ssb, true);
     php_url_free(resource);
   ...
   }
   if(!HT_IS_INITIALIZED(&phar->manifest)) {
     php_url_free(resource);
   ...
   }
   internal_file_len = strlen(internal_file);
   phar_entry_info *entry = zend_hash_str_find_ptr(&phar->manifest, internal_file, internal_file_len);
   if(entry) {
     phar_dostat(phar, entry, ssb, false);
     php_url_free(resource);
   ...
   }
   if(zend_hash_str_exists(&(phar->virtual_dirs), internal_file, internal_file_len)) {
     phar_dostat(phar, NULL, ssb, true);
     php_url_free(resource);
   ...
   }
   if(HT_IS_INITIALIZED(&phar->mounted_dirs)&& zend_hash_num_elements(&phar->mounted_dirs)) {
     zend_string *str_key;
     ZEND_HASH_MAP_FOREACH_STR_KEY(&phar->mounted_dirs, str_key)
       if(ZSTR_LEN(str_key)>= internal_file_len || strncmp(ZSTR_VAL(str_key), internal_file, ZSTR_LEN(str_key))) {
   ...
       } else {
         char *test;
   ...
         if(NULL ==(entry = zend_hash_find_ptr(&phar->manifest, str_key))) {
   ...
         }
         if(!entry->tmp || !entry->is_mounted) {
   ...
         }
         test_len = spprintf(&test, MAXPATHLEN, "%s%s", entry->tmp, internal_file + ZSTR_LEN(str_key));
   ...
         if(SUCCESS != phar_mount_entry(phar, test, test_len, internal_file, internal_file_len)) {
   ...
         }
   ...
         entry = zend_hash_str_find_ptr(&phar->manifest, internal_file, internal_file_len);
         if(!entry) {
   ...
         }
         phar_dostat(phar, entry, ssb, false);
         php_url_free(resource);
   ...
       }
   }
   ...
   php_url_free(resource);
   ...
}

CALLEES (19):
  phar_parse_url (ext/phar/stream.c:58): reads filename, mode, options, wrapper; writes -; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  php_url_free (ext/standard/url.c:28): reads theurl; writes -; returns -
  phar_request_initialize (ext/phar/phar.c:3369): reads -; writes -; returns -
  phar_get_archive (ext/phar/util.c:946): reads alias, alias_len, error, fname, fname_len; writes error*; returns return NULL; | return archive; | return NULL; | return archive; | return NULL; | return archive;
  phar_dostat (ext/phar/stream.c:485): reads data, is_temp_dir, phar, ssb; writes ssb*; returns -
  zend_hash_str_find_ptr (Zend/zend_hash.h:915): reads ht, len, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  zend_hash_str_exists (Zend/zend_hash.h:240): reads ht, len, str; writes -; returns return zend_hash_str_find(ht, str, len)!= NULL;
  phar_mount_entry (ext/phar/util.c:199): reads filename, filename_len, path, path_len, phar; writes -; returns return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return SUCCESS;
  zend_hash_find_ptr (Zend/zend_hash.h:889): reads ht, key; writes -; returns return Z_PTR_P(zv); | return NULL;
  zend_hash_num_elements (Zend/zend_hash.h:319): reads ht; writes -; returns return ht->nNumOfElements;
  zend_string_equals_literal_ci [macro]: #define zend_string_equals_literal_ci(str, c) \
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  HT_IS_INITIALIZED [macro]: #define HT_IS_INITIALIZED(ht) \
  ZEND_HASH_FOREACH_END [macro]: #define ZEND_HASH_FOREACH_END() \
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  php_stream_stat_path [macro]: #define php_stream_stat_path(path, ssb) _php_stream_stat_path((path), 0, (ssb), NULL)
  spprintf [macro]: #define spprintf zend_spprintf
  ZEND_HASH_MAP_FOREACH_STR_KEY [macro]: #define ZEND_HASH_MAP_FOREACH_STR_KEY(ht, _key) \

CALLERS (0):
```

- `get_context_at(file=ext/phar/stream.c, line=663, version=old)` →

```
phar_wrapper_unlink — ext/phar/stream.c:657 [function] static int phar_wrapper_unlink(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /*
  reads: options, url, wrapper; writes: -; returns: return 0; | return 0; | return 0; | return 0; | return 0; | return 0;

SLICE around line 663 (def-use, level 2; '>' marks the seed):
static int phar_wrapper_unlink(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {
   ...
   phar_entry_data *idata;
>  php_url *resource = phar_parse_url(wrapper, url, "rb", options);
   if(!resource) {
   ...
   }
   if(!resource->scheme || !resource->host || !resource->path) {
     php_url_free(resource);
   ...
   }
   if(!zend_string_equals_literal_ci(resource->scheme, "phar")) {
     php_url_free(resource);
   ...
   }
   ...
   const phar_archive_data *pphar = zend_hash_find_ptr(&(PHAR_G(phar_fname_map)), resource->host);
   if(PHAR_G(readonly)&&(!pphar || !pphar->is_data)) {
     php_url_free(resource);
   ...
   }
   internal_file = estrndup(ZSTR_VAL(resource->path)+ 1, ZSTR_LEN(resource->path)- 1);
   internal_file_len = ZSTR_LEN(resource->path)- 1;
   if(FAILURE == phar_get_entry_data(&idata, resource->host, internal_file, internal_file_len, "r", 0, &error, true)) {
   ...
     efree(internal_file);
     php_url_free(resource);
   ...
   }
   if(idata->internal_file->fp_refcount > 1) {
     php_stream_wrapper_log_error(wrapper, options, "phar error: \"%s\" in phar \"%s\", has open file pointers, cannot unlink", internal_file, ZSTR_VAL(resource->host));
     efree(internal_file);
     php_url_free(resource);
   ...
   }
   php_url_free(resource);
   efree(internal_file);
   ...
}

CALLEES (14):
  phar_parse_url (ext/phar/stream.c:58): reads filename, mode, options, wrapper; writes -; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  php_stream_wrapper_log_error (main/streams/streams.c:242): reads fmt, options, wrapper; writes -; returns -
  php_url_free (ext/standard/url.c:28): reads theurl; writes -; returns -
  phar_request_initialize (ext/phar/phar.c:3369): reads -; writes -; returns -
  zend_hash_find_ptr (Zend/zend_hash.h:889): reads ht, key; writes -; returns return Z_PTR_P(zv); | return NULL;
  phar_get_entry_data (ext/phar/util.c:452): reads allow_dir, error, fname, mode, path, path_len, ret, security; writes error*, ret*; returns return FAILURE; | return FAILURE; | return FAILURE; | return SUCCESS; | return FAILURE; | return SUCCESS;
  phar_entry_delref (ext/phar/phar.c:397): reads idata; writes -; returns -
  phar_entry_remove (ext/phar/phar.c:422): reads error, idata; writes idata*; returns -
  zend_string_equals_literal_ci [macro]: #define zend_string_equals_literal_ci(str, c) \
  estrndup [macro]: #define estrndup(s, length) _estrndup((s), (length) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  not defined in this repository: PHAR_G

CALLERS (0):
```

- `get_context_at(file=ext/phar/stream.c, line=733, version=old)` →

```
phar_wrapper_rename — ext/phar/stream.c:725 [function] static int phar_wrapper_rename(php_stream_wrapper *wrapper, const char *url_from, const char *url_to, int options, php_stream_context *context) /*
  reads: options, url_from, url_to, wrapper; writes: -; returns: return 0; | return 0; | return 0; | return 0; | return 0; | return 0;

SLICE around line 733 (def-use, level 2; '>' marks the seed):
static int phar_wrapper_rename(php_stream_wrapper *wrapper, const char *url_from, const char *url_to, int options, php_stream_context *context) /* {
   ...
   bool is_dir = false;
   bool is_modified = false;
   error = NULL;
>  php_url *resource_from = phar_parse_url(wrapper, url_from, "wb", options|PHP_STREAM_URL_STAT_QUIET);
   if(!resource_from) {
   ...
   }
   phar_archive_data *pfrom = phar_get_archive(ZSTR_VAL(resource_from->host), ZSTR_LEN(resource_from->host), NULL, 0, NULL);
   if(PHAR_G(readonly)&&(!pfrom || !pfrom->is_data)) {
     php_url_free(resource_from);
   ...
   }
   php_url *resource_to = phar_parse_url(wrapper, url_to, "wb", options|PHP_STREAM_URL_STAT_QUIET);
   if(!resource_to) {
     php_url_free(resource_from);
   ...
   }
   phar_archive_data *pto = phar_get_archive(ZSTR_VAL(resource_to->host), ZSTR_LEN(resource_to->host), NULL, 0, NULL);
   if(PHAR_G(readonly)&&(!pto || !pto->is_data)) {
     php_url_free(resource_from);
   ...
   }
   if(!zend_string_equals(resource_from->host, resource_to->host)) {
     php_url_free(resource_from);
   ...
   }
   if(!resource_from->scheme || !resource_from->host || !resource_from->path) {
     php_url_free(resource_from);
   ...
   }
   if(!resource_to->scheme || !resource_to->host || !resource_to->path) {
     php_url_free(resource_from);
   ...
   }
   if(!zend_string_equals_literal_ci(resource_from->scheme, "phar")) {
     php_url_free(resource_from);
   ...
   }
   if(!zend_string_equals_literal_ci(resource_to->scheme, "phar")) {
     php_url_free(resource_from);
   ...
   }
   phar_archive_data *phar = phar_get_archive(ZSTR_VAL(resource_from->host), ZSTR_LEN(resource_from->host), NULL, 0, &error);
   if(!phar) {
     php_url_free(resource_from);
   ...
   }
   if(phar->is_persistent && FAILURE == phar_copy_on_write(&phar)) {
     php_url_free(resource_from);
   ...
   }
   phar_entry_info *entry = zend_hash_str_find_ptr(&(phar->manifest), ZSTR_VAL(resource_from->path)+1, ZSTR_LEN(resource_from->path)-1);
   if(entry) {
   ...
     if(entry->is_deleted) {
       php_url_free(resource_from);
   ...
     }
     memcpy((void *)&new, (void *)entry, sizeof(phar_entry_info));
     entry->is_deleted = 1;
     entry->fp = NULL;
     ZVAL_UNDEF(&entry->metadata_tracker.val);
     entry->symlink = NULL;
     entry->tmp = NULL;
     source = entry;
     entry = zend_hash_str_update_mem(&(phar->manifest), ZSTR_VAL(resource_to->path)+1, ZSTR_LEN(resource_to->path)-1, (void **)&new, sizeof(phar_entry_info));
     entry->filename = zend_string_init(ZSTR_VAL(resource_to->path)+1, ZSTR_LEN(resource_to->path)-1, false);
     if(FAILURE == phar_copy_entry_fp(source, entry, &error)) {
       php_url_free(resource_from);
   ...
       zend_hash_del(&phar->manifest, entry->filename);
   ...
     }
     is_modified = true;
     entry->is_modified = true;
     is_dir = entry->is_dir;
   } else {
     is_dir = zend_hash_str_exists(&(phar->virtual_dirs), ZSTR_VAL(resource_from->path)+1, ZSTR_LEN(resource_from->path)-1);
     if(!is_dir) {
       php_url_free(resource_from);
   ...
     }
   }
   if(is_dir) {
     Bucket *b;
   ...
     size_t from_len = ZSTR_LEN(resource_from->path)- 1;
     size_t to_len = ZSTR_LEN(resource_to->path)- 1;
     ZEND_HASH_MAP_FOREACH_BUCKET(&phar->manifest, b)
       str_key = b->key;
       entry = Z_PTR(b->val);
       if(!entry->is_deleted && ZSTR_LEN(str_key)> from_len && memcmp(ZSTR_VAL(str_key), ZSTR_VAL(resource_from->path)+1, from_len)== 0 && IS_SLASH(ZSTR_VAL(str_key)[from_len])) {
         new_str_key = zend_string_concat2(ZSTR_VAL(resource_to->path)+ 1, to_len, ZSTR_VAL(str_key)+ from_len, ZSTR_LEN(str_key)- from_len);
         is_modified = true;
         entry->is_modified = true;
         zend_string_release(entry->filename);
         entry->filename = zend_string_copy(new_str_key);
   ...
         b->h = zend_string_hash_val(new_str_key);
         b->key = new_str_key;
       }
   ...
     zend_hash_rehash(&phar->manifest);
     ZEND_HASH_MAP_FOREACH_BUCKET(&phar->virtual_dirs, b)
       str_key = b->key;
       if(zend_string_starts_with_cstr(str_key, ZSTR_VAL(resource_from->path)+1, from_len)&&(ZSTR_LEN(str_key)== from_len || IS_SLASH(ZSTR_VAL(str_key)[from_len]))) {
         new_str_key = zend_string_concat2(ZSTR_VAL(resource_to->path)+ 1, to_len, ZSTR_VAL(str_key)+ from_len, ZSTR_LEN(str_key)- from_len);
         zend_string_release_ex(str_key, 0);
         b->h = zend_string_hash_val(new_str_key);
         b->key = new_str_key;
       }
   ...
     zend_hash_rehash(&phar->virtual_dirs);
     ZEND_HASH_MAP_FOREACH_BUCKET(&phar->mounted_dirs, b)
       str_key = b->key;
       if(zend_string_starts_with_cstr(str_key, ZSTR_VAL(resource_from->path)+1, from_len)&&(ZSTR_LEN(str_key)== from_len || IS_SLASH(ZSTR_VAL(str_key)[from_len]))) {
         new_str_key = zend_string_concat2(ZSTR_VAL(resource_to->path)+ 1, to_len, ZSTR_VAL(str_key)+ from_len, ZSTR_LEN(str_key)- from_len);
         zend_string_release_ex(str_key, 0);
         b->h = zend_string_hash_val(new_str_key);
         b->key = new_str_key;
       }
   ...
     zend_hash_rehash(&phar->mounted_dirs);
   }
   if(is_modified) {
     phar_flush(phar, &error);
     if(error) {
       php_url_free(resource_from);
   ...
     }
   }
   php_url_free(resource_from);
   ...
}

CALLEES (30):
  phar_parse_url (ext/phar/stream.c:58): reads filename, mode, options, wrapper; writes -; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  php_error_docref (main/main.c:1241): reads docref, format, type; writes -; returns -
  phar_get_archive (ext/phar/util.c:946): reads alias, alias_len, error, fname, fname_len; writes error*; returns return NULL; | return archive; | return NULL; | return archive; | return NULL; | return archive;
  php_url_free (ext/standard/url.c:28): reads theurl; writes -; returns -
  zend_string_equals (Zend/zend_string.h:395): reads s1, s2; writes -; returns return s1 == s2 || zend_string_equal_content(s1, s2);
  phar_copy_on_write (ext/phar/util.c:2056): reads pphar; writes pphar*; returns return FAILURE; | return FAILURE; | return SUCCESS;
  zend_hash_str_find_ptr (Zend/zend_hash.h:915): reads ht, len, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  zend_hash_str_exists (Zend/zend_hash.h:240): reads ht, len, str; writes -; returns return zend_hash_str_find(ht, str, len)!= NULL;
  zend_hash_del (Zend/zend_hash.c:1549): reads ht, key; writes -; returns return SUCCESS; | return FAILURE;
  phar_copy_entry_fp (ext/phar/util.c:721): reads dest, error, source; writes dest*, error*; returns return FAILURE; | return EOF; | return FAILURE; | return SUCCESS;
  zend_string_init (Zend/zend_string.h:202): reads len, persistent, str; writes -; returns return ret;
  zend_hash_str_update_mem (Zend/zend_hash.h:802): reads ht, len, pData, size, str; writes -; returns return zend_hash_str_update_ptr(ht, str, len, p);
  zend_hash_rehash (Zend/zend_hash.c:1343): reads ht; writes ht*; returns -
  zend_string_hash_val (Zend/zend_string.h:145): reads s; writes -; returns return ZSTR_H(s)? ZSTR_H(s): zend_string_hash_func(s);
  zend_string_release_ex (Zend/zend_string.h:359): reads persistent, s; writes -; returns -
  zend_string_concat2 (Zend/zend_string.c:473): reads str1, str1_len, str2, str2_len; writes -; returns return res;
  zend_string_starts_with_cstr (Zend/zend_string.h:409): reads prefix, prefix_length, str; writes -; returns return ZSTR_LEN(str)>= prefix_length && !memcmp(ZSTR_VAL(str), prefix, prefix_length);
  zend_string_copy (Zend/zend_string.h:222): reads s; writes -; returns return s;
  zend_string_release (Zend/zend_string.h:350): reads s; writes -; returns -
  phar_flush (ext/phar/phar.c:2493): reads error, phar; writes -; returns return phar_flush_ex(phar, NULL, false, error);
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  zend_string_equals_literal_ci [macro]: #define zend_string_equals_literal_ci(str, c) \
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZVAL_UNDEF [macro]: #define ZVAL_UNDEF(z) do { \
  ZEND_HASH_FOREACH_END [macro]: #define ZEND_HASH_FOREACH_END() \
  IS_SLASH [macro (1 of 2 definitions)]: #define IS_SLASH(c) ((c) == '/')
  ZEND_HASH_MAP_FOREACH_BUCKET [macro]: #define ZEND_HASH_MAP_FOREACH_BUCKET(ht, _bucket) \
  Z_PTR [macro]: #define Z_PTR(zval) (zval).value.ptr
  not defined in this repository: PHAR_G

CALLERS (0):
```

- `get_context_at(file=ext/phar/stream.c, line=746, version=old)` →

```
phar_wrapper_rename — ext/phar/stream.c:725 [function] static int phar_wrapper_rename(php_stream_wrapper *wrapper, const char *url_from, const char *url_to, int options, php_stream_context *context) /*
  reads: options, url_from, url_to, wrapper; writes: -; returns: return 0; | return 0; | return 0; | return 0; | return 0; | return 0;

SLICE around line 746 (def-use, level 2; '>' marks the seed):
static int phar_wrapper_rename(php_stream_wrapper *wrapper, const char *url_from, const char *url_to, int options, php_stream_context *context) /* {
   ...
   bool is_dir = false;
   bool is_modified = false;
   error = NULL;
   php_url *resource_from = phar_parse_url(wrapper, url_from, "wb", options|PHP_STREAM_URL_STAT_QUIET);
   ...
>  php_url *resource_to = phar_parse_url(wrapper, url_to, "wb", options|PHP_STREAM_URL_STAT_QUIET);
   if(!resource_to) {
   ...
   }
   phar_archive_data *pto = phar_get_archive(ZSTR_VAL(resource_to->host), ZSTR_LEN(resource_to->host), NULL, 0, NULL);
   if(PHAR_G(readonly)&&(!pto || !pto->is_data)) {
   ...
     php_url_free(resource_to);
   ...
   }
   if(!zend_string_equals(resource_from->host, resource_to->host)) {
   ...
     php_url_free(resource_to);
   ...
   }
   if(!resource_from->scheme || !resource_from->host || !resource_from->path) {
   ...
     php_url_free(resource_to);
   ...
   }
   if(!resource_to->scheme || !resource_to->host || !resource_to->path) {
   ...
     php_url_free(resource_to);
   ...
   }
   if(!zend_string_equals_literal_ci(resource_from->scheme, "phar")) {
   ...
     php_url_free(resource_to);
   ...
   }
   if(!zend_string_equals_literal_ci(resource_to->scheme, "phar")) {
   ...
     php_url_free(resource_to);
   ...
   }
   phar_archive_data *phar = phar_get_archive(ZSTR_VAL(resource_from->host), ZSTR_LEN(resource_from->host), NULL, 0, &error);
   if(!phar) {
   ...
     php_url_free(resource_to);
   ...
   }
   if(phar->is_persistent && FAILURE == phar_copy_on_write(&phar)) {
   ...
     php_url_free(resource_to);
   ...
   }
   phar_entry_info *entry = zend_hash_str_find_ptr(&(phar->manifest), ZSTR_VAL(resource_from->path)+1, ZSTR_LEN(resource_from->path)-1);
   if(entry) {
   ...
     if(entry->is_deleted) {
   ...
       php_url_free(resource_to);
   ...
     }
     memcpy((void *)&new, (void *)entry, sizeof(phar_entry_info));
     entry->is_deleted = 1;
   ...
     entry->tmp = NULL;
     source = entry;
     entry = zend_hash_str_update_mem(&(phar->manifest), ZSTR_VAL(resource_to->path)+1, ZSTR_LEN(resource_to->path)-1, (void **)&new, sizeof(phar_entry_info));
     entry->filename = zend_string_init(ZSTR_VAL(resource_to->path)+1, ZSTR_LEN(resource_to->path)-1, false);
     if(FAILURE == phar_copy_entry_fp(source, entry, &error)) {
   ...
       php_url_free(resource_to);
   ...
       zend_hash_del(&phar->manifest, entry->filename);
   ...
     }
     is_modified = true;
     entry->is_modified = true;
     is_dir = entry->is_dir;
   } else {
     is_dir = zend_hash_str_exists(&(phar->virtual_dirs), ZSTR_VAL(resource_from->path)+1, ZSTR_LEN(resource_from->path)-1);
     if(!is_dir) {
   ...
       php_url_free(resource_to);
   ...
     }
   }
   if(is_dir) {
     Bucket *b;
   ...
     size_t from_len = ZSTR_LEN(resource_from->path)- 1;
     size_t to_len = ZSTR_LEN(resource_to->path)- 1;
   ...
       str_key = b->key;
       entry = Z_PTR(b->val);
       if(!entry->is_deleted && ZSTR_LEN(str_key)> from_len && memcmp(ZSTR_VAL(str_key), ZSTR_VAL(resource_from->path)+1, from_len)== 0 && IS_SLASH(ZSTR_VAL(str_key)[from_len])) {
         new_str_key = zend_string_concat2(ZSTR_VAL(resource_to->path)+ 1, to_len, ZSTR_VAL(str_key)+ from_len, ZSTR_LEN(str_key)- from_len);
         is_modified = true;
         entry->is_modified = true;
         zend_string_release(entry->filename);
         entry->filename = zend_string_copy(new_str_key);
   ...
         b->h = zend_string_hash_val(new_str_key);
         b->key = new_str_key;
       }
   ...
     ZEND_HASH_MAP_FOREACH_BUCKET(&phar->virtual_dirs, b)
       str_key = b->key;
       if(zend_string_starts_with_cstr(str_key, ZSTR_VAL(resource_from->path)+1, from_len)&&(ZSTR_LEN(str_key)== from_len || IS_SLASH(ZSTR_VAL(str_key)[from_len]))) {
         new_str_key = zend_string_concat2(ZSTR_VAL(resource_to->path)+ 1, to_len, ZSTR_VAL(str_key)+ from_len, ZSTR_LEN(str_key)- from_len);
         zend_string_release_ex(str_key, 0);
         b->h = zend_string_hash_val(new_str_key);
         b->key = new_str_key;
       }
   ...
     ZEND_HASH_MAP_FOREACH_BUCKET(&phar->mounted_dirs, b)
       str_key = b->key;
       if(zend_string_starts_with_cstr(str_key, ZSTR_VAL(resource_from->path)+1, from_len)&&(ZSTR_LEN(str_key)== from_len || IS_SLASH(ZSTR_VAL(str_key)[from_len]))) {
         new_str_key = zend_string_concat2(ZSTR_VAL(resource_to->path)+ 1, to_len, ZSTR_VAL(str_key)+ from_len, ZSTR_LEN(str_key)- from_len);
         zend_string_release_ex(str_key, 0);
         b->h = zend_string_hash_val(new_str_key);
         b->key = new_str_key;
   ...
       }
   }
   if(is_modified) {
   ...
     if(error) {
   ...
       php_url_free(resource_to);
   ...
     }
   }
   ...
   php_url_free(resource_to);
   ...
}

CALLEES (30):
  phar_parse_url (ext/phar/stream.c:58): reads filename, mode, options, wrapper; writes -; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  php_error_docref (main/main.c:1241): reads docref, format, type; writes -; returns -
  phar_get_archive (ext/phar/util.c:946): reads alias, alias_len, error, fname, fname_len; writes error*; returns return NULL; | return archive; | return NULL; | return archive; | return NULL; | return archive;
  php_url_free (ext/standard/url.c:28): reads theurl; writes -; returns -
  zend_string_equals (Zend/zend_string.h:395): reads s1, s2; writes -; returns return s1 == s2 || zend_string_equal_content(s1, s2);
  phar_copy_on_write (ext/phar/util.c:2056): reads pphar; writes pphar*; returns return FAILURE; | return FAILURE; | return SUCCESS;
  zend_hash_str_find_ptr (Zend/zend_hash.h:915): reads ht, len, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  zend_hash_str_exists (Zend/zend_hash.h:240): reads ht, len, str; writes -; returns return zend_hash_str_find(ht, str, len)!= NULL;
  zend_hash_del (Zend/zend_hash.c:1549): reads ht, key; writes -; returns return SUCCESS; | return FAILURE;
  phar_copy_entry_fp (ext/phar/util.c:721): reads dest, error, source; writes dest*, error*; returns return FAILURE; | return EOF; | return FAILURE; | return SUCCESS;
  zend_string_init (Zend/zend_string.h:202): reads len, persistent, str; writes -; returns return ret;
  zend_hash_str_update_mem (Zend/zend_hash.h:802): reads ht, len, pData, size, str; writes -; returns return zend_hash_str_update_ptr(ht, str, len, p);
  zend_hash_rehash (Zend/zend_hash.c:1343): reads ht; writes ht*; returns -
  zend_string_hash_val (Zend/zend_string.h:145): reads s; writes -; returns return ZSTR_H(s)? ZSTR_H(s): zend_string_hash_func(s);
  zend_string_release_ex (Zend/zend_string.h:359): reads persistent, s; writes -; returns -
  zend_string_concat2 (Zend/zend_string.c:473): reads str1, str1_len, str2, str2_len; writes -; returns return res;
  zend_string_starts_with_cstr (Zend/zend_string.h:409): reads prefix, prefix_length, str; writes -; returns return ZSTR_LEN(str)>= prefix_length && !memcmp(ZSTR_VAL(str), prefix, prefix_length);
  zend_string_copy (Zend/zend_string.h:222): reads s; writes -; returns return s;
  zend_string_release (Zend/zend_string.h:350): reads s; writes -; returns -
  phar_flush (ext/phar/phar.c:2493): reads error, phar; writes -; returns return phar_flush_ex(phar, NULL, false, error);
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  zend_string_equals_literal_ci [macro]: #define zend_string_equals_literal_ci(str, c) \
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZVAL_UNDEF [macro]: #define ZVAL_UNDEF(z) do { \
  ZEND_HASH_FOREACH_END [macro]: #define ZEND_HASH_FOREACH_END() \
  IS_SLASH [macro (1 of 2 definitions)]: #define IS_SLASH(c) ((c) == '/')
  ZEND_HASH_MAP_FOREACH_BUCKET [macro]: #define ZEND_HASH_MAP_FOREACH_BUCKET(ht, _bucket) \
  Z_PTR [macro]: #define Z_PTR(zval) (zval).value.ptr
  not defined in this repository: PHAR_G

CALLERS (0):
```

### Turn 4  _(tok 21777+110, stop=tool_use)_

**Reasoning:** We have confirmed. Need maybe use get_callers too to ensure complete. We should call get_callers for phar_parse_url maybe.

- `get_callers(name=phar_parse_url, version=old, limit=50)` →

```
{
  "name": "phar_parse_url",
  "version": "old",
  "callers": [
    {
      "caller": "phar_wrapper_open_dir",
      "file": "ext/phar/dirstream.c",
      "line": 250
    },
    {
      "caller": "phar_wrapper_mkdir",
      "file": "ext/phar/dirstream.c",
      "line": 360
    },
    {
      "caller": "phar_wrapper_rmdir",
      "file": "ext/phar/dirstream.c",
      "line": 484
    },
    {
      "caller": "phar_wrapper_open_url",
      "file": "ext/phar/stream.c",
      "line": 169
    },
    {
      "caller": "phar_wrapper_stat",
      "file": "ext/phar/stream.c",
      "line": 560
    },
    {
      "caller": "phar_wrapper_unlink",
      "file": "ext/phar/stream.c",
      "line": 663
    },
    {
      "caller": "phar_wrapper_rename",
      "file": "ext/phar/stream.c",
      "line": 733
    },
    {
      "caller": "phar_wrapper_rename",
      "file": "ext/phar/stream.c",
      "line": 746
    }
  ]
}
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 22215+421, stop=tool_use, forced)_

**Reasoning:** The results are complete. There are exactly 7 unique callers, with `phar_wrapper_rename` appearing twice (at lines 733 and 746). Let me submit.

The unique enclosing functions that call `phar_parse_url`:

1. phar_wrapper_open_dir — ext/phar/dirstream.c
2. phar_wrapper_mkdir — ext/phar/dirstream.c
3. phar_wrapper_rmdir — ext/phar/dirstream.c
4. phar_wrapper_open_url — ext/phar/stream.c
5. phar_wrapper_stat — ext/phar/stream.c
6. phar_wrapper_unlink — ext/phar/stream.c
7. phar_wrapper_rename — ext/phar/stream.c

phar_wrapper_rename has two call sites. But the question asks for "every function" - so just the function name and file.

- **submit_callers** → `{"callers": [{"function": "phar_wrapper_open_dir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_stat", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_unlink", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_rename", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2309+102, stop=tool_use)_

**Reasoning:** The user wants me to find all callers of `phar_parse_url` in the repository. Let me start by looking at the function's definition and its callers.

- `get_callers(name=phar_parse_url, limit=100)` →

```
{
  "name": "phar_parse_url",
  "version": "old",
  "callers": [
    {
      "caller": "phar_wrapper_open_dir",
      "file": "ext/phar/dirstream.c",
      "line": 250
    },
    {
      "caller": "phar_wrapper_mkdir",
      "file": "ext/phar/dirstream.c",
      "line": 360
    },
    {
      "caller": "phar_wrapper_rmdir",
      "file": "ext/phar/dirstream.c",
      "line": 484
    },
    {
      "caller": "phar_wrapper_open_url",
      "file": "ext/phar/stream.c",
      "line": 169
    },
    {
      "caller": "phar_wrapper_stat",
      "file": "ext/phar/stream.c",
      "line": 560
    },
    {
      "caller": "phar_wrapper_unlink",
      "file": "ext/phar/stream.c",
      "line": 663
    },
    {
      "caller": "phar_wrapper_rename",
      "file": "ext/phar/stream.c",
      "line": 733
    },
    {
      "caller": "phar_wrapper_rename",
      "file": "ext/phar/stream.c",
      "line": 746
    }
  ]
}
```

### Turn 2  _(tok 2741+106, stop=tool_use)_

**Reasoning:** I found the callers. Let me also check the "work" version to make sure I have the complete list.

- `get_callers(name=phar_parse_url, limit=100, rev=work)` →

```
{
  "name": "phar_parse_url",
  "version": "old",
  "callers": [
    {
      "caller": "phar_wrapper_open_dir",
      "file": "ext/phar/dirstream.c",
      "line": 250
    },
    {
      "caller": "phar_wrapper_mkdir",
      "file": "ext/phar/dirstream.c",
      "line": 360
    },
    {
      "caller": "phar_wrapper_rmdir",
      "file": "ext/phar/dirstream.c",
      "line": 484
    },
    {
      "caller": "phar_wrapper_open_url",
      "file": "ext/phar/stream.c",
      "line": 169
    },
    {
      "caller": "phar_wrapper_stat",
      "file": "ext/phar/stream.c",
      "line": 560
    },
    {
      "caller": "phar_wrapper_unlink",
      "file": "ext/phar/stream.c",
      "line": 663
    },
    {
      "caller": "phar_wrapper_rename",
      "file": "ext/phar/stream.c",
      "line": 733
    },
    {
      "caller": "phar_wrapper_rename",
      "file": "ext/phar/stream.c",
      "line": 746
    }
  ]
}
```

### Turn 3  _(tok 3177+520, stop=tool_use)_

**Reasoning:** Both versions agree. The callers are:

1. `phar_wrapper_open_dir` — `ext/phar/dirstream.c`
2. `phar_wrapper_mkdir` — `ext/phar/dirstream.c`
3. `phar_wrapper_rmdir` — `ext/phar/dirstream.c`
4. `phar_wrapper_open_url` — `ext/phar/stream.c`
5. `phar_wrapper_stat` — `ext/phar/stream.c`
6. `phar_wrapper_unlink` — `ext/phar/stream.c`
7. `phar_wrapper_rename` — `ext/phar/stream.c` (two call sites)

So the unique enclosing functions are:
- `phar_wrapper_open_dir` (ext/phar/dirstream.c)
- `phar_wrapper_mkdir` (ext/phar/dirstream.c)
- `phar_wrapper_rmdir` (ext/phar/dirstream.c)
- `phar_wrapper_open_url` (ext/phar/stream.c)
- `phar_wrapper_stat` (ext/phar/stream.c)
- `phar_wrapper_unlink` (ext/phar/stream.c)
- `phar_wrapper_rename` (ext/phar/stream.c)

That's 7 unique functions. All are confirmed. Let me submit.

- **submit_callers** → `{"callers": [{"function": "phar_wrapper_open_dir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_stat", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_unlink", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_rename", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

