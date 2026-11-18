# Impact-analysis transcript — php-src @ 2f0a758fbbf3 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `php_dom_create_object` (ext/dom/php_dom.c), arity 4->3
- truth: [['ext/dom/attr.c', 'dom_attr_owner_element_read'], ['ext/dom/document.c', 'dom_document_doctype_read'], ['ext/dom/document.c', 'dom_document_document_element_read'], ['ext/dom/dom_iterators.c', 'php_dom_get_iterator'], ['ext/dom/dom_iterators.c', 'php_dom_iterator_move_forward'], ['ext/dom/node.c', 'dom_node_first_child_read'], ['ext/dom/node.c', 'dom_node_last_child_read'], ['ext/dom/node.c', 'dom_node_next_sibling_read'], ['ext/dom/node.c', 'dom_node_owner_document_read'], ['ext/dom/node.c', 'dom_node_parent_node_read'], ['ext/dom/node.c', 'dom_node_previous_sibling_read'], ['ext/dom/text.c', 'PHP_FUNCTION(dom_text_split_text)'], ['ext/dom/xpath.c', 'dom_xpath_document_read'], ['ext/dom/xpath.c', 'dom_xpath_ext_function_php'], ['ext/dom/xpath.c', 'php_xpath_eval'], ['ext/xsl/xsltprocessor.c', 'xsl_ext_function_php']]

## Self-navigation arm

### Turn 1  _(tok 904+71, stop=tool_use)_

**Reasoning:** I'll search for calls to php_dom_create_object within the repository.


- `grep(pattern=php_dom_create_object, version=old, max_results=200)` →

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

### Turn 2  _(tok 1702+561, stop=tool_use)_

**Reasoning:** Let me look into the context around each call site and identify the enclosing function name. Also, let me verify that there are no other matches (grep returned 20 matches. It says "up to max_results matches", and since I set it to 200, it's possible that 20 matches is the complete set, but let me double-check). In fact, grep returned exactly 20 results. Let me verify whether there are more than 20. I'll search again, or search in a different way to check.

Let me look at each file to identify the enclosing function:

1. ext/dom/attr.c:231
2. ext/dom/document.c:264, 314
3. ext/dom/dom_iterators.c:241, 320
4. ext/dom/node.c:432, 501, 538, 572, 605, 677
5. ext/dom/text.c:199
6. ext/dom/xml_common.h:82 — this is a macro (PHP_DOM_GET_ASSOCIATED...?). I need to identify the name of the macro, then find the functions that use that macro. Hmm, the task says "enumerate all functions in this repository that call php_dom_create_object." Macros also count as call sites, but since the question asks for the enclosing function name and its file, I need to find the functions that use the macro. Wait — but the macro itself is where the call is written. Let me read the macro definition to see which macro it is.
7. ext/dom/xpath.c:167, 335, 502
8. ext/xsl/xsltprocessor.c:286

Let me read the context for each.

**Says:** I have 20 matches. Now I need the enclosing function for each call site. Let me examine each file's context, and also check the macro in `xml_common.h`.



- `read_file(path=ext/dom/xml_common.h, start_line=50, end_line=110, version=old)` →

```
ext/dom/xml_common.h lines 50-107 of 107
   50| #	define PHPAPI __attribute__ ((visibility("default")))
   51| #endif /* PHP_WIN32 */
   52| 
   53| #define PHP_DOM_EXPORT PHPAPI
   54| 
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
  101|  * tab-width: 4
  102|  * c-basic-offset: 4
  103|  * End:
  104|  * vim600: noet sw=4 ts=4 fdm=marker
  105|  * vim<600: noet sw=4 ts=4
  106|  */
  107| 
```

- `read_file(path=ext/dom/attr.c, start_line=200, end_line=245, version=old)` →

```
ext/dom/attr.c lines 200-245 of 290
  200| 
  201| 	return SUCCESS;
  202| }
  203| 
  204| /* }}} */
  205| 
  206| /* {{{ ownerElement	DOMElement	
  207| readonly=yes 
  208| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#Attr-ownerElement
  209| Since: DOM Level 2
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
  236| 
  237| }
  238| 
  239| /* }}} */
  240| 
  241| /* {{{ schemaTypeInfo	DOMTypeInfo	
  242| readonly=yes 
  243| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#Attr-schemaTypeInfo
  244| Since: DOM Level 3
  245| */
```

### Turn 3  _(tok 3883+106, stop=tool_use)_

**Reasoning:** attr.c:231 -> `dom_attr_owner_element_read` in ext/dom/attr.c.

Next, document.c:264 and 314.

- `read_file(path=ext/dom/document.c, start_line=240, end_line=330, version=old)` →

```
ext/dom/document.c lines 240-330 of 2446
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
  321| /* }}} */
  322| 
  323| /* {{{ encoding	string
  324| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-Document3-encoding
  325| Since: DOM Level 3
  326| */
  327| int dom_document_encoding_read(dom_object *obj, zval **retval TSRMLS_DC)
  328| {
  329| 	xmlDoc *docp;
  330| 	char *encoding;
```

### Turn 4  _(tok 5331+118, stop=tool_use)_

**Reasoning:** document.c:264 -> `dom_document_doctype_read`
document.c:314 -> `dom_document_document_element_read`

Next, dom_iterators.c:241, 320.

- `read_file(path=ext/dom/dom_iterators.c, start_line=210, end_line=340, version=old)` →

```
ext/dom/dom_iterators.c lines 210-339 of 339
  210| 			} else {
  211| 				curnode = (xmlNodePtr)((php_libxml_node_ptr *)intern->ptr)->node;
  212| 				if (objmap->nodetype == XML_ATTRIBUTE_NODE || 
  213| 					objmap->nodetype == XML_ELEMENT_NODE) {
  214| 					curnode = curnode->next;
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
  326| }
  327| /* }}} */
  328| 
  329| #endif
  330| 
  331| /*
  332|  * Local variables:
  333|  * tab-width: 4
  334|  * c-basic-offset: 4
  335|  * End:
  336|  * vim600: noet sw=4 ts=4 fdm=marker
  337|  * vim<600: noet sw=4 ts=4
  338|  */
  339| 
```

### Turn 5  _(tok 7551+119, stop=tool_use)_

**Reasoning:** dom_iterators.c:320 -> `php_dom_get_iterator`.
dom_iterators.c:241 -> need to find the function that contains it. Let's go back and check before line 210.

- `read_file(path=ext/dom/dom_iterators.c, start_line=140, end_line=210, version=old)` →

```
ext/dom/dom_iterators.c lines 140-210 of 339
  140| {
  141| 
  142| 	php_dom_iterator *iterator = (php_dom_iterator *)iter;
  143| 
  144| 	if (iterator->curobj) {
  145| 		return SUCCESS;
  146| 	} else {
  147| 		return FAILURE;
  148| 	}
  149| }
  150| /* }}} */
  151| 
  152| static void php_dom_iterator_current_data(zend_object_iterator *iter, zval ***data TSRMLS_DC) /* {{{ */
  153| {
  154| 	php_dom_iterator *iterator = (php_dom_iterator *)iter;
  155| 
  156| 	*data = &iterator->curobj;
  157| }
  158| /* }}} */
  159| 
  160| static void php_dom_iterator_current_key(zend_object_iterator *iter, zval *key TSRMLS_DC) /* {{{ */
  161| {
  162| 	php_dom_iterator *iterator = (php_dom_iterator *)iter;
  163| 	zval *object = (zval *)iterator->intern.data;
  164| 
  165| 	if (instanceof_function(Z_OBJCE_P(object), dom_nodelist_class_entry TSRMLS_CC)) {
  166| 		ZVAL_LONG(key, iter->index);
  167| 	} else {
  168| 		dom_object *intern = (dom_object *)zend_object_store_get_object(iterator->curobj TSRMLS_CC);
  169| 
  170| 		if (intern != NULL && intern->ptr != NULL) {
  171| 			xmlNodePtr curnode = (xmlNodePtr)((php_libxml_node_ptr *)intern->ptr)->node;
  172| 			ZVAL_STRINGL(key, (char *) curnode->name, xmlStrlen(curnode->name), 1);
  173| 		} else {
  174| 			ZVAL_NULL(key);
  175| 		}
  176| 	}
  177| }
  178| /* }}} */
  179| 
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
```

_(budget of 20,000 tokens exhausted — forcing submission)_

