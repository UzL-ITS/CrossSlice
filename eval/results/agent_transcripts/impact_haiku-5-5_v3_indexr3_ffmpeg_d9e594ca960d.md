# Impact-analysis transcript — ffmpeg @ d9e594ca960d — anthropic:claude-haiku-5-5

- target: `ff_sws_graph_add_pass` (libswscale/graph.c), arity 8->9
- truth: [['libswscale/graph.c', 'adapt_colors'], ['libswscale/graph.c', 'init_legacy_subpass'], ['libswscale/graph.c', 'init_passes'], ['libswscale/graph.c', 'pass_append'], ['libswscale/ops_dispatch.c', 'compile']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1394+153, stop=tool_use)_

**Reasoning:** I'll start by searching for references to the symbol using find_references.



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

### Turn 2  _(tok 2441+556, stop=tool_use)_

**Reasoning:** I need the enclosing functions, so I'm checking the wrapper around line 160, which should start near line 157. I'm going to read those sections now.



**Says:** Six call sites in three files. I need the enclosing function for each, so I'll read those regions.

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

- `read_file(path=libswscale/graph.c, version=old, start_line=380, end_line=425)` →

```
libswscale/graph.c lines 380-425 of 925
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

- `read_file(path=libswscale/graph.c, version=old, start_line=680, end_line=760)` →

```
libswscale/graph.c lines 680-760 of 925
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

- `read_file(path=libswscale/ops_dispatch.c, version=old, start_line=320, end_line=360)` →

```
libswscale/ops_dispatch.c lines 320-360 of 396
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

### Turn 3  _(tok 7220+392, stop=tool_use)_

**Reasoning:** I need the enclosing function for ops_dispatch.c line 349, which probably starts around lines 318–319. For graph.c line 418, I think it sits inside init_legacy_subpass, since line 390 calls that function, so I'll check the function headers to confirm.



**Says:** I need the function headers that enclose lines 418, 349, 710 and 751 to confirm the names.

- `grep(pattern=^[A-Za-z_].*\(|^\{, version=old, path_glob=libswscale/graph.c)` →

```
66 matches (showing 60)
libswscale/graph.c:42:static int frame_alloc_planes(AVFrame *dst)
libswscale/graph.c:43:{
libswscale/graph.c:77:static int pass_alloc_output(SwsPass *pass)
libswscale/graph.c:78:{
libswscale/graph.c:101:static void free_buffer(AVRefStructOpaque opaque, void *obj)
libswscale/graph.c:102:{
libswscale/graph.c:107:SwsPass *ff_sws_graph_add_pass(SwsGraph *graph, enum AVPixelFormat fmt,
libswscale/graph.c:110:{
libswscale/graph.c:157:static int pass_append(SwsGraph *graph, enum AVPixelFormat fmt, int w, int h,
libswscale/graph.c:159:{
libswscale/graph.c:167:static void frame_shift(const SwsFrame *f, const int y, uint8_t *data[4])
libswscale/graph.c:168:{
libswscale/graph.c:177:static void run_copy(const SwsFrame *out, const SwsFrame *in, int y, int h,
libswscale/graph.c:179:{
libswscale/graph.c:203:static void run_rgb0(const SwsFrame *out, const SwsFrame *in, int y, int h,
libswscale/graph.c:205:{
libswscale/graph.c:224:static void run_xyz2rgb(const SwsFrame *out, const SwsFrame *in, int y, int h,
libswscale/graph.c:226:{
libswscale/graph.c:233:static void run_rgb2xyz(const SwsFrame *out, const SwsFrame *in, int y, int h,
libswscale/graph.c:235:{
libswscale/graph.c:248:static void free_legacy_swscale(void *priv)
libswscale/graph.c:249:{
libswscale/graph.c:254:static void setup_legacy_swscale(const SwsFrame *out, const SwsFrame *in,
libswscale/graph.c:256:{
libswscale/graph.c:268:static inline SwsContext *slice_ctx(const SwsPass *pass, int y)
libswscale/graph.c:269:{
libswscale/graph.c:287:static void run_legacy_unscaled(const SwsFrame *out, const SwsFrame *in,
libswscale/graph.c:289:{
libswscale/graph.c:299:static void run_legacy_swscale(const SwsFrame *out, const SwsFrame *in,
libswscale/graph.c:301:{
libswscale/graph.c:311:static void get_chroma_pos(SwsGraph *graph, int *h_chr_pos, int *v_chr_pos,
libswscale/graph.c:313:{
libswscale/graph.c:354:static void legacy_chr_pos(SwsGraph *graph, int *chr_pos, int override, int *warned)
libswscale/graph.c:355:{
libswscale/graph.c:370:static int init_legacy_subpass(SwsGraph *graph, SwsContext *sws,
libswscale/graph.c:372:{
libswscale/graph.c:480:static int add_legacy_sws_pass(SwsGraph *graph, const SwsFormat *src,
libswscale/graph.c:483:{
libswscale/graph.c:555:static int add_convert_pass(SwsGraph *graph, const SwsFormat *src,
libswscale/graph.c:558:{
libswscale/graph.c:630:static void free_lut3d(void *priv)
libswscale/graph.c:631:{
libswscale/graph.c:636:static void setup_lut3d(const SwsFrame *out, const SwsFrame *in, const SwsPass *pass)
libswscale/graph.c:637:{
libswscale/graph.c:644:static void run_lut3d(const SwsFrame *out, const SwsFrame *in, int y, int h,
libswscale/graph.c:646:{
libswscale/graph.c:656:static int adapt_colors(SwsGraph *graph, SwsFormat src, SwsFormat dst,
libswscale/graph.c:658:{
libswscale/graph.c:727:static int init_passes(SwsGraph *graph)
libswscale/graph.c:728:{
libswscale/graph.c:760:static void sws_graph_worker(void *priv, int jobnr, int threadnr, int nb_jobs,
libswscale/graph.c:762:{
libswscale/graph.c:771:int ff_sws_graph_create(SwsContext *ctx, const SwsFormat *dst, const SwsFormat *src,
libswscale/graph.c:773:{
libswscale/graph.c:812:void ff_sws_graph_free(SwsGraph **pgraph)
libswscale/graph.c:813:{
libswscale/graph.c:834:static int opts_equal(const SwsContext *c1, const SwsContext *c2)
libswscale/graph.c:835:{
libswscale/graph.c:850:int ff_sws_graph_reinit(SwsContext *ctx, const SwsFormat *dst, const SwsFormat *src,
libswscale/graph.c:852:{
```

- `grep(pattern=^[A-Za-z_].*\(, version=old, path_glob=libswscale/ops_dispatch.c)` →

```
11 matches
libswscale/ops_dispatch.c:47:int ff_sws_ops_compile_backend(SwsContext *ctx, const SwsOpBackend *backend,
libswscale/ops_dispatch.c:74:int ff_sws_ops_compile(SwsContext *ctx, const SwsOpList *ops, SwsCompiledOp *out)
libswscale/ops_dispatch.c:96:static void op_pass_free(void *ptr)
libswscale/ops_dispatch.c:108:static inline void get_row_data(const SwsOpPass *p, const int y,
libswscale/ops_dispatch.c:118:static void op_pass_setup(const SwsFrame *out, const SwsFrame *in,
libswscale/ops_dispatch.c:188:handle_tail(const SwsOpPass *p, SwsOpExec *exec,
libswscale/ops_dispatch.c:252:static void op_pass_run(const SwsFrame *out, const SwsFrame *in, const int y,
libswscale/ops_dispatch.c:304:static int rw_planes(const SwsOp *op)
libswscale/ops_dispatch.c:309:static int rw_pixel_bits(const SwsOp *op)
libswscale/ops_dispatch.c:318:static int compile(SwsGraph *graph, const SwsOpList *ops,
libswscale/ops_dispatch.c:366:int ff_sws_compile_pass(SwsGraph *graph, SwsOpList *ops, int flags,
```

### Turn 4  _(tok 9966+576, stop=tool_use)_

**Reasoning:** I'm mapping each line number to its enclosing function: 160 is in pass_append, 418 is inside init_legacy_subpass, 710 falls between adapt_colors and init_passes so it belongs to adapt_colors, and 751 is in init_passes. Line 710 is not in add_convert_pass, since that starts at 555.

I'm checking whether anything else calls this function through a pointer or macro, and the reference search and grep both came back with only 6 hits. I'm also confirming line 710 falls inside adapt_colors, which sits between 656 and 727, so it's correct.



**Says:** The six call sites resolve to five enclosing functions. A text grep and the GNU Global index both returned the same set of references, so the list should be complete.

- **submit_callers** → `{"callers": [{"function": "pass_append", "file": "libswscale/graph.c"}, {"function": "init_legacy_subpass", "file": "libswscale/graph.c"}, {"function": "adapt_colors", "file": "libswscale/graph.c"}, {"function": "init_passes", "file": "libswscale/graph.c"}, {"function": "compile", "file": "libswscale/ops_dispatch.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

