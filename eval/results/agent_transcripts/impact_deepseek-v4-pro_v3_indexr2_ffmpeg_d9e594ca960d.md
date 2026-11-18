# Impact-analysis transcript — ffmpeg @ d9e594ca960d — openrouter:deepseek/deepseek-v4-pro

- target: `ff_sws_graph_add_pass` (libswscale/graph.c), arity 8->9
- truth: [['libswscale/graph.c', 'adapt_colors'], ['libswscale/graph.c', 'init_legacy_subpass'], ['libswscale/graph.c', 'init_passes'], ['libswscale/graph.c', 'pass_append'], ['libswscale/ops_dispatch.c', 'compile']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1029+79, stop=tool_use)_

**Reasoning:** Let me find all callers of `ff_sws_graph_add_pass`. I'll start by searching for references to this function.

- `find_references(name=ff_sws_graph_add_pass)` →

```
6 references
ff_sws_graph_add_pass  160 libswscale/graph.c     SwsPass *new = ff_sws_graph_add_pass(graph, fmt, w, h, *pass, align, priv, run);
ff_sws_graph_add_pass  418 libswscale/graph.c     pass = ff_sws_graph_add_pass(graph, sws->dst_format, dst_w, dst_h, input, align, sws,
ff_sws_graph_add_pass  710 libswscale/graph.c     pass = ff_sws_graph_add_pass(graph, fmt_out, src.width, src.height,
ff_sws_graph_add_pass  751 libswscale/graph.c         pass = ff_sws_graph_add_pass(graph, dst.format, dst.width, dst.height,
ff_sws_graph_add_pass  159 libswscale/graph.h SwsPass *ff_sws_graph_add_pass(SwsGraph *graph, enum AVPixelFormat fmt,
ff_sws_graph_add_pass  349 libswscale/ops_dispatch.c     pass = ff_sws_graph_add_pass(graph, dst->format, dst->width, dst->height,
```

### Turn 2  _(tok 1366+543, stop=tool_use)_

**Reasoning:** Let me analyze the results:

1. `libswscale/graph.c:160` - This is a call within the function itself (or within another function in graph.c). Let me check what function this is in.
2. `libswscale/graph.c:418` - Another call in graph.c
3. `libswscale/graph.c:710` - Another call in graph.c
4. `libswscale/graph.c:751` - Another call in graph.c
5. `libswscale/graph.h:159` - This is the prototype/declaration, not a call
6. `libswscale/ops_dispatch.c:349` - This is a call in ops_dispatch.c

So I need to determine which functions in graph.c contain the calls at lines 160, 418, 710, and 751. Let me read those sections.

- `read_file(path=libswscale/graph.c, version=old, start_line=140, end_line=175)` →

```
libswscale/graph.c lines 140-175 of 925
  140|     /* Align output buffer to include extra slice padding */
  141|     pass->output->width  = pass->width;
  142|     pass->output->height = pass->slice_h * pass->num_slices;
  143| 
  144|     ret = av_dynarray_add_nofree(&graph->passes, &graph->num_passes, pass);
  145|     if (ret < 0)
  146|         goto fail;
  147| 
  148|     return pass;
  149| 
  150| fail:
  151|     av_refstruct_unref(&pass->output);
  152|     av_free(pass);
  153|     return NULL;
  154| }
  155| 
  156| /* Wrapper around ff_sws_graph_add_pass() that chains a pass "in-place" */
  157| static int pass_append(SwsGraph *graph, enum AVPixelFormat fmt, int w, int h,
  158|                        SwsPass **pass, int align, void *priv, sws_filter_run_t run)
  159| {
  160|     SwsPass *new = ff_sws_graph_add_pass(graph, fmt, w, h, *pass, align, priv, run);
  161|     if (!new)
  162|         return AVERROR(ENOMEM);
  163|     *pass = new;
  164|     return 0;
  165| }
  166| 
  167| static void frame_shift(const SwsFrame *f, const int y, uint8_t *data[4])
  168| {
  169|     for (int i = 0; i < 4; i++) {
  170|         if (f->data[i])
  171|             data[i] = f->data[i] + (y >> ff_fmt_vshift(f->format, i)) * f->linesize[i];
  172|         else
  173|             data[i] = NULL;
  174|     }
  175| }
```

- `read_file(path=libswscale/graph.c, version=old, start_line=400, end_line=435)` →

```
libswscale/graph.c lines 400-435 of 925
  400|         align = 0; /* disable slice threading */
  401| 
  402|     if (c->src0Alpha && !c->dst0Alpha && isALPHA(sws->dst_format)) {
  403|         ret = pass_append(graph, AV_PIX_FMT_RGBA, src_w, src_h, &input, 1, c, run_rgb0);
  404|         if (ret < 0) {
  405|             sws_free_context(&sws);
  406|             return ret;
  407|         }
  408|     }
  409| 
  410|     if (c->srcXYZ && !(c->dstXYZ && unscaled)) {
  411|         ret = pass_append(graph, AV_PIX_FMT_RGB48, src_w, src_h, &input, 1, c, run_xyz2rgb);
  412|         if (ret < 0) {
  413|             sws_free_context(&sws);
  414|             return ret;
  415|         }
  416|     }
  417| 
  418|     pass = ff_sws_graph_add_pass(graph, sws->dst_format, dst_w, dst_h, input, align, sws,
  419|                                  c->convert_unscaled ? run_legacy_unscaled : run_legacy_swscale);
  420|     if (!pass) {
  421|         sws_free_context(&sws);
  422|         return AVERROR(ENOMEM);
  423|     }
  424|     pass->setup = setup_legacy_swscale;
  425|     pass->free = free_legacy_swscale;
  426| 
  427|     /**
  428|      * For slice threading, we need to create sub contexts, similar to how
  429|      * swscale normally handles it internally. The most important difference
  430|      * is that we handle cascaded contexts before threaded contexts; whereas
  431|      * context_init_threaded() does it the other way around.
  432|      */
  433| 
  434|     if (pass->num_slices > 1) {
  435|         c->slice_ctx = av_calloc(pass->num_slices, sizeof(*c->slice_ctx));
```

- `read_file(path=libswscale/graph.c, version=old, start_line=690, end_line=760)` →

```
libswscale/graph.c lines 690-760 of 925
  690|     lut = ff_sws_lut3d_alloc();
  691|     if (!lut)
  692|         return AVERROR(ENOMEM);
  693| 
  694|     fmt_in  = ff_sws_lut3d_pick_pixfmt(src, 0);
  695|     fmt_out = ff_sws_lut3d_pick_pixfmt(dst, 1);
  696|     if (fmt_in != src.format) {
  697|         SwsFormat tmp = src;
  698|         tmp.format = fmt_in;
  699|         ret = add_convert_pass(graph, &src, &tmp, input, &input);
  700|         if (ret < 0)
  701|             return ret;
  702|     }
  703| 
  704|     ret = ff_sws_lut3d_generate(lut, fmt_in, fmt_out, &map);
  705|     if (ret < 0) {
  706|         ff_sws_lut3d_free(&lut);
  707|         return ret;
  708|     }
  709| 
  710|     pass = ff_sws_graph_add_pass(graph, fmt_out, src.width, src.height,
  711|                                  input, 1, lut, run_lut3d);
  712|     if (!pass) {
  713|         ff_sws_lut3d_free(&lut);
  714|         return AVERROR(ENOMEM);
  715|     }
  716|     pass->setup = setup_lut3d;
  717|     pass->free = free_lut3d;
  718| 
  719|     *output = pass;
  720|     return 0;
  721| }
  722| 
  723| /***************************************
  724|  * Main filter graph construction code *
  725|  ***************************************/
  726| 
  727| static int init_passes(SwsGraph *graph)
  728| {
  729|     SwsFormat src = graph->src;
  730|     SwsFormat dst = graph->dst;
  731|     SwsPass *pass = NULL; /* read from main input image */
  732|     int ret;
  733| 
  734|     ret = adapt_colors(graph, src, dst, pass, &pass);
  735|     if (ret < 0)
  736|         return ret;
  737|     src.format = pass ? pass->format : src.format;
  738|     src.color  = dst.color;
  739| 
  740|     if (!ff_fmt_equal(&src, &dst)) {
  741|         ret = add_convert_pass(graph, &src, &dst, pass, &pass);
  742|         if (ret < 0)
  743|             return ret;
  744|     }
  745| 
  746|     if (!pass) {
  747|         /* No passes were added, so no operations were necessary */
  748|         graph->noop = 1;
  749| 
  750|         /* Add threaded memcpy pass */
  751|         pass = ff_sws_graph_add_pass(graph, dst.format, dst.width, dst.height,
  752|                                      pass, 1, NULL, run_copy);
  753|         if (!pass)
  754|             return AVERROR(ENOMEM);
  755|     }
  756| 
  757|     return 0;
  758| }
  759| 
  760| static void sws_graph_worker(void *priv, int jobnr, int threadnr, int nb_jobs,
```

- `read_file(path=libswscale/ops_dispatch.c, version=old, start_line=330, end_line=365)` →

```
libswscale/ops_dispatch.c lines 330-365 of 396
  330|     const SwsOp *read  = ff_sws_op_list_input(ops);
  331|     const SwsOp *write = ff_sws_op_list_output(ops);
  332|     p->planes_in  = rw_planes(read);
  333|     p->planes_out = rw_planes(write);
  334|     p->pixel_bits_in  = rw_pixel_bits(read);
  335|     p->pixel_bits_out = rw_pixel_bits(write);
  336|     p->exec_base = (SwsOpExec) {
  337|         .width  = dst->width,
  338|         .height = dst->height,
  339|         .block_size_in  = p->comp.block_size * p->pixel_bits_in  >> 3,
  340|         .block_size_out = p->comp.block_size * p->pixel_bits_out >> 3,
  341|     };
  342| 
  343|     for (int i = 0; i < 4; i++) {
  344|         p->idx_in[i]  = i < p->planes_in  ? ops->order_src.in[i] : -1;
  345|         p->idx_out[i] = i < p->planes_out ? ops->order_dst.in[i] : -1;
  346|     }
  347| 
  348|     SwsPass *pass;
  349|     pass = ff_sws_graph_add_pass(graph, dst->format, dst->width, dst->height,
  350|                                  input, p->comp.slice_align, p, op_pass_run);
  351|     if (!pass) {
  352|         ret = AVERROR(ENOMEM);
  353|         goto fail;
  354|     }
  355|     pass->setup = op_pass_setup;
  356|     pass->free  = op_pass_free;
  357| 
  358|     *output = pass;
  359|     return 0;
  360| 
  361| fail:
  362|     op_pass_free(p);
  363|     return ret;
  364| }
  365| 
```

### Turn 3  _(tok 4288+439, stop=tool_use)_

**Reasoning:** Now I need to identify the enclosing functions. Let me find the function names for each call site:

1. `graph.c:160` - This is inside `pass_append` (line 157 starts the function)
2. `graph.c:418` - I need to find the enclosing function. Let me look upwards.
3. `graph.c:710` - I need to find the enclosing function. Let me look upwards.
4. `graph.c:751` - This is inside `init_passes` (line 727 starts the function)
5. `ops_dispatch.c:349` - I need to find the enclosing function. Let me look upwards.

Let me search more to find the function names for the calls at lines 418 and 710, and for ops_dispatch.c:349.

- `read_file(end_line=380, path=libswscale/graph.c, start_line=365, version=old)` →

```
libswscale/graph.c lines 365-380 of 925
  365| 
  366|     *chr_pos = override;
  367| }
  368| 
  369| /* Takes over ownership of `sws` */
  370| static int init_legacy_subpass(SwsGraph *graph, SwsContext *sws,
  371|                                SwsPass *input, SwsPass **output)
  372| {
  373|     SwsInternal *c = sws_internal(sws);
  374|     const int src_w = sws->src_w, src_h = sws->src_h;
  375|     const int dst_w = sws->dst_w, dst_h = sws->dst_h;
  376|     const int unscaled = src_w == dst_w && src_h == dst_h;
  377|     int align = c->dst_slice_align;
  378|     SwsPass *pass = NULL;
  379|     int ret;
  380| 
```

- `read_file(end_line=680, path=libswscale/graph.c, start_line=650, version=old)` →

```
libswscale/graph.c lines 650-680 of 925
  650|     frame_shift(out, y, out_data);
  651| 
  652|     ff_sws_lut3d_apply(lut, in_data[0], in->linesize[0], out_data[0],
  653|                        out->linesize[0], pass->width, h);
  654| }
  655| 
  656| static int adapt_colors(SwsGraph *graph, SwsFormat src, SwsFormat dst,
  657|                         SwsPass *input, SwsPass **output)
  658| {
  659|     enum AVPixelFormat fmt_in, fmt_out;
  660|     SwsColorMap map = {0};
  661|     SwsLut3D *lut;
  662|     SwsPass *pass;
  663|     int ret;
  664| 
  665|     /**
  666|      * Grayspace does not really have primaries, so just force the use of
  667|      * the equivalent other primary set to avoid a conversion. Technically,
  668|      * this does affect the weights used for the Grayscale conversion, but
  669|      * in practise, that should give the expected results more often than not.
  670|      */
  671|     if (isGray(dst.format)) {
  672|         dst.color = src.color;
  673|     } else if (isGray(src.format)) {
  674|         src.color = dst.color;
  675|     }
  676| 
  677|     /* Fully infer color spaces before color mapping logic */
  678|     graph->incomplete |= ff_infer_colors(&src.color, &dst.color);
  679| 
  680|     map.intent = graph->ctx->intent;
```

- `read_file(end_line=310, path=libswscale/ops_dispatch.c, start_line=290, version=old)` →

```
libswscale/ops_dispatch.c lines 290-310 of 396
  290| 
  291|     if (memcpy_in) {
  292|         /* Safe part of last row */
  293|         get_row_data(p, y + h_main, exec.in, exec.out);
  294|         comp->func(&exec, comp->priv, 0, y + h_main, num_blocks - 1, y + h);
  295|     }
  296| 
  297|     /* Handle last column via memcpy, takes over `exec` so call these last */
  298|     if (memcpy_out)
  299|         handle_tail(p, &exec, true, false, y, h_main);
  300|     if (memcpy_in)
  301|         handle_tail(p, &exec, memcpy_out, true, y + h_main, 1);
  302| }
  303| 
  304| static int rw_planes(const SwsOp *op)
  305| {
  306|     return op->rw.packed ? 1 : op->rw.elems;
  307| }
  308| 
  309| static int rw_pixel_bits(const SwsOp *op)
  310| {
```

### Turn 4  _(tok 5677+89, stop=tool_use)_

- `grep(pattern=^static.*\(, path_glob=libswscale/ops_dispatch.c, version=old)` →

```
7 matches
libswscale/ops_dispatch.c:96:static void op_pass_free(void *ptr)
libswscale/ops_dispatch.c:108:static inline void get_row_data(const SwsOpPass *p, const int y,
libswscale/ops_dispatch.c:118:static void op_pass_setup(const SwsFrame *out, const SwsFrame *in,
libswscale/ops_dispatch.c:252:static void op_pass_run(const SwsFrame *out, const SwsFrame *in, const int y,
libswscale/ops_dispatch.c:304:static int rw_planes(const SwsOp *op)
libswscale/ops_dispatch.c:309:static int rw_pixel_bits(const SwsOp *op)
libswscale/ops_dispatch.c:318:static int compile(SwsGraph *graph, const SwsOpList *ops,
```

### Turn 5  _(tok 5972+402, stop=tool_use)_

**Reasoning:** Now I have all the enclosing functions:

1. `graph.c:160` → `pass_append` (line 157)
2. `graph.c:418` → `init_legacy_subpass` (line 370)
3. `graph.c:710` → `adapt_colors` (line 656)
4. `graph.c:751` → `init_passes` (line 727)
5. `ops_dispatch.c:349` → `compile` (line 318)

All are in `libswscale/graph.c` and `libswscale/ops_dispatch.c`. Let me verify the call at line 418 is indeed inside `init_legacy_subpass`.

**Says:** Now I have all the data I need. Let me verify the function boundaries:

- `graph.c:157` – `pass_append`
- `graph.c:370` – `init_legacy_subpass`
- `graph.c:656` – `adapt_colors`
- `graph.c:727` – `init_passes`
- `ops_dispatch.c:318` – `compile`

All confirmed. Let me submit

- **submit_callers** → `{"callers": [{"function": "pass_append", "file": "libswscale/graph.c"}, {"function": "init_legacy_subpass", "file": "libswscale/graph.c"}, {"function": "adapt_colors", "file": "libswscale/graph.c"}, {"function": "init_passes", "file": "libswscale/graph.c"}, {"function": "compile", "file": "libswscale/ops_dispatch.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

