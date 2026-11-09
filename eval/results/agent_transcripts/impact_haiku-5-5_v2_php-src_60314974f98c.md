# Impact-analysis transcript — php-src @ 60314974f98c — anthropic:claude-haiku-5-5

- target: `phar_free_alias` (ext/phar/util.c), arity 3->1
- truth: [['ext/phar/phar.c', 'phar_create_or_parse_filename'], ['ext/phar/phar.c', 'phar_parse_pharfile'], ['ext/phar/tar.c', 'phar_parse_tarfile'], ['ext/phar/util.c', 'phar_get_archive'], ['ext/phar/zip.c', 'phar_parse_zipfile']]

## Self-navigation arm

### Turn 1  _(tok 1213+96, stop=tool_use)_

**Reasoning:** I should search the repo for phar_free_alias to see where it's used.



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

### Turn 2  _(tok 1860+812, stop=tool_use)_

**Reasoning:** I need to find which functions enclose each location, so I'm checking util.c around line 1006 to identify the surrounding function.



**Says:** I have 10 matches. Next I need the enclosing function for each call site, so I'll read the surrounding code.

- `read_file(path=ext/phar/phar.c, version=old, start_line=1200, end_line=1270)` →

```
ext/phar/phar.c lines 1200-1270 of 3484
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

- `read_file(path=ext/phar/phar_object.c, version=old, start_line=2660, end_line=2715)` →

```
ext/phar/phar_object.c lines 2660-2715 of 5059
 2660| 	PHAR_ARCHIVE_OBJECT();
 2661| 
 2662| 	RETURN_STRINGL(phar_obj->archive->fname, phar_obj->archive->fname_len);
 2663| }
 2664| /* }}} */
 2665| 
 2666| /* {{{ Sets the alias for a Phar archive. The default value is the full path
 2667|  * to the archive.
 2668|  */
 2669| PHP_METHOD(Phar, setAlias)
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

- `read_file(path=ext/phar/tar.c, version=old, start_line=600, end_line=690)` →

```
ext/phar/tar.c lines 600-690 of 1318
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
```

- `read_file(path=ext/phar/util.c, version=old, start_line=925, end_line=1020)` →

```
ext/phar/util.c lines 925-1020 of 2088
  925| 		spprintf(error, 4096, "phar error: cannot seek to start of file \"%s\" in phar \"%s\"", ZSTR_VAL(entry->filename), phar->fname);
  926| 		return NULL;
  927| 	}
  928| 	return entry;
  929| }
  930| /* }}} */
  931| 
  932| zend_result phar_free_alias(phar_archive_data *phar, char *alias, size_t alias_len) /* {{{ */
  933| {
  934| 	if (phar->refcount || phar->is_persistent) {
  935| 		return FAILURE;
  936| 	}
  937| 
  938| 	/* this archive has no open references, so emit a notice and remove it */
  939| 	if (zend_hash_str_del(&(PHAR_G(phar_fname_map)), phar->fname, phar->fname_len) != SUCCESS) {
  940| 		return FAILURE;
  941| 	}
  942| 
  943| 	/* invalidate phar cache */
  944| 	PHAR_G(last_phar) = NULL;
  945| 	PHAR_G(last_phar_name) = PHAR_G(last_alias) = NULL;
  946| 
  947| 	return SUCCESS;
  948| }
  949| /* }}} */
  950| 
  951| /**
  952|  * Looks up a phar archive in the filename map, connecting it to the alias
  953|  * (if any) or returns null
  954|  */
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
```

- `read_file(path=ext/phar/zip.c, version=old, start_line=690, end_line=775)` →

```
ext/phar/zip.c lines 690-775 of 1486
  690| 						entry.uncompressed_filesize = ZSTR_LEN(str);
  691| 						actual_alias = estrndup(ZSTR_VAL(str), ZSTR_LEN(str));
  692| 						zend_string_release_ex(str, 0);
  693| 					} else {
  694| 						actual_alias = NULL;
  695| 						entry.uncompressed_filesize = 0;
  696| 					}
  697| 				}
  698| 
  699| 				if (!entry.uncompressed_filesize) {
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
  771| 				}
  772| 			}
  773| 
  774| 			zend_hash_str_add_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len, mydata);
  775| 			mydata->alias = pestrndup(alias, alias_len, mydata->is_persistent);
```

### Turn 3  _(tok 13077+367, stop=tool_use)_

**Reasoning:** I need to find the enclosing function names, so I'm searching for function definitions like PHP_METHOD and PHP_FUNCTION across phar.c, tar.c, zip.c, util.c, and phar_object.c.



**Says:** I have the call sites. Now I need the enclosing function names, so I'll locate the function definitions in these files.

- `grep(pattern=^(static |zend_result |int |void |PHP_METHOD\(|PHP_FUNCTION\, path_glob=ext/phar/*.c, version=old, max_results=1000)` →

```
252 matches (showing 200)
ext/phar/dirstream.c:22:void phar_dostat(phar_archive_data *phar, phar_entry_info *data, php_stream_statbuf *ssb, bool is_dir);
ext/phar/dirstream.c:24:static const php_stream_ops phar_dir_ops = {
ext/phar/dirstream.c:39:static int phar_dir_close(php_stream *stream, int close_handle)  /* {{{ */
ext/phar/dirstream.c:56:static int phar_dir_seek(php_stream *stream, zend_off_t offset, int whence, zend_off_t *newoffset) /* {{{ */
ext/phar/dirstream.c:88:static ssize_t phar_dir_read(php_stream *stream, char *buf, size_t count) /* {{{ */
ext/phar/dirstream.c:120:static ssize_t phar_dir_write(php_stream *stream, const char *buf, size_t count) /* {{{ */
ext/phar/dirstream.c:129:static int phar_dir_flush(php_stream *stream) /* {{{ */
ext/phar/dirstream.c:138:static int phar_compare_dir_name(Bucket *f, Bucket *s)  /* {{{ */
ext/phar/dirstream.c:151:static php_stream *phar_make_dirstream(const char *dir, size_t dirlen, const HashTable *manifest) /* {{{ */
ext/phar/dirstream.c:248:php_stream *phar_wrapper_open_dir(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STREAMS_
ext/phar/dirstream.c:344:int phar_wrapper_mkdir(php_stream_wrapper *wrapper, const char *url_from, int mode, int options, php_stream_context *context) /* {{{ */
ext/phar/dirstream.c:470:int phar_wrapper_rmdir(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
ext/phar/func_interceptors.c:21:PHP_FUNCTION(phar_opendir) /* {{{ */
ext/phar/func_interceptors.c:85:static zend_string* phar_get_name_for_relative_paths(zend_string *filename, bool using_include_path)
ext/phar/func_interceptors.c:148:PHP_FUNCTION(phar_file_get_contents) /* {{{ */
ext/phar/func_interceptors.c:225:PHP_FUNCTION(phar_readfile) /* {{{ */
ext/phar/func_interceptors.c:269:PHP_FUNCTION(phar_fopen) /* {{{ */
ext/phar/func_interceptors.c:322:static void phar_fancy_stat(zend_stat_t *stat_sb, int type, zval *return_value)
ext/phar/func_interceptors.c:471:static void phar_file_stat(const char *filename, size_t filename_length, int type, zif_handler orig_stat_func, INTERNAL_FUNCTION_PARAMETERS) /* {{{ */
ext/phar/func_interceptors.c:635:PHP_FUNCTION(fname) { \
ext/phar/func_interceptors.c:707:PHP_FUNCTION(phar_is_file) /* {{{ */
ext/phar/func_interceptors.c:765:PHP_FUNCTION(phar_is_link) /* {{{ */
ext/phar/func_interceptors.c:831:void phar_intercept_functions(void)
ext/phar/func_interceptors.c:842:void phar_release_functions(void)
ext/phar/func_interceptors.c:856:void phar_intercept_functions_init(void)
ext/phar/func_interceptors.c:893:void phar_intercept_functions_shutdown(void)
ext/phar/func_interceptors.c:922:static struct _phar_orig_functions {
ext/phar/func_interceptors.c:947:void phar_save_orig_functions(void) /* {{{ */
ext/phar/func_interceptors.c:974:void phar_restore_orig_functions(void) /* {{{ */
ext/phar/phar.c:29:static void destroy_phar_data(zval *zv);
ext/phar/phar.c:31:ZEND_DECLARE_MODULE_GLOBALS(phar)
ext/phar/phar.c:32:static zend_string *(*phar_save_resolve_path)(zend_string *filename);
ext/phar/phar.c:37:static int phar_set_writeable_bit(zval *zv, void *argument) /* {{{ */
ext/phar/phar.c:51:ZEND_INI_MH(phar_ini_modify_handler) /* {{{ */
ext/phar/phar.c:91:static void phar_split_cache_list(void) /* {{{ */
ext/phar/phar.c:171:ZEND_INI_MH(phar_ini_cache_list) /* {{{ */
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
ext/phar/phar.c:3131:static zend_string *phar_resolve_path(zend_string *filename)
ext/phar/phar.c:3140:static zend_op_array *phar_compile_file(zend_file_handle *file_handle, int type) /* {{{ */
ext/phar/phar.c:3215:static void mime_type_dtor(zval *zv)
ext/phar/phar.c:3331:void phar_request_initialize(void) /* {{{ */
ext/phar/phar.c:3455:static const zend_module_dep phar_deps[] = {
ext/phar/phar_object.c:29:static zend_class_entry *phar_ce_archive;
ext/phar/phar_object.c:30:static zend_class_entry *phar_ce_data;
ext/phar/phar_object.c:31:static zend_class_entry *phar_ce_PharException;
ext/phar/phar_object.c:32:static zend_class_entry *phar_ce_entry;
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
ext/phar/phar_object.c:1065:static const spl_other_handler phar_spl_foreign_handler = {
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
ext/phar/stream.c:23:static const php_stream_ops phar_ops = {
ext/phar/stream.c:35:static const php_stream_wrapper_ops phar_stream_wops = {
ext/phar/stream.c:159:static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STR
ext/phar/stream.c:351:static int phar_stream_close(php_stream *stream, int close_handle) /* {{{ */
ext/phar/stream.c:365:static ssize_t phar_stream_read(php_stream *stream, char *buf, size_t count) /* {{{ */
ext/phar/stream.c:396:static int phar_stream_seek(php_stream *stream, zend_off_t offset, int whence, zend_off_t *newoffset) /* {{{ */
ext/phar/stream.c:440:static ssize_t phar_stream_write(php_stream *stream, const char *buf, size_t count) /* {{{ */
ext/phar/stream.c:463:static int phar_stream_flush(php_stream *stream) /* {{{ */
ext/phar/stream.c:487:void phar_dostat(phar_archive_data *phar, phar_entry_info *data, php_stream_statbuf *ssb, bool is_temp_dir)
ext/phar/stream.c:539:static int phar_stream_stat(php_stream *stream, php_stream_statbuf *ssb) /* {{{ */
ext/phar/stream.c:556:static int phar_wrapper_stat(php_stream_wrapper *wrapper, const char *url, int flags,
ext/phar/stream.c:657:static int phar_wrapper_unlink(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
ext/phar/stream.c:729:static int phar_wrapper_rename(php_stream_wrapper *wrapper, const char *url_from, const char *url_to, int options, php_stream_context *context) /* {{{ */
ext/phar/tar.c:21:static uint32_t phar_tar_number(const char *buf, size_t len) /* {{{ */
ext/phar/tar.c:64:static zend_result phar_tar_octal(char *buf, uint32_t val, size_t len) /* {{{ */
ext/phar/tar.c:88:static uint32_t phar_tar_checksum(const char *buf, size_t len) /* {{{ */
ext/phar/tar.c:101:bool phar_is_tar(const char *buf, const char *fname) /* {{{ */
ext/phar/tar.c:129:ZEND_ATTRIBUTE_NONNULL_ARGS(1, 7, 8) zend_result phar_open_or_create_tar(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_archive_d
ext/phar/tar.c:158:static zend_result phar_tar_process_metadata(phar_entry_info *entry, php_stream *fp) /* {{{ */
```

### Turn 4  _(tok 23229+969, stop=tool_use)_

**Reasoning:** I'm tracing which functions enclose each line: line 1266 falls inside phar_parse_pharfile, while line 1465 falls inside phar_create_or_parse_filename rather than phar_open_or_create_filename.

Continuing the mapping, phar_object.c:2708 lands in PHP_METHOD(Phar, setAlias). For tar.c lines 666 and 681, I suspect they're in phar_open_or_create_tar but my grep results got truncated before confirming there's no intervening function, so I need to re-check tar.c, zip.c, and util.c function boundaries more carefully. Util.c:1006 falls inside phar_get_archive, and I still need to verify which function contains zip.c:743 and 765.



**Says:** Several call sites fall inside functions whose definitions are cut off in that listing (tar.c, zip.c, util.c). I'll pull the definitions for those files and for the `phar.c` region around 1304–1370.

- `grep(pattern=^[a-zA-Z_].*\(.*\)? *(\{|/\*|$), path_glob=ext/phar/tar.c, version=old)` →

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

- `grep(pattern=^[a-zA-Z_].*\(, path_glob=ext/phar/zip.c, version=old)` →

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

- `grep(pattern=^[a-zA-Z_].*\(, path_glob=ext/phar/util.c, version=old)` →

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

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 28221+255, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "phar_parse_pharfile", "file": "ext/phar/phar.c"}, {"function": "phar_create_or_parse_filename", "file": "ext/phar/phar.c"}, {"function": "PHP_METHOD(Phar, setAlias)", "file": "ext/phar/phar_object.c"}, {"function": "phar_parse_tarfile", "file": "ext/phar/tar.c"}, {"function": "phar_get_archive", "file": "ext/phar/util.c"}, {"function": "phar_parse_zipfile", "file": "ext/phar/zip.c"}], "confidence_overall": "medium"}`

**Score (self):** `{"n_pred": 6, "n_truth": 5, "tp": 5, "precision": 0.8333333333333334, "recall": 1.0, "f1": 0.9090909090909091}`

## Tool arm

### Turn 1  _(tok 3748+228, stop=tool_use)_

**Reasoning:** I'll check who calls phar_free_alias, and also grep the codebase directly to be thorough.



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

- `grep(pattern=phar_free_alias, version=old, max_results=500)` →

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

### Turn 2  _(tok 4951+711, stop=tool_use)_

**Reasoning:** I notice the grep found a reference at phar_object.c:2708 that my earlier caller search missed, so I need to check the surrounding code to identify which function contains that line.



**Says:** The grep found a call in `ext/phar/phar_object.c:2708` that `get_callers` did not return. I'll check its enclosing function, and confirm the others.

- `get_context_at(file=ext/phar/phar_object.c, line=2708, rev=None, version=old)` →

```
{
  "error": "ext/phar/phar_object.c:2708 is not inside a function definition in the old version"
}
```

- `get_context_at(file=ext/phar/phar.c, line=1266, version=old)` →

```
phar_parse_pharfile — ext/phar/phar.c:725 [function] static zend_result phar_parse_pharfile(php_stream *fp, char *fname, size_t fname_len, char *alias, size_t alias_len, zend_long halt_offset, phar_archive_data** pphar, uint32_t compression, char **erro
  reads: alias, alias_len, compression, error, fname, fname_len, fp, halt_offset, pphar; writes: error*, pphar*; returns: return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE;

SLICE around line 1266 (def-use, level 2; '>' marks the seed):
static zend_result phar_parse_pharfile(php_stream *fp, char *fname, size_t fname_len, char *alias, size_t alias_len, zend_long halt_offset, phar_archive_data** pphar, uint32_t compression, char **erro {
   char b32[4], *buffer, *endbuffer, *savebuf;
   ...
   uint32_t manifest_len, manifest_count, manifest_flags, manifest_index, tmp_len, sig_flags;
   ...
   bool register_alias = false, temp_alias = false;
   ...
   buffer = b32;
   ...
   buffer = b32;
   ...
   buffer =(char *)emalloc(manifest_len);
   ...
   buffer += 2;
   ...
   if(tmp_len) {
   ...
     alias_len = tmp_len;
     alias = buffer;
   ...
     register_alias = true;
   } else if(!alias_len || !alias) {
     alias = NULL;
     alias_len = 0;
     register_alias = false;
   } else if(alias_len) {
     register_alias = true;
   ...
   }
   ...
   if(register_alias) {
     phar_archive_data *fd_ptr;
   ...
     if(NULL !=(fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
>      if(SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
         signature = NULL;
         fp = NULL;
         MAPPHAR_FAIL("Cannot open archive \"%s\", alias is already in use by existing archive");
   ...
       }
     }
   }
}

CALLEES (39):
  phar_verify_signature (ext/phar/util.c:1476): reads end_of_phar, error, fname, fp, sig, sig_len, sig_type, signature, signature_len; writes error*, signature_len*; returns return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE;
  phar_parse_metadata_lazy (ext/phar/phar.c:694): reads buffer, persistent, tracker, zip_metadata_len; writes tracker*; returns -
  zend_string_release (Zend/zend_string.h:334): reads s; writes -; returns -
  zend_hash_add_mem (Zend/zend_hash.h:741): reads ht, key, pData, size; writes -; returns return Z_PTR_P(zv); | return NULL;
  phar_set_inode (ext/phar/phar_internal.h:381): reads entry; writes entry*; returns -
  zend_string_free (Zend/zend_string.h:318): reads s; writes -; returns -
  phar_metadata_tracker_free (ext/phar/phar.c:636): reads persistent, tracker; writes tracker*; returns -
  zend_string_init (Zend/zend_string.h:186): reads len, persistent, str; writes -; returns return ret;
  phar_add_virtual_dirs (ext/phar/util.c:1962): reads filename, filename_len, phar; writes phar*; returns -
  phar_request_initialize (ext/phar/phar.c:3331): reads -; writes -; returns -
  zend_hash_add_ptr (Zend/zend_hash.h:665): reads ht, key, pData; writes -; returns return Z_PTR_P(zv); | return NULL;
  phar_free_alias (ext/phar/util.c:932): reads phar; writes -; returns return FAILURE; | return FAILURE; | return SUCCESS;
  zend_hash_str_find_ptr (Zend/zend_hash.h:915): reads ht, len, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  phar_validate_alias (ext/phar/phar_internal.h:374): reads alias, alias_len; writes -; returns return !(memchr(alias, '/', alias_len)|| memchr(alias, '\\', alias_len)|| memchr(alias, ':', alias_len)|| memchr(alias, ';', alias_len)|| memchr(alias, '\n', alias_len)|| memchr(alias, '\r', alias_len));
  MAPPHAR_ALLOC_FAIL [macro]: #define MAPPHAR_ALLOC_FAIL(msg) \
  php_stream_seek [macro]: #define php_stream_seek(stream, offset, whence) _php_stream_seek((stream), (offset), (whence))
  php_stream_read [macro]: #define php_stream_read(stream, buf, count) _php_stream_read((stream), (buf), (count))
  php_stream_getc [macro]: #define php_stream_getc(stream) _php_stream_getc((stream))
  PHAR_GET_32 [macro (1 of 5 definitions)]: # define PHAR_GET_32(buffer, var) \
  emalloc [macro]: #define emalloc(size) _emalloc((size) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  MAPPHAR_FAIL [macro]: #define MAPPHAR_FAIL(msg) \
  SAFE_PHAR_GET_32 [macro]: #define SAFE_PHAR_GET_32(buffer, endbuffer, var) \
  spprintf [macro]: #define spprintf zend_spprintf
  php_stream_close [macro]: #define php_stream_close(stream) _php_stream_free((stream), PHP_STREAM_FREE_CLOSE)
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  php_stream_tell [macro]: #define php_stream_tell(stream) _php_stream_tell((stream))
  pecalloc [macro]: #define pecalloc(nmemb, size, persistent) ((persistent)?__zend_calloc((nmemb), (size) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC):ecalloc((nmemb), (size)))
  HT_INVALIDATE [macro]: #define HT_INVALIDATE(ht) do { \
  zend_hash_init [macro]: #define zend_hash_init(ht, nSize, pHashFunction, pDestructor, persistent) \
  pestrndup [macro]: #define pestrndup(s, length, persistent) ((persistent)?zend_strndup((s),(length)):estrndup((s),(length)))
  not defined in this repository: PHAR_G, phar_unixify_path_separators, zend_string_init_interned, strrchr, memchr
  not shown (4): ZSTR_LEN, ZSTR_VAL, ZVAL_UNDEF, GC_MAKE_PERSISTENT_LOCAL

CALLERS (1):
  phar_open_from_fp (ext/phar/phar.c:1729): return phar_parse_pharfile(fp, fname, fname_len, alias, alias_len, halt_offset, pphar, compression, error);
```

- `get_context_at(file=ext/phar/phar.c, line=1465, version=old)` →

```
phar_create_or_parse_filename — ext/phar/phar.c:1370 [function] zend_result phar_create_or_parse_filename(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_archive_data** pphar, char **error) /*
  reads: alias, alias_len, error, fname, fname_len, is_data, options, pphar; writes: pphar*; returns: return FAILURE; | return SUCCESS; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE;

SLICE around line 1465 (def-use, level 2; '>' marks the seed):
zend_result phar_create_or_parse_filename(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_archive_data** pphar, char **error) /* {
   ...
   zend_string *actual = NULL;
   ...
   if(actual) {
     fname = ZSTR_VAL(actual);
     fname_len = ZSTR_LEN(actual);
   }
   ...
   phar_archive_data *mydata = ecalloc(1, sizeof(phar_archive_data));
   mydata->fname = expand_filepath(fname, NULL);
   ...
   fname_len = strlen(mydata->fname);
   ...
   if(is_data) {
     alias = NULL;
     alias_len = 0;
   ...
   } else {
     phar_archive_data *fd_ptr;
     if(alias && NULL !=(fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
>      if(SUCCESS != phar_free_alias(fd_ptr, alias, alias_len)) {
         spprintf(error, 4096, "phar error: phar \"%s\" cannot set alias \"%s\", already in use by another phar archive", mydata->fname, alias);
         zend_hash_str_del(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len);
         *pphar = NULL;
         return FAILURE;
   ...
       }
     }
   }
}

CALLEES (22):
  php_check_open_basedir (main/fopen_wrappers.c:282): reads path; writes -; returns return php_check_open_basedir_ex(path, 1);
  zend_string_release_ex (Zend/zend_string.h:343): reads persistent, s; writes -; returns -
  phar_open_from_fp (ext/phar/phar.c:1564): reads alias, alias_len, error, fname, fname_len, fp, pphar; writes error*; returns return phar_parse_zipfile(fp, fname, fname_len, alias, alias_len, pphar, error); | return phar_parse_tarfile(fp, fname, fname_len, alias, alias_len, pphar, compression, error); | return phar_parse_pharfile(fp, fname, fname_len, alias, alias_len, halt_offset, pphar, compression, error);
  expand_filepath (main/fopen_wrappers.c:770): reads filepath, real_path; writes -; returns return expand_filepath_ex(filepath, real_path, NULL, 0);
  phar_request_initialize (ext/phar/phar.c:3331): reads -; writes -; returns -
  zend_hash_str_add_ptr (Zend/zend_hash.h:693): reads ht, len, pData, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  zend_hash_str_del (Zend/zend_hash.c:1676): reads ht, len, str; writes -; returns return SUCCESS; | return FAILURE;
  phar_free_alias (ext/phar/util.c:932): reads phar; writes -; returns return FAILURE; | return FAILURE; | return SUCCESS;
  zend_hash_str_find_ptr (Zend/zend_hash.h:915): reads ht, len, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  php_stream_open_wrapper [macro]: #define php_stream_open_wrapper(path, mode, options, opened) _php_stream_open_wrapper_ex((path), (mode), (options), (opened), NULL STREAMS_CC)
  ZSTR_LEN [macro]: #define ZSTR_LEN(zstr) (zstr)->len
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  spprintf [macro]: #define spprintf zend_spprintf
  ecalloc [macro]: #define ecalloc(nmemb, size) _ecalloc((nmemb), (size) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  zend_hash_init [macro]: #define zend_hash_init(ht, nSize, pHashFunction, pDestructor, persistent) \
  estrndup [macro]: #define estrndup(s, length) _estrndup((s), (length) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  ZEND_ASSERT [macro (1 of 3 definitions)]: # define ZEND_ASSERT(c) ZEND_ASSUME(c)
  not defined in this repository: PHAR_G, phar_unixify_path_separators, strrchr, memchr

CALLERS (0):
```

- `get_context_at(file=ext/phar/tar.c, line=666, version=old)` →

```
phar_parse_tarfile — ext/phar/tar.c:200 [function] zend_result phar_parse_tarfile(php_stream* fp, char *fname, size_t fname_len, char *alias, size_t alias_len, phar_archive_data** pphar, uint32_t compression, char **error) /*
  reads: alias, alias_len, compression, error, fname, fname_len, fp, pphar; writes: error*, pphar*; returns: return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE;

SLICE around line 666 (def-use, level 2; '>' marks the seed):
zend_result phar_parse_tarfile(php_stream* fp, char *fname, size_t fname_len, char *alias, size_t alias_len, phar_archive_data** pphar, uint32_t compression, char **error) /* {
   char buf[512], *actual_alias = NULL, *p;
   phar_entry_info entry = {0};
   ...
   tar_header *hdr;
   ...
   phar_archive_data *myphar, *actual;
   bool last_was_longlink = false;
   ...
   hdr =(tar_header*)buf;
   old =(memcmp(hdr->magic, "ustar", sizeof("ustar")-1)!= 0);
   myphar =(phar_archive_data *)pecalloc(1, sizeof(phar_archive_data), PHAR_G(persist));
   myphar->is_persistent = PHAR_G(persist);
   ...
   myphar->is_tar = 1;
   myphar->flags = compression;
   ...
   while(true) {
   ...
     hdr =(tar_header*)buf;
   ...
     if(old && sum2 != sum1) {
   ...
       if(sum3 == sum1) {
   ...
         old = 0;
       }
     }
     size = entry.uncompressed_filesize = entry.compressed_filesize = phar_tar_number(hdr->size, sizeof(hdr->size));
     if(!old &&(hdr->typeflag == TAR_GLOBAL_HDR || hdr->typeflag == TAR_FILE_HDR)) {
       size =(size+511)&~511;
   ...
     }
     if(((!old && hdr->prefix[0] == 0)|| old)&& zend_strnlen(hdr->name, 100)== sizeof(".phar/signature.bin")-1 && !strncmp(hdr->name, ".phar/signature.bin", sizeof(".phar/signature.bin")-1)) {
   ...
       size_t sig_len;
   ...
       #ifdef ...
       # ...
       #else None
       # ...
       #endif
       myphar->sig_flags = PHAR_GET_32(buf);
   ...
       myphar->sig_len = sig_len;
   ...
       hdr =(tar_header*)buf;
   ...
     }
     if(!last_was_longlink && hdr->typeflag == 'L') {
   ...
       entry.filename = zend_string_alloc(entry.uncompressed_filesize, myphar->is_persistent);
   ...
       size =((size+511)&~511)- size;
   ...
     } else if(!last_was_longlink && !old && hdr->prefix[0] != 0) {
       char name[256];
   ...
       for(j = 0; j < 100; j++) {
         name[i+j] = hdr->name[j];
   ...
       }
       uint32_t filename_len = i + j;
       if(name[filename_len - 1] == '/') {
         filename_len--;
       }
       entry.filename = zend_string_init(name, filename_len, myphar->is_persistent);
   ...
     } else if(!last_was_longlink) {
   ...
       for(filename_len = 0; filename_len < 100; filename_len++) {
   ...
       }
       if(filename_len > 0 && hdr->name[filename_len - 1] == '/') {
         filename_len--;
       }
       entry.filename = zend_string_init(hdr->name, filename_len, myphar->is_persistent);
   ...
     }
   ...
     if(!actual_alias && zend_string_equals_literal(entry.filename, ".phar/alias.txt")) {
   ...
       read = php_stream_read(fp, buf, size);
       if(read == size) {
         buf[size] = '\0';
         if(!phar_validate_alias(buf, size)) {
           if(size > 50) {
             buf[50] = '.';
             buf[51] = '.';
             buf[52] = '.';
             buf[53] = '\0';
   ...
           }
         }
         actual_alias = pestrndup(buf, size, myphar->is_persistent);
         myphar->alias = actual_alias;
         myphar->alias_len = size;
   ...
       } else {
       }
     }
   }
   if(zend_hash_str_exists(&(myphar->manifest), ".phar/stub.php", sizeof(".phar/stub.php")-1)) {
     myphar->is_data = 0;
   } else {
     myphar->is_data = 1;
   }
   ...
   myphar->fname = pestrndup(fname, fname_len, myphar->is_persistent);
   ...
   myphar->fname_len = fname_len;
   myphar->fp = fp;
   p = strrchr(myphar->fname, '/');
   if(p) {
     myphar->ext = memchr(p, '.', (myphar->fname + fname_len)- p);
     if(myphar->ext == p) {
       myphar->ext = memchr(p + 1, '.', (myphar->fname + fname_len)- p - 1);
     }
     if(myphar->ext) {
       myphar->ext_len =(myphar->fname + fname_len)- myphar->ext;
     }
   }
   ...
   if(NULL ==(actual = zend_hash_str_add_ptr(&(PHAR_G(phar_fname_map)), myphar->fname, fname_len, myphar))) {
   ...
   }
   myphar = actual;
   if(actual_alias) {
     phar_archive_data *fd_ptr;
   ...
     if(NULL !=(fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), actual_alias, myphar->alias_len))) {
>      if(SUCCESS != phar_free_alias(fd_ptr, actual_alias, myphar->alias_len)) {
         if(error) {
   ...
         }
         zend_hash_str_del(&(PHAR_G(phar_fname_map)), myphar->fname, fname_len);
         return FAILURE;
   ...
       }
     }
   }
}

CALLEES (42):
  phar_validate_alias (ext/phar/phar_internal.h:374): reads alias, alias_len; writes -; returns return !(memchr(alias, '/', alias_len)|| memchr(alias, '\\', alias_len)|| memchr(alias, ':', alias_len)|| memchr(alias, ';', alias_len)|| memchr(alias, '\n', alias_len)|| memchr(alias, '\r', alias_len));
  phar_tar_process_metadata (ext/phar/tar.c:158): reads entry, fp; writes entry*; returns return FAILURE; | return FAILURE; | return FAILURE; | return SUCCESS;
  zend_hash_update_mem (Zend/zend_hash.h:793): reads ht, key, pData, size; writes -; returns return zend_hash_update_ptr(ht, key, p);
  phar_set_inode (ext/phar/phar_internal.h:381): reads entry; writes entry*; returns -
  zend_string_release_ex (Zend/zend_string.h:343): reads persistent, s; writes -; returns -
  zend_hash_str_exists (Zend/zend_hash.h:240): reads ht, len, str; writes -; returns return zend_hash_str_find(ht, str, len)!= NULL;
  zend_strnlen (Zend/zend_operators.h:293): reads maxlen, s; writes -; returns return strnlen(s, maxlen); | return p ? p-s : maxlen;
  phar_tar_number (ext/phar/tar.c:21): reads buf, len; writes -; returns return num;
  phar_add_virtual_dirs (ext/phar/util.c:1962): reads filename, filename_len, phar; writes phar*; returns -
  zend_string_init (Zend/zend_string.h:186): reads len, persistent, str; writes -; returns return ret;
  zend_string_free (Zend/zend_string.h:318): reads s; writes -; returns -
  zend_string_alloc (Zend/zend_string.h:164): reads len, persistent; writes -; returns return ret;
  phar_tar_checksum (ext/phar/tar.c:88): reads buf, len; writes -; returns return sum;
  phar_verify_signature (ext/phar/util.c:1476): reads end_of_phar, error, fname, fp, sig, sig_len, sig_type, signature, signature_len; writes error*, signature_len*; returns return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE;
  phar_request_initialize (ext/phar/phar.c:3331): reads -; writes -; returns -
  zend_hash_str_add_ptr (Zend/zend_hash.h:693): reads ht, len, pData, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  zend_hash_str_del (Zend/zend_hash.c:1676): reads ht, len, str; writes -; returns return SUCCESS; | return FAILURE;
  phar_free_alias (ext/phar/util.c:932): reads phar; writes -; returns return FAILURE; | return FAILURE; | return SUCCESS;
  zend_hash_str_find_ptr (Zend/zend_hash.h:915): reads ht, len, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  php_stream_seek [macro]: #define php_stream_seek(stream, offset, whence) _php_stream_seek((stream), (offset), (whence))
  php_stream_tell [macro]: #define php_stream_tell(stream) _php_stream_tell((stream))
  php_stream_read [macro]: #define php_stream_read(stream, buf, count) _php_stream_read((stream), (buf), (count))
  php_stream_close [macro]: #define php_stream_close(stream) _php_stream_free((stream), PHP_STREAM_FREE_CLOSE)
  spprintf [macro]: #define spprintf zend_spprintf
  pecalloc [macro]: #define pecalloc(nmemb, size, persistent) ((persistent)?__zend_calloc((nmemb), (size) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC):ecalloc((nmemb), (size)))
  zend_hash_init [macro]: #define zend_hash_init(ht, nSize, pHashFunction, pDestructor, persistent) \
  pestrndup [macro]: #define pestrndup(s, length, persistent) ((persistent)?zend_strndup((s),(length)):estrndup((s),(length)))
  zend_string_equals_literal [macro]: #define zend_string_equals_literal(str, literal) \
  ZSTR_VAL [macro]: #define ZSTR_VAL(zstr) (zstr)->val
  zend_string_starts_with_literal [macro]: #define zend_string_starts_with_literal(str, prefix) \
  not defined in this repository: PHAR_G, phar_destroy_phar_data, phar_unixify_path_separators, strrchr, memchr
  not shown (7): ZEND_ASSERT, estrndup, S_ISDIR, ZSTR_LEN, GC_MAKE_PERSISTENT_LOCAL, efree, PHAR_GET_32

CALLERS (1):
  phar_open_from_fp (ext/phar/phar.c:1722): return phar_parse_tarfile(fp, fname, fname_len, alias, alias_len, pphar, compression, error);
```

- `get_context_at(file=ext/phar/util.c, line=1006, version=old)` →

```
phar_get_archive — ext/phar/util.c:955 [function] zend_result phar_get_archive(phar_archive_data **archive, char *fname, size_t fname_len, char *alias, size_t alias_len, char **error) /*
  reads: alias, alias_len, archive, error, fname, fname_len; writes: archive*, error*; returns: return FAILURE; | return SUCCESS; | return FAILURE; | return SUCCESS; | return FAILURE; | return SUCCESS;

SLICE around line 1006 (def-use, level 2; '>' marks the seed):
zend_result phar_get_archive(phar_archive_data **archive, char *fname, size_t fname_len, char *alias, size_t alias_len, char **error) /* {
   phar_archive_data *fd, *fd_ptr;
   ...
   if(PHAR_G(last_phar)&& fname_len == PHAR_G(last_phar_name_len)&& !memcmp(fname, PHAR_G(last_phar_name), fname_len)) {
   ...
     if(alias && alias_len) {
   ...
       if(PHAR_G(last_phar)->alias_len && NULL !=(fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), PHAR_G(last_phar)->alias, PHAR_G(last_phar)->alias_len))) {
   ...
       }
     }
   }
   if(alias && alias_len && PHAR_G(last_phar)&& alias_len == PHAR_G(last_alias_len)&& !memcmp(alias, PHAR_G(last_alias), alias_len)) {
     fd = PHAR_G(last_phar);
     fd_ptr = fd;
   ...
   }
   if(alias && alias_len) {
     if(NULL !=(fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), alias, alias_len))) {
   ...
       if(fname &&(fname_len != fd_ptr->fname_len || strncmp(fname, fd_ptr->fname, fname_len))) {
   ...
>        if(SUCCESS == phar_free_alias(fd_ptr, alias, alias_len)) {
           if(error) {
   ...
           }
         }
       }
     }
   }
}

CALLEES (10):
  phar_request_initialize (ext/phar/phar.c:3331): reads -; writes -; returns -
  zend_hash_str_add_ptr (Zend/zend_hash.h:693): reads ht, len, pData, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  zend_hash_str_del (Zend/zend_hash.c:1676): reads ht, len, str; writes -; returns return SUCCESS; | return FAILURE;
  zend_hash_str_find_ptr (Zend/zend_hash.h:915): reads ht, len, str; writes -; returns return Z_PTR_P(zv); | return NULL;
  phar_free_alias (ext/phar/util.c:932): reads phar; writes -; returns return FAILURE; | return FAILURE; | return SUCCESS;
  expand_filepath (main/fopen_wrappers.c:770): reads filepath, real_path; writes -; returns return expand_filepath_ex(filepath, real_path, NULL, 0);
  spprintf [macro]: #define spprintf zend_spprintf
  efree [macro]: #define efree(ptr) _efree((ptr) ZEND_FILE_LINE_CC ZEND_FILE_LINE_EMPTY_CC)
  not defined in this repository: PHAR_G, phar_unixify_path_separators

CALLERS (7):
  phar_wrapper_open_dir (ext/phar/dirstream.c:279): if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
  phar_wrapper_mkdir (ext/phar/dirstream.c:358): if (FAILURE == phar_get_archive(&phar, arch, arch_len, NULL, 0, NULL)) {
  phar_wrapper_mkdir (ext/phar/dirstream.c:386): if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
  phar_wrapper_rmdir (ext/phar/dirstream.c:484): if (FAILURE == phar_get_archive(&phar, arch, arch_len, NULL, 0, NULL)) {
  phar_wrapper_rmdir (ext/phar/dirstream.c:512): if (FAILURE == phar_get_archive(&phar, ZSTR_VAL(resource->host), ZSTR_LEN(resource->host), NULL, 0, &error)) {
  phar_get_name_for_relative_paths (ext/phar/func_interceptors.c:104): if (FAILURE == phar_get_archive(&phar, arch, arch_len, NULL, 0, NULL)) {
  phar_file_stat (ext/phar/func_interceptors.c:499): zend_result has_archive = phar_get_archive(&phar, arch, arch_len, NULL, 0, NULL);
  ... only the first 8 of 22 reference sites were followed
```

- `get_context_at(file=ext/phar/zip.c, line=743, version=old)` →

```
phar_parse_zipfile — ext/phar/zip.c:227 [function] zend_result phar_parse_zipfile(php_stream *fp, char *fname, size_t fname_len, char *alias, size_t alias_len, phar_archive_data** pphar, char **error) /*
  reads: alias, alias_len, error, fname, fname_len, fp, pphar; writes: fp*, pphar*; returns: return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE; | return FAILURE;

SLICE around line 743 (def-use, level 2; '>' marks the seed):
zend_result phar_parse_zipfile(php_stream *fp, char *fname, size_t fname_len, char *alias, size_t alias_len, phar_archive_data** pphar, char **error) /* {
   ...
   phar_archive_data *mydata = NULL;
   phar_entry_info entry = {0};
   char *ext, *actual_alias = NULL;
   ...
   char *p = phar_find_eocd(buf, size);
   ...
   memcpy((void *)&locator, (void *)p, sizeof(locator));
   ...
   mydata = pecalloc(1, sizeof(phar_archive_data), PHAR_G(persist));
   mydata->is_persistent = PHAR_G(persist);
   ...
   mydata->fname = pestrndup(fname, fname_len, mydata->is_persistent);
   ...
   entry.is_persistent = mydata->is_persistent;
   ...
   for(i = 0; i < PHAR_GET_16(locator.count); ++i) {
     phar_zip_central_dir_file zipentry;
   ...
     entry.uncompressed_filesize = PHAR_GET_32(zipentry.uncompsize);
   ...
     entry.flags = PHAR_ENT_PERM_DEF_FILE;
   ...
     uint32_t filename_len = PHAR_GET_16(zipentry.filename_len);
     entry.filename = zend_string_alloc(filename_len, entry.is_persistent);
   ...
     if(ZSTR_VAL(entry.filename)[filename_len - 1] == '/') {
   ...
       entry.flags |= PHAR_ENT_PERM_DEF_DIR;
     } else {
     }
   ...
     switch(PHAR_GET_16(zipentry.compressed)) {
   ...
       case PHAR_ZIP_COMP_DEFLATE : entry.flags |= PHAR_ENT_COMPRESSED_GZ; if(!PHAR_G(has_zlib)) {
       entry.flags |= PHAR_ENT_COMPRESSED_GZ;
   ...
       }
       case PHAR_ZIP_COMP_BZIP2 : entry.flags |= PHAR_ENT_COMPRESSED_BZ2; if(!PHAR_G(has_bz2)) {
       entry.flags |= PHAR_ENT_COMPRESSED_BZ2;
   ...
       }
     }
   ...
     if(!actual_alias && zend_string_equals_literal(entry.filename, ".phar/alias.txt")) {
   ...
       mydata->alias_len = entry.uncompressed_filesize;
       if(entry.flags & PHAR_ENT_COMPRESSED_GZ) {
   ...
           zend_string *str = php_stream_copy_to_mem(fp, entry.uncompressed_filesize, 0);
           if(str) {
             entry.uncompressed_filesize = ZSTR_LEN(str);
             actual_alias = estrndup(ZSTR_VAL(str), ZSTR_LEN(str));
   ...
           } else {
             actual_alias = NULL;
             entry.uncompressed_filesize = 0;
   ...
           }
       } else if(entry.flags & PHAR_ENT_COMPRESSED_BZ2) {
   ...
           zend_string *str = php_stream_copy_to_mem(fp, entry.uncompressed_filesize, 0);
           if(str) {
             entry.uncompressed_filesize = ZSTR_LEN(str);
             actual_alias = estrndup(ZSTR_VAL(str), ZSTR_LEN(str));
   ...
           } else {
             actual_alias = NULL;
             entry.uncompressed_filesize = 0;
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
     phar_archive_data *fd_ptr;
   ...
     if(NULL !=(fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), actual_alias, mydata->alias_len))) {
>      if(SUCCESS != phar_free_alias(fd_ptr, actual_alias, mydata->alias_len)) {
         if(error) {
   ...
         }
         efree(actual_alias);
         zend_hash_str_del(&(PHAR_G(phar_fname_map)), mydata->fname, fname_len);
         return FAILURE;
   ...
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

### Turn 3  _(tok 20490+676, stop=tool_use)_

**Reasoning:** I need to check the enclosing function around phar_object.c:2708 since the context lookup didn't find one—possibly inside a macro or the parser missed it. I should also look at zip.c:765 and tar.c:681, which seem to be additional call sites within the same functions already identified (phar_parse_zipfile and phar_parse_tarfile).



**Says:** `get_context_at` could not resolve an enclosing function for `phar_object.c:2708`. I'll read that region directly, and check the second call sites in `tar.c` and `zip.c`.

- `read_file(path=ext/phar/phar_object.c, version=old, start_line=2640, end_line=2730)` →

```
ext/phar/phar_object.c lines 2640-2730 of 5059
 2640| /* }}} */
 2641| 
 2642| /* {{{ Returns the alias for the Phar or NULL. */
 2643| PHP_METHOD(Phar, getAlias)
 2644| {
 2645| 	ZEND_PARSE_PARAMETERS_NONE();
 2646| 
 2647| 	PHAR_ARCHIVE_OBJECT();
 2648| 
 2649| 	if (phar_obj->archive->alias && phar_obj->archive->alias != phar_obj->archive->fname) {
 2650| 		RETURN_STRINGL(phar_obj->archive->alias, phar_obj->archive->alias_len);
 2651| 	}
 2652| }
 2653| /* }}} */
 2654| 
 2655| /* {{{ Returns the real path to the phar archive on disk */
 2656| PHP_METHOD(Phar, getPath)
 2657| {
 2658| 	ZEND_PARSE_PARAMETERS_NONE();
 2659| 
 2660| 	PHAR_ARCHIVE_OBJECT();
 2661| 
 2662| 	RETURN_STRINGL(phar_obj->archive->fname, phar_obj->archive->fname_len);
 2663| }
 2664| /* }}} */
 2665| 
 2666| /* {{{ Sets the alias for a Phar archive. The default value is the full path
 2667|  * to the archive.
 2668|  */
 2669| PHP_METHOD(Phar, setAlias)
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
 2716| 	}
 2717| 	if (phar_obj->archive->is_persistent && FAILURE == phar_copy_on_write(&(phar_obj->archive))) {
 2718| 		zend_throw_exception_ex(phar_ce_PharException, 0, "phar \"%s\" is persistent, unable to copy on write", phar_obj->archive->fname);
 2719| 		RETURN_THROWS();
 2720| 	}
 2721| 	if (phar_obj->archive->alias_len && NULL != (fd_ptr = zend_hash_str_find_ptr(&(PHAR_G(phar_alias_map)), phar_obj->archive->alias, phar_obj->archive->alias_len))) {
 2722| 		zend_hash_str_del(&(PHAR_G(phar_alias_map)), phar_obj->archive->alias, phar_obj->archive->alias_len);
 2723| 		readd = true;
 2724| 	}
 2725| 
 2726| 	ZEND_ASSERT(!phar_obj->archive->is_persistent);
 2727| 
 2728| 	oldalias = phar_obj->archive->alias;
 2729| 	oldalias_len = phar_obj->archive->alias_len;
 2730| 	old_temp = phar_obj->archive->is_temporary_alias;
```

- `grep(pattern=^[a-zA-Z_].*\(|^PHP_METHOD|^PHP_FUNCTION, version=old, path_glob=ext/phar/phar_object.c, max_results=400)` →

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

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 4  _(tok 27574+266, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "phar_parse_pharfile", "file": "ext/phar/phar.c"}, {"function": "phar_create_or_parse_filename", "file": "ext/phar/phar.c"}, {"function": "phar_parse_tarfile", "file": "ext/phar/tar.c"}, {"function": "phar_get_archive", "file": "ext/phar/util.c"}, {"function": "phar_parse_zipfile", "file": "ext/phar/zip.c"}, {"function": "PHP_METHOD(Phar, setAlias)", "file": "ext/phar/phar_object.c"}], "confidence_overall": "medium"}`

**Score (tool):** `{"n_pred": 6, "n_truth": 5, "tp": 5, "precision": 0.8333333333333334, "recall": 1.0, "f1": 0.9090909090909091}`

## Semantic arm

### Turn 1  _(tok 3200+76, stop=tool_use)_

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

### Turn 2  _(tok 3654+314, stop=tool_use)_

**Reasoning:** The result shows version "old," which seems to default to the parent commit rather than the current work tree state. Since what matters here is the current code where the signature change is happening, I should check again using version "work" instead.



**Says:** The default lookup returned the "old" version. I'll check the working tree too, since that's the code that will actually need updating.

- `get_callers(name=phar_free_alias, limit=200, rev=HEAD)` →

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

- `resolve_symbol(name=phar_free_alias)` →

```
{
  "resolved": true,
  "name": "phar_free_alias",
  "version": "old",
  "file": "ext/phar/util.c",
  "line": 932,
  "kind": "function",
  "signature": "zend_result phar_free_alias(phar_archive_data *phar, char *alias, size_t alias_len) /*",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 3  _(tok 4542+246, stop=tool_use)_

**Reasoning:** I'm wondering if version is always "old," or if the server's commit is the parent—let me try version "work" instead to check the working tree.



**Says:** Both calls still report "old", so I'll query the working tree explicitly to confirm the current call sites.

- `get_callers(name=phar_free_alias, limit=200, rev=work)` →

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

- `resolve_symbol(name=phar_free_alias, rev=work)` →

```
{
  "resolved": true,
  "name": "phar_free_alias",
  "version": "old",
  "file": "ext/phar/util.c",
  "line": 932,
  "kind": "function",
  "signature": "zend_result phar_free_alias(phar_archive_data *phar, char *alias, size_t alias_len) /*",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 4  _(tok 5362+453, stop=tool_use)_

**Reasoning:** The results look consistent across versions, and the caller list from the call graph seems reliable enough. I'll finalize with six unique functions: phar_parse_pharfile and phar_create_or_parse_filename in phar.c, phar_parse_tarfile in tar.c, phar_get_archive in util.c, and the remaining phar_parse variant.



- **submit_callers** → `{"callers": [{"function": "phar_parse_pharfile", "file": "ext/phar/phar.c"}, {"function": "phar_create_or_parse_filename", "file": "ext/phar/phar.c"}, {"function": "phar_parse_tarfile", "file": "ext/phar/tar.c"}, {"function": "phar_get_archive", "file": "ext/phar/util.c"}, {"function": "phar_parse_zipfile", "file": "ext/phar/zip.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

