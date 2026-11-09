# Impact-analysis transcript — ffmpeg @ 75914b582280 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_hevc_frame_nb_refs` (libavcodec/hevc/refs.c), arity 2->3
- truth: [['libavcodec/hevc/hevcdec.c', 'hls_slice_header'], ['libavcodec/nvdec_hevc.c', 'nvdec_hevc_start_frame'], ['libavcodec/vdpau_hevc.c', 'vdpau_hevc_start_frame']]

## Self-navigation arm

### Turn 1  _(tok 949+101, stop=tool_use)_

**Reasoning:** Let me start by exploring the repository to find all references to `ff_hevc_frame_nb_refs`.

Let me use grep to search for this function name across the repository.


**Says:** 

I'll search for all references to `ff_hevc_frame_nb_refs` across the repository.



- `grep(pattern=ff_hevc_frame_nb_refs, version=old)` →

```
5 matches
libavcodec/hevc/hevcdec.c:787:            nb_refs = ff_hevc_frame_nb_refs(sh, pps);
libavcodec/hevc/hevcdec.h:618:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
libavcodec/hevc/refs.c:483:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)
libavcodec/nvdec_hevc.c:191:            .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
libavcodec/vdpau_hevc.c:209:    info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

### Turn 2  _(tok 1242+414, stop=tool_use)_

**Reasoning:** Found 5 matches:
1. `libavcodec/hevc/hevcdec.c:787` - a call site
2. `libavcodec/hevc/hevcdec.h:618` - prototype (skip)
3. `libavcodec/hevc/refs.c:483` - definition (skip)
4. `libavcodec/nvdec_hevc.c:191` - a call site
5. `libavcodec/vdpau_hevc.c:209` - a call site

Now I need to find the enclosing function for each of the 3 call sites. Let me read the relevant portions of each file.

Let me look at each call site to determine the enclosing function name.


**Says:** 

I found 5 matches: 3 call sites, 1 prototype, and 1 definition. Let me examine each call site to determine the enclosing function.





- `read_file(path=libavcodec/hevc/hevcdec.c, start_line=740, end_line=800, version=old)` →

```
libavcodec/hevc/hevcdec.c lines 740-800 of 3844
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
  751|             }
  752|         }
  753| 
  754|         if (sps->sao_enabled) {
  755|             sh->slice_sample_adaptive_offset_flag[0] = get_bits1(gb);
  756|             if (sps->chroma_format_idc) {
  757|                 sh->slice_sample_adaptive_offset_flag[1] =
  758|                 sh->slice_sample_adaptive_offset_flag[2] = get_bits1(gb);
  759|             }
  760|         } else {
  761|             sh->slice_sample_adaptive_offset_flag[0] = 0;
  762|             sh->slice_sample_adaptive_offset_flag[1] = 0;
  763|             sh->slice_sample_adaptive_offset_flag[2] = 0;
  764|         }
  765| 
  766|         sh->nb_refs[L0] = sh->nb_refs[L1] = 0;
  767|         if (sh->slice_type == HEVC_SLICE_P || sh->slice_type == HEVC_SLICE_B) {
  768|             int nb_refs;
  769| 
  770|             sh->nb_refs[L0] = pps->num_ref_idx_l0_default_active;
  771|             if (sh->slice_type == HEVC_SLICE_B)
  772|                 sh->nb_refs[L1] = pps->num_ref_idx_l1_default_active;
  773| 
  774|             if (get_bits1(gb)) { // num_ref_idx_active_override_flag
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

- `read_file(path=libavcodec/nvdec_hevc.c, start_line=150, end_line=210, version=old)` →

```
libavcodec/nvdec_hevc.c lines 150-210 of 336
  150|             .slice_segment_header_extension_present_flag  = pps->slice_header_extension_present_flag,
  151|             .sign_data_hiding_enabled_flag                = pps->sign_data_hiding_flag,
  152|             .cu_qp_delta_enabled_flag                     = pps->cu_qp_delta_enabled_flag,
  153|             .diff_cu_qp_delta_depth                       = pps->diff_cu_qp_delta_depth,
  154|             .init_qp_minus26                              = pps->pic_init_qp_minus26,
  155|             .pps_cb_qp_offset                             = pps->cb_qp_offset,
  156|             .pps_cr_qp_offset                             = pps->cr_qp_offset,
  157|             .constrained_intra_pred_flag                  = pps->constrained_intra_pred_flag,
  158|             .weighted_pred_flag                           = pps->weighted_pred_flag,
  159|             .weighted_bipred_flag                         = pps->weighted_bipred_flag,
  160|             .transform_skip_enabled_flag                  = pps->transform_skip_enabled_flag,
  161|             .transquant_bypass_enabled_flag               = pps->transquant_bypass_enable_flag,
  162|             .entropy_coding_sync_enabled_flag             = pps->entropy_coding_sync_enabled_flag,
  163|             .log2_parallel_merge_level_minus2             = pps->log2_parallel_merge_level - 2,
  164|             .num_extra_slice_header_bits                  = pps->num_extra_slice_header_bits,
  165|             .loop_filter_across_tiles_enabled_flag        = pps->loop_filter_across_tiles_enabled_flag,
  166|             .loop_filter_across_slices_enabled_flag       = pps->seq_loop_filter_across_slices_enabled_flag,
  167|             .output_flag_present_flag                     = pps->output_flag_present_flag,
  168|             .num_ref_idx_l0_default_active_minus1         = pps->num_ref_idx_l0_default_active - 1,
  169|             .num_ref_idx_l1_default_active_minus1         = pps->num_ref_idx_l1_default_active - 1,
  170|             .lists_modification_present_flag              = pps->lists_modification_present_flag,
  171|             .cabac_init_present_flag                      = pps->cabac_init_present_flag,
  172|             .pps_slice_chroma_qp_offsets_present_flag     = pps->pic_slice_level_chroma_qp_offsets_present_flag,
  173|             .deblocking_filter_override_enabled_flag      = pps->deblocking_filter_override_enabled_flag,
  174|             .pps_deblocking_filter_disabled_flag          = pps->disable_dbf,
  175|             .pps_beta_offset_div2                         = pps->beta_offset / 2,
  176|             .pps_tc_offset_div2                           = pps->tc_offset / 2,
  177|             .tiles_enabled_flag                           = pps->tiles_enabled_flag,
  178|             .uniform_spacing_flag                         = pps->uniform_spacing_flag,
  179|             .num_tile_columns_minus1                      = pps->num_tile_columns - 1,
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
  201|         av_log(avctx, AV_LOG_ERROR, "Too many tiles\n");
  202|         return AVERROR(ENOSYS);
  203|     }
  204|     for (i = 0; i < pps->num_tile_columns; i++)
  205|         ppc->column_width_minus1[i] = pps->column_width[i] - 1;
  206|     for (i = 0; i < pps->num_tile_rows; i++)
  207|         ppc->row_height_minus1[i] = pps->row_height[i] - 1;
  208| 
  209| #if NVDECAPI_CHECK_VERSION(9, 0)
  210|     if (pps->chroma_qp_offset_list_len_minus1 >= FF_ARRAY_ELEMS(ppc->cb_qp_offset_list) ||
```

- `read_file(path=libavcodec/vdpau_hevc.c, start_line=170, end_line=220, version=old)` →

```
libavcodec/vdpau_hevc.c lines 170-220 of 559
  170|         /* Only needed if tiles_enabled_flag is set. Invalid values are
  171|            ignored. */
  172|         info->loop_filter_across_tiles_enabled_flag = pps->loop_filter_across_tiles_enabled_flag;
  173|     }
  174|     info->pps_loop_filter_across_slices_enabled_flag = pps->seq_loop_filter_across_slices_enabled_flag;
  175|     info->deblocking_filter_control_present_flag = pps->deblocking_filter_control_present_flag;
  176|     /* Only valid if deblocking_filter_control_present_flag is set. Ignored
  177|        otherwise. */
  178|     info->deblocking_filter_override_enabled_flag = pps->deblocking_filter_override_enabled_flag;
  179|     /* Only valid if deblocking_filter_control_present_flag is set. Ignored
  180|        otherwise. */
  181|     info->pps_deblocking_filter_disabled_flag = pps->disable_dbf;
  182|     /* Only valid if deblocking_filter_control_present_flag is set and
  183|        pps_deblocking_filter_disabled_flag is not set. Ignored otherwise.*/
  184|     info->pps_beta_offset_div2 = pps->beta_offset / 2;
  185|     /* Only valid if deblocking_filter_control_present_flag is set and
  186|        pps_deblocking_filter_disabled_flag is not set. Ignored otherwise. */
  187|     info->pps_tc_offset_div2 = pps->tc_offset / 2;
  188|     info->lists_modification_present_flag = pps->lists_modification_present_flag;
  189|     info->log2_parallel_merge_level_minus2 = pps->log2_parallel_merge_level - 2;
  190|     info->slice_segment_header_extension_present_flag = pps->slice_header_extension_present_flag;
  191| 
  192|     /* Set to 1 if nal_unit_type is equal to IDR_W_RADL or IDR_N_LP.
  193|        Set to zero otherwise. */
  194|     info->IDRPicFlag = IS_IDR(h);
  195|     /* Set to 1 if nal_unit_type in the range of BLA_W_LP to
  196|        RSV_IRAP_VCL23, inclusive. Set to zero otherwise.*/
  197|     info->RAPPicFlag = IS_IRAP(h);
  198|     /* See section 7.4.7.1 of the specification. */
  199|     info->CurrRpsIdx = sps->nb_st_rps;
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

### Turn 3  _(tok 5527+202, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing function names for each. Let me grep for function definitions in these files before the relevant lines.

For hevcdec.c line 787 - I need to find the enclosing function. Let me search for the function definitions in hevcdec.c.

For nvdec_hevc.c line 191 - need enclosing function.

For vdpau_hevc.c line 209 - need enclosing function.

Let me search for function definitions (lines starting with a return type and function name, followed by `(`).


- `grep(pattern=^[a-zA-Z_].*\(.*\)?$, path_glob=libavcodec/hevc/hevcdec.c, max_results=100, version=old)` →

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

### Turn 4  _(tok 7429+276, stop=tool_use)_

**Reasoning:** For hevcdec.c line 787, the enclosing function is `hls_slice_header` (starts at line 583, next function at 1022).

Now for nvdec_hevc.c line 191 and vdpau_hevc.c line 209.


**Says:** 

The call at hevcdec.c:787 is inside `hls_slice_header` (defined at line 583, next function starts at 1022). Now let me find the enclosing functions in the other two files.




- `grep(max_results=50, path_glob=libavcodec/nvdec_hevc.c, pattern=^[a-zA-Z_].*\(, version=old)` →

```
6 matches
libavcodec/nvdec_hevc.c:35:static void dpb_add(CUVIDHEVCPICPARAMS *pp, int idx, const HEVCFrame *src)
libavcodec/nvdec_hevc.c:45:static void fill_scaling_lists(CUVIDHEVCPICPARAMS *ppc, const HEVCContext *s)
libavcodec/nvdec_hevc.c:72:static int nvdec_hevc_start_frame(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:273:static int nvdec_hevc_decode_slice(AVCodecContext *avctx, const uint8_t *buffer,
libavcodec/nvdec_hevc.c:300:static int nvdec_hevc_frame_params(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:308:static int nvdec_hevc_decode_init(AVCodecContext *avctx) {
```

- `grep(max_results=50, path_glob=libavcodec/vdpau_hevc.c, pattern=^[a-zA-Z_].*\(, version=old)` →

```
6 matches
libavcodec/vdpau_hevc.c:34:static int vdpau_hevc_start_frame(AVCodecContext *avctx,
libavcodec/vdpau_hevc.c:403:static int vdpau_hevc_decode_slice(AVCodecContext *avctx,
libavcodec/vdpau_hevc.c:421:static int vdpau_hevc_end_frame(AVCodecContext *avctx)
libavcodec/vdpau_hevc.c:436:static int ptl_convert(const PTLCommon *general_ptl, H265RawProfileTierLevel *h265_raw_ptl)
libavcodec/vdpau_hevc.c:470:static int vdpau_hevc_parse_rext_profile(AVCodecContext *avctx, VdpDecoderProfile *vdp_profile)
libavcodec/vdpau_hevc.c:516:static int vdpau_hevc_init(AVCodecContext *avctx)
```

### Turn 5  _(tok 8167+409, stop=tool_use)_

**Reasoning:** - nvdec_hevc.c:191 → `nvdec_hevc_start_frame` (line 72, next function at 273)
- vdpau_hevc.c:209 → `vdpau_hevc_start_frame` (line 34, next function at 403)

Now, let me double check whether there might be any indirect callers or calls through other means, like a function pointer, or via macros. Let me also check if there are other variants of the name (e.g., in other directories, tests, or a differently-named wrapper). Also check whether there's a build system or a header with a different spelling.

Also, I should check whether the grep was limited by max_results. It found 5 matches with default max_results. Let me re-run with a higher max_results to make sure nothing was truncated. Also let me search for a partial name like "frame_nb_refs" in case of macro-wrapped calls or a differently prefixed name.

Also check for possible calls in tests or other places (e.g., libavcodec/hevc_mvs.c, or an assembly file). Let's also check whether there might be calls hidden behind a macro like `#define` or something.

Let me also verify that there isn't a second version of the repo (the "old" version is the only one available per the tool schema). The tool only supports "old" version. So all searches are on old.

Let me do a broader grep for "frame_nb_refs" and also check for any function pointer assignments.


**Says:** 

Let me verify completeness with broader searches — checking for partial matches, macro wrappers, or function-pointer usage.



- `grep(max_results=200, pattern=frame_nb_refs, version=old)` →

```
5 matches
libavcodec/hevc/hevcdec.c:787:            nb_refs = ff_hevc_frame_nb_refs(sh, pps);
libavcodec/hevc/hevcdec.h:618:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
libavcodec/hevc/refs.c:483:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)
libavcodec/nvdec_hevc.c:191:            .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
libavcodec/vdpau_hevc.c:209:    info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 8376+196, stop=tool_use, forced)_

**Reasoning:** I have all three call sites identified:
1. `hls_slice_header` in libavcodec/hevc/hevcdec.c
2. `nvdec_hevc_start_frame` in libavcodec/nvdec_hevc.c
3. `vdpau_hevc_start_frame` in libavcodec/vdpau_hevc.c

Confidence: high.


- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2778+117, stop=tool_use)_

**Reasoning:** Let me start by finding the definition and all call sites.


- `grep(pattern=ff_hevc_frame_nb_refs, version=old, max_results=100)` →

```
5 matches
libavcodec/hevc/hevcdec.c:787:            nb_refs = ff_hevc_frame_nb_refs(sh, pps);
libavcodec/hevc/hevcdec.h:618:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
libavcodec/hevc/refs.c:483:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)
libavcodec/nvdec_hevc.c:191:            .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
libavcodec/vdpau_hevc.c:209:    info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

- `get_callers(name=ff_hevc_frame_nb_refs, limit=100)` →

```
{
  "name": "ff_hevc_frame_nb_refs",
  "version": "old",
  "callers": [
    {
      "caller": "hls_slice_header",
      "file": "libavcodec/hevc/hevcdec.c",
      "line": 787
    },
    {
      "caller": "nvdec_hevc_start_frame",
      "file": "libavcodec/nvdec_hevc.c",
      "line": 191
    },
    {
      "caller": "vdpau_hevc_start_frame",
      "file": "libavcodec/vdpau_hevc.c",
      "line": 209
    }
  ]
}
```

### Turn 2  _(tok 3269+176, stop=tool_use)_

**Reasoning:** Both grep and get_callers agree: 3 call sites. Let me verify the enclosing function names by reading the surrounding lines quickly.


- `read_file(path=libavcodec/hevc/hevcdec.c, start_line=770, end_line=795, version=old)` →

```
libavcodec/hevc/hevcdec.c lines 770-795 of 3844
  770|             sh->nb_refs[L0] = pps->num_ref_idx_l0_default_active;
  771|             if (sh->slice_type == HEVC_SLICE_B)
  772|                 sh->nb_refs[L1] = pps->num_ref_idx_l1_default_active;
  773| 
  774|             if (get_bits1(gb)) { // num_ref_idx_active_override_flag
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
```

- `read_file(path=libavcodec/nvdec_hevc.c, start_line=180, end_line=195, version=old)` →

```
libavcodec/nvdec_hevc.c lines 180-195 of 336
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
```

### Turn 3  _(tok 4490+178, stop=tool_use)_

**Reasoning:** Confirm the enclosing function names for nvdec_hevc.c:191 and vdpau_hevc.c:209. get_callers says nvdec_hevc_start_frame and vdpau_hevc_start_frame. Let me double-check with get_context_at for vdpau.

Also check whether there are any other callers through function pointers or in other branches (e.g., a macro). Grep found only 5 matches total, so complete.

Let me verify vdpau.


- `read_file(end_line=215, path=libavcodec/vdpau_hevc.c, start_line=195, version=old)` →

```
libavcodec/vdpau_hevc.c lines 195-215 of 559
  195|     /* Set to 1 if nal_unit_type in the range of BLA_W_LP to
  196|        RSV_IRAP_VCL23, inclusive. Set to zero otherwise.*/
  197|     info->RAPPicFlag = IS_IRAP(h);
  198|     /* See section 7.4.7.1 of the specification. */
  199|     info->CurrRpsIdx = sps->nb_st_rps;
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

### Turn 4  _(tok 5165+130, stop=tool_use)_

**Reasoning:** All three confirmed. The enclosing function in vdpau_hevc.c: let me verify it's vdpau_hevc_start_frame by grep for function definitions before line 209.


- `grep(path_glob=libavcodec/vdpau_hevc.c, pattern=^(static )?\w[\w \*]*\(.*\)\s*\{?$, max_results=30, version=old)` →

```
0 matches

```

### Turn 5  _(tok 5312+115, stop=tool_use)_

**Reasoning:** Not important; get_callers already resolved it. But let me confirm quickly by reading around line 160-195 of vdpau_hevc.c to see function start.


- `read_file(end_line=195, path=libavcodec/vdpau_hevc.c, start_line=160, version=old)` →

```
libavcodec/vdpau_hevc.c lines 160-195 of 559
  160|            ignored. */
  161|         for (ssize_t i = 0; i < pps->num_tile_columns; i++) {
  162|             info->column_width_minus1[i] = pps->column_width[i] - 1;
  163|         }
  164|         /* Only need to set 0..num_tile_rows_minus1. The struct
  165|            definition reserves up to the maximum of 22. Invalid values are
  166|            ignored.*/
  167|         for (ssize_t i = 0; i < pps->num_tile_rows; i++) {
  168|             info->row_height_minus1[i] = pps->row_height[i] - 1;
  169|         }
  170|         /* Only needed if tiles_enabled_flag is set. Invalid values are
  171|            ignored. */
  172|         info->loop_filter_across_tiles_enabled_flag = pps->loop_filter_across_tiles_enabled_flag;
  173|     }
  174|     info->pps_loop_filter_across_slices_enabled_flag = pps->seq_loop_filter_across_slices_enabled_flag;
  175|     info->deblocking_filter_control_present_flag = pps->deblocking_filter_control_present_flag;
  176|     /* Only valid if deblocking_filter_control_present_flag is set. Ignored
  177|        otherwise. */
  178|     info->deblocking_filter_override_enabled_flag = pps->deblocking_filter_override_enabled_flag;
  179|     /* Only valid if deblocking_filter_control_present_flag is set. Ignored
  180|        otherwise. */
  181|     info->pps_deblocking_filter_disabled_flag = pps->disable_dbf;
  182|     /* Only valid if deblocking_filter_control_present_flag is set and
  183|        pps_deblocking_filter_disabled_flag is not set. Ignored otherwise.*/
  184|     info->pps_beta_offset_div2 = pps->beta_offset / 2;
  185|     /* Only valid if deblocking_filter_control_present_flag is set and
  186|        pps_deblocking_filter_disabled_flag is not set. Ignored otherwise. */
  187|     info->pps_tc_offset_div2 = pps->tc_offset / 2;
  188|     info->lists_modification_present_flag = pps->lists_modification_present_flag;
  189|     info->log2_parallel_merge_level_minus2 = pps->log2_parallel_merge_level - 2;
  190|     info->slice_segment_header_extension_present_flag = pps->slice_header_extension_present_flag;
  191| 
  192|     /* Set to 1 if nal_unit_type is equal to IDR_W_RADL or IDR_N_LP.
  193|        Set to zero otherwise. */
  194|     info->IDRPicFlag = IS_IDR(h);
  195|     /* Set to 1 if nal_unit_type in the range of BLA_W_LP to
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 4043+125, stop=tool_use, forced)_

**Reasoning:** Submit the three callers.


- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2317+61, stop=tool_use)_

**Reasoning:** I need to locate all the places where this function is being called.


- `get_callers(name=ff_hevc_frame_nb_refs, limit=200)` →

```
{
  "name": "ff_hevc_frame_nb_refs",
  "version": "old",
  "callers": [
    {
      "caller": "hls_slice_header",
      "file": "libavcodec/hevc/hevcdec.c",
      "line": 787
    },
    {
      "caller": "nvdec_hevc_start_frame",
      "file": "libavcodec/nvdec_hevc.c",
      "line": 191
    },
    {
      "caller": "vdpau_hevc_start_frame",
      "file": "libavcodec/vdpau_hevc.c",
      "line": 209
    }
  ]
}
```

### Turn 2  _(tok 2559+149, stop=tool_use)_

**Reasoning:** Let's check whether there are other call sites. For example, inside refs.c itself (hevc_frame_start, etc.) or vaapi_hevc, and so on. The tool returned 3 results. Let's check the usage in refs.c — maybe ff_hevc_frame_nb_refs is called inside refs.c. Just to be safe, I'll resolve it and look at the callers once more. I'll also check whether hevcdec.h has any inline usage. The tool probably covers the whole repository. To double-check for thoroughness, let's expand the function.


- `expand_function(name=ff_hevc_frame_nb_refs)` →

```
{
  "name": "ff_hevc_frame_nb_refs",
  "version": "old",
  "levels": 1,
  "node": {
    "name": "ff_hevc_frame_nb_refs",
    "file": "libavcodec/hevc/refs.c",
    "line": 483,
    "kind": "function",
    "state": "analyzed"
  },
  "callees": [],
  "callers": [
    {
      "name": "hls_slice_header",
      "file": "libavcodec/hevc/hevcdec.c",
      "line": 583,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        787
      ]
    },
    {
      "name": "nvdec_hevc_start_frame",
      "file": "libavcodec/nvdec_hevc.c",
      "line": 72,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        191
      ]
    },
    {
      "name": "vdpau_hevc_start_frame",
      "file": "libavcodec/vdpau_hevc.c",
      "line": 34,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        209
      ]
    }
  ]
}
```

### Turn 3  _(tok 3072+313, stop=tool_use)_

**Reasoning:** There are two tools that agree on the three call sites. Also, I should consider the possibility that it's called within refs.c itself (e.g., export_stream_params or hevc_frame_start). The tools don't show any additional calls. Should I double-check by looking at the refs.c source near the usage sites of ff_hevc_frame_nb_refs? There's no grep. I could use resolve_symbol, or check functions like export_stream_params within refs.c. Actually, in upstream FFmpeg, ff_hevc_frame_nb_refs is called from hls_slice_header in hevcdec.c, nvdec_hevc.c, and vdpau_hevc.c. Also, there's a possibility that export_stream_params in refs.c calls it too, but... in upstream's refs.c, export_stream_params uses s->ps.sps and doesn't use nb_refs. In fact, in upstream there's `ff_hevc_frame_nb_refs` used in export_stream_params, and there it does `int nb_refs = 0;`... anyway, let's check the body of export_stream_params.

**Says:** Two independent lookups agree. Let me sanity-check `refs.c` itself (e.g., `export_stream_params`) for any internal call sites:



- `get_summary(name=export_stream_params)` →

```
{
  "name": "export_stream_params",
  "version": "old",
  "params_read": [
    "s",
    "sps"
  ],
  "params_written": [
    "s*"
  ],
  "params_rebound": [],
  "returns": []
}
```

- `get_neighborhood(name=ff_hevc_frame_nb_refs)` →

```
ff_hevc_frame_nb_refs — libavcodec/hevc/refs.c:483 [function] int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)
  reads: pps, sh; writes: -; returns: return ret;

CALLEES (0):

CALLERS (3):
  hls_slice_header (libavcodec/hevc/hevcdec.c:787): nb_refs = ff_hevc_frame_nb_refs(sh, pps);
  nvdec_hevc_start_frame (libavcodec/nvdec_hevc.c:191): .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
  vdpau_hevc_start_frame (libavcodec/vdpau_hevc.c:209): info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

### Turn 4  _(tok 3689+166, stop=tool_use)_

**Reasoning:** Confirmed the three callers. Submitting.

**Says:** All three sources (gtags callers, function expansion, and neighborhood with call-site lines) agree: there are exactly 3 call sites, and none inside `refs.c` itself.



- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

