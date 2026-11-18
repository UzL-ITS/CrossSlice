# Impact-analysis transcript — php-src @ 079409bbc232 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `zend_unmangle_property_name_ex` (Zend/zend_compile.c), arity 5->4
- truth: [['Zend/zend.c', 'print_hash'], ['Zend/zend_builtin_functions.c', 'ZEND_FUNCTION(get_object_vars)'], ['Zend/zend_compile.c', 'zend_do_traits_property_binding'], ['Zend/zend_object_handlers.c', 'zend_check_property_access'], ['Zend/zend_vm_def.h', 'ZEND_VM_HANDLER(78, ZEND_FE_FETCH, VAR, ANY)'], ['Zend/zend_vm_execute.h', 'ZEND_FE_FETCH_SPEC_VAR_HANDLER'], ['ext/reflection/php_reflection.c', 'reflection_property_factory'], ['ext/standard/http.c', 'php_url_encode_hash_ex']]

## Self-navigation arm

### Turn 1  _(tok 910+80, stop=tool_use)_

**Reasoning:** Let me search for the `zend_unmangle_property_name_ex` function in the codebase.

- `grep(pattern=zend_unmangle_property_name_ex, version=old, max_results=200)` →

```
11 matches
Zend/zend.c:160:				int mangled = zend_unmangle_property_name_ex(string_key->val, string_key->len, &class_name, &prop_name, &prop_len);
Zend/zend_builtin_functions.c:1073:					zend_unmangle_property_name_ex(key->val, key->len, &class_name, &prop_name, (int*) &prop_len);
Zend/zend_compile.c:2306:				zend_unmangle_property_name_ex(property_info->name->val, property_info->name->len,
Zend/zend_compile.c:2693:ZEND_API int zend_unmangle_property_name_ex(const char *mangled_property, int len, const char **class_name, const char **prop_name, int *prop_len) /* {{{ */
Zend/zend_compile.h:504:        zend_unmangle_property_name_ex(mangled_property, mangled_property_len, class_name, prop_name, NULL)
Zend/zend_compile.h:505:ZEND_API int zend_unmangle_property_name_ex(const char *mangled_property, int mangled_property_len, const char **class_name, const char **prop_name, int *prop_len);
Zend/zend_object_handlers.c:403:		zend_unmangle_property_name_ex(prop_info_name->val, prop_info_name->len, &class_name, &prop_name, &prop_name_len);
Zend/zend_vm_def.h:4815:							zend_unmangle_property_name_ex(
Zend/zend_vm_execute.h:16795:							zend_unmangle_property_name_ex(
ext/reflection/php_reflection.c:1303:	zend_unmangle_property_name_ex(prop->name->val, prop->name->len, &class_name, &prop_name, &prop_name_len);
ext/standard/http.c:69:				zend_unmangle_property_name_ex(key->val, key->len, &tmp, &prop_name, (int *)&prop_len);
```

### Turn 2  _(tok 1454+346, stop=tool_use)_

**Reasoning:** Next, I need to identify the function that encloses each call site. Also, note that line 504 of zend_compile.h is a macro (zend_unmangle_property_name) that wraps it — but the task instructs me to only enumerate call sites of zend_unmangle_property_name_ex. Direct callers only. The task says "all functions that call zend_unmangle_property_name_ex." Since this macro indirectly calls it, should I also consider callers of zend_unmangle_property_name? The instructions say "list all functions that call zend_unmangle_property_name_ex." I'll limit to direct calls (including the call at zend_vm_execute.h:16795, which is generated from zend_vm_def.h). Hmm, zend_vm_execute.h is generated, but it exists within the repository, so both should be enumerated.

Let me examine each call site to identify the enclosing function.

**Says:** Found 11 matches. Let me examine each call site to determine enclosing functions.



- `read_file(path=Zend/zend.c, start_line=130, end_line=175, version=old)` →

```
Zend/zend.c lines 130-175 of 1428
  130| #define ZEND_CORE_VERSION_INFO	"Zend Engine v" ZEND_VERSION ", Copyright (c) 1998-2014 Zend Technologies\n"
  131| #define PRINT_ZVAL_INDENT 4
  132| 
  133| static void print_hash(zend_write_func_t write_func, HashTable *ht, int indent, zend_bool is_object TSRMLS_DC) /* {{{ */
  134| {
  135| 	zval *tmp;
  136| 	zend_string *string_key;
  137| 	zend_ulong num_key;
  138| 	int i;
  139| 
  140| 	for (i = 0; i < indent; i++) {
  141| 		ZEND_PUTS_EX(" ");
  142| 	}
  143| 	ZEND_PUTS_EX("(\n");
  144| 	indent += PRINT_ZVAL_INDENT;
  145| 	ZEND_HASH_FOREACH_KEY_VAL(ht, num_key, string_key, tmp) {
  146| 		if (Z_TYPE_P(tmp) == IS_INDIRECT) {
  147| 			tmp = Z_INDIRECT_P(tmp);
  148| 			if (Z_TYPE_P(tmp) == IS_UNDEF) {
  149| 				continue;
  150| 			}
  151| 		}
  152| 		for (i = 0; i < indent; i++) {
  153| 			ZEND_PUTS_EX(" ");
  154| 		}
  155| 		ZEND_PUTS_EX("[");
  156| 		if (string_key) {
  157| 			if (is_object) {
  158| 				const char *prop_name, *class_name;
  159| 				int prop_len;
  160| 				int mangled = zend_unmangle_property_name_ex(string_key->val, string_key->len, &class_name, &prop_name, &prop_len);
  161| 
  162| 				ZEND_WRITE_EX(prop_name, prop_len);
  163| 				if (class_name && mangled == SUCCESS) {
  164| 					if (class_name[0]=='*') {
  165| 						ZEND_PUTS_EX(":protected");
  166| 					} else {
  167| 						ZEND_PUTS_EX(":");
  168| 						ZEND_PUTS_EX(class_name);
  169| 						ZEND_PUTS_EX(":private");
  170| 					}
  171| 				}
  172| 			} else {
  173| 				ZEND_WRITE_EX(string_key->val, string_key->len);
  174| 			}
  175| 		} else {
```

- `read_file(path=Zend/zend_builtin_functions.c, start_line=1040, end_line=1080, version=old)` →

```
Zend/zend_builtin_functions.c lines 1040-1080 of 2648
 1040| 	uint prop_len;
 1041| 	zend_object *zobj;
 1042| 
 1043| #ifndef FAST_ZPP
 1044| 	if (zend_parse_parameters(ZEND_NUM_ARGS() TSRMLS_CC, "o", &obj) == FAILURE) {
 1045| 		return;
 1046| 	}
 1047| #else
 1048| 	ZEND_PARSE_PARAMETERS_START(1, 1)
 1049| 		Z_PARAM_OBJECT(obj)
 1050| 	ZEND_PARSE_PARAMETERS_END();
 1051| #endif
 1052| 
 1053| 	if (Z_OBJ_HT_P(obj)->get_properties == NULL) {
 1054| 		RETURN_FALSE;
 1055| 	}
 1056| 
 1057| 	properties = Z_OBJ_HT_P(obj)->get_properties(obj TSRMLS_CC);
 1058| 
 1059| 	if (properties == NULL) {
 1060| 		RETURN_FALSE;
 1061| 	}
 1062| 
 1063| 	zobj = Z_OBJ_P(obj);
 1064| 
 1065| 	array_init_size(return_value, zend_hash_num_elements(properties));
 1066| 
 1067| 	ZEND_HASH_FOREACH_STR_KEY_VAL_IND(properties, key, value) {
 1068| 		if (key) {
 1069| 			if (zend_check_property_access(zobj, key TSRMLS_CC) == SUCCESS) {
 1070| 				/* Not separating references */
 1071| 				if (Z_REFCOUNTED_P(value)) Z_ADDREF_P(value);
 1072| 				if (key->val[0] == 0) {
 1073| 					zend_unmangle_property_name_ex(key->val, key->len, &class_name, &prop_name, (int*) &prop_len);
 1074| 					zend_hash_str_add_new(Z_ARRVAL_P(return_value), prop_name, prop_len, value);
 1075| 				} else {
 1076| 					zend_hash_add_new(Z_ARRVAL_P(return_value), key, value);
 1077| 				}
 1078| 			}
 1079| 		}
 1080| 	} ZEND_HASH_FOREACH_END();
```

### Turn 3  _(tok 3219+160, stop=tool_use)_

**Reasoning:** Need the function name — it's before line 1040.


- `read_file(end_line=1040, path=Zend/zend_builtin_functions.c, start_line=1030, version=old)` →

```
Zend/zend_builtin_functions.c lines 1030-1040 of 2648
 1030| 
 1031| /* {{{ proto array get_object_vars(object obj)
 1032|    Returns an array of object properties */
 1033| ZEND_FUNCTION(get_object_vars)
 1034| {
 1035| 	zval *obj;
 1036| 	zval *value;
 1037| 	HashTable *properties;
 1038| 	zend_string *key;
 1039| 	const char *prop_name, *class_name;
 1040| 	uint prop_len;
```

- `read_file(end_line=2320, path=Zend/zend_compile.c, start_line=2270, version=old)` →

```
Zend/zend_compile.c lines 2270-2320 of 7950
 2270| 
 2271| 	return coliding_ce;
 2272| }
 2273| /* }}} */
 2274| 
 2275| static void zend_do_traits_property_binding(zend_class_entry *ce TSRMLS_DC) /* {{{ */
 2276| {
 2277| 	size_t i;
 2278| 	zend_property_info *property_info;
 2279| 	zend_property_info *coliding_prop;
 2280| 	zval compare_result;
 2281| 	zend_string* prop_name;
 2282| 	const char* class_name_unused;
 2283| 	zend_bool not_compatible;
 2284| 	zval* prop_value;
 2285| 	uint32_t flags;
 2286| 	zend_string *doc_comment;
 2287| 
 2288| 	/* In the following steps the properties are inserted into the property table
 2289| 	 * for that, a very strict approach is applied:
 2290| 	 * - check for compatibility, if not compatible with any property in class -> fatal
 2291| 	 * - if compatible, then strict notice
 2292| 	 */
 2293| 	for (i = 0; i < ce->num_traits; i++) {
 2294| 		ZEND_HASH_FOREACH_PTR(&ce->traits[i]->properties_info, property_info) {
 2295| 			/* first get the unmangeld name if necessary,
 2296| 			 * then check whether the property is already there
 2297| 			 */
 2298| 			flags = property_info->flags;
 2299| 			if ((flags & ZEND_ACC_PPP_MASK) == ZEND_ACC_PUBLIC) {
 2300| 				prop_name = zend_string_copy(property_info->name);
 2301| 			} else {
 2302| 				const char *pname;
 2303| 				int pname_len;
 2304| 
 2305| 				/* for private and protected we need to unmangle the names */
 2306| 				zend_unmangle_property_name_ex(property_info->name->val, property_info->name->len,
 2307| 											&class_name_unused, &pname, &pname_len);
 2308| 				prop_name = zend_string_init(pname, pname_len, 0);
 2309| 			}
 2310| 
 2311| 			/* next: check for conflicts with current class */
 2312| 			if ((coliding_prop = zend_hash_find_ptr(&ce->properties_info, prop_name)) != NULL) {
 2313| 				if (coliding_prop->flags & ZEND_ACC_SHADOW) {
 2314| 					zend_hash_del(&ce->properties_info, prop_name);
 2315| 					flags |= ZEND_ACC_CHANGED;
 2316| 				} else {
 2317| 					if ((coliding_prop->flags & (ZEND_ACC_PPP_MASK | ZEND_ACC_STATIC))
 2318| 						== (flags & (ZEND_ACC_PPP_MASK | ZEND_ACC_STATIC))) {
 2319| 						/* flags are identical, now the value needs to be checked */
 2320| 						if (flags & ZEND_ACC_STATIC) {
```

### Turn 4  _(tok 4446+116, stop=tool_use)_

**Reasoning:** In other words, the call site at Zend/zend_compile.c:2306 is inside `zend_do_traits_property_binding`.

Next, let me check Zend/zend_object_handlers.c:403.

- `read_file(end_line=410, path=Zend/zend_object_handlers.c, start_line=370, version=old)` →

```
Zend/zend_object_handlers.c lines 370-410 of 1684
  370| 			if (cache_slot) {
  371| 				CACHE_POLYMORPHIC_PTR_EX(cache_slot, ce, property_info);
  372| 			}
  373| 		}
  374| 	} else {
  375| 		if (cache_slot) {
  376| 			CACHE_POLYMORPHIC_PTR_EX(cache_slot, ce, NULL);
  377| 		}
  378| 		EG(std_property_info).flags = ZEND_ACC_PUBLIC;
  379| 		EG(std_property_info).name = member;
  380| 		EG(std_property_info).ce = ce;
  381| 		EG(std_property_info).offset = -1;
  382| 		property_info = &EG(std_property_info);
  383| 	}
  384| 	return property_info;
  385| }
  386| /* }}} */
  387| 
  388| ZEND_API struct _zend_property_info *zend_get_property_info(zend_class_entry *ce, zend_string *member, int silent TSRMLS_DC) /* {{{ */
  389| {
  390| 	return zend_get_property_info_quick(ce, member, silent, NULL TSRMLS_CC);
  391| }
  392| /* }}} */
  393| 
  394| ZEND_API int zend_check_property_access(zend_object *zobj, zend_string *prop_info_name TSRMLS_DC) /* {{{ */
  395| {
  396| 	zend_property_info *property_info;
  397| 	const char *class_name = NULL;
  398| 	const char *prop_name;
  399| 	zend_string *member;
  400| 	int prop_name_len;
  401| 
  402| 	if (prop_info_name->val[0] == 0) {
  403| 		zend_unmangle_property_name_ex(prop_info_name->val, prop_info_name->len, &class_name, &prop_name, &prop_name_len);
  404| 		member = zend_string_init(prop_name, prop_name_len, 0);
  405| 	} else {
  406| 		member = zend_string_copy(prop_info_name);
  407| 	}
  408| 	property_info = zend_get_property_info_quick(zobj->ce, member, 1, NULL TSRMLS_CC);
  409| 	zend_string_release(member);
  410| 	if (!property_info) {
```

### Turn 5  _(tok 5261+119, stop=tool_use)_

**Reasoning:** Next, let's check Zend/zend_vm_def.h:4815 and zend_vm_execute.h:16795. These are inside the opcode handlers ZEND_VM_HANDLER. Let's find the enclosing handlers.

- `read_file(end_line=4830, path=Zend/zend_vm_def.h, start_line=4760, version=old)` →

```
Zend/zend_vm_def.h lines 4760-4830 of 6034
 4760| 			if (pos == INVALID_IDX) {
 4761| 				/* reached end of iteration */
 4762| 				ZEND_VM_JMP(opline->op2.jmp_addr);
 4763| 			} else if (UNEXPECTED(ptr->ht != fe_ht)) {
 4764| 				ptr->ht = fe_ht;
 4765| 				pos = 0;
 4766| 			} else if (UNEXPECTED(fe_ht->nInternalPointer != ptr->pos)) {
 4767| 				if (fe_ht->u.flags & HASH_FLAG_PACKED) {
 4768| 					pos = ptr->h;
 4769| 				} else {
 4770| 					pos = fe_ht->arHash[ptr->h & fe_ht->nTableMask];
 4771| 					while (pos != INVALID_IDX) {
 4772| 						if (fe_ht->arData[pos].h == ptr->h && pos == ptr->pos) {
 4773| 							break;
 4774| 						}
 4775| 						pos = Z_NEXT(fe_ht->arData[pos].val);
 4776| 					}
 4777| 				}
 4778| 			}
 4779| 			while (1) {
 4780| 				if (UNEXPECTED(pos >= fe_ht->nNumUsed)) {
 4781| 					/* reached end of iteration */
 4782| 					ZEND_VM_JMP(opline->op2.jmp_addr);
 4783| 				}
 4784| 
 4785| 				p = fe_ht->arData + pos;
 4786| 				value = &p->val;
 4787| 				if (UNEXPECTED(Z_TYPE_P(value) == IS_UNDEF)) {
 4788| 					pos++;
 4789| 					continue;
 4790| 				} else if (UNEXPECTED(Z_TYPE_P(value) == IS_INDIRECT)) {
 4791| 					value = Z_INDIRECT_P(value);
 4792| 					if (UNEXPECTED(Z_TYPE_P(value) == IS_UNDEF)) {
 4793| 						pos++;
 4794| 						continue;
 4795| 					}
 4796| 				}
 4797| 
 4798| 				if (UNEXPECTED(!p->key)) {
 4799| 					if (opline->extended_value & ZEND_FE_FETCH_WITH_KEY) {
 4800| 						ZVAL_LONG(EX_VAR((opline+1)->result.var), p->h);
 4801| 					}
 4802| 					break;
 4803| 				} else if (zend_check_property_access(zobj, p->key TSRMLS_CC) == SUCCESS) {
 4804| 					if (opline->extended_value & ZEND_FE_FETCH_WITH_KEY) {
 4805| 						if (p->key->val[0]) {
 4806| 							if (IS_INTERNED(p->key)) {
 4807| 								ZVAL_INTERNED_STR(EX_VAR((opline+1)->result.var), p->key);
 4808| 							} else {
 4809| 								ZVAL_NEW_STR(EX_VAR((opline+1)->result.var), p->key);
 4810| 								GC_REFCOUNT(p->key)++;
 4811| 							}
 4812| 						} else {
 4813| 							const char *class_name, *prop_name;
 4814| 							int prop_name_len;
 4815| 							zend_unmangle_property_name_ex(
 4816| 								p->key->val, p->key->len, &class_name, &prop_name, &prop_name_len);
 4817| 							ZVAL_STRINGL(EX_VAR((opline+1)->result.var), prop_name, prop_name_len);
 4818| 						}
 4819| 					}
 4820| 					break;
 4821| 				}
 4822| 				pos++;
 4823| 			}
 4824| 			if (opline->extended_value & ZEND_FE_FETCH_BYREF) {
 4825| 				ZVAL_MAKE_REF(value);
 4826| 				Z_ADDREF_P(value);
 4827| 				ZVAL_REF(EX_VAR(opline->result.var), Z_REF_P(value));
 4828| 			} else {
 4829| 				ZVAL_COPY(EX_VAR(opline->result.var), value);
 4830| 			}
```

### Turn 6  _(tok 6596+96, stop=tool_use)_

**Reasoning:** I need to find the ZEND_VM_HANDLER that contains line 4815. Let me search upward.

- `grep(pattern=ZEND_VM_HANDLER\(, path_glob=Zend/zend_vm_def.h, version=old, max_results=50)` →

```
157 matches (showing 50)
Zend/zend_vm_def.h:28:ZEND_VM_HANDLER(1, ZEND_ADD, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:43:ZEND_VM_HANDLER(2, ZEND_SUB, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:58:ZEND_VM_HANDLER(3, ZEND_MUL, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:73:ZEND_VM_HANDLER(4, ZEND_DIV, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:88:ZEND_VM_HANDLER(5, ZEND_MOD, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:103:ZEND_VM_HANDLER(6, ZEND_SL, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:118:ZEND_VM_HANDLER(7, ZEND_SR, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:133:ZEND_VM_HANDLER(8, ZEND_CONCAT, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:148:ZEND_VM_HANDLER(15, ZEND_IS_IDENTICAL, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:163:ZEND_VM_HANDLER(16, ZEND_IS_NOT_IDENTICAL, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:179:ZEND_VM_HANDLER(17, ZEND_IS_EQUAL, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:195:ZEND_VM_HANDLER(18, ZEND_IS_NOT_EQUAL, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:211:ZEND_VM_HANDLER(19, ZEND_IS_SMALLER, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:227:ZEND_VM_HANDLER(20, ZEND_IS_SMALLER_OR_EQUAL, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:243:ZEND_VM_HANDLER(9, ZEND_BW_OR, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:258:ZEND_VM_HANDLER(10, ZEND_BW_AND, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:273:ZEND_VM_HANDLER(11, ZEND_BW_XOR, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:288:ZEND_VM_HANDLER(14, ZEND_BOOL_XOR, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:303:ZEND_VM_HANDLER(12, ZEND_BW_NOT, CONST|TMP|VAR|CV, ANY)
Zend/zend_vm_def.h:316:ZEND_VM_HANDLER(13, ZEND_BOOL_NOT, CONST|TMP|VAR|CV, ANY)
Zend/zend_vm_def.h:538:ZEND_VM_HANDLER(23, ZEND_ASSIGN_ADD, VAR|UNUSED|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:551:ZEND_VM_HANDLER(24, ZEND_ASSIGN_SUB, VAR|UNUSED|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:564:ZEND_VM_HANDLER(25, ZEND_ASSIGN_MUL, VAR|UNUSED|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:577:ZEND_VM_HANDLER(26, ZEND_ASSIGN_DIV, VAR|UNUSED|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:590:ZEND_VM_HANDLER(27, ZEND_ASSIGN_MOD, VAR|UNUSED|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:603:ZEND_VM_HANDLER(28, ZEND_ASSIGN_SL, VAR|UNUSED|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:616:ZEND_VM_HANDLER(29, ZEND_ASSIGN_SR, VAR|UNUSED|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:629:ZEND_VM_HANDLER(30, ZEND_ASSIGN_CONCAT, VAR|UNUSED|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:642:ZEND_VM_HANDLER(31, ZEND_ASSIGN_BW_OR, VAR|UNUSED|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:655:ZEND_VM_HANDLER(32, ZEND_ASSIGN_BW_AND, VAR|UNUSED|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:668:ZEND_VM_HANDLER(33, ZEND_ASSIGN_BW_XOR, VAR|UNUSED|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:763:ZEND_VM_HANDLER(132, ZEND_PRE_INC_OBJ, VAR|UNUSED|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:768:ZEND_VM_HANDLER(133, ZEND_PRE_DEC_OBJ, VAR|UNUSED|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:851:ZEND_VM_HANDLER(134, ZEND_POST_INC_OBJ, VAR|UNUSED|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:856:ZEND_VM_HANDLER(135, ZEND_POST_DEC_OBJ, VAR|UNUSED|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:861:ZEND_VM_HANDLER(34, ZEND_PRE_INC, VAR|CV, ANY)
Zend/zend_vm_def.h:917:ZEND_VM_HANDLER(35, ZEND_PRE_DEC, VAR|CV, ANY)
Zend/zend_vm_def.h:973:ZEND_VM_HANDLER(36, ZEND_POST_INC, VAR|CV, ANY)
Zend/zend_vm_def.h:1028:ZEND_VM_HANDLER(37, ZEND_POST_DEC, VAR|CV, ANY)
Zend/zend_vm_def.h:1083:ZEND_VM_HANDLER(40, ZEND_ECHO, CONST|TMP|VAR|CV, ANY)
Zend/zend_vm_def.h:1099:ZEND_VM_HANDLER(41, ZEND_PRINT, CONST|TMP|VAR|CV, ANY)
Zend/zend_vm_def.h:1224:ZEND_VM_HANDLER(80, ZEND_FETCH_R, CONST|TMP|VAR|CV, UNUSED|CONST|VAR)
Zend/zend_vm_def.h:1229:ZEND_VM_HANDLER(83, ZEND_FETCH_W, CONST|TMP|VAR|CV, UNUSED|CONST|VAR)
Zend/zend_vm_def.h:1234:ZEND_VM_HANDLER(86, ZEND_FETCH_RW, CONST|TMP|VAR|CV, UNUSED|CONST|VAR)
Zend/zend_vm_def.h:1239:ZEND_VM_HANDLER(92, ZEND_FETCH_FUNC_ARG, CONST|TMP|VAR|CV, UNUSED|CONST|VAR)
Zend/zend_vm_def.h:1250:ZEND_VM_HANDLER(95, ZEND_FETCH_UNSET, CONST|TMP|VAR|CV, UNUSED|CONST|VAR)
Zend/zend_vm_def.h:1255:ZEND_VM_HANDLER(89, ZEND_FETCH_IS, CONST|TMP|VAR|CV, UNUSED|CONST|VAR)
Zend/zend_vm_def.h:1260:ZEND_VM_HANDLER(81, ZEND_FETCH_DIM_R, CONST|TMP|VAR|CV, CONST|TMP|VAR|CV)
Zend/zend_vm_def.h:1277:ZEND_VM_HANDLER(84, ZEND_FETCH_DIM_W, VAR|CV, CONST|TMP|VAR|UNUSED|CV)
Zend/zend_vm_def.h:1303:ZEND_VM_HANDLER(87, ZEND_FETCH_DIM_RW, VAR|CV, CONST|TMP|VAR|UNUSED|CV)
```

_(budget of 20,000 tokens exhausted — forcing submission)_

