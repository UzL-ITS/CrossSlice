# Impact-analysis transcript — php-src @ b04136ee71db — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `phar_open_from_filename` (ext/phar/phar.c), arity 7->6
- truth: [['ext/phar/phar.c', 'phar_compile_file'], ['ext/phar/phar.c', 'phar_split_cache_list'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, loadPhar)'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, unlinkArchive)'], ['ext/phar/phar_object.c', 'PHP_METHOD(PharFileInfo, __construct)'], ['ext/phar/stream.c', 'phar_parse_url']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1036+117, stop=tool_use)_

**Reasoning:** Let me search the repository for all references to `phar_open_from_filename`.

- `find_references(name=phar_open_from_filename, max_results=100)` →

```
7 references
phar_open_from_filename  134 ext/phar/phar.c  		if (SUCCESS == phar_open_from_filename(key, len, NULL, 0, 0, &phar, NULL)) {
phar_open_from_filename 3161 ext/phar/phar.c  		if (SUCCESS == phar_open_from_filename(ZSTR_VAL(file_handle->filename), ZSTR_LEN(file_handle->filename), NULL, 0, 0, &phar, NULL)) {
phar_open_from_filename  409 ext/phar/phar_internal.h zend_result phar_open_from_filename(char *fname, size_t fname_len, const char *alias, size_t alias_len, uint32_t options, phar_archive_data** ppha
phar_open_from_filename  982 ext/phar/phar_object.c 	RETVAL_BOOL(phar_open_from_filename(ZSTR_VAL(fname), ZSTR_LEN(fname), alias, alias_len, REPORT_ERRORS, NULL, &error) == SUCCESS);
phar_open_from_filename 1269 ext/phar/phar_object.c 	if (FAILURE == phar_open_from_filename(ZSTR_VAL(fname), ZSTR_LEN(fname), NULL, 0, REPORT_ERRORS, &phar, &error)) {
phar_open_from_filename 4419 ext/phar/phar_object.c 	if (phar_open_from_filename(ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, REPORT_ERRORS, &phar_data, &error) == FAILURE) {
phar_open_from_filename  140 ext/phar/stream.c 		if (phar_open_from_filename(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, options, NULL, &error) == FAILURE)
```

- `grep(max_results=100, pattern=phar_open_from_filename, version=old)` →

```
9 matches
ext/phar/phar.c:134:		if (SUCCESS == phar_open_from_filename(key, len, NULL, 0, 0, &phar, NULL)) {
ext/phar/phar.c:720: * This is used by phar_open_from_filename to process the manifest, but can be called
ext/phar/phar.c:1510:zend_result phar_open_from_filename(char *fname, size_t fname_len, const char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error) /* {{{ */
ext/phar/phar.c:3161:		if (SUCCESS == phar_open_from_filename(ZSTR_VAL(file_handle->filename), ZSTR_LEN(file_handle->filename), NULL, 0, 0, &phar, NULL)) {
ext/phar/phar_internal.h:409:zend_result phar_open_from_filename(char *fname, size_t fname_len, const char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error);
ext/phar/phar_object.c:982:	RETVAL_BOOL(phar_open_from_filename(ZSTR_VAL(fname), ZSTR_LEN(fname), alias, alias_len, REPORT_ERRORS, NULL, &error) == SUCCESS);
ext/phar/phar_object.c:1269:	if (FAILURE == phar_open_from_filename(ZSTR_VAL(fname), ZSTR_LEN(fname), NULL, 0, REPORT_ERRORS, &phar, &error)) {
ext/phar/phar_object.c:4419:	if (phar_open_from_filename(ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, REPORT_ERRORS, &phar_data, &error) == FAILURE) {
ext/phar/stream.c:140:		if (phar_open_from_filename(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, options, NULL, &error) == FAILURE)
```

### Turn 2  _(tok 2013+597, stop=tool_use)_

**Reasoning:** There are 6 call sites (excluding the definition on line 1510, the prototype on line 409 of phar_internal.h, and the comment on line 720):

1. ext/phar/phar.c:134
2. ext/phar/phar.c:3161
3. ext/phar/phar_object.c:982
4. ext/phar/phar_object.c:1269
5. ext/phar/phar_object.c:4419
6. ext/phar/stream.c:140

Next, I need to identify the enclosing function for each call site. Let me read the context around each line.

**Says:** I found 6 call sites. Now let me identify the enclosing function for each.



- `read_file(end_line=140, path=ext/phar/phar.c, start_line=100, version=old)` →

```
ext/phar/phar.c lines 100-140 of 3495
  100| 		return;
  101| 	}
  102| 
  103| 	ds[0] = DEFAULT_DIR_SEPARATOR;
  104| 	ds[1] = '\0';
  105| 	tmp = estrdup(PHAR_G(cache_list));
  106| 
  107| 	/* fake request startup */
  108| 	PHAR_G(request_init) = 1;
  109| 	zend_init_rsrc_list();
  110| 	EG(regular_list).nNextFreeElement=1;	/* we don't want resource id 0 */
  111| 
  112| 	PHAR_G(has_bz2) = zend_hash_str_exists(&module_registry, "bz2", sizeof("bz2")-1);
  113| 	PHAR_G(has_zlib) = zend_hash_str_exists(&module_registry, "zlib", sizeof("zlib")-1);
  114| 	/* these two are dummies and will be destroyed later */
  115| 	zend_hash_init(&cached_phars, sizeof(phar_archive_data*), zend_get_hash_value, destroy_phar_data,  1);
  116| 	zend_hash_init(&cached_alias, sizeof(phar_archive_data*), zend_get_hash_value, NULL, 1);
  117| 	/* these two are real and will be copied over cached_phars/cached_alias later */
  118| 	zend_hash_init(&(PHAR_G(phar_fname_map)), sizeof(phar_archive_data*), zend_get_hash_value, destroy_phar_data,  1);
  119| 	zend_hash_init(&(PHAR_G(phar_alias_map)), sizeof(phar_archive_data*), zend_get_hash_value, NULL, 1);
  120| 	PHAR_G(manifest_cached) = 1;
  121| 	PHAR_G(persist) = 1;
  122| 
  123| 	for (key = php_strtok_r(tmp, ds, &lasts);
  124| 			key;
  125| 			key = php_strtok_r(NULL, ds, &lasts)) {
  126| 		size_t len;
  127| 		const char *end = strchr(key, DEFAULT_DIR_SEPARATOR);
  128| 		if (end) {
  129| 			len = end - key;
  130| 		} else {
  131| 			len = strlen(key);
  132| 		}
  133| 
  134| 		if (SUCCESS == phar_open_from_filename(key, len, NULL, 0, 0, &phar, NULL)) {
  135| 			phar->phar_pos = i++;
  136| 			php_stream_close(phar->fp);
  137| 			phar->fp = NULL;
  138| 		} else {
  139| 			PHAR_G(persist) = 0;
  140| 			PHAR_G(manifest_cached) = 0;
```

- `read_file(end_line=3165, path=ext/phar/phar.c, start_line=3130, version=old)` →

```
ext/phar/phar.c lines 3130-3165 of 3495
 3130| 	return php_stream_read(phar_get_pharfp((phar_archive_data*)handle), buf, len);
 3131| }
 3132| /* }}} */
 3133| 
 3134| static size_t phar_zend_stream_fsizer(void *handle) /* {{{ */
 3135| {
 3136| 	return ((phar_archive_data*)handle)->halt_offset + 32;
 3137| } /* }}} */
 3138| 
 3139| zend_op_array *(*phar_orig_compile_file)(zend_file_handle *file_handle, int type);
 3140| 
 3141| static zend_string *phar_resolve_path(zend_string *filename)
 3142| {
 3143| 	zend_string *ret = phar_find_in_include_path(filename, NULL);
 3144| 	if (!ret) {
 3145| 		ret = phar_save_resolve_path(filename);
 3146| 	}
 3147| 	return ret;
 3148| }
 3149| 
 3150| static zend_op_array *phar_compile_file(zend_file_handle *file_handle, int type) /* {{{ */
 3151| {
 3152| 	zend_op_array *res;
 3153| 	zend_string *name = NULL;
 3154| 	bool failed;
 3155| 	phar_archive_data *phar;
 3156| 
 3157| 	if (!file_handle || !file_handle->filename) {
 3158| 		return phar_orig_compile_file(file_handle, type);
 3159| 	}
 3160| 	if (strstr(ZSTR_VAL(file_handle->filename), ".phar") && !strstr(ZSTR_VAL(file_handle->filename), "://")) {
 3161| 		if (SUCCESS == phar_open_from_filename(ZSTR_VAL(file_handle->filename), ZSTR_LEN(file_handle->filename), NULL, 0, 0, &phar, NULL)) {
 3162| 			if (phar->is_zip || phar->is_tar) {
 3163| 				zend_file_handle f;
 3164| 
 3165| 				/* zip or tar-based phar */
```

- `read_file(end_line=990, path=ext/phar/phar_object.c, start_line=950, version=old)` →

```
ext/phar/phar_object.c lines 950-990 of 5059
  950| {
  951| 	zend_string *alias = NULL;
  952| 	char *error;
  953| 	zend_long dataoffset = 0;
  954| 
  955| 	if (zend_parse_parameters(ZEND_NUM_ARGS(), "|S!l", &alias, &dataoffset) == FAILURE) {
  956| 		RETURN_THROWS();
  957| 	}
  958| 
  959| 	phar_request_initialize();
  960| 
  961| 	RETVAL_BOOL(phar_open_executed_filename(alias, &error) == SUCCESS);
  962| 
  963| 	if (error) {
  964| 		zend_throw_exception_ex(phar_ce_PharException, 0, "%s", error);
  965| 		efree(error);
  966| 	}
  967| } /* }}} */
  968| 
  969| /* {{{ Loads any phar archive with an alias */
  970| PHP_METHOD(Phar, loadPhar)
  971| {
  972| 	zend_string *fname;
  973| 	char *alias = NULL, *error;
  974| 	size_t alias_len = 0;
  975| 
  976| 	if (zend_parse_parameters(ZEND_NUM_ARGS(), "P|s!", &fname, &alias, &alias_len) == FAILURE) {
  977| 		RETURN_THROWS();
  978| 	}
  979| 
  980| 	phar_request_initialize();
  981| 
  982| 	RETVAL_BOOL(phar_open_from_filename(ZSTR_VAL(fname), ZSTR_LEN(fname), alias, alias_len, REPORT_ERRORS, NULL, &error) == SUCCESS);
  983| 
  984| 	if (error) {
  985| 		zend_throw_exception_ex(phar_ce_PharException, 0, "%s", error);
  986| 		efree(error);
  987| 	}
  988| } /* }}} */
  989| 
  990| /* {{{ Returns the api version */
```

- `read_file(end_line=1275, path=ext/phar/phar_object.c, start_line=1240, version=old)` →

```
ext/phar/phar_object.c lines 1240-1275 of 5059
 1240| 	array_init(return_value);
 1241| 	phar_request_initialize();
 1242| 
 1243| 	if (PHAR_G(has_zlib)) {
 1244| 		add_next_index_stringl(return_value, "GZ", 2);
 1245| 	}
 1246| 
 1247| 	if (PHAR_G(has_bz2)) {
 1248| 		add_next_index_stringl(return_value, "BZIP2", 5);
 1249| 	}
 1250| }
 1251| /* }}} */
 1252| 
 1253| /* {{{ Completely remove a phar archive from memory and disk */
 1254| PHP_METHOD(Phar, unlinkArchive)
 1255| {
 1256| 	char *error;
 1257| 	zend_string *fname;
 1258| 	phar_archive_data *phar;
 1259| 
 1260| 	if (zend_parse_parameters(ZEND_NUM_ARGS(), "P", &fname) == FAILURE) {
 1261| 		RETURN_THROWS();
 1262| 	}
 1263| 
 1264| 	if (ZSTR_LEN(fname) == 0) {
 1265| 		zend_throw_exception_ex(phar_ce_PharException, 0, "Unknown phar archive \"\"");
 1266| 		RETURN_THROWS();
 1267| 	}
 1268| 
 1269| 	if (FAILURE == phar_open_from_filename(ZSTR_VAL(fname), ZSTR_LEN(fname), NULL, 0, REPORT_ERRORS, &phar, &error)) {
 1270| 		if (error) {
 1271| 			zend_throw_exception_ex(phar_ce_PharException, 0, "Unknown phar archive \"%s\": %s", ZSTR_VAL(fname), error);
 1272| 			efree(error);
 1273| 		} else {
 1274| 			zend_throw_exception_ex(phar_ce_PharException, 0, "Unknown phar archive \"%s\"", ZSTR_VAL(fname));
 1275| 		}
```

- `read_file(end_line=4425, path=ext/phar/phar_object.c, start_line=4390, version=old)` →

```
ext/phar/phar_object.c lines 4390-4425 of 5059
 4390| 	phar_entry_object *entry_obj;
 4391| 	phar_archive_data *phar_data;
 4392| 	zval arg1;
 4393| 
 4394| 	if (zend_parse_parameters(ZEND_NUM_ARGS(), "p", &fname, &fname_len) == FAILURE) {
 4395| 		RETURN_THROWS();
 4396| 	}
 4397| 
 4398| 	entry_obj = PHAR_FETCH_INTERNAL();
 4399| 
 4400| 	if (entry_obj->entry) {
 4401| 		zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Cannot call constructor twice");
 4402| 		RETURN_THROWS();
 4403| 	}
 4404| 
 4405| 	if (fname_len < 7 || memcmp(fname, "phar://", 7)) {
 4406| 		zend_throw_exception_ex(spl_ce_RuntimeException, 0,
 4407| 			"'%s' is not a valid phar archive URL (must have at least phar://filename.phar)", fname);
 4408| 		RETURN_THROWS();
 4409| 	}
 4410| 
 4411| 	zend_string *entry = NULL;
 4412| 	zend_string *arch = phar_split_fname(fname, fname_len, &entry, 2, 0);
 4413| 	if (!arch) {
 4414| 		zend_throw_exception_ex(spl_ce_RuntimeException, 0,
 4415| 			"'%s' is not a valid phar archive URL (must have at least phar://filename.phar)", fname);
 4416| 		RETURN_THROWS();
 4417| 	}
 4418| 
 4419| 	if (phar_open_from_filename(ZSTR_VAL(arch), ZSTR_LEN(arch), NULL, 0, REPORT_ERRORS, &phar_data, &error) == FAILURE) {
 4420| 		zend_string_release_ex(arch, false);
 4421| 		efree(entry);
 4422| 		if (error) {
 4423| 			zend_throw_exception_ex(spl_ce_RuntimeException, 0,
 4424| 				"Cannot open phar file '%s': %s", fname, error);
 4425| 			efree(error);
```

- `read_file(end_line=150, path=ext/phar/stream.c, start_line=110, version=old)` →

```
ext/phar/stream.c lines 110-150 of 947
  110| 		if (PHAR_G(readonly) && (!pphar || !pphar->is_data)) {
  111| 			if (!(options & PHP_STREAM_URL_STAT_QUIET)) {
  112| 				php_stream_wrapper_log_error(wrapper, options, "phar error: write operations disabled by the php.ini setting phar.readonly");
  113| 			}
  114| 			php_url_free(resource);
  115| 			return NULL;
  116| 		}
  117| 		if (phar_open_or_create_filename(resource->host, NULL, 0, 0, options, &phar, &error) == FAILURE)
  118| 		{
  119| 			if (error) {
  120| 				if (!(options & PHP_STREAM_URL_STAT_QUIET)) {
  121| 					php_stream_wrapper_log_error(wrapper, options, "%s", error);
  122| 				}
  123| 				efree(error);
  124| 			}
  125| 			php_url_free(resource);
  126| 			return NULL;
  127| 		}
  128| 		if (phar->is_persistent && FAILURE == phar_copy_on_write(&phar)) {
  129| 			if (error) {
  130| 				spprintf(&error, 0, "Cannot open cached phar '%s' as writeable, copy on write failed", ZSTR_VAL(resource->host));
  131| 				if (!(options & PHP_STREAM_URL_STAT_QUIET)) {
  132| 					php_stream_wrapper_log_error(wrapper, options, "%s", error);
  133| 				}
  134| 				efree(error);
  135| 			}
  136| 			php_url_free(resource);
  137| 			return NULL;
  138| 		}
  139| 	} else {
  140| 		if (phar_open_from_filename(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, options, NULL, &error) == FAILURE)
  141| 		{
  142| 			if (error) {
  143| 				if (!(options & PHP_STREAM_URL_STAT_QUIET)) {
  144| 					php_stream_wrapper_log_error(wrapper, options, "%s", error);
  145| 				}
  146| 				efree(error);
  147| 			}
  148| 			php_url_free(resource);
  149| 			return NULL;
  150| 		}
```

### Turn 3  _(tok 6690+174, stop=tool_use)_

**Reasoning:** Need to find the function containing phar.c:134 and stream.c:140. Need to look for where these functions start.

For phar.c:134 — I've already confirmed part of the code. Need to find where this function begins. I'll try searching around lines 80–100.

For stream.c:140 — need to find the beginning of the function. I'll try searching around lines 60–110.

- `read_file(end_line=100, path=ext/phar/phar.c, start_line=75, version=old)` →

```
ext/phar/phar.c lines 75-100 of 3495
   75| 		PHAR_G(readonly) = ini;
   76| 		if (PHAR_G(request_init) && HT_IS_INITIALIZED(&PHAR_G(phar_fname_map))) {
   77| 			zend_hash_apply_with_argument(&(PHAR_G(phar_fname_map)), phar_set_writeable_bit, (void *)&ini);
   78| 		}
   79| 	} else {
   80| 		PHAR_G(require_hash) = ini;
   81| 	}
   82| 
   83| 	return SUCCESS;
   84| }
   85| /* }}}*/
   86| 
   87| /* this global stores the global cached pre-parsed manifests */
   88| HashTable cached_phars;
   89| HashTable cached_alias;
   90| 
   91| static void phar_split_cache_list(void) /* {{{ */
   92| {
   93| 	char *tmp;
   94| 	char *key, *lasts;
   95| 	char ds[2];
   96| 	phar_archive_data *phar;
   97| 	uint32_t i = 0;
   98| 
   99| 	if (!PHAR_G(cache_list) || !(PHAR_G(cache_list)[0])) {
  100| 		return;
```

### Turn 4  _(tok 7249+106, stop=tool_use)_

**Reasoning:** phar.c:134 is inside `phar_split_cache_list`.

Next is stream.c:140 — need to look for the beginning of that function.


- `read_file(end_line=110, path=ext/phar/stream.c, start_line=60, version=old)` →

```
ext/phar/stream.c lines 60-110 of 947
   60| 	php_url *resource;
   61| 	char *error;
   62| 
   63| 	if (strncasecmp(filename, "phar://", 7)) {
   64| 		return NULL;
   65| 	}
   66| 	if (mode[0] == 'a') {
   67| 		if (!(options & PHP_STREAM_URL_STAT_QUIET)) {
   68| 			php_stream_wrapper_log_error(wrapper, options, "phar error: open mode append not supported");
   69| 		}
   70| 		return NULL;
   71| 	}
   72| 
   73| 	zend_string *entry = NULL;
   74| 	const char *arch_error = NULL;
   75| 	zend_string *arch = phar_split_fname_ex(filename, strlen(filename), &entry, 2, (mode[0] == 'w' ? 2 : 0), &arch_error);
   76| 	if (!arch) {
   77| 		if (!(options & PHP_STREAM_URL_STAT_QUIET)) {
   78| 			if (arch_error && !entry) {
   79| 				php_stream_wrapper_log_error(wrapper, options, "phar error: no directory in \"%s\", must have at least phar://%s/ for root directory (always use full path to a new phar)", filename, arch_error);
   80| 			} else {
   81| 				php_stream_wrapper_log_error(wrapper, options, "phar error: invalid url or non-existent phar \"%s\"", filename);
   82| 			}
   83| 		}
   84| 		return NULL;
   85| 	}
   86| 	resource = ecalloc(1, sizeof(php_url));
   87| 	resource->scheme = ZSTR_INIT_LITERAL("phar", 0);
   88| 	resource->host = arch;
   89| 	resource->path = entry;
   90| 
   91| #ifdef MBO_0
   92| 		if (resource) {
   93| 			fprintf(stderr, "Alias:     %s\n", alias);
   94| 			fprintf(stderr, "Scheme:    %s\n", ZSTR_VAL(resource->scheme));
   95| /*			fprintf(stderr, "User:      %s\n", resource->user);*/
   96| /*			fprintf(stderr, "Pass:      %s\n", resource->pass ? "***" : NULL);*/
   97| 			fprintf(stderr, "Host:      %s\n", ZSTR_VAL(resource->host));
   98| /*			fprintf(stderr, "Port:      %d\n", resource->port);*/
   99| 			fprintf(stderr, "Path:      %s\n", ZSTR_VAL(resource->path));
  100| /*			fprintf(stderr, "Query:     %s\n", resource->query);*/
  101| /*			fprintf(stderr, "Fragment:  %s\n", resource->fragment);*/
  102| 		}
  103| #endif
  104| 	if (mode[0] == 'w' || (mode[0] == 'r' && mode[1] == '+')) {
  105| 		phar_archive_data *pphar = NULL, *phar;
  106| 
  107| 		if (PHAR_G(request_init) && HT_IS_INITIALIZED(&PHAR_G(phar_fname_map)) && NULL == (pphar = zend_hash_find_ptr(&(PHAR_G(phar_fname_map)), resource->host))) {
  108| 			pphar = NULL;
  109| 		}
  110| 		if (PHAR_G(readonly) && (!pphar || !pphar->is_data)) {
```

### Turn 5  _(tok 8339+111, stop=tool_use)_

**Reasoning:** Need to find the name of the function that contains line 140 of stream.c. The function seems to start around line 55. I'll try reading lines 50–60.


- `read_file(end_line=60, path=ext/phar/stream.c, start_line=50, version=old)` →

```
ext/phar/stream.c lines 50-60 of 947
   50| 	&phar_stream_wops,
   51| 	NULL,
   52| 	0 /* is_url */
   53| };
   54| 
   55| /**
   56|  * Open a phar file for streams API
   57|  */
   58| php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options) /* {{{ */
   59| {
   60| 	php_url *resource;
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 8160+461, stop=tool_use, forced)_

**Reasoning:** I have already identified all 6 call sites and their corresponding functions:

1. ext/phar/phar.c:134 — `phar_split_cache_list`
2. ext/phar/phar.c:3161 — `phar_compile_file`
3. ext/phar/phar_object.c:982 — `PHP_METHOD(Phar, loadPhar)` → `zim_Phar_loadPhar` / PHP_METHOD(Phar, loadPhar)
4. ext/phar/phar_object.c:1269 — `PHP_METHOD(Phar, unlinkArchive)`
5. ext/phar/phar_object.c:4419 — need to confirm the function name. I read from line 4390, but couldn't confirm the function's starting position. Probably `PHP_METHOD(PharFileInfo, __construct)`. The line number is approximately 4385. Given the context (entry_obj = PHAR_FETCH_INTERNAL(), "Cannot call constructor twice", phar_split_fname with a phar:// URL), this is PharFileInfo::__construct. I'll note it as PHP_METHOD(PharFileInfo, __construct).
6. ext/phar/stream.c:140 — `phar_parse_url`

I'm fairly confident about #5. Let's submit.


- **submit_callers** → `{"callers": [{"function": "phar_split_cache_list", "file": "ext/phar/phar.c"}, {"function": "phar_compile_file", "file": "ext/phar/phar.c"}, {"function": "PHP_METHOD(Phar, loadPhar)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, unlinkArchive)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(PharFileInfo, __construct)", "file": "ext/phar/phar_object.c"}, {"function": "phar_parse_url", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 6, "n_truth": 6, "tp": 6, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

