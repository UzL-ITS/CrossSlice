# Impact-analysis transcript — php-src @ ea67883a1ff3 — openrouter:deepseek/deepseek-v4-pro

- target: `phar_create_signature` (ext/phar/util.c), arity 5->3
- truth: [['ext/phar/phar.c', 'phar_flush_ex'], ['ext/phar/tar.c', 'phar_tar_flush'], ['ext/phar/zip.c', 'phar_zip_applysignature']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1024+81, stop=tool_use)_

**Reasoning:** The user wants me to find every function that calls `phar_create_signature`. Let me search for all references to this function in the codebase.

- `find_references(name=phar_create_signature)` →

```
4 references
phar_create_signature 3002 ext/phar/phar.c  				if (FAILURE == phar_create_signature(phar, newfile, &digest, &digest_len, &signature_error)) {
phar_create_signature  416 ext/phar/phar_internal.h ZEND_ATTRIBUTE_NONNULL zend_result phar_create_signature(phar_archive_data *phar, php_stream *fp, char **signature, size_t *signature_length, char *
phar_create_signature 1171 ext/phar/tar.c   		if (FAILURE == phar_create_signature(phar, newfile, &signature, &signature_length, &signature_error)) {
phar_create_signature 1174 ext/phar/zip.c   		if (FAILURE == phar_create_signature(phar, newfile, &signature, &signature_length, &signature_error)) {
```

### Turn 2  _(tok 1324+387, stop=tool_use)_

**Reasoning:** Let me analyze the references:

1. `ext/phar/phar.c` line 3002 - This is a call site. I need to find the enclosing function.
2. `ext/phar/phar_internal.h` line 416 - This is the declaration/prototype, not a call site.
3. `ext/phar/tar.c` line 1171 - This is a call site. I need to find the enclosing function.
4. `ext/phar/zip.c` line 1174 - This is a call site. I need to find the enclosing function.

Now I need to find the enclosing functions for the three call sites in phar.c, tar.c, and zip.c. Let me read the relevant files to determine the function names.

- `read_file(path=ext/phar/phar.c, start_line=2980, end_line=3010)` →

```
ext/phar/phar.c lines 2980-3010 of 3499
 2980| 	if (shared_cfp != NULL) {
 2981| 		php_stream_close(shared_cfp);
 2982| 		shared_cfp = NULL;
 2983| 	}
 2984| 
 2985| 	/* append signature */
 2986| 	if (global_flags & PHAR_HDR_SIGNATURE) {
 2987| 		char sig_buf[4];
 2988| 
 2989| 		php_stream_rewind(newfile);
 2990| 
 2991| 		if (phar->signature) {
 2992| 			efree(phar->signature);
 2993| 			phar->signature = NULL;
 2994| 		}
 2995| 
 2996| 		switch(phar->sig_flags) {
 2997| 			default: {
 2998| 				char *digest = NULL;
 2999| 				size_t digest_len;
 3000| 
 3001| 				char *signature_error = NULL;
 3002| 				if (FAILURE == phar_create_signature(phar, newfile, &digest, &digest_len, &signature_error)) {
 3003| 					spprintf(error, 0, "phar error: unable to write signature: %s", signature_error);
 3004| 					efree(signature_error);
 3005| 
 3006| 					if (digest) {
 3007| 						efree(digest);
 3008| 					}
 3009| 					if (must_close_old_file) {
 3010| 						php_stream_close(oldfile);
```

- `read_file(path=ext/phar/tar.c, start_line=1150, end_line=1180)` →

```
ext/phar/tar.c lines 1150-1180 of 1320
 1150| 
 1151| 		/* on error in the hash iterator above, error is set */
 1152| 		php_stream_close(newfile);
 1153| 		return EOF;
 1154| 	}
 1155| 
 1156| 	zend_hash_apply_with_argument(&phar->manifest, phar_tar_writeheaders, (void *) &pass);
 1157| 
 1158| 	if (*error) {
 1159| 		if (must_close_old_file) {
 1160| 			php_stream_close(oldfile);
 1161| 		}
 1162| 
 1163| 		/* on error in the hash iterator above, error is set */
 1164| 		php_stream_close(newfile);
 1165| 		return EOF;
 1166| 	}
 1167| 
 1168| 	/* add signature for executable tars or tars explicitly set with setSignatureAlgorithm */
 1169| 	if (!phar->is_data || phar->sig_flags) {
 1170| 		char *signature_error = NULL;
 1171| 		if (FAILURE == phar_create_signature(phar, newfile, &signature, &signature_length, &signature_error)) {
 1172| 			spprintf(error, 0, "phar error: unable to write signature to tar-based phar: %s", signature_error);
 1173| 			efree(signature_error);
 1174| 
 1175| 			if (must_close_old_file) {
 1176| 				php_stream_close(oldfile);
 1177| 			}
 1178| 
 1179| 			php_stream_close(newfile);
 1180| 			return EOF;
```

- `read_file(path=ext/phar/zip.c, start_line=1150, end_line=1185)` →

```
ext/phar/zip.c lines 1150-1185 of 1487
 1150| 	if (!phar->is_data || phar->sig_flags) {
 1151| 		size_t signature_length;
 1152| 		char *signature, sigbuf[8];
 1153| 		phar_entry_info entry = {0};
 1154| 		php_stream *newfile;
 1155| 		zend_off_t tell;
 1156| 
 1157| 		newfile = php_stream_fopen_tmpfile();
 1158| 		if (newfile == NULL) {
 1159| 			spprintf(pass->error, 0, "phar error: unable to create temporary file for the signature file");
 1160| 			return FAILURE;
 1161| 		}
 1162| 		tell = php_stream_tell(pass->filefp);
 1163| 		/* copy the local files, central directory, and the zip comment to generate the hash */
 1164| 		php_stream_seek(pass->filefp, 0, SEEK_SET);
 1165| 		php_stream_copy_to_stream_ex(pass->filefp, newfile, tell, NULL);
 1166| 		tell = php_stream_tell(pass->centralfp);
 1167| 		php_stream_seek(pass->centralfp, 0, SEEK_SET);
 1168| 		php_stream_copy_to_stream_ex(pass->centralfp, newfile, tell, NULL);
 1169| 		if (phar->metadata_tracker.str) {
 1170| 			php_stream_write(newfile, ZSTR_VAL(phar->metadata_tracker.str), ZSTR_LEN(phar->metadata_tracker.str));
 1171| 		}
 1172| 
 1173| 		char *signature_error = NULL;
 1174| 		if (FAILURE == phar_create_signature(phar, newfile, &signature, &signature_length, &signature_error)) {
 1175| 			if (signature_error) {
 1176| 				spprintf(pass->error, 0, "phar error: unable to write signature to zip-based phar: %s", signature_error);
 1177| 				efree(signature_error);
 1178| 			}
 1179| 
 1180| 			php_stream_close(newfile);
 1181| 			return FAILURE;
 1182| 		}
 1183| 
 1184| 		entry.fp = php_stream_fopen_tmpfile();
 1185| 		entry.fp_type = PHAR_MOD;
```

### Turn 3  _(tok 3195+334, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing function names. Let me look at the function definitions for each file.

For phar.c, I need to search backwards from line 3002 to find the function definition.
For tar.c, I need to search backwards from line 1171.
For zip.c, I need to search backwards from line 1174.

Let me find the function names.

- `grep(pattern=^(zend_result|int|bool|static|PHP_METHOD|PHP_FUNCTION|void)\, path_glob=ext/phar/phar.c)` →

```
15 matches
ext/phar/phar.c:193:void phar_destroy_phar_data(phar_archive_data *phar) /* {{{ */
ext/phar/phar.c:244:bool phar_archive_delref(phar_archive_data *phar) /* {{{ */
ext/phar/phar.c:360:void destroy_phar_manifest_entry_int(phar_entry_info *entry) /* {{{ */
ext/phar/phar.c:389:void destroy_phar_manifest_entry(zval *zv) /* {{{ */
ext/phar/phar.c:397:void phar_entry_delref(phar_entry_data *idata) /* {{{ */
ext/phar/phar.c:562:void phar_metadata_tracker_try_ensure_has_serialized_data(phar_metadata_tracker *tracker, bool persistent) /* {{{ */
ext/phar/phar.c:588:zend_result phar_metadata_tracker_unserialize_or_copy(phar_metadata_tracker *tracker, zval *metadata, bool persistent, HashTable *unserialize_options, const char* method_name) /* {
ext/phar/phar.c:625:bool phar_metadata_tracker_has_data(const phar_metadata_tracker *tracker, bool persistent) /* {{{ */
ext/phar/phar.c:635:void phar_metadata_tracker_free(phar_metadata_tracker *tracker, bool persistent) /* {{{ */
ext/phar/phar.c:657:void phar_metadata_tracker_copy(phar_metadata_tracker *dest, const phar_metadata_tracker *source, bool persistent) /* {{{ */
ext/phar/phar.c:675:void phar_metadata_tracker_clone(phar_metadata_tracker *tracker) /* {{{ */
ext/phar/phar.c:693:void phar_parse_metadata_lazy(const char *buffer, phar_metadata_tracker *tracker, uint32_t zip_metadata_len, bool persistent) /* {{{ */
ext/phar/phar.c:1511:zend_result phar_open_from_filename(char *fname, size_t fname_len, char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error) /* {{{ */
ext/phar/phar.c:1911:zend_result phar_detect_phar_fname_ext(const char *filename, size_t filename_len, const char **ext_str, size_t *ext_len, int executable, int for_create, bool is_complete) /* {{{ *
ext/phar/phar.c:3345:void phar_request_initialize(void) /* {{{ */
```

- `grep(pattern=^(zend_result|int|bool|static|PHP_METHOD|PHP_FUNCTION|void)\, path_glob=ext/phar/tar.c)` →

```
2 matches
ext/phar/tar.c:101:bool phar_is_tar(const char *buf, const char *fname) /* {{{ */
ext/phar/tar.c:200:zend_result phar_parse_tarfile(php_stream* fp, const char *fname, size_t fname_len, const char *alias, size_t alias_len, phar_archive_data** pphar, uint32_t compression, char **erro
```

- `grep(pattern=^(zend_result|int|bool|static|PHP_METHOD|PHP_FUNCTION|void)\, path_glob=ext/phar/zip.c)` →

```
1 matches
ext/phar/zip.c:227:zend_result phar_parse_zipfile(php_stream *fp, const char *fname, size_t fname_len, const char *alias, size_t alias_len, phar_archive_data** pphar, char **error) /* {{{ */
```

### Turn 4  _(tok 4336+163, stop=tool_use)_

**Reasoning:** The function definitions visible are only the top-level ones. The call sites at lines ~3002 in phar.c, ~1171 in tar.c, and ~1174 in zip.c are likely inside other static functions. Let me search more broadly.

For phar.c around line 3002 - I need to find the enclosing function. Let me look earlier in the file.

- `read_file(end_line=2800, path=ext/phar/phar.c, start_line=2700)` →

```
ext/phar/phar.c lines 2700-2800 of 3499
 2700| 			if (must_close_old_file) {
 2701| 				php_stream_close(oldfile);
 2702| 			}
 2703| 			php_stream_close(newfile);
 2704| 			spprintf(error, 0, "unable to %s compress file \"%s\" to new phar \"%s\"",
 2705| 				entry->flags & PHAR_ENT_COMPRESSED_GZ ? "gzip" : "bzip2",
 2706| 				ZSTR_VAL(entry->filename),
 2707| 				ZSTR_VAL(phar->fname));
 2708| 			return EOF;
 2709| 		}
 2710| 
 2711| 		/* create new file that holds the compressed versions */
 2712| 		/* work around inability to specify freedom in write and strictness
 2713| 		in read count */
 2714| 		if (shared_cfp == NULL) {
 2715| 			shared_cfp = php_stream_fopen_tmpfile();
 2716| 		}
 2717| 		entry->cfp = shared_cfp;
 2718| 		if (!entry->cfp) {
 2719| 			php_stream_filter_free(filter);
 2720| 			*error = estrdup("unable to create temporary file");
 2721| 			if (must_close_old_file) {
 2722| 				php_stream_close(oldfile);
 2723| 			}
 2724| 			php_stream_close(newfile);
 2725| 			goto cleanup;
 2726| 		}
 2727| 		/* for real phars, header_offset is unused; we misuse it here to store the offset in the temp file */
 2728| 		ZEND_ASSERT(entry->header_offset == 0);
 2729| 		entry->header_offset = php_stream_tell(entry->cfp);
 2730| 		php_stream_flush(file);
 2731| 		if (-1 == phar_seek_efp(entry, 0, SEEK_SET, 0, false)) {
 2732| 			php_stream_filter_free(filter);
 2733| 			if (must_close_old_file) {
 2734| 				php_stream_close(oldfile);
 2735| 			}
 2736| 			php_stream_close(newfile);
 2737| 			spprintf(error, 0, "unable to seek to start of file \"%s\" while creating new phar \"%s\"",
 2738| 				ZSTR_VAL(entry->filename), ZSTR_VAL(phar->fname));
 2739| 			goto cleanup;
 2740| 		}
 2741| 		php_stream_filter_append((&entry->cfp->writefilters), filter);
 2742| 		if (SUCCESS != php_stream_copy_to_stream_ex(file, entry->cfp, entry->uncompressed_filesize, NULL)) {
 2743| 			php_stream_filter_remove(filter, 1);
 2744| 			if (must_close_old_file) {
 2745| 				php_stream_close(oldfile);
 2746| 			}
 2747| 			php_stream_close(newfile);
 2748| 			spprintf(error, 0, "unable to copy compressed file contents of file \"%s\" while creating new phar \"%s\"",
 2749| 				ZSTR_VAL(entry->filename), ZSTR_VAL(phar->fname));
 2750| 			goto cleanup;
 2751| 		}
 2752| 		php_stream_filter_flush(filter, 1);
 2753| 		php_stream_flush(entry->cfp);
 2754| 		php_stream_filter_remove(filter, 1);
 2755| 		php_stream_seek(entry->cfp, 0, SEEK_END);
 2756| 		entry->compressed_filesize = ((uint32_t) php_stream_tell(entry->cfp)) - entry->header_offset;
 2757| 		/* generate crc on compressed file */
 2758| 		entry->old_flags = entry->flags;
 2759| 		entry->is_modified = 1;
 2760| 		global_flags |= (entry->flags & PHAR_ENT_COMPRESSION_MASK);
 2761| 	} ZEND_HASH_FOREACH_END();
 2762| 	global_flags |= PHAR_HDR_SIGNATURE;
 2763| 
 2764| 	/* write out manifest pre-header */
 2765| 	/*  4: manifest length
 2766| 	 *  4: manifest entry count
 2767| 	 *  2: phar version
 2768| 	 *  4: phar global flags
 2769| 	 *  4: alias length
 2770| 	 *  ?: the alias itself
 2771| 	 *  4: phar metadata length
 2772| 	 *  ?: phar metadata
 2773| 	 */
 2774| 	restore_alias_len = phar->alias_len;
 2775| 	if (phar->is_temporary_alias) {
 2776| 		phar->alias_len = 0;
 2777| 	}
 2778| 
 2779| 	manifest_len = offset + phar->alias_len + sizeof(manifest) + (main_metadata_str.s ? ZSTR_LEN(main_metadata_str.s) : 0);
 2780| 	phar_set_32(manifest, manifest_len);
 2781| 	/* Hack - see bug #65028, add padding byte to the end of the manifest */
 2782| 	if(manifest[0] == '\r' || manifest[0] == '\n') {
 2783| 		manifest_len++;
 2784| 		phar_set_32(manifest, manifest_len);
 2785| 		manifest_hack = true;
 2786| 	}
 2787| 	phar_set_32(manifest+4, new_manifest_count);
 2788| 	if (has_dirs) {
 2789| 		*(manifest + 8) = (unsigned char) (((PHAR_API_VERSION) >> 8) & 0xFF);
 2790| 		*(manifest + 9) = (unsigned char) (((PHAR_API_VERSION) & 0xF0));
 2791| 	} else {
 2792| 		*(manifest + 8) = (unsigned char) (((PHAR_API_VERSION_NODIR) >> 8) & 0xFF);
 2793| 		*(manifest + 9) = (unsigned char) (((PHAR_API_VERSION_NODIR) & 0xF0));
 2794| 	}
 2795| 	phar_set_32(manifest+10, global_flags);
 2796| 	phar_set_32(manifest+14, phar->alias_len);
 2797| 
 2798| 	/* write the manifest header */
 2799| 	if (sizeof(manifest) != php_stream_write(newfile, manifest, sizeof(manifest))
 2800| 	|| (size_t)phar->alias_len != php_stream_write(newfile, phar->alias, phar->alias_len)) {
```

### Turn 5  _(tok 6205+118, stop=tool_use)_

**Reasoning:** I need to find the function that contains line 3002. Let me search backwards for function definitions from around line 2600 or earlier

- `grep(pattern=^static\s+(zend_result|int|bool|void|char|size_t|php_stream), path_glob=ext/phar/phar.c)` →

```
17 matches
ext/phar/phar.c:29:static void destroy_phar_data(zval *zv);
ext/phar/phar.c:37:static int phar_set_writeable_bit(zval *zv, void *argument) /* {{{ */
ext/phar/phar.c:91:static void phar_split_cache_list(void) /* {{{ */
ext/phar/phar.c:295:static void destroy_phar_data_only(zval *zv) /* {{{ */
ext/phar/phar.c:308:static int phar_unalias_apply(zval *zv, void *argument) /* {{{ */
ext/phar/phar.c:317:static int phar_tmpclose_apply(zval *zv) /* {{{ */
ext/phar/phar.c:337:static void destroy_phar_data(zval *zv) /* {{{ */
ext/phar/phar.c:487:static zend_result phar_open_parsed_phar(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_archive_data** pphar, char **error) /* {
ext/phar/phar.c:724:static zend_result phar_parse_pharfile(php_stream *fp, char *fname, size_t fname_len, char *alias, size_t alias_len, zend_long halt_offset, phar_archive_data** pphar, uint32_t comp
ext/phar/phar.c:1370:static zend_result phar_open_from_fp(php_stream* fp, char *fname, size_t fname_len, char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error);
ext/phar/phar.c:1568:static zend_result phar_open_from_fp(php_stream* fp, char *fname, size_t fname_len, char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error) /* {{
ext/phar/phar.c:1753:static zend_result phar_analyze_path(const char *fname, const char *ext, size_t ext_len, int for_create) /* {{{ */
ext/phar/phar.c:1859:static zend_result phar_check_str(const char *fname, const char *ext_str, size_t ext_len, int executable, int for_create) /* {{{ */
ext/phar/phar.c:2047:static bool php_check_dots(const char *element, size_t n) /* {{{ */
ext/phar/phar.c:2405:static int phar_flush_clean_deleted_apply(zval *zv) /* {{{ */
ext/phar/phar.c:3138:static size_t phar_zend_stream_fsizer(void *handle) /* {{{ */
ext/phar/phar.c:3229:static void mime_type_dtor(zval *zv)
```

### Turn 6  _(tok 6975+149, stop=tool_use)_

**Reasoning:** I need to look for the function that contains line 3002. Let me look for a function definition around line 2400-2600 area, since that might be where the enclosing function starts. Let me look for something like `static zend_result phar_flush` or similar.

- `grep(pattern=^(static\s+)?(zend_result|int|bool|void)\s+\w+\(, path_glob=ext/phar/phar.c)` →

```
31 matches
ext/phar/phar.c:29:static void destroy_phar_data(zval *zv);
ext/phar/phar.c:37:static int phar_set_writeable_bit(zval *zv, void *argument) /* {{{ */
ext/phar/phar.c:91:static void phar_split_cache_list(void) /* {{{ */
ext/phar/phar.c:193:void phar_destroy_phar_data(phar_archive_data *phar) /* {{{ */
ext/phar/phar.c:244:bool phar_archive_delref(phar_archive_data *phar) /* {{{ */
ext/phar/phar.c:295:static void destroy_phar_data_only(zval *zv) /* {{{ */
ext/phar/phar.c:308:static int phar_unalias_apply(zval *zv, void *argument) /* {{{ */
ext/phar/phar.c:317:static int phar_tmpclose_apply(zval *zv) /* {{{ */
ext/phar/phar.c:337:static void destroy_phar_data(zval *zv) /* {{{ */
ext/phar/phar.c:360:void destroy_phar_manifest_entry_int(phar_entry_info *entry) /* {{{ */
ext/phar/phar.c:389:void destroy_phar_manifest_entry(zval *zv) /* {{{ */
ext/phar/phar.c:397:void phar_entry_delref(phar_entry_data *idata) /* {{{ */
ext/phar/phar.c:487:static zend_result phar_open_parsed_phar(char *fname, size_t fname_len, char *alias, size_t alias_len, bool is_data, uint32_t options, phar_archive_data** pphar, char **error) /* {
ext/phar/phar.c:562:void phar_metadata_tracker_try_ensure_has_serialized_data(phar_metadata_tracker *tracker, bool persistent) /* {{{ */
ext/phar/phar.c:588:zend_result phar_metadata_tracker_unserialize_or_copy(phar_metadata_tracker *tracker, zval *metadata, bool persistent, HashTable *unserialize_options, const char* method_name) /* {
ext/phar/phar.c:625:bool phar_metadata_tracker_has_data(const phar_metadata_tracker *tracker, bool persistent) /* {{{ */
ext/phar/phar.c:635:void phar_metadata_tracker_free(phar_metadata_tracker *tracker, bool persistent) /* {{{ */
ext/phar/phar.c:657:void phar_metadata_tracker_copy(phar_metadata_tracker *dest, const phar_metadata_tracker *source, bool persistent) /* {{{ */
ext/phar/phar.c:675:void phar_metadata_tracker_clone(phar_metadata_tracker *tracker) /* {{{ */
ext/phar/phar.c:693:void phar_parse_metadata_lazy(const char *buffer, phar_metadata_tracker *tracker, uint32_t zip_metadata_len, bool persistent) /* {{{ */
ext/phar/phar.c:724:static zend_result phar_parse_pharfile(php_stream *fp, char *fname, size_t fname_len, char *alias, size_t alias_len, zend_long halt_offset, phar_archive_data** pphar, uint32_t comp
ext/phar/phar.c:1370:static zend_result phar_open_from_fp(php_stream* fp, char *fname, size_t fname_len, char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error);
ext/phar/phar.c:1511:zend_result phar_open_from_filename(char *fname, size_t fname_len, char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error) /* {{{ */
ext/phar/phar.c:1568:static zend_result phar_open_from_fp(php_stream* fp, char *fname, size_t fname_len, char *alias, size_t alias_len, uint32_t options, phar_archive_data** pphar, char **error) /* {{
ext/phar/phar.c:1753:static zend_result phar_analyze_path(const char *fname, const char *ext, size_t ext_len, int for_create) /* {{{ */
ext/phar/phar.c:1859:static zend_result phar_check_str(const char *fname, const char *ext_str, size_t ext_len, int executable, int for_create) /* {{{ */
ext/phar/phar.c:1911:zend_result phar_detect_phar_fname_ext(const char *filename, size_t filename_len, const char **ext_str, size_t *ext_len, int executable, int for_create, bool is_complete) /* {{{ *
ext/phar/phar.c:2047:static bool php_check_dots(const char *element, size_t n) /* {{{ */
ext/phar/phar.c:2405:static int phar_flush_clean_deleted_apply(zval *zv) /* {{{ */
ext/phar/phar.c:3229:static void mime_type_dtor(zval *zv)
ext/phar/phar.c:3345:void phar_request_initialize(void) /* {{{ */
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 7  _(tok 8350+213, stop=tool_use, forced)_

**Reasoning:** I need to find the enclosing functions. Let me look at the pattern more carefully. The grep found functions up to line 2405, then jumps to 3229. The call at line 3002 must be in a function defined between these. Let me search for more function definitions in the range, possibly with different patterns.

Let me search for function definitions between lines 2400 and 3100.

- **submit_callers** → `{"callers": [{"function": "phar_flush", "file": "ext/phar/phar.c"}, {"function": "phar_tar_flush", "file": "ext/phar/tar.c"}, {"function": "phar_zip_flush", "file": "ext/phar/zip.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 3, "n_truth": 3, "tp": 1, "precision": 0.3333333333333333, "recall": 0.3333333333333333, "f1": 0.3333333333333333}`

