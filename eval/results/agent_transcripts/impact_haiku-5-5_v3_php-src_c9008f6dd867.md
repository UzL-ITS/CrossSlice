# Impact-analysis transcript — php-src @ c9008f6dd867 — anthropic:claude-haiku-5-5

- target: `phar_get_or_create_entry_data` (ext/phar/util.c), arity 8->9
- truth: [['ext/phar/phar_object.c', 'phar_add_file'], ['ext/phar/phar_object.c', 'phar_build'], ['ext/phar/phar_object.c', 'phar_mkdir'], ['ext/phar/stream.c', 'phar_wrapper_open_url']]

## Self-navigation arm

### Turn 1  _(tok 1225+94, stop=tool_use)_

**Reasoning:** I'm searching the codebase for the function name.



- `grep(pattern=phar_get_or_create_entry_data, version=old)` →

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

### Turn 2  _(tok 1941+492, stop=tool_use)_

**Reasoning:** I'm checking which grep matches are real: the definition sits in util.c, and there are seven matches in total. Grep might be case-sensitive and could miss macros or other call sites, so I'll keep that in mind. Next I need the enclosing functions for the phar_object.c and stream.c lines, and I'm leaving out phar.c:402 since it's a comment.



**Says:** The search returned 7 matches. One is a comment in `phar.c` and two are the prototype and definition, so I need the enclosing functions for the four call sites in `phar_object.c` and `stream.c`.

- `grep(pattern=^(static |ZEND_METHOD|PHP_METHOD|[a-zA-Z_].*\(), version=old, path_glob=ext/phar/phar_object.c, max_results=400)` →

```
98 matches
ext/phar/phar_object.c:32:static zend_class_entry *phar_ce_archive;
ext/phar/phar_object.c:33:static zend_class_entry *phar_ce_data;
ext/phar/phar_object.c:34:static zend_class_entry *phar_ce_PharException;
ext/phar/phar_object.c:35:static zend_class_entry *phar_ce_entry;
ext/phar/phar_object.c:48:static int phar_file_type(const HashTable *mimes, const char *file, char **mime_type) /* {{{ */
ext/phar/phar_object.c:68:static void phar_mung_server_vars(char *fname, char *entry, size_t entry_len, const char *basename, size_t request_uri_len) /* {{{ */
ext/phar/phar_object.c:159:static phar_action_status phar_file_action(phar_archive_data *phar, phar_entry_info *info, char *mime_type, int code, char *entry, size_t entry_len, char *arch, const char *
ext/phar/phar_object.c:309:static void phar_do_403(void) /* {{{ */
ext/phar/phar_object.c:323:static void phar_do_404(phar_archive_data *phar, char *fname, size_t fname_len, zend_string *f404) /* {{{ */
ext/phar/phar_object.c:351:static void phar_postprocess_ru_web(const char *fname, size_t fname_len, const char *entry, size_t *entry_len, char **ru, size_t *ru_len) /* {{{ */
ext/phar/phar_object.c:409:PHP_METHOD(Phar, running)
ext/phar/phar_object.c:450:PHP_METHOD(Phar, mount)
ext/phar/phar_object.c:554:PHP_METHOD(Phar, webPhar)
ext/phar/phar_object.c:866:PHP_METHOD(Phar, mungServer)
ext/phar/phar_object.c:916:PHP_METHOD(Phar, interceptFileFuncs)
ext/phar/phar_object.c:927:PHP_METHOD(Phar, createDefaultStub)
ext/phar/phar_object.c:949:PHP_METHOD(Phar, mapPhar)
ext/phar/phar_object.c:970:PHP_METHOD(Phar, loadPhar)
ext/phar/phar_object.c:990:PHP_METHOD(Phar, apiVersion)
ext/phar/phar_object.c:998:PHP_METHOD(Phar, canCompress)
ext/phar/phar_object.c:1019:PHP_METHOD(Phar, canWrite)
ext/phar/phar_object.c:1027:PHP_METHOD(Phar, isValidPharFilename)
ext/phar/phar_object.c:1046:static void phar_spl_foreign_dtor(spl_filesystem_object *object) /* {{{ */
ext/phar/phar_object.c:1061:static void phar_spl_foreign_clone(spl_filesystem_object *src, spl_filesystem_object *dst) /* {{{ */
ext/phar/phar_object.c:1071:static const spl_other_handler phar_spl_foreign_handler = {
ext/phar/phar_object.c:1084:PHP_METHOD(Phar, __construct)
ext/phar/phar_object.c:1215:PHP_METHOD(Phar, getSupportedSignatures)
ext/phar/phar_object.c:1240:PHP_METHOD(Phar, getSupportedCompression)
ext/phar/phar_object.c:1258:PHP_METHOD(Phar, unlinkArchive)
ext/phar/phar_object.c:1323:PHP_METHOD(Phar, __destruct)
ext/phar/phar_object.c:1344:static int phar_build(zend_object_iterator *iter, void *puser) /* {{{ */
ext/phar/phar_object.c:1655:PHP_METHOD(Phar, buildFromDirectory)
ext/phar/phar_object.c:1763:PHP_METHOD(Phar, buildFromIterator)
ext/phar/phar_object.c:1814:PHP_METHOD(Phar, count)
ext/phar/phar_object.c:1832:PHP_METHOD(Phar, isFileFormat)
ext/phar/phar_object.c:1855:static zend_result phar_copy_file_contents(phar_entry_info *entry, php_stream *fp) /* {{{ */
ext/phar/phar_object.c:1890:static zend_object *phar_rename_archive(phar_archive_data **sphar, char *ext) /* {{{ */
ext/phar/phar_object.c:2147:static zend_object *phar_convert_to_other(phar_archive_data *source, int convert, char *ext, uint32_t flags) /* {{{ */
ext/phar/phar_object.c:2272:PHP_METHOD(Phar, convertToExecutable)
ext/phar/phar_object.c:2382:PHP_METHOD(Phar, convertToData)
ext/phar/phar_object.c:2490:PHP_METHOD(Phar, isCompressed)
ext/phar/phar_object.c:2509:PHP_METHOD(Phar, isWritable)
ext/phar/phar_object.c:2531:PHP_METHOD(Phar, delete)
ext/phar/phar_object.c:2579:PHP_METHOD(Phar, getAlias)
ext/phar/phar_object.c:2592:PHP_METHOD(Phar, getPath)
ext/phar/phar_object.c:2605:PHP_METHOD(Phar, setAlias)
ext/phar/phar_object.c:2702:PHP_METHOD(Phar, getVersion)
ext/phar/phar_object.c:2713:PHP_METHOD(Phar, startBuffering)
ext/phar/phar_object.c:2724:PHP_METHOD(Phar, isBuffering)
ext/phar/phar_object.c:2735:PHP_METHOD(Phar, stopBuffering)
ext/phar/phar_object.c:2762:PHP_METHOD(Phar, setStub)
ext/phar/phar_object.c:2859:PHP_METHOD(Phar, setDefaultStub)
ext/phar/phar_object.c:2934:PHP_METHOD(Phar, setSignatureAlgorithm)
ext/phar/phar_object.c:2983:PHP_METHOD(Phar, getSignature)
ext/phar/phar_object.c:3028:PHP_METHOD(Phar, getModified)
ext/phar/phar_object.c:3038:static int phar_set_compression(zval *zv, void *argument) /* {{{ */
ext/phar/phar_object.c:3055:static int phar_test_compression(zval *zv, void *argument) /* {{{ */
ext/phar/phar_object.c:3081:static void pharobj_set_compression(HashTable *manifest, uint32_t compress) /* {{{ */
ext/phar/phar_object.c:3087:static int pharobj_cancompress(HashTable *manifest) /* {{{ */
ext/phar/phar_object.c:3101:PHP_METHOD(Phar, compress)
ext/phar/phar_object.c:3169:PHP_METHOD(Phar, decompress)
ext/phar/phar_object.c:3211:PHP_METHOD(Phar, compressFiles)
ext/phar/phar_object.c:3286:PHP_METHOD(Phar, decompressFiles)
ext/phar/phar_object.c:3329:PHP_METHOD(Phar, copy)
ext/phar/phar_object.c:3423:PHP_METHOD(Phar, offsetExists)
ext/phar/phar_object.c:3453:PHP_METHOD(Phar, offsetGet)
ext/phar/phar_object.c:3504:static void phar_add_file(phar_archive_data **pphar, zend_string *file_name, const zend_string *content, zval *zresource)
ext/phar/phar_object.c:3606:static void phar_mkdir(phar_archive_data **pphar, zend_string *dir_name)
ext/phar/phar_object.c:3641:PHP_METHOD(Phar, offsetSet)
ext/phar/phar_object.c:3679:PHP_METHOD(Phar, offsetUnset)
ext/phar/phar_object.c:3726:PHP_METHOD(Phar, addEmptyDir)
ext/phar/phar_object.c:3746:PHP_METHOD(Phar, addFile)
ext/phar/phar_object.c:3780:PHP_METHOD(Phar, addFromString)
ext/phar/phar_object.c:3796:PHP_METHOD(Phar, getStub)
ext/phar/phar_object.c:3891:PHP_METHOD(Phar, hasMetadata)
ext/phar/phar_object.c:3902:PHP_METHOD(Phar, getMetadata)
ext/phar/phar_object.c:3922:static zend_result serialize_metadata_or_throw(phar_metadata_tracker *tracker, bool persistent, zval *metadata)
ext/phar/phar_object.c:3953:PHP_METHOD(Phar, setMetadata)
ext/phar/phar_object.c:3990:PHP_METHOD(Phar, delMetadata)
ext/phar/phar_object.c:4021:ZEND_ATTRIBUTE_NONNULL static zend_result phar_extract_file(bool overwrite, phar_entry_info *entry, const zend_string *path, char **error) /* {{{ */
ext/phar/phar_object.c:4199:ZEND_ATTRIBUTE_NONNULL_ARGS(1, 3, 5) static int extract_helper(const phar_archive_data *archive, zend_string *search, const zend_string *path_to, bool overwrite, char **err
ext/phar/phar_object.c:4229:PHP_METHOD(Phar, extractTo)
ext/phar/phar_object.c:4329:PHP_METHOD(PharFileInfo, __construct)
ext/phar/phar_object.c:4411:PHP_METHOD(PharFileInfo, __destruct)
ext/phar/phar_object.c:4438:PHP_METHOD(PharFileInfo, getCompressedSize)
ext/phar/phar_object.c:4449:PHP_METHOD(PharFileInfo, isCompressed)
ext/phar/phar_object.c:4479:PHP_METHOD(PharFileInfo, getCRC32)
ext/phar/phar_object.c:4501:PHP_METHOD(PharFileInfo, isCRCChecked)
ext/phar/phar_object.c:4512:PHP_METHOD(PharFileInfo, getPharFlags)
ext/phar/phar_object.c:4523:PHP_METHOD(PharFileInfo, chmod)
ext/phar/phar_object.c:4585:PHP_METHOD(PharFileInfo, hasMetadata)
ext/phar/phar_object.c:4596:PHP_METHOD(PharFileInfo, getMetadata)
ext/phar/phar_object.c:4616:PHP_METHOD(PharFileInfo, setMetadata)
ext/phar/phar_object.c:4666:PHP_METHOD(PharFileInfo, delMetadata)
ext/phar/phar_object.c:4718:PHP_METHOD(PharFileInfo, getContent)
ext/phar/phar_object.c:4765:PHP_METHOD(PharFileInfo, compress)
ext/phar/phar_object.c:4892:PHP_METHOD(PharFileInfo, decompress)
ext/phar/phar_object.c:4983:void phar_object_init(void) /* {{{ */
```

- `read_file(path=ext/phar/stream.c, version=old, start_line=150, end_line=200)` →

```
ext/phar/stream.c lines 150-200 of 957
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

### Turn 3  _(tok 7604+611, stop=tool_use)_

**Reasoning:** I'm checking which functions contain the flagged lines: line 1581 falls inside phar_build, since it sits between phar_build at 1344 and the next function at 1655. Line 3539 is inside phar_add_file, which spans 3504 to 3606.

I'm checking that the stream.c:194 hit sits in phar_wrapper_open_url, and I'm confirming that the grep list is complete, since the pattern covers lines starting with letters and the search was repo-wide.



- **submit_callers** → `{"callers": [{"function": "phar_build", "file": "ext/phar/phar_object.c"}, {"function": "phar_add_file", "file": "ext/phar/phar_object.c"}, {"function": "phar_mkdir", "file": "ext/phar/phar_object.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 4, "n_truth": 4, "tp": 4, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3760+226, stop=tool_use)_

**Reasoning:** I'm going to call get_callers and run a grep at the same time.



- `get_callers(name=phar_get_or_create_entry_data, version=old, limit=200)` →

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

- `grep(pattern=phar_get_or_create_entry_data, version=old, max_results=500)` →

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

### Turn 2  _(tok 4890+386, stop=tool_use)_

**Reasoning:** I've confirmed the grep matches are consistent and that the callers tool located the enclosing functions: phar_build at line 1581, phar_add_file at 3539, phar_mkdir at 3611, and phar_wrapper_open_url in stream.c at 194. The search covered the whole repo since no path filter was set. I'm now checking whether line 1581 really sits inside phar_build.

The callers lookup already backs up the enclosing function names, so I'm treating line 1581 as inside phar_build. Macros or ifdefs could still complicate that, but nothing so far points that way, so I'll submit this.



- **submit_callers** → `{"callers": [{"function": "phar_build", "file": "ext/phar/phar_object.c"}, {"function": "phar_add_file", "file": "ext/phar/phar_object.c"}, {"function": "phar_mkdir", "file": "ext/phar/phar_object.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 4, "n_truth": 4, "tp": 4, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3212+116, stop=tool_use)_

**Reasoning:** I'm going to pull the callers of phar_get_or_create_entry_data first, asking for a large result limit so I don't miss any.



- `get_callers(name=phar_get_or_create_entry_data, limit=200)` →

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

### Turn 2  _(tok 3564+306, stop=tool_use)_

**Reasoning:** The tool gave back version "old," which is the parent of the revision I asked for, not the working tree I actually care about. The working tree may have changed since then, so I want to rerun the check against version "work" before trusting the result.



**Says:** The result came back labelled as the "old" version. I'll check the working-tree version too, in case the call sites differ.

- `get_callers(name=phar_get_or_create_entry_data, limit=200, rev=HEAD)` →

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

- `get_callers(name=phar_get_or_create_entry_data, limit=200, version=work)` →

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

### Turn 3  _(tok 4390+657, stop=tool_use)_

**Reasoning:** All three reports show the "old" version, so the server's commit might be the parent of the working tree. I'm weighing whether to check the function's neighborhood for more context. The callers list comes from the call graph, which could miss callers reached through function pointers, but that seems acceptable here. I'll confirm the definition exists in the work tree and check one call site, such as phar_build at line 1581.

The "old" label keeps showing up, so I'm wondering whether the tool reports "old" for every caller regardless of the actual version. I'll check the work tree directly with get_context_at at phar_object.c line 1581 and stream.c line 194.



**Says:** All three queries return the same four callers. To confirm the call sites still exist in the working tree, I'll check them directly.

- `get_context_at(file=ext/phar/phar_object.c, line=1581, version=work)` →

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

- `get_context_at(file=ext/phar/stream.c, line=194, version=work)` →

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

- `get_context_at(file=ext/phar/phar_object.c, line=3539, version=work)` →

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

- `get_context_at(file=ext/phar/phar_object.c, line=3611, version=work)` →

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

### Turn 4  _(tok 16545+259, stop=tool_use)_

**Reasoning:** I've confirmed all four items. The call graph may miss callers that come in through macros, but that's an acceptable gap, so I'm going ahead and submitting.



**Says:** All four call sites are confirmed in the working tree. Submitting the list.

- **submit_callers** → `{"callers": [{"function": "phar_build", "file": "ext/phar/phar_object.c"}, {"function": "phar_add_file", "file": "ext/phar/phar_object.c"}, {"function": "phar_mkdir", "file": "ext/phar/phar_object.c"}, {"function": "phar_wrapper_open_url", "file": "ext/phar/stream.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 4, "n_truth": 4, "tp": 4, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

