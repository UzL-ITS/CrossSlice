# Impact-analysis transcript — ffmpeg @ 75914b582280 — openrouter:deepseek/deepseek-v4-pro

- target: `ff_hevc_frame_nb_refs` (libavcodec/hevc/refs.c), arity 2->3
- truth: [['libavcodec/hevc/hevcdec.c', 'hls_slice_header'], ['libavcodec/nvdec_hevc.c', 'nvdec_hevc_start_frame'], ['libavcodec/vdpau_hevc.c', 'vdpau_hevc_start_frame']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1041+75, stop=tool_use)_

**Reasoning:** Let me find all references to `ff_hevc_frame_nb_refs` in the repository.

- `find_references(name=ff_hevc_frame_nb_refs)` →

```
4 references
ff_hevc_frame_nb_refs  787 libavcodec/hevc/hevcdec.c             nb_refs = ff_hevc_frame_nb_refs(sh, pps);
ff_hevc_frame_nb_refs  618 libavcodec/hevc/hevcdec.h int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
ff_hevc_frame_nb_refs  191 libavcodec/nvdec_hevc.c             .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
ff_hevc_frame_nb_refs  209 libavcodec/vdpau_hevc.c     info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

### Turn 2  _(tok 1314+484, stop=tool_use)_

**Reasoning:** Let me analyze the results:

1. `libavcodec/hevc/hevcdec.c` line 787: `nb_refs = ff_hevc_frame_nb_refs(sh, pps);` - I need to find the enclosing function.
2. `libavcodec/hevc/hevcdec.h` line 618: This is the declaration/prototype, not a call site — skip.
3. `libavcodec/nvdec_hevc.c` line 191: `.NumPocTotalCurr = ff_hevc_frame_nb_refs(&s->sh, pps),` - Need enclosing function.
4. `libavcodec/vdpau_hevc.c` line 209: `info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);` - Need enclosing function.

Let me now find the enclosing functions for each call site.

- `read_file(path=libavcodec/hevc/hevcdec.c, start_line=775, end_line=800, version=old)` →

```
libavcodec/hevc/hevcdec.c lines 775-800 of 3844
  775|                 sh->nb_refs[L0] = get_ue_golomb_31(gb) + 1;
  776|                 if (sh->slice_type == HEVC_SLICE_B)
  777|                     sh->nb_refs[L1] = get_ue_golomb_31(gb) + 1;
  778|             }
  779|             if (sh->nb_refs[L0] >= HEVC_MAX_REFS || sh->nb_refs[L1] >= HEVC_MAX_REFS) {
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

- `read_file(path=libavcodec/vdpau_hevc.c, start_line=200, end_line=220, version=old)` →

```
libavcodec/vdpau_hevc.c lines 200-220 of 559
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
  216|     /* Section 7.6.3.1 of the H.265/HEVC Specification defines the syntax of
  217|        the slice_segment_header. This header contains information that
  218|        some VDPAU implementations may choose to skip. The VDPAU API
  219|        requires client applications to track the number of bits used in the
  220|        slice header for structures associated with short term and long term
```

### Turn 3  _(tok 3245+154, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing functions. Let me look for the function definitions that contain these call sites.

For `hevcdec.c`, line 787 is inside some function. Let me search backwards for the function definition.

- `grep(pattern=^static.*\(, path_glob=libavcodec/hevc/hevcdec.c, max_results=50, version=old)` →

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

### Turn 4  _(tok 5039+214, stop=tool_use)_

**Reasoning:** Line 787 is between `hls_slice_header` at line 583 and `hls_sao_param` at line 1022. Let me look more carefully to confirm. The function `hls_slice_header` is the one that starts at line 583 and ends somewhere before line 1022. Let me verify by reading around line 785 to see the function context.

Actually, let me just look at the function boundaries. Line 583 starts `hls_slice_header`. Let me find where it ends.

- `grep(pattern=^}, path_glob=libavcodec/hevc/hevcdec.c, max_results=80, version=old)` →

```
52 matches
libavcodec/hevc/hevcdec.c:95:}
libavcodec/hevc/hevcdec.c:168:}
libavcodec/hevc/hevcdec.c:285:}
libavcodec/hevc/hevcdec.c:342:}
libavcodec/hevc/hevcdec.c:398:}
libavcodec/hevc/hevcdec.c:418:}
libavcodec/hevc/hevcdec.c:551:}
libavcodec/hevc/hevcdec.c:581:}
libavcodec/hevc/hevcdec.c:1006:}
libavcodec/hevc/hevcdec.c:1020:} while (0)
libavcodec/hevc/hevcdec.c:1093:}
libavcodec/hevc/hevcdec.c:1112:}
libavcodec/hevc/hevcdec.c:1324:}
libavcodec/hevc/hevcdec.c:1340:}
libavcodec/hevc/hevcdec.c:1424:} while (0)
libavcodec/hevc/hevcdec.c:1468:}
libavcodec/hevc/hevcdec.c:1511:}
libavcodec/hevc/hevcdec.c:1575:}
libavcodec/hevc/hevcdec.c:1668:}
libavcodec/hevc/hevcdec.c:1738:}
libavcodec/hevc/hevcdec.c:1848:}
libavcodec/hevc/hevcdec.c:1858:}
libavcodec/hevc/hevcdec.c:1905:}
libavcodec/hevc/hevcdec.c:2031:}
libavcodec/hevc/hevcdec.c:2116:}
libavcodec/hevc/hevcdec.c:2130:}
libavcodec/hevc/hevcdec.c:2204:}
libavcodec/hevc/hevcdec.c:2229:}
libavcodec/hevc/hevcdec.c:2416:}
libavcodec/hevc/hevcdec.c:2509:}
libavcodec/hevc/hevcdec.c:2560:}
libavcodec/hevc/hevcdec.c:2614:}
libavcodec/hevc/hevcdec.c:2705:}
libavcodec/hevc/hevcdec.c:2807:}
libavcodec/hevc/hevcdec.c:2861:}
libavcodec/hevc/hevcdec.c:2949:}
libavcodec/hevc/hevcdec.c:3096:}
libavcodec/hevc/hevcdec.c:3211:}
libavcodec/hevc/hevcdec.c:3259:}
libavcodec/hevc/hevcdec.c:3346:}
libavcodec/hevc/hevcdec.c:3440:}
libavcodec/hevc/hevcdec.c:3467:}
libavcodec/hevc/hevcdec.c:3526:}
libavcodec/hevc/hevcdec.c:3557:}
libavcodec/hevc/hevcdec.c:3599:}
libavcodec/hevc/hevcdec.c:3641:}
libavcodec/hevc/hevcdec.c:3719:}
libavcodec/hevc/hevcdec.c:3762:}
libavcodec/hevc/hevcdec.c:3775:}
libavcodec/hevc/hevcdec.c:3786:};
libavcodec/hevc/hevcdec.c:3793:};
libavcodec/hevc/hevcdec.c:3843:};
```

### Turn 5  _(tok 6047+234, stop=tool_use)_

**Reasoning:** From the function list and closing braces:
- `hls_slice_header` starts at 583 and the next function after it (`hls_sao_param`) starts at 1022. But `hls_slice_header` closes at 1006 (the `}` at line 1006). Line 787 is inside `hls_slice_header`. 

So for `hevcdec.c`, the enclosing function is `hls_slice_header`.

Now for `nvdec_hevc.c` line 191. Let me find the enclosing function.

- `grep(max_results=30, path_glob=libavcodec/nvdec_hevc.c, pattern=^(static\s+)?\w+\s+\w+\(, version=old)` →

```
6 matches
libavcodec/nvdec_hevc.c:35:static void dpb_add(CUVIDHEVCPICPARAMS *pp, int idx, const HEVCFrame *src)
libavcodec/nvdec_hevc.c:45:static void fill_scaling_lists(CUVIDHEVCPICPARAMS *ppc, const HEVCContext *s)
libavcodec/nvdec_hevc.c:72:static int nvdec_hevc_start_frame(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:273:static int nvdec_hevc_decode_slice(AVCodecContext *avctx, const uint8_t *buffer,
libavcodec/nvdec_hevc.c:300:static int nvdec_hevc_frame_params(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:308:static int nvdec_hevc_decode_init(AVCodecContext *avctx) {
```

### Turn 6  _(tok 6519+190, stop=tool_use)_

**Reasoning:** Line 191 is between `nvdec_hevc_start_frame` (line 72) and `nvdec_hevc_decode_slice` (line 273). So the enclosing function is `nvdec_hevc_start_frame`.

Now for `vdpau_hevc.c` line 209. Let me find the enclosing function.

- `grep(max_results=30, path_glob=libavcodec/vdpau_hevc.c, pattern=^(static\s+)?\w+\s+\w+\(, version=old)` →

```
6 matches
libavcodec/vdpau_hevc.c:34:static int vdpau_hevc_start_frame(AVCodecContext *avctx,
libavcodec/vdpau_hevc.c:403:static int vdpau_hevc_decode_slice(AVCodecContext *avctx,
libavcodec/vdpau_hevc.c:421:static int vdpau_hevc_end_frame(AVCodecContext *avctx)
libavcodec/vdpau_hevc.c:436:static int ptl_convert(const PTLCommon *general_ptl, H265RawProfileTierLevel *h265_raw_ptl)
libavcodec/vdpau_hevc.c:470:static int vdpau_hevc_parse_rext_profile(AVCodecContext *avctx, VdpDecoderProfile *vdp_profile)
libavcodec/vdpau_hevc.c:516:static int vdpau_hevc_init(AVCodecContext *avctx)
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 7  _(tok 6964+336, stop=tool_use, forced)_

**Reasoning:** Let me confirm: line 209 is between `vdpau_hevc_start_frame` (line 34) and `vdpau_hevc_decode_slice` (line 403). So the enclosing function is `vdpau_hevc_start_frame`.

Now let me summarize:

1. `hls_slice_header` in `libavcodec/hevc/hevcdec.c` (line 787)
2. `nvdec_hevc_start_frame` in `libavcodec/nvdec_hevc.c` (line 191)
3. `vdpau_hevc_start_frame` in `libavcodec/vdpau_hevc.c` (line 209)

These are the three call sites. The line 618 in hevcdec.h is a declaration (prototype), not a call site.

I'm confident these are the only three call sites.

- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

