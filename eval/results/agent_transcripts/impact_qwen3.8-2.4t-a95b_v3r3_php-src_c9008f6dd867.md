# Impact-analysis transcript — php-src @ c9008f6dd867 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `phar_get_or_create_entry_data` (ext/phar/util.c), arity 8->9
- truth: [['ext/phar/phar_object.c', 'phar_add_file'], ['ext/phar/phar_object.c', 'phar_build'], ['ext/phar/phar_object.c', 'phar_mkdir'], ['ext/phar/stream.c', 'phar_wrapper_open_url']]

## Self-navigation arm

### Turn 1  _(tok 948+72, stop=tool_use)_

**Reasoning:** I'll search for all occurrences of the function name.


- `grep(pattern=phar_get_or_create_entry_data, version=old, max_results=200)` →

```
7 matches
ext/phar/phar.c:402:		/* if phar_get_or_create_entry_data returns a sub-directory, we have to free it */
ext/phar/phar_internal.h:467:ZEND_ATTRIBUTE_NONNULL phar_entry_data *phar_get_or_create_entry_data(char *fname, size_t fname_len, char *path, size_t path_len, const char *mode, char allow_dir, char **
ext/phar/phar_object.c:1581:	if (!(data = phar_get_or_create_entry_data(phar_obj->archive->fname, phar_obj->archive->fname_len, str_key, str_key_len, "w+b", 0, &error, true))) {
ext/phar/phar_object.c:3539:	if (!(data = phar_get_or_create_entry_data((*pphar)->fname, (*pphar)->fname_len, filename, filename_len, "w+b", 0, &error, true))) {
ext/phar/phar_object.c:3611:	if (!(data = phar_get_or_create_entry_data((*pphar)->fname, (*pphar)->fname_len, ZSTR_VAL(dir_name), ZSTR_LEN(dir_name), "w+b", 2, &error, true))) {
ext/phar/stream.c:194:		if (NULL == (idata = phar_get_or_create_entry_data(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), internal_file, strlen(internal_file), mode, 0, &error, true))) {
ext/phar/util.c:609:ZEND_ATTRIBUTE_NONNULL phar_entry_data *phar_get_or_create_entry_data(char *fname, size_t fname_len, char *path, size_t path_len, const char *mode, char allow_dir, char **error, bo
```

### Turn 2  _(tok 1389+237, stop=tool_use)_

**Reasoning:** I need to find the functions that enclose each call site. I'll read around each line.


- `read_file(path=ext/phar/phar_object.c, start_line=1500, end_line=1590, version=old)` →

```
ext/phar/phar_object.c lines 1500-1590 of 4994
 1500| 
 1501| 			return ZEND_HASH_APPLY_STOP;
 1502| 		}
 1503| 	} else {
 1504| 		if (iter->funcs->get_current_key) {
 1505| 			zval key;
 1506| 			iter->funcs->get_current_key(iter, &key);
 1507| 
 1508| 			if (EG(exception)) {
 1509| 				return ZEND_HASH_APPLY_STOP;
 1510| 			}
 1511| 
 1512| 			if (Z_TYPE(key) != IS_STRING) {
 1513| 				zval_ptr_dtor(&key);
 1514| 				zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0, "Iterator %s returned an invalid key (must return a string)", ZSTR_VAL(ce->name));
 1515| 				return ZEND_HASH_APPLY_STOP;
 1516| 			}
 1517| 
 1518| 			str_key_len = Z_STRLEN(key);
 1519| 			str_key = estrndup(Z_STRVAL(key), str_key_len);
 1520| 
 1521| 			save = str_key;
 1522| 			zval_ptr_dtor_str(&key);
 1523| 		} else {
 1524| 			zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0, "Iterator %s returned an invalid key (must return a string)", ZSTR_VAL(ce->name));
 1525| 			return ZEND_HASH_APPLY_STOP;
 1526| 		}
 1527| 	}
 1528| 
 1529| 	if (php_check_open_basedir(fname)) {
 1530| 		zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0, "Iterator %s returned a path \"%s\" that open_basedir prevents opening", ZSTR_VAL(ce->name), fname);
 1531| 
 1532| 		if (save) {
 1533| 			efree(save);
 1534| 		}
 1535| 
 1536| 		if (temp) {
 1537| 			efree(temp);
 1538| 		}
 1539| 
 1540| 		return ZEND_HASH_APPLY_STOP;
 1541| 	}
 1542| 
 1543| 	/* try to open source file, then create internal phar file and copy contents */
 1544| 	fp = php_stream_open_wrapper(fname, "rb", STREAM_MUST_SEEK|0, &opened);
 1545| 
 1546| 	if (!fp) {
 1547| 		zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0, "Iterator %s returned a file that could not be opened \"%s\"", ZSTR_VAL(ce->name), fname);
 1548| 
 1549| 		if (save) {
 1550| 			efree(save);
 1551| 		}
 1552| 
 1553| 		if (temp) {
 1554| 			efree(temp);
 1555| 		}
 1556| 
 1557| 		return ZEND_HASH_APPLY_STOP;
 1558| 	}
 1559| after_open_fp:
 1560| 	if (str_key_len >= sizeof(".phar")-1 && !memcmp(str_key, ".phar", sizeof(".phar")-1)) {
 1561| 		/* silently skip any files that would be added to the magic .phar directory */
 1562| 		if (save) {
 1563| 			efree(save);
 1564| 		}
 1565| 
 1566| 		if (temp) {
 1567| 			efree(temp);
 1568| 		}
 1569| 
 1570| 		if (opened) {
 1571| 			zend_string_release_ex(opened, 0);
 1572| 		}
 1573| 
 1574| 		if (close_fp) {
 1575| 			php_stream_close(fp);
 1576| 		}
 1577| 
 1578| 		return ZEND_HASH_APPLY_KEEP;
 1579| 	}
 1580| 
 1581| 	if (!(data = phar_get_or_create_entry_data(phar_obj->archive->fname, phar_obj->archive->fname_len, str_key, str_key_len, "w+b", 0, &error, true))) {
 1582| 		zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Entry %s cannot be created: %s", str_key, error);
 1583| 		efree(error);
 1584| 
 1585| 		if (save) {
 1586| 			efree(save);
 1587| 		}
 1588| 
 1589| 		if (opened) {
 1590| 			zend_string_release_ex(opened, 0);
```

- `read_file(path=ext/phar/phar_object.c, start_line=3450, end_line=3620, version=old)` →

```
ext/phar/phar_object.c lines 3450-3620 of 4994
 3450| /* }}} */
 3451| 
 3452| /* {{{ get a PharFileInfo object for a specific file */
 3453| PHP_METHOD(Phar, offsetGet)
 3454| {
 3455| 	char *error;
 3456| 	phar_entry_info *entry;
 3457| 	zend_string *file_name = NULL;
 3458| 
 3459| 	if (zend_parse_parameters(ZEND_NUM_ARGS(), "P", &file_name) == FAILURE) {
 3460| 		RETURN_THROWS();
 3461| 	}
 3462| 
 3463| 	PHAR_ARCHIVE_OBJECT();
 3464| 
 3465| 	/* security is 0 here so that we can get a better error message than "entry doesn't exist" */
 3466| 	if (!(entry = phar_get_entry_info_dir(phar_obj->archive, ZSTR_VAL(file_name), ZSTR_LEN(file_name), 1, &error, false))) {
 3467| 		zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Entry %s does not exist%s%s", ZSTR_VAL(file_name), error?", ":"", error?error:"");
 3468| 	} else {
 3469| 		if (zend_string_equals_literal(file_name, ".phar/stub.php")) {
 3470| 			zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Cannot get stub \".phar/stub.php\" directly in phar \"%s\", use getStub", phar_obj->archive->fname);
 3471| 			RETURN_THROWS();
 3472| 		}
 3473| 
 3474| 		if (zend_string_equals_literal(file_name, ".phar/alias.txt")) {
 3475| 			zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Cannot get alias \".phar/alias.txt\" directly in phar \"%s\", use getAlias", phar_obj->archive->fname);
 3476| 			RETURN_THROWS();
 3477| 		}
 3478| 
 3479| 		if (zend_string_starts_with_literal(file_name, ".phar")) {
 3480| 			zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Cannot directly get any files or directories in magic \".phar\" directory");
 3481| 			RETURN_THROWS();
 3482| 		}
 3483| 
 3484| 		if (entry->is_temp_dir) {
 3485| 			zend_string_efree(entry->filename);
 3486| 			efree(entry);
 3487| 		}
 3488| 
 3489| 		zend_string *sfname = strpprintf(0, "phar://%s/%s", phar_obj->archive->fname, ZSTR_VAL(file_name));
 3490| 		zval zfname;
 3491| 		ZVAL_NEW_STR(&zfname, sfname);
 3492| 
 3493| 		/* Instantiate object and call constructor */
 3494| 		zend_result is_initialized = object_init_with_constructor(return_value, phar_obj->spl.info_class, 1, &zfname, NULL);
 3495| 		zend_string_release_ex(sfname, false);
 3496| 		if (is_initialized == FAILURE) {
 3497| 			RETURN_THROWS();
 3498| 		}
 3499| 	}
 3500| }
 3501| /* }}} */
 3502| 
 3503| /* {{{ add a file within the phar archive from a string or resource */
 3504| static void phar_add_file(phar_archive_data **pphar, zend_string *file_name, const zend_string *content, zval *zresource)
 3505| {
 3506| 	char *error;
 3507| 	phar_entry_data *data;
 3508| 	php_stream *contents_file = NULL;
 3509| 	php_stream_statbuf ssb;
 3510| #ifdef PHP_WIN32
 3511| 	char *save_filename;
 3512| 	ALLOCA_FLAG(filename_use_heap)
 3513| #endif
 3514| 
 3515| 	if (
 3516| 		zend_string_starts_with_literal(file_name, ".phar")
 3517| 		|| zend_string_starts_with_literal(file_name, "/.phar")
 3518| 	) {
 3519| 		size_t prefix_len = (ZSTR_VAL(file_name)[0] == '/') + sizeof(".phar")-1;
 3520| 		char next_char = ZSTR_VAL(file_name)[prefix_len];
 3521| 		if (next_char == '/' || next_char == '\\' || next_char == '\0') {
 3522| 			zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Cannot create any files in magic \".phar\" directory");
 3523| 			return;
 3524| 		}
 3525| 	}
 3526| 
 3527| 	/* TODO How to handle Windows path normalisation with zend_string ? */
 3528| 	char *filename = ZSTR_VAL(file_name);
 3529| 	size_t filename_len = ZSTR_LEN(file_name);
 3530| #ifdef PHP_WIN32
 3531| 	save_filename = filename;
 3532| 	if (memchr(filename, '\\', filename_len)) {
 3533| 		filename = do_alloca(filename_len + 1, filename_use_heap);
 3534| 		memcpy(filename, save_filename, filename_len);
 3535| 		filename[filename_len] = '\0';
 3536| 	}
 3537| #endif
 3538| 
 3539| 	if (!(data = phar_get_or_create_entry_data((*pphar)->fname, (*pphar)->fname_len, filename, filename_len, "w+b", 0, &error, true))) {
 3540| 		if (error) {
 3541| 			zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Entry %s does not exist and cannot be created: %s", filename, error);
 3542| 			efree(error);
 3543| 		} else {
 3544| 			zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Entry %s does not exist and cannot be created", filename);
 3545| 		}
 3546| 		goto finish;
 3547| 	} else {
 3548| 		if (error) {
 3549| 			efree(error);
 3550| 		}
 3551| 
 3552| 		if (!data->internal_file->is_dir) {
 3553| 			size_t contents_len = 0;
 3554| 			if (content) {
 3555| 				contents_len = ZSTR_LEN(content);
 3556| 				size_t written_len = php_stream_write(data->fp, ZSTR_VAL(content), ZSTR_LEN(content));
 3557| 				if (written_len != contents_len) {
 3558| 					zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Entry %s could not be written to", filename);
 3559| 					goto finish;
 3560| 				}
 3561| 			} else {
 3562| 				if (!(php_stream_from_zval_no_verify(contents_file, zresource))) {
 3563| 					zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Entry %s could not be written to", filename);
 3564| 					goto finish;
 3565| 				}
 3566| 				php_stream_copy_to_stream_ex(contents_file, data->fp, PHP_STREAM_COPY_ALL, &contents_len);
 3567| 			}
 3568| 			data->internal_file->compressed_filesize = data->internal_file->uncompressed_filesize = contents_len;
 3569| 		}
 3570| 
 3571| 		if (contents_file != NULL && php_stream_stat(contents_file, &ssb) != -1) {
 3572| 			data->internal_file->flags = ssb.sb.st_mode & PHAR_ENT_PERM_MASK ;
 3573| 		} else {
 3574| #ifndef _WIN32
 3575| 			mode_t mask;
 3576| 			mask = umask(0);
 3577| 			umask(mask);
 3578| 			data->internal_file->flags &= ~mask;
 3579| #endif
 3580| 		}
 3581| 
 3582| 		/* check for copy-on-write */
 3583| 		if (pphar[0] != data->phar) {
 3584| 			*pphar = data->phar;
 3585| 		}
 3586| 		phar_entry_delref(data);
 3587| 		phar_flush(*pphar, &error);
 3588| 
 3589| 		if (error) {
 3590| 			zend_throw_exception_ex(phar_ce_PharException, 0, "%s", error);
 3591| 			efree(error);
 3592| 		}
 3593| 	}
 3594| 
 3595| finish: ;
 3596| #ifdef PHP_WIN32
 3597| 	if (filename != save_filename) {
 3598| 		free_alloca(filename, filename_use_heap);
 3599| 		filename = save_filename;
 3600| 	}
 3601| #endif
 3602| }
 3603| /* }}} */
 3604| 
 3605| /* {{{ create a directory within the phar archive */
 3606| static void phar_mkdir(phar_archive_data **pphar, zend_string *dir_name)
 3607| {
 3608| 	char *error;
 3609| 	phar_entry_data *data;
 3610| 
 3611| 	if (!(data = phar_get_or_create_entry_data((*pphar)->fname, (*pphar)->fname_len, ZSTR_VAL(dir_name), ZSTR_LEN(dir_name), "w+b", 2, &error, true))) {
 3612| 		if (error) {
 3613| 			zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Directory %s does not exist and cannot be created: %s", ZSTR_VAL(dir_name), error);
 3614| 			efree(error);
 3615| 		} else {
 3616| 			zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Directory %s does not exist and cannot be created", ZSTR_VAL(dir_name));
 3617| 		}
 3618| 
 3619| 		return;
 3620| 	} else {
```

- `read_file(path=ext/phar/stream.c, start_line=120, end_line=200, version=old)` →

```
ext/phar/stream.c lines 120-200 of 957
  120| 		{
  121| 			if (error) {
  122| 				if (!(options & PHP_STREAM_URL_STAT_QUIET)) {
  123| 					php_stream_wrapper_log_error(wrapper, options, "%s", error);
  124| 				}
  125| 				efree(error);
  126| 			}
  127| 			php_url_free(resource);
  128| 			return NULL;
  129| 		}
  130| 		if (phar->is_persistent && FAILURE == phar_copy_on_write(&phar)) {
  131| 			if (error) {
  132| 				spprintf(&error, 0, "Cannot open cached phar '%s' as writeable, copy on write failed", ZSTR_VAL(resource->host));
  133| 				if (!(options & PHP_STREAM_URL_STAT_QUIET)) {
  134| 					php_stream_wrapper_log_error(wrapper, options, "%s", error);
  135| 				}
  136| 				efree(error);
  137| 			}
  138| 			php_url_free(resource);
  139| 			return NULL;
  140| 		}
  141| 	} else {
  142| 		if (phar_open_from_filename(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, options, NULL, &error) == FAILURE)
  143| 		{
  144| 			if (error) {
  145| 				if (!(options & PHP_STREAM_URL_STAT_QUIET)) {
  146| 					php_stream_wrapper_log_error(wrapper, options, "%s", error);
  147| 				}
  148| 				efree(error);
  149| 			}
  150| 			php_url_free(resource);
  151| 			return NULL;
  152| 		}
  153| 	}
  154| 	return resource;
  155| }
  156| /* }}} */
  157| 
  158| /**
  159|  * used for fopen('phar://...') and company
  160|  */
  161| static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /* {{{ */
  162| {
  163| 	phar_archive_data *phar;
  164| 	phar_entry_data *idata;
  165| 	char *internal_file;
  166| 	char *error;
  167| 	HashTable *pharcontext;
  168| 	php_url *resource = NULL;
  169| 	php_stream *fpf;
  170| 	zval *pzoption, *metadata;
  171| 
  172| 	if ((resource = phar_parse_url(wrapper, path, mode, options)) == NULL) {
  173| 		return NULL;
  174| 	}
  175| 
  176| 	/* we must have at the very least phar://alias.phar/internalfile.php */
  177| 	if (!resource->scheme || !resource->host || !resource->path) {
  178| 		php_url_free(resource);
  179| 		php_stream_wrapper_log_error(wrapper, options, "phar error: invalid url \"%s\"", path);
  180| 		return NULL;
  181| 	}
  182| 
  183| 	if (!zend_string_equals_literal_ci(resource->scheme, "phar")) {
  184| 		php_url_free(resource);
  185| 		php_stream_wrapper_log_error(wrapper, options, "phar error: not a phar stream url \"%s\"", path);
  186| 		return NULL;
  187| 	}
  188| 
  189| 	phar_request_initialize();
  190| 
  191| 	/* strip leading "/" */
  192| 	internal_file = estrndup(ZSTR_VAL(resource->path) + 1, ZSTR_LEN(resource->path) - 1);
  193| 	if (mode[0] == 'w' || (mode[0] == 'r' && mode[1] == '+')) {
  194| 		if (NULL == (idata = phar_get_or_create_entry_data(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), internal_file, strlen(internal_file), mode, 0, &error, true))) {
  195| 			if (error) {
  196| 				php_stream_wrapper_log_error(wrapper, options, "%s", error);
  197| 				efree(error);
  198| 			} else {
  199| 				php_stream_wrapper_log_error(wrapper, options, "phar error: file \"%s\" could not be created in phar \"%s\"", internal_file, ZSTR_VAL(resource->host));
  200| 			}
```

### Turn 3  _(tok 7374+154, stop=tool_use)_

**Reasoning:** The call on line 194 of stream.c is inside `phar_wrapper_open_url` (a static function that starts on line 161). Let me confirm — yes, that's right.

Line 1581 of phar_object.c — I need to find the enclosing function. Let me try searching for function definitions around line 1400.


- `read_file(path=ext/phar/phar_object.c, start_line=1380, end_line=1500, version=old)` →

```
ext/phar/phar_object.c lines 1380-1500 of 4994
 1380| 			if (!fp) {
 1381| 				zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Iterator %s returned an invalid stream handle", ZSTR_VAL(ce->name));
 1382| 				return ZEND_HASH_APPLY_STOP;
 1383| 			}
 1384| 
 1385| 			if (iter->funcs->get_current_key) {
 1386| 				zval key;
 1387| 				iter->funcs->get_current_key(iter, &key);
 1388| 
 1389| 				if (EG(exception)) {
 1390| 					return ZEND_HASH_APPLY_STOP;
 1391| 				}
 1392| 
 1393| 				if (Z_TYPE(key) != IS_STRING) {
 1394| 					zval_ptr_dtor(&key);
 1395| 					zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0, "Iterator %s returned an invalid key (must return a string)", ZSTR_VAL(ce->name));
 1396| 					return ZEND_HASH_APPLY_STOP;
 1397| 				}
 1398| 
 1399| 				str_key_len = Z_STRLEN(key);
 1400| 				str_key = estrndup(Z_STRVAL(key), str_key_len);
 1401| 
 1402| 				save = str_key;
 1403| 				zval_ptr_dtor_str(&key);
 1404| 			} else {
 1405| 				zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0, "Iterator %s returned an invalid key (must return a string)", ZSTR_VAL(ce->name));
 1406| 				return ZEND_HASH_APPLY_STOP;
 1407| 			}
 1408| 
 1409| 			close_fp = false;
 1410| 			opened = ZSTR_INIT_LITERAL("[stream]", 0);
 1411| 			goto after_open_fp;
 1412| 		case IS_OBJECT:
 1413| 			if (instanceof_function(Z_OBJCE_P(value), spl_ce_SplFileInfo)) {
 1414| 				spl_filesystem_object *intern = PHAR_FETCH_INTERNAL_EX(value);
 1415| 
 1416| 				if (!base_len) {
 1417| 					zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Iterator %s returns an SplFileInfo object, so base directory must be specified", ZSTR_VAL(ce->name));
 1418| 					return ZEND_HASH_APPLY_STOP;
 1419| 				}
 1420| 
 1421| 				switch (intern->type) {
 1422| 					case SPL_FS_DIR: {
 1423| 						char *tmp;
 1424| 						zend_string *test_str = spl_filesystem_object_get_path(intern);
 1425| 						fname_len = spprintf(&tmp, 0, "%s%c%s", ZSTR_VAL(test_str), DEFAULT_SLASH, intern->u.dir.entry.d_name);
 1426| 						zend_string_release_ex(test_str, /* persistent */ false);
 1427| 						if (php_stream_stat_path(tmp, &ssb) == 0 && S_ISDIR(ssb.sb.st_mode)) {
 1428| 							/* ignore directories */
 1429| 							efree(tmp);
 1430| 							return ZEND_HASH_APPLY_KEEP;
 1431| 						}
 1432| 
 1433| 						fname = expand_filepath(tmp, NULL);
 1434| 						efree(tmp);
 1435| 						break;
 1436| 					}
 1437| 					case SPL_FS_INFO:
 1438| 					case SPL_FS_FILE:
 1439| 						fname = expand_filepath(ZSTR_VAL(intern->file_name), NULL);
 1440| 						break;
 1441| 				}
 1442| 
 1443| 				if (!fname) {
 1444| 					zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0, "Could not resolve file path");
 1445| 					return ZEND_HASH_APPLY_STOP;
 1446| 				}
 1447| 
 1448| 				fname_len = strlen(fname);
 1449| 				save = fname;
 1450| 				goto phar_spl_fileinfo;
 1451| 			}
 1452| 			ZEND_FALLTHROUGH;
 1453| 		default:
 1454| 			zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0, "Iterator %s returned an invalid value (must return a string, a stream, or an SplFileInfo object)", ZSTR_VAL(ce->name));
 1455| 			return ZEND_HASH_APPLY_STOP;
 1456| 	}
 1457| 
 1458| 	fname = Z_STRVAL_P(value);
 1459| 	fname_len = Z_STRLEN_P(value);
 1460| 
 1461| phar_spl_fileinfo:
 1462| 	if (base_len) {
 1463| 		temp = expand_filepath(base, NULL);
 1464| 		if (!temp) {
 1465| 			zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0, "Could not resolve file path");
 1466| 			if (save) {
 1467| 				efree(save);
 1468| 			}
 1469| 			return ZEND_HASH_APPLY_STOP;
 1470| 		}
 1471| 
 1472| 		base = temp;
 1473| 		base_len = strlen(base);
 1474| 
 1475| 		if (fname_len >= base_len && strncmp(fname, base, base_len) == 0 && ((ch = fname[base_len - IS_SLASH(base[base_len - 1])]) == '\0' || IS_SLASH(ch))) {
 1476| 			str_key_len = fname_len - base_len;
 1477| 
 1478| 			if (str_key_len <= 0) {
 1479| 				if (save) {
 1480| 					efree(save);
 1481| 					efree(temp);
 1482| 				}
 1483| 				return ZEND_HASH_APPLY_KEEP;
 1484| 			}
 1485| 
 1486| 			str_key = fname + base_len;
 1487| 
 1488| 			if (*str_key == '/' || *str_key == '\\') {
 1489| 				str_key++;
 1490| 				str_key_len--;
 1491| 			}
 1492| 
 1493| 		} else {
 1494| 			zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0, "Iterator %s returned a path \"%s\" that is not in the base directory \"%s\"", ZSTR_VAL(ce->name), fname, base);
 1495| 
 1496| 			if (save) {
 1497| 				efree(save);
 1498| 				efree(temp);
 1499| 			}
 1500| 
```

### Turn 4  _(tok 9470+102, stop=tool_use)_

**Reasoning:** I need to find where this function starts — before line 1380. Let me search for the beginning of the function.

- `read_file(path=ext/phar/phar_object.c, start_line=1280, end_line=1380, version=old)` →

```
ext/phar/phar_object.c lines 1280-1380 of 4994
 1280| 		}
 1281| 		RETURN_THROWS();
 1282| 	}
 1283| 
 1284| 	zend_string *zend_file_name = zend_get_executed_filename_ex();
 1285| 
 1286| 	if (
 1287| 		zend_file_name
 1288| 		&& zend_string_starts_with_literal_ci(zend_file_name, "phar://")
 1289| 		&& SUCCESS == phar_split_fname(ZSTR_VAL(zend_file_name), ZSTR_LEN(zend_file_name), &arch, &arch_len, NULL, NULL, 2, 0)
 1290| 	) {
 1291| 		if (arch_len == fname_len && !memcmp(arch, fname, arch_len)) {
 1292| 			zend_throw_exception_ex(phar_ce_PharException, 0, "phar archive \"%s\" cannot be unlinked from within itself", fname);
 1293| 			efree(arch);
 1294| 			RETURN_THROWS();
 1295| 		}
 1296| 		efree(arch);
 1297| 	}
 1298| 
 1299| 	if (phar->is_persistent) {
 1300| 		zend_throw_exception_ex(phar_ce_PharException, 0, "phar archive \"%s\" is in phar.cache_list, cannot unlinkArchive()", fname);
 1301| 		RETURN_THROWS();
 1302| 	}
 1303| 
 1304| 	if (phar->refcount) {
 1305| 		zend_throw_exception_ex(phar_ce_PharException, 0, "phar archive \"%s\" has open file handles or objects.  fclose() all file handles, and unset() all objects prior to calling unlinkArchive()", fname);
 1306| 		RETURN_THROWS();
 1307| 	}
 1308| 
 1309| 	fname = estrndup(phar->fname, phar->fname_len);
 1310| 
 1311| 	/* invalidate phar cache */
 1312| 	PHAR_G(last_phar) = NULL;
 1313| 	PHAR_G(last_phar_name) = PHAR_G(last_alias) = NULL;
 1314| 
 1315| 	phar_archive_delref(phar);
 1316| 	unlink(fname);
 1317| 	efree(fname);
 1318| 	RETURN_TRUE;
 1319| }
 1320| /* }}} */
 1321| 
 1322| /* {{{ if persistent, remove from the cache */
 1323| PHP_METHOD(Phar, __destruct)
 1324| {
 1325| 	phar_archive_object *phar_obj = PHAR_FETCH_INTERNAL();
 1326| 
 1327| 	ZEND_PARSE_PARAMETERS_NONE();
 1328| 
 1329| 	if (phar_obj->archive && phar_obj->archive->is_persistent) {
 1330| 		zend_hash_str_del(&PHAR_G(phar_persist_map), (const char *) phar_obj->archive, sizeof(phar_obj->archive));
 1331| 	}
 1332| }
 1333| /* }}} */
 1334| 
 1335| struct _phar_t {
 1336| 	phar_archive_object *p;
 1337| 	zend_class_entry *c;
 1338| 	zend_string *base;
 1339| 	zval *ret;
 1340| 	php_stream *fp;
 1341| 	int count;
 1342| };
 1343| 
 1344| static int phar_build(zend_object_iterator *iter, void *puser) /* {{{ */
 1345| {
 1346| 	zval *value;
 1347| 	bool close_fp = true;
 1348| 	struct _phar_t *p_obj = (struct _phar_t*) puser;
 1349| 	size_t str_key_len, base_len = ZSTR_LEN(p_obj->base);
 1350| 	phar_entry_data *data;
 1351| 	php_stream *fp;
 1352| 	size_t fname_len;
 1353| 	size_t contents_len;
 1354| 	char *fname, *error = NULL, *base = ZSTR_VAL(p_obj->base), *save = NULL, *temp = NULL;
 1355| 	zend_string *opened;
 1356| 	char *str_key;
 1357| 	zend_class_entry *ce = p_obj->c;
 1358| 	phar_archive_object *phar_obj = p_obj->p;
 1359| 	php_stream_statbuf ssb;
 1360| 	char ch;
 1361| 
 1362| 	value = iter->funcs->get_current_data(iter);
 1363| 
 1364| 	if (EG(exception)) {
 1365| 		return ZEND_HASH_APPLY_STOP;
 1366| 	}
 1367| 
 1368| 	if (!value) {
 1369| 		/* failure in get_current_data */
 1370| 		zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0, "Iterator %s returned no value", ZSTR_VAL(ce->name));
 1371| 		return ZEND_HASH_APPLY_STOP;
 1372| 	}
 1373| 
 1374| 	switch (Z_TYPE_P(value)) {
 1375| 		case IS_STRING:
 1376| 			break;
 1377| 		case IS_RESOURCE:
 1378| 			php_stream_from_zval_no_verify(fp, value);
 1379| 
 1380| 			if (!fp) {
```

### Turn 5  _(tok 11174+295, stop=tool_use)_

**Reasoning:** The call on line 1581 is inside `phar_build`. Confirm that there are no other function definitions between line 1344 and line 1581 — the code I checked was continuous inside phar_build. Yes.

So the callers are:
- phar_build (ext/phar/phar_object.c)
- phar_add_file (ext/phar/phar_object.c)
- phar_mkdir (ext/phar/phar_object.c)
- phar_wrapper_open_url (ext/phar/stream.c)

Checking other files (e.g., tests?). Grep only found these 7 matches across the entire repo. Good. Also checking whether there are any other files like function pointers. Grep already covers the entire repo.

Confidence is high.

- **submit_callers** → `{"callers": [{"function": "phar_build", "file": "ext/phar/phar_object.c"}, {"function": "phar_add_file", "file": "ext/phar/phar_object.c"}, {"function": "phar_mkdir", "file": "ext/phar/phar_object.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 4, "n_truth": 4, "tp": 4, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2777+120, stop=tool_use)_

**Reasoning:** I need to locate all the places where this is being called.


- `get_callers(name=phar_get_or_create_entry_data, limit=100)` →

```
{
  "name": "phar_get_or_create_entry_data",
  "version": "old",
  "callers": [
    {
      "caller": "phar_build",
      "file": "ext/phar/phar_object.c",
      "line": 1581
    },
    {
      "caller": "phar_add_file",
      "file": "ext/phar/phar_object.c",
      "line": 3539
    },
    {
      "caller": "phar_mkdir",
      "file": "ext/phar/phar_object.c",
      "line": 3611
    },
    {
      "caller": "phar_wrapper_open_url",
      "file": "ext/phar/stream.c",
      "line": 194
    }
  ]
}
```

- `grep(pattern=phar_get_or_create_entry_data, version=old, max_results=100)` →

```
7 matches
ext/phar/phar.c:402:		/* if phar_get_or_create_entry_data returns a sub-directory, we have to free it */
ext/phar/phar_internal.h:467:ZEND_ATTRIBUTE_NONNULL phar_entry_data *phar_get_or_create_entry_data(char *fname, size_t fname_len, char *path, size_t path_len, const char *mode, char allow_dir, char **
ext/phar/phar_object.c:1581:	if (!(data = phar_get_or_create_entry_data(phar_obj->archive->fname, phar_obj->archive->fname_len, str_key, str_key_len, "w+b", 0, &error, true))) {
ext/phar/phar_object.c:3539:	if (!(data = phar_get_or_create_entry_data((*pphar)->fname, (*pphar)->fname_len, filename, filename_len, "w+b", 0, &error, true))) {
ext/phar/phar_object.c:3611:	if (!(data = phar_get_or_create_entry_data((*pphar)->fname, (*pphar)->fname_len, ZSTR_VAL(dir_name), ZSTR_LEN(dir_name), "w+b", 2, &error, true))) {
ext/phar/stream.c:194:		if (NULL == (idata = phar_get_or_create_entry_data(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), internal_file, strlen(internal_file), mode, 0, &error, true))) {
ext/phar/util.c:609:ZEND_ATTRIBUTE_NONNULL phar_entry_data *phar_get_or_create_entry_data(char *fname, size_t fname_len, char *path, size_t path_len, const char *mode, char allow_dir, char **error, bo
```

### Turn 2  _(tok 3517+249, stop=tool_use)_

**Reasoning:** The grep confirms 4 call sites. Let me verify enclosing functions at those lines.


- `get_context_at(file=ext/phar/phar_object.c, line=1581, rev=old)` →

```
phar_build — ext/phar/phar_object.c:1344 [function] static int phar_build(zend_object_iterator *iter, void *puser) /*
  reads: iter, puser; writes: -; returns: return ZEND_HASH_APPLY_STOP; | return ZEND_HASH_APPLY_STOP; | return ZEND_HASH_APPLY_STOP; | return ZEND_HASH_APPLY_STOP; | return ZEND_HASH_APPLY_STOP; | return ZEND_HASH_APPLY_STOP;

SLICE around line 1581 (def-use, level 2; '>' marks the seed):
static int phar_build(zend_object_iterator *iter, void *puser) /* {
   zval *value;
   bool close_fp = true;
   struct _phar_t *p_obj =(struct _phar_t*)puser;
   size_t str_key_len, base_len = ZSTR_LEN(p_obj->base);
   phar_entry_data *data;
   php_stream *fp;
   size_t fname_len;
   size_t contents_len;
   char *fname, *error = NULL, *base = ZSTR_VAL(p_obj->base), *save = NULL, *temp = NULL;
   zend_string *opened;
   char *str_key;
   ...
   phar_archive_object *phar_obj = p_obj->p;
   php_stream_statbuf ssb;
   ...
   value = iter->funcs->get_current_data(iter);
   ...
   switch(Z_TYPE_P(value)) {
   ...
     case IS_RESOURCE: php_stream_from_zval_no_verify(fp, value); if(!fp) {
   ...
     if(iter->funcs->get_current_key) {
       zval key;
   ...
       str_key_len = Z_STRLEN(key);
       str_key = estrndup(Z_STRVAL(key), str_key_len);
       save = str_key;
   ...
     } else {
     }
   ...
     close_fp = false;
     opened = ZSTR_INIT_LITERAL("[stream]", 0);
   ...
     }
     case IS_OBJECT: if(instanceof_function(Z_OBJCE_P(value), spl_ce_SplFileInfo)) {
     if(instanceof_function(Z_OBJCE_P(value), spl_ce_SplFileInfo)) {
       spl_filesystem_object *intern = PHAR_FETCH_INTERNAL_EX(value);
   ...
       switch(intern->type) {
         case SPL_FS_DIR: {
           char *tmp;
           zend_string *test_str = spl_filesystem_object_get_path(intern);
           fname_len = spprintf(&tmp, 0, "%s%c%s", ZSTR_VAL(test_str), DEFAULT_SLASH, intern->u.dir.entry.d_name);
   ...
           fname = expand_filepath(tmp, NULL);
   ...
         }
   ...
         case SPL_FS_FILE: fname = expand_filepath(ZSTR_VAL(intern->file_name), NULL); break;
           fname = expand_filepath(ZSTR_VAL(intern->file_name), NULL);
   ...
       }
   ...
       fname_len = strlen(fname);
       save = fname;
   ...
     }
     }
   }
   fname = Z_STRVAL_P(value);
   fname_len = Z_STRLEN_P(value);
   ...
   if(base_len) {
     temp = expand_filepath(base, NULL);
   ...
     base = temp;
     base_len = strlen(base);
     if(fname_len >= base_len && strncmp(fname, base, base_len)== 0 &&((ch = fname[base_len - IS_SLASH(base[base_len - 1])])== '\0' || IS_SLASH(ch))) {
       str_key_len = fname_len - base_len;
   ...
       str_key = fname + base_len;
       if(*str_key == '/' || *str_key == '\\') {
         str_key++;
         str_key_len--;
   ...
       }
     } else {
     }
   } else {
     if(iter->funcs->get_current_key) {
       zval key;
   ...
       str_key_len = Z_STRLEN(key);
       str_key = estrndup(Z_STRVAL(key), str_key_len);
       save = str_key;
   ...
     } else {
     }
   }
   ...
   fp = php_stream_open_wrapper(fname, "rb", STREAM_MUST_SEEK|0, &opened);
   ...
>  if(!(data = phar_get_or_create_entry_data(phar_obj->archive->fname, phar_obj->archive->fname_len, str_key, str_key_len, "w+b", 0, &error, true))) {
     zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Entry %s cannot be created: %s", str_key, error);
     efree(error);
     if(save) {
   ...
     }
     if(opened) {
   ...
     }
     if(temp) {
   ...
     }
     if(close_fp) {
   ...
     }
     return ZEND_HASH_APPLY_STOP;
   } else {
     if(error) {
   ...
     }
     if(data->internal_file->fp_type == PHAR_MOD) {
       php_stream_close(data->internal_file->fp);
     }
     data->internal_file->fp = NULL;
     data->internal_file->fp_type = PHAR_UFP;
     data->internal_file->offset_abs = data->internal_file->offset = php_stream_tell(p_obj->fp);
     data->fp = NULL;
     php_stream_copy_to_stream_ex(fp, p_obj->fp, PHP_STREAM_COPY_ALL, &contents_len);
     if(php_stream_stat(fp, &ssb)!= -1) {
       data->internal_file->flags = ssb.sb.st_mode & PHAR_ENT_PERM_MASK ;
     } else {
       #ifndef ...
   ...
       mask = umask(0);
   ...
       data->internal_file->flags &= ~mask;
       #endif
     }
   }
   ...
   data->internal_file->compressed_filesize = data->internal_file->uncompressed_filesize = contents_len;
   phar_entry_delref(data);
   ...
}

CALLEES (36):
  zend_throw_exception_ex (Zend/zend_exceptions.c:895): reads code, exception_ce, format; writes -; returns return obj;
  expand_filepath (main/fopen_wrappers.c:773): reads filepath, real_path; writes -; returns return expand_filepath_ex(filepath, real_path, NULL, 0);
  zend_string_release_ex (Zend/zend_string.h:344): reads persistent, s; writes -; returns -
  spl_filesystem_object_get_path (ext/spl/spl_directory.c:212): reads intern; writes -; returns return NULL; | return zend_string_init(tmp, len, false); | return NULL; | return zend_string_copy(intern->path);
  zval_ptr_dtor_str (Zend/zend_variables.h:70): reads zval_ptr; writes -; returns -
  zval_ptr_dtor (Zend/zend_variables.c:82): reads zval_ptr; writes -; returns -
  php_check_open_basedir (main/fopen_wrappers.c:285): reads path; writes -; returns return php_check_open_basedir_ex(path, 1);
  phar_get_or_create_entry_data (ext/phar/util.c:609): reads allow_dir, error, fname, fname_len, mode, path, path_len, security; writes error*; returns return NULL; | return NULL; | return ret; | return NULL; | return NULL; | return NULL;
  add_assoc_str (Zend/zend_API.h:572): reads arg, key, str; writes -; returns -
  phar_entry_delref (ext/phar/phar.c:392): reads idata; writes -; returns -
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  EG [macro (1 of 2 definitions)]: # define EG(v) (executor_globals.v)
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  S_ISDIR [macro]: #define S_ISDIR(mode) (((mode)&S_IFMT) == S_IFDIR)
  php_stream_stat_path [macro]: #define php_stream_stat_path(path, ssb) _php_stream_stat_path((path), 0, (ssb), NULL)
  spprintf [macro]: #define spprintf zend_spprintf
  PHAR_FETCH_INTERNAL_EX [macro]: #define PHAR_FETCH_INTERNAL_EX(zv) (void *)((char *) Z_OBJ_P(zv) - Z_OBJ_P(zv)->handlers->offset);
  Z_OBJCE_P [macro]: #define Z_OBJCE_P(zval_p) Z_OBJCE(*(zval_p))
  ZSTR_INIT_LITERAL [macro]: #define ZSTR_INIT_LITERAL(s, persistent) (zend_string_init(("" s), sizeof(s) - 1, (persistent)))
  estrndup [macro]: #define estrndup(s, length) _estrndup((s), (length) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  Z_STRVAL [macro]: #define Z_STRVAL(zval) ZSTR_VAL(Z_STR(zval))
  Z_STRLEN [macro]: #define Z_STRLEN(zval) ZSTR_LEN(Z_STR(zval))
  Z_TYPE [macro]: #define Z_TYPE(zval) zval_get_type(&(zval))
  php_stream_from_zval_no_verify [macro]: #define php_stream_from_zval_no_verify(xstr, pzval) (xstr) = (php_stream*)zend_fetch_resource2_ex((pzval), "stream", php_file_le_stream(), php_file_le_pstream())
  Z_TYPE_P [macro]: #define Z_TYPE_P(zval_p) Z_TYPE(*(zval_p))
  Z_STRVAL_P [macro]: #define Z_STRVAL_P(zval_p) Z_STRVAL(*(zval_p))
  Z_STRLEN_P [macro]: #define Z_STRLEN_P(zval_p) Z_STRLEN(*(zval_p))
  IS_SLASH [macro (1 of 2 definitions)]: #define IS_SLASH(c) ((c) == '/')
  php_stream_open_wrapper [macro]: #define php_stream_open_wrapper(path, mode, options, opened) _php_stream_open_wrapper_ex((path), (mode), (options), (opened), NULL STREAMS_CC)
  not defined in this repository: instanceof_function, umask
  not shown (4): php_stream_close, php_stream_stat, php_stream_copy_to_stream_ex, php_stream_tell

CALLERS (2):
  PHP_METHOD(Phar, buildFromDirectory) (ext/phar/phar_object.c:1729): if (SUCCESS == spl_iterator_apply((apply_reg ? &regexiter : &iteriter), (spl_iterator_apply_func_t) phar_build, (void *) &pass)) {
  PHP_METHOD(Phar, buildFromIterator) (ext/phar/phar_object.c:1800): if (SUCCESS == spl_iterator_apply(obj, (spl_iterator_apply_func_t) phar_build, (void *) &pass)) {

TYPES (1):
  _phar_t — ext/phar/phar_object.c:1335
    struct _phar_t {
    	phar_archive_object *p;
    	zend_class_entry *c;
    	zend_string *base;
    	zval *ret;
    	php_stream *fp;
    	int count;
    }
```

- `get_context_at(file=ext/phar/phar_object.c, line=3539, rev=old)` →

```
phar_add_file — ext/phar/phar_object.c:3504 [function] static void phar_add_file(phar_archive_data **pphar, zend_string *file_name, const zend_string *content, zval *zresource)
  reads: content, file_name, pphar, zresource; writes: pphar*; returns: -

SLICE around line 3539 (def-use, level 2; '>' marks the seed):
static void phar_add_file(phar_archive_data **pphar, zend_string *file_name, const zend_string *content, zval *zresource) {
   char *error;
   phar_entry_data *data;
   php_stream *contents_file = NULL;
   php_stream_statbuf ssb;
   #ifdef ...
   char *save_filename;
   #endif
   ...
   char *filename = ZSTR_VAL(file_name);
   size_t filename_len = ZSTR_LEN(file_name);
   #ifdef ...
   save_filename = filename;
   if(memchr(filename, '\\', filename_len)) {
     filename = do_alloca(filename_len + 1, filename_use_heap);
     memcpy(filename, save_filename, filename_len);
     filename[filename_len] = '\0';
   }
   #endif
>  if(!(data = phar_get_or_create_entry_data((*pphar)->fname, (*pphar)->fname_len, filename, filename_len, "w+b", 0, &error, true))) {
     if(error) {
   ...
     } else {
     }
   ...
     goto finish;
   } else {
     if(error) {
   ...
     }
     if(!data->internal_file->is_dir) {
       size_t contents_len = 0;
       if(content) {
         contents_len = ZSTR_LEN(content);
         size_t written_len = php_stream_write(data->fp, ZSTR_VAL(content), ZSTR_LEN(content));
         if(written_len != contents_len) {
   ...
         }
       } else {
   ...
         php_stream_copy_to_stream_ex(contents_file, data->fp, PHP_STREAM_COPY_ALL, &contents_len);
       }
       data->internal_file->compressed_filesize = data->internal_file->uncompressed_filesize = contents_len;
     }
     if(contents_file != NULL && php_stream_stat(contents_file, &ssb)!= -1) {
       data->internal_file->flags = ssb.sb.st_mode & PHAR_ENT_PERM_MASK ;
     } else {
       #ifndef ...
       mode_t mask;
       mask = umask(0);
   ...
       data->internal_file->flags &= ~mask;
       #endif
     }
     if(pphar[0] != data->phar) {
       *pphar = data->phar;
     }
     phar_entry_delref(data);
     phar_flush(*pphar, &error);
     if(error) {
   ...
     }
   }
}

CALLEES (16):
  zend_throw_exception_ex (Zend/zend_exceptions.c:895): reads code, exception_ce, format; writes -; returns return obj;
  phar_flush (ext/phar/phar.c:2456): reads error, phar; writes -; returns return phar_flush_ex(phar, NULL, false, error);
  phar_entry_delref (ext/phar/phar.c:392): reads idata; writes -; returns -
  phar_get_or_create_entry_data (ext/phar/util.c:609): reads allow_dir, error, fname, fname_len, mode, path, path_len, security; writes error*; returns return NULL; | return NULL; | return ret; | return NULL; | return NULL; | return NULL;
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  zend_string_starts_with_literal [macro]: #define zend_string_starts_with_literal(str, prefix) \
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  do_alloca [macro (1 of 2 definitions)]: # define do_alloca(p, use_heap) emalloc(p)
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  php_stream_stat [macro]: #define php_stream_stat(stream, ssb) _php_stream_stat((stream), (ssb))
  php_stream_copy_to_stream_ex [macro]: #define php_stream_copy_to_stream_ex(src, dest, maxlen, len) _php_stream_copy_to_stream_ex((src), (dest), (maxlen), (len) STREAMS_CC)
  php_stream_from_zval_no_verify [macro]: #define php_stream_from_zval_no_verify(xstr, pzval) (xstr) = (php_stream*)zend_fetch_resource2_ex((pzval), "stream", php_file_le_stream(), php_file_le_pstream())
  php_stream_write [macro]: #define php_stream_write_string(stream, str) _php_stream_write(stream, str, strlen(str))
  free_alloca [macro (1 of 2 definitions)]: # define free_alloca(p, use_heap) efree(p)
  not defined in this repository: memchr, umask

CALLERS (3):
  PHP_METHOD(Phar, offsetSet) (ext/phar/phar_object.c:3674): phar_add_file(&(phar_obj->archive), file_name, file_content, zresource);
  PHP_METHOD(Phar, addFile) (ext/phar/phar_object.c:3774): phar_add_file(&(phar_obj->archive), file_name, NULL, &zresource);
  PHP_METHOD(Phar, addFromString) (ext/phar/phar_object.c:3791): phar_add_file(&(phar_obj->archive), local_name, file_content, NULL);
```

- `get_context_at(file=ext/phar/phar_object.c, line=3611, rev=old)` →

```
phar_mkdir — ext/phar/phar_object.c:3606 [function] static void phar_mkdir(phar_archive_data **pphar, zend_string *dir_name)
  reads: dir_name, pphar; writes: pphar*; returns: -

SLICE around line 3611 (def-use, level 2; '>' marks the seed):
static void phar_mkdir(phar_archive_data **pphar, zend_string *dir_name) {
   char *error;
   phar_entry_data *data;
>  if(!(data = phar_get_or_create_entry_data((*pphar)->fname, (*pphar)->fname_len, ZSTR_VAL(dir_name), ZSTR_LEN(dir_name), "w+b", 2, &error, true))) {
     if(error) {
   ...
     } else {
     }
   ...
     return;
   } else {
     if(error) {
   ...
     }
     if(data->phar != *pphar) {
       *pphar = data->phar;
     }
     phar_entry_delref(data);
     phar_flush(*pphar, &error);
     if(error) {
   ...
     }
   }
}

CALLEES (7):
  zend_throw_exception_ex (Zend/zend_exceptions.c:895): reads code, exception_ce, format; writes -; returns return obj;
  phar_flush (ext/phar/phar.c:2456): reads error, phar; writes -; returns return phar_flush_ex(phar, NULL, false, error);
  phar_entry_delref (ext/phar/phar.c:392): reads idata; writes -; returns -
  phar_get_or_create_entry_data (ext/phar/util.c:609): reads allow_dir, error, fname, fname_len, mode, path, path_len, security; writes error*; returns return NULL; | return NULL; | return ret; | return NULL; | return NULL; | return NULL;
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len

CALLERS (1):
  PHP_METHOD(Phar, addEmptyDir) (ext/phar/phar_object.c:3741): phar_mkdir(&phar_obj->archive, dir_name);
```

- `get_context_at(file=ext/phar/stream.c, line=194, rev=old)` →

```
phar_wrapper_open_url — ext/phar/stream.c:161 [function] static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /*
  reads: mode, opened_path, options, path, wrapper; writes: opened_path*; returns: return NULL; | return NULL; | return NULL; | return NULL; | return fpf; | return NULL;

SLICE around line 194 (def-use, level 2; '>' marks the seed):
static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /* {
   phar_archive_data *phar;
   phar_entry_data *idata;
   char *internal_file;
   char *error;
   ...
   php_url *resource = NULL;
   ...
   if((resource = phar_parse_url(wrapper, path, mode, options))== NULL) {
   ...
   }
   ...
   internal_file = estrndup(ZSTR_VAL(resource->path)+ 1, ZSTR_LEN(resource->path)- 1);
   if(mode[0] == 'w' ||(mode[0] == 'r' && mode[1] == '+')) {
>    if(NULL ==(idata = phar_get_or_create_entry_data(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), internal_file, strlen(internal_file), mode, 0, &error, true))) {
       if(error) {
   ...
       } else {
       }
   ...
       efree(internal_file);
       php_url_free(resource);
       return NULL;
     }
   ...
     fpf = php_stream_alloc(&phar_ops, idata, NULL, mode);
   ...
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
       *opened_path = zend_strpprintf_unchecked(MAXPATHLEN, "phar://%s/%S", idata->phar->fname, idata->internal_file->filename);
     }
     return fpf;
   } else {
     if(!*internal_file &&(options & STREAM_OPEN_FOR_INCLUDE)) {
   ...
       if(phar->is_tar || phar->is_zip) {
         if((FAILURE == phar_get_entry_data(&idata, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), ".phar/stub.php", sizeof(".phar/stub.php")-1, "r", 0, &error, false))|| !idata) {
   ...
         }
       } else {
         php_stream *stream = phar_get_pharfp(phar);
         if(stream == NULL) {
   ...
           stream = phar_get_pharfp(phar);
         }
   ...
         entry =(phar_entry_info *)ecalloc(1, sizeof(phar_entry_info));
   ...
         entry->is_crc_checked = 1;
         idata =(phar_entry_data *)ecalloc(1, sizeof(phar_entry_data));
         idata->fp = stream;
         idata->phar = phar;
         idata->internal_file = entry;
   ...
       }
     }
     if((FAILURE == phar_get_entry_data(&idata, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), internal_file, strlen(internal_file), "r", 0, &error, false))|| !idata) {
   ...
     }
   }
   ...
   #ifdef ...
   fprintf(stderr, "Pharname: %s\n", idata->phar->fname);
   ...
   fprintf(stderr, "Entry: %s\n", ZSTR_VAL(idata->internal_file->filename));
   fprintf(stderr, "Size: %u\n", idata->internal_file->uncompressed_filesize);
   fprintf(stderr, "Compressed: %u\n", idata->internal_file->flags);
   #endif
   if(!idata->internal_file->is_crc_checked && phar_postprocess_file(idata, idata->internal_file->crc32, &error, 2)!= SUCCESS) {
   ...
     phar_entry_delref(idata);
   ...
   }
   if(!PHAR_G(cwd_init)&&(options & STREAM_OPEN_FOR_INCLUDE)) {
     char *entry = ZSTR_VAL(idata->internal_file->filename), *cwd;
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
     *opened_path = zend_strpprintf_unchecked(MAXPATHLEN, "phar://%s/%S", idata->phar->fname, idata->internal_file->filename);
   }
   ...
   fpf = php_stream_alloc(&phar_ops, idata, NULL, mode);
   return fpf;
}

CALLEES (32):
  phar_parse_url (ext/phar/stream.c:60): reads filename, mode, options, wrapper; writes -; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  php_stream_wrapper_log_error (main/streams/streams.c:243): reads fmt, options, wrapper; writes -; returns -
  php_url_free (ext/standard/url.c:30): reads theurl; writes -; returns -
  phar_request_initialize (ext/phar/phar.c:3337): reads -; writes -; returns -
  phar_get_entry_data (ext/phar/util.c:466): reads allow_dir, error, fname, fname_len, mode, path, path_len, ret, security; writes error*, ret*; returns return FAILURE; | return FAILURE; | return FAILURE; | return SUCCESS; | return FAILURE; | return SUCCESS;
  phar_get_pharfp (ext/phar/phar_internal.h:308): reads phar; writes -; returns return phar->fp; | return PHAR_G(cached_fp)[phar->phar_pos].fp;
  phar_open_archive_fp (ext/phar/util.c:712): reads phar; writes -; returns return SUCCESS; | return FAILURE; | return FAILURE; | return SUCCESS;
  phar_get_archive (ext/phar/util.c:957): reads alias, alias_len, archive, error, fname, fname_len; writes archive*, error*; returns return FAILURE; | return SUCCESS; | return FAILURE; | return SUCCESS; | return FAILURE; | return SUCCESS;
  zend_strpprintf_unchecked (Zend/zend.c:366): reads format, max_len; writes -; returns return str;
  phar_metadata_tracker_free (ext/phar/phar.c:632): reads persistent, tracker; writes tracker*; returns -
  zend_hash_str_find_ind (Zend/zend_hash.h:458): reads ht, len, str; writes -; returns return(zv && Z_TYPE_P(zv)== IS_INDIRECT)?((Z_TYPE_P(Z_INDIRECT_P(zv))!= IS_UNDEF)? Z_INDIRECT_P(zv): NULL): zv;
  phar_get_or_create_entry_data (ext/phar/util.c:609): reads allow_dir, error, fname, fname_len, mode, path, path_len, security; writes error*; returns return NULL; | return NULL; | return ret; | return NULL; | return NULL; | return NULL;
  phar_entry_delref (ext/phar/phar.c:392): reads idata; writes -; returns -
  phar_postprocess_file (ext/phar/phar.c:2302): reads crc32, error, idata, process_zip; writes error*, idata*; returns return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return SUCCESS; | return SUCCESS;
  zend_string_equals_literal_ci [macro]: #define zend_string_equals_literal_ci(str, c) \
  estrndup [macro]: #define estrndup(s, length) _estrndup((s), (length) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  strpprintf [macro]: #define strpprintf zend_strpprintf
  ecalloc [macro]: #define ecalloc(nmemb, size) _ecalloc((nmemb), (size) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZSTR_EMPTY_ALLOC [macro]: #define ZSTR_EMPTY_ALLOC() zend_empty_string
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

### Turn 3  _(tok 10934+282, stop=tool_use)_

**Reasoning:** All four call sites confirmed with their enclosing functions. Also check phar.c line 402 — that's a comment inside phar_entry_delref presumably. Confirmed as comment (not a call).

Let me double check there are no other files (e.g. tests, other dirs) — grep across the whole repo returned 7 matches, including definition, prototype, comment, and 4 call sites. Also check if any indirect usage via function pointer — unlikely.

Submit.


**Says:** 

All four call sites are verified against the grep results (7 total matches: 1 definition in `util.c`, 1 prototype in `phar_internal.h`, 1 comment in `phar.c:402`, and 4 real calls).



- **submit_callers** → `{"callers": [{"function": "phar_build", "file": "ext/phar/phar_object.c"}, {"function": "phar_add_file", "file": "ext/phar/phar_object.c"}, {"function": "phar_mkdir", "file": "ext/phar/phar_object.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 4, "n_truth": 4, "tp": 4, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2354+86, stop=tool_use)_

**Reasoning:** Looking for the callers.


- `get_callers(name=phar_get_or_create_entry_data, limit=100)` →

```
{
  "name": "phar_get_or_create_entry_data",
  "version": "old",
  "callers": [
    {
      "caller": "phar_build",
      "file": "ext/phar/phar_object.c",
      "line": 1581
    },
    {
      "caller": "phar_add_file",
      "file": "ext/phar/phar_object.c",
      "line": 3539
    },
    {
      "caller": "phar_mkdir",
      "file": "ext/phar/phar_object.c",
      "line": 3611
    },
    {
      "caller": "phar_wrapper_open_url",
      "file": "ext/phar/stream.c",
      "line": 194
    }
  ]
}
```

- `resolve_symbol(name=phar_get_or_create_entry_data)` →

```
{
  "resolved": true,
  "name": "phar_get_or_create_entry_data",
  "version": "old",
  "file": "ext/phar/util.c",
  "line": 609,
  "kind": "function",
  "signature": "ZEND_ATTRIBUTE_NONNULL phar_entry_data *phar_get_or_create_entry_data(char *fname, size_t fname_len, char *path, size_t path_len, const char *mode, char allow_dir, char **error, bool security) /*",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 2  _(tok 2805+256, stop=tool_use)_

**Reasoning:** Let me verify each caller by checking the call sites in the sources. Also check whether there are additional call sites not captured (e.g., in ext/phar/dirstream.c, phar_object.c other places). Let me check get_context_at for each line, and also maybe check other candidates. Let me look at callers via expand_function as well.


- `get_context_at(file=ext/phar/phar_object.c, line=1581)` →

```
phar_build — ext/phar/phar_object.c:1344 [function] static int phar_build(zend_object_iterator *iter, void *puser) /*
  reads: iter, puser; writes: -; returns: return ZEND_HASH_APPLY_STOP; | return ZEND_HASH_APPLY_STOP; | return ZEND_HASH_APPLY_STOP; | return ZEND_HASH_APPLY_STOP; | return ZEND_HASH_APPLY_STOP; | return ZEND_HASH_APPLY_STOP;

SLICE around line 1581 (def-use, level 2; '>' marks the seed):
static int phar_build(zend_object_iterator *iter, void *puser) /* {
   zval *value;
   bool close_fp = true;
   struct _phar_t *p_obj =(struct _phar_t*)puser;
   size_t str_key_len, base_len = ZSTR_LEN(p_obj->base);
   phar_entry_data *data;
   php_stream *fp;
   size_t fname_len;
   size_t contents_len;
   char *fname, *error = NULL, *base = ZSTR_VAL(p_obj->base), *save = NULL, *temp = NULL;
   zend_string *opened;
   char *str_key;
   ...
   phar_archive_object *phar_obj = p_obj->p;
   php_stream_statbuf ssb;
   ...
   value = iter->funcs->get_current_data(iter);
   ...
   switch(Z_TYPE_P(value)) {
   ...
     case IS_RESOURCE: php_stream_from_zval_no_verify(fp, value); if(!fp) {
   ...
     if(iter->funcs->get_current_key) {
       zval key;
   ...
       str_key_len = Z_STRLEN(key);
       str_key = estrndup(Z_STRVAL(key), str_key_len);
       save = str_key;
   ...
     } else {
     }
   ...
     close_fp = false;
     opened = ZSTR_INIT_LITERAL("[stream]", 0);
   ...
     }
     case IS_OBJECT: if(instanceof_function(Z_OBJCE_P(value), spl_ce_SplFileInfo)) {
     if(instanceof_function(Z_OBJCE_P(value), spl_ce_SplFileInfo)) {
       spl_filesystem_object *intern = PHAR_FETCH_INTERNAL_EX(value);
   ...
       switch(intern->type) {
         case SPL_FS_DIR: {
           char *tmp;
           zend_string *test_str = spl_filesystem_object_get_path(intern);
           fname_len = spprintf(&tmp, 0, "%s%c%s", ZSTR_VAL(test_str), DEFAULT_SLASH, intern->u.dir.entry.d_name);
   ...
           fname = expand_filepath(tmp, NULL);
   ...
         }
   ...
         case SPL_FS_FILE: fname = expand_filepath(ZSTR_VAL(intern->file_name), NULL); break;
           fname = expand_filepath(ZSTR_VAL(intern->file_name), NULL);
   ...
       }
   ...
       fname_len = strlen(fname);
       save = fname;
   ...
     }
     }
   }
   fname = Z_STRVAL_P(value);
   fname_len = Z_STRLEN_P(value);
   ...
   if(base_len) {
     temp = expand_filepath(base, NULL);
   ...
     base = temp;
     base_len = strlen(base);
     if(fname_len >= base_len && strncmp(fname, base, base_len)== 0 &&((ch = fname[base_len - IS_SLASH(base[base_len - 1])])== '\0' || IS_SLASH(ch))) {
       str_key_len = fname_len - base_len;
   ...
       str_key = fname + base_len;
       if(*str_key == '/' || *str_key == '\\') {
         str_key++;
         str_key_len--;
   ...
       }
     } else {
     }
   } else {
     if(iter->funcs->get_current_key) {
       zval key;
   ...
       str_key_len = Z_STRLEN(key);
       str_key = estrndup(Z_STRVAL(key), str_key_len);
       save = str_key;
   ...
     } else {
     }
   }
   ...
   fp = php_stream_open_wrapper(fname, "rb", STREAM_MUST_SEEK|0, &opened);
   ...
>  if(!(data = phar_get_or_create_entry_data(phar_obj->archive->fname, phar_obj->archive->fname_len, str_key, str_key_len, "w+b", 0, &error, true))) {
     zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Entry %s cannot be created: %s", str_key, error);
     efree(error);
     if(save) {
   ...
     }
     if(opened) {
   ...
     }
     if(temp) {
   ...
     }
     if(close_fp) {
   ...
     }
     return ZEND_HASH_APPLY_STOP;
   } else {
     if(error) {
   ...
     }
     if(data->internal_file->fp_type == PHAR_MOD) {
       php_stream_close(data->internal_file->fp);
     }
     data->internal_file->fp = NULL;
     data->internal_file->fp_type = PHAR_UFP;
     data->internal_file->offset_abs = data->internal_file->offset = php_stream_tell(p_obj->fp);
     data->fp = NULL;
     php_stream_copy_to_stream_ex(fp, p_obj->fp, PHP_STREAM_COPY_ALL, &contents_len);
     if(php_stream_stat(fp, &ssb)!= -1) {
       data->internal_file->flags = ssb.sb.st_mode & PHAR_ENT_PERM_MASK ;
     } else {
       #ifndef ...
   ...
       mask = umask(0);
   ...
       data->internal_file->flags &= ~mask;
       #endif
     }
   }
   ...
   data->internal_file->compressed_filesize = data->internal_file->uncompressed_filesize = contents_len;
   phar_entry_delref(data);
   ...
}

CALLEES (36):
  zend_throw_exception_ex (Zend/zend_exceptions.c:895): reads code, exception_ce, format; writes -; returns return obj;
  expand_filepath (main/fopen_wrappers.c:773): reads filepath, real_path; writes -; returns return expand_filepath_ex(filepath, real_path, NULL, 0);
  zend_string_release_ex (Zend/zend_string.h:344): reads persistent, s; writes -; returns -
  spl_filesystem_object_get_path (ext/spl/spl_directory.c:212): reads intern; writes -; returns return NULL; | return zend_string_init(tmp, len, false); | return NULL; | return zend_string_copy(intern->path);
  zval_ptr_dtor_str (Zend/zend_variables.h:70): reads zval_ptr; writes -; returns -
  zval_ptr_dtor (Zend/zend_variables.c:82): reads zval_ptr; writes -; returns -
  php_check_open_basedir (main/fopen_wrappers.c:285): reads path; writes -; returns return php_check_open_basedir_ex(path, 1);
  phar_get_or_create_entry_data (ext/phar/util.c:609): reads allow_dir, error, fname, fname_len, mode, path, path_len, security; writes error*; returns return NULL; | return NULL; | return ret; | return NULL; | return NULL; | return NULL;
  add_assoc_str (Zend/zend_API.h:572): reads arg, key, str; writes -; returns -
  phar_entry_delref (ext/phar/phar.c:392): reads idata; writes -; returns -
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  EG [macro (1 of 2 definitions)]: # define EG(v) (executor_globals.v)
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  S_ISDIR [macro]: #define S_ISDIR(mode) (((mode)&S_IFMT) == S_IFDIR)
  php_stream_stat_path [macro]: #define php_stream_stat_path(path, ssb) _php_stream_stat_path((path), 0, (ssb), NULL)
  spprintf [macro]: #define spprintf zend_spprintf
  PHAR_FETCH_INTERNAL_EX [macro]: #define PHAR_FETCH_INTERNAL_EX(zv) (void *)((char *) Z_OBJ_P(zv) - Z_OBJ_P(zv)->handlers->offset);
  Z_OBJCE_P [macro]: #define Z_OBJCE_P(zval_p) Z_OBJCE(*(zval_p))
  ZSTR_INIT_LITERAL [macro]: #define ZSTR_INIT_LITERAL(s, persistent) (zend_string_init(("" s), sizeof(s) - 1, (persistent)))
  estrndup [macro]: #define estrndup(s, length) _estrndup((s), (length) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  Z_STRVAL [macro]: #define Z_STRVAL(zval) ZSTR_VAL(Z_STR(zval))
  Z_STRLEN [macro]: #define Z_STRLEN(zval) ZSTR_LEN(Z_STR(zval))
  Z_TYPE [macro]: #define Z_TYPE(zval) zval_get_type(&(zval))
  php_stream_from_zval_no_verify [macro]: #define php_stream_from_zval_no_verify(xstr, pzval) (xstr) = (php_stream*)zend_fetch_resource2_ex((pzval), "stream", php_file_le_stream(), php_file_le_pstream())
  Z_TYPE_P [macro]: #define Z_TYPE_P(zval_p) Z_TYPE(*(zval_p))
  Z_STRVAL_P [macro]: #define Z_STRVAL_P(zval_p) Z_STRVAL(*(zval_p))
  Z_STRLEN_P [macro]: #define Z_STRLEN_P(zval_p) Z_STRLEN(*(zval_p))
  IS_SLASH [macro (1 of 2 definitions)]: #define IS_SLASH(c) ((c) == '/')
  php_stream_open_wrapper [macro]: #define php_stream_open_wrapper(path, mode, options, opened) _php_stream_open_wrapper_ex((path), (mode), (options), (opened), NULL STREAMS_CC)
  not defined in this repository: instanceof_function, umask
  not shown (4): php_stream_close, php_stream_stat, php_stream_copy_to_stream_ex, php_stream_tell

CALLERS (2):
  PHP_METHOD(Phar, buildFromDirectory) (ext/phar/phar_object.c:1729): if (SUCCESS == spl_iterator_apply((apply_reg ? &regexiter : &iteriter), (spl_iterator_apply_func_t) phar_build, (void *) &pass)) {
  PHP_METHOD(Phar, buildFromIterator) (ext/phar/phar_object.c:1800): if (SUCCESS == spl_iterator_apply(obj, (spl_iterator_apply_func_t) phar_build, (void *) &pass)) {

TYPES (1):
  _phar_t — ext/phar/phar_object.c:1335
    struct _phar_t {
    	phar_archive_object *p;
    	zend_class_entry *c;
    	zend_string *base;
    	zval *ret;
    	php_stream *fp;
    	int count;
    }
```

- `get_context_at(file=ext/phar/phar_object.c, line=3539)` →

```
phar_add_file — ext/phar/phar_object.c:3504 [function] static void phar_add_file(phar_archive_data **pphar, zend_string *file_name, const zend_string *content, zval *zresource)
  reads: content, file_name, pphar, zresource; writes: pphar*; returns: -

SLICE around line 3539 (def-use, level 2; '>' marks the seed):
static void phar_add_file(phar_archive_data **pphar, zend_string *file_name, const zend_string *content, zval *zresource) {
   char *error;
   phar_entry_data *data;
   php_stream *contents_file = NULL;
   php_stream_statbuf ssb;
   #ifdef ...
   char *save_filename;
   #endif
   ...
   char *filename = ZSTR_VAL(file_name);
   size_t filename_len = ZSTR_LEN(file_name);
   #ifdef ...
   save_filename = filename;
   if(memchr(filename, '\\', filename_len)) {
     filename = do_alloca(filename_len + 1, filename_use_heap);
     memcpy(filename, save_filename, filename_len);
     filename[filename_len] = '\0';
   }
   #endif
>  if(!(data = phar_get_or_create_entry_data((*pphar)->fname, (*pphar)->fname_len, filename, filename_len, "w+b", 0, &error, true))) {
     if(error) {
   ...
     } else {
     }
   ...
     goto finish;
   } else {
     if(error) {
   ...
     }
     if(!data->internal_file->is_dir) {
       size_t contents_len = 0;
       if(content) {
         contents_len = ZSTR_LEN(content);
         size_t written_len = php_stream_write(data->fp, ZSTR_VAL(content), ZSTR_LEN(content));
         if(written_len != contents_len) {
   ...
         }
       } else {
   ...
         php_stream_copy_to_stream_ex(contents_file, data->fp, PHP_STREAM_COPY_ALL, &contents_len);
       }
       data->internal_file->compressed_filesize = data->internal_file->uncompressed_filesize = contents_len;
     }
     if(contents_file != NULL && php_stream_stat(contents_file, &ssb)!= -1) {
       data->internal_file->flags = ssb.sb.st_mode & PHAR_ENT_PERM_MASK ;
     } else {
       #ifndef ...
       mode_t mask;
       mask = umask(0);
   ...
       data->internal_file->flags &= ~mask;
       #endif
     }
     if(pphar[0] != data->phar) {
       *pphar = data->phar;
     }
     phar_entry_delref(data);
     phar_flush(*pphar, &error);
     if(error) {
   ...
     }
   }
}

CALLEES (16):
  zend_throw_exception_ex (Zend/zend_exceptions.c:895): reads code, exception_ce, format; writes -; returns return obj;
  phar_flush (ext/phar/phar.c:2456): reads error, phar; writes -; returns return phar_flush_ex(phar, NULL, false, error);
  phar_entry_delref (ext/phar/phar.c:392): reads idata; writes -; returns -
  phar_get_or_create_entry_data (ext/phar/util.c:609): reads allow_dir, error, fname, fname_len, mode, path, path_len, security; writes error*; returns return NULL; | return NULL; | return ret; | return NULL; | return NULL; | return NULL;
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  zend_string_starts_with_literal [macro]: #define zend_string_starts_with_literal(str, prefix) \
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  do_alloca [macro (1 of 2 definitions)]: # define do_alloca(p, use_heap) emalloc(p)
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  php_stream_stat [macro]: #define php_stream_stat(stream, ssb) _php_stream_stat((stream), (ssb))
  php_stream_copy_to_stream_ex [macro]: #define php_stream_copy_to_stream_ex(src, dest, maxlen, len) _php_stream_copy_to_stream_ex((src), (dest), (maxlen), (len) STREAMS_CC)
  php_stream_from_zval_no_verify [macro]: #define php_stream_from_zval_no_verify(xstr, pzval) (xstr) = (php_stream*)zend_fetch_resource2_ex((pzval), "stream", php_file_le_stream(), php_file_le_pstream())
  php_stream_write [macro]: #define php_stream_write_string(stream, str) _php_stream_write(stream, str, strlen(str))
  free_alloca [macro (1 of 2 definitions)]: # define free_alloca(p, use_heap) efree(p)
  not defined in this repository: memchr, umask

CALLERS (3):
  PHP_METHOD(Phar, offsetSet) (ext/phar/phar_object.c:3674): phar_add_file(&(phar_obj->archive), file_name, file_content, zresource);
  PHP_METHOD(Phar, addFile) (ext/phar/phar_object.c:3774): phar_add_file(&(phar_obj->archive), file_name, NULL, &zresource);
  PHP_METHOD(Phar, addFromString) (ext/phar/phar_object.c:3791): phar_add_file(&(phar_obj->archive), local_name, file_content, NULL);
```

- `get_context_at(file=ext/phar/phar_object.c, line=3611)` →

```
phar_mkdir — ext/phar/phar_object.c:3606 [function] static void phar_mkdir(phar_archive_data **pphar, zend_string *dir_name)
  reads: dir_name, pphar; writes: pphar*; returns: -

SLICE around line 3611 (def-use, level 2; '>' marks the seed):
static void phar_mkdir(phar_archive_data **pphar, zend_string *dir_name) {
   char *error;
   phar_entry_data *data;
>  if(!(data = phar_get_or_create_entry_data((*pphar)->fname, (*pphar)->fname_len, ZSTR_VAL(dir_name), ZSTR_LEN(dir_name), "w+b", 2, &error, true))) {
     if(error) {
   ...
     } else {
     }
   ...
     return;
   } else {
     if(error) {
   ...
     }
     if(data->phar != *pphar) {
       *pphar = data->phar;
     }
     phar_entry_delref(data);
     phar_flush(*pphar, &error);
     if(error) {
   ...
     }
   }
}

CALLEES (7):
  zend_throw_exception_ex (Zend/zend_exceptions.c:895): reads code, exception_ce, format; writes -; returns return obj;
  phar_flush (ext/phar/phar.c:2456): reads error, phar; writes -; returns return phar_flush_ex(phar, NULL, false, error);
  phar_entry_delref (ext/phar/phar.c:392): reads idata; writes -; returns -
  phar_get_or_create_entry_data (ext/phar/util.c:609): reads allow_dir, error, fname, fname_len, mode, path, path_len, security; writes error*; returns return NULL; | return NULL; | return ret; | return NULL; | return NULL; | return NULL;
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len

CALLERS (1):
  PHP_METHOD(Phar, addEmptyDir) (ext/phar/phar_object.c:3741): phar_mkdir(&phar_obj->archive, dir_name);
```

- `get_context_at(file=ext/phar/stream.c, line=194)` →

```
phar_wrapper_open_url — ext/phar/stream.c:161 [function] static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /*
  reads: mode, opened_path, options, path, wrapper; writes: opened_path*; returns: return NULL; | return NULL; | return NULL; | return NULL; | return fpf; | return NULL;

SLICE around line 194 (def-use, level 2; '>' marks the seed):
static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_DC) /* {
   phar_archive_data *phar;
   phar_entry_data *idata;
   char *internal_file;
   char *error;
   ...
   php_url *resource = NULL;
   ...
   if((resource = phar_parse_url(wrapper, path, mode, options))== NULL) {
   ...
   }
   ...
   internal_file = estrndup(ZSTR_VAL(resource->path)+ 1, ZSTR_LEN(resource->path)- 1);
   if(mode[0] == 'w' ||(mode[0] == 'r' && mode[1] == '+')) {
>    if(NULL ==(idata = phar_get_or_create_entry_data(ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), internal_file, strlen(internal_file), mode, 0, &error, true))) {
       if(error) {
   ...
       } else {
       }
   ...
       efree(internal_file);
       php_url_free(resource);
       return NULL;
     }
   ...
     fpf = php_stream_alloc(&phar_ops, idata, NULL, mode);
   ...
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
       *opened_path = zend_strpprintf_unchecked(MAXPATHLEN, "phar://%s/%S", idata->phar->fname, idata->internal_file->filename);
     }
     return fpf;
   } else {
     if(!*internal_file &&(options & STREAM_OPEN_FOR_INCLUDE)) {
   ...
       if(phar->is_tar || phar->is_zip) {
         if((FAILURE == phar_get_entry_data(&idata, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), ".phar/stub.php", sizeof(".phar/stub.php")-1, "r", 0, &error, false))|| !idata) {
   ...
         }
       } else {
         php_stream *stream = phar_get_pharfp(phar);
         if(stream == NULL) {
   ...
           stream = phar_get_pharfp(phar);
         }
   ...
         entry =(phar_entry_info *)ecalloc(1, sizeof(phar_entry_info));
   ...
         entry->is_crc_checked = 1;
         idata =(phar_entry_data *)ecalloc(1, sizeof(phar_entry_data));
         idata->fp = stream;
         idata->phar = phar;
         idata->internal_file = entry;
   ...
       }
     }
     if((FAILURE == phar_get_entry_data(&idata, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), internal_file, strlen(internal_file), "r", 0, &error, false))|| !idata) {
   ...
     }
   }
   ...
   #ifdef ...
   fprintf(stderr, "Pharname: %s\n", idata->phar->fname);
   ...
   fprintf(stderr, "Entry: %s\n", ZSTR_VAL(idata->internal_file->filename));
   fprintf(stderr, "Size: %u\n", idata->internal_file->uncompressed_filesize);
   fprintf(stderr, "Compressed: %u\n", idata->internal_file->flags);
   #endif
   if(!idata->internal_file->is_crc_checked && phar_postprocess_file(idata, idata->internal_file->crc32, &error, 2)!= SUCCESS) {
   ...
     phar_entry_delref(idata);
   ...
   }
   if(!PHAR_G(cwd_init)&&(options & STREAM_OPEN_FOR_INCLUDE)) {
     char *entry = ZSTR_VAL(idata->internal_file->filename), *cwd;
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
     *opened_path = zend_strpprintf_unchecked(MAXPATHLEN, "phar://%s/%S", idata->phar->fname, idata->internal_file->filename);
   }
   ...
   fpf = php_stream_alloc(&phar_ops, idata, NULL, mode);
   return fpf;
}

CALLEES (32):
  phar_parse_url (ext/phar/stream.c:60): reads filename, mode, options, wrapper; writes -; returns return NULL; | return NULL; | return NULL; | return NULL; | return NULL; | return NULL;
  php_stream_wrapper_log_error (main/streams/streams.c:243): reads fmt, options, wrapper; writes -; returns -
  php_url_free (ext/standard/url.c:30): reads theurl; writes -; returns -
  phar_request_initialize (ext/phar/phar.c:3337): reads -; writes -; returns -
  phar_get_entry_data (ext/phar/util.c:466): reads allow_dir, error, fname, fname_len, mode, path, path_len, ret, security; writes error*, ret*; returns return FAILURE; | return FAILURE; | return FAILURE; | return SUCCESS; | return FAILURE; | return SUCCESS;
  phar_get_pharfp (ext/phar/phar_internal.h:308): reads phar; writes -; returns return phar->fp; | return PHAR_G(cached_fp)[phar->phar_pos].fp;
  phar_open_archive_fp (ext/phar/util.c:712): reads phar; writes -; returns return SUCCESS; | return FAILURE; | return FAILURE; | return SUCCESS;
  phar_get_archive (ext/phar/util.c:957): reads alias, alias_len, archive, error, fname, fname_len; writes archive*, error*; returns return FAILURE; | return SUCCESS; | return FAILURE; | return SUCCESS; | return FAILURE; | return SUCCESS;
  zend_strpprintf_unchecked (Zend/zend.c:366): reads format, max_len; writes -; returns return str;
  phar_metadata_tracker_free (ext/phar/phar.c:632): reads persistent, tracker; writes tracker*; returns -
  zend_hash_str_find_ind (Zend/zend_hash.h:458): reads ht, len, str; writes -; returns return(zv && Z_TYPE_P(zv)== IS_INDIRECT)?((Z_TYPE_P(Z_INDIRECT_P(zv))!= IS_UNDEF)? Z_INDIRECT_P(zv): NULL): zv;
  phar_get_or_create_entry_data (ext/phar/util.c:609): reads allow_dir, error, fname, fname_len, mode, path, path_len, security; writes error*; returns return NULL; | return NULL; | return ret; | return NULL; | return NULL; | return NULL;
  phar_entry_delref (ext/phar/phar.c:392): reads idata; writes -; returns -
  phar_postprocess_file (ext/phar/phar.c:2302): reads crc32, error, idata, process_zip; writes error*, idata*; returns return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return SUCCESS; | return SUCCESS;
  zend_string_equals_literal_ci [macro]: #define zend_string_equals_literal_ci(str, c) \
  estrndup [macro]: #define estrndup(s, length) _estrndup((s), (length) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  strpprintf [macro]: #define strpprintf zend_strpprintf
  ecalloc [macro]: #define ecalloc(nmemb, size) _ecalloc((nmemb), (size) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZSTR_EMPTY_ALLOC [macro]: #define ZSTR_EMPTY_ALLOC() zend_empty_string
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

### Turn 3  _(tok 10229+118, stop=tool_use)_

**Reasoning:** All four confirmed. Let me also double-check there's no call site in dirstream.c or other places that gtags might have missed. I could check the neighborhood of the function definition (which lists callers). Let's do expand_function on phar_get_or_create_entry_data.

Also, there's a possibility of a call inside a macro or in phar_internal.h. Let me check expand_function.


- `expand_function(name=phar_get_or_create_entry_data)` →

```
{
  "name": "phar_get_or_create_entry_data",
  "version": "old",
  "levels": 1,
  "node": {
    "name": "phar_get_or_create_entry_data",
    "file": "ext/phar/util.c",
    "line": 609,
    "kind": "function",
    "state": "analyzed"
  },
  "callees": [
    {
      "name": "ZSTR_VAL",
      "file": "Zend/zend_string.h",
      "line": 68,
      "kind": "macro",
      "state": "analyzed",
      "call_lines": [
        685
      ]
    },
    {
      "name": "efree",
      "file": "Zend/zend_alloc.h",
      "line": 155,
      "kind": "macro",
      "state": "analyzed",
      "call_lines": [
        653,
        686
      ]
    },
    {
      "name": "spprintf",
      "file": "main/spprintf.h",
      "line": 29,
      "kind": "macro",
      "state": "analyzed",
      "call_lines": [
        634,
        639,
        684
      ]
    },
    {
      "name": "php_stream_close",
      "file": "main/php_streams.h",
      "line": 357,
      "kind": "macro",
      "state": "analyzed",
      "call_lines": [
        683
      ]
    },
    {
      "name": "phar_get_entry_data",
      "file": "ext/phar/util.c",
      "line": 466,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        627
      ]
    },
    {
      "name": "phar_get_archive",
      "file": "ext/phar/util.c",
      "line": 957,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        623
      ]
    },
    {
      "name": "phar_copy_on_write",
      "file": "ext/phar/util.c",
      "line": 2065,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        638
      ]
    },
    {
      "name": "emalloc",
      "file": "Zend/zend_alloc.h",
      "line": 151,
      "kind": "macro",
      "state": "analyzed",
      "call_lines": [
        644
      ]
    },
    {
      "name": "php_stream_fopen_tmpfile",
      "file": "main/streams/php_stream_plain_wrapper.h",
      "line": 42,
      "kind": "macro",
      "state": "analyzed",
      "call_lines": [
        649
      ]
    },
    {
      "name": "estrdup",
      "file": "Zend/zend_alloc.h",
      "line": 164,
      "kind": "macro",
      "state": "analyzed",
      "call_lines": [
        652
      ]
    },
    {
      "name": "phar_add_virtual_dirs",
      "file": "ext/phar/util.c",
      "line": 1964,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        669
      ]
    },
    {
      "name": "zend_string_init",
      "file": "Zend/zend_string.h",
      "line": 187,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        674
      ]
    },
    {
      "name": "zend_string_efree",
      "file": "Zend/zend_string.h",
      "line": 327,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        687
      ]
    },
    {
      "name": "zend_hash_add_mem",
      "file": "Zend/zend_hash.h",
      "line": 742,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        682
      ]
    }
  ],
  "callers": [
    {
      "name": "phar_build",
      "file": "ext/phar/phar_object.c",
      "line": 1344,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        1581
      ]
    },
    {
      "name": "phar_add_file",
      "file": "ext/phar/phar_object.c",
      "line": 3504,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        3539
      ]
    },
    {
      "name": "phar_mkdir",
      "file": "ext/phar/phar_object.c",
      "line": 3606,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        3611
      ]
    },
    {
      "name": "phar_wrapper_open_url",
      "file": "ext/phar/stream.c",
      "line": 161,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        194
      ]
    }
  ]
}
```

### Turn 4  _(tok 11806+392, stop=tool_use)_

**Reasoning:** Both tools agree: 4 callers, each with exactly one call site. Note phar_wrapper_open_url appears in stream.c; also check whether there's a similar function in dirstream.c that calls it — no.

One thing: are these functions possibly defined via macros (PHP_METHOD)? No, they're plain static functions with names phar_build, phar_add_file, phar_mkdir, phar_wrapper_open_url.

Submit.


**Says:** 

Verified with both `get_callers` and `expand_function` (which independently report the same four callers), and I confirmed each call site in the source slices:

| Caller | File | Call site |
|---|---|---|
| `phar_build` | ext/phar/phar_object.c | line 1581 |
| `phar_add_file` | ext/phar/phar_object.c | line 3539 |
| `phar_mkdir` | ext/phar/phar_object.c | line 3611 |
| `phar_wrapper_open_url` | ext/phar/stream.c | line 194 |

Each has exactly one call site; the definition (ext/phar/util.c:609) and the prototype are excluded.



- **submit_callers** → `{"callers": [{"function": "phar_build", "file": "ext/phar/phar_object.c"}, {"function": "phar_add_file", "file": "ext/phar/phar_object.c"}, {"function": "phar_mkdir", "file": "ext/phar/phar_object.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 4, "n_truth": 4, "tp": 4, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

