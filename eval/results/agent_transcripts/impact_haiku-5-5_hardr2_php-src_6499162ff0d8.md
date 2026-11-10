# Impact-analysis transcript — php-src @ 6499162ff0d8 — anthropic:claude-haiku-5-5

- target: `zval_update_constant_ex` (Zend/zend_execute_API.c), arity 3->2
- truth: [['Zend/zend_API.c', 'zend_update_class_constants'], ['Zend/zend_ast.c', 'zend_ast_evaluate'], ['Zend/zend_builtin_functions.c', 'add_class_vars'], ['Zend/zend_constants.c', 'zend_get_constant_ex'], ['Zend/zend_execute.c', 'is_null_constant'], ['Zend/zend_vm_def.h', 'ZEND_VM_HANDLER(143, ZEND_DECLARE_CONST, CONST, CONST)'], ['Zend/zend_vm_def.h', 'ZEND_VM_HANDLER(183, ZEND_BIND_STATIC, CV, CONST, REF)'], ['Zend/zend_vm_def.h', 'ZEND_VM_HANDLER(64, ZEND_RECV_INIT, NUM, CONST)'], ['ext/reflection/php_reflection.c', 'ZEND_METHOD(reflection_class, getConstant)'], ['ext/reflection/php_reflection.c', 'ZEND_METHOD(reflection_class, getConstants)'], ['ext/reflection/php_reflection.c', 'ZEND_METHOD(reflection_function, getStaticVariables)'], ['ext/reflection/php_reflection.c', 'add_class_vars'], ['ext/standard/basic_functions.c', 'PHP_FUNCTION(constant)']]

## Self-navigation arm

### Turn 1  _(tok 1223+105, stop=tool_use)_

**Reasoning:** I'm searching the repo for every reference to zval_update_constant_ex to see where it's used.



- `grep(pattern=zval_update_constant_ex, version=old)` →

```
31 matches
Zend/tests/bug47572.phpt:2:Bug #47572 (zval_update_constant_ex: Segmentation fault)
Zend/zend_API.c:1133:					if (UNEXPECTED(zval_update_constant_ex(val, 1, class_type) != SUCCESS)) {
Zend/zend_API.c:1151:							if (UNEXPECTED(zval_update_constant_ex(val, 1, NULL) != SUCCESS)) {
Zend/zend_ast.c:262:					if (UNEXPECTED(zval_update_constant_ex(zv, 1, scope) != SUCCESS)) {
Zend/zend_ast.c:271:					if (UNEXPECTED(zval_update_constant_ex(result, 1, scope) != SUCCESS)) {
Zend/zend_builtin_functions.c:1183:			if (UNEXPECTED(zval_update_constant_ex(prop, 0, NULL) != SUCCESS)) {
Zend/zend_constants.c:397:			if (UNEXPECTED(zval_update_constant_ex(ret_constant, 1, ce) != SUCCESS)) {
Zend/zend_execute.c:654:		if (UNEXPECTED(zval_update_constant_ex(&constant, 0, NULL) != SUCCESS)) {
Zend/zend_execute.h:126:ZEND_API int zval_update_constant_ex(zval *pp, zend_bool inline_change, zend_class_entry *scope);
Zend/zend_execute_API.c:554:ZEND_API int zval_update_constant_ex(zval *p, zend_bool inline_change, zend_class_entry *scope) /* {{{ */
Zend/zend_execute_API.c:638:				if (UNEXPECTED(zval_update_constant_ex(p, 1, NULL) != SUCCESS)) {
Zend/zend_execute_API.c:662:	return zval_update_constant_ex(pp, inline_change, NULL);
Zend/zend_ini_parser.y:137:				zval_update_constant_ex(&tmp, 1, NULL);
Zend/zend_vm_def.h:4694:			if (UNEXPECTED(zval_update_constant_ex(param, 0, NULL) != SUCCESS)) {
Zend/zend_vm_def.h:5093:				zval_update_constant_ex(value, 1, NULL);
Zend/zend_vm_def.h:7204:		if (UNEXPECTED(zval_update_constant_ex(&c.value, 0, NULL) != SUCCESS)) {
Zend/zend_vm_def.h:8007:			if (UNEXPECTED(zval_update_constant_ex(value, 1, NULL) != SUCCESS)) {
Zend/zend_vm_execute.h:2295:			if (UNEXPECTED(zval_update_constant_ex(param, 0, NULL) != SUCCESS)) {
Zend/zend_vm_execute.h:5646:				zval_update_constant_ex(value, 1, NULL);
Zend/zend_vm_execute.h:6142:		if (UNEXPECTED(zval_update_constant_ex(&c.value, 0, NULL) != SUCCESS)) {
Zend/zend_vm_execute.h:18996:				zval_update_constant_ex(value, 1, NULL);
Zend/zend_vm_execute.h:28404:				zval_update_constant_ex(value, 1, NULL);
Zend/zend_vm_execute.h:40179:			if (UNEXPECTED(zval_update_constant_ex(value, 1, NULL) != SUCCESS)) {
ext/reflection/php_reflection.c:459:			zval_update_constant_ex(&c->value, 1, NULL);
ext/reflection/php_reflection.c:715:			zval_update_constant_ex(&zv, 1, NULL);
ext/reflection/php_reflection.c:1934:			if (UNEXPECTED(zval_update_constant_ex(val, 1, fptr->common.scope) != SUCCESS)) {
ext/reflection/php_reflection.c:2896:		zval_update_constant_ex(return_value, 0, NULL);
ext/reflection/php_reflection.c:3968:			if (UNEXPECTED(zval_update_constant_ex(&prop_copy, 1, NULL) != SUCCESS)) {
ext/reflection/php_reflection.c:4624:		if (UNEXPECTED(zval_update_constant_ex(&c->value, 1, ce) != SUCCESS)) {
ext/reflection/php_reflection.c:4672:		if (UNEXPECTED(zval_update_constant_ex(&c->value, 1, ce) != SUCCESS)) {
ext/standard/basic_functions.c:3846:			if (UNEXPECTED(zval_update_constant_ex(return_value, 1, NULL) != SUCCESS)) {
```

### Turn 2  _(tok 3036+1665, stop=tool_use)_

**Reasoning:** I need to figure out which functions enclose each location. Some of these sit in the generated VM handler files, where the code is inside handler macros, so I'll have to read the surrounding context. I'll go through them in batches, starting with the first one.

I'm checking the locations in zend_API.c and zend_ast.c next, and I'll read a window of roughly 60 lines before each one. Grepping for function definitions isn't practical here, so I'll batch the reads in parallel.



- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=Zend/zend_API.c, max_results=300)` →

```
178 matches
Zend/zend_API.c:48:ZEND_API int zend_get_parameters(int ht, int param_count, ...) /* {{{ */
Zend/zend_API.c:83:ZEND_API int zend_get_parameters_ex(int param_count, ...) /* {{{ */
Zend/zend_API.c:108:ZEND_API int _zend_get_parameters_array_ex(int param_count, zval *argument_array) /* {{{ */
Zend/zend_API.c:130:ZEND_API int zend_copy_parameters_array(int param_count, zval *argument_array) /* {{{ */
Zend/zend_API.c:154:ZEND_API ZEND_COLD void zend_wrong_param_count(void) /* {{{ */
Zend/zend_API.c:164:ZEND_API char *zend_get_type_by_const(int type) /* {{{ */
Zend/zend_API.c:195:ZEND_API char *zend_zval_type_name(const zval *arg) /* {{{ */
Zend/zend_API.c:203:ZEND_API ZEND_COLD void ZEND_FASTCALL zend_wrong_parameters_count_error(int num_args, int min_num_args, int max_num_args) /* {{{ */
Zend/zend_API.c:219:ZEND_API ZEND_COLD void ZEND_FASTCALL zend_wrong_parameter_type_error(int num, zend_expected_type expected_type, zval *arg) /* {{{ */
Zend/zend_API.c:233:ZEND_API ZEND_COLD void ZEND_FASTCALL zend_wrong_parameter_class_error(int num, char *name, zval *arg) /* {{{ */
Zend/zend_API.c:243:ZEND_API ZEND_COLD void ZEND_FASTCALL zend_wrong_callback_error(int severity, int num, char *error) /* {{{ */
Zend/zend_API.c:262:ZEND_API int ZEND_FASTCALL zend_parse_arg_class(zval *arg, zend_class_entry **pce, int num, int check_null) /* {{{ */
Zend/zend_API.c:298:ZEND_API int ZEND_FASTCALL zend_parse_arg_bool_weak(zval *arg, zend_bool *dest) /* {{{ */
Zend/zend_API.c:309:ZEND_API int ZEND_FASTCALL zend_parse_arg_bool_slow(zval *arg, zend_bool *dest) /* {{{ */
Zend/zend_API.c:318:ZEND_API int ZEND_FASTCALL zend_parse_arg_long_weak(zval *arg, zend_long *dest) /* {{{ */
Zend/zend_API.c:358:ZEND_API int ZEND_FASTCALL zend_parse_arg_long_slow(zval *arg, zend_long *dest) /* {{{ */
Zend/zend_API.c:367:ZEND_API int ZEND_FASTCALL zend_parse_arg_long_cap_weak(zval *arg, zend_long *dest) /* {{{ */
Zend/zend_API.c:399:ZEND_API int ZEND_FASTCALL zend_parse_arg_long_cap_slow(zval *arg, zend_long *dest) /* {{{ */
Zend/zend_API.c:408:ZEND_API int ZEND_FASTCALL zend_parse_arg_double_weak(zval *arg, double *dest) /* {{{ */
Zend/zend_API.c:434:ZEND_API int ZEND_FASTCALL zend_parse_arg_double_slow(zval *arg, double *dest) /* {{{ */
Zend/zend_API.c:446:ZEND_API int ZEND_FASTCALL zend_parse_arg_str_weak(zval *arg, zend_string **dest) /* {{{ */
Zend/zend_API.c:484:ZEND_API int ZEND_FASTCALL zend_parse_arg_str_slow(zval *arg, zend_string **dest) /* {{{ */
Zend/zend_API.c:493:static const char *zend_parse_arg_impl(int arg_num, zval *arg, va_list *va, const char **spec, char **error, int *severity) /* {{{ */
Zend/zend_API.c:743:static int zend_parse_arg(int arg_num, zval *arg, va_list *va, const char **spec, int flags) /* {{{ */
Zend/zend_API.c:777:ZEND_API int zend_parse_parameter(int flags, int arg_num, zval *arg, const char *spec, ...)
Zend/zend_API.c:789:static ZEND_COLD void zend_parse_parameters_debug_error(const char *msg) {
Zend/zend_API.c:798:static int zend_parse_va_args(int num_args, const char *type_spec, va_list *va, int flags) /* {{{ */
Zend/zend_API.c:935:ZEND_API int zend_parse_parameters_ex(int flags, int num_args, const char *type_spec, ...) /* {{{ */
Zend/zend_API.c:948:ZEND_API int zend_parse_parameters(int num_args, const char *type_spec, ...) /* {{{ */
Zend/zend_API.c:962:ZEND_API int zend_parse_parameters_throw(int num_args, const char *type_spec, ...) /* {{{ */
Zend/zend_API.c:976:ZEND_API int zend_parse_method_parameters(int num_args, zval *this_ptr, const char *type_spec, ...) /* {{{ */
Zend/zend_API.c:1016:ZEND_API int zend_parse_method_parameters_ex(int flags, int num_args, zval *this_ptr, const char *type_spec, ...) /* {{{ */
Zend/zend_API.c:1053:ZEND_API int _array_init(zval *arg, uint32_t size ZEND_FILE_LINE_DC) /* {{{ */
Zend/zend_API.c:1063:ZEND_API void zend_merge_properties(zval *obj, HashTable *properties) /* {{{ */
Zend/zend_API.c:1083:ZEND_API int zend_update_class_constants(zend_class_entry *class_type) /* {{{ */
Zend/zend_API.c:1167:ZEND_API void object_properties_init(zend_object *object, zend_class_entry *class_type) /* {{{ */
Zend/zend_API.c:1188:ZEND_API void object_properties_init_ex(zend_object *object, HashTable *properties) /* {{{ */
Zend/zend_API.c:1210:ZEND_API void object_properties_load(zend_object *object, HashTable *properties) /* {{{ */
Zend/zend_API.c:1272:ZEND_API int _object_and_properties_init(zval *arg, zend_class_entry *class_type, HashTable *properties ZEND_FILE_LINE_DC) /* {{{ */
Zend/zend_API.c:1309:ZEND_API int _object_init_ex(zval *arg, zend_class_entry *class_type ZEND_FILE_LINE_DC) /* {{{ */
Zend/zend_API.c:1315:ZEND_API int _object_init(zval *arg ZEND_FILE_LINE_DC) /* {{{ */
Zend/zend_API.c:1321:ZEND_API int add_assoc_long_ex(zval *arg, const char *key, size_t key_len, zend_long n) /* {{{ */
Zend/zend_API.c:1331:ZEND_API int add_assoc_null_ex(zval *arg, const char *key, size_t key_len) /* {{{ */
Zend/zend_API.c:1341:ZEND_API int add_assoc_bool_ex(zval *arg, const char *key, size_t key_len, int b) /* {{{ */
Zend/zend_API.c:1351:ZEND_API int add_assoc_resource_ex(zval *arg, const char *key, size_t key_len, zend_resource *r) /* {{{ */
Zend/zend_API.c:1361:ZEND_API int add_assoc_double_ex(zval *arg, const char *key, size_t key_len, double d) /* {{{ */
Zend/zend_API.c:1371:ZEND_API int add_assoc_str_ex(zval *arg, const char *key, size_t key_len, zend_string *str) /* {{{ */
Zend/zend_API.c:1381:ZEND_API int add_assoc_string_ex(zval *arg, const char *key, size_t key_len, char *str) /* {{{ */
Zend/zend_API.c:1391:ZEND_API int add_assoc_stringl_ex(zval *arg, const char *key, size_t key_len, char *str, size_t length) /* {{{ */
Zend/zend_API.c:1401:ZEND_API int add_assoc_zval_ex(zval *arg, const char *key, size_t key_len, zval *value) /* {{{ */
Zend/zend_API.c:1410:ZEND_API int add_index_long(zval *arg, zend_ulong index, zend_long n) /* {{{ */
Zend/zend_API.c:1419:ZEND_API int add_index_null(zval *arg, zend_ulong index) /* {{{ */
Zend/zend_API.c:1428:ZEND_API int add_index_bool(zval *arg, zend_ulong index, int b) /* {{{ */
Zend/zend_API.c:1437:ZEND_API int add_index_resource(zval *arg, zend_ulong index, zend_resource *r) /* {{{ */
Zend/zend_API.c:1446:ZEND_API int add_index_double(zval *arg, zend_ulong index, double d) /* {{{ */
Zend/zend_API.c:1455:ZEND_API int add_index_str(zval *arg, zend_ulong index, zend_string *str) /* {{{ */
Zend/zend_API.c:1464:ZEND_API int add_index_string(zval *arg, zend_ulong index, const char *str) /* {{{ */
Zend/zend_API.c:1473:ZEND_API int add_index_stringl(zval *arg, zend_ulong index, const char *str, size_t length) /* {{{ */
Zend/zend_API.c:1482:ZEND_API int add_index_zval(zval *arg, zend_ulong index, zval *value) /* {{{ */
Zend/zend_API.c:1488:ZEND_API int add_next_index_long(zval *arg, zend_long n) /* {{{ */
Zend/zend_API.c:1497:ZEND_API int add_next_index_null(zval *arg) /* {{{ */
Zend/zend_API.c:1506:ZEND_API int add_next_index_bool(zval *arg, int b) /* {{{ */
Zend/zend_API.c:1515:ZEND_API int add_next_index_resource(zval *arg, zend_resource *r) /* {{{ */
Zend/zend_API.c:1524:ZEND_API int add_next_index_double(zval *arg, double d) /* {{{ */
Zend/zend_API.c:1533:ZEND_API int add_next_index_str(zval *arg, zend_string *str) /* {{{ */
Zend/zend_API.c:1542:ZEND_API int add_next_index_string(zval *arg, const char *str) /* {{{ */
Zend/zend_API.c:1551:ZEND_API int add_next_index_stringl(zval *arg, const char *str, size_t length) /* {{{ */
Zend/zend_API.c:1560:ZEND_API int add_next_index_zval(zval *arg, zval *value) /* {{{ */
Zend/zend_API.c:1566:ZEND_API zval *add_get_assoc_string_ex(zval *arg, const char *key, uint key_len, const char *str) /* {{{ */
Zend/zend_API.c:1576:ZEND_API zval *add_get_assoc_stringl_ex(zval *arg, const char *key, uint key_len, const char *str, size_t length) /* {{{ */
Zend/zend_API.c:1586:ZEND_API zval *add_get_index_long(zval *arg, zend_ulong index, zend_long l) /* {{{ */
Zend/zend_API.c:1595:ZEND_API zval *add_get_index_double(zval *arg, zend_ulong index, double d) /* {{{ */
Zend/zend_API.c:1604:ZEND_API zval *add_get_index_str(zval *arg, zend_ulong index, zend_string *str) /* {{{ */
Zend/zend_API.c:1613:ZEND_API zval *add_get_index_string(zval *arg, zend_ulong index, const char *str) /* {{{ */
Zend/zend_API.c:1622:ZEND_API zval *add_get_index_stringl(zval *arg, zend_ulong index, const char *str, size_t length) /* {{{ */
Zend/zend_API.c:1631:ZEND_API int array_set_zval_key(HashTable *ht, zval *key, zval *value) /* {{{ */
Zend/zend_API.c:1674:ZEND_API int add_property_long_ex(zval *arg, const char *key, size_t key_len, zend_long n) /* {{{ */
Zend/zend_API.c:1688:ZEND_API int add_property_bool_ex(zval *arg, const char *key, size_t key_len, zend_long b) /* {{{ */
Zend/zend_API.c:1702:ZEND_API int add_property_null_ex(zval *arg, const char *key, size_t key_len) /* {{{ */
Zend/zend_API.c:1716:ZEND_API int add_property_resource_ex(zval *arg, const char *key, size_t key_len, zend_resource *r) /* {{{ */
Zend/zend_API.c:1730:ZEND_API int add_property_double_ex(zval *arg, const char *key, size_t key_len, double d) /* {{{ */
Zend/zend_API.c:1744:ZEND_API int add_property_str_ex(zval *arg, const char *key, size_t key_len, zend_string *str) /* {{{ */
Zend/zend_API.c:1758:ZEND_API int add_property_string_ex(zval *arg, const char *key, size_t key_len, const char *str) /* {{{ */
Zend/zend_API.c:1772:ZEND_API int add_property_stringl_ex(zval *arg, const char *key, size_t key_len, const char *str, size_t length) /* {{{ */
Zend/zend_API.c:1786:ZEND_API int add_property_zval_ex(zval *arg, const char *key, size_t key_len, zval *value) /* {{{ */
Zend/zend_API.c:1797:ZEND_API int zend_startup_module_ex(zend_module_entry *module) /* {{{ */
Zend/zend_API.c:1855:static int zend_startup_module_zval(zval *zv) /* {{{ */
Zend/zend_API.c:1863:static void zend_sort_modules(void *base, size_t count, size_t siz, compare_func_t compare, swap_func_t swp) /* {{{ */
Zend/zend_API.c:1898:ZEND_API void zend_collect_module_handlers(void) /* {{{ */
Zend/zend_API.c:1967:ZEND_API int zend_startup_modules(void) /* {{{ */
Zend/zend_API.c:1975:ZEND_API void zend_destroy_modules(void) /* {{{ */
Zend/zend_API.c:1983:ZEND_API zend_module_entry* zend_register_module_ex(zend_module_entry *module) /* {{{ */
Zend/zend_API.c:2043:ZEND_API zend_module_entry* zend_register_internal_module(zend_module_entry *module) /* {{{ */
Zend/zend_API.c:2051:ZEND_API void zend_check_magic_method_implementation(const zend_class_entry *ce, const zend_function *fptr, int error_type) /* {{{ */
Zend/zend_API.c:2116:ZEND_API int zend_register_functions(zend_class_entry *scope, const zend_function_entry *functions, HashTable *function_table, int type) /* {{{ */
Zend/zend_API.c:2425:ZEND_API void zend_unregister_functions(const zend_function_entry *functions, int count, HashTable *function_table) /* {{{ */
Zend/zend_API.c:2451:ZEND_API int zend_startup_module(zend_module_entry *module) /* {{{ */
Zend/zend_API.c:2460:ZEND_API int zend_get_module_started(const char *module_name) /* {{{ */
Zend/zend_API.c:2469:static int clean_module_class(zval *el, void *arg) /* {{{ */
Zend/zend_API.c:2481:static void clean_module_classes(int module_number) /* {{{ */
Zend/zend_API.c:2487:void module_destructor(zend_module_entry *module) /* {{{ */
Zend/zend_API.c:2531:ZEND_API void zend_activate_modules(void) /* {{{ */
Zend/zend_API.c:2548:static int module_registry_cleanup(zval *zv) /* {{{ */
Zend/zend_API.c:2562:ZEND_API void zend_deactivate_modules(void) /* {{{ */
Zend/zend_API.c:2583:ZEND_API void zend_cleanup_internal_classes(void) /* {{{ */
Zend/zend_API.c:2594:int module_registry_unload_temp(const zend_module_entry *module) /* {{{ */
Zend/zend_API.c:2600:static int module_registry_unload_temp_wrapper(zval *el) /* {{{ */
Zend/zend_API.c:2607:static int exec_done_cb(zval *el) /* {{{ */
Zend/zend_API.c:2617:ZEND_API void zend_post_deactivate_modules(void) /* {{{ */
Zend/zend_API.c:2636:ZEND_API int zend_next_free_module(void) /* {{{ */
Zend/zend_API.c:2642:static zend_class_entry *do_register_internal_class(zend_class_entry *orig_class_entry, uint32_t ce_flags) /* {{{ */
Zend/zend_API.c:2670:ZEND_API zend_class_entry *zend_register_internal_class_ex(zend_class_entry *class_entry, zend_class_entry *parent_ce) /* {{{ */
Zend/zend_API.c:2683:ZEND_API void zend_class_implements(zend_class_entry *class_entry, int num_interfaces, ...) /* {{{ */
Zend/zend_API.c:2700:ZEND_API zend_class_entry *zend_register_internal_class(zend_class_entry *orig_class_entry) /* {{{ */
Zend/zend_API.c:2706:ZEND_API zend_class_entry *zend_register_internal_interface(zend_class_entry *orig_class_entry) /* {{{ */
Zend/zend_API.c:2712:ZEND_API int zend_register_class_alias_ex(const char *name, size_t name_len, zend_class_entry *ce) /* {{{ */
Zend/zend_API.c:2736:ZEND_API int zend_set_hash_symbol(zval *symbol, const char *name, int name_length, zend_bool is_ref, int num_symbol_tables, ...) /* {{{ */
Zend/zend_API.c:2764:ZEND_API ZEND_FUNCTION(display_disabled_function)
Zend/zend_API.c:2770:ZEND_API int zend_disable_function(char *function_name, size_t function_name_length) /* {{{ */
Zend/zend_API.c:2787:static zend_object *display_disabled_class(zend_class_entry *class_type) /* {{{ */
Zend/zend_API.c:2804:ZEND_API int zend_disable_class(char *class_name, size_t class_name_length) /* {{{ */
Zend/zend_API.c:2822:static int zend_is_callable_check_class(zend_string *name, zend_fcall_info_cache *fcc, int *strict_class, char **error) /* {{{ */
Zend/zend_API.c:2906:static int zend_is_callable_check_func(int check_flags, zval *callable, zend_fcall_info_cache *fcc, int strict_class, char **error) /* {{{ */
Zend/zend_API.c:3177:ZEND_API zend_bool zend_is_callable_ex(zval *callable, zend_object *object, uint check_flags, zend_string **callable_name, zend_fcall_info_cache *fcc, char **error) /* {{{ */
Zend/zend_API.c:3376:ZEND_API zend_bool zend_is_callable(zval *callable, uint check_flags, zend_string **callable_name) /* {{{ */
Zend/zend_API.c:3382:ZEND_API zend_bool zend_make_callable(zval *callable, zend_string **callable_name) /* {{{ */
Zend/zend_API.c:3408:ZEND_API int zend_fcall_info_init(zval *callable, uint check_flags, zend_fcall_info *fci, zend_fcall_info_cache *fcc, zend_string **callable_name, char **error) /* {{{ */
Zend/zend_API.c:3426:ZEND_API void zend_fcall_info_args_clear(zend_fcall_info *fci, int free_mem) /* {{{ */
Zend/zend_API.c:3445:ZEND_API void zend_fcall_info_args_save(zend_fcall_info *fci, int *param_count, zval **params) /* {{{ */
Zend/zend_API.c:3454:ZEND_API void zend_fcall_info_args_restore(zend_fcall_info *fci, int param_count, zval *params) /* {{{ */
Zend/zend_API.c:3462:ZEND_API int zend_fcall_info_args_ex(zend_fcall_info *fci, zend_function *func, zval *args) /* {{{ */
Zend/zend_API.c:3497:ZEND_API int zend_fcall_info_args(zend_fcall_info *fci, zval *args) /* {{{ */
Zend/zend_API.c:3503:ZEND_API int zend_fcall_info_argp(zend_fcall_info *fci, int argc, zval *argv) /* {{{ */
Zend/zend_API.c:3526:ZEND_API int zend_fcall_info_argv(zend_fcall_info *fci, int argc, va_list *argv) /* {{{ */
Zend/zend_API.c:3551:ZEND_API int zend_fcall_info_argn(zend_fcall_info *fci, int argc, ...) /* {{{ */
Zend/zend_API.c:3564:ZEND_API int zend_fcall_info_call(zend_fcall_info *fci, zend_fcall_info_cache *fcc, zval *retval_ptr, zval *args) /* {{{ */
Zend/zend_API.c:3586:ZEND_API const char *zend_get_module_version(const char *module_name) /* {{{ */
Zend/zend_API.c:3600:ZEND_API int zend_declare_property_ex(zend_class_entry *ce, zend_string *name, zval *property, int access_type, zend_string *doc_comment) /* {{{ */
Zend/zend_API.c:3676:ZEND_API int zend_declare_property(zend_class_entry *ce, const char *name, size_t name_length, zval *property, int access_type) /* {{{ */
Zend/zend_API.c:3685:ZEND_API int zend_declare_property_null(zend_class_entry *ce, const char *name, size_t name_length, int access_type) /* {{{ */
Zend/zend_API.c:3694:ZEND_API int zend_declare_property_bool(zend_class_entry *ce, const char *name, size_t name_length, zend_long value, int access_type) /* {{{ */
Zend/zend_API.c:3703:ZEND_API int zend_declare_property_long(zend_class_entry *ce, const char *name, size_t name_length, zend_long value, int access_type) /* {{{ */
Zend/zend_API.c:3712:ZEND_API int zend_declare_property_double(zend_class_entry *ce, const char *name, size_t name_length, double value, int access_type) /* {{{ */
Zend/zend_API.c:3721:ZEND_API int zend_declare_property_string(zend_class_entry *ce, const char *name, size_t name_length, const char *value, int access_type) /* {{{ */
Zend/zend_API.c:3730:ZEND_API int zend_declare_property_stringl(zend_class_entry *ce, const char *name, size_t name_length, const char *value, size_t value_len, int access_type) /* {{{ */
Zend/zend_API.c:3739:ZEND_API int zend_declare_class_constant_ex(zend_class_entry *ce, zend_string *name, zval *value, int access_type, zend_string *doc_comment) /* {{{ */
Zend/zend_API.c:3776:ZEND_API int zend_declare_class_constant(zend_class_entry *ce, const char *name, size_t name_length, zval *value) /* {{{ */
Zend/zend_API.c:3787:ZEND_API int zend_declare_class_constant_null(zend_class_entry *ce, const char *name, size_t name_length) /* {{{ */
Zend/zend_API.c:3796:ZEND_API int zend_declare_class_constant_long(zend_class_entry *ce, const char *name, size_t name_length, zend_long value) /* {{{ */
Zend/zend_API.c:3805:ZEND_API int zend_declare_class_constant_bool(zend_class_entry *ce, const char *name, size_t name_length, zend_bool value) /* {{{ */
Zend/zend_API.c:3814:ZEND_API int zend_declare_class_constant_double(zend_class_entry *ce, const char *name, size_t name_length, double value) /* {{{ */
Zend/zend_API.c:3823:ZEND_API int zend_declare_class_constant_stringl(zend_class_entry *ce, const char *name, size_t name_length, const char *value, size_t value_length) /* {{{ */
Zend/zend_API.c:3832:ZEND_API int zend_declare_class_constant_string(zend_class_entry *ce, const char *name, size_t name_length, const char *value) /* {{{ */
Zend/zend_API.c:3838:ZEND_API void zend_update_property_ex(zend_class_entry *scope, zval *object, zend_string *name, zval *value) /* {{{ */
Zend/zend_API.c:3855:ZEND_API void zend_update_property(zend_class_entry *scope, zval *object, const char *name, size_t name_length, zval *value) /* {{{ */
Zend/zend_API.c:3873:ZEND_API void zend_update_property_null(zend_class_entry *scope, zval *object, const char *name, size_t name_length) /* {{{ */
Zend/zend_API.c:3882:ZEND_API void zend_update_property_bool(zend_class_entry *scope, zval *object, const char *name, size_t name_length, zend_long value) /* {{{ */
Zend/zend_API.c:3891:ZEND_API void zend_update_property_long(zend_class_entry *scope, zval *object, const char *name, size_t name_length, zend_long value) /* {{{ */
Zend/zend_API.c:3900:ZEND_API void zend_update_property_double(zend_class_entry *scope, zval *object, const char *name, size_t name_length, double value) /* {{{ */
Zend/zend_API.c:3909:ZEND_API void zend_update_property_str(zend_class_entry *scope, zval *object, const char *name, size_t name_length, zend_string *value) /* {{{ */
Zend/zend_API.c:3918:ZEND_API void zend_update_property_string(zend_class_entry *scope, zval *object, const char *name, size_t name_length, const char *value) /* {{{ */
Zend/zend_API.c:3928:ZEND_API void zend_update_property_stringl(zend_class_entry *scope, zval *object, const char *name, size_t name_length, const char *value, size_t value_len) /* {{{ */
Zend/zend_API.c:3938:ZEND_API int zend_update_static_property(zend_class_entry *scope, const char *name, size_t name_length, zval *value) /* {{{ */
Zend/zend_API.c:3977:ZEND_API int zend_update_static_property_null(zend_class_entry *scope, const char *name, size_t name_length) /* {{{ */
Zend/zend_API.c:3986:ZEND_API int zend_update_static_property_bool(zend_class_entry *scope, const char *name, size_t name_length, zend_long value) /* {{{ */
Zend/zend_API.c:3995:ZEND_API int zend_update_static_property_long(zend_class_entry *scope, const char *name,
... [truncated to budget] ...
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=Zend/zend_ast.c, max_results=300)` →

```
39 matches
Zend/zend_ast.c:31:static inline void *zend_ast_alloc(size_t size) {
Zend/zend_ast.c:35:static inline void *zend_ast_realloc(void *old, size_t old_size, size_t new_size) {
Zend/zend_ast.c:41:static inline size_t zend_ast_size(uint32_t children) {
Zend/zend_ast.c:45:static inline size_t zend_ast_list_size(uint32_t children) {
Zend/zend_ast.c:49:ZEND_API zend_ast *zend_ast_create_znode(znode *node) {
Zend/zend_ast.c:60:ZEND_API zend_ast *zend_ast_create_zval_ex(zval *zv, zend_ast_attr attr) {
Zend/zend_ast.c:71:ZEND_API zend_ast *zend_ast_create_decl(
Zend/zend_ast.c:94:static zend_ast *zend_ast_create_from_va_list(zend_ast_kind kind, zend_ast_attr attr, va_list va) {
Zend/zend_ast.c:120:ZEND_API zend_ast *zend_ast_create_ex(zend_ast_kind kind, zend_ast_attr attr, ...) {
Zend/zend_ast.c:131:ZEND_API zend_ast *zend_ast_create(zend_ast_kind kind, ...) {
Zend/zend_ast.c:142:ZEND_API zend_ast *zend_ast_create_list(uint32_t init_children, zend_ast_kind kind, ...) {
Zend/zend_ast.c:166:static inline zend_bool is_power_of_two(uint32_t n) {
Zend/zend_ast.c:170:ZEND_API zend_ast *zend_ast_list_add(zend_ast *ast, zend_ast *op) {
Zend/zend_ast.c:180:static int zend_ast_add_array_element(zval *result, zval *offset, zval *expr)
Zend/zend_ast.c:212:ZEND_API int zend_ast_evaluate(zval *result, zend_ast *ast, zend_class_entry *scope)
Zend/zend_ast.c:439:ZEND_API zend_ast *zend_ast_copy(zend_ast *ast)
Zend/zend_ast.c:472:static void zend_ast_destroy_ex(zend_ast *ast, zend_bool free) {
Zend/zend_ast.c:522:ZEND_API void zend_ast_destroy(zend_ast *ast) {
Zend/zend_ast.c:525:ZEND_API void zend_ast_destroy_and_free(zend_ast *ast) {
Zend/zend_ast.c:529:ZEND_API void zend_ast_apply(zend_ast *ast, zend_ast_apply_func fn) {
Zend/zend_ast.c:579:static void zend_ast_export_ex(smart_str *str, zend_ast *ast, int priority, int indent);
Zend/zend_ast.c:581:static void zend_ast_export_str(smart_str *str, zend_string *s)
Zend/zend_ast.c:596:static void zend_ast_export_qstr(smart_str *str, char quote, zend_string *s)
Zend/zend_ast.c:641:static void zend_ast_export_indent(smart_str *str, int indent)
Zend/zend_ast.c:649:static void zend_ast_export_name(smart_str *str, zend_ast *ast, int priority, int indent)
Zend/zend_ast.c:662:static void zend_ast_export_ns_name(smart_str *str, zend_ast *ast, int priority, int indent)
Zend/zend_ast.c:680:static int zend_ast_valid_var_char(char ch)
Zend/zend_ast.c:693:static int zend_ast_valid_var_name(const char *s, size_t len)
Zend/zend_ast.c:719:static void zend_ast_export_var(smart_str *str, zend_ast *ast, int priority, int indent)
Zend/zend_ast.c:737:static void zend_ast_export_list(smart_str *str, zend_ast_list *list, int separator, int priority, int indent)
Zend/zend_ast.c:750:static void zend_ast_export_encaps_list(smart_str *str, char quote, zend_ast_list *list, int indent)
Zend/zend_ast.c:779:static void zend_ast_export_name_list(smart_str *str, zend_ast_list *list, int indent)
Zend/zend_ast.c:792:static void zend_ast_export_var_list(smart_str *str, zend_ast_list *list, int indent)
Zend/zend_ast.c:809:static void zend_ast_export_stmt(smart_str *str, zend_ast *ast, int indent)
Zend/zend_ast.c:851:static void zend_ast_export_if_stmt(smart_str *str, zend_ast_list *list, int indent)
Zend/zend_ast.c:888:static void zend_ast_export_zval(smart_str *str, zval *zv, int priority, int indent)
Zend/zend_ast.c:950:static void zend_ast_export_class_no_header(smart_str *str, zend_ast_decl *decl, int indent) {
Zend/zend_ast.c:1007:static void zend_ast_export_ex(smart_str *str, zend_ast *ast, int priority, int indent)
Zend/zend_ast.c:1697:ZEND_API zend_string *zend_ast_export(const char *prefix, zend_ast *ast, const char *suffix)
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=Zend/zend_builtin_functions.c, max_results=300)` →

```
205 matches (showing 200)
Zend/zend_builtin_functions.c:40:static ZEND_FUNCTION(zend_version);
Zend/zend_builtin_functions.c:41:static ZEND_FUNCTION(func_num_args);
Zend/zend_builtin_functions.c:42:static ZEND_FUNCTION(func_get_arg);
Zend/zend_builtin_functions.c:43:static ZEND_FUNCTION(func_get_args);
Zend/zend_builtin_functions.c:44:static ZEND_FUNCTION(strlen);
Zend/zend_builtin_functions.c:45:static ZEND_FUNCTION(strcmp);
Zend/zend_builtin_functions.c:46:static ZEND_FUNCTION(strncmp);
Zend/zend_builtin_functions.c:47:static ZEND_FUNCTION(strcasecmp);
Zend/zend_builtin_functions.c:48:static ZEND_FUNCTION(strncasecmp);
Zend/zend_builtin_functions.c:49:static ZEND_FUNCTION(each);
Zend/zend_builtin_functions.c:50:static ZEND_FUNCTION(error_reporting);
Zend/zend_builtin_functions.c:51:static ZEND_FUNCTION(define);
Zend/zend_builtin_functions.c:52:static ZEND_FUNCTION(defined);
Zend/zend_builtin_functions.c:53:static ZEND_FUNCTION(get_class);
Zend/zend_builtin_functions.c:54:static ZEND_FUNCTION(get_called_class);
Zend/zend_builtin_functions.c:55:static ZEND_FUNCTION(get_parent_class);
Zend/zend_builtin_functions.c:56:static ZEND_FUNCTION(method_exists);
Zend/zend_builtin_functions.c:57:static ZEND_FUNCTION(property_exists);
Zend/zend_builtin_functions.c:58:static ZEND_FUNCTION(class_exists);
Zend/zend_builtin_functions.c:59:static ZEND_FUNCTION(interface_exists);
Zend/zend_builtin_functions.c:60:static ZEND_FUNCTION(trait_exists);
Zend/zend_builtin_functions.c:61:static ZEND_FUNCTION(function_exists);
Zend/zend_builtin_functions.c:62:static ZEND_FUNCTION(class_alias);
Zend/zend_builtin_functions.c:64:static ZEND_FUNCTION(leak);
Zend/zend_builtin_functions.c:65:static ZEND_FUNCTION(leak_variable);
Zend/zend_builtin_functions.c:67:static ZEND_FUNCTION(crash);
Zend/zend_builtin_functions.c:70:static ZEND_FUNCTION(get_included_files);
Zend/zend_builtin_functions.c:71:static ZEND_FUNCTION(is_subclass_of);
Zend/zend_builtin_functions.c:72:static ZEND_FUNCTION(is_a);
Zend/zend_builtin_functions.c:73:static ZEND_FUNCTION(get_class_vars);
Zend/zend_builtin_functions.c:74:static ZEND_FUNCTION(get_object_vars);
Zend/zend_builtin_functions.c:75:static ZEND_FUNCTION(get_class_methods);
Zend/zend_builtin_functions.c:76:static ZEND_FUNCTION(trigger_error);
Zend/zend_builtin_functions.c:77:static ZEND_FUNCTION(set_error_handler);
Zend/zend_builtin_functions.c:78:static ZEND_FUNCTION(restore_error_handler);
Zend/zend_builtin_functions.c:79:static ZEND_FUNCTION(set_exception_handler);
Zend/zend_builtin_functions.c:80:static ZEND_FUNCTION(restore_exception_handler);
Zend/zend_builtin_functions.c:81:static ZEND_FUNCTION(get_declared_classes);
Zend/zend_builtin_functions.c:82:static ZEND_FUNCTION(get_declared_traits);
Zend/zend_builtin_functions.c:83:static ZEND_FUNCTION(get_declared_interfaces);
Zend/zend_builtin_functions.c:84:static ZEND_FUNCTION(get_defined_functions);
Zend/zend_builtin_functions.c:85:static ZEND_FUNCTION(get_defined_vars);
Zend/zend_builtin_functions.c:86:static ZEND_FUNCTION(create_function);
Zend/zend_builtin_functions.c:87:static ZEND_FUNCTION(get_resource_type);
Zend/zend_builtin_functions.c:88:static ZEND_FUNCTION(get_resources);
Zend/zend_builtin_functions.c:89:static ZEND_FUNCTION(get_loaded_extensions);
Zend/zend_builtin_functions.c:90:static ZEND_FUNCTION(extension_loaded);
Zend/zend_builtin_functions.c:91:static ZEND_FUNCTION(get_extension_funcs);
Zend/zend_builtin_functions.c:92:static ZEND_FUNCTION(get_defined_constants);
Zend/zend_builtin_functions.c:93:static ZEND_FUNCTION(debug_backtrace);
Zend/zend_builtin_functions.c:94:static ZEND_FUNCTION(debug_print_backtrace);
Zend/zend_builtin_functions.c:96:static ZEND_FUNCTION(zend_test_func);
Zend/zend_builtin_functions.c:97:static ZEND_FUNCTION(zend_test_func2);
Zend/zend_builtin_functions.c:99:static ZEND_FUNCTION(zend_thread_id);
Zend/zend_builtin_functions.c:102:static ZEND_FUNCTION(gc_mem_caches);
Zend/zend_builtin_functions.c:103:static ZEND_FUNCTION(gc_collect_cycles);
Zend/zend_builtin_functions.c:104:static ZEND_FUNCTION(gc_enabled);
Zend/zend_builtin_functions.c:105:static ZEND_FUNCTION(gc_enable);
Zend/zend_builtin_functions.c:106:static ZEND_FUNCTION(gc_disable);
Zend/zend_builtin_functions.c:109:ZEND_BEGIN_ARG_INFO(arginfo_zend__void, 0)
Zend/zend_builtin_functions.c:110:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:112:ZEND_BEGIN_ARG_INFO_EX(arginfo_func_get_arg, 0, 0, 1)
Zend/zend_builtin_functions.c:114:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:116:ZEND_BEGIN_ARG_INFO_EX(arginfo_strlen, 0, 0, 1)
Zend/zend_builtin_functions.c:118:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:120:ZEND_BEGIN_ARG_INFO_EX(arginfo_strcmp, 0, 0, 2)
Zend/zend_builtin_functions.c:123:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:125:ZEND_BEGIN_ARG_INFO_EX(arginfo_strncmp, 0, 0, 3)
Zend/zend_builtin_functions.c:129:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:131:ZEND_BEGIN_ARG_INFO_EX(arginfo_each, 0, 0, 1)
Zend/zend_builtin_functions.c:133:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:135:ZEND_BEGIN_ARG_INFO_EX(arginfo_error_reporting, 0, 0, 0)
Zend/zend_builtin_functions.c:137:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:139:ZEND_BEGIN_ARG_INFO_EX(arginfo_define, 0, 0, 2)
Zend/zend_builtin_functions.c:143:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:145:ZEND_BEGIN_ARG_INFO_EX(arginfo_defined, 0, 0, 1)
Zend/zend_builtin_functions.c:147:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:149:ZEND_BEGIN_ARG_INFO_EX(arginfo_get_class, 0, 0, 0)
Zend/zend_builtin_functions.c:151:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:153:ZEND_BEGIN_ARG_INFO_EX(arginfo_is_subclass_of, 0, 0, 2)
Zend/zend_builtin_functions.c:157:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:159:ZEND_BEGIN_ARG_INFO_EX(arginfo_get_class_vars, 0, 0, 1)
Zend/zend_builtin_functions.c:161:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:163:ZEND_BEGIN_ARG_INFO_EX(arginfo_get_object_vars, 0, 0, 1)
Zend/zend_builtin_functions.c:165:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:167:ZEND_BEGIN_ARG_INFO_EX(arginfo_get_class_methods, 0, 0, 1)
Zend/zend_builtin_functions.c:169:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:171:ZEND_BEGIN_ARG_INFO_EX(arginfo_method_exists, 0, 0, 2)
Zend/zend_builtin_functions.c:174:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:176:ZEND_BEGIN_ARG_INFO_EX(arginfo_property_exists, 0, 0, 2)
Zend/zend_builtin_functions.c:179:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:181:ZEND_BEGIN_ARG_INFO_EX(arginfo_class_exists, 0, 0, 1)
Zend/zend_builtin_functions.c:184:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:186:ZEND_BEGIN_ARG_INFO_EX(arginfo_trait_exists, 0, 0, 1)
Zend/zend_builtin_functions.c:189:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:191:ZEND_BEGIN_ARG_INFO_EX(arginfo_function_exists, 0, 0, 1)
Zend/zend_builtin_functions.c:193:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:195:ZEND_BEGIN_ARG_INFO_EX(arginfo_class_alias, 0, 0, 2)
Zend/zend_builtin_functions.c:199:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:202:ZEND_BEGIN_ARG_INFO_EX(arginfo_leak_variable, 0, 0, 1)
Zend/zend_builtin_functions.c:205:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:208:ZEND_BEGIN_ARG_INFO_EX(arginfo_trigger_error, 0, 0, 1)
Zend/zend_builtin_functions.c:211:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:213:ZEND_BEGIN_ARG_INFO_EX(arginfo_set_error_handler, 0, 0, 1)
Zend/zend_builtin_functions.c:216:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:218:ZEND_BEGIN_ARG_INFO_EX(arginfo_set_exception_handler, 0, 0, 1)
Zend/zend_builtin_functions.c:220:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:222:ZEND_BEGIN_ARG_INFO_EX(arginfo_create_function, 0, 0, 2)
Zend/zend_builtin_functions.c:225:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:227:ZEND_BEGIN_ARG_INFO_EX(arginfo_get_resource_type, 0, 0, 1)
Zend/zend_builtin_functions.c:229:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:231:ZEND_BEGIN_ARG_INFO_EX(arginfo_get_resources, 0, 0, 0)
Zend/zend_builtin_functions.c:233:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:235:ZEND_BEGIN_ARG_INFO_EX(arginfo_get_loaded_extensions, 0, 0, 0)
Zend/zend_builtin_functions.c:237:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:239:ZEND_BEGIN_ARG_INFO_EX(arginfo_get_defined_constants, 0, 0, 0)
Zend/zend_builtin_functions.c:241:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:243:ZEND_BEGIN_ARG_INFO_EX(arginfo_debug_backtrace, 0, 0, 0)
Zend/zend_builtin_functions.c:246:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:248:ZEND_BEGIN_ARG_INFO_EX(arginfo_debug_print_backtrace, 0, 0, 0)
Zend/zend_builtin_functions.c:251:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:253:ZEND_BEGIN_ARG_INFO_EX(arginfo_extension_loaded, 0, 0, 1)
Zend/zend_builtin_functions.c:255:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:258:ZEND_BEGIN_ARG_WITH_RETURN_TYPE_INFO(arginfo_zend_test_func, IS_ARRAY, NULL, 0)
Zend/zend_builtin_functions.c:259:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:260:ZEND_BEGIN_ARG_WITH_RETURN_TYPE_INFO(arginfo_zend_test_func2, IS_ARRAY, NULL, 1)
Zend/zend_builtin_functions.c:261:ZEND_END_ARG_INFO()
Zend/zend_builtin_functions.c:267:static zend_object *zend_test_class_new(zend_class_entry *class_type) /* {{{ */ {
Zend/zend_builtin_functions.c:274:static zend_function *zend_test_class_method_get(zend_object **object, zend_string *name, const zval *key) /* {{{ */ {
Zend/zend_builtin_functions.c:289:static zend_function *zend_test_class_static_method_get(zend_class_entry *ce, zend_string *name) /* {{{ */ {
Zend/zend_builtin_functions.c:304:static int zend_test_class_call_method(zend_string *method, zend_object *object, INTERNAL_FUNCTION_PARAMETERS) /* {{{ */ {
Zend/zend_builtin_functions.c:385:ZEND_MINIT_FUNCTION(core) { /* {{{ */
Zend/zend_builtin_functions.c:426:int zend_startup_builtin_functions(void) /* {{{ */
Zend/zend_builtin_functions.c:436:ZEND_FUNCTION(zend_version)
Zend/zend_builtin_functions.c:445:ZEND_FUNCTION(gc_mem_caches)
Zend/zend_builtin_functions.c:454:ZEND_FUNCTION(gc_collect_cycles)
Zend/zend_builtin_functions.c:462:ZEND_FUNCTION(gc_enabled)
Zend/zend_builtin_functions.c:470:ZEND_FUNCTION(gc_enable)
Zend/zend_builtin_functions.c:480:ZEND_FUNCTION(gc_disable)
Zend/zend_builtin_functions.c:490:ZEND_FUNCTION(func_num_args)
Zend/zend_builtin_functions.c:505:ZEND_FUNCTION(func_get_arg)
Zend/zend_builtin_functions.c:549:ZEND_FUNCTION(func_get_args)
Zend/zend_builtin_functions.c:609:ZEND_FUNCTION(strlen)
Zend/zend_builtin_functions.c:629:ZEND_FUNCTION(strcmp)
Zend/zend_builtin_functions.c:643:ZEND_FUNCTION(strncmp)
Zend/zend_builtin_functions.c:663:ZEND_FUNCTION(strcasecmp)
Zend/zend_builtin_functions.c:677:ZEND_FUNCTION(strncasecmp)
Zend/zend_builtin_functions.c:697:ZEND_FUNCTION(each)
Zend/zend_builtin_functions.c:756:ZEND_FUNCTION(error_reporting)
Zend/zend_builtin_functions.c:812:static int validate_constant_array(HashTable *ht) /* {{{ */
Zend/zend_builtin_functions.c:844:static void copy_constant_array(zval *dst, zval *src) /* {{{ */
Zend/zend_builtin_functions.c:875:ZEND_FUNCTION(define)
Zend/zend_builtin_functions.c:971:ZEND_FUNCTION(defined)
Zend/zend_builtin_functions.c:995:ZEND_FUNCTION(get_class)
Zend/zend_builtin_functions.c:1018:ZEND_FUNCTION(get_called_class)
Zend/zend_builtin_functions.c:1038:ZEND_FUNCTION(get_parent_class)
Zend/zend_builtin_functions.c:1070:static void is_a_impl(INTERNAL_FUNCTION_PARAMETERS, zend_bool only_subclass) /* {{{ */
Zend/zend_builtin_functions.c:1130:ZEND_FUNCTION(is_subclass_of)
Zend/zend_builtin_functions.c:1138:ZEND_FUNCTION(is_a)
Zend/zend_builtin_functions.c:1145:static void add_class_vars(zend_class_entry *ce, int statics, zval *return_value)
Zend/zend_builtin_functions.c:1195:ZEND_FUNCTION(get_class_vars)
Zend/zend_builtin_functions.c:1222:ZEND_FUNCTION(get_object_vars)
Zend/zend_builtin_functions.c:1288:static int same_name(zend_string *key, zend_string *name) /* {{{ */
Zend/zend_builtin_functions.c:1308:ZEND_FUNCTION(get_class_methods)
Zend/zend_builtin_functions.c:1367:ZEND_FUNCTION(method_exists)
Zend/zend_builtin_functions.c:1426:ZEND_FUNCTION(property_exists)
Zend/zend_builtin_functions.c:1472:ZEND_FUNCTION(class_exists)
Zend/zend_builtin_functions.c:1516:ZEND_FUNCTION(interface_exists)
Zend/zend_builtin_functions.c:1558:ZEND_FUNCTION(trait_exists)
Zend/zend_builtin_functions.c:1601:ZEND_FUNCTION(function_exists)
Zend/zend_builtin_functions.c:1639:ZEND_FUNCTION(class_alias)
Zend/zend_builtin_functions.c:1675:ZEND_FUNCTION(leak)
Zend/zend_builtin_functions.c:1689:ZEND_FUNCTION(leak_variable)
Zend/zend_builtin_functions.c:1714:ZEND_FUNCTION(crash)
Zend/zend_builtin_functions.c:1731:ZEND_FUNCTION(get_included_files)
Zend/zend_builtin_functions.c:1750:ZEND_FUNCTION(trigger_error)
Zend/zend_builtin_functions.c:1779:ZEND_FUNCTION(set_error_handler)
Zend/zend_builtin_functions.c:1818:ZEND_FUNCTION(restore_error_handler)
Zend/zend_builtin_functions.c:1848:ZEND_FUNCTION(set_exception_handler)
Zend/zend_builtin_functions.c:1884:ZEND_FUNCTION(restore_exception_handler)
Zend/zend_builtin_functions.c:1904:static int copy_class_or_interface_name(zval *el, int num_args, va_list args, zend_hash_key *hash_key) /* {{{ */
Zend/zend_builtin_functions.c:1927:ZEND_FUNCTION(get_declared_traits)
Zend/zend_builtin_functions.c:1943:ZEND_FUNCTION(get_declared_classes)
Zend/zend_builtin_functions.c:1959:ZEND_FUNCTION(get_declared_interfaces)
Zend/zend_builtin_functions.c:1973:static int copy_function_name(zval *zv, int num_args, va_list args, zend_hash_key *hash_key) /* {{{ */
Zend/zend_builtin_functions.c:1995:ZEND_FUNCTION(get_defined_functions)
Zend/zend_builtin_functions.c:2016:ZEND_FUNCTION(get_defined_vars)
Zend/zend_builtin_functions.c:2031:ZEND_FUNCTION(create_function)
Zend/zend_builtin_functions.c:2101:ZEND_FUNCTION(zend_test_func)
Zend/zend_builtin_functions.c:2108:ZEND_FUNCTION(zend_test_func2)
Zend/zend_builtin_functions.c:2116:ZEND_FUNCTION(zend_thread_id)
Zend/zend_builtin_functions.c:2125:ZEND_FUNCTION(get_resource_type)
Zend/zend_builtin_functions.c:2145:ZEND_FUNCTION(get_resources)
Zend/zend_builtin_functions.c:2191:static int add_extension_info(zval *item, void *arg) /* {{{ */
Zend/zend_builtin_functions.c:2200:static int add_zendext_info(zend_extension *ext, void *arg) /* {{{ */
Zend/zend_builtin_functions.c:2208:static int add_constant_info(zval *item, void *arg) /* {{{ */
Zend/zend_builtin_functions.c:2227:ZEND_FUNCTION(get_loaded_extensions)
Zend/zend_builtin_functions.c:2247:ZEND_FUNCTION(get_defined_constants)
Zend/zend_builtin_functions.c:2307:static void debug_backtrace_get_args(zend_execute_data *call, zval *arg_array) /* {{{ */
Zend/zend_builtin_functions.c:2355:void debug_print_backtrace_args(zval *arg_array) /* {{{ */
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=Zend/zend_constants.c, max_results=300)` →

```
25 matches
Zend/zend_constants.c:31:void free_zend_constant(zval *zv)
Zend/zend_constants.c:47:static void copy_zend_constant(zval *zv)
Zend/zend_constants.c:66:void zend_copy_constants(HashTable *target, HashTable *source)
Zend/zend_constants.c:72:static int clean_non_persistent_constant(zval *zv)
Zend/zend_constants.c:79:static int clean_non_persistent_constant_full(zval *zv)
Zend/zend_constants.c:86:static int clean_module_constant(zval *el, void *arg)
Zend/zend_constants.c:99:void clean_module_constants(int module_number)
Zend/zend_constants.c:105:int zend_startup_constants(void)
Zend/zend_constants.c:115:void zend_register_standard_constants(void)
Zend/zend_constants.c:148:int zend_shutdown_constants(void)
Zend/zend_constants.c:156:void clean_non_persistent_constants(void)
Zend/zend_constants.c:165:ZEND_API void zend_register_null_constant(const char *name, size_t name_len, int flags, int module_number)
Zend/zend_constants.c:176:ZEND_API void zend_register_bool_constant(const char *name, size_t name_len, zend_bool bval, int flags, int module_number)
Zend/zend_constants.c:187:ZEND_API void zend_register_long_constant(const char *name, size_t name_len, zend_long lval, int flags, int module_number)
Zend/zend_constants.c:199:ZEND_API void zend_register_double_constant(const char *name, size_t name_len, double dval, int flags, int module_number)
Zend/zend_constants.c:211:ZEND_API void zend_register_stringl_constant(const char *name, size_t name_len, char *strval, size_t strlen, int flags, int module_number)
Zend/zend_constants.c:223:ZEND_API void zend_register_string_constant(const char *name, size_t name_len, char *strval, int flags, int module_number)
Zend/zend_constants.c:228:static zend_constant *zend_get_special_constant(const char *name, size_t name_len)
Zend/zend_constants.c:254:ZEND_API int zend_verify_const_access(zend_class_constant *c, zend_class_entry *scope) /* {{{ */
Zend/zend_constants.c:267:ZEND_API zval *zend_get_constant_str(const char *name, size_t name_len)
Zend/zend_constants.c:288:ZEND_API zval *zend_get_constant(zend_string *name)
Zend/zend_constants.c:309:ZEND_API zval *zend_get_constant_ex(zend_string *cname, zend_class_entry *scope, uint32_t flags)
Zend/zend_constants.c:449:zend_constant *zend_quick_get_constant(const zval *key, uint32_t flags)
Zend/zend_constants.c:477:static void* zend_hash_add_constant(HashTable *ht, zend_string *key, zend_constant *c)
Zend/zend_constants.c:490:ZEND_API int zend_register_constant(zend_constant *c)
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=Zend/zend_execute.c, max_results=300)` →

```
124 matches
Zend/zend_execute.c:54:typedef int (ZEND_FASTCALL *incdec_t)(zval *);
Zend/zend_execute.c:68:static void zend_extension_statement_handler(const zend_extension *extension, zend_op_array *op_array);
Zend/zend_execute.c:69:static void zend_extension_fcall_begin_handler(const zend_extension *extension, zend_op_array *op_array);
Zend/zend_execute.c:70:static void zend_extension_fcall_end_handler(const zend_extension *extension, zend_op_array *op_array);
Zend/zend_execute.c:74:static ZEND_FUNCTION(pass)
Zend/zend_execute.c:135:static zend_always_inline zend_vm_stack zend_vm_stack_new_page(size_t size, zend_vm_stack prev) {
Zend/zend_execute.c:144:ZEND_API void zend_vm_stack_init(void)
Zend/zend_execute.c:152:ZEND_API void zend_vm_stack_destroy(void)
Zend/zend_execute.c:163:ZEND_API void* zend_vm_stack_extend(size_t size)
Zend/zend_execute.c:180:ZEND_API zval* zend_get_compiled_variable_value(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:185:static zend_always_inline zval *_get_zval_ptr_tmp(uint32_t var, const zend_execute_data *execute_data, zend_free_op *should_free)
Zend/zend_execute.c:195:static zend_always_inline zval *_get_zval_ptr_var(uint32_t var, const zend_execute_data *execute_data, zend_free_op *should_free)
Zend/zend_execute.c:203:static zend_always_inline zval *_get_zval_ptr_var_deref(uint32_t var, const zend_execute_data *execute_data, zend_free_op *should_free)
Zend/zend_execute.c:212:static zend_never_inline ZEND_COLD void zval_undefined_cv(uint32_t var, const zend_execute_data *execute_data)
Zend/zend_execute.c:219:static zend_never_inline zval *_get_zval_cv_lookup(zval *ptr, uint32_t var, int type, const zend_execute_data *execute_data)
Zend/zend_execute.c:239:static zend_always_inline zval *_get_zval_cv_lookup_BP_VAR_R(zval *ptr, uint32_t var, const zend_execute_data *execute_data)
Zend/zend_execute.c:245:static zend_always_inline zval *_get_zval_cv_lookup_BP_VAR_UNSET(zval *ptr, uint32_t var, const zend_execute_data *execute_data)
Zend/zend_execute.c:251:static zend_always_inline zval *_get_zval_cv_lookup_BP_VAR_RW(zval *ptr, uint32_t var, const zend_execute_data *execute_data)
Zend/zend_execute.c:258:static zend_always_inline zval *_get_zval_cv_lookup_BP_VAR_W(zval *ptr, uint32_t var, const zend_execute_data *execute_data)
Zend/zend_execute.c:264:static zend_always_inline zval *_get_zval_ptr_cv(const zend_execute_data *execute_data, uint32_t var, int type)
Zend/zend_execute.c:274:static zend_always_inline zval *_get_zval_ptr_cv_undef(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:279:static zend_always_inline zval *_get_zval_ptr_cv_deref(const zend_execute_data *execute_data, uint32_t var, int type)
Zend/zend_execute.c:290:static zend_always_inline zval *_get_zval_ptr_cv_BP_VAR_R(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:300:static zend_always_inline zval *_get_zval_ptr_cv_deref_BP_VAR_R(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:311:static zend_always_inline zval *_get_zval_ptr_cv_BP_VAR_UNSET(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:321:static zend_always_inline zval *_get_zval_ptr_cv_deref_BP_VAR_UNSET(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:332:static zend_always_inline zval *_get_zval_ptr_cv_BP_VAR_IS(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:339:static zend_always_inline zval *_get_zval_ptr_cv_deref_BP_VAR_IS(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:347:static zend_always_inline zval *_get_zval_ptr_cv_BP_VAR_RW(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:357:static zend_always_inline zval *_get_zval_ptr_cv_deref_BP_VAR_RW(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:368:static zend_always_inline zval *_get_zval_ptr_cv_BP_VAR_W(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:378:static zend_always_inline zval *_get_zval_ptr_cv_undef_BP_VAR_W(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:383:static zend_always_inline zval *_get_zval_ptr_cv_undef_BP_VAR_RW(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:388:static zend_always_inline zval *_get_zval_ptr_cv_undef_BP_VAR_UNSET(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:393:static zend_always_inline zval *_get_zval_ptr_cv_deref_BP_VAR_W(const zend_execute_data *execute_data, uint32_t var)
Zend/zend_execute.c:404:static zend_always_inline zval *_get_zval_ptr(int op_type, znode_op node, const zend_execute_data *execute_data, zend_free_op *should_free, int type)
Zend/zend_execute.c:425:static zend_always_inline zval *_get_zval_ptr_r(int op_type, znode_op node, const zend_execute_data *execute_data, zend_free_op *should_free)
Zend/zend_execute.c:446:static zend_always_inline zval *_get_zval_ptr_deref(int op_type, znode_op node, const zend_execute_data *execute_data, zend_free_op *should_free, int type)
Zend/zend_execute.c:467:static zend_always_inline zval *_get_zval_ptr_r_deref(int op_type, znode_op node, const zend_execute_data *execute_data, zend_free_op *should_free)
Zend/zend_execute.c:488:static zend_always_inline zval *_get_zval_ptr_undef(int op_type, znode_op node, const zend_execute_data *execute_data, zend_free_op *should_free, int type)
Zend/zend_execute.c:509:static zend_always_inline zval *_get_zval_ptr_ptr_var(uint32_t var, const zend_execute_data *execute_data, zend_free_op *should_free)
Zend/zend_execute.c:522:static inline zval *_get_zval_ptr_ptr(int op_type, znode_op node, const zend_execute_data *execute_data, zend_free_op *should_free, int type)
Zend/zend_execute.c:533:static zend_always_inline zval *_get_obj_zval_ptr_unused(zend_execute_data *execute_data)
Zend/zend_execute.c:538:static inline zval *_get_obj_zval_ptr(int op_type, znode_op op, zend_execute_data *execute_data, zend_free_op *should_free, int type)
Zend/zend_execute.c:547:static inline zval *_get_obj_zval_ptr_undef(int op_type, znode_op op, zend_execute_data *execute_data, zend_free_op *should_free, int type)
Zend/zend_execute.c:556:static inline zval *_get_obj_zval_ptr_ptr(int op_type, znode_op node, zend_execute_data *execute_data, zend_free_op *should_free, int type)
Zend/zend_execute.c:565:static inline void zend_assign_to_variable_reference(zval *variable_ptr, zval *value_ptr)
Zend/zend_execute.c:582:static inline int make_real_object(zval *object)
Zend/zend_execute.c:598:static char * zend_verify_internal_arg_class_kind(const zend_internal_arg_info *cur_arg_info, char **class_name, zend_class_entry **pce)
Zend/zend_execute.c:615:static zend_always_inline zend_class_entry* zend_verify_arg_class_kind(const zend_arg_info *cur_arg_info)
Zend/zend_execute.c:620:static ZEND_COLD void zend_verify_arg_error(const zend_function *zf, uint32_t arg_num, const char *need_msg, const char *need_kind, const char *given_msg, const char *given_kin
Zend/zend_execute.c:648:static int is_null_constant(zval *default_value)
Zend/zend_execute.c:665:static zend_bool zend_verify_weak_scalar_type_hint(zend_uchar type_hint, zval *arg)
Zend/zend_execute.c:712:static zend_bool zend_verify_scalar_type_hint(zend_uchar type_hint, zval *arg, zend_bool strict)
Zend/zend_execute.c:726:static int zend_verify_internal_arg_type(zend_function *zf, uint32_t arg_num, zval *arg)
Zend/zend_execute.c:772:static zend_never_inline int zend_verify_internal_arg_types(zend_function *fbc, zend_execute_data *call)
Zend/zend_execute.c:789:static zend_always_inline int zend_verify_arg_type(zend_function *zf, uint32_t arg_num, zval *arg, zval *default_value, void **cache_slot)
Zend/zend_execute.c:863:static zend_always_inline int zend_verify_missing_arg_type(zend_function *zf, uint32_t arg_num, void **cache_slot)
Zend/zend_execute.c:903:static ZEND_COLD void zend_verify_missing_arg(zend_execute_data *execute_data, uint32_t arg_num, void **cache_slot)
Zend/zend_execute.c:920:static ZEND_COLD void zend_verify_return_error(const zend_function *zf, const char *need_msg, const char *need_kind, const char *returned_msg, const char *returned_kind)
Zend/zend_execute.c:938:static ZEND_COLD void zend_verify_internal_return_error(const zend_function *zf, const char *need_msg, const char *need_kind, const char *returned_msg, const char *returned_kin
Zend/zend_execute.c:956:static ZEND_COLD void zend_verify_void_return_error(const zend_function *zf, const char *returned_msg, const char *returned_kind)
Zend/zend_execute.c:975:static int zend_verify_internal_return_type(zend_function *zf, zval *ret)
Zend/zend_execute.c:1016:static zend_always_inline void zend_verify_return_type(zend_function *zf, zval *ret, void **cache_slot)
Zend/zend_execute.c:1078:static ZEND_COLD int zend_verify_missing_return_type(zend_function *zf, void **cache_slot)
Zend/zend_execute.c:1111:static zend_never_inline void zend_assign_to_object_dim(zval *object, zval *dim, zval *value)
Zend/zend_execute.c:1121:static zend_never_inline void zend_binary_assign_op_obj_dim(zval *object, zval *property, zval *value, zval *retval, binary_op_type binary_op)
Zend/zend_execute.c:1155:static zend_never_inline zend_long zend_check_string_offset(zval *dim, int type)
Zend/zend_execute.c:1194:static zend_never_inline ZEND_COLD void zend_wrong_string_offset(void)
Zend/zend_execute.c:1308:static zend_never_inline void zend_assign_to_string_offset(zval *str, zval *dim, zval *value, zval *result)
Zend/zend_execute.c:1378:static zend_never_inline void zend_post_incdec_overloaded_property(zval *object, zval *property, void **cache_slot, int inc, zval *result)
Zend/zend_execute.c:1423:static zend_never_inline void zend_pre_incdec_overloaded_property(zval *object, zval *property, void **cache_slot, int inc, zval *result)
Zend/zend_execute.c:1468:static zend_never_inline void zend_assign_op_overloaded_property(zval *object, zval *property, void **cache_slot, zval *value, binary_op_type binary_op, zval *result)
Zend/zend_execute.c:1510:static void zend_extension_statement_handler(const zend_extension *extension, zend_op_array *op_array)
Zend/zend_execute.c:1518:static void zend_extension_fcall_begin_handler(const zend_extension *extension, zend_op_array *op_array)
Zend/zend_execute.c:1526:static void zend_extension_fcall_end_handler(const zend_extension *extension, zend_op_array *op_array)
Zend/zend_execute.c:1534:static zend_always_inline HashTable *zend_get_target_symbol_table(zend_execute_data *execute_data, int fetch_type)
Zend/zend_execute.c:1551:static zend_always_inline zval *zend_fetch_dimension_address_inner(HashTable *ht, const zval *dim, int dim_type, int type)
Zend/zend_execute.c:1662:static zend_never_inline zval* ZEND_FASTCALL zend_fetch_dimension_address_inner_W(HashTable *ht, const zval *dim)
Zend/zend_execute.c:1667:static zend_never_inline zval* ZEND_FASTCALL zend_fetch_dimension_address_inner_W_CONST(HashTable *ht, const zval *dim)
Zend/zend_execute.c:1672:static zend_never_inline zval* ZEND_FASTCALL zend_fetch_dimension_address_inner_RW(HashTable *ht, const zval *dim)
Zend/zend_execute.c:1677:static zend_never_inline zval* ZEND_FASTCALL zend_fetch_dimension_address_inner_RW_CONST(HashTable *ht, const zval *dim)
Zend/zend_execute.c:1682:static zend_always_inline void zend_fetch_dimension_address(zval *result, zval *container, zval *dim, int dim_type, int type)
Zend/zend_execute.c:1799:static zend_never_inline void zend_fetch_dimension_address_W(zval *result, zval *container_ptr, zval *dim, int dim_type)
Zend/zend_execute.c:1804:static zend_never_inline void zend_fetch_dimension_address_RW(zval *result, zval *container_ptr, zval *dim, int dim_type)
Zend/zend_execute.c:1809:static zend_never_inline void zend_fetch_dimension_address_UNSET(zval *result, zval *container_ptr, zval *dim, int dim_type)
Zend/zend_execute.c:1814:static zend_always_inline void zend_fetch_dimension_address_read(zval *result, zval *container, zval *dim, int dim_type, int type, int support_strings)
Zend/zend_execute.c:1921:static zend_never_inline void zend_fetch_dimension_address_read_R(zval *result, zval *container, zval *dim, int dim_type)
Zend/zend_execute.c:1926:static zend_never_inline void zend_fetch_dimension_address_read_IS(zval *result, zval *container, zval *dim, int dim_type)
Zend/zend_execute.c:1931:static zend_never_inline void zend_fetch_dimension_address_read_LIST(zval *result, zval *container, zval *dim)
Zend/zend_execute.c:1936:ZEND_API void zend_fetch_dimension_by_zval(zval *result, zval *container, zval *dim)
Zend/zend_execute.c:1941:ZEND_API void zend_fetch_dimension_by_zval_is(zval *result, zval *container, zval *dim, int dim_type)
Zend/zend_execute.c:1947:static zend_always_inline void zend_fetch_property_address(zval *result, zval *container, uint32_t container_op_type, zval *prop_ptr, uint32_t prop_op_type, void **cache_slot,
Zend/zend_execute.c:2040:static int zend_check_symbol(zval *pz)
Zend/zend_execute.c:2066:ZEND_API void execute_internal(zend_execute_data *execute_data, zval *return_value)
Zend/zend_execute.c:2071:ZEND_API void zend_clean_and_cache_symbol_table(zend_array *symbol_table) /* {{{ */
Zend/zend_execute.c:2084:static zend_always_inline void i_free_compiled_variables(zend_execute_data *execute_data) /* {{{ */
Zend/zend_execute.c:2103:void zend_free_compiled_variables(zend_execute_data *execute_data) /* {{{ */
Zend/zend_execute.c:2109:static zend_never_inline ZEND_COLD ZEND_NORETURN void ZEND_FASTCALL zend_interrupt(void) /* {{{ */
Zend/zend_execute.c:2141:static zend_always_inline void i_init_func_execute_data(zend_execute_data *execute_data, zend_op_array *op_array, zval *return_value, int check_this) /* {{{ */
Zend/zend_execute.c:2211:static zend_never_inline void ZEND_FASTCALL init_func_run_time_cache(zend_op_array *op_array) /* {{{ */
Zend/zend_execute.c:2219:static zend_always_inline void i_init_code_execute_data(zend_execute_data *execute_data, zend_op_array *op_array, zval *return_value) /* {{{ */
Zend/zend_execute.c:2247:static zend_always_inline void i_init_execute_data(zend_execute_data *execute_data, zend_op_array *op_array, zval *return_value) /* {{{ */
Zend/zend_execute.c:2337:ZEND_API zend_execute_data *zend_create_generator_execute_data(zend_execute_data *call, zend_op_array *op_array, zval *return_value) /* {{{ */
Zend/zend_execute.c:2396:ZEND_API void zend_init_execute_data(zend_execute_data *execute_data, zend_op_array *op_array, zval *return_value) /* {{{ */
Zend/zend_execute.c:2403:static zend_always_inline zend_bool zend_is_by_ref_func_arg_fetch(const zend_op *opline, zend_execute_data *call) /* {{{ */
Zend/zend_execute.c:2414:static zend_execute_data *zend_vm_stack_copy_call_frame(zend_execute_data *call, uint32_t passed_args, uint32_t additional_args) /* {{{ */
Zend/zend_execute.c:2450:static zend_always_inline void zend_vm_stack_extend_call_frame(zend_execute_data **call, uint32_t passed_args, uint32_t additional_args) /* {{{ */
Zend/zend_execute.c:2460:static zend_always_inline zend_generator *zend_get_running_generator(zend_execute_data *execute_data) /* {{{ */
Zend/zend_execute.c:2470:static void cleanup_unfinished_calls(zend_execute_data *execute_data, uint32_t op_num) /* {{{ */
Zend/zend_execute.c:2595:static void cleanup_live_vars(zend_execute_data *execute_data, uint32_t op_num, uint32_t catch_op_num) /* {{{ */
Zend/zend_execute.c:2645:void zend_cleanup_unfinished_execution(zend_execute_data *execute_data, uint32_t op_num, uint32_t catch_op_num) {
Zend/zend_execute.c:2650:static void zend_swap_operands(zend_op *op) /* {{{ */
Zend/zend_execute.c:2664:static zend_never_inline zend_execute_data *zend_init_dynamic_call_string(zend_string *function, uint32_t num_args) /* {{{ */
Zend/zend_execute.c:2750:static zend_never_inline zend_execute_data *zend_init_dynamic_call_object(zval *function, uint32_t num_args) /* {{{ */
Zend/zend_execute.c:2783:static zend_never_inline zend_execute_data *zend_init_dynamic_call_array(zend_array *function, uint32_t num_args) /* {{{ */
Zend/zend_execute.c:2882:static zend_never_inline zend_op_array* ZEND_FASTCALL zend_include_or_eval(zval *inc_filename, int type) /* {{{ */
Zend/zend_execute.c:2964:static zend_never_inline int zend_do_fcall_overloaded(zend_function *fbc, zend_execute_data *call, zval *ret) /* {{{ */
Zend/zend_execute.c:3129:ZEND_API int zend_set_user_opcode_handler(zend_uchar opcode, user_opcode_handler_t handler)
Zend/zend_execute.c:3144:ZEND_API user_opcode_handler_t zend_get_user_opcode_handler(zend_uchar opcode)
Zend/zend_execute.c:3149:ZEND_API zval *zend_get_zval_ptr(int op_type, const znode_op *node, const zend_execute_data *execute_data, zend_free_op *should_free, int type)
Zend/zend_execute.c:3154:ZEND_API void ZEND_FASTCALL zend_check_internal_arg_type(zend_function *zf, uint32_t arg_num, zval *arg)
Zend/zend_execute.c:3159:ZEND_API int ZEND_FASTCALL zend_check_arg_type(zend_function *zf, uint32_t arg_num, zval *arg, zval *default_value, void **cache_slot)
Zend/zend_execute.c:3164:ZEND_API void ZEND_FASTCALL zend_check_missing_arg(zend_execute_data *execute_data, uint32_t arg_num, void **cache_slot)
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=Zend/zend_execute_API.c, max_results=300)` →

```
53 matches
Zend/zend_execute_API.c:45:ZEND_API void (*zend_execute_ex)(zend_execute_data *execute_data);
Zend/zend_execute_API.c:46:ZEND_API void (*zend_execute_internal)(zend_execute_data *execute_data, zval *return_value);
Zend/zend_execute_API.c:57:static void (*original_sigsegv_handler)(int);
Zend/zend_execute_API.c:58:static void zend_handle_sigsegv(int dummy) /* {{{ */
Zend/zend_execute_API.c:87:static void zend_extension_activator(zend_extension *extension) /* {{{ */
Zend/zend_execute_API.c:95:static void zend_extension_deactivator(zend_extension *extension) /* {{{ */
Zend/zend_execute_API.c:103:static int clean_non_persistent_function(zval *zv) /* {{{ */
Zend/zend_execute_API.c:110:ZEND_API int clean_non_persistent_function_full(zval *zv) /* {{{ */
Zend/zend_execute_API.c:117:static int clean_non_persistent_class(zval *zv) /* {{{ */
Zend/zend_execute_API.c:124:ZEND_API int clean_non_persistent_class_full(zval *zv) /* {{{ */
Zend/zend_execute_API.c:131:void init_executor(void) /* {{{ */
Zend/zend_execute_API.c:191:static int zval_call_destructor(zval *zv) /* {{{ */
Zend/zend_execute_API.c:204:static void zend_unclean_zval_ptr_dtor(zval *zv) /* {{{ */
Zend/zend_execute_API.c:213:static void zend_throw_or_error(int fetch_type, zend_class_entry *exception_ce, const char *format, ...) /* {{{ */
Zend/zend_execute_API.c:232:void shutdown_destructors(void) /* {{{ */
Zend/zend_execute_API.c:251:void shutdown_executor(void) /* {{{ */
Zend/zend_execute_API.c:417:ZEND_API const char *get_active_class_name(const char **space) /* {{{ */
Zend/zend_execute_API.c:449:ZEND_API const char *get_active_function_name(void) /* {{{ */
Zend/zend_execute_API.c:477:ZEND_API const char *zend_get_executed_filename(void) /* {{{ */
Zend/zend_execute_API.c:492:ZEND_API zend_string *zend_get_executed_filename_ex(void) /* {{{ */
Zend/zend_execute_API.c:507:ZEND_API uint zend_get_executed_lineno(void) /* {{{ */
Zend/zend_execute_API.c:526:ZEND_API zend_bool zend_is_executing(void) /* {{{ */
Zend/zend_execute_API.c:532:ZEND_API void _zval_ptr_dtor(zval *zval_ptr ZEND_FILE_LINE_DC) /* {{{ */
Zend/zend_execute_API.c:538:ZEND_API void _zval_internal_ptr_dtor(zval *zval_ptr ZEND_FILE_LINE_DC) /* {{{ */
Zend/zend_execute_API.c:554:ZEND_API int zval_update_constant_ex(zval *p, zend_bool inline_change, zend_class_entry *scope) /* {{{ */
Zend/zend_execute_API.c:660:ZEND_API int zval_update_constant(zval *pp, zend_bool inline_change) /* {{{ */
Zend/zend_execute_API.c:666:int _call_user_function_ex(zval *object, zval *function_name, zval *retval_ptr, uint32_t param_count, zval params[], int no_separation) /* {{{ */
Zend/zend_execute_API.c:682:int zend_call_function(zend_fcall_info *fci, zend_fcall_info_cache *fci_cache) /* {{{ */
Zend/zend_execute_API.c:935:ZEND_API zend_class_entry *zend_lookup_class_ex(zend_string *name, const zval *key, int use_autoload) /* {{{ */
Zend/zend_execute_API.c:1052:ZEND_API zend_class_entry *zend_lookup_class(zend_string *name) /* {{{ */
Zend/zend_execute_API.c:1058:ZEND_API zend_class_entry *zend_get_called_scope(zend_execute_data *ex) /* {{{ */
Zend/zend_execute_API.c:1076:ZEND_API zend_object *zend_get_this_object(zend_execute_data *ex) /* {{{ */
Zend/zend_execute_API.c:1092:ZEND_API int zend_eval_stringl(char *str, size_t str_len, zval *retval_ptr, char *string_name) /* {{{ */
Zend/zend_execute_API.c:1154:ZEND_API int zend_eval_string(char *str, zval *retval_ptr, char *string_name) /* {{{ */
Zend/zend_execute_API.c:1160:ZEND_API int zend_eval_stringl_ex(char *str, size_t str_len, zval *retval_ptr, char *string_name, int handle_exceptions) /* {{{ */
Zend/zend_execute_API.c:1173:ZEND_API int zend_eval_string_ex(char *str, zval *retval_ptr, char *string_name, int handle_exceptions) /* {{{ */
Zend/zend_execute_API.c:1179:static void zend_set_timeout_ex(zend_long seconds, int reset_signals);
Zend/zend_execute_API.c:1181:ZEND_API ZEND_NORETURN void zend_timeout(int dummy) /* {{{ */
Zend/zend_execute_API.c:1190:static void zend_timeout_handler(int dummy) /* {{{ */
Zend/zend_execute_API.c:1247:VOID CALLBACK tq_timer_cb(PVOID arg, BOOLEAN timed_out)
Zend/zend_execute_API.c:1267:static void zend_set_timeout_ex(zend_long seconds, int reset_signals) /* {{{ */
Zend/zend_execute_API.c:1339:void zend_set_timeout(zend_long seconds, int reset_signals) /* {{{ */
Zend/zend_execute_API.c:1348:void zend_unset_timeout(void) /* {{{ */
Zend/zend_execute_API.c:1380:zend_class_entry *zend_fetch_class(zend_string *class_name, int fetch_type) /* {{{ */
Zend/zend_execute_API.c:1435:zend_class_entry *zend_fetch_class_by_name(zend_string *class_name, const zval *key, int fetch_type) /* {{{ */
Zend/zend_execute_API.c:1471:static void zend_verify_abstract_class_function(zend_function *fn, zend_abstract_info *ai) /* {{{ */
Zend/zend_execute_API.c:1491:void zend_verify_abstract_class(zend_class_entry *ce) /* {{{ */
Zend/zend_execute_API.c:1516:ZEND_API int zend_delete_global_variable(zend_string *name) /* {{{ */
Zend/zend_execute_API.c:1522:ZEND_API zend_array *zend_rebuild_symbol_table(void) /* {{{ */
Zend/zend_execute_API.c:1571:ZEND_API void zend_attach_symbol_table(zend_execute_data *execute_data) /* {{{ */
Zend/zend_execute_API.c:1606:ZEND_API void zend_detach_symbol_table(zend_execute_data *execute_data) /* {{{ */
Zend/zend_execute_API.c:1631:ZEND_API int zend_set_local_var(zend_string *name, zval *value, int force) /* {{{ */
Zend/zend_execute_API.c:1673:ZEND_API int zend_set_local_var_str(const char *name, size_t len, zval *value, int force) /* {{{ */
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=Zend/zend_ini_parser.y, max_results=300)` →

```
9 matches
Zend/zend_ini_parser.y:39:int ini_parse(void);
Zend/zend_ini_parser.y:51:static void zend_ini_do_op(char type, zval *result, zval *op1, zval *op2)
Zend/zend_ini_parser.y:95:static void zend_ini_init_string(zval *result)
Zend/zend_ini_parser.y:103:static void zend_ini_add_string(zval *result, zval *op1, zval *op2)
Zend/zend_ini_parser.y:127:static void zend_ini_get_constant(zval *result, zval *name)
Zend/zend_ini_parser.y:156:static void zend_ini_get_var(zval *result, zval *name)
Zend/zend_ini_parser.y:176:static ZEND_COLD void ini_error(const char *msg)
Zend/zend_ini_parser.y:206:ZEND_API int zend_parse_ini_file(zend_file_handle *fh, zend_bool unbuffered_errors, int scanner_mode, zend_ini_parser_cb_t ini_parser_cb, void *arg)
Zend/zend_ini_parser.y:235:ZEND_API int zend_parse_ini_string(char *str, zend_bool unbuffered_errors, int scanner_mode, zend_ini_parser_cb_t ini_parser_cb, void *arg)
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ext/reflection/php_reflection.c, max_results=300)` →

```
345 matches (showing 200)
ext/reflection/php_reflection.c:72:ZEND_BEGIN_MODULE_GLOBALS(reflection)
ext/reflection/php_reflection.c:74:ZEND_END_MODULE_GLOBALS(reflection)
ext/reflection/php_reflection.c:85:ZEND_DECLARE_MODULE_GLOBALS(reflection)
ext/reflection/php_reflection.c:127:static void string_init(string *str)
ext/reflection/php_reflection.c:135:static string *string_printf(string *str, const char *format, ...)
ext/reflection/php_reflection.c:159:static string *string_write(string *str, char *buf, size_t len)
ext/reflection/php_reflection.c:174:static string *string_append(string *str, string *append)
ext/reflection/php_reflection.c:182:static void string_free(string *str)
ext/reflection/php_reflection.c:234:static inline reflection_object *reflection_object_from_obj(zend_object *obj) {
ext/reflection/php_reflection.c:243:static zval *_default_load_entry(zval *object, char *name, size_t name_len) /* {{{ */
ext/reflection/php_reflection.c:254:static void _default_get_entry(zval *object, char *name, int name_len, zval *return_value) /* {{{ */
ext/reflection/php_reflection.c:266:static void _default_lookup_entry(zval *object, char *name, int name_len, zval **return_value) /* {{{ */
ext/reflection/php_reflection.c:279:static zend_function *_copy_function(zend_function *fptr) /* {{{ */
ext/reflection/php_reflection.c:296:static void _free_function(zend_function *fptr) /* {{{ */
ext/reflection/php_reflection.c:307:static void reflection_free_objects_storage(zend_object *object) /* {{{ */
ext/reflection/php_reflection.c:349:static zend_object *reflection_objects_new(zend_class_entry *class_type) /* {{{ */
ext/reflection/php_reflection.c:363:static zval *reflection_instantiate(zend_class_entry *pce, zval *object) /* {{{ */
ext/reflection/php_reflection.c:370:static void _const_string(string *str, char *name, zval *value, char *indent);
ext/reflection/php_reflection.c:371:static void _function_string(string *str, zend_function *fptr, zend_class_entry *scope, char* indent);
ext/reflection/php_reflection.c:372:static void _property_string(string *str, zend_property_info *prop, char *prop_name, char* indent);
ext/reflection/php_reflection.c:373:static void _class_const_string(string *str, char *name, zend_class_constant *c, char* indent);
ext/reflection/php_reflection.c:374:static void _class_string(string *str, zend_class_entry *ce, zval *obj, char *indent);
ext/reflection/php_reflection.c:375:static void _extension_string(string *str, zend_module_entry *module, char *indent);
ext/reflection/php_reflection.c:376:static void _zend_extension_string(string *str, zend_extension *extension, char *indent);
ext/reflection/php_reflection.c:379:static void _class_string(string *str, zend_class_entry *ce, zval *obj, char *indent)
ext/reflection/php_reflection.c:621:static void _const_string(string *str, char *name, zval *value, char *indent)
ext/reflection/php_reflection.c:634:static void _class_const_string(string *str, char *name, zend_class_constant *c, char *indent)
ext/reflection/php_reflection.c:648:static zend_op* _get_recv_op(zend_op_array *op_array, uint32_t offset)
ext/reflection/php_reflection.c:667:static void _parameter_string(string *str, zend_function *fptr, struct _zend_arg_info *arg_info, uint32_t offset, uint32_t required, char* indent)
ext/reflection/php_reflection.c:745:static void _function_parameter_string(string *str, zend_function *fptr, char* indent)
ext/reflection/php_reflection.c:771:static void _function_closure_string(string *str, zend_function *fptr, char* indent)
ext/reflection/php_reflection.c:799:static void _function_string(string *str, zend_function *fptr, zend_class_entry *scope, char* indent)
ext/reflection/php_reflection.c:923:static void _property_string(string *str, zend_property_info *prop, char *prop_name, char* indent)
ext/reflection/php_reflection.c:963:static int _extension_ini_string(zval *el, int num_args, va_list args, zend_hash_key *hash_key) /* {{{ */
ext/reflection/php_reflection.c:1000:static int _extension_class_string(zval *el, int num_args, va_list args, zend_hash_key *hash_key) /* {{{ */
ext/reflection/php_reflection.c:1020:static int _extension_const_string(zval *el, int num_args, va_list args, zend_hash_key *hash_key) /* {{{ */
ext/reflection/php_reflection.c:1036:static void _extension_string(string *str, zend_module_entry *module, char *indent) /* {{{ */
ext/reflection/php_reflection.c:1151:static void _zend_extension_string(string *str, zend_extension *extension, char *indent) /* {{{ */
ext/reflection/php_reflection.c:1173:static void _function_check_flag(INTERNAL_FUNCTION_PARAMETERS, int mask)
ext/reflection/php_reflection.c:1187:PHPAPI void zend_reflection_class_factory(zend_class_entry *ce, zval *object)
ext/reflection/php_reflection.c:1203:static void reflection_extension_factory(zval *object, const char *name_str)
ext/reflection/php_reflection.c:1230:static void reflection_parameter_factory(zend_function *fptr, zval *closure_object, struct _zend_arg_info *arg_info, uint32_t offset, uint32_t required, zval *obje
ext/reflection/php_reflection.c:1265:static void reflection_type_factory(zend_function *fptr, zval *closure_object, struct _zend_arg_info *arg_info, zval *object)
ext/reflection/php_reflection.c:1286:static void reflection_function_factory(zend_function *function, zval *closure_object, zval *object)
ext/reflection/php_reflection.c:1307:static void reflection_method_factory(zend_class_entry *ce, zend_function *method, zval *closure_object, zval *object)
ext/reflection/php_reflection.c:1331:static void reflection_property_factory(zend_class_entry *ce, zend_property_info *prop, zval *object)
ext/reflection/php_reflection.c:1377:static void reflection_class_constant_factory(zend_class_entry *ce, zend_string *name_str, zend_class_constant *constant, zval *object)
ext/reflection/php_reflection.c:1398:static void _reflection_export(INTERNAL_FUNCTION_PARAMETERS, zend_class_entry *ce_ptr, int ctor_argc)
ext/reflection/php_reflection.c:1491:static parameter_reference *_reflection_param_get_default_param(INTERNAL_FUNCTION_PARAMETERS)
ext/reflection/php_reflection.c:1515:static zend_op *_reflection_param_get_default_precv(INTERNAL_FUNCTION_PARAMETERS, parameter_reference *param)
ext/reflection/php_reflection.c:1534:ZEND_METHOD(reflection, __clone)
ext/reflection/php_reflection.c:1543:ZEND_METHOD(reflection, export)
ext/reflection/php_reflection.c:1589:ZEND_METHOD(reflection, getModifierNames)
ext/reflection/php_reflection.c:1630:ZEND_METHOD(reflection_function, export)
ext/reflection/php_reflection.c:1638:ZEND_METHOD(reflection_function, __construct)
ext/reflection/php_reflection.c:1693:ZEND_METHOD(reflection_function, __toString)
ext/reflection/php_reflection.c:1711:ZEND_METHOD(reflection_function, getName)
ext/reflection/php_reflection.c:1722:ZEND_METHOD(reflection_function, isClosure)
ext/reflection/php_reflection.c:1737:ZEND_METHOD(reflection_function, getClosureThis)
ext/reflection/php_reflection.c:1757:ZEND_METHOD(reflection_function, getClosureScopeClass)
ext/reflection/php_reflection.c:1777:ZEND_METHOD(reflection_function, getClosure)
ext/reflection/php_reflection.c:1798:ZEND_METHOD(reflection_function, isInternal)
ext/reflection/php_reflection.c:1813:ZEND_METHOD(reflection_function, isUserDefined)
ext/reflection/php_reflection.c:1828:ZEND_METHOD(reflection_function, isDisabled)
ext/reflection/php_reflection.c:1841:ZEND_METHOD(reflection_function, getFileName)
ext/reflection/php_reflection.c:1859:ZEND_METHOD(reflection_function, getStartLine)
ext/reflection/php_reflection.c:1877:ZEND_METHOD(reflection_function, getEndLine)
ext/reflection/php_reflection.c:1895:ZEND_METHOD(reflection_function, getDocComment)
ext/reflection/php_reflection.c:1913:ZEND_METHOD(reflection_function, getStaticVariables)
ext/reflection/php_reflection.c:1945:ZEND_METHOD(reflection_function, invoke)
ext/reflection/php_reflection.c:1992:ZEND_METHOD(reflection_function, invokeArgs)
ext/reflection/php_reflection.c:2055:ZEND_METHOD(reflection_function, returnsReference)
ext/reflection/php_reflection.c:2069:ZEND_METHOD(reflection_function, getNumberOfParameters)
ext/reflection/php_reflection.c:2089:ZEND_METHOD(reflection_function, getNumberOfRequiredParameters)
ext/reflection/php_reflection.c:2103:ZEND_METHOD(reflection_function, getParameters)
ext/reflection/php_reflection.c:2133:ZEND_METHOD(reflection_function, getExtension)
ext/reflection/php_reflection.c:2157:ZEND_METHOD(reflection_function, getExtensionName)
ext/reflection/php_reflection.c:2180:ZEND_METHOD(reflection_generator, __construct)
ext/reflection/php_reflection.c:2212:ZEND_METHOD(reflection_generator, getTrace)
ext/reflection/php_reflection.c:2248:ZEND_METHOD(reflection_generator, getExecutingLine)
ext/reflection/php_reflection.c:2264:ZEND_METHOD(reflection_generator, getExecutingFile)
ext/reflection/php_reflection.c:2280:ZEND_METHOD(reflection_generator, getFunction)
ext/reflection/php_reflection.c:2304:ZEND_METHOD(reflection_generator, getThis)
ext/reflection/php_reflection.c:2324:ZEND_METHOD(reflection_generator, getExecutingGenerator)
ext/reflection/php_reflection.c:2346:ZEND_METHOD(reflection_parameter, export)
ext/reflection/php_reflection.c:2354:ZEND_METHOD(reflection_parameter, __construct)
ext/reflection/php_reflection.c:2549:ZEND_METHOD(reflection_parameter, __toString)
ext/reflection/php_reflection.c:2568:ZEND_METHOD(reflection_parameter, getName)
ext/reflection/php_reflection.c:2579:ZEND_METHOD(reflection_parameter, getDeclaringFunction)
ext/reflection/php_reflection.c:2599:ZEND_METHOD(reflection_parameter, getDeclaringClass)
ext/reflection/php_reflection.c:2617:ZEND_METHOD(reflection_parameter, getClass)
ext/reflection/php_reflection.c:2694:ZEND_METHOD(reflection_parameter, hasType)
ext/reflection/php_reflection.c:2710:ZEND_METHOD(reflection_parameter, getType)
ext/reflection/php_reflection.c:2733:ZEND_METHOD(reflection_parameter, isArray)
ext/reflection/php_reflection.c:2749:ZEND_METHOD(reflection_parameter, isCallable)
ext/reflection/php_reflection.c:2765:ZEND_METHOD(reflection_parameter, allowsNull)
ext/reflection/php_reflection.c:2781:ZEND_METHOD(reflection_parameter, isPassedByReference)
ext/reflection/php_reflection.c:2797:ZEND_METHOD(reflection_parameter, canBePassedByValue)
ext/reflection/php_reflection.c:2814:ZEND_METHOD(reflection_parameter, getPosition)
ext/reflection/php_reflection.c:2830:ZEND_METHOD(reflection_parameter, isOptional)
ext/reflection/php_reflection.c:2846:ZEND_METHOD(reflection_parameter, isDefaultValueAvailable)
ext/reflection/php_reflection.c:2872:ZEND_METHOD(reflection_parameter, getDefaultValue)
ext/reflection/php_reflection.c:2906:ZEND_METHOD(reflection_parameter, isDefaultValueConstant)
ext/reflection/php_reflection.c:2931:ZEND_METHOD(reflection_parameter, getDefaultValueConstantName)
ext/reflection/php_reflection.c:2954:ZEND_METHOD(reflection_parameter, isVariadic)
ext/reflection/php_reflection.c:2970:ZEND_METHOD(reflection_type, allowsNull)
ext/reflection/php_reflection.c:2986:ZEND_METHOD(reflection_type, isBuiltin)
ext/reflection/php_reflection.c:3002:ZEND_METHOD(reflection_type, __toString)
ext/reflection/php_reflection.c:3033:ZEND_METHOD(reflection_method, export)
ext/reflection/php_reflection.c:3041:ZEND_METHOD(reflection_method, __construct)
ext/reflection/php_reflection.c:3134:ZEND_METHOD(reflection_method, __toString)
ext/reflection/php_reflection.c:3152:ZEND_METHOD(reflection_method, getClosure)
ext/reflection/php_reflection.c:3187:ZEND_METHOD(reflection_method, invoke)
ext/reflection/php_reflection.c:3280:ZEND_METHOD(reflection_method, invokeArgs)
ext/reflection/php_reflection.c:3397:ZEND_METHOD(reflection_method, isFinal)
ext/reflection/php_reflection.c:3405:ZEND_METHOD(reflection_method, isAbstract)
ext/reflection/php_reflection.c:3413:ZEND_METHOD(reflection_method, isPublic)
ext/reflection/php_reflection.c:3421:ZEND_METHOD(reflection_method, isPrivate)
ext/reflection/php_reflection.c:3429:ZEND_METHOD(reflection_method, isProtected)
ext/reflection/php_reflection.c:3437:ZEND_METHOD(reflection_method, isStatic)
ext/reflection/php_reflection.c:3445:ZEND_METHOD(reflection_function, isDeprecated)
ext/reflection/php_reflection.c:3453:ZEND_METHOD(reflection_function, isGenerator)
ext/reflection/php_reflection.c:3461:ZEND_METHOD(reflection_function, isVariadic)
ext/reflection/php_reflection.c:3469:ZEND_METHOD(reflection_function, inNamespace)
ext/reflection/php_reflection.c:3492:ZEND_METHOD(reflection_function, getNamespaceName)
ext/reflection/php_reflection.c:3515:ZEND_METHOD(reflection_function, getShortName)
ext/reflection/php_reflection.c:3539:ZEND_METHOD(reflection_function, hasReturnType)
ext/reflection/php_reflection.c:3556:ZEND_METHOD(reflection_function, getReturnType)
ext/reflection/php_reflection.c:3577:ZEND_METHOD(reflection_method, isConstructor)
ext/reflection/php_reflection.c:3595:ZEND_METHOD(reflection_method, isDestructor)
ext/reflection/php_reflection.c:3610:ZEND_METHOD(reflection_method, getModifiers)
ext/reflection/php_reflection.c:3626:ZEND_METHOD(reflection_method, getDeclaringClass)
ext/reflection/php_reflection.c:3644:ZEND_METHOD(reflection_method, getPrototype)
ext/reflection/php_reflection.c:3668:ZEND_METHOD(reflection_method, setAccessible)
ext/reflection/php_reflection.c:3685:ZEND_METHOD(reflection_class_constant, __construct)
ext/reflection/php_reflection.c:3738:ZEND_METHOD(reflection_class_constant, __toString)
ext/reflection/php_reflection.c:3759:ZEND_METHOD(reflection_class_constant, getName)
ext/reflection/php_reflection.c:3768:static void _class_constant_check_flag(INTERNAL_FUNCTION_PARAMETERS, int mask) /* {{{ */
ext/reflection/php_reflection.c:3783:ZEND_METHOD(reflection_class_constant, isPublic)
ext/reflection/php_reflection.c:3791:ZEND_METHOD(reflection_class_constant, isPrivate)
ext/reflection/php_reflection.c:3799:ZEND_METHOD(reflection_class_constant, isProtected)
ext/reflection/php_reflection.c:3807:ZEND_METHOD(reflection_class_constant, getModifiers)
ext/reflection/php_reflection.c:3823:ZEND_METHOD(reflection_class_constant, getValue)
ext/reflection/php_reflection.c:3839:ZEND_METHOD(reflection_class_constant, getDeclaringClass)
ext/reflection/php_reflection.c:3855:ZEND_METHOD(reflection_class_constant, getDocComment)
ext/reflection/php_reflection.c:3873:ZEND_METHOD(reflection_class, export)
ext/reflection/php_reflection.c:3880:static void reflection_class_object_ctor(INTERNAL_FUNCTION_PARAMETERS, int is_object)
ext/reflection/php_reflection.c:3929:ZEND_METHOD(reflection_class, __construct)
ext/reflection/php_reflection.c:3936:static void add_class_vars(zend_class_entry *ce, int statics, zval *return_value)
ext/reflection/php_reflection.c:3980:ZEND_METHOD(reflection_class, getStaticProperties)
ext/reflection/php_reflection.c:4002:ZEND_METHOD(reflection_class, getStaticPropertyValue)
ext/reflection/php_reflection.c:4036:ZEND_METHOD(reflection_class, setStaticPropertyValue)
ext/reflection/php_reflection.c:4066:ZEND_METHOD(reflection_class, getDefaultProperties)
ext/reflection/php_reflection.c:4086:ZEND_METHOD(reflection_class, __toString)
ext/reflection/php_reflection.c:4104:ZEND_METHOD(reflection_class, getName)
ext/reflection/php_reflection.c:4115:ZEND_METHOD(reflection_class, isInternal)
ext/reflection/php_reflection.c:4130:ZEND_METHOD(reflection_class, isUserDefined)
ext/reflection/php_reflection.c:4145:ZEND_METHOD(reflection_class, isAnonymous)
ext/reflection/php_reflection.c:4160:ZEND_METHOD(reflection_class, getFileName)
ext/reflection/php_reflection.c:4178:ZEND_METHOD(reflection_class, getStartLine)
ext/reflection/php_reflection.c:4196:ZEND_METHOD(reflection_class, getEndLine)
ext/reflection/php_reflection.c:4214:ZEND_METHOD(reflection_class, getDocComment)
ext/reflection/php_reflection.c:4232:ZEND_METHOD(reflection_class, getConstructor)
ext/reflection/php_reflection.c:4252:ZEND_METHOD(reflection_class, hasMethod)
ext/reflection/php_reflection.c:4280:ZEND_METHOD(reflection_class, getMethod)
ext/reflection/php_reflection.c:4325:static void _addmethod(zend_function *mptr, zend_class_entry *ce, zval *retval, zend_long filter, zval *obj)
ext/reflection/php_reflection.c:4347:static int _addmethod_va(zval *el, int num_args, va_list args, zend_hash_key *hash_key)
ext/reflection/php_reflection.c:4362:ZEND_METHOD(reflection_class, getMethods)
ext/reflection/php_reflection.c:4395:ZEND_METHOD(reflection_class, hasProperty)
ext/reflection/php_reflection.c:4430:ZEND_METHOD(reflection_class, getProperty)
ext/reflection/php_reflection.c:4502:static int _addproperty(zval *el, int num_args, va_list args, zend_hash_key *hash_key)
ext/reflection/php_reflection.c:4523:static int _adddynproperty(zval *ptr, int num_args, va_list args, zend_hash_key *hash_key)
ext/reflection/php_reflection.c:4557:ZEND_METHOD(reflection_class, getProperties)
ext/reflection/php_reflection.c:4588:ZEND_METHOD(reflection_class, hasConstant)
ext/reflection/php_reflection.c:4610:ZEND_METHOD(reflection_class, getConstants)
ext/reflection/php_reflection.c:4636:ZEND_METHOD(reflection_class, getReflectionConstants)
ext/reflection/php_reflection.c:4658:ZEND_METHOD(reflection_class, getConstant)
ext/reflection/php_reflection.c:4685:ZEND_METHOD(reflection_class, getReflectionConstant)
ext/reflection/php_reflection.c:4705:static void _class_check_flag(INTERNAL_FUNCTION_PARAMETERS, int mask)
ext/reflection/php_reflection.c:4720:ZEND_METHOD(reflection_class, isInstantiable)
ext/reflection/php_reflection.c:4745:ZEND_METHOD(reflection_class, isCloneable)
ext/reflection/php_reflection.c:4780:ZEND_METHOD(reflection_class, isInterface)
ext/reflection/php_reflection.c:4788:ZEND_METHOD(reflection_class, isTrait)
ext/reflection/php_reflection.c:4796:ZEND_METHOD(reflection_class, isFinal)
ext/reflection/php_reflection.c:4804:ZEND_METHOD(reflection_class, isAbstract)
ext/reflection/php_reflection.c:4812:ZEND_METHOD(reflection_class, getModifiers)
ext/reflection/php_reflection.c:4828:ZEND_METHOD(reflection_class, isInstance)
ext/reflection/php_reflection.c:4845:ZEND_METHOD(reflection_class, newInstance)
ext/reflection/php_reflection.c:4918:ZEND_METHOD(reflection_class, newInstanceWithoutConstructor)
ext/reflection/php_reflection.c:4937:ZEND_METHOD(reflection_class, newInstanceArgs)
ext/reflection/php_reflection.c:5024:ZEND_METHOD(reflection_class, getInterfaces)
ext/reflection/php_reflection.c:5051:ZEND_METHOD(reflection_class, getInterfaceNames)
ext/reflection/php_reflection.c:5073:ZEND_METHOD(reflection_class, getTraits)
ext/reflection/php_reflection.c:5096:ZEND_METHOD(reflection_class, getTraitNames)
ext/reflection/php_reflection.c:5117:ZEND_METHOD(reflection_class, getTraitAliases)
ext/reflection/php_reflection.c:5149:ZEND_METHOD(reflection_class, getParentClass)
ext/reflection/php_reflection.c:5169:ZEND_METHOD(reflection_class, isSubclassOf)
ext/reflection/php_reflection.c:5213:ZEND_METHOD(reflection_class, implementsInterface)
ext/reflection/php_reflection.c:5262:ZEND_METHOD(reflection_class, isIterateable)
ext/reflection/php_reflection.c:5280:ZEND_METHOD(reflection_class, getExtension)
```

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ext/standard/basic_functions.c, max_results=300)` →

```
1093 matches (showing 200)
ext/standard/basic_functions.c:129:static void user_shutdown_function_dtor(zval *zv);
ext/standard/basic_functions.c:130:static void user_tick_function_dtor(user_tick_function_entry *tick_function_entry);
ext/standard/basic_functions.c:138:ZEND_BEGIN_ARG_INFO(arginfo_set_time_limit, 0)
ext/standard/basic_functions.c:140:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:144:ZEND_BEGIN_ARG_INFO(arginfo_header_register_callback, 0)
ext/standard/basic_functions.c:146:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:150:ZEND_BEGIN_ARG_INFO_EX(arginfo_ob_start, 0, 0, 0)
ext/standard/basic_functions.c:154:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:156:ZEND_BEGIN_ARG_INFO(arginfo_ob_flush, 0)
ext/standard/basic_functions.c:157:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:159:ZEND_BEGIN_ARG_INFO(arginfo_ob_clean, 0)
ext/standard/basic_functions.c:160:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:162:ZEND_BEGIN_ARG_INFO(arginfo_ob_end_flush, 0)
ext/standard/basic_functions.c:163:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:165:ZEND_BEGIN_ARG_INFO(arginfo_ob_end_clean, 0)
ext/standard/basic_functions.c:166:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:168:ZEND_BEGIN_ARG_INFO(arginfo_ob_get_flush, 0)
ext/standard/basic_functions.c:169:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:171:ZEND_BEGIN_ARG_INFO(arginfo_ob_get_clean, 0)
ext/standard/basic_functions.c:172:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:174:ZEND_BEGIN_ARG_INFO(arginfo_ob_get_contents, 0)
ext/standard/basic_functions.c:175:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:177:ZEND_BEGIN_ARG_INFO(arginfo_ob_get_level, 0)
ext/standard/basic_functions.c:178:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:180:ZEND_BEGIN_ARG_INFO(arginfo_ob_get_length, 0)
ext/standard/basic_functions.c:181:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:183:ZEND_BEGIN_ARG_INFO(arginfo_ob_list_handlers, 0)
ext/standard/basic_functions.c:184:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:186:ZEND_BEGIN_ARG_INFO_EX(arginfo_ob_get_status, 0, 0, 0)
ext/standard/basic_functions.c:188:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:190:ZEND_BEGIN_ARG_INFO_EX(arginfo_ob_implicit_flush, 0, 0, 0)
ext/standard/basic_functions.c:192:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:194:ZEND_BEGIN_ARG_INFO(arginfo_output_reset_rewrite_vars, 0)
ext/standard/basic_functions.c:195:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:197:ZEND_BEGIN_ARG_INFO(arginfo_output_add_rewrite_var, 0)
ext/standard/basic_functions.c:200:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:203:ZEND_BEGIN_ARG_INFO_EX(arginfo_stream_wrapper_register, 0, 0, 2)
ext/standard/basic_functions.c:207:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:209:ZEND_BEGIN_ARG_INFO(arginfo_stream_wrapper_unregister, 0)
ext/standard/basic_functions.c:211:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:213:ZEND_BEGIN_ARG_INFO(arginfo_stream_wrapper_restore, 0)
ext/standard/basic_functions.c:215:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:218:ZEND_BEGIN_ARG_INFO_EX(arginfo_krsort, 0, 0, 1)
ext/standard/basic_functions.c:221:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:223:ZEND_BEGIN_ARG_INFO_EX(arginfo_ksort, 0, 0, 1)
ext/standard/basic_functions.c:226:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:228:ZEND_BEGIN_ARG_INFO_EX(arginfo_count, 0, 0, 1)
ext/standard/basic_functions.c:231:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:233:ZEND_BEGIN_ARG_INFO(arginfo_natsort, 0)
ext/standard/basic_functions.c:235:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:237:ZEND_BEGIN_ARG_INFO(arginfo_natcasesort, 0)
ext/standard/basic_functions.c:239:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:241:ZEND_BEGIN_ARG_INFO_EX(arginfo_asort, 0, 0, 1)
ext/standard/basic_functions.c:244:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:246:ZEND_BEGIN_ARG_INFO_EX(arginfo_arsort, 0, 0, 1)
ext/standard/basic_functions.c:249:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:251:ZEND_BEGIN_ARG_INFO_EX(arginfo_sort, 0, 0, 1)
ext/standard/basic_functions.c:254:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:256:ZEND_BEGIN_ARG_INFO_EX(arginfo_rsort, 0, 0, 1)
ext/standard/basic_functions.c:259:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:261:ZEND_BEGIN_ARG_INFO(arginfo_usort, 0)
ext/standard/basic_functions.c:264:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:266:ZEND_BEGIN_ARG_INFO(arginfo_uasort, 0)
ext/standard/basic_functions.c:269:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:271:ZEND_BEGIN_ARG_INFO(arginfo_uksort, 0)
ext/standard/basic_functions.c:274:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:276:ZEND_BEGIN_ARG_INFO(arginfo_end, 0)
ext/standard/basic_functions.c:278:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:280:ZEND_BEGIN_ARG_INFO(arginfo_prev, 0)
ext/standard/basic_functions.c:282:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:284:ZEND_BEGIN_ARG_INFO(arginfo_next, 0)
ext/standard/basic_functions.c:286:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:288:ZEND_BEGIN_ARG_INFO(arginfo_reset, 0)
ext/standard/basic_functions.c:290:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:292:ZEND_BEGIN_ARG_INFO(arginfo_current, 0)
ext/standard/basic_functions.c:294:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:296:ZEND_BEGIN_ARG_INFO(arginfo_key, 0)
ext/standard/basic_functions.c:298:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:300:ZEND_BEGIN_ARG_INFO_EX(arginfo_min, 0, 0, 1)
ext/standard/basic_functions.c:302:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:304:ZEND_BEGIN_ARG_INFO_EX(arginfo_max, 0, 0, 1)
ext/standard/basic_functions.c:306:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:308:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_walk, 0, 0, 2)
ext/standard/basic_functions.c:312:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:314:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_walk_recursive, 0, 0, 2)
ext/standard/basic_functions.c:318:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:320:ZEND_BEGIN_ARG_INFO_EX(arginfo_in_array, 0, 0, 2)
ext/standard/basic_functions.c:324:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:326:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_search, 0, 0, 2)
ext/standard/basic_functions.c:330:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:332:ZEND_BEGIN_ARG_INFO_EX(arginfo_extract, 0, 0, 1)
ext/standard/basic_functions.c:336:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:338:ZEND_BEGIN_ARG_INFO_EX(arginfo_compact, 0, 0, 1)
ext/standard/basic_functions.c:340:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:342:ZEND_BEGIN_ARG_INFO(arginfo_array_fill, 0)
ext/standard/basic_functions.c:346:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:348:ZEND_BEGIN_ARG_INFO(arginfo_array_fill_keys, 0)
ext/standard/basic_functions.c:351:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:353:ZEND_BEGIN_ARG_INFO_EX(arginfo_range, 0, 0, 2)
ext/standard/basic_functions.c:357:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:359:ZEND_BEGIN_ARG_INFO(arginfo_shuffle, 0)
ext/standard/basic_functions.c:361:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:363:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_push, 0, 0, 2)
ext/standard/basic_functions.c:366:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:368:ZEND_BEGIN_ARG_INFO(arginfo_array_pop, 0)
ext/standard/basic_functions.c:370:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:372:ZEND_BEGIN_ARG_INFO(arginfo_array_shift, 0)
ext/standard/basic_functions.c:374:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:376:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_unshift, 0, 0, 2)
ext/standard/basic_functions.c:379:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:381:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_splice, 0, 0, 2)
ext/standard/basic_functions.c:386:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:388:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_slice, 0, 0, 2)
ext/standard/basic_functions.c:393:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:395:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_merge, 0, 0, 2)
ext/standard/basic_functions.c:398:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:400:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_merge_recursive, 0, 0, 2)
ext/standard/basic_functions.c:403:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:405:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_replace, 0, 0, 2)
ext/standard/basic_functions.c:408:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:410:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_replace_recursive, 0, 0, 2)
ext/standard/basic_functions.c:413:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:415:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_keys, 0, 0, 1)
ext/standard/basic_functions.c:419:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:421:ZEND_BEGIN_ARG_INFO(arginfo_array_values, 0)
ext/standard/basic_functions.c:423:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:425:ZEND_BEGIN_ARG_INFO(arginfo_array_count_values, 0)
ext/standard/basic_functions.c:427:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:429:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_column, 0, 0, 2)
ext/standard/basic_functions.c:433:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:435:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_reverse, 0, 0, 1)
ext/standard/basic_functions.c:438:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:440:ZEND_BEGIN_ARG_INFO(arginfo_array_pad, 0)
ext/standard/basic_functions.c:444:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:446:ZEND_BEGIN_ARG_INFO(arginfo_array_flip, 0)
ext/standard/basic_functions.c:448:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:450:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_change_key_case, 0, 0, 1)
ext/standard/basic_functions.c:453:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:455:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_unique, 0, 0, 1)
ext/standard/basic_functions.c:458:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:460:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_intersect_key, 0, 0, 2)
ext/standard/basic_functions.c:463:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:465:ZEND_BEGIN_ARG_INFO(arginfo_array_intersect_ukey, 0)
ext/standard/basic_functions.c:469:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:471:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_intersect, 0, 0, 2)
ext/standard/basic_functions.c:474:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:476:ZEND_BEGIN_ARG_INFO(arginfo_array_uintersect, 0)
ext/standard/basic_functions.c:480:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:482:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_intersect_assoc, 0, 0, 2)
ext/standard/basic_functions.c:485:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:487:ZEND_BEGIN_ARG_INFO(arginfo_array_uintersect_assoc, 0)
ext/standard/basic_functions.c:491:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:493:ZEND_BEGIN_ARG_INFO(arginfo_array_intersect_uassoc, 0)
ext/standard/basic_functions.c:497:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:499:ZEND_BEGIN_ARG_INFO(arginfo_array_uintersect_uassoc, 0)
ext/standard/basic_functions.c:504:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:506:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_diff_key, 0, 0, 2)
ext/standard/basic_functions.c:509:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:511:ZEND_BEGIN_ARG_INFO(arginfo_array_diff_ukey, 0)
ext/standard/basic_functions.c:515:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:517:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_diff, 0, 0, 2)
ext/standard/basic_functions.c:520:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:522:ZEND_BEGIN_ARG_INFO(arginfo_array_udiff, 0)
ext/standard/basic_functions.c:526:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:528:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_diff_assoc, 0, 0, 2)
ext/standard/basic_functions.c:531:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:533:ZEND_BEGIN_ARG_INFO(arginfo_array_diff_uassoc, 0)
ext/standard/basic_functions.c:537:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:539:ZEND_BEGIN_ARG_INFO(arginfo_array_udiff_assoc, 0)
ext/standard/basic_functions.c:543:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:545:ZEND_BEGIN_ARG_INFO(arginfo_array_udiff_uassoc, 0)
ext/standard/basic_functions.c:550:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:552:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_multisort, 0, 0, 1)
ext/standard/basic_functions.c:557:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:559:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_rand, 0, 0, 1)
ext/standard/basic_functions.c:562:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:564:ZEND_BEGIN_ARG_INFO(arginfo_array_sum, 0)
ext/standard/basic_functions.c:566:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:568:ZEND_BEGIN_ARG_INFO(arginfo_array_product, 0)
ext/standard/basic_functions.c:570:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:572:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_reduce, 0, 0, 2)
ext/standard/basic_functions.c:576:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:578:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_filter, 0, 0, 1)
ext/standard/basic_functions.c:582:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:584:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_map, 0, 0, 2)
ext/standard/basic_functions.c:587:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:589:ZEND_BEGIN_ARG_INFO(arginfo_array_key_exists, 0)
ext/standard/basic_functions.c:592:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:594:ZEND_BEGIN_ARG_INFO_EX(arginfo_array_chunk, 0, 0, 2)
ext/standard/basic_functions.c:598:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:600:ZEND_BEGIN_ARG_INFO(arginfo_array_combine, 0)
ext/standard/basic_functions.c:603:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:606:ZEND_BEGIN_ARG_INFO(arginfo_get_magic_quotes_gpc, 0)
ext/standard/basic_functions.c:607:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:609:ZEND_BEGIN_ARG_INFO(arginfo_get_magic_quotes_runtime, 0)
ext/standard/basic_functions.c:610:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:612:ZEND_BEGIN_ARG_INFO(arginfo_constant, 0)
ext/standard/basic_functions.c:614:ZEND_END_ARG_INFO()
ext/standard/basic_functions.c:617:ZEND_BEGIN_ARG_INFO(arginfo_inet_ntop, 0)
ext/standard/basic_functions.c:619:ZEND_END_ARG_INFO()
```

### Turn 3  _(tok 55640+1436, stop=tool_use)_

**Reasoning:** I'm dropping the broad search and reading the specific call sites instead. For each one I'll look at a window of lines leading up to the call, to find the enclosing function. The first site is at zend_API.c line 1133, which calls zend_update_class_constants, defined at line 1083.

I'm checking the remaining call sites one at a time, confirming each enclosing function by its line range. For the recursive call at line 638, I'm weighing whether zval_update_constant_ex should count as its own caller, and I plan to re-read that function's body to settle it.

I'm checking the remaining call sites, starting with the zend_vm_def.h and zend_vm_execute.h handlers, then the php_reflection.c and basic_functions.c entries. The zend_ini_parser.y call should be verified against whether a generated zend_ini_parser.c also exists in the repo.

I'm going to look up the ZEND_VM_HANDLER definitions in zend_vm_def.h with their line numbers, so I can match each of the VM call sites to its handler.



- `grep(pattern=^ZEND_VM_(HOT_)?(HANDLER|C_LABEL|HELPER|NOCONST_HANDLER)\(|^, version=old, path_glob=Zend/zend_vm_def.h, max_results=400)` →

```
229 matches (showing 200)
Zend/zend_vm_def.h:28:ZEND_VM_HANDLER(1, ZEND_ADD, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:71:ZEND_VM_HANDLER(2, ZEND_SUB, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:114:ZEND_VM_HANDLER(3, ZEND_MUL, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:160:ZEND_VM_HANDLER(4, ZEND_DIV, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:175:ZEND_VM_HANDLER(5, ZEND_MOD, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:213:ZEND_VM_HANDLER(6, ZEND_SL, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:228:ZEND_VM_HANDLER(7, ZEND_SR, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:243:ZEND_VM_HANDLER(166, ZEND_POW, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:258:ZEND_VM_HANDLER(8, ZEND_CONCAT, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:318:ZEND_VM_HANDLER(15, ZEND_IS_IDENTICAL, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:336:ZEND_VM_HANDLER(16, ZEND_IS_NOT_IDENTICAL, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:354:ZEND_VM_HANDLER(17, ZEND_IS_EQUAL, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:422:ZEND_VM_HANDLER(18, ZEND_IS_NOT_EQUAL, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:490:ZEND_VM_HANDLER(19, ZEND_IS_SMALLER, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:540:ZEND_VM_HANDLER(20, ZEND_IS_SMALLER_OR_EQUAL, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:590:ZEND_VM_HANDLER(170, ZEND_SPACESHIP, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:605:ZEND_VM_HANDLER(9, ZEND_BW_OR, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:620:ZEND_VM_HANDLER(10, ZEND_BW_AND, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:635:ZEND_VM_HANDLER(11, ZEND_BW_XOR, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:650:ZEND_VM_HANDLER(14, ZEND_BOOL_XOR, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:665:ZEND_VM_HANDLER(12, ZEND_BW_NOT, CONST|TMPVAR|CV, ANY)
Zend/zend_vm_def.h:677:ZEND_VM_HANDLER(13, ZEND_BOOL_NOT, CONST|TMPVAR|CV, ANY)
Zend/zend_vm_def.h:702:ZEND_VM_HELPER(zend_binary_assign_op_obj_helper, VAR|UNUSED|CV, CONST|TMPVAR|CV, binary_op_type binary_op)
Zend/zend_vm_def.h:765:ZEND_VM_HELPER(zend_binary_assign_op_dim_helper, VAR|UNUSED|CV, CONST|TMPVAR|UNUSED|CV, binary_op_type binary_op)
Zend/zend_vm_def.h:782:ZEND_VM_C_LABEL(assign_dim_op_array):
Zend/zend_vm_def.h:784:ZEND_VM_C_LABEL(assign_dim_op_new_array):
Zend/zend_vm_def.h:835:ZEND_VM_C_LABEL(assign_dim_op_convert_to_array):
Zend/zend_vm_def.h:854:ZEND_VM_C_LABEL(assign_dim_op_ret_null):
Zend/zend_vm_def.h:869:ZEND_VM_HELPER(zend_binary_assign_op_helper, VAR|CV, CONST|TMPVAR|CV, binary_op_type binary_op)
Zend/zend_vm_def.h:900:ZEND_VM_HANDLER(23, ZEND_ASSIGN_ADD, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:920:ZEND_VM_HANDLER(24, ZEND_ASSIGN_SUB, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:940:ZEND_VM_HANDLER(25, ZEND_ASSIGN_MUL, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:960:ZEND_VM_HANDLER(26, ZEND_ASSIGN_DIV, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:980:ZEND_VM_HANDLER(27, ZEND_ASSIGN_MOD, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:1000:ZEND_VM_HANDLER(28, ZEND_ASSIGN_SL, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:1020:ZEND_VM_HANDLER(29, ZEND_ASSIGN_SR, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:1040:ZEND_VM_HANDLER(30, ZEND_ASSIGN_CONCAT, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:1060:ZEND_VM_HANDLER(31, ZEND_ASSIGN_BW_OR, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:1080:ZEND_VM_HANDLER(32, ZEND_ASSIGN_BW_AND, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:1100:ZEND_VM_HANDLER(33, ZEND_ASSIGN_BW_XOR, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:1120:ZEND_VM_HANDLER(167, ZEND_ASSIGN_POW, VAR|UNUSED|THIS|CV, CONST|TMPVAR|UNUSED|NEXT|CV, DIM_OBJ)
Zend/zend_vm_def.h:1140:ZEND_VM_HELPER(zend_pre_incdec_property_helper, VAR|UNUSED|CV, CONST|TMPVAR|CV, int inc)
Zend/zend_vm_def.h:1209:ZEND_VM_HANDLER(132, ZEND_PRE_INC_OBJ, VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:1214:ZEND_VM_HANDLER(133, ZEND_PRE_DEC_OBJ, VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:1219:ZEND_VM_HELPER(zend_post_incdec_property_helper, VAR|UNUSED|CV, CONST|TMPVAR|CV, int inc)
Zend/zend_vm_def.h:1283:ZEND_VM_HANDLER(134, ZEND_POST_INC_OBJ, VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:1288:ZEND_VM_HANDLER(135, ZEND_POST_DEC_OBJ, VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:1293:ZEND_VM_HANDLER(34, ZEND_PRE_INC, VAR|CV, ANY, SPEC(RETVAL))
Zend/zend_vm_def.h:1333:ZEND_VM_HANDLER(35, ZEND_PRE_DEC, VAR|CV, ANY, SPEC(RETVAL))
Zend/zend_vm_def.h:1373:ZEND_VM_HANDLER(36, ZEND_POST_INC, VAR|CV, ANY)
Zend/zend_vm_def.h:1406:ZEND_VM_HANDLER(37, ZEND_POST_DEC, VAR|CV, ANY)
Zend/zend_vm_def.h:1439:ZEND_VM_HANDLER(40, ZEND_ECHO, CONST|TMPVAR|CV, ANY)
Zend/zend_vm_def.h:1469:ZEND_VM_HELPER(zend_fetch_var_address_helper, CONST|TMPVAR|CV, UNUSED, int type)
Zend/zend_vm_def.h:1556:ZEND_VM_HANDLER(80, ZEND_FETCH_R, CONST|TMPVAR|CV, UNUSED, VAR_FETCH)
Zend/zend_vm_def.h:1561:ZEND_VM_HANDLER(83, ZEND_FETCH_W, CONST|TMPVAR|CV, UNUSED, VAR_FETCH)
Zend/zend_vm_def.h:1566:ZEND_VM_HANDLER(86, ZEND_FETCH_RW, CONST|TMPVAR|CV, UNUSED, VAR_FETCH)
Zend/zend_vm_def.h:1571:ZEND_VM_HANDLER(92, ZEND_FETCH_FUNC_ARG, CONST|TMPVAR|CV, UNUSED, VAR_FETCH|ARG_NUM)
Zend/zend_vm_def.h:1582:ZEND_VM_HANDLER(95, ZEND_FETCH_UNSET, CONST|TMPVAR|CV, UNUSED, VAR_FETCH)
Zend/zend_vm_def.h:1587:ZEND_VM_HANDLER(89, ZEND_FETCH_IS, CONST|TMPVAR|CV, UNUSED, VAR_FETCH)
Zend/zend_vm_def.h:1592:ZEND_VM_HELPER(zend_fetch_static_prop_helper, CONST|TMPVAR|CV, UNUSED|CONST|VAR, int type)
Zend/zend_vm_def.h:1684:ZEND_VM_C_LABEL(fetch_static_prop_return):
Zend/zend_vm_def.h:1697:ZEND_VM_HANDLER(173, ZEND_FETCH_STATIC_PROP_R, CONST|TMPVAR|CV, UNUSED|CLASS_FETCH|CONST|VAR)
Zend/zend_vm_def.h:1702:ZEND_VM_HANDLER(174, ZEND_FETCH_STATIC_PROP_W, CONST|TMPVAR|CV, UNUSED|CLASS_FETCH|CONST|VAR)
Zend/zend_vm_def.h:1707:ZEND_VM_HANDLER(175, ZEND_FETCH_STATIC_PROP_RW, CONST|TMPVAR|CV, UNUSED|CLASS_FETCH|CONST|VAR)
Zend/zend_vm_def.h:1712:ZEND_VM_HANDLER(177, ZEND_FETCH_STATIC_PROP_FUNC_ARG, CONST|TMPVAR|CV, UNUSED|CLASS_FETCH|CONST|VAR, NUM)
Zend/zend_vm_def.h:1723:ZEND_VM_HANDLER(178, ZEND_FETCH_STATIC_PROP_UNSET, CONST|TMPVAR|CV, UNUSED|CLASS_FETCH|CONST|VAR)
Zend/zend_vm_def.h:1728:ZEND_VM_HANDLER(176, ZEND_FETCH_STATIC_PROP_IS, CONST|TMPVAR|CV, UNUSED|CLASS_FETCH|CONST|VAR)
Zend/zend_vm_def.h:1733:ZEND_VM_HANDLER(81, ZEND_FETCH_DIM_R, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:1747:ZEND_VM_HANDLER(84, ZEND_FETCH_DIM_W, VAR|CV, CONST|TMPVAR|UNUSED|NEXT|CV)
Zend/zend_vm_def.h:1765:ZEND_VM_HANDLER(87, ZEND_FETCH_DIM_RW, VAR|CV, CONST|TMPVAR|UNUSED|NEXT|CV)
Zend/zend_vm_def.h:1783:ZEND_VM_HANDLER(90, ZEND_FETCH_DIM_IS, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:1797:ZEND_VM_HANDLER(93, ZEND_FETCH_DIM_FUNC_ARG, CONST|TMP|VAR|CV, CONST|TMPVAR|UNUSED|NEXT|CV, NUM)
Zend/zend_vm_def.h:1834:ZEND_VM_HANDLER(96, ZEND_FETCH_DIM_UNSET, VAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:1852:ZEND_VM_HANDLER(82, ZEND_FETCH_OBJ_R, CONST|TMP|VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:1908:ZEND_VM_C_LABEL(fetch_obj_r_no_object):
Zend/zend_vm_def.h:1925:ZEND_VM_HANDLER(85, ZEND_FETCH_OBJ_W, VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:1951:ZEND_VM_HANDLER(88, ZEND_FETCH_OBJ_RW, VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:1976:ZEND_VM_HANDLER(91, ZEND_FETCH_OBJ_IS, CONST|TMPVAR|UNUSED|THIS|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:2032:ZEND_VM_C_LABEL(fetch_obj_is_no_object):
Zend/zend_vm_def.h:2049:ZEND_VM_HANDLER(94, ZEND_FETCH_OBJ_FUNC_ARG, CONST|TMP|VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV, NUM)
Zend/zend_vm_def.h:2086:ZEND_VM_HANDLER(97, ZEND_FETCH_OBJ_UNSET, VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:2112:ZEND_VM_HANDLER(98, ZEND_FETCH_LIST, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:2125:ZEND_VM_HANDLER(136, ZEND_ASSIGN_OBJ, VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV, SPEC(OP_DATA=CONST|TMP|VAR|CV))
Zend/zend_vm_def.h:2197:ZEND_VM_C_LABEL(fast_assign_obj):
Zend/zend_vm_def.h:2289:ZEND_VM_C_LABEL(exit_assign_obj):
Zend/zend_vm_def.h:2296:ZEND_VM_HANDLER(147, ZEND_ASSIGN_DIM, VAR|CV, CONST|TMPVAR|UNUSED|NEXT|CV, SPEC(OP_DATA=CONST|TMP|VAR|CV))
Zend/zend_vm_def.h:2310:ZEND_VM_C_LABEL(try_assign_dim_array):
Zend/zend_vm_def.h:2375:ZEND_VM_C_LABEL(assign_dim_convert_to_array):
Zend/zend_vm_def.h:2387:ZEND_VM_C_LABEL(assign_dim_error):
Zend/zend_vm_def.h:2402:ZEND_VM_HANDLER(38, ZEND_ASSIGN, VAR|CV, CONST|TMP|VAR|CV, SPEC(RETVAL))
Zend/zend_vm_def.h:2430:ZEND_VM_HANDLER(39, ZEND_ASSIGN_REF, VAR|CV, VAR|CV, SRC)
Zend/zend_vm_def.h:2485:ZEND_VM_HELPER(zend_leave_helper, ANY, ANY)
Zend/zend_vm_def.h:2603:ZEND_VM_HANDLER(42, ZEND_JMP, JMP_ADDR, ANY)
Zend/zend_vm_def.h:2611:ZEND_VM_HANDLER(43, ZEND_JMPZ, CONST|TMPVAR|CV, JMP_ADDR)
Zend/zend_vm_def.h:2646:ZEND_VM_HANDLER(44, ZEND_JMPNZ, CONST|TMPVAR|CV, JMP_ADDR)
Zend/zend_vm_def.h:2680:ZEND_VM_HANDLER(45, ZEND_JMPZNZ, CONST|TMPVAR|CV, JMP_ADDR, JMP_ADDR)
Zend/zend_vm_def.h:2717:ZEND_VM_HANDLER(46, ZEND_JMPZ_EX, CONST|TMPVAR|CV, JMP_ADDR)
Zend/zend_vm_def.h:2760:ZEND_VM_HANDLER(47, ZEND_JMPNZ_EX, CONST|TMPVAR|CV, JMP_ADDR)
Zend/zend_vm_def.h:2800:ZEND_VM_HANDLER(70, ZEND_FREE, TMPVAR, LIVE_RANGE)
Zend/zend_vm_def.h:2809:ZEND_VM_HANDLER(127, ZEND_FE_FREE, TMPVAR, LIVE_RANGE)
Zend/zend_vm_def.h:2823:ZEND_VM_HANDLER(53, ZEND_FAST_CONCAT, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:2890:ZEND_VM_HANDLER(54, ZEND_ROPE_INIT, UNUSED, CONST|TMPVAR|CV, NUM)
Zend/zend_vm_def.h:2923:ZEND_VM_HANDLER(55, ZEND_ROPE_ADD, TMP, CONST|TMPVAR|CV, NUM)
Zend/zend_vm_def.h:2956:ZEND_VM_HANDLER(56, ZEND_ROPE_END, TMP, CONST|TMPVAR|CV, NUM)
Zend/zend_vm_def.h:3009:ZEND_VM_HANDLER(109, ZEND_FETCH_CLASS, ANY, CONST|TMPVAR|UNUSED|CV, CLASS_FETCH)
Zend/zend_vm_def.h:3021:ZEND_VM_C_LABEL(try_class_name):
Zend/zend_vm_def.h:3052:ZEND_VM_HANDLER(112, ZEND_INIT_METHOD_CALL, CONST|TMPVAR|UNUSED|THIS|CV, CONST|TMPVAR|CV, NUM)
Zend/zend_vm_def.h:3176:ZEND_VM_HANDLER(113, ZEND_INIT_STATIC_METHOD_CALL, UNUSED|CLASS_FETCH|CONST|VAR, CONST|TMPVAR|UNUSED|CONSTRUCTOR|CV, NUM)
Zend/zend_vm_def.h:3334:ZEND_VM_HANDLER(59, ZEND_INIT_FCALL_BY_NAME, ANY, CONST, NUM)
Zend/zend_vm_def.h:3364:ZEND_VM_HANDLER(128, ZEND_INIT_DYNAMIC_CALL, ANY, CONST|TMPVAR|CV, NUM)
Zend/zend_vm_def.h:3374:ZEND_VM_C_LABEL(try_function_name):
Zend/zend_vm_def.h:3407:ZEND_VM_HANDLER(118, ZEND_INIT_USER_CALL, CONST, CONST|TMPVAR|CV, NUM)
Zend/zend_vm_def.h:3468:ZEND_VM_HANDLER(69, ZEND_INIT_NS_FCALL_BY_NAME, ANY, CONST, NUM)
Zend/zend_vm_def.h:3504:ZEND_VM_HANDLER(61, ZEND_INIT_FCALL, NUM, CONST, NUM)
Zend/zend_vm_def.h:3537:ZEND_VM_HANDLER(129, ZEND_DO_ICALL, ANY, ANY, SPEC(RETVAL))
Zend/zend_vm_def.h:3584:ZEND_VM_HANDLER(130, ZEND_DO_UCALL, ANY, ANY, SPEC(RETVAL))
Zend/zend_vm_def.h:3608:ZEND_VM_HANDLER(131, ZEND_DO_FCALL_BY_NAME, ANY, ANY, SPEC(RETVAL))
Zend/zend_vm_def.h:3701:ZEND_VM_HANDLER(60, ZEND_DO_FCALL, ANY, ANY, SPEC(RETVAL))
Zend/zend_vm_def.h:3830:ZEND_VM_C_LABEL(fcall_end_change_scope):
Zend/zend_vm_def.h:3847:ZEND_VM_C_LABEL(fcall_end):
Zend/zend_vm_def.h:3861:ZEND_VM_HANDLER(124, ZEND_VERIFY_RETURN_TYPE, CONST|TMP|VAR|UNUSED|CV, UNUSED)
Zend/zend_vm_def.h:3916:ZEND_VM_HANDLER(62, ZEND_RETURN, CONST|TMP|VAR|CV, ANY)
Zend/zend_vm_def.h:3981:ZEND_VM_HANDLER(111, ZEND_RETURN_BY_REF, CONST|TMP|VAR|CV, ANY, SRC)
Zend/zend_vm_def.h:4039:ZEND_VM_HANDLER(161, ZEND_GENERATOR_RETURN, CONST|TMP|VAR|CV, ANY)
Zend/zend_vm_def.h:4084:ZEND_VM_HANDLER(108, ZEND_THROW, CONST|TMP|VAR|CV, ANY)
Zend/zend_vm_def.h:4124:ZEND_VM_HANDLER(107, ZEND_CATCH, CONST, CV, JMP_ADDR)
Zend/zend_vm_def.h:4174:ZEND_VM_HANDLER(65, ZEND_SEND_VAL, CONST|TMP, NUM)
Zend/zend_vm_def.h:4191:ZEND_VM_HANDLER(116, ZEND_SEND_VAL_EX, CONST|TMP, NUM, SPEC(QUICK_ARG))
Zend/zend_vm_def.h:4203:ZEND_VM_C_LABEL(send_val_by_ref):
Zend/zend_vm_def.h:4222:ZEND_VM_HANDLER(117, ZEND_SEND_VAR, VAR|CV, NUM)
Zend/zend_vm_def.h:4261:ZEND_VM_HANDLER(106, ZEND_SEND_VAR_NO_REF, VAR, NUM, SEND)
Zend/zend_vm_def.h:4295:ZEND_VM_HANDLER(67, ZEND_SEND_REF, VAR|CV, NUM)
Zend/zend_vm_def.h:4323:ZEND_VM_HANDLER(66, ZEND_SEND_VAR_EX, VAR|CV, NUM, SPEC(QUICK_ARG))
Zend/zend_vm_def.h:4335:ZEND_VM_C_LABEL(send_var_by_ref):
Zend/zend_vm_def.h:4372:ZEND_VM_HANDLER(165, ZEND_SEND_UNPACK, ANY, ANY)
Zend/zend_vm_def.h:4383:ZEND_VM_C_LABEL(send_again):
Zend/zend_vm_def.h:4516:ZEND_VM_C_LABEL(unpack_iter_dtor):
Zend/zend_vm_def.h:4533:ZEND_VM_HANDLER(119, ZEND_SEND_ARRAY, ANY, ANY)
Zend/zend_vm_def.h:4565:ZEND_VM_C_LABEL(send_array):
Zend/zend_vm_def.h:4611:ZEND_VM_HANDLER(120, ZEND_SEND_USER, VAR|CV, NUM)
Zend/zend_vm_def.h:4659:ZEND_VM_HANDLER(63, ZEND_RECV, NUM, ANY)
Zend/zend_vm_def.h:4680:ZEND_VM_HANDLER(64, ZEND_RECV_INIT, NUM, CONST)
Zend/zend_vm_def.h:4718:ZEND_VM_HANDLER(164, ZEND_RECV_VARIADIC, NUM, ANY)
Zend/zend_vm_def.h:4758:ZEND_VM_HANDLER(52, ZEND_BOOL, CONST|TMPVAR|CV, ANY)
Zend/zend_vm_def.h:4783:ZEND_VM_HANDLER(48, ZEND_CASE, CONST|TMPVAR|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:4857:ZEND_VM_HANDLER(68, ZEND_NEW, UNUSED|CLASS_FETCH|CONST|VAR, ANY, NUM)
Zend/zend_vm_def.h:4921:ZEND_VM_HANDLER(110, ZEND_CLONE, CONST|TMPVAR|UNUSED|THIS|CV, ANY)
Zend/zend_vm_def.h:4997:ZEND_VM_HANDLER(99, ZEND_FETCH_CONSTANT, UNUSED, CONST, CONST_FETCH)
Zend/zend_vm_def.h:5041:ZEND_VM_HANDLER(181, ZEND_FETCH_CLASS_CONSTANT, VAR|CONST|UNUSED|CLASS_FETCH, CONST)
Zend/zend_vm_def.h:5123:ZEND_VM_HANDLER(72, ZEND_ADD_ARRAY_ELEMENT, CONST|TMP|VAR|CV, CONST|TMPVAR|UNUSED|NEXT|CV, REF)
Zend/zend_vm_def.h:5173:ZEND_VM_C_LABEL(add_again):
Zend/zend_vm_def.h:5181:ZEND_VM_C_LABEL(str_index):
Zend/zend_vm_def.h:5185:ZEND_VM_C_LABEL(num_index):
Zend/zend_vm_def.h:5217:ZEND_VM_HANDLER(71, ZEND_INIT_ARRAY, CONST|TMP|VAR|UNUSED|CV, CONST|TMPVAR|UNUSED|NEXT|CV, ARRAY_INIT|REF)
Zend/zend_vm_def.h:5248:ZEND_VM_HANDLER(21, ZEND_CAST, CONST|TMP|VAR|CV, ANY, TYPE)
Zend/zend_vm_def.h:5350:ZEND_VM_HANDLER(73, ZEND_INCLUDE_OR_EVAL, CONST|TMPVAR|CV, ANY, EVAL)
Zend/zend_vm_def.h:5411:ZEND_VM_HANDLER(74, ZEND_UNSET_VAR, CONST|TMPVAR|CV, UNUSED, VAR_FETCH|ISSET)
Zend/zend_vm_def.h:5466:ZEND_VM_HANDLER(179, ZEND_UNSET_STATIC_PROP, CONST|TMPVAR|CV, UNUSED|CLASS_FETCH|CONST|VAR)
Zend/zend_vm_def.h:5524:ZEND_VM_HANDLER(75, ZEND_UNSET_DIM, VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:5546:ZEND_VM_C_LABEL(unset_dim_array):
Zend/zend_vm_def.h:5549:ZEND_VM_C_LABEL(offset_again):
Zend/zend_vm_def.h:5557:ZEND_VM_C_LABEL(str_index_dim):
Zend/zend_vm_def.h:5565:ZEND_VM_C_LABEL(num_index_dim):
Zend/zend_vm_def.h:5621:ZEND_VM_HANDLER(76, ZEND_UNSET_OBJ, VAR|UNUSED|THIS|CV, CONST|TMPVAR|CV)
Zend/zend_vm_def.h:5660:ZEND_VM_HANDLER(77, ZEND_FE_RESET_R, CONST|TMP|VAR|CV, JMP_ADDR)
Zend/zend_vm_def.h:5765:ZEND_VM_HANDLER(125, ZEND_FE_RESET_RW, CONST|TMP|VAR|CV, JMP_ADDR)
Zend/zend_vm_def.h:5930:ZEND_VM_HANDLER(78, ZEND_FE_FETCH_R, VAR, ANY, JMP_ADDR)
Zend/zend_vm_def.h:6083:ZEND_VM_C_LABEL(fe_fetch_r_exit):
Zend/zend_vm_def.h:6103:ZEND_VM_HANDLER(126, ZEND_FE_FETCH_RW, VAR, ANY, JMP_ADDR)
Zend/zend_vm_def.h:6271:ZEND_VM_C_LABEL(fe_fetch_w_exit):
Zend/zend_vm_def.h:6300:ZEND_VM_HANDLER(114, ZEND_ISSET_ISEMPTY_VAR, CONST|TMPVAR|CV, UNUSED, VAR_FETCH|ISSET)
Zend/zend_vm_def.h:6358:ZEND_VM_HANDLER(180, ZEND_ISSET_ISEMPTY_STATIC_PROP, CONST|TMPVAR|CV, UNUSED|CLASS_FETCH|CONST|VAR, ISSET)
Zend/zend_vm_def.h:6429:ZEND_VM_C_LABEL(is_static_prop_return):
Zend/zend_vm_def.h:6442:ZEND_VM_HANDLER(115, ZEND_ISSET_ISEMPTY_DIM_OBJ, CONST|TMPVAR|UNUSED|THIS|CV, CONST|TMPVAR|CV, ISSET)
Zend/zend_vm_def.h:6467:ZEND_VM_C_LABEL(isset_dim_obj_array):
Zend/zend_vm_def.h:6469:ZEND_VM_C_LABEL(isset_again):
Zend/zend_vm_def.h:6477:ZEND_VM_C_LABEL(str_index_prop):
Zend/zend_vm_def.h:6481:ZEND_VM_C_LABEL(num_index_prop):
Zend/zend_vm_def.h:6544:ZEND_VM_C_LABEL(isset_str_offset):
Zend/zend_vm_def.h:6570:ZEND_VM_C_LABEL(isset_not_found):
Zend/zend_vm_def.h:6574:ZEND_VM_C_LABEL(isset_dim_obj_exit):
Zend/zend_vm_def.h:6582:ZEND_VM_HANDLER(148, ZEND_ISSET_ISEMPTY_PROP_OBJ, CONST|TMPVAR|UNUSED|THIS|CV, CONST|TMPVAR|CV, ISSET)
Zend/zend_vm_def.h:6614:ZEND_VM_C_LABEL(isset_no_object):
Zend/zend_vm_def.h:6629:ZEND_VM_HANDLER(79, ZEND_EXIT, CONST|TMPVAR|UNUSED|CV, ANY)
Zend/zend_vm_def.h:6658:ZEND_VM_HANDLER(57, ZEND_BEGIN_SILENCE, ANY, ANY)
Zend/zend_vm_def.h:6691:ZEND_VM_HANDLER(58, ZEND_END_SILENCE, TMP, ANY)
Zend/zend_vm_def.h:6701:ZEND_VM_HANDLER(152, ZEND_JMP_SET, CONST|TMP|VAR|CV, JMP_ADDR)
Zend/zend_vm_def.h:6740:ZEND_VM_HANDLER(169, ZEND_COALESCE, CONST|TMP|VAR|CV, JMP_ADDR)
Zend/zend_vm_def.h:6780:ZEND_VM_HANDLER(22, ZEND_QM_ASSIGN, CONST|TMP|VAR|CV, ANY)
Zend/zend_vm_def.h:6814:ZEND_VM_HANDLER(101, ZEND_EXT_STMT, ANY, ANY)
Zend/zend_vm_def.h:6826:ZEND_VM_HANDLER(102, ZEND_EXT_FCALL_BEGIN, ANY, ANY)
Zend/zend_vm_def.h:6838:ZEND_VM_HANDLER(103, ZEND_EXT_FCALL_END, ANY, ANY)
Zend/zend_vm_def.h:6850:ZEND_VM_HANDLER(139, ZEND_DECLARE_CLASS, ANY, ANY)
Zend/zend_vm_def.h:6859:ZEND_VM_HANDLER(140, ZEND_DECLARE_INHERITED_CLASS, ANY, VAR)
Zend/zend_vm_def.h:6868:ZEND_VM_HANDLER(145, ZEND_DECLARE_INHERITED_CLASS_DELAYED, ANY, VAR)
Zend/zend_vm_def.h:6882:ZEND_VM_HANDLER(171, ZEND_DECLARE_ANON_CLASS, ANY, ANY, JMP_ADDR)
Zend/zend_vm_def.h:6904:ZEND_VM_HANDLER(172, ZEND_DECLARE_ANON_INHERITED_CLASS, ANY, VAR, JMP_ADDR)
Zend/zend_vm_def.h:6924:ZEND_VM_HANDLER(141, ZEND_DECLARE_FUNCTION, ANY, ANY)
Zend/zend_vm_def.h:6933:ZEND_VM_HANDLER(105, ZEND_TICKS, ANY, ANY, NUM)
Zend/zend_vm_def.h:6948:ZEND_VM_HANDLER(138, ZEND_INSTANCEOF, TMPVAR|CV, UNUSED|CLASS_FETCH|CONST|VAR)
```

- `read_file(path=Zend/zend_execute_API.c, version=old, start_line=554, end_line=664)` →

```
Zend/zend_execute_API.c lines 554-664 of 1722
  554| ZEND_API int zval_update_constant_ex(zval *p, zend_bool inline_change, zend_class_entry *scope) /* {{{ */
  555| {
  556| 	zval *const_value;
  557| 	char *colon;
  558| 
  559| 	if (IS_CONSTANT_VISITED(p)) {
  560| 		zend_throw_error(NULL, "Cannot declare self-referencing constant '%s'", Z_STRVAL_P(p));
  561| 		return FAILURE;
  562| 	} else if (Z_TYPE_P(p) == IS_CONSTANT) {
  563| 
  564| 		SEPARATE_ZVAL_NOREF(p);
  565| 		MARK_CONSTANT_VISITED(p);
  566| 		if (Z_CONST_FLAGS_P(p) & IS_CONSTANT_CLASS) {
  567| 			ZEND_ASSERT(EG(current_execute_data));
  568| 			if (inline_change) {
  569| 				zend_string_release(Z_STR_P(p));
  570| 			}
  571| 			if (EG(scope) && EG(scope)->name) {
  572| 				ZVAL_STR_COPY(p, EG(scope)->name);
  573| 			} else {
  574| 				ZVAL_EMPTY_STRING(p);
  575| 			}
  576| 		} else if (UNEXPECTED((const_value = zend_get_constant_ex(Z_STR_P(p), scope, Z_CONST_FLAGS_P(p))) == NULL)) {
  577| 			char *actual = Z_STRVAL_P(p);
  578| 
  579| 			if (UNEXPECTED(EG(exception))) {
  580| 				RESET_CONSTANT_VISITED(p);
  581| 				return FAILURE;
  582| 			} else if ((colon = (char*)zend_memrchr(Z_STRVAL_P(p), ':', Z_STRLEN_P(p)))) {
  583| 				zend_throw_error(NULL, "Undefined class constant '%s'", Z_STRVAL_P(p));
  584| 				RESET_CONSTANT_VISITED(p);
  585| 				return FAILURE;
  586| 			} else {
  587| 				zend_string *save = Z_STR_P(p);
  588| 				char *slash;
  589| 				size_t actual_len = Z_STRLEN_P(p);
  590| 				if ((Z_CONST_FLAGS_P(p) & IS_CONSTANT_UNQUALIFIED) && (slash = (char *)zend_memrchr(actual, '\\', actual_len))) {
  591| 					actual = slash + 1;
  592| 					actual_len -= (actual - Z_STRVAL_P(p));
  593| 					if (inline_change) {
  594| 						zend_string *s = zend_string_init(actual, actual_len, 0);
  595| 						Z_STR_P(p) = s;
  596| 						Z_TYPE_FLAGS_P(p) = IS_TYPE_REFCOUNTED | IS_TYPE_COPYABLE;
  597| 					}
  598| 				}
  599| 				if (actual[0] == '\\') {
  600| 					if (inline_change) {
  601| 						memmove(Z_STRVAL_P(p), Z_STRVAL_P(p)+1, Z_STRLEN_P(p));
  602| 						--Z_STRLEN_P(p);
  603| 					} else {
  604| 						++actual;
  605| 					}
  606| 					--actual_len;
  607| 				}
  608| 				if ((Z_CONST_FLAGS_P(p) & IS_CONSTANT_UNQUALIFIED) == 0) {
  609| 					if (ZSTR_VAL(save)[0] == '\\') {
  610| 						zend_throw_error(NULL, "Undefined constant '%s'", ZSTR_VAL(save) + 1);
  611| 					} else {
  612| 						zend_throw_error(NULL, "Undefined constant '%s'", ZSTR_VAL(save));
  613| 					}
  614| 					if (inline_change) {
  615| 						zend_string_release(save);
  616| 					}
  617| 					RESET_CONSTANT_VISITED(p);
  618| 					return FAILURE;
  619| 				} else {
  620| 					zend_error(E_NOTICE, "Use of undefined constant %s - assumed '%s'",  actual,  actual);
  621| 					if (!inline_change) {
  622| 						ZVAL_STRINGL(p, actual, actual_len);
  623| 					} else {
  624| 						Z_TYPE_INFO_P(p) = Z_REFCOUNTED_P(p) ?
  625| 							IS_STRING_EX : IS_INTERNED_STRING_EX;
  626| 						if (save && ZSTR_VAL(save) != actual) {
  627| 							zend_string_release(save);
  628| 						}
  629| 					}
  630| 				}
  631| 			}
  632| 		} else {
  633| 			if (inline_change) {
  634| 				zend_string_release(Z_STR_P(p));
  635| 			}
  636| 			ZVAL_COPY_VALUE(p, const_value);
  637| 			if (Z_OPT_CONSTANT_P(p)) {
  638| 				if (UNEXPECTED(zval_update_constant_ex(p, 1, NULL) != SUCCESS)) {
  639| 					RESET_CONSTANT_VISITED(p);
  640| 					return FAILURE;
  641| 				}
  642| 			}
  643| 			zval_opt_copy_ctor(p);
  644| 		}
  645| 	} else if (Z_TYPE_P(p) == IS_CONSTANT_AST) {
  646| 		zval tmp;
  647| 
  648| 		if (UNEXPECTED(zend_ast_evaluate(&tmp, Z_ASTVAL_P(p), scope) != SUCCESS)) {
  649| 			return FAILURE;
  650| 		}
  651| 		if (inline_change) {
  652| 			zval_ptr_dtor(p);
  653| 		}
  654| 		ZVAL_COPY_VALUE(p, &tmp);
  655| 	}
  656| 	return SUCCESS;
  657| }
  658| /* }}} */
  659| 
  660| ZEND_API int zval_update_constant(zval *pp, zend_bool inline_change) /* {{{ */
  661| {
  662| 	return zval_update_constant_ex(pp, inline_change, NULL);
  663| }
  664| /* }}} */
```

- `read_file(path=Zend/zend_ini_parser.y, version=old, start_line=125, end_line=140)` →

```
Zend/zend_ini_parser.y lines 125-140 of 404
  125| /* {{{ zend_ini_get_constant()
  126| */
  127| static void zend_ini_get_constant(zval *result, zval *name)
  128| {
  129| 	zval *c, tmp;
  130| 
  131| 	/* If name contains ':' it is not a constant. Bug #26893. */
  132| 	if (!memchr(Z_STRVAL_P(name), ':', Z_STRLEN_P(name))
  133| 		   	&& (c = zend_get_constant(Z_STR_P(name))) != 0) {
  134| 		if (Z_TYPE_P(c) != IS_STRING) {
  135| 			ZVAL_COPY_VALUE(&tmp, c);
  136| 			if (Z_OPT_CONSTANT(tmp)) {
  137| 				zval_update_constant_ex(&tmp, 1, NULL);
  138| 			}
  139| 			zval_opt_copy_ctor(&tmp);
  140| 			convert_to_string(&tmp);
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 4  _(tok 74009+604, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "zend_update_class_constants", "file": "Zend/zend_API.c"}, {"function": "zend_ast_evaluate", "file": "Zend/zend_ast.c"}, {"function": "add_class_vars", "file": "Zend/zend_builtin_functions.c"}, {"function": "zend_get_constant_ex", "file": "Zend/zend_constants.c"}, {"function": "is_null_constant", "file": "Zend/zend_execute.c"}, {"function": "zval_update_constant_ex", "file": "Zend/zend_execute_API.c"}, {"function": "zval_update_constant", "file": "Zend/zend_execute_API.c"}, {"function": "zend_ini_get_constant", "file": "Zend/zend_ini_parser.y"}, {"function": "<UNRESOLVED: enclosing handlers for zend_vm_def.h lines 4694, 5093, 7204, 8007>", "file": "Zend/zend_vm_def.h"}, {"function": "<UNRESOLVED: enclosing handlers for zend_vm_execute.h lines 2295, 5646, 6142, 18996, 28404, 40179>", "file": "Zend/zend_vm_execute.h"}, {"function": "<UNRESOLVED: enclosing functions for ext/reflection/php_reflection.c lines 459, 715, 1934, 2896, 3968, 4624, 4672>", "file": "ext/reflection/php_reflection.c"}, {"function": "<UNRESOLVED: enclosing function for ext/standard/basic_functions.c line 3846>", "file": "ext/standard/basic_functions.c"}], "confidence_overall": "low"}`

**Score (self):** `{"n_pred": 12, "n_truth": 12, "tp": 5, "precision": 0.4166666666666667, "recall": 0.4166666666666667, "f1": 0.4166666666666667}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1392+84, stop=tool_use)_

**Reasoning:** I'm starting by pulling every reference to zval_update_constant_ex with find_references.



- `find_references(name=zval_update_constant_ex)` →

```
29 references
zval_update_constant_ex 1133 Zend/zend_API.c  					if (UNEXPECTED(zval_update_constant_ex(val, 1, class_type) != SUCCESS)) {
zval_update_constant_ex 1151 Zend/zend_API.c  							if (UNEXPECTED(zval_update_constant_ex(val, 1, NULL) != SUCCESS)) {
zval_update_constant_ex  262 Zend/zend_ast.c  					if (UNEXPECTED(zval_update_constant_ex(zv, 1, scope) != SUCCESS)) {
zval_update_constant_ex  271 Zend/zend_ast.c  					if (UNEXPECTED(zval_update_constant_ex(result, 1, scope) != SUCCESS)) {
zval_update_constant_ex 1183 Zend/zend_builtin_functions.c 			if (UNEXPECTED(zval_update_constant_ex(prop, 0, NULL) != SUCCESS)) {
zval_update_constant_ex  397 Zend/zend_constants.c 			if (UNEXPECTED(zval_update_constant_ex(ret_constant, 1, ce) != SUCCESS)) {
zval_update_constant_ex  654 Zend/zend_execute.c 		if (UNEXPECTED(zval_update_constant_ex(&constant, 0, NULL) != SUCCESS)) {
zval_update_constant_ex  126 Zend/zend_execute.h ZEND_API int zval_update_constant_ex(zval *pp, zend_bool inline_change, zend_class_entry *scope);
zval_update_constant_ex  638 Zend/zend_execute_API.c 				if (UNEXPECTED(zval_update_constant_ex(p, 1, NULL) != SUCCESS)) {
zval_update_constant_ex  662 Zend/zend_execute_API.c 	return zval_update_constant_ex(pp, inline_change, NULL);
zval_update_constant_ex  137 Zend/zend_ini_parser.y 				zval_update_constant_ex(&tmp, 1, NULL);
zval_update_constant_ex 4694 Zend/zend_vm_def.h 			if (UNEXPECTED(zval_update_constant_ex(param, 0, NULL) != SUCCESS)) {
zval_update_constant_ex 5093 Zend/zend_vm_def.h 				zval_update_constant_ex(value, 1, NULL);
zval_update_constant_ex 7204 Zend/zend_vm_def.h 		if (UNEXPECTED(zval_update_constant_ex(&c.value, 0, NULL) != SUCCESS)) {
zval_update_constant_ex 8007 Zend/zend_vm_def.h 			if (UNEXPECTED(zval_update_constant_ex(value, 1, NULL) != SUCCESS)) {
zval_update_constant_ex 2295 Zend/zend_vm_execute.h 			if (UNEXPECTED(zval_update_constant_ex(param, 0, NULL) != SUCCESS)) {
zval_update_constant_ex 5646 Zend/zend_vm_execute.h 				zval_update_constant_ex(value, 1, NULL);
zval_update_constant_ex 6142 Zend/zend_vm_execute.h 		if (UNEXPECTED(zval_update_constant_ex(&c.value, 0, NULL) != SUCCESS)) {
zval_update_constant_ex 18996 Zend/zend_vm_execute.h 				zval_update_constant_ex(value, 1, NULL);
zval_update_constant_ex 28404 Zend/zend_vm_execute.h 				zval_update_constant_ex(value, 1, NULL);
zval_update_constant_ex 40179 Zend/zend_vm_execute.h 			if (UNEXPECTED(zval_update_constant_ex(value, 1, NULL) != SUCCESS)) {
zval_update_constant_ex  459 ext/reflection/php_reflection.c 			zval_update_constant_ex(&c->value, 1, NULL);
zval_update_constant_ex  715 ext/reflection/php_reflection.c 			zval_update_constant_ex(&zv, 1, NULL);
zval_update_constant_ex 1934 ext/reflection/php_reflection.c 			if (UNEXPECTED(zval_update_constant_ex(val, 1, fptr->common.scope) != SUCCESS)) {
zval_update_constant_ex 2896 ext/reflection/php_reflection.c 		zval_update_constant_ex(return_value, 0, NULL);
zval_update_constant_ex 3968 ext/reflection/php_reflection.c 			if (UNEXPECTED(zval_update_constant_ex(&prop_copy, 1, NULL) != SUCCESS)) {
zval_update_constant_ex 4624 ext/reflection/php_reflection.c 		if (UNEXPECTED(zval_update_constant_ex(&c->value, 1, ce) != SUCCESS)) {
zval_update_constant_ex 4672 ext/reflection/php_reflection.c 		if (UNEXPECTED(zval_update_constant_ex(&c->value, 1, ce) != SUCCESS)) {
zval_update_constant_ex 3846 ext/standard/basic_functions.c 			if (UNEXPECTED(zval_update_constant_ex(return_value, 1, NULL) != SUCCESS)) {
```

### Turn 2  _(tok 3387+1347, stop=tool_use)_

**Reasoning:** I need the enclosing function for each of these locations, so I'll read the files to find them. The list covers zend_API.c at lines 1133 and 1151, zend_ast.c at 262 and 271, zend_builtin_functions.c at 1183, zend_constants.c at 397, zend_execute.c at 654, and zend_execute_API.c, with the zend_execute.h prototype at 126 left out.

Now I'm working through the remaining locations in the list, pulling in zend_execute_API.c around 662 and the zend_ini_parser.y entry at 137, then a long run of zend_vm_def.h and zend_vm_execute.h offsets along with php_reflection.c and basic_functions.c. I want the enclosing function for each one, so I'll read ranges before every line and maybe grep as well for macros or function pointers that the first pass could miss.



- `read_file(path=Zend/zend_API.c, version=old, start_line=1080, end_line=1135)` →

```
Zend/zend_API.c lines 1080-1135 of 4199
 1080| }
 1081| /* }}} */
 1082| 
 1083| ZEND_API int zend_update_class_constants(zend_class_entry *class_type) /* {{{ */
 1084| {
 1085| 	if (!(class_type->ce_flags & ZEND_ACC_CONSTANTS_UPDATED)) {
 1086| 		class_type->ce_flags |= ZEND_ACC_CONSTANTS_UPDATED;
 1087| 
 1088| 		if (class_type->parent) {
 1089| 			if (UNEXPECTED(zend_update_class_constants(class_type->parent) != SUCCESS)) {
 1090| 				return FAILURE;
 1091| 			}
 1092| 		}
 1093| 
 1094| 		if (!CE_STATIC_MEMBERS(class_type) && class_type->default_static_members_count) {
 1095| 			/* initialize static members of internal class */
 1096| 			int i;
 1097| 			zval *p;
 1098| 
 1099| #if ZTS
 1100| 			CG(static_members_table)[(zend_intptr_t)(class_type->static_members_table)] = emalloc(sizeof(zval) * class_type->default_static_members_count);
 1101| #else
 1102| 			class_type->static_members_table = emalloc(sizeof(zval) * class_type->default_static_members_count);
 1103| #endif
 1104| 			for (i = 0; i < class_type->default_static_members_count; i++) {
 1105| 				p = &class_type->default_static_members_table[i];
 1106| 				if (Z_ISREF_P(p) &&
 1107| 					class_type->parent &&
 1108| 					i < class_type->parent->default_static_members_count &&
 1109| 					p == &class_type->parent->default_static_members_table[i] &&
 1110| 					Z_TYPE(CE_STATIC_MEMBERS(class_type->parent)[i]) != IS_UNDEF
 1111| 				) {
 1112| 					zval *q = &CE_STATIC_MEMBERS(class_type->parent)[i];
 1113| 
 1114| 					ZVAL_NEW_REF(q, q);
 1115| 					ZVAL_COPY_VALUE(&CE_STATIC_MEMBERS(class_type)[i], q);
 1116| 					Z_ADDREF_P(q);
 1117| 				} else {
 1118| 					ZVAL_DUP(&CE_STATIC_MEMBERS(class_type)[i], p);
 1119| 				}
 1120| 			}
 1121| 		} else {
 1122| 			zend_class_entry **scope = EG(current_execute_data) ? &EG(scope) : &CG(active_class_entry);
 1123| 			zend_class_entry *old_scope = *scope;
 1124| 			zend_class_entry *ce;
 1125| 			zend_class_constant *c;
 1126| 			zval *val;
 1127| 			zend_property_info *prop_info;
 1128| 
 1129| 			*scope = class_type;
 1130| 			ZEND_HASH_FOREACH_PTR(&class_type->constants_table, c) {
 1131| 				val = &c->value;
 1132| 				if (Z_CONSTANT_P(val)) {
 1133| 					if (UNEXPECTED(zval_update_constant_ex(val, 1, class_type) != SUCCESS)) {
 1134| 						return FAILURE;
 1135| 					}
```

- `read_file(path=Zend/zend_ast.c, version=old, start_line=230, end_line=275)` →

```
Zend/zend_ast.c lines 230-275 of 1707
  230| 			break;
  231| 		case ZEND_AST_GREATER:
  232| 		case ZEND_AST_GREATER_EQUAL:
  233| 			if (UNEXPECTED(zend_ast_evaluate(&op1, ast->child[0], scope) != SUCCESS)) {
  234| 				ret = FAILURE;
  235| 			} else if (UNEXPECTED(zend_ast_evaluate(&op2, ast->child[1], scope) != SUCCESS)) {
  236| 				zval_dtor(&op1);
  237| 				ret = FAILURE;
  238| 			} else {
  239| 				/* op1 > op2 is the same as op2 < op1 */
  240| 				binary_op_type op = ast->kind == ZEND_AST_GREATER
  241| 					? is_smaller_function : is_smaller_or_equal_function;
  242| 				ret = op(result, &op2, &op1);
  243| 				zval_dtor(&op1);
  244| 				zval_dtor(&op2);
  245| 			}
  246| 			break;
  247| 		case ZEND_AST_UNARY_OP:
  248| 			if (UNEXPECTED(zend_ast_evaluate(&op1, ast->child[0], scope) != SUCCESS)) {
  249| 				ret = FAILURE;
  250| 			} else {
  251| 				unary_op_type op = get_unary_op(ast->attr);
  252| 				ret = op(result, &op1);
  253| 				zval_dtor(&op1);
  254| 			}
  255| 			break;
  256| 		case ZEND_AST_ZVAL:
  257| 		{
  258| 			zval *zv = zend_ast_get_zval(ast);
  259| 			if (scope) {
  260| 				/* class constants may be updated in-place */
  261| 				if (Z_OPT_CONSTANT_P(zv)) {
  262| 					if (UNEXPECTED(zval_update_constant_ex(zv, 1, scope) != SUCCESS)) {
  263| 						ret = FAILURE;
  264| 						break;
  265| 					}
  266| 				}
  267| 				ZVAL_DUP(result, zv);
  268| 			} else {
  269| 				ZVAL_DUP(result, zv);
  270| 				if (Z_OPT_CONSTANT_P(result)) {
  271| 					if (UNEXPECTED(zval_update_constant_ex(result, 1, scope) != SUCCESS)) {
  272| 						ret = FAILURE;
  273| 						break;
  274| 					}
  275| 				}
```

- `read_file(path=Zend/zend_builtin_functions.c, version=old, start_line=1150, end_line=1185)` →

```
Zend/zend_builtin_functions.c lines 1150-1185 of 2853
 1150| 
 1151| 	ZEND_HASH_FOREACH_STR_KEY_PTR(&ce->properties_info, key, prop_info) {
 1152| 		if (((prop_info->flags & ZEND_ACC_SHADOW) &&
 1153| 		     prop_info->ce != EG(scope)) ||
 1154| 		    ((prop_info->flags & ZEND_ACC_PROTECTED) &&
 1155| 		     !zend_check_protected(prop_info->ce, EG(scope))) ||
 1156| 		    ((prop_info->flags & ZEND_ACC_PRIVATE) &&
 1157| 		      ce != EG(scope) &&
 1158| 			  prop_info->ce != EG(scope))) {
 1159| 			continue;
 1160| 		}
 1161| 		prop = NULL;
 1162| 		if (statics && (prop_info->flags & ZEND_ACC_STATIC) != 0) {
 1163| 			prop = &ce->default_static_members_table[prop_info->offset];
 1164| 		} else if (!statics && (prop_info->flags & ZEND_ACC_STATIC) == 0) {
 1165| 			prop = &ce->default_properties_table[OBJ_PROP_TO_NUM(prop_info->offset)];
 1166| 		}
 1167| 		if (!prop || Z_TYPE_P(prop) == IS_UNDEF) {
 1168| 			continue;
 1169| 		}
 1170| 
 1171| 		/* copy: enforce read only access */
 1172| 		ZVAL_DEREF(prop);
 1173| 		if (UNEXPECTED(Z_COPYABLE_P(prop))) {
 1174| 			ZVAL_DUP(&prop_copy, prop);
 1175| 			prop = &prop_copy;
 1176| 		} else {
 1177| 			Z_TRY_ADDREF_P(prop);
 1178| 		}
 1179| 
 1180| 		/* this is necessary to make it able to work with default array
 1181| 		 * properties, returned to user */
 1182| 		if (Z_OPT_CONSTANT_P(prop)) {
 1183| 			if (UNEXPECTED(zval_update_constant_ex(prop, 0, NULL) != SUCCESS)) {
 1184| 				return;
 1185| 			}
```

- `read_file(path=Zend/zend_constants.c, version=old, start_line=370, end_line=400)` →

```
Zend/zend_constants.c lines 370-400 of 547
  370| 		} else {
  371| 			ce = zend_fetch_class(class_name, flags);
  372| 		}
  373| 		free_alloca(lcname, use_heap);
  374| 		if (ce) {
  375| 			zend_class_constant *c = zend_hash_find_ptr(&ce->constants_table, constant_name);
  376| 			if (c == NULL) {
  377| 				if ((flags & ZEND_FETCH_CLASS_SILENT) == 0) {
  378| 					zend_throw_error(NULL, "Undefined class constant '%s::%s'", ZSTR_VAL(class_name), ZSTR_VAL(constant_name));
  379| 					zend_string_release(class_name);
  380| 					zend_string_free(constant_name);
  381| 					return NULL;
  382| 				}
  383| 				ret_constant = NULL;
  384| 			} else {
  385| 				if (!zend_verify_const_access(c, scope)) {
  386| 					zend_throw_error(NULL, "Cannot access %s const %s::%s", zend_visibility_string(Z_ACCESS_FLAGS(c->value)), ZSTR_VAL(class_name), ZSTR_VAL(constant_name));
  387| 					zend_string_release(class_name);
  388| 					zend_string_free(constant_name);
  389| 					return NULL;
  390| 				}
  391| 				ret_constant = &c->value;
  392| 			}
  393| 		}
  394| 		zend_string_release(class_name);
  395| 		zend_string_free(constant_name);
  396| 		if (ret_constant && Z_CONSTANT_P(ret_constant)) {
  397| 			if (UNEXPECTED(zval_update_constant_ex(ret_constant, 1, ce) != SUCCESS)) {
  398| 				return NULL;
  399| 			}
  400| 		}
```

- `read_file(path=Zend/zend_execute.c, version=old, start_line=620, end_line=660)` →

```
Zend/zend_execute.c lines 620-660 of 3176
  620| static ZEND_COLD void zend_verify_arg_error(const zend_function *zf, uint32_t arg_num, const char *need_msg, const char *need_kind, const char *given_msg, const char *given_kind, zval *arg)
  621| {
  622| 	zend_execute_data *ptr = EG(current_execute_data)->prev_execute_data;
  623| 	const char *fname = ZSTR_VAL(zf->common.function_name);
  624| 	const char *fsep;
  625| 	const char *fclass;
  626| 
  627| 	if (zf->common.scope) {
  628| 		fsep =  "::";
  629| 		fclass = ZSTR_VAL(zf->common.scope->name);
  630| 	} else {
  631| 		fsep =  "";
  632| 		fclass = "";
  633| 	}
  634| 
  635| 	if (zf->common.type == ZEND_USER_FUNCTION) {
  636| 		if (ptr && ptr->func && ZEND_USER_CODE(ptr->func->common.type)) {
  637| 			zend_type_error("Argument %d passed to %s%s%s() must %s%s, %s%s given, called in %s on line %d",
  638| 					arg_num, fclass, fsep, fname, need_msg, need_kind, given_msg, given_kind,
  639| 					ZSTR_VAL(ptr->func->op_array.filename), ptr->opline->lineno);
  640| 		} else {
  641| 			zend_type_error("Argument %d passed to %s%s%s() must %s%s, %s%s given", arg_num, fclass, fsep, fname, need_msg, need_kind, given_msg, given_kind);
  642| 		}
  643| 	} else {
  644| 		zend_type_error("Argument %d passed to %s%s%s() must %s%s, %s%s given", arg_num, fclass, fsep, fname, need_msg, need_kind, given_msg, given_kind);
  645| 	}
  646| }
  647| 
  648| static int is_null_constant(zval *default_value)
  649| {
  650| 	if (Z_CONSTANT_P(default_value)) {
  651| 		zval constant;
  652| 
  653| 		ZVAL_COPY_VALUE(&constant, default_value);
  654| 		if (UNEXPECTED(zval_update_constant_ex(&constant, 0, NULL) != SUCCESS)) {
  655| 			return 0;
  656| 		}
  657| 		if (Z_TYPE(constant) == IS_NULL) {
  658| 			return 1;
  659| 		}
  660| 		zval_dtor(&constant);
```

- `read_file(path=Zend/zend_execute_API.c, version=old, start_line=610, end_line=665)` →

```
Zend/zend_execute_API.c lines 610-665 of 1722
  610| 						zend_throw_error(NULL, "Undefined constant '%s'", ZSTR_VAL(save) + 1);
  611| 					} else {
  612| 						zend_throw_error(NULL, "Undefined constant '%s'", ZSTR_VAL(save));
  613| 					}
  614| 					if (inline_change) {
  615| 						zend_string_release(save);
  616| 					}
  617| 					RESET_CONSTANT_VISITED(p);
  618| 					return FAILURE;
  619| 				} else {
  620| 					zend_error(E_NOTICE, "Use of undefined constant %s - assumed '%s'",  actual,  actual);
  621| 					if (!inline_change) {
  622| 						ZVAL_STRINGL(p, actual, actual_len);
  623| 					} else {
  624| 						Z_TYPE_INFO_P(p) = Z_REFCOUNTED_P(p) ?
  625| 							IS_STRING_EX : IS_INTERNED_STRING_EX;
  626| 						if (save && ZSTR_VAL(save) != actual) {
  627| 							zend_string_release(save);
  628| 						}
  629| 					}
  630| 				}
  631| 			}
  632| 		} else {
  633| 			if (inline_change) {
  634| 				zend_string_release(Z_STR_P(p));
  635| 			}
  636| 			ZVAL_COPY_VALUE(p, const_value);
  637| 			if (Z_OPT_CONSTANT_P(p)) {
  638| 				if (UNEXPECTED(zval_update_constant_ex(p, 1, NULL) != SUCCESS)) {
  639| 					RESET_CONSTANT_VISITED(p);
  640| 					return FAILURE;
  641| 				}
  642| 			}
  643| 			zval_opt_copy_ctor(p);
  644| 		}
  645| 	} else if (Z_TYPE_P(p) == IS_CONSTANT_AST) {
  646| 		zval tmp;
  647| 
  648| 		if (UNEXPECTED(zend_ast_evaluate(&tmp, Z_ASTVAL_P(p), scope) != SUCCESS)) {
  649| 			return FAILURE;
  650| 		}
  651| 		if (inline_change) {
  652| 			zval_ptr_dtor(p);
  653| 		}
  654| 		ZVAL_COPY_VALUE(p, &tmp);
  655| 	}
  656| 	return SUCCESS;
  657| }
  658| /* }}} */
  659| 
  660| ZEND_API int zval_update_constant(zval *pp, zend_bool inline_change) /* {{{ */
  661| {
  662| 	return zval_update_constant_ex(pp, inline_change, NULL);
  663| }
  664| /* }}} */
  665| 
```

- `read_file(path=Zend/zend_ini_parser.y, version=old, start_line=120, end_line=140)` →

```
Zend/zend_ini_parser.y lines 120-140 of 404
  120| 	ZVAL_NEW_STR(result, zend_string_extend(Z_STR_P(op1), length, 1));
  121| 	memcpy(Z_STRVAL_P(result) + op1_len, Z_STRVAL_P(op2), Z_STRLEN_P(op2) + 1);
  122| }
  123| /* }}} */
  124| 
  125| /* {{{ zend_ini_get_constant()
  126| */
  127| static void zend_ini_get_constant(zval *result, zval *name)
  128| {
  129| 	zval *c, tmp;
  130| 
  131| 	/* If name contains ':' it is not a constant. Bug #26893. */
  132| 	if (!memchr(Z_STRVAL_P(name), ':', Z_STRLEN_P(name))
  133| 		   	&& (c = zend_get_constant(Z_STR_P(name))) != 0) {
  134| 		if (Z_TYPE_P(c) != IS_STRING) {
  135| 			ZVAL_COPY_VALUE(&tmp, c);
  136| 			if (Z_OPT_CONSTANT(tmp)) {
  137| 				zval_update_constant_ex(&tmp, 1, NULL);
  138| 			}
  139| 			zval_opt_copy_ctor(&tmp);
  140| 			convert_to_string(&tmp);
```

### Turn 3  _(tok 11077+1050, stop=tool_use)_

**Reasoning:** I'm checking which function encloses lines 1133 and 1151 in zend_API.c, and it looks like zend_update_class_constants, which starts at line 1083. I still need to confirm that no other function boundary falls between 1135 and 1151.

I'm going through the rest of the zend_API.c and related call sites, and I'll check the remaining enclosing functions in the other files: zend_ast.c around 262 and 271, zend_builtin_functions.c at 1183, zend_constants.c at 397, zend_execute.c at 654, zend_execute_API.c at 638 and 662, and zend_ini_parser.y at 137.



- `read_file(path=Zend/zend_ast.c, version=old, start_line=180, end_line=200)` →

```
Zend/zend_ast.c lines 180-200 of 1707
  180| static int zend_ast_add_array_element(zval *result, zval *offset, zval *expr)
  181| {
  182| 	switch (Z_TYPE_P(offset)) {
  183| 		case IS_UNDEF:
  184| 			zend_hash_next_index_insert(Z_ARRVAL_P(result), expr);
  185| 			break;
  186| 		case IS_STRING:
  187| 			zend_symtable_update(Z_ARRVAL_P(result), Z_STR_P(offset), expr);
  188| 			zval_dtor(offset);
  189| 			break;
  190| 		case IS_NULL:
  191| 			zend_symtable_update(Z_ARRVAL_P(result), ZSTR_EMPTY_ALLOC(), expr);
  192| 			break;
  193| 		case IS_LONG:
  194| 			zend_hash_index_update(Z_ARRVAL_P(result), Z_LVAL_P(offset), expr);
  195| 			break;
  196| 		case IS_FALSE:
  197| 			zend_hash_index_update(Z_ARRVAL_P(result), 0, expr);
  198| 			break;
  199| 		case IS_TRUE:
  200| 			zend_hash_index_update(Z_ARRVAL_P(result), 1, expr);
```

- `read_file(path=Zend/zend_builtin_functions.c, version=old, start_line=1120, end_line=1150)` →

```
Zend/zend_builtin_functions.c lines 1120-1150 of 2853
 1120| 			}
 1121| 		}
 1122| 	}
 1123| 
 1124| 	RETURN_BOOL(retval);
 1125| }
 1126| /* }}} */
 1127| 
 1128| /* {{{ proto bool is_subclass_of(mixed object_or_string, string class_name [, bool allow_string])
 1129|    Returns true if the object has this class as one of its parents */
 1130| ZEND_FUNCTION(is_subclass_of)
 1131| {
 1132| 	is_a_impl(INTERNAL_FUNCTION_PARAM_PASSTHRU, 1);
 1133| }
 1134| /* }}} */
 1135| 
 1136| /* {{{ proto bool is_a(mixed object_or_string, string class_name [, bool allow_string])
 1137|    Returns true if the first argument is an object and is this class or has this class as one of its parents, */
 1138| ZEND_FUNCTION(is_a)
 1139| {
 1140| 	is_a_impl(INTERNAL_FUNCTION_PARAM_PASSTHRU, 0);
 1141| }
 1142| /* }}} */
 1143| 
 1144| /* {{{ add_class_vars */
 1145| static void add_class_vars(zend_class_entry *ce, int statics, zval *return_value)
 1146| {
 1147| 	zend_property_info *prop_info;
 1148| 	zval *prop, prop_copy;
 1149| 	zend_string *key;
 1150| 
```

- `read_file(path=Zend/zend_execute_API.c, version=old, start_line=560, end_line=600)` →

```
Zend/zend_execute_API.c lines 560-600 of 1722
  560| 		zend_throw_error(NULL, "Cannot declare self-referencing constant '%s'", Z_STRVAL_P(p));
  561| 		return FAILURE;
  562| 	} else if (Z_TYPE_P(p) == IS_CONSTANT) {
  563| 
  564| 		SEPARATE_ZVAL_NOREF(p);
  565| 		MARK_CONSTANT_VISITED(p);
  566| 		if (Z_CONST_FLAGS_P(p) & IS_CONSTANT_CLASS) {
  567| 			ZEND_ASSERT(EG(current_execute_data));
  568| 			if (inline_change) {
  569| 				zend_string_release(Z_STR_P(p));
  570| 			}
  571| 			if (EG(scope) && EG(scope)->name) {
  572| 				ZVAL_STR_COPY(p, EG(scope)->name);
  573| 			} else {
  574| 				ZVAL_EMPTY_STRING(p);
  575| 			}
  576| 		} else if (UNEXPECTED((const_value = zend_get_constant_ex(Z_STR_P(p), scope, Z_CONST_FLAGS_P(p))) == NULL)) {
  577| 			char *actual = Z_STRVAL_P(p);
  578| 
  579| 			if (UNEXPECTED(EG(exception))) {
  580| 				RESET_CONSTANT_VISITED(p);
  581| 				return FAILURE;
  582| 			} else if ((colon = (char*)zend_memrchr(Z_STRVAL_P(p), ':', Z_STRLEN_P(p)))) {
  583| 				zend_throw_error(NULL, "Undefined class constant '%s'", Z_STRVAL_P(p));
  584| 				RESET_CONSTANT_VISITED(p);
  585| 				return FAILURE;
  586| 			} else {
  587| 				zend_string *save = Z_STR_P(p);
  588| 				char *slash;
  589| 				size_t actual_len = Z_STRLEN_P(p);
  590| 				if ((Z_CONST_FLAGS_P(p) & IS_CONSTANT_UNQUALIFIED) && (slash = (char *)zend_memrchr(actual, '\\', actual_len))) {
  591| 					actual = slash + 1;
  592| 					actual_len -= (actual - Z_STRVAL_P(p));
  593| 					if (inline_change) {
  594| 						zend_string *s = zend_string_init(actual, actual_len, 0);
  595| 						Z_STR_P(p) = s;
  596| 						Z_TYPE_FLAGS_P(p) = IS_TYPE_REFCOUNTED | IS_TYPE_COPYABLE;
  597| 					}
  598| 				}
  599| 				if (actual[0] == '\\') {
  600| 					if (inline_change) {
```

- `read_file(path=Zend/zend_API.c, version=old, start_line=1135, end_line=1160)` →

```
Zend/zend_API.c lines 1135-1160 of 4199
 1135| 					}
 1136| 				}
 1137| 			} ZEND_HASH_FOREACH_END();
 1138| 
 1139| 			ce = class_type;
 1140| 			while (ce) {
 1141| 				ZEND_HASH_FOREACH_PTR(&ce->properties_info, prop_info) {
 1142| 					if (prop_info->ce == ce) {
 1143| 						if (prop_info->flags & ZEND_ACC_STATIC) {
 1144| 							val = CE_STATIC_MEMBERS(class_type) + prop_info->offset;
 1145| 						} else {
 1146| 							val = (zval*)((char*)class_type->default_properties_table + prop_info->offset - OBJ_PROP_TO_OFFSET(0));
 1147| 						}
 1148| 						ZVAL_DEREF(val);
 1149| 						if (Z_CONSTANT_P(val)) {
 1150| 							*scope = ce;
 1151| 							if (UNEXPECTED(zval_update_constant_ex(val, 1, NULL) != SUCCESS)) {
 1152| 								return FAILURE;
 1153| 							}
 1154| 						}
 1155| 					}
 1156| 				} ZEND_HASH_FOREACH_END();
 1157| 				ce = ce->parent;
 1158| 			}
 1159| 
 1160| 			*scope = old_scope;
```

- `read_file(path=Zend/zend_constants.c, version=old, start_line=340, end_line=370)` →

```
Zend/zend_constants.c lines 340-370 of 547
  340| 			} else {
  341| 				scope = CG(active_class_entry);
  342| 			}
  343| 		}
  344| 
  345| 		if (class_name_len == sizeof("self")-1 &&
  346| 		    !memcmp(lcname, "self", sizeof("self")-1)) {
  347| 			if (UNEXPECTED(!scope)) {
  348| 				zend_throw_error(NULL, "Cannot access self:: when no class scope is active");
  349| 				return NULL;
  350| 			}
  351| 			ce = scope;
  352| 		} else if (class_name_len == sizeof("parent")-1 &&
  353| 		           !memcmp(lcname, "parent", sizeof("parent")-1)) {
  354| 			if (UNEXPECTED(!scope)) {
  355| 				zend_throw_error(NULL, "Cannot access parent:: when no class scope is active");
  356| 				return NULL;
  357| 			} else if (UNEXPECTED(!scope->parent)) {
  358| 				zend_throw_error(NULL, "Cannot access parent:: when current class scope has no parent");
  359| 				return NULL;
  360| 			} else {
  361| 				ce = scope->parent;
  362| 			}
  363| 		} else if (class_name_len == sizeof("static")-1 &&
  364| 		           !memcmp(lcname, "static", sizeof("static")-1)) {
  365| 			ce = zend_get_called_scope(EG(current_execute_data));
  366| 			if (UNEXPECTED(!ce)) {
  367| 				zend_throw_error(NULL, "Cannot access static:: when no class scope is active");
  368| 				return NULL;
  369| 			}
  370| 		} else {
```

### Turn 4  _(tok 15483+630, stop=tool_use)_

**Reasoning:** I need the function names for both files. My guess is that line 262 in zend_ast.c falls inside zend_ast_evaluate and line 397 in zend_constants.c falls inside zend_get_class_constant_ex, but I'll confirm that with a grep for function definitions in each file.



- `grep(pattern=^[A-Za-z_].*\(.*\)\s*$|^[A-Za-z_][A-Za-z_ *]*\(, version=old, path_glob=Zend/zend_ast.c)` →

```
39 matches
Zend/zend_ast.c:31:static inline void *zend_ast_alloc(size_t size) {
Zend/zend_ast.c:35:static inline void *zend_ast_realloc(void *old, size_t old_size, size_t new_size) {
Zend/zend_ast.c:41:static inline size_t zend_ast_size(uint32_t children) {
Zend/zend_ast.c:45:static inline size_t zend_ast_list_size(uint32_t children) {
Zend/zend_ast.c:49:ZEND_API zend_ast *zend_ast_create_znode(znode *node) {
Zend/zend_ast.c:60:ZEND_API zend_ast *zend_ast_create_zval_ex(zval *zv, zend_ast_attr attr) {
Zend/zend_ast.c:71:ZEND_API zend_ast *zend_ast_create_decl(
Zend/zend_ast.c:94:static zend_ast *zend_ast_create_from_va_list(zend_ast_kind kind, zend_ast_attr attr, va_list va) {
Zend/zend_ast.c:120:ZEND_API zend_ast *zend_ast_create_ex(zend_ast_kind kind, zend_ast_attr attr, ...) {
Zend/zend_ast.c:131:ZEND_API zend_ast *zend_ast_create(zend_ast_kind kind, ...) {
Zend/zend_ast.c:142:ZEND_API zend_ast *zend_ast_create_list(uint32_t init_children, zend_ast_kind kind, ...) {
Zend/zend_ast.c:166:static inline zend_bool is_power_of_two(uint32_t n) {
Zend/zend_ast.c:170:ZEND_API zend_ast *zend_ast_list_add(zend_ast *ast, zend_ast *op) {
Zend/zend_ast.c:180:static int zend_ast_add_array_element(zval *result, zval *offset, zval *expr)
Zend/zend_ast.c:212:ZEND_API int zend_ast_evaluate(zval *result, zend_ast *ast, zend_class_entry *scope)
Zend/zend_ast.c:439:ZEND_API zend_ast *zend_ast_copy(zend_ast *ast)
Zend/zend_ast.c:472:static void zend_ast_destroy_ex(zend_ast *ast, zend_bool free) {
Zend/zend_ast.c:522:ZEND_API void zend_ast_destroy(zend_ast *ast) {
Zend/zend_ast.c:525:ZEND_API void zend_ast_destroy_and_free(zend_ast *ast) {
Zend/zend_ast.c:529:ZEND_API void zend_ast_apply(zend_ast *ast, zend_ast_apply_func fn) {
Zend/zend_ast.c:579:static void zend_ast_export_ex(smart_str *str, zend_ast *ast, int priority, int indent);
Zend/zend_ast.c:581:static void zend_ast_export_str(smart_str *str, zend_string *s)
Zend/zend_ast.c:596:static void zend_ast_export_qstr(smart_str *str, char quote, zend_string *s)
Zend/zend_ast.c:641:static void zend_ast_export_indent(smart_str *str, int indent)
Zend/zend_ast.c:649:static void zend_ast_export_name(smart_str *str, zend_ast *ast, int priority, int indent)
Zend/zend_ast.c:662:static void zend_ast_export_ns_name(smart_str *str, zend_ast *ast, int priority, int indent)
Zend/zend_ast.c:680:static int zend_ast_valid_var_char(char ch)
Zend/zend_ast.c:693:static int zend_ast_valid_var_name(const char *s, size_t len)
Zend/zend_ast.c:719:static void zend_ast_export_var(smart_str *str, zend_ast *ast, int priority, int indent)
Zend/zend_ast.c:737:static void zend_ast_export_list(smart_str *str, zend_ast_list *list, int separator, int priority, int indent)
Zend/zend_ast.c:750:static void zend_ast_export_encaps_list(smart_str *str, char quote, zend_ast_list *list, int indent)
Zend/zend_ast.c:779:static void zend_ast_export_name_list(smart_str *str, zend_ast_list *list, int indent)
Zend/zend_ast.c:792:static void zend_ast_export_var_list(smart_str *str, zend_ast_list *list, int indent)
Zend/zend_ast.c:809:static void zend_ast_export_stmt(smart_str *str, zend_ast *ast, int indent)
Zend/zend_ast.c:851:static void zend_ast_export_if_stmt(smart_str *str, zend_ast_list *list, int indent)
Zend/zend_ast.c:888:static void zend_ast_export_zval(smart_str *str, zval *zv, int priority, int indent)
Zend/zend_ast.c:950:static void zend_ast_export_class_no_header(smart_str *str, zend_ast_decl *decl, int indent) {
Zend/zend_ast.c:1007:static void zend_ast_export_ex(smart_str *str, zend_ast *ast, int priority, int indent)
Zend/zend_ast.c:1697:ZEND_API zend_string *zend_ast_export(const char *prefix, zend_ast *ast, const char *suffix)
```

- `grep(pattern=^[A-Za-z_].*\(, version=old, path_glob=Zend/zend_constants.c)` →

```
25 matches
Zend/zend_constants.c:31:void free_zend_constant(zval *zv)
Zend/zend_constants.c:47:static void copy_zend_constant(zval *zv)
Zend/zend_constants.c:66:void zend_copy_constants(HashTable *target, HashTable *source)
Zend/zend_constants.c:72:static int clean_non_persistent_constant(zval *zv)
Zend/zend_constants.c:79:static int clean_non_persistent_constant_full(zval *zv)
Zend/zend_constants.c:86:static int clean_module_constant(zval *el, void *arg)
Zend/zend_constants.c:99:void clean_module_constants(int module_number)
Zend/zend_constants.c:105:int zend_startup_constants(void)
Zend/zend_constants.c:115:void zend_register_standard_constants(void)
Zend/zend_constants.c:148:int zend_shutdown_constants(void)
Zend/zend_constants.c:156:void clean_non_persistent_constants(void)
Zend/zend_constants.c:165:ZEND_API void zend_register_null_constant(const char *name, size_t name_len, int flags, int module_number)
Zend/zend_constants.c:176:ZEND_API void zend_register_bool_constant(const char *name, size_t name_len, zend_bool bval, int flags, int module_number)
Zend/zend_constants.c:187:ZEND_API void zend_register_long_constant(const char *name, size_t name_len, zend_long lval, int flags, int module_number)
Zend/zend_constants.c:199:ZEND_API void zend_register_double_constant(const char *name, size_t name_len, double dval, int flags, int module_number)
Zend/zend_constants.c:211:ZEND_API void zend_register_stringl_constant(const char *name, size_t name_len, char *strval, size_t strlen, int flags, int module_number)
Zend/zend_constants.c:223:ZEND_API void zend_register_string_constant(const char *name, size_t name_len, char *strval, int flags, int module_number)
Zend/zend_constants.c:228:static zend_constant *zend_get_special_constant(const char *name, size_t name_len)
Zend/zend_constants.c:254:ZEND_API int zend_verify_const_access(zend_class_constant *c, zend_class_entry *scope) /* {{{ */
Zend/zend_constants.c:267:ZEND_API zval *zend_get_constant_str(const char *name, size_t name_len)
Zend/zend_constants.c:288:ZEND_API zval *zend_get_constant(zend_string *name)
Zend/zend_constants.c:309:ZEND_API zval *zend_get_constant_ex(zend_string *cname, zend_class_entry *scope, uint32_t flags)
Zend/zend_constants.c:449:zend_constant *zend_quick_get_constant(const zval *key, uint32_t flags)
Zend/zend_constants.c:477:static void* zend_hash_add_constant(HashTable *ht, zend_string *key, zend_constant *c)
Zend/zend_constants.c:490:ZEND_API int zend_register_constant(zend_constant *c)
```

- `grep(pattern=^[A-Za-z_].*\(, version=old, path_glob=Zend/zend_builtin_functions.c)` →

```
205 matches (showing 60)
Zend/zend_builtin_functions.c:40:static ZEND_FUNCTION(zend_version);
Zend/zend_builtin_functions.c:41:static ZEND_FUNCTION(func_num_args);
Zend/zend_builtin_functions.c:42:static ZEND_FUNCTION(func_get_arg);
Zend/zend_builtin_functions.c:43:static ZEND_FUNCTION(func_get_args);
Zend/zend_builtin_functions.c:44:static ZEND_FUNCTION(strlen);
Zend/zend_builtin_functions.c:45:static ZEND_FUNCTION(strcmp);
Zend/zend_builtin_functions.c:46:static ZEND_FUNCTION(strncmp);
Zend/zend_builtin_functions.c:47:static ZEND_FUNCTION(strcasecmp);
Zend/zend_builtin_functions.c:48:static ZEND_FUNCTION(strncasecmp);
Zend/zend_builtin_functions.c:49:static ZEND_FUNCTION(each);
Zend/zend_builtin_functions.c:50:static ZEND_FUNCTION(error_reporting);
Zend/zend_builtin_functions.c:51:static ZEND_FUNCTION(define);
Zend/zend_builtin_functions.c:52:static ZEND_FUNCTION(defined);
Zend/zend_builtin_functions.c:53:static ZEND_FUNCTION(get_class);
Zend/zend_builtin_functions.c:54:static ZEND_FUNCTION(get_called_class);
Zend/zend_builtin_functions.c:55:static ZEND_FUNCTION(get_parent_class);
Zend/zend_builtin_functions.c:56:static ZEND_FUNCTION(method_exists);
Zend/zend_builtin_functions.c:57:static ZEND_FUNCTION(property_exists);
Zend/zend_builtin_functions.c:58:static ZEND_FUNCTION(class_exists);
Zend/zend_builtin_functions.c:59:static ZEND_FUNCTION(interface_exists);
Zend/zend_builtin_functions.c:60:static ZEND_FUNCTION(trait_exists);
Zend/zend_builtin_functions.c:61:static ZEND_FUNCTION(function_exists);
Zend/zend_builtin_functions.c:62:static ZEND_FUNCTION(class_alias);
Zend/zend_builtin_functions.c:64:static ZEND_FUNCTION(leak);
Zend/zend_builtin_functions.c:65:static ZEND_FUNCTION(leak_variable);
Zend/zend_builtin_functions.c:67:static ZEND_FUNCTION(crash);
Zend/zend_builtin_functions.c:70:static ZEND_FUNCTION(get_included_files);
Zend/zend_builtin_functions.c:71:static ZEND_FUNCTION(is_subclass_of);
Zend/zend_builtin_functions.c:72:static ZEND_FUNCTION(is_a);
Zend/zend_builtin_functions.c:73:static ZEND_FUNCTION(get_class_vars);
Zend/zend_builtin_functions.c:74:static ZEND_FUNCTION(get_object_vars);
Zend/zend_builtin_functions.c:75:static ZEND_FUNCTION(get_class_methods);
Zend/zend_builtin_functions.c:76:static ZEND_FUNCTION(trigger_error);
Zend/zend_builtin_functions.c:77:static ZEND_FUNCTION(set_error_handler);
Zend/zend_builtin_functions.c:78:static ZEND_FUNCTION(restore_error_handler);
Zend/zend_builtin_functions.c:79:static ZEND_FUNCTION(set_exception_handler);
Zend/zend_builtin_functions.c:80:static ZEND_FUNCTION(restore_exception_handler);
Zend/zend_builtin_functions.c:81:static ZEND_FUNCTION(get_declared_classes);
Zend/zend_builtin_functions.c:82:static ZEND_FUNCTION(get_declared_traits);
Zend/zend_builtin_functions.c:83:static ZEND_FUNCTION(get_declared_interfaces);
Zend/zend_builtin_functions.c:84:static ZEND_FUNCTION(get_defined_functions);
Zend/zend_builtin_functions.c:85:static ZEND_FUNCTION(get_defined_vars);
Zend/zend_builtin_functions.c:86:static ZEND_FUNCTION(create_function);
Zend/zend_builtin_functions.c:87:static ZEND_FUNCTION(get_resource_type);
Zend/zend_builtin_functions.c:88:static ZEND_FUNCTION(get_resources);
Zend/zend_builtin_functions.c:89:static ZEND_FUNCTION(get_loaded_extensions);
Zend/zend_builtin_functions.c:90:static ZEND_FUNCTION(extension_loaded);
Zend/zend_builtin_functions.c:91:static ZEND_FUNCTION(get_extension_funcs);
Zend/zend_builtin_functions.c:92:static ZEND_FUNCTION(get_defined_constants);
Zend/zend_builtin_functions.c:93:static ZEND_FUNCTION(debug_backtrace);
Zend/zend_builtin_functions.c:94:static ZEND_FUNCTION(debug_print_backtrace);
Zend/zend_builtin_functions.c:96:static ZEND_FUNCTION(zend_test_func);
Zend/zend_builtin_functions.c:97:static ZEND_FUNCTION(zend_test_func2);
Zend/zend_builtin_functions.c:99:static ZEND_FUNCTION(zend_thread_id);
Zend/zend_builtin_functions.c:102:static ZEND_FUNCTION(gc_mem_caches);
Zend/zend_builtin_functions.c:103:static ZEND_FUNCTION(gc_collect_cycles);
Zend/zend_builtin_functions.c:104:static ZEND_FUNCTION(gc_enabled);
Zend/zend_builtin_functions.c:105:static ZEND_FUNCTION(gc_enable);
Zend/zend_builtin_functions.c:106:static ZEND_FUNCTION(gc_disable);
Zend/zend_builtin_functions.c:109:ZEND_BEGIN_ARG_INFO(arginfo_zend__void, 0)
```

- `grep(pattern=^[A-Za-z_].*\(, version=old, path_glob=Zend/zend_execute_API.c)` →

```
53 matches
Zend/zend_execute_API.c:45:ZEND_API void (*zend_execute_ex)(zend_execute_data *execute_data);
Zend/zend_execute_API.c:46:ZEND_API void (*zend_execute_internal)(zend_execute_data *execute_data, zval *return_value);
Zend/zend_execute_API.c:57:static void (*original_sigsegv_handler)(int);
Zend/zend_execute_API.c:58:static void zend_handle_sigsegv(int dummy) /* {{{ */
Zend/zend_execute_API.c:87:static void zend_extension_activator(zend_extension *extension) /* {{{ */
Zend/zend_execute_API.c:95:static void zend_extension_deactivator(zend_extension *extension) /* {{{ */
Zend/zend_execute_API.c:103:static int clean_non_persistent_function(zval *zv) /* {{{ */
Zend/zend_execute_API.c:110:ZEND_API int clean_non_persistent_function_full(zval *zv) /* {{{ */
Zend/zend_execute_API.c:117:static int clean_non_persistent_class(zval *zv) /* {{{ */
Zend/zend_execute_API.c:124:ZEND_API int clean_non_persistent_class_full(zval *zv) /* {{{ */
Zend/zend_execute_API.c:131:void init_executor(void) /* {{{ */
Zend/zend_execute_API.c:191:static int zval_call_destructor(zval *zv) /* {{{ */
Zend/zend_execute_API.c:204:static void zend_unclean_zval_ptr_dtor(zval *zv) /* {{{ */
Zend/zend_execute_API.c:213:static void zend_throw_or_error(int fetch_type, zend_class_entry *exception_ce, const char *format, ...) /* {{{ */
Zend/zend_execute_API.c:232:void shutdown_destructors(void) /* {{{ */
Zend/zend_execute_API.c:251:void shutdown_executor(void) /* {{{ */
Zend/zend_execute_API.c:417:ZEND_API const char *get_active_class_name(const char **space) /* {{{ */
Zend/zend_execute_API.c:449:ZEND_API const char *get_active_function_name(void) /* {{{ */
Zend/zend_execute_API.c:477:ZEND_API const char *zend_get_executed_filename(void) /* {{{ */
Zend/zend_execute_API.c:492:ZEND_API zend_string *zend_get_executed_filename_ex(void) /* {{{ */
Zend/zend_execute_API.c:507:ZEND_API uint zend_get_executed_lineno(void) /* {{{ */
Zend/zend_execute_API.c:526:ZEND_API zend_bool zend_is_executing(void) /* {{{ */
Zend/zend_execute_API.c:532:ZEND_API void _zval_ptr_dtor(zval *zval_ptr ZEND_FILE_LINE_DC) /* {{{ */
Zend/zend_execute_API.c:538:ZEND_API void _zval_internal_ptr_dtor(zval *zval_ptr ZEND_FILE_LINE_DC) /* {{{ */
Zend/zend_execute_API.c:554:ZEND_API int zval_update_constant_ex(zval *p, zend_bool inline_change, zend_class_entry *scope) /* {{{ */
Zend/zend_execute_API.c:660:ZEND_API int zval_update_constant(zval *pp, zend_bool inline_change) /* {{{ */
Zend/zend_execute_API.c:666:int _call_user_function_ex(zval *object, zval *function_name, zval *retval_ptr, uint32_t param_count, zval params[], int no_separation) /* {{{ */
Zend/zend_execute_API.c:682:int zend_call_function(zend_fcall_info *fci, zend_fcall_info_cache *fci_cache) /* {{{ */
Zend/zend_execute_API.c:935:ZEND_API zend_class_entry *zend_lookup_class_ex(zend_string *name, const zval *key, int use_autoload) /* {{{ */
Zend/zend_execute_API.c:1052:ZEND_API zend_class_entry *zend_lookup_class(zend_string *name) /* {{{ */
Zend/zend_execute_API.c:1058:ZEND_API zend_class_entry *zend_get_called_scope(zend_execute_data *ex) /* {{{ */
Zend/zend_execute_API.c:1076:ZEND_API zend_object *zend_get_this_object(zend_execute_data *ex) /* {{{ */
Zend/zend_execute_API.c:1092:ZEND_API int zend_eval_stringl(char *str, size_t str_len, zval *retval_ptr, char *string_name) /* {{{ */
Zend/zend_execute_API.c:1154:ZEND_API int zend_eval_string(char *str, zval *retval_ptr, char *string_name) /* {{{ */
Zend/zend_execute_API.c:1160:ZEND_API int zend_eval_stringl_ex(char *str, size_t str_len, zval *retval_ptr, char *string_name, int handle_exceptions) /* {{{ */
Zend/zend_execute_API.c:1173:ZEND_API int zend_eval_string_ex(char *str, zval *retval_ptr, char *string_name, int handle_exceptions) /* {{{ */
Zend/zend_execute_API.c:1179:static void zend_set_timeout_ex(zend_long seconds, int reset_signals);
Zend/zend_execute_API.c:1181:ZEND_API ZEND_NORETURN void zend_timeout(int dummy) /* {{{ */
Zend/zend_execute_API.c:1190:static void zend_timeout_handler(int dummy) /* {{{ */
Zend/zend_execute_API.c:1247:VOID CALLBACK tq_timer_cb(PVOID arg, BOOLEAN timed_out)
Zend/zend_execute_API.c:1267:static void zend_set_timeout_ex(zend_long seconds, int reset_signals) /* {{{ */
Zend/zend_execute_API.c:1339:void zend_set_timeout(zend_long seconds, int reset_signals) /* {{{ */
Zend/zend_execute_API.c:1348:void zend_unset_timeout(void) /* {{{ */
Zend/zend_execute_API.c:1380:zend_class_entry *zend_fetch_class(zend_string *class_name, int fetch_type) /* {{{ */
Zend/zend_execute_API.c:1435:zend_class_entry *zend_fetch_class_by_name(zend_string *class_name, const zval *key, int fetch_type) /* {{{ */
Zend/zend_execute_API.c:1471:static void zend_verify_abstract_class_function(zend_function *fn, zend_abstract_info *ai) /* {{{ */
Zend/zend_execute_API.c:1491:void zend_verify_abstract_class(zend_class_entry *ce) /* {{{ */
Zend/zend_execute_API.c:1516:ZEND_API int zend_delete_global_variable(zend_string *name) /* {{{ */
Zend/zend_execute_API.c:1522:ZEND_API zend_array *zend_rebuild_symbol_table(void) /* {{{ */
Zend/zend_execute_API.c:1571:ZEND_API void zend_attach_symbol_table(zend_execute_data *execute_data) /* {{{ */
Zend/zend_execute_API.c:1606:ZEND_API void zend_detach_symbol_table(zend_execute_data *execute_data) /* {{{ */
Zend/zend_execute_API.c:1631:ZEND_API int zend_set_local_var(zend_string *name, zval *value, int force) /* {{{ */
Zend/zend_execute_API.c:1673:ZEND_API int zend_set_local_var_str(const char *name, size_t len, zval *value, int force) /* {{{ */
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 24550+282, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "zend_update_class_constants", "file": "Zend/zend_API.c"}, {"function": "zend_ast_evaluate", "file": "Zend/zend_ast.c"}, {"function": "add_class_vars", "file": "Zend/zend_builtin_functions.c"}, {"function": "zend_get_class_constant_ex", "file": "Zend/zend_constants.c"}, {"function": "is_null_constant", "file": "Zend/zend_execute.c"}, {"function": "zval_update_constant", "file": "Zend/zend_execute_API.c"}, {"function": "zend_ini_get_constant", "file": "Zend/zend_ini_parser.y"}], "confidence_overall": "low"}`

**Score (index):** `{"n_pred": 7, "n_truth": 12, "tp": 4, "precision": 0.5714285714285714, "recall": 0.3333333333333333, "f1": 0.4210526315789474}`

## Tool arm

### Turn 1  _(tok 3758+220, stop=tool_use)_

**Reasoning:** I'll call get_callers and run a grep at the same time.



- `get_callers(name=zval_update_constant_ex, limit=200, version=old)` →

```
{
  "name": "zval_update_constant_ex",
  "version": "old",
  "callers": [
    {
      "caller": "zend_update_class_constants",
      "file": "Zend/zend_API.c",
      "line": 1133
    },
    {
      "caller": "zend_update_class_constants",
      "file": "Zend/zend_API.c",
      "line": 1151
    },
    {
      "caller": "zend_ast_evaluate",
      "file": "Zend/zend_ast.c",
      "line": 262
    },
    {
      "caller": "zend_ast_evaluate",
      "file": "Zend/zend_ast.c",
      "line": 271
    },
    {
      "caller": "add_class_vars",
      "file": "Zend/zend_builtin_functions.c",
      "line": 1183
    },
    {
      "caller": "zend_get_constant_ex",
      "file": "Zend/zend_constants.c",
      "line": 397
    },
    {
      "caller": "is_null_constant",
      "file": "Zend/zend_execute.c",
      "line": 654
    },
    {
      "caller": "zval_update_constant",
      "file": "Zend/zend_execute_API.c",
      "line": 662
    },
    {
      "caller": "ZEND_VM_HANDLER(64, ZEND_RECV_INIT, NUM, CONST)",
      "file": "Zend/zend_vm_def.h",
      "line": 4694
    },
    {
      "caller": "ZEND_VM_HANDLER(181, ZEND_FETCH_CLASS_CONSTANT, VAR|CONST|UNUSED|CLASS_FETCH, CONST)",
      "file": "Zend/zend_vm_def.h",
      "line": 5093
    },
    {
      "caller": "ZEND_VM_HANDLER(143, ZEND_DECLARE_CONST, CONST, CONST)",
      "file": "Zend/zend_vm_def.h",
      "line": 7204
    },
    {
      "caller": "ZEND_VM_HANDLER(183, ZEND_BIND_STATIC, CV, CONST, REF)",
      "file": "Zend/zend_vm_def.h",
      "line": 8007
    },
    {
      "caller": "ZEND_RECV_INIT_SPEC_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 2295
    },
    {
      "caller": "ZEND_FETCH_CLASS_CONSTANT_SPEC_CONST_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 5646
    },
    {
      "caller": "ZEND_DECLARE_CONST_SPEC_CONST_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 6142
    },
    {
      "caller": "ZEND_FETCH_CLASS_CONSTANT_SPEC_VAR_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 18996
    },
    {
      "caller": "ZEND_FETCH_CLASS_CONSTANT_SPEC_UNUSED_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 28404
    },
    {
      "caller": "ZEND_BIND_STATIC_SPEC_CV_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 40179
    },
    {
      "caller": "_class_string",
      "file": "ext/reflection/php_reflection.c",
      "line": 459
    },
    {
      "caller": "_parameter_string",
      "file": "ext/reflection/php_reflection.c",
      "line": 715
    },
    {
      "caller": "ZEND_METHOD(reflection_function, getStaticVariables)",
      "file": "ext/reflection/php_reflection.c",
      "line": 1934
    },
    {
      "caller": "ZEND_METHOD(reflection_parameter, getDefaultValue)",
      "file": "ext/reflection/php_reflection.c",
      "line": 2896
    },
    {
      "caller": "add_class_vars",
      "file": "ext/reflection/php_reflection.c",
      "line": 3968
    },
    {
      "caller": "ZEND_METHOD(reflection_class, getConstants)",
      "file": "ext/reflection/php_reflection.c",
      "line": 4624
    },
    {
      "caller": "ZEND_METHOD(reflection_class, getConstant)",
      "file": "ext/reflection/php_reflection.c",
      "line": 4672
    },
    {
      "caller": "PHP_FUNCTION(constant)",
      "file": "ext/standard/basic_functions.c",
      "line": 3846
    }
  ]
}
```

- `grep(pattern=zval_update_constant_ex, version=old, max_results=500)` →

```
31 matches
Zend/tests/bug47572.phpt:2:Bug #47572 (zval_update_constant_ex: Segmentation fault)
Zend/zend_API.c:1133:					if (UNEXPECTED(zval_update_constant_ex(val, 1, class_type) != SUCCESS)) {
Zend/zend_API.c:1151:							if (UNEXPECTED(zval_update_constant_ex(val, 1, NULL) != SUCCESS)) {
Zend/zend_ast.c:262:					if (UNEXPECTED(zval_update_constant_ex(zv, 1, scope) != SUCCESS)) {
Zend/zend_ast.c:271:					if (UNEXPECTED(zval_update_constant_ex(result, 1, scope) != SUCCESS)) {
Zend/zend_builtin_functions.c:1183:			if (UNEXPECTED(zval_update_constant_ex(prop, 0, NULL) != SUCCESS)) {
Zend/zend_constants.c:397:			if (UNEXPECTED(zval_update_constant_ex(ret_constant, 1, ce) != SUCCESS)) {
Zend/zend_execute.c:654:		if (UNEXPECTED(zval_update_constant_ex(&constant, 0, NULL) != SUCCESS)) {
Zend/zend_execute.h:126:ZEND_API int zval_update_constant_ex(zval *pp, zend_bool inline_change, zend_class_entry *scope);
Zend/zend_execute_API.c:554:ZEND_API int zval_update_constant_ex(zval *p, zend_bool inline_change, zend_class_entry *scope) /* {{{ */
Zend/zend_execute_API.c:638:				if (UNEXPECTED(zval_update_constant_ex(p, 1, NULL) != SUCCESS)) {
Zend/zend_execute_API.c:662:	return zval_update_constant_ex(pp, inline_change, NULL);
Zend/zend_ini_parser.y:137:				zval_update_constant_ex(&tmp, 1, NULL);
Zend/zend_vm_def.h:4694:			if (UNEXPECTED(zval_update_constant_ex(param, 0, NULL) != SUCCESS)) {
Zend/zend_vm_def.h:5093:				zval_update_constant_ex(value, 1, NULL);
Zend/zend_vm_def.h:7204:		if (UNEXPECTED(zval_update_constant_ex(&c.value, 0, NULL) != SUCCESS)) {
Zend/zend_vm_def.h:8007:			if (UNEXPECTED(zval_update_constant_ex(value, 1, NULL) != SUCCESS)) {
Zend/zend_vm_execute.h:2295:			if (UNEXPECTED(zval_update_constant_ex(param, 0, NULL) != SUCCESS)) {
Zend/zend_vm_execute.h:5646:				zval_update_constant_ex(value, 1, NULL);
Zend/zend_vm_execute.h:6142:		if (UNEXPECTED(zval_update_constant_ex(&c.value, 0, NULL) != SUCCESS)) {
Zend/zend_vm_execute.h:18996:				zval_update_constant_ex(value, 1, NULL);
Zend/zend_vm_execute.h:28404:				zval_update_constant_ex(value, 1, NULL);
Zend/zend_vm_execute.h:40179:			if (UNEXPECTED(zval_update_constant_ex(value, 1, NULL) != SUCCESS)) {
ext/reflection/php_reflection.c:459:			zval_update_constant_ex(&c->value, 1, NULL);
ext/reflection/php_reflection.c:715:			zval_update_constant_ex(&zv, 1, NULL);
ext/reflection/php_reflection.c:1934:			if (UNEXPECTED(zval_update_constant_ex(val, 1, fptr->common.scope) != SUCCESS)) {
ext/reflection/php_reflection.c:2896:		zval_update_constant_ex(return_value, 0, NULL);
ext/reflection/php_reflection.c:3968:			if (UNEXPECTED(zval_update_constant_ex(&prop_copy, 1, NULL) != SUCCESS)) {
ext/reflection/php_reflection.c:4624:		if (UNEXPECTED(zval_update_constant_ex(&c->value, 1, ce) != SUCCESS)) {
ext/reflection/php_reflection.c:4672:		if (UNEXPECTED(zval_update_constant_ex(&c->value, 1, ce) != SUCCESS)) {
ext/standard/basic_functions.c:3846:			if (UNEXPECTED(zval_update_constant_ex(return_value, 1, NULL) != SUCCESS)) {
```

### Turn 2  _(tok 7584+2354, stop=tool_use)_

**Reasoning:** I'm going through the grep hits and matching each one to the function that encloses it, starting with zend_update_class_constants for the Zend/zend_API.c lines, which the callers list confirms. The remaining matches point to zend_ast_evaluate, add_class_vars, and zend_get_constant_ex, and I still need to find the enclosing function for the zend_execute.c:654 hit.

I'm working out the enclosing function for zend_execute_API.c:638, which sits inside zval_update_constant_ex itself, so it looks like a recursive call. I still need to check that function's source and figure out which function the zend_ini_parser.y:137 grammar action belongs to.

I'm now working out which function encloses the generated VM handlers, since the grep only shows ZEND_VM_HANDLER macro lines in zend_vm_def.h and the real functions are probably in zend_vm_execute.h. I'm weighing whether to report the handler names from there or the macro entries, and I'm noting that the callers list has duplicate function names that I'll need to deduplicate.

I'm checking which function holds the zend_ini_parser.y:137 grammar action, since the grep tool skipped it as a non-C file. I also need to confirm whether the zend_execute_API.c:638 hit really sits inside zval_update_constant_ex, and I'm noting that the callers list has duplicate function names to deduplicate.

I'm settling on how to report the ZEND_VM_HANDLER entries: the real C functions are the generated handlers in zend_vm_execute.h, while the zend_vm_def.h lines are only macro templates, so I'm leaning toward listing the former.

I'm settling on the generated handler functions in zend_vm_execute.h as the real C functions to report, since the zend_vm_def.h entries are just macro templates for the same handlers, and I'm listing names like ZEND_RECV_INIT_SPEC_CONST_HANDLER and ZEND_FETCH_CLASS_CONSTANT_SPEC_CONST_CONST_HANDLER.

I'm checking the source of zval_update_constant_ex around lines 554 to 665 to confirm whether the line 638 call is actually recursive, and I still need to work out which function the zend_ini_parser.y:137 action belongs to.

I'm going to check the source around line 638 in zend_execute_API.c, along with the lines near 554–665, to see whether that call is really recursive. I also want to look at the zend_ini_parser.y action around line 137 to find which function it sits in.



- `read_file(path=Zend/zend_execute_API.c, version=old, start_line=554, end_line=664)` →

```
Zend/zend_execute_API.c lines 554-664 of 1722
  554| ZEND_API int zval_update_constant_ex(zval *p, zend_bool inline_change, zend_class_entry *scope) /* {{{ */
  555| {
  556| 	zval *const_value;
  557| 	char *colon;
  558| 
  559| 	if (IS_CONSTANT_VISITED(p)) {
  560| 		zend_throw_error(NULL, "Cannot declare self-referencing constant '%s'", Z_STRVAL_P(p));
  561| 		return FAILURE;
  562| 	} else if (Z_TYPE_P(p) == IS_CONSTANT) {
  563| 
  564| 		SEPARATE_ZVAL_NOREF(p);
  565| 		MARK_CONSTANT_VISITED(p);
  566| 		if (Z_CONST_FLAGS_P(p) & IS_CONSTANT_CLASS) {
  567| 			ZEND_ASSERT(EG(current_execute_data));
  568| 			if (inline_change) {
  569| 				zend_string_release(Z_STR_P(p));
  570| 			}
  571| 			if (EG(scope) && EG(scope)->name) {
  572| 				ZVAL_STR_COPY(p, EG(scope)->name);
  573| 			} else {
  574| 				ZVAL_EMPTY_STRING(p);
  575| 			}
  576| 		} else if (UNEXPECTED((const_value = zend_get_constant_ex(Z_STR_P(p), scope, Z_CONST_FLAGS_P(p))) == NULL)) {
  577| 			char *actual = Z_STRVAL_P(p);
  578| 
  579| 			if (UNEXPECTED(EG(exception))) {
  580| 				RESET_CONSTANT_VISITED(p);
  581| 				return FAILURE;
  582| 			} else if ((colon = (char*)zend_memrchr(Z_STRVAL_P(p), ':', Z_STRLEN_P(p)))) {
  583| 				zend_throw_error(NULL, "Undefined class constant '%s'", Z_STRVAL_P(p));
  584| 				RESET_CONSTANT_VISITED(p);
  585| 				return FAILURE;
  586| 			} else {
  587| 				zend_string *save = Z_STR_P(p);
  588| 				char *slash;
  589| 				size_t actual_len = Z_STRLEN_P(p);
  590| 				if ((Z_CONST_FLAGS_P(p) & IS_CONSTANT_UNQUALIFIED) && (slash = (char *)zend_memrchr(actual, '\\', actual_len))) {
  591| 					actual = slash + 1;
  592| 					actual_len -= (actual - Z_STRVAL_P(p));
  593| 					if (inline_change) {
  594| 						zend_string *s = zend_string_init(actual, actual_len, 0);
  595| 						Z_STR_P(p) = s;
  596| 						Z_TYPE_FLAGS_P(p) = IS_TYPE_REFCOUNTED | IS_TYPE_COPYABLE;
  597| 					}
  598| 				}
  599| 				if (actual[0] == '\\') {
  600| 					if (inline_change) {
  601| 						memmove(Z_STRVAL_P(p), Z_STRVAL_P(p)+1, Z_STRLEN_P(p));
  602| 						--Z_STRLEN_P(p);
  603| 					} else {
  604| 						++actual;
  605| 					}
  606| 					--actual_len;
  607| 				}
  608| 				if ((Z_CONST_FLAGS_P(p) & IS_CONSTANT_UNQUALIFIED) == 0) {
  609| 					if (ZSTR_VAL(save)[0] == '\\') {
  610| 						zend_throw_error(NULL, "Undefined constant '%s'", ZSTR_VAL(save) + 1);
  611| 					} else {
  612| 						zend_throw_error(NULL, "Undefined constant '%s'", ZSTR_VAL(save));
  613| 					}
  614| 					if (inline_change) {
  615| 						zend_string_release(save);
  616| 					}
  617| 					RESET_CONSTANT_VISITED(p);
  618| 					return FAILURE;
  619| 				} else {
  620| 					zend_error(E_NOTICE, "Use of undefined constant %s - assumed '%s'",  actual,  actual);
  621| 					if (!inline_change) {
  622| 						ZVAL_STRINGL(p, actual, actual_len);
  623| 					} else {
  624| 						Z_TYPE_INFO_P(p) = Z_REFCOUNTED_P(p) ?
  625| 							IS_STRING_EX : IS_INTERNED_STRING_EX;
  626| 						if (save && ZSTR_VAL(save) != actual) {
  627| 							zend_string_release(save);
  628| 						}
  629| 					}
  630| 				}
  631| 			}
  632| 		} else {
  633| 			if (inline_change) {
  634| 				zend_string_release(Z_STR_P(p));
  635| 			}
  636| 			ZVAL_COPY_VALUE(p, const_value);
  637| 			if (Z_OPT_CONSTANT_P(p)) {
  638| 				if (UNEXPECTED(zval_update_constant_ex(p, 1, NULL) != SUCCESS)) {
  639| 					RESET_CONSTANT_VISITED(p);
  640| 					return FAILURE;
  641| 				}
  642| 			}
  643| 			zval_opt_copy_ctor(p);
  644| 		}
  645| 	} else if (Z_TYPE_P(p) == IS_CONSTANT_AST) {
  646| 		zval tmp;
  647| 
  648| 		if (UNEXPECTED(zend_ast_evaluate(&tmp, Z_ASTVAL_P(p), scope) != SUCCESS)) {
  649| 			return FAILURE;
  650| 		}
  651| 		if (inline_change) {
  652| 			zval_ptr_dtor(p);
  653| 		}
  654| 		ZVAL_COPY_VALUE(p, &tmp);
  655| 	}
  656| 	return SUCCESS;
  657| }
  658| /* }}} */
  659| 
  660| ZEND_API int zval_update_constant(zval *pp, zend_bool inline_change) /* {{{ */
  661| {
  662| 	return zval_update_constant_ex(pp, inline_change, NULL);
  663| }
  664| /* }}} */
```

- `read_file(path=Zend/zend_ini_parser.y, version=old, start_line=120, end_line=145)` →

```
Zend/zend_ini_parser.y lines 120-145 of 404
  120| 	ZVAL_NEW_STR(result, zend_string_extend(Z_STR_P(op1), length, 1));
  121| 	memcpy(Z_STRVAL_P(result) + op1_len, Z_STRVAL_P(op2), Z_STRLEN_P(op2) + 1);
  122| }
  123| /* }}} */
  124| 
  125| /* {{{ zend_ini_get_constant()
  126| */
  127| static void zend_ini_get_constant(zval *result, zval *name)
  128| {
  129| 	zval *c, tmp;
  130| 
  131| 	/* If name contains ':' it is not a constant. Bug #26893. */
  132| 	if (!memchr(Z_STRVAL_P(name), ':', Z_STRLEN_P(name))
  133| 		   	&& (c = zend_get_constant(Z_STR_P(name))) != 0) {
  134| 		if (Z_TYPE_P(c) != IS_STRING) {
  135| 			ZVAL_COPY_VALUE(&tmp, c);
  136| 			if (Z_OPT_CONSTANT(tmp)) {
  137| 				zval_update_constant_ex(&tmp, 1, NULL);
  138| 			}
  139| 			zval_opt_copy_ctor(&tmp);
  140| 			convert_to_string(&tmp);
  141| 			c = &tmp;
  142| 		}
  143| 		ZVAL_PSTRINGL(result, Z_STRVAL_P(c), Z_STRLEN_P(c));
  144| 		if (c == &tmp) {
  145| 			zend_string_release(Z_STR(tmp));
```

### Turn 3  _(tok 12959+2848, stop=tool_use)_

**Reasoning:** I'm noting that zend_ini_get_constant is the enclosing function of the parser source, and that its generated C file isn't in the repo, so I'll leave that one alone. The recursive call at zend_execute_API.c:638 sits inside zval_update_constant_ex itself, and I need to decide whether a self-call counts as a call site that has to be updated.

I'm settling that the recursive self-call in zval_update_constant_ex is a call site that needs updating, and I'm adding zval_update_constant to the list as well. For the VM handlers, I'm leaning toward the executable functions in zend_vm_execute.h rather than the ZEND_VM_HANDLER macro templates in zend_vm_def.h, since those templates aren't functions themselves.

I'm checking whether the vm handler names in zend_vm_execute.h match the reported names with the argument lists stripped off, and I'm listing the remaining enclosing functions to include, such as the reflection methods and the macro-generated ZEND_METHOD functions.

I'm reporting the reflection method as ZEND_METHOD(reflection_function, getStaticVariables) and PHP_FUNCTION(constant) exactly as they're written in source, and I'm confirming that the six vm_execute.h call sites line up with the handlers already gathered.

I'm listing the remaining call sites, starting with zend_update_class_constants in Zend/zend_API.c and continuing through the rest of the list.

I'm listing the rest of the enclosing functions, including the reflection helpers and the ZEND_METHOD ones, and I'll keep each name as it appears in the source.

I'm going through the remaining entries in the list, covering the reflection methods and the PHP function constant in basic_functions.c. I'm also noting that I still need to decide whether the zend_vm_def.h templates belong in the list alongside the generated handlers.



- **submit_callers** → `{"callers": [{"function": "zend_update_class_constants", "file": "Zend/zend_API.c"}, {"function": "zend_ast_evaluate", "file": "Zend/zend_ast.c"}, {"function": "add_class_vars", "file": "Zend/zend_builtin_functions.c"}, {"function": "zend_get_constant_ex", "file": "Zend/zend_constants.c"}, {"function": "is_null_constant", "file": "Zend/zend_execute.c"}, {"function": "zval_update_constant", "file": "Zend/zend_execute_API.c"}, {"function": "zval_update_constant_ex", "file": "Zend/zend_execute_API.c"}, {"function": "zend_ini_get_constant", "file": "Zend/zend_ini_parser.y"}, {"function": "ZEND_RECV_INIT_SPEC_CONST_HANDLER", "file": "Zend/zend_vm_execute.h"}, {"function": "ZEND_FETCH_CLASS_CONSTANT_SPEC_CONST_CONST_HANDLER", "file": "Zend/zend_vm_execute.h"}, {"function": "ZEND_DECLARE_CONST_SPEC_CONST_CONST_HANDLER", "file": "Zend/zend_vm_execute.h"}, {"function": "ZEND_FETCH_CLASS_CONSTANT_SPEC_VAR_CONST_HANDLER", "file": "Zend/zend_vm_execute.h"}, {"function": "ZEND_FETCH_CLASS_CONSTANT_SPEC_UNUSED_CONST_HANDLER", "file": "Zend/zend_vm_execute.h"}, {"function": "ZEND_BIND_STATIC_SPEC_CV_CONST_HANDLER", "file": "Zend/zend_vm_execute.h"}, {"function": "_class_string", "file": "ext/reflection/php_reflection.c"}, {"function": "_parameter_string", "file": "ext/reflection/php_reflection.c"}, {"function": "ZEND_METHOD(reflection_function, getStaticVariables)", "file": "ext/reflection/php_reflection.c"}, {"function": "ZEND_METHOD(reflection_parameter, getDefaultValue)", "file": "ext/reflection/php_reflection.c"}, {"function": "add_class_vars", "file": "ext/reflection/php_reflection.c"}, {"function": "ZEND_METHOD(reflection_class, getConstants)", "file": "ext/reflection/php_reflection.c"}, {"function": "ZEND_METHOD(reflection_class, getConstant)", "file": "ext/reflection/php_reflection.c"}, {"function": "PHP_FUNCTION(constant)", "file": "ext/standard/basic_functions.c"}], "confidence_overall": "medium"}`

**Score (tool):** `{"n_pred": 21, "n_truth": 12, "tp": 9, "precision": 0.42857142857142855, "recall": 0.75, "f1": 0.5454545454545454}`

## Semantic arm

### Turn 1  _(tok 3210+99, stop=tool_use)_

**Reasoning:** I'm going to call get_callers and ask for a high limit so I get the full set of results.



- `get_callers(name=zval_update_constant_ex, limit=200)` →

```
{
  "name": "zval_update_constant_ex",
  "version": "old",
  "callers": [
    {
      "caller": "zend_update_class_constants",
      "file": "Zend/zend_API.c",
      "line": 1133
    },
    {
      "caller": "zend_update_class_constants",
      "file": "Zend/zend_API.c",
      "line": 1151
    },
    {
      "caller": "zend_ast_evaluate",
      "file": "Zend/zend_ast.c",
      "line": 262
    },
    {
      "caller": "zend_ast_evaluate",
      "file": "Zend/zend_ast.c",
      "line": 271
    },
    {
      "caller": "add_class_vars",
      "file": "Zend/zend_builtin_functions.c",
      "line": 1183
    },
    {
      "caller": "zend_get_constant_ex",
      "file": "Zend/zend_constants.c",
      "line": 397
    },
    {
      "caller": "is_null_constant",
      "file": "Zend/zend_execute.c",
      "line": 654
    },
    {
      "caller": "zval_update_constant",
      "file": "Zend/zend_execute_API.c",
      "line": 662
    },
    {
      "caller": "ZEND_VM_HANDLER(64, ZEND_RECV_INIT, NUM, CONST)",
      "file": "Zend/zend_vm_def.h",
      "line": 4694
    },
    {
      "caller": "ZEND_VM_HANDLER(181, ZEND_FETCH_CLASS_CONSTANT, VAR|CONST|UNUSED|CLASS_FETCH, CONST)",
      "file": "Zend/zend_vm_def.h",
      "line": 5093
    },
    {
      "caller": "ZEND_VM_HANDLER(143, ZEND_DECLARE_CONST, CONST, CONST)",
      "file": "Zend/zend_vm_def.h",
      "line": 7204
    },
    {
      "caller": "ZEND_VM_HANDLER(183, ZEND_BIND_STATIC, CV, CONST, REF)",
      "file": "Zend/zend_vm_def.h",
      "line": 8007
    },
    {
      "caller": "ZEND_RECV_INIT_SPEC_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 2295
    },
    {
      "caller": "ZEND_FETCH_CLASS_CONSTANT_SPEC_CONST_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 5646
    },
    {
      "caller": "ZEND_DECLARE_CONST_SPEC_CONST_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 6142
    },
    {
      "caller": "ZEND_FETCH_CLASS_CONSTANT_SPEC_VAR_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 18996
    },
    {
      "caller": "ZEND_FETCH_CLASS_CONSTANT_SPEC_UNUSED_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 28404
    },
    {
      "caller": "ZEND_BIND_STATIC_SPEC_CV_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 40179
    },
    {
      "caller": "_class_string",
      "file": "ext/reflection/php_reflection.c",
      "line": 459
    },
    {
      "caller": "_parameter_string",
      "file": "ext/reflection/php_reflection.c",
      "line": 715
    },
    {
      "caller": "ZEND_METHOD(reflection_function, getStaticVariables)",
      "file": "ext/reflection/php_reflection.c",
      "line": 1934
    },
    {
      "caller": "ZEND_METHOD(reflection_parameter, getDefaultValue)",
      "file": "ext/reflection/php_reflection.c",
      "line": 2896
    },
    {
      "caller": "add_class_vars",
      "file": "ext/reflection/php_reflection.c",
      "line": 3968
    },
    {
      "caller": "ZEND_METHOD(reflection_class, getConstants)",
      "file": "ext/reflection/php_reflection.c",
      "line": 4624
    },
    {
      "caller": "ZEND_METHOD(reflection_class, getConstant)",
      "file": "ext/reflection/php_reflection.c",
      "line": 4672
    },
    {
      "caller": "PHP_FUNCTION(constant)",
      "file": "ext/standard/basic_functions.c",
      "line": 3846
    }
  ]
}
```

### Turn 2  _(tok 5161+478, stop=tool_use)_

**Reasoning:** I'm checking whether the server's default version is the commit or the working tree, since the function is about to change and the tool returned "old," which seems off. I'll re-query with version "work" to see if that matches. I also need to account for callers in zend_vm_execute.h, which is generated but still counts as functions in the repo.

I'm checking whether the callers in the generated zend_vm_execute.h count, since they're still functions in this repo, and the names there are macro-generated handlers. I also need to include zval_update_constant at line 662 of zend_execute_API.c, and verify the list against the work version, including zend_ast_evaluate in zend_ast.c.



- `get_callers(name=zval_update_constant_ex, limit=200, rev=None, version=work)` →

```
{
  "name": "zval_update_constant_ex",
  "version": "old",
  "callers": [
    {
      "caller": "zend_update_class_constants",
      "file": "Zend/zend_API.c",
      "line": 1133
    },
    {
      "caller": "zend_update_class_constants",
      "file": "Zend/zend_API.c",
      "line": 1151
    },
    {
      "caller": "zend_ast_evaluate",
      "file": "Zend/zend_ast.c",
      "line": 262
    },
    {
      "caller": "zend_ast_evaluate",
      "file": "Zend/zend_ast.c",
      "line": 271
    },
    {
      "caller": "add_class_vars",
      "file": "Zend/zend_builtin_functions.c",
      "line": 1183
    },
    {
      "caller": "zend_get_constant_ex",
      "file": "Zend/zend_constants.c",
      "line": 397
    },
    {
      "caller": "is_null_constant",
      "file": "Zend/zend_execute.c",
      "line": 654
    },
    {
      "caller": "zval_update_constant",
      "file": "Zend/zend_execute_API.c",
      "line": 662
    },
    {
      "caller": "ZEND_VM_HANDLER(64, ZEND_RECV_INIT, NUM, CONST)",
      "file": "Zend/zend_vm_def.h",
      "line": 4694
    },
    {
      "caller": "ZEND_VM_HANDLER(181, ZEND_FETCH_CLASS_CONSTANT, VAR|CONST|UNUSED|CLASS_FETCH, CONST)",
      "file": "Zend/zend_vm_def.h",
      "line": 5093
    },
    {
      "caller": "ZEND_VM_HANDLER(143, ZEND_DECLARE_CONST, CONST, CONST)",
      "file": "Zend/zend_vm_def.h",
      "line": 7204
    },
    {
      "caller": "ZEND_VM_HANDLER(183, ZEND_BIND_STATIC, CV, CONST, REF)",
      "file": "Zend/zend_vm_def.h",
      "line": 8007
    },
    {
      "caller": "ZEND_RECV_INIT_SPEC_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 2295
    },
    {
      "caller": "ZEND_FETCH_CLASS_CONSTANT_SPEC_CONST_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 5646
    },
    {
      "caller": "ZEND_DECLARE_CONST_SPEC_CONST_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 6142
    },
    {
      "caller": "ZEND_FETCH_CLASS_CONSTANT_SPEC_VAR_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 18996
    },
    {
      "caller": "ZEND_FETCH_CLASS_CONSTANT_SPEC_UNUSED_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 28404
    },
    {
      "caller": "ZEND_BIND_STATIC_SPEC_CV_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)",
      "file": "Zend/zend_vm_execute.h",
      "line": 40179
    },
    {
      "caller": "_class_string",
      "file": "ext/reflection/php_reflection.c",
      "line": 459
    },
    {
      "caller": "_parameter_string",
      "file": "ext/reflection/php_reflection.c",
      "line": 715
    },
    {
      "caller": "ZEND_METHOD(reflection_function, getStaticVariables)",
      "file": "ext/reflection/php_reflection.c",
      "line": 1934
    },
    {
      "caller": "ZEND_METHOD(reflection_parameter, getDefaultValue)",
      "file": "ext/reflection/php_reflection.c",
      "line": 2896
    },
    {
      "caller": "add_class_vars",
      "file": "ext/reflection/php_reflection.c",
      "line": 3968
    },
    {
      "caller": "ZEND_METHOD(reflection_class, getConstants)",
      "file": "ext/reflection/php_reflection.c",
      "line": 4624
    },
    {
      "caller": "ZEND_METHOD(reflection_class, getConstant)",
      "file": "ext/reflection/php_reflection.c",
      "line": 4672
    },
    {
      "caller": "PHP_FUNCTION(constant)",
      "file": "ext/standard/basic_functions.c",
      "line": 3846
    }
  ]
}
```

### Turn 3  _(tok 7491+3458, stop=tool_use)_

**Reasoning:** The result matches the earlier one, so I'm weighing whether to verify a few more callers. The call graph might miss function-pointer or macro-based calls, and there's no grep available, but the tool output seems consistent. I'm considering checking other callers like zend_update_class_constants, though it isn't strictly necessary, and I'm leaning toward submitting.

I'm working out which handler entries to report: the zend_vm_def.h ones are just macro sources, while zend_vm_execute.h holds the generated functions, so I'm weighing whether listing both would double-count the same handlers.

I'm deciding whether listing the zend_vm_def.h entries alongside the zend_vm_execute.h ones counts as double-counting. Both are real call sites, since the def file is the handler source and the execute file is its generated output, and a signature change would have to touch both to compile. So I'm leaning toward including all of them, with the def-file entries named by their macro form.

I'm going through the caller list, and I've settled on including the zval_update_constant caller from zend_execute_API.c as well. Counting the entries, I see duplicates of zend_update_class_constants and zend_ast_evaluate that I'll collapse, while add_class_vars stays in both of its files.

Still listing the callers from the tool output, working through the handler entries from zend_vm_def.h.

Still going through the handler entries, the rest of the zend_vm_def.h list and the zend_vm_execute.h generated functions, to make sure each one is counted once.

Still going through the caller list, now the reflection methods and the constant() function in ext/standard.

I'm settling on 24 entries after collapsing the duplicates, and I'm reporting the names exactly as the tool gave them. My confidence is medium, since the call graph may still miss function-pointer calls.



- **submit_callers** → `{"callers": [{"function": "zend_update_class_constants", "file": "Zend/zend_API.c"}, {"function": "zend_ast_evaluate", "file": "Zend/zend_ast.c"}, {"function": "add_class_vars", "file": "Zend/zend_builtin_functions.c"}, {"function": "zend_get_constant_ex", "file": "Zend/zend_constants.c"}, {"function": "is_null_constant", "file": "Zend/zend_execute.c"}, {"function": "zval_update_constant", "file": "Zend/zend_execute_API.c"}, {"function": "ZEND_VM_HANDLER(64, ZEND_RECV_INIT, NUM, CONST)", "file": "Zend/zend_vm_def.h"}, {"function": "ZEND_VM_HANDLER(181, ZEND_FETCH_CLASS_CONSTANT, VAR|CONST|UNUSED|CLASS_FETCH, CONST)", "file": "Zend/zend_vm_def.h"}, {"function": "ZEND_VM_HANDLER(143, ZEND_DECLARE_CONST, CONST, CONST)", "file": "Zend/zend_vm_def.h"}, {"function": "ZEND_VM_HANDLER(183, ZEND_BIND_STATIC, CV, CONST, REF)", "file": "Zend/zend_vm_def.h"}, {"function": "ZEND_RECV_INIT_SPEC_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)", "file": "Zend/zend_vm_execute.h"}, {"function": "ZEND_FETCH_CLASS_CONSTANT_SPEC_CONST_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)", "file": "Zend/zend_vm_execute.h"}, {"function": "ZEND_DECLARE_CONST_SPEC_CONST_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)", "file": "Zend/zend_vm_execute.h"}, {"function": "ZEND_FETCH_CLASS_CONSTANT_SPEC_VAR_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)", "file": "Zend/zend_vm_execute.h"}, {"function": "ZEND_FETCH_CLASS_CONSTANT_SPEC_UNUSED_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)", "file": "Zend/zend_vm_execute.h"}, {"function": "ZEND_BIND_STATIC_SPEC_CV_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)", "file": "Zend/zend_vm_execute.h"}, {"function": "_class_string", "file": "ext/reflection/php_reflection.c"}, {"function": "_parameter_string", "file": "ext/reflection/php_reflection.c"}, {"function": "ZEND_METHOD(reflection_function, getStaticVariables)", "file": "ext/reflection/php_reflection.c"}, {"function": "ZEND_METHOD(reflection_parameter, getDefaultValue)", "file": "ext/reflection/php_reflection.c"}, {"function": "add_class_vars", "file": "ext/reflection/php_reflection.c"}, {"function": "ZEND_METHOD(reflection_class, getConstants)", "file": "ext/reflection/php_reflection.c"}, {"function": "ZEND_METHOD(reflection_class, getConstant)", "file": "ext/reflection/php_reflection.c"}, {"function": "PHP_FUNCTION(constant)", "file": "ext/standard/basic_functions.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 23, "n_truth": 12, "tp": 12, "precision": 0.5217391304347826, "recall": 1.0, "f1": 0.6857142857142856}`

