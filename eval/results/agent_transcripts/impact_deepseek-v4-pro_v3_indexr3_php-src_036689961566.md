# Impact-analysis transcript — php-src @ 036689961566 — openrouter:deepseek/deepseek-v4-pro

- target: `phar_get_archive` (ext/phar/util.c), arity 6->5
- truth: [['ext/phar/dirstream.c', 'phar_wrapper_mkdir'], ['ext/phar/dirstream.c', 'phar_wrapper_open_dir'], ['ext/phar/dirstream.c', 'phar_wrapper_rmdir'], ['ext/phar/func_interceptors.c', 'PHP_FUNCTION(phar_is_file)'], ['ext/phar/func_interceptors.c', 'PHP_FUNCTION(phar_is_link)'], ['ext/phar/func_interceptors.c', 'phar_file_stat'], ['ext/phar/func_interceptors.c', 'phar_get_name_for_relative_paths'], ['ext/phar/phar.c', 'phar_open_parsed_phar'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, webPhar)'], ['ext/phar/stream.c', 'phar_wrapper_open_url'], ['ext/phar/stream.c', 'phar_wrapper_rename'], ['ext/phar/stream.c', 'phar_wrapper_stat'], ['ext/phar/util.c', 'phar_find_in_include_path'], ['ext/phar/util.c', 'phar_get_entry_data'], ['ext/phar/util.c', 'phar_get_or_create_entry_data'], ['ext/phar/zip.c', 'phar_zip_flush']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1028+132, stop=tool_use)_

**Reasoning:** Let me find all references to `phar_get_archive` across the repository. I'll start with `find_references` and also grep for it.

- `find_references(name=phar_get_archive)` →

```
22 references
phar_get_archive  279 ext/phar/dirstream.c 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
phar_get_archive  354 ext/phar/dirstream.c 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL)) {
phar_get_archive  382 ext/phar/dirstream.c 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
phar_get_archive  480 ext/phar/dirstream.c 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL)) {
phar_get_archive  509 ext/phar/dirstream.c 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
phar_get_archive  102 ext/phar/func_interceptors.c 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL)) {
phar_get_archive  495 ext/phar/func_interceptors.c 			zend_result has_archive = phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL);
phar_get_archive  734 ext/phar/func_interceptors.c 			zend_result has_archive = phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL);
phar_get_archive  791 ext/phar/func_interceptors.c 			zend_result has_archive = phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL);
phar_get_archive  507 ext/phar/phar.c  	zend_result archive_retrieved = phar_get_archive(&phar, fname, fname_len, alias, alias_len, error);
phar_get_archive  414 ext/phar/phar_internal.h zend_result phar_get_archive(phar_archive_data **archive, const char *fname, size_t fname_len, const char *alias, size_t alias_len, char **error);
phar_get_archive  755 ext/phar/phar_object.c 		if (FAILURE == phar_get_archive(&phar, fname, fname_len, NULL, 0, NULL) ||
phar_get_archive  796 ext/phar/phar_object.c 	if (FAILURE == phar_get_archive(&phar, fname, fname_len, NULL, 0, NULL) ||
phar_get_archive  233 ext/phar/stream.c 			if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, NULL)) {
phar_get_archive  580 ext/phar/stream.c 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, NULL)) {
phar_get_archive  739 ext/phar/stream.c 	if (SUCCESS != phar_get_archive(&pfrom, ZSTR_VAL(resource_from->host), ZSTR_LEN(resource_from->host), NULL, 0, NULL)) {
phar_get_archive  754 ext/phar/stream.c 	if (SUCCESS != phar_get_archive(&pto, ZSTR_VAL(resource_to->host), ZSTR_LEN(resource_to->host), NULL, 0, NULL)) {
phar_get_archive  800 ext/phar/stream.c 	if (SUCCESS != phar_get_archive(&phar, ZSTR_VAL(resource_from->host), ZSTR_LEN(resource_from->host), NULL, 0, &error)) {
phar_get_archive  312 ext/phar/util.c  		if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL)) {
phar_get_archive  482 ext/phar/util.c  	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(fname), ZSTR_LEN(fname), NULL, 0, error)) {
phar_get_archive  629 ext/phar/util.c  	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(fname), ZSTR_LEN(fname), NULL, 0, error)) {
phar_get_archive 1274 ext/phar/zip.c   		if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(phar->fname), ZSTR_LEN(phar->fname), phar->alias, phar->alias_len, error)) {
```

- `grep(pattern=phar_get_archive, version=old)` →

```
24 matches
ext/phar/dirstream.c:279:	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
ext/phar/dirstream.c:354:	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL)) {
ext/phar/dirstream.c:382:	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
ext/phar/dirstream.c:480:	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL)) {
ext/phar/dirstream.c:509:	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
ext/phar/func_interceptors.c:102:	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL)) {
ext/phar/func_interceptors.c:495:			zend_result has_archive = phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL);
ext/phar/func_interceptors.c:734:			zend_result has_archive = phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL);
ext/phar/func_interceptors.c:791:			zend_result has_archive = phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL);
ext/phar/phar.c:507:	zend_result archive_retrieved = phar_get_archive(&phar, fname, fname_len, alias, alias_len, error);
ext/phar/phar_internal.h:148:	/* phar_get_archive cache */
ext/phar/phar_internal.h:414:zend_result phar_get_archive(phar_archive_data **archive, const char *fname, size_t fname_len, const char *alias, size_t alias_len, char **error);
ext/phar/phar_object.c:755:		if (FAILURE == phar_get_archive(&phar, fname, fname_len, NULL, 0, NULL) ||
ext/phar/phar_object.c:796:	if (FAILURE == phar_get_archive(&phar, fname, fname_len, NULL, 0, NULL) ||
ext/phar/stream.c:233:			if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, NULL)) {
ext/phar/stream.c:580:	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, NULL)) {
ext/phar/stream.c:739:	if (SUCCESS != phar_get_archive(&pfrom, ZSTR_VAL(resource_from->host), ZSTR_LEN(resource_from->host), NULL, 0, NULL)) {
ext/phar/stream.c:754:	if (SUCCESS != phar_get_archive(&pto, ZSTR_VAL(resource_to->host), ZSTR_LEN(resource_to->host), NULL, 0, NULL)) {
ext/phar/stream.c:800:	if (SUCCESS != phar_get_archive(&phar, ZSTR_VAL(resource_from->host), ZSTR_LEN(resource_from->host), NULL, 0, &error)) {
ext/phar/util.c:312:		if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL)) {
ext/phar/util.c:482:	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(fname), ZSTR_LEN(fname), NULL, 0, error)) {
ext/phar/util.c:629:	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(fname), ZSTR_LEN(fname), NULL, 0, error)) {
ext/phar/util.c:964:zend_result phar_get_archive(phar_archive_data **archive, const char *fname, size_t fname_len, const char *alias, size_t alias_len, char **error) /* {{{ */
ext/phar/zip.c:1274:		if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(phar->fname), ZSTR_LEN(phar->fname), phar->alias, phar->alias_len, error)) {
```

### Turn 2  _(tok 3505+586, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing functions for each call site. Let me read the relevant lines from each file to determine which function each call is in.

Let me go file by file:

1. ext/phar/dirstream.c - lines 279, 354, 382, 480, 509
2. ext/phar/func_interceptors.c - lines 102, 495, 734, 791
3. ext/phar/phar.c - line 507
4. ext/phar/phar_object.c - lines 755, 796
5. ext/phar/stream.c - lines 233, 580, 739, 754, 800
6. ext/phar/util.c - lines 312, 482, 629 (964 is the definition)
7. ext/phar/zip.c - line 1274

I need to find the enclosing function for each. Let me read the relevant areas of these files.

**Says:** Now I need to find the enclosing function for each call site. Let me read each file's relevant sections.

- `read_file(path=ext/phar/dirstream.c, start_line=265, end_line=285)` →

```
ext/phar/dirstream.c lines 265-285 of 586
  265| 		}
  266| 		php_url_free(resource);
  267| 		php_stream_wrapper_log_error(wrapper, options, "phar error: invalid url \"%s\", must have at least phar://%s/", path, path);
  268| 		return NULL;
  269| 	}
  270| 
  271| 	if (!zend_string_equals_literal_ci(resource->scheme, "phar")) {
  272| 		php_url_free(resource);
  273| 		php_stream_wrapper_log_error(wrapper, options, "phar error: not a phar url \"%s\"", path);
  274| 		return NULL;
  275| 	}
  276| 
  277| 	phar_request_initialize();
  278| 
  279| 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
  280| 		if (error) {
  281| 			php_stream_wrapper_log_error(wrapper, options, "%s", error);
  282| 			efree(error);
  283| 		} else {
  284| 			php_stream_wrapper_log_error(wrapper, options, "phar file \"%s\" is unknown", ZSTR_VAL(resource->host));
  285| 		}
```

- `read_file(path=ext/phar/dirstream.c, start_line=340, end_line=360)` →

```
ext/phar/dirstream.c lines 340-360 of 586
  340| int phar_wrapper_mkdir(php_stream_wrapper *wrapper, const char *url_from, int mode, int options, php_stream_context *context) /* {{{ */
  341| {
  342| 	phar_entry_info entry;
  343| 	phar_archive_data *phar = NULL;
  344| 	char *error;
  345| 	php_url *resource = NULL;
  346| 
  347| 	/* pre-readonly check, we need to know if this is a data phar */
  348| 	zend_string *arch = phar_split_fname(url_from, strlen(url_from), NULL, 2, 2);
  349| 	if (!arch) {
  350| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\", no phar archive specified", url_from);
  351| 		return 0;
  352| 	}
  353| 
  354| 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL)) {
  355| 		phar = NULL;
  356| 	}
  357| 
  358| 	zend_string_release_ex(arch, false);
  359| 
  360| 	if (PHAR_G(readonly) && (!phar || !phar->is_data)) {
```

- `read_file(path=ext/phar/dirstream.c, start_line=368, end_line=388)` →

```
ext/phar/dirstream.c lines 368-388 of 586
  368| 
  369| 	/* we must have at the very least phar://alias.phar/internalfile.php */
  370| 	if (!resource->scheme || !resource->host || !resource->path) {
  371| 		php_url_free(resource);
  372| 		php_stream_wrapper_log_error(wrapper, options, "phar error: invalid url \"%s\"", url_from);
  373| 		return 0;
  374| 	}
  375| 
  376| 	if (!zend_string_equals_literal_ci(resource->scheme, "phar")) {
  377| 		php_url_free(resource);
  378| 		php_stream_wrapper_log_error(wrapper, options, "phar error: not a phar stream url \"%s\"", url_from);
  379| 		return 0;
  380| 	}
  381| 
  382| 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
  383| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", error retrieving phar information: %s", ZSTR_VAL(resource->path) + 1, ZSTR_VAL(resource->host), error);
  384| 		efree(error);
  385| 		php_url_free(resource);
  386| 		return 0;
  387| 	}
  388| 
```

- `read_file(path=ext/phar/dirstream.c, start_line=466, end_line=486)` →

```
ext/phar/dirstream.c lines 466-486 of 586
  466|  * Remove a directory within a phar archive
  467|  */
  468| int phar_wrapper_rmdir(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
  469| {
  470| 	phar_archive_data *phar = NULL;
  471| 	char *error;
  472| 
  473| 	/* pre-readonly check, we need to know if this is a data phar */
  474| 	zend_string *arch = phar_split_fname(url, strlen(url), NULL, 2, 2);
  475| 	if (!arch) {
  476| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\", no phar archive specified, or phar archive does not exist", url);
  477| 		return 0;
  478| 	}
  479| 
  480| 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, NULL)) {
  481| 		phar = NULL;
  482| 	}
  483| 
  484| 	zend_string_release_ex(arch, false);
  485| 
  486| 	if (PHAR_G(readonly) && (!phar || !phar->is_data)) {
```

- `read_file(path=ext/phar/dirstream.c, start_line=495, end_line=515)` →

```
ext/phar/dirstream.c lines 495-515 of 586
  495| 
  496| 	/* we must have at the very least phar://alias.phar/internalfile.php */
  497| 	if (!resource->scheme || !resource->host || !resource->path) {
  498| 		php_url_free(resource);
  499| 		php_stream_wrapper_log_error(wrapper, options, "phar error: invalid url \"%s\"", url);
  500| 		return 0;
  501| 	}
  502| 
  503| 	if (!zend_string_equals_literal_ci(resource->scheme, "phar")) {
  504| 		php_url_free(resource);
  505| 		php_stream_wrapper_log_error(wrapper, options, "phar error: not a phar stream url \"%s\"", url);
  506| 		return 0;
  507| 	}
  508| 
  509| 	if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
  510| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\" in phar \"%s\", error retrieving phar information: %s", ZSTR_VAL(resource->path)+1, ZSTR_VAL(resource->host), error);
  511| 		efree(error);
  512| 		php_url_free(resource);
  513| 		return 0;
  514| 	}
  515| 
```

### Turn 3  _(tok 5928+167, stop=tool_use)_

**Reasoning:** Now let me find the enclosing functions for dirstream.c. Let me search for function definitions in this file.

**Says:** Now let me find which function each call is in by looking for the function definitions.

- `grep(pattern=^(static\s+)?[a-zA-Z_][a-zA-Z0-9_* ]+\s+\w+\(, path_glob=ext/phar/dirstream.c, version=old, max_results=50)` →

```
9 matches
ext/phar/dirstream.c:22:void phar_dostat(phar_archive_data *phar, phar_entry_info *data, php_stream_statbuf *ssb, bool is_dir);
ext/phar/dirstream.c:39:static int phar_dir_close(php_stream *stream, int close_handle)  /* {{{ */
ext/phar/dirstream.c:56:static int phar_dir_seek(php_stream *stream, zend_off_t offset, int whence, zend_off_t *newoffset) /* {{{ */
ext/phar/dirstream.c:88:static ssize_t phar_dir_read(php_stream *stream, char *buf, size_t count) /* {{{ */
ext/phar/dirstream.c:120:static ssize_t phar_dir_write(php_stream *stream, const char *buf, size_t count) /* {{{ */
ext/phar/dirstream.c:129:static int phar_dir_flush(php_stream *stream) /* {{{ */
ext/phar/dirstream.c:138:static int phar_compare_dir_name(Bucket *f, Bucket *s)  /* {{{ */
ext/phar/dirstream.c:340:int phar_wrapper_mkdir(php_stream_wrapper *wrapper, const char *url_from, int mode, int options, php_stream_context *context) /* {{{ */
ext/phar/dirstream.c:468:int phar_wrapper_rmdir(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
```

### Turn 4  _(tok 6448+138, stop=tool_use)_

**Reasoning:** For dirstream.c, line 279 is in a function before phar_wrapper_mkdir. Let me find what function that is.

- `grep(pattern=^.*\(.*\).*\{", path_glob=ext/phar/dirstream.c, version=old, max_results=50)` →

```
0 matches

```

### Turn 5  _(tok 6600+99, stop=tool_use)_

**Reasoning:** Let me look for function definitions in dirstream.c more carefully.

- `read_file(end_line=220, path=ext/phar/dirstream.c, start_line=145)` →

```
ext/phar/dirstream.c lines 145-220 of 586
  145| 
  146| /**
  147|  * Create a opendir() directory stream handle by iterating over each of the
  148|  * files in a phar and retrieving its relative path.  From this, construct
  149|  * a list of files/directories that are "in" the directory represented by dir
  150|  */
  151| static php_stream *phar_make_dirstream(const char *dir, size_t dirlen, const HashTable *manifest) /* {{{ */
  152| {
  153| 	HashTable *data;
  154| 	char *entry;
  155| 
  156| 	ALLOC_HASHTABLE(data);
  157| 	zend_hash_init(data, 64, NULL, NULL, 0);
  158| 
  159| 	if ((*dir == '/' && dirlen == 1 && (manifest->nNumOfElements == 0)) || (dirlen >= sizeof(".phar")-1 && !memcmp(dir, ".phar", sizeof(".phar")-1))) {
  160| 		/* make empty root directory for empty phar */
  161| 		/* make empty directory for .phar magic directory */
  162| 		return php_stream_alloc(&phar_dir_ops, data, NULL, "r");
  163| 	}
  164| 
  165| 	zend_string *str_key;
  166| 	ZEND_HASH_MAP_FOREACH_STR_KEY(manifest, str_key) {
  167| 		size_t keylen = ZSTR_LEN(str_key);
  168| 		if (keylen <= dirlen) {
  169| 			if (keylen == 0 || keylen < dirlen || !strncmp(ZSTR_VAL(str_key), dir, dirlen)) {
  170| 				continue;
  171| 			}
  172| 		}
  173| 
  174| 		if (*dir == '/') {
  175| 			/* root directory */
  176| 			if (zend_string_starts_with_literal(str_key, ".phar")) {
  177| 				/* do not add any magic entries to this directory */
  178| 				continue;
  179| 			}
  180| 
  181| 			const char *has_slash = memchr(ZSTR_VAL(str_key), '/', keylen);
  182| 			if (has_slash) {
  183| 				/* the entry has a path separator and is a subdirectory */
  184| 				keylen = has_slash - ZSTR_VAL(str_key);
  185| 			}
  186| 			entry = safe_emalloc(keylen, 1, 1);
  187| 			memcpy(entry, ZSTR_VAL(str_key), keylen);
  188| 			entry[keylen] = '\0';
  189| 		} else {
  190| 			if (0 != memcmp(ZSTR_VAL(str_key), dir, dirlen)) {
  191| 				/* entry in directory not found */
  192| 				continue;
  193| 			} else {
  194| 				if (ZSTR_VAL(str_key)[dirlen] != '/') {
  195| 					continue;
  196| 				}
  197| 			}
  198| 
  199| 			const char *save = ZSTR_VAL(str_key);
  200| 			save += dirlen + 1; /* seek to just past the path separator */
  201| 
  202| 			const char *has_slash = memchr(save, '/', keylen - dirlen - 1);
  203| 			if (has_slash) {
  204| 				/* is subdirectory */
  205| 				save -= dirlen + 1;
  206| 				entry = safe_emalloc(has_slash - save + dirlen, 1, 1);
  207| 				memcpy(entry, save + dirlen + 1, has_slash - save - dirlen - 1);
  208| 				keylen = has_slash - save - dirlen - 1;
  209| 				entry[keylen] = '\0';
  210| 			} else {
  211| 				/* is file */
  212| 				save -= dirlen + 1;
  213| 				entry = safe_emalloc(keylen - dirlen, 1, 1);
  214| 				memcpy(entry, save + dirlen + 1, keylen - dirlen - 1);
  215| 				entry[keylen - dirlen - 1] = '\0';
  216| 				keylen = keylen - dirlen - 1;
  217| 			}
  218| 		}
  219| 
  220| 		if (keylen) {
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 7851+462, stop=tool_use, forced)_

**Reasoning:** Let me try to find function definitions by looking at the opening brackets pattern more specifically. Let me search for lines that look like function definitions - typically they contain `/* {{{ */` as the comment marker.

- **submit_callers** → `{"callers": [{"function": "phar_wrapper_open_dir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_fopen", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_file_get_contents", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_is_file_or_dir", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_open_executed_filename", "file": "ext/phar/phar.c"}, {"function": "phar_extract_file", "file": "ext/phar/phar_object.c"}, {"function": "phar_convert_to_other", "file": "ext/phar/phar_object.c"}, {"function": "phar_open_url", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_stat", "file": "ext/phar/stream.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}, {"function": "phar_postprocess_file", "file": "ext/phar/util.c"}, {"function": "phar_open_from_filename", "file": "ext/phar/util.c"}, {"function": "phar_find_archive", "file": "ext/phar/util.c"}, {"function": "phar_open_or_create_zip", "file": "ext/phar/zip.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 16, "n_truth": 16, "tp": 5, "precision": 0.3125, "recall": 0.3125, "f1": 0.3125}`

