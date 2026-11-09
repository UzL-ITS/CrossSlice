# Impact-analysis transcript — ffmpeg @ d9e594ca960d — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_sws_graph_add_pass` (libswscale/graph.c), arity 8->9
- truth: [['libswscale/graph.c', 'adapt_colors'], ['libswscale/graph.c', 'init_legacy_subpass'], ['libswscale/graph.c', 'init_passes'], ['libswscale/graph.c', 'pass_append'], ['libswscale/ops_dispatch.c', 'compile']]

## Self-navigation arm

### Turn 1  _(tok 946+159, stop=tool_use)_

**Reasoning:** Let me search for the function name.

Note: the repository tools have a "version" parameter with enum "old". Interesting — maybe there's only "old" version. Let's just use "old".

Wait, but the task says "this repository". Let me list files first.


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

- `list_files(path=libswscale, version=old)` →

```
134 files
libswscale/Makefile	2487
libswscale/alphablend.c	9798
libswscale/bayer_template.c	9418
libswscale/cms.c	25919
libswscale/cms.h	3597
libswscale/csputils.c	25290
libswscale/csputils.h	3486
libswscale/format.c	52155
libswscale/format.h	6686
libswscale/gamma.c	2227
libswscale/graph.c	29608
libswscale/graph.h	6090
libswscale/half2float.c	798
libswscale/hscale.c	9682
libswscale/hscale_fast_bilinear.c	2065
libswscale/input.c	123615
libswscale/libswscale.v	90
libswscale/log2_tab.c	32
libswscale/lut3d.c	9302
libswscale/lut3d.h	3187
libswscale/ops.c	29447
libswscale/ops.h	10561
libswscale/ops_backend.c	3089
libswscale/ops_backend.h	7180
libswscale/ops_chain.c	9143
libswscale/ops_chain.h	4908
libswscale/ops_dispatch.c	13485
libswscale/ops_dispatch.h	3217
libswscale/ops_internal.h	4306
libswscale/ops_memcpy.c	4420
libswscale/ops_optimizer.c	25328
libswscale/ops_tmpl_common.c	6992
libswscale/ops_tmpl_float.c	9321
libswscale/ops_tmpl_int.c	20011
libswscale/options.c	9763
libswscale/output.c	147086
libswscale/rgb2rgb.c	21240
libswscale/rgb2rgb.h	9019
libswscale/rgb2rgb_template.c	28379
libswscale/slice.c	12469
libswscale/swscale.c	55941
libswscale/swscale.h	25762
libswscale/swscale_internal.h	50523
libswscale/swscale_unscaled.c	115602
libswscale/swscaleres.rc	2030
libswscale/utils.c	89355
libswscale/version.c	1260
libswscale/version.h	1589
libswscale/version_major.h	1175
libswscale/vscale.c	13539
libswscale/yuv2rgb.c	46540
libswscale/aarch64/Makefile	551
libswscale/aarch64/asm-offsets.h	1230
libswscale/aarch64/hscale.S	76669
libswscale/aarch64/input.S	15831
libswscale/aarch64/output.S	30637
libswscale/aarch64/range_convert_neon.S	6112
libswscale/aarch64/rgb2rgb.c	5419
libswscale/aarch64/rgb2rgb_neon.S	30246
libswscale/aarch64/swscale.c	19171
libswscale/aarch64/swscale_unscaled.c	21620
libswscale/aarch64/swscale_unscaled_neon.S	2762
libswscale/aarch64/xyz2rgb_neon.S	43541
libswscale/aarch64/yuv2rgb_neon.S	15590
libswscale/arm/Makefile	325
libswscale/arm/hscale.S	5374
libswscale/arm/output.S	5806
libswscale/arm/rgb2yuv_neon_16.S	2294
libswscale/arm/rgb2yuv_neon_32.S	3282
libswscale/arm/rgb2yuv_neon_common.S	6921
libswscale/arm/swscale.c	1777
libswscale/arm/swscale_unscaled.c	11335
libswscale/arm/yuv2rgb_neon.S	13201
libswscale/loongarch/Makefile	738
libswscale/loongarch/input.S	24237
libswscale/loongarch/input_lasx.c	8948
libswscale/loongarch/input_lsx.c	1960
libswscale/loongarch/output.S	12482
libswscale/loongarch/output_lasx.c	85065
libswscale/loongarch/output_lsx.c	77156
libswscale/loongarch/rgb2rgb_lasx.c	1896
libswscale/loongarch/swscale.S	82453
libswscale/loongarch/swscale_init_loongarch.c	6524
libswscale/loongarch/swscale_lasx.c	47414
libswscale/loongarch/swscale_loongarch.h	10994
libswscale/loongarch/swscale_lsx.c	2337
libswscale/loongarch/yuv2rgb_lasx.c	23414
libswscale/loongarch/yuv2rgb_lsx.c	19060
libswscale/ppc/Makefile	248
libswscale/ppc/swscale_altivec.c	8849
libswscale/ppc/swscale_ppc_template.c	6878
libswscale/ppc/swscale_vsx.c	82427
libswscale/ppc/yuv2rgb_altivec.c	40955
libswscale/ppc/yuv2rgb_altivec.h	2079
libswscale/ppc/yuv2yuv_altivec.c	8872
libswscale/riscv/Makefile	210
libswscale/riscv/cpu_common.c	40
libswscale/riscv/input_rvv.S	8881
libswscale/riscv/range_rvv.S	3286
libswscale/riscv/rgb2rgb.c	2916
libswscale/riscv/rgb2rgb_rvb.S	1008
libswscale/riscv/rgb2rgb_rvv.S	4479
libswscale/riscv/swscale.c	4595
libswscale/tests/.gitignore	59
libswscale/tests/colorspace.c	5931
libswscale/tests/floatimg_cmp.c	9347
libswscale/tests/pixdesc_query.c	3004
libswscale/tests/sws_ops.c	5173
libswscale/tests/swscale.c	23136
libswscale/vulkan/Makefile	215
libswscale/vulkan/ops.c	12407
libswscale/vulkan/ops.h	1303
libswscale/vulkan/vulkan.c	794
libswscale/vulkan/vulkan_glslang.c	802
libswscale/vulkan/vulkan_shaderc.c	802
libswscale/x86/Makefile	1224
libswscale/x86/hscale_fast_bilinear_simd.c	14040
libswscale/x86/input.asm	41703
libswscale/x86/ops.c	42449
libswscale/x86/ops_common.asm	10045
libswscale/x86/ops_float.asm	10845
libswscale/x86/ops_int.asm	29555
libswscale/x86/output.asm	27005
libswscale/x86/range_convert.asm	5789
libswscale/x86/rgb2rgb.c	92653
libswscale/x86/rgb_2_rgb.asm	12529
libswscale/x86/scale.asm	13664
libswscale/x86/scale_avx2.asm	4110
libswscale/x86/swscale.c	36157
libswscale/x86/swscale_template.c	68992
libswscale/x86/w64xmmtest.c	1253
libswscale/x86/yuv2rgb.c	11231
libswscale/x86/yuv2yuvX.asm	4255
libswscale/x86/yuv_2_rgb.asm	10004
```

### Turn 2  _(tok 3491+260, stop=tool_use)_

**Reasoning:** Now let's identify enclosing functions for each call site.

graph.c lines: 160, 418, 710, 751. ops_dispatch.c: 349.

Let's read the relevant regions.

Also note grep might have missed matches due to line wrapping? Not for calls. But could there be calls in files that grep missed because of max_results? Only 8 matches. Also there could be calls through macro. Let's also check for "graph_add_pass" partial.

Let me read graph.c around each line.


- `read_file(path=libswscale/graph.c, start_line=95, end_line=185, version=old)` →

```
libswscale/graph.c lines 95-185 of 925
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
```

- `read_file(path=libswscale/graph.c, start_line=380, end_line=440, version=old)` →

```
libswscale/graph.c lines 380-440 of 925
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

### Turn 3  _(tok 6232+116, stop=tool_use)_

**Reasoning:** Need to find the enclosing function for line 418. Let me look back further, e.g., search for "static int init_legacy" in graph.c.


- `grep(pattern=^[A-Za-z_].*\(|^static .*\(, path_glob=libswscale/graph.c, version=old, max_results=100)` →

```
33 matches
libswscale/graph.c:42:static int frame_alloc_planes(AVFrame *dst)
libswscale/graph.c:77:static int pass_alloc_output(SwsPass *pass)
libswscale/graph.c:101:static void free_buffer(AVRefStructOpaque opaque, void *obj)
libswscale/graph.c:107:SwsPass *ff_sws_graph_add_pass(SwsGraph *graph, enum AVPixelFormat fmt,
libswscale/graph.c:157:static int pass_append(SwsGraph *graph, enum AVPixelFormat fmt, int w, int h,
libswscale/graph.c:167:static void frame_shift(const SwsFrame *f, const int y, uint8_t *data[4])
libswscale/graph.c:177:static void run_copy(const SwsFrame *out, const SwsFrame *in, int y, int h,
libswscale/graph.c:203:static void run_rgb0(const SwsFrame *out, const SwsFrame *in, int y, int h,
libswscale/graph.c:224:static void run_xyz2rgb(const SwsFrame *out, const SwsFrame *in, int y, int h,
libswscale/graph.c:233:static void run_rgb2xyz(const SwsFrame *out, const SwsFrame *in, int y, int h,
libswscale/graph.c:248:static void free_legacy_swscale(void *priv)
libswscale/graph.c:254:static void setup_legacy_swscale(const SwsFrame *out, const SwsFrame *in,
libswscale/graph.c:268:static inline SwsContext *slice_ctx(const SwsPass *pass, int y)
libswscale/graph.c:287:static void run_legacy_unscaled(const SwsFrame *out, const SwsFrame *in,
libswscale/graph.c:299:static void run_legacy_swscale(const SwsFrame *out, const SwsFrame *in,
libswscale/graph.c:311:static void get_chroma_pos(SwsGraph *graph, int *h_chr_pos, int *v_chr_pos,
libswscale/graph.c:354:static void legacy_chr_pos(SwsGraph *graph, int *chr_pos, int override, int *warned)
libswscale/graph.c:370:static int init_legacy_subpass(SwsGraph *graph, SwsContext *sws,
libswscale/graph.c:480:static int add_legacy_sws_pass(SwsGraph *graph, const SwsFormat *src,
libswscale/graph.c:555:static int add_convert_pass(SwsGraph *graph, const SwsFormat *src,
libswscale/graph.c:630:static void free_lut3d(void *priv)
libswscale/graph.c:636:static void setup_lut3d(const SwsFrame *out, const SwsFrame *in, const SwsPass *pass)
libswscale/graph.c:644:static void run_lut3d(const SwsFrame *out, const SwsFrame *in, int y, int h,
libswscale/graph.c:656:static int adapt_colors(SwsGraph *graph, SwsFormat src, SwsFormat dst,
libswscale/graph.c:727:static int init_passes(SwsGraph *graph)
libswscale/graph.c:760:static void sws_graph_worker(void *priv, int jobnr, int threadnr, int nb_jobs,
libswscale/graph.c:771:int ff_sws_graph_create(SwsContext *ctx, const SwsFormat *dst, const SwsFormat *src,
libswscale/graph.c:812:void ff_sws_graph_free(SwsGraph **pgraph)
libswscale/graph.c:834:static int opts_equal(const SwsContext *c1, const SwsContext *c2)
libswscale/graph.c:850:int ff_sws_graph_reinit(SwsContext *ctx, const SwsFormat *dst, const SwsFormat *src,
libswscale/graph.c:866:void ff_sws_graph_update_metadata(SwsGraph *graph, const SwsColor *color)
libswscale/graph.c:874:static void get_field(SwsGraph *graph, const AVFrame *avframe, SwsFrame *frame)
libswscale/graph.c:901:void ff_sws_graph_run(SwsGraph *graph, const AVFrame *dst, const AVFrame *src)
```

### Turn 4  _(tok 7392+194, stop=tool_use)_

**Reasoning:** Line 418 is between 370 (init_legacy_subpass) and 480 (add_legacy_sws_pass), so line 418 is in `init_legacy_subpass`.

Line 710 is between 656 (adapt_colors) and 727 (init_passes) → in `adapt_colors`.

Line 751 is between 727 (init_passes) and 760 → in `init_passes`.

ops_dispatch.c line 349. Let's find enclosing function.


- `read_file(end_line=365, path=libswscale/ops_dispatch.c, start_line=300, version=old)` →

```
libswscale/ops_dispatch.c lines 300-365 of 396
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
```

### Turn 5  _(tok 8668+182, stop=tool_use)_

**Reasoning:** Now check whether ops_dispatch.c has another compile-like function... only one match there.

Also verify that graph.c line 710 and 751 are indeed in adapt_colors and init_passes. Let me read those areas to confirm.

Also double check for any other calls hidden, e.g., in a macro or through a function pointer. Let me grep for "graph_add_pass" broadly (already done — 8 matches total). Also check whether there are calls split across lines like "ff_sws_graph_\nadd_pass". Unlikely. Let me grep "add_pass" to catch variations.


- `grep(pattern=add_pass, version=old, max_results=100)` →

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

### Turn 6  _(tok 8747+200, stop=tool_use, forced)_

**Reasoning:** Enclosing functions:
- graph.c:160 → pass_append
- graph.c:418 → init_legacy_subpass
- graph.c:710 → adapt_colors
- graph.c:751 → init_passes
- ops_dispatch.c:349 → compile

Submit.


- **submit_callers** → `{"callers": [{"function": "pass_append", "file": "libswscale/graph.c"}, {"function": "init_legacy_subpass", "file": "libswscale/graph.c"}, {"function": "adapt_colors", "file": "libswscale/graph.c"}, {"function": "init_passes", "file": "libswscale/graph.c"}, {"function": "compile", "file": "libswscale/ops_dispatch.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2775+145, stop=tool_use)_

**Reasoning:** The user wants me to find all call sites of `ff_sws_graph_add_pass`. Let me start by grepping.


**Says:** 

I'll start by finding all references to this symbol in the repository.




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

- `get_callers(name=ff_sws_graph_add_pass, limit=200)` →

```
{
  "name": "ff_sws_graph_add_pass",
  "version": "old",
  "callers": [
    {
      "caller": "pass_append",
      "file": "libswscale/graph.c",
      "line": 160
    },
    {
      "caller": "init_legacy_subpass",
      "file": "libswscale/graph.c",
      "line": 418
    },
    {
      "caller": "adapt_colors",
      "file": "libswscale/graph.c",
      "line": 710
    },
    {
      "caller": "init_passes",
      "file": "libswscale/graph.c",
      "line": 751
    },
    {
      "caller": "compile",
      "file": "libswscale/ops_dispatch.c",
      "line": 349
    }
  ]
}
```

### Turn 2  _(tok 3444+484, stop=tool_use)_

**Reasoning:** Both tools agree on 5 call sites. Let me verify each enclosing function name by reading the context at each line, to be sure the enclosing function names are right (grep tool may have missed things like a macro wrapping or function pointers). Let me use get_context_at for each site.

Also, check whether there are calls through a function pointer (e.g., assigned to a variable). Let me check graph.h line 159 declaration and any place where the function is passed as a value (without parens). The grep already found all occurrences of the name — 8 total: definition (107), comment (156), prototype (159), and 5 call sites. So there are no other references, including no function-pointer assignments.

Let me verify enclosing functions with get_context_at for each of the 5 lines.


**Says:** 

Both tools agree on 5 call sites. Let me verify each enclosing function name and confirm no indirect uses (function pointers, macro wrappers).







- `get_context_at(file=libswscale/graph.c, line=160, rev=HEAD)` →

```
pass_append — libswscale/graph.c:157 [function] static int pass_append(SwsGraph *graph, enum AVPixelFormat fmt, int w, int h, SwsPass **pass, int align, void *priv, sws_filter_run_t run)
  reads: align, fmt, graph, h, pass, priv, run, w; writes: pass*; returns: return AVERROR(ENOMEM); | return 0;

SLICE around line 160 (def-use, level 2; '>' marks the seed):
static int pass_append(SwsGraph *graph, enum AVPixelFormat fmt, int w, int h, SwsPass **pass, int align, void *priv, sws_filter_run_t run) {
>  SwsPass *new = ff_sws_graph_add_pass(graph, fmt, w, h, *pass, align, priv, run);
   if(!new)
   ...
   *pass = new;
   ...
}

CALLEES (2):
  ff_sws_graph_add_pass (libswscale/graph.c:107): reads align, fmt, graph, height, input, priv, run, width; writes graph*; returns return NULL; | return pass; | return NULL;
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)

CALLERS (3):
  init_legacy_subpass (libswscale/graph.c:403): ret = pass_append(graph, AV_PIX_FMT_RGBA, src_w, src_h, &input, 1, c, run_rgb0);
  init_legacy_subpass (libswscale/graph.c:411): ret = pass_append(graph, AV_PIX_FMT_RGB48, src_w, src_h, &input, 1, c, run_xyz2rgb);
  init_legacy_subpass (libswscale/graph.c:471): ret = pass_append(graph, AV_PIX_FMT_RGB48, dst_w, dst_h, &pass, 1, c, run_rgb2xyz);

TYPES (1):
  AVPixelFormat — libavutil/pixfmt.h:71
    enum AVPixelFormat {
        AV_PIX_FMT_NONE = -1,
        AV_PIX_FMT_YUV420P,   
        AV_PIX_FMT_YUYV422,   
        AV_PIX_FMT_RGB24,     
        AV_PIX_FMT_BGR24,     
        AV_PIX_FMT_YUV422P,   
        AV_PIX_FMT_YUV444P,   
        AV_PIX_FMT_YUV410P,   
        AV_PIX_FMT_YUV411P,   
        AV_PIX_FMT_GRAY8,     
        AV_PIX_FMT_MONOWHITE, 
        AV_PIX_FMT_MONOBLACK, 
        AV_PIX_FMT_PAL8,      
        AV_PIX_FMT_YUVJ420P,  
        AV_PIX_FMT_YUVJ422P,  
        AV_PIX_FMT_YUVJ444P,  
        AV_PIX_FMT_UYVY422,   
        AV_PIX_FMT_UYYVYY411, 
        AV_PIX_FMT_BGR8,      
        AV_PIX_FMT_BGR4,      
        AV_PIX_FMT_BGR4_BYTE, 
        AV_PIX_FMT_RGB8,      
        AV_PIX_FMT_RGB4,      
        AV_PIX_FMT_RGB4_BYTE, 
        AV_PIX_FMT_NV12,      
        AV_PIX_FMT_NV21,      
        AV_PIX_FMT_ARGB,      
        AV_PIX_FMT_RGBA,      
        AV_PIX_FMT_ABGR,      
        AV_PIX_FMT_BGRA,      
        AV_PIX_FMT_GRAY16BE,  
        AV_PIX_FMT_GRAY16LE,  
        AV_PIX_FMT_YUV440P,   
        AV_PIX_FMT_YUVJ440P,  
        AV_PIX_FMT_YUVA420P,  
        AV_PIX_FMT_RGB48BE,   
        AV_PIX_FMT_RGB48LE,   
        AV_PIX_FMT_RGB565BE,  
        AV_PIX_FMT_RGB565LE,  
```

- `get_context_at(file=libswscale/graph.c, line=418, rev=HEAD)` →

```
init_legacy_subpass — libswscale/graph.c:370 [function] static int init_legacy_subpass(SwsGraph *graph, SwsContext *sws, SwsPass *input, SwsPass **output)
  reads: graph, input, output, sws; writes: input*, output*, sws*; returns: return ret; | return ret; | return ret; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM);

SLICE around line 418 (def-use, level 2; '>' marks the seed):
static int init_legacy_subpass(SwsGraph *graph, SwsContext *sws, SwsPass *input, SwsPass **output) {
   SwsInternal *c = sws_internal(sws);
   const int src_w = sws->src_w, src_h = sws->src_h;
   const int dst_w = sws->dst_w, dst_h = sws->dst_h;
   const int unscaled = src_w == dst_w && src_h == dst_h;
   int align = c->dst_slice_align;
   ...
   if(c->cascaded_context[0]) {
   ...
     for(int i = 0;; i < num_cascaded; i++) {
     int i = 0;
   ...
       c->cascaded_context[i] = NULL;
   ...
     }
   }
   if(sws->dither == SWS_DITHER_ED && !c->convert_unscaled)
     align = 0;
   ...
>  pass = ff_sws_graph_add_pass(graph, sws->dst_format, dst_w, dst_h, input, align, sws, c->convert_unscaled ? run_legacy_unscaled : run_legacy_swscale);
   if(!pass) {
   ...
   }
   pass->setup = setup_legacy_swscale;
   pass->free = free_legacy_swscale;
   if(pass->num_slices > 1) {
     c->slice_ctx = av_calloc(pass->num_slices, sizeof(*c->slice_ctx));
     if(!c->slice_ctx)
   ...
     for(int i = 0;; i < pass->num_slices; i++) {
   ...
       slice = c->slice_ctx[i] = sws_alloc_context();
       if(!slice)
   ...
       c->nb_slice_ctx++;
       c2 = sws_internal(slice);
       c2->parent = sws;
       ret = av_opt_copy(slice, sws);
       if(ret < 0)
         return ret;
       ret = ff_sws_init_single_context(slice, NULL, NULL);
       if(ret < 0)
         return ret;
       sws_setColorspaceDetails(slice, c->srcColorspaceTable, slice->src_range, c->dstColorspaceTable, slice->dst_range, c->brightness, c->contrast, c->saturation);
       for(int i = 0;; i < FF_ARRAY_ELEMS(c->srcColorspaceTable); i++) {
       int i = 0;
         c2->srcColorspaceTable[i] = c->srcColorspaceTable[i];
         c2->dstColorspaceTable[i] = c->dstColorspaceTable[i];
       }
     }
   }
   if(c->dstXYZ && !(c->srcXYZ && unscaled)) {
     ret = pass_append(graph, AV_PIX_FMT_RGB48, dst_w, dst_h, &pass, 1, c, run_rgb2xyz);
     if(ret < 0)
       return ret;
   }
   *output = pass;
   ...
}

CALLEES (12):
  sws_internal (libswscale/swscale_internal.h:78): reads sws; writes -; returns return(SwsInternal *)sws;
  sws_free_context (libswscale/utils.c:2328): reads pctx; writes pctx*; returns -
  pass_append (libswscale/graph.c:157): reads align, fmt, graph, h, pass, priv, run, w; writes pass*; returns return AVERROR(ENOMEM); | return 0;
  isALPHA (libswscale/swscale_internal.h:891): reads pix_fmt; writes -; returns return 1; | return desc->flags & AV_PIX_FMT_FLAG_ALPHA;
  ff_sws_graph_add_pass (libswscale/graph.c:107): reads align, fmt, graph, height, input, priv, run, width; writes graph*; returns return NULL; | return pass; | return NULL;
  sws_setColorspaceDetails (libswscale/utils.c:850): reads brightness, contrast, dstRange, inv_table, saturation, srcRange, sws, table; writes sws*; returns return parent_ret; | return ret; | return sws_setColorspaceDetails(c->cascaded_context[c->cascaded_mainindex], inv_table, srcRange, table, dstRange, brightness, contrast, saturation); | return 0; | return ret; | return -1;
  ff_sws_init_single_context (libswscale/utils.c:1122): reads dstFilter, srcFilter, sws; writes sws*; returns return ret; | return AVERROR(EINVAL); | return AVERROR(EINVAL); | return AVERROR(EINVAL); | return AVERROR(EINVAL); | return ret;
  av_opt_copy (libavutil/opt.c:2155): reads dst, src; writes -; returns return AVERROR(EINVAL); | return AVERROR(EINVAL); | return ret;
  sws_alloc_context (libswscale/utils.c:1033): reads -; writes -; returns return NULL; | return &c->opts;
  av_calloc (libavutil/mem.c:264): reads nmemb, size; writes -; returns return NULL; | return av_mallocz(result);
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)
  FF_ARRAY_ELEMS [macro (1 of 3 definitions)]: #define FF_ARRAY_ELEMS(a) (sizeof(a) / sizeof((a)[0]))

CALLERS (1):
  add_legacy_sws_pass (libswscale/graph.c:547): return init_legacy_subpass(graph, sws, input, output);
```

- `get_context_at(file=libswscale/graph.c, line=710, rev=HEAD)` →

```
adapt_colors — libswscale/graph.c:656 [function] static int adapt_colors(SwsGraph *graph, SwsFormat src, SwsFormat dst, SwsPass *input, SwsPass **output)
  reads: dst, graph, input, output, src; writes: dst*, graph*, input*, output*, src*; returns: return 0; | return AVERROR(ENOTSUP); | return AVERROR(ENOMEM); | return ret; | return ret; | return AVERROR(ENOMEM);

SLICE around line 710 (def-use, level 2; '>' marks the seed):
static int adapt_colors(SwsGraph *graph, SwsFormat src, SwsFormat dst, SwsPass *input, SwsPass **output) {
   ...
   SwsLut3D *lut;
   ...
   if(isGray(dst.format)) {
     dst.color = src.color;
   } else if(isGray(src.format)) {
     src.color = dst.color;
   }
   graph->incomplete |= ff_infer_colors(&src.color, &dst.color);
   ...
   lut = ff_sws_lut3d_alloc();
   ...
   fmt_out = ff_sws_lut3d_pick_pixfmt(dst, 1);
   ...
>  pass = ff_sws_graph_add_pass(graph, fmt_out, src.width, src.height, input, 1, lut, run_lut3d);
   if(!pass) {
   ...
   }
   pass->setup = setup_lut3d;
   pass->free = free_lut3d;
   *output = pass;
   ...
}

CALLEES (10):
  isGray (libswscale/swscale_internal.h:800): reads pix_fmt; writes -; returns return !(desc->flags & AV_PIX_FMT_FLAG_PAL)&& !(desc->flags & AV_PIX_FMT_FLAG_HWACCEL)&& desc->nb_components <= 2 && pix_fmt != AV_PIX_FMT_MONOBLACK && pix_fmt != AV_PIX_FMT_MONOWHITE;
  ff_infer_colors (libswscale/format.c:526): reads dst, src; writes -; returns return incomplete;
  ff_sws_color_map_noop (libswscale/cms.c:34): reads map; writes map*; returns return false; | return false; | return ff_prim_superset(&map->dst.gamut, &map->src.gamut)&& av_cmp_q(map->src.max_luma, map->dst.max_luma)<= 0; | return ff_prim_equal(&map->dst.gamut, &map->src.gamut)&& !av_cmp_q(map->src.max_luma, map->dst.max_luma); | return true;
  ff_sws_lut3d_alloc (libswscale/lut3d.c:32): reads -; writes -; returns return NULL; | return lut3d;
  ff_sws_lut3d_pick_pixfmt (libswscale/lut3d.c:52): reads -; writes -; returns return AV_PIX_FMT_RGBA64;
  add_convert_pass (libswscale/graph.c:555 (1 of 2 definitions)): reads dst, graph, input, output, src; writes graph*; returns return AVERROR(ENOMEM); | return add_legacy_sws_pass(graph, src, dst, input, output); | return ret;
  ff_sws_lut3d_generate (libswscale/lut3d.c:211): reads fmt_in, fmt_out, lut3d, map; writes lut3d*, map*; returns return AVERROR(EINVAL); | return ret; | return 0; | return ff_sws_color_map_generate_static(&lut3d->input[0][0][0], INPUT_LUT_SIZE, map);
  ff_sws_lut3d_free (libswscale/lut3d.c:42): reads plut3d; writes -; returns -
  ff_sws_graph_add_pass (libswscale/graph.c:107): reads align, fmt, graph, height, input, priv, run, width; writes graph*; returns return NULL; | return pass; | return NULL;
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)

CALLERS (7):
  generate_slice (libswscale/cms.c:636): ipt = ctx.adapt_colors(&ctx, ipt);
  generate_slice (libswscale/cms.c:665): IPT ipt = ctx.adapt_colors(&ctx, (IPT) { I, P, T });
  ff_sws_color_map_generate_dynamic (libswscale/cms.c:703): case SWS_INTENT_PERCEPTUAL:            ctx.adapt_colors = perceptual; break;
  ff_sws_color_map_generate_dynamic (libswscale/cms.c:704): case SWS_INTENT_RELATIVE_COLORIMETRIC: ctx.adapt_colors = relative;   break;
  ff_sws_color_map_generate_dynamic (libswscale/cms.c:705): case SWS_INTENT_SATURATION:            ctx.adapt_colors = saturation; break;
  ff_sws_color_map_generate_dynamic (libswscale/cms.c:706): case SWS_INTENT_ABSOLUTE_COLORIMETRIC: ctx.adapt_colors = absolute;   break;
  init_passes (libswscale/graph.c:734): ret = adapt_colors(graph, src, dst, pass, &pass);

TYPES (1):
  AVPixelFormat — libavutil/pixfmt.h:71
    enum AVPixelFormat {
        AV_PIX_FMT_NONE = -1,
        AV_PIX_FMT_YUV420P,   
        AV_PIX_FMT_YUYV422,   
        AV_PIX_FMT_RGB24,     
        AV_PIX_FMT_BGR24,     
        AV_PIX_FMT_YUV422P,   
        AV_PIX_FMT_YUV444P,   
        AV_PIX_FMT_YUV410P,   
        AV_PIX_FMT_YUV411P,   
        AV_PIX_FMT_GRAY8,     
        AV_PIX_FMT_MONOWHITE, 
        AV_PIX_FMT_MONOBLACK, 
        AV_PIX_FMT_PAL8,      
        AV_PIX_FMT_YUVJ420P,  
        AV_PIX_FMT_YUVJ422P,  
        AV_PIX_FMT_YUVJ444P,  
        AV_PIX_FMT_UYVY422,   
        AV_PIX_FMT_UYYVYY411, 
        AV_PIX_FMT_BGR8,      
        AV_PIX_FMT_BGR4,      
        AV_PIX_FMT_BGR4_BYTE, 
        AV_PIX_FMT_RGB8,      
        AV_PIX_FMT_RGB4,      
        AV_PIX_FMT_RGB4_BYTE, 
        AV_PIX_FMT_NV12,      
        AV_PIX_FMT_NV21,      
        AV_PIX_FMT_ARGB,      
        AV_PIX_FMT_RGBA,      
        AV_PIX_FMT_ABGR,      
        AV_PIX_FMT_BGRA,      
        AV_PIX_FMT_GRAY16BE,  
        AV_PIX_FMT_GRAY16LE,  
        AV_PIX_FMT_YUV440P,   
        AV_PIX_FMT_YUVJ440P,  
        AV_PIX_FMT_YUVA420P,  
        AV_PIX_FMT_RGB48BE,   
        AV_PIX_FMT_RGB48LE,   
        AV_PIX_FMT_RGB565BE,  
        AV_PIX_FMT_RGB565LE,  
```

- `get_context_at(file=libswscale/graph.c, line=751, rev=HEAD)` →

```
init_passes — libswscale/graph.c:727 [function] static int init_passes(SwsGraph *graph)
  reads: graph; writes: graph*; returns: return ret; | return ret; | return AVERROR(ENOMEM); | return 0;

SLICE around line 751 (def-use, level 2; '>' marks the seed):
static int init_passes(SwsGraph *graph) {
   ...
   SwsFormat dst = graph->dst;
   SwsPass *pass = NULL;
   ...
   if(!pass) {
     graph->noop = 1;
>    pass = ff_sws_graph_add_pass(graph, dst.format, dst.width, dst.height, pass, 1, NULL, run_copy);
     if(!pass)
   ...
   }
}

CALLEES (5):
  adapt_colors (libswscale/graph.c:656): reads dst, graph, input, output, src; writes dst*, graph*, input*, output*, src*; returns return 0; | return AVERROR(ENOTSUP); | return AVERROR(ENOMEM); | return ret; | return ret; | return AVERROR(ENOMEM);
  add_convert_pass (libswscale/graph.c:555 (1 of 2 definitions)): reads dst, graph, input, output, src; writes graph*; returns return AVERROR(ENOMEM); | return add_legacy_sws_pass(graph, src, dst, input, output); | return ret;
  ff_fmt_equal (libswscale/format.h:130): reads fmt1, fmt2; writes -; returns return fmt1->width == fmt2->width && fmt1->height == fmt2->height && ff_props_equal(fmt1, fmt2);
  ff_sws_graph_add_pass (libswscale/graph.c:107): reads align, fmt, graph, height, input, priv, run, width; writes graph*; returns return NULL; | return pass; | return NULL;
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)

CALLERS (1):
  ff_sws_graph_create (libswscale/graph.c:800): ret = init_passes(graph);
```

- `get_context_at(file=libswscale/ops_dispatch.c, line=349, rev=HEAD)` →

```
compile — libswscale/ops_dispatch.c:318 [function] static int compile(SwsGraph *graph, const SwsOpList *ops, const SwsFormat *dst, SwsPass *input, SwsPass **output)
  reads: dst, graph, input, ops, output; writes: output*; returns: return AVERROR(ENOMEM); | return 0; | return ret;

SLICE around line 349 (def-use, level 2; '>' marks the seed):
static int compile(SwsGraph *graph, const SwsOpList *ops, const SwsFormat *dst, SwsPass *input, SwsPass **output) {
   ...
   SwsOpPass *p = av_mallocz(sizeof(*p));
   ...
   const SwsOp *read = ff_sws_op_list_input(ops);
   const SwsOp *write = ff_sws_op_list_output(ops);
   p->planes_in = rw_planes(read);
   p->planes_out = rw_planes(write);
   p->pixel_bits_in = rw_pixel_bits(read);
   p->pixel_bits_out = rw_pixel_bits(write);
   p->exec_base =(SwsOpExec){ .width = dst->width, .height = dst->height, .block_size_in = p->comp.block_size * p->pixel_bits_in >> 3, .block_size_out = p->comp.block_size * p->pixel_bits_out >> 3, };
   for(int i = 0;; i < 4; i++) {
   int i = 0;
     p->idx_in[i] = i < p->planes_in ? ops->order_src.in[i] : -1;
     p->idx_out[i] = i < p->planes_out ? ops->order_dst.in[i] : -1;
   }
   ...
>  pass = ff_sws_graph_add_pass(graph, dst->format, dst->width, dst->height, input, p->comp.slice_align, p, op_pass_run);
   if(!pass) {
   ...
   }
   pass->setup = op_pass_setup;
   pass->free = op_pass_free;
   *output = pass;
   ...
}

CALLEES (9):
  av_mallocz (libavutil/mem.c:256 (1 of 3 definitions)): reads size; writes -; returns return ptr;
  ff_sws_ops_compile (libswscale/ops_dispatch.c:74): reads ctx, ops, out; writes -; returns return 0; | return AVERROR(ENOTSUP);
  ff_sws_op_list_input (libswscale/ops.c:544): reads ops; writes -; returns return NULL; | return read->op == SWS_OP_READ ? read : NULL;
  ff_sws_op_list_output (libswscale/ops.c:553): reads ops; writes -; returns return NULL; | return write->op == SWS_OP_WRITE ? write : NULL;
  rw_planes (libswscale/ops_dispatch.c:304): reads op; writes -; returns return op->rw.packed ? 1 : op->rw.elems;
  rw_pixel_bits (libswscale/ops_dispatch.c:309 (1 of 2 definitions)): reads op; writes -; returns return elems * size * bits;
  ff_sws_graph_add_pass (libswscale/graph.c:107): reads align, fmt, graph, height, input, priv, run, width; writes graph*; returns return NULL; | return pass; | return NULL;
  op_pass_free (libswscale/ops_dispatch.c:96): reads ptr; writes -; returns -
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)

CALLERS (2):
  ff_sws_ops_compile_backend (libswscale/ops_dispatch.c:61): ret = backend->compile(ctx, copy, &compiled);
  ff_sws_compile_pass (libswscale/ops_dispatch.c:394): return compile(graph, ops, dst, input, output);
```

### Turn 3  _(tok 9300+718, stop=tool_use)_

**Reasoning:** All 5 confirmed. Now double-check there are no additional indirect usages — e.g., a macro alias, or the name appearing in a different spelling. The grep found all 8 textual occurrences. Since grep is over all files (git grep), that covers headers and all C files. But could there be calls in files not tracked (e.g., generated)? Unlikely relevant.

Also, one thing: `pass_append` is a wrapper — could there be other wrappers? The grep shows all. Also check whether the declaration in graph.h at line 159 is a prototype only (yes).

Let me also double check the definition at line 107 in graph.c is indeed the definition, and that there is only one definition (no other file defining it). Yes.

One more consideration: is there any place calling via a function pointer stored, e.g., `graph_add_pass` alias? grep covers exact name; a macro alias like `#define add_pass ff_sws_graph_add_pass` would show up in grep too. All 8 occurrences are accounted for: 1 definition, 1 comment, 1 prototype, 5 calls.

So the answer: 5 callers.

Files: libswscale/graph.c (pass_append, init_legacy_subpass, adapt_colors, init_passes) and libswscale/ops_dispatch.c (compile).

Note: adapt_colors also exists as a function pointer member in cms.c (ctx.adapt_colors) — but that's a different thing; the callers listed there are for the cms context field. Irrelevant here — the call site in graph.c's adapt_colors is what matters.

Also `compile` in ops_dispatch.c — there may be multiple `compile` functions (e.g., backend->compile is a function pointer field). The one containing line 349 is `compile` in ops_dispatch.c. Good.

Submit with high confidence.


**Says:** 

All 5 call sites verified. The grep found exactly 8 textual occurrences of the symbol: the definition (graph.c:107), a comment (graph.c:156), the prototype (graph.h:159), and 5 real call sites — so there are no indirect/function-pointer uses or macro aliases to worry about.

| Enclosing function | File | Call site |
|---|---|---|
| `pass_append` | libswscale/graph.c | 160 |
| `init_legacy_subpass` | libswscale/graph.c | 418 |
| `adapt_colors` | libswscale/graph.c | 710 |
| `init_passes` | libswscale/graph.c | 751 |
| `compile` | libswscale/ops_dispatch.c | 349 |



- **submit_callers** → `{"callers": [{"function": "pass_append", "file": "libswscale/graph.c"}, {"function": "init_legacy_subpass", "file": "libswscale/graph.c"}, {"function": "adapt_colors", "file": "libswscale/graph.c"}, {"function": "init_passes", "file": "libswscale/graph.c"}, {"function": "compile", "file": "libswscale/ops_dispatch.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2352+104, stop=tool_use)_

**Reasoning:** Let me find callers of ff_sws_graph_add_pass.


**Says:** 

I'll start by resolving the symbol and finding its callers.




- `resolve_symbol(name=ff_sws_graph_add_pass)` →

```
{
  "resolved": true,
  "name": "ff_sws_graph_add_pass",
  "version": "old",
  "file": "libswscale/graph.c",
  "line": 107,
  "kind": "function",
  "signature": "SwsPass *ff_sws_graph_add_pass(SwsGraph *graph, enum AVPixelFormat fmt, int width, int height, SwsPass *input, int align, void *priv, sws_filter_run_t run)",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

- `get_callers(name=ff_sws_graph_add_pass, limit=100)` →

```
{
  "name": "ff_sws_graph_add_pass",
  "version": "old",
  "callers": [
    {
      "caller": "pass_append",
      "file": "libswscale/graph.c",
      "line": 160
    },
    {
      "caller": "init_legacy_subpass",
      "file": "libswscale/graph.c",
      "line": 418
    },
    {
      "caller": "adapt_colors",
      "file": "libswscale/graph.c",
      "line": 710
    },
    {
      "caller": "init_passes",
      "file": "libswscale/graph.c",
      "line": 751
    },
    {
      "caller": "compile",
      "file": "libswscale/ops_dispatch.c",
      "line": 349
    }
  ]
}
```

### Turn 2  _(tok 2837+95, stop=tool_use)_

**Reasoning:** Let me verify by expanding the function and checking neighborhood. Also, some callers might be macro-wrapped or in headers. Let me check the neighborhood.


- `expand_function(name=ff_sws_graph_add_pass)` →

```
{
  "name": "ff_sws_graph_add_pass",
  "version": "old",
  "levels": 1,
  "node": {
    "name": "ff_sws_graph_add_pass",
    "file": "libswscale/graph.c",
    "line": 107,
    "kind": "function",
    "state": "analyzed"
  },
  "callees": [
    {
      "name": "av_mallocz",
      "file": "libavutil/mem.c",
      "line": 256,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        112
      ]
    },
    {
      "name": "av_refstruct_alloc_ext",
      "file": "libavutil/refstruct.h",
      "line": 93,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        123
      ]
    },
    {
      "name": "pass_alloc_output",
      "file": "libswscale/graph.c",
      "line": 77,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        127
      ]
    },
    {
      "name": "FFALIGN",
      "file": "libavutil/macros.h",
      "line": 78,
      "kind": "macro",
      "state": "summarized",
      "call_lines": [
        136
      ]
    },
    {
      "name": "av_dynarray_add_nofree",
      "file": "libavutil/mem.c",
      "line": 315,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        144
      ]
    },
    {
      "name": "av_refstruct_unref",
      "file": "libavutil/refstruct.c",
      "line": 120,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        151
      ]
    },
    {
      "name": "av_free",
      "file": "libavutil/mem.c",
      "line": 238,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        152
      ]
    }
  ],
  "callers": [
    {
      "name": "pass_append",
      "file": "libswscale/graph.c",
      "line": 157,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        160
      ]
    },
    {
      "name": "init_legacy_subpass",
      "file": "libswscale/graph.c",
      "line": 370,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        418
      ]
    },
    {
      "name": "adapt_colors",
      "file": "libswscale/graph.c",
      "line": 656,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        710
      ]
    },
    {
      "name": "init_passes",
      "file": "libswscale/graph.c",
      "line": 727,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        751
      ]
    },
    {
      "name": "compile",
      "file": "libswscale/ops_dispatch.c",
      "line": 318,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        349
      ]
    }
  ]
}
```

- `get_neighborhood(name=ff_sws_graph_add_pass)` →

```
ff_sws_graph_add_pass — libswscale/graph.c:107 [function] SwsPass *ff_sws_graph_add_pass(SwsGraph *graph, enum AVPixelFormat fmt, int width, int height, SwsPass *input, int align, void *priv, sws_filter_run_t run)
  reads: align, fmt, graph, height, input, priv, run, width; writes: graph*; returns: return NULL; | return pass; | return NULL;

CALLEES (7):
  av_mallocz (libavutil/mem.c:256 (1 of 3 definitions)): reads size; writes -; returns return ptr;
  av_refstruct_alloc_ext (libavutil/refstruct.h:93): reads flags, opaque, size; writes -; returns return av_refstruct_alloc_ext_c(size, flags, (AVRefStructOpaque){.nc = opaque}, free_cb);
  pass_alloc_output (libswscale/graph.c:77): reads pass; writes pass*; returns return 0; | return AVERROR(ENOMEM); | return ret; | return 0;
  av_dynarray_add_nofree (libavutil/mem.c:315): reads elem, nb_ptr, tab_ptr; writes tab_ptr*; returns return AVERROR(ENOMEM); | return 0;
  av_refstruct_unref (libavutil/refstruct.c:120): reads objp; writes objp*; returns -
  av_free (libavutil/mem.c:238 (1 of 3 definitions)): reads ptr; writes -; returns -
  FFALIGN [macro]: #define FFALIGN(x, a) (((x)+(a)-1)&~((a)-1))

CALLERS (5):
  pass_append (libswscale/graph.c:160): SwsPass *new = ff_sws_graph_add_pass(graph, fmt, w, h, *pass, align, priv, run);
  init_legacy_subpass (libswscale/graph.c:418): pass = ff_sws_graph_add_pass(graph, sws->dst_format, dst_w, dst_h, input, align, sws,
  adapt_colors (libswscale/graph.c:710): pass = ff_sws_graph_add_pass(graph, fmt_out, src.width, src.height,
  init_passes (libswscale/graph.c:751): pass = ff_sws_graph_add_pass(graph, dst.format, dst.width, dst.height,
  compile (libswscale/ops_dispatch.c:349): pass = ff_sws_graph_add_pass(graph, dst->format, dst->width, dst->height,

TYPES (1):
  AVPixelFormat — libavutil/pixfmt.h:71
    enum AVPixelFormat {
        AV_PIX_FMT_NONE = -1,
        AV_PIX_FMT_YUV420P,   
        AV_PIX_FMT_YUYV422,   
        AV_PIX_FMT_RGB24,     
        AV_PIX_FMT_BGR24,     
        AV_PIX_FMT_YUV422P,   
        AV_PIX_FMT_YUV444P,   
        AV_PIX_FMT_YUV410P,   
        AV_PIX_FMT_YUV411P,   
        AV_PIX_FMT_GRAY8,     
        AV_PIX_FMT_MONOWHITE, 
        AV_PIX_FMT_MONOBLACK, 
        AV_PIX_FMT_PAL8,      
        AV_PIX_FMT_YUVJ420P,  
        AV_PIX_FMT_YUVJ422P,  
        AV_PIX_FMT_YUVJ444P,  
        AV_PIX_FMT_UYVY422,   
        AV_PIX_FMT_UYYVYY411, 
        AV_PIX_FMT_BGR8,      
        AV_PIX_FMT_BGR4,      
        AV_PIX_FMT_BGR4_BYTE, 
        AV_PIX_FMT_RGB8,      
        AV_PIX_FMT_RGB4,      
        AV_PIX_FMT_RGB4_BYTE, 
        AV_PIX_FMT_NV12,      
        AV_PIX_FMT_NV21,      
        AV_PIX_FMT_ARGB,      
        AV_PIX_FMT_RGBA,      
        AV_PIX_FMT_ABGR,      
        AV_PIX_FMT_BGRA,      
        AV_PIX_FMT_GRAY16BE,  
        AV_PIX_FMT_GRAY16LE,  
        AV_PIX_FMT_YUV440P,   
        AV_PIX_FMT_YUVJ440P,  
        AV_PIX_FMT_YUVA420P,  
        AV_PIX_FMT_RGB48BE,   
        AV_PIX_FMT_RGB48LE,   
        AV_PIX_FMT_RGB565BE,  
        AV_PIX_FMT_RGB565LE,  
```

### Turn 3  _(tok 4932+334, stop=tool_use)_

**Reasoning:** Both sources agree: 5 callers. Let me also check if there are any function-pointer usages or macro wrappers, e.g., something that aliases it. Also check whether pass_append's callers matter — no, we only need direct callers.

One thing to check: is there a header declaring it, and could there be indirect calls via function pointers? Let's check the header declaration and see if the symbol is assigned anywhere. There's no grep tool. But let's check resolve_symbol for related things. Actually the neighborhood listing is derived from the call graph, which should be complete for direct calls.

Let me double-check the `compile` function in ops_dispatch.c — is it a real function or something else? Let's verify with get_context_at for line 349 of ops_dispatch.c, and also verify pass_append etc. Actually, more valuable: check whether there's a possibility that `compile` is a static function inside a macro or that ops_dispatch.c contains multiple definitions. Let me quickly check the context at those lines.

Also, could there be calls in files that aren't indexed (e.g., template files included multiple times like graph_template.c)? gtags should still find them. Let's verify the context at ops_dispatch.c:349.


- `get_context_at(file=libswscale/ops_dispatch.c, line=349)` →

```
compile — libswscale/ops_dispatch.c:318 [function] static int compile(SwsGraph *graph, const SwsOpList *ops, const SwsFormat *dst, SwsPass *input, SwsPass **output)
  reads: dst, graph, input, ops, output; writes: output*; returns: return AVERROR(ENOMEM); | return 0; | return ret;

SLICE around line 349 (def-use, level 2; '>' marks the seed):
static int compile(SwsGraph *graph, const SwsOpList *ops, const SwsFormat *dst, SwsPass *input, SwsPass **output) {
   ...
   SwsOpPass *p = av_mallocz(sizeof(*p));
   ...
   const SwsOp *read = ff_sws_op_list_input(ops);
   const SwsOp *write = ff_sws_op_list_output(ops);
   p->planes_in = rw_planes(read);
   p->planes_out = rw_planes(write);
   p->pixel_bits_in = rw_pixel_bits(read);
   p->pixel_bits_out = rw_pixel_bits(write);
   p->exec_base =(SwsOpExec){ .width = dst->width, .height = dst->height, .block_size_in = p->comp.block_size * p->pixel_bits_in >> 3, .block_size_out = p->comp.block_size * p->pixel_bits_out >> 3, };
   for(int i = 0;; i < 4; i++) {
   int i = 0;
     p->idx_in[i] = i < p->planes_in ? ops->order_src.in[i] : -1;
     p->idx_out[i] = i < p->planes_out ? ops->order_dst.in[i] : -1;
   }
   ...
>  pass = ff_sws_graph_add_pass(graph, dst->format, dst->width, dst->height, input, p->comp.slice_align, p, op_pass_run);
   if(!pass) {
   ...
   }
   pass->setup = op_pass_setup;
   pass->free = op_pass_free;
   *output = pass;
   ...
}

CALLEES (9):
  av_mallocz (libavutil/mem.c:256 (1 of 3 definitions)): reads size; writes -; returns return ptr;
  ff_sws_ops_compile (libswscale/ops_dispatch.c:74): reads ctx, ops, out; writes -; returns return 0; | return AVERROR(ENOTSUP);
  ff_sws_op_list_input (libswscale/ops.c:544): reads ops; writes -; returns return NULL; | return read->op == SWS_OP_READ ? read : NULL;
  ff_sws_op_list_output (libswscale/ops.c:553): reads ops; writes -; returns return NULL; | return write->op == SWS_OP_WRITE ? write : NULL;
  rw_planes (libswscale/ops_dispatch.c:304): reads op; writes -; returns return op->rw.packed ? 1 : op->rw.elems;
  rw_pixel_bits (libswscale/ops_dispatch.c:309 (1 of 2 definitions)): reads op; writes -; returns return elems * size * bits;
  ff_sws_graph_add_pass (libswscale/graph.c:107): reads align, fmt, graph, height, input, priv, run, width; writes graph*; returns return NULL; | return pass; | return NULL;
  op_pass_free (libswscale/ops_dispatch.c:96): reads ptr; writes -; returns -
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)

CALLERS (2):
  ff_sws_ops_compile_backend (libswscale/ops_dispatch.c:61): ret = backend->compile(ctx, copy, &compiled);
  ff_sws_compile_pass (libswscale/ops_dispatch.c:394): return compile(graph, ops, dst, input, output);
```

- `resolve_symbol(name=compile)` →

```
{
  "resolved": true,
  "name": "compile",
  "version": "old",
  "file": "libswscale/ops_dispatch.c",
  "line": 318,
  "kind": "function",
  "signature": "static int compile(SwsGraph *graph, const SwsOpList *ops, const SwsFormat *dst, SwsPass *input, SwsPass **output)",
  "resolution_method": "location",
  "ambiguous": false
}
```

### Turn 4  _(tok 6322+227, stop=tool_use)_

**Reasoning:** Good, unambiguous. Both tools consistently report 5 callers.

Let me double check whether there might be additional callers hidden — e.g., in a file not indexed like `libswscale/graph.h` inline function, or a macro wrapper. Let me check the header declaration location and see if any wrapper macro exists. I could try resolve_symbol on something like "sws_graph_add_pass" — not useful.

An alternative: check whether the call graph captured all files. The tool reports limit 100 and only 5 results, so presumably complete.

I'm reasonably confident. Let me also quickly sanity-check that pass_append, init_legacy_subpass, adapt_colors, init_passes are indeed function definitions (not macros). They're reported as functions in graph.c.

Submit.


**Says:** 

Both the callers query and the call-graph expansion agree on the same set of direct call sites. Let me verify the remaining four are real function definitions in `graph.c`.



- `resolve_symbol(name=pass_append)` →

```
{
  "resolved": true,
  "name": "pass_append",
  "version": "old",
  "file": "libswscale/graph.c",
  "line": 157,
  "kind": "function",
  "signature": "static int pass_append(SwsGraph *graph, enum AVPixelFormat fmt, int w, int h, SwsPass **pass, int align, void *priv, sws_filter_run_t run)",
  "resolution_method": "location",
  "ambiguous": false
}
```

### Turn 5  _(tok 6683+291, stop=tool_use)_

**Reasoning:** Confirmed. All 5 callers verified. Submit.


**Says:** 

All five call sites are verified as real function definitions with actual invocations of `ff_sws_graph_add_pass`:

| Caller | File | Call line |
|---|---|---|
| `pass_append` | `libswscale/graph.c` | 160 |
| `init_legacy_subpass` | `libswscale/graph.c` | 418 |
| `adapt_colors` | `libswscale/graph.c` | 710 |
| `init_passes` | `libswscale/graph.c` | 751 |
| `compile` | `libswscale/ops_dispatch.c` | 349 |



- **submit_callers** → `{"callers": [{"function": "pass_append", "file": "libswscale/graph.c"}, {"function": "init_legacy_subpass", "file": "libswscale/graph.c"}, {"function": "adapt_colors", "file": "libswscale/graph.c"}, {"function": "init_passes", "file": "libswscale/graph.c"}, {"function": "compile", "file": "libswscale/ops_dispatch.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

