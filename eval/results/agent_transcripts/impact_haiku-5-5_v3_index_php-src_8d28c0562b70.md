# Impact-analysis transcript — php-src @ 8d28c0562b70 — anthropic:claude-haiku-5-5

- target: `phar_split_fname` (ext/phar/phar.c), arity 7->5
- truth: [['ext/phar/dirstream.c', 'phar_wrapper_mkdir'], ['ext/phar/dirstream.c', 'phar_wrapper_rmdir'], ['ext/phar/func_interceptors.c', 'PHP_FUNCTION(phar_is_file)'], ['ext/phar/func_interceptors.c', 'PHP_FUNCTION(phar_is_link)'], ['ext/phar/func_interceptors.c', 'PHP_FUNCTION(phar_opendir)'], ['ext/phar/func_interceptors.c', 'phar_file_stat'], ['ext/phar/func_interceptors.c', 'phar_get_name_for_relative_paths'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, __construct)'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, mount)'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, running)'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, unlinkArchive)'], ['ext/phar/phar_object.c', 'PHP_METHOD(PharFileInfo, __construct)'], ['ext/phar/stream.c', 'phar_parse_url'], ['ext/phar/util.c', 'phar_find_in_include_path']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1383+141, stop=tool_use)_

**Reasoning:** I'm going to look up where this symbol is used, starting with a find_references call.



- `find_references(name=phar_split_fname)` →

```
17 references
phar_split_fname  353 ext/phar/dirstream.c 	if (FAILURE == phar_split_fname(url_from, strlen(url_from), &arch, &arch_len, NULL, 2, 2)) {
phar_split_fname  479 ext/phar/dirstream.c 	if (FAILURE == phar_split_fname(url, strlen(url), &arch, &arch_len, NULL, 2, 2)) {
phar_split_fname   51 ext/phar/func_interceptors.c 		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
phar_split_fname   97 ext/phar/func_interceptors.c 	if (FAILURE == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
phar_split_fname  497 ext/phar/func_interceptors.c 		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
phar_split_fname  734 ext/phar/func_interceptors.c 		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
phar_split_fname  792 ext/phar/func_interceptors.c 		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
phar_split_fname  477 ext/phar/phar_internal.h zend_result phar_split_fname(const char *filename, size_t filename_len, char **arch, size_t *arch_len, zend_string **entry, int executable, int for_creat
phar_split_fname  422 ext/phar/phar_object.c 		&& SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)
phar_split_fname  480 ext/phar/phar_object.c 	if (fname_len > 7 && !memcmp(fname, "phar://", 7) && SUCCESS == phar_split_fname(fname, fname_len, &arch, &arch_len, NULL, 2, 0)) {
phar_split_fname  524 ext/phar/phar_object.c 	} else if (SUCCESS == phar_split_fname(path, path_len, &arch, &arch_len, &entry, 2, 0)) {
phar_split_fname 1111 ext/phar/phar_object.c 	if (SUCCESS == phar_split_fname(fname, fname_len, &arch, &arch_len, &entry, !is_data, 2)) {
phar_split_fname 1292 ext/phar/phar_object.c 		&& SUCCESS == phar_split_fname(ZSTR_VAL(zend_file_name), ZSTR_LEN(zend_file_name), &arch, &arch_len, NULL, 2, 0)
phar_split_fname 4417 ext/phar/phar_object.c 	if (fname_len < 7 || memcmp(fname, "phar://", 7) || phar_split_fname(fname, fname_len, &arch, &arch_len, &entry, 2, 0) == FAILURE) {
phar_split_fname   74 ext/phar/stream.c 	if (phar_split_fname(filename, strlen(filename), &arch, &arch_len, &entry, 2, (mode[0] == 'w' ? 2 : 0)) == FAILURE) {
phar_split_fname  303 ext/phar/util.c  	if (!is_file_a_phar_wrapper || SUCCESS != phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 1, 0)) {
phar_split_fname  347 ext/phar/util.c  		if (SUCCESS != phar_split_fname(ZSTR_VAL(ret), ZSTR_LEN(ret), &arch, &arch_len, NULL, 1, 0)) {
```

- `grep(pattern=phar_split_fname, version=old)` →

```
18 matches
ext/phar/dirstream.c:353:	if (FAILURE == phar_split_fname(url_from, strlen(url_from), &arch, &arch_len, NULL, 2, 2)) {
ext/phar/dirstream.c:479:	if (FAILURE == phar_split_fname(url, strlen(url), &arch, &arch_len, NULL, 2, 2)) {
ext/phar/func_interceptors.c:51:		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
ext/phar/func_interceptors.c:97:	if (FAILURE == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
ext/phar/func_interceptors.c:497:		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
ext/phar/func_interceptors.c:734:		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
ext/phar/func_interceptors.c:792:		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
ext/phar/phar.c:2167:zend_result phar_split_fname(const char *filename, size_t filename_len, char **arch, size_t *arch_len, zend_string **entry, int executable, int for_create) /* {{{ */
ext/phar/phar_internal.h:477:zend_result phar_split_fname(const char *filename, size_t filename_len, char **arch, size_t *arch_len, zend_string **entry, int executable, int for_create);
ext/phar/phar_object.c:422:		&& SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)
ext/phar/phar_object.c:480:	if (fname_len > 7 && !memcmp(fname, "phar://", 7) && SUCCESS == phar_split_fname(fname, fname_len, &arch, &arch_len, NULL, 2, 0)) {
ext/phar/phar_object.c:524:	} else if (SUCCESS == phar_split_fname(path, path_len, &arch, &arch_len, &entry, 2, 0)) {
ext/phar/phar_object.c:1111:	if (SUCCESS == phar_split_fname(fname, fname_len, &arch, &arch_len, &entry, !is_data, 2)) {
ext/phar/phar_object.c:1292:		&& SUCCESS == phar_split_fname(ZSTR_VAL(zend_file_name), ZSTR_LEN(zend_file_name), &arch, &arch_len, NULL, 2, 0)
ext/phar/phar_object.c:4417:	if (fname_len < 7 || memcmp(fname, "phar://", 7) || phar_split_fname(fname, fname_len, &arch, &arch_len, &entry, 2, 0) == FAILURE) {
ext/phar/stream.c:74:	if (phar_split_fname(filename, strlen(filename), &arch, &arch_len, &entry, 2, (mode[0] == 'w' ? 2 : 0)) == FAILURE) {
ext/phar/util.c:303:	if (!is_file_a_phar_wrapper || SUCCESS != phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 1, 0)) {
ext/phar/util.c:347:		if (SUCCESS != phar_split_fname(ZSTR_VAL(ret), ZSTR_LEN(ret), &arch, &arch_len, NULL, 1, 0)) {
```

### Turn 2  _(tok 4516+850, stop=tool_use)_

**Reasoning:** I need to find the enclosing function for each call site, so I'll read about 60 lines before each one. The call sites are in dirstream.c, func_interceptors.c, phar_object.c, stream.c, and util.c.

I'm going to read the files in parallel to cover the remaining call sites.



**Says:** The grep and the index agree on 17 references (one is the definition in phar.c and one the prototype in phar_internal.h). I need the enclosing function for each call site, so I'll read the surrounding code.

- `read_file(path=ext/phar/dirstream.c, version=old, start_line=320, end_line=355)` →

```
ext/phar/dirstream.c lines 320-355 of 588
  320| 		php_url_free(resource);
  321| 		return ret;
  322| 	} else {
  323| 		zend_string *str_key;
  324| 
  325| 		/* search for directory */
  326| 		ZEND_HASH_MAP_FOREACH_STR_KEY(&phar->manifest, str_key) {
  327| 			if (zend_string_starts_with_cstr(str_key, internal_file, internal_file_len)) {
  328| 				/* directory found */
  329| 				ret = phar_make_dirstream(internal_file, internal_file_len, &phar->manifest);
  330| 				php_url_free(resource);
  331| 				return ret;
  332| 			}
  333| 		} ZEND_HASH_FOREACH_END();
  334| 	}
  335| 
  336| 	php_url_free(resource);
  337| 	return NULL;
  338| }
  339| /* }}} */
  340| 
  341| /**
  342|  * Make a new directory within a phar archive
  343|  */
  344| int phar_wrapper_mkdir(php_stream_wrapper *wrapper, const char *url_from, int mode, int options, php_stream_context *context) /* {{{ */
  345| {
  346| 	phar_entry_info entry, *e;
  347| 	phar_archive_data *phar = NULL;
  348| 	char *error, *arch;
  349| 	size_t arch_len;
  350| 	php_url *resource = NULL;
  351| 
  352| 	/* pre-readonly check, we need to know if this is a data phar */
  353| 	if (FAILURE == phar_split_fname(url_from, strlen(url_from), &arch, &arch_len, NULL, 2, 2)) {
  354| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\", no phar archive specified", url_from);
  355| 		return 0;
```

- `read_file(path=ext/phar/dirstream.c, version=old, start_line=455, end_line=480)` →

```
ext/phar/dirstream.c lines 455-480 of 588
  455| 	if (error) {
  456| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\" in phar \"%s\", %s", ZSTR_VAL(entry.filename), phar->fname, error);
  457| 		zend_hash_del(&phar->manifest, entry.filename);
  458| 		efree(error);
  459| 		return 0;
  460| 	}
  461| 
  462| 	phar_add_virtual_dirs(phar, ZSTR_VAL(entry.filename), ZSTR_LEN(entry.filename));
  463| 	return 1;
  464| }
  465| /* }}} */
  466| 
  467| /**
  468|  * Remove a directory within a phar archive
  469|  */
  470| int phar_wrapper_rmdir(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
  471| {
  472| 	phar_entry_info *entry;
  473| 	phar_archive_data *phar = NULL;
  474| 	char *error, *arch;
  475| 	size_t arch_len;
  476| 	php_url *resource = NULL;
  477| 
  478| 	/* pre-readonly check, we need to know if this is a data phar */
  479| 	if (FAILURE == phar_split_fname(url, strlen(url), &arch, &arch_len, NULL, 2, 2)) {
  480| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot remove directory \"%s\", no phar archive specified, or phar archive does not exist", url);
```

- `read_file(path=ext/phar/func_interceptors.c, version=old, start_line=30, end_line=100)` →

```
ext/phar/func_interceptors.c lines 30-100 of 1000
   30| 
   31| 	if ((HT_IS_INITIALIZED(&PHAR_G(phar_fname_map)) && !zend_hash_num_elements(&(PHAR_G(phar_fname_map))))
   32| 		&& !HT_IS_INITIALIZED(&cached_phars)) {
   33| 		goto skip_phar;
   34| 	}
   35| 
   36| 	if (zend_parse_parameters(ZEND_NUM_ARGS(), "p|r!", &filename, &filename_len, &zcontext) == FAILURE) {
   37| 		RETURN_THROWS();
   38| 	}
   39| 
   40| 	if (!IS_ABSOLUTE_PATH(filename, filename_len) && !strstr(filename, "://")) {
   41| 		char *arch;
   42| 		size_t arch_len;
   43| 		zend_string *fname = zend_get_executed_filename_ex();
   44| 
   45| 		/* we are checking for existence of a file within the relative path.  Chances are good that this is
   46| 		   retrieving something from within the phar archive */
   47| 		if (!fname || !zend_string_starts_with_literal_ci(fname, "phar://")) {
   48| 			goto skip_phar;
   49| 		}
   50| 
   51| 		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
   52| 			php_stream_context *context = NULL;
   53| 			php_stream *stream;
   54| 			char *name;
   55| 
   56| 			/* fopen within phar, if :// is not in the url, then prepend phar://<archive>/ */
   57| 			/* retrieving a file within the current directory, so use this if possible */
   58| 			zend_string *entry = phar_fix_filepath(filename, filename_len, true);
   59| 
   60| 			if (ZSTR_VAL(entry)[0] == '/') {
   61| 				spprintf(&name, 4096, "phar://%s%s", arch, ZSTR_VAL(entry));
   62| 			} else {
   63| 				spprintf(&name, 4096, "phar://%s/%s", arch, ZSTR_VAL(entry));
   64| 			}
   65| 			zend_string_release_ex(entry, false);
   66| 			efree(arch);
   67| 			if (zcontext) {
   68| 				context = php_stream_context_from_zval(zcontext, 0);
   69| 			}
   70| 			stream = php_stream_opendir(name, REPORT_ERRORS, context);
   71| 			efree(name);
   72| 			if (!stream) {
   73| 				RETURN_FALSE;
   74| 			}
   75| 			php_stream_to_zval(stream, return_value);
   76| 			return;
   77| 		}
   78| 	}
   79| skip_phar:
   80| 	PHAR_G(orig_opendir)(INTERNAL_FUNCTION_PARAM_PASSTHRU);
   81| 	return;
   82| }
   83| /* }}} */
   84| 
   85| static zend_string* phar_get_name_for_relative_paths(zend_string *filename, bool using_include_path)
   86| {
   87| 	char *arch;
   88| 	size_t arch_len;
   89| 	zend_string *fname = zend_get_executed_filename_ex();
   90| 
   91| 	/* we are checking for existence of a file within the relative path.  Chances are good that this is
   92| 	   retrieving something from within the phar archive */
   93| 	if (!fname || !zend_string_starts_with_literal_ci(fname, "phar://")) {
   94| 		return NULL;
   95| 	}
   96| 
   97| 	if (FAILURE == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
   98| 		return NULL;
   99| 	}
  100| 
```

- `read_file(path=ext/phar/func_interceptors.c, version=old, start_line=470, end_line=500)` →

```
ext/phar/func_interceptors.c lines 470-500 of 1000
  470| 
  471| static void phar_file_stat(const char *filename, size_t filename_length, int type, zif_handler orig_stat_func, INTERNAL_FUNCTION_PARAMETERS) /* {{{ */
  472| {
  473| 	if (!filename_length) {
  474| 		RETURN_FALSE;
  475| 	}
  476| 
  477| 	if (!IS_ABSOLUTE_PATH(filename, filename_length) && !strstr(filename, "://")) {
  478| 		zend_string *fname;
  479| 		zend_stat_t sb = {0};
  480| 		phar_archive_data *phar;
  481| 
  482| 		fname = zend_get_executed_filename_ex();
  483| 
  484| 		/* we are checking for existence of a file within the relative path.  Chances are good that this is
  485| 		   retrieving something from within the phar archive */
  486| 		if (!fname || !zend_string_starts_with_literal_ci(fname, "phar://")) {
  487| 			goto skip_phar;
  488| 		}
  489| 
  490| 		if (PHAR_G(last_phar) && ZSTR_LEN(fname) - 7 >= PHAR_G(last_phar_name_len) && !memcmp(ZSTR_VAL(fname) + 7, PHAR_G(last_phar_name), PHAR_G(last_phar_name_len))) {
  491| 			/* fopen within phar, if :// is not in the url, then prepend phar://<archive>/ */
  492| 			phar = PHAR_G(last_phar);
  493| 			goto splitted;
  494| 		}
  495| 		char *arch;
  496| 		size_t arch_len;
  497| 		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
  498| 			/* fopen within phar, if :// is not in the url, then prepend phar://<archive>/ */
  499| 			zend_result has_archive = phar_get_archive(&phar, arch, arch_len, NULL, 0, NULL);
  500| 			efree(arch);
```

- `read_file(path=ext/phar/func_interceptors.c, version=old, start_line=700, end_line=800)` →

```
ext/phar/func_interceptors.c lines 700-800 of 1000
  700| PharFileFunction(phar_file_exists, FS_EXISTS, orig_file_exists)
  701| /* }}} */
  702| 
  703| /* {{{ Returns true if file is directory */
  704| PharFileFunction(phar_is_dir, FS_IS_DIR, orig_is_dir)
  705| /* }}} */
  706| 
  707| PHP_FUNCTION(phar_is_file) /* {{{ */
  708| {
  709| 	char *filename;
  710| 	size_t filename_len;
  711| 
  712| 	if (!PHAR_G(intercepted)) {
  713| 		goto skip_phar;
  714| 	}
  715| 
  716| 	if ((HT_IS_INITIALIZED(&PHAR_G(phar_fname_map)) && !zend_hash_num_elements(&(PHAR_G(phar_fname_map))))
  717| 		&& !HT_IS_INITIALIZED(&cached_phars)) {
  718| 		goto skip_phar;
  719| 	}
  720| 	if (zend_parse_parameters_ex(ZEND_PARSE_PARAMS_QUIET, ZEND_NUM_ARGS(), "p", &filename, &filename_len) == FAILURE) {
  721| 		goto skip_phar;
  722| 	}
  723| 	if (!IS_ABSOLUTE_PATH(filename, filename_len) && !strstr(filename, "://")) {
  724| 		char *arch;
  725| 		size_t arch_len;
  726| 		zend_string *fname = zend_get_executed_filename_ex();
  727| 
  728| 		/* we are checking for existence of a file within the relative path.  Chances are good that this is
  729| 		   retrieving something from within the phar archive */
  730| 		if (!fname || !zend_string_starts_with_literal_ci(fname, "phar://")) {
  731| 			goto skip_phar;
  732| 		}
  733| 
  734| 		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
  735| 			phar_archive_data *phar;
  736| 
  737| 			/* fopen within phar, if :// is not in the url, then prepend phar://<archive>/ */
  738| 			/* retrieving a file within the current directory, so use this if possible */
  739| 			if (SUCCESS == phar_get_archive(&phar, arch, arch_len, NULL, 0, NULL)) {
  740| 				phar_entry_info *etemp;
  741| 
  742| 				zend_string *entry = phar_fix_filepath(filename, filename_len, true);
  743| 				if (ZSTR_VAL(entry)[0] == '/') {
  744| 					etemp = zend_hash_str_find_ptr(&(phar->manifest), ZSTR_VAL(entry) + 1, ZSTR_LEN(entry) - 1);
  745| 				} else {
  746| 					etemp = zend_hash_find_ptr(&(phar->manifest), entry);
  747| 				}
  748| 				zend_string_release_ex(entry, false);
  749| 				if (etemp) {
  750| 					efree(arch);
  751| 					RETURN_BOOL(!etemp->is_dir);
  752| 				}
  753| 				/* this file is not in the current directory, use the original path */
  754| 			}
  755| 			efree(arch);
  756| 			RETURN_FALSE;
  757| 		}
  758| 	}
  759| skip_phar:
  760| 	PHAR_G(orig_is_file)(INTERNAL_FUNCTION_PARAM_PASSTHRU);
  761| 	return;
  762| }
  763| /* }}} */
  764| 
  765| PHP_FUNCTION(phar_is_link) /* {{{ */
  766| {
  767| 	char *filename;
  768| 	size_t filename_len;
  769| 
  770| 	if (!PHAR_G(intercepted)) {
  771| 		goto skip_phar;
  772| 	}
  773| 
  774| 	if ((HT_IS_INITIALIZED(&PHAR_G(phar_fname_map)) && !zend_hash_num_elements(&(PHAR_G(phar_fname_map))))
  775| 		&& !HT_IS_INITIALIZED(&cached_phars)) {
  776| 		goto skip_phar;
  777| 	}
  778| 	if (zend_parse_parameters_ex(ZEND_PARSE_PARAMS_QUIET, ZEND_NUM_ARGS(), "p", &filename, &filename_len) == FAILURE) {
  779| 		goto skip_phar;
  780| 	}
  781| 	if (!IS_ABSOLUTE_PATH(filename, filename_len) && !strstr(filename, "://")) {
  782| 		char *arch;
  783| 		size_t arch_len;
  784| 		zend_string *fname = zend_get_executed_filename_ex();
  785| 
  786| 		/* we are checking for existence of a file within the relative path.  Chances are good that this is
  787| 		   retrieving something from within the phar archive */
  788| 		if (!fname || !zend_string_starts_with_literal_ci(fname, "phar://")) {
  789| 			goto skip_phar;
  790| 		}
  791| 
  792| 		if (SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)) {
  793| 			phar_archive_data *phar;
  794| 
  795| 			/* fopen within phar, if :// is not in the url, then prepend phar://<archive>/ */
  796| 			/* retrieving a file within the current directory, so use this if possible */
  797| 			if (SUCCESS == phar_get_archive(&phar, arch, arch_len, NULL, 0, NULL)) {
  798| 				phar_entry_info *etemp;
  799| 
  800| 				zend_string *entry = phar_fix_filepath(filename, filename_len, true);
```

### Turn 3  _(tok 11147+1238, stop=tool_use)_

**Reasoning:** I need to find the function enclosing line 51 of func_interceptors.c, probably the opendir handler around lines 20-30, so I'll check lines 15-30. I also have line markers to note: line 97 is phar_get_name_for_relative_paths, line 497 is phar_file_stat, and lines 734 and 792 are phar_is_file and phar_is_link.

I still need line 51, so I'll read lines 15-30 to pin down its enclosing function. I also have the phar_wrapper_mkdir and phar_wrapper_rmdir locations at lines 353 and 479, and after that I'll move on to phar_object.c.



**Says:** So far: dirstream.c → `phar_wrapper_mkdir`, `phar_wrapper_rmdir`; func_interceptors.c → `phar_get_name_for_relative_paths`, `phar_file_stat`, `PHP_FUNCTION(phar_is_file)`, `PHP_FUNCTION(phar_is_link)`. Still need line 51's enclosing function and the phar_object.c, stream.c, and util.c sites.

- `read_file(path=ext/phar/func_interceptors.c, version=old, start_line=15, end_line=30)` →

```
ext/phar/func_interceptors.c lines 15-30 of 1000
   15| */
   16| 
   17| #include "phar_internal.h"
   18| #include "ext/standard/php_filestat.h"
   19| #include "ext/standard/file.h" /* For php_le_stream_context() */
   20| 
   21| PHP_FUNCTION(phar_opendir) /* {{{ */
   22| {
   23| 	char *filename;
   24| 	size_t filename_len;
   25| 	zval *zcontext = NULL;
   26| 
   27| 	if (!PHAR_G(intercepted)) {
   28| 		goto skip_phar;
   29| 	}
   30| 
```

- `read_file(path=ext/phar/phar_object.c, version=old, start_line=400, end_line=530)` →

```
ext/phar/phar_object.c lines 400-530 of 5062
  400| 
  401| /* {{{ return the name of the currently running phar archive.  If the optional parameter
  402|  * is set to true, return the phar:// URL to the currently running phar
  403|  */
  404| PHP_METHOD(Phar, running)
  405| {
  406| 	zend_string *fname;
  407| 	char *arch;
  408| 	size_t arch_len;
  409| 	bool retphar = true;
  410| 
  411| 	if (zend_parse_parameters(ZEND_NUM_ARGS(), "|b", &retphar) == FAILURE) {
  412| 		RETURN_THROWS();
  413| 	}
  414| 
  415| 	fname = zend_get_executed_filename_ex();
  416| 	if (!fname) {
  417| 		RETURN_EMPTY_STRING();
  418| 	}
  419| 
  420| 	if (
  421| 		zend_string_starts_with_literal_ci(fname, "phar://")
  422| 		&& SUCCESS == phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 2, 0)
  423| 	) {
  424| 		if (retphar) {
  425| 			RETVAL_STRINGL(ZSTR_VAL(fname), arch_len + 7);
  426| 			efree(arch);
  427| 			return;
  428| 		} else {
  429| 			// TODO: avoid reallocation ???
  430| 			RETVAL_STRINGL(arch, arch_len);
  431| 			efree(arch);
  432| 			return;
  433| 		}
  434| 	}
  435| 
  436| 	RETURN_EMPTY_STRING();
  437| }
  438| /* }}} */
  439| 
  440| /* {{{ mount an external file or path to a location within the phar.  This maps
  441|  * an external file or directory to a location within the phar archive, allowing
  442|  * reference to an external location as if it were within the phar archive.  This
  443|  * is useful for writable temp files like databases
  444|  */
  445| PHP_METHOD(Phar, mount)
  446| {
  447| 	char *fname, *arch = NULL, *path, *actual;
  448| 	size_t fname_len, arch_len;
  449| 	size_t path_len, actual_len;
  450| 	phar_archive_data *pphar;
  451| #ifdef PHP_WIN32
  452| 	char *save_fname;
  453| 	ALLOCA_FLAG(fname_use_heap)
  454| #endif
  455| 
  456| 	if (zend_parse_parameters(ZEND_NUM_ARGS(), "pp", &path, &path_len, &actual, &actual_len) == FAILURE) {
  457| 		RETURN_THROWS();
  458| 	}
  459| 
  460| 	zend_string *zend_file_name = zend_get_executed_filename_ex();
  461| 	if (UNEXPECTED(!zend_file_name)) {
  462| 		fname = "";
  463| 		fname_len = 0;
  464| 	} else {
  465| 		fname = ZSTR_VAL(zend_file_name);
  466| 		fname_len = ZSTR_LEN(zend_file_name);
  467| 	}
  468| 
  469| #ifdef PHP_WIN32
  470| 	save_fname = fname;
  471| 	if (memchr(fname, '\\', fname_len)) {
  472| 		fname = do_alloca(fname_len + 1, fname_use_heap);
  473| 		memcpy(fname, save_fname, fname_len);
  474| 		fname[fname_len] = '\0';
  475| 		phar_unixify_path_separators(fname, fname_len);
  476| 	}
  477| #endif
  478| 
  479| 	zend_string *entry = NULL;
  480| 	if (fname_len > 7 && !memcmp(fname, "phar://", 7) && SUCCESS == phar_split_fname(fname, fname_len, &arch, &arch_len, NULL, 2, 0)) {
  481| 		if (path_len > 7 && !memcmp(path, "phar://", 7)) {
  482| 			zend_throw_exception_ex(phar_ce_PharException, 0, "Can only mount internal paths within a phar archive, use a relative path instead of \"%s\"", path);
  483| 			efree(arch);
  484| 			goto finish;
  485| 		}
  486| carry_on2:
  487| 		if (NULL == (pphar = zend_hash_str_find_ptr(&(PHAR_G(phar_fname_map)), arch, arch_len))) {
  488| 			if (PHAR_G(manifest_cached) && NULL != (pphar = zend_hash_str_find_ptr(&cached_phars, arch, arch_len))) {
  489| 				if (SUCCESS == phar_copy_on_write(&pphar)) {
  490| 					goto carry_on;
  491| 				}
  492| 			}
  493| 
  494| 			zend_throw_exception_ex(phar_ce_PharException, 0, "%s is not a phar archive, cannot mount", arch);
  495| 
  496| 			if (arch) {
  497| 				efree(arch);
  498| 			}
  499| 
  500| 			goto finish;
  501| 		}
  502| carry_on:
  503| 		if (SUCCESS != phar_mount_entry(pphar, actual, actual_len, path, path_len)) {
  504| 			zend_throw_exception_ex(phar_ce_PharException, 0, "Mounting of %s to %s within phar %s failed", path, actual, arch);
  505| 		}
  506| 
  507| 		if (entry && path == ZSTR_VAL(entry)) {
  508| 			zend_string_release_ex(entry, false);
  509| 		}
  510| 
  511| 		if (arch) {
  512| 			efree(arch);
  513| 		}
  514| 
  515| 		goto finish;
  516| 	} else if (HT_IS_INITIALIZED(&PHAR_G(phar_fname_map)) && NULL != (pphar = zend_hash_str_find_ptr(&(PHAR_G(phar_fname_map)), fname, fname_len))) {
  517| 		goto carry_on;
  518| 	} else if (PHAR_G(manifest_cached) && NULL != (pphar = zend_hash_str_find_ptr(&cached_phars, fname, fname_len))) {
  519| 		if (SUCCESS == phar_copy_on_write(&pphar)) {
  520| 			goto carry_on;
  521| 		}
  522| 
  523| 		goto carry_on;
  524| 	} else if (SUCCESS == phar_split_fname(path, path_len, &arch, &arch_len, &entry, 2, 0)) {
  525| 		path = ZSTR_VAL(entry);
  526| 		path_len = ZSTR_LEN(entry);
  527| 		goto carry_on2;
  528| 	}
  529| 
  530| 	zend_throw_exception_ex(phar_ce_PharException, 0, "Mounting of %s to %s failed", path, actual);
```

- `read_file(path=ext/phar/phar_object.c, version=old, start_line=1085, end_line=1115)` →

```
ext/phar/phar_object.c lines 1085-1115 of 5062
 1085| 	zend_long format = 0;
 1086| 	phar_archive_object *phar_obj;
 1087| 	phar_archive_data   *phar_data;
 1088| 	zval arg1, arg2;
 1089| 
 1090| 	phar_obj = PHAR_FETCH_INTERNAL();
 1091| 
 1092| 	is_data = instanceof_function(Z_OBJCE_P(ZEND_THIS), phar_ce_data);
 1093| 
 1094| 	if (is_data) {
 1095| 		if (zend_parse_parameters(ZEND_NUM_ARGS(), "p|ls!l", &fname, &fname_len, &flags, &alias, &alias_len, &format) == FAILURE) {
 1096| 			RETURN_THROWS();
 1097| 		}
 1098| 	} else {
 1099| 		if (zend_parse_parameters(ZEND_NUM_ARGS(), "p|ls!", &fname, &fname_len, &flags, &alias, &alias_len) == FAILURE) {
 1100| 			RETURN_THROWS();
 1101| 		}
 1102| 	}
 1103| 
 1104| 	if (phar_obj->archive) {
 1105| 		zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Cannot call constructor twice");
 1106| 		RETURN_THROWS();
 1107| 	}
 1108| 
 1109| 	save_fname = fname;
 1110| 	zend_string *entry = NULL;
 1111| 	if (SUCCESS == phar_split_fname(fname, fname_len, &arch, &arch_len, &entry, !is_data, 2)) {
 1112| 		/* use arch (the basename for the archive) for fname instead of fname */
 1113| 		/* this allows support for RecursiveDirectoryIterator of subdirectories */
 1114| #ifdef PHP_WIN32
 1115| 		phar_unixify_path_separators(arch, arch_len);
```

- `read_file(path=ext/phar/phar_object.c, version=old, start_line=1265, end_line=1295)` →

```
ext/phar/phar_object.c lines 1265-1295 of 5062
 1265| 	size_t arch_len;
 1266| 	phar_archive_data *phar;
 1267| 
 1268| 	if (zend_parse_parameters(ZEND_NUM_ARGS(), "p", &fname, &fname_len) == FAILURE) {
 1269| 		RETURN_THROWS();
 1270| 	}
 1271| 
 1272| 	if (!fname_len) {
 1273| 		zend_throw_exception_ex(phar_ce_PharException, 0, "Unknown phar archive \"\"");
 1274| 		RETURN_THROWS();
 1275| 	}
 1276| 
 1277| 	if (FAILURE == phar_open_from_filename(fname, fname_len, NULL, 0, REPORT_ERRORS, &phar, &error)) {
 1278| 		if (error) {
 1279| 			zend_throw_exception_ex(phar_ce_PharException, 0, "Unknown phar archive \"%s\": %s", fname, error);
 1280| 			efree(error);
 1281| 		} else {
 1282| 			zend_throw_exception_ex(phar_ce_PharException, 0, "Unknown phar archive \"%s\"", fname);
 1283| 		}
 1284| 		RETURN_THROWS();
 1285| 	}
 1286| 
 1287| 	zend_string *zend_file_name = zend_get_executed_filename_ex();
 1288| 
 1289| 	if (
 1290| 		zend_file_name
 1291| 		&& zend_string_starts_with_literal_ci(zend_file_name, "phar://")
 1292| 		&& SUCCESS == phar_split_fname(ZSTR_VAL(zend_file_name), ZSTR_LEN(zend_file_name), &arch, &arch_len, NULL, 2, 0)
 1293| 	) {
 1294| 		if (arch_len == fname_len && !memcmp(arch, fname, arch_len)) {
 1295| 			zend_throw_exception_ex(phar_ce_PharException, 0, "phar archive \"%s\" cannot be unlinked from within itself", fname);
```

- `read_file(path=ext/phar/phar_object.c, version=old, start_line=4395, end_line=4420)` →

```
ext/phar/phar_object.c lines 4395-4420 of 5062
 4395| /* {{{ Construct a Phar entry object */
 4396| PHP_METHOD(PharFileInfo, __construct)
 4397| {
 4398| 	char *fname, *arch, *error;
 4399| 	size_t fname_len;
 4400| 	size_t arch_len;
 4401| 	phar_entry_object *entry_obj;
 4402| 	phar_archive_data *phar_data;
 4403| 	zval arg1;
 4404| 
 4405| 	if (zend_parse_parameters(ZEND_NUM_ARGS(), "p", &fname, &fname_len) == FAILURE) {
 4406| 		RETURN_THROWS();
 4407| 	}
 4408| 
 4409| 	entry_obj = PHAR_FETCH_INTERNAL();
 4410| 
 4411| 	if (entry_obj->entry) {
 4412| 		zend_throw_exception_ex(spl_ce_BadMethodCallException, 0, "Cannot call constructor twice");
 4413| 		RETURN_THROWS();
 4414| 	}
 4415| 
 4416| 	zend_string *entry = NULL;
 4417| 	if (fname_len < 7 || memcmp(fname, "phar://", 7) || phar_split_fname(fname, fname_len, &arch, &arch_len, &entry, 2, 0) == FAILURE) {
 4418| 		zend_throw_exception_ex(spl_ce_RuntimeException, 0,
 4419| 			"'%s' is not a valid phar archive URL (must have at least phar://filename.phar)", fname);
 4420| 		RETURN_THROWS();
```

- `read_file(path=ext/phar/stream.c, version=old, start_line=55, end_line=76)` →

```
ext/phar/stream.c lines 55-76 of 957
   55| /**
   56|  * Open a phar file for streams API
   57|  */
   58| php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options) /* {{{ */
   59| {
   60| 	php_url *resource;
   61| 	char *arch = NULL, *error;
   62| 	size_t arch_len;
   63| 
   64| 	if (strncasecmp(filename, "phar://", 7)) {
   65| 		return NULL;
   66| 	}
   67| 	if (mode[0] == 'a') {
   68| 		if (!(options & PHP_STREAM_URL_STAT_QUIET)) {
   69| 			php_stream_wrapper_log_error(wrapper, options, "phar error: open mode append not supported");
   70| 		}
   71| 		return NULL;
   72| 	}
   73| 	zend_string *entry = NULL;
   74| 	if (phar_split_fname(filename, strlen(filename), &arch, &arch_len, &entry, 2, (mode[0] == 'w' ? 2 : 0)) == FAILURE) {
   75| 		if (!(options & PHP_STREAM_URL_STAT_QUIET)) {
   76| 			if (arch && !entry) {
```

- `read_file(path=ext/phar/util.c, version=old, start_line=280, end_line=350)` →

```
ext/phar/util.c lines 280-350 of 2090
  280| 		return NULL;
  281| 	}
  282| 
  283| 	zend_string *fname = zend_get_executed_filename_ex();
  284| 	if (!fname) {
  285| 		return NULL;
  286| 	}
  287| 
  288| 	bool is_file_a_phar_wrapper = zend_string_starts_with_literal_ci(fname, "phar://");
  289| 	size_t length_phar_protocol = strlen("phar://");
  290| 
  291| 	if (
  292| 		PHAR_G(last_phar)
  293| 		&& is_file_a_phar_wrapper
  294| 		&& ZSTR_LEN(fname) - length_phar_protocol >= PHAR_G(last_phar_name_len)
  295| 		&& !memcmp(ZSTR_VAL(fname) + length_phar_protocol, PHAR_G(last_phar_name), PHAR_G(last_phar_name_len))
  296| 	) {
  297| 		arch = estrndup(PHAR_G(last_phar_name), PHAR_G(last_phar_name_len));
  298| 		arch_len = PHAR_G(last_phar_name_len);
  299| 		phar = PHAR_G(last_phar);
  300| 		goto splitted;
  301| 	}
  302| 
  303| 	if (!is_file_a_phar_wrapper || SUCCESS != phar_split_fname(ZSTR_VAL(fname), ZSTR_LEN(fname), &arch, &arch_len, NULL, 1, 0)) {
  304| 		return NULL;
  305| 	}
  306| 
  307| 	if (*ZSTR_VAL(filename) == '.') {
  308| 		if (FAILURE == phar_get_archive(&phar, arch, arch_len, NULL, 0, NULL)) {
  309| 			efree(arch);
  310| 			return NULL;
  311| 		}
  312| splitted:
  313| 		if (pphar) {
  314| 			*pphar = phar;
  315| 		}
  316| 
  317| 		zend_string *test = phar_fix_filepath(ZSTR_VAL(filename), ZSTR_LEN(filename), true);
  318| 		if (ZSTR_VAL(test)[0] == '/') {
  319| 			if (zend_hash_str_exists(&(phar->manifest), ZSTR_VAL(test) + 1, ZSTR_LEN(test) - 1)) {
  320| 				ret = zend_string_concat3(
  321| 					"phar://", strlen("phar://"),
  322| 					arch, arch_len,
  323| 					ZSTR_VAL(test), ZSTR_LEN(test)
  324| 				);
  325| 				zend_string_release_ex(test, false);
  326| 				efree(arch);
  327| 				return ret;
  328| 			}
  329| 		} else {
  330| 			if (zend_hash_exists(&(phar->manifest), test)) {
  331| 				ret = strpprintf(0, "phar://%s/%s", arch, ZSTR_VAL(test));
  332| 				zend_string_release_ex(test, false);
  333| 				efree(arch);
  334| 				return ret;
  335| 			}
  336| 		}
  337| 		zend_string_release_ex(test, false);
  338| 	}
  339| 
  340| 	spprintf(&path, MAXPATHLEN + 1 + strlen(PG(include_path)), "phar://%s/%s%c%s", arch, PHAR_G(cwd), DEFAULT_DIR_SEPARATOR, PG(include_path));
  341| 	efree(arch);
  342| 	ret = php_resolve_path(ZSTR_VAL(filename), ZSTR_LEN(filename), path);
  343| 	efree(path);
  344| 
  345| 	if (ret && zend_string_starts_with_literal_ci(ret, "phar://")) {
  346| 		/* found phar:// */
  347| 		if (SUCCESS != phar_split_fname(ZSTR_VAL(ret), ZSTR_LEN(ret), &arch, &arch_len, NULL, 1, 0)) {
  348| 			return ret;
  349| 		}
  350| 
```

### Turn 4  _(tok 19369+582, stop=tool_use)_

**Reasoning:** I'm pinning down the enclosing functions for util.c lines 303 and 347, where the range 280–350 starts before 280. Then I'm checking phar_object.c lines 1111 and 1292 for their enclosing methods, likely Phar::__construct and Phar::unlinkArchive, and noting that lines 422, 480, 524, and 4417 belong to Phar::running, Phar::mount, and PharFileInfo.

I'm finishing the check on the constructor and confirming the names for 1111 and 1292, along with the enclosing function for util.c. Next I'll grep for the function definitions.



**Says:** I still need the enclosing function names for util.c (lines 303 and 347) and phar_object.c (lines 1111 and 1292). I'll locate the function headers.

- `grep(pattern=^(PHP_METHOD|PHP_FUNCTION|PharFileFunction|[a-z_ ]+\*? ?[a-z, version=old, path_glob=ext/phar/util.c, max_results=200)` →

```
27 matches
ext/phar/util.c:37:static zend_result phar_call_openssl_signverify(bool is_sign, php_stream *fp, zend_off_t end, const char *key, size_t key_len, char **signature, size_t *signature_len, uint32_t sig_
ext/phar/util.c:41:static char *phar_get_link_location(phar_entry_info *entry) /* {{{ */
ext/phar/util.c:63:phar_entry_info *phar_get_link_source(phar_entry_info *entry) /* {{{ */
ext/phar/util.c:88:static php_stream *phar_get_entrypufp(const phar_entry_info *entry)
ext/phar/util.c:97:php_stream *phar_get_efp(phar_entry_info *entry, bool follow_links) /* {{{ */
ext/phar/util.c:128:static zend_off_t phar_get_fp_offset(const phar_entry_info *entry)
ext/phar/util.c:141:int phar_seek_efp(phar_entry_info *entry, zend_off_t offset, int whence, zend_off_t position, bool follow_links) /* {{{ */
ext/phar/util.c:191:zend_result phar_mount_entry(phar_archive_data *phar, const char *filename, size_t filename_len, char *path, size_t path_len) /* {{{ */
ext/phar/util.c:266:zend_string *phar_find_in_include_path(zend_string *filename, phar_archive_data **pphar) /* {{{ */
ext/phar/util.c:700:static inline void phar_set_pharfp(phar_archive_data *phar, php_stream *fp)
ext/phar/util.c:712:php_stream *phar_open_archive_fp(phar_archive_data *phar) /* {{{ */
ext/phar/util.c:772:static void phar_set_entrypufp(const phar_entry_info *entry, php_stream *fp)
ext/phar/util.c:782:static void phar_set_fp_type(phar_entry_info *entry, enum phar_fp_type type, zend_off_t offset)
ext/phar/util.c:932:zend_result phar_free_alias(const phar_archive_data *phar) /* {{{ */
ext/phar/util.c:956:zend_result phar_get_archive(phar_archive_data **archive, const char *fname, size_t fname_len, const char *alias, size_t alias_len, char **error) /* {{{ */
ext/phar/util.c:1160:const char * phar_compress_filter(const phar_entry_info *entry, bool return_unknown) /* {{{ */
ext/phar/util.c:1176:const char * phar_decompress_filter(const phar_entry_info *entry, bool return_unknown) /* {{{ */
ext/phar/util.c:1200:phar_entry_info *phar_get_entry_info(phar_archive_data *phar, char *path, size_t path_len, char **error, bool security) /* {{{ */
ext/phar/util.c:1211:phar_entry_info *phar_get_entry_info_dir(phar_archive_data *phar, char *path, size_t path_len, char dir, char **error, bool security) /* {{{ */
ext/phar/util.c:1369:static int phar_hex_str(const char *digest, size_t digest_len, char **signature) /* {{{ */
ext/phar/util.c:1386:static zend_result phar_call_openssl_signverify(bool is_sign, php_stream *fp, zend_off_t end, const char *key, size_t key_len, char **signature, size_t *signature_len, uint32_t si
ext/phar/util.c:1477:zend_result phar_verify_signature(php_stream *fp, size_t end_of_phar, uint32_t sig_type, char *sig, size_t sig_len, const char *fname, char **signature, size_t *signature_len, cha
ext/phar/util.c:1963:void phar_add_virtual_dirs(phar_archive_data *phar, const char *filename, size_t filename_len) /* {{{ */
ext/phar/util.c:1988:static int phar_update_cached_entry(zval *data, void *argument) /* {{{ */
ext/phar/util.c:2011:static void phar_manifest_copy_ctor(zval *zv) /* {{{ */
ext/phar/util.c:2019:static void phar_copy_cached_phar(phar_archive_data **pphar) /* {{{ */
ext/phar/util.c:2064:zend_result phar_copy_on_write(phar_archive_data **pphar) /* {{{ */
```

- `grep(pattern=^(PHP_METHOD|PHP_FUNCTION)\(, version=old, path_glob=ext/phar/phar_object.c, max_results=200)` →

```
71 matches
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
ext/phar/phar_object.c:1078:PHP_METHOD(Phar, __construct)
ext/phar/phar_object.c:1218:PHP_METHOD(Phar, getSupportedSignatures)
ext/phar/phar_object.c:1243:PHP_METHOD(Phar, getSupportedCompression)
ext/phar/phar_object.c:1261:PHP_METHOD(Phar, unlinkArchive)
ext/phar/phar_object.c:1327:PHP_METHOD(Phar, __destruct)
ext/phar/phar_object.c:1720:PHP_METHOD(Phar, buildFromDirectory)
ext/phar/phar_object.c:1828:PHP_METHOD(Phar, buildFromIterator)
ext/phar/phar_object.c:1879:PHP_METHOD(Phar, count)
ext/phar/phar_object.c:1897:PHP_METHOD(Phar, isFileFormat)
ext/phar/phar_object.c:2338:PHP_METHOD(Phar, convertToExecutable)
ext/phar/phar_object.c:2448:PHP_METHOD(Phar, convertToData)
ext/phar/phar_object.c:2556:PHP_METHOD(Phar, isCompressed)
ext/phar/phar_object.c:2575:PHP_METHOD(Phar, isWritable)
ext/phar/phar_object.c:2597:PHP_METHOD(Phar, delete)
ext/phar/phar_object.c:2645:PHP_METHOD(Phar, getAlias)
ext/phar/phar_object.c:2658:PHP_METHOD(Phar, getPath)
ext/phar/phar_object.c:2671:PHP_METHOD(Phar, setAlias)
ext/phar/phar_object.c:2769:PHP_METHOD(Phar, getVersion)
ext/phar/phar_object.c:2780:PHP_METHOD(Phar, startBuffering)
ext/phar/phar_object.c:2791:PHP_METHOD(Phar, isBuffering)
ext/phar/phar_object.c:2802:PHP_METHOD(Phar, stopBuffering)
ext/phar/phar_object.c:2829:PHP_METHOD(Phar, setStub)
ext/phar/phar_object.c:2926:PHP_METHOD(Phar, setDefaultStub)
ext/phar/phar_object.c:3001:PHP_METHOD(Phar, setSignatureAlgorithm)
ext/phar/phar_object.c:3050:PHP_METHOD(Phar, getSignature)
ext/phar/phar_object.c:3095:PHP_METHOD(Phar, getModified)
ext/phar/phar_object.c:3168:PHP_METHOD(Phar, compress)
ext/phar/phar_object.c:3236:PHP_METHOD(Phar, decompress)
ext/phar/phar_object.c:3278:PHP_METHOD(Phar, compressFiles)
ext/phar/phar_object.c:3353:PHP_METHOD(Phar, decompressFiles)
ext/phar/phar_object.c:3396:PHP_METHOD(Phar, copy)
ext/phar/phar_object.c:3490:PHP_METHOD(Phar, offsetExists)
ext/phar/phar_object.c:3520:PHP_METHOD(Phar, offsetGet)
ext/phar/phar_object.c:3708:PHP_METHOD(Phar, offsetSet)
ext/phar/phar_object.c:3746:PHP_METHOD(Phar, offsetUnset)
ext/phar/phar_object.c:3793:PHP_METHOD(Phar, addEmptyDir)
ext/phar/phar_object.c:3813:PHP_METHOD(Phar, addFile)
ext/phar/phar_object.c:3847:PHP_METHOD(Phar, addFromString)
ext/phar/phar_object.c:3863:PHP_METHOD(Phar, getStub)
ext/phar/phar_object.c:3958:PHP_METHOD(Phar, hasMetadata)
ext/phar/phar_object.c:3969:PHP_METHOD(Phar, getMetadata)
ext/phar/phar_object.c:4020:PHP_METHOD(Phar, setMetadata)
ext/phar/phar_object.c:4057:PHP_METHOD(Phar, delMetadata)
ext/phar/phar_object.c:4296:PHP_METHOD(Phar, extractTo)
ext/phar/phar_object.c:4396:PHP_METHOD(PharFileInfo, __construct)
ext/phar/phar_object.c:4479:PHP_METHOD(PharFileInfo, __destruct)
ext/phar/phar_object.c:4506:PHP_METHOD(PharFileInfo, getCompressedSize)
ext/phar/phar_object.c:4517:PHP_METHOD(PharFileInfo, isCompressed)
ext/phar/phar_object.c:4547:PHP_METHOD(PharFileInfo, getCRC32)
ext/phar/phar_object.c:4569:PHP_METHOD(PharFileInfo, isCRCChecked)
ext/phar/phar_object.c:4580:PHP_METHOD(PharFileInfo, getPharFlags)
ext/phar/phar_object.c:4591:PHP_METHOD(PharFileInfo, chmod)
ext/phar/phar_object.c:4653:PHP_METHOD(PharFileInfo, hasMetadata)
ext/phar/phar_object.c:4664:PHP_METHOD(PharFileInfo, getMetadata)
ext/phar/phar_object.c:4684:PHP_METHOD(PharFileInfo, setMetadata)
ext/phar/phar_object.c:4734:PHP_METHOD(PharFileInfo, delMetadata)
ext/phar/phar_object.c:4786:PHP_METHOD(PharFileInfo, getContent)
ext/phar/phar_object.c:4833:PHP_METHOD(PharFileInfo, compress)
ext/phar/phar_object.c:4960:PHP_METHOD(PharFileInfo, decompress)
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 24310+622, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "PHP_FUNCTION(phar_opendir)", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_get_name_for_relative_paths", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_file_stat", "file": "ext/phar/func_interceptors.c"}, {"function": "PHP_FUNCTION(phar_is_file)", "file": "ext/phar/func_interceptors.c"}, {"function": "PHP_FUNCTION(phar_is_link)", "file": "ext/phar/func_interceptors.c"}, {"function": "PHP_METHOD(Phar, running)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, mount)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, __construct)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, unlinkArchive)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(PharFileInfo, __construct)", "file": "ext/phar/phar_object.c"}, {"function": "phar_parse_url", "file": "ext/phar/stream.c"}, {"function": "phar_find_in_include_path", "file": "ext/phar/util.c"}, {"function": "phar_resolve_path", "file": "ext/phar/util.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 15, "n_truth": 14, "tp": 14, "precision": 0.9333333333333333, "recall": 1.0, "f1": 0.9655172413793104}`

