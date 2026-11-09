# Impact-analysis transcript — php-src @ f2b371e747d2 — anthropic:claude-haiku-5-5

- target: `phar_parse_url` (ext/phar/stream.c), arity 4->5
- truth: [['ext/phar/dirstream.c', 'phar_wrapper_mkdir'], ['ext/phar/dirstream.c', 'phar_wrapper_open_dir'], ['ext/phar/dirstream.c', 'phar_wrapper_rmdir'], ['ext/phar/stream.c', 'phar_wrapper_open_url'], ['ext/phar/stream.c', 'phar_wrapper_rename'], ['ext/phar/stream.c', 'phar_wrapper_stat'], ['ext/phar/stream.c', 'phar_wrapper_unlink']]

## Self-navigation arm

### Turn 1  _(tok 1214+96, stop=tool_use)_

**Reasoning:** I'm searching the repo for every reference to phar_parse_url.



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

### Turn 2  _(tok 1949+933, stop=tool_use)_

**Reasoning:** I need the enclosing function names for each call site, so I'll read the code around those lines in dirstream.c and stream.c.



**Says:** I need the enclosing function for each call site, so I'll read the surrounding code.

- `read_file(path=ext/phar/dirstream.c, version=old, start_line=240, end_line=255)` →

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

- `read_file(path=ext/phar/dirstream.c, version=old, start_line=345, end_line=365)` →

```
ext/phar/dirstream.c lines 345-365 of 580
  345| 	zend_string *arch = phar_split_fname(url_from, strlen(url_from), NULL, 2, 2);
  346| 	if (!arch) {
  347| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\", no phar archive specified", url_from);
  348| 		return 0;
  349| 	}
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

- `read_file(path=ext/phar/dirstream.c, version=old, start_line=475, end_line=490)` →

```
ext/phar/dirstream.c lines 475-490 of 580
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

- `read_file(path=ext/phar/stream.c, version=old, start_line=160, end_line=172)` →

```
ext/phar/stream.c lines 160-172 of 947
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
```

- `read_file(path=ext/phar/stream.c, version=old, start_line=545, end_line=562)` →

```
ext/phar/stream.c lines 545-562 of 947
  545| 
  546| 	phar_dostat(data->phar, data->internal_file, ssb, false);
  547| 	return 0;
  548| }
  549| /* }}} */
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
```

- `read_file(path=ext/phar/stream.c, version=old, start_line=650, end_line=665)` →

```
ext/phar/stream.c lines 650-665 of 947
  650| 	return FAILURE;
  651| }
  652| /* }}} */
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
```

- `read_file(path=ext/phar/stream.c, version=old, start_line=715, end_line=750)` →

```
ext/phar/stream.c lines 715-750 of 947
  715| 	efree(internal_file);
  716| 	phar_entry_remove(idata, &error);
  717| 	if (error) {
  718| 		php_stream_wrapper_log_error(wrapper, options, "%s", error);
  719| 		efree(error);
  720| 	}
  721| 	return 1;
  722| }
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

### Turn 3  _(tok 5826+278, stop=tool_use)_

**Reasoning:** I need the enclosing function names for lines 360 and 484 in dirstream.c. Line 360 is probably inside phar_wrapper_mkdir, which starts before line 345, and line 484 looks like phar_wrapper_rmdir. I'll grep dirstream.c for function definitions to confirm both.



**Says:** Two call sites in dirstream.c (lines 360 and 484) still need their enclosing function names confirmed. I'll check the function headers.

- `grep(pattern=^(static |)[a-z_ ]*\*?phar_wrapper_[a-z_]*\(, version=old, path_glob=ext/phar/dirstream.c)` →

```
3 matches
ext/phar/dirstream.c:246:php_stream *phar_wrapper_open_dir(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_
ext/phar/dirstream.c:338:int phar_wrapper_mkdir(php_stream_wrapper *wrapper, const char *url_from, int mode, int options, php_stream_context *context) /* {{{ */
ext/phar/dirstream.c:464:int phar_wrapper_rmdir(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
```

### Turn 4  _(tok 6344+261, stop=tool_use)_

**Reasoning:** I'm checking the phar wrapper functions: mkdir and rmdir at lines 360 and 484, and stat, unlink, and rename at 560, 663, and 733/746. I still need the name of the function around line 169 in stream.c, since its header starts at 160, and I've read lines 150 to 160.



- `read_file(path=ext/phar/stream.c, version=old, start_line=155, end_line=160)` →

```
ext/phar/stream.c lines 155-160 of 947
  155| 
  156| /**
  157|  * used for fopen('phar://...') and company
  158|  */
  159| static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /* {{{ */
  160| {
```

### Turn 5  _(tok 6756+715, stop=tool_use)_

**Reasoning:** I'm checking whether any other callers exist outside the phar_parse_url matches, including tests and macros or function pointers, and the grep already covers the whole repo. Next I'm listing the enclosing functions in ext/phar/dirstream.c: phar_wrapper_open_dir, phar_wrapper_mkdir, and phar_wrapper_rmdir, with their line numbers.

I'm now listing the stream.c functions: phar_wrapper_open_url, phar_wrapper_stat, phar_wrapper_unlink, and phar_wrapper_rename at two lines. Rename appears once in the list, so the count comes to seven distinct functions, three in dirstream.c and four in stream.c.



**Says:** The search found 12 matches for `phar_parse_url`. Excluding the definition, the prototypes in `dirstream.h` and `stream.h`, and the comment in `phar.c`, that leaves 7 call sites. Each one sits in a different function, except `phar_wrapper_rename`, which has two.

- **submit_callers** → `{"callers": [{"function": "phar_wrapper_open_dir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_stat", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_unlink", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_rename", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3749+228, stop=tool_use)_

**Reasoning:** I'm going to pull up the callers of phar_parse_url first, and run a grep for it too so nothing gets missed.



- `get_callers(name=phar_parse_url, limit=200, rev=None)` →

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

- `grep(pattern=phar_parse_url, version=old, max_results=200)` →

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

### Turn 2  _(tok 5101+636, stop=tool_use)_

**Reasoning:** I'm listing where the phar wrapper functions are called from: dirstream.c at lines 250, 360 and 484, stream.c at 169, 560, 663, and 733 and 746 for the rename calls. The grep covers all eight call sites.

I'm checking the enclosing functions for the dirstream calls and confirming the callgraph, then wondering whether a whole-repo grep rules out callers elsewhere. The phar.c:2200 hit is just a comment. The stream.c definition at line 58 doesn't count, and phar_wrapper_rename shows up twice but is one function, so I'll list it once.



- **submit_callers** → `{"callers": [{"function": "phar_wrapper_open_dir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_stat", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_unlink", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_rename", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3201+76, stop=tool_use)_

- `get_callers(name=phar_parse_url, limit=200)` →

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

### Turn 2  _(tok 3716+334, stop=tool_use)_

**Reasoning:** The tool reports version "old", which is the parent of the revision it resolved, so the callers are on the older version. Since the question is about the current repo state, I'll also check with version "work" to be safe.



**Says:** The result came from the "old" version (parent of the server's commit). I'll check the working tree too, since that's the state that matters for the signature change.

- `get_callers(name=phar_parse_url, limit=200, rev=HEAD)` →

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

- `get_callers(name=phar_parse_url, limit=200, rev=work)` →

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

### Turn 3  _(tok 4976+467, stop=tool_use)_

**Reasoning:** I'm checking whether the work version also reports "old", which might mean the tool defaults to HEAD or labels versions oddly. I want to confirm with resolve_symbol and get_neighborhood on phar_wrapper_rename whether the definition and callers match for the work version. I'll also run get_context_at on a caller line with the work version to see whether it agrees.

I'm questioning the tool's "rev" argument, since get_callers may not accept a version parameter and rev="work" could be read as a nonexistent git revision, though it returned results anyway. I'll try get_neighborhood on phar_wrapper_rename for the work version to see if it lists callers.



**Says:** Both queries returned the same list, but they're labeled "old", so I want to confirm the working-tree state directly before trusting it.

- `get_neighborhood(name=phar_parse_url, rev=work)` →

```
phar_parse_url — ext/phar/stream.c:58 [function] php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options) /*
  reads: filename, mode, options, wrapper; writes: -; returns: return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;

CALLEES (16):
  php_stream_wrapper_log_error (main/streams/streams.c:242): reads fmt, options, wrapper; writes -; returns -
  phar_split_fname_ex (ext/phar/phar.c:2202): reads entry, error, executable, filename, filename_len, for_create; writes entry*, error*; returns return NULL; | return NULL; | return arch;
  php_url_free (ext/standard/url.c:28): reads theurl; writes -; returns -
  phar_open_from_filename (ext/phar/phar.c:1527): reads alias, error, fname, fname_len, options, pphar; writes error*; returns return SUCCESS; | return FAILURE; | return FAILURE; | return FAILURE; | return ret;
  phar_copy_on_write (ext/phar/util.c:2056): reads pphar; writes pphar*; returns return FAILURE; | return FAILURE; | return SUCCESS;
  zend_hash_find_ptr (Zend/zend_hash.h:889): reads ht, key; writes -; returns return Z_PTR_P(zv); | return NULL;
  strncasecmp [macro (1 of 2 definitions)]: #define strncasecmp(s1, s2, n) _strnicmp(s1, s2, n)
  ecalloc [macro]: #define ecalloc(nmemb, size) _ecalloc((nmemb), (size) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZSTR_INIT_LITERAL [macro]: #define ZSTR_INIT_LITERAL(s, persistent) (zend_string_init(("" s), sizeof(s) - 1, (persistent)))
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  spprintf [macro]: #define spprintf zend_spprintf
  HT_IS_INITIALIZED [macro]: #define HT_IS_INITIALIZED(ht) \
  not defined in this repository: phar_open_or_create_filename, PHAR_G

CALLERS (8):
  phar_wrapper_open_dir (ext/phar/dirstream.c:250): php_url *resource = phar_parse_url(wrapper, path, mode, options);
  phar_wrapper_mkdir (ext/phar/dirstream.c:360): if ((resource = phar_parse_url(wrapper, url_from, "w", options)) == NULL) {
  phar_wrapper_rmdir (ext/phar/dirstream.c:484): php_url *resource = phar_parse_url(wrapper, url, "w", options);
  phar_wrapper_open_url (ext/phar/stream.c:169): php_url *resource = phar_parse_url(wrapper, path, mode, options);
  phar_wrapper_stat (ext/phar/stream.c:560): php_url *resource = phar_parse_url(wrapper, url, "r", flags|PHP_STREAM_URL_STAT_QUIET);
  phar_wrapper_unlink (ext/phar/stream.c:663): php_url *resource = phar_parse_url(wrapper, url, "rb", options);
  phar_wrapper_rename (ext/phar/stream.c:733): php_url *resource_from = phar_parse_url(wrapper, url_from, "wb", options|PHP_STREAM_URL_STAT_QUIET);
  phar_wrapper_rename (ext/phar/stream.c:746): php_url *resource_to = phar_parse_url(wrapper, url_to, "wb", options|PHP_STREAM_URL_STAT_QUIET);
  ... only the first 8 of 10 reference sites were followed
```

- `resolve_symbol(name=phar_parse_url, rev=work)` →

```
{
  "resolved": true,
  "name": "phar_parse_url",
  "version": "old",
  "file": "ext/phar/stream.c",
  "line": 58,
  "kind": "function",
  "signature": "php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options) /*",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 4  _(tok 7158+1207, stop=tool_use)_

**Reasoning:** The neighborhood reports that only 8 of 10 reference sites were followed, and get_callers returned 8 entries, with phar_wrapper_rename appearing twice. I'm wondering whether the 10 includes the definition site or a prototype, or whether a couple of calls were simply left out of the listing.

I'm trying to account for the 10th reference site, since get_callers only gave 8. I'll check the phar_wrapper functions in stream.c and dirstream.c for extra calls, and consider whether the definition or a prototype might be counted.



**Says:** The neighborhood view reports 10 reference sites but only 8 callers were followed, so two call sites may be unaccounted for. I'll inspect the caller bodies for additional calls.

- `get_function_source(name=phar_wrapper_rename, rev=work)` →

```
phar_wrapper_rename (function, old version) — ext/phar/stream.c:725-945
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
  751| 	}
  752| 
  753| 	phar_archive_data *pto = phar_get_archive(ZSTR_VAL(resource_to->host), ZSTR_LEN(resource_to->host), NULL, 0, NULL);
  754| 	if (PHAR_G(readonly) && (!pto || !pto->is_data)) {
  755| 		php_url_free(resource_from);
  756| 		php_url_free(resource_to);
  757| 		php_error_docref(NULL, E_WARNING, "phar error: Write operations disabled by the php.ini setting phar.readonly");
  758| 		return 0;
  759| 	}
  760| 
  761| 	if (!zend_string_equals(resource_from->host, resource_to->host)) {
  762| 		php_url_free(resource_from);
  763| 		php_url_free(resource_to);
  764| 		php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\", not within the same phar archive", url_from, url_to);
  765| 		return 0;
  766| 	}
  767| 
  768| 	/* we must have at the very least phar://alias.phar/internalfile.php */
  769| 	if (!resource_from->scheme || !resource_from->host || !resource_from->path) {
  770| 		php_url_free(resource_from);
  771| 		php_url_free(resource_to);
  772| 		php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\": invalid url \"%s\"", url_from, url_to, url_from);
  773| 		return 0;
  774| 	}
  775| 
  776| 	if (!resource_to->scheme || !resource_to->host || !resource_to->path) {
  777| 		php_url_free(resource_from);
  778| 		php_url_free(resource_to);
  779| 		php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\": invalid url \"%s\"", url_from, url_to, url_to);
  780| 		return 0;
  781| 	}
  782| 
  783| 	if (!zend_string_equals_literal_ci(resource_from->scheme, "phar")) {
  784| 		php_url_free(resource_from);
  785| 		php_url_free(resource_to);
  786| 		php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\": not a phar stream url \"%s\"", url_from, url_to, url_from);
  787| 		return 0;
  788| 	}
  789| 
  790| 	if (!zend_string_equals_literal_ci(resource_to->scheme, "phar")) {
  791| 		php_url_free(resource_from);
  792| 		php_url_free(resource_to);
  793| 		php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\": not a phar stream url \"%s\"", url_from, url_to, url_to);
  794| 		return 0;
  795| 	}
  796| 
  797| 	phar_archive_data *phar = phar_get_archive(ZSTR_VAL(resource_from->host), ZSTR_LEN(resource_from->host), NULL, 0, &error);
  798| 	if (!phar) {
  799| 		php_url_free(resource_from);
  800| 		php_url_free(resource_to);
  801| 		php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\": %s", url_from, url_to, error);
  802| 		efree(error);
  803| 		return 0;
  804| 	}
  805| 
  806| 	if (phar->is_persistent && FAILURE == phar_copy_on_write(&phar)) {
  807| 		php_url_free(resource_from);
  808| 		php_url_free(resource_to);
  809| 		php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\": could not make cached phar writeable", url_from, url_to);
  810| 		return 0;
  811| 	}
  812| 
  813| 	phar_entry_info *entry = zend_hash_str_find_ptr(&(phar->manifest), ZSTR_VAL(resource_from->path)+1, ZSTR_LEN(resource_from->path)-1);
  814| 	if (entry) {
  815| 		phar_entry_info new, *source;
  816| 
  817| 		/* perform rename magic */
  818| 		if (entry->is_deleted) {
  819| 			php_url_free(resource_from);
  820| 			php_url_free(resource_to);
  821| 			php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\" from extracted phar archive, source has been deleted", url_from, url_to);
  822| 			return 0;
  823| 		}
  824| 		/* transfer all data over to the new entry */
  825| 		memcpy((void *) &new, (void *) entry, sizeof(phar_entry_info));
  826| 		/* mark the old one for deletion */
  827| 		entry->is_deleted = 1;
  828| 		entry->fp = NULL;
  829| 		ZVAL_UNDEF(&entry->metadata_tracker.val);
  830| 		entry->symlink = NULL;
  831| 		entry->tmp = NULL;
  832| 		source = entry;
  833| 
  834| 		/* add to the manifest, and then store the pointer to the new guy in entry
  835| 		 * if it already exists, we overwrite the destination like what copy('phar://...', 'phar://...') does. */
  836| 		entry = zend_hash_str_update_mem(&(phar->manifest), ZSTR_VAL(resource_to->path)+1, ZSTR_LEN(resource_to->path)-1, (void **)&new, sizeof(phar_entry_info));
  837| 
  838| 		entry->filename = zend_string_init(ZSTR_VAL(resource_to->path)+1, ZSTR_LEN(resource_to->path)-1, false);
  839| 		if (FAILURE == phar_copy_entry_fp(source, entry, &error)) {
  840| 			php_url_free(resource_from);
  841| 			php_url_free(resource_to);
  842| 			php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\": %s", url_from, url_to, error);
  843| 			efree(error);
  844| 			zend_hash_del(&phar->manifest, entry->filename);
  845| 			return 0;
  846| 		}
  847| 		is_modified = true;
  848| 		entry->is_modified = true;
  849| 		is_dir = entry->is_dir;
  850| 	} else {
  851| 		is_dir = zend_hash_str_exists(&(phar->virtual_dirs), ZSTR_VAL(resource_from->path)+1, ZSTR_LEN(resource_from->path)-1);
  852| 		if (!is_dir) {
  853| 			/* file does not exist */
  854| 			php_url_free(resource_from);
  855| 			php_url_free(resource_to);
  856| 			php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\" from extracted phar archive, source does not exist", url_from, url_to);
  857| 			return 0;
  858| 
  859| 		}
  860| 	}
  861| 
  862| 	/* Rename directory. Update all nested paths */
  863| 	if (is_dir) {
  864| 		Bucket *b;
  865| 		zend_string *str_key;
  866| 		zend_string *new_str_key;
  867| 		size_t from_len = ZSTR_LEN(resource_from->path) - 1;
  868| 		size_t to_len = ZSTR_LEN(resource_to->path) - 1;
  869| 
  870| 		ZEND_HASH_MAP_FOREACH_BUCKET(&phar->manifest, b) {
  871| 			str_key = b->key;
  872| 			entry = Z_PTR(b->val);
  873| 			if (!entry->is_deleted &&
  874| 				ZSTR_LEN(str_key) > from_len &&
  875| 				memcmp(ZSTR_VAL(str_key), ZSTR_VAL(resource_from->path)+1, from_len) == 0 &&
  876| 				IS_SLASH(ZSTR_VAL(str_key)[from_len])) {
  877| 
  878| 				new_str_key = zend_string_concat2(
  879| 					ZSTR_VAL(resource_to->path) + 1, to_len,
  880| 					ZSTR_VAL(str_key) + from_len, ZSTR_LEN(str_key) - from_len
  881| 				);
  882| 
  883| 				is_modified = true;
  884| 				entry->is_modified = true;
  885| 				zend_string_release(entry->filename);
  886| 				entry->filename = zend_string_copy(new_str_key);
  887| 
  888| 				zend_string_release_ex(str_key, 0);
  889| 				b->h = zend_string_hash_val(new_str_key);
  890| 				b->key = new_str_key;
  891| 			}
  892| 		} ZEND_HASH_FOREACH_END();
  893| 		zend_hash_rehash(&phar->manifest);
  894| 
  895| 		ZEND_HASH_MAP_FOREACH_BUCKET(&phar->virtual_dirs, b) {
  896| 			str_key = b->key;
  897| 			if (zend_string_starts_with_cstr(str_key, ZSTR_VAL(resource_from->path)+1, from_len) &&
  898| 				(ZSTR_LEN(str_key) == from_len || IS_SLASH(ZSTR_VAL(str_key)[from_len]))) {
  899| 
  900| 				new_str_key = zend_string_concat2(
  901| 					ZSTR_VAL(resource_to->path) + 1, to_len,
  902| 					ZSTR_VAL(str_key) + from_len, ZSTR_LEN(str_key) - from_len
  903| 				);
  904| 
  905| 				zend_string_release_ex(str_key, 0);
  906| 				b->h = zend_string_hash_val(new_str_key);
  907| 				b->key = new_str_key;
  908| 			}
  909| 		} ZEND_HASH_FOREACH_END();
  910| 		zend_hash_rehash(&phar->virtual_dirs);
  911| 
  912| 		ZEND_HASH_MAP_FOREACH_BUCKET(&phar->mounted_dirs, b) {
  913| 			str_key = b->key;
  914| 			if (zend_string_starts_with_cstr(str_key, ZSTR_VAL(resource_from->path)+1, from_len) &&
  915| 				(ZSTR_LEN(str_key) == from_len || IS_SLASH(ZSTR_VAL(str_key)[from_len]))) {
  916| 
  917| 				new_str_key = zend_string_concat2(
  918| 					ZSTR_VAL(resource_to->path) + 1, to_len,
  919| 					ZSTR_VAL(str_key) + from_len, ZSTR_LEN(str_key) - from_len
  920| 				);
  921| 
  922| 				zend_string_release_ex(str_key, 0);
  923| 				b->h = zend_string_hash_val(new_str_key);
  924| 				b->key = new_str_key;
  925| 			}
  926| 		} ZEND_HASH_FOREACH_END();
  927| 		zend_hash_rehash(&phar->mounted_dirs);
  928| 	}
  929| 
  930| 	if (is_modified) {
  931| 		phar_flush(phar, &error);
  932| 		if (error) {
  933| 			php_url_free(resource_from);
  934| 			php_url_free(resource_to);
  935| 			php_error_docref(NULL, E_WARNING, "phar error: cannot rename \"%s\" to \"%s\": %s", url_from, url_to, error);
  936| 			efree(error);
  937| 			return 0;
  938| 		}
  939| 	}
  940| 
  941| 	php_url_free(resource_from);
  942| 	php_url_free(resource_to);
  943| 
  944| 	return 1;
  945| }
```

- `get_function_source(name=phar_wrapper_open_dir, rev=work)` →

```
phar_wrapper_open_dir (function, old version) — ext/phar/dirstream.c:246-332
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
  256| 	/* we must have at the very least phar://alias.phar/ */
  257| 	if (!resource->scheme || !resource->host || !resource->path) {
  258| 		if (resource->host && !resource->path) {
  259| 			php_stream_wrapper_log_error(wrapper, options, "phar error: no directory in \"%s\", must have at least phar://%s/ for root directory (always use full path to a new phar)", path, ZSTR_VAL(resource->host));
  260| 			php_url_free(resource);
  261| 			return NULL;
  262| 		}
  263| 		php_url_free(resource);
  264| 		php_stream_wrapper_log_error(wrapper, options, "phar error: invalid url \"%s\", must have at least phar://%s/", path, path);
  265| 		return NULL;
  266| 	}
  267| 
  268| 	if (!zend_string_equals_literal_ci(resource->scheme, "phar")) {
  269| 		php_url_free(resource);
  270| 		php_stream_wrapper_log_error(wrapper, options, "phar error: not a phar url \"%s\"", path);
  271| 		return NULL;
  272| 	}
  273| 
  274| 	phar_request_initialize();
  275| 
  276| 	const phar_archive_data *phar = phar_get_archive(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error);
  277| 	if (!phar) {
  278| 		if (error) {
  279| 			php_stream_wrapper_log_error(wrapper, options, "%s", error);
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
  331| 	return NULL;
  332| }
```

- `get_function_source(name=phar_wrapper_mkdir, rev=work)` →

```
phar_wrapper_mkdir (function, old version) — ext/phar/dirstream.c:338-458
  338| int phar_wrapper_mkdir(php_stream_wrapper *wrapper, const char *url_from, int mode, int options, php_stream_context *context) /* {{{ */
  339| {
  340| 	phar_entry_info entry;
  341| 	char *error;
  342| 	php_url *resource = NULL;
  343| 
  344| 	/* pre-readonly check, we need to know if this is a data phar */
  345| 	zend_string *arch = phar_split_fname(url_from, strlen(url_from), NULL, 2, 2);
  346| 	if (!arch) {
  347| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\", no phar archive specified", url_from);
  348| 		return 0;
  349| 	}
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
  366| 		php_url_free(resource);
  367| 		php_stream_wrapper_log_error(wrapper, options, "phar error: invalid url \"%s\"", url_from);
  368| 		return 0;
  369| 	}
  370| 
  371| 	if (!zend_string_equals_literal_ci(resource->scheme, "phar")) {
  372| 		php_url_free(resource);
  373| 		php_stream_wrapper_log_error(wrapper, options, "phar error: not a phar stream url \"%s\"", url_from);
  374| 		return 0;
  375| 	}
  376| 
  377| 	phar = phar_get_archive(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error);
  378| 	if (!phar) {
  379| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", error retrieving phar information: %s", ZSTR_VAL(resource->path) + 1, ZSTR_VAL(resource->host), error);
  380| 		efree(error);
  381| 		php_url_free(resource);
  382| 		return 0;
  383| 	}
  384| 
  385| 	phar_entry_info *e = phar_get_entry_info_dir(phar, ZSTR_VAL(resource->path) + 1, ZSTR_LEN(resource->path) - 1, 2, &error, true);
  386| 	if (e) {
  387| 		/* directory exists, or is a subdirectory of an existing file */
  388| 		if (e->is_temp_dir) {
  389| 			zend_string_efree(e->filename);
  390| 			efree(e);
  391| 		}
  392| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", directory already exists", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host));
  393| 		php_url_free(resource);
  394| 		return 0;
  395| 	}
  396| 
  397| 	if (error) {
  398| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", %s", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host), error);
  399| 		efree(error);
  400| 		php_url_free(resource);
  401| 		return 0;
  402| 	}
  403| 
  404| 	if (phar_get_entry_info_dir(phar, ZSTR_VAL(resource->path) + 1, ZSTR_LEN(resource->path) - 1, 0, &error, true)) {
  405| 		/* entry exists as a file */
  406| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", file already exists", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host));
  407| 		php_url_free(resource);
  408| 		return 0;
  409| 	}
  410| 
  411| 	if (error) {
  412| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", %s", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host), error);
  413| 		efree(error);
  414| 		php_url_free(resource);
  415| 		return 0;
  416| 	}
  417| 
  418| 	memset((void *) &entry, 0, sizeof(phar_entry_info));
  419| 
  420| 	/* strip leading "/" */
  421| 	if (phar->is_zip) {
  422| 		entry.is_zip = 1;
  423| 	}
  424| 
  425| 	entry.filename = zend_string_init(ZSTR_VAL(resource->path) + 1, ZSTR_LEN(resource->path) - 1, false);
  426| 
  427| 	if (phar->is_tar) {
  428| 		entry.is_tar = 1;
  429| 		entry.tar_type = TAR_DIR;
  430| 	}
  431| 
  432| 	php_url_free(resource);
  433| 	entry.is_dir = 1;
  434| 	entry.phar = phar;
  435| 	entry.is_modified = 1;
  436| 	entry.is_crc_checked = 1;
  437| 	entry.flags = PHAR_ENT_PERM_DEF_DIR;
  438| 	entry.old_flags = PHAR_ENT_PERM_DEF_DIR;
  439| 
  440| 	void *had_been_added = zend_hash_add_mem(&phar->manifest, entry.filename, &entry, sizeof(phar_entry_info));
  441| 	if (!had_been_added) {
  442| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", adding to manifest failed", ZSTR_VAL(entry.filename), ZSTR_VAL(phar->fname));
  443| 		zend_string_efree(entry.filename);
  444| 		return 0;
  445| 	}
  446| 
  447| 	phar_flush(phar, &error);
  448| 
  449| 	if (error) {
  450| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", %s", ZSTR_VAL(entry.filename), ZSTR_VAL(phar->fname), error);
  451| 		zend_hash_del(&phar->manifest, entry.filename);
  452| 		efree(error);
  453| 		return 0;
  454| 	}
  455| 
  456| 	phar_add_virtual_dirs(phar, ZSTR_VAL(entry.filename), ZSTR_LEN(entry.filename));
  457| 	return 1;
  458| }
```

- `get_function_source(name=phar_wrapper_rmdir, rev=work)` →

```
phar_wrapper_rmdir (function, old version) — ext/phar/dirstream.c:464-578
  464| int phar_wrapper_rmdir(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
  465| {
  466| 	char *error;
  467| 
  468| 	/* pre-readonly check, we need to know if this is a data phar */
  469| 	zend_string *arch = phar_split_fname(url, strlen(url), NULL, 2, 2);
  470| 	if (!arch) {
  471| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\", no phar archive specified, or phar archive does not exist", url);
  472| 		return 0;
  473| 	}
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
  491| 		php_url_free(resource);
  492| 		php_stream_wrapper_log_error(wrapper, options, "phar error: invalid url \"%s\"", url);
  493| 		return 0;
  494| 	}
  495| 
  496| 	if (!zend_string_equals_literal_ci(resource->scheme, "phar")) {
  497| 		php_url_free(resource);
  498| 		php_stream_wrapper_log_error(wrapper, options, "phar error: not a phar stream url \"%s\"", url);
  499| 		return 0;
  500| 	}
  501| 
  502| 	phar = phar_get_archive(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error);
  503| 	if (!phar) {
  504| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\" in phar \"%s\", error retrieving phar information: %s", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host), error);
  505| 		efree(error);
  506| 		php_url_free(resource);
  507| 		return 0;
  508| 	}
  509| 
  510| 	size_t path_len = ZSTR_LEN(resource->path) - 1;
  511| 
  512| 	phar_entry_info *entry = phar_get_entry_info_dir(phar, ZSTR_VAL(resource->path) + 1, path_len, 2, &error, true);
  513| 	if (!entry) {
  514| 		if (error) {
  515| 			php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\" in phar \"%s\", %s", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host), error);
  516| 			efree(error);
  517| 		} else {
  518| 			php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\" in phar \"%s\", directory does not exist", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host));
  519| 		}
  520| 		php_url_free(resource);
  521| 		return 0;
  522| 	}
  523| 
  524| 	if (!entry->is_deleted) {
  525| 		zend_string *str_key;
  526| 
  527| 		ZEND_HASH_MAP_FOREACH_STR_KEY(&phar->manifest, str_key) {
  528| 			if (
  529| 				zend_string_starts_with_cstr(str_key, ZSTR_VAL(resource->path)+1, path_len)
  530| 				&& IS_SLASH(ZSTR_VAL(str_key)[path_len])
  531| 			) {
  532| 				php_stream_wrapper_log_error(wrapper, options, "phar error: Directory not empty");
  533| 				if (entry->is_temp_dir) {
  534| 					zend_string_efree(entry->filename);
  535| 					efree(entry);
  536| 				}
  537| 				php_url_free(resource);
  538| 				return 0;
  539| 			}
  540| 		} ZEND_HASH_FOREACH_END();
  541| 
  542| 		ZEND_HASH_MAP_FOREACH_STR_KEY(&phar->virtual_dirs, str_key) {
  543| 			ZEND_ASSERT(str_key);
  544| 			if (
  545| 				zend_string_starts_with_cstr(str_key, ZSTR_VAL(resource->path)+1, path_len)
  546| 				&& IS_SLASH(ZSTR_VAL(str_key)[path_len])
  547| 			) {
  548| 				php_stream_wrapper_log_error(wrapper, options, "phar error: Directory not empty");
  549| 				if (entry->is_temp_dir) {
  550| 					zend_string_efree(entry->filename);
  551| 					efree(entry);
  552| 				}
  553| 				php_url_free(resource);
  554| 				return 0;
  555| 			}
  556| 		} ZEND_HASH_FOREACH_END();
  557| 	}
  558| 
  559| 	if (entry->is_temp_dir) {
  560| 		zend_hash_str_del(&phar->virtual_dirs, ZSTR_VAL(resource->path)+1, path_len);
  561| 		zend_string_efree(entry->filename);
  562| 		efree(entry);
  563| 	} else {
  564| 		entry->is_deleted = 1;
  565| 		entry->is_modified = 1;
  566| 		phar_flush(phar, &error);
  567| 
  568| 		if (error) {
  569| 			php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\" in phar \"%s\", %s", ZSTR_VAL(entry->filename), ZSTR_VAL(phar->fname), error);
  570| 			php_url_free(resource);
  571| 			efree(error);
  572| 			return 0;
  573| 		}
  574| 	}
  575| 
  576| 	php_url_free(resource);
  577| 	return 1;
  578| }
```

- `get_function_source(name=phar_wrapper_stat, rev=work)` →

```
phar_wrapper_stat (function, old version) — ext/phar/stream.c:554-651
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
  566| 	if (!resource->scheme || !resource->host || !resource->path) {
  567| 		php_url_free(resource);
  568| 		return FAILURE;
  569| 	}
  570| 
  571| 	if (!zend_string_equals_literal_ci(resource->scheme, "phar")) {
  572| 		php_url_free(resource);
  573| 		return FAILURE;
  574| 	}
  575| 
  576| 	phar_request_initialize();
  577| 
  578| 	internal_file = ZSTR_VAL(resource->path) + 1; /* strip leading "/" */
  579| 	/* find the phar in our trusty global hash indexed by alias (host of phar://blah.phar/file.whatever) */
  580| 	phar_archive_data *phar = phar_get_archive(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, NULL);
  581| 	if (!phar) {
  582| 		php_url_free(resource);
  583| 		return FAILURE;
  584| 	}
  585| 	if (*internal_file == '\0') {
  586| 		/* root directory requested */
  587| 		phar_dostat(phar, NULL, ssb, true);
  588| 		php_url_free(resource);
  589| 		return SUCCESS;
  590| 	}
  591| 	if (!HT_IS_INITIALIZED(&phar->manifest)) {
  592| 		php_url_free(resource);
  593| 		return FAILURE;
  594| 	}
  595| 	internal_file_len = strlen(internal_file);
  596| 	/* search through the manifest of files, and if we have an exact match, it's a file */
  597| 	phar_entry_info *entry = zend_hash_str_find_ptr(&phar->manifest, internal_file, internal_file_len);
  598| 	if (entry) {
  599| 		phar_dostat(phar, entry, ssb, false);
  600| 		php_url_free(resource);
  601| 		return SUCCESS;
  602| 	}
  603| 	if (zend_hash_str_exists(&(phar->virtual_dirs), internal_file, internal_file_len)) {
  604| 		phar_dostat(phar, NULL, ssb, true);
  605| 		php_url_free(resource);
  606| 		return SUCCESS;
  607| 	}
  608| 	/* check for mounted directories */
  609| 	if (HT_IS_INITIALIZED(&phar->mounted_dirs) && zend_hash_num_elements(&phar->mounted_dirs)) {
  610| 		zend_string *str_key;
  611| 
  612| 		ZEND_HASH_MAP_FOREACH_STR_KEY(&phar->mounted_dirs, str_key) {
  613| 			if (ZSTR_LEN(str_key) >= internal_file_len || strncmp(ZSTR_VAL(str_key), internal_file, ZSTR_LEN(str_key))) {
  614| 				continue;
  615| 			} else {
  616| 				char *test;
  617| 				size_t test_len;
  618| 				php_stream_statbuf ssbi;
  619| 
  620| 				if (NULL == (entry = zend_hash_find_ptr(&phar->manifest, str_key))) {
  621| 					goto free_resource;
  622| 				}
  623| 				if (!entry->tmp || !entry->is_mounted) {
  624| 					goto free_resource;
  625| 				}
  626| 				test_len = spprintf(&test, MAXPATHLEN, "%s%s", entry->tmp, internal_file + ZSTR_LEN(str_key));
  627| 				if (SUCCESS != php_stream_stat_path(test, &ssbi)) {
  628| 					efree(test);
  629| 					continue;
  630| 				}
  631| 				/* mount the file/directory just in time */
  632| 				if (SUCCESS != phar_mount_entry(phar, test, test_len, internal_file, internal_file_len)) {
  633| 					efree(test);
  634| 					goto free_resource;
  635| 				}
  636| 				efree(test);
  637| 
  638| 				entry = zend_hash_str_find_ptr(&phar->manifest, internal_file, internal_file_len);
  639| 				if (!entry) {
  640| 					goto free_resource;
  641| 				}
  642| 				phar_dostat(phar, entry, ssb, false);
  643| 				php_url_free(resource);
  644| 				return SUCCESS;
  645| 			}
  646| 		} ZEND_HASH_FOREACH_END();
  647| 	}
  648| free_resource:
  649| 	php_url_free(resource);
  650| 	return FAILURE;
  651| }
```

- `get_function_source(name=phar_wrapper_unlink, rev=work)` →

```
phar_wrapper_unlink (function, old version) — ext/phar/stream.c:657-722
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
  669| 	/* we must have at the very least phar://alias.phar/internalfile.php */
  670| 	if (!resource->scheme || !resource->host || !resource->path) {
  671| 		php_url_free(resource);
  672| 		php_stream_wrapper_log_error(wrapper, options, "phar error: invalid url \"%s\"", url);
  673| 		return 0;
  674| 	}
  675| 
  676| 	if (!zend_string_equals_literal_ci(resource->scheme, "phar")) {
  677| 		php_url_free(resource);
  678| 		php_stream_wrapper_log_error(wrapper, options, "phar error: not a phar stream url \"%s\"", url);
  679| 		return 0;
  680| 	}
  681| 
  682| 	phar_request_initialize();
  683| 
  684| 	const phar_archive_data *pphar = zend_hash_find_ptr(&(PHAR_G(phar_fname_map)), resource->host);
  685| 	if (PHAR_G(readonly) && (!pphar || !pphar->is_data)) {
  686| 		php_url_free(resource);
  687| 		php_stream_wrapper_log_error(wrapper, options, "phar error: write operations disabled by the php.ini setting phar.readonly");
  688| 		return 0;
  689| 	}
  690| 
  691| 	/* need to copy to strip leading "/", will get touched again */
  692| 	internal_file = estrndup(ZSTR_VAL(resource->path) + 1, ZSTR_LEN(resource->path) - 1);
  693| 	internal_file_len = ZSTR_LEN(resource->path) - 1;
  694| 	if (FAILURE == phar_get_entry_data(&idata, resource->host, internal_file, internal_file_len, "r", 0, &error, true)) {
  695| 		/* constraints of fp refcount were not met */
  696| 		if (error) {
  697| 			php_stream_wrapper_log_error(wrapper, options, "unlink of \"%s\" failed: %s", url, error);
  698| 			efree(error);
  699| 		} else {
  700| 			php_stream_wrapper_log_error(wrapper, options, "unlink of \"%s\" failed, file does not exist", url);
  701| 		}
  702| 		efree(internal_file);
  703| 		php_url_free(resource);
  704| 		return 0;
  705| 	}
  706| 	if (idata->internal_file->fp_refcount > 1) {
  707| 		/* more than just our fp resource is open for this file */
  708| 		php_stream_wrapper_log_error(wrapper, options, "phar error: \"%s\" in phar \"%s\", has open file pointers, cannot unlink", internal_file, ZSTR_VAL(resource->host));
  709| 		efree(internal_file);
  710| 		php_url_free(resource);
  711| 		phar_entry_delref(idata);
  712| 		return 0;
  713| 	}
  714| 	php_url_free(resource);
  715| 	efree(internal_file);
  716| 	phar_entry_remove(idata, &error);
  717| 	if (error) {
  718| 		php_stream_wrapper_log_error(wrapper, options, "%s", error);
  719| 		efree(error);
  720| 	}
  721| 	return 1;
  722| }
```

- `get_function_source(name=phar_wrapper_open_url, rev=work)` →

```
phar_wrapper_open_url (function, old version) — ext/phar/stream.c:159-343
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
  176| 		php_url_free(resource);
  177| 		php_stream_wrapper_log_error(wrapper, options, "phar error: invalid url \"%s\"", path);
  178| 		return NULL;
  179| 	}
  180| 
  181| 	if (!zend_string_equals_literal_ci(resource->scheme, "phar")) {
  182| 		php_url_free(resource);
  183| 		php_stream_wrapper_log_error(wrapper, options, "phar error: not a phar stream url \"%s\"", path);
  184| 		return NULL;
  185| 	}
  186| 
  187| 	phar_request_initialize();
  188| 
  189| 	/* strip leading "/" */
  190| 	internal_file = estrndup(ZSTR_VAL(resource->path) + 1, ZSTR_LEN(resource->path) - 1);
  191| 	if (mode[0] == 'w' || (mode[0] == 'r' && mode[1] == '+')) {
  192| 		if (NULL == (idata = phar_get_or_create_entry_data(resource->host, internal_file, strlen(internal_file), mode, 0, &error, true, time(NULL)))) {
  193| 			if (error) {
  194| 				php_stream_wrapper_log_error(wrapper, options, "%s", error);
  195| 				efree(error);
  196| 			} else {
  197| 				php_stream_wrapper_log_error(wrapper, options, "phar error: file \"%s\" could not be created in phar \"%s\"", internal_file, ZSTR_VAL(resource->host));
  198| 			}
  199| 			efree(internal_file);
  200| 			php_url_free(resource);
  201| 			return NULL;
  202| 		}
  203| 		fpf = php_stream_alloc(&phar_ops, idata, NULL, mode);
  204| 		php_url_free(resource);
  205| 		efree(internal_file);
  206| 
  207| 		if (context && Z_TYPE(context->options) != IS_UNDEF && (pzoption = zend_hash_str_find_ind(HASH_OF(&context->options), "phar", sizeof("phar")-1)) != NULL) {
  208| 			pharcontext = HASH_OF(pzoption);
  209| 			if (idata->internal_file->uncompressed_filesize == 0
  210| 				&& idata->internal_file->compressed_filesize == 0
  211| 				&& (pzoption = zend_hash_str_find_ind(pharcontext, "compress", sizeof("compress")-1)) != NULL
  212| 				&& Z_TYPE_P(pzoption) == IS_LONG
  213| 				&& (Z_LVAL_P(pzoption) & ~PHAR_ENT_COMPRESSION_MASK) == 0
  214| 			) {
  215| 				idata->internal_file->flags &= ~PHAR_ENT_COMPRESSION_MASK;
  216| 				idata->internal_file->flags |= Z_LVAL_P(pzoption);
  217| 			}
  218| 			if ((pzoption = zend_hash_str_find_ind(pharcontext, "metadata", sizeof("metadata")-1)) != NULL) {
  219| 				phar_metadata_tracker_free(&idata->internal_file->metadata_tracker, idata->internal_file->is_persistent);
  220| 
  221| 				metadata = pzoption;
  222| 				ZVAL_COPY_DEREF(&idata->internal_file->metadata_tracker.val, metadata);
  223| 				idata->phar->is_modified = true;
  224| 			}
  225| 		}
  226| 		if (opened_path) {
  227| 			*opened_path = zend_strpprintf_unchecked(MAXPATHLEN, "phar://%S/%S", idata->phar->fname, idata->internal_file->filename);
  228| 		}
  229| 		return fpf;
  230| 	} else {
  231| 		if (!*internal_file && (options & STREAM_OPEN_FOR_INCLUDE)) {
  232| 			/* retrieve the stub */
  233| 			phar = phar_get_archive(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, NULL);
  234| 			if (!phar) {
  235| 				php_stream_wrapper_log_error(wrapper, options, "file %s is not a valid phar archive", ZSTR_VAL(resource->host));
  236| 				efree(internal_file);
  237| 				php_url_free(resource);
  238| 				return NULL;
  239| 			}
  240| 			if (phar->is_tar || phar->is_zip) {
  241| 				if ((FAILURE == phar_get_entry_data(&idata, resource->host, ".phar/stub.php", sizeof(".phar/stub.php")-1, "r", 0, &error, false)) || !idata) {
  242| 					goto idata_error;
  243| 				}
  244| 				efree(internal_file);
  245| 				if (opened_path) {
  246| 					*opened_path = zend_string_copy(phar->fname);
  247| 				}
  248| 				php_url_free(resource);
  249| 				goto phar_stub;
  250| 			} else {
  251| 				php_stream *stream = phar_get_pharfp(phar);
  252| 				if (stream == NULL) {
  253| 					stream = phar_open_archive_fp(phar);
  254| 					if (UNEXPECTED(!stream)) {
  255| 						php_stream_wrapper_log_error(wrapper, options, "phar error: could not reopen phar \"%s\"", ZSTR_VAL(resource->host));
  256| 						efree(internal_file);
  257| 						php_url_free(resource);
  258| 						return NULL;
  259| 					}
  260| 				}
  261| 
  262| 				phar_entry_info *entry;
  263| 
  264| 				entry = (phar_entry_info *) ecalloc(1, sizeof(phar_entry_info));
  265| 				entry->is_temp_dir = 1;
  266| 				entry->filename = ZSTR_EMPTY_ALLOC();
  267| 				entry->phar = phar;
  268| 				entry->offset = entry->offset_abs = 0;
  269| 				entry->compressed_filesize = entry->uncompressed_filesize = phar->halt_offset;
  270| 				entry->is_crc_checked = 1;
  271| 
  272| 				idata = (phar_entry_data *) ecalloc(1, sizeof(phar_entry_data));
  273| 				idata->fp = stream;
  274| 				idata->phar = phar;
  275| 				idata->internal_file = entry;
  276| 				if (!phar->is_persistent) {
  277| 					++(entry->phar->refcount);
  278| 				}
  279| 				++(entry->fp_refcount);
  280| 				php_url_free(resource);
  281| 				if (opened_path) {
  282| 					*opened_path = zend_string_copy(phar->fname);
  283| 				}
  284| 				efree(internal_file);
  285| 				goto phar_stub;
  286| 			}
  287| 		}
  288| 		/* read-only access is allowed to magic files in .phar directory */
  289| 		if ((FAILURE == phar_get_entry_data(&idata, resource->host, internal_file, strlen(internal_file), "r", 0, &error, false)) || !idata) {
  290| idata_error:
  291| 			if (error) {
  292| 				php_stream_wrapper_log_error(wrapper, options, "%s", error);
  293| 				efree(error);
  294| 			} else {
  295| 				php_stream_wrapper_log_error(wrapper, options, "phar error: \"%s\" is not a file in phar \"%s\"", internal_file, ZSTR_VAL(resource->host));
  296| 			}
  297| 			efree(internal_file);
  298| 			php_url_free(resource);
  299| 			return NULL;
  300| 		}
  301| 	}
  302| 	php_url_free(resource);
  303| #ifdef MBO_0
  304| 		fprintf(stderr, "Pharname:   %s\n", ZSTR_VAL(idata->phar->fname));
  305| 		fprintf(stderr, "Filename:   %s\n", internal_file);
  306| 		fprintf(stderr, "Entry:      %s\n", ZSTR_VAL(idata->internal_file->filename));
  307| 		fprintf(stderr, "Size:       %u\n", idata->internal_file->uncompressed_filesize);
  308| 		fprintf(stderr, "Compressed: %u\n", idata->internal_file->flags);
  309| #endif
  310| 
  311| 	/* check length, crc32 */
  312| 	if (!idata->internal_file->is_crc_checked && phar_postprocess_file(idata, idata->internal_file->crc32, &error, 2) != SUCCESS) {
  313| 		php_stream_wrapper_log_error(wrapper, options, "%s", error);
  314| 		efree(error);
  315| 		phar_entry_delref(idata);
  316| 		efree(internal_file);
  317| 		return NULL;
  318| 	}
  319| 
  320| 	if (!PHAR_G(cwd_init) && (options & STREAM_OPEN_FOR_INCLUDE)) {
  321| 		const char *entry = ZSTR_VAL(idata->internal_file->filename), *cwd;
  322| 
  323| 		PHAR_G(cwd_init) = 1;
  324| 		if ((idata->phar->is_tar || idata->phar->is_zip) && zend_string_equals_literal(idata->internal_file->filename, ".phar/stub.php")) {
  325| 			/* we're executing the stub, which doesn't count as a file */
  326| 			PHAR_G(cwd_init) = 0;
  327| 		} else if ((cwd = strrchr(entry, '/'))) {
  328| 			PHAR_G(cwd_len) = cwd - entry;
  329| 			PHAR_G(cwd) = estrndup(entry, PHAR_G(cwd_len));
  330| 		} else {
  331| 			/* root directory */
  332| 			PHAR_G(cwd_len) = 0;
  333| 			PHAR_G(cwd) = NULL;
  334| 		}
  335| 	}
  336| 	if (opened_path) {
  337| 		*opened_path = zend_strpprintf_unchecked(MAXPATHLEN, "phar://%S/%S", idata->phar->fname, idata->internal_file->filename);
  338| 	}
  339| 	efree(internal_file);
  340| phar_stub:
  341| 	fpf = php_stream_alloc(&phar_ops, idata, NULL, mode);
  342| 	return fpf;
  343| }
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 28188+292, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "phar_wrapper_open_dir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_stat", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_unlink", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_rename", "file": "ext/phar/stream.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

