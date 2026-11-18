# Impact-analysis transcript — ffmpeg @ d9e594ca960d — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_sws_graph_add_pass` (libswscale/graph.c), arity 8->9
- truth: [['libswscale/graph.c', 'adapt_colors'], ['libswscale/graph.c', 'init_legacy_subpass'], ['libswscale/graph.c', 'init_passes'], ['libswscale/graph.c', 'pass_append'], ['libswscale/ops_dispatch.c', 'compile']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1075+163, stop=tool_use)_

**Reasoning:** Let me look at the repository to find calls to ff_sws_graph_add_pass.

Note the tool says "which version of the repository to look at" with enum "old". So list_files requires version "old". find_references doesn't require version.

Let me start.


**Says:** 

I'll start by looking at the definition and all references to this symbol.




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

- `grep(pattern=ff_sws_graph_add_pass, version=old, max_results=200)` →

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

### Turn 2  _(tok 1794+316, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing functions for each call site. Let me read the relevant portions of graph.c and ops_dispatch.c.

Let me read around lines 100-200, 380-430, 650-770 of graph.c, and around 300-360 of ops_dispatch.c.

Also, I should check whether the wrapper function at line 156-160 is itself called by other functions — but the task asks for functions that call ff_sws_graph_add_pass directly. Hmm, "List every function in this repository that calls ff_sws_graph_add_pass". That's direct callers. But impact analysis: EVERY call site must be updated — so direct call sites. I'll list direct callers only.

Let me read the files.


- `read_file(path=libswscale/graph.c, start_line=90, end_line=200, version=old)` →

```
libswscale/graph.c lines 90-200 of 925
   90|     int ret = frame_alloc_planes(avframe);
   91|     if (ret < 0) {
   92|         av_frame_free(&avframe);
   93|         return ret;
   94|     }
   95| 
   96|     buffer->avframe = avframe;
   97|     ff_sws_frame_from_avframe(&buffer->frame, avframe);
   98|     return 0;
   99| }
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
  171|             data[i] = f->data[i] + (y >> ff_fmt_vshift(f->format, i)) * f->linesize[i];
  172|         else
  173|             data[i] = NULL;
  174|     }
  175| }
  176| 
  177| static void run_copy(const SwsFrame *out, const SwsFrame *in, int y, int h,
  178|                      const SwsPass *pass)
  179| {
  180|     uint8_t *in_data[4], *out_data[4];
  181|     frame_shift(in,  y, in_data);
  182|     frame_shift(out, y, out_data);
  183| 
  184|     for (int i = 0; i < 4 && out_data[i]; i++) {
  185|         const int lines = h >> ff_fmt_vshift(in->format, i);
  186|         av_assert1(in_data[i]);
  187| 
  188|         if (in_data[i] == out_data[i]) {
  189|             av_assert0(in->linesize[i] == out->linesize[i]);
  190|         } else if (in->linesize[i] == out->linesize[i]) {
  191|             memcpy(out_data[i], in_data[i], lines * out->linesize[i]);
  192|         } else {
  193|             const int linesize = FFMIN(out->linesize[i], in->linesize[i]);
  194|             for (int j = 0; j < lines; j++) {
  195|                 memcpy(out_data[i], in_data[i], linesize);
  196|                 in_data[i]  += in->linesize[i];
  197|                 out_data[i] += out->linesize[i];
  198|             }
  199|         }
  200|     }
```

- `read_file(path=libswscale/ops_dispatch.c, start_line=280, end_line=380, version=old)` →

```
libswscale/ops_dispatch.c lines 280-380 of 396
  280|     const int last_slice  = y + h == pass->height;
  281|     const bool memcpy_in  = last_slice && p->memcpy_in;
  282|     const bool memcpy_out = p->memcpy_out;
  283|     const int num_blocks  = p->num_blocks;
  284|     const int blocks_main = num_blocks - memcpy_out;
  285|     const int h_main      = h - memcpy_in;
  286| 
  287|     /* Handle main section */
  288|     get_row_data(p, y, exec.in, exec.out);
  289|     comp->func(&exec, comp->priv, 0, y, blocks_main, y + h_main);
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
  361| fail:
  362|     op_pass_free(p);
  363|     return ret;
  364| }
  365| 
  366| int ff_sws_compile_pass(SwsGraph *graph, SwsOpList *ops, int flags,
  367|                         const SwsFormat *dst, SwsPass *input, SwsPass **output)
  368| {
  369|     SwsContext *ctx = graph->ctx;
  370|     int ret;
  371| 
  372|     /* Check if the whole operation graph is an end-to-end no-op */
  373|     if (ff_sws_op_list_is_noop(ops)) {
  374|         *output = input;
  375|         return 0;
  376|     }
  377| 
  378|     const SwsOp *read  = ff_sws_op_list_input(ops);
  379|     const SwsOp *write = ff_sws_op_list_output(ops);
  380|     if (!read || !write) {
```

### Turn 3  _(tok 5570+116, stop=tool_use)_

**Reasoning:** So one caller in ops_dispatch.c: `compile` at line 318.

Now graph.c line 418, 710, 751. Let's read those regions.


- `read_file(end_line=440, path=libswscale/graph.c, start_line=370, version=old)` →

```
libswscale/graph.c lines 370-440 of 925
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
  436|         if (!c->slice_ctx)
  437|             return AVERROR(ENOMEM);
  438| 
  439|         for (int i = 0; i < pass->num_slices; i++) {
  440|             SwsContext *slice;
```

### Turn 4  _(tok 6931+102, stop=tool_use)_

**Reasoning:** Caller at 418: `init_legacy_subpass` in graph.c.

Now lines 710 and 751.


- `read_file(end_line=780, path=libswscale/graph.c, start_line=650, version=old)` →

```
libswscale/graph.c lines 650-780 of 925
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
  761|                              int nb_threads)
  762| {
  763|     SwsGraph *graph = priv;
  764|     const SwsPass *pass = graph->exec.pass;
  765|     const int slice_y = jobnr * pass->slice_h;
  766|     const int slice_h = FFMIN(pass->slice_h, pass->height - slice_y);
  767| 
  768|     pass->run(graph->exec.output, graph->exec.input, slice_y, slice_h, pass);
  769| }
  770| 
  771| int ff_sws_graph_create(SwsContext *ctx, const SwsFormat *dst, const SwsFormat *src,
  772|                         int field, SwsGraph **out_graph)
  773| {
  774|     int ret;
  775|     SwsGraph *graph = av_mallocz(sizeof(*graph));
  776|     if (!graph)
  777|         return AVERROR(ENOMEM);
  778| 
  779|     graph->ctx = ctx;
  780|     graph->src = *src;
```

### Turn 5  _(tok 9022+803, stop=tool_use)_

**Reasoning:** Callers:
1. `pass_append` in libswscale/graph.c (line 160)
2. `init_legacy_subpass` in libswscale/graph.c (line 418)
3. `adapt_colors` in libswscale/graph.c (line 710)
4. `init_passes` in libswscale/graph.c (line 751)
5. `compile` in libswscale/ops_dispatch.c (line 349)

But wait — could there be other files that include graph.h and call it? grep found all matches (8 matches, including definition, prototype, comment). So 5 call sites.

But also, I should double-check that there aren't calls through a macro or a wrapper, or a similarly-named function. Let me check whether there might be other versions of the repo... The tool says version "old" is the only option. Also, maybe the grep only searched tracked files. Let's also check if there's any function pointer assignment of ff_sws_graph_add_pass. No.

Also, could there be a call site hidden with a line break, e.g. "ff_sws_graph_add_pass\n(" — grep with line-based matching would catch the name anyway since the name appears.

Hmm, but wait: is there any possibility that a call site exists where the name is split across lines like "ff_sws_graph_" + "add_pass"? Unlikely.

Also should I check whether `pass_append` wrapper is what the question considers... The question says list every function that calls ff_sws_graph_add_pass — direct callers. So 5 functions.

Let me double-check that there isn't another file like libswscale/ops_dispatch.c having another call, and check whether there's a second definition or a declaration in another header. Already covered.

Let me also verify the enclosing function names precisely by checking that lines 418 is inside init_legacy_subpass (function starts at 370) and there's no other function boundary between. Let me quickly check the region between 370 and 418 — I read 370-440, and there's no function boundary. Good.

For 710: function adapt_colors starts at 656, ends at 721. Good.

For 751: init_passes starts at 727, ends 758. Good.

For 160: pass_append starts at 157, ends 165. Good.

For 349 in ops_dispatch.c: compile starts at 318, ends 364. Good.

Also, let me check whether there might be calls in other directories (e.g., tests). grep searched whole repo with 8 matches. Good.

One more consideration: maybe the grep tool's default max_results truncated? I set max_results 200 and got 8 matches. Fine.

Let me also verify there's no alias e.g. `#define add_pass ff_sws_graph_add_pass`. grep would show ff_sws_graph_add_pass occurrences only in those places. So no.

Confidence: high.

Let me do one sanity check for any similar-named symbols like ff_sws_graph_add_pass variants.

Actually, let me also double check whether graph.c has multiple functions and whether there could be a call hidden inside a macro definition that spans lines. I'll do a quick grep for "add_pass" to see all.


- `grep(max_results=100, pattern=add_pass, version=old)` →

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

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 9616+141, stop=tool_use, forced)_

**Reasoning:** Submit the 5 callers.


- **submit_callers** → `{"callers": [{"function": "pass_append", "file": "libswscale/graph.c"}, {"function": "init_legacy_subpass", "file": "libswscale/graph.c"}, {"function": "adapt_colors", "file": "libswscale/graph.c"}, {"function": "init_passes", "file": "libswscale/graph.c"}, {"function": "compile", "file": "libswscale/ops_dispatch.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

