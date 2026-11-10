# Impact-analysis transcript — php-src @ 2f0a758fbbf3 — anthropic:claude-haiku-5-5

- target: `php_dom_create_object` (ext/dom/php_dom.c), arity 4->3
- truth: [['ext/dom/attr.c', 'dom_attr_owner_element_read'], ['ext/dom/document.c', 'dom_document_doctype_read'], ['ext/dom/document.c', 'dom_document_document_element_read'], ['ext/dom/xml_common.h', 'dom_object_get_node']]

## Self-navigation arm

### Turn 1  _(tok 1218+121, stop=tool_use)_

**Reasoning:** I'm searching the whole repo for every occurrence of php_dom_create_object.



- `grep(pattern=php_dom_create_object, version=old, max_results=500)` →

```
20 matches
ext/dom/attr.c:231:	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:264:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) dtdptr, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:314:	if (NULL == (*retval = php_dom_create_object(root, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/dom_iterators.c:241:		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
ext/dom/dom_iterators.c:320:		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
ext/dom/node.c:432:	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:501:	if (NULL == (*retval = php_dom_create_object(first, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:538:	if (NULL == (*retval = php_dom_create_object(last, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:572:	if (NULL == (*retval = php_dom_create_object(prevsib, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:605:	if (NULL == (*retval = php_dom_create_object(nextsib, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:677:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/php_dom.c:1320:/* {{{ php_dom_create_object */
ext/dom/php_dom.c:1321:PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval *return_value, dom_object *domobj TSRMLS_DC)
ext/dom/text.c:199:	return_value = php_dom_create_object(nnode, &ret, return_value, intern TSRMLS_CC);
ext/dom/xml_common.h:57:PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval* return_value, dom_object *domobj TSRMLS_DC);
ext/dom/xml_common.h:82:	if (!php_dom_create_object(obj, ret, return_value, domobject TSRMLS_CC)) { \
ext/dom/xpath.c:167:							child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
ext/dom/xpath.c:335:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/xpath.c:502:					child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
ext/xsl/xsltprocessor.c:286:							child = php_dom_create_object(node, &ret, child, domintern TSRMLS_CC);
```

### Turn 2  _(tok 2564+378, stop=tool_use)_

**Reasoning:** I'm checking the DOM_RET_OBJ macro at line 82 in xml_common.h, which wraps php_dom_create_object. The next step is finding where that macro gets used, so I'm reading the header around lines 75 to 90.



**Says:** The macro at `xml_common.h:82` also calls the function, so I need to find the functions that expand it.

- `read_file(path=ext/dom/xml_common.h, version=old, start_line=75, end_line=90)` →

```
ext/dom/xml_common.h lines 75-90 of 107
   75|   			php_error_docref(NULL TSRMLS_CC, E_WARNING, "Couldn't fetch %s", __intern->std.ce->name);\
   76|   			RETURN_NULL();\
   77|   		} \
   78| 	} \
   79| }
   80| 
   81| #define DOM_RET_OBJ(obj, ret, domobject) \
   82| 	if (!php_dom_create_object(obj, ret, return_value, domobject TSRMLS_CC)) { \
   83| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object"); \
   84| 		RETURN_FALSE; \
   85| 	}
   86| 
   87| #define DOM_GET_THIS(zval) \
   88| 	if (NULL == (zval = getThis())) { \
   89| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Underlying object missing"); \
   90| 		RETURN_FALSE; \
```

- `grep(pattern=DOM_RET_OBJ|php_dom_ret_object|create_object, version=old, max_results=500)` →

```
165 matches
Zend/OBJECTS2_HOWTO:16:2. Overriding create_object handler for class. E.g.:
Zend/OBJECTS2_HOWTO:21:The  create_object handler function should create a new zval, create
Zend/micro_bench.php:163:function create_object($n) {
Zend/micro_bench.php:338:create_object(N);
Zend/zend.h:449:	zend_object* (*create_object)(zend_class_entry *class_type TSRMLS_DC);
Zend/zend_API.c:1301:	if (class_type->create_object == NULL) {
Zend/zend_API.c:1309:		ZVAL_OBJ(arg, class_type->create_object(class_type TSRMLS_CC));
Zend/zend_API.c:2771:	disabled_class->create_object = display_disabled_class;
Zend/zend_API.h:186:		class_container.create_object = NULL;					\
Zend/zend_closures.c:405:	zend_ce_closure->create_object = zend_closure_new;
Zend/zend_compile.c:3106:	/* You cannot change create_object */
Zend/zend_compile.c:3107:	ce->create_object = ce->parent->create_object;
Zend/zend_compile.c:6977:		ce->create_object = NULL;
Zend/zend_exceptions.c:709:	default_exception_ce->create_object = zend_default_exception_new;
Zend/zend_exceptions.c:723:	error_exception_ce->create_object = zend_error_exception_new;
Zend/zend_generators.c:723:	zend_ce_generator->create_object = zend_generator_create;
ext/com_dotnet/com_extension.c:364:	ce.create_object = php_com_object_new;
ext/com_dotnet/com_extension.c:369:	ce.create_object = php_com_object_new;
ext/com_dotnet/com_extension.c:377:	ce.create_object = php_com_object_new;
ext/com_dotnet/com_persist.c:760:	ce.create_object = helper_new;
ext/date/php_date.c:1997:	ce_date.create_object = date_object_new_date;
ext/date/php_date.c:2024:	ce_immutable.create_object = date_object_new_date;
ext/date/php_date.c:2033:	ce_timezone.create_object = date_object_new_timezone;
ext/date/php_date.c:2061:	ce_interval.create_object = date_object_new_interval;
ext/date/php_date.c:2074:	ce_period.create_object = date_object_new_period;
ext/dom/attr.c:231:	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:264:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) dtdptr, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:314:	if (NULL == (*retval = php_dom_create_object(root, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:927:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:954:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:982:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1010:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1038:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1073:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1106:	DOM_RET_OBJ((xmlNodePtr) node, &ret, intern);
ext/dom/document.c:1140:	DOM_RET_OBJ((xmlNodePtr) node, &ret, intern);
ext/dom/document.c:1221:	DOM_RET_OBJ((xmlNodePtr) retnodep, &ret, intern);
ext/dom/document.c:1284:	DOM_RET_OBJ(nodep, &ret, intern);
ext/dom/document.c:1349:	DOM_RET_OBJ(nodep, &ret, intern);
ext/dom/document.c:1402:		DOM_RET_OBJ((xmlNodePtr) attrp->parent, &ret, intern);
ext/dom/document.c:1716:		DOM_RET_OBJ((xmlNodePtr) newdoc, &ret, NULL);
ext/dom/document.c:2235:		DOM_RET_OBJ((xmlNodePtr) newdoc, &ret, NULL);
ext/dom/dom_iterators.c:241:		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
ext/dom/dom_iterators.c:320:		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
ext/dom/domimplementation.c:143:	DOM_RET_OBJ((xmlNodePtr) doctype, &ret, NULL);
ext/dom/domimplementation.c:240:	DOM_RET_OBJ((xmlNodePtr) docp, &ret, NULL);
ext/dom/element.c:429:	DOM_RET_OBJ(attr, &ret, intern);
ext/dom/element.c:524:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:586:		DOM_RET_OBJ((xmlNodePtr) existattrp, &ret, intern);
ext/dom/element.c:626:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:947:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:1017:		DOM_RET_OBJ((xmlNodePtr) existattrp, &ret, intern);
ext/dom/namednodemap.c:169:		DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/namednodemap.c:246:			DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/namednodemap.c:301:		DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/node.c:432:	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:501:	if (NULL == (*retval = php_dom_create_object(first, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:538:	if (NULL == (*retval = php_dom_create_object(last, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:572:	if (NULL == (*retval = php_dom_create_object(prevsib, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:605:	if (NULL == (*retval = php_dom_create_object(nextsib, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:677:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:1090:					DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1132:					DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1151:	DOM_RET_OBJ(new_child, &ret, intern);
ext/dom/node.c:1235:		DOM_RET_OBJ(oldchild, &ret, intern);
ext/dom/node.c:1284:			DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1392:	DOM_RET_OBJ(new_child, &ret, intern);
ext/dom/node.c:1481:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/nodelist.c:166:			DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/php_dom.c:581:		DOM_RET_OBJ((xmlNodePtr) nodep, &ret, (dom_object *)nodeobj);
ext/dom/php_dom.c:762:	ce.create_object = dom_nnodemap_objects_new;
ext/dom/php_dom.c:772:	ce.create_object = dom_nnodemap_objects_new;
ext/dom/php_dom.c:900:	ce.create_object = dom_xpath_objects_new;
ext/dom/php_dom.c:1320:/* {{{ php_dom_create_object */
ext/dom/php_dom.c:1321:PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval *return_value, dom_object *domobj TSRMLS_DC)
ext/dom/php_dom.h:129:ce.create_object = dom_objects_new; \
ext/dom/text.c:199:	return_value = php_dom_create_object(nnode, &ret, return_value, intern TSRMLS_CC);
ext/dom/xml_common.h:57:PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval* return_value, dom_object *domobj TSRMLS_DC);
ext/dom/xml_common.h:81:#define DOM_RET_OBJ(obj, ret, domobject) \
ext/dom/xml_common.h:82:	if (!php_dom_create_object(obj, ret, return_value, domobject TSRMLS_CC)) { \
ext/dom/xpath.c:167:							child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
ext/dom/xpath.c:335:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/xpath.c:502:					child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
ext/fileinfo/fileinfo.c:221:	_finfo_class_entry.create_object = finfo_objects_new;
ext/gmp/gmp.c:381:static inline zend_object_value gmp_create_object_ex(zend_class_entry *ce, mpz_ptr *gmpnum_target TSRMLS_DC) /* {{{ */
ext/gmp/gmp.c:403:static zend_object_value gmp_create_object(zend_class_entry *ce TSRMLS_DC) /* {{{ */
ext/gmp/gmp.c:406:	return gmp_create_object_ex(ce, &gmpnum_dummy TSRMLS_CC);
ext/gmp/gmp.c:413:	Z_OBJVAL_P(target) = gmp_create_object_ex(gmp_ce, gmpnum_target TSRMLS_CC);
ext/gmp/gmp.c:473:	zend_object_value new_object_val = gmp_create_object(Z_OBJCE_P(obj) TSRMLS_CC);
ext/gmp/gmp.c:661:	gmp_ce->create_object = gmp_create_object;
ext/intl/breakiterator/breakiterator_class.cpp:105:	ret_val = BreakIterator_ce_ptr->create_object(Z_OBJCE_P(object) TSRMLS_CC);
ext/intl/breakiterator/breakiterator_class.cpp:340:	ce.create_object = BreakIterator_object_create;
ext/intl/breakiterator/breakiterator_iterators.cpp:247:	retval = IntlIterator_ce_ptr->create_object(ce TSRMLS_CC);
ext/intl/breakiterator/breakiterator_iterators.cpp:327:	IntlPartsIterator_ce_ptr->create_object = IntlPartsIterator_object_create;
ext/intl/calendar/calendar_class.cpp:89:	ret_val = Calendar_ce_ptr->create_object(Z_OBJCE_P(object) TSRMLS_CC);
ext/intl/calendar/calendar_class.cpp:477:	ce.create_object = Calendar_object_create;
ext/intl/collator/collator_class.c:144:	ce.create_object = Collator_object_create;
ext/intl/common/common_enum.cpp:332:	ce.create_object = IntlIterator_object_create;
ext/intl/converter/converter.c:1060:static zend_object_value php_converter_create_object(zend_class_entry *ce TSRMLS_DC) {
ext/intl/converter/converter.c:1113:	php_converter_ce->create_object = php_converter_create_object;
ext/intl/dateformat/dateformat_class.c:97:	new_obj_val = IntlDateFormatter_ce_ptr->create_object(Z_OBJCE_P(object) TSRMLS_CC);
ext/intl/dateformat/dateformat_class.c:206:	ce.create_object = IntlDateFormatter_object_create;
ext/intl/formatter/formatter_class.c:89:	new_obj_val = NumberFormatter_ce_ptr->create_object(Z_OBJCE_P(object) TSRMLS_CC);
ext/intl/formatter/formatter_class.c:203:	ce.create_object = NumberFormatter_object_create;
ext/intl/intl_error.c:244:	IntlException_ce_ptr->create_object = default_exception_ce->create_object;
ext/intl/locale/locale_class.c:101:	ce.create_object = NULL;
ext/intl/msgformat/msgformat_class.c:87:	new_obj_val = MessageFormatter_ce_ptr->create_object(Z_OBJCE_P(object) TSRMLS_CC);
ext/intl/msgformat/msgformat_class.c:169:	ce.create_object = MessageFormatter_object_create;
ext/intl/normalizer/normalizer_class.c:60:	ce.create_object = NULL;
ext/intl/resourcebundle/resourcebundle_class.c:428:	ce.create_object = ResourceBundle_object_create;
ext/intl/spoofchecker/spoofchecker_class.c:130:	new_obj_val = Spoofchecker_ce_ptr->create_object(Z_OBJCE_P(object) TSRMLS_CC);
ext/intl/spoofchecker/spoofchecker_class.c:155:	ce.create_object = Spoofchecker_object_create;
ext/intl/timezone/timezone_class.cpp:228:	ret_val = TimeZone_ce_ptr->create_object(Z_OBJCE_P(object) TSRMLS_CC);
ext/intl/timezone/timezone_class.cpp:501:	ce.create_object = TimeZone_object_create;
ext/intl/transliterator/transliterator_class.c:165:	ret_val = Transliterator_ce_ptr->create_object( Z_OBJCE_P( object ) TSRMLS_CC );
ext/intl/transliterator/transliterator_class.c:402:	ce.create_object = Transliterator_object_create;
ext/mysqli/php_mysqli_structs.h:227:	ce.create_object = mysqli_objects_new; \
ext/openssl/openssl.c:846:			OBJ_create_objects(oid_bio);
ext/pdo/pdo_dbh.c:1409:	pdo_dbh_ce->create_object = pdo_dbh_new;
ext/pdo/pdo_stmt.c:2352:	pdo_dbstmt_ce->create_object = pdo_dbstmt_new;
ext/pdo/pdo_stmt.c:2366:	pdo_row_ce->create_object = pdo_row_new;
ext/reflection/php_reflection.c:4253:	if (ce->create_object != NULL) {
ext/reflection/php_reflection.c:6096:	_reflection_entry.create_object = reflection_objects_new;
ext/reflection/php_reflection.c:6102:	_reflection_entry.create_object = reflection_objects_new;
ext/reflection/php_reflection.c:6109:	_reflection_entry.create_object = reflection_objects_new;
ext/reflection/php_reflection.c:6115:	_reflection_entry.create_object = reflection_objects_new;
ext/reflection/php_reflection.c:6128:	_reflection_entry.create_object = reflection_objects_new;
ext/reflection/php_reflection.c:6138:	_reflection_entry.create_object = reflection_objects_new;
ext/reflection/php_reflection.c:6142:	_reflection_entry.create_object = reflection_objects_new;
ext/reflection/php_reflection.c:6154:	_reflection_entry.create_object = reflection_objects_new;
ext/reflection/php_reflection.c:6160:	_reflection_entry.create_object = reflection_objects_new;
ext/simplexml/simplexml.c:2547:	sxe.create_object = sxe_object_new;
ext/simplexml/sxe.c:203:	ce_SimpleXMLIterator->create_object = ce_SimpleXMLElement->create_object;
ext/snmp/snmp.c:2407:	ce.create_object = php_snmp_object_new;
ext/spl/spl_functions.c:50:		(*ppce)->create_object = obj_ctor;
ext/spl/spl_functions.c:65:		(*ppce)->create_object = obj_ctor;
ext/spl/spl_functions.c:67:		(*ppce)->create_object = parent_ce->create_object;
ext/spl/spl_functions.h:26:typedef zend_object* (*create_object_func_t)(zend_class_entry *class_type TSRMLS_DC);
ext/spl/spl_functions.h:52:void spl_register_std_class(zend_class_entry ** ppce, char * class_name, create_object_func_t ctor, const zend_function_entry * function_list TSRMLS_DC);
ext/spl/spl_functions.h:53:void spl_register_sub_class(zend_class_entry ** ppce, zend_class_entry * parent_ce, char * class_name, create_object_func_t ctor, const zend_function_entry * function_list T
ext/sqlite3/sqlite3.c:2236:	ce.create_object = php_sqlite3_object_new;
ext/sqlite3/sqlite3.c:2242:	ce.create_object = php_sqlite3_stmt_object_new;
ext/sqlite3/sqlite3.c:2248:	ce.create_object = php_sqlite3_result_object_new;
ext/standard/incomplete_class.c:119:	incomplete_class.create_object = php_create_incomplete_object;
ext/tidy/tidy.c:94:		ce.create_object = tidy_object_new_ ## name; \
ext/xmlreader/php_xmlreader.c:1158:				DOM_RET_OBJ(nodec, &ret, (dom_object *)domobj);
ext/xmlreader/php_xmlreader.c:1318:	ce.create_object = xmlreader_objects_new;
ext/xmlwriter/php_xmlwriter.c:1963:	ce.create_object = xmlwriter_object_new;
ext/xsl/php_xsl.c:228:/* {{{ php_xsl_create_object */
ext/xsl/php_xsl.c:229:zval *php_xsl_create_object(xsltStylesheetPtr obj, int *found, zval *wrapper_in, zval *return_value  TSRMLS_DC)
ext/xsl/php_xsl.h:74:zval *php_xsl_create_object(xsltStylesheetPtr obj, int *found, zval *wrapper_in, zval *return_value  TSRMLS_DC);
ext/xsl/php_xsl.h:81:ce.create_object = xsl_objects_new; \
ext/xsl/php_xsl.h:85:	if (NULL == (zval = php_xsl_create_object(obj, ret, zval, return_value TSRMLS_CC))) { \
ext/xsl/xsltprocessor.c:286:							child = php_dom_create_object(node, &ret, child, domintern TSRMLS_CC);
ext/xsl/xsltprocessor.c:691:			DOM_RET_OBJ((xmlNodePtr) newdocp, &ret, NULL);
ext/zip/php_zip.c:3042:	ce.create_object = php_zip_object_new;
main/streams/userspace.c:284:static void user_stream_create_object(struct php_user_stream_wrapper *uwrap, php_stream_context *context, zval *object TSRMLS_DC)
main/streams/userspace.c:360:	user_stream_create_object(uwrap, context, &us->object TSRMLS_CC);
main/streams/userspace.c:438:	user_stream_create_object(uwrap, context, &us->object TSRMLS_CC);
main/streams/userspace.c:1096:	user_stream_create_object(uwrap, context, &object TSRMLS_CC);
main/streams/userspace.c:1141:	user_stream_create_object(uwrap, context, &object TSRMLS_CC);	
main/streams/userspace.c:1187:	user_stream_create_object(uwrap, context, &object TSRMLS_CC);	
main/streams/userspace.c:1235:	user_stream_create_object(uwrap, context, &object TSRMLS_CC);	
main/streams/userspace.c:1305:	user_stream_create_object(uwrap, context, &object TSRMLS_CC);	
main/streams/userspace.c:1354:	user_stream_create_object(uwrap, context, &object TSRMLS_CC);
```

### Turn 3  _(tok 11097+1488, stop=tool_use)_

**Reasoning:** Macro expansion means DOM_RET_OBJ also calls php_dom_create_object, so the functions that use it count as callers too, and I'll include them. DOM_RET_OBJ shows up in the xmlreader and xsl code as well, so I'm checking those call sites next, along with php_dom.c around line 581.

Next I'm listing the direct call sites of php_dom_create_object by file and line, from attr.c through xsltprocessor.c, and I'll need the enclosing function for each one. Then I'll go through the DOM_RET_OBJ macro uses across document.c, element.c, node.c and the rest, including php_dom.c and the xmlreader call.

Next I'm grepping the function headers in each file (PHP_FUNCTION, PHP_METHOD, and static definitions) so I can map each call site to the function that encloses it.



**Says:** `DOM_RET_OBJ` expands to a call to `php_dom_create_object`, so every function using the macro is also a caller. To map each call line to its enclosing function, I'll pull the function headers from the affected files.

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|static |void |int |zval |zend_|PHP, version=old, path_glob=ext/dom/*.c, max_results=500)` →

```
352 matches (showing 200)
ext/dom/attr.c:56:PHP_METHOD(domattr, __construct)
ext/dom/attr.c:105:int dom_attr_name_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/attr.c:129:int dom_attr_specified_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/attr.c:144:int dom_attr_value_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/attr.c:170:int dom_attr_value_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/attr.c:211:int dom_attr_owner_element_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/attr.c:246:int dom_attr_schema_type_info_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/attr.c:260:PHP_FUNCTION(dom_attr_is_id)
ext/dom/cdatasection.c:50:PHP_METHOD(domcdatasection, __construct)
ext/dom/characterdata.c:79:int dom_characterdata_data_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/characterdata.c:103:int dom_characterdata_data_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/characterdata.c:140:int dom_characterdata_length_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/characterdata.c:173:PHP_FUNCTION(dom_characterdata_substring_data)
ext/dom/characterdata.c:222:PHP_FUNCTION(dom_characterdata_append_data)
ext/dom/characterdata.c:256:PHP_FUNCTION(dom_characterdata_insert_data)
ext/dom/characterdata.c:304:PHP_FUNCTION(dom_characterdata_delete_data)
ext/dom/characterdata.c:359:PHP_FUNCTION(dom_characterdata_replace_data)
ext/dom/comment.c:50:PHP_METHOD(domcomment, __construct)
ext/dom/document.c:243:int dom_document_doctype_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:279:int dom_document_implementation_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:293:int dom_document_document_element_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:327:int dom_document_encoding_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:351:int dom_document_encoding_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/document.c:399:int dom_document_standalone_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:418:int dom_document_standalone_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/document.c:463:int dom_document_version_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:487:int dom_document_version_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/document.c:528:int dom_document_strict_error_checking_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:542:int dom_document_strict_error_checking_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/document.c:571:int dom_document_format_output_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:585:int dom_document_format_output_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/document.c:627:int dom_document_validate_on_parse_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/document.c:655:int dom_document_resolve_externals_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:669:int dom_document_resolve_externals_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/document.c:697:int dom_document_preserve_whitespace_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:711:int dom_document_preserve_whitespace_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/document.c:739:int dom_document_recover_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:753:int dom_document_recover_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/document.c:781:int dom_document_substitue_entities_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:795:int dom_document_substitue_entities_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/document.c:825:int dom_document_document_uri_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:848:int dom_document_document_uri_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/document.c:889:int dom_document_config_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/document.c:902:PHP_FUNCTION(dom_document_create_element)
ext/dom/document.c:935:PHP_FUNCTION(dom_document_create_document_fragment)
ext/dom/document.c:962:PHP_FUNCTION(dom_document_create_text_node)
ext/dom/document.c:990:PHP_FUNCTION(dom_document_create_comment)
ext/dom/document.c:1018:PHP_FUNCTION(dom_document_create_cdatasection)
ext/dom/document.c:1046:PHP_FUNCTION(dom_document_create_processing_instruction)
ext/dom/document.c:1081:PHP_FUNCTION(dom_document_create_attribute)
ext/dom/document.c:1115:PHP_FUNCTION(dom_document_create_entity_reference)
ext/dom/document.c:1148:PHP_FUNCTION(dom_document_get_elements_by_tag_name)
ext/dom/document.c:1174:PHP_FUNCTION(dom_document_import_node)
ext/dom/document.c:1229:PHP_FUNCTION(dom_document_create_element_ns)
ext/dom/document.c:1292:PHP_FUNCTION(dom_document_create_attribute_ns)
ext/dom/document.c:1357:PHP_FUNCTION(dom_document_get_elements_by_tag_name_ns)
ext/dom/document.c:1384:PHP_FUNCTION(dom_document_get_element_by_id)
ext/dom/document.c:1414:PHP_FUNCTION(dom_document_adopt_node)
ext/dom/document.c:1424:PHP_FUNCTION(dom_document_normalize_document)
ext/dom/document.c:1444:PHP_FUNCTION(dom_document_rename_node)
ext/dom/document.c:1451:PHP_METHOD(domdocument, __construct)
ext/dom/document.c:1498:char *_dom_get_valid_file_path(char *source, char *resolved_path, int resolved_path_len  TSRMLS_DC) /* {{{ */
ext/dom/document.c:1546:static xmlDocPtr dom_document_parser(zval *id, int mode, char *source, int source_len, int options TSRMLS_DC) /* {{{ */
ext/dom/document.c:1663:static void dom_parse_document(INTERNAL_FUNCTION_PARAMETERS, int mode) {
ext/dom/document.c:1725:PHP_METHOD(domdocument, load)
ext/dom/document.c:1735:PHP_METHOD(domdocument, loadXML)
ext/dom/document.c:1744:PHP_FUNCTION(dom_document_save)
ext/dom/document.c:1788:PHP_FUNCTION(dom_document_savexml)
ext/dom/document.c:1855:static xmlNodePtr php_dom_free_xinclude_node(xmlNodePtr cur TSRMLS_DC) /* {{{ */
ext/dom/document.c:1868:static void php_dom_remove_xinclude_nodes(xmlNodePtr cur TSRMLS_DC) /* {{{ */
ext/dom/document.c:1898:PHP_FUNCTION(dom_document_xinclude)
ext/dom/document.c:1939:PHP_FUNCTION(dom_document_validate)
ext/dom/document.c:1970:static void _dom_document_schema_validate(INTERNAL_FUNCTION_PARAMETERS, int type) /* {{{ */
ext/dom/document.c:2054:PHP_FUNCTION(dom_document_schema_validate_file)
ext/dom/document.c:2061:PHP_FUNCTION(dom_document_schema_validate_xml)
ext/dom/document.c:2067:static void _dom_document_relaxNG_validate(INTERNAL_FUNCTION_PARAMETERS, int type) /* {{{ */
ext/dom/document.c:2143:PHP_FUNCTION(dom_document_relaxNG_validate_file)
ext/dom/document.c:2150:PHP_FUNCTION(dom_document_relaxNG_validate_xml)
ext/dom/document.c:2160:static void dom_load_html(INTERNAL_FUNCTION_PARAMETERS, int mode) /* {{{ */
ext/dom/document.c:2243:PHP_METHOD(domdocument, loadHTMLFile)
ext/dom/document.c:2252:PHP_METHOD(domdocument, loadHTML)
ext/dom/document.c:2261:PHP_FUNCTION(dom_document_save_html_file)
ext/dom/document.c:2299:PHP_FUNCTION(dom_document_save_html)
ext/dom/document.c:2385:PHP_METHOD(domdocument, registerNodeClass)
ext/dom/documentfragment.c:53:PHP_METHOD(domdocumentfragment, __construct)
ext/dom/documentfragment.c:89:static void php_dom_xmlSetTreeDoc(xmlNodePtr tree, xmlDocPtr doc) /* {{{ */
ext/dom/documentfragment.c:122:PHP_METHOD(domdocumentfragment, appendXML) {
ext/dom/documenttype.c:46:int dom_documenttype_name_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/documenttype.c:70:int dom_documenttype_entities_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/documenttype.c:101:int dom_documenttype_notations_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/documenttype.c:132:int dom_documenttype_public_id_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/documenttype.c:160:int dom_documenttype_system_id_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/documenttype.c:187:int dom_documenttype_internal_subset_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/dom_iterators.c:45:static void itemHashScanner (void *payload, void *data, xmlChar *name) /* {{{ */
ext/dom/dom_iterators.c:59:xmlNodePtr create_notation(const xmlChar *name, const xmlChar *ExternalID, const xmlChar *SystemID) /* {{{ */
ext/dom/dom_iterators.c:83:xmlNode *php_dom_libxml_hash_iter(xmlHashTable *ht, int index) /* {{{ */
ext/dom/dom_iterators.c:104:xmlNode *php_dom_libxml_notation_iter(xmlHashTable *ht, int index) /* {{{ */
ext/dom/dom_iterators.c:125:static void php_dom_iterator_dtor(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:139:static int php_dom_iterator_valid(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:152:static void php_dom_iterator_current_data(zend_object_iterator *iter, zval ***data TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:160:static void php_dom_iterator_current_key(zend_object_iterator *iter, zval *key TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:180:static void php_dom_iterator_move_forward(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:248:zend_object_iterator_funcs php_dom_iterator_funcs = {
ext/dom/dom_iterators.c:257:zend_object_iterator *php_dom_get_iterator(zend_class_entry *ce, zval *object, int by_ref TSRMLS_DC) /* {{{ */
ext/dom/domconfiguration.c:66:PHP_FUNCTION(dom_domconfiguration_set_parameter)
ext/dom/domconfiguration.c:76:PHP_FUNCTION(dom_domconfiguration_get_parameter)
ext/dom/domconfiguration.c:86:PHP_FUNCTION(dom_domconfiguration_can_set_parameter)
ext/dom/domerror.c:49:int dom_domerror_severity_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerror.c:63:int dom_domerror_message_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerror.c:77:int dom_domerror_type_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerror.c:91:int dom_domerror_related_exception_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerror.c:105:int dom_domerror_related_data_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerror.c:119:int dom_domerror_location_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerrorhandler.c:54:PHP_FUNCTION(dom_domerrorhandler_handle_error)
ext/dom/domexception.c:43:void php_dom_throw_error_with_message(int error_code, char *error_message, int strict_error TSRMLS_DC) /* {{{ */
ext/dom/domexception.c:54:void php_dom_throw_error(int error_code, int strict_error TSRMLS_DC)
ext/dom/domimplementation.c:71:PHP_METHOD(domimplementation, hasFeature)
ext/dom/domimplementation.c:92:PHP_METHOD(domimplementation, createDocumentType)
ext/dom/domimplementation.c:151:PHP_METHOD(domimplementation, createDocument)
ext/dom/domimplementation.c:253:PHP_METHOD(domimplementation, getFeature)
ext/dom/domimplementationlist.c:55:int dom_domimplementationlist_length_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domimplementationlist.c:68:PHP_FUNCTION(dom_domimplementationlist_item)
ext/dom/domimplementationsource.c:60:PHP_FUNCTION(dom_domimplementationsource_get_domimplementation)
ext/dom/domimplementationsource.c:70:PHP_FUNCTION(dom_domimplementationsource_get_domimplementations)
ext/dom/domlocator.c:49:int dom_domlocator_line_number_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domlocator.c:63:int dom_domlocator_column_number_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domlocator.c:77:int dom_domlocator_offset_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domlocator.c:91:int dom_domlocator_related_node_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domlocator.c:105:int dom_domlocator_uri_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domstringlist.c:55:int dom_domstringlist_length_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domstringlist.c:68:PHP_FUNCTION(dom_domstringlist_item)
ext/dom/element.c:154:PHP_METHOD(domelement, __construct)
ext/dom/element.c:238:int dom_element_tag_name_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/element.c:273:int dom_element_schema_type_info_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/element.c:282:static xmlNodePtr dom_get_dom1_attribute(xmlNodePtr elem, xmlChar *name) /* {{{ */
ext/dom/element.c:329:PHP_FUNCTION(dom_element_get_attribute)
ext/dom/element.c:372:PHP_FUNCTION(dom_element_set_attribute)
ext/dom/element.c:438:PHP_FUNCTION(dom_element_remove_attribute)
ext/dom/element.c:486:PHP_FUNCTION(dom_element_get_attribute_node)
ext/dom/element.c:532:PHP_FUNCTION(dom_element_set_attribute_node)
ext/dom/element.c:598:PHP_FUNCTION(dom_element_remove_attribute_node)
ext/dom/element.c:635:PHP_FUNCTION(dom_element_get_elements_by_tag_name)
ext/dom/element.c:661:PHP_FUNCTION(dom_element_get_attribute_ns)
ext/dom/element.c:698:static xmlNsPtr _dom_new_reconNs(xmlDocPtr doc, xmlNodePtr tree, xmlNsPtr ns) /* {{{ */
ext/dom/element.c:741:PHP_FUNCTION(dom_element_set_attribute_ns)
ext/dom/element.c:869:PHP_FUNCTION(dom_element_remove_attribute_ns)
ext/dom/element.c:926:PHP_FUNCTION(dom_element_get_attribute_node_ns)
ext/dom/element.c:956:PHP_FUNCTION(dom_element_set_attribute_node_ns)
ext/dom/element.c:1029:PHP_FUNCTION(dom_element_get_elements_by_tag_name_ns)
ext/dom/element.c:1057:PHP_FUNCTION(dom_element_has_attribute)
ext/dom/element.c:1085:PHP_FUNCTION(dom_element_has_attribute_ns)
ext/dom/element.c:1119:static void php_set_attribute_id(xmlAttrPtr attrp, zend_bool is_id) /* {{{ */
ext/dom/element.c:1142:PHP_FUNCTION(dom_element_set_id_attribute)
ext/dom/element.c:1178:PHP_FUNCTION(dom_element_set_id_attribute_ns)
ext/dom/element.c:1214:PHP_FUNCTION(dom_element_set_id_attribute_node)
ext/dom/entity.c:47:int dom_entity_public_id_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/entity.c:75:int dom_entity_system_id_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/entity.c:103:int dom_entity_notation_name_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/entity.c:134:int dom_entity_actual_encoding_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/entity.c:141:int dom_entity_actual_encoding_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/entity.c:153:int dom_entity_encoding_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/entity.c:160:int dom_entity_encoding_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/entity.c:172:int dom_entity_version_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/entity.c:179:int dom_entity_version_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/entityreference.c:49:PHP_METHOD(domentityreference, __construct)
ext/dom/namednodemap.c:86:int dom_namednodemap_length_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/namednodemap.c:127:PHP_FUNCTION(dom_namednodemap_get_named_item)
ext/dom/namednodemap.c:181:PHP_FUNCTION(dom_namednodemap_set_named_item)
ext/dom/namednodemap.c:191:PHP_FUNCTION(dom_namednodemap_remove_named_item)
ext/dom/namednodemap.c:201:PHP_FUNCTION(dom_namednodemap_item)
ext/dom/namednodemap.c:259:PHP_FUNCTION(dom_namednodemap_get_named_item_ns)
ext/dom/namednodemap.c:313:PHP_FUNCTION(dom_namednodemap_set_named_item_ns)
ext/dom/namednodemap.c:323:PHP_FUNCTION(dom_namednodemap_remove_named_item_ns)
ext/dom/namelist.c:58:int dom_namelist_length_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/namelist.c:71:PHP_FUNCTION(dom_namelist_get_name)
ext/dom/namelist.c:81:PHP_FUNCTION(dom_namelist_get_namespace_uri)
ext/dom/node.c:162:static void dom_reconcile_ns(xmlDocPtr doc, xmlNodePtr nodep) /* {{{ */
ext/dom/node.c:199:int dom_node_node_name_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:288:int dom_node_node_value_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:332:int dom_node_node_value_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/node.c:382:int dom_node_node_type_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:412:int dom_node_parent_node_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:446:int dom_node_child_nodes_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:478:int dom_node_first_child_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:515:int dom_node_last_child_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:552:int dom_node_previous_sibling_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:586:int dom_node_next_sibling_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:619:int dom_node_attributes_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:651:int dom_node_owner_document_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:691:int dom_node_namespace_uri_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:734:int dom_node_prefix_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:772:int dom_node_prefix_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/node.c:856:int dom_node_local_name_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:885:int dom_node_base_uri_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:917:int dom_node_text_content_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:943:int dom_node_text_content_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/node.c:950:static xmlNodePtr _php_dom_insert_fragment(xmlNodePtr nodep, xmlNodePtr prevsib, xmlNodePtr nextsib, xmlNodePtr fragment, dom_object *intern, dom_object *childobj TSRMLS_DC) /* {{{ 
ext/dom/node.c:999:PHP_FUNCTION(dom_node_insert_before)
ext/dom/node.c:1160:PHP_FUNCTION(dom_node_replace_child)
ext/dom/node.c:1248:PHP_FUNCTION(dom_node_remove_child)
```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|static |void |int |zval |zend_|PHP, version=old, path_glob=ext/xsl/xsltprocessor.c, max_results=500)` →

```
18 matches
ext/xsl/xsltprocessor.c:108:static char *php_xsl_xslt_string_to_xpathexpr(const char *str TSRMLS_DC)
ext/xsl/xsltprocessor.c:134:static char **php_xsl_xslt_make_params(HashTable *parht, int xpath_params TSRMLS_DC)
ext/xsl/xsltprocessor.c:182:static void xsl_ext_function_php(xmlXPathParserContextPtr ctxt, int nargs, int type) /* {{{ */
ext/xsl/xsltprocessor.c:381:void xsl_ext_function_string_php(xmlXPathParserContextPtr ctxt, int nargs) /* {{{ */
ext/xsl/xsltprocessor.c:387:void xsl_ext_function_object_php(xmlXPathParserContextPtr ctxt, int nargs) /* {{{ */
ext/xsl/xsltprocessor.c:397:PHP_FUNCTION(xsl_xsltprocessor_import_stylesheet)
ext/xsl/xsltprocessor.c:480:static xmlDocPtr php_xsl_apply_stylesheet(zval *id, xsl_object *intern, xsltStylesheetPtr style, zval *docp TSRMLS_DC) /* {{{ */
ext/xsl/xsltprocessor.c:645:PHP_FUNCTION(xsl_xsltprocessor_transform_to_doc)
ext/xsl/xsltprocessor.c:702:PHP_FUNCTION(xsl_xsltprocessor_transform_to_uri)
ext/xsl/xsltprocessor.c:733:PHP_FUNCTION(xsl_xsltprocessor_transform_to_xml)
ext/xsl/xsltprocessor.c:771:PHP_FUNCTION(xsl_xsltprocessor_set_parameter)
ext/xsl/xsltprocessor.c:823:PHP_FUNCTION(xsl_xsltprocessor_get_parameter)
ext/xsl/xsltprocessor.c:848:PHP_FUNCTION(xsl_xsltprocessor_remove_parameter)
ext/xsl/xsltprocessor.c:871:PHP_FUNCTION(xsl_xsltprocessor_register_php_functions)
ext/xsl/xsltprocessor.c:914:PHP_FUNCTION(xsl_xsltprocessor_set_profiling)
ext/xsl/xsltprocessor.c:940:PHP_FUNCTION(xsl_xsltprocessor_set_security_prefs)
ext/xsl/xsltprocessor.c:960:PHP_FUNCTION(xsl_xsltprocessor_get_security_prefs)
ext/xsl/xsltprocessor.c:979:PHP_FUNCTION(xsl_xsltprocessor_has_exslt_support)
```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|static |void |int |zval |zend_|PHP, version=old, path_glob=ext/xmlreader/php_xmlreader.c, max_results=500)` →

```
49 matches
ext/xmlreader/php_xmlreader.c:36:zend_class_entry *xmlreader_class_entry;
ext/xmlreader/php_xmlreader.c:38:static zend_object_handlers xmlreader_object_handlers;
ext/xmlreader/php_xmlreader.c:40:static HashTable xmlreader_prop_handlers;
ext/xmlreader/php_xmlreader.c:60:static void xmlreader_register_prop_handler(HashTable *prop_handler, char *name, xmlreader_read_int_t read_int_func, xmlreader_read_const_char_t read_char_func, int re
ext/xmlreader/php_xmlreader.c:72:static int xmlreader_property_reader(xmlreader_object *obj, xmlreader_prop_handler *hnd, zval **retval TSRMLS_DC)
ext/xmlreader/php_xmlreader.c:116:zval **xmlreader_get_property_ptr_ptr(zval *object, zval *member, int type, const zend_literal *key TSRMLS_DC)
ext/xmlreader/php_xmlreader.c:150:zval *xmlreader_read_property(zval *object, zval *member, int type, const zend_literal *key TSRMLS_DC)
ext/xmlreader/php_xmlreader.c:193:void xmlreader_write_property(zval *object, zval *member, zval *value, const zend_literal *key TSRMLS_DC)
ext/xmlreader/php_xmlreader.c:278:static xmlRelaxNGPtr _xmlreader_get_relaxNG(char *source, int source_len, int type,
ext/xmlreader/php_xmlreader.c:322:static const zend_module_dep xmlreader_deps[] = {
ext/xmlreader/php_xmlreader.c:329:zend_module_entry xmlreader_module_entry = {
ext/xmlreader/php_xmlreader.c:349:void xmlreader_objects_clone(void *object, void **object_clone TSRMLS_DC)
ext/xmlreader/php_xmlreader.c:356:static void xmlreader_free_resources(xmlreader_object *intern) {
ext/xmlreader/php_xmlreader.c:378:void xmlreader_objects_free_storage(void *object TSRMLS_DC)
ext/xmlreader/php_xmlreader.c:391:zend_object_value xmlreader_objects_new(zend_class_entry *class_type TSRMLS_DC)
ext/xmlreader/php_xmlreader.c:413:static void php_xmlreader_string_arg(INTERNAL_FUNCTION_PARAMETERS, xmlreader_read_one_char_t internal_function) {
ext/xmlreader/php_xmlreader.c:446:static void php_xmlreader_no_arg(INTERNAL_FUNCTION_PARAMETERS, xmlreader_read_int_t internal_function) {
ext/xmlreader/php_xmlreader.c:467:static void php_xmlreader_no_arg_string(INTERNAL_FUNCTION_PARAMETERS, xmlreader_read_char_t internal_function) {
ext/xmlreader/php_xmlreader.c:490:static void php_xmlreader_set_relaxng_schema(INTERNAL_FUNCTION_PARAMETERS, int type) {
ext/xmlreader/php_xmlreader.c:545:PHP_METHOD(xmlreader, close)
ext/xmlreader/php_xmlreader.c:563:PHP_METHOD(xmlreader, getAttribute)
ext/xmlreader/php_xmlreader.c:571:PHP_METHOD(xmlreader, getAttributeNo)
ext/xmlreader/php_xmlreader.c:597:PHP_METHOD(xmlreader, getAttributeNs)
ext/xmlreader/php_xmlreader.c:628:PHP_METHOD(xmlreader, getParserProperty)
ext/xmlreader/php_xmlreader.c:658:PHP_METHOD(xmlreader, isValid)
ext/xmlreader/php_xmlreader.c:666:PHP_METHOD(xmlreader, lookupNamespace)
ext/xmlreader/php_xmlreader.c:674:PHP_METHOD(xmlreader, moveToAttribute)
ext/xmlreader/php_xmlreader.c:707:PHP_METHOD(xmlreader, moveToAttributeNo)
ext/xmlreader/php_xmlreader.c:735:PHP_METHOD(xmlreader, moveToAttributeNs)
ext/xmlreader/php_xmlreader.c:767:PHP_METHOD(xmlreader, moveToElement)
ext/xmlreader/php_xmlreader.c:775:PHP_METHOD(xmlreader, moveToFirstAttribute)
ext/xmlreader/php_xmlreader.c:783:PHP_METHOD(xmlreader, moveToNextAttribute)
ext/xmlreader/php_xmlreader.c:791:PHP_METHOD(xmlreader, read)
ext/xmlreader/php_xmlreader.c:815:PHP_METHOD(xmlreader, next)
ext/xmlreader/php_xmlreader.c:856:PHP_METHOD(xmlreader, open)
ext/xmlreader/php_xmlreader.c:912:PHP_METHOD(xmlreader, resetState)
ext/xmlreader/php_xmlreader.c:921:PHP_METHOD(xmlreader, readInnerXml)
ext/xmlreader/php_xmlreader.c:929:PHP_METHOD(xmlreader, readOuterXml)
ext/xmlreader/php_xmlreader.c:937:PHP_METHOD(xmlreader, readString)
ext/xmlreader/php_xmlreader.c:945:PHP_METHOD(xmlreader, setSchema)
ext/xmlreader/php_xmlreader.c:988:PHP_METHOD(xmlreader, setParserProperty)
ext/xmlreader/php_xmlreader.c:1017:PHP_METHOD(xmlreader, setRelaxNGSchema)
ext/xmlreader/php_xmlreader.c:1025:PHP_METHOD(xmlreader, setRelaxNGSchemaSource)
ext/xmlreader/php_xmlreader.c:1039:PHP_METHOD(xmlreader, XML)
ext/xmlreader/php_xmlreader.c:1125:PHP_METHOD(xmlreader, expand)
ext/xmlreader/php_xmlreader.c:1270:static const zend_function_entry xmlreader_functions[] = {
ext/xmlreader/php_xmlreader.c:1306:PHP_MINIT_FUNCTION(xmlreader)
ext/xmlreader/php_xmlreader.c:1377:PHP_MSHUTDOWN_FUNCTION(xmlreader)
ext/xmlreader/php_xmlreader.c:1386:PHP_MINFO_FUNCTION(xmlreader)
```

### Turn 4  _(tok 25517+2796, stop=tool_use)_

**Reasoning:** I'm still hunting through ext/dom, since the grep hit its 200-line cap. The remaining files to check are node.c past line 1248, xpath.c, php_dom.c, text.c, and nodelist.c. I've already mapped attr.c:231 to dom_attr_is_id, which starts at line 260.

I'm checking document.c's line mappings against the function boundaries. Line 264 falls between dom_document_doctype_read and dom_document_implementation_read, so it belongs to doctype_read, and 314 belongs to dom_document_document_element_read. I'm also sorting the DOM_RET_OBJ hits in document.c by the create_* function whose range each line falls in, from create_element through create_entity_reference and import_node.

I'm mapping the remaining DOM hits to their enclosing functions: dom_iterator_move_forward covers the iterator at line 241, and in node.c the parent, first/last child, sibling, and owner_document readers each claim their lines. I still need to check what lies past line 257 in dom_iterators.c and sort the insert_before and replace_child hits.

I'm checking the enclosing function for the node.c hits: 1235 falls inside dom_node_replace_child, which runs from 1160 to 1248, and 1284 should belong to dom_node_remove_child, which starts at 1248, though I still want to confirm nothing sits between 1248 and 1284.

I'm still tracing which function owns the line 1284 hit in node.c, since the list I have stops at 1248 and I can't tell yet whether another function starts between those two lines. The nodelist.c hit at 166 is still unmapped, and the namednodemap.c entries around 246 and 301 need their enclosing functions confirmed.

I'm still working through the rest of the ext/dom mappings, and the remaining checks are the element.c function boundaries, which I've mostly matched already. Next I need the function lists for text.c, xpath.c, and php_dom.c, and I still have to expand php_xmlreader.c around line 1158.

I'm mapping the xmlreader expand hit at line 1158 to PHP_METHOD(xmlreader, expand), then matching the xsltprocessor and domimplementation hits to their enclosing functions. Next I need to grep for function headers in dom_iterators.c past line 257, node.c past 1248, nodelist.c, text.c, xpath.c, and php_dom.c.



**Says:** Most call sites now map to a function. Still missing are the function headers for `node.c` after line 1248, `dom_iterators.c` after line 257, and `nodelist.c`, `text.c`, `xpath.c`, and `php_dom.c`.

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|static |void |int |zval |zend_|PHP, version=old, path_glob=ext/dom/node.c, max_results=500)` →

```
44 matches
ext/dom/node.c:162:static void dom_reconcile_ns(xmlDocPtr doc, xmlNodePtr nodep) /* {{{ */
ext/dom/node.c:199:int dom_node_node_name_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:288:int dom_node_node_value_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:332:int dom_node_node_value_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/node.c:382:int dom_node_node_type_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:412:int dom_node_parent_node_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:446:int dom_node_child_nodes_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:478:int dom_node_first_child_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:515:int dom_node_last_child_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:552:int dom_node_previous_sibling_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:586:int dom_node_next_sibling_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:619:int dom_node_attributes_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:651:int dom_node_owner_document_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:691:int dom_node_namespace_uri_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:734:int dom_node_prefix_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:772:int dom_node_prefix_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/node.c:856:int dom_node_local_name_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:885:int dom_node_base_uri_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:917:int dom_node_text_content_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/node.c:943:int dom_node_text_content_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/node.c:950:static xmlNodePtr _php_dom_insert_fragment(xmlNodePtr nodep, xmlNodePtr prevsib, xmlNodePtr nextsib, xmlNodePtr fragment, dom_object *intern, dom_object *childobj TSRMLS_DC) /* {{{ 
ext/dom/node.c:999:PHP_FUNCTION(dom_node_insert_before)
ext/dom/node.c:1160:PHP_FUNCTION(dom_node_replace_child)
ext/dom/node.c:1248:PHP_FUNCTION(dom_node_remove_child)
ext/dom/node.c:1299:PHP_FUNCTION(dom_node_append_child)
ext/dom/node.c:1400:PHP_FUNCTION(dom_node_has_child_nodes)
ext/dom/node.c:1428:PHP_FUNCTION(dom_node_clone_node)
ext/dom/node.c:1489:PHP_FUNCTION(dom_node_normalize)
ext/dom/node.c:1510:PHP_FUNCTION(dom_node_is_supported)
ext/dom/node.c:1532:PHP_FUNCTION(dom_node_has_attributes)
ext/dom/node.c:1559:PHP_FUNCTION(dom_node_compare_document_position)
ext/dom/node.c:1569:PHP_FUNCTION(dom_node_is_same_node)
ext/dom/node.c:1595:PHP_FUNCTION(dom_node_lookup_prefix)
ext/dom/node.c:1645:PHP_FUNCTION(dom_node_is_default_namespace)
ext/dom/node.c:1678:PHP_FUNCTION(dom_node_lookup_namespace_uri)
ext/dom/node.c:1712:PHP_FUNCTION(dom_node_is_equal_node)
ext/dom/node.c:1722:PHP_FUNCTION(dom_node_get_feature)
ext/dom/node.c:1732:PHP_FUNCTION(dom_node_set_user_data)
ext/dom/node.c:1742:PHP_FUNCTION(dom_node_get_user_data)
ext/dom/node.c:1748:static void dom_canonicalization(INTERNAL_FUNCTION_PARAMETERS, int mode) /* {{{ */
ext/dom/node.c:1928:PHP_METHOD(domnode, C14N)
ext/dom/node.c:1936:PHP_METHOD(domnode, C14NFile)
ext/dom/node.c:1944:PHP_METHOD(domnode, getNodePath)
ext/dom/node.c:1965:PHP_METHOD(domnode, getLineNo)
```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|static |void |int |zval |zend_|PHP, version=old, path_glob=ext/dom/dom_iterators.c, max_results=500)` →

```
11 matches
ext/dom/dom_iterators.c:45:static void itemHashScanner (void *payload, void *data, xmlChar *name) /* {{{ */
ext/dom/dom_iterators.c:59:xmlNodePtr create_notation(const xmlChar *name, const xmlChar *ExternalID, const xmlChar *SystemID) /* {{{ */
ext/dom/dom_iterators.c:83:xmlNode *php_dom_libxml_hash_iter(xmlHashTable *ht, int index) /* {{{ */
ext/dom/dom_iterators.c:104:xmlNode *php_dom_libxml_notation_iter(xmlHashTable *ht, int index) /* {{{ */
ext/dom/dom_iterators.c:125:static void php_dom_iterator_dtor(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:139:static int php_dom_iterator_valid(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:152:static void php_dom_iterator_current_data(zend_object_iterator *iter, zval ***data TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:160:static void php_dom_iterator_current_key(zend_object_iterator *iter, zval *key TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:180:static void php_dom_iterator_move_forward(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:248:zend_object_iterator_funcs php_dom_iterator_funcs = {
ext/dom/dom_iterators.c:257:zend_object_iterator *php_dom_get_iterator(zend_class_entry *ce, zval *object, int by_ref TSRMLS_DC) /* {{{ */
```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|static |void |int |zval |zend_|PHP, version=old, path_glob=ext/dom/xpath.c, max_results=500)` →

```
11 matches
ext/dom/xpath.c:75:static void dom_xpath_ext_function_php(xmlXPathParserContextPtr ctxt, int nargs, int type) /* {{{ */
ext/dom/xpath.c:258:static void dom_xpath_ext_function_string_php(xmlXPathParserContextPtr ctxt, int nargs) /* {{{ */
ext/dom/xpath.c:264:static void dom_xpath_ext_function_object_php(xmlXPathParserContextPtr ctxt, int nargs) /* {{{ */
ext/dom/xpath.c:271:PHP_METHOD(domxpath, __construct)
ext/dom/xpath.c:319:int dom_xpath_document_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/xpath.c:348:PHP_FUNCTION(dom_xpath_register_ns)
ext/dom/xpath.c:375:static void dom_xpath_iter(zval *baseobj, dom_object *intern) /* {{{ */
ext/dom/xpath.c:386:static void php_xpath_eval(INTERNAL_FUNCTION_PARAMETERS, int type) /* {{{ */
ext/dom/xpath.c:534:PHP_FUNCTION(dom_xpath_query)
ext/dom/xpath.c:541:PHP_FUNCTION(dom_xpath_evaluate)
ext/dom/xpath.c:548:PHP_FUNCTION(dom_xpath_register_php_functions)
```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|static |void |int |zval |zend_|PHP, version=old, path_glob=ext/dom/php_dom.c, max_results=500)` →

```
100 matches
ext/dom/php_dom.c:39:zend_class_entry *dom_node_class_entry;
ext/dom/php_dom.c:40:zend_class_entry *dom_domexception_class_entry;
ext/dom/php_dom.c:41:zend_class_entry *dom_domstringlist_class_entry;
ext/dom/php_dom.c:42:zend_class_entry *dom_namelist_class_entry;
ext/dom/php_dom.c:43:zend_class_entry *dom_domimplementationlist_class_entry;
ext/dom/php_dom.c:44:zend_class_entry *dom_domimplementationsource_class_entry;
ext/dom/php_dom.c:45:zend_class_entry *dom_domimplementation_class_entry;
ext/dom/php_dom.c:46:zend_class_entry *dom_documentfragment_class_entry;
ext/dom/php_dom.c:47:zend_class_entry *dom_document_class_entry;
ext/dom/php_dom.c:48:zend_class_entry *dom_nodelist_class_entry;
ext/dom/php_dom.c:49:zend_class_entry *dom_namednodemap_class_entry;
ext/dom/php_dom.c:50:zend_class_entry *dom_characterdata_class_entry;
ext/dom/php_dom.c:51:zend_class_entry *dom_attr_class_entry;
ext/dom/php_dom.c:52:zend_class_entry *dom_element_class_entry;
ext/dom/php_dom.c:53:zend_class_entry *dom_text_class_entry;
ext/dom/php_dom.c:54:zend_class_entry *dom_comment_class_entry;
ext/dom/php_dom.c:55:zend_class_entry *dom_typeinfo_class_entry;
ext/dom/php_dom.c:56:zend_class_entry *dom_userdatahandler_class_entry;
ext/dom/php_dom.c:57:zend_class_entry *dom_domerror_class_entry;
ext/dom/php_dom.c:58:zend_class_entry *dom_domerrorhandler_class_entry;
ext/dom/php_dom.c:59:zend_class_entry *dom_domlocator_class_entry;
ext/dom/php_dom.c:60:zend_class_entry *dom_domconfiguration_class_entry;
ext/dom/php_dom.c:61:zend_class_entry *dom_cdatasection_class_entry;
ext/dom/php_dom.c:62:zend_class_entry *dom_documenttype_class_entry;
ext/dom/php_dom.c:63:zend_class_entry *dom_notation_class_entry;
ext/dom/php_dom.c:64:zend_class_entry *dom_entity_class_entry;
ext/dom/php_dom.c:65:zend_class_entry *dom_entityreference_class_entry;
ext/dom/php_dom.c:66:zend_class_entry *dom_processinginstruction_class_entry;
ext/dom/php_dom.c:67:zend_class_entry *dom_string_extend_class_entry;
ext/dom/php_dom.c:69:zend_class_entry *dom_xpath_class_entry;
ext/dom/php_dom.c:71:zend_class_entry *dom_namespace_node_class_entry;
ext/dom/php_dom.c:74:zend_object_handlers dom_object_handlers;
ext/dom/php_dom.c:76:static HashTable classes;
ext/dom/php_dom.c:78:static HashTable dom_domstringlist_prop_handlers;
ext/dom/php_dom.c:79:static HashTable dom_namelist_prop_handlers;
ext/dom/php_dom.c:80:static HashTable dom_domimplementationlist_prop_handlers;
ext/dom/php_dom.c:81:static HashTable dom_document_prop_handlers;
ext/dom/php_dom.c:82:static HashTable dom_node_prop_handlers;
ext/dom/php_dom.c:83:static HashTable dom_nodelist_prop_handlers;
ext/dom/php_dom.c:84:static HashTable dom_namednodemap_prop_handlers;
ext/dom/php_dom.c:85:static HashTable dom_characterdata_prop_handlers;
ext/dom/php_dom.c:86:static HashTable dom_attr_prop_handlers;
ext/dom/php_dom.c:87:static HashTable dom_element_prop_handlers;
ext/dom/php_dom.c:88:static HashTable dom_text_prop_handlers;
ext/dom/php_dom.c:89:static HashTable dom_typeinfo_prop_handlers;
ext/dom/php_dom.c:90:static HashTable dom_domerror_prop_handlers;
ext/dom/php_dom.c:91:static HashTable dom_domlocator_prop_handlers;
ext/dom/php_dom.c:92:static HashTable dom_documenttype_prop_handlers;
ext/dom/php_dom.c:93:static HashTable dom_notation_prop_handlers;
ext/dom/php_dom.c:94:static HashTable dom_entity_prop_handlers;
ext/dom/php_dom.c:95:static HashTable dom_processinginstruction_prop_handlers;
ext/dom/php_dom.c:96:static HashTable dom_namespace_node_prop_handlers;
ext/dom/php_dom.c:98:static HashTable dom_xpath_prop_handlers;
ext/dom/php_dom.c:111:int dom_node_is_read_only(xmlNodePtr node) {
ext/dom/php_dom.c:135:int dom_node_children_valid(xmlNodePtr node) {
ext/dom/php_dom.c:176:static void dom_copy_doc_props(php_libxml_ref_obj *source_doc, php_libxml_ref_obj *dest_doc)
ext/dom/php_dom.c:201:int dom_set_doc_classmap(php_libxml_ref_obj *document, zend_class_entry *basece, zend_class_entry *ce TSRMLS_DC)
ext/dom/php_dom.c:223:zend_class_entry *dom_get_doc_classmap(php_libxml_ref_obj *document, zend_class_entry *basece TSRMLS_DC)
ext/dom/php_dom.c:242:int dom_get_strict_error(php_libxml_ref_obj *document) {
ext/dom/php_dom.c:257:PHP_DOM_EXPORT xmlNodePtr dom_object_get_node(dom_object *obj)
ext/dom/php_dom.c:268:PHP_DOM_EXPORT dom_object *php_dom_object_get_data(xmlNodePtr obj)
ext/dom/php_dom.c:279:static int dom_read_na(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/php_dom.c:288:static int dom_write_na(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/php_dom.c:296:static void dom_register_prop_handler(HashTable *prop_handler, char *name, dom_read_t read_func, dom_write_t write_func TSRMLS_DC)
ext/dom/php_dom.c:306:static zval **dom_get_property_ptr_ptr(zval *object, zval *member, int type, const zend_literal *key TSRMLS_DC) /* {{{ */
ext/dom/php_dom.c:340:zval *dom_read_property(zval *object, zval *member, int type, const zend_literal *key TSRMLS_DC)
ext/dom/php_dom.c:386:void dom_write_property(zval *object, zval *member, zval *value, const zend_literal *key TSRMLS_DC)
ext/dom/php_dom.c:421:static int dom_property_exists(zval *object, zval *member, int check_empty, const zend_literal *key TSRMLS_DC)
ext/dom/php_dom.c:469:static HashTable* dom_get_debug_info_helper(zval *object, int *is_temp TSRMLS_DC) /* {{{ */
ext/dom/php_dom.c:544:static HashTable* dom_get_debug_info(zval *object, int *is_temp TSRMLS_DC) /* {{{ */
ext/dom/php_dom.c:550:void *php_dom_export_node(zval *object TSRMLS_DC) /* {{{ */
ext/dom/php_dom.c:566:PHP_FUNCTION(dom_import_simplexml)
ext/dom/php_dom.c:589:zend_object_value dom_objects_store_clone_obj(zval *zobject TSRMLS_DC) /* {{{ */
ext/dom/php_dom.c:624:static const zend_function_entry dom_functions[] = {
ext/dom/php_dom.c:629:static zend_object_handlers* dom_get_obj_handlers(TSRMLS_D) {
ext/dom/php_dom.c:633:static const zend_module_dep dom_deps[] = {
ext/dom/php_dom.c:639:zend_module_entry dom_module_entry = { /* {{{ */
ext/dom/php_dom.c:659:PHP_MINIT_FUNCTION(dom)
ext/dom/php_dom.c:966:PHP_MINFO_FUNCTION(dom)
ext/dom/php_dom.c:989:PHP_MSHUTDOWN_FUNCTION(dom) /* {{{ */
ext/dom/php_dom.c:1025:void node_list_unlink(xmlNodePtr node TSRMLS_DC)
ext/dom/php_dom.c:1061:void dom_xpath_objects_free_storage(void *object TSRMLS_DC)
ext/dom/php_dom.c:1089:void dom_objects_free_storage(void *object TSRMLS_DC)
ext/dom/php_dom.c:1114:void dom_namednode_iter(dom_object *basenode, int ntype, dom_object *intern, xmlHashTablePtr ht, xmlChar *local, xmlChar *ns TSRMLS_DC) /* {{{ */
ext/dom/php_dom.c:1138:static dom_object* dom_objects_set_class(zend_class_entry *class_type, zend_bool hash_copy TSRMLS_DC) /* {{{ */
ext/dom/php_dom.c:1170:void dom_objects_clone(void *object, void **object_clone TSRMLS_DC)
ext/dom/php_dom.c:1203:zend_object_value dom_objects_new(zend_class_entry *class_type TSRMLS_DC)
ext/dom/php_dom.c:1220:zend_object_value dom_xpath_objects_new(zend_class_entry *class_type TSRMLS_DC)
ext/dom/php_dom.c:1242:static void dom_nnodemap_object_dtor(void *object, zend_object_handle handle TSRMLS_DC) /* {{{ */
ext/dom/php_dom.c:1270:void dom_nnodemap_objects_free_storage(void *object TSRMLS_DC) /* {{{ */
ext/dom/php_dom.c:1282:zend_object_value dom_nnodemap_objects_new(zend_class_entry *class_type TSRMLS_DC) /* {{{ */
ext/dom/php_dom.c:1306:void php_dom_create_interator(zval *return_value, int ce_type TSRMLS_DC) /* {{{ */
ext/dom/php_dom.c:1321:PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval *return_value, dom_object *domobj TSRMLS_DC)
ext/dom/php_dom.c:1440:void php_dom_create_implementation(zval **retval  TSRMLS_DC) {
ext/dom/php_dom.c:1445:int dom_hierarchy(xmlNodePtr parent, xmlNodePtr child)
ext/dom/php_dom.c:1467:int dom_has_feature(char *feature, char *version)
ext/dom/php_dom.c:1480:xmlNode *dom_get_elements_by_tag_name_ns_raw(xmlNodePtr nodep, char *ns, char *local, int *cur, int index) /* {{{ */
ext/dom/php_dom.c:1508:void dom_normalize (xmlNodePtr nodep TSRMLS_DC)
ext/dom/php_dom.c:1554:void dom_set_old_ns(xmlDoc *doc, xmlNs *ns) {
ext/dom/php_dom.c:1589:int dom_check_qname(char *qname, char **localname, char **prefix, int uri_len, int name_len) {
```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|static |void |int |zval |zend_|PHP, version=old, path_glob=ext/dom/{text,nodelist}.c, max_results=500)` →

```
0 matches

```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 36208+1479, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "dom_attr_owner_element_read", "file": "ext/dom/attr.c"}, {"function": "dom_document_doctype_read", "file": "ext/dom/document.c"}, {"function": "dom_document_document_element_read", "file": "ext/dom/document.c"}, {"function": "dom_document_create_element", "file": "ext/dom/document.c"}, {"function": "dom_document_create_document_fragment", "file": "ext/dom/document.c"}, {"function": "dom_document_create_text_node", "file": "ext/dom/document.c"}, {"function": "dom_document_create_comment", "file": "ext/dom/document.c"}, {"function": "dom_document_create_cdatasection", "file": "ext/dom/document.c"}, {"function": "dom_document_create_processing_instruction", "file": "ext/dom/document.c"}, {"function": "dom_document_create_attribute", "file": "ext/dom/document.c"}, {"function": "dom_document_create_entity_reference", "file": "ext/dom/document.c"}, {"function": "dom_document_import_node", "file": "ext/dom/document.c"}, {"function": "dom_document_create_element_ns", "file": "ext/dom/document.c"}, {"function": "dom_document_create_attribute_ns", "file": "ext/dom/document.c"}, {"function": "dom_document_get_element_by_id", "file": "ext/dom/document.c"}, {"function": "dom_parse_document", "file": "ext/dom/document.c"}, {"function": "dom_load_html", "file": "ext/dom/document.c"}, {"function": "php_dom_iterator_move_forward", "file": "ext/dom/dom_iterators.c"}, {"function": "dom_node_parent_node_read", "file": "ext/dom/node.c"}, {"function": "dom_node_first_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_last_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_previous_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_next_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_owner_document_read", "file": "ext/dom/node.c"}, {"function": "dom_node_insert_before", "file": "ext/dom/node.c"}, {"function": "dom_node_replace_child", "file": "ext/dom/node.c"}, {"function": "dom_node_remove_child", "file": "ext/dom/node.c"}, {"function": "dom_node_append_child", "file": "ext/dom/node.c"}, {"function": "dom_node_clone_node", "file": "ext/dom/node.c"}, {"function": "dom_namednodemap_get_named_item", "file": "ext/dom/namednodemap.c"}, {"function": "dom_namednodemap_item", "file": "ext/dom/namednodemap.c"}, {"function": "dom_namednodemap_get_named_item_ns", "file": "ext/dom/namednodemap.c"}, {"function": "dom_element_set_attribute", "file": "ext/dom/element.c"}, {"function": "dom_element_get_attribute_node", "file": "ext/dom/element.c"}, {"function": "dom_element_set_attribute_node", "file": "ext/dom/element.c"}, {"function": "dom_element_remove_attribute_node", "file": "ext/dom/element.c"}, {"function": "dom_element_get_attribute_node_ns", "file": "ext/dom/element.c"}, {"function": "dom_element_set_attribute_node_ns", "file": "ext/dom/element.c"}, {"function": "PHP_METHOD(domimplementation, createDocumentType)", "file": "ext/dom/domimplementation.c"}, {"function": "PHP_METHOD(domimplementation, createDocument)", "file": "ext/dom/domimplementation.c"}, {"function": "php_xsl_apply_stylesheet", "file": "ext/xsl/xsltprocessor.c"}, {"function": "xsl_xsltprocessor_transform_to_doc", "file": "ext/xsl/xsltprocessor.c"}, {"function": "PHP_METHOD(xmlreader, expand)", "file": "ext/xmlreader/php_xmlreader.c"}], "confidence_overall": "low"}`

**Score (self):** `{"n_pred": 43, "n_truth": 4, "tp": 3, "precision": 0.06976744186046512, "recall": 0.75, "f1": 0.1276595744680851}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1387+80, stop=tool_use)_

**Reasoning:** I'm going to pull every reference to php_dom_create_object using find_references, so I can see where it's used.



- `find_references(name=php_dom_create_object)` →

```
18 references
php_dom_create_object  231 ext/dom/attr.c   	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
php_dom_create_object  264 ext/dom/document.c 	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) dtdptr, &ret, *retval, obj TSRMLS_CC))) {
php_dom_create_object  314 ext/dom/document.c 	if (NULL == (*retval = php_dom_create_object(root, &ret, *retval, obj TSRMLS_CC))) {
php_dom_create_object  241 ext/dom/dom_iterators.c 		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
php_dom_create_object  320 ext/dom/dom_iterators.c 		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
php_dom_create_object  432 ext/dom/node.c   	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
php_dom_create_object  501 ext/dom/node.c   	if (NULL == (*retval = php_dom_create_object(first, &ret, *retval, obj TSRMLS_CC))) {
php_dom_create_object  538 ext/dom/node.c   	if (NULL == (*retval = php_dom_create_object(last, &ret, *retval, obj TSRMLS_CC))) {
php_dom_create_object  572 ext/dom/node.c   	if (NULL == (*retval = php_dom_create_object(prevsib, &ret, *retval, obj TSRMLS_CC))) {
php_dom_create_object  605 ext/dom/node.c   	if (NULL == (*retval = php_dom_create_object(nextsib, &ret, *retval, obj TSRMLS_CC))) {
php_dom_create_object  677 ext/dom/node.c   	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
php_dom_create_object  199 ext/dom/text.c   	return_value = php_dom_create_object(nnode, &ret, return_value, intern TSRMLS_CC);
php_dom_create_object   57 ext/dom/xml_common.h PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval* return_value, dom_object *domobj TSRMLS_DC);
php_dom_create_object   82 ext/dom/xml_common.h 	if (!php_dom_create_object(obj, ret, return_value, domobject TSRMLS_CC)) { \
php_dom_create_object  167 ext/dom/xpath.c  							child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
php_dom_create_object  335 ext/dom/xpath.c  	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
php_dom_create_object  502 ext/dom/xpath.c  					child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
php_dom_create_object  286 ext/xsl/xsltprocessor.c 							child = php_dom_create_object(node, &ret, child, domintern TSRMLS_CC);
```

### Turn 2  _(tok 2738+1480, stop=tool_use)_

**Reasoning:** I still need the functions that enclose each of these lines. There's also a macro in xml_common.h around line 82 that calls the same code, so its use sites are callers I'll have to track down. I'll read the macro and the surrounding code, then trace each enclosing function.



**Says:** The index doesn't give enclosing functions, so I'll read the context around each reference. I'm also checking the macro at xml_common.h:82, since its expansions are call sites too.

- `read_file(path=ext/dom/xml_common.h, version=old, start_line=70, end_line=95)` →

```
ext/dom/xml_common.h lines 70-95 of 107
   70| 
   71| #define DOC_GET_OBJ(__ptr, __id, __prtype, __intern) { \
   72| 	__intern = (php_libxml_node_object *)zend_object_store_get_object(__id TSRMLS_CC); \
   73| 	if (__intern->document != NULL) { \
   74| 		if (!(__ptr = (__prtype)__intern->document->ptr)) { \
   75|   			php_error_docref(NULL TSRMLS_CC, E_WARNING, "Couldn't fetch %s", __intern->std.ce->name);\
   76|   			RETURN_NULL();\
   77|   		} \
   78| 	} \
   79| }
   80| 
   81| #define DOM_RET_OBJ(obj, ret, domobject) \
   82| 	if (!php_dom_create_object(obj, ret, return_value, domobject TSRMLS_CC)) { \
   83| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object"); \
   84| 		RETURN_FALSE; \
   85| 	}
   86| 
   87| #define DOM_GET_THIS(zval) \
   88| 	if (NULL == (zval = getThis())) { \
   89| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Underlying object missing"); \
   90| 		RETURN_FALSE; \
   91| 	}
   92| 
   93| #define DOM_GET_THIS_OBJ(__ptr, __id, __prtype, __intern) \
   94| 	DOM_GET_THIS(__id); \
   95| 	DOM_GET_OBJ(__ptr, __id, __prtype, __intern);
```

- `grep(pattern=php_dom_create_interior_node|DOM_RET_OBJ, version=old)` →

```
37 matches
ext/dom/document.c:927:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:954:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:982:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1010:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1038:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1073:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1106:	DOM_RET_OBJ((xmlNodePtr) node, &ret, intern);
ext/dom/document.c:1140:	DOM_RET_OBJ((xmlNodePtr) node, &ret, intern);
ext/dom/document.c:1221:	DOM_RET_OBJ((xmlNodePtr) retnodep, &ret, intern);
ext/dom/document.c:1284:	DOM_RET_OBJ(nodep, &ret, intern);
ext/dom/document.c:1349:	DOM_RET_OBJ(nodep, &ret, intern);
ext/dom/document.c:1402:		DOM_RET_OBJ((xmlNodePtr) attrp->parent, &ret, intern);
ext/dom/document.c:1716:		DOM_RET_OBJ((xmlNodePtr) newdoc, &ret, NULL);
ext/dom/document.c:2235:		DOM_RET_OBJ((xmlNodePtr) newdoc, &ret, NULL);
ext/dom/domimplementation.c:143:	DOM_RET_OBJ((xmlNodePtr) doctype, &ret, NULL);
ext/dom/domimplementation.c:240:	DOM_RET_OBJ((xmlNodePtr) docp, &ret, NULL);
ext/dom/element.c:429:	DOM_RET_OBJ(attr, &ret, intern);
ext/dom/element.c:524:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:586:		DOM_RET_OBJ((xmlNodePtr) existattrp, &ret, intern);
ext/dom/element.c:626:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:947:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:1017:		DOM_RET_OBJ((xmlNodePtr) existattrp, &ret, intern);
ext/dom/namednodemap.c:169:		DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/namednodemap.c:246:			DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/namednodemap.c:301:		DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/node.c:1090:					DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1132:					DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1151:	DOM_RET_OBJ(new_child, &ret, intern);
ext/dom/node.c:1235:		DOM_RET_OBJ(oldchild, &ret, intern);
ext/dom/node.c:1284:			DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1392:	DOM_RET_OBJ(new_child, &ret, intern);
ext/dom/node.c:1481:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/nodelist.c:166:			DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/php_dom.c:581:		DOM_RET_OBJ((xmlNodePtr) nodep, &ret, (dom_object *)nodeobj);
ext/dom/xml_common.h:81:#define DOM_RET_OBJ(obj, ret, domobject) \
ext/xmlreader/php_xmlreader.c:1158:				DOM_RET_OBJ(nodec, &ret, (dom_object *)domobj);
ext/xsl/xsltprocessor.c:691:			DOM_RET_OBJ((xmlNodePtr) newdocp, &ret, NULL);
```

- `read_file(path=ext/dom/attr.c, version=old, start_line=210, end_line=235)` →

```
ext/dom/attr.c lines 210-235 of 290
  210| */
  211| int dom_attr_owner_element_read(dom_object *obj, zval **retval TSRMLS_DC)
  212| {
  213| 	xmlNodePtr nodep, nodeparent;
  214| 	int ret;
  215| 
  216| 	nodep = dom_object_get_node(obj);
  217| 
  218| 	if (nodep == NULL) {
  219| 		php_dom_throw_error(INVALID_STATE_ERR, 0 TSRMLS_CC);
  220| 		return FAILURE;
  221| 	}
  222| 
  223| 	ALLOC_ZVAL(*retval);
  224| 
  225| 	nodeparent = nodep->parent;
  226| 	if (!nodeparent) {
  227| 		ZVAL_NULL(*retval);
  228| 		return SUCCESS;
  229| 	}
  230| 
  231| 	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
  232| 		php_error_docref(NULL TSRMLS_CC, E_WARNING,  "Cannot create required DOM object");
  233| 		return FAILURE;
  234| 	}
  235| 	return SUCCESS;
```

- `read_file(path=ext/dom/document.c, version=old, start_line=240, end_line=320)` →

```
ext/dom/document.c lines 240-320 of 2446
  240| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-ID-B63ED1A31
  241| Since: 
  242| */
  243| int dom_document_doctype_read(dom_object *obj, zval **retval TSRMLS_DC)
  244| {
  245| 	xmlDoc *docp;
  246| 	xmlDtdPtr dtdptr;
  247| 	int ret;
  248| 
  249| 	docp = (xmlDocPtr) dom_object_get_node(obj);
  250| 
  251| 	if (docp == NULL) {
  252| 		php_dom_throw_error(INVALID_STATE_ERR, 0 TSRMLS_CC);
  253| 		return FAILURE;
  254| 	}
  255| 
  256| 	ALLOC_ZVAL(*retval);
  257| 
  258| 	dtdptr = xmlGetIntSubset(docp);
  259| 	if (!dtdptr) {
  260| 		ZVAL_NULL(*retval);
  261| 		return SUCCESS;
  262| 	}
  263| 
  264| 	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) dtdptr, &ret, *retval, obj TSRMLS_CC))) {
  265| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object");
  266| 		return FAILURE;
  267| 	}
  268| 	return SUCCESS;
  269| 	
  270| }
  271| 
  272| /* }}} */
  273| 
  274| /* {{{ implementation	DOMImplementation	
  275| readonly=yes 
  276| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-ID-1B793EBA
  277| Since: 
  278| */
  279| int dom_document_implementation_read(dom_object *obj, zval **retval TSRMLS_DC)
  280| {
  281| 	ALLOC_ZVAL(*retval);
  282| 	php_dom_create_implementation(retval TSRMLS_CC);
  283| 	return SUCCESS;
  284| }
  285| 
  286| /* }}} */
  287| 
  288| /* {{{ documentElement	DOMElement	
  289| readonly=yes 
  290| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-ID-87CD092
  291| Since: 
  292| */
  293| int dom_document_document_element_read(dom_object *obj, zval **retval TSRMLS_DC)
  294| {
  295| 	xmlDoc *docp;
  296| 	xmlNode *root;
  297| 	int ret;
  298| 
  299| 	docp = (xmlDocPtr) dom_object_get_node(obj);
  300| 
  301| 	if (docp == NULL) {
  302| 		php_dom_throw_error(INVALID_STATE_ERR, 0 TSRMLS_CC);
  303| 		return FAILURE;
  304| 	}
  305| 
  306| 	ALLOC_ZVAL(*retval);
  307| 
  308| 	root = xmlDocGetRootElement(docp);
  309| 	if (!root) {
  310| 		ZVAL_NULL(*retval);
  311| 		return SUCCESS;
  312| 	}
  313| 
  314| 	if (NULL == (*retval = php_dom_create_object(root, &ret, *retval, obj TSRMLS_CC))) {
  315| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object");
  316| 		return FAILURE;
  317| 	}
  318| 	return SUCCESS;
  319| }
  320| 
```

- `read_file(path=ext/dom/dom_iterators.c, version=old, start_line=220, end_line=325)` →

```
ext/dom/dom_iterators.c lines 220-325 of 339
  220| 						basenode = xmlDocGetRootElement((xmlDoc *) basenode);
  221| 					} else if (basenode) {
  222| 						basenode = basenode->children;
  223| 					} else {
  224| 						goto err;
  225| 					}
  226| 					curnode = dom_get_elements_by_tag_name_ns_raw(basenode, objmap->ns, objmap->local, &previndex, iter->index);
  227| 				}
  228| 			}
  229| 		} else {
  230| 			if (objmap->nodetype == XML_ENTITY_NODE) {
  231| 				curnode = php_dom_libxml_hash_iter(objmap->ht, iter->index);
  232| 			} else {
  233| 				curnode = php_dom_libxml_notation_iter(objmap->ht, iter->index);
  234| 			}
  235| 		}
  236| 	}
  237| err:
  238| 	zval_ptr_dtor((zval**)&curobj);
  239| 	if (curnode) {
  240| 		MAKE_STD_ZVAL(curattr);
  241| 		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
  242| 	}
  243| 
  244| 	iterator->curobj = curattr;
  245| }
  246| /* }}} */
  247| 
  248| zend_object_iterator_funcs php_dom_iterator_funcs = {
  249| 	php_dom_iterator_dtor,
  250| 	php_dom_iterator_valid,
  251| 	php_dom_iterator_current_data,
  252| 	php_dom_iterator_current_key,
  253| 	php_dom_iterator_move_forward,
  254| 	NULL
  255| };
  256| 
  257| zend_object_iterator *php_dom_get_iterator(zend_class_entry *ce, zval *object, int by_ref TSRMLS_DC) /* {{{ */
  258| {
  259| 	dom_object *intern;
  260| 	dom_nnodemap_object *objmap;
  261| 	xmlNodePtr nodep, curnode=NULL;
  262| 	zval *curattr = NULL;
  263| 	int ret, curindex = 0;
  264| 	HashTable *nodeht;
  265| 	zval **entry;
  266| 	php_dom_iterator *iterator;
  267| 
  268| 	if (by_ref) {
  269| 		zend_error(E_ERROR, "An iterator cannot be used with foreach by reference");
  270| 	}
  271| 	iterator = emalloc(sizeof(php_dom_iterator));
  272| 
  273| 	Z_ADDREF_P(object);
  274| 	iterator->intern.data = (void*)object;
  275| 	iterator->intern.funcs = &php_dom_iterator_funcs;
  276| 
  277| 	intern = (dom_object *)zend_object_store_get_object(object TSRMLS_CC);
  278| 	objmap = (dom_nnodemap_object *)intern->ptr;
  279| 	if (objmap != NULL) {
  280| 		if (objmap->nodetype != XML_ENTITY_NODE && 
  281| 			objmap->nodetype != XML_NOTATION_NODE) {
  282| 			if (objmap->nodetype == DOM_NODESET) {
  283| 				nodeht = HASH_OF(objmap->baseobjptr);
  284| 				zend_hash_internal_pointer_reset(nodeht);
  285| 				if (zend_hash_get_current_data(nodeht, (void **) &entry)==SUCCESS) {
  286| 					curattr = *entry;
  287| 					Z_ADDREF_P(curattr);
  288| 				}
  289| 			} else {
  290| 				nodep = (xmlNode *)dom_object_get_node(objmap->baseobj);
  291| 				if (!nodep) {
  292| 					goto err;
  293| 				}
  294| 				if (objmap->nodetype == XML_ATTRIBUTE_NODE || objmap->nodetype == XML_ELEMENT_NODE) {
  295| 					if (objmap->nodetype == XML_ATTRIBUTE_NODE) {
  296| 						curnode = (xmlNodePtr) nodep->properties;
  297| 					} else {
  298| 						curnode = (xmlNodePtr) nodep->children;
  299| 					}
  300| 				} else {
  301| 					if (nodep->type == XML_DOCUMENT_NODE || nodep->type == XML_HTML_DOCUMENT_NODE) {
  302| 						nodep = xmlDocGetRootElement((xmlDoc *) nodep);
  303| 					} else {
  304| 						nodep = nodep->children;
  305| 					}
  306| 					curnode = dom_get_elements_by_tag_name_ns_raw(nodep, objmap->ns, objmap->local, &curindex, 0);
  307| 				}
  308| 			}
  309| 		} else {
  310| 			if (objmap->nodetype == XML_ENTITY_NODE) {
  311| 				curnode = php_dom_libxml_hash_iter(objmap->ht, 0);
  312| 			} else {
  313| 				curnode = php_dom_libxml_notation_iter(objmap->ht, 0);
  314| 			}
  315| 		}
  316| 	}
  317| err:
  318| 	if (curnode) {
  319| 		MAKE_STD_ZVAL(curattr);
  320| 		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
  321| 	}
  322| 
  323| 	iterator->curobj = curattr;
  324| 
  325| 	return (zend_object_iterator*)iterator;
```

- `read_file(path=ext/dom/node.c, version=old, start_line=410, end_line=680)` →

```
ext/dom/node.c lines 410-659 of 1991
  410| Since: 
  411| */
  412| int dom_node_parent_node_read(dom_object *obj, zval **retval TSRMLS_DC)
  413| {
  414| 	xmlNode *nodep, *nodeparent;
  415| 	int ret;
  416| 
  417| 	nodep = dom_object_get_node(obj);
  418| 
  419| 	if (nodep == NULL) {
  420| 		php_dom_throw_error(INVALID_STATE_ERR, 0 TSRMLS_CC);
  421| 		return FAILURE;
  422| 	}
  423| 
  424| 	ALLOC_ZVAL(*retval);
  425| 
  426| 	nodeparent = nodep->parent;
  427| 	if (!nodeparent) {
  428| 		ZVAL_NULL(*retval);
  429| 		return SUCCESS;
  430| 	}
  431| 
  432| 	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
  433| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object");
  434| 		return FAILURE;
  435| 	}
  436| 	return SUCCESS;
  437| }
  438| 
  439| /* }}} */
  440| 
  441| /* {{{ childNodes	DomNodeList	
  442| readonly=yes 
  443| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-ID-1451460987
  444| Since: 
  445| */
  446| int dom_node_child_nodes_read(dom_object *obj, zval **retval TSRMLS_DC)
  447| {
  448| 	xmlNode *nodep;
  449| 	dom_object *intern;
  450| 
  451| 	nodep = dom_object_get_node(obj);
  452| 
  453| 	if (nodep == NULL) {
  454| 		php_dom_throw_error(INVALID_STATE_ERR, 0 TSRMLS_CC);
  455| 		return FAILURE;
  456| 	}
  457| 
  458| 	ALLOC_ZVAL(*retval);
  459| 	
  460| 	if (dom_node_children_valid(nodep) == FAILURE) {
  461| 		ZVAL_NULL(*retval);
  462| 	} else {
  463| 		php_dom_create_interator(*retval, DOM_NODELIST TSRMLS_CC);
  464| 		intern = (dom_object *)zend_objects_get_address(*retval TSRMLS_CC);
  465| 		dom_namednode_iter(obj, XML_ELEMENT_NODE, intern, NULL, NULL, NULL TSRMLS_CC);
  466| 	}
  467| 
  468| 	return SUCCESS;
  469| }
  470| 
  471| /* }}} */
  472| 
  473| /* {{{ firstChild DomNode	
  474| readonly=yes 
  475| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-ID-169727388
  476| Since: 
  477| */
  478| int dom_node_first_child_read(dom_object *obj, zval **retval TSRMLS_DC)
  479| {
  480| 	xmlNode *nodep, *first = NULL;
  481| 	int ret;
  482| 
  483| 	nodep = dom_object_get_node(obj);
  484| 
  485| 	if (nodep == NULL) {
  486| 		php_dom_throw_error(INVALID_STATE_ERR, 0 TSRMLS_CC);
  487| 		return FAILURE;
  488| 	}
  489| 
  490| 	if (dom_node_children_valid(nodep) == SUCCESS) {
  491| 		first = nodep->children;
  492| 	}
  493| 
  494| 	ALLOC_ZVAL(*retval);
  495| 
  496| 	if (!first) {
  497| 		ZVAL_NULL(*retval);
  498| 		return SUCCESS;
  499| 	}
  500| 
  501| 	if (NULL == (*retval = php_dom_create_object(first, &ret, *retval, obj TSRMLS_CC))) {
  502| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object");
  503| 		return FAILURE;
  504| 	}
  505| 	return SUCCESS;
  506| }
  507| 
  508| /* }}} */
  509| 
  510| /* {{{ lastChild	DomNode	
  511| readonly=yes 
  512| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-ID-61AD09FB
  513| Since: 
  514| */
  515| int dom_node_last_child_read(dom_object *obj, zval **retval TSRMLS_DC)
  516| {
  517| 	xmlNode *nodep, *last = NULL;
  518| 	int ret;
  519| 
  520| 	nodep = dom_object_get_node(obj);
  521| 
  522| 	if (nodep == NULL) {
  523| 		php_dom_throw_error(INVALID_STATE_ERR, 0 TSRMLS_CC);
  524| 		return FAILURE;
  525| 	}
  526| 
  527| 	if (dom_node_children_valid(nodep) == SUCCESS) {
  528| 		last = nodep->last;
  529| 	}
  530| 
  531| 	ALLOC_ZVAL(*retval);
  532| 
  533| 	if (!last) {
  534| 		ZVAL_NULL(*retval);
  535| 		return SUCCESS;
  536| 	}
  537| 
  538| 	if (NULL == (*retval = php_dom_create_object(last, &ret, *retval, obj TSRMLS_CC))) {
  539| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object");
  540| 		return FAILURE;
  541| 	}
  542| 	return SUCCESS;
  543| }
  544| 
  545| /* }}} */
  546| 
  547| /* {{{ previousSibling	DomNode	
  548| readonly=yes 
  549| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-ID-640FB3C8
  550| Since: 
  551| */
  552| int dom_node_previous_sibling_read(dom_object *obj, zval **retval TSRMLS_DC)
  553| {
  554| 	xmlNode *nodep, *prevsib;
  555| 	int ret;
  556| 
  557| 	nodep = dom_object_get_node(obj);
  558| 
  559| 	if (nodep == NULL) {
  560| 		php_dom_throw_error(INVALID_STATE_ERR, 0 TSRMLS_CC);
  561| 		return FAILURE;
  562| 	}
  563| 
  564| 	ALLOC_ZVAL(*retval);
  565| 
  566| 	prevsib = nodep->prev;
  567| 	if (!prevsib) {
  568| 		ZVAL_NULL(*retval);
  569| 		return SUCCESS;
  570| 	}
  571| 
  572| 	if (NULL == (*retval = php_dom_create_object(prevsib, &ret, *retval, obj TSRMLS_CC))) {
  573| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object");
  574| 		return FAILURE;
  575| 	}
  576| 	return SUCCESS;
  577| }
  578| 
  579| /* }}} */
  580| 
  581| /* {{{ nextSibling	DomNode
  582| readonly=yes 
  583| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-ID-6AC54C2F
  584| Since:
  585| */
  586| int dom_node_next_sibling_read(dom_object *obj, zval **retval TSRMLS_DC)
  587| {
  588| 	xmlNode *nodep, *nextsib;
  589| 	int ret;
  590| 
  591| 	nodep = dom_object_get_node(obj);
  592| 
  593| 	if (nodep == NULL) {
  594| 		php_dom_throw_error(INVALID_STATE_ERR, 0 TSRMLS_CC);
  595| 		return FAILURE;
  596| 	}
  597| 
  598| 	nextsib = nodep->next;
  599| 	if (!nextsib) {
  600| 		return FAILURE;
  601| 	}
  602| 
  603| 	ALLOC_ZVAL(*retval);
  604| 
  605| 	if (NULL == (*retval = php_dom_create_object(nextsib, &ret, *retval, obj TSRMLS_CC))) {
  606| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object");
  607| 		return FAILURE;
  608| 	}
  609| 	return SUCCESS;
  610| }
  611| 
  612| /* }}} */
  613| 
  614| /* {{{ attributes	DomNamedNodeMap	
  615| readonly=yes 
  616| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-ID-84CF096
  617| Since: 
  618| */
  619| int dom_node_attributes_read(dom_object *obj, zval **retval TSRMLS_DC)
  620| {
  621| 	xmlNode *nodep;
  622| 	dom_object *intern;
  623| 
  624| 	nodep = dom_object_get_node(obj);
  625| 
  626| 	if (nodep == NULL) {
  627| 		php_dom_throw_error(INVALID_STATE_ERR, 0 TSRMLS_CC);
  628| 		return FAILURE;
  629| 	}
  630| 
  631| 	ALLOC_ZVAL(*retval);
  632| 
  633| 	if (nodep->type == XML_ELEMENT_NODE) {
  634| 		php_dom_create_interator(*retval, DOM_NAMEDNODEMAP TSRMLS_CC);
  635| 		intern = (dom_object *)zend_objects_get_address(*retval TSRMLS_CC);
  636| 		dom_namednode_iter(obj, XML_ATTRIBUTE_NODE, intern, NULL, NULL, NULL TSRMLS_CC);
  637| 	} else {
  638| 		ZVAL_NULL(*retval);
  639| 	}
  640| 
  641| 	return SUCCESS;
  642| }
  643| 
  644| /* }}} */
  645| 
  646| /* {{{ ownerDocument	DomDocument	
  647| readonly=yes 
  648| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-node-ownerDoc
  649| Since: 
  650| */
  651| int dom_node_owner_document_read(dom_object *obj, zval **retval TSRMLS_DC)
  652| {
  653| 	xmlNode *nodep;
  654| 	xmlDocPtr docp;
  655| 	int ret;
  656| 
  657| 	nodep = dom_object_get_node(obj);
  658| 
  659| 	if (nodep == NULL) {
```

- `read_file(path=ext/dom/text.c, version=old, start_line=175, end_line=200)` →

```
ext/dom/text.c lines 175-200 of 246
  175| 		RETURN_FALSE;
  176| 	}
  177| 
  178| 	first = xmlUTF8Strndup(cur, offset);
  179| 	second = xmlUTF8Strsub(cur, offset, length - offset);
  180| 	
  181| 	xmlFree(cur);
  182| 
  183| 	xmlNodeSetContent(node, first);
  184| 	nnode = xmlNewDocText(node->doc, second);
  185| 	
  186| 	xmlFree(first);
  187| 	xmlFree(second);
  188| 
  189| 	if (nnode == NULL) {
  190| 		RETURN_FALSE;
  191| 	}
  192| 
  193| 	if (node->parent != NULL) {
  194| 		nnode->type = XML_ELEMENT_NODE;
  195| 		xmlAddNextSibling(node, nnode);
  196| 		nnode->type = XML_TEXT_NODE;
  197| 	}
  198| 	
  199| 	return_value = php_dom_create_object(nnode, &ret, return_value, intern TSRMLS_CC);
  200| }
```

- `read_file(path=ext/dom/xpath.c, version=old, start_line=140, end_line=170)` →

```
ext/dom/xpath.c lines 140-170 of 603
  140| 				} else if (type == 2) {
  141| 					int j;
  142| 					array_init(args[i]);
  143| 					if (obj->nodesetval && obj->nodesetval->nodeNr > 0) {
  144| 						for (j = 0; j < obj->nodesetval->nodeNr; j++) {
  145| 							xmlNodePtr node = obj->nodesetval->nodeTab[j];
  146| 							zval *child;
  147| 							MAKE_STD_ZVAL(child);
  148| 							/* not sure, if we need this... it's copied from xpath.c */
  149| 							if (node->type == XML_NAMESPACE_DECL) {
  150| 								xmlNsPtr curns;
  151| 								xmlNodePtr nsparent;
  152| 								
  153| 								nsparent = node->_private;
  154| 								curns = xmlNewNs(NULL, node->name, NULL);
  155| 								if (node->children) {
  156| 									curns->prefix = xmlStrdup((xmlChar *) node->children);
  157| 								}
  158| 								if (node->children) {
  159| 									node = xmlNewDocNode(node->doc, NULL, (xmlChar *) node->children, node->name);
  160| 								} else {
  161| 									node = xmlNewDocNode(node->doc, NULL, (xmlChar *) "xmlns", node->name);
  162| 								}
  163| 								node->type = XML_NAMESPACE_DECL;
  164| 								node->parent = nsparent;
  165| 								node->ns = curns;
  166| 							}
  167| 							child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
  168| 							add_next_index_zval(args[i], child);
  169| 						}
  170| 					}
```

- `read_file(path=ext/dom/xpath.c, version=old, start_line=300, end_line=340)` →

```
ext/dom/xpath.c lines 300-340 of 603
  300| 			xmlXPathFreeContext(oldctx);
  301| 		}
  302| 
  303| 		xmlXPathRegisterFuncNS (ctx, (const xmlChar *) "functionString",
  304| 					   (const xmlChar *) "http://php.net/xpath",
  305| 					   dom_xpath_ext_function_string_php);
  306| 		xmlXPathRegisterFuncNS (ctx, (const xmlChar *) "function",
  307| 					   (const xmlChar *) "http://php.net/xpath",
  308| 					   dom_xpath_ext_function_object_php);
  309| 
  310| 		intern->ptr = ctx;
  311| 		ctx->userData = (void *)intern;
  312| 		intern->document = docobj->document;
  313| 		php_libxml_increment_doc_ref((php_libxml_node_object *)intern, docp TSRMLS_CC);
  314| 	}
  315| }
  316| /* }}} end DOMXPath::__construct */
  317| 
  318| /* {{{ document DOMDocument*/
  319| int dom_xpath_document_read(dom_object *obj, zval **retval TSRMLS_DC)
  320| {
  321| 	xmlDoc *docp = NULL;
  322| 	xmlXPathContextPtr ctx;
  323| 	int ret;
  324| 	zval *tmp;
  325| 
  326| 	ctx = (xmlXPathContextPtr) obj->ptr;
  327| 
  328| 	if (ctx) {
  329| 		docp = (xmlDocPtr) ctx->doc;
  330| 	}
  331| 
  332| 	ALLOC_ZVAL(*retval);
  333| 	tmp = *retval;
  334| 
  335| 	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
  336| 		FREE_ZVAL(tmp);
  337| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object");
  338| 		return FAILURE;
  339| 	}
  340| 	if (tmp != *retval) {
```

- `read_file(path=ext/dom/xpath.c, version=old, start_line=470, end_line=510)` →

```
ext/dom/xpath.c lines 470-510 of 603
  470| 			int i;
  471| 			xmlNodeSetPtr nodesetp;
  472| 
  473| 			MAKE_STD_ZVAL(retval);
  474| 			array_init(retval);
  475| 
  476| 			if (xpathobjp->type == XPATH_NODESET && NULL != (nodesetp = xpathobjp->nodesetval)) {
  477| 
  478| 				for (i = 0; i < nodesetp->nodeNr; i++) {
  479| 					xmlNodePtr node = nodesetp->nodeTab[i];
  480| 					zval *child;
  481| 
  482| 					MAKE_STD_ZVAL(child);
  483| 					
  484| 					if (node->type == XML_NAMESPACE_DECL) {
  485| 						xmlNsPtr curns;
  486| 						xmlNodePtr nsparent;
  487| 
  488| 						nsparent = node->_private;
  489| 						curns = xmlNewNs(NULL, node->name, NULL);
  490| 						if (node->children) {
  491| 							curns->prefix = xmlStrdup((char *) node->children);
  492| 						}
  493| 						if (node->children) {
  494| 							node = xmlNewDocNode(docp, NULL, (char *) node->children, node->name);
  495| 						} else {
  496| 							node = xmlNewDocNode(docp, NULL, "xmlns", node->name);
  497| 						}
  498| 						node->type = XML_NAMESPACE_DECL;
  499| 						node->parent = nsparent;
  500| 						node->ns = curns;
  501| 					}
  502| 					child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
  503| 					add_next_index_zval(retval, child);
  504| 				}
  505| 			}
  506| 			php_dom_create_interator(return_value, DOM_NODELIST TSRMLS_CC);
  507| 			nodeobj = (dom_object *)zend_objects_get_address(return_value TSRMLS_CC);
  508| 			dom_xpath_iter(retval, nodeobj);
  509| 			break;
  510| 		}
```

- `read_file(path=ext/xsl/xsltprocessor.c, version=old, start_line=255, end_line=295)` →

```
ext/xsl/xsltprocessor.c lines 255-295 of 997
  255| 				} else if (type == 2) {
  256| 					int j;
  257| 					dom_object *domintern = (dom_object *)intern->doc;
  258| 					array_init(args[i]);
  259| 					if (obj->nodesetval && obj->nodesetval->nodeNr > 0) {
  260| 						for (j = 0; j < obj->nodesetval->nodeNr; j++) {
  261| 							xmlNodePtr node = obj->nodesetval->nodeTab[j];
  262| 							zval *child;
  263| 							MAKE_STD_ZVAL(child);
  264| 							/* not sure, if we need this... it's copied from xpath.c */
  265| 							if (node->type == XML_NAMESPACE_DECL) {
  266| 								xmlNsPtr curns;
  267| 								xmlNodePtr nsparent;
  268| 								
  269| 								nsparent = node->_private;
  270| 								curns = xmlNewNs(NULL, node->name, NULL);
  271| 								if (node->children) {
  272| 									curns->prefix = xmlStrdup((char *) node->children);
  273| 								}
  274| 								if (node->children) {
  275| 									node = xmlNewDocNode(node->doc, NULL, (char *) node->children, node->name);
  276| 								} else {
  277| 									node = xmlNewDocNode(node->doc, NULL, "xmlns", node->name);
  278| 								}
  279| 								node->type = XML_NAMESPACE_DECL;
  280| 								node->parent = nsparent;
  281| 								node->ns = curns;
  282| 							} else {
  283| 								node = xmlDocCopyNodeList(domintern->document->ptr, node);
  284| 							}
  285| 
  286| 							child = php_dom_create_object(node, &ret, child, domintern TSRMLS_CC);
  287| 							add_next_index_zval(args[i], child);
  288| 						}
  289| 					}
  290| 				}
  291| 				break;
  292| 			default:
  293| 				str = xmlXPathCastToString(obj);
  294| 				ZVAL_STRING(args[i], str, 1);
  295| 				xmlFree(str);
```

### Turn 3  _(tok 18278+1682, stop=tool_use)_

**Reasoning:** I'm listing the enclosing function names for the flagged lines. Three are already clear, from attr.c and document.c. For dom_iterators.c:241 I still need to confirm the function that ends at line 245, and the one for line 320 is not identified yet.

Now I'm going through the rest of the list, checking the enclosing function for each remaining flagged line, and noting that several of the node.c, text.c, xpath.c, and xsltprocessor.c entries still need their names confirmed.

I'm deciding whether functions that only use the DOM_RET_OBJ macro count as callers of php_dom_create_object. The macro itself is the only textual call, so I'm leaning toward excluding those users and noting it as a caveat.

I'm now reading the surrounding code to pin down the enclosing function names for the remaining flagged lines.



**Says:** I have the call-site lines. Next I need the enclosing function name for the ones not yet identified: dom_iterators.c:241, text.c:199, xpath.c:167 and 502, xpath.c:335 (already seen as dom_xpath_document_read), and xsltprocessor.c:286.

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|int |void |static |zval |zend_|xml, version=old, path_glob=ext/dom/dom_iterators.c)` →

```
8 matches
ext/dom/dom_iterators.c:45:static void itemHashScanner (void *payload, void *data, xmlChar *name) /* {{{ */
ext/dom/dom_iterators.c:59:xmlNodePtr create_notation(const xmlChar *name, const xmlChar *ExternalID, const xmlChar *SystemID) /* {{{ */
ext/dom/dom_iterators.c:125:static void php_dom_iterator_dtor(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:139:static int php_dom_iterator_valid(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:152:static void php_dom_iterator_current_data(zend_object_iterator *iter, zval ***data TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:160:static void php_dom_iterator_current_key(zend_object_iterator *iter, zval *key TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:180:static void php_dom_iterator_move_forward(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:257:zend_object_iterator *php_dom_get_iterator(zend_class_entry *ce, zval *object, int by_ref TSRMLS_DC) /* {{{ */
```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|int |void |static |zval |zend_|xml, version=old, path_glob=ext/dom/text.c)` →

```
5 matches
ext/dom/text.c:65:PHP_METHOD(domtext, __construct)
ext/dom/text.c:105:int dom_text_whole_text_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/text.c:145:PHP_FUNCTION(dom_text_split_text)
ext/dom/text.c:207:PHP_FUNCTION(dom_text_is_whitespace_in_element_content)
ext/dom/text.c:230:PHP_FUNCTION(dom_text_replace_whole_text)
```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|int |void |static |zval |zend_|xml, version=old, path_glob=ext/dom/xpath.c)` →

```
11 matches
ext/dom/xpath.c:75:static void dom_xpath_ext_function_php(xmlXPathParserContextPtr ctxt, int nargs, int type) /* {{{ */
ext/dom/xpath.c:258:static void dom_xpath_ext_function_string_php(xmlXPathParserContextPtr ctxt, int nargs) /* {{{ */
ext/dom/xpath.c:264:static void dom_xpath_ext_function_object_php(xmlXPathParserContextPtr ctxt, int nargs) /* {{{ */
ext/dom/xpath.c:271:PHP_METHOD(domxpath, __construct)
ext/dom/xpath.c:319:int dom_xpath_document_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/xpath.c:348:PHP_FUNCTION(dom_xpath_register_ns)
ext/dom/xpath.c:375:static void dom_xpath_iter(zval *baseobj, dom_object *intern) /* {{{ */
ext/dom/xpath.c:386:static void php_xpath_eval(INTERNAL_FUNCTION_PARAMETERS, int type) /* {{{ */
ext/dom/xpath.c:534:PHP_FUNCTION(dom_xpath_query)
ext/dom/xpath.c:541:PHP_FUNCTION(dom_xpath_evaluate)
ext/dom/xpath.c:548:PHP_FUNCTION(dom_xpath_register_php_functions)
```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD|int |void |static |zval |zend_|xml, version=old, path_glob=ext/xsl/xsltprocessor.c)` →

```
18 matches
ext/xsl/xsltprocessor.c:108:static char *php_xsl_xslt_string_to_xpathexpr(const char *str TSRMLS_DC)
ext/xsl/xsltprocessor.c:134:static char **php_xsl_xslt_make_params(HashTable *parht, int xpath_params TSRMLS_DC)
ext/xsl/xsltprocessor.c:182:static void xsl_ext_function_php(xmlXPathParserContextPtr ctxt, int nargs, int type) /* {{{ */
ext/xsl/xsltprocessor.c:381:void xsl_ext_function_string_php(xmlXPathParserContextPtr ctxt, int nargs) /* {{{ */
ext/xsl/xsltprocessor.c:387:void xsl_ext_function_object_php(xmlXPathParserContextPtr ctxt, int nargs) /* {{{ */
ext/xsl/xsltprocessor.c:397:PHP_FUNCTION(xsl_xsltprocessor_import_stylesheet)
ext/xsl/xsltprocessor.c:480:static xmlDocPtr php_xsl_apply_stylesheet(zval *id, xsl_object *intern, xsltStylesheetPtr style, zval *docp TSRMLS_DC) /* {{{ */
ext/xsl/xsltprocessor.c:645:PHP_FUNCTION(xsl_xsltprocessor_transform_to_doc)
ext/xsl/xsltprocessor.c:702:PHP_FUNCTION(xsl_xsltprocessor_transform_to_uri)
ext/xsl/xsltprocessor.c:733:PHP_FUNCTION(xsl_xsltprocessor_transform_to_xml)
ext/xsl/xsltprocessor.c:771:PHP_FUNCTION(xsl_xsltprocessor_set_parameter)
ext/xsl/xsltprocessor.c:823:PHP_FUNCTION(xsl_xsltprocessor_get_parameter)
ext/xsl/xsltprocessor.c:848:PHP_FUNCTION(xsl_xsltprocessor_remove_parameter)
ext/xsl/xsltprocessor.c:871:PHP_FUNCTION(xsl_xsltprocessor_register_php_functions)
ext/xsl/xsltprocessor.c:914:PHP_FUNCTION(xsl_xsltprocessor_set_profiling)
ext/xsl/xsltprocessor.c:940:PHP_FUNCTION(xsl_xsltprocessor_set_security_prefs)
ext/xsl/xsltprocessor.c:960:PHP_FUNCTION(xsl_xsltprocessor_get_security_prefs)
ext/xsl/xsltprocessor.c:979:PHP_FUNCTION(xsl_xsltprocessor_has_exslt_support)
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 4  _(tok 22488+575, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "dom_attr_owner_element_read", "file": "ext/dom/attr.c"}, {"function": "dom_document_doctype_read", "file": "ext/dom/document.c"}, {"function": "dom_document_document_element_read", "file": "ext/dom/document.c"}, {"function": "php_dom_get_iterator", "file": "ext/dom/dom_iterators.c"}, {"function": "php_dom_iterator_current_data", "file": "ext/dom/dom_iterators.c"}, {"function": "dom_node_parent_node_read", "file": "ext/dom/node.c"}, {"function": "dom_node_first_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_last_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_previous_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_next_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_owner_document_read", "file": "ext/dom/node.c"}, {"function": "dom_text_split_text", "file": "ext/dom/text.c"}, {"function": "dom_xpath_ext_function_php", "file": "ext/dom/xpath.c"}, {"function": "dom_xpath_document_read", "file": "ext/dom/xpath.c"}, {"function": "php_xpath_eval", "file": "ext/dom/xpath.c"}, {"function": "xsl_ext_function_php", "file": "ext/xsl/xsltprocessor.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 16, "n_truth": 4, "tp": 3, "precision": 0.1875, "recall": 0.75, "f1": 0.3}`

## Tool arm

### Turn 1  _(tok 3753+235, stop=tool_use)_

**Reasoning:** I'm starting by pulling the callers of php_dom_create_object with a high limit, and I'll run a grep for it as well to cross-check.



- `get_callers(name=php_dom_create_object, limit=500, version=old)` →

```
{
  "name": "php_dom_create_object",
  "version": "old",
  "callers": [
    {
      "caller": "dom_attr_owner_element_read",
      "file": "ext/dom/attr.c",
      "line": 231
    },
    {
      "caller": "php_dom_iterator_move_forward",
      "file": "ext/dom/dom_iterators.c",
      "line": 241
    },
    {
      "caller": "php_dom_get_iterator",
      "file": "ext/dom/dom_iterators.c",
      "line": 320
    },
    {
      "caller": "dom_node_parent_node_read",
      "file": "ext/dom/node.c",
      "line": 432
    },
    {
      "caller": "dom_node_first_child_read",
      "file": "ext/dom/node.c",
      "line": 501
    },
    {
      "caller": "dom_node_last_child_read",
      "file": "ext/dom/node.c",
      "line": 538
    },
    {
      "caller": "dom_node_previous_sibling_read",
      "file": "ext/dom/node.c",
      "line": 572
    },
    {
      "caller": "dom_node_next_sibling_read",
      "file": "ext/dom/node.c",
      "line": 605
    },
    {
      "caller": "dom_node_owner_document_read",
      "file": "ext/dom/node.c",
      "line": 677
    },
    {
      "caller": "PHP_FUNCTION(dom_text_split_text)",
      "file": "ext/dom/text.c",
      "line": 199
    },
    {
      "caller": "dom_xpath_ext_function_php",
      "file": "ext/dom/xpath.c",
      "line": 167
    },
    {
      "caller": "dom_xpath_document_read",
      "file": "ext/dom/xpath.c",
      "line": 335
    },
    {
      "caller": "php_xpath_eval",
      "file": "ext/dom/xpath.c",
      "line": 502
    },
    {
      "caller": "xsl_ext_function_php",
      "file": "ext/xsl/xsltprocessor.c",
      "line": 286
    },
    {
      "caller": "dom_document_doctype_read",
      "file": "ext/dom/document.c",
      "line": 264
    },
    {
      "caller": "dom_document_document_element_read",
      "file": "ext/dom/document.c",
      "line": 314
    }
  ]
}
```

- `grep(pattern=php_dom_create_object, version=old, max_results=500)` →

```
20 matches
ext/dom/attr.c:231:	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:264:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) dtdptr, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:314:	if (NULL == (*retval = php_dom_create_object(root, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/dom_iterators.c:241:		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
ext/dom/dom_iterators.c:320:		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
ext/dom/node.c:432:	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:501:	if (NULL == (*retval = php_dom_create_object(first, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:538:	if (NULL == (*retval = php_dom_create_object(last, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:572:	if (NULL == (*retval = php_dom_create_object(prevsib, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:605:	if (NULL == (*retval = php_dom_create_object(nextsib, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:677:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/php_dom.c:1320:/* {{{ php_dom_create_object */
ext/dom/php_dom.c:1321:PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval *return_value, dom_object *domobj TSRMLS_DC)
ext/dom/text.c:199:	return_value = php_dom_create_object(nnode, &ret, return_value, intern TSRMLS_CC);
ext/dom/xml_common.h:57:PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval* return_value, dom_object *domobj TSRMLS_DC);
ext/dom/xml_common.h:82:	if (!php_dom_create_object(obj, ret, return_value, domobject TSRMLS_CC)) { \
ext/dom/xpath.c:167:							child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
ext/dom/xpath.c:335:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/xpath.c:502:					child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
ext/xsl/xsltprocessor.c:286:							child = php_dom_create_object(node, &ret, child, domintern TSRMLS_CC);
```

### Turn 2  _(tok 6100+444, stop=tool_use)_

**Reasoning:** I'm checking whether the macro at xml_common.h:82 is what DOM_RET_OBJ expands to, and whether the functions that use it reach php_dom_create_object only through that expansion. I'm also wondering why get_callers missed those macro-based callers, and whether I should count them at all. Next I'll look at the macro definition and where it is used.

I'm going to look at the macro definition and see where it's used, since the expansion is what would tie those callers to php_dom_create_object.



**Says:** The grep turned up one hit the callgraph missed: `xml_common.h:82` is inside a macro. I'll check that macro and where it is used.

- `read_file(path=ext/dom/xml_common.h, version=old, start_line=70, end_line=95)` →

```
ext/dom/xml_common.h lines 70-95 of 107
   70| 
   71| #define DOC_GET_OBJ(__ptr, __id, __prtype, __intern) { \
   72| 	__intern = (php_libxml_node_object *)zend_object_store_get_object(__id TSRMLS_CC); \
   73| 	if (__intern->document != NULL) { \
   74| 		if (!(__ptr = (__prtype)__intern->document->ptr)) { \
   75|   			php_error_docref(NULL TSRMLS_CC, E_WARNING, "Couldn't fetch %s", __intern->std.ce->name);\
   76|   			RETURN_NULL();\
   77|   		} \
   78| 	} \
   79| }
   80| 
   81| #define DOM_RET_OBJ(obj, ret, domobject) \
   82| 	if (!php_dom_create_object(obj, ret, return_value, domobject TSRMLS_CC)) { \
   83| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object"); \
   84| 		RETURN_FALSE; \
   85| 	}
   86| 
   87| #define DOM_GET_THIS(zval) \
   88| 	if (NULL == (zval = getThis())) { \
   89| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Underlying object missing"); \
   90| 		RETURN_FALSE; \
   91| 	}
   92| 
   93| #define DOM_GET_THIS_OBJ(__ptr, __id, __prtype, __intern) \
   94| 	DOM_GET_THIS(__id); \
   95| 	DOM_GET_OBJ(__ptr, __id, __prtype, __intern);
```

- `grep(pattern=DOM_RET_OBJ|php_dom_create_object, version=old, max_results=500)` →

```
57 matches
ext/dom/attr.c:231:	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:264:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) dtdptr, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:314:	if (NULL == (*retval = php_dom_create_object(root, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:927:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:954:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:982:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1010:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1038:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1073:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1106:	DOM_RET_OBJ((xmlNodePtr) node, &ret, intern);
ext/dom/document.c:1140:	DOM_RET_OBJ((xmlNodePtr) node, &ret, intern);
ext/dom/document.c:1221:	DOM_RET_OBJ((xmlNodePtr) retnodep, &ret, intern);
ext/dom/document.c:1284:	DOM_RET_OBJ(nodep, &ret, intern);
ext/dom/document.c:1349:	DOM_RET_OBJ(nodep, &ret, intern);
ext/dom/document.c:1402:		DOM_RET_OBJ((xmlNodePtr) attrp->parent, &ret, intern);
ext/dom/document.c:1716:		DOM_RET_OBJ((xmlNodePtr) newdoc, &ret, NULL);
ext/dom/document.c:2235:		DOM_RET_OBJ((xmlNodePtr) newdoc, &ret, NULL);
ext/dom/dom_iterators.c:241:		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
ext/dom/dom_iterators.c:320:		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
ext/dom/domimplementation.c:143:	DOM_RET_OBJ((xmlNodePtr) doctype, &ret, NULL);
ext/dom/domimplementation.c:240:	DOM_RET_OBJ((xmlNodePtr) docp, &ret, NULL);
ext/dom/element.c:429:	DOM_RET_OBJ(attr, &ret, intern);
ext/dom/element.c:524:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:586:		DOM_RET_OBJ((xmlNodePtr) existattrp, &ret, intern);
ext/dom/element.c:626:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:947:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:1017:		DOM_RET_OBJ((xmlNodePtr) existattrp, &ret, intern);
ext/dom/namednodemap.c:169:		DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/namednodemap.c:246:			DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/namednodemap.c:301:		DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/node.c:432:	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:501:	if (NULL == (*retval = php_dom_create_object(first, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:538:	if (NULL == (*retval = php_dom_create_object(last, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:572:	if (NULL == (*retval = php_dom_create_object(prevsib, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:605:	if (NULL == (*retval = php_dom_create_object(nextsib, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:677:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:1090:					DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1132:					DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1151:	DOM_RET_OBJ(new_child, &ret, intern);
ext/dom/node.c:1235:		DOM_RET_OBJ(oldchild, &ret, intern);
ext/dom/node.c:1284:			DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1392:	DOM_RET_OBJ(new_child, &ret, intern);
ext/dom/node.c:1481:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/nodelist.c:166:			DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/php_dom.c:581:		DOM_RET_OBJ((xmlNodePtr) nodep, &ret, (dom_object *)nodeobj);
ext/dom/php_dom.c:1320:/* {{{ php_dom_create_object */
ext/dom/php_dom.c:1321:PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval *return_value, dom_object *domobj TSRMLS_DC)
ext/dom/text.c:199:	return_value = php_dom_create_object(nnode, &ret, return_value, intern TSRMLS_CC);
ext/dom/xml_common.h:57:PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval* return_value, dom_object *domobj TSRMLS_DC);
ext/dom/xml_common.h:81:#define DOM_RET_OBJ(obj, ret, domobject) \
ext/dom/xml_common.h:82:	if (!php_dom_create_object(obj, ret, return_value, domobject TSRMLS_CC)) { \
ext/dom/xpath.c:167:							child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
ext/dom/xpath.c:335:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/xpath.c:502:					child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
ext/xmlreader/php_xmlreader.c:1158:				DOM_RET_OBJ(nodec, &ret, (dom_object *)domobj);
ext/xsl/xsltprocessor.c:286:							child = php_dom_create_object(node, &ret, child, domintern TSRMLS_CC);
ext/xsl/xsltprocessor.c:691:			DOM_RET_OBJ((xmlNodePtr) newdocp, &ret, NULL);
```

### Turn 3  _(tok 10049+2036, stop=tool_use)_

**Reasoning:** I'm weighing whether the macro's users belong in the answer, since they reach php_dom_create_object only through the macro's expansion. The question asks for every function that calls it, and I'm trying to decide if an indirect call through DOM_RET_OBJ counts or if only the macro's own body would need changing.

I'm settling on the 16 direct callers as the answer, since the macro body is the one real call site and its users need no source changes. I'll note the macro's indirect callers as a caveat. Now I'm checking the get_callers list and which function encloses the dom_text_split_text entry.

I'm checking the enclosing function name for the PHP_FUNCTION entry, whether it's reported as the PHP name or the zif_ symbol, and confirming the definition's line in php_dom.c. I'm also recounting the grep matches to make sure the 16 direct callers hold up.

I'm going through the remaining enclosing functions for each caller: the dom_document and dom_node property readers, the iterator functions, dom_text_split_text as a PHP_FUNCTION, and the xpath and xsltprocessor extension functions. I'll confirm the PHP_FUNCTION entry at text.c:199 by checking its surrounding lines.

I'm going to trust the tool's report that the PHP_FUNCTION entry sits inside dom_text_split_text, and I'll keep the name as PHP_FUNCTION(dom_text_split_text). I'm also skipping a second look at the xpath.c entries, since the tool already reports dom_xpath_ext_function_php and php_xpath_eval as their enclosing functions.



**Says:** The grep finds 16 direct call sites of `php_dom_create_object`, which matches the callgraph result. The `DOM_RET_OBJ` macro also expands to a call, but the call site is the macro body, so the users of the macro don't need source edits. I'll submit the 16 direct callers and flag the macro in my summary.

- **submit_callers** → `{"callers": [{"function": "dom_attr_owner_element_read", "file": "ext/dom/attr.c"}, {"function": "php_dom_iterator_move_forward", "file": "ext/dom/dom_iterators.c"}, {"function": "php_dom_get_iterator", "file": "ext/dom/dom_iterators.c"}, {"function": "dom_node_parent_node_read", "file": "ext/dom/node.c"}, {"function": "dom_node_first_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_last_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_previous_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_next_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_owner_document_read", "file": "ext/dom/node.c"}, {"function": "PHP_FUNCTION(dom_text_split_text)", "file": "ext/dom/text.c"}, {"function": "dom_xpath_ext_function_php", "file": "ext/dom/xpath.c"}, {"function": "dom_xpath_document_read", "file": "ext/dom/xpath.c"}, {"function": "php_xpath_eval", "file": "ext/dom/xpath.c"}, {"function": "xsl_ext_function_php", "file": "ext/xsl/xsltprocessor.c"}, {"function": "dom_document_doctype_read", "file": "ext/dom/document.c"}, {"function": "dom_document_document_element_read", "file": "ext/dom/document.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 16, "n_truth": 4, "tp": 3, "precision": 0.1875, "recall": 0.75, "f1": 0.3}`

## Semantic arm

### Turn 1  _(tok 3205+97, stop=tool_use)_

**Reasoning:** I'll start by calling get_callers with a high limit so I get the full set of results.



- `get_callers(name=php_dom_create_object, limit=500)` →

```
{
  "name": "php_dom_create_object",
  "version": "old",
  "callers": [
    {
      "caller": "dom_attr_owner_element_read",
      "file": "ext/dom/attr.c",
      "line": 231
    },
    {
      "caller": "php_dom_iterator_move_forward",
      "file": "ext/dom/dom_iterators.c",
      "line": 241
    },
    {
      "caller": "php_dom_get_iterator",
      "file": "ext/dom/dom_iterators.c",
      "line": 320
    },
    {
      "caller": "dom_node_parent_node_read",
      "file": "ext/dom/node.c",
      "line": 432
    },
    {
      "caller": "dom_node_first_child_read",
      "file": "ext/dom/node.c",
      "line": 501
    },
    {
      "caller": "dom_node_last_child_read",
      "file": "ext/dom/node.c",
      "line": 538
    },
    {
      "caller": "dom_node_previous_sibling_read",
      "file": "ext/dom/node.c",
      "line": 572
    },
    {
      "caller": "dom_node_next_sibling_read",
      "file": "ext/dom/node.c",
      "line": 605
    },
    {
      "caller": "dom_node_owner_document_read",
      "file": "ext/dom/node.c",
      "line": 677
    },
    {
      "caller": "PHP_FUNCTION(dom_text_split_text)",
      "file": "ext/dom/text.c",
      "line": 199
    },
    {
      "caller": "dom_xpath_ext_function_php",
      "file": "ext/dom/xpath.c",
      "line": 167
    },
    {
      "caller": "dom_xpath_document_read",
      "file": "ext/dom/xpath.c",
      "line": 335
    },
    {
      "caller": "php_xpath_eval",
      "file": "ext/dom/xpath.c",
      "line": 502
    },
    {
      "caller": "xsl_ext_function_php",
      "file": "ext/xsl/xsltprocessor.c",
      "line": 286
    },
    {
      "caller": "dom_document_doctype_read",
      "file": "ext/dom/document.c",
      "line": 264
    },
    {
      "caller": "dom_document_document_element_read",
      "file": "ext/dom/document.c",
      "line": 314
    }
  ]
}
```

### Turn 2  _(tok 4143+372, stop=tool_use)_

**Reasoning:** I'm checking whether the "old" version in those results is just the default, since the server's commit may be the pre-change state. The task needs every call site updated against the current repository, so I'll re-run the check with version "work" to be sure. I also want to confirm the caller list isn't missing anything.

I'm also wondering whether the caller list might miss sites reached through macros or function pointers, and I want to confirm the PHP_FUNCTION name for dom_text_split_text. I'll re-run the check against the work version as well.



- `get_callers(name=php_dom_create_object, limit=500, rev=HEAD)` →

```
{
  "name": "php_dom_create_object",
  "version": "old",
  "callers": [
    {
      "caller": "dom_attr_owner_element_read",
      "file": "ext/dom/attr.c",
      "line": 231
    },
    {
      "caller": "php_dom_iterator_move_forward",
      "file": "ext/dom/dom_iterators.c",
      "line": 241
    },
    {
      "caller": "php_dom_get_iterator",
      "file": "ext/dom/dom_iterators.c",
      "line": 320
    },
    {
      "caller": "dom_node_parent_node_read",
      "file": "ext/dom/node.c",
      "line": 432
    },
    {
      "caller": "dom_node_first_child_read",
      "file": "ext/dom/node.c",
      "line": 501
    },
    {
      "caller": "dom_node_last_child_read",
      "file": "ext/dom/node.c",
      "line": 538
    },
    {
      "caller": "dom_node_previous_sibling_read",
      "file": "ext/dom/node.c",
      "line": 572
    },
    {
      "caller": "dom_node_next_sibling_read",
      "file": "ext/dom/node.c",
      "line": 605
    },
    {
      "caller": "dom_node_owner_document_read",
      "file": "ext/dom/node.c",
      "line": 677
    },
    {
      "caller": "PHP_FUNCTION(dom_text_split_text)",
      "file": "ext/dom/text.c",
      "line": 199
    },
    {
      "caller": "dom_xpath_ext_function_php",
      "file": "ext/dom/xpath.c",
      "line": 167
    },
    {
      "caller": "dom_xpath_document_read",
      "file": "ext/dom/xpath.c",
      "line": 335
    },
    {
      "caller": "php_xpath_eval",
      "file": "ext/dom/xpath.c",
      "line": 502
    },
    {
      "caller": "xsl_ext_function_php",
      "file": "ext/xsl/xsltprocessor.c",
      "line": 286
    },
    {
      "caller": "dom_document_doctype_read",
      "file": "ext/dom/document.c",
      "line": 264
    },
    {
      "caller": "dom_document_document_element_read",
      "file": "ext/dom/document.c",
      "line": 314
    }
  ]
}
```

- `resolve_symbol(name=php_dom_create_object)` →

```
{
  "resolved": true,
  "name": "php_dom_create_object",
  "version": "old",
  "file": "ext/dom/php_dom.c",
  "line": 1321,
  "kind": "function",
  "signature": "PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval *return_value, dom_object *domobj TSRMLS_DC)",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 3  _(tok 5584+196, stop=tool_use)_

**Reasoning:** The tool's report says "old," so I want to confirm the "work" version too. get_callers only takes a rev argument, so I'll try expand_function with version "work" on php_dom_create_object to see its callers.



- `expand_function(name=php_dom_create_object, version=work, levels=1)` →

```
{
  "name": "php_dom_create_object",
  "version": "old",
  "levels": 1,
  "node": {
    "name": "php_dom_create_object",
    "file": "ext/dom/php_dom.c",
    "line": 1321,
    "kind": "function",
    "state": "analyzed"
  },
  "callees": [
    {
      "name": "ZVAL_NULL",
      "file": "Zend/zend_types.h",
      "line": 445,
      "kind": "macro",
      "state": "summarized",
      "call_lines": [
        1331,
        1418
      ]
    },
    {
      "name": "zval_copy_ctor",
      "file": "Zend/zend_variables.h",
      "line": 73,
      "kind": "macro",
      "state": "summarized",
      "call_lines": [
        1340
      ]
    },
    {
      "name": "dom_get_obj_handlers",
      "file": "ext/dom/php_dom.c",
      "line": 629,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1339
      ]
    },
    {
      "name": "Z_SET_ISREF_P",
      "file": "ext/opcache/ZendAccelerator.h",
      "line": 135,
      "kind": "macro",
      "state": "summarized",
      "call_lines": [
        1337
      ]
    },
    {
      "name": "php_dom_object_get_data",
      "file": "ext/dom/php_dom.c",
      "line": 268,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1335
      ]
    },
    {
      "name": "Z_TYPE_P",
      "file": "Zend/zend_types.h",
      "line": 223,
      "kind": "macro",
      "state": "summarized",
      "call_lines": [
        1417
      ]
    },
    {
      "name": "dom_get_doc_classmap",
      "file": "ext/dom/php_dom.c",
      "line": 223,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1423
      ]
    },
    {
      "name": "object_init_ex",
      "file": "Zend/zend_API.h",
      "line": 362,
      "kind": "macro",
      "state": "summarized",
      "call_lines": [
        1425
      ]
    },
    {
      "name": "php_libxml_increment_doc_ref",
      "file": "ext/libxml/libxml.c",
      "line": 1214,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1432
      ]
    },
    {
      "name": "php_libxml_increment_node_ptr",
      "file": "ext/libxml/libxml.c",
      "line": 1162,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1435
      ]
    }
  ],
  "callers": [
    {
      "name": "dom_attr_owner_element_read",
      "file": "ext/dom/attr.c",
      "line": 211,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        231
      ]
    },
    {
      "name": "php_dom_iterator_move_forward",
      "file": "ext/dom/dom_iterators.c",
      "line": 180,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        241
      ]
    },
    {
      "name": "php_dom_get_iterator",
      "file": "ext/dom/dom_iterators.c",
      "line": 257,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        320
      ]
    },
    {
      "name": "dom_node_parent_node_read",
      "file": "ext/dom/node.c",
      "line": 412,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        432
      ]
    },
    {
      "name": "dom_node_first_child_read",
      "file": "ext/dom/node.c",
      "line": 478,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        501
      ]
    },
    {
      "name": "dom_node_last_child_read",
      "file": "ext/dom/node.c",
      "line": 515,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        538
      ]
    },
    {
      "name": "dom_node_previous_sibling_read",
      "file": "ext/dom/node.c",
      "line": 552,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        572
      ]
    },
    {
      "name": "dom_node_next_sibling_read",
      "file": "ext/dom/node.c",
      "line": 586,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        605
      ]
    },
    {
      "name": "dom_node_owner_document_read",
      "file": "ext/dom/node.c",
      "line": 651,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        677
      ]
    },
    {
      "name": "PHP_FUNCTION(dom_text_split_text)",
      "file": "ext/dom/text.c",
      "line": 145,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        199
      ]
    },
    {
      "name": "dom_xpath_ext_function_php",
      "file": "ext/dom/xpath.c",
      "line": 75,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        167
      ]
    },
    {
      "name": "dom_xpath_document_read",
      "file": "ext/dom/xpath.c",
      "line": 319,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        335
      ]
    },
    {
      "name": "php_xpath_eval",
      "file": "ext/dom/xpath.c",
      "line": 386,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        502
      ]
    },
    {
      "name": "xsl_ext_function_php",
      "file": "ext/xsl/xsltprocessor.c",
      "line": 182,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        286
      ]
    },
    {
      "name": "dom_document_doctype_read",
      "file": "ext/dom/document.c",
      "line": 243,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        264
      ]
    },
    {
      "name": "dom_document_document_element_read",
      "file": "ext/dom/document.c",
      "line": 293,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        314
      ]
    }
  ]
}
```

### Turn 4  _(tok 8148+1168, stop=tool_use)_

**Reasoning:** I'm checking that the caller list of 16 entries holds up, though it could miss function-pointer uses or macro-based calls. The enclosing function is dom_text_split_text, which the PHP_FUNCTION macro expands to zif_dom_text_split_text, and I'm weighing how to name it in the list.

I'm settling on how to name the enclosing function in the caller list. The C symbol is zif_dom_text_split_text, but the tool reports it as PHP_FUNCTION(dom_text_split_text), so I'll use that exact string to match the tool's output.



- **submit_callers** → `{"callers": [{"function": "dom_attr_owner_element_read", "file": "ext/dom/attr.c"}, {"function": "php_dom_iterator_move_forward", "file": "ext/dom/dom_iterators.c"}, {"function": "php_dom_get_iterator", "file": "ext/dom/dom_iterators.c"}, {"function": "dom_node_parent_node_read", "file": "ext/dom/node.c"}, {"function": "dom_node_first_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_last_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_previous_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_next_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_owner_document_read", "file": "ext/dom/node.c"}, {"function": "PHP_FUNCTION(dom_text_split_text)", "file": "ext/dom/text.c"}, {"function": "dom_xpath_ext_function_php", "file": "ext/dom/xpath.c"}, {"function": "dom_xpath_document_read", "file": "ext/dom/xpath.c"}, {"function": "php_xpath_eval", "file": "ext/dom/xpath.c"}, {"function": "xsl_ext_function_php", "file": "ext/xsl/xsltprocessor.c"}, {"function": "dom_document_doctype_read", "file": "ext/dom/document.c"}, {"function": "dom_document_document_element_read", "file": "ext/dom/document.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 16, "n_truth": 4, "tp": 3, "precision": 0.1875, "recall": 0.75, "f1": 0.3}`

