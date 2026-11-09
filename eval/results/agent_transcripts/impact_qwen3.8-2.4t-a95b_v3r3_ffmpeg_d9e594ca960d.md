# Impact-analysis transcript — ffmpeg @ d9e594ca960d — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_sws_graph_add_pass` (libswscale/graph.c), arity 8->9
- truth: [['libswscale/graph.c', 'adapt_colors'], ['libswscale/graph.c', 'init_legacy_subpass'], ['libswscale/graph.c', 'init_passes'], ['libswscale/graph.c', 'pass_append'], ['libswscale/ops_dispatch.c', 'compile']]

## Self-navigation arm

### Turn 1  _(tok 946+132, stop=tool_use)_

**Reasoning:** Let me start by exploring the repository to find the function definition and all call sites.


**Says:** 

I'll start by exploring the repository structure and finding the target function.




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

- `list_files(version=old, pattern=libswscale)` →

```
136 files
doc/libswscale.texi	1531
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
tests/fate/libswscale.mak	2797
```

### Turn 2  _(tok 3490+159, stop=tool_use)_

**Reasoning:** Now, let's read the graph.c file around those lines to determine the enclosing function names.


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

### Turn 3  _(tok 6457+107, stop=tool_use)_

**Reasoning:** I need the enclosing function name for line 418. Let me search backwards for the function definition. Let me read lines 320-390.


- `read_file(end_line=380, path=libswscale/graph.c, start_line=300, version=old)` →

```
libswscale/graph.c lines 300-380 of 925
  300|                                int y, int h, const SwsPass *pass)
  301| {
  302|     SwsContext *sws = slice_ctx(pass, y);
  303|     SwsInternal *c = sws_internal(sws);
  304|     uint8_t *out_data[4];
  305|     frame_shift(out, y, out_data);
  306| 
  307|     ff_swscale(c, (const uint8_t *const *) in->data, in->linesize, 0,
  308|                sws->src_h, out_data, out->linesize, y, h);
  309| }
  310| 
  311| static void get_chroma_pos(SwsGraph *graph, int *h_chr_pos, int *v_chr_pos,
  312|                            const SwsFormat *fmt)
  313| {
  314|     enum AVChromaLocation chroma_loc = fmt->loc;
  315|     const int sub_x = fmt->desc->log2_chroma_w;
  316|     const int sub_y = fmt->desc->log2_chroma_h;
  317|     int x_pos, y_pos;
  318| 
  319|     /* Explicitly default to center siting for compatibility with swscale */
  320|     if (chroma_loc == AVCHROMA_LOC_UNSPECIFIED) {
  321|         chroma_loc = AVCHROMA_LOC_CENTER;
  322|         graph->incomplete |= sub_x || sub_y;
  323|     }
  324| 
  325|     /* av_chroma_location_enum_to_pos() always gives us values in the range from
  326|      * 0 to 256, but we need to adjust this to the true value range of the
  327|      * subsampling grid, which may be larger for h/v_sub > 1 */
  328|     av_chroma_location_enum_to_pos(&x_pos, &y_pos, chroma_loc);
  329|     x_pos *= (1 << sub_x) - 1;
  330|     y_pos *= (1 << sub_y) - 1;
  331| 
  332|     /* Fix vertical chroma position for interlaced frames */
  333|     if (sub_y && fmt->interlaced) {
  334|         /* When vertically subsampling, chroma samples are effectively only
  335|          * placed next to even rows. To access them from the odd field, we need
  336|          * to account for this shift by offsetting the distance of one luma row.
  337|          *
  338|          * For 4x vertical subsampling (v_sub == 2), they are only placed
  339|          * next to every *other* even row, so we need to shift by three luma
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
```

### Turn 4  _(tok 8023+110, stop=tool_use)_

**Reasoning:** So line 418 is inside `init_legacy_subpass` in libswscale/graph.c.

Now let's look at lines 710 and 751.


- `read_file(end_line=790, path=libswscale/graph.c, start_line=640, version=old)` →

```
libswscale/graph.c lines 640-790 of 925
  640|     /* Update dynamic frame metadata from the original source frame */
  641|     ff_sws_lut3d_update(lut, &pass->graph->src.color);
  642| }
  643| 
  644| static void run_lut3d(const SwsFrame *out, const SwsFrame *in, int y, int h,
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
  781|     graph->dst = *dst;
  782|     graph->field = field;
  783|     graph->opts_copy = *ctx;
  784| 
  785|     if (ctx->threads == 1) {
  786|         graph->num_threads = 1;
  787|     } else {
  788|         ret = avpriv_slicethread_create(&graph->slicethread, (void *) graph,
  789|                                         sws_graph_worker, NULL, ctx->threads);
  790|         if (ret == AVERROR(ENOSYS)) {
```

### Turn 5  _(tok 10468+91, stop=tool_use)_

**Reasoning:** Now the ops_dispatch.c line 349. Let me read around it.


- `read_file(end_line=380, path=libswscale/ops_dispatch.c, start_line=280, version=old)` →

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

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 11865+279, stop=tool_use, forced)_

**Reasoning:** I found the callers:
1. `pass_append` in libswscale/graph.c (line 160)
2. `init_legacy_subpass` in libswscale/graph.c (line 418)
3. `adapt_colors` in libswscale/graph.c (line 710)
4. `init_passes` in libswscale/graph.c (line 751)
5. `compile` in libswscale/ops_dispatch.c (line 349)

The prototype in graph.h line 159 and definition at graph.c line 107 and comment at line 156 are excluded.

Submit.


- **submit_callers** → `{"callers": [{"function": "pass_append", "file": "libswscale/graph.c"}, {"function": "init_legacy_subpass", "file": "libswscale/graph.c"}, {"function": "adapt_colors", "file": "libswscale/graph.c"}, {"function": "init_passes", "file": "libswscale/graph.c"}, {"function": "compile", "file": "libswscale/ops_dispatch.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2775+198, stop=tool_use)_

**Reasoning:** The user wants a list of all functions that call `ff_sws_graph_add_pass`. Let me search the repository.

Note: libswscale is part of FFmpeg. But `ff_sws_graph_add_pass` — hmm, in FFmpeg there's `ff_sws_graph_add_pass`? Let me search.

Let me use grep first.


**Says:** 

I'll search for all references to `ff_sws_graph_add_pass` in the repository.




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

### Turn 2  _(tok 3497+429, stop=tool_use)_

**Reasoning:** Now I need to verify the enclosing function names. The `compile` in ops_dispatch.c might be a static function within a struct or similar. Let me check each call site with get_context_at to confirm the enclosing function names.

Note: grep showed only 8 matches, but there may be calls through macro wrappers or via a function pointer. Let me check whether `ff_sws_graph_add_pass` is assigned to a function pointer anywhere — the grep covered all occurrences of the name, and only 8 lines. Line 107 is the definition, 159 in graph.h is the prototype, 156 is a comment. So call sites: 160, 418, 710, 751 in graph.c, and 349 in ops_dispatch.c. That's 5 call sites.

But wait — maybe the call sites are within a macro that gets expanded, or maybe there's a wrapper macro like `graph_add_pass(...)`. Let me check line 156-165 in graph.c to see the wrapper and whether there's a macro alias.

Also need to check for possible indirect usage, e.g., `#define add_pass ff_sws_graph_add_pass`. The grep for the exact string covered that. But maybe there's something like a wrapper function `pass_append` used elsewhere — those aren't calls to ff_sws_graph_add_pass directly, so they don't need updating.

Let me verify the enclosing functions.


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
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (-(e)) ///< Returns a negative error code from a POSIX error code, to return from library functions.

CALLERS (2):
  ff_sws_ops_compile_backend (libswscale/ops_dispatch.c:61): ret = backend->compile(ctx, copy, &compiled);
  ff_sws_compile_pass (libswscale/ops_dispatch.c:394): return compile(graph, ops, dst, input, output);
```

- `read_file(path=libswscale/graph.c, start_line=100, end_line=175, version=old)` →

```
libswscale/graph.c lines 100-175 of 925
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
```

### Turn 3  _(tok 6066+132, stop=tool_use)_

**Reasoning:** Now verify the other three call sites' enclosing functions in graph.c: lines 418, 710, 751. Let me use get_context_at for each. Actually, get_callers already gave the names, but I want to double-check that these are the correct enclosing function names (e.g., nested functions or the call might be inside a lambda/macro). Let me check them quickly.


- `get_context_at(file=libswscale/graph.c, line=418)` →

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
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (-(e)) ///< Returns a negative error code from a POSIX error code, to return from library functions.
  FF_ARRAY_ELEMS [macro (1 of 3 definitions)]: #define FF_ARRAY_ELEMS(a) (sizeof(a) / sizeof((a)[0]))

CALLERS (1):
  add_legacy_sws_pass (libswscale/graph.c:547): return init_legacy_subpass(graph, sws, input, output);
```

### Turn 4  _(tok 7651+184, stop=tool_use)_

**Reasoning:** Now check lines 710 and 751 enclosing functions.

Also I should double-check whether there might be calls in other files that use a different spelling, e.g., via a macro alias defined in graph.h. Let me look at graph.h around line 159 to see if there's a macro wrapper.

Also check whether any call sites exist in tests (e.g., libswscale/tests/) — grep covered whole repo, so no.

Let me also make sure grep is case-sensitive and complete — 8 matches found, max_results 200, so complete.

Let me verify 710 and 751.


- `get_context_at(file=libswscale/graph.c, line=710)` →

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
  ff_sws_lut3d_generate (libswscale/lut3d.c:211): reads fmt_in, fmt_out, lut3d, map; writes lut3d*, map*; returns return AVERROR(EINVAL); | return ret; | return 0; | return ff_sws_color_map_generate_static(&lut3d->input[0][0][0], INPUT_LUT_SIZE, map);
  ff_sws_lut3d_free (libswscale/lut3d.c:42): reads plut3d; writes -; returns -
  ff_sws_graph_add_pass (libswscale/graph.c:107): reads align, fmt, graph, height, input, priv, run, width; writes graph*; returns return NULL; | return pass; | return NULL;
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (-(e)) ///< Returns a negative error code from a POSIX error code, to return from library functions.
  add_convert_pass [macro (1 of 2 definitions)]: #define add_convert_pass add_legacy_sws_pass

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

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 7260+179, stop=tool_use, forced)_

**Reasoning:** I have verified 4 of 5; the last one (init_passes at 751) is confirmed by get_callers and also referenced as init_passes in adapt_colors' callers list. Submit.


- **submit_callers** → `{"callers": [{"function": "pass_append", "file": "libswscale/graph.c"}, {"function": "init_legacy_subpass", "file": "libswscale/graph.c"}, {"function": "adapt_colors", "file": "libswscale/graph.c"}, {"function": "init_passes", "file": "libswscale/graph.c"}, {"function": "compile", "file": "libswscale/ops_dispatch.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2352+132, stop=tool_use)_

**Reasoning:** The task: list every function that calls `ff_sws_graph_add_pass`. Let me use get_callers with a high limit.

Let me start with get_callers.


**Says:** 

I'll start by finding all callers of `ff_sws_graph_add_pass`.




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

### Turn 2  _(tok 2865+127, stop=tool_use)_

**Reasoning:** Now let's verify each caller site. Let me get the neighborhoods / context at each call site to confirm the enclosing function names and check for possible mis-attribution (e.g., call at line 160 inside `pass_append`, but maybe inside a nested static function or macro).

Let me call get_context_at for each site.


**Says:** 

Let me verify each call site and its enclosing function.



- `get_context_at(file=libswscale/graph.c, line=160)` →

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
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (-(e)) ///< Returns a negative error code from a POSIX error code, to return from library functions.

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

### Turn 3  _(tok 3883+121, stop=tool_use)_

**Reasoning:** Now check the other sites: 418, 710, 751 in graph.c, and 349 in ops_dispatch.c.

Also note: pass_append is a wrapper — but the task asks only for direct callers of ff_sws_graph_add_pass. So pass_append counts.

Let me check the remaining sites in parallel.


- `get_context_at(file=libswscale/graph.c, line=418)` →

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
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (-(e)) ///< Returns a negative error code from a POSIX error code, to return from library functions.
  FF_ARRAY_ELEMS [macro (1 of 3 definitions)]: #define FF_ARRAY_ELEMS(a) (sizeof(a) / sizeof((a)[0]))

CALLERS (1):
  add_legacy_sws_pass (libswscale/graph.c:547): return init_legacy_subpass(graph, sws, input, output);
```

### Turn 4  _(tok 5457+171, stop=tool_use)_

**Reasoning:** Confirmed. Now check lines 710 and 751 in graph.c, and 349 in ops_dispatch.c.

Note: line numbers may differ between "old" and "work" versions. get_context_at with no rev defaults to... The tool description says version: "work" default? Actually the parameter `rev` defaults to the server's commit else HEAD. Hmm, the returned version says "old" for get_callers. Interesting — get_callers returned version "old". That may be the server default. Let's just proceed consistently.

Let me check the remaining sites.


- `get_context_at(file=libswscale/graph.c, line=710)` →

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
  ff_sws_lut3d_generate (libswscale/lut3d.c:211): reads fmt_in, fmt_out, lut3d, map; writes lut3d*, map*; returns return AVERROR(EINVAL); | return ret; | return 0; | return ff_sws_color_map_generate_static(&lut3d->input[0][0][0], INPUT_LUT_SIZE, map);
  ff_sws_lut3d_free (libswscale/lut3d.c:42): reads plut3d; writes -; returns -
  ff_sws_graph_add_pass (libswscale/graph.c:107): reads align, fmt, graph, height, input, priv, run, width; writes graph*; returns return NULL; | return pass; | return NULL;
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (-(e)) ///< Returns a negative error code from a POSIX error code, to return from library functions.
  add_convert_pass [macro (1 of 2 definitions)]: #define add_convert_pass add_legacy_sws_pass

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

### Turn 5  _(tok 7239+105, stop=tool_use)_

**Reasoning:** Note: there's another `adapt_colors` in cms.c (as a function pointer field named adapt_colors). The call at graph.c:710 is in graph.c's adapt_colors. Fine.

Now check graph.c:751 and ops_dispatch.c:349.


- `get_context_at(file=libswscale/graph.c, line=751)` →

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
  ff_fmt_equal (libswscale/format.h:130): reads fmt1, fmt2; writes -; returns return fmt1->width == fmt2->width && fmt1->height == fmt2->height && ff_props_equal(fmt1, fmt2);
  ff_sws_graph_add_pass (libswscale/graph.c:107): reads align, fmt, graph, height, input, priv, run, width; writes graph*; returns return NULL; | return pass; | return NULL;
  add_convert_pass [macro (1 of 2 definitions)]: #define add_convert_pass add_legacy_sws_pass
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (-(e)) ///< Returns a negative error code from a POSIX error code, to return from library functions.

CALLERS (1):
  ff_sws_graph_create (libswscale/graph.c:800): ret = init_passes(graph);
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 6058+220, stop=tool_use, forced)_

**Reasoning:** I haven't verified ops_dispatch.c:349 `compile`, but get_callers reported it. I'll include it. Note that `compile` in ops_dispatch.c might actually be a different `compile` — but the report is from the tool. Include all 5.

Confidence: high-ish. I verified 4 of 5 sites. The fifth is from the index. I'll say high.


- **submit_callers** → `{"callers": [{"function": "pass_append", "file": "libswscale/graph.c"}, {"function": "init_legacy_subpass", "file": "libswscale/graph.c"}, {"function": "adapt_colors", "file": "libswscale/graph.c"}, {"function": "init_passes", "file": "libswscale/graph.c"}, {"function": "compile", "file": "libswscale/ops_dispatch.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

