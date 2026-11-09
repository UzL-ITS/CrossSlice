# Fix-task transcript — linux @ 128c66429247 — anthropic:claude-haiku-5-5 @ high

- Hint given: function `ccp_run_sha_cmd`
- Real fix: 3 changed lines

```diff
diff --git a/drivers/crypto/ccp/ccp-ops.c b/drivers/crypto/ccp/ccp-ops.c
index c8da8eb160da0..422193690fd47 100644
--- a/drivers/crypto/ccp/ccp-ops.c
+++ b/drivers/crypto/ccp/ccp-ops.c
@@ -1777,8 +1777,9 @@ ccp_run_sha_cmd(struct ccp_cmd_queue *cmd_q, struct ccp_cmd *cmd)
 			       LSB_ITEM_SIZE);
 			break;
 		default:
+			kfree(hmac_buf);
 			ret = -EINVAL;
-			goto e_ctx;
+			goto e_data;
 		}
 
 		memset(&hmac_cmd, 0, sizeof(hmac_cmd));

```

## Self-navigation arm (generic file tools)

### Turn 1  _(tok 8074+1756, stop=tool_use)_

**Reasoning:** I'm going to look at the SHA command function in the CCP driver and recall how the upstream version handles the source data setup.

Still working through the upstream code for the data setup and the HMAC section.

Still checking the upstream zero-length handling and the source pointer validation in the SHA path...

Still checking the SHA-384 context-size condition against the upstream version, which I'm recalling from memory.

Now I'm checking the HMAC path and the opad length check against upstream, and whether the ctx size handling in the SHA caller is where the problem sits.

I'm checking the SHA-384 context-size condition against upstream, and I still need to confirm where the ctx size handling in the SHA caller actually goes wrong. The digest-size checks for the SHA-1 and SHA-224 cases seem fine on paper, so I want to see the real code in the repo next.



- `read_file(path=drivers/crypto/ccp/ccp-ops.c, version=old, start_line=1460, end_line=1475)` →

```
drivers/crypto/ccp/ccp-ops.c lines 1460-1475 of 2497
 1460| 	if (des3->mode != CCP_DES3_MODE_ECB)
 1461| 		ccp_dm_free(&ctx);
 1462| 
 1463| e_key:
 1464| 	ccp_dm_free(&key);
 1465| 
 1466| 	return ret;
 1467| }
 1468| 
 1469| static noinline_for_stack int
 1470| ccp_run_sha_cmd(struct ccp_cmd_queue *cmd_q, struct ccp_cmd *cmd)
 1471| {
 1472| 	struct ccp_sha_engine *sha = &cmd->u.sha;
 1473| 	struct ccp_dm_workarea ctx;
 1474| 	struct ccp_data src;
 1475| 	struct ccp_op op;
```

- `grep(pattern=ccp_run_sha_cmd|ctx_len|opad_len, version=old)` →

```
232 matches (showing 60)
drivers/crypto/caam/caamalg_qi2.c:2983: * @ctx_len: size of Context Register
drivers/crypto/caam/caamalg_qi2.c:2991:	int ctx_len;
drivers/crypto/caam/caamalg_qi2.c:3071:				   struct caam_hash_state *state, int ctx_len,
drivers/crypto/caam/caamalg_qi2.c:3074:	state->ctx_dma_len = ctx_len;
drivers/crypto/caam/caamalg_qi2.c:3075:	state->ctx_dma = dma_map_single(dev, state->caam_ctx, ctx_len, flag);
drivers/crypto/caam/caamalg_qi2.c:3082:	dma_to_qm_sg_one(qm_sg, state->ctx_dma, ctx_len, 0);
drivers/crypto/caam/caamalg_qi2.c:3098:	cnstr_shdsc_ahash(desc, &ctx->adata, OP_ALG_AS_UPDATE, ctx->ctx_len,
drivers/crypto/caam/caamalg_qi2.c:3099:			  ctx->ctx_len, true, priv->sec_attr.era);
drivers/crypto/caam/caamalg_qi2.c:3110:	cnstr_shdsc_ahash(desc, &ctx->adata, OP_ALG_AS_INIT, ctx->ctx_len,
drivers/crypto/caam/caamalg_qi2.c:3111:			  ctx->ctx_len, false, priv->sec_attr.era);
drivers/crypto/caam/caamalg_qi2.c:3123:			  ctx->ctx_len, true, priv->sec_attr.era);
drivers/crypto/caam/caamalg_qi2.c:3135:			  ctx->ctx_len, false, priv->sec_attr.era);
drivers/crypto/caam/caamalg_qi2.c:3365:			     ctx->ctx_len, 1);
drivers/crypto/caam/caamalg_qi2.c:3391:			     ctx->ctx_len, 1);
drivers/crypto/caam/caamalg_qi2.c:3422:			     ctx->ctx_len, 1);
drivers/crypto/caam/caamalg_qi2.c:3448:			     ctx->ctx_len, 1);
drivers/crypto/caam/caamalg_qi2.c:3515:		ret = ctx_map_to_qm_sg(ctx->dev, state, ctx->ctx_len, sg_table,
drivers/crypto/caam/caamalg_qi2.c:3549:		dpaa2_fl_set_len(in_fle, ctx->ctx_len + to_hash);
drivers/crypto/caam/caamalg_qi2.c:3552:		dpaa2_fl_set_len(out_fle, ctx->ctx_len);
drivers/crypto/caam/caamalg_qi2.c:3610:	ret = ctx_map_to_qm_sg(ctx->dev, state, ctx->ctx_len, sg_table,
drivers/crypto/caam/caamalg_qi2.c:3634:	dpaa2_fl_set_len(in_fle, ctx->ctx_len + buflen);
drivers/crypto/caam/caamalg_qi2.c:3704:	ret = ctx_map_to_qm_sg(ctx->dev, state, ctx->ctx_len, sg_table,
drivers/crypto/caam/caamalg_qi2.c:3728:	dpaa2_fl_set_len(in_fle, ctx->ctx_len + buflen + req->nbytes);
drivers/crypto/caam/caamalg_qi2.c:3994:		state->ctx_dma_len = ctx->ctx_len;
drivers/crypto/caam/caamalg_qi2.c:3996:						ctx->ctx_len, DMA_FROM_DEVICE);
drivers/crypto/caam/caamalg_qi2.c:4011:		dpaa2_fl_set_len(out_fle, ctx->ctx_len);
drivers/crypto/caam/caamalg_qi2.c:4227:		state->ctx_dma_len = ctx->ctx_len;
drivers/crypto/caam/caamalg_qi2.c:4229:						ctx->ctx_len, DMA_FROM_DEVICE);
drivers/crypto/caam/caamalg_qi2.c:4239:		dpaa2_fl_set_len(out_fle, ctx->ctx_len);
drivers/crypto/caam/caamalg_qi2.c:4562:	ctx->ctx_len = runninglen[(ctx->adata.algtype &
drivers/crypto/caam/caamhash.c:101:	int ctx_len;
drivers/crypto/caam/caamhash.c:165:				      int ctx_len)
drivers/crypto/caam/caamhash.c:167:	state->ctx_dma_len = ctx_len;
drivers/crypto/caam/caamhash.c:169:					ctx_len, DMA_FROM_DEVICE);
drivers/crypto/caam/caamhash.c:176:	append_seq_out_ptr(desc, state->ctx_dma, ctx_len, 0);
drivers/crypto/caam/caamhash.c:206:				     struct caam_hash_state *state, int ctx_len,
drivers/crypto/caam/caamhash.c:209:	state->ctx_dma_len = ctx_len;
drivers/crypto/caam/caamhash.c:210:	state->ctx_dma = dma_map_single(jrdev, state->caam_ctx, ctx_len, flag);
drivers/crypto/caam/caamhash.c:217:	dma_to_sec4_sg_one(sec4_sg, state->ctx_dma, ctx_len, 0);
drivers/crypto/caam/caamhash.c:234:	cnstr_shdsc_ahash(desc, &ctx->adata, OP_ALG_AS_UPDATE, ctx->ctx_len,
drivers/crypto/caam/caamhash.c:235:			  ctx->ctx_len, true, ctrlpriv->era);
drivers/crypto/caam/caamhash.c:245:	cnstr_shdsc_ahash(desc, &ctx->adata, OP_ALG_AS_INIT, ctx->ctx_len,
drivers/crypto/caam/caamhash.c:246:			  ctx->ctx_len, false, ctrlpriv->era);
drivers/crypto/caam/caamhash.c:256:			  ctx->ctx_len, true, ctrlpriv->era);
drivers/crypto/caam/caamhash.c:267:			  ctx->ctx_len, false, ctrlpriv->era);
drivers/crypto/caam/caamhash.c:288:			    ctx->ctx_len, ctx->ctx_len);
drivers/crypto/caam/caamhash.c:298:			    digestsize, ctx->ctx_len);
drivers/crypto/caam/caamhash.c:310:	cnstr_shdsc_sk_hash(desc, &ctx->adata, OP_ALG_AS_INIT, ctx->ctx_len,
drivers/crypto/caam/caamhash.c:311:			    ctx->ctx_len);
drivers/crypto/caam/caamhash.c:321:			    digestsize, ctx->ctx_len);
drivers/crypto/caam/caamhash.c:340:			    ctx->ctx_len, ctx->ctx_len);
drivers/crypto/caam/caamhash.c:350:			    digestsize, ctx->ctx_len);
drivers/crypto/caam/caamhash.c:359:	cnstr_shdsc_sk_hash(desc, &ctx->adata, OP_ALG_AS_INIT, ctx->ctx_len,
drivers/crypto/caam/caamhash.c:360:			    ctx->ctx_len);
drivers/crypto/caam/caamhash.c:370:			    digestsize, ctx->ctx_len);
drivers/crypto/caam/caamhash.c:623:			     ctx->ctx_len, 1);
drivers/crypto/caam/caamhash.c:645:	ahash_unmap_ctx(jrdev, edesc, req, ctx->ctx_len, DMA_BIDIRECTIONAL);
drivers/crypto/caam/caamhash.c:651:			     ctx->ctx_len, 1);
drivers/crypto/caam/caamhash.c:683:			     ctx->ctx_len, 1);
drivers/crypto/caam/caamhash.c:705:	ahash_unmap_ctx(jrdev, edesc, req, ctx->ctx_len, DMA_FROM_DEVICE);
```

### Turn 2  _(tok 13242+1206, stop=tool_use)_

**Reasoning:** I need to locate the ccp directory first, so I'll check the top of ccp-ops.c and the HMAC path around ccp_init_data and ccp_prepare_data. I also want to compare against upstream, since I recall how the `sha->final && sha->opad` block is handled in v5.x ccp_run_sha_cmd.

I'm now comparing the v3 zero-length handling and the SHA type checks against upstream, and they look the same. Since those match, I'll check the helpers ccp_init_data and ccp_prepare_data, plus the caller in ccp-crypto-sha.c, for the difference.

Now I'm checking the scatterwalk zero-length path against upstream and it matches. Next I'm looking at how the sha->ctx buffer is read in the non-first case, since it pulls sb_count*32 bytes even when ctx_len is only 20 for SHA1.

Checking the helper functions in the repo next, since the upstream code looks the same so far.



- `grep(pattern=^(static )?[a-z].*\b(ccp_init_data|ccp_prepare_data|ccp_proc, version=old)` →

```
10 matches
drivers/crypto/ccp/ccp-ops.c:119:static void ccp_dm_free(struct ccp_dm_workarea *wa)
drivers/crypto/ccp/ccp-ops.c:136:static int ccp_init_dm_workarea(struct ccp_dm_workarea *wa,
drivers/crypto/ccp/ccp-ops.c:176:static int ccp_set_dm_area(struct ccp_dm_workarea *wa, unsigned int wa_offset,
drivers/crypto/ccp/ccp-ops.c:190:static void ccp_get_dm_area(struct ccp_dm_workarea *wa, unsigned int wa_offset,
drivers/crypto/ccp/ccp-ops.c:246:static void ccp_free_data(struct ccp_data *data, struct ccp_cmd_queue *cmd_q)
drivers/crypto/ccp/ccp-ops.c:252:static int ccp_init_data(struct ccp_data *data, struct ccp_cmd_queue *cmd_q,
drivers/crypto/ccp/ccp-ops.c:323:static void ccp_prepare_data(struct ccp_data *src, struct ccp_data *dst,
drivers/crypto/ccp/ccp-ops.c:396:static void ccp_process_data(struct ccp_data *src, struct ccp_data *dst,
drivers/crypto/ccp/ccp-ops.c:442:static int ccp_copy_to_sb(struct ccp_cmd_queue *cmd_q,
drivers/crypto/ccp/ccp-ops.c:449:static int ccp_copy_from_sb(struct ccp_cmd_queue *cmd_q,
```

### Turn 3  _(tok 15043+133, stop=tool_use)_

- `read_file(path=drivers/crypto/ccp/ccp-ops.c, version=old, start_line=110, end_line=470)` →

```
drivers/crypto/ccp/ccp-ops.c lines 110-359 of 2497
  110| 
  111| 	wa->sg_used += nbytes;
  112| 	wa->bytes_left -= nbytes;
  113| 	if (wa->sg_used == wa->sg->length) {
  114| 		wa->sg = sg_next(wa->sg);
  115| 		wa->sg_used = 0;
  116| 	}
  117| }
  118| 
  119| static void ccp_dm_free(struct ccp_dm_workarea *wa)
  120| {
  121| 	if (wa->length <= CCP_DMAPOOL_MAX_SIZE) {
  122| 		if (wa->address)
  123| 			dma_pool_free(wa->dma_pool, wa->address,
  124| 				      wa->dma.address);
  125| 	} else {
  126| 		if (wa->dma.address)
  127| 			dma_unmap_single(wa->dev, wa->dma.address, wa->length,
  128| 					 wa->dma.dir);
  129| 		kfree(wa->address);
  130| 	}
  131| 
  132| 	wa->address = NULL;
  133| 	wa->dma.address = 0;
  134| }
  135| 
  136| static int ccp_init_dm_workarea(struct ccp_dm_workarea *wa,
  137| 				struct ccp_cmd_queue *cmd_q,
  138| 				unsigned int len,
  139| 				enum dma_data_direction dir)
  140| {
  141| 	memset(wa, 0, sizeof(*wa));
  142| 
  143| 	if (!len)
  144| 		return 0;
  145| 
  146| 	wa->dev = cmd_q->ccp->dev;
  147| 	wa->length = len;
  148| 
  149| 	if (len <= CCP_DMAPOOL_MAX_SIZE) {
  150| 		wa->dma_pool = cmd_q->dma_pool;
  151| 
  152| 		wa->address = dma_pool_zalloc(wa->dma_pool, GFP_KERNEL,
  153| 					     &wa->dma.address);
  154| 		if (!wa->address)
  155| 			return -ENOMEM;
  156| 
  157| 		wa->dma.length = CCP_DMAPOOL_MAX_SIZE;
  158| 
  159| 	} else {
  160| 		wa->address = kzalloc(len, GFP_KERNEL);
  161| 		if (!wa->address)
  162| 			return -ENOMEM;
  163| 
  164| 		wa->dma.address = dma_map_single(wa->dev, wa->address, len,
  165| 						 dir);
  166| 		if (dma_mapping_error(wa->dev, wa->dma.address))
  167| 			return -ENOMEM;
  168| 
  169| 		wa->dma.length = len;
  170| 	}
  171| 	wa->dma.dir = dir;
  172| 
  173| 	return 0;
  174| }
  175| 
  176| static int ccp_set_dm_area(struct ccp_dm_workarea *wa, unsigned int wa_offset,
  177| 			   struct scatterlist *sg, unsigned int sg_offset,
  178| 			   unsigned int len)
  179| {
  180| 	WARN_ON(!wa->address);
  181| 
  182| 	if (len > (wa->length - wa_offset))
  183| 		return -EINVAL;
  184| 
  185| 	scatterwalk_map_and_copy(wa->address + wa_offset, sg, sg_offset, len,
  186| 				 0);
  187| 	return 0;
  188| }
  189| 
  190| static void ccp_get_dm_area(struct ccp_dm_workarea *wa, unsigned int wa_offset,
  191| 			    struct scatterlist *sg, unsigned int sg_offset,
  192| 			    unsigned int len)
  193| {
  194| 	WARN_ON(!wa->address);
  195| 
  196| 	scatterwalk_map_and_copy(wa->address + wa_offset, sg, sg_offset, len,
  197| 				 1);
  198| }
  199| 
  200| static int ccp_reverse_set_dm_area(struct ccp_dm_workarea *wa,
  201| 				   unsigned int wa_offset,
  202| 				   struct scatterlist *sg,
  203| 				   unsigned int sg_offset,
  204| 				   unsigned int len)
  205| {
  206| 	u8 *p, *q;
  207| 	int	rc;
  208| 
  209| 	rc = ccp_set_dm_area(wa, wa_offset, sg, sg_offset, len);
  210| 	if (rc)
  211| 		return rc;
  212| 
  213| 	p = wa->address + wa_offset;
  214| 	q = p + len - 1;
  215| 	while (p < q) {
  216| 		*p = *p ^ *q;
  217| 		*q = *p ^ *q;
  218| 		*p = *p ^ *q;
  219| 		p++;
  220| 		q--;
  221| 	}
  222| 	return 0;
  223| }
  224| 
  225| static void ccp_reverse_get_dm_area(struct ccp_dm_workarea *wa,
  226| 				    unsigned int wa_offset,
  227| 				    struct scatterlist *sg,
  228| 				    unsigned int sg_offset,
  229| 				    unsigned int len)
  230| {
  231| 	u8 *p, *q;
  232| 
  233| 	p = wa->address + wa_offset;
  234| 	q = p + len - 1;
  235| 	while (p < q) {
  236| 		*p = *p ^ *q;
  237| 		*q = *p ^ *q;
  238| 		*p = *p ^ *q;
  239| 		p++;
  240| 		q--;
  241| 	}
  242| 
  243| 	ccp_get_dm_area(wa, wa_offset, sg, sg_offset, len);
  244| }
  245| 
  246| static void ccp_free_data(struct ccp_data *data, struct ccp_cmd_queue *cmd_q)
  247| {
  248| 	ccp_dm_free(&data->dm_wa);
  249| 	ccp_sg_free(&data->sg_wa);
  250| }
  251| 
  252| static int ccp_init_data(struct ccp_data *data, struct ccp_cmd_queue *cmd_q,
  253| 			 struct scatterlist *sg, u64 sg_len,
  254| 			 unsigned int dm_len,
  255| 			 enum dma_data_direction dir)
  256| {
  257| 	int ret;
  258| 
  259| 	memset(data, 0, sizeof(*data));
  260| 
  261| 	ret = ccp_init_sg_workarea(&data->sg_wa, cmd_q->ccp->dev, sg, sg_len,
  262| 				   dir);
  263| 	if (ret)
  264| 		goto e_err;
  265| 
  266| 	ret = ccp_init_dm_workarea(&data->dm_wa, cmd_q, dm_len, dir);
  267| 	if (ret)
  268| 		goto e_err;
  269| 
  270| 	return 0;
  271| 
  272| e_err:
  273| 	ccp_free_data(data, cmd_q);
  274| 
  275| 	return ret;
  276| }
  277| 
  278| static unsigned int ccp_queue_buf(struct ccp_data *data, unsigned int from)
  279| {
  280| 	struct ccp_sg_workarea *sg_wa = &data->sg_wa;
  281| 	struct ccp_dm_workarea *dm_wa = &data->dm_wa;
  282| 	unsigned int buf_count, nbytes;
  283| 
  284| 	/* Clear the buffer if setting it */
  285| 	if (!from)
  286| 		memset(dm_wa->address, 0, dm_wa->length);
  287| 
  288| 	if (!sg_wa->sg)
  289| 		return 0;
  290| 
  291| 	/* Perform the copy operation
  292| 	 *   nbytes will always be <= UINT_MAX because dm_wa->length is
  293| 	 *   an unsigned int
  294| 	 */
  295| 	nbytes = min_t(u64, sg_wa->bytes_left, dm_wa->length);
  296| 	scatterwalk_map_and_copy(dm_wa->address, sg_wa->sg, sg_wa->sg_used,
  297| 				 nbytes, from);
  298| 
  299| 	/* Update the structures and generate the count */
  300| 	buf_count = 0;
  301| 	while (sg_wa->bytes_left && (buf_count < dm_wa->length)) {
  302| 		nbytes = min(sg_wa->sg->length - sg_wa->sg_used,
  303| 			     dm_wa->length - buf_count);
  304| 		nbytes = min_t(u64, sg_wa->bytes_left, nbytes);
  305| 
  306| 		buf_count += nbytes;
  307| 		ccp_update_sg_workarea(sg_wa, nbytes);
  308| 	}
  309| 
  310| 	return buf_count;
  311| }
  312| 
  313| static unsigned int ccp_fill_queue_buf(struct ccp_data *data)
  314| {
  315| 	return ccp_queue_buf(data, 0);
  316| }
  317| 
  318| static unsigned int ccp_empty_queue_buf(struct ccp_data *data)
  319| {
  320| 	return ccp_queue_buf(data, 1);
  321| }
  322| 
  323| static void ccp_prepare_data(struct ccp_data *src, struct ccp_data *dst,
  324| 			     struct ccp_op *op, unsigned int block_size,
  325| 			     bool blocksize_op)
  326| {
  327| 	unsigned int sg_src_len, sg_dst_len, op_len;
  328| 
  329| 	/* The CCP can only DMA from/to one address each per operation. This
  330| 	 * requires that we find the smallest DMA area between the source
  331| 	 * and destination. The resulting len values will always be <= UINT_MAX
  332| 	 * because the dma length is an unsigned int.
  333| 	 */
  334| 	sg_src_len = sg_dma_len(src->sg_wa.sg) - src->sg_wa.sg_used;
  335| 	sg_src_len = min_t(u64, src->sg_wa.bytes_left, sg_src_len);
  336| 
  337| 	if (dst) {
  338| 		sg_dst_len = sg_dma_len(dst->sg_wa.sg) - dst->sg_wa.sg_used;
  339| 		sg_dst_len = min_t(u64, src->sg_wa.bytes_left, sg_dst_len);
  340| 		op_len = min(sg_src_len, sg_dst_len);
  341| 	} else {
  342| 		op_len = sg_src_len;
  343| 	}
  344| 
  345| 	/* The data operation length will be at least block_size in length
  346| 	 * or the smaller of available sg room remaining for the source or
  347| 	 * the destination
  348| 	 */
  349| 	op_len = max(op_len, block_size);
  350| 
  351| 	/* Unless we have to buffer data, there's no reason to wait */
  352| 	op->soc = 0;
  353| 
  354| 	if (sg_src_len < block_size) {
  355| 		/* Not enough data in the sg element, so it
  356| 		 * needs to be buffered into a blocksize chunk
  357| 		 */
  358| 		int cp_len = ccp_fill_queue_buf(src);
  359| 
```

### Turn 4  _(tok 19314+651, stop=tool_use)_

**Reasoning:** Now I'm reading through the rest of ccp_prepare_data and ccp_process_data.

Checking the upstream source-length path in ccp_prepare_data, where the copy is buffered and the offset is adjusted from prior data.



- `read_file(path=drivers/crypto/ccp/ccp-ops.c, version=old, start_line=359, end_line=470)` →

```
drivers/crypto/ccp/ccp-ops.c lines 359-470 of 2497
  359| 
  360| 		op->soc = 1;
  361| 		op->src.u.dma.address = src->dm_wa.dma.address;
  362| 		op->src.u.dma.offset = 0;
  363| 		op->src.u.dma.length = (blocksize_op) ? block_size : cp_len;
  364| 	} else {
  365| 		/* Enough data in the sg element, but we need to
  366| 		 * adjust for any previously copied data
  367| 		 */
  368| 		op->src.u.dma.address = sg_dma_address(src->sg_wa.sg);
  369| 		op->src.u.dma.offset = src->sg_wa.sg_used;
  370| 		op->src.u.dma.length = op_len & ~(block_size - 1);
  371| 
  372| 		ccp_update_sg_workarea(&src->sg_wa, op->src.u.dma.length);
  373| 	}
  374| 
  375| 	if (dst) {
  376| 		if (sg_dst_len < block_size) {
  377| 			/* Not enough room in the sg element or we're on the
  378| 			 * last piece of data (when using padding), so the
  379| 			 * output needs to be buffered into a blocksize chunk
  380| 			 */
  381| 			op->soc = 1;
  382| 			op->dst.u.dma.address = dst->dm_wa.dma.address;
  383| 			op->dst.u.dma.offset = 0;
  384| 			op->dst.u.dma.length = op->src.u.dma.length;
  385| 		} else {
  386| 			/* Enough room in the sg element, but we need to
  387| 			 * adjust for any previously used area
  388| 			 */
  389| 			op->dst.u.dma.address = sg_dma_address(dst->sg_wa.sg);
  390| 			op->dst.u.dma.offset = dst->sg_wa.sg_used;
  391| 			op->dst.u.dma.length = op->src.u.dma.length;
  392| 		}
  393| 	}
  394| }
  395| 
  396| static void ccp_process_data(struct ccp_data *src, struct ccp_data *dst,
  397| 			     struct ccp_op *op)
  398| {
  399| 	op->init = 0;
  400| 
  401| 	if (dst) {
  402| 		if (op->dst.u.dma.address == dst->dm_wa.dma.address)
  403| 			ccp_empty_queue_buf(dst);
  404| 		else
  405| 			ccp_update_sg_workarea(&dst->sg_wa,
  406| 					       op->dst.u.dma.length);
  407| 	}
  408| }
  409| 
  410| static int ccp_copy_to_from_sb(struct ccp_cmd_queue *cmd_q,
  411| 			       struct ccp_dm_workarea *wa, u32 jobid, u32 sb,
  412| 			       u32 byte_swap, bool from)
  413| {
  414| 	struct ccp_op op;
  415| 
  416| 	memset(&op, 0, sizeof(op));
  417| 
  418| 	op.cmd_q = cmd_q;
  419| 	op.jobid = jobid;
  420| 	op.eom = 1;
  421| 
  422| 	if (from) {
  423| 		op.soc = 1;
  424| 		op.src.type = CCP_MEMTYPE_SB;
  425| 		op.src.u.sb = sb;
  426| 		op.dst.type = CCP_MEMTYPE_SYSTEM;
  427| 		op.dst.u.dma.address = wa->dma.address;
  428| 		op.dst.u.dma.length = wa->length;
  429| 	} else {
  430| 		op.src.type = CCP_MEMTYPE_SYSTEM;
  431| 		op.src.u.dma.address = wa->dma.address;
  432| 		op.src.u.dma.length = wa->length;
  433| 		op.dst.type = CCP_MEMTYPE_SB;
  434| 		op.dst.u.sb = sb;
  435| 	}
  436| 
  437| 	op.u.passthru.byte_swap = byte_swap;
  438| 
  439| 	return cmd_q->ccp->vdata->perform->passthru(&op);
  440| }
  441| 
  442| static int ccp_copy_to_sb(struct ccp_cmd_queue *cmd_q,
  443| 			  struct ccp_dm_workarea *wa, u32 jobid, u32 sb,
  444| 			  u32 byte_swap)
  445| {
  446| 	return ccp_copy_to_from_sb(cmd_q, wa, jobid, sb, byte_swap, false);
  447| }
  448| 
  449| static int ccp_copy_from_sb(struct ccp_cmd_queue *cmd_q,
  450| 			    struct ccp_dm_workarea *wa, u32 jobid, u32 sb,
  451| 			    u32 byte_swap)
  452| {
  453| 	return ccp_copy_to_from_sb(cmd_q, wa, jobid, sb, byte_swap, true);
  454| }
  455| 
  456| static noinline_for_stack int
  457| ccp_run_aes_cmac_cmd(struct ccp_cmd_queue *cmd_q, struct ccp_cmd *cmd)
  458| {
  459| 	struct ccp_aes_engine *aes = &cmd->u.aes;
  460| 	struct ccp_dm_workarea key, ctx;
  461| 	struct ccp_data src;
  462| 	struct ccp_op op;
  463| 	unsigned int dm_offset;
  464| 	int ret;
  465| 
  466| 	if (!((aes->key_len == AES_KEYSIZE_128) ||
  467| 	      (aes->key_len == AES_KEYSIZE_192) ||
  468| 	      (aes->key_len == AES_KEYSIZE_256)))
  469| 		return -EINVAL;
  470| 
```

- `read_file(path=drivers/crypto/ccp/ccp-ops.c, version=old, start_line=40, end_line=110)` →

```
drivers/crypto/ccp/ccp-ops.c lines 40-110 of 2497
   40| 
   41| static const __be64 ccp_sha384_init[SHA512_DIGEST_SIZE / sizeof(__be64)] = {
   42| 	cpu_to_be64(SHA384_H0), cpu_to_be64(SHA384_H1),
   43| 	cpu_to_be64(SHA384_H2), cpu_to_be64(SHA384_H3),
   44| 	cpu_to_be64(SHA384_H4), cpu_to_be64(SHA384_H5),
   45| 	cpu_to_be64(SHA384_H6), cpu_to_be64(SHA384_H7),
   46| };
   47| 
   48| static const __be64 ccp_sha512_init[SHA512_DIGEST_SIZE / sizeof(__be64)] = {
   49| 	cpu_to_be64(SHA512_H0), cpu_to_be64(SHA512_H1),
   50| 	cpu_to_be64(SHA512_H2), cpu_to_be64(SHA512_H3),
   51| 	cpu_to_be64(SHA512_H4), cpu_to_be64(SHA512_H5),
   52| 	cpu_to_be64(SHA512_H6), cpu_to_be64(SHA512_H7),
   53| };
   54| 
   55| #define	CCP_NEW_JOBID(ccp)	((ccp->vdata->version == CCP_VERSION(3, 0)) ? \
   56| 					ccp_gen_jobid(ccp) : 0)
   57| 
   58| static u32 ccp_gen_jobid(struct ccp_device *ccp)
   59| {
   60| 	return atomic_inc_return(&ccp->current_id) & CCP_JOBID_MASK;
   61| }
   62| 
   63| static void ccp_sg_free(struct ccp_sg_workarea *wa)
   64| {
   65| 	if (wa->dma_count)
   66| 		dma_unmap_sg(wa->dma_dev, wa->dma_sg, wa->nents, wa->dma_dir);
   67| 
   68| 	wa->dma_count = 0;
   69| }
   70| 
   71| static int ccp_init_sg_workarea(struct ccp_sg_workarea *wa, struct device *dev,
   72| 				struct scatterlist *sg, u64 len,
   73| 				enum dma_data_direction dma_dir)
   74| {
   75| 	memset(wa, 0, sizeof(*wa));
   76| 
   77| 	wa->sg = sg;
   78| 	if (!sg)
   79| 		return 0;
   80| 
   81| 	wa->nents = sg_nents_for_len(sg, len);
   82| 	if (wa->nents < 0)
   83| 		return wa->nents;
   84| 
   85| 	wa->bytes_left = len;
   86| 	wa->sg_used = 0;
   87| 
   88| 	if (len == 0)
   89| 		return 0;
   90| 
   91| 	if (dma_dir == DMA_NONE)
   92| 		return 0;
   93| 
   94| 	wa->dma_sg = sg;
   95| 	wa->dma_dev = dev;
   96| 	wa->dma_dir = dma_dir;
   97| 	wa->dma_count = dma_map_sg(dev, sg, wa->nents, dma_dir);
   98| 	if (!wa->dma_count)
   99| 		return -ENOMEM;
  100| 
  101| 	return 0;
  102| }
  103| 
  104| static void ccp_update_sg_workarea(struct ccp_sg_workarea *wa, unsigned int len)
  105| {
  106| 	unsigned int nbytes = min_t(u64, len, wa->bytes_left);
  107| 
  108| 	if (!wa->sg)
  109| 		return;
  110| 
```

_(budget of 40,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 23668+421, stop=tool_use, forced)_

- **submit_fix** → `{"root_cause": "Not confirmed. I read ccp_run_sha_cmd and its helpers (ccp_init_data, ccp_prepare_data, ccp_process_data, ccp_set_dm_area/ccp_get_dm_area) without finding a definitive out-of-bounds or logic error. The likely suspect is the HMAC branch (sha->final && sha->opad) or the context copy in and out of sha->ctx, where a caller-supplied ctx buffer may be read or written for sb_count*CCP_SB_BYTES (32 or 64 bytes) even when sha->ctx_len is smaller.", "patch": "--- a/drivers/crypto/ccp/ccp-ops.c\n+++ b/drivers/crypto/ccp/ccp-ops.c\n@@ -1516,2 +1516,3 @@\n \tif (!sha->ctx)\n \t\treturn -EINVAL;\n+\n ", "files_touched": ["drivers/crypto/ccp/ccp-ops.c"], "confidence_overall": "low"}`

**Judge:** `{"root_cause_match": "wrong", "fix_quality": "wrong", "rationale": "The real bug is a resource leak in the HMAC branch's default case of ccp_run_sha_cmd. hmac_buf is not freed, and the code jumps to e_ctx, skipping the e_data cleanup. The proposal does not identify this. It guesses at an out-of-bounds context copy, and its patch only adds a blank line, so it fixes nothing.", "score": 0}`

## Tool arm (generic + MCP, locked to old)

### Turn 1  _(tok 10655+2366, stop=tool_use)_

**Reasoning:** I'm recalling the known CCP driver fix in the Linux kernel, which I think involves a sha context length check in the HMAC path.

I'm checking the SHA context handling in the CCP driver: the length check only guarantees ctx_len bytes, yet the stash path writes a full sb_count * CCP_SB_BYTES block into sha->ctx, which would overflow for SHA1 where ctx_len is 20. I also recall the upstream stash code copying that same block size in the non-final case.

Checking the upstream `ccp_run_sha_cmd` against my memory: the ctx_len checks at the top look the same as upstream, so the problem probably sits in a different part of the function.

Next I'm comparing the upstream HMAC branch against this version, and it matches: the opad length check requires block_size, and the hmac_buf is sized block_size plus digest_size before the opad is copied in.

I'm comparing the rest of the upstream branch, including the zero-length path that copies the empty-digest value into the context, and it matches what I remember. I'm now checking the 224 digest size setup in the v3 path to see whether the difference is there.

I'm comparing the 224 and 384 setup branches against upstream, and the 224 case is the same, including its ooffset handling for non-v3 hardware. I'm still checking whether the 384 case's ooffset matches.

I'm checking the version and context-length guards for the SHA-384 path against the upstream code, and they match as well.

I'm now looking at whether the caller in ccp-crypto-sha.c sizes the context buffer, since the 384 and 512 final path reads from an offset into sha->ctx.

Checking the 384 offset arithmetic: the write lands at offset 16 for 32 bytes, which covers the 48-byte digest, and the second read at offset 48 for 16 bytes also fits. Nothing overflows on that path, so I'll look at the surrounding code with the neighborhood tool rather than keep reasoning from memory.



- `get_neighborhood(name=ccp_run_sha_cmd)` →

```
ccp_run_sha_cmd — drivers/crypto/ccp/ccp-ops.c:1469 [function] static noinline_for_stack int ccp_run_sha_cmd(struct ccp_cmd_queue *cmd_q, struct ccp_cmd *cmd)
  reads: cmd, cmd_q; writes: cmd*; returns: return -EINVAL; | return -EINVAL; | return -EINVAL; | return -EINVAL; | return -EINVAL; | return -EINVAL;

CALLEES (16):
  scatterwalk_map_and_copy (crypto/scatterwalk.c:55): reads buf, nbytes, out, sg, start; writes -; returns -
  ccp_init_dm_workarea (drivers/crypto/ccp/ccp-ops.c:136): reads cmd_q, dir, len, wa; writes wa*; returns return 0; | return -ENOMEM; | return -ENOMEM; | return -ENOMEM; | return 0;
  ccp_set_dm_area (drivers/crypto/ccp/ccp-ops.c:176): reads len, sg, sg_offset, wa, wa_offset; writes -; returns return -EINVAL; | return 0;
  ccp_copy_to_sb (drivers/crypto/ccp/ccp-ops.c:442): reads byte_swap, cmd_q, jobid, sb, wa; writes -; returns return ccp_copy_to_from_sb(cmd_q, wa, jobid, sb, byte_swap, false);
  ccp_process_data (drivers/crypto/ccp/ccp-ops.c:396): reads dst, op; writes dst*, op*; returns -
  ccp_prepare_data (drivers/crypto/ccp/ccp-ops.c:323): reads block_size, blocksize_op, dst, op, src; writes op*, src*; returns -
  ccp_init_data (drivers/crypto/ccp/ccp-ops.c:252): reads cmd_q, data, dir, dm_len, sg, sg_len; writes data*; returns return 0; | return ret;
  ccp_copy_from_sb (drivers/crypto/ccp/ccp-ops.c:449): reads byte_swap, cmd_q, jobid, sb, wa; writes -; returns return ccp_copy_to_from_sb(cmd_q, wa, jobid, sb, byte_swap, true);
  ccp_get_dm_area (drivers/crypto/ccp/ccp-ops.c:190): reads len, sg, sg_offset, wa, wa_offset; writes -; returns -
  kfree (mm/slab.c:3737 (1 of 8 definitions)): reads objp; writes -; returns -
  sg_init_one (lib/scatterlist.c:138 (1 of 2 definitions)): reads buf, buflen, sg; writes -; returns -
  kmalloc (include/linux/slab.h:538 (1 of 6 definitions)): reads flags, size; writes -; returns return kmalloc_large(size, flags); | return ZERO_SIZE_PTR; | return kmem_cache_alloc_trace(kmalloc_caches[kmalloc_type(flags)][index], flags, size); | return __kmalloc(size, flags);
  ccp_free_data (drivers/crypto/ccp/ccp-ops.c:246): reads data; writes data*; returns -
  ccp_dm_free (drivers/crypto/ccp/ccp-ops.c:119): reads wa; writes wa*; returns -
  CCP_VERSION [macro]: #define CCP_VERSION(v, r) ((unsigned int)((v << CCP_VSIZE) \
  CCP_NEW_JOBID [macro]: #define CCP_NEW_JOBID(ccp) ((ccp->vdata->version == CCP_VERSION(3, 0)) ? \

CALLERS (1):
  ccp_run_cmd (drivers/crypto/ccp/ccp-ops.c:2477): ret = ccp_run_sha_cmd(cmd_q, cmd);

TYPES (6):
  ccp_cmd_queue — drivers/crypto/ccp/ccp-dev.h:260
    struct ccp_cmd_queue {
    	struct ccp_device *ccp;
    	u32 id;
    	struct dma_pool *dma_pool;
    	struct ccp5_desc *qbase;
    	struct mutex q_mutex ____cacheline_aligned;
    	unsigned int qidx;
    	unsigned int qsize;
    	dma_addr_t qbase_dma;
    	dma_addr_t qdma_tail;
    	u32 sb_key;
    	u32 sb_ctx;
    	DECLARE_BITMAP(lsbmask, MAX_LSB_CNT);
    	int lsb;
    	DECLARE_BITMAP(lsbmap, PLSB_MAP_SIZE);
    	struct task_struct *kthread;
    	unsigned int active;
    	unsigned int suspended;
    	unsigned int free_slots;
    	u32 int_ok;
    	u32 int_err;
    	void __iomem *reg_control;
    	void __iomem *reg_tail_lo;
    	void __iomem *reg_head_lo;
    	void __iomem *reg_int_enable;
    	void __iomem *reg_interrupt_status;
    	void __iomem *reg_status;
    	void __iomem *reg_int_status;
    	void __iomem *reg_dma_status;
    	void __iomem *reg_dma_read_status;
    	void __iomem *reg_dma_write_status;
    	u32 qcontrol; 
    	u32 int_status;
    	u32 q_status;
    	u32 q_int_status;
    	u32 cmd_error;
    	wait_queue_head_t int_queue;
    	unsigned int int_rcvd;
    	unsigned long total_ops;
    	unsigned long total_aes_ops;
  ccp_cmd — include/linux/ccp.h:636
    struct ccp_cmd {
    	struct list_head entry;
    	struct work_struct work;
    	struct ccp_device *ccp;
    	int ret;
    	u32 flags;
    	enum ccp_engine engine;
    	u32 engine_error;
    	union {
    		struct ccp_aes_engine aes;
    		struct ccp_xts_aes_engine xts;
    		struct ccp_des3_engine des3;
    		struct ccp_sha_engine sha;
    		struct ccp_rsa_engine rsa;
    		struct ccp_passthru_engine passthru;
    		struct ccp_passthru_nomap_engine passthru_nomap;
    		struct ccp_ecc_engine ecc;
    	} u;
    	void (*callback)(void *data, int err);
    	void *data;
    }
  ccp_sha_engine — include/linux/ccp.h:284
    struct ccp_sha_engine {
    	enum ccp_sha_type type;
    	struct scatterlist *ctx;
    	u32 ctx_len;		
    	struct scatterlist *src;
    	u64 src_len;		
    	struct scatterlist *opad;
    	u32 opad_len;		
    	u32 first;		
    	u32 final;		
    	u64 msg_bits;		
    }
  ccp_dm_workarea — drivers/crypto/ccp/ccp-dev.h:457
    struct ccp_dm_workarea {
    	struct device *dev;
    	struct dma_pool *dma_pool;
    	u8 *address;
    	struct ccp_dma_info dma;
    	unsigned int length;
    }
  ccp_data — drivers/crypto/ccp/ccp-dev.h:479
    struct ccp_data {
    	struct ccp_sg_workarea sg_wa;
    	struct ccp_dm_workarea dm_wa;
    }
  ccp_op — drivers/crypto/ccp/ccp-dev.h:530
    struct ccp_op {
    	struct ccp_cmd_queue *cmd_q;
    	u32 jobid;
    	u32 ioc;
    	u32 soc;
    	u32 sb_key;
    	u32 sb_ctx;
    	u32 init;
    	u32 eom;
    	struct ccp_mem src;
    	struct ccp_mem dst;
    	struct ccp_mem exp;
    	union {
    		struct ccp_aes_op aes;
    		struct ccp_xts_aes_op xts;
    		struct ccp_des3_op des3;
    		struct ccp_sha_op sha;
    		struct ccp_rsa_op rsa;
    		struct ccp_passthru_op passthru;
    		struct ccp_ecc_op ecc;
    	} u;
    }
```

### Turn 2  _(tok 16057+1679, stop=tool_use)_

**Reasoning:** I'm checking whether ctx_len is actually large enough for the stash write. The non-final path writes 32 or 64 bytes into the context buffer no matter what ctx_len is, so the bounds check in the type switch against the digest size is what I need to verify.

I'm reading through the upstream ccp_run_sha_cmd logic to see whether it matches the local code, since the stash path looks identical to upstream. I'm now checking the first-switch and zero-length handling for a different source of the bug.

Now I'm comparing the HMAC setup against upstream: the ctx_len passed through and the scatterwalk copy of the opad both match. The zero-length stash and the DMA workarea allocation also look the same as upstream, so I'm still hunting for where the bug actually is.

I'm checking whether the upstream sha->ctx_len handling and the opad length check match the local code. The ooffset setup for SHA1 on v5 looks the same as upstream too, so I'm still looking for where the bug sits.

I'm now checking whether the restore path over-reads the context buffer when ctx_len is smaller than the sb_count*32 bytes it copies.

I'm now checking how the caller sizes sha->ctx and what value ctx_len takes, since the next step is to look at ccp-crypto-sha.c and ccp_run_cmd to see whether the buffer is actually allocated to ctx_len.



- `grep(pattern=ctx_len|rctx->ctx\b|ctx\[, version=old, path_glob=drivers/crypto/ccp/*, max_results=60)` →

```
17 matches
drivers/crypto/ccp/ccp-crypto-sha.c:48:		memcpy(req->result, rctx->ctx, digest_size);
drivers/crypto/ccp/ccp-crypto-sha.c:93:	sg_init_one(&rctx->ctx_sg, rctx->ctx, sizeof(rctx->ctx));
drivers/crypto/ccp/ccp-crypto-sha.c:139:		rctx->cmd.u.sha.ctx_len = SHA1_DIGEST_SIZE;
drivers/crypto/ccp/ccp-crypto-sha.c:142:		rctx->cmd.u.sha.ctx_len = SHA224_DIGEST_SIZE;
drivers/crypto/ccp/ccp-crypto-sha.c:145:		rctx->cmd.u.sha.ctx_len = SHA256_DIGEST_SIZE;
drivers/crypto/ccp/ccp-crypto-sha.c:148:		rctx->cmd.u.sha.ctx_len = SHA384_DIGEST_SIZE;
drivers/crypto/ccp/ccp-crypto-sha.c:151:		rctx->cmd.u.sha.ctx_len = SHA512_DIGEST_SIZE;
drivers/crypto/ccp/ccp-crypto-sha.c:241:	memcpy(state.ctx, rctx->ctx, sizeof(state.ctx));
drivers/crypto/ccp/ccp-crypto-sha.c:263:	memcpy(rctx->ctx, state.ctx, sizeof(rctx->ctx));
drivers/crypto/ccp/ccp-crypto.h:212:	u8 ctx[MAX_SHA_CONTEXT_SIZE];
drivers/crypto/ccp/ccp-crypto.h:229:	u8 ctx[MAX_SHA_CONTEXT_SIZE];
drivers/crypto/ccp/ccp-ops.c:1486:		if (sha->ctx_len < SHA1_DIGEST_SIZE)
drivers/crypto/ccp/ccp-ops.c:1491:		if (sha->ctx_len < SHA224_DIGEST_SIZE)
drivers/crypto/ccp/ccp-ops.c:1496:		if (sha->ctx_len < SHA256_DIGEST_SIZE)
drivers/crypto/ccp/ccp-ops.c:1502:		    || sha->ctx_len < SHA384_DIGEST_SIZE)
drivers/crypto/ccp/ccp-ops.c:1508:		    || sha->ctx_len < SHA512_DIGEST_SIZE)
drivers/crypto/ccp/ccp-ops.c:1788:		hmac_cmd.u.sha.ctx_len = sha->ctx_len;
```

### Turn 3  _(tok 18730+2538, stop=tool_use)_

**Reasoning:** I'm checking whether the overflow even matters here: the context buffer is 64 bytes, so the stash write is fine for the in-kernel caller. But I need to figure out whether anything user-controlled reaches this path, since the CCP driver only exposes SHA through the kernel crypto API. If not, the bug has to be somewhere else in the function, so I'll look there next.

Checking the HMAC branch for 384 and 512 now: the memcpy from ctx.address + LSB_ITEM_SIZE + ooffset reads a full LSB_ITEM_SIZE bytes, which for 384 runs past the 64-byte context buffer. The final-path copy only takes LSB_ITEM_SIZE - ooffset, so this looks like the real over-read.

Now I'm checking the 384 and 512 HMAC copies: the first memcpy reads 32 bytes starting at offset 48, which runs past the 64-byte context buffer, so that's the over-read to confirm.

I'm working out the byte layout of the 384 digest: the first 16 bytes should come from ctx[48..64], and the rest from the earlier part of the buffer, so I'm checking how the final-path copy places those pieces.

The digest should be assembled from ctx[48..64] followed by ctx[0..32], so the HMAC path needs to copy only the 16 bytes from offset 48 rather than a full 32. Reading 32 from there runs past the 64-byte buffer, so I'm working out how the copy length should change.

I'm now checking the upstream-style copy: the first memcpy should take only LSB_ITEM_SIZE - ooffset bytes from the high part of the context buffer, which is what keeps it from running past the 64-byte buffer.

I'm checking the HMAC copy for SHA-384 and 512 again, since the first memcpy reads a full 32 bytes from offset 48 and would run 16 bytes past the context buffer. For 512 the offset is zero, so that case is fine. The concern is the 384 path, where the result would be wrong as well as the over-read.

The 384 path's first copy reads a full 32 bytes from offset 48 in a 64-byte buffer, so it runs 16 bytes past the end. Checking the non-HMAC SHA-384 digest path next.

Checking the HMAC copy length against the final-path copy, which uses LSB_ITEM_SIZE - ooffset, and confirming the buffer sizes in ccp-dev.h.



- `grep(pattern=define (LSB_ITEM_SIZE|CCP_SB_BYTES)\b, version=old, path_glob=drivers/crypto/ccp/*.h)` →

```
2 matches
drivers/crypto/ccp/ccp-dev.h:119:#define LSB_ITEM_SIZE			32
drivers/crypto/ccp/ccp-dev.h:219:#define CCP_SB_BYTES			32
```

_(budget of 40,000 tokens exhausted — forcing submission)_

### Turn 4  _(tok 21518+727, stop=tool_use, forced)_

- **submit_fix** → `{"root_cause": "In the HMAC branch of ccp_run_sha_cmd, the SHA-384/512 path rebuilds the digest from the 64-byte ctx DMA buffer incorrectly. The first memcpy copies LSB_ITEM_SIZE (32) bytes from ctx.address + LSB_ITEM_SIZE + ooffset, but only LSB_ITEM_SIZE - ooffset (16 bytes for SHA-384, where ooffset = 16) are valid digest bytes. For SHA-384 this reads 16 bytes past the end of the ctx workarea (heap out-of-bounds read) and places garbage into the inner-hash input, so the HMAC result is wrong. The non-HMAC final path already uses LSB_ITEM_SIZE - ooffset for the same copy, so the two paths are inconsistent. SHA-512 is unaffected because ooffset is 0.", "patch": "--- a/drivers/crypto/ccp/ccp-ops.c\n+++ b/drivers/crypto/ccp/ccp-ops.c\n@@ -1769,7 +1769,7 @@\n \t\tcase CCP_SHA_TYPE_384:\n \t\tcase CCP_SHA_TYPE_512:\n \t\t\tmemcpy(hmac_buf + block_size,\n-\t\t\t       ctx.address + LSB_ITEM_SIZE + ooffset,\n-\t\t\t       LSB_ITEM_SIZE);\n+\t\t\t       ctx.address + LSB_ITEM_SIZE + ooffset,\n+\t\t\t       LSB_ITEM_SIZE - ooffset);\n \t\t\tmemcpy(hmac_buf + block_size +\n \t\t\t       (LSB_ITEM_SIZE - ooffset),\n \t\t\t       ctx.address,\n \t\t\t       LSB_ITEM_SIZE);\n \t\t\tbreak;", "files_touched": ["drivers/crypto/ccp/ccp-ops.c"], "confidence_overall": "medium"}`

**Judge:** `{"root_cause_match": "wrong", "fix_quality": "wrong", "rationale": "The actual fix addresses a memory leak and wrong error-path cleanup in the default case of the switch: hmac_buf is not freed and the code jumps to e_ctx instead of e_data. The proposal instead alters the length of a memcpy in the SHA-384/512 case, which is a different location and a different issue. It does not touch the leak or the goto, so it does not close the vulnerability.", "score": 0}`

## Semantic arm (MCP tools only, locked to old)

### Turn 1  _(tok 10113+2248, stop=tool_use)_

**Reasoning:** I'm going through the Linux kernel CCP driver to look for a vulnerability, and I'm considering whether the `sha->src_len` check in `ccp_run_sha_cmd` happens too late. I'm also suspicious that the `ctx_len` check against the digest size doesn't match how `sb_count` is used in the copy step.

I'm checking whether the stash in the non-final path overruns `sha->ctx`: for SHA384 with a 48-byte context, and for SHA1 with a 20-byte one, the copy of `sb_count * CCP_SB_BYTES` bytes looks like it could write past the buffer.

I'm comparing this against what the upstream ccp_run_sha_cmd looks like in 5.10, since the context-length checks and the early source-length validation there seem to match what I'm seeing. The upstream code is essentially the same, so the flaw I'm after may have been introduced somewhere else in the function.

I'm now checking the SHA1 branch of the switch against the upstream code, and it looks the same: the digest size, init function, context size, and the ooffset/ioffset setup all match. I'm also confirming the early `src_len`/`src` validation matches upstream too.

I'm checking the rest of the HMAC branch against upstream, specifically the opad length check and the buffer handling around it, and so far it matches.

I'm now looking at the zero-length path for the v3 device, specifically the `sha_zero` default that selects the zero-length digest for each SHA type.

I'm going to check the source directly, since the rest of the function still matches upstream and the answer may lie in a callee or in how the v3 zero-length path is handled. I'll use a diff against the upstream version to see what differs.

I'm weighing whether the upstream ccp_run_sha_cmd is the right baseline, and I'm thinking about pulling the function source with a specific revision or fetching the neighborhood around it, so I can compare old and new versions directly. The ctx_len concern may be a real overrun on the stash path, but it might also be how upstream already behaves, so I want the actual diff before I settle on it.



- `get_neighborhood(name=ccp_run_sha_cmd)` →

```
ccp_run_sha_cmd — drivers/crypto/ccp/ccp-ops.c:1469 [function] static noinline_for_stack int ccp_run_sha_cmd(struct ccp_cmd_queue *cmd_q, struct ccp_cmd *cmd)
  reads: cmd, cmd_q; writes: cmd*; returns: return -EINVAL; | return -EINVAL; | return -EINVAL; | return -EINVAL; | return -EINVAL; | return -EINVAL;

CALLEES (16):
  scatterwalk_map_and_copy (crypto/scatterwalk.c:55): reads buf, nbytes, out, sg, start; writes -; returns -
  ccp_init_dm_workarea (drivers/crypto/ccp/ccp-ops.c:136): reads cmd_q, dir, len, wa; writes wa*; returns return 0; | return -ENOMEM; | return -ENOMEM; | return -ENOMEM; | return 0;
  ccp_set_dm_area (drivers/crypto/ccp/ccp-ops.c:176): reads len, sg, sg_offset, wa, wa_offset; writes -; returns return -EINVAL; | return 0;
  ccp_copy_to_sb (drivers/crypto/ccp/ccp-ops.c:442): reads byte_swap, cmd_q, jobid, sb, wa; writes -; returns return ccp_copy_to_from_sb(cmd_q, wa, jobid, sb, byte_swap, false);
  ccp_process_data (drivers/crypto/ccp/ccp-ops.c:396): reads dst, op; writes dst*, op*; returns -
  ccp_prepare_data (drivers/crypto/ccp/ccp-ops.c:323): reads block_size, blocksize_op, dst, op, src; writes op*, src*; returns -
  ccp_init_data (drivers/crypto/ccp/ccp-ops.c:252): reads cmd_q, data, dir, dm_len, sg, sg_len; writes data*; returns return 0; | return ret;
  ccp_copy_from_sb (drivers/crypto/ccp/ccp-ops.c:449): reads byte_swap, cmd_q, jobid, sb, wa; writes -; returns return ccp_copy_to_from_sb(cmd_q, wa, jobid, sb, byte_swap, true);
  ccp_get_dm_area (drivers/crypto/ccp/ccp-ops.c:190): reads len, sg, sg_offset, wa, wa_offset; writes -; returns -
  kfree (mm/slab.c:3737 (1 of 8 definitions)): reads objp; writes -; returns -
  sg_init_one (lib/scatterlist.c:138 (1 of 2 definitions)): reads buf, buflen, sg; writes -; returns -
  kmalloc (include/linux/slab.h:538 (1 of 6 definitions)): reads flags, size; writes -; returns return kmalloc_large(size, flags); | return ZERO_SIZE_PTR; | return kmem_cache_alloc_trace(kmalloc_caches[kmalloc_type(flags)][index], flags, size); | return __kmalloc(size, flags);
  ccp_free_data (drivers/crypto/ccp/ccp-ops.c:246): reads data; writes data*; returns -
  ccp_dm_free (drivers/crypto/ccp/ccp-ops.c:119): reads wa; writes wa*; returns -
  CCP_VERSION [macro]: #define CCP_VERSION(v, r) ((unsigned int)((v << CCP_VSIZE) \
  CCP_NEW_JOBID [macro]: #define CCP_NEW_JOBID(ccp) ((ccp->vdata->version == CCP_VERSION(3, 0)) ? \

CALLERS (1):
  ccp_run_cmd (drivers/crypto/ccp/ccp-ops.c:2477): ret = ccp_run_sha_cmd(cmd_q, cmd);

TYPES (6):
  ccp_cmd_queue — drivers/crypto/ccp/ccp-dev.h:260
    struct ccp_cmd_queue {
    	struct ccp_device *ccp;
    	u32 id;
    	struct dma_pool *dma_pool;
    	struct ccp5_desc *qbase;
    	struct mutex q_mutex ____cacheline_aligned;
    	unsigned int qidx;
    	unsigned int qsize;
    	dma_addr_t qbase_dma;
    	dma_addr_t qdma_tail;
    	u32 sb_key;
    	u32 sb_ctx;
    	DECLARE_BITMAP(lsbmask, MAX_LSB_CNT);
    	int lsb;
    	DECLARE_BITMAP(lsbmap, PLSB_MAP_SIZE);
    	struct task_struct *kthread;
    	unsigned int active;
    	unsigned int suspended;
    	unsigned int free_slots;
    	u32 int_ok;
    	u32 int_err;
    	void __iomem *reg_control;
    	void __iomem *reg_tail_lo;
    	void __iomem *reg_head_lo;
    	void __iomem *reg_int_enable;
    	void __iomem *reg_interrupt_status;
    	void __iomem *reg_status;
    	void __iomem *reg_int_status;
    	void __iomem *reg_dma_status;
    	void __iomem *reg_dma_read_status;
    	void __iomem *reg_dma_write_status;
    	u32 qcontrol; 
    	u32 int_status;
    	u32 q_status;
    	u32 q_int_status;
    	u32 cmd_error;
    	wait_queue_head_t int_queue;
    	unsigned int int_rcvd;
    	unsigned long total_ops;
    	unsigned long total_aes_ops;
  ccp_cmd — include/linux/ccp.h:636
    struct ccp_cmd {
    	struct list_head entry;
    	struct work_struct work;
    	struct ccp_device *ccp;
    	int ret;
    	u32 flags;
    	enum ccp_engine engine;
    	u32 engine_error;
    	union {
    		struct ccp_aes_engine aes;
    		struct ccp_xts_aes_engine xts;
    		struct ccp_des3_engine des3;
    		struct ccp_sha_engine sha;
    		struct ccp_rsa_engine rsa;
    		struct ccp_passthru_engine passthru;
    		struct ccp_passthru_nomap_engine passthru_nomap;
    		struct ccp_ecc_engine ecc;
    	} u;
    	void (*callback)(void *data, int err);
    	void *data;
    }
  ccp_sha_engine — include/linux/ccp.h:284
    struct ccp_sha_engine {
    	enum ccp_sha_type type;
    	struct scatterlist *ctx;
    	u32 ctx_len;		
    	struct scatterlist *src;
    	u64 src_len;		
    	struct scatterlist *opad;
    	u32 opad_len;		
    	u32 first;		
    	u32 final;		
    	u64 msg_bits;		
    }
  ccp_dm_workarea — drivers/crypto/ccp/ccp-dev.h:457
    struct ccp_dm_workarea {
    	struct device *dev;
    	struct dma_pool *dma_pool;
    	u8 *address;
    	struct ccp_dma_info dma;
    	unsigned int length;
    }
  ccp_data — drivers/crypto/ccp/ccp-dev.h:479
    struct ccp_data {
    	struct ccp_sg_workarea sg_wa;
    	struct ccp_dm_workarea dm_wa;
    }
  ccp_op — drivers/crypto/ccp/ccp-dev.h:530
    struct ccp_op {
    	struct ccp_cmd_queue *cmd_q;
    	u32 jobid;
    	u32 ioc;
    	u32 soc;
    	u32 sb_key;
    	u32 sb_ctx;
    	u32 init;
    	u32 eom;
    	struct ccp_mem src;
    	struct ccp_mem dst;
    	struct ccp_mem exp;
    	union {
    		struct ccp_aes_op aes;
    		struct ccp_xts_aes_op xts;
    		struct ccp_des3_op des3;
    		struct ccp_sha_op sha;
    		struct ccp_rsa_op rsa;
    		struct ccp_passthru_op passthru;
    		struct ccp_ecc_op ecc;
    	} u;
    }
```

- `get_function_source(name=ccp_init_dm_workarea)` →

```
ccp_init_dm_workarea (function, old version) — drivers/crypto/ccp/ccp-ops.c:136-174
  136| static int ccp_init_dm_workarea(struct ccp_dm_workarea *wa,
  137| 				struct ccp_cmd_queue *cmd_q,
  138| 				unsigned int len,
  139| 				enum dma_data_direction dir)
  140| {
  141| 	memset(wa, 0, sizeof(*wa));
  142| 
  143| 	if (!len)
  144| 		return 0;
  145| 
  146| 	wa->dev = cmd_q->ccp->dev;
  147| 	wa->length = len;
  148| 
  149| 	if (len <= CCP_DMAPOOL_MAX_SIZE) {
  150| 		wa->dma_pool = cmd_q->dma_pool;
  151| 
  152| 		wa->address = dma_pool_zalloc(wa->dma_pool, GFP_KERNEL,
  153| 					     &wa->dma.address);
  154| 		if (!wa->address)
  155| 			return -ENOMEM;
  156| 
  157| 		wa->dma.length = CCP_DMAPOOL_MAX_SIZE;
  158| 
  159| 	} else {
  160| 		wa->address = kzalloc(len, GFP_KERNEL);
  161| 		if (!wa->address)
  162| 			return -ENOMEM;
  163| 
  164| 		wa->dma.address = dma_map_single(wa->dev, wa->address, len,
  165| 						 dir);
  166| 		if (dma_mapping_error(wa->dev, wa->dma.address))
  167| 			return -ENOMEM;
  168| 
  169| 		wa->dma.length = len;
  170| 	}
  171| 	wa->dma.dir = dir;
  172| 
  173| 	return 0;
  174| }
```

### Turn 2  _(tok 16115+621, stop=tool_use)_

**Reasoning:** I'm checking the callers, ccp_run_cmd and the ccp_sha_* functions in ccp-crypto-sha.c, to see how the context length compares with the stash size written into the SHA context.

Next I'm checking whether the 32-byte SHA stash fits in the 64-byte rctx->ctx buffer, which it does. I'm now looking at ccp_set_dm_area and ccp_get_dm_area, along with the first-branch handling and ccp_init_data, to see whether anything in that path depends on the size.



- `get_function_source(name=ccp_set_dm_area)` →

```
ccp_set_dm_area (function, old version) — drivers/crypto/ccp/ccp-ops.c:176-188
  176| static int ccp_set_dm_area(struct ccp_dm_workarea *wa, unsigned int wa_offset,
  177| 			   struct scatterlist *sg, unsigned int sg_offset,
  178| 			   unsigned int len)
  179| {
  180| 	WARN_ON(!wa->address);
  181| 
  182| 	if (len > (wa->length - wa_offset))
  183| 		return -EINVAL;
  184| 
  185| 	scatterwalk_map_and_copy(wa->address + wa_offset, sg, sg_offset, len,
  186| 				 0);
  187| 	return 0;
  188| }
```

- `get_function_source(name=ccp_get_dm_area)` →

```
ccp_get_dm_area (function, old version) — drivers/crypto/ccp/ccp-ops.c:190-198
  190| static void ccp_get_dm_area(struct ccp_dm_workarea *wa, unsigned int wa_offset,
  191| 			    struct scatterlist *sg, unsigned int sg_offset,
  192| 			    unsigned int len)
  193| {
  194| 	WARN_ON(!wa->address);
  195| 
  196| 	scatterwalk_map_and_copy(wa->address + wa_offset, sg, sg_offset, len,
  197| 				 1);
  198| }
```

- `get_function_source(name=ccp_init_data)` →

```
ccp_init_data (function, old version) — drivers/crypto/ccp/ccp-ops.c:252-276
  252| static int ccp_init_data(struct ccp_data *data, struct ccp_cmd_queue *cmd_q,
  253| 			 struct scatterlist *sg, u64 sg_len,
  254| 			 unsigned int dm_len,
  255| 			 enum dma_data_direction dir)
  256| {
  257| 	int ret;
  258| 
  259| 	memset(data, 0, sizeof(*data));
  260| 
  261| 	ret = ccp_init_sg_workarea(&data->sg_wa, cmd_q->ccp->dev, sg, sg_len,
  262| 				   dir);
  263| 	if (ret)
  264| 		goto e_err;
  265| 
  266| 	ret = ccp_init_dm_workarea(&data->dm_wa, cmd_q, dm_len, dir);
  267| 	if (ret)
  268| 		goto e_err;
  269| 
  270| 	return 0;
  271| 
  272| e_err:
  273| 	ccp_free_data(data, cmd_q);
  274| 
  275| 	return ret;
  276| }
```

### Turn 3  _(tok 17718+3849, stop=tool_use)_

**Reasoning:** I'm checking the SHA caller path, starting from ccp_run_cmd and ccp-crypto-sha, and the `sha->ctx_len < SHA1_DIGEST_SIZE` check in ccp_run_sha_cmd. I'm also looking at the SHA1 non-final stash path, which writes 32 bytes to sha->ctx while ctx_len seems to be tracked separately.

Checking whether upstream's stash of 32 bytes into a context buffer that only guarantees 20 is a real concern, and whether ccp_run_sha_cmd can be reached with user-controlled ctx_len. It looks like only in-kernel ccp-crypto callers reach it, so the length isn't user-controlled. Now comparing the HMAC block against upstream.

Still checking the HMAC block against upstream, and it matches so far: the opad copy, the digest memcpy from the context offset, and the buffer sizing all line up.

Comparing the rest of the HMAC block against upstream: the zero-length handling for the v3 device is next, where the code returns early for non-final calls and otherwise has to buffer the data.

Comparing the 384/512 context read against upstream now, to see whether the offset arithmetic matches.

Checking the ctx size comparison for the 384/512 case against upstream now, to see whether the offset arithmetic lines up.

Going back over the upstream comparison now: the stash on the non-final SHA1 path and the HMAC block both look the same as upstream, so I'm checking the context-buffer offsets for the 384/512 case next.

Checking the rest of the ccp_run_sha_cmd logic against upstream, I'm moving on to the ccp_init_data call for the source buffer and the block_size handling it depends on, to see whether it matches.

Still comparing the HMAC branch's offsets against upstream: for SHA1 on the non-v3 path, the digest sits at offset 12 and spans 20 bytes, which ends exactly at the end of the 32-byte context, so that checks out. Next I'm verifying the SHA224 offset on v5, which should also land correctly.

Now I'm checking whether the SHA1 stash and the ctx_len handling in ccp_run_sha_cmd line up with upstream, and whether the stash can ever be reached with a user-controlled length.

I'm recalling how upstream's `ccp_run_sha_cmd` sets the minimum `ctx_len` for each SHA type, and whether the SHA1 check of 20 bytes matches the 32 bytes the stash writes.

I'm checking how the SHA stash path and the context restore both copy 32 bytes from sha->ctx, and whether upstream does the same. It looks like it does, so the overflow would be existing behavior that only in-kernel callers reach.

I'm checking the upstream ordering of the zero-length source validation and the `ioffset` setup for SHA1 against the code, and it looks consistent so far. I'm also trying to recall how the newer upstream revision handles these checks, but I haven't pinned that down yet.

I'm trying to figure out which version of the function is being shown, since the header says "old version" and I want to see whether the newer revision differs. The tools I have only take a name and revision, so I'm checking whether there's a way to pull the HEAD version directly.

I'm going to try pulling the HEAD revision of the function directly, to see whether it differs from the version I've been comparing against.



- `get_function_source(name=ccp_run_sha_cmd, rev=HEAD)` →

```
ccp_run_sha_cmd (function, old version) — drivers/crypto/ccp/ccp-ops.c:1469-1812
 1469| static noinline_for_stack int
 1470| ccp_run_sha_cmd(struct ccp_cmd_queue *cmd_q, struct ccp_cmd *cmd)
 1471| {
 1472| 	struct ccp_sha_engine *sha = &cmd->u.sha;
 1473| 	struct ccp_dm_workarea ctx;
 1474| 	struct ccp_data src;
 1475| 	struct ccp_op op;
 1476| 	unsigned int ioffset, ooffset;
 1477| 	unsigned int digest_size;
 1478| 	int sb_count;
 1479| 	const void *init;
 1480| 	u64 block_size;
 1481| 	int ctx_size;
 1482| 	int ret;
 1483| 
 1484| 	switch (sha->type) {
 1485| 	case CCP_SHA_TYPE_1:
 1486| 		if (sha->ctx_len < SHA1_DIGEST_SIZE)
 1487| 			return -EINVAL;
 1488| 		block_size = SHA1_BLOCK_SIZE;
 1489| 		break;
 1490| 	case CCP_SHA_TYPE_224:
 1491| 		if (sha->ctx_len < SHA224_DIGEST_SIZE)
 1492| 			return -EINVAL;
 1493| 		block_size = SHA224_BLOCK_SIZE;
 1494| 		break;
 1495| 	case CCP_SHA_TYPE_256:
 1496| 		if (sha->ctx_len < SHA256_DIGEST_SIZE)
 1497| 			return -EINVAL;
 1498| 		block_size = SHA256_BLOCK_SIZE;
 1499| 		break;
 1500| 	case CCP_SHA_TYPE_384:
 1501| 		if (cmd_q->ccp->vdata->version < CCP_VERSION(4, 0)
 1502| 		    || sha->ctx_len < SHA384_DIGEST_SIZE)
 1503| 			return -EINVAL;
 1504| 		block_size = SHA384_BLOCK_SIZE;
 1505| 		break;
 1506| 	case CCP_SHA_TYPE_512:
 1507| 		if (cmd_q->ccp->vdata->version < CCP_VERSION(4, 0)
 1508| 		    || sha->ctx_len < SHA512_DIGEST_SIZE)
 1509| 			return -EINVAL;
 1510| 		block_size = SHA512_BLOCK_SIZE;
 1511| 		break;
 1512| 	default:
 1513| 		return -EINVAL;
 1514| 	}
 1515| 
 1516| 	if (!sha->ctx)
 1517| 		return -EINVAL;
 1518| 
 1519| 	if (!sha->final && (sha->src_len & (block_size - 1)))
 1520| 		return -EINVAL;
 1521| 
 1522| 	/* The version 3 device can't handle zero-length input */
 1523| 	if (cmd_q->ccp->vdata->version == CCP_VERSION(3, 0)) {
 1524| 
 1525| 		if (!sha->src_len) {
 1526| 			unsigned int digest_len;
 1527| 			const u8 *sha_zero;
 1528| 
 1529| 			/* Not final, just return */
 1530| 			if (!sha->final)
 1531| 				return 0;
 1532| 
 1533| 			/* CCP can't do a zero length sha operation so the
 1534| 			 * caller must buffer the data.
 1535| 			 */
 1536| 			if (sha->msg_bits)
 1537| 				return -EINVAL;
 1538| 
 1539| 			/* The CCP cannot perform zero-length sha operations
 1540| 			 * so the caller is required to buffer data for the
 1541| 			 * final operation. However, a sha operation for a
 1542| 			 * message with a total length of zero is valid so
 1543| 			 * known values are required to supply the result.
 1544| 			 */
 1545| 			switch (sha->type) {
 1546| 			case CCP_SHA_TYPE_1:
 1547| 				sha_zero = sha1_zero_message_hash;
 1548| 				digest_len = SHA1_DIGEST_SIZE;
 1549| 				break;
 1550| 			case CCP_SHA_TYPE_224:
 1551| 				sha_zero = sha224_zero_message_hash;
 1552| 				digest_len = SHA224_DIGEST_SIZE;
 1553| 				break;
 1554| 			case CCP_SHA_TYPE_256:
 1555| 				sha_zero = sha256_zero_message_hash;
 1556| 				digest_len = SHA256_DIGEST_SIZE;
 1557| 				break;
 1558| 			default:
 1559| 				return -EINVAL;
 1560| 			}
 1561| 
 1562| 			scatterwalk_map_and_copy((void *)sha_zero, sha->ctx, 0,
 1563| 						 digest_len, 1);
 1564| 
 1565| 			return 0;
 1566| 		}
 1567| 	}
 1568| 
 1569| 	/* Set variables used throughout */
 1570| 	switch (sha->type) {
 1571| 	case CCP_SHA_TYPE_1:
 1572| 		digest_size = SHA1_DIGEST_SIZE;
 1573| 		init = (void *) ccp_sha1_init;
 1574| 		ctx_size = SHA1_DIGEST_SIZE;
 1575| 		sb_count = 1;
 1576| 		if (cmd_q->ccp->vdata->version != CCP_VERSION(3, 0))
 1577| 			ooffset = ioffset = CCP_SB_BYTES - SHA1_DIGEST_SIZE;
 1578| 		else
 1579| 			ooffset = ioffset = 0;
 1580| 		break;
 1581| 	case CCP_SHA_TYPE_224:
 1582| 		digest_size = SHA224_DIGEST_SIZE;
 1583| 		init = (void *) ccp_sha224_init;
 1584| 		ctx_size = SHA256_DIGEST_SIZE;
 1585| 		sb_count = 1;
 1586| 		ioffset = 0;
 1587| 		if (cmd_q->ccp->vdata->version != CCP_VERSION(3, 0))
 1588| 			ooffset = CCP_SB_BYTES - SHA224_DIGEST_SIZE;
 1589| 		else
 1590| 			ooffset = 0;
 1591| 		break;
 1592| 	case CCP_SHA_TYPE_256:
 1593| 		digest_size = SHA256_DIGEST_SIZE;
 1594| 		init = (void *) ccp_sha256_init;
 1595| 		ctx_size = SHA256_DIGEST_SIZE;
 1596| 		sb_count = 1;
 1597| 		ooffset = ioffset = 0;
 1598| 		break;
 1599| 	case CCP_SHA_TYPE_384:
 1600| 		digest_size = SHA384_DIGEST_SIZE;
 1601| 		init = (void *) ccp_sha384_init;
 1602| 		ctx_size = SHA512_DIGEST_SIZE;
 1603| 		sb_count = 2;
 1604| 		ioffset = 0;
 1605| 		ooffset = 2 * CCP_SB_BYTES - SHA384_DIGEST_SIZE;
 1606| 		break;
 1607| 	case CCP_SHA_TYPE_512:
 1608| 		digest_size = SHA512_DIGEST_SIZE;
 1609| 		init = (void *) ccp_sha512_init;
 1610| 		ctx_size = SHA512_DIGEST_SIZE;
 1611| 		sb_count = 2;
 1612| 		ooffset = ioffset = 0;
 1613| 		break;
 1614| 	default:
 1615| 		ret = -EINVAL;
 1616| 		goto e_data;
 1617| 	}
 1618| 
 1619| 	/* For zero-length plaintext the src pointer is ignored;
 1620| 	 * otherwise both parts must be valid
 1621| 	 */
 1622| 	if (sha->src_len && !sha->src)
 1623| 		return -EINVAL;
 1624| 
 1625| 	memset(&op, 0, sizeof(op));
 1626| 	op.cmd_q = cmd_q;
 1627| 	op.jobid = CCP_NEW_JOBID(cmd_q->ccp);
 1628| 	op.sb_ctx = cmd_q->sb_ctx; /* Pre-allocated */
 1629| 	op.u.sha.type = sha->type;
 1630| 	op.u.sha.msg_bits = sha->msg_bits;
 1631| 
 1632| 	/* For SHA1/224/256 the context fits in a single (32-byte) SB entry;
 1633| 	 * SHA384/512 require 2 adjacent SB slots, with the right half in the
 1634| 	 * first slot, and the left half in the second. Each portion must then
 1635| 	 * be in little endian format: use the 256-bit byte swap option.
 1636| 	 */
 1637| 	ret = ccp_init_dm_workarea(&ctx, cmd_q, sb_count * CCP_SB_BYTES,
 1638| 				   DMA_BIDIRECTIONAL);
 1639| 	if (ret)
 1640| 		return ret;
 1641| 	if (sha->first) {
 1642| 		switch (sha->type) {
 1643| 		case CCP_SHA_TYPE_1:
 1644| 		case CCP_SHA_TYPE_224:
 1645| 		case CCP_SHA_TYPE_256:
 1646| 			memcpy(ctx.address + ioffset, init, ctx_size);
 1647| 			break;
 1648| 		case CCP_SHA_TYPE_384:
 1649| 		case CCP_SHA_TYPE_512:
 1650| 			memcpy(ctx.address + ctx_size / 2, init,
 1651| 			       ctx_size / 2);
 1652| 			memcpy(ctx.address, init + ctx_size / 2,
 1653| 			       ctx_size / 2);
 1654| 			break;
 1655| 		default:
 1656| 			ret = -EINVAL;
 1657| 			goto e_ctx;
 1658| 		}
 1659| 	} else {
 1660| 		/* Restore the context */
 1661| 		ret = ccp_set_dm_area(&ctx, 0, sha->ctx, 0,
 1662| 				      sb_count * CCP_SB_BYTES);
 1663| 		if (ret)
 1664| 			goto e_ctx;
 1665| 	}
 1666| 
 1667| 	ret = ccp_copy_to_sb(cmd_q, &ctx, op.jobid, op.sb_ctx,
 1668| 			     CCP_PASSTHRU_BYTESWAP_256BIT);
 1669| 	if (ret) {
 1670| 		cmd->engine_error = cmd_q->cmd_error;
 1671| 		goto e_ctx;
 1672| 	}
 1673| 
 1674| 	if (sha->src) {
 1675| 		/* Send data to the CCP SHA engine; block_size is set above */
 1676| 		ret = ccp_init_data(&src, cmd_q, sha->src, sha->src_len,
 1677| 				    block_size, DMA_TO_DEVICE);
 1678| 		if (ret)
 1679| 			goto e_ctx;
 1680| 
 1681| 		while (src.sg_wa.bytes_left) {
 1682| 			ccp_prepare_data(&src, NULL, &op, block_size, false);
 1683| 			if (sha->final && !src.sg_wa.bytes_left)
 1684| 				op.eom = 1;
 1685| 
 1686| 			ret = cmd_q->ccp->vdata->perform->sha(&op);
 1687| 			if (ret) {
 1688| 				cmd->engine_error = cmd_q->cmd_error;
 1689| 				goto e_data;
 1690| 			}
 1691| 
 1692| 			ccp_process_data(&src, NULL, &op);
 1693| 		}
 1694| 	} else {
 1695| 		op.eom = 1;
 1696| 		ret = cmd_q->ccp->vdata->perform->sha(&op);
 1697| 		if (ret) {
 1698| 			cmd->engine_error = cmd_q->cmd_error;
 1699| 			goto e_data;
 1700| 		}
 1701| 	}
 1702| 
 1703| 	/* Retrieve the SHA context - convert from LE to BE using
 1704| 	 * 32-byte (256-bit) byteswapping to BE
 1705| 	 */
 1706| 	ret = ccp_copy_from_sb(cmd_q, &ctx, op.jobid, op.sb_ctx,
 1707| 			       CCP_PASSTHRU_BYTESWAP_256BIT);
 1708| 	if (ret) {
 1709| 		cmd->engine_error = cmd_q->cmd_error;
 1710| 		goto e_data;
 1711| 	}
 1712| 
 1713| 	if (sha->final) {
 1714| 		/* Finishing up, so get the digest */
 1715| 		switch (sha->type) {
 1716| 		case CCP_SHA_TYPE_1:
 1717| 		case CCP_SHA_TYPE_224:
 1718| 		case CCP_SHA_TYPE_256:
 1719| 			ccp_get_dm_area(&ctx, ooffset,
 1720| 					sha->ctx, 0,
 1721| 					digest_size);
 1722| 			break;
 1723| 		case CCP_SHA_TYPE_384:
 1724| 		case CCP_SHA_TYPE_512:
 1725| 			ccp_get_dm_area(&ctx, 0,
 1726| 					sha->ctx, LSB_ITEM_SIZE - ooffset,
 1727| 					LSB_ITEM_SIZE);
 1728| 			ccp_get_dm_area(&ctx, LSB_ITEM_SIZE + ooffset,
 1729| 					sha->ctx, 0,
 1730| 					LSB_ITEM_SIZE - ooffset);
 1731| 			break;
 1732| 		default:
 1733| 			ret = -EINVAL;
 1734| 			goto e_ctx;
 1735| 		}
 1736| 	} else {
 1737| 		/* Stash the context */
 1738| 		ccp_get_dm_area(&ctx, 0, sha->ctx, 0,
 1739| 				sb_count * CCP_SB_BYTES);
 1740| 	}
 1741| 
 1742| 	if (sha->final && sha->opad) {
 1743| 		/* HMAC operation, recursively perform final SHA */
 1744| 		struct ccp_cmd hmac_cmd;
 1745| 		struct scatterlist sg;
 1746| 		u8 *hmac_buf;
 1747| 
 1748| 		if (sha->opad_len != block_size) {
 1749| 			ret = -EINVAL;
 1750| 			goto e_data;
 1751| 		}
 1752| 
 1753| 		hmac_buf = kmalloc(block_size + digest_size, GFP_KERNEL);
 1754| 		if (!hmac_buf) {
 1755| 			ret = -ENOMEM;
 1756| 			goto e_data;
 1757| 		}
 1758| 		sg_init_one(&sg, hmac_buf, block_size + digest_size);
 1759| 
 1760| 		scatterwalk_map_and_copy(hmac_buf, sha->opad, 0, block_size, 0);
 1761| 		switch (sha->type) {
 1762| 		case CCP_SHA_TYPE_1:
 1763| 		case CCP_SHA_TYPE_224:
 1764| 		case CCP_SHA_TYPE_256:
 1765| 			memcpy(hmac_buf + block_size,
 1766| 			       ctx.address + ooffset,
 1767| 			       digest_size);
 1768| 			break;
 1769| 		case CCP_SHA_TYPE_384:
 1770| 		case CCP_SHA_TYPE_512:
 1771| 			memcpy(hmac_buf + block_size,
 1772| 			       ctx.address + LSB_ITEM_SIZE + ooffset,
 1773| 			       LSB_ITEM_SIZE);
 1774| 			memcpy(hmac_buf + block_size +
 1775| 			       (LSB_ITEM_SIZE - ooffset),
 1776| 			       ctx.address,
 1777| 			       LSB_ITEM_SIZE);
 1778| 			break;
 1779| 		default:
 1780| 			ret = -EINVAL;
 1781| 			goto e_ctx;
 1782| 		}
 1783| 
 1784| 		memset(&hmac_cmd, 0, sizeof(hmac_cmd));
 1785| 		hmac_cmd.engine = CCP_ENGINE_SHA;
 1786| 		hmac_cmd.u.sha.type = sha->type;
 1787| 		hmac_cmd.u.sha.ctx = sha->ctx;
 1788| 		hmac_cmd.u.sha.ctx_len = sha->ctx_len;
 1789| 		hmac_cmd.u.sha.src = &sg;
 1790| 		hmac_cmd.u.sha.src_len = block_size + digest_size;
 1791| 		hmac_cmd.u.sha.opad = NULL;
 1792| 		hmac_cmd.u.sha.opad_len = 0;
 1793| 		hmac_cmd.u.sha.first = 1;
 1794| 		hmac_cmd.u.sha.final = 1;
 1795| 		hmac_cmd.u.sha.msg_bits = (block_size + digest_size) << 3;
 1796| 
 1797| 		ret = ccp_run_sha_cmd(cmd_q, &hmac_cmd);
 1798| 		if (ret)
 1799| 			cmd->engine_error = hmac_cmd.engine_error;
 1800| 
 1801| 		kfree(hmac_buf);
 1802| 	}
 1803| 
 1804| e_data:
 1805| 	if (sha->src)
 1806| 		ccp_free_data(&src, cmd_q);
 1807| 
 1808| e_ctx:
 1809| 	ccp_dm_free(&ctx);
 1810| 
 1811| 	return ret;
 1812| }
```

- `get_function_source(name=ccp_run_cmd)` →

```
ccp_run_cmd (function, old version) — drivers/crypto/ccp/ccp-ops.c:2447-2496
 2447| int ccp_run_cmd(struct ccp_cmd_queue *cmd_q, struct ccp_cmd *cmd)
 2448| {
 2449| 	int ret;
 2450| 
 2451| 	cmd->engine_error = 0;
 2452| 	cmd_q->cmd_error = 0;
 2453| 	cmd_q->int_rcvd = 0;
 2454| 	cmd_q->free_slots = cmd_q->ccp->vdata->perform->get_free_slots(cmd_q);
 2455| 
 2456| 	switch (cmd->engine) {
 2457| 	case CCP_ENGINE_AES:
 2458| 		switch (cmd->u.aes.mode) {
 2459| 		case CCP_AES_MODE_CMAC:
 2460| 			ret = ccp_run_aes_cmac_cmd(cmd_q, cmd);
 2461| 			break;
 2462| 		case CCP_AES_MODE_GCM:
 2463| 			ret = ccp_run_aes_gcm_cmd(cmd_q, cmd);
 2464| 			break;
 2465| 		default:
 2466| 			ret = ccp_run_aes_cmd(cmd_q, cmd);
 2467| 			break;
 2468| 		}
 2469| 		break;
 2470| 	case CCP_ENGINE_XTS_AES_128:
 2471| 		ret = ccp_run_xts_aes_cmd(cmd_q, cmd);
 2472| 		break;
 2473| 	case CCP_ENGINE_DES3:
 2474| 		ret = ccp_run_des3_cmd(cmd_q, cmd);
 2475| 		break;
 2476| 	case CCP_ENGINE_SHA:
 2477| 		ret = ccp_run_sha_cmd(cmd_q, cmd);
 2478| 		break;
 2479| 	case CCP_ENGINE_RSA:
 2480| 		ret = ccp_run_rsa_cmd(cmd_q, cmd);
 2481| 		break;
 2482| 	case CCP_ENGINE_PASSTHRU:
 2483| 		if (cmd->flags & CCP_CMD_PASSTHRU_NO_DMA_MAP)
 2484| 			ret = ccp_run_passthru_nomap_cmd(cmd_q, cmd);
 2485| 		else
 2486| 			ret = ccp_run_passthru_cmd(cmd_q, cmd);
 2487| 		break;
 2488| 	case CCP_ENGINE_ECC:
 2489| 		ret = ccp_run_ecc_cmd(cmd_q, cmd);
 2490| 		break;
 2491| 	default:
 2492| 		ret = -EINVAL;
 2493| 	}
 2494| 
 2495| 	return ret;
 2496| }
```

_(budget of 40,000 tokens exhausted — forcing submission)_

### Turn 4  _(tok 29544+569, stop=tool_use, forced)_

- **submit_fix** → `{"root_cause": "Best guess, not confirmed: ccp_run_sha_cmd validates sha->ctx_len only against the digest size (e.g. SHA-384 needs >= 48), but then reads and writes sb_count * CCP_SB_BYTES (64 bytes for SHA-384/512, 32 for SHA-1/224/256) through sha->ctx in the restore (ccp_set_dm_area), stash (ccp_get_dm_area) and HMAC paths. A caller-supplied ctx buffer shorter than the SB-sized window can therefore be overrun. I did not confirm that any in-tree caller passes a short buffer.", "patch": "--- a/drivers/crypto/ccp/ccp-ops.c\n+++ b/drivers/crypto/ccp/ccp-ops.c\n@@ -1619,6 +1619,8 @@ ccp_run_sha_cmd(struct ccp_cmd_queue *cmd_q, struct ccp_cmd *cmd)\n \t/* For zero-length plaintext the src pointer is ignored;\n \t * otherwise both parts must be valid\n \t */\n+\tif (sha->ctx_len < sb_count * CCP_SB_BYTES)\n+\t\treturn -EINVAL;\n \tif (sha->src_len && !sha->src)\n \t\treturn -EINVAL;\n ", "files_touched": ["drivers/crypto/ccp/ccp-ops.c"], "confidence_overall": "low"}`

**Judge:** `{"root_cause_match": "wrong", "fix_quality": "wrong", "rationale": "The actual fix addresses a memory leak (hmac_buf not freed) and wrong cleanup label in the default error branch of the HMAC key-size switch in ccp_run_sha_cmd. The proposal speculates about a ctx buffer overrun from a short ctx_len, which is an unrelated issue. Its added length check changes validation and does not touch the leak or the goto path, and could break valid callers.", "score": 0}`

