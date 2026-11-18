# Impact-analysis transcript — php-src @ b04136ee71db — openrouter:deepseek/deepseek-v4-pro

- target: `phar_open_from_filename` (ext/phar/phar.c), arity 7->6
- truth: [['ext/phar/phar.c', 'phar_compile_file'], ['ext/phar/phar.c', 'phar_split_cache_list'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, loadPhar)'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, unlinkArchive)'], ['ext/phar/phar_object.c', 'PHP_METHOD(PharFileInfo, __construct)'], ['ext/phar/stream.c', 'phar_parse_url']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1029+67, stop=tool_use)_

**Reasoning:** Let me find all references to `phar_open_from_filename` across the repository.

- `find_references(name=phar_open_from_filename)` →

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

### Turn 2  _(tok 1501+607, stop=tool_use)_

**Reasoning:** I need to find the enclosing functions for each of these references. Let me look at each reference more carefully.

1. ext/phar/phar.c line 134 - I need to see the enclosing function
2. ext/phar/phar.c line 3161 - I need to see the enclosing function
3. ext/phar/phar_internal.h line 409 - This is the prototype/declaration, skip
4. ext/phar/phar_object.c line 982 - need enclosing function
5. ext/phar/phar_object.c line 1269 - need enclosing function
6. ext/phar/phar_object.c line 4419 - need enclosing function
7. ext/phar/stream.c line 140 - need enclosing function

Let me read around each of these to find the enclosing functions.

- `read_file(path=ext/phar/phar.c, start_line=115, end_line=145)` →

```
ext/phar/phar.c lines 115-145 of 3495
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
  141| 			efree(tmp);
  142| 			zend_hash_destroy(&(PHAR_G(phar_fname_map)));
  143| 			HT_INVALIDATE(&PHAR_G(phar_fname_map));
  144| 			zend_hash_destroy(&(PHAR_G(phar_alias_map)));
  145| 			HT_INVALIDATE(&PHAR_G(phar_alias_map));
```

- `read_file(path=ext/phar/phar.c, start_line=3140, end_line=3175)` →

```
ext/phar/phar.c lines 3140-3175 of 3495
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
 3166| 				name = zend_strpprintf(4096, "phar://%s/%s", ZSTR_VAL(file_handle->filename), ".phar/stub.php");
 3167| 				zend_stream_init_filename_ex(&f, name);
 3168| 				if (SUCCESS == zend_stream_open_function(&f)) {
 3169| 					zend_string_release(f.filename);
 3170| 					f.filename = file_handle->filename;
 3171| 					if (f.opened_path) {
 3172| 						zend_string_release(f.opened_path);
 3173| 					}
 3174| 					f.opened_path = file_handle->opened_path;
 3175| 
```

- `read_file(path=ext/phar/phar_object.c, start_line=960, end_line=995)` →

```
ext/phar/phar_object.c lines 960-995 of 5059
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
  991| PHP_METHOD(Phar, apiVersion)
  992| {
  993| 	ZEND_PARSE_PARAMETERS_NONE();
  994| 	RETURN_STRINGL(PHP_PHAR_API_VERSION, sizeof(PHP_PHAR_API_VERSION)-1);
  995| }
```

- `read_file(path=ext/phar/phar_object.c, start_line=1245, end_line=1280)` →

```
ext/phar/phar_object.c lines 1245-1280 of 5059
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
 1276| 		RETURN_THROWS();
 1277| 	}
 1278| 
 1279| 	const zend_string *zend_file_name = zend_get_executed_filename_ex();
 1280| 	if (zend_file_name && zend_string_starts_with_literal_ci(zend_file_name, "phar://")) {
```

- `read_file(path=ext/phar/phar_object.c, start_line=4398, end_line=4430)` →

```
ext/phar/phar_object.c lines 4398-4430 of 5059
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
 4426| 		} else {
 4427| 			zend_throw_exception_ex(spl_ce_RuntimeException, 0,
 4428| 				"Cannot open phar file '%s'", fname);
 4429| 		}
 4430| 		RETURN_THROWS();
```

- `read_file(path=ext/phar/stream.c, start_line=120, end_line=150)` →

```
ext/phar/stream.c lines 120-150 of 947
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

### Turn 3  _(tok 5426+431, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing function for each of these. Let me look at what function each reference is in.

1. ext/phar/phar.c line 134 - I need to scroll up to find the function
2. ext/phar/phar.c line 3161 - This is in `phar_compile_file` (line 3150)
3. ext/phar/phar_object.c line 982 - This is in `PHP_METHOD(Phar, loadPhar)` (line 970)
4. ext/phar/phar_object.c line 1269 - This is in `PHP_METHOD(Phar, unlinkArchive)` (line 1254)
5. ext/phar/phar_object.c line 4419 - Need to find the enclosing function
6. ext/phar/stream.c line 140 - Need to find the enclosing function

Let me look at the first one and the stream.c one and the phar_object.c line 4419.

- `read_file(end_line=115, path=ext/phar/phar.c, start_line=90)` →

```
ext/phar/phar.c lines 90-115 of 3495
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
```

- `read_file(end_line=120, path=ext/phar/stream.c, start_line=80)` →

```
ext/phar/stream.c lines 80-120 of 947
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
```

- `read_file(end_line=4405, path=ext/phar/phar_object.c, start_line=4375)` →

```
ext/phar/phar_object.c lines 4375-4405 of 5059
 4375| 		zend_throw_exception_ex(phar_ce_PharException, 0,
 4376| 			"phar error: attempted to extract non-existent file or directory \"%s\" from phar \"%s\"",
 4377| 			ZSTR_VAL(filename), ZSTR_VAL(phar_obj->archive->fname));
 4378| 	} else {
 4379| 		RETURN_TRUE;
 4380| 	}
 4381| }
 4382| /* }}} */
 4383| 
 4384| 
 4385| /* {{{ Construct a Phar entry object */
 4386| PHP_METHOD(PharFileInfo, __construct)
 4387| {
 4388| 	char *fname, *error;
 4389| 	size_t fname_len;
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
```

### Turn 4  _(tok 7470+111, stop=tool_use)_

**Reasoning:** Now let me find the enclosing function for stream.c line 140. I need to find the function that starts before line 80.

- `read_file(end_line=70, path=ext/phar/stream.c, start_line=45)` →

```
ext/phar/stream.c lines 45-70 of 947
   45| 	phar_wrapper_rmdir,    /* remove directory */
   46| 	NULL
   47| };
   48| 
   49| const php_stream_wrapper php_stream_phar_wrapper = {
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
```

### Turn 5  _(tok 7886+785, stop=tool_use)_

**Reasoning:** Now I have all the enclosing functions:

1. ext/phar/phar.c line 134 → `phar_split_cache_list` (line 91)
2. ext/phar/phar.c line 3161 → `phar_compile_file` (line 3150)
3. ext/phar/phar_object.c line 982 → `PHP_METHOD(Phar, loadPhar)` (line 970) — in C, the function is `zim_Phar_loadPhar`
4. ext/phar/phar_object.c line 1269 → `PHP_METHOD(Phar, unlinkArchive)` (line 1254) — `zim_Phar_unlinkArchive`
5. ext/phar/phar_object.c line 4419 → `PHP_METHOD(PharFileInfo, __construct)` (line 4386) — `zim_PharFileInfo___construct`
6. ext/phar/stream.c line 140 → `phar_parse_url` (line 58)

Now, for PHP_METHOD macros, those expand to function definitions. Let me confirm the actual C function names. In PHP, `PHP_METHOD(Phar, loadPhar)` expands to `void zim_Phar_loadPhar(zend_execute_data *execute_data, zval *return_value)`. But the question says "the enclosing function name". I think the function names would be `zim_Phar_loadPhar`, `zim_Phar_unlinkArchive`, `zim_PharFileInfo___construct` — or if they prefer the PHP_METHOD notation. Let me use the actual C function names since the question asks for function names.

Actually, looking at this more carefully, the PHP_METHOD macro defines a C function. The convention in PHP source is `zim_<class>_<method>`. But some tools and developers also refer to them as `PHP_METHOD(Phar, loadPhar)`. Let me just use the actual C function name that the macro produces: `zim_Phar_loadPhar`, `zim_Phar_unlinkArchive`, `zim_PharFileInfo___construct`.

Let me verify the line 140 call in stream.c more carefully. The function is `phar_parse_url`.

So the complete list:

1. `phar_split_cache_list` - ext/phar/phar.c
2. `phar_compile_file` - ext/phar/phar.c
3. `zim_Phar_loadPhar` - ext/phar/phar_object.c
4. `zim_Phar_unlinkArchive` - ext/phar/phar_object.c
5. `zim_PharFileInfo___construct` - ext/phar/phar_object.c
6. `phar_parse_url` - ext/phar/stream.c

Let me double-check that the phar_internal.h entry at line 409 is indeed the declaration/prototype and not a call site - the find_references output says "phar_internal.h" which is a header, and the text shows `zend_result phar_open_from_filename(...)` which looks like a prototype. Yes, that's the declaration.

I'm confident in these 6 callers.

**Says:** Now let me verify by reading the reference in the header to confirm it's just the prototype (not a call):

- `read_file(end_line=410, path=ext/phar/phar_internal.h, start_line=407)` →

```
ext/phar/phar_internal.h lines 407-410 of 492
  407| 
  408| ZEND_ATTRIBUTE_NONNULL zend_result phar_postprocess_file(phar_entry_data *idata, uint32_t crc32, char **error, int process_zip);
  409| zend_result phar_open_from_filename(char *fname, size_t fname_len, const char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error);
  410| ZEND_ATTRIBUTE_NONNULL_ARGS(1, 6, 7) zend_result phar_open_or_create_filename(zend_string *fname, const char *alias, size_t alias_len, bool is_data, uint32_t options, phar_archive_data** pphar, char **error);
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 8890+346, stop=tool_use, forced)_

**Reasoning:** All confirmed. The 6 call sites and their enclosing functions:

1. `phar_split_cache_list` - ext/phar/phar.c
2. `phar_compile_file` - ext/phar/phar.c
3. `zim_Phar_loadPhar` - ext/phar/phar_object.c
4. `zim_Phar_unlinkArchive` - ext/phar/phar_object.c
5. `zim_PharFileInfo___construct` - ext/phar/phar_object.c
6. `phar_parse_url` - ext/phar/stream.c

The header at line 409 is indeed the prototype/declaration, not a call site.

- **submit_callers** → `{"callers": [{"function": "phar_split_cache_list", "file": "ext/phar/phar.c"}, {"function": "phar_compile_file", "file": "ext/phar/phar.c"}, {"function": "zim_Phar_loadPhar", "file": "ext/phar/phar_object.c"}, {"function": "zim_Phar_unlinkArchive", "file": "ext/phar/phar_object.c"}, {"function": "zim_PharFileInfo___construct", "file": "ext/phar/phar_object.c"}, {"function": "phar_parse_url", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 6, "n_truth": 6, "tp": 6, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

