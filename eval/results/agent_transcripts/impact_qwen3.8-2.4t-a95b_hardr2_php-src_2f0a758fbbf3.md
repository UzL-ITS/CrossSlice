# Impact-analysis transcript — php-src @ 2f0a758fbbf3 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `php_dom_create_object` (ext/dom/php_dom.c), arity 4->3
- truth: [['ext/dom/attr.c', 'dom_attr_owner_element_read'], ['ext/dom/document.c', 'dom_document_doctype_read'], ['ext/dom/document.c', 'dom_document_document_element_read'], ['ext/dom/dom_iterators.c', 'php_dom_get_iterator'], ['ext/dom/dom_iterators.c', 'php_dom_iterator_move_forward'], ['ext/dom/node.c', 'dom_node_first_child_read'], ['ext/dom/node.c', 'dom_node_last_child_read'], ['ext/dom/node.c', 'dom_node_next_sibling_read'], ['ext/dom/node.c', 'dom_node_owner_document_read'], ['ext/dom/node.c', 'dom_node_parent_node_read'], ['ext/dom/node.c', 'dom_node_previous_sibling_read'], ['ext/dom/text.c', 'PHP_FUNCTION(dom_text_split_text)'], ['ext/dom/xpath.c', 'dom_xpath_document_read'], ['ext/dom/xpath.c', 'dom_xpath_ext_function_php'], ['ext/dom/xpath.c', 'php_xpath_eval'], ['ext/xsl/xsltprocessor.c', 'xsl_ext_function_php']]

## Self-navigation arm

### Turn 1  _(tok 904+69, stop=tool_use)_

**Reasoning:** Let's search for php_dom_create_object within the repository.


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

### Turn 2  _(tok 1700+161, stop=tool_use)_

**Reasoning:** I need to find the function enclosing each call site. Let me try reading the surrounding area for each location.

- `read_file(path=ext/dom/attr.c, start_line=200, end_line=240, version=old)` →

```
ext/dom/attr.c lines 200-240 of 290
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
```

- `read_file(path=ext/dom/document.c, start_line=235, end_line=320, version=old)` →

```
ext/dom/document.c lines 235-320 of 2446
  235| };
  236| /* }}} */
  237| 
  238| /* {{{ docType	DOMDocumentType	
  239| readonly=yes 
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

### Turn 3  _(tok 3657+485, stop=tool_use)_

**Reasoning:** Wait, document.c only shows 2 matches, but there might be more (only lines 264 and 314). But grep found matches in document.c at lines 264 and 314 — both have been handled. However, there might be other calls in document.c that I missed? Grep found a total of 20 matches, and the list seems complete.

Also, I need to check whether grep missed any lines — max_results is 200, and 20 matches were found, so it's fine.

Next, let me check the other files: dom_iterators.c lines 241, 320; node.c lines 432, 501, 538, 572, 605, 677; text.c line 199; xpath.c lines 167, 335, 502; xsltprocessor.c line 286; xml_common.h line 82 (a macro — need to check which macro it is, and also whether that macro is used somewhere. The question is asking for callers of php_dom_create_object. If a macro wraps it, then users of that macro are indirectly calling it. Hmm. "List all functions that call php_dom_create_object — enclosing function names and their files." The macro at xml_common.h:82 — let me look at it. It's probably PHP_DOM_GET_RETVAL or something similar. Should functions using that macro be counted? It's ambiguous. The task probably wants direct callers. But for thoroughness, let me investigate the macro.


- `read_file(end_line=100, path=ext/dom/xml_common.h, start_line=50, version=old)` →

```
ext/dom/xml_common.h lines 50-100 of 107
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
```

- `read_file(end_line=330, path=ext/dom/dom_iterators.c, start_line=210, version=old)` →

```
ext/dom/dom_iterators.c lines 210-330 of 339
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
```

### Turn 4  _(tok 6982+110, stop=tool_use)_

**Reasoning:** Line 241: which function is it? I need to check above line 210 to find the function definition. Probably php_dom_iterator_move_forward. Let me check.

- `read_file(end_line=210, path=ext/dom/dom_iterators.c, start_line=170, version=old)` →

```
ext/dom/dom_iterators.c lines 170-210 of 339
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

### Turn 5  _(tok 7815+135, stop=tool_use)_

**Reasoning:** dom_iterators.c: php_dom_iterator_move_forward (line 241) and php_dom_get_iterator (line 320).

Next, node.c lines 432, 501, 538, 572, 605, 677.

- `read_file(end_line=690, path=ext/dom/node.c, start_line=400, version=old)` →

```
ext/dom/node.c lines 400-649 of 1991
  400| 	}
  401| 
  402| 	return SUCCESS;
  403| }
  404| 
  405| /* }}} */
  406| 
  407| /* {{{ parentNode	DomNode	
  408| readonly=yes 
  409| URL: http://www.w3.org/TR/2003/WD-DOM-Level-3-Core-20030226/DOM3-Core.html#core-ID-1060184317
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
```

_(budget of 20,000 tokens exhausted — forcing submission)_

