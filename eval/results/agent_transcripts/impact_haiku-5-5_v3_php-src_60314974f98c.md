# Impact-analysis transcript — php-src @ 60314974f98c — anthropic:claude-haiku-5-5

- target: `phar_free_alias` (ext/phar/util.c), arity 3->1
- truth: [['ext/phar/phar.c', 'phar_create_or_parse_filename'], ['ext/phar/phar.c', 'phar_parse_pharfile'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, setAlias)'], ['ext/phar/tar.c', 'phar_parse_tarfile'], ['ext/phar/util.c', 'phar_get_archive'], ['ext/phar/zip.c', 'phar_parse_zipfile']]

## Self-navigation arm

### Turn 1  _(tok 1213+92, stop=tool_use)_

**Reasoning:** I'm going to grep the codebase for phar_free_alias.



- `grep(pattern=phar_free_alias, version=old)` →

```
10 matches
ext/phar/phar.c:1266:			if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
ext/phar/phar.c:1465:			if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
ext/phar/phar_internal.h:416:zend_result phar_free_alias(phar_archive_data *phar, char *alias, size_t alias_len);
ext/phar/phar_object.c:2708:		if (SUCCESS != phar_free_alias(fd_ptr, ZSTR_VAL(new_alias), ZSTR_LEN(new_alias))) {
ext/phar/tar.c:666:			if (SUCCESS != phar_free_alias(fd_ptr, actual_alias, myphar->alias_len)) {
ext/phar/tar.c:681:				if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
ext/phar/util.c:932:zend_result phar_free_alias(phar_archive_data *phar, char *alias, size_t alias_len) /* {{{ */
ext/phar/util.c:1006:				if (SUCCESS == phar_free_alias(fd_ptr, alias, alias_len)) {
ext/phar/zip.c:743:			if (SUCCESS != phar_free_alias(fd_ptr, actual_alias, mydata->alias_len)) {
ext/phar/zip.c:765:				if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
```

### Turn 2  _(tok 1856+804, stop=tool_use)_

**Reasoning:** I need the names of the functions that enclose these lines, so I'll open the code around each location. util.c:1006 sits inside some function I haven't identified yet, so I'm reading the surrounding region to find it.



**Says:** Ten matches. I need the enclosing function for each call site, so I'll read the surrounding code.

- `read_file(path=ext/phar/phar.c, version=old, start_line=1220, end_line=1270)` →

```
ext/phar/phar.c lines 1220-1270 of 3484
 1220| 		} else {
 1221| 			str = entry.filename;
 1222| 		}
 1223| 		zend_hash_add_mem(&mydata->manifest, str, (void*)&entry, sizeof(phar_entry_info));
 1224| 		if (mydata->is_persistent) {
 1225| 			zend_string_release(str);
 1226| 		}
 1227| 	}
 1228| 
 1229| 	snprintf(mydata->version, sizeof(mydata->version), "%u.%u.%u", manifest_ver >> 12, (manifest_ver >> 8) & 0xF, (manifest_ver >> 4) & 0xF);
 1230| 	mydata->halt_offset = halt_offset;
 1231| 	mydata->flags = manifest_flags;
 1232| 	endbuffer = strrchr(mydata->fname, '/');
 1233| 
 1234| 	if (endbuffer) {
 1235| 		mydata->ext = memchr(endbuffer, '.', (mydata->fname + fname_len) - endbuffer);
 1236| 		if (mydata->ext == endbuffer) {
 1237| 			mydata->ext = memchr(endbuffer + 1, '.', (mydata->fname + fname_len) - endbuffer - 1);
 1238| 		}
 1239| 		if (mydata->ext) {
 1240| 			mydata->ext_len = (mydata->fname + mydata->fname_len) - mydata->ext;
 1241| 		}
 1242| 	}
 1243| 
 1244| 	mydata->alias = alias ?
 1245| 		pestrndup(alias, alias_len, mydata->is_persistent) :
 1246| 		pestrndup(mydata->fname, fname_len, mydata->is_persistent);
 1247| 	mydata->alias_len = alias ? alias_len : fname_len;
 1248| 	mydata->sig_flags = sig_flags;
 1249| 	mydata->fp = fp;
 1250| 	mydata->sig_len = sig_len;
 1251| 	mydata->signature = signature;
 1252| 	phar_request_initialize();
 1253| 
 1254| 	if (register_alias) {
 1255| 		phar_archive_data *fd_ptr;
 1256| 
 1257| 		mydata->is_temporary_alias = temp_alias;
 1258| 
 1259| 		if (!phar_validate_alias(mydata->alias, mydata->alias_len)) {
 1260| 			signature = NULL;
 1261| 			fp = NULL;
 1262| 			MAPPHAR_FAIL("Cannot open archive \"%s\", invalid alias");
 1263| 		}
 1264| 
 1265| 		if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
 1266| 			if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
 1267| 				signature = NULL;
 1268| 				fp = NULL;
 1269| 				MAPPHAR_FAIL("Cannot open archive \"%s\", alias is already in use by existing archive");
 1270| 			}
```

- `read_file(path=ext/phar/phar.c, version=old, start_line=1400, end_line=1470)` →

```
ext/phar/phar.c lines 1400-1470 of 3484
 1400| 				zend_string_release_ex(actual, 0);
 1401| 			}
 1402| 			return FAILURE;
 1403| 		}
 1404| 	}
 1405| 
 1406| 	if (actual) {
 1407| 		zend_string_release_ex(actual, 0);
 1408| 	}
 1409| 
 1410| 	if (PHAR_G(readonly) && !is_data) {
 1411| 		if (options & REPORT_ERRORS) {
 1412| 			spprintf(error, 0, "creating archive \"%s\" disabled by the php.ini setting phar.readonly", fname);
 1413| 		}
 1414| 		return FAILURE;
 1415| 	}
 1416| 
 1417| 	/* set up our manifest */
 1418| 	phar_archive_data *mydata = ecalloc(1, sizeof(phar_archive_data));
 1419| 	mydata->fname = expand_filepath(fname, NULL);
 1420| 	if (mydata->fname == NULL) {
 1421| 		efree(mydata);
 1422| 		return FAILURE;
 1423| 	}
 1424| 	fname_len = strlen(mydata->fname);
 1425| #ifdef PHP_WIN32
 1426| 	phar_unixify_path_separators(mydata->fname, fname_len);
 1427| #endif
 1428| 	p = strrchr(mydata->fname, '/');
 1429| 
 1430| 	if (p) {
 1431| 		mydata->ext = memchr(p, '.', (mydata->fname + fname_len) - p);
 1432| 		if (mydata->ext == p) {
 1433| 			mydata->ext = memchr(p + 1, '.', (mydata->fname + fname_len) - p - 1);
 1434| 		}
 1435| 		if (mydata->ext) {
 1436| 			mydata->ext_len = (mydata->fname + fname_len) - mydata->ext;
 1437| 		}
 1438| 	}
 1439| 
 1440| 	zend_hash_init(&mydata->manifest, sizeof(phar_entry_info),
 1441| 		zend_get_hash_value, destroy_phar_manifest_entry, 0);
 1442| 	zend_hash_init(&mydata->mounted_dirs, sizeof(char *),
 1443| 		zend_get_hash_value, NULL, 0);
 1444| 	zend_hash_init(&mydata->virtual_dirs, sizeof(char *),
 1445| 		zend_get_hash_value, NULL, mydata->is_persistent);
 1446| 	mydata->fname_len = fname_len;
 1447| 	snprintf(mydata->version, sizeof(mydata->version), "%s", PHP_PHAR_API_VERSION);
 1448| 	mydata->is_temporary_alias = alias ? 0 : 1;
 1449| 	mydata->fp = NULL;
 1450| 	mydata->is_writeable = 1;
 1451| 	mydata->is_brandnew = 1;
 1452| 	phar_request_initialize();
 1453| 	zend_hash_str_add_ptr(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len, mydata);
 1454| 
 1455| 	if (is_data) {
 1456| 		alias = NULL;
 1457| 		alias_len = 0;
 1458| 		mydata->is_data = 1;
 1459| 		/* assume tar format, PharData can specify other */
 1460| 		mydata->is_tar = 1;
 1461| 	} else {
 1462| 		phar_archive_data *fd_ptr;
 1463| 
 1464| 		if (alias && NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
 1465| 			if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
 1466| 				spprintf(error, 4096, "phar error: phar \"%s\" cannot set alias \"%s\", already in use by another phar archive", mydata->fname, alias);
 1467| 
 1468| 				zend_hash_str_del(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len);
 1469| 
 1470| 				*pphar = NULL;
```

- `read_file(path=ext/phar/phar_object.c, version=old, start_line=2670, end_line=2715)` →

```
ext/phar/phar_object.c lines 2670-2715 of 5059
 2670| {
 2671| 	zend_string *new_alias = NULL;
 2672| 	char *error, *oldalias;
 2673| 	phar_archive_data *fd_ptr;
 2674| 	size_t oldalias_len;
 2675| 	bool old_temp, readd = false;
 2676| 
 2677| 	if (zend_parse_parameters(ZEND_NUM_ARGS(), "S", &new_alias) == FAILURE) {
 2678| 		RETURN_THROWS();
 2679| 	}
 2680| 
 2681| 	PHAR_ARCHIVE_OBJECT();
 2682| 
 2683| 	if (PHAR_G(readonly) && !phar_obj->archive->is_data) {
 2684| 		zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0,
 2685| 			"Cannot write out phar archive, phar is read-only");
 2686| 		RETURN_THROWS();
 2687| 	}
 2688| 
 2689| 	/* invalidate phar cache */
 2690| 	PHAR_G(last_phar) = NULL;
 2691| 	PHAR_G(last_phar_name) = PHAR_G(last_alias) = NULL;
 2692| 
 2693| 	if (phar_obj->archive->is_data) {
 2694| 		if (phar_obj->archive->is_tar) {
 2695| 			zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0,
 2696| 				"A Phar alias cannot be set in a plain tar archive");
 2697| 		} else {
 2698| 			zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0,
 2699| 				"A Phar alias cannot be set in a plain zip archive");
 2700| 		}
 2701| 		RETURN_THROWS();
 2702| 	}
 2703| 
 2704| 	if (zend_string_equals_cstr(new_alias, phar_obj->archive->alias, phar_obj->archive->alias_len)) {
 2705| 		RETURN_TRUE;
 2706| 	}
 2707| 	if (NULL != (fd_ptr = zend_hash_find_ptr(&(PHAR_G(phar_alias_map)), new_alias))) {
 2708| 		if (SUCCESS != phar_free_alias(fd_ptr, ZSTR_VAL(new_alias), ZSTR_LEN(new_alias))) {
 2709| 			zend_throw_exception_ex(phar_ce_PharException, 0, "alias \"%s\" is already used for archive \"%s\" and cannot be used for other archives", ZSTR_VAL(new_alias), fd_ptr->fname);
 2710| 			RETURN_THROWS();
 2711| 		}
 2712| 	} else if (!phar_validate_alias(ZSTR_VAL(new_alias), ZSTR_LEN(new_alias))) {
 2713| 		zend_throw_exception_ex(spl_ce_UnexpectedValueException, 0,
 2714| 			"Invalid alias \"%s\" specified for phar \"%s\"", ZSTR_VAL(new_alias), phar_obj->archive->fname);
 2715| 		RETURN_THROWS();
```

- `read_file(path=ext/phar/tar.c, version=old, start_line=620, end_line=690)` →

```
ext/phar/tar.c lines 620-690 of 1318
  620| 	if (!myphar->is_data && PHAR_G(require_hash) && !myphar->signature) {
  621| 		php_stream_close(fp);
  622| 		phar_destroy_phar_data(myphar);
  623| 		if (error) {
  624| 			spprintf(error, 0, "tar-based phar \"%s\" does not have a signature", fname);
  625| 		}
  626| 		return FAILURE;
  627| 	}
  628| 
  629| 	myphar->fname = pestrndup(fname, fname_len, myphar->is_persistent);
  630| #ifdef PHP_WIN32
  631| 	phar_unixify_path_separators(myphar->fname, fname_len);
  632| #endif
  633| 	myphar->fname_len = fname_len;
  634| 	myphar->fp = fp;
  635| 	p = strrchr(myphar->fname, '/');
  636| 
  637| 	if (p) {
  638| 		myphar->ext = memchr(p, '.', (myphar->fname + fname_len) - p);
  639| 		if (myphar->ext == p) {
  640| 			myphar->ext = memchr(p + 1, '.', (myphar->fname + fname_len) - p - 1);
  641| 		}
  642| 		if (myphar->ext) {
  643| 			myphar->ext_len = (myphar->fname + fname_len) - myphar->ext;
  644| 		}
  645| 	}
  646| 
  647| 	phar_request_initialize();
  648| 
  649| 	if (NULL == (actual = zend_hash_str_add_ptr(&(PHAR_G(phar_fname_map)), myphar->fname, fname_len, myphar))) {
  650| 		if (error) {
  651| 			spprintf(error, 4096, "phar error: Unable to add tar-based phar \"%s\" to phar registry", fname);
  652| 		}
  653| 		php_stream_close(fp);
  654| 		phar_destroy_phar_data(myphar);
  655| 		return FAILURE;
  656| 	}
  657| 
  658| 	myphar = actual;
  659| 
  660| 	if (actual_alias) {
  661| 		phar_archive_data *fd_ptr;
  662| 
  663| 		myphar->is_temporary_alias = 0;
  664| 
  665| 		if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), actual_alias, myphar->alias_len))) {
  666| 			if (SUCCESS != phar_free_alias(fd_ptr, actual_alias, myphar->alias_len)) {
  667| 				if (error) {
  668| 					spprintf(error, 4096, "phar error: Unable to add tar-based phar \"%s\", alias is already in use", fname);
  669| 				}
  670| 				zend_hash_str_del(&(PHAR_G(phar_fname_map)), myphar->fname, fname_len);
  671| 				return FAILURE;
  672| 			}
  673| 		}
  674| 
  675| 		zend_hash_str_add_ptr(&(PHAR_G(phar_alias_map)), actual_alias, myphar->alias_len, myphar);
  676| 	} else {
  677| 		phar_archive_data *fd_ptr;
  678| 
  679| 		if (alias_len) {
  680| 			if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
  681| 				if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
  682| 					if (error) {
  683| 						spprintf(error, 4096, "phar error: Unable to add tar-based phar \"%s\", alias is already in use", fname);
  684| 					}
  685| 					zend_hash_str_del(&(PHAR_G(phar_fname_map)), myphar->fname, fname_len);
  686| 					return FAILURE;
  687| 				}
  688| 			}
  689| 			zend_hash_str_add_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len, myphar);
  690| 			myphar->alias = pestrndup(alias, alias_len, myphar->is_persistent);
```

- `read_file(path=ext/phar/util.c, version=old, start_line=975, end_line=1010)` →

```
ext/phar/util.c lines 975-1010 of 2088
  975| 					spprintf(error, 0, "alias \"%s\" is already used for archive \"%s\" cannot be overloaded with \"%s\"", alias, PHAR_G(last_phar)->fname, fname);
  976| 				}
  977| 				*archive = NULL;
  978| 				return FAILURE;
  979| 			}
  980| 
  981| 			if (PHAR_G(last_phar)->alias_len && NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), PHAR_G(last_phar)->alias, PHAR_G(last_phar)->alias_len))) {
  982| 				zend_hash_str_del(&(PHAR_G(phar_alias_map)), PHAR_G(last_phar)->alias, PHAR_G(last_phar)->alias_len);
  983| 			}
  984| 
  985| 			zend_hash_str_add_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len, *archive);
  986| 			PHAR_G(last_alias) = alias;
  987| 			PHAR_G(last_alias_len) = alias_len;
  988| 		}
  989| 
  990| 		return SUCCESS;
  991| 	}
  992| 
  993| 	if (alias && alias_len && PHAR_G(last_phar) && alias_len == PHAR_G(last_alias_len) && !memcmp(alias, PHAR_G(last_alias), alias_len)) {
  994| 		fd = PHAR_G(last_phar);
  995| 		fd_ptr = fd;
  996| 		goto alias_success;
  997| 	}
  998| 
  999| 	if (alias && alias_len) {
 1000| 		if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
 1001| alias_success:
 1002| 			if (fname && (fname_len != fd_ptr->fname_len || strncmp(fname, fd_ptr->fname, fname_len))) {
 1003| 				if (error) {
 1004| 					spprintf(error, 0, "alias \"%s\" is already used for archive \"%s\" cannot be overloaded with \"%s\"", alias, fd_ptr->fname, fname);
 1005| 				}
 1006| 				if (SUCCESS == phar_free_alias(fd_ptr, alias, alias_len)) {
 1007| 					if (error) {
 1008| 						efree(*error);
 1009| 						*error = NULL;
 1010| 					}
```

- `read_file(path=ext/phar/zip.c, version=old, start_line=700, end_line=770)` →

```
ext/phar/zip.c lines 700-770 of 1486
  700| 					zend_string_release_ex(entry.filename, entry.is_persistent);
  701| 					PHAR_ZIP_FAIL("unable to read in alias, truncated");
  702| 				}
  703| 			}
  704| 
  705| 			/* return to central directory parsing */
  706| 			php_stream_seek(fp, restore_pos, SEEK_SET);
  707| 		}
  708| 
  709| 		phar_set_inode(&entry);
  710| 		zend_hash_add_mem(&mydata->manifest, entry.filename, &entry, sizeof(phar_entry_info));
  711| 	}
  712| 
  713| 	if (zend_hash_str_exists(&(mydata->manifest), ".phar/stub.php", sizeof(".phar/stub.php")-1)) {
  714| 		mydata->is_data = 0;
  715| 	} else {
  716| 		mydata->is_data = 1;
  717| 	}
  718| 
  719| 	/* ensure signature set */
  720| 	if (!mydata->is_data && PHAR_G(require_hash) && !mydata->signature) {
  721| 		PHAR_ZIP_FAIL("signature is missing");
  722| 	}
  723| 
  724| 	mydata->fp = fp;
  725| 
  726| 	zend_hash_str_add_ptr(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len, mydata);
  727| 
  728| 	if (actual_alias) {
  729| 		phar_archive_data *fd_ptr;
  730| 
  731| 		if (!phar_validate_alias(actual_alias, mydata->alias_len)) {
  732| 			if (error) {
  733| 				spprintf(error, 4096, "phar error: invalid alias \"%s\" in zip-based phar \"%s\"", actual_alias, fname);
  734| 			}
  735| 			efree(actual_alias);
  736| 			zend_hash_str_del(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len);
  737| 			return FAILURE;
  738| 		}
  739| 
  740| 		mydata->is_temporary_alias = 0;
  741| 
  742| 		if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), actual_alias, mydata->alias_len))) {
  743| 			if (SUCCESS != phar_free_alias(fd_ptr, actual_alias, mydata->alias_len)) {
  744| 				if (error) {
  745| 					spprintf(error, 4096, "phar error: Unable to add zip-based phar \"%s\" with implicit alias, alias is already in use", fname);
  746| 				}
  747| 				efree(actual_alias);
  748| 				zend_hash_str_del(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len);
  749| 				return FAILURE;
  750| 			}
  751| 		}
  752| 
  753| 		mydata->alias = entry.is_persistent ? pestrndup(actual_alias, mydata->alias_len, 1) : actual_alias;
  754| 
  755| 		if (entry.is_persistent) {
  756| 			efree(actual_alias);
  757| 		}
  758| 
  759| 		zend_hash_str_add_ptr(&(PHAR_G(phar_alias_map)), mydata->alias, mydata->alias_len, mydata);
  760| 	} else {
  761| 		phar_archive_data *fd_ptr;
  762| 
  763| 		if (alias_len) {
  764| 			if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
  765| 				if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
  766| 					if (error) {
  767| 						spprintf(error, 4096, "phar error: Unable to add zip-based phar \"%s\" with explicit alias, alias is already in use", fname);
  768| 					}
  769| 					zend_hash_str_del(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len);
  770| 					return FAILURE;
```

### Turn 3  _(tok 10652+890, stop=tool_use)_

**Reasoning:** I need to find the enclosing function for each site, so I'll grep the files for function definitions, matching lines that start with an identifier followed by an open paren.



**Says:** The call sites are identified, but I still need the enclosing function for each one. I'll locate the function definitions in these files.

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ext/phar/phar.c, max_results=300)` →

```
61 matches
ext/phar/phar.c:29:static void destroy_phar_data(zval *zv);
ext/phar/phar.c:31:ZEND_DECLARE_MODULE_GLOBALS(phar)
ext/phar/phar.c:32:static zend_string *(*phar_save_resolve_path)(zend_string *filename);
ext/phar/phar.c:37:static int phar_set_writeable_bit(zval *zv, void *argument) /* {{{ */
ext/phar/phar.c:51:ZEND_INI_MH(phar_ini_modify_handler) /* {{{ */
ext/phar/phar.c:91:static void phar_split_cache_list(void) /* {{{ */
ext/phar/phar.c:171:ZEND_INI_MH(phar_ini_cache_list) /* {{{ */
ext/phar/phar.c:183:PHP_INI_BEGIN()
ext/phar/phar.c:187:PHP_INI_END()
ext/phar/phar.c:193:void phar_destroy_phar_data(phar_archive_data *phar) /* {{{ */
ext/phar/phar.c:244:bool phar_archive_delref(phar_archive_data *phar) /* {{{ */
ext/phar/phar.c:294:static void destroy_phar_data_only(zval *zv) /* {{{ */
ext/phar/phar.c:307:static int phar_unalias_apply(zval *zv, void *argument) /* {{{ */
ext/phar/phar.c:316:static int phar_tmpclose_apply(zval *zv) /* {{{ */
ext/phar/phar.c:336:static void destroy_phar_data(zval *zv) /* {{{ */
ext/phar/phar.c:359:void destroy_phar_manifest_entry_int(phar_entry_info *entry) /* {{{ */
ext/phar/phar.c:388:void destroy_phar_manifest_entry(zval *zv) /* {{{ */
ext/phar/phar.c:396:void phar_entry_delref(phar_entry_data *idata) /* {{{ */
ext/phar/phar.c:421:ZEND_ATTRIBUTE_NONNULL void phar_entry_remove(phar_entry_data *idata, char **error) /* {{{ */
ext/phar/phar.c:486:static zend_result phar_open_parsed_phar(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_archive_data** pphar, char **error) /* {
ext/phar/phar.c:563:void phar_metadata_tracker_try_ensure_has_serialized_data(phar_metadata_tracker *tracker, bool persistent) /* {{{ */
ext/phar/phar.c:589:zend_result phar_metadata_tracker_unserialize_or_copy(phar_metadata_tracker *tracker, zval *metadata, bool persistent, HashTable *unserialize_options, const char* method_name) /* {
ext/phar/phar.c:626:bool phar_metadata_tracker_has_data(const phar_metadata_tracker *tracker, bool persistent) /* {{{ */
ext/phar/phar.c:636:void phar_metadata_tracker_free(phar_metadata_tracker *tracker, bool persistent) /* {{{ */
ext/phar/phar.c:658:void phar_metadata_tracker_copy(phar_metadata_tracker *dest, const phar_metadata_tracker *source, bool persistent) /* {{{ */
ext/phar/phar.c:676:void phar_metadata_tracker_clone(phar_metadata_tracker *tracker) /* {{{ */
ext/phar/phar.c:694:void phar_parse_metadata_lazy(const char *buffer, phar_metadata_tracker *tracker, uint32_t zip_metadata_len, bool persistent) /* {{{ */
ext/phar/phar.c:725:static zend_result phar_parse_pharfile(php_stream *fp, char *fname, size_t fname_len, char *alias, size_t alias_len, zend_long halt_offset, phar_archive_data** pphar, uint32_t comp
ext/phar/phar.c:1304:ZEND_ATTRIBUTE_NONNULL_ARGS(1, 7, 8) zend_result phar_open_or_create_filename(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_ar
ext/phar/phar.c:1368:static zend_result phar_open_from_fp(php_stream* fp, char *fname, size_t fname_len, char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error);
ext/phar/phar.c:1370:ZEND_ATTRIBUTE_NONNULL_ARGS(1, 7, 8) zend_result phar_create_or_parse_filename(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_a
ext/phar/phar.c:1507:zend_result phar_open_from_filename(char *fname, size_t fname_len, char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error) /* {{{ */
ext/phar/phar.c:1564:static zend_result phar_open_from_fp(php_stream* fp, char *fname, size_t fname_len, char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error) /* {{
ext/phar/phar.c:1749:static zend_result phar_analyze_path(const char *fname, const char *ext, size_t ext_len, int for_create) /* {{{ */
ext/phar/phar.c:1854:static zend_result phar_check_str(const char *fname, const char *ext_str, size_t ext_len, int executable, int for_create) /* {{{ */
ext/phar/phar.c:1906:zend_result phar_detect_phar_fname_ext(const char *filename, size_t filename_len, const char **ext_str, size_t *ext_len, int executable, int for_create, bool is_complete) /* {{{ *
ext/phar/phar.c:2040:static bool php_check_dots(const char *element, size_t n) /* {{{ */
ext/phar/phar.c:2062:zend_string* phar_fix_filepath(const char *path, size_t path_length, bool use_cwd) /* {{{ */
ext/phar/phar.c:2166:zend_result phar_split_fname(const char *filename, size_t filename_len, char **arch, size_t *arch_len, zend_string **entry, int executable, int for_create) /* {{{ */
ext/phar/phar.c:2242:ZEND_ATTRIBUTE_NONNULL_ARGS(3) zend_result phar_open_executed_filename(char *alias, size_t alias_len, char **error) /* {{{ */
ext/phar/phar.c:2295:ZEND_ATTRIBUTE_NONNULL zend_result phar_postprocess_file(phar_entry_data *idata, uint32_t crc32, char **error, int process_zip) /* {{{ */
ext/phar/phar.c:2379:static inline void phar_set_32(char *buffer, uint32_t var) /* {{{ */
ext/phar/phar.c:2391:static int phar_flush_clean_deleted_apply(zval *zv) /* {{{ */
ext/phar/phar.c:2405:zend_string *phar_create_default_stub(const zend_string *php_index_str, const zend_string *web_index_str, char **error) /* {{{ */
ext/phar/phar.c:2450:ZEND_ATTRIBUTE_NONNULL int phar_flush(phar_archive_data *phar, char **error) {
ext/phar/phar.c:2459:ZEND_ATTRIBUTE_NONNULL_ARGS(1, 4) int phar_flush_ex(phar_archive_data *phar, zend_string *user_stub, bool is_default_stub, char **error) /* {{{ */
ext/phar/phar.c:3113:ZEND_TSRMLS_CACHE_DEFINE()
ext/phar/phar.c:3115:ZEND_GET_MODULE(phar)
ext/phar/phar.c:3118:static ssize_t phar_zend_stream_reader(void *handle, char *buf, size_t len) /* {{{ */
ext/phar/phar.c:3124:static size_t phar_zend_stream_fsizer(void *handle) /* {{{ */
ext/phar/phar.c:3129:zend_op_array *(*phar_orig_compile_file)(zend_file_handle *file_handle, int type);
ext/phar/phar.c:3131:static zend_string *phar_resolve_path(zend_string *filename)
ext/phar/phar.c:3140:static zend_op_array *phar_compile_file(zend_file_handle *file_handle, int type) /* {{{ */
ext/phar/phar.c:3215:static void mime_type_dtor(zval *zv)
ext/phar/phar.c:3220:PHP_GINIT_FUNCTION(phar) /* {{{ */
ext/phar/phar.c:3286:PHP_GSHUTDOWN_FUNCTION(phar) /* {{{ */
ext/phar/phar.c:3292:PHP_MINIT_FUNCTION(phar) /* {{{ */
ext/phar/phar.c:3311:PHP_MSHUTDOWN_FUNCTION(phar) /* {{{ */
ext/phar/phar.c:3331:void phar_request_initialize(void) /* {{{ */
ext/phar/phar.c:3365:PHP_RSHUTDOWN_FUNCTION(phar) /* {{{ */
ext/phar/phar.c:3410:PHP_MINFO_FUNCTION(phar) /* {{{ */
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ext/phar/phar_object.c, max_results=300)` →

```
95 matches
ext/phar/phar_object.c:45:static int phar_file_type(const HashTable *mimes, const char *file, char **mime_type) /* {{{ */
ext/phar/phar_object.c:64:static void phar_mung_server_vars(char *fname, char *entry, size_t entry_len, const char *basename, size_t request_uri_len) /* {{{ */
ext/phar/phar_object.c:155:static phar_action_status phar_file_action(phar_archive_data *phar, phar_entry_info *info, char *mime_type, int code, char *entry, size_t entry_len, char *arch, const char *
ext/phar/phar_object.c:305:static void phar_do_403(void) /* {{{ */
ext/phar/phar_object.c:319:static void phar_do_404(phar_archive_data *phar, char *fname, size_t fname_len, zend_string *f404) /* {{{ */
ext/phar/phar_object.c:347:static void phar_postprocess_ru_web(char *fname, size_t fname_len, char *entry, size_t *entry_len, char **ru, size_t *ru_len) /* {{{ */
ext/phar/phar_object.c:404:PHP_METHOD(Phar, running)
ext/phar/phar_object.c:445:PHP_METHOD(Phar, mount)
ext/phar/phar_object.c:548:PHP_METHOD(Phar, webPhar)
ext/phar/phar_object.c:860:PHP_METHOD(Phar, mungServer)
ext/phar/phar_object.c:910:PHP_METHOD(Phar, interceptFileFuncs)
ext/phar/phar_object.c:921:PHP_METHOD(Phar, createDefaultStub)
ext/phar/phar_object.c:943:PHP_METHOD(Phar, mapPhar)
ext/phar/phar_object.c:964:PHP_METHOD(Phar, loadPhar)
ext/phar/phar_object.c:984:PHP_METHOD(Phar, apiVersion)
ext/phar/phar_object.c:992:PHP_METHOD(Phar, canCompress)
ext/phar/phar_object.c:1013:PHP_METHOD(Phar, canWrite)
ext/phar/phar_object.c:1021:PHP_METHOD(Phar, isValidPharFilename)
ext/phar/phar_object.c:1040:static void phar_spl_foreign_dtor(spl_filesystem_object *object) /* {{{ */
ext/phar/phar_object.c:1055:static void phar_spl_foreign_clone(spl_filesystem_object *src, spl_filesystem_object *dst) /* {{{ */
ext/phar/phar_object.c:1078:PHP_METHOD(Phar, __construct)
ext/phar/phar_object.c:1218:PHP_METHOD(Phar, getSupportedSignatures)
ext/phar/phar_object.c:1243:PHP_METHOD(Phar, getSupportedCompression)
ext/phar/phar_object.c:1261:PHP_METHOD(Phar, unlinkArchive)
ext/phar/phar_object.c:1326:PHP_METHOD(Phar, __destruct)
ext/phar/phar_object.c:1347:static zend_always_inline void phar_call_method_with_unwrap(zend_object *obj, const char *name, zval *rv)
ext/phar/phar_object.c:1356:static phar_entry_data *phar_build_entry_data(char *fname, size_t fname_len, char *path, size_t path_len, char **error, zval *file_info)
ext/phar/phar_object.c:1385:static int phar_build(zend_object_iterator *iter, void *puser) /* {{{ */
ext/phar/phar_object.c:1719:PHP_METHOD(Phar, buildFromDirectory)
ext/phar/phar_object.c:1827:PHP_METHOD(Phar, buildFromIterator)
ext/phar/phar_object.c:1878:PHP_METHOD(Phar, count)
ext/phar/phar_object.c:1896:PHP_METHOD(Phar, isFileFormat)
ext/phar/phar_object.c:1919:static zend_result phar_copy_file_contents(phar_entry_info *entry, php_stream *fp) /* {{{ */
ext/phar/phar_object.c:1954:static zend_object *phar_rename_archive(phar_archive_data **sphar, char *ext) /* {{{ */
ext/phar/phar_object.c:2211:static zend_object *phar_convert_to_other(phar_archive_data *source, int convert, char *ext, uint32_t flags) /* {{{ */
ext/phar/phar_object.c:2336:PHP_METHOD(Phar, convertToExecutable)
ext/phar/phar_object.c:2446:PHP_METHOD(Phar, convertToData)
ext/phar/phar_object.c:2554:PHP_METHOD(Phar, isCompressed)
ext/phar/phar_object.c:2573:PHP_METHOD(Phar, isWritable)
ext/phar/phar_object.c:2595:PHP_METHOD(Phar, delete)
ext/phar/phar_object.c:2643:PHP_METHOD(Phar, getAlias)
ext/phar/phar_object.c:2656:PHP_METHOD(Phar, getPath)
ext/phar/phar_object.c:2669:PHP_METHOD(Phar, setAlias)
ext/phar/phar_object.c:2766:PHP_METHOD(Phar, getVersion)
ext/phar/phar_object.c:2777:PHP_METHOD(Phar, startBuffering)
ext/phar/phar_object.c:2788:PHP_METHOD(Phar, isBuffering)
ext/phar/phar_object.c:2799:PHP_METHOD(Phar, stopBuffering)
ext/phar/phar_object.c:2826:PHP_METHOD(Phar, setStub)
ext/phar/phar_object.c:2923:PHP_METHOD(Phar, setDefaultStub)
ext/phar/phar_object.c:2998:PHP_METHOD(Phar, setSignatureAlgorithm)
ext/phar/phar_object.c:3047:PHP_METHOD(Phar, getSignature)
ext/phar/phar_object.c:3092:PHP_METHOD(Phar, getModified)
ext/phar/phar_object.c:3102:static int phar_set_compression(zval *zv, void *argument) /* {{{ */
ext/phar/phar_object.c:3119:static int phar_test_compression(zval *zv, void *argument) /* {{{ */
ext/phar/phar_object.c:3145:static void pharobj_set_compression(HashTable *manifest, uint32_t compress) /* {{{ */
ext/phar/phar_object.c:3151:static int pharobj_cancompress(HashTable *manifest) /* {{{ */
ext/phar/phar_object.c:3165:PHP_METHOD(Phar, compress)
ext/phar/phar_object.c:3233:PHP_METHOD(Phar, decompress)
ext/phar/phar_object.c:3275:PHP_METHOD(Phar, compressFiles)
ext/phar/phar_object.c:3350:PHP_METHOD(Phar, decompressFiles)
ext/phar/phar_object.c:3393:PHP_METHOD(Phar, copy)
ext/phar/phar_object.c:3487:PHP_METHOD(Phar, offsetExists)
ext/phar/phar_object.c:3517:PHP_METHOD(Phar, offsetGet)
ext/phar/phar_object.c:3568:static void phar_add_file(phar_archive_data **pphar, zend_string *file_name, const zend_string *content, zval *zresource)
ext/phar/phar_object.c:3670:static void phar_mkdir(phar_archive_data **pphar, zend_string *dir_name)
ext/phar/phar_object.c:3705:PHP_METHOD(Phar, offsetSet)
ext/phar/phar_object.c:3743:PHP_METHOD(Phar, offsetUnset)
ext/phar/phar_object.c:3790:PHP_METHOD(Phar, addEmptyDir)
ext/phar/phar_object.c:3810:PHP_METHOD(Phar, addFile)
ext/phar/phar_object.c:3844:PHP_METHOD(Phar, addFromString)
ext/phar/phar_object.c:3860:PHP_METHOD(Phar, getStub)
ext/phar/phar_object.c:3955:PHP_METHOD(Phar, hasMetadata)
ext/phar/phar_object.c:3966:PHP_METHOD(Phar, getMetadata)
ext/phar/phar_object.c:3986:static zend_result serialize_metadata_or_throw(phar_metadata_tracker *tracker, bool persistent, zval *metadata)
ext/phar/phar_object.c:4017:PHP_METHOD(Phar, setMetadata)
ext/phar/phar_object.c:4054:PHP_METHOD(Phar, delMetadata)
ext/phar/phar_object.c:4085:ZEND_ATTRIBUTE_NONNULL static zend_result phar_extract_file(bool overwrite, phar_entry_info *entry, const zend_string *path, char **error) /* {{{ */
ext/phar/phar_object.c:4263:ZEND_ATTRIBUTE_NONNULL_ARGS(1, 3, 5) static int extract_helper(const phar_archive_data *archive, zend_string *search, const zend_string *path_to, bool overwrite, char **err
ext/phar/phar_object.c:4293:PHP_METHOD(Phar, extractTo)
ext/phar/phar_object.c:4393:PHP_METHOD(PharFileInfo, __construct)
ext/phar/phar_object.c:4476:PHP_METHOD(PharFileInfo, __destruct)
ext/phar/phar_object.c:4503:PHP_METHOD(PharFileInfo, getCompressedSize)
ext/phar/phar_object.c:4514:PHP_METHOD(PharFileInfo, isCompressed)
ext/phar/phar_object.c:4544:PHP_METHOD(PharFileInfo, getCRC32)
ext/phar/phar_object.c:4566:PHP_METHOD(PharFileInfo, isCRCChecked)
ext/phar/phar_object.c:4577:PHP_METHOD(PharFileInfo, getPharFlags)
ext/phar/phar_object.c:4588:PHP_METHOD(PharFileInfo, chmod)
ext/phar/phar_object.c:4650:PHP_METHOD(PharFileInfo, hasMetadata)
ext/phar/phar_object.c:4661:PHP_METHOD(PharFileInfo, getMetadata)
ext/phar/phar_object.c:4681:PHP_METHOD(PharFileInfo, setMetadata)
ext/phar/phar_object.c:4731:PHP_METHOD(PharFileInfo, delMetadata)
ext/phar/phar_object.c:4783:PHP_METHOD(PharFileInfo, getContent)
ext/phar/phar_object.c:4830:PHP_METHOD(PharFileInfo, compress)
ext/phar/phar_object.c:4957:PHP_METHOD(PharFileInfo, decompress)
ext/phar/phar_object.c:5048:void phar_object_init(void) /* {{{ */
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ext/phar/tar.c, max_results=300)` →

```
12 matches
ext/phar/tar.c:21:static uint32_t phar_tar_number(const char *buf, size_t len) /* {{{ */
ext/phar/tar.c:64:static zend_result phar_tar_octal(char *buf, uint32_t val, size_t len) /* {{{ */
ext/phar/tar.c:88:static uint32_t phar_tar_checksum(const char *buf, size_t len) /* {{{ */
ext/phar/tar.c:101:bool phar_is_tar(const char *buf, const char *fname) /* {{{ */
ext/phar/tar.c:129:ZEND_ATTRIBUTE_NONNULL_ARGS(1, 7, 8) zend_result phar_open_or_create_tar(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_archive_d
ext/phar/tar.c:158:static zend_result phar_tar_process_metadata(phar_entry_info *entry, php_stream *fp) /* {{{ */
ext/phar/tar.c:200:zend_result phar_parse_tarfile(php_stream* fp, char *fname, size_t fname_len, char *alias, size_t alias_len, phar_archive_data** pphar, uint32_t compression, char **error) /* {{{ */
ext/phar/tar.c:716:static int phar_tar_writeheaders_int(phar_entry_info *entry, void *argument) /* {{{ */
ext/phar/tar.c:869:static int phar_tar_writeheaders(zval *zv, void *argument) /* {{{ */
ext/phar/tar.c:875:ZEND_ATTRIBUTE_NONNULL static int phar_tar_setmetadata(const phar_metadata_tracker *tracker, phar_entry_info *entry, char **error) /* {{{ */
ext/phar/tar.c:908:ZEND_ATTRIBUTE_NONNULL static int phar_tar_setupmetadata(zval *zv, void *argument) /* {{{ */
ext/phar/tar.c:962:ZEND_ATTRIBUTE_NONNULL_ARGS(1, 4) int phar_tar_flush(phar_archive_data *phar, zend_string *user_stub, bool is_default_stub, char **error) /* {{{ */
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ext/phar/util.c, max_results=300)` →

```
35 matches
ext/phar/util.c:37:static zend_result phar_call_openssl_signverify(bool is_sign, php_stream *fp, zend_off_t end, char *key, size_t key_len, char **signature, size_t *signature_len, uint32_t sig_type);
ext/phar/util.c:41:static char *phar_get_link_location(phar_entry_info *entry) /* {{{ */
ext/phar/util.c:63:phar_entry_info *phar_get_link_source(phar_entry_info *entry) /* {{{ */
ext/phar/util.c:88:static php_stream *phar_get_entrypufp(const phar_entry_info *entry)
ext/phar/util.c:97:php_stream *phar_get_efp(phar_entry_info *entry, bool follow_links) /* {{{ */
ext/phar/util.c:128:static zend_off_t phar_get_fp_offset(const phar_entry_info *entry)
ext/phar/util.c:141:int phar_seek_efp(phar_entry_info *entry, zend_off_t offset, int whence, zend_off_t position, bool follow_links) /* {{{ */
ext/phar/util.c:191:zend_result phar_mount_entry(phar_archive_data *phar, char *filename, size_t filename_len, char *path, size_t path_len) /* {{{ */
ext/phar/util.c:266:zend_string *phar_find_in_include_path(zend_string *filename, phar_archive_data **pphar) /* {{{ */
ext/phar/util.c:364:static ZEND_ATTRIBUTE_NONNULL zend_result phar_create_writeable_entry(phar_archive_data *phar, phar_entry_info *entry, char **error) /* {{{ */
ext/phar/util.c:413:ZEND_ATTRIBUTE_NONNULL static zend_result phar_separate_entry_fp(phar_entry_info *entry, char **error) /* {{{ */
ext/phar/util.c:465:ZEND_ATTRIBUTE_NONNULL zend_result phar_get_entry_data(phar_entry_data **ret, char *fname, size_t fname_len, char *path, size_t path_len, const char *mode, char allow_dir, char **e
ext/phar/util.c:608:ZEND_ATTRIBUTE_NONNULL phar_entry_data *phar_get_or_create_entry_data(char *fname, size_t fname_len, char *path, size_t path_len, const char *mode, char allow_dir, char **error, bo
ext/phar/util.c:700:static inline void phar_set_pharfp(phar_archive_data *phar, php_stream *fp)
ext/phar/util.c:712:php_stream *phar_open_archive_fp(phar_archive_data *phar) /* {{{ */
ext/phar/util.c:731:ZEND_ATTRIBUTE_NONNULL zend_result phar_copy_entry_fp(phar_entry_info *source, phar_entry_info *dest, char **error) /* {{{ */
ext/phar/util.c:772:static void phar_set_entrypufp(const phar_entry_info *entry, php_stream *fp)
ext/phar/util.c:782:static void phar_set_fp_type(phar_entry_info *entry, enum phar_fp_type type, zend_off_t offset)
ext/phar/util.c:798:ZEND_ATTRIBUTE_NONNULL zend_result phar_open_entry_fp(phar_entry_info *entry, char **error, bool follow_links) /* {{{ */
ext/phar/util.c:917:ZEND_ATTRIBUTE_NONNULL phar_entry_info * phar_open_jit(const phar_archive_data *phar, phar_entry_info *entry, char **error) /* {{{ */
ext/phar/util.c:932:zend_result phar_free_alias(phar_archive_data *phar, char *alias, size_t alias_len) /* {{{ */
ext/phar/util.c:955:zend_result phar_get_archive(phar_archive_data **archive, char *fname, size_t fname_len, char *alias, size_t alias_len, char **error) /* {{{ */
ext/phar/util.c:1159:const char * phar_compress_filter(const phar_entry_info *entry, bool return_unknown) /* {{{ */
ext/phar/util.c:1175:const char * phar_decompress_filter(const phar_entry_info *entry, bool return_unknown) /* {{{ */
ext/phar/util.c:1199:phar_entry_info *phar_get_entry_info(phar_archive_data *phar, char *path, size_t path_len, char **error, bool security) /* {{{ */
ext/phar/util.c:1210:phar_entry_info *phar_get_entry_info_dir(phar_archive_data *phar, char *path, size_t path_len, char dir, char **error, bool security) /* {{{ */
ext/phar/util.c:1368:static int phar_hex_str(const char *digest, size_t digest_len, char **signature) /* {{{ */
ext/phar/util.c:1385:static zend_result phar_call_openssl_signverify(bool is_sign, php_stream *fp, zend_off_t end, char *key, size_t key_len, char **signature, size_t *signature_len, uint32_t sig_type
ext/phar/util.c:1476:zend_result phar_verify_signature(php_stream *fp, size_t end_of_phar, uint32_t sig_type, char *sig, size_t sig_len, char *fname, char **signature, size_t *signature_len, char **er
ext/phar/util.c:1790:ZEND_ATTRIBUTE_NONNULL zend_result phar_create_signature(phar_archive_data *phar, php_stream *fp, char **signature, size_t *signature_length, char **error) /* {{{ */
ext/phar/util.c:1962:void phar_add_virtual_dirs(phar_archive_data *phar, char *filename, size_t filename_len) /* {{{ */
ext/phar/util.c:1987:static int phar_update_cached_entry(zval *data, void *argument) /* {{{ */
ext/phar/util.c:2010:static void phar_manifest_copy_ctor(zval *zv) /* {{{ */
ext/phar/util.c:2018:static void phar_copy_cached_phar(phar_archive_data **pphar) /* {{{ */
ext/phar/util.c:2063:zend_result phar_copy_on_write(phar_archive_data **pphar) /* {{{ */
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ext/phar/zip.c, max_results=300)` →

```
12 matches
ext/phar/zip.c:27:static inline void phar_write_32(char buffer[4], uint32_t value)
ext/phar/zip.c:34:static inline void phar_write_16(char buffer[2], uint32_t value)
ext/phar/zip.c:42:static zend_result phar_zip_process_extra(php_stream *fp, phar_entry_info *entry, uint16_t len) /* {{{ */
ext/phar/zip.c:153:static time_t phar_zip_d2u_time(const char *cdtime, const char *cddate) /* {{{ */
ext/phar/zip.c:174:static void phar_zip_u2d_time(time_t time, char *dtime, char *ddate) /* {{{ */
ext/phar/zip.c:195:static char *phar_find_eocd(const char *s, size_t n)
ext/phar/zip.c:227:zend_result phar_parse_zipfile(php_stream *fp, char *fname, size_t fname_len, char *alias, size_t alias_len, phar_archive_data** pphar, char **error) /* {{{ */
ext/phar/zip.c:796:ZEND_ATTRIBUTE_NONNULL_ARGS(1, 7, 8) zend_result phar_open_or_create_zip(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_archive_d
ext/phar/zip.c:835:static int phar_zip_changed_apply_int(phar_entry_info *entry, void *arg) /* {{{ */
ext/phar/zip.c:1140:static int phar_zip_changed_apply(zval *zv, void *arg) /* {{{ */
ext/phar/zip.c:1146:static zend_result phar_zip_applysignature(phar_archive_data *phar, struct _phar_zip_pass *pass) /* {{{ */
ext/phar/zip.c:1225:ZEND_ATTRIBUTE_NONNULL_ARGS(1, 4) int phar_zip_flush(phar_archive_data *phar, zend_string *user_stub, bool is_default_stub, char **error) /* {{{ */
```

### Turn 4  _(tok 22921+639, stop=tool_use)_

**Reasoning:** I'm checking which function encloses line 1266 in phar.c, and it looks like that's phar_parse_pharfile. I'm also looking at line 1465, which sits near phar_open_from_fp, though I'm not yet sure whether it falls inside that definition or between prototypes.

I'm now checking the enclosing functions for several other call sites, including phar_object.c:2708 inside PHP_METHOD(Phar, setAlias), tar.c around lines 666 and 681, util.c:1006, and zip.c at 743 and 765. For line 1370 in phar.c, I still need to confirm whether it's a definition or a prototype, so I'll look at lines 1370 to 1372.



**Says:** Most enclosing functions are now clear from the definition list. The one open question is whether line 1370 in `phar.c` is a definition or a prototype, which decides the enclosing function for line 1465. I'll check that.

- `read_file(path=ext/phar/phar.c, version=old, start_line=1368, end_line=1376)` →

```
ext/phar/phar.c lines 1368-1376 of 3484
 1368| static zend_result phar_open_from_fp(php_stream* fp, char *fname, size_t fname_len, char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error);
 1369| 
 1370| ZEND_ATTRIBUTE_NONNULL_ARGS(1, 7, 8) zend_result phar_create_or_parse_filename(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_archive_data** pphar, char **error) /* {{{ */
 1371| {
 1372| 	php_stream *fp;
 1373| 	zend_string *actual = NULL;
 1374| 	char *p;
 1375| 
 1376| 	if (php_check_open_basedir(fname)) {
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 24031+251, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "phar_parse_pharfile", "file": "ext/phar/phar.c"}, {"function": "phar_create_or_parse_filename", "file": "ext/phar/phar.c"}, {"function": "setAlias", "file": "ext/phar/phar_object.c"}, {"function": "phar_parse_tarfile", "file": "ext/phar/tar.c"}, {"function": "phar_get_archive", "file": "ext/phar/util.c"}, {"function": "phar_parse_zipfile", "file": "ext/phar/zip.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 6, "n_truth": 6, "tp": 5, "precision": 0.8333333333333334, "recall": 0.8333333333333334, "f1": 0.8333333333333334}`

## Tool arm

### Turn 1  _(tok 3748+228, stop=tool_use)_

**Reasoning:** I'm going to pull the callers of phar_free_alias first, then run a grep on it as well to make sure nothing is missed.



- `get_callers(name=phar_free_alias, limit=200, rev=None)` →

```
{
  "name": "phar_free_alias",
  "version": "old",
  "callers": [
    {
      "caller": "phar_parse_pharfile",
      "file": "ext/phar/phar.c",
      "line": 1266
    },
    {
      "caller": "phar_create_or_parse_filename",
      "file": "ext/phar/phar.c",
      "line": 1465
    },
    {
      "caller": "PHP_METHOD(Phar, setAlias)",
      "file": "ext/phar/phar_object.c",
      "line": 2708
    },
    {
      "caller": "phar_parse_tarfile",
      "file": "ext/phar/tar.c",
      "line": 666
    },
    {
      "caller": "phar_parse_tarfile",
      "file": "ext/phar/tar.c",
      "line": 681
    },
    {
      "caller": "phar_get_archive",
      "file": "ext/phar/util.c",
      "line": 1006
    },
    {
      "caller": "phar_parse_zipfile",
      "file": "ext/phar/zip.c",
      "line": 743
    },
    {
      "caller": "phar_parse_zipfile",
      "file": "ext/phar/zip.c",
      "line": 765
    }
  ]
}
```

- `grep(pattern=phar_free_alias, version=old, max_results=200)` →

```
10 matches
ext/phar/phar.c:1266:			if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
ext/phar/phar.c:1465:			if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
ext/phar/phar_internal.h:416:zend_result phar_free_alias(phar_archive_data *phar, char *alias, size_t alias_len);
ext/phar/phar_object.c:2708:		if (SUCCESS != phar_free_alias(fd_ptr, ZSTR_VAL(new_alias), ZSTR_LEN(new_alias))) {
ext/phar/tar.c:666:			if (SUCCESS != phar_free_alias(fd_ptr, actual_alias, myphar->alias_len)) {
ext/phar/tar.c:681:				if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
ext/phar/util.c:932:zend_result phar_free_alias(phar_archive_data *phar, char *alias, size_t alias_len) /* {{{ */
ext/phar/util.c:1006:				if (SUCCESS == phar_free_alias(fd_ptr, alias, alias_len)) {
ext/phar/zip.c:743:			if (SUCCESS != phar_free_alias(fd_ptr, actual_alias, mydata->alias_len)) {
ext/phar/zip.c:765:				if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
```

### Turn 2  _(tok 5010+681, stop=tool_use)_

**Reasoning:** Callers are the same across grep, so I'm checking which function encloses the util.c:1006 hit, since the caller list points to phar_get_archive. I also want to confirm the enclosing function for each other call site before I decide what to do next.

I'm going to check that the grep really covers every call site, and I'm noting that the tool reports PHP_METHOD(Phar, setAlias) even though the C symbol is zim_Phar_setAlias. I'll list it under the tool's name and mention the C symbol alongside it.



- **submit_callers** → `{"callers": [{"function": "phar_parse_pharfile", "file": "ext/phar/phar.c"}, {"function": "phar_create_or_parse_filename", "file": "ext/phar/phar.c"}, {"function": "PHP_METHOD(Phar, setAlias)", "file": "ext/phar/phar_object.c"}, {"function": "phar_parse_tarfile", "file": "ext/phar/tar.c"}, {"function": "phar_get_archive", "file": "ext/phar/util.c"}, {"function": "phar_parse_zipfile", "file": "ext/phar/zip.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 6, "n_truth": 6, "tp": 6, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3200+104, stop=tool_use)_

**Reasoning:** I'm going to call get_callers on phar_free_alias with a high limit to pull up everything that references it.



- `get_callers(name=phar_free_alias, limit=200)` →

```
{
  "name": "phar_free_alias",
  "version": "old",
  "callers": [
    {
      "caller": "phar_parse_pharfile",
      "file": "ext/phar/phar.c",
      "line": 1266
    },
    {
      "caller": "phar_create_or_parse_filename",
      "file": "ext/phar/phar.c",
      "line": 1465
    },
    {
      "caller": "PHP_METHOD(Phar, setAlias)",
      "file": "ext/phar/phar_object.c",
      "line": 2708
    },
    {
      "caller": "phar_parse_tarfile",
      "file": "ext/phar/tar.c",
      "line": 666
    },
    {
      "caller": "phar_parse_tarfile",
      "file": "ext/phar/tar.c",
      "line": 681
    },
    {
      "caller": "phar_get_archive",
      "file": "ext/phar/util.c",
      "line": 1006
    },
    {
      "caller": "phar_parse_zipfile",
      "file": "ext/phar/zip.c",
      "line": 743
    },
    {
      "caller": "phar_parse_zipfile",
      "file": "ext/phar/zip.c",
      "line": 765
    }
  ]
}
```

### Turn 2  _(tok 3741+517, stop=tool_use)_

**Reasoning:** I'm checking why the tool reported version "old" when no rev was passed, since the default should have been the server's commit or HEAD. It seems the rev fell back to the parent of HEAD, which doesn't match what I expected. I'm wondering whether I should inspect the working tree version before the function signature changes.

I'm going to check the version directly by resolving the symbol against the working tree and rerunning the neighborhood lookup for phar_free_alias. I also want to expand the function, since the caller list might miss references made through macros or function pointers.



- `get_neighborhood(name=phar_free_alias, rev=HEAD)` →

```
phar_free_alias — ext/phar/util.c:932 [function] zend_result phar_free_alias(phar_archive_data *phar, char *alias, size_t alias_len) /*
  reads: phar; writes: -; returns: return FAILURE; | return FAILURE; | return SUCCESS;

CALLEES (2):
  zend_hash_str_del (Zend/zend_hash.c:1676): reads ht, len, str; writes -; returns return SUCCESS; | return FAILURE;
  not defined in this repository: PHAR_G

CALLERS (8):
  phar_parse_pharfile (ext/phar/phar.c:1266): if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
  phar_create_or_parse_filename (ext/phar/phar.c:1465): if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
  PHP_METHOD(Phar, setAlias) (ext/phar/phar_object.c:2708): if (SUCCESS != phar_free_alias(fd_ptr, ZSTR_VAL(new_alias), ZSTR_LEN(new_alias))) {
  phar_parse_tarfile (ext/phar/tar.c:666): if (SUCCESS != phar_free_alias(fd_ptr, actual_alias, myphar->alias_len)) {
  phar_parse_tarfile (ext/phar/tar.c:681): if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
  phar_get_archive (ext/phar/util.c:1006): if (SUCCESS == phar_free_alias(fd_ptr, alias, alias_len)) {
  phar_parse_zipfile (ext/phar/zip.c:743): if (SUCCESS != phar_free_alias(fd_ptr, actual_alias, mydata->alias_len)) {
  phar_parse_zipfile (ext/phar/zip.c:765): if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
  ... only the first 8 of 9 reference sites were followed
```

- `get_callers(name=phar_free_alias, limit=200, version=work)` →

```
{
  "name": "phar_free_alias",
  "version": "old",
  "callers": [
    {
      "caller": "phar_parse_pharfile",
      "file": "ext/phar/phar.c",
      "line": 1266
    },
    {
      "caller": "phar_create_or_parse_filename",
      "file": "ext/phar/phar.c",
      "line": 1465
    },
    {
      "caller": "PHP_METHOD(Phar, setAlias)",
      "file": "ext/phar/phar_object.c",
      "line": 2708
    },
    {
      "caller": "phar_parse_tarfile",
      "file": "ext/phar/tar.c",
      "line": 666
    },
    {
      "caller": "phar_parse_tarfile",
      "file": "ext/phar/tar.c",
      "line": 681
    },
    {
      "caller": "phar_get_archive",
      "file": "ext/phar/util.c",
      "line": 1006
    },
    {
      "caller": "phar_parse_zipfile",
      "file": "ext/phar/zip.c",
      "line": 743
    },
    {
      "caller": "phar_parse_zipfile",
      "file": "ext/phar/zip.c",
      "line": 765
    }
  ]
}
```

### Turn 3  _(tok 5493+478, stop=tool_use)_

**Reasoning:** I count nine reference sites nearby but only eight show up in the callers list, so one is missing. My guess is it duplicates a file that already appears, since a couple of the functions have two call sites each. Let me check whether it's in a different file, possibly the phar object or header code, and whether expanding the function view turns up the rest.

I'm thinking the ninth site could be a third call inside one of the functions that already shows up, like phar_parse_tarfile. Or the count might include the definition itself. I'll check the source of the callers, starting with phar_parse_pharfile and phar_create_or_parse_filename, and try expanding phar_free_alias to see whether it lists more.



- `expand_function(name=phar_free_alias, levels=1)` →

```
{
  "name": "phar_free_alias",
  "version": "old",
  "levels": 1,
  "node": {
    "name": "phar_free_alias",
    "file": "ext/phar/util.c",
    "line": 932,
    "kind": "function",
    "state": "analyzed"
  },
  "callees": [
    {
      "name": "zend_hash_str_del",
      "file": "Zend/zend_hash.c",
      "line": 1676,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        939
      ]
    }
  ],
  "callers": [
    {
      "name": "phar_parse_pharfile",
      "file": "ext/phar/phar.c",
      "line": 725,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1266
      ]
    },
    {
      "name": "phar_create_or_parse_filename",
      "file": "ext/phar/phar.c",
      "line": 1370,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1465
      ]
    },
    {
      "name": "PHP_METHOD(Phar, setAlias)",
      "file": "ext/phar/phar_object.c",
      "line": 2669,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        2708
      ]
    },
    {
      "name": "phar_parse_tarfile",
      "file": "ext/phar/tar.c",
      "line": 200,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        666,
        681
      ]
    },
    {
      "name": "phar_get_archive",
      "file": "ext/phar/util.c",
      "line": 955,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1006
      ]
    },
    {
      "name": "phar_parse_zipfile",
      "file": "ext/phar/zip.c",
      "line": 227,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        743,
        765
      ]
    }
  ]
}
```

- `get_context_at(file=ext/phar/zip.c, line=765)` →

```
phar_parse_zipfile — ext/phar/zip.c:227 [function] zend_result phar_parse_zipfile(php_stream *fp, char *fname, size_t fname_len, char *alias, size_t alias_len, phar_archive_data** pphar, char **error) /*
  reads: alias, alias_len, error, fname, fname_len, fp, pphar; writes: fp*, pphar*; returns: return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE;

SLICE around line 765 (def-use, level 2; '>' marks the seed):
zend_result phar_parse_zipfile(php_stream *fp, char *fname, size_t fname_len, char *alias, size_t alias_len, phar_archive_data** pphar, char **error) /* {
   ...
   phar_archive_data *mydata = NULL;
   ...
   mydata = pecalloc(1, sizeof(phar_archive_data), PHAR_G(persist));
   mydata->is_persistent = PHAR_G(persist);
   ...
   mydata->fname = pestrndup(fname, fname_len, mydata->is_persistent);
   ...
   for(i = 0; i < PHAR_GET_16(locator.count); ++i) {
   ...
     if(!actual_alias && zend_string_equals_literal(entry.filename, ".phar/alias.txt")) {
   ...
       if(entry.flags & PHAR_ENT_COMPRESSED_GZ) {
   ...
       } else if(entry.flags & PHAR_ENT_COMPRESSED_BZ2) {
   ...
           zend_string *str = php_stream_copy_to_mem(fp, entry.uncompressed_filesize, 0);
           if(str) {
   ...
             actual_alias = estrndup(ZSTR_VAL(str), ZSTR_LEN(str));
   ...
           } else {
             actual_alias = NULL;
   ...
           }
       } else {
           zend_string *str = php_stream_copy_to_mem(fp, entry.uncompressed_filesize, 0);
           if(str) {
   ...
             actual_alias = estrndup(ZSTR_VAL(str), ZSTR_LEN(str));
   ...
           } else {
             actual_alias = NULL;
   ...
           }
       }
     }
   }
   ...
   if(actual_alias) {
   ...
   } else {
     phar_archive_data *fd_ptr;
     if(alias_len) {
       if(NULL !=(fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
>        if(SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
           if(error) {
   ...
           }
           zend_hash_str_del(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len);
           return FAILURE;
   ...
         }
       }
     }
   }
}

CALLEES (50):
  phar_find_eocd (ext/phar/zip.c:195): reads n, s; writes -; returns return NULL; | return(char *)eocd_start; | return NULL;
  phar_parse_metadata_lazy (ext/phar/phar.c:694): reads buffer, persistent, tracker, zip_metadata_len; writes tracker*; returns -
  zend_hash_add_mem (Zend/zend_hash.h:741): reads ht, key, pData, size; writes -; returns return Z_PTR_P(zv); | return NULL;
  phar_set_inode (ext/phar/phar_internal.h:381): reads entry; writes entry*; returns -
  zend_string_release_ex (Zend/zend_string.h:343): reads persistent, s; writes -; returns -
  php_stream_filter_remove (main/streams/filter.c:487): reads call_dtor, filter; writes -; returns return NULL; | return filter;
  php_stream_filter_create (main/streams/filter.c:217): reads filtername, filterparams, persistent; writes -; returns return filter;
  phar_zip_process_extra (ext/phar/zip.c:42): reads entry, fp, len; writes entry*; returns return FAILURE; | return FAILURE; | return FAILURE; | return SUCCESS;
  phar_add_virtual_dirs (ext/phar/util.c:1962): reads filename, filename_len, phar; writes phar*; returns -
  phar_verify_signature (ext/phar/util.c:1476): reads end_of_phar, error, fname, fp, sig, sig_len, sig_type, signature, signature_len; writes error*, signature_len*; returns return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE;
  zend_string_free (Zend/zend_string.h:318): reads s; writes -; returns -
  zend_string_alloc (Zend/zend_string.h:164): reads len, persistent; writes -; returns return ret;
  phar_zip_d2u_time (ext/phar/zip.c:153): reads cddate, cdtime; writes -; returns return mktime(tm);
  zend_hash_str_exists (Zend/zend_hash.h:240): reads ht, len, str; writes -; returns return zend_hash_str_find(ht, str, len)!= NULL;
  zend_hash_str_add_ptr (Zend/zend_hash.h:693): reads ht, len, pData, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  zend_hash_str_del (Zend/zend_hash.c:1676): reads ht, len, str; writes -; returns return SUCCESS; | return FAILURE;
  phar_free_alias (ext/phar/util.c:932): reads phar; writes -; returns return FAILURE; | return FAILURE; | return SUCCESS;
  zend_hash_str_find_ptr (Zend/zend_hash.h:915): reads ht, len, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  phar_validate_alias (ext/phar/phar_internal.h:374): reads alias, alias_len; writes -; returns return !(memchr(alias, '/', alias_len)|| memchr(alias, '\\', alias_len)|| memchr(alias, ':', alias_len)|| memchr(alias, ';', alias_len)|| memchr(alias, '\n', alias_len)|| memchr(alias, '\r', alias_len));
  php_stream_tell [macro]: #define php_stream_tell(stream) _php_stream_tell((stream))
  php_stream_seek [macro]: #define php_stream_seek(stream, offset, whence) _php_stream_seek((stream), (offset), (whence))
  spprintf [macro]: #define spprintf zend_spprintf
  php_stream_close [macro]: #define php_stream_close(stream) _php_stream_free((stream), PHP_STREAM_FREE_CLOSE)
  php_stream_read [macro]: #define php_stream_read(stream, buf, count) _php_stream_read((stream), (buf), (count))
  PHAR_GET_16 [macro]: #define PHAR_GET_16(var) ((uint16_t)((((uint16_t)var[0]) & 0xff) | \
  pecalloc [macro]: #define pecalloc(nmemb, size, persistent) ((persistent)?__zend_calloc((nmemb), (size) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC):ecalloc((nmemb), (size)))
  ZVAL_UNDEF [macro]: #define ZVAL_UNDEF(z) do { \
  pefree [macro (1 of 2 definitions)]: #define pefree(ptr, persistent) ((persistent)?free(ptr):efree(ptr))
  pestrndup [macro]: #define pestrndup(s, length, persistent) ((persistent)?zend_strndup((s),(length)):estrndup((s),(length)))
  PHAR_GET_32 [macro (1 of 5 definitions)]: # define PHAR_GET_32(buffer, var) \
  not defined in this repository: PHAR_G, phar_unixify_path_separators, strrchr, memchr
  not shown (16): zend_hash_init, PHAR_ZIP_FAIL, estrndup, ZSTR_LEN, ZSTR_VAL, php_stream_copy_to_mem, php_stream_filter_flush, php_stream_filter_append, php_stream_is_persistent, ZEND_ASSERT, zend_string_equals_literal, efree, emalloc, php_stream_write, php_stream_copy_to_stream_ex, php_stream_fopen_tmpfile

CALLERS (1):
  phar_open_from_fp (ext/phar/phar.c:1716): return phar_parse_zipfile(fp, fname, fname_len, alias, alias_len, pphar, error);
```

### Turn 4  _(tok 9871+891, stop=tool_use)_

**Reasoning:** I'm checking the 9th reference, which could be phar_parse_tarfile at 681 or some other site. The list shows eight sites so far, so the missing one might be a recursive call, a function-pointer use, or a caller in a file that isn't indexed. I can't confirm which without grepping.

I'm going to check the callers of phar_parse_tarfile and the other functions, and look at the zip one too, because my count of call sites adds up to 8 across six functions while the neighborhood says 9. That leaves one reference unaccounted for, possibly a second call in the same function or something indirect like a macro.

I'm going to pull the full source of phar_parse_pharfile, PHP_METHOD(Phar, setAlias), and phar_get_archive instead of slicing them, since slicing might drop the call I'm missing.



- `get_function_source(name=phar_parse_pharfile)` →

```
phar_parse_pharfile (function, old version) — ext/phar/phar.c:725-1298
  725| static zend_result phar_parse_pharfile(php_stream *fp, char *fname, size_t fname_len, char *alias, size_t alias_len, zend_long halt_offset, phar_archive_data** pphar, uint32_t compression, char **error) /* {{{ */
  726| {
  727| 	char b32[4], *buffer, *endbuffer, *savebuf;
  728| 	phar_archive_data *mydata = NULL;
  729| 	phar_entry_info entry;
  730| 	uint32_t manifest_len, manifest_count, manifest_flags, manifest_index, tmp_len, sig_flags;
  731| 	uint16_t manifest_ver;
  732| 	uint32_t len;
  733| 	zend_long offset;
  734| 	size_t sig_len;
  735| 	bool register_alias = false, temp_alias = false;
  736| 	char *signature = NULL;
  737| 	zend_string *str;
  738| 
  739| 	if (pphar) {
  740| 		*pphar = NULL;
  741| 	}
  742| 
  743| 	if (error) {
  744| 		*error = NULL;
  745| 	}
  746| 
  747| 	/* check for ?>\n and increment accordingly */
  748| 	if (-1 == php_stream_seek(fp, halt_offset, SEEK_SET)) {
  749| 		MAPPHAR_ALLOC_FAIL("cannot seek to __HALT_COMPILER(); location in phar \"%s\"")
  750| 	}
  751| 
  752| 	buffer = b32;
  753| 
  754| 	if (3 != php_stream_read(fp, buffer, 3)) {
  755| 		MAPPHAR_ALLOC_FAIL("internal corruption of phar \"%s\" (truncated manifest at stub end)")
  756| 	}
  757| 
  758| 	if ((*buffer == ' ' || *buffer == '\n') && *(buffer + 1) == '?' && *(buffer + 2) == '>') {
  759| 		int nextchar;
  760| 		halt_offset += 3;
  761| 		if (EOF == (nextchar = php_stream_getc(fp))) {
  762| 			MAPPHAR_ALLOC_FAIL("internal corruption of phar \"%s\" (truncated manifest at stub end)")
  763| 		}
  764| 
  765| 		if ((char) nextchar == '\r') {
  766| 			/* if we have an \r we require an \n as well */
  767| 			if (EOF == (nextchar = php_stream_getc(fp)) || (char)nextchar != '\n') {
  768| 				MAPPHAR_ALLOC_FAIL("internal corruption of phar \"%s\" (truncated manifest at stub end)")
  769| 			}
  770| 			++halt_offset;
  771| 		}
  772| 
  773| 		if ((char) nextchar == '\n') {
  774| 			++halt_offset;
  775| 		}
  776| 	}
  777| 
  778| 	/* make sure we are at the right location to read the manifest */
  779| 	if (-1 == php_stream_seek(fp, halt_offset, SEEK_SET)) {
  780| 		MAPPHAR_ALLOC_FAIL("cannot seek to __HALT_COMPILER(); location in phar \"%s\"")
  781| 	}
  782| 
  783| 	/* read in manifest */
  784| 	buffer = b32;
  785| 
  786| 	if (4 != php_stream_read(fp, buffer, 4)) {
  787| 		MAPPHAR_ALLOC_FAIL("internal corruption of phar \"%s\" (truncated manifest at manifest length)")
  788| 	}
  789| 
  790| 	PHAR_GET_32(buffer, manifest_len);
  791| 
  792| 	if (manifest_len > 1048576 * 100) {
  793| 		/* prevent serious memory issues by limiting manifest to at most 100 MB in length */
  794| 		MAPPHAR_ALLOC_FAIL("manifest cannot be larger than 100 MB in phar \"%s\"")
  795| 	}
  796| 
  797| 	buffer = (char *)emalloc(manifest_len);
  798| 	savebuf = buffer;
  799| 	endbuffer = buffer + manifest_len;
  800| 
  801| 	if (manifest_len < MANIFEST_FIXED_LEN || manifest_len != php_stream_read(fp, buffer, manifest_len)) {
  802| 		MAPPHAR_FAIL("internal corruption of phar \"%s\" (truncated manifest header)")
  803| 	}
  804| 
  805| 	/* extract the number of entries */
  806| 	SAFE_PHAR_GET_32(buffer, endbuffer, manifest_count);
  807| 
  808| 	if (manifest_count == 0) {
  809| 		MAPPHAR_FAIL("in phar \"%s\", manifest claims to have zero entries.  Phars must have at least 1 entry");
  810| 	}
  811| 
  812| 	/* extract API version, lowest nibble currently unused */
  813| 	manifest_ver = (((unsigned char)buffer[0]) << 8)
  814| 				 + ((unsigned char)buffer[1]);
  815| 	buffer += 2;
  816| 
  817| 	if ((manifest_ver & PHAR_API_VER_MASK) < PHAR_API_MIN_READ) {
  818| 		efree(savebuf);
  819| 		php_stream_close(fp);
  820| 		if (error) {
  821| 			spprintf(error, 0, "phar \"%s\" is API version %1.u.%1.u.%1.u, and cannot be processed", fname, manifest_ver >> 12, (manifest_ver >> 8) & 0xF, (manifest_ver >> 4) & 0x0F);
  822| 		}
  823| 		return FAILURE;
  824| 	}
  825| 
  826| 	SAFE_PHAR_GET_32(buffer, endbuffer, manifest_flags);
  827| 
  828| 	manifest_flags &= ~PHAR_HDR_COMPRESSION_MASK;
  829| 	manifest_flags &= ~PHAR_FILE_COMPRESSION_MASK;
  830| 	/* remember whether this entire phar was compressed with gz/bzip2 */
  831| 	manifest_flags |= compression;
  832| 
  833| 	/* The lowest nibble contains the phar wide flags. The compression flags can */
  834| 	/* be ignored on reading because it is being generated anyways. */
  835| 	if (manifest_flags & PHAR_HDR_SIGNATURE) {
  836| 		char sig_buf[8], *sig_ptr = sig_buf;
  837| 		zend_off_t read_len;
  838| 		size_t end_of_phar;
  839| 
  840| 		if (-1 == php_stream_seek(fp, -8, SEEK_END)
  841| 		|| (read_len = php_stream_tell(fp)) < 20
  842| 		|| 8 != php_stream_read(fp, sig_buf, 8)
  843| 		|| memcmp(sig_buf+4, "GBMB", 4)) {
  844| 			efree(savebuf);
  845| 			php_stream_close(fp);
  846| 			if (error) {
  847| 				spprintf(error, 0, "phar \"%s\" has a broken signature", fname);
  848| 			}
  849| 			return FAILURE;
  850| 		}
  851| 
  852| 		PHAR_GET_32(sig_ptr, sig_flags);
  853| 
  854| 		switch(sig_flags) {
  855| 			case PHAR_SIG_OPENSSL_SHA512:
  856| 			case PHAR_SIG_OPENSSL_SHA256:
  857| 			case PHAR_SIG_OPENSSL: {
  858| 				uint32_t signature_len;
  859| 				char *sig;
  860| 				zend_off_t whence;
  861| 
  862| 				/* we store the signature followed by the signature length */
  863| 				if (-1 == php_stream_seek(fp, -12, SEEK_CUR)
  864| 				|| 4 != php_stream_read(fp, sig_buf, 4)) {
  865| 					efree(savebuf);
  866| 					php_stream_close(fp);
  867| 					if (error) {
  868| 						spprintf(error, 0, "phar \"%s\" openssl signature length could not be read", fname);
  869| 					}
  870| 					return FAILURE;
  871| 				}
  872| 
  873| 				sig_ptr = sig_buf;
  874| 				PHAR_GET_32(sig_ptr, signature_len);
  875| 				sig = (char *) emalloc(signature_len);
  876| 				whence = signature_len + 4;
  877| 				whence = -whence;
  878| 
  879| 				if (-1 == php_stream_seek(fp, whence, SEEK_CUR)
  880| 				|| !(end_of_phar = php_stream_tell(fp))
  881| 				|| signature_len != php_stream_read(fp, sig, signature_len)) {
  882| 					efree(savebuf);
  883| 					efree(sig);
  884| 					php_stream_close(fp);
  885| 					if (error) {
  886| 						spprintf(error, 0, "phar \"%s\" openssl signature could not be read", fname);
  887| 					}
  888| 					return FAILURE;
  889| 				}
  890| 
  891| 				if (FAILURE == phar_verify_signature(fp, end_of_phar, sig_flags, sig, signature_len, fname, &signature, &sig_len, error)) {
  892| 					efree(savebuf);
  893| 					efree(sig);
  894| 					php_stream_close(fp);
  895| 					if (error) {
  896| 						char *save = *error;
  897| 						spprintf(error, 0, "phar \"%s\" openssl signature could not be verified: %s", fname, *error);
  898| 						efree(save);
  899| 					}
  900| 					return FAILURE;
  901| 				}
  902| 				efree(sig);
  903| 			}
  904| 			break;
  905| 			case PHAR_SIG_SHA512: {
  906| 				unsigned char digest[64];
  907| 
  908| 				php_stream_seek(fp, -(8 + 64), SEEK_END);
  909| 				read_len = php_stream_tell(fp);
  910| 
  911| 				if (php_stream_read(fp, (char*)digest, sizeof(digest)) != sizeof(digest)) {
  912| 					efree(savebuf);
  913| 					php_stream_close(fp);
  914| 					if (error) {
  915| 						spprintf(error, 0, "phar \"%s\" has a broken signature", fname);
  916| 					}
  917| 					return FAILURE;
  918| 				}
  919| 
  920| 				if (FAILURE == phar_verify_signature(fp, read_len, PHAR_SIG_SHA512, (char *)digest, 64, fname, &signature, &sig_len, error)) {
  921| 					efree(savebuf);
  922| 					php_stream_close(fp);
  923| 					if (error) {
  924| 						char *save = *error;
  925| 						spprintf(error, 0, "phar \"%s\" SHA512 signature could not be verified: %s", fname, *error);
  926| 						efree(save);
  927| 					}
  928| 					return FAILURE;
  929| 				}
  930| 				break;
  931| 			}
  932| 			case PHAR_SIG_SHA256: {
  933| 				unsigned char digest[32];
  934| 
  935| 				php_stream_seek(fp, -(8 + 32), SEEK_END);
  936| 				read_len = php_stream_tell(fp);
  937| 
  938| 				if (php_stream_read(fp, (char*)digest, sizeof(digest)) != sizeof(digest)) {
  939| 					efree(savebuf);
  940| 					php_stream_close(fp);
  941| 					if (error) {
  942| 						spprintf(error, 0, "phar \"%s\" has a broken signature", fname);
  943| 					}
  944| 					return FAILURE;
  945| 				}
  946| 
  947| 				if (FAILURE == phar_verify_signature(fp, read_len, PHAR_SIG_SHA256, (char *)digest, 32, fname, &signature, &sig_len, error)) {
  948| 					efree(savebuf);
  949| 					php_stream_close(fp);
  950| 					if (error) {
  951| 						char *save = *error;
  952| 						spprintf(error, 0, "phar \"%s\" SHA256 signature could not be verified: %s", fname, *error);
  953| 						efree(save);
  954| 					}
  955| 					return FAILURE;
  956| 				}
  957| 				break;
  958| 			}
  959| 			case PHAR_SIG_SHA1: {
  960| 				unsigned char digest[20];
  961| 
  962| 				php_stream_seek(fp, -(8 + 20), SEEK_END);
  963| 				read_len = php_stream_tell(fp);
  964| 
  965| 				if (php_stream_read(fp, (char*)digest, sizeof(digest)) != sizeof(digest)) {
  966| 					efree(savebuf);
  967| 					php_stream_close(fp);
  968| 					if (error) {
  969| 						spprintf(error, 0, "phar \"%s\" has a broken signature", fname);
  970| 					}
  971| 					return FAILURE;
  972| 				}
  973| 
  974| 				if (FAILURE == phar_verify_signature(fp, read_len, PHAR_SIG_SHA1, (char *)digest, 20, fname, &signature, &sig_len, error)) {
  975| 					efree(savebuf);
  976| 					php_stream_close(fp);
  977| 					if (error) {
  978| 						char *save = *error;
  979| 						spprintf(error, 0, "phar \"%s\" SHA1 signature could not be verified: %s", fname, *error);
  980| 						efree(save);
  981| 					}
  982| 					return FAILURE;
  983| 				}
  984| 				break;
  985| 			}
  986| 			case PHAR_SIG_MD5: {
  987| 				unsigned char digest[16];
  988| 
  989| 				php_stream_seek(fp, -(8 + 16), SEEK_END);
  990| 				read_len = php_stream_tell(fp);
  991| 
  992| 				if (php_stream_read(fp, (char*)digest, sizeof(digest)) != sizeof(digest)) {
  993| 					efree(savebuf);
  994| 					php_stream_close(fp);
  995| 					if (error) {
  996| 						spprintf(error, 0, "phar \"%s\" has a broken signature", fname);
  997| 					}
  998| 					return FAILURE;
  999| 				}
 1000| 
 1001| 				if (FAILURE == phar_verify_signature(fp, read_len, PHAR_SIG_MD5, (char *)digest, 16, fname, &signature, &sig_len, error)) {
 1002| 					efree(savebuf);
 1003| 					php_stream_close(fp);
 1004| 					if (error) {
 1005| 						char *save = *error;
 1006| 						spprintf(error, 0, "phar \"%s\" MD5 signature could not be verified: %s", fname, *error);
 1007| 						efree(save);
 1008| 					}
 1009| 					return FAILURE;
 1010| 				}
 1011| 				break;
 1012| 			}
 1013| 			default:
 1014| 				efree(savebuf);
 1015| 				php_stream_close(fp);
 1016| 
 1017| 				if (error) {
 1018| 					spprintf(error, 0, "phar \"%s\" has a broken or unsupported signature", fname);
 1019| 				}
 1020| 				return FAILURE;
 1021| 		}
 1022| 	} else if (PHAR_G(require_hash)) {
 1023| 		efree(savebuf);
 1024| 		php_stream_close(fp);
 1025| 
 1026| 		if (error) {
 1027| 			spprintf(error, 0, "phar \"%s\" does not have a signature", fname);
 1028| 		}
 1029| 		return FAILURE;
 1030| 	} else {
 1031| 		sig_flags = 0;
 1032| 		sig_len = 0;
 1033| 	}
 1034| 
 1035| 	/* extract alias */
 1036| 	SAFE_PHAR_GET_32(buffer, endbuffer, tmp_len);
 1037| 
 1038| 	if (buffer + tmp_len > endbuffer) {
 1039| 		MAPPHAR_FAIL("internal corruption of phar \"%s\" (buffer overrun)");
 1040| 	}
 1041| 
 1042| 	if (manifest_len < MANIFEST_FIXED_LEN + tmp_len) {
 1043| 		MAPPHAR_FAIL("internal corruption of phar \"%s\" (truncated manifest header)")
 1044| 	}
 1045| 
 1046| 	/* tmp_len = 0 says alias length is 0, which means the alias is not stored in the phar */
 1047| 	if (tmp_len) {
 1048| 		/* if the alias is stored we enforce it (implicit overrides explicit) */
 1049| 		if (alias && alias_len && (alias_len != tmp_len || strncmp(alias, buffer, tmp_len)))
 1050| 		{
 1051| 			php_stream_close(fp);
 1052| 
 1053| 			if (signature) {
 1054| 				efree(signature);
 1055| 			}
 1056| 
 1057| 			if (error) {
 1058| 				spprintf(error, 0, "cannot load phar \"%s\" with implicit alias \"%.*s\" under different alias \"%s\"", fname, tmp_len, buffer, alias);
 1059| 			}
 1060| 
 1061| 			efree(savebuf);
 1062| 			return FAILURE;
 1063| 		}
 1064| 
 1065| 		alias_len = tmp_len;
 1066| 		alias = buffer;
 1067| 		buffer += tmp_len;
 1068| 		register_alias = true;
 1069| 	} else if (!alias_len || !alias) {
 1070| 		/* if we neither have an explicit nor an implicit alias, we use the filename */
 1071| 		alias = NULL;
 1072| 		alias_len = 0;
 1073| 		register_alias = false;
 1074| 	} else if (alias_len) {
 1075| 		register_alias = true;
 1076| 		temp_alias = true;
 1077| 	}
 1078| 
 1079| 	/* we have 5 32-bit items plus 1 byte at least */
 1080| 	if (manifest_count > ((manifest_len - MANIFEST_FIXED_LEN - tmp_len) / (5 * 4 + 1))) {
 1081| 		/* prevent serious memory issues */
 1082| 		MAPPHAR_FAIL("internal corruption of phar \"%s\" (too many manifest entries for size of manifest)")
 1083| 	}
 1084| 
 1085| 	mydata = pecalloc(1, sizeof(phar_archive_data), PHAR_G(persist));
 1086| 	mydata->is_persistent = PHAR_G(persist);
 1087| 	HT_INVALIDATE(&mydata->manifest);
 1088| 	HT_INVALIDATE(&mydata->mounted_dirs);
 1089| 	HT_INVALIDATE(&mydata->virtual_dirs);
 1090| 
 1091| 	/* check whether we have meta data, zero check works regardless of byte order */
 1092| 	SAFE_PHAR_GET_32(buffer, endbuffer, len);
 1093| 	if (mydata->is_persistent) {
 1094| 		if (!len) {
 1095| 			/* FIXME: not sure why this is needed but removing it breaks tests */
 1096| 			SAFE_PHAR_GET_32(buffer, endbuffer, len);
 1097| 		}
 1098| 	}
 1099| 	if(len > (size_t)(endbuffer - buffer)) {
 1100| 		MAPPHAR_FAIL("internal corruption of phar \"%s\" (trying to read past buffer end)");
 1101| 	}
 1102| 	/* Don't implicitly call unserialize() on potentially untrusted input unless getMetadata() is called directly. */
 1103| 	phar_parse_metadata_lazy(buffer, &mydata->metadata_tracker, len, mydata->is_persistent);
 1104| 	buffer += len;
 1105| 
 1106| 	/* set up our manifest */
 1107| 	zend_hash_init(&mydata->manifest, manifest_count,
 1108| 		zend_get_hash_value, destroy_phar_manifest_entry, mydata->is_persistent);
 1109| 	zend_hash_init(&mydata->mounted_dirs, 5,
 1110| 		zend_get_hash_value, NULL, mydata->is_persistent);
 1111| 	zend_hash_init(&mydata->virtual_dirs, manifest_count * 2,
 1112| 		zend_get_hash_value, NULL, mydata->is_persistent);
 1113| 	mydata->fname = pestrndup(fname, fname_len, mydata->is_persistent);
 1114| #ifdef PHP_WIN32
 1115| 	phar_unixify_path_separators(mydata->fname, fname_len);
 1116| #endif
 1117| 	mydata->fname_len = fname_len;
 1118| 	offset = halt_offset + manifest_len + 4;
 1119| 	memset(&entry, 0, sizeof(phar_entry_info));
 1120| 	entry.phar = mydata;
 1121| 	entry.fp_type = PHAR_FP;
 1122| 	entry.is_persistent = mydata->is_persistent;
 1123| 
 1124| 	for (manifest_index = 0; manifest_index < manifest_count; ++manifest_index) {
 1125| 		if (buffer + 28 > endbuffer) {
 1126| 			MAPPHAR_FAIL("internal corruption of phar \"%s\" (truncated manifest entry)")
 1127| 		}
 1128| 
 1129| 		uint32_t filename_len;
 1130| 		PHAR_GET_32(buffer, filename_len);
 1131| 
 1132| 		if (filename_len == 0) {
 1133| 			MAPPHAR_FAIL("zero-length filename encountered in phar \"%s\"");
 1134| 		}
 1135| 
 1136| 		if (entry.is_persistent) {
 1137| 			entry.manifest_pos = manifest_index;
 1138| 		}
 1139| 
 1140| 		if (filename_len > (size_t)(endbuffer - buffer - 24)) {
 1141| 			MAPPHAR_FAIL("internal corruption of phar \"%s\" (truncated manifest entry)");
 1142| 		}
 1143| 
 1144| 		if ((manifest_ver & PHAR_API_VER_MASK) >= PHAR_API_MIN_DIR && buffer[filename_len - 1] == '/') {
 1145| 			entry.is_dir = 1;
 1146| 		} else {
 1147| 			entry.is_dir = 0;
 1148| 		}
 1149| 
 1150| 		phar_add_virtual_dirs(mydata, buffer, filename_len);
 1151| 		const char *filename_raw = buffer;
 1152| 		buffer += filename_len;
 1153| 		PHAR_GET_32(buffer, entry.uncompressed_filesize);
 1154| 		PHAR_GET_32(buffer, entry.timestamp);
 1155| 
 1156| 		if (offset == halt_offset + manifest_len + 4
 1157| 		 || mydata->max_timestamp < entry.timestamp) {
 1158| 			mydata->max_timestamp = entry.timestamp;
 1159| 		}
 1160| 
 1161| 		PHAR_GET_32(buffer, entry.compressed_filesize);
 1162| 		PHAR_GET_32(buffer, entry.crc32);
 1163| 		PHAR_GET_32(buffer, entry.flags);
 1164| 
 1165| 		if (entry.is_dir) {
 1166| 			filename_len--;
 1167| 			entry.flags |= PHAR_ENT_PERM_DEF_DIR;
 1168| 		}
 1169| 
 1170| 		entry.filename = zend_string_init(filename_raw, filename_len, entry.is_persistent);
 1171| 		if (entry.is_persistent) {
 1172| 			GC_MAKE_PERSISTENT_LOCAL(entry.filename);
 1173| 		}
 1174| 
 1175| 		PHAR_GET_32(buffer, len);
 1176| 		if (len > (size_t)(endbuffer - buffer)) {
 1177| 			zend_string_free(entry.filename);
 1178| 			MAPPHAR_FAIL("internal corruption of phar \"%s\" (truncated manifest entry)");
 1179| 		}
 1180| 		/* Don't implicitly call unserialize() on potentially untrusted input unless getMetadata() is called directly. */
 1181| 		/* The same local variable entry is reused in a loop, so reset the state before reading data. */
 1182| 		ZVAL_UNDEF(&entry.metadata_tracker.val);
 1183| 		entry.metadata_tracker.str = NULL;
 1184| 		phar_parse_metadata_lazy(buffer, &entry.metadata_tracker, len, entry.is_persistent);
 1185| 		buffer += len;
 1186| 
 1187| 		entry.offset = entry.offset_abs = offset;
 1188| 		offset += entry.compressed_filesize;
 1189| 
 1190| 		switch (entry.flags & PHAR_ENT_COMPRESSION_MASK) {
 1191| 			case PHAR_ENT_COMPRESSED_GZ:
 1192| 				if (!PHAR_G(has_zlib)) {
 1193| 					phar_metadata_tracker_free(&entry.metadata_tracker, entry.is_persistent);
 1194| 					zend_string_free(entry.filename);
 1195| 					MAPPHAR_FAIL("zlib extension is required for gz compressed .phar file \"%s\"");
 1196| 				}
 1197| 				break;
 1198| 			case PHAR_ENT_COMPRESSED_BZ2:
 1199| 				if (!PHAR_G(has_bz2)) {
 1200| 					phar_metadata_tracker_free(&entry.metadata_tracker, entry.is_persistent);
 1201| 					zend_string_free(entry.filename);
 1202| 					MAPPHAR_FAIL("bz2 extension is required for bzip2 compressed .phar file \"%s\"");
 1203| 				}
 1204| 				break;
 1205| 			default:
 1206| 				if (entry.uncompressed_filesize != entry.compressed_filesize) {
 1207| 					phar_metadata_tracker_free(&entry.metadata_tracker, entry.is_persistent);
 1208| 					zend_string_free(entry.filename);
 1209| 					MAPPHAR_FAIL("internal corruption of phar \"%s\" (compressed and uncompressed size does not match for uncompressed entry)");
 1210| 				}
 1211| 				break;
 1212| 		}
 1213| 
 1214| 		manifest_flags |= (entry.flags & PHAR_ENT_COMPRESSION_MASK);
 1215| 		/* if signature matched, no need to check CRC32 for each file */
 1216| 		entry.is_crc_checked = (manifest_flags & PHAR_HDR_SIGNATURE ? 1 : 0);
 1217| 		phar_set_inode(&entry);
 1218| 		if (mydata->is_persistent) {
 1219| 			str = zend_string_init_interned(ZSTR_VAL(entry.filename), ZSTR_LEN(entry.filename), 1);
 1220| 		} else {
 1221| 			str = entry.filename;
 1222| 		}
 1223| 		zend_hash_add_mem(&mydata->manifest, str, (void*)&entry, sizeof(phar_entry_info));
 1224| 		if (mydata->is_persistent) {
 1225| 			zend_string_release(str);
 1226| 		}
 1227| 	}
 1228| 
 1229| 	snprintf(mydata->version, sizeof(mydata->version), "%u.%u.%u", manifest_ver >> 12, (manifest_ver >> 8) & 0xF, (manifest_ver >> 4) & 0xF);
 1230| 	mydata->halt_offset = halt_offset;
 1231| 	mydata->flags = manifest_flags;
 1232| 	endbuffer = strrchr(mydata->fname, '/');
 1233| 
 1234| 	if (endbuffer) {
 1235| 		mydata->ext = memchr(endbuffer, '.', (mydata->fname + fname_len) - endbuffer);
 1236| 		if (mydata->ext == endbuffer) {
 1237| 			mydata->ext = memchr(endbuffer
... [truncated to budget] ...
```

- `get_function_source(name=phar_create_or_parse_filename)` →

```
phar_create_or_parse_filename (function, old version) — ext/phar/phar.c:1370-1497
 1370| ZEND_ATTRIBUTE_NONNULL_ARGS(1, 7, 8) zend_result phar_create_or_parse_filename(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_archive_data** pphar, char **error) /* {{{ */
 1371| {
 1372| 	php_stream *fp;
 1373| 	zend_string *actual = NULL;
 1374| 	char *p;
 1375| 
 1376| 	if (php_check_open_basedir(fname)) {
 1377| 		return FAILURE;
 1378| 	}
 1379| 
 1380| 	/* first open readonly so it won't be created if not present */
 1381| 	fp = php_stream_open_wrapper(fname, "rb", IGNORE_URL|STREAM_MUST_SEEK|0, &actual);
 1382| 
 1383| 	if (actual) {
 1384| 		fname = ZSTR_VAL(actual);
 1385| 		fname_len = ZSTR_LEN(actual);
 1386| 	}
 1387| 
 1388| 	if (fp) {
 1389| 		if (phar_open_from_fp(fp, fname, fname_len, alias, alias_len, options, pphar, error) == SUCCESS) {
 1390| 			if ((*pphar)->is_data || !PHAR_G(readonly)) {
 1391| 				(*pphar)->is_writeable = 1;
 1392| 			}
 1393| 			if (actual) {
 1394| 				zend_string_release_ex(actual, 0);
 1395| 			}
 1396| 			return SUCCESS;
 1397| 		} else {
 1398| 			/* file exists, but is either corrupt or not a phar archive */
 1399| 			if (actual) {
 1400| 				zend_string_release_ex(actual, 0);
 1401| 			}
 1402| 			return FAILURE;
 1403| 		}
 1404| 	}
 1405| 
 1406| 	if (actual) {
 1407| 		zend_string_release_ex(actual, 0);
 1408| 	}
 1409| 
 1410| 	if (PHAR_G(readonly) && !is_data) {
 1411| 		if (options & REPORT_ERRORS) {
 1412| 			spprintf(error, 0, "creating archive \"%s\" disabled by the php.ini setting phar.readonly", fname);
 1413| 		}
 1414| 		return FAILURE;
 1415| 	}
 1416| 
 1417| 	/* set up our manifest */
 1418| 	phar_archive_data *mydata = ecalloc(1, sizeof(phar_archive_data));
 1419| 	mydata->fname = expand_filepath(fname, NULL);
 1420| 	if (mydata->fname == NULL) {
 1421| 		efree(mydata);
 1422| 		return FAILURE;
 1423| 	}
 1424| 	fname_len = strlen(mydata->fname);
 1425| #ifdef PHP_WIN32
 1426| 	phar_unixify_path_separators(mydata->fname, fname_len);
 1427| #endif
 1428| 	p = strrchr(mydata->fname, '/');
 1429| 
 1430| 	if (p) {
 1431| 		mydata->ext = memchr(p, '.', (mydata->fname + fname_len) - p);
 1432| 		if (mydata->ext == p) {
 1433| 			mydata->ext = memchr(p + 1, '.', (mydata->fname + fname_len) - p - 1);
 1434| 		}
 1435| 		if (mydata->ext) {
 1436| 			mydata->ext_len = (mydata->fname + fname_len) - mydata->ext;
 1437| 		}
 1438| 	}
 1439| 
 1440| 	zend_hash_init(&mydata->manifest, sizeof(phar_entry_info),
 1441| 		zend_get_hash_value, destroy_phar_manifest_entry, 0);
 1442| 	zend_hash_init(&mydata->mounted_dirs, sizeof(char *),
 1443| 		zend_get_hash_value, NULL, 0);
 1444| 	zend_hash_init(&mydata->virtual_dirs, sizeof(char *),
 1445| 		zend_get_hash_value, NULL, mydata->is_persistent);
 1446| 	mydata->fname_len = fname_len;
 1447| 	snprintf(mydata->version, sizeof(mydata->version), "%s", PHP_PHAR_API_VERSION);
 1448| 	mydata->is_temporary_alias = alias ? 0 : 1;
 1449| 	mydata->fp = NULL;
 1450| 	mydata->is_writeable = 1;
 1451| 	mydata->is_brandnew = 1;
 1452| 	phar_request_initialize();
 1453| 	zend_hash_str_add_ptr(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len, mydata);
 1454| 
 1455| 	if (is_data) {
 1456| 		alias = NULL;
 1457| 		alias_len = 0;
 1458| 		mydata->is_data = 1;
 1459| 		/* assume tar format, PharData can specify other */
 1460| 		mydata->is_tar = 1;
 1461| 	} else {
 1462| 		phar_archive_data *fd_ptr;
 1463| 
 1464| 		if (alias && NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
 1465| 			if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
 1466| 				spprintf(error, 4096, "phar error: phar \"%s\" cannot set alias \"%s\", already in use by another phar archive", mydata->fname, alias);
 1467| 
 1468| 				zend_hash_str_del(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len);
 1469| 
 1470| 				*pphar = NULL;
 1471| 
 1472| 				return FAILURE;
 1473| 			}
 1474| 		}
 1475| 
 1476| 		ZEND_ASSERT(!mydata->is_persistent);
 1477| 		mydata->alias = alias ? estrndup(alias, alias_len) : estrndup(mydata->fname, fname_len);
 1478| 		mydata->alias_len = alias ? alias_len : fname_len;
 1479| 	}
 1480| 
 1481| 	if (alias_len && alias) {
 1482| 		if (NULL == zend_hash_str_add_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len, mydata)) {
 1483| 			if (options & REPORT_ERRORS) {
 1484| 				spprintf(error, 0, "archive \"%s\" cannot be associated with alias \"%s\", already in use", fname, alias);
 1485| 			}
 1486| 
 1487| 			zend_hash_str_del(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len);
 1488| 
 1489| 			*pphar = NULL;
 1490| 
 1491| 			return FAILURE;
 1492| 		}
 1493| 	}
 1494| 
 1495| 	*pphar = mydata;
 1496| 	return SUCCESS;
 1497| }
```

- `get_function_source(name=phar_get_archive)` →

```
phar_get_archive (function, old version) — ext/phar/util.c:955-1153
  955| zend_result phar_get_archive(phar_archive_data **archive, char *fname, size_t fname_len, char *alias, size_t alias_len, char **error) /* {{{ */
  956| {
  957| 	phar_archive_data *fd, *fd_ptr;
  958| 	char *my_realpath, *save;
  959| 	size_t save_len;
  960| 
  961| 	phar_request_initialize();
  962| 
  963| 	if (error) {
  964| 		*error = NULL;
  965| 	}
  966| 
  967| 	*archive = NULL;
  968| 
  969| 	if (PHAR_G(last_phar) && fname_len == PHAR_G(last_phar_name_len) && !memcmp(fname, PHAR_G(last_phar_name), fname_len)) {
  970| 		*archive = PHAR_G(last_phar);
  971| 		if (alias && alias_len) {
  972| 
  973| 			if (!PHAR_G(last_phar)->is_temporary_alias && (alias_len != PHAR_G(last_phar)->alias_len || memcmp(PHAR_G(last_phar)->alias, alias, alias_len))) {
  974| 				if (error) {
  975| 					spprintf(error, 0, "alias \"%s\" is already used for archive \"%s\" cannot be overloaded with \"%s\"", alias, PHAR_G(last_phar)->fname, fname);
  976| 				}
  977| 				*archive = NULL;
  978| 				return FAILURE;
  979| 			}
  980| 
  981| 			if (PHAR_G(last_phar)->alias_len && NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), PHAR_G(last_phar)->alias, PHAR_G(last_phar)->alias_len))) {
  982| 				zend_hash_str_del(&(PHAR_G(phar_alias_map)), PHAR_G(last_phar)->alias, PHAR_G(last_phar)->alias_len);
  983| 			}
  984| 
  985| 			zend_hash_str_add_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len, *archive);
  986| 			PHAR_G(last_alias) = alias;
  987| 			PHAR_G(last_alias_len) = alias_len;
  988| 		}
  989| 
  990| 		return SUCCESS;
  991| 	}
  992| 
  993| 	if (alias && alias_len && PHAR_G(last_phar) && alias_len == PHAR_G(last_alias_len) && !memcmp(alias, PHAR_G(last_alias), alias_len)) {
  994| 		fd = PHAR_G(last_phar);
  995| 		fd_ptr = fd;
  996| 		goto alias_success;
  997| 	}
  998| 
  999| 	if (alias && alias_len) {
 1000| 		if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
 1001| alias_success:
 1002| 			if (fname && (fname_len != fd_ptr->fname_len || strncmp(fname, fd_ptr->fname, fname_len))) {
 1003| 				if (error) {
 1004| 					spprintf(error, 0, "alias \"%s\" is already used for archive \"%s\" cannot be overloaded with \"%s\"", alias, fd_ptr->fname, fname);
 1005| 				}
 1006| 				if (SUCCESS == phar_free_alias(fd_ptr, alias, alias_len)) {
 1007| 					if (error) {
 1008| 						efree(*error);
 1009| 						*error = NULL;
 1010| 					}
 1011| 				}
 1012| 				return FAILURE;
 1013| 			}
 1014| 
 1015| 			*archive = fd_ptr;
 1016| 			fd = fd_ptr;
 1017| 			PHAR_G(last_phar) = fd;
 1018| 			PHAR_G(last_phar_name) = fd->fname;
 1019| 			PHAR_G(last_phar_name_len) = fd->fname_len;
 1020| 			PHAR_G(last_alias) = alias;
 1021| 			PHAR_G(last_alias_len) = alias_len;
 1022| 
 1023| 			return SUCCESS;
 1024| 		}
 1025| 
 1026| 		if (PHAR_G(manifest_cached) && NULL != (fd_ptr = zend_hash_str_find_ptr(&cached_alias, alias, alias_len))) {
 1027| 			goto alias_success;
 1028| 		}
 1029| 	}
 1030| 
 1031| 	my_realpath = NULL;
 1032| 	save = fname;
 1033| 	save_len = fname_len;
 1034| 
 1035| 	if (fname && fname_len) {
 1036| 		if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_fname_map)), fname, fname_len))) {
 1037| 			*archive = fd_ptr;
 1038| 			fd = fd_ptr;
 1039| 
 1040| 			if (alias && alias_len) {
 1041| 				if (!fd->is_temporary_alias && (alias_len != fd->alias_len || memcmp(fd->alias, alias, alias_len))) {
 1042| 					if (error) {
 1043| 						spprintf(error, 0, "alias \"%s\" is already used for archive \"%s\" cannot be overloaded with \"%s\"", alias, fd_ptr->fname, fname);
 1044| 					}
 1045| 					return FAILURE;
 1046| 				}
 1047| 
 1048| 				if (fd->alias_len && NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), fd->alias, fd->alias_len))) {
 1049| 					zend_hash_str_del(&(PHAR_G(phar_alias_map)), fd->alias, fd->alias_len);
 1050| 				}
 1051| 
 1052| 				zend_hash_str_add_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len, fd);
 1053| 			}
 1054| 
 1055| 			PHAR_G(last_phar) = fd;
 1056| 			PHAR_G(last_phar_name) = fd->fname;
 1057| 			PHAR_G(last_phar_name_len) = fd->fname_len;
 1058| 			PHAR_G(last_alias) = fd->alias;
 1059| 			PHAR_G(last_alias_len) = fd->alias_len;
 1060| 
 1061| 			return SUCCESS;
 1062| 		}
 1063| 
 1064| 		if (PHAR_G(manifest_cached) && NULL != (fd_ptr = zend_hash_str_find_ptr(&cached_phars, fname, fname_len))) {
 1065| 			*archive = fd_ptr;
 1066| 			fd = fd_ptr;
 1067| 
 1068| 			/* this could be problematic - alias should never be different from manifest alias
 1069| 			   for cached phars */
 1070| 			if (!fd->is_temporary_alias && alias && alias_len) {
 1071| 				if (alias_len != fd->alias_len || memcmp(fd->alias, alias, alias_len)) {
 1072| 					if (error) {
 1073| 						spprintf(error, 0, "alias \"%s\" is already used for archive \"%s\" cannot be overloaded with \"%s\"", alias, fd_ptr->fname, fname);
 1074| 					}
 1075| 					return FAILURE;
 1076| 				}
 1077| 			}
 1078| 
 1079| 			PHAR_G(last_phar) = fd;
 1080| 			PHAR_G(last_phar_name) = fd->fname;
 1081| 			PHAR_G(last_phar_name_len) = fd->fname_len;
 1082| 			PHAR_G(last_alias) = fd->alias;
 1083| 			PHAR_G(last_alias_len) = fd->alias_len;
 1084| 
 1085| 			return SUCCESS;
 1086| 		}
 1087| 
 1088| 		if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), save, save_len))) {
 1089| 			fd = *archive = fd_ptr;
 1090| 
 1091| 			PHAR_G(last_phar) = fd;
 1092| 			PHAR_G(last_phar_name) = fd->fname;
 1093| 			PHAR_G(last_phar_name_len) = fd->fname_len;
 1094| 			PHAR_G(last_alias) = fd->alias;
 1095| 			PHAR_G(last_alias_len) = fd->alias_len;
 1096| 
 1097| 			return SUCCESS;
 1098| 		}
 1099| 
 1100| 		if (PHAR_G(manifest_cached) && NULL != (fd_ptr = zend_hash_str_find_ptr(&cached_alias, save, save_len))) {
 1101| 			fd = *archive = fd_ptr;
 1102| 
 1103| 			PHAR_G(last_phar) = fd;
 1104| 			PHAR_G(last_phar_name) = fd->fname;
 1105| 			PHAR_G(last_phar_name_len) = fd->fname_len;
 1106| 			PHAR_G(last_alias) = fd->alias;
 1107| 			PHAR_G(last_alias_len) = fd->alias_len;
 1108| 
 1109| 			return SUCCESS;
 1110| 		}
 1111| 
 1112| 		/* not found, try converting \ to / */
 1113| 		my_realpath = expand_filepath(fname, my_realpath);
 1114| 
 1115| 		if (my_realpath) {
 1116| 			fname_len = strlen(my_realpath);
 1117| 			fname = my_realpath;
 1118| 		} else {
 1119| 			return FAILURE;
 1120| 		}
 1121| #ifdef PHP_WIN32
 1122| 		phar_unixify_path_separators(fname, fname_len);
 1123| #endif
 1124| 
 1125| 		if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_fname_map)), fname, fname_len))) {
 1126| realpath_success:
 1127| 			*archive = fd_ptr;
 1128| 			fd = fd_ptr;
 1129| 
 1130| 			if (alias && alias_len) {
 1131| 				zend_hash_str_add_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len, fd);
 1132| 			}
 1133| 
 1134| 			efree(my_realpath);
 1135| 
 1136| 			PHAR_G(last_phar) = fd;
 1137| 			PHAR_G(last_phar_name) = fd->fname;
 1138| 			PHAR_G(last_phar_name_len) = fd->fname_len;
 1139| 			PHAR_G(last_alias) = fd->alias;
 1140| 			PHAR_G(last_alias_len) = fd->alias_len;
 1141| 
 1142| 			return SUCCESS;
 1143| 		}
 1144| 
 1145| 		if (PHAR_G(manifest_cached) && NULL != (fd_ptr = zend_hash_str_find_ptr(&cached_phars, fname, fname_len))) {
 1146| 			goto realpath_success;
 1147| 		}
 1148| 
 1149| 		efree(my_realpath);
 1150| 	}
 1151| 
 1152| 	return FAILURE;
 1153| }
```

- `get_function_source(name=phar_parse_tarfile)` →

```
phar_parse_tarfile (function, old version) — ext/phar/tar.c:200-705
  200| zend_result phar_parse_tarfile(php_stream* fp, char *fname, size_t fname_len, char *alias, size_t alias_len, phar_archive_data** pphar, uint32_t compression, char **error) /* {{{ */
  201| {
  202| 	char buf[512], *actual_alias = NULL, *p;
  203| 	phar_entry_info entry = {0};
  204| 	size_t pos = 0, read, totalsize;
  205| 	tar_header *hdr;
  206| 	uint32_t sum1, sum2, size, old;
  207| 	phar_archive_data *myphar, *actual;
  208| 	bool last_was_longlink = false;
  209| 	size_t linkname_len;
  210| 
  211| 	if (error) {
  212| 		*error = NULL;
  213| 	}
  214| 
  215| 	php_stream_seek(fp, 0, SEEK_END);
  216| 	totalsize = php_stream_tell(fp);
  217| 	php_stream_seek(fp, 0, SEEK_SET);
  218| 	read = php_stream_read(fp, buf, sizeof(buf));
  219| 
  220| 	if (read != sizeof(buf)) {
  221| 		if (error) {
  222| 			spprintf(error, 4096, "phar error: \"%s\" is not a tar file or is truncated", fname);
  223| 		}
  224| 		php_stream_close(fp);
  225| 		return FAILURE;
  226| 	}
  227| 
  228| 	hdr = (tar_header*)buf;
  229| 	old = (memcmp(hdr->magic, "ustar", sizeof("ustar")-1) != 0);
  230| 
  231| 	myphar = (phar_archive_data *) pecalloc(1, sizeof(phar_archive_data), PHAR_G(persist));
  232| 	myphar->is_persistent = PHAR_G(persist);
  233| 	/* estimate number of entries, can't be certain with tar files */
  234| 	zend_hash_init(&myphar->manifest, 2 + (totalsize >> 12),
  235| 		zend_get_hash_value, destroy_phar_manifest_entry, myphar->is_persistent);
  236| 	zend_hash_init(&myphar->mounted_dirs, 5,
  237| 		zend_get_hash_value, NULL, myphar->is_persistent);
  238| 	zend_hash_init(&myphar->virtual_dirs, 4 + (totalsize >> 11),
  239| 		zend_get_hash_value, NULL, myphar->is_persistent);
  240| 	myphar->is_tar = 1;
  241| 	/* remember whether this entire phar was compressed with gz/bzip2 */
  242| 	myphar->flags = compression;
  243| 
  244| 	entry.is_tar = 1;
  245| 	entry.is_crc_checked = 1;
  246| 	entry.phar = myphar;
  247| 
  248| 	while (true) {
  249| 		phar_entry_info *newentry;
  250| 
  251| 		pos = php_stream_tell(fp);
  252| 		hdr = (tar_header*) buf;
  253| 		sum1 = phar_tar_number(hdr->checksum, sizeof(hdr->checksum));
  254| 		if (sum1 == 0 && phar_tar_checksum(buf, sizeof(buf)) == 0) {
  255| 			break;
  256| 		}
  257| 		memset(hdr->checksum, ' ', sizeof(hdr->checksum));
  258| 		sum2 = phar_tar_checksum(buf, old?sizeof(old_tar_header):sizeof(tar_header));
  259| 
  260| 		if (old && sum2 != sum1) {
  261| 			uint32_t sum3 = phar_tar_checksum(buf, sizeof(tar_header));
  262| 			if (sum3 == sum1) {
  263| 				/* apparently a broken tar which is in ustar format w/o setting the ustar marker */
  264| 				sum2 = sum3;
  265| 				old = 0;
  266| 			}
  267| 		}
  268| 
  269| 		size = entry.uncompressed_filesize = entry.compressed_filesize =
  270| 			phar_tar_number(hdr->size, sizeof(hdr->size));
  271| 
  272| 		/* skip global/file headers (pax) */
  273| 		if (!old && (hdr->typeflag == TAR_GLOBAL_HDR || hdr->typeflag == TAR_FILE_HDR)) {
  274| 			size = (size+511)&~511;
  275| 			goto next;
  276| 		}
  277| 
  278| 		if (((!old && hdr->prefix[0] == 0) || old) && zend_strnlen(hdr->name, 100) == sizeof(".phar/signature.bin")-1 && !strncmp(hdr->name, ".phar/signature.bin", sizeof(".phar/signature.bin")-1)) {
  279| 			zend_off_t curloc;
  280| 			size_t sig_len;
  281| 
  282| 			if (size > 511) {
  283| 				if (error) {
  284| 					spprintf(error, 4096, "phar error: tar-based phar \"%s\" has signature that is larger than 511 bytes, cannot process", fname);
  285| 				}
  286| bail:
  287| 				php_stream_close(fp);
  288| 				phar_destroy_phar_data(myphar);
  289| 				return FAILURE;
  290| 			}
  291| 			curloc = php_stream_tell(fp);
  292| 			read = php_stream_read(fp, buf, size);
  293| 			if (read != size || read <= 8) {
  294| 				if (error) {
  295| 					spprintf(error, 4096, "phar error: tar-based phar \"%s\" signature cannot be read", fname);
  296| 				}
  297| 				goto bail;
  298| 			}
  299| #ifdef WORDS_BIGENDIAN
  300| # define PHAR_GET_32(buffer) \
  301| 	(((((unsigned char*)(buffer))[3]) << 24) \
  302| 		| ((((unsigned char*)(buffer))[2]) << 16) \
  303| 		| ((((unsigned char*)(buffer))[1]) <<  8) \
  304| 		| (((unsigned char*)(buffer))[0]))
  305| #else
  306| # define PHAR_GET_32(buffer) (uint32_t) *(buffer)
  307| #endif
  308| 			myphar->sig_flags = PHAR_GET_32(buf);
  309| 			if (FAILURE == phar_verify_signature(fp, php_stream_tell(fp) - size - 512, myphar->sig_flags, buf + 8, size - 8, fname, &myphar->signature, &sig_len, error)) {
  310| 				if (error) {
  311| 					char *save = *error;
  312| 					spprintf(error, 4096, "phar error: tar-based phar \"%s\" signature cannot be verified: %s", fname, save);
  313| 					efree(save);
  314| 				}
  315| 				goto bail;
  316| 			}
  317| 			myphar->sig_len = sig_len;
  318| 			php_stream_seek(fp, curloc + 512, SEEK_SET);
  319| 			/* signature checked out, let's ensure this is the last file in the phar */
  320| 			if (((hdr->typeflag == '\0') || (hdr->typeflag == TAR_FILE)) && size > 0) {
  321| 				/* this is not good enough - seek succeeds even on truncated tars */
  322| 				php_stream_seek(fp, 512, SEEK_CUR);
  323| 				if ((uint32_t)php_stream_tell(fp) > totalsize) {
  324| 					if (error) {
  325| 						spprintf(error, 4096, "phar error: \"%s\" is a corrupted tar file (truncated)", fname);
  326| 					}
  327| 					php_stream_close(fp);
  328| 					phar_destroy_phar_data(myphar);
  329| 					return FAILURE;
  330| 				}
  331| 			}
  332| 
  333| 			read = php_stream_read(fp, buf, sizeof(buf));
  334| 
  335| 			if (read != sizeof(buf)) {
  336| 				if (error) {
  337| 					spprintf(error, 4096, "phar error: \"%s\" is a corrupted tar file (truncated)", fname);
  338| 				}
  339| 				php_stream_close(fp);
  340| 				phar_destroy_phar_data(myphar);
  341| 				return FAILURE;
  342| 			}
  343| 
  344| 			hdr = (tar_header*) buf;
  345| 			sum1 = phar_tar_number(hdr->checksum, sizeof(hdr->checksum));
  346| 
  347| 			if (sum1 == 0 && phar_tar_checksum(buf, sizeof(buf)) == 0) {
  348| 				break;
  349| 			}
  350| 
  351| 			if (error) {
  352| 				spprintf(error, 4096, "phar error: \"%s\" has entries after signature, invalid phar", fname);
  353| 			}
  354| 
  355| 			goto bail;
  356| 		}
  357| 
  358| 		if (!last_was_longlink && hdr->typeflag == 'L') {
  359| 			last_was_longlink = true;
  360| 			/* support the ././@LongLink system for storing long filenames */
  361| 
  362| 			/* Check for overflow - bug 61065 */
  363| 			if (entry.uncompressed_filesize == UINT_MAX || entry.uncompressed_filesize == 0) {
  364| 				if (error) {
  365| 					spprintf(error, 4096, "phar error: \"%s\" is a corrupted tar file (invalid entry size)", fname);
  366| 				}
  367| 				php_stream_close(fp);
  368| 				phar_destroy_phar_data(myphar);
  369| 				return FAILURE;
  370| 			}
  371| 			entry.filename = zend_string_alloc(entry.uncompressed_filesize, myphar->is_persistent);
  372| 			if (myphar->is_persistent) {
  373| 				GC_MAKE_PERSISTENT_LOCAL(entry.filename);
  374| 			}
  375| 			ZSTR_VAL(entry.filename)[entry.uncompressed_filesize] = '\0';
  376| 
  377| 			read = php_stream_read(fp, ZSTR_VAL(entry.filename), entry.uncompressed_filesize);
  378| 			if (read != entry.uncompressed_filesize) {
  379| 				zend_string_free(entry.filename);
  380| 				if (error) {
  381| 					spprintf(error, 4096, "phar error: \"%s\" is a corrupted tar file (truncated)", fname);
  382| 				}
  383| 				php_stream_close(fp);
  384| 				phar_destroy_phar_data(myphar);
  385| 				return FAILURE;
  386| 			}
  387| 
  388| 			/* skip blank stuff */
  389| 			size = ((size+511)&~511) - size;
  390| 
  391| 			/* this is not good enough - seek succeeds even on truncated tars */
  392| 			php_stream_seek(fp, size, SEEK_CUR);
  393| 			if ((uint32_t)php_stream_tell(fp) > totalsize) {
  394| 				zend_string_free(entry.filename);
  395| 				if (error) {
  396| 					spprintf(error, 4096, "phar error: \"%s\" is a corrupted tar file (truncated)", fname);
  397| 				}
  398| 				php_stream_close(fp);
  399| 				phar_destroy_phar_data(myphar);
  400| 				return FAILURE;
  401| 			}
  402| 
  403| 			read = php_stream_read(fp, buf, sizeof(buf));
  404| 
  405| 			if (read != sizeof(buf)) {
  406| 				zend_string_free(entry.filename);
  407| 				if (error) {
  408| 					spprintf(error, 4096, "phar error: \"%s\" is a corrupted tar file (truncated)", fname);
  409| 				}
  410| 				php_stream_close(fp);
  411| 				phar_destroy_phar_data(myphar);
  412| 				return FAILURE;
  413| 			}
  414| 			continue;
  415| 		} else if (!last_was_longlink && !old && hdr->prefix[0] != 0) {
  416| 			char name[256];
  417| 			int i, j;
  418| 
  419| 			for (i = 0; i < 155; i++) {
  420| 				name[i] = hdr->prefix[i];
  421| 				if (name[i] == '\0') {
  422| 					break;
  423| 				}
  424| 			}
  425| 			name[i++] = '/';
  426| 			for (j = 0; j < 100; j++) {
  427| 				name[i+j] = hdr->name[j];
  428| 				if (name[i+j] == '\0') {
  429| 					break;
  430| 				}
  431| 			}
  432| 
  433| 			uint32_t filename_len = i + j;
  434| 
  435| 			if (name[filename_len - 1] == '/') {
  436| 				/* some tar programs store directories with trailing slash */
  437| 				filename_len--;
  438| 			}
  439| 
  440| 			entry.filename = zend_string_init(name, filename_len, myphar->is_persistent);
  441| 			if (myphar->is_persistent) {
  442| 				GC_MAKE_PERSISTENT_LOCAL(entry.filename);
  443| 			}
  444| 		} else if (!last_was_longlink) {
  445| 			/* calculate strlen, which can be no longer than 100 */
  446| 			uint32_t filename_len;
  447| 			for (filename_len = 0; filename_len < 100; filename_len++) {
  448| 				if (hdr->name[filename_len] == '\0') {
  449| 					break;
  450| 				}
  451| 			}
  452| 
  453| 			if (filename_len > 0 && hdr->name[filename_len - 1] == '/') {
  454| 				/* some tar programs store directories with trailing slash */
  455| 				filename_len--;
  456| 			}
  457| 
  458| 			entry.filename = zend_string_init(hdr->name, filename_len, myphar->is_persistent);
  459| 			if (myphar->is_persistent) {
  460| 				GC_MAKE_PERSISTENT_LOCAL(entry.filename);
  461| 			}
  462| 		}
  463| 		last_was_longlink = false;
  464| 
  465| 		phar_add_virtual_dirs(myphar, ZSTR_VAL(entry.filename), ZSTR_LEN(entry.filename));
  466| 
  467| 		if (sum1 != sum2) {
  468| 			if (error) {
  469| 				spprintf(error, 4096, "phar error: \"%s\" is a corrupted tar file (checksum mismatch of file \"%s\")", fname, ZSTR_VAL(entry.filename));
  470| 			}
  471| 			zend_string_release_ex(entry.filename, myphar->is_persistent);
  472| 			php_stream_close(fp);
  473| 			phar_destroy_phar_data(myphar);
  474| 			return FAILURE;
  475| 		}
  476| 
  477| 		uint32_t entry_mode = phar_tar_number(hdr->mode, sizeof(hdr->mode));
  478| 		entry.tar_type = ((old & (hdr->typeflag == '\0')) ? TAR_FILE : hdr->typeflag);
  479| 		entry.offset = entry.offset_abs = pos; /* header_offset unused in tar */
  480| 		entry.fp_type = PHAR_FP;
  481| 		entry.flags = entry_mode & PHAR_ENT_PERM_MASK;
  482| 		entry.timestamp = phar_tar_number(hdr->mtime, sizeof(hdr->mtime));
  483| 		entry.is_persistent = myphar->is_persistent;
  484| 
  485| 		if (old && entry.tar_type == TAR_FILE && S_ISDIR(entry_mode)) {
  486| 			entry.tar_type = TAR_DIR;
  487| 		}
  488| 
  489| 		if (entry.tar_type == TAR_DIR) {
  490| 			entry.is_dir = 1;
  491| 		} else {
  492| 			entry.is_dir = 0;
  493| 		}
  494| 
  495| 		entry.link = NULL;
  496| 		/* link field is null-terminated unless it has 100 non-null chars.
  497| 		 * Thus we cannot use strlen. */
  498| 		linkname_len = zend_strnlen(hdr->linkname, 100);
  499| 		if (entry.tar_type == TAR_LINK) {
  500| 			if (!zend_hash_str_exists(&myphar->manifest, hdr->linkname, linkname_len)) {
  501| 				if (error) {
  502| 					spprintf(error, 4096, "phar error: \"%s\" is a corrupted tar file - hard link to non-existent file \"%.*s\"", fname, (int)linkname_len, hdr->linkname);
  503| 				}
  504| 				zend_string_release_ex(entry.filename, myphar->is_persistent);
  505| 				php_stream_close(fp);
  506| 				phar_destroy_phar_data(myphar);
  507| 				return FAILURE;
  508| 			}
  509| 			entry.link = estrndup(hdr->linkname, linkname_len);
  510| 		} else if (entry.tar_type == TAR_SYMLINK) {
  511| 			entry.link = estrndup(hdr->linkname, linkname_len);
  512| 		}
  513| 		phar_set_inode(&entry);
  514| 
  515| 		newentry = zend_hash_update_mem(&myphar->manifest, entry.filename, &entry, sizeof(phar_entry_info));
  516| 		ZEND_ASSERT(newentry != NULL);
  517| 
  518| 		if (entry.is_persistent) {
  519| 			++entry.manifest_pos;
  520| 		}
  521| 
  522| 		if (zend_string_starts_with_literal(entry.filename, ".phar/.metadata")) {
  523| 			if (FAILURE == phar_tar_process_metadata(newentry, fp)) {
  524| 				if (error) {
  525| 					spprintf(error, 4096, "phar error: tar-based phar \"%s\" has invalid metadata in magic file \"%s\"", fname, ZSTR_VAL(entry.filename));
  526| 				}
  527| 				php_stream_close(fp);
  528| 				phar_destroy_phar_data(myphar);
  529| 				return FAILURE;
  530| 			}
  531| 		}
  532| 
  533| 		if (!actual_alias && zend_string_equals_literal(entry.filename, ".phar/alias.txt")) {
  534| 			/* found explicit alias */
  535| 			if (size > 511) {
  536| 				if (error) {
  537| 					spprintf(error, 4096, "phar error: tar-based phar \"%s\" has alias that is larger than 511 bytes, cannot process", fname);
  538| 				}
  539| 				php_stream_close(fp);
  540| 				phar_destroy_phar_data(myphar);
  541| 				return FAILURE;
  542| 			}
  543| 
  544| 			read = php_stream_read(fp, buf, size);
  545| 
  546| 			if (read == size) {
  547| 				buf[size] = '\0';
  548| 				if (!phar_validate_alias(buf, size)) {
  549| 					if (size > 50) {
  550| 						buf[50] = '.';
  551| 						buf[51] = '.';
  552| 						buf[52] = '.';
  553| 						buf[53] = '\0';
  554| 					}
  555| 
  556| 					if (error) {
  557| 						spprintf(error, 4096, "phar error: invalid alias \"%s\" in tar-based phar \"%s\"", buf, fname);
  558| 					}
  559| 
  560| 					php_stream_close(fp);
  561| 					phar_destroy_phar_data(myphar);
  562| 					return FAILURE;
  563| 				}
  564| 
  565| 				actual_alias = pestrndup(buf, size, myphar->is_persistent);
  566| 				myphar->alias = actual_alias;
  567| 				myphar->alias_len = size;
  568| 				php_stream_seek(fp, pos, SEEK_SET);
  569| 			} else {
  570| 				if (error) {
  571| 					spprintf(error, 4096, "phar error: Unable to read alias from tar-based phar \"%s\"", fname);
  572| 				}
  573| 
  574| 				php_stream_close(fp);
  575| 				phar_destroy_phar_data(myphar);
  576| 				return FAILURE;
  577| 			}
  578| 		}
  579| 
  580| 		size = (size+511)&~511;
  581| 
  582| 		if (((hdr->typeflag == '\0') || (hdr->typeflag == TAR_FILE)) && size > 0) {
  583| next:
  584| 			/* this is not good enough - seek succeeds even on truncated tars */
  585| 			php_stream_seek(fp, size, SEEK_CUR);
  586| 			if ((uint32_t)php_stream_tell(fp) > totalsize) {
  587| 				if (error) {
  588| 					spprintf(error, 4096, "phar error: \"%s\" is a corrupted tar file (truncated)", fname);
  589| 				}
  590| 				php_stream_close(fp);
  591| 				phar_destroy_phar_data(myphar);
  592| 				return FAILURE;
  593| 			}
  594| 		}
  595| 
  596| 		/* Only read next header if we're not yet at the end */
  597| 		if (php_stream_tell(fp) == totalsize) {
  598| 			break;
  599| 		}
  600| 
  601| 		read = php_stream_read(fp, buf, sizeof(buf));
  602| 
  603| 		if (read != sizeof(buf)) {
  604| 			if (error) {
  605| 				spprintf(error, 4096, "phar error: \"%s\" is a corrupted tar file (truncated)", fname);
  606| 			}
  607| 			php_stream_close(fp);
  608| 			phar_destroy_phar_data(myphar);
  609| 			return FAILURE;
  610| 		}
  611| 	}
  612| 
  613| 	if (zend_hash_str_exists(&(myphar->manifest), ".phar/stub.php", sizeof(".phar/stub.php")-1)) {
  614| 		myphar->is_data = 0;
  615| 	} else {
  616| 		myphar->is_data = 1;
  617| 	}
  618| 
  619| 	/* ensure signature set */
  620| 	if (!myphar->is_data && PHAR_G(require_hash) && !myphar->signature) {
  621| 		php_stream_close(fp);
  622| 		phar_destroy_phar_data(myphar);
  623| 		if (error) {
  624| 			spprintf(error, 0, "tar-based phar \"%s\" does not have a signature", fname);
  625| 		}
  626| 		return FAILURE;
  627| 	}
  628| 
  629| 	myphar->fname = pestrndup(fname, fname_len, myphar->is_persistent);
  630| #ifdef PHP_WIN32
  631| 	phar_unixify_path_separators(myphar->fname, fname_len);
  632| #endif
  633| 	myphar->fname_len = fname_len;
  634| 	myphar->fp = fp;
  635| 	p = strrchr(myphar->fname, '/');
  636| 
  637| 	if (p) {
  638| 		myphar->ext = memchr(p, '.', (myphar->fname + fname_len) - p);
  639| 		if (myphar->ext == p) {
  640| 			myphar->ext = memchr(p + 1, '.', (myphar->fname + fname_len) - p - 1);
  641| 		}
  642| 		if (myphar->ext) {
  643| 			myphar->ext_len = (myphar->fname + fname_len) - myphar->ext;
  644| 		}
  645| 	}
  646| 
  647| 	phar_request_initialize();
  648| 
  649| 	if (NULL == (actual = zend_hash_str_add_ptr(&(PHAR_G(phar_fname_map)), myphar->fname, fname_len, myphar))) {
  650| 		if (error) {
  651| 			spprintf(error, 4096, "phar error: Unable to add tar-based phar \"%s\" to phar registry", fname);
  652| 		}
  653| 		php_stream_close(fp);
  654| 		phar_destroy_phar_data(myphar);
  655| 		return FAILURE;
  656| 	}
  657| 
  658| 	myphar = actual;
  659| 
  660| 	if (actual_alias) {
  661| 		phar_archive_data *fd_ptr;
  662| 
  663| 		myphar->is_temporary_alias = 0;
  664| 
  665| 		if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), actual_alias, myphar->alias_len))) {
  666| 			if (SUCCESS != phar_free_alias(fd_ptr, actual_alias, myphar->alias_len)) {
  667| 				if (error) {
  668| 					spprintf(error, 4096, "phar error: Unable to add tar-based phar \"%s\", alias is already in use", fname);
  669| 				}
  670| 				zend_hash_str_del(&(PHAR_G(phar_fname_map)), myphar->fname, fname_len);
  671| 				return FAILURE;
  672| 			}
  673| 		}
  674| 
  675| 		zend_hash_str_add_ptr(&(PHAR_G(phar_alias_map)), actual_alias, myphar->alias_len, myphar);
  676| 	} else {
  677| 		phar_archive_data *fd_ptr;
  678| 
  679| 		if (alias_len) {
  680| 			if (NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
  681| 				if (SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
  682| 					if (error) {
  683| 						spprintf(error, 4096, "phar error: Unable to add tar-based phar \"%s\", alias is already in use", fname);
  684| 					}
  685| 					zend_hash_str_del(&(PHAR_G(phar_fname_map)), myphar->fname, fname_len);
  686| 					return FAILURE;
  687| 				}
  688| 			}
  689| 			zend_hash_str_add_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len, myphar);
  690| 			myphar->alias = pestrndup(alias, alias_len, myphar->is_persistent);
  691| 			myphar->alias_len = alias_len;
  692| 		} else {
  693| 			myphar->alias = pestrndup(myphar->fname, fname_len, myphar->is_persistent);
  694| 			myphar->alias_len = fname_len;
  695| 		}
  696| 
  697| 		myphar->is_temporary_alias = 1;
  698| 	}
  699| 
  700| 	if (pphar) {
  701| 		*pphar = myphar;
  702| 	}
  703| 
  704| 	return SUCCESS;
  705| }
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 38298+266, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "phar_parse_pharfile", "file": "ext/phar/phar.c"}, {"function": "phar_create_or_parse_filename", "file": "ext/phar/phar.c"}, {"function": "PHP_METHOD(Phar, setAlias)", "file": "ext/phar/phar_object.c"}, {"function": "phar_parse_tarfile", "file": "ext/phar/tar.c"}, {"function": "phar_get_archive", "file": "ext/phar/util.c"}, {"function": "phar_parse_zipfile", "file": "ext/phar/zip.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 6, "n_truth": 6, "tp": 6, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

