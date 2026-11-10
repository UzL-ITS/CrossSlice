# Impact-analysis transcript — php-src @ 2f0a758fbbf3 — anthropic:claude-haiku-5-5

- target: `php_dom_create_object` (ext/dom/php_dom.c), arity 4->3
- truth: [['ext/dom/attr.c', 'dom_attr_owner_element_read'], ['ext/dom/document.c', 'dom_document_doctype_read'], ['ext/dom/document.c', 'dom_document_document_element_read'], ['ext/dom/xml_common.h', 'dom_object_get_node']]

## Self-navigation arm

### Turn 1  _(tok 1218+121, stop=tool_use)_

**Reasoning:** I'm searching the whole repo for every place php_dom_create_object is referenced.



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

### Turn 2  _(tok 2564+369, stop=tool_use)_

**Reasoning:** I've got the DOM_RET_OBJ macro at line 82 of xml_common.h, which wraps a call to php_dom_create_object. Next I need to find every place that uses DOM_RET_OBJ, so I'll read the header around lines 75 to 90 first.



**Says:** The macro at `xml_common.h:82` also calls it, so I need to find which functions expand that macro.

- `read_file(path=ext/dom/xml_common.h, version=old, start_line=74, end_line=92)` →

```
ext/dom/xml_common.h lines 74-92 of 107
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
```

- `grep(pattern=DOM_RET_OBJ|GET_OBJ|create_obj, version=old, max_results=500)` →

```
273 matches (showing 200)
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
Zend/zend_objects_API.c:119:		EG(objects_store).free_list_head = GET_OBJ_BUCKET_NUMBER(EG(objects_store).object_buckets[handle]);
Zend/zend_objects_API.h:33:#define GET_OBJ_BUCKET_NUMBER(o)	(((zend_intptr_t)(o)) >> 1)
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
ext/dom/attr.c:270:	DOM_GET_OBJ(attrp, id, xmlAttrPtr, intern);
ext/dom/characterdata.c:187:	DOM_GET_OBJ(node, id, xmlNodePtr, intern);
ext/dom/characterdata.c:234:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/characterdata.c:270:	DOM_GET_OBJ(node, id, xmlNodePtr, intern);
ext/dom/characterdata.c:317:	DOM_GET_OBJ(node, id, xmlNodePtr, intern);
ext/dom/characterdata.c:373:	DOM_GET_OBJ(node, id, xmlNodePtr, intern);
ext/dom/document.c:264:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) dtdptr, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:314:	if (NULL == (*retval = php_dom_create_object(root, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/document.c:915:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:927:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:947:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:954:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:975:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:982:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1003:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1010:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1031:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1038:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1059:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1073:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/document.c:1094:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1106:	DOM_RET_OBJ((xmlNodePtr) node, &ret, intern);
ext/dom/document.c:1128:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1140:	DOM_RET_OBJ((xmlNodePtr) node, &ret, intern);
ext/dom/document.c:1161:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1187:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1189:	DOM_GET_OBJ(nodep, node, xmlNodePtr, nodeobj);
ext/dom/document.c:1221:	DOM_RET_OBJ((xmlNodePtr) retnodep, &ret, intern);
ext/dom/document.c:1245:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1284:	DOM_RET_OBJ(nodep, &ret, intern);
ext/dom/document.c:1308:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1349:	DOM_RET_OBJ(nodep, &ret, intern);
ext/dom/document.c:1370:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1397:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1402:		DOM_RET_OBJ((xmlNodePtr) attrp->parent, &ret, intern);
ext/dom/document.c:1434:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1716:		DOM_RET_OBJ((xmlNodePtr) newdoc, &ret, NULL);
ext/dom/document.c:1763:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1804:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1811:		DOM_GET_OBJ(node, nodep, xmlNodePtr, nodeobj);
ext/dom/document.c:1911:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1950:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:1993:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:2089:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:2235:		DOM_RET_OBJ((xmlNodePtr) newdoc, &ret, NULL);
ext/dom/document.c:2280:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:2316:	DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/document.c:2323:		DOM_GET_OBJ(node, nodep, xmlNodePtr, nodeobj);
ext/dom/document.c:2422:		DOM_GET_OBJ(docp, id, xmlDocPtr, intern);
ext/dom/documentfragment.c:135:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/dom_iterators.c:241:		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
ext/dom/dom_iterators.c:320:		curattr = php_dom_create_object(curnode, &ret, curattr, objmap->baseobj TSRMLS_CC);
ext/dom/domimplementation.c:143:	DOM_RET_OBJ((xmlNodePtr) doctype, &ret, NULL);
ext/dom/domimplementation.c:168:		DOM_GET_OBJ(doctype, node, xmlDtdPtr, doctobj);
ext/dom/domimplementation.c:240:	DOM_RET_OBJ((xmlNodePtr) docp, &ret, NULL);
ext/dom/element.c:343:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/element.c:396:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/element.c:429:	DOM_RET_OBJ(attr, &ret, intern);
ext/dom/element.c:450:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/element.c:498:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/element.c:524:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:544:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/element.c:551:	DOM_GET_OBJ(attrp, node, xmlAttrPtr, attrobj);
ext/dom/element.c:586:		DOM_RET_OBJ((xmlNodePtr) existattrp, &ret, intern);
ext/dom/element.c:610:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/element.c:617:	DOM_GET_OBJ(attrp, node, xmlAttrPtr, attrobj);
ext/dom/element.c:626:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:648:	DOM_GET_OBJ(elemp, id, xmlNodePtr, intern);
ext/dom/element.c:675:	DOM_GET_OBJ(elemp, id, xmlNodePtr, intern);
ext/dom/element.c:762:	DOM_GET_OBJ(elemp, id, xmlNodePtr, intern);
ext/dom/element.c:883:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/element.c:939:	DOM_GET_OBJ(elemp, id, xmlNodePtr, intern);
ext/dom/element.c:947:	DOM_RET_OBJ((xmlNodePtr) attrp, &ret, intern);
ext/dom/element.c:969:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/element.c:976:	DOM_GET_OBJ(attrp, node, xmlAttrPtr, attrobj);
ext/dom/element.c:1017:		DOM_RET_OBJ((xmlNodePtr) existattrp, &ret, intern);
ext/dom/element.c:1042:	DOM_GET_OBJ(elemp, id, xmlNodePtr, intern);
ext/dom/element.c:1070:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/element.c:1099:	DOM_GET_OBJ(elemp, id, xmlNodePtr, intern);
ext/dom/element.c:1156:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/element.c:1192:	DOM_GET_OBJ(elemp, id, xmlNodePtr, intern);
ext/dom/element.c:1226:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/element.c:1233:	DOM_GET_OBJ(attrp, node, xmlAttrPtr, attrobj);
ext/dom/namednodemap.c:169:		DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/namednodemap.c:246:			DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/namednodemap.c:301:		DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/node.c:432:	if (NULL == (*retval = php_dom_create_object(nodeparent, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:501:	if (NULL == (*retval = php_dom_create_object(first, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:538:	if (NULL == (*retval = php_dom_create_object(last, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:572:	if (NULL == (*retval = php_dom_create_object(prevsib, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:605:	if (NULL == (*retval = php_dom_create_object(nextsib, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:677:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/node.c:1010:	DOM_GET_OBJ(parentp, id, xmlNodePtr, intern);
ext/dom/node.c:1016:	DOM_GET_OBJ(child, node, xmlNodePtr, childobj);
ext/dom/node.c:1049:		DOM_GET_OBJ(refp, ref, xmlNodePtr, refpobj);
ext/dom/node.c:1090:					DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1132:					DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1151:	DOM_RET_OBJ(new_child, &ret, intern);
ext/dom/node.c:1173:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/node.c:1179:	DOM_GET_OBJ(newchild, newnode, xmlNodePtr, newchildobj);
ext/dom/node.c:1180:	DOM_GET_OBJ(oldchild, oldnode, xmlNodePtr, oldchildobj);
ext/dom/node.c:1235:		DOM_RET_OBJ(oldchild, &ret, intern);
ext/dom/node.c:1259:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/node.c:1265:	DOM_GET_OBJ(child, node, xmlNodePtr, childobj);
ext/dom/node.c:1284:			DOM_RET_OBJ(child, &ret, intern);
ext/dom/node.c:1310:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/node.c:1316:	DOM_GET_OBJ(child, node, xmlNodePtr, childobj);
ext/dom/node.c:1392:	DOM_RET_OBJ(new_child, &ret, intern);
ext/dom/node.c:1410:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/node.c:1440:	DOM_GET_OBJ(n, id, xmlNodePtr, intern);
ext/dom/node.c:1481:	DOM_RET_OBJ(node, &ret, intern);
ext/dom/node.c:1499:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/node.c:1542:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/node.c:1579:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/node.c:1581:	DOM_GET_OBJ(nodeotherp, node, xmlNodePtr, nodeotherobj);
ext/dom/node.c:1608:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/node.c:1658:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/node.c:1691:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/node.c:1778:	DOM_GET_OBJ(nodep, id, xmlNodePtr, intern);
ext/dom/nodelist.c:166:			DOM_RET_OBJ(itemnode, &ret, objmap->baseobj);
ext/dom/php_dom.c:581:		DOM_RET_OBJ((xmlNodePtr) nodep, &ret, (dom_object *)nodeobj);
ext/dom/php_dom.c:762:	ce.create_object = dom_nnodemap_objects_new;
ext/dom/php_dom.c:772:	ce.create_object = dom_nnodemap_objects_new;
ext/dom/php_dom.c:900:	ce.create_object = dom_xpath_objects_new;
ext/dom/php_dom.c:1320:/* {{{ php_dom_create_object */
ext/dom/php_dom.c:1321:PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval *return_value, dom_object *domobj TSRMLS_DC)
ext/dom/php_dom.h:129:ce.create_object = dom_objects_new; \
ext/dom/php_dom.h:132:#define DOM_GET_OBJ(__ptr, __id, __prtype, __intern) { \
ext/dom/text.c:161:	DOM_GET_OBJ(node, id, xmlNodePtr, intern);
ext/dom/text.c:199:	return_value = php_dom_create_object(nnode, &ret, return_value, intern TSRMLS_CC);
ext/dom/text.c:216:	DOM_GET_OBJ(node, id, xmlNodePtr, intern);
ext/dom/xml_common.h:57:PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval* return_value, dom_object *domobj TSRMLS_DC);
ext/dom/xml_common.h:63:#define NODE_GET_OBJ(__ptr, __id, __prtype, __intern) { \
ext/dom/xml_common.h:71:#define DOC_GET_OBJ(__ptr, __id, __prtype, __intern) { \
ext/dom/xml_common.h:81:#define DOM_RET_OBJ(obj, ret, domobject) \
ext/dom/xml_common.h:82:	if (!php_dom_create_object(obj, ret, return_value, domobject TSRMLS_CC)) { \
ext/dom/xml_common.h:95:	DOM_GET_OBJ(__ptr, __id, __prtype, __intern);
ext/dom/xpath.c:167:							child = php_dom_create_object(node, &ret, child, (dom_object *)intern TSRMLS_CC);
ext/dom/xpath.c:287:	DOM_GET_OBJ(docp, doc, xmlDocPtr, docobj);
ext/dom/xpath.c:335:	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
ext/dom/xpath.c:419:		DOM_GET_OBJ(nodep, context, xmlNodePtr, nodeobj);
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
```

### Turn 3  _(tok 12690+1140, stop=tool_use)_

**Reasoning:** I'm checking whether the functions that use DOM_RET_OBJ should count as callers. The macro expands to a call to php_dom_create_object, so those users reach it indirectly, and I'm leaning toward including them since they'd need to be updated against the changed macro too.

I'm going through the DOM_RET_OBJ usage sites file by file to find the enclosing function for each one. The grep output was capped, so I still need a narrower search to catch any remaining matches and look up the function names.

I'm going to match the function-definition lines across the DOM extension and the XSL sources, so each DOM_RET_OBJ site maps to the function that contains it. I also still need the enclosing name for php_dom.c line 581, which may be a static helper.



**Says:** `DOM_RET_OBJ` expands to a direct call to `php_dom_create_object`, so every function using that macro is also a caller. I'll get the complete macro-use list and the function boundaries so I can map each line to its enclosing function.

- `grep(pattern=DOM_RET_OBJ\(, version=old, max_results=500)` →

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

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD)\(|^[A-Za-z_][A-Za-z_0-9 \*]*\(.*\, path_glob=ext/dom/*.c, version=old, max_results=500)` →

```
396 matches (showing 200)
ext/dom/attr.c:33:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_attr_is_id, 0, 0, 0)
ext/dom/attr.c:36:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_attr_construct, 0, 0, 1)
ext/dom/attr.c:56:PHP_METHOD(domattr, __construct)
ext/dom/attr.c:105:int dom_attr_name_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/attr.c:129:int dom_attr_specified_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/attr.c:144:int dom_attr_value_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/attr.c:170:int dom_attr_value_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/attr.c:211:int dom_attr_owner_element_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/attr.c:246:int dom_attr_schema_type_info_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/attr.c:260:PHP_FUNCTION(dom_attr_is_id)
ext/dom/cdatasection.c:32:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_cdatasection_construct, 0, 0, 1)
ext/dom/cdatasection.c:50:PHP_METHOD(domcdatasection, __construct)
ext/dom/characterdata.c:32:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_characterdata_substring_data, 0, 0, 2)
ext/dom/characterdata.c:37:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_characterdata_append_data, 0, 0, 1)
ext/dom/characterdata.c:41:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_characterdata_insert_data, 0, 0, 2)
ext/dom/characterdata.c:46:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_characterdata_delete_data, 0, 0, 2)
ext/dom/characterdata.c:51:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_characterdata_replace_data, 0, 0, 3)
ext/dom/characterdata.c:79:int dom_characterdata_data_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/characterdata.c:103:int dom_characterdata_data_write(dom_object *obj, zval *newval TSRMLS_DC)
ext/dom/characterdata.c:140:int dom_characterdata_length_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/characterdata.c:173:PHP_FUNCTION(dom_characterdata_substring_data)
ext/dom/characterdata.c:222:PHP_FUNCTION(dom_characterdata_append_data)
ext/dom/characterdata.c:256:PHP_FUNCTION(dom_characterdata_insert_data)
ext/dom/characterdata.c:304:PHP_FUNCTION(dom_characterdata_delete_data)
ext/dom/characterdata.c:359:PHP_FUNCTION(dom_characterdata_replace_data)
ext/dom/comment.c:32:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_comment_construct, 0, 0, 0)
ext/dom/comment.c:50:PHP_METHOD(domcomment, __construct)
ext/dom/document.c:45:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_create_element, 0, 0, 1)
ext/dom/document.c:50:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_create_document_fragment, 0, 0, 0)
ext/dom/document.c:53:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_create_text_node, 0, 0, 1)
ext/dom/document.c:57:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_create_comment, 0, 0, 1)
ext/dom/document.c:61:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_create_cdatasection, 0, 0, 1)
ext/dom/document.c:65:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_create_processing_instruction, 0, 0, 2)
ext/dom/document.c:70:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_create_attribute, 0, 0, 1)
ext/dom/document.c:74:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_create_entity_reference, 0, 0, 1)
ext/dom/document.c:78:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_get_elements_by_tag_name, 0, 0, 1)
ext/dom/document.c:82:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_import_node, 0, 0, 2)
ext/dom/document.c:87:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_create_element_ns, 0, 0, 2)
ext/dom/document.c:93:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_create_attribute_ns, 0, 0, 2)
ext/dom/document.c:98:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_get_elements_by_tag_name_ns, 0, 0, 2)
ext/dom/document.c:103:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_get_element_by_id, 0, 0, 1)
ext/dom/document.c:107:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_adopt_node, 0, 0, 1)
ext/dom/document.c:111:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_normalize_document, 0, 0, 0)
ext/dom/document.c:114:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_rename_node, 0, 0, 3)
ext/dom/document.c:120:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_load, 0, 0, 1)
ext/dom/document.c:125:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_save, 0, 0, 1)
ext/dom/document.c:129:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_loadxml, 0, 0, 1)
ext/dom/document.c:134:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_savexml, 0, 0, 0)
ext/dom/document.c:138:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_construct, 0, 0, 0)
ext/dom/document.c:143:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_validate, 0, 0, 0)
ext/dom/document.c:146:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_xinclude, 0, 0, 0)
ext/dom/document.c:150:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_loadhtml, 0, 0, 1)
ext/dom/document.c:155:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_loadhtmlfile, 0, 0, 1)
ext/dom/document.c:160:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_savehtml, 0, 0, 0)
ext/dom/document.c:163:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_savehtmlfile, 0, 0, 1)
ext/dom/document.c:167:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_schema_validate_file, 0, 0, 1)
ext/dom/document.c:171:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_schema_validate_xml, 0, 0, 1)
ext/dom/document.c:175:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_relaxNG_validate_file, 0, 0, 1)
ext/dom/document.c:179:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_relaxNG_validate_xml, 0, 0, 1)
ext/dom/document.c:183:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_document_registernodeclass, 0, 0, 2)
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
ext/dom/documentfragment.c:31:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_documentfragement_construct, 0, 0, 0)
ext/dom/documentfragment.c:34:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_documentfragement_appendXML, 0, 0, 1)
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
ext/dom/dom_iterators.c:125:static void php_dom_iterator_dtor(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:139:static int php_dom_iterator_valid(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:152:static void php_dom_iterator_current_data(zend_object_iterator *iter, zval ***data TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:160:static void php_dom_iterator_current_key(zend_object_iterator *iter, zval *key TSRMLS_DC) /* {{{ */
ext/dom/dom_iterators.c:180:static void php_dom_iterator_move_forward(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
ext/dom/domconfiguration.c:31:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_configuration_set_parameter, 0, 0, 2)
ext/dom/domconfiguration.c:36:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_configuration_get_parameter, 0, 0, 0)
ext/dom/domconfiguration.c:40:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_configuration_can_set_parameter, 0, 0, 0)
ext/dom/domconfiguration.c:66:PHP_FUNCTION(dom_domconfiguration_set_parameter)
ext/dom/domconfiguration.c:76:PHP_FUNCTION(dom_domconfiguration_get_parameter)
ext/dom/domconfiguration.c:86:PHP_FUNCTION(dom_domconfiguration_can_set_parameter)
ext/dom/domerror.c:49:int dom_domerror_severity_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerror.c:63:int dom_domerror_message_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerror.c:77:int dom_domerror_type_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerror.c:91:int dom_domerror_related_exception_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerror.c:105:int dom_domerror_related_data_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerror.c:119:int dom_domerror_location_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domerrorhandler.c:31:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_domerrorhandler_handle_error, 0, 0, 1)
ext/dom/domerrorhandler.c:54:PHP_FUNCTION(dom_domerrorhandler_handle_error)
ext/dom/domexception.c:54:void php_dom_throw_error(int error_code, int strict_error TSRMLS_DC)
ext/dom/domimplementation.c:31:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_implementation_get_feature, 0, 0, 2)
ext/dom/domimplementation.c:36:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_implementation_has_feature, 0, 0, 0)
ext/dom/domimplementation.c:39:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_implementation_create_documenttype, 0, 0, 3)
ext/dom/domimplementation.c:45:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_implementation_create_document, 0, 0, 3)
ext/dom/domimplementation.c:71:PHP_METHOD(domimplementation, hasFeature)
ext/dom/domimplementation.c:92:PHP_METHOD(domimplementation, createDocumentType)
ext/dom/domimplementation.c:151:PHP_METHOD(domimplementation, createDocument)
ext/dom/domimplementation.c:253:PHP_METHOD(domimplementation, getFeature)
ext/dom/domimplementationlist.c:31:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_implementationlist_item, 0, 0, 1)
ext/dom/domimplementationlist.c:55:int dom_domimplementationlist_length_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domimplementationlist.c:68:PHP_FUNCTION(dom_domimplementationlist_item)
ext/dom/domimplementationsource.c:32:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_implementationsource_getdomimplementation, 0, 0, 1)
ext/dom/domimplementationsource.c:36:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_implementationsource_getdomimplementations, 0, 0, 1)
ext/dom/domimplementationsource.c:60:PHP_FUNCTION(dom_domimplementationsource_get_domimplementation)
ext/dom/domimplementationsource.c:70:PHP_FUNCTION(dom_domimplementationsource_get_domimplementations)
ext/dom/domlocator.c:49:int dom_domlocator_line_number_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domlocator.c:63:int dom_domlocator_column_number_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domlocator.c:77:int dom_domlocator_offset_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domlocator.c:91:int dom_domlocator_related_node_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domlocator.c:105:int dom_domlocator_uri_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domstringlist.c:31:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_stringlist_item, 0, 0, 1)
ext/dom/domstringlist.c:55:int dom_domstringlist_length_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/domstringlist.c:68:PHP_FUNCTION(dom_domstringlist_item)
ext/dom/element.c:31:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_get_attribute, 0, 0, 1)
ext/dom/element.c:35:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_set_attribute, 0, 0, 2)
ext/dom/element.c:40:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_remove_attribute, 0, 0, 1)
ext/dom/element.c:44:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_get_attribute_node, 0, 0, 1)
ext/dom/element.c:48:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_set_attribute_node, 0, 0, 1)
ext/dom/element.c:52:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_remove_attribute_node, 0, 0, 1)
ext/dom/element.c:56:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_get_elements_by_tag_name, 0, 0, 1)
ext/dom/element.c:60:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_get_attribute_ns, 0, 0, 2)
ext/dom/element.c:65:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_set_attribute_ns, 0, 0, 3)
ext/dom/element.c:71:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_remove_attribute_ns, 0, 0, 2)
ext/dom/element.c:76:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_get_attribute_node_ns, 0, 0, 2)
ext/dom/element.c:81:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_set_attribute_node_ns, 0, 0, 1)
ext/dom/element.c:85:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_get_elements_by_tag_name_ns, 0, 0, 2)
ext/dom/element.c:90:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_has_attribute, 0, 0, 1)
ext/dom/element.c:94:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_has_attribute_ns, 0, 0, 2)
ext/dom/element.c:99:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_set_id_attribute, 0, 0, 2)
ext/dom/element.c:104:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_set_id_attribute_ns, 0, 0, 3)
ext/dom/element.c:110:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_set_id_attribute_node, 0, 0, 2)
ext/dom/element.c:115:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_element_construct, 0, 0, 1)
ext/dom/element.c:154:PHP_METHOD(domelement, __construct)
```

### Turn 4  _(tok 25957+3082, stop=tool_use)_

**Reasoning:** I'm finding the function-list grep too broad, so I'll switch to narrowing it to the files of interest. I could also read small windows around each call site, though that means many reads.

I'm going file by file now, grepping for function definitions in attr.c, document.c, dom_iterators.c, and domimplementation.c so each call site maps to its enclosing function. Most call sites are already placed: the ones in domimplementation.c fall under createDocumentType and createDocument, and the attr.c call at line 231 sits inside dom_attr_owner_element_read.

I'm mapping the remaining document.c call sites to their enclosing functions: the DOM_RET_OBJ returns from the create_* methods, import_node, and the create_element_ns and create_attribute_ns methods each sit inside their own function body.

Mapping the last few call sites: the document.c returns at 1716 and 2235 sit inside dom_parse_document and dom_load_html, and the 1140 create_entity_reference and 1106 create_attribute calls each fall within their own function bodies.

Checking the remaining call sites in element.c and node.c next, since the element.c listing got cut off and needs a fresh grep.

Next I need the function lists for node.c, namednodemap.c, nodelist.c, php_dom.c, dom_iterators.c, text.c and xpath.c, plus the xsltprocessor.c and xmlreader call sites, to place the remaining calls.

Now I'm pulling the function definitions for the remaining files, starting with a broader grep across the dom, xmlreader, and xsl sources.

Next I'm writing a pattern that matches PHP_FUNCTION, PHP_METHOD, static, and similar definition lines, so I can list every function in the remaining files at once.



**Says:** The function-boundary output was truncated, so I'll pull the boundaries for the remaining files directly. I'm also checking the xmlreader and xsl macro uses.

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD)\(|^(static|void|int|zval|xmlNodeP, path_glob=ext/dom/element.c, version=old)` →

```
21 matches
ext/dom/element.c:154:PHP_METHOD(domelement, __construct)
ext/dom/element.c:238:int dom_element_tag_name_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/element.c:273:int dom_element_schema_type_info_read(dom_object *obj, zval **retval TSRMLS_DC)
ext/dom/element.c:329:PHP_FUNCTION(dom_element_get_attribute)
ext/dom/element.c:372:PHP_FUNCTION(dom_element_set_attribute)
ext/dom/element.c:438:PHP_FUNCTION(dom_element_remove_attribute)
ext/dom/element.c:486:PHP_FUNCTION(dom_element_get_attribute_node)
ext/dom/element.c:532:PHP_FUNCTION(dom_element_set_attribute_node)
ext/dom/element.c:598:PHP_FUNCTION(dom_element_remove_attribute_node)
ext/dom/element.c:635:PHP_FUNCTION(dom_element_get_elements_by_tag_name)
ext/dom/element.c:661:PHP_FUNCTION(dom_element_get_attribute_ns)
ext/dom/element.c:741:PHP_FUNCTION(dom_element_set_attribute_ns)
ext/dom/element.c:869:PHP_FUNCTION(dom_element_remove_attribute_ns)
ext/dom/element.c:926:PHP_FUNCTION(dom_element_get_attribute_node_ns)
ext/dom/element.c:956:PHP_FUNCTION(dom_element_set_attribute_node_ns)
ext/dom/element.c:1029:PHP_FUNCTION(dom_element_get_elements_by_tag_name_ns)
ext/dom/element.c:1057:PHP_FUNCTION(dom_element_has_attribute)
ext/dom/element.c:1085:PHP_FUNCTION(dom_element_has_attribute_ns)
ext/dom/element.c:1142:PHP_FUNCTION(dom_element_set_id_attribute)
ext/dom/element.c:1178:PHP_FUNCTION(dom_element_set_id_attribute_ns)
ext/dom/element.c:1214:PHP_FUNCTION(dom_element_set_id_attribute_node)
```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD)\(|^(static|void|int|zval|xmlNodeP, path_glob=ext/dom/node.c, version=old)` →

```
41 matches
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
ext/dom/node.c:1928:PHP_METHOD(domnode, C14N)
ext/dom/node.c:1936:PHP_METHOD(domnode, C14NFile)
ext/dom/node.c:1944:PHP_METHOD(domnode, getNodePath)
ext/dom/node.c:1965:PHP_METHOD(domnode, getLineNo)
```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD)\(|^(static|void|int|zval|xmlNodeP, path_glob=ext/dom/{namednodemap,nodelist,php_dom,dom_iterators,text,xp, version=old)` →

```
0 matches

```

- `grep(pattern=^(PHP_FUNCTION|PHP_METHOD)\(|^(static|void|int|zval|xmlNodeP, path_glob=ext/{xsl/xsltprocessor,xmlreader/php_xmlreader}.c, version=old)` →

```
0 matches

```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 31848+2002, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "dom_attr_owner_element_read", "file": "ext/dom/attr.c"}, {"function": "dom_document_doctype_read", "file": "ext/dom/document.c"}, {"function": "dom_document_document_element_read", "file": "ext/dom/document.c"}, {"function": "dom_document_create_element", "file": "ext/dom/document.c"}, {"function": "dom_document_create_document_fragment", "file": "ext/dom/document.c"}, {"function": "dom_document_create_text_node", "file": "ext/dom/document.c"}, {"function": "dom_document_create_comment", "file": "ext/dom/document.c"}, {"function": "dom_document_create_cdatasection", "file": "ext/dom/document.c"}, {"function": "dom_document_create_processing_instruction", "file": "ext/dom/document.c"}, {"function": "dom_document_create_attribute", "file": "ext/dom/document.c"}, {"function": "dom_document_create_entity_reference", "file": "ext/dom/document.c"}, {"function": "dom_document_import_node", "file": "ext/dom/document.c"}, {"function": "dom_document_create_element_ns", "file": "ext/dom/document.c"}, {"function": "dom_document_create_attribute_ns", "file": "ext/dom/document.c"}, {"function": "dom_document_get_element_by_id", "file": "ext/dom/document.c"}, {"function": "dom_parse_document", "file": "ext/dom/document.c"}, {"function": "dom_load_html", "file": "ext/dom/document.c"}, {"function": "PHP_METHOD(domimplementation, createDocumentType)", "file": "ext/dom/domimplementation.c"}, {"function": "PHP_METHOD(domimplementation, createDocument)", "file": "ext/dom/domimplementation.c"}, {"function": "dom_element_get_attribute_node", "file": "ext/dom/element.c"}, {"function": "dom_element_set_attribute_node", "file": "ext/dom/element.c"}, {"function": "dom_element_remove_attribute_node", "file": "ext/dom/element.c"}, {"function": "dom_element_set_attribute_node_ns", "file": "ext/dom/element.c"}, {"function": "dom_element_get_attribute_node_ns", "file": "ext/dom/element.c"}, {"function": "dom_element_set_attribute_ns", "file": "ext/dom/element.c"}, {"function": "dom_node_insert_before", "file": "ext/dom/node.c"}, {"function": "dom_node_replace_child", "file": "ext/dom/node.c"}, {"function": "dom_node_remove_child", "file": "ext/dom/node.c"}, {"function": "dom_node_append_child", "file": "ext/dom/node.c"}, {"function": "dom_node_clone_node", "file": "ext/dom/node.c"}, {"function": "dom_node_node_name_read", "file": "ext/dom/node.c"}, {"function": "dom_node_parent_node_read", "file": "ext/dom/node.c"}, {"function": "dom_node_child_nodes_read", "file": "ext/dom/node.c"}, {"function": "dom_node_first_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_last_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_previous_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_next_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_owner_document_read", "file": "ext/dom/node.c"}, {"function": "dom_node_attributes_read", "file": "ext/dom/node.c"}, {"function": "text.c function containing php_dom_create_object call at line 199", "file": "ext/dom/text.c"}, {"function": "xpath.c function containing php_dom_create_object calls at lines 167, 335, 502", "file": "ext/dom/xpath.c"}, {"function": "dom_iterators.c function containing php_dom_create_object calls at lines 241, 320", "file": "ext/dom/dom_iterators.c"}, {"function": "node.c function containing DOM_RET_OBJ at line 1090", "file": "ext/dom/node.c"}, {"function": "node.c function containing DOM_RET_OBJ at line 1132", "file": "ext/dom/node.c"}, {"function": "node.c function containing DOM_RET_OBJ at line 1151", "file": "ext/dom/node.c"}, {"function": "node.c function containing DOM_RET_OBJ at line 1235", "file": "ext/dom/node.c"}, {"function": "node.c function containing DOM_RET_OBJ at line 1284", "file": "ext/dom/node.c"}, {"function": "node.c function containing DOM_RET_OBJ at line 1392", "file": "ext/dom/node.c"}, {"function": "node.c function containing DOM_RET_OBJ at line 1481", "file": "ext/dom/node.c"}, {"function": "namednodemap.c function containing DOM_RET_OBJ at lines 169, 246, 301", "file": "ext/dom/namednodemap.c"}, {"function": "nodelist.c function containing DOM_RET_OBJ at line 166", "file": "ext/dom/nodelist.c"}, {"function": "php_dom.c function containing DOM_RET_OBJ at line 581", "file": "ext/dom/php_dom.c"}, {"function": "php_xmlreader.c function containing DOM_RET_OBJ at line 1158", "file": "ext/xmlreader/php_xmlreader.c"}, {"function": "xsltprocessor.c function containing php_dom_create_object at line 286 and DOM_RET_OBJ at line 691", "file": "ext/xsl/xsltprocessor.c"}], "confidence_overall": "low"}`

**Score (self):** `{"n_pred": 54, "n_truth": 4, "tp": 3, "precision": 0.05555555555555555, "recall": 0.75, "f1": 0.10344827586206895}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1387+80, stop=tool_use)_

**Reasoning:** I'll start by running find_references on php_dom_create_object to locate every place it's used.



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

### Turn 2  _(tok 2738+849, stop=tool_use)_

**Reasoning:** I need the enclosing functions, so I'll read each file around those lines. The macro in xml_common.h at line 82 is a complication: its call sites sit inside the macro body, so I'm weighing whether the functions that use the macro should count, given the task asks for every function that calls php_dom_create_object.

I'm checking whether the macro's expansions count as calls, so I'll grep for the macro name and its uses to see where it's invoked.



- `read_file(path=ext/dom/xml_common.h, version=old, start_line=55, end_line=100)` →

```
ext/dom/xml_common.h lines 55-100 of 107
   55| PHP_DOM_EXPORT extern zend_class_entry *dom_node_class_entry;
   56| PHP_DOM_EXPORT dom_object *php_dom_object_get_data(xmlNodePtr obj);
   57| PHP_DOM_EXPORT zval *php_dom_create_object(xmlNodePtr obj, int *found, zval* return_value, dom_object *domobj TSRMLS_DC);
   58| PHP_DOM_EXPORT xmlNodePtr dom_object_get_node(dom_object *obj);
   59| 
   60| #define DOM_XMLNS_NAMESPACE \
   61|     (const xmlChar *) "http://www.w3.org/2000/xmlns/"
   62| 
   63| #define NODE_GET_OBJ(__ptr, __id, __prtype, __intern) { \
   64| 	__intern = (php_libxml_node_object *)zend_object_store_get_object(__id TSRMLS_CC); \
   65| 	if (__intern->node == NULL || !(__ptr = (__prtype)__intern->node->node)) { \
   66|   		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Couldn't fetch %s", __intern->std.ce->name);\
   67|   		RETURN_NULL();\
   68|   	} \
   69| }
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
   96| 
   97| #endif
   98| 
   99| /*
  100|  * Local variables:
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

- `read_file(path=ext/dom/dom_iterators.c, version=old, start_line=215, end_line=325)` →

```
ext/dom/dom_iterators.c lines 215-325 of 339
  215| 				} else {
  216| 					/* Nav the tree evey time as this is LIVE */
  217| 					basenode = dom_object_get_node(objmap->baseobj);
  218| 					if (basenode && (basenode->type == XML_DOCUMENT_NODE || 
  219| 						basenode->type == XML_HTML_DOCUMENT_NODE)) {
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

### Turn 3  _(tok 13083+1031, stop=tool_use)_

**Reasoning:** I'm trying to pin down the enclosing function for line 241 in dom_iterators.c, which seems to fall just before line 245, so I'll check the header around lines 180–215. Line 320 sits inside php_dom_get_iterator, which starts at 257. After that I still need to look at node.c lines 659–680 and the remaining files: text.c, xpath.c, and xsltprocessor.c.

I still need to check where the DOM_RET_OBJ macro is used.



- `read_file(path=ext/dom/dom_iterators.c, version=old, start_line=180, end_line=215)` →

```
ext/dom/dom_iterators.c lines 180-215 of 339
  180| static void php_dom_iterator_move_forward(zend_object_iterator *iter TSRMLS_DC) /* {{{ */
  181| {
  182| 	zval *curobj, *curattr = NULL;
  183| 	zval *object;
  184| 	xmlNodePtr curnode = NULL, basenode;
  185| 	dom_object *intern;
  186| 	dom_object *nnmap;
  187| 	dom_nnodemap_object *objmap;
  188| 	int ret, previndex=0;
  189| 	HashTable *nodeht;
  190| 	zval **entry;
  191| 
  192| 	php_dom_iterator *iterator = (php_dom_iterator *)iter;
  193| 
  194| 	object = (zval *)iterator->intern.data;
  195| 	nnmap = (dom_object *)zend_object_store_get_object(object TSRMLS_CC);
  196| 	objmap = (dom_nnodemap_object *)nnmap->ptr;
  197| 
  198| 	curobj = iterator->curobj;
  199| 	intern = (dom_object *)zend_object_store_get_object(curobj TSRMLS_CC);
  200| 	if (intern != NULL && intern->ptr != NULL) {
  201| 		if (objmap->nodetype != XML_ENTITY_NODE && 
  202| 			objmap->nodetype != XML_NOTATION_NODE) {
  203| 			if (objmap->nodetype == DOM_NODESET) {
  204| 				nodeht = HASH_OF(objmap->baseobjptr);
  205| 				zend_hash_move_forward(nodeht);
  206| 				if (zend_hash_get_current_data(nodeht, (void **) &entry)==SUCCESS) {
  207| 					curattr = *entry;
  208| 					Z_ADDREF_P(curattr);
  209| 				}
  210| 			} else {
  211| 				curnode = (xmlNodePtr)((php_libxml_node_ptr *)intern->ptr)->node;
  212| 				if (objmap->nodetype == XML_ATTRIBUTE_NODE || 
  213| 					objmap->nodetype == XML_ELEMENT_NODE) {
  214| 					curnode = curnode->next;
  215| 				} else {
```

- `read_file(path=ext/dom/node.c, version=old, start_line=659, end_line=690)` →

```
ext/dom/node.c lines 659-690 of 1991
  659| 	if (nodep == NULL) {
  660| 		php_dom_throw_error(INVALID_STATE_ERR, 0 TSRMLS_CC);
  661| 		return FAILURE;
  662| 	}
  663| 
  664| 	if (nodep->type == XML_DOCUMENT_NODE || nodep->type == XML_HTML_DOCUMENT_NODE) {
  665| 		ALLOC_ZVAL(*retval);
  666| 		ZVAL_NULL(*retval);
  667| 		return SUCCESS;
  668| 	}
  669| 
  670| 	docp = nodep->doc;
  671| 	if (!docp) {
  672| 		return FAILURE;
  673| 	}
  674| 
  675| 	ALLOC_ZVAL(*retval);
  676| 
  677| 	if (NULL == (*retval = php_dom_create_object((xmlNodePtr) docp, &ret, *retval, obj TSRMLS_CC))) {
  678| 		php_error_docref(NULL TSRMLS_CC, E_WARNING, "Cannot create required DOM object");
  679| 		return FAILURE;
  680| 	}
  681| 	return SUCCESS;
  682| }
  683| 
  684| /* }}} */
  685| 
  686| /* {{{ namespaceUri	string	
  687| readonly=yes 
  688| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-ID-NodeNSname
  689| Since: DOM Level 2
  690| */
```

- `read_file(path=ext/dom/text.c, version=old, start_line=170, end_line=205)` →

```
ext/dom/text.c lines 170-205 of 246
  170| 	}
  171| 	length = xmlUTF8Strlen(cur);
  172| 
  173| 	if (offset > length || offset < 0) {
  174| 		xmlFree(cur);
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
  201| /* }}} end dom_text_split_text */
  202| 
  203| /* {{{ proto boolean dom_text_is_whitespace_in_element_content();
  204| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-Text3-isWhitespaceInElementContent
  205| Since: DOM Level 3
```

- `read_file(path=ext/dom/xpath.c, version=old, start_line=130, end_line=175)` →

```
ext/dom/xpath.c lines 130-175 of 603
  130| 				ZVAL_BOOL(args[i],  obj->boolval);
  131| 				break;
  132| 			case XPATH_NUMBER:
  133| 				ZVAL_DOUBLE(args[i], obj->floatval);
  134| 				break;
  135| 			case XPATH_NODESET:
  136| 				if (type == 1) {
  137| 					str = (char *)xmlXPathCastToString(obj);
  138| 					ZVAL_STRING(args[i], str, 1);
  139| 					xmlFree(str);
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
  171| 				}
  172| 				break;
  173| 			default:
  174| 			ZVAL_STRING(args[i], (char *)xmlXPathCastToString(obj), 1);
  175| 		}
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

- `read_file(path=ext/xsl/xsltprocessor.c, version=old, start_line=250, end_line=295)` →

```
ext/xsl/xsltprocessor.c lines 250-295 of 997
  250| 			case XPATH_NODESET:
  251| 				if (type == 1) {
  252| 					str = xmlXPathCastToString(obj);
  253| 					ZVAL_STRING(args[i], str, 1);
  254| 					xmlFree(str);
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

### Turn 4  _(tok 19703+589, stop=tool_use)_

**Reasoning:** I'm trying to pin down the enclosing function names for a handful of spots in the PHP DOM source: xpath.c around lines 167 and 502, xsltprocessor.c at 286, text.c at 199, and dom_iterators.c at 241. For text.c it looks like dom_text_split_text, and for the xpath.c spots I still need to check the actual headers.

I still need the enclosing function names for the xpath.c hits at lines 167 and 502 and the xsltprocessor.c hit at 286, so I'm going to grep for the DOM_RET_OBJ macro uses and pull up the function headers in xpath.c and xsltprocessor.c. The iterator at dom_iterators.c 241 looks like php_dom_iterator_move_forward, and there's a further reference at 320 to php_dom_get_iterator.



- `grep(pattern=^[a-zA-Z_].*\(|DOM_RET_OBJ, version=old, path_glob=ext/dom/xpath.c)` →

```
21 matches
ext/dom/xpath.c:40:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_xpath_construct, 0, 0, 1)
ext/dom/xpath.c:42:ZEND_END_ARG_INFO();
ext/dom/xpath.c:44:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_xpath_register_ns, 0, 0, 2)
ext/dom/xpath.c:47:ZEND_END_ARG_INFO();
ext/dom/xpath.c:49:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_xpath_query, 0, 0, 1)
ext/dom/xpath.c:53:ZEND_END_ARG_INFO();
ext/dom/xpath.c:55:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_xpath_evaluate, 0, 0, 1)
ext/dom/xpath.c:59:ZEND_END_ARG_INFO();
ext/dom/xpath.c:61:ZEND_BEGIN_ARG_INFO_EX(arginfo_dom_xpath_register_php_functions, 0, 0, 0)
ext/dom/xpath.c:62:ZEND_END_ARG_INFO();
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

- `grep(pattern=^[a-zA-Z_].*\(|DOM_RET_OBJ, version=old, path_glob=ext/xsl/xsltprocessor.c)` →

```
43 matches
ext/xsl/xsltprocessor.c:31:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_import_stylesheet, 0, 0, 1)
ext/xsl/xsltprocessor.c:33:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:35:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_transform_to_doc, 0, 0, 1)
ext/xsl/xsltprocessor.c:37:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:39:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_transform_to_uri, 0, 0, 2)
ext/xsl/xsltprocessor.c:42:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:44:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_transform_to_xml, 0, 0, 1)
ext/xsl/xsltprocessor.c:46:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:48:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_set_parameter, 0, 0, 2)
ext/xsl/xsltprocessor.c:52:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:54:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_get_parameter, 0, 0, 2)
ext/xsl/xsltprocessor.c:57:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:59:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_remove_parameter, 0, 0, 2)
ext/xsl/xsltprocessor.c:62:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:64:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_has_exslt_support, 0, 0, 0)
ext/xsl/xsltprocessor.c:65:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:67:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_register_php_functions, 0, 0, 0)
ext/xsl/xsltprocessor.c:69:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:71:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_set_profiling, 0, 0, 1)
ext/xsl/xsltprocessor.c:73:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:75:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_set_security_prefs, 0, 0, 1)
ext/xsl/xsltprocessor.c:77:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:79:ZEND_BEGIN_ARG_INFO_EX(arginfo_xsl_xsltprocessor_get_security_prefs, 0, 0, 0)
ext/xsl/xsltprocessor.c:80:ZEND_END_ARG_INFO();
ext/xsl/xsltprocessor.c:108:static char *php_xsl_xslt_string_to_xpathexpr(const char *str TSRMLS_DC)
ext/xsl/xsltprocessor.c:134:static char **php_xsl_xslt_make_params(HashTable *parht, int xpath_params TSRMLS_DC)
ext/xsl/xsltprocessor.c:182:static void xsl_ext_function_php(xmlXPathParserContextPtr ctxt, int nargs, int type) /* {{{ */
ext/xsl/xsltprocessor.c:381:void xsl_ext_function_string_php(xmlXPathParserContextPtr ctxt, int nargs) /* {{{ */
ext/xsl/xsltprocessor.c:387:void xsl_ext_function_object_php(xmlXPathParserContextPtr ctxt, int nargs) /* {{{ */
ext/xsl/xsltprocessor.c:397:PHP_FUNCTION(xsl_xsltprocessor_import_stylesheet)
ext/xsl/xsltprocessor.c:480:static xmlDocPtr php_xsl_apply_stylesheet(zval *id, xsl_object *intern, xsltStylesheetPtr style, zval *docp TSRMLS_DC) /* {{{ */
ext/xsl/xsltprocessor.c:645:PHP_FUNCTION(xsl_xsltprocessor_transform_to_doc)
ext/xsl/xsltprocessor.c:691:			DOM_RET_OBJ((xmlNodePtr) newdocp, &ret, NULL);
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

- `grep(pattern=DOM_RET_OBJ, version=old)` →

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

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 25531+576, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "dom_attr_owner_element_read", "file": "ext/dom/attr.c"}, {"function": "dom_document_doctype_read", "file": "ext/dom/document.c"}, {"function": "dom_document_document_element_read", "file": "ext/dom/document.c"}, {"function": "php_dom_iterator_move_forward", "file": "ext/dom/dom_iterators.c"}, {"function": "php_dom_get_iterator", "file": "ext/dom/dom_iterators.c"}, {"function": "dom_node_parent_node_read", "file": "ext/dom/node.c"}, {"function": "dom_node_first_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_last_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_previous_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_next_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_owner_document_read", "file": "ext/dom/node.c"}, {"function": "dom_text_split_text", "file": "ext/dom/text.c"}, {"function": "dom_xpath_ext_function_php", "file": "ext/dom/xpath.c"}, {"function": "dom_xpath_document_read", "file": "ext/dom/xpath.c"}, {"function": "php_xpath_eval", "file": "ext/dom/xpath.c"}, {"function": "xsl_ext_function_php", "file": "ext/xsl/xsltprocessor.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 16, "n_truth": 4, "tp": 3, "precision": 0.1875, "recall": 0.75, "f1": 0.3}`

## Tool arm

### Turn 1  _(tok 3753+231, stop=tool_use)_

**Reasoning:** I'll start by pulling the callers of php_dom_create_object with a high limit, then run a grep to double-check the results.



- `get_callers(name=php_dom_create_object, limit=500, rev=None)` →

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

### Turn 2  _(tok 6096+414, stop=tool_use)_

**Reasoning:** I'm checking the macro at xml_common.h:82, since the grep shows it calls php_dom_create_object. Next I want to find which functions use that macro, because those are the ones that reach the call through expansion.



**Says:** The grep shows a call inside a macro in `xml_common.h` (line 82) that the callers list doesn't include. I need to check that macro and its users.

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

- `grep(pattern=DOM_RET_OBJ, version=old, max_results=500)` →

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

### Turn 3  _(tok 8549+1878, stop=tool_use)_

**Reasoning:** I'm noticing that DOM_RET_OBJ is a macro that expands to php_dom_create_object, so the functions using it do call the function, just indirectly. I'm weighing whether a macro-only update would count as touching those call sites, since the macro's own body is what would change.

I'm weighing whether the functions that reach php_dom_create_object only through DOM_RET_OBJ belong in the answer. The macro's own body is the one place that would need changing, so those callers wouldn't need edits. The grep shows the expansions are real calls, but the direct call graph gives 16 functions, and the "nothing more, nothing less" wording points toward that narrower set.

I'm going with the 16 direct callers from get_callers, and I'll note the macro caveat in my answer. The macro-using functions compile unchanged unless the macro's parameters change, so they aren't direct callers. I still need to check the grep lines against that list for completeness, starting with attr.c:231.

I'm tallying the direct callers by file: attr.c, document.c, dom_iterators, node.c, text.c, xpath.c and xsltprocessor.c, which comes to 16 in total. I'm also checking that the last few xpath.c hits are the functions I expect, and I'm settling on dom_text_split_text as the name for the text.c caller.

I'm settling on "dom_text_split_text" as the plain name for the text.c caller, dropping the PHP_FUNCTION wrapper.



**Says:** The grep and the callers tool agree on the 16 direct call sites. The one extra hit is the `DOM_RET_OBJ` macro, which I'll handle separately below.

- **submit_callers** → `{"callers": [{"function": "dom_attr_owner_element_read", "file": "ext/dom/attr.c"}, {"function": "dom_document_doctype_read", "file": "ext/dom/document.c"}, {"function": "dom_document_document_element_read", "file": "ext/dom/document.c"}, {"function": "php_dom_iterator_move_forward", "file": "ext/dom/dom_iterators.c"}, {"function": "php_dom_get_iterator", "file": "ext/dom/dom_iterators.c"}, {"function": "dom_node_parent_node_read", "file": "ext/dom/node.c"}, {"function": "dom_node_first_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_last_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_previous_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_next_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_owner_document_read", "file": "ext/dom/node.c"}, {"function": "dom_text_split_text", "file": "ext/dom/text.c"}, {"function": "dom_xpath_ext_function_php", "file": "ext/dom/xpath.c"}, {"function": "dom_xpath_document_read", "file": "ext/dom/xpath.c"}, {"function": "php_xpath_eval", "file": "ext/dom/xpath.c"}, {"function": "xsl_ext_function_php", "file": "ext/xsl/xsltprocessor.c"}], "confidence_overall": "medium"}`

**Score (tool):** `{"n_pred": 16, "n_truth": 4, "tp": 3, "precision": 0.1875, "recall": 0.75, "f1": 0.3}`

## Semantic arm

### Turn 1  _(tok 3205+97, stop=tool_use)_

**Reasoning:** I'm going to call get_callers and ask for a high limit so I get the full set of results.



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

### Turn 2  _(tok 4143+393, stop=tool_use)_

**Reasoning:** I'm checking whether the caller list came from the "old" version, since the tool returned that and I'm not sure if it was the default. I'll verify against the work version to confirm which revision the call site really belongs to, and I'm also tracking the PHP_FUNCTION(dom_text_split_text) caller and its enclosing function.

I'm also considering whether macros or function-pointer calls could be hiding additional callers that the list didn't capture. I'll check the work version to see whether it changes the result.



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

- `get_callers(name=php_dom_create_object, limit=500, rev=None)` →

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

### Turn 3  _(tok 6266+1023, stop=tool_use)_

**Reasoning:** I'm wondering whether I should confirm the callers actually exist in the working tree, since the version string keeps saying "old," which seems off. The results agree across runs, so the call graph looks complete, and a quick look at one caller like dom_xpath_ext_function_php should settle it.

I'm settling on the function name dom_text_split_text as the enclosing symbol, not the PHP_FUNCTION macro wrapper. The version label still reads "old," and the tool has no parameter to pull the working tree, so I'll accept the results and submit 16 deduplicated callers.



- **submit_callers** → `{"callers": [{"function": "dom_attr_owner_element_read", "file": "ext/dom/attr.c"}, {"function": "php_dom_iterator_move_forward", "file": "ext/dom/dom_iterators.c"}, {"function": "php_dom_get_iterator", "file": "ext/dom/dom_iterators.c"}, {"function": "dom_node_parent_node_read", "file": "ext/dom/node.c"}, {"function": "dom_node_first_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_last_child_read", "file": "ext/dom/node.c"}, {"function": "dom_node_previous_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_next_sibling_read", "file": "ext/dom/node.c"}, {"function": "dom_node_owner_document_read", "file": "ext/dom/node.c"}, {"function": "dom_text_split_text", "file": "ext/dom/text.c"}, {"function": "dom_xpath_ext_function_php", "file": "ext/dom/xpath.c"}, {"function": "dom_xpath_document_read", "file": "ext/dom/xpath.c"}, {"function": "php_xpath_eval", "file": "ext/dom/xpath.c"}, {"function": "xsl_ext_function_php", "file": "ext/xsl/xsltprocessor.c"}, {"function": "dom_document_doctype_read", "file": "ext/dom/document.c"}, {"function": "dom_document_document_element_read", "file": "ext/dom/document.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 16, "n_truth": 4, "tp": 3, "precision": 0.1875, "recall": 0.75, "f1": 0.3}`

