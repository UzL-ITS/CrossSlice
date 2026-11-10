# Impact-analysis transcript — ffmpeg @ d9e594ca960d — anthropic:claude-haiku-5-5

- target: `ff_sws_graph_add_pass` (libswscale/graph.c), arity 8->9
- truth: [['libswscale/graph.c', 'adapt_colors'], ['libswscale/graph.c', 'init_legacy_subpass'], ['libswscale/graph.c', 'init_passes'], ['libswscale/graph.c', 'pass_append'], ['libswscale/ops_dispatch.c', 'compile']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1394+153, stop=tool_use)_

**Reasoning:** I'll start by looking up where this symbol is referenced, using find_references.



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

- `grep(pattern=ff_sws_graph_add_pass, version=old)` →

```
8 matches
libswscale/graph.c:107:SwsPass *ff_sws_graph_add_pass(SwsGraph *graph, enum AVPixelFormat fmt,
libswscale/graph.c:156:/* Wrapper around ff_sws_graph_add_pass() that chains a pass "in-place" */
libswscale/graph.c:160:    SwsPass *new = ff_sws_graph_add_pass(graph, fmt, w, h, *pass, align, priv, run);
libswscale/graph.c:418:    pass = ff_sws_graph_add_pass(graph, sws->dst_format, dst_w, dst_h, input, align, sws,
libswscale/graph.c:710:    pass = ff_sws_graph_add_pass(graph, fmt_out, src.width, src.height,
libswscale/graph.c:751:        pass = ff_sws_graph_add_pass(graph, dst.format, dst.width, dst.height,
libswscale/graph.h:159:SwsPass *ff_sws_graph_add_pass(SwsGraph *graph, enum AVPixelFormat fmt,
libswscale/ops_dispatch.c:349:    pass = ff_sws_graph_add_pass(graph, dst->format, dst->width, dst->height,
```

### Turn 2  _(tok 2441+573, stop=tool_use)_

**Reasoning:** I need to find the enclosing function for each location: graph.c lines 160, 418, 710, and 751, plus ops_dispatch.c line 349. I'll read those sections of the files.



**Says:** The index gives five call sites (plus the prototype and definition). I need the enclosing function for each, so I'll read those regions.

- `read_file(path=libswscale/graph.c, version=old, start_line=100, end_line=170)` →

```
libswscale/graph.c lines 100-170 of 925
  100| 
  101| static void free_buffer(AVRefStructOpaque opaque, void *obj)
  102| {
  103|     SwsPassBuffer *buffer = obj;
  104|     av_frame_free(&buffer->avframe);
  105| }
  106| 
  107| SwsPass *ff_sws_graph_add_pass(SwsGraph *graph, enum AVPixelFormat fmt,
  108|                                int width, int height, SwsPass *input,
  109|                                int align, void *priv, sws_filter_run_t run)
  110| {
  111|     int ret;
  112|     SwsPass *pass = av_mallocz(sizeof(*pass));
  113|     if (!pass)
  114|         return NULL;
  115| 
  116|     pass->graph  = graph;
  117|     pass->run    = run;
  118|     pass->priv   = priv;
  119|     pass->format = fmt;
  120|     pass->width  = width;
  121|     pass->height = height;
  122|     pass->input  = input;
  123|     pass->output = av_refstruct_alloc_ext(sizeof(*pass->output), 0, NULL, free_buffer);
  124|     if (!pass->output)
  125|         goto fail;
  126| 
  127|     ret = pass_alloc_output(input);
  128|     if (ret < 0)
  129|         goto fail;
  130| 
  131|     if (!align) {
  132|         pass->slice_h = pass->height;
  133|         pass->num_slices = 1;
  134|     } else {
  135|         pass->slice_h = (pass->height + graph->num_threads - 1) / graph->num_threads;
  136|         pass->slice_h = FFALIGN(pass->slice_h, align);
  137|         pass->num_slices = (pass->height + pass->slice_h - 1) / pass->slice_h;
  138|     }
  139| 
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
```

- `read_file(path=libswscale/graph.c, version=old, start_line=340, end_line=425)` →

```
libswscale/graph.c lines 340-425 of 925
  340|          * rows to get to the chroma sample. */
  341|         if (graph->field == FIELD_BOTTOM)
  342|             y_pos += (256 << sub_y) - 256;
  343| 
  344|         /* Luma row distance is doubled for fields, so halve offsets */
  345|         y_pos >>= 1;
  346|     }
  347| 
  348|     /* Explicitly strip chroma offsets when not subsampling, because it
  349|      * interferes with the operation of flags like SWS_FULL_CHR_H_INP */
  350|     *h_chr_pos = sub_x ? x_pos : -513;
  351|     *v_chr_pos = sub_y ? y_pos : -513;
  352| }
  353| 
  354| static void legacy_chr_pos(SwsGraph *graph, int *chr_pos, int override, int *warned)
  355| {
  356|     if (override == -513 || override == *chr_pos)
  357|         return;
  358| 
  359|     if (!*warned) {
  360|         av_log(NULL, AV_LOG_WARNING,
  361|                "Setting chroma position directly is deprecated, make sure "
  362|                "the frame is tagged with the correct chroma location.\n");
  363|         *warned = 1;
  364|     }
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
  381|     if (c->cascaded_context[0]) {
  382|         const int num_cascaded = c->cascaded_context[2] ? 3 : 2;
  383|         for (int i = 0; i < num_cascaded; i++) {
  384|             const int is_last = i + 1 == num_cascaded;
  385| 
  386|             /* Steal cascaded context, so we can manage its lifetime independently */
  387|             SwsContext *sub = c->cascaded_context[i];
  388|             c->cascaded_context[i] = NULL;
  389| 
  390|             ret = init_legacy_subpass(graph, sub, input, is_last ? output : &input);
  391|             if (ret < 0)
  392|                 break;
  393|         }
  394| 
  395|         sws_free_context(&sws);
  396|         return ret;
  397|     }
  398| 
  399|     if (sws->dither == SWS_DITHER_ED && !c->convert_unscaled)
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
```

- `read_file(path=libswscale/graph.c, version=old, start_line=660, end_line=760)` →

```
libswscale/graph.c lines 660-760 of 925
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
  681|     map.src    = src.color;
  682|     map.dst    = dst.color;
  683| 
  684|     if (ff_sws_color_map_noop(&map))
  685|         return 0;
  686| 
  687|     if (src.hw_format != AV_PIX_FMT_NONE || dst.hw_format != AV_PIX_FMT_NONE)
  688|         return AVERROR(ENOTSUP);
  689| 
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

- `read_file(path=libswscale/ops_dispatch.c, version=old, start_line=300, end_line=360)` →

```
libswscale/ops_dispatch.c lines 300-360 of 396
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
  311|     const int elems = op->rw.packed ? op->rw.elems : 1;
  312|     const int size  = ff_sws_pixel_type_size(op->type);
  313|     const int bits  = 8 >> op->rw.frac;
  314|     av_assert1(bits >= 1);
  315|     return elems * size * bits;
  316| }
  317| 
  318| static int compile(SwsGraph *graph, const SwsOpList *ops,
  319|                    const SwsFormat *dst, SwsPass *input, SwsPass **output)
  320| {
  321|     SwsContext *ctx = graph->ctx;
  322|     SwsOpPass *p = av_mallocz(sizeof(*p));
  323|     if (!p)
  324|         return AVERROR(ENOMEM);
  325| 
  326|     int ret = ff_sws_ops_compile(ctx, ops, &p->comp);
  327|     if (ret < 0)
  328|         goto fail;
  329| 
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
```

### Turn 3  _(tok 8601+365, stop=tool_use)_

**Reasoning:** I'm mapping each reference site to its enclosing function: pass_append, init_legacy_subpass, init_passes, and compile are identified, but the one at line 710 still needs a name. I'll read the header above line 660 to find it, and I also want to check whether find_references might miss hits inside macros.

I'm checking that the search index and grep turn up the same set of references, and I'm also looking for function-pointer or other non-call uses, which grep should already catch since it scans all the text.



**Says:** Four of the five enclosing functions are clear. The call at line 710 sits in a function whose header is above my read window, so I need to find it.

- `read_file(path=libswscale/graph.c, version=old, start_line=645, end_line=660)` →

```
libswscale/graph.c lines 645-660 of 925
  645|                       const SwsPass *pass)
  646| {
  647|     SwsLut3D *lut = pass->priv;
  648|     uint8_t *in_data[4], *out_data[4];
  649|     frame_shift(in,  y, in_data);
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
```

### Turn 4  _(tok 9285+305, stop=tool_use)_

**Reasoning:** I've pinned down the two spots: line 710 is in adapt_colors and line 160 is in pass_append. The reference search returned six hits and matches the grep, so I'm confident the list is complete and I'll submit.



**Says:** I've checked all five call sites against their enclosing functions, and the index and grep agree on the full set of references.

- **submit_callers** → `{"callers": [{"function": "pass_append", "file": "libswscale/graph.c"}, {"function": "init_legacy_subpass", "file": "libswscale/graph.c"}, {"function": "adapt_colors", "file": "libswscale/graph.c"}, {"function": "init_passes", "file": "libswscale/graph.c"}, {"function": "compile", "file": "libswscale/ops_dispatch.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

