# Impact-analysis transcript — ffmpeg @ 75914b582280 — openrouter:deepseek/deepseek-v4-pro

- target: `ff_hevc_frame_nb_refs` (libavcodec/hevc/refs.c), arity 2->3
- truth: [['libavcodec/hevc/hevcdec.c', 'hls_slice_header'], ['libavcodec/nvdec_hevc.c', 'nvdec_hevc_start_frame'], ['libavcodec/vdpau_hevc.c', 'vdpau_hevc_start_frame']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1037+76, stop=tool_use)_

**Reasoning:** Let me find all callers of `ff_hevc_frame_nb_refs` in the repository

- `find_references(name=ff_hevc_frame_nb_refs)` →

```
4 references
ff_hevc_frame_nb_refs  787 libavcodec/hevc/hevcdec.c             nb_refs = ff_hevc_frame_nb_refs(sh, pps);
ff_hevc_frame_nb_refs  618 libavcodec/hevc/hevcdec.h int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
ff_hevc_frame_nb_refs  191 libavcodec/nvdec_hevc.c             .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
ff_hevc_frame_nb_refs  209 libavcodec/vdpau_hevc.c     info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

### Turn 2  _(tok 1310+413, stop=tool_use)_

**Reasoning:** Let me analyze the results:

1. `libavcodec/hevc/hevcdec.c` line 787 - I need to find the enclosing function
2. `libavcodec/hevc/hevcdec.h` line 618 - This is the prototype/declaration, not a call site
3. `libavcodec/nvdec_hevc.c` line 191 - I need to find the enclosing function
4. `libavcodec/vdpau_hevc.c` line 209 - I need to find the enclosing function

Let me look at the enclosing functions for each call site.

- `read_file(path=libavcodec/hevc/hevcdec.c, start_line=780, end_line=800, version=old)` →

```
libavcodec/hevc/hevcdec.c lines 780-800 of 3844
  780|                 av_log(s->avctx, AV_LOG_ERROR, "Too many refs: %d/%d.\n",
  781|                        sh->nb_refs[L0], sh->nb_refs[L1]);
  782|                 return AVERROR_INVALIDDATA;
  783|             }
  784| 
  785|             sh->rpl_modification_flag[0] = 0;
  786|             sh->rpl_modification_flag[1] = 0;
  787|             nb_refs = ff_hevc_frame_nb_refs(sh, pps);
  788|             if (!nb_refs) {
  789|                 av_log(s->avctx, AV_LOG_ERROR, "Zero refs for a frame with P or B slices.\n");
  790|                 return AVERROR_INVALIDDATA;
  791|             }
  792| 
  793|             if (pps->lists_modification_present_flag && nb_refs > 1) {
  794|                 sh->rpl_modification_flag[0] = get_bits1(gb);
  795|                 if (sh->rpl_modification_flag[0]) {
  796|                     for (i = 0; i < sh->nb_refs[L0]; i++)
  797|                         sh->list_entry_lx[0][i] = get_bits(gb, av_ceil_log2(nb_refs));
  798|                 }
  799| 
  800|                 if (sh->slice_type == HEVC_SLICE_B) {
```

- `read_file(path=libavcodec/nvdec_hevc.c, start_line=180, end_line=200, version=old)` →

```
libavcodec/nvdec_hevc.c lines 180-200 of 336
  180|             .num_tile_rows_minus1                         = pps->num_tile_rows - 1,
  181| #if NVDECAPI_CHECK_VERSION(9, 0)
  182|             .pps_range_extension_flag                     = pps->pps_range_extensions_flag,
  183|             .cross_component_prediction_enabled_flag      = pps->cross_component_prediction_enabled_flag,
  184|             .chroma_qp_offset_list_enabled_flag           = pps->chroma_qp_offset_list_enabled_flag,
  185|             .diff_cu_chroma_qp_offset_depth               = pps->diff_cu_chroma_qp_offset_depth,
  186|             .chroma_qp_offset_list_len_minus1             = pps->chroma_qp_offset_list_len_minus1,
  187| #endif
  188| 
  189|             .NumBitsForShortTermRPSInSlice                = s->sh.short_term_rps ? s->sh.short_term_ref_pic_set_size : 0,
  190|             .NumDeltaPocsOfRefRpsIdx                      = s->sh.short_term_rps ? s->sh.short_term_rps->rps_idx_num_delta_pocs : 0,
  191|             .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
  192|             .NumPocStCurrBefore                           = s->rps[ST_CURR_BEF].nb_refs,
  193|             .NumPocStCurrAfter                            = s->rps[ST_CURR_AFT].nb_refs,
  194|             .NumPocLtCurr                                 = s->rps[LT_CURR].nb_refs,
  195|             .CurrPicOrderCntVal                           = s->cur_frame->poc,
  196|         },
  197|     };
  198| 
  199|     if (pps->num_tile_columns > FF_ARRAY_ELEMS(ppc->column_width_minus1) ||
  200|         pps->num_tile_rows    > FF_ARRAY_ELEMS(ppc->row_height_minus1)) {
```

- `read_file(path=libavcodec/vdpau_hevc.c, start_line=200, end_line=215, version=old)` →

```
libavcodec/vdpau_hevc.c lines 200-215 of 559
  200|     if (sh->short_term_ref_pic_set_sps_flag == 1) {
  201|         for (size_t i = 0; i < sps->nb_st_rps; i++) {
  202|             if (sh->short_term_rps == &sps->st_rps[i]) {
  203|                 info->CurrRpsIdx = i;
  204|                 break;
  205|             }
  206|         }
  207|     }
  208|     /* See section 7.4.7.2 of the specification. */
  209|     info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
  210|     if (sh->short_term_ref_pic_set_sps_flag == 0 && sh->short_term_rps) {
  211|         /* Corresponds to specification field, NumDeltaPocs[RefRpsIdx].
  212|            Only applicable when short_term_ref_pic_set_sps_flag == 0.
  213|            Implementations will ignore this value in other cases. See 7.4.8. */
  214|         info->NumDeltaPocsOfRefRpsIdx = sh->short_term_rps->rps_idx_num_delta_pocs;
  215|     }
```

### Turn 3  _(tok 2954+301, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing function names. Let me look backwards to find the function declarations

- `grep(pattern=^(static\s+)?\w[\w\s\*]+\(, path_glob=libavcodec/hevc/hevcdec.c, version=old)` →

```
0 matches

```

- `grep(pattern=^(static\s+)?\w[\w\s\*]+\(, path_glob=libavcodec/nvdec_hevc.c, version=old)` →

```
0 matches

```

- `grep(pattern=^(static\s+)?\w[\w\s\*]+\(, path_glob=libavcodec/vdpau_hevc.c, version=old)` →

```
0 matches

```

### Turn 4  _(tok 3326+118, stop=tool_use)_

**Reasoning:** Let me look further back in each file to find the enclosing function.

- `read_file(end_line=750, path=libavcodec/hevc/hevcdec.c, start_line=700, version=old)` →

```
libavcodec/hevc/hevcdec.c lines 700-750 of 3844
  700|             } else {
  701|                 int numbits, rps_idx;
  702| 
  703|                 if (!sps->nb_st_rps) {
  704|                     av_log(s->avctx, AV_LOG_ERROR, "No ref lists in the SPS.\n");
  705|                     return AVERROR_INVALIDDATA;
  706|                 }
  707| 
  708|                 numbits = av_ceil_log2(sps->nb_st_rps);
  709|                 rps_idx = numbits > 0 ? get_bits(gb, numbits) : 0;
  710|                 sh->short_term_rps = &sps->st_rps[rps_idx];
  711|             }
  712|             sh->short_term_ref_pic_set_size = pos - get_bits_left(gb);
  713| 
  714|             pos = get_bits_left(gb);
  715|             ret = decode_lt_rps(sps, &sh->long_term_rps, gb, sh->poc, sh->pic_order_cnt_lsb);
  716|             if (ret < 0) {
  717|                 av_log(s->avctx, AV_LOG_WARNING, "Invalid long term RPS.\n");
  718|                 if (s->avctx->err_recognition & AV_EF_EXPLODE)
  719|                     return AVERROR_INVALIDDATA;
  720|             }
  721|             sh->long_term_ref_pic_set_size = pos - get_bits_left(gb);
  722| 
  723|             if (sps->temporal_mvp_enabled)
  724|                 sh->slice_temporal_mvp_enabled_flag = get_bits1(gb);
  725|             else
  726|                 sh->slice_temporal_mvp_enabled_flag = 0;
  727|         } else {
  728|             sh->poc                             = 0;
  729|             sh->pic_order_cnt_lsb               = 0;
  730|             sh->short_term_ref_pic_set_sps_flag = 0;
  731|             sh->short_term_ref_pic_set_size     = 0;
  732|             sh->short_term_rps                  = NULL;
  733|             sh->long_term_ref_pic_set_size      = 0;
  734|             sh->slice_temporal_mvp_enabled_flag = 0;
  735|         }
  736| 
  737|         sh->inter_layer_pred = 0;
  738|         if (s->nuh_layer_id > 0) {
  739|             int num_direct_ref_layers = vps->num_direct_ref_layers[layer_idx];
  740| 
  741|             if (vps->default_ref_layers_active)
  742|                 sh->inter_layer_pred = !!num_direct_ref_layers;
  743|             else if (num_direct_ref_layers) {
  744|                 sh->inter_layer_pred = get_bits1(gb);
  745| 
  746|                 if (sh->inter_layer_pred && num_direct_ref_layers > 1) {
  747|                     av_log(s->avctx, AV_LOG_ERROR,
  748|                            "NumDirectRefLayers>1 not supported\n");
  749|                     return AVERROR_PATCHWELCOME;
  750|                 }
```

### Turn 5  _(tok 4276+119, stop=tool_use)_

**Reasoning:** Need to find function start. Let me search backwards with function signature. Maybe use grep for `static int` in hevcdec.c.

- `grep(path_glob=libavcodec/hevc/hevcdec.c, pattern=^static .*\(, version=old)` →

```
48 matches
libavcodec/hevc/hevcdec.c:69:static void pic_arrays_free(HEVCLayerContext *l)
libavcodec/hevc/hevcdec.c:98:static int pic_arrays_init(HEVCLayerContext *l, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:170:static int pred_weight_table(SliceHeader *sh, void *logctx,
libavcodec/hevc/hevcdec.c:287:static int decode_lt_rps(const HEVCSPS *sps, LongTermRPS *rps,
libavcodec/hevc/hevcdec.c:344:static void export_stream_params(HEVCContext *s, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:400:static int export_stream_params_from_sei(HEVCContext *s)
libavcodec/hevc/hevcdec.c:420:static enum AVPixelFormat get_format(HEVCContext *s, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:553:static int set_sps(HEVCContext *s, HEVCLayerContext *l, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:583:static int hls_slice_header(SliceHeader *sh, const HEVCContext *s, GetBitContext *gb)
libavcodec/hevc/hevcdec.c:1022:static void hls_sao_param(HEVCLocalContext *lc, const HEVCLayerContext *l,
libavcodec/hevc/hevcdec.c:1098:static int hls_cross_component_pred(HEVCLocalContext *lc, int idx)
libavcodec/hevc/hevcdec.c:1114:static int hls_transform_unit(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1326:static void set_deblocking_bypass(uint8_t *is_pcm, const HEVCSPS *sps,
libavcodec/hevc/hevcdec.c:1342:static int hls_transform_tree(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1470:static int hls_pcm_sample(HEVCLocalContext *lc, const HEVCLayerContext *l,
libavcodec/hevc/hevcdec.c:1529:static void luma_mc_uni(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1593:static void luma_mc_bi(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1687:static void chroma_mc_uni(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1757:static void chroma_mc_bi(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1850:static void hevc_await_progress(const HEVCContext *s, const HEVCFrame *ref,
libavcodec/hevc/hevcdec.c:1860:static void hevc_luma_mv_mvp_mode(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1907:static void hls_prediction_unit(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:2036:static int luma_intra_pred_mode(HEVCLocalContext *lc, const HEVCLayerContext *l,
libavcodec/hevc/hevcdec.c:2118:static av_always_inline void set_ct_depth(const HEVCSPS *sps, uint8_t *tab_ct_depth,
libavcodec/hevc/hevcdec.c:2136:static void intra_prediction_unit(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:2206:static void intra_prediction_unit_default_value(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:2231:static int hls_coding_unit(HEVCLocalContext *lc, const HEVCContext *s,
libavcodec/hevc/hevcdec.c:2418:static int hls_coding_quadtree(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:2511:static void hls_decode_neighbour(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:2562:static int hls_decode_entry(HEVCContext *s, GetBitContext *gb)
libavcodec/hevc/hevcdec.c:2616:static int hls_decode_entry_wpp(AVCodecContext *avctx, void *hevc_lclist,
libavcodec/hevc/hevcdec.c:2707:static int hls_slice_data_wpp(HEVCContext *s, const H2645NAL *nal)
libavcodec/hevc/hevcdec.c:2809:static int decode_slice_data(HEVCContext *s, const HEVCLayerContext *l,
libavcodec/hevc/hevcdec.c:2863:static int set_side_data(HEVCContext *s)
libavcodec/hevc/hevcdec.c:2951:static int hevc_frame_start(HEVCContext *s, HEVCLayerContext *l)
libavcodec/hevc/hevcdec.c:3098:static int verify_md5(HEVCContext *s, AVFrame *frame)
libavcodec/hevc/hevcdec.c:3167:static int hevc_frame_end(HEVCContext *s)
libavcodec/hevc/hevcdec.c:3213:static int decode_slice(HEVCContext *s, HEVCLayerContext *l,
libavcodec/hevc/hevcdec.c:3261:static int decode_nal_unit(HEVCContext *s, const H2645NAL *nal)
libavcodec/hevc/hevcdec.c:3348:static int decode_nal_units(HEVCContext *s, const uint8_t *buf, int length)
libavcodec/hevc/hevcdec.c:3442:static int hevc_decode_extradata(HEVCContext *s, uint8_t *buf, int length, int first)
libavcodec/hevc/hevcdec.c:3469:static int hevc_receive_frame(AVCodecContext *avctx, AVFrame *frame)
libavcodec/hevc/hevcdec.c:3528:static int hevc_ref_frame(HEVCFrame *dst, const HEVCFrame *src)
libavcodec/hevc/hevcdec.c:3559:static av_cold int hevc_decode_free(AVCodecContext *avctx)
libavcodec/hevc/hevcdec.c:3601:static av_cold int hevc_init_context(AVCodecContext *avctx)
libavcodec/hevc/hevcdec.c:3644:static int hevc_update_thread_context(AVCodecContext *dst,
libavcodec/hevc/hevcdec.c:3722:static av_cold int hevc_decode_init(AVCodecContext *avctx)
libavcodec/hevc/hevcdec.c:3764:static void hevc_decode_flush(AVCodecContext *avctx)
```

### Turn 6  _(tok 6036+164, stop=tool_use)_

**Reasoning:** Line 787 is within `hls_slice_header` (starts line 583, next function starts 1022). So enclosing function is `hls_slice_header` in libavcodec/hevc/hevcdec.c.

Now nvdec_hevc.c and vdpau_hevc.c. Let me find function starts.

- `grep(path_glob=libavcodec/nvdec_hevc.c, pattern=^static .*\(, version=old)` →

```
6 matches
libavcodec/nvdec_hevc.c:35:static void dpb_add(CUVIDHEVCPICPARAMS *pp, int idx, const HEVCFrame *src)
libavcodec/nvdec_hevc.c:45:static void fill_scaling_lists(CUVIDHEVCPICPARAMS *ppc, const HEVCContext *s)
libavcodec/nvdec_hevc.c:72:static int nvdec_hevc_start_frame(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:273:static int nvdec_hevc_decode_slice(AVCodecContext *avctx, const uint8_t *buffer,
libavcodec/nvdec_hevc.c:300:static int nvdec_hevc_frame_params(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:308:static int nvdec_hevc_decode_init(AVCodecContext *avctx) {
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 7  _(tok 6400+302, stop=tool_use, forced)_

**Reasoning:** Let me determine the enclosing functions:

1. `libavcodec/hevc/hevcdec.c` line 787 - between `hls_slice_header` (line 583) and `hls_sao_param` (line 1022). So enclosing function is `hls_slice_header`.

2. `libavcodec/nvdec_hevc.c` line 191 - between `nvdec_hevc_start_frame` (line 72) and `nvdec_hevc_decode_slice` (line 273). So enclosing function is `nvdec_hevc_start_frame`.

3. `libavcodec/vdpau_hevc.c` line 209 - I need to find the enclosing function. Let me check.

For vdpau_hevc.c, I know the call is at line 209. Let me search for function definitions.

- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 2, "n_truth": 3, "tp": 2, "precision": 1.0, "recall": 0.6666666666666666, "f1": 0.8}`

