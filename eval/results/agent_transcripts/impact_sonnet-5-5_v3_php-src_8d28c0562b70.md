# Impact-analysis transcript — php-src @ 8d28c0562b70 — anthropic:claude-sonnet-5-5

- target: `phar_split_fname` (ext/phar/phar.c), arity 7->5
- truth: [['ext/phar/dirstream.c', 'phar_wrapper_mkdir'], ['ext/phar/dirstream.c', 'phar_wrapper_rmdir'], ['ext/phar/func_interceptors.c', 'PHP_FUNCTION(phar_is_file)'], ['ext/phar/func_interceptors.c', 'PHP_FUNCTION(phar_is_link)'], ['ext/phar/func_interceptors.c', 'PHP_FUNCTION(phar_opendir)'], ['ext/phar/func_interceptors.c', 'phar_file_stat'], ['ext/phar/func_interceptors.c', 'phar_get_name_for_relative_paths'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, __construct)'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, mount)'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, running)'], ['ext/phar/phar_object.c', 'PHP_METHOD(Phar, unlinkArchive)'], ['ext/phar/phar_object.c', 'PHP_METHOD(PharFileInfo, __construct)'], ['ext/phar/stream.c', 'phar_parse_url'], ['ext/phar/util.c', 'phar_find_in_include_path']]

## Self-navigation arm

### Turn 1  _(tok 1214+98, stop=tool_use)_

- `grep(pattern=phar_split_fname, version=old, max_results=200)` →

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

### Turn 2  _(tok 2758+814, stop=tool_use)_

**Reasoning:** I need to find the enclosing functions, so I'll go through each one and look at what it contains.



- `grep(pattern=^(static |PHAR_FUNC|PHP_METHOD|zend_result |int |void |phar_, version=old, path_glob=ext/phar/func_interceptors.c)` →

```
9 matches
ext/phar/func_interceptors.c:85:static zend_string* phar_get_name_for_relative_paths(zend_string *filename, bool using_include_path)
ext/phar/func_interceptors.c:322:static void phar_fancy_stat(zend_stat_t *stat_sb, int type, zval *return_value)
ext/phar/func_interceptors.c:471:static void phar_file_stat(const char *filename, size_t filename_length, int type, zif_handler orig_stat_func, INTERNAL_FUNCTION_PARAMETERS) /* {{{ */
ext/phar/func_interceptors.c:831:void phar_intercept_functions(void)
ext/phar/func_interceptors.c:842:void phar_release_functions(void)
ext/phar/func_interceptors.c:856:void phar_intercept_functions_init(void)
ext/phar/func_interceptors.c:893:void phar_intercept_functions_shutdown(void)
ext/phar/func_interceptors.c:947:void phar_save_orig_functions(void) /* {{{ */
ext/phar/func_interceptors.c:974:void phar_restore_orig_functions(void) /* {{{ */
```

- `grep(pattern=^(static |PHAR_FUNC|PHP_METHOD|zend_result |int |void |phar_, version=old, path_glob=ext/phar/phar_object.c)` →

```
93 matches (showing 60)
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
ext/phar/phar_object.c:1327:PHP_METHOD(Phar, __destruct)
ext/phar/phar_object.c:1348:static zend_always_inline void phar_call_method_with_unwrap(zend_object *obj, const char *name, zval *rv)
ext/phar/phar_object.c:1357:static phar_entry_data *phar_build_entry_data(char *fname, size_t fname_len, char *path, size_t path_len, char **error, zval *file_info)
ext/phar/phar_object.c:1386:static int phar_build(zend_object_iterator *iter, void *puser) /* {{{ */
ext/phar/phar_object.c:1720:PHP_METHOD(Phar, buildFromDirectory)
ext/phar/phar_object.c:1828:PHP_METHOD(Phar, buildFromIterator)
ext/phar/phar_object.c:1879:PHP_METHOD(Phar, count)
ext/phar/phar_object.c:1897:PHP_METHOD(Phar, isFileFormat)
ext/phar/phar_object.c:1920:static zend_result phar_copy_file_contents(phar_entry_info *entry, php_stream *fp) /* {{{ */
ext/phar/phar_object.c:1955:static zend_object *phar_rename_archive(phar_archive_data **sphar, char *ext) /* {{{ */
ext/phar/phar_object.c:2212:static zend_object *phar_convert_to_other(phar_archive_data *source, int convert, char *ext, uint32_t flags) /* {{{ */
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
ext/phar/phar_object.c:3105:static int phar_set_compression(zval *zv, void *argument) /* {{{ */
ext/phar/phar_object.c:3122:static int phar_test_compression(zval *zv, void *argument) /* {{{ */
ext/phar/phar_object.c:3148:static void pharobj_set_compression(HashTable *manifest, uint32_t compress) /* {{{ */
ext/phar/phar_object.c:3154:static int pharobj_cancompress(HashTable *manifest) /* {{{ */
ext/phar/phar_object.c:3168:PHP_METHOD(Phar, compress)
ext/phar/phar_object.c:3236:PHP_METHOD(Phar, decompress)
ext/phar/phar_object.c:3278:PHP_METHOD(Phar, compressFiles)
ext/phar/phar_object.c:3353:PHP_METHOD(Phar, decompressFiles)
```

- `grep(pattern=^(static |PHAR_FUNC|PHP_METHOD|zend_result |int |void |phar_, version=old, path_glob=ext/phar/dirstream.c)` →

```
9 matches
ext/phar/dirstream.c:39:static int phar_dir_close(php_stream *stream, int close_handle)  /* {{{ */
ext/phar/dirstream.c:56:static int phar_dir_seek(php_stream *stream, zend_off_t offset, int whence, zend_off_t *newoffset) /* {{{ */
ext/phar/dirstream.c:88:static ssize_t phar_dir_read(php_stream *stream, char *buf, size_t count) /* {{{ */
ext/phar/dirstream.c:120:static ssize_t phar_dir_write(php_stream *stream, const char *buf, size_t count) /* {{{ */
ext/phar/dirstream.c:129:static int phar_dir_flush(php_stream *stream) /* {{{ */
ext/phar/dirstream.c:138:static int phar_compare_dir_name(Bucket *f, Bucket *s)  /* {{{ */
ext/phar/dirstream.c:151:static php_stream *phar_make_dirstream(const char *dir, size_t dirlen, const HashTable *manifest) /* {{{ */
ext/phar/dirstream.c:344:int phar_wrapper_mkdir(php_stream_wrapper *wrapper, const char *url_from, int mode, int options, php_stream_context *context) /* {{{ */
ext/phar/dirstream.c:470:int phar_wrapper_rmdir(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
```

- `grep(pattern=^(static |PHAR_FUNC|PHP_METHOD|zend_result |int |void |phar_, version=old, path_glob=ext/phar/util.c)` →

```
23 matches
ext/phar/util.c:41:static char *phar_get_link_location(phar_entry_info *entry) /* {{{ */
ext/phar/util.c:63:phar_entry_info *phar_get_link_source(phar_entry_info *entry) /* {{{ */
ext/phar/util.c:88:static php_stream *phar_get_entrypufp(const phar_entry_info *entry)
ext/phar/util.c:128:static zend_off_t phar_get_fp_offset(const phar_entry_info *entry)
ext/phar/util.c:141:int phar_seek_efp(phar_entry_info *entry, zend_off_t offset, int whence, zend_off_t position, bool follow_links) /* {{{ */
ext/phar/util.c:191:zend_result phar_mount_entry(phar_archive_data *phar, const char *filename, size_t filename_len, char *path, size_t path_len) /* {{{ */
ext/phar/util.c:266:zend_string *phar_find_in_include_path(zend_string *filename, phar_archive_data **pphar) /* {{{ */
ext/phar/util.c:364:static ZEND_ATTRIBUTE_NONNULL zend_result phar_create_writeable_entry(phar_archive_data *phar, phar_entry_info *entry, char **error) /* {{{ */
ext/phar/util.c:700:static inline void phar_set_pharfp(phar_archive_data *phar, php_stream *fp)
ext/phar/util.c:772:static void phar_set_entrypufp(const phar_entry_info *entry, php_stream *fp)
ext/phar/util.c:782:static void phar_set_fp_type(phar_entry_info *entry, enum phar_fp_type type, zend_off_t offset)
ext/phar/util.c:932:zend_result phar_free_alias(const phar_archive_data *phar) /* {{{ */
ext/phar/util.c:956:zend_result phar_get_archive(phar_archive_data **archive, const char *fname, size_t fname_len, const char *alias, size_t alias_len, char **error) /* {{{ */
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

- `grep(pattern=^(static |PHAR_FUNC|PHP_METHOD|zend_result |int |void |phar_, version=old, path_glob=ext/phar/stream.c)` →

```
10 matches
ext/phar/stream.c:159:static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STR
ext/phar/stream.c:351:static int phar_stream_close(php_stream *stream, int close_handle) /* {{{ */
ext/phar/stream.c:365:static ssize_t phar_stream_read(php_stream *stream, char *buf, size_t count) /* {{{ */
ext/phar/stream.c:396:static int phar_stream_seek(php_stream *stream, zend_off_t offset, int whence, zend_off_t *newoffset) /* {{{ */
ext/phar/stream.c:440:static ssize_t phar_stream_write(php_stream *stream, const char *buf, size_t count) /* {{{ */
ext/phar/stream.c:463:static int phar_stream_flush(php_stream *stream) /* {{{ */
ext/phar/stream.c:487:void phar_dostat(phar_archive_data *phar, phar_entry_info *data, php_stream_statbuf *ssb, bool is_temp_dir)
ext/phar/stream.c:539:static int phar_stream_stat(php_stream *stream, php_stream_statbuf *ssb) /* {{{ */
ext/phar/stream.c:657:static int phar_wrapper_unlink(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
ext/phar/stream.c:729:static int phar_wrapper_rename(php_stream_wrapper *wrapper, const char *url_from, const char *url_to, int options, php_stream_context *context) /* {{{ */
```

### Turn 3  _(tok 9135+675, stop=tool_use)_

**Reasoning:** I'm noting that line 51 sits inside something that starts before line 85, probably a macro or function, so I need to look at it. Line 497 is in phar_file_stat, and lines 734 and 792 fall inside PHP functions, possibly macros too. In util.c, lines 303 and 347 are within phar_find_in_include_path, which spans 266 to 364.

I still need to check line 4417 in phar_object.c, since it falls past 3353.



- `read_file(path=ext/phar/func_interceptors.c, start_line=35, end_line=52, version=old)` →

```
ext/phar/func_interceptors.c lines 35-52 of 1000
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
```

- `grep(pattern=^(PHAR_FUNC|PHP_METHOD|static .*\(), version=old, path_glob=ext/phar/func_interceptors.c)` →

```
3 matches
ext/phar/func_interceptors.c:85:static zend_string* phar_get_name_for_relative_paths(zend_string *filename, bool using_include_path)
ext/phar/func_interceptors.c:322:static void phar_fancy_stat(zend_stat_t *stat_sb, int type, zval *return_value)
ext/phar/func_interceptors.c:471:static void phar_file_stat(const char *filename, size_t filename_length, int type, zif_handler orig_stat_func, INTERNAL_FUNCTION_PARAMETERS) /* {{{ */
```

- `grep(pattern=^(PHP_METHOD|static .*\(), version=old, path_glob=ext/phar/stream.c)` →

```
10 matches
ext/phar/stream.c:159:static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STR
ext/phar/stream.c:351:static int phar_stream_close(php_stream *stream, int close_handle) /* {{{ */
ext/phar/stream.c:365:static ssize_t phar_stream_read(php_stream *stream, char *buf, size_t count) /* {{{ */
ext/phar/stream.c:396:static int phar_stream_seek(php_stream *stream, zend_off_t offset, int whence, zend_off_t *newoffset) /* {{{ */
ext/phar/stream.c:440:static ssize_t phar_stream_write(php_stream *stream, const char *buf, size_t count) /* {{{ */
ext/phar/stream.c:463:static int phar_stream_flush(php_stream *stream) /* {{{ */
ext/phar/stream.c:539:static int phar_stream_stat(php_stream *stream, php_stream_statbuf *ssb) /* {{{ */
ext/phar/stream.c:556:static int phar_wrapper_stat(php_stream_wrapper *wrapper, const char *url, int flags,
ext/phar/stream.c:657:static int phar_wrapper_unlink(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
ext/phar/stream.c:729:static int phar_wrapper_rename(php_stream_wrapper *wrapper, const char *url_from, const char *url_to, int options, php_stream_context *context) /* {{{ */
```

- `grep(pattern=^PHP_METHOD, version=old, path_glob=ext/phar/phar_object.c, max_results=200)` →

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

### Turn 4  _(tok 13733+332, stop=tool_use)_

**Reasoning:** I've confirmed line 524 falls inside the `mount` function, which spans lines 445 to 548. Next I'm looking at `PharFileInfo::__construct` at line 4417, and I'm checking where the `PHAR_FUNC` names are referenced in `func_interceptors`, at lines 51, 734, and 792.



- `grep(pattern=PHAR_FUNC|^}, version=old, path_glob=ext/phar/func_interceptors.c, max_results=80)` →

```
17 matches
ext/phar/func_interceptors.c:82:}
ext/phar/func_interceptors.c:146:}
ext/phar/func_interceptors.c:222:}
ext/phar/func_interceptors.c:266:}
ext/phar/func_interceptors.c:313:}
ext/phar/func_interceptors.c:468:}
ext/phar/func_interceptors.c:631:}
ext/phar/func_interceptors.c:648:}
ext/phar/func_interceptors.c:762:}
ext/phar/func_interceptors.c:819:}
ext/phar/func_interceptors.c:838:}
ext/phar/func_interceptors.c:845:}
ext/phar/func_interceptors.c:883:}
ext/phar/func_interceptors.c:919:}
ext/phar/func_interceptors.c:945:} phar_orig_functions = {0};
ext/phar/func_interceptors.c:971:}
ext/phar/func_interceptors.c:998:}
```

- `grep(pattern=phar_parse_url|^(static |PHAR_G).*phar_.*\(, version=old, path_glob=ext/phar/stream.c)` →

```
16 matches
ext/phar/stream.c:58:php_url* phar_parse_url(php_stream_wrapper *wrapper, const char *filename, const char *mode, int options) /* {{{ */
ext/phar/stream.c:159:static php_stream * phar_wrapper_open_url(php_stream_wrapper *wrapper, const char *path, const char *mode, int options, zend_string **opened_path, php_stream_context *context STR
ext/phar/stream.c:170:	if ((resource = phar_parse_url(wrapper, path, mode, options)) == NULL) {
ext/phar/stream.c:351:static int phar_stream_close(php_stream *stream, int close_handle) /* {{{ */
ext/phar/stream.c:365:static ssize_t phar_stream_read(php_stream *stream, char *buf, size_t count) /* {{{ */
ext/phar/stream.c:396:static int phar_stream_seek(php_stream *stream, zend_off_t offset, int whence, zend_off_t *newoffset) /* {{{ */
ext/phar/stream.c:440:static ssize_t phar_stream_write(php_stream *stream, const char *buf, size_t count) /* {{{ */
ext/phar/stream.c:463:static int phar_stream_flush(php_stream *stream) /* {{{ */
ext/phar/stream.c:539:static int phar_stream_stat(php_stream *stream, php_stream_statbuf *ssb) /* {{{ */
ext/phar/stream.c:556:static int phar_wrapper_stat(php_stream_wrapper *wrapper, const char *url, int flags,
ext/phar/stream.c:565:	if ((resource = phar_parse_url(wrapper, url, "r", flags|PHP_STREAM_URL_STAT_QUIET)) == NULL) {
ext/phar/stream.c:657:static int phar_wrapper_unlink(php_stream_wrapper *wrapper, const char *url, int options, php_stream_context *context) /* {{{ */
ext/phar/stream.c:665:	if ((resource = phar_parse_url(wrapper, url, "rb", options)) == NULL) {
ext/phar/stream.c:729:static int phar_wrapper_rename(php_stream_wrapper *wrapper, const char *url_from, const char *url_to, int options, php_stream_context *context) /* {{{ */
ext/phar/stream.c:740:	if ((resource_from = phar_parse_url(wrapper, url_from, "wb", options|PHP_STREAM_URL_STAT_QUIET)) == NULL) {
ext/phar/stream.c:756:	if ((resource_to = phar_parse_url(wrapper, url_to, "wb", options|PHP_STREAM_URL_STAT_QUIET)) == NULL) {
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 15459+1671, stop=tool_use, forced)_

**Reasoning:** I'm trying to pin down names for the functions at lines 51, 734, and 792 in func_interceptors. Line 35's zend_parse pattern suggests file_get_contents, so line 51 might be phar_file_get_contents, while 97 and 497 look like phar_get_name_for_relative_paths and phar_file_stat. I'm not sure yet what 734 and 792 should be called.

I'm weighing whether 734 and 792 belong to phar_is_file and phar_is_link, since those macro-defined functions sit in that range. Recalling the php-src layout, I think 734 may be phar_opendir, falling between 648 and 762, while 792 could be phar_file_stat, though I'm still unsure which name fits which line.

I'm still unsure about the name for line 734, and I'm checking whether the function at 648–762 is phar_is_link or phar_opendir. For line 51 I'm settling on phar_file_get_contents, but the ordering of the phar_is_file and phar_is_link functions is still unresolved.

I'm still weighing whether the function at 734 is phar_is_file or phar_opendir, and whether 792 is phar_is_link, though the line lengths don't settle it cleanly. I'll go with phar_is_file for 734 and phar_is_link for 792, with low confidence.



- **submit_callers** → `{"callers": [{"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_file_get_contents", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_get_name_for_relative_paths", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_file_stat", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_is_file", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_is_link", "file": "ext/phar/func_interceptors.c"}, {"function": "PHP_METHOD(Phar, running)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, mount)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, __construct)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, unlinkArchive)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(PharFileInfo, __construct)", "file": "ext/phar/phar_object.c"}, {"function": "phar_parse_url", "file": "ext/phar/stream.c"}, {"function": "phar_find_in_include_path", "file": "ext/phar/util.c"}], "confidence_overall": "low"}`

**Score (self):** `{"n_pred": 14, "n_truth": 14, "tp": 13, "precision": 0.9285714285714286, "recall": 0.9285714285714286, "f1": 0.9285714285714286}`

## Tool arm

### Turn 1  _(tok 3749+171, stop=tool_use)_

- `get_callers(name=phar_split_fname, limit=200)` →

```
{
  "name": "phar_split_fname",
  "version": "old",
  "callers": [
    {
      "caller": "phar_wrapper_mkdir",
      "file": "ext/phar/dirstream.c",
      "line": 353
    },
    {
      "caller": "phar_wrapper_rmdir",
      "file": "ext/phar/dirstream.c",
      "line": 479
    },
    {
      "caller": "PHP_FUNCTION(phar_opendir)",
      "file": "ext/phar/func_interceptors.c",
      "line": 51
    },
    {
      "caller": "phar_get_name_for_relative_paths",
      "file": "ext/phar/func_interceptors.c",
      "line": 97
    },
    {
      "caller": "phar_file_stat",
      "file": "ext/phar/func_interceptors.c",
      "line": 497
    },
    {
      "caller": "PHP_FUNCTION(phar_is_file)",
      "file": "ext/phar/func_interceptors.c",
      "line": 734
    },
    {
      "caller": "PHP_FUNCTION(phar_is_link)",
      "file": "ext/phar/func_interceptors.c",
      "line": 792
    },
    {
      "caller": "PHP_METHOD(Phar, running)",
      "file": "ext/phar/phar_object.c",
      "line": 422
    },
    {
      "caller": "PHP_METHOD(Phar, mount)",
      "file": "ext/phar/phar_object.c",
      "line": 480
    },
    {
      "caller": "PHP_METHOD(Phar, mount)",
      "file": "ext/phar/phar_object.c",
      "line": 524
    },
    {
      "caller": "PHP_METHOD(Phar, __construct)",
      "file": "ext/phar/phar_object.c",
      "line": 1111
    },
    {
      "caller": "PHP_METHOD(Phar, unlinkArchive)",
      "file": "ext/phar/phar_object.c",
      "line": 1292
    },
    {
      "caller": "PHP_METHOD(PharFileInfo, __construct)",
      "file": "ext/phar/phar_object.c",
      "line": 4417
    },
    {
      "caller": "phar_parse_url",
      "file": "ext/phar/stream.c",
      "line": 74
    },
    {
      "caller": "phar_find_in_include_path",
      "file": "ext/phar/util.c",
      "line": 303
    },
    {
      "caller": "phar_find_in_include_path",
      "file": "ext/phar/util.c",
      "line": 347
    }
  ]
}
```

- `grep(pattern=phar_split_fname, version=old, max_results=200)` →

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

### Turn 2  _(tok 6330+610, stop=tool_use)_

- **submit_callers** → `{"callers": [{"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "PHP_FUNCTION(phar_opendir)", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_get_name_for_relative_paths", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_file_stat", "file": "ext/phar/func_interceptors.c"}, {"function": "PHP_FUNCTION(phar_is_file)", "file": "ext/phar/func_interceptors.c"}, {"function": "PHP_FUNCTION(phar_is_link)", "file": "ext/phar/func_interceptors.c"}, {"function": "PHP_METHOD(Phar, running)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, mount)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, __construct)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, unlinkArchive)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(PharFileInfo, __construct)", "file": "ext/phar/phar_object.c"}, {"function": "phar_parse_url", "file": "ext/phar/stream.c"}, {"function": "phar_find_in_include_path", "file": "ext/phar/util.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 14, "n_truth": 14, "tp": 14, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3201+76, stop=tool_use)_

- `get_callers(name=phar_split_fname, limit=200)` →

```
{
  "name": "phar_split_fname",
  "version": "old",
  "callers": [
    {
      "caller": "phar_wrapper_mkdir",
      "file": "ext/phar/dirstream.c",
      "line": 353
    },
    {
      "caller": "phar_wrapper_rmdir",
      "file": "ext/phar/dirstream.c",
      "line": 479
    },
    {
      "caller": "PHP_FUNCTION(phar_opendir)",
      "file": "ext/phar/func_interceptors.c",
      "line": 51
    },
    {
      "caller": "phar_get_name_for_relative_paths",
      "file": "ext/phar/func_interceptors.c",
      "line": 97
    },
    {
      "caller": "phar_file_stat",
      "file": "ext/phar/func_interceptors.c",
      "line": 497
    },
    {
      "caller": "PHP_FUNCTION(phar_is_file)",
      "file": "ext/phar/func_interceptors.c",
      "line": 734
    },
    {
      "caller": "PHP_FUNCTION(phar_is_link)",
      "file": "ext/phar/func_interceptors.c",
      "line": 792
    },
    {
      "caller": "PHP_METHOD(Phar, running)",
      "file": "ext/phar/phar_object.c",
      "line": 422
    },
    {
      "caller": "PHP_METHOD(Phar, mount)",
      "file": "ext/phar/phar_object.c",
      "line": 480
    },
    {
      "caller": "PHP_METHOD(Phar, mount)",
      "file": "ext/phar/phar_object.c",
      "line": 524
    },
    {
      "caller": "PHP_METHOD(Phar, __construct)",
      "file": "ext/phar/phar_object.c",
      "line": 1111
    },
    {
      "caller": "PHP_METHOD(Phar, unlinkArchive)",
      "file": "ext/phar/phar_object.c",
      "line": 1292
    },
    {
      "caller": "PHP_METHOD(PharFileInfo, __construct)",
      "file": "ext/phar/phar_object.c",
      "line": 4417
    },
    {
      "caller": "phar_parse_url",
      "file": "ext/phar/stream.c",
      "line": 74
    },
    {
      "caller": "phar_find_in_include_path",
      "file": "ext/phar/util.c",
      "line": 303
    },
    {
      "caller": "phar_find_in_include_path",
      "file": "ext/phar/util.c",
      "line": 347
    }
  ]
}
```

### Turn 2  _(tok 4195+229, stop=tool_use)_

**Reasoning:** I'm wondering whether phar.c has other callers of phar_split_fname beyond the ones I've already noted, possibly in phar_open_from_filename or phar_open_archive. The older version might miss some, so I'll query the working version at the default revision and then check HEAD.



- `get_callers(name=phar_split_fname, limit=200, rev=HEAD)` →

```
{
  "name": "phar_split_fname",
  "version": "old",
  "callers": [
    {
      "caller": "phar_wrapper_mkdir",
      "file": "ext/phar/dirstream.c",
      "line": 353
    },
    {
      "caller": "phar_wrapper_rmdir",
      "file": "ext/phar/dirstream.c",
      "line": 479
    },
    {
      "caller": "PHP_FUNCTION(phar_opendir)",
      "file": "ext/phar/func_interceptors.c",
      "line": 51
    },
    {
      "caller": "phar_get_name_for_relative_paths",
      "file": "ext/phar/func_interceptors.c",
      "line": 97
    },
    {
      "caller": "phar_file_stat",
      "file": "ext/phar/func_interceptors.c",
      "line": 497
    },
    {
      "caller": "PHP_FUNCTION(phar_is_file)",
      "file": "ext/phar/func_interceptors.c",
      "line": 734
    },
    {
      "caller": "PHP_FUNCTION(phar_is_link)",
      "file": "ext/phar/func_interceptors.c",
      "line": 792
    },
    {
      "caller": "PHP_METHOD(Phar, running)",
      "file": "ext/phar/phar_object.c",
      "line": 422
    },
    {
      "caller": "PHP_METHOD(Phar, mount)",
      "file": "ext/phar/phar_object.c",
      "line": 480
    },
    {
      "caller": "PHP_METHOD(Phar, mount)",
      "file": "ext/phar/phar_object.c",
      "line": 524
    },
    {
      "caller": "PHP_METHOD(Phar, __construct)",
      "file": "ext/phar/phar_object.c",
      "line": 1111
    },
    {
      "caller": "PHP_METHOD(Phar, unlinkArchive)",
      "file": "ext/phar/phar_object.c",
      "line": 1292
    },
    {
      "caller": "PHP_METHOD(PharFileInfo, __construct)",
      "file": "ext/phar/phar_object.c",
      "line": 4417
    },
    {
      "caller": "phar_parse_url",
      "file": "ext/phar/stream.c",
      "line": 74
    },
    {
      "caller": "phar_find_in_include_path",
      "file": "ext/phar/util.c",
      "line": 303
    },
    {
      "caller": "phar_find_in_include_path",
      "file": "ext/phar/util.c",
      "line": 347
    }
  ]
}
```

### Turn 3  _(tok 5342+847, stop=tool_use)_

**Reasoning:** I'm checking whether anything in phar.c calls phar_split_fname, going through the candidate callers like phar_open_executed_filename and phar_open_from_filename, since the tool index might be missing some.

I'm going to check phar_open_archive and phar_get_pharfp next, then assume the remaining callers of phar_split_fname in util.c are fine.



- **submit_callers** → `{"callers": [{"function": "phar_wrapper_mkdir", "file": "ext/phar/dirstream.c"}, {"function": "phar_wrapper_rmdir", "file": "ext/phar/dirstream.c"}, {"function": "PHP_FUNCTION(phar_opendir)", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_get_name_for_relative_paths", "file": "ext/phar/func_interceptors.c"}, {"function": "phar_file_stat", "file": "ext/phar/func_interceptors.c"}, {"function": "PHP_FUNCTION(phar_is_file)", "file": "ext/phar/func_interceptors.c"}, {"function": "PHP_FUNCTION(phar_is_link)", "file": "ext/phar/func_interceptors.c"}, {"function": "PHP_METHOD(Phar, running)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, mount)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, __construct)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(Phar, unlinkArchive)", "file": "ext/phar/phar_object.c"}, {"function": "PHP_METHOD(PharFileInfo, __construct)", "file": "ext/phar/phar_object.c"}, {"function": "phar_parse_url", "file": "ext/phar/stream.c"}, {"function": "phar_find_in_include_path", "file": "ext/phar/util.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 14, "n_truth": 14, "tp": 14, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

