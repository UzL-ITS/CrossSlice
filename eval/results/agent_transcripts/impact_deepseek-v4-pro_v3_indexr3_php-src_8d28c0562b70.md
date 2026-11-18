# Impact-analysis transcript — php-src @ 8d28c0562b70 — openrouter:deepseek/deepseek-v4-pro

- target: `phar_split_fname` (ext/phar/phar.c), arity 7->5
- truth: [['ext/phar/dirstream.c', 'phar_wrapper_mkdir'], ['ext/phar/dirstream.c', 'phar_wrapper_rmdir'], ['ext/phar/func_interceptors.c', 'PHP_FUNCTION(phar_is_file)'], ['ext/phar/func_interceptors.c', 'PHP_FUNCTION(phar_is_link)'], ['ext/phar/func_interceptors.c', 'PHP_FUNCTION(phar_opendir)'], ['ext/phar/func_interceptors.c', 'phar_file_stat'], ['ext/phar/func_interceptors.c', 'phar_get_name_for_relative_paths'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, __construct)'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, mount)'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, running)'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, unlinkArchive)'], ['ext/phar/phar_object.c', 'PHP_METHOD(PharFileInfo, __construct)'], ['ext/phar/stream.c', 'phar_parse_url'], ['ext/phar/util.c', 'phar_find_in_include_path']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1025+67, stop=tool_use)_

**Reasoning:** Let me find all references to `phar_split_fname` in the repository

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

### Turn 2  _(tok 2067+739, stop=tool_use)_

**Reasoning:** Now I need to determine the enclosing function for each of these references. Let me look at each file and line to find the enclosing function. Let me read the relevant sections.

Let me process each file:

1. ext/phar/dirstream.c: lines 353, 479
2. ext/phar/func_interceptors.c: lines 51, 97, 497, 734, 792
3. ext/phar/phar_internal.h: line 477 - this is the prototype/declaration, skip it
4. ext/phar/phar_object.c: lines 422, 480, 524, 1111, 1292, 4417
5. ext/phar/stream.c: line 74
6. ext/phar/util.c: lines 303, 347

I need to find the enclosing functions. Let me read around these lines.

**Says:** Now let me find the enclosing functions for each call site. I'll read around each reference.



- `read_file(path=ext/phar/dirstream.c, start_line=340, end_line=370, version=old)` →

```
ext/phar/dirstream.c lines 340-370 of 588
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
  356| 	}
  357| 
  358| 	if (FAILURE == phar_get_archive(&phar, arch, arch_len, NULL, 0, NULL)) {
  359| 		phar = NULL;
  360| 	}
  361| 
  362| 	efree(arch);
  363| 
  364| 	if (PHAR_G(readonly) && (!phar || !phar->is_data)) {
  365| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot create directory \"%s\", write operations disabled", url_from);
  366| 		return 0;
  367| 	}
  368| 
  369| 	if ((resource = phar_parse_url(wrapper, url_from, "w", options)) == NULL) {
  370| 		return 0;
```

- `read_file(path=ext/phar/dirstream.c, start_line=465, end_line=495, version=old)` →

```
ext/phar/dirstream.c lines 465-495 of 588
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
  481| 		return 0;
  482| 	}
  483| 
  484| 	if (FAILURE == phar_get_archive(&phar, arch, arch_len, NULL, 0, NULL)) {
  485| 		phar = NULL;
  486| 	}
  487| 
  488| 	efree(arch);
  489| 
  490| 	if (PHAR_G(readonly) && (!phar || !phar->is_data)) {
  491| 		php_stream_wrapper_log_error(wrapper, options, "phar error: cannot rmdir directory \"%s\", write operations disabled", url);
  492| 		return 0;
  493| 	}
  494| 
  495| 	if ((resource = phar_parse_url(wrapper, url, "w", options)) == NULL) {
```

- `read_file(path=ext/phar/func_interceptors.c, start_line=40, end_line=110, version=old)` →

```
ext/phar/func_interceptors.c lines 40-110 of 1000
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
  101| 	/* fopen within phar, if :// is not in the url, then prepend phar://<archive>/ */
  102| 	/* retrieving a file defaults to within the current directory, so use this if possible */
  103| 	phar_archive_data *phar;
  104| 	if (FAILURE == phar_get_archive(&phar, arch, arch_len, NULL, 0, NULL)) {
  105| 		efree(arch);
  106| 		return NULL;
  107| 	}
  108| 
  109| 	zend_string *name = NULL;
  110| 	if (using_include_path) {
```

- `read_file(path=ext/phar/func_interceptors.c, start_line=485, end_line=510, version=old)` →

```
ext/phar/func_interceptors.c lines 485-510 of 1000
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
  501| 			if (FAILURE == has_archive) {
  502| 				goto skip_phar;
  503| 			}
  504| splitted:;
  505| 			zend_string *entry = phar_fix_filepath(filename, filename_length, true);
  506| 			const phar_entry_info *data = NULL;
  507| 			if (ZSTR_VAL(entry)[0] == '/') {
  508| 				data = zend_hash_str_find_ptr(&(phar->manifest), ZSTR_VAL(entry) + 1, ZSTR_LEN(entry) - 1);
  509| 				if (data) {
  510| 					zend_string_release_ex(entry, false);
```

- `read_file(path=ext/phar/func_interceptors.c, start_line=720, end_line=750, version=old)` →

```
ext/phar/func_interceptors.c lines 720-750 of 1000
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
```

- `read_file(path=ext/phar/func_interceptors.c, start_line=778, end_line=810, version=old)` →

```
ext/phar/func_interceptors.c lines 778-810 of 1000
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
  801| 				if (ZSTR_VAL(entry)[0] == '/') {
  802| 					etemp = zend_hash_str_find_ptr(&(phar->manifest), ZSTR_VAL(entry) + 1, ZSTR_LEN(entry) - 1);
  803| 				} else {
  804| 					etemp = zend_hash_find_ptr(&(phar->manifest), entry);
  805| 				}
  806| 				zend_string_release_ex(entry, false);
  807| 				if (etemp) {
  808| 					efree(arch);
  809| 					RETURN_BOOL(etemp->link);
  810| 				}
```

### Turn 3  _(tok 6530+163, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing function names for these references in func_interceptors.c. Let me look at the function definitions.

- `grep(pattern=^(static\s+)?(PHP_FUNCTION|PHP_METHOD|int\s|zend_result\s|vo, path_glob=ext/phar/func_interceptors.c, version=old)` →

```
8 matches
ext/phar/func_interceptors.c:322:static void phar_fancy_stat(zend_stat_t *stat_sb, int type, zval *return_value)
ext/phar/func_interceptors.c:471:static void phar_file_stat(const char *filename, size_t filename_length, int type, zif_handler orig_stat_func, INTERNAL_FUNCTION_PARAMETERS) /* {{{ */
ext/phar/func_interceptors.c:831:void phar_intercept_functions(void)
ext/phar/func_interceptors.c:842:void phar_release_functions(void)
ext/phar/func_interceptors.c:856:void phar_intercept_functions_init(void)
ext/phar/func_interceptors.c:893:void phar_intercept_functions_shutdown(void)
ext/phar/func_interceptors.c:947:void phar_save_orig_functions(void) /* {{{ */
ext/phar/func_interceptors.c:974:void phar_restore_orig_functions(void) /* {{{ */
```

### Turn 4  _(tok 6925+171, stop=tool_use)_

**Reasoning:** Hmm, I need to find the functions that contain the call sites. Let me look at the function definitions more carefully. The call sites are at lines 51, 97, 497, 734, 792. Let me search backwards from each to find the enclosing function.

For line 51, let me look above it

- `read_file(end_line=40, path=ext/phar/func_interceptors.c, start_line=1, version=old)` →

```
ext/phar/func_interceptors.c lines 1-40 of 1000
    1| /*
    2|   +----------------------------------------------------------------------+
    3|   | phar php single-file executable PHP extension                        |
    4|   +----------------------------------------------------------------------+
    5|   | Copyright © The PHP Group and Contributors.                          |
    6|   +----------------------------------------------------------------------+
    7|   | This source file is subject to the Modified BSD License that is      |
    8|   | bundled with this package in the file LICENSE, and is available      |
    9|   | through the World Wide Web at <https://www.php.net/license/>.        |
   10|   |                                                                      |
   11|   | SPDX-License-Identifier: BSD-3-Clause                                |
   12|   +----------------------------------------------------------------------+
   13|   | Authors: Gregory Beaver <cellog@php.net>                             |
   14|   +----------------------------------------------------------------------+
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
```

### Turn 5  _(tok 7630+141, stop=tool_use)_

**Reasoning:** So line 51 is in `phar_opendir` (PHP_FUNCTION starts at line 21).

Now line 97 - let me look for the function def above it.

- `grep(path_glob=ext/phar/func_interceptors.c, pattern=^(PHP_FUNCTION|static\s+\w+\s+\w+\s*\(), version=old)` →

```
9 matches
ext/phar/func_interceptors.c:21:PHP_FUNCTION(phar_opendir) /* {{{ */
ext/phar/func_interceptors.c:148:PHP_FUNCTION(phar_file_get_contents) /* {{{ */
ext/phar/func_interceptors.c:225:PHP_FUNCTION(phar_readfile) /* {{{ */
ext/phar/func_interceptors.c:269:PHP_FUNCTION(phar_fopen) /* {{{ */
ext/phar/func_interceptors.c:322:static void phar_fancy_stat(zend_stat_t *stat_sb, int type, zval *return_value)
ext/phar/func_interceptors.c:471:static void phar_file_stat(const char *filename, size_t filename_length, int type, zif_handler orig_stat_func, INTERNAL_FUNCTION_PARAMETERS) /* {{{ */
ext/phar/func_interceptors.c:635:PHP_FUNCTION(fname) { \
ext/phar/func_interceptors.c:707:PHP_FUNCTION(phar_is_file) /* {{{ */
ext/phar/func_interceptors.c:765:PHP_FUNCTION(phar_is_link) /* {{{ */
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 8052+586, stop=tool_use, forced)_

**Reasoning:** Let me compile what I have so far. I need to determine the enclosing function for each call site. Let me look at the function definitions more carefully.

From the grep, the functions are:
- line 21: `phar_opendir` - contains line 51
- line 85: `phar_get_name_for_relative_paths` (static zend_string*) - contains line 97
- line 148: `phar_file_get_contents`
- line 225: `phar_readfile`
- line 269: `phar_fopen`
- line 322: `phar_fancy_stat`
- line 471: `phar_file_stat` - contains line 497
- line 635: macro
- line 707: `phar_is_file` - contains line 734
- line 765: `phar_is_link` - contains line 792

Now for phar_object.c:
- lines 422, 480, 524, 1111, 1292, 4417

For stream.c line 74
For util.c lines 303, 347

And dirstream.c:
- line 344: `phar_wrapper_mkdir`
- line 470: `phar_wrapper_rmdir`

Let me also look at phar_object.c to find function names. Let me grep for function definitions.

- **submit_callers** → `{"callers": [{"function": "phar_opendir", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_get_name_for_relative_paths", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_file_stat", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_is_file", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_is_link", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_opendir", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_stream_url_stat", "file": "ext/phar/stream.c"}, {"function": "phar_analyze_path", "file": "ext/phar/util.c"}], "confidence_overall": "low"}`

**Score (index):** `{"n_pred": 9, "n_truth": 14, "tp": 7, "precision": 0.7777777777777778, "recall": 0.5, "f1": 0.6086956521739131}`

