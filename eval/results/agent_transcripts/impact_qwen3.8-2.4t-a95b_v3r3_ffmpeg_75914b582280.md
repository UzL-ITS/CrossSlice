# Impact-analysis transcript — ffmpeg @ 75914b582280 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_hevc_frame_nb_refs` (libavcodec/hevc/refs.c), arity 2->3
- truth: [['libavcodec/hevc/hevcdec.c', 'hls_slice_header'], ['libavcodec/nvdec_hevc.c', 'nvdec_hevc_start_frame'], ['libavcodec/vdpau_hevc.c', 'vdpau_hevc_start_frame']]

## Self-navigation arm

### Turn 1  _(tok 949+101, stop=tool_use)_

**Reasoning:** Let me search for calls to `ff_hevc_frame_nb_refs`.


- `grep(pattern=ff_hevc_frame_nb_refs, version=old)` →

```
5 matches
libavcodec/hevc/hevcdec.c:787:            nb_refs = ff_hevc_frame_nb_refs(sh, pps);
libavcodec/hevc/hevcdec.h:618:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
libavcodec/hevc/refs.c:483:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)
libavcodec/nvdec_hevc.c:191:            .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
libavcodec/vdpau_hevc.c:209:    info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

- `list_files(version=old, path=libavcodec/hevc)` →

```
24 files
libavcodec/hevc/Makefile	660
libavcodec/hevc/cabac.c	50627
libavcodec/hevc/data.c	1664
libavcodec/hevc/data.h	1102
libavcodec/hevc/dsp.c	15839
libavcodec/hevc/dsp.h	7635
libavcodec/hevc/dsp_template.c	37168
libavcodec/hevc/filter.c	40879
libavcodec/hevc/hevc.h	5885
libavcodec/hevc/hevcdec.c	151270
libavcodec/hevc/hevcdec.h	20556
libavcodec/hevc/mvs.c	27057
libavcodec/hevc/parse.c	5280
libavcodec/hevc/parse.h	1198
libavcodec/hevc/parser.c	11763
libavcodec/hevc/pred.c	2367
libavcodec/hevc/pred.h	1777
libavcodec/hevc/pred_template.c	22664
libavcodec/hevc/ps.c	95274
libavcodec/hevc/ps.h	17875
libavcodec/hevc/ps_enc.c	4255
libavcodec/hevc/refs.c	16131
libavcodec/hevc/sei.c	11517
libavcodec/hevc/sei.h	3726
```

### Turn 2  _(tok 1575+298, stop=tool_use)_

**Reasoning:** Next, I need to find the enclosing function for each call site:

1. libavcodec/hevc/hevcdec.c:787 — find the enclosing function
2. libavcodec/nvdec_hevc.c:191 — find the enclosing function
3. libavcodec/vdpau_hevc.c:209 — find the enclosing function

- `read_file(path=libavcodec/hevc/hevcdec.c, version=old, start_line=720, end_line=800)` →

```
libavcodec/hevc/hevcdec.c lines 720-800 of 3844
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

- `read_file(path=libavcodec/nvdec_hevc.c, version=old, start_line=120, end_line=200)` →

```
libavcodec/nvdec_hevc.c lines 120-200 of 336
  120|             .pcm_loop_filter_disabled_flag                = sps->pcm_loop_filter_disabled,
  121|             .strong_intra_smoothing_enabled_flag          = sps->strong_intra_smoothing_enabled,
  122|             .max_transform_hierarchy_depth_intra          = sps->max_transform_hierarchy_depth_intra,
  123|             .max_transform_hierarchy_depth_inter          = sps->max_transform_hierarchy_depth_inter,
  124|             .amp_enabled_flag                             = sps->amp_enabled,
  125|             .separate_colour_plane_flag                   = sps->separate_colour_plane,
  126|             .log2_max_pic_order_cnt_lsb_minus4            = sps->log2_max_poc_lsb - 4,
  127|             .num_short_term_ref_pic_sets                  = sps->nb_st_rps,
  128|             .long_term_ref_pics_present_flag              = sps->long_term_ref_pics_present,
  129|             .num_long_term_ref_pics_sps                   = sps->num_long_term_ref_pics_sps,
  130|             .sps_temporal_mvp_enabled_flag                = sps->temporal_mvp_enabled,
  131|             .sample_adaptive_offset_enabled_flag          = sps->sao_enabled,
  132|             .scaling_list_enable_flag                     = sps->scaling_list_enabled,
  133|             .IrapPicFlag                                  = IS_IRAP(s),
  134|             .IdrPicFlag                                   = IS_IDR(s),
  135|             .bit_depth_luma_minus8                        = sps->bit_depth - 8,
  136|             .bit_depth_chroma_minus8                      = sps->bit_depth - 8,
  137| #if NVDECAPI_CHECK_VERSION(9, 0)
  138|             .sps_range_extension_flag                     = sps->range_extension,
  139|             .transform_skip_rotation_enabled_flag         = sps->transform_skip_rotation_enabled,
  140|             .transform_skip_context_enabled_flag          = sps->transform_skip_context_enabled,
  141|             .implicit_rdpcm_enabled_flag                  = sps->implicit_rdpcm_enabled,
  142|             .explicit_rdpcm_enabled_flag                  = sps->explicit_rdpcm_enabled,
  143|             .extended_precision_processing_flag           = sps->extended_precision_processing,
  144|             .intra_smoothing_disabled_flag                = sps->intra_smoothing_disabled,
  145|             .persistent_rice_adaptation_enabled_flag      = sps->persistent_rice_adaptation_enabled,
  146|             .cabac_bypass_alignment_enabled_flag          = sps->cabac_bypass_alignment_enabled,
  147| #endif
  148| 
  149|             .dependent_slice_segments_enabled_flag        = pps->dependent_slice_segments_enabled_flag,
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
```

- `read_file(path=libavcodec/vdpau_hevc.c, version=old, start_line=140, end_line=215)` →

```
libavcodec/vdpau_hevc.c lines 140-215 of 559
  140|     info->cu_qp_delta_enabled_flag = pps->cu_qp_delta_enabled_flag;
  141|     /* Only needed if cu_qp_delta_enabled_flag is set. Ignored otherwise. */
  142|     info->diff_cu_qp_delta_depth = pps->diff_cu_qp_delta_depth;
  143|     info->pps_cb_qp_offset = pps->cb_qp_offset;
  144|     info->pps_cr_qp_offset = pps->cr_qp_offset;
  145|     info->pps_slice_chroma_qp_offsets_present_flag = pps->pic_slice_level_chroma_qp_offsets_present_flag;
  146|     info->weighted_pred_flag = pps->weighted_pred_flag;
  147|     info->weighted_bipred_flag = pps->weighted_bipred_flag;
  148|     info->transquant_bypass_enabled_flag = pps->transquant_bypass_enable_flag;
  149|     info->tiles_enabled_flag = pps->tiles_enabled_flag;
  150|     info->entropy_coding_sync_enabled_flag = pps->entropy_coding_sync_enabled_flag;
  151|     if (info->tiles_enabled_flag) {
  152|         /* Only valid if tiles_enabled_flag is set. Ignored otherwise. */
  153|         info->num_tile_columns_minus1 = pps->num_tile_columns - 1;
  154|         /* Only valid if tiles_enabled_flag is set. Ignored otherwise. */
  155|         info->num_tile_rows_minus1 = pps->num_tile_rows - 1;
  156|         /* Only valid if tiles_enabled_flag is set. Ignored otherwise. */
  157|         info->uniform_spacing_flag = pps->uniform_spacing_flag;
  158|         /* Only need to set 0..num_tile_columns_minus1. The struct
  159|            definition reserves up to the maximum of 20. Invalid values are
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

### Turn 3  _(tok 7150+152, stop=tool_use)_

**Reasoning:** Next, let's identify the functions that wrap these call sites:

1. hevcdec.c:787 — Need to look for the function that contains line 787. Search backward from line 787 to find the function start. Let's look at the function signatures before line 720.


- `grep(pattern=^[a-zA-Z_].*\b\w+\(, path_glob=libavcodec/hevc/hevcdec.c, version=old, max_results=200)` →

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

### Turn 4  _(tok 9003+129, stop=tool_use)_

**Reasoning:** Line 787 of hevcdec.c is inside `hls_slice_header` (line 583). Next, I'll look for the wrapping functions of nvdec_hevc.c:191 and vdpau_hevc.c:209.

- `read_file(path=libavcodec/nvdec_hevc.c, version=old, start_line=55, end_line=75)` →

```
libavcodec/nvdec_hevc.c lines 55-75 of 336
   55|         }
   56| 
   57|         for (j = 0; j < 64; j++) {
   58|             pos = 8 * ff_hevc_diag_scan8x8_y[j] + ff_hevc_diag_scan8x8_x[j];
   59|             ppc->ScalingList8x8[i][j]   = sl->sl[1][i][pos];
   60|             ppc->ScalingList16x16[i][j] = sl->sl[2][i][pos];
   61| 
   62|             if (i < 2)
   63|                 ppc->ScalingList32x32[i][j] = sl->sl[3][i * 3][pos];
   64|         }
   65| 
   66|         ppc->ScalingListDCCoeff16x16[i] = sl->sl_dc[0][i];
   67|         if (i < 2)
   68|             ppc->ScalingListDCCoeff32x32[i] = sl->sl_dc[1][i * 3];
   69|     }
   70| }
   71| 
   72| static int nvdec_hevc_start_frame(AVCodecContext *avctx,
   73|                                   const uint8_t *buffer, uint32_t size)
   74| {
   75|     const HEVCContext *s = avctx->priv_data;
```

### Turn 5  _(tok 9544+137, stop=tool_use)_

**Reasoning:** nvdec_hevc.c:191 is located within `nvdec_hevc_start_frame` (starting from line 72). Next, I'll identify the enclosing function at vdpau_hevc.c:209. Let me try reading the beginning portion of vdpau_hevc.c.

- `read_file(path=libavcodec/vdpau_hevc.c, version=old, start_line=30, end_line=120)` →

```
libavcodec/vdpau_hevc.c lines 30-120 of 559
   30| #include "vdpau_internal.h"
   31| #include "h265_profile_level.h"
   32| 
   33| 
   34| static int vdpau_hevc_start_frame(AVCodecContext *avctx,
   35|                                   const uint8_t *buffer, uint32_t size)
   36| {
   37|     HEVCContext *h = avctx->priv_data;
   38|     const HEVCLayerContext *l = &h->layers[h->cur_layer];
   39|     HEVCFrame *pic = h->cur_frame;
   40|     struct vdpau_picture_context *pic_ctx = pic->hwaccel_picture_private;
   41| 
   42|     VdpPictureInfoHEVC *info = &pic_ctx->info.hevc;
   43| #ifdef VDP_YCBCR_FORMAT_Y_U_V_444
   44|     VdpPictureInfoHEVC444 *info2 = &pic_ctx->info.hevc_444;
   45| #endif
   46| 
   47|     const HEVCPPS *pps = h->pps;
   48|     const HEVCSPS *sps = pps->sps;
   49|     const SliceHeader *sh = &h->sh;
   50|     const ScalingList *sl = pps->scaling_list_data_present_flag ?
   51|                             &pps->scaling_list : &sps->scaling_list;
   52| 
   53|     /* init VdpPictureInfoHEVC */
   54| 
   55|     /* SPS */
   56|     info->chroma_format_idc = sps->chroma_format_idc;
   57|     info->separate_colour_plane_flag = sps->separate_colour_plane;
   58|     info->pic_width_in_luma_samples = sps->width;
   59|     info->pic_height_in_luma_samples = sps->height;
   60|     info->bit_depth_luma_minus8 = sps->bit_depth - 8;
   61|     info->bit_depth_chroma_minus8 = sps->bit_depth - 8;
   62|     info->log2_max_pic_order_cnt_lsb_minus4 = sps->log2_max_poc_lsb - 4;
   63|     /* Provide the value corresponding to the nuh_temporal_id of the frame
   64|        to be decoded. */
   65|     info->sps_max_dec_pic_buffering_minus1 = sps->temporal_layer[sps->max_sub_layers - 1].max_dec_pic_buffering - 1;
   66|     info->log2_min_luma_coding_block_size_minus3 = sps->log2_min_cb_size - 3;
   67|     info->log2_diff_max_min_luma_coding_block_size = sps->log2_diff_max_min_coding_block_size;
   68|     info->log2_min_transform_block_size_minus2 = sps->log2_min_tb_size - 2;
   69|     info->log2_diff_max_min_transform_block_size = sps->log2_max_trafo_size - sps->log2_min_tb_size;
   70|     info->max_transform_hierarchy_depth_inter = sps->max_transform_hierarchy_depth_inter;
   71|     info->max_transform_hierarchy_depth_intra = sps->max_transform_hierarchy_depth_intra;
   72|     info->scaling_list_enabled_flag = sps->scaling_list_enabled;
   73|     /* Scaling lists, in diagonal order, to be used for this frame. */
   74|     for (size_t i = 0; i < 6; i++) {
   75|         for (size_t j = 0; j < 16; j++) {
   76|             /* Scaling List for 4x4 quantization matrix,
   77|                indexed as ScalingList4x4[matrixId][i]. */
   78|             uint8_t pos = 4 * ff_hevc_diag_scan4x4_y[j] + ff_hevc_diag_scan4x4_x[j];
   79|             info->ScalingList4x4[i][j] = sl->sl[0][i][pos];
   80|         }
   81|         for (size_t j = 0; j < 64; j++) {
   82|             uint8_t pos = 8 * ff_hevc_diag_scan8x8_y[j] + ff_hevc_diag_scan8x8_x[j];
   83|             /* Scaling List for 8x8 quantization matrix,
   84|                indexed as ScalingList8x8[matrixId][i]. */
   85|             info->ScalingList8x8[i][j] = sl->sl[1][i][pos];
   86|             /* Scaling List for 16x16 quantization matrix,
   87|                indexed as ScalingList16x16[matrixId][i]. */
   88|             info->ScalingList16x16[i][j] = sl->sl[2][i][pos];
   89|             if (i < 2) {
   90|                 /* Scaling List for 32x32 quantization matrix,
   91|                    indexed as ScalingList32x32[matrixId][i]. */
   92|                 info->ScalingList32x32[i][j] = sl->sl[3][i * 3][pos];
   93|             }
   94|         }
   95|         /* Scaling List DC Coefficients for 16x16,
   96|            indexed as ScalingListDCCoeff16x16[matrixId]. */
   97|         info->ScalingListDCCoeff16x16[i] = sl->sl_dc[0][i];
   98|         if (i < 2) {
   99|             /* Scaling List DC Coefficients for 32x32,
  100|                indexed as ScalingListDCCoeff32x32[matrixId]. */
  101|             info->ScalingListDCCoeff32x32[i] = sl->sl_dc[1][i * 3];
  102|         }
  103|     }
  104|     info->amp_enabled_flag = sps->amp_enabled;
  105|     info->sample_adaptive_offset_enabled_flag = sps->sao_enabled;
  106|     info->pcm_enabled_flag = sps->pcm_enabled;
  107|     if (info->pcm_enabled_flag) {
  108|         /* Only needs to be set if pcm_enabled_flag is set. Ignored otherwise. */
  109|         info->pcm_sample_bit_depth_luma_minus1 = sps->pcm.bit_depth - 1;
  110|         /* Only needs to be set if pcm_enabled_flag is set. Ignored otherwise. */
  111|         info->pcm_sample_bit_depth_chroma_minus1 = sps->pcm.bit_depth_chroma - 1;
  112|         /* Only needs to be set if pcm_enabled_flag is set. Ignored otherwise. */
  113|         info->log2_min_pcm_luma_coding_block_size_minus3 = sps->pcm.log2_min_pcm_cb_size - 3;
  114|         /* Only needs to be set if pcm_enabled_flag is set. Ignored otherwise. */
  115|         info->log2_diff_max_min_pcm_luma_coding_block_size = sps->pcm.log2_max_pcm_cb_size - sps->pcm.log2_min_pcm_cb_size;
  116|         /* Only needs to be set if pcm_enabled_flag is set. Ignored otherwise. */
  117|         info->pcm_loop_filter_disabled_flag = sps->pcm_loop_filter_disabled;
  118|     }
  119|     /* Per spec, when zero, assume short_term_ref_pic_set_sps_flag
  120|        is also zero. */
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 11356+155, stop=tool_use, forced)_

**Reasoning:** vdpau_hevc.c:209 is inside `vdpau_hevc_start_frame` (starting from line 34). There are 3 callers.


- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2778+125, stop=tool_use)_

**Reasoning:** I need to find all the places where `ff_hevc_frame_nb_refs` is being called.


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

### Turn 2  _(tok 3277+263, stop=tool_use)_

**Reasoning:** The grep and get_callers agree. Let me verify the enclosing functions at each line to be safe, and check for any indirect references (e.g., function pointer assignments). Let me look at the context at each line briefly.

Also check for other variants, e.g. usage via a macro or alias. Let me grep for "frame_nb_refs" without the ff_ prefix — already done essentially. Also check other files possibly referencing it in other directories (e.g. hwaccels). The grep was repo-wide, 5 matches. Good.

Let me confirm enclosing functions.


- `get_context_at(file=libavcodec/hevc/hevcdec.c, line=787)` →

```
hls_slice_header — libavcodec/hevc/hevcdec.c:583 [function] static int hls_slice_header(SliceHeader *sh, const HEVCContext *s, GetBitContext *gb)
  reads: gb, s, sh; writes: s*, sh*; returns: return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;

SLICE around line 787 (def-use, level 2; '>' marks the seed):
static int hls_slice_header(SliceHeader *sh, const HEVCContext *s, GetBitContext *gb) {
   const HEVCPPS *pps;
   const HEVCSPS *sps;
   const HEVCVPS *vps;
   unsigned pps_id, layer_idx;
   ...
   sh->first_slice_in_pic_flag = get_bits1(gb);
   sh->no_output_of_prior_pics_flag = 0;
   if(IS_IRAP(s))
     sh->no_output_of_prior_pics_flag = get_bits1(gb);
   pps_id = get_ue_golomb_long(gb);
   ...
   sh->pps_id = pps_id;
   pps = s->ps.pps_list[pps_id];
   sps = pps->sps;
   vps = sps->vps;
   layer_idx = vps->layer_idx[s->nuh_layer_id];
   if(s->nal_unit_type == HEVC_NAL_CRA_NUT && s->last_eos == 1)
     sh->no_output_of_prior_pics_flag = 1;
   sh->dependent_slice_segment_flag = 0;
   if(!sh->first_slice_in_pic_flag) {
     int slice_address_length;
     if(pps->dependent_slice_segments_enabled_flag)
       sh->dependent_slice_segment_flag = get_bits1(gb);
   ...
     slice_address_length = av_ceil_log2(sps->ctb_width * sps->ctb_height);
     sh->slice_segment_addr = get_bitsz(gb, slice_address_length);
   ...
     if(!sh->dependent_slice_segment_flag) {
       sh->slice_addr = sh->slice_segment_addr;
     }
   } else {
     sh->slice_segment_addr = sh->slice_addr = 0;
   }
   if(!sh->dependent_slice_segment_flag) {
   ...
     sh->slice_type = get_ue_golomb_long(gb);
   ...
     sh->pic_output_flag = 1;
     if(pps->output_flag_present_flag)
       sh->pic_output_flag = get_bits1(gb);
     if(sps->separate_colour_plane)
       sh->colour_plane_id = get_bits(gb, 2);
     if(!IS_IDR(s)||(s->nuh_layer_id > 0 && !(vps->poc_lsb_not_present &(1 << layer_idx)))) {
       int poc;
       sh->pic_order_cnt_lsb = get_bits(gb, sps->log2_max_poc_lsb);
       poc = ff_hevc_compute_poc(sps, s->poc_tid0, sh->pic_order_cnt_lsb, s->nal_unit_type);
       if(!sh->first_slice_in_pic_flag && poc != sh->poc) {
   ...
         poc = sh->poc;
       }
       sh->poc = poc;
     }
     if(!IS_IDR(s)) {
       int pos;
       sh->short_term_ref_pic_set_sps_flag = get_bits1(gb);
       pos = get_bits_left(gb);
       if(!sh->short_term_ref_pic_set_sps_flag) {
   ...
         sh->short_term_rps = &sh->slice_rps;
       } else {
         int numbits, rps_idx;
   ...
         numbits = av_ceil_log2(sps->nb_st_rps);
         rps_idx = numbits > 0 ? get_bits(gb, numbits): 0;
         sh->short_term_rps = &sps->st_rps[rps_idx];
       }
       sh->short_term_ref_pic_set_size = pos - get_bits_left(gb);
       pos = get_bits_left(gb);
   ...
       sh->long_term_ref_pic_set_size = pos - get_bits_left(gb);
       if(sps->temporal_mvp_enabled)
         sh->slice_temporal_mvp_enabled_flag = get_bits1(gb);
       else
         sh->slice_temporal_mvp_enabled_flag = 0;
     } else {
       sh->poc = 0;
       sh->pic_order_cnt_lsb = 0;
       sh->short_term_ref_pic_set_sps_flag = 0;
       sh->short_term_ref_pic_set_size = 0;
       sh->short_term_rps = NULL;
       sh->long_term_ref_pic_set_size = 0;
       sh->slice_temporal_mvp_enabled_flag = 0;
     }
     sh->inter_layer_pred = 0;
     if(s->nuh_layer_id > 0) {
       int num_direct_ref_layers = vps->num_direct_ref_layers[layer_idx];
       if(vps->default_ref_layers_active)
         sh->inter_layer_pred = !!num_direct_ref_layers;
       else if(num_direct_ref_layers) {
         sh->inter_layer_pred = get_bits1(gb);
   ...
       }
     }
     if(sps->sao_enabled) {
       sh->slice_sample_adaptive_offset_flag[0] = get_bits1(gb);
       if(sps->chroma_format_idc) {
         sh->slice_sample_adaptive_offset_flag[1] = sh->slice_sample_adaptive_offset_flag[2] = get_bits1(gb);
       }
     } else {
       sh->slice_sample_adaptive_offset_flag[0] = 0;
       sh->slice_sample_adaptive_offset_flag[1] = 0;
       sh->slice_sample_adaptive_offset_flag[2] = 0;
     }
     sh->nb_refs[L0] = sh->nb_refs[L1] = 0;
     if(sh->slice_type == HEVC_SLICE_P || sh->slice_type == HEVC_SLICE_B) {
   ...
       sh->nb_refs[L0] = pps->num_ref_idx_l0_default_active;
       if(sh->slice_type == HEVC_SLICE_B)
         sh->nb_refs[L1] = pps->num_ref_idx_l1_default_active;
       if(get_bits1(gb)) {
         sh->nb_refs[L0] = get_ue_golomb_31(gb)+ 1;
         if(sh->slice_type == HEVC_SLICE_B)
           sh->nb_refs[L1] = get_ue_golomb_31(gb)+ 1;
       }
   ...
       sh->rpl_modification_flag[0] = 0;
       sh->rpl_modification_flag[1] = 0;
>      nb_refs = ff_hevc_frame_nb_refs(sh, pps);
       if(!nb_refs) {
   ...
       }
       if(pps->lists_modification_present_flag && nb_refs > 1) {
         sh->rpl_modification_flag[0] = get_bits1(gb);
         if(sh->rpl_modification_flag[0]) {
           for(i = 0; i < sh->nb_refs[L0]; i++)
             sh->list_entry_lx[0][i] = get_bits(gb, av_ceil_log2(nb_refs));
         }
         if(sh->slice_type == HEVC_SLICE_B) {
           sh->rpl_modification_flag[1] = get_bits1(gb);
           if(sh->rpl_modification_flag[1] == 1)
             for(i = 0; i < sh->nb_refs[L1]; i++)
               sh->list_entry_lx[1][i] = get_bits(gb, av_ceil_log2(nb_refs));
         }
       }
   ...
       sh->collocated_ref_idx = 0;
       if(sh->slice_temporal_mvp_enabled_flag) {
         sh->collocated_list = L0;
         if(sh->slice_type == HEVC_SLICE_B)
           sh->collocated_list = !get_bits1(gb);
         if(sh->nb_refs[sh->collocated_list] > 1) {
           sh->collocated_ref_idx = get_ue_golomb_long(gb);
   ...
         }
       }
       if((pps->weighted_pred_flag && sh->slice_type == HEVC_SLICE_P)||(pps->weighted_bipred_flag && sh->slice_type == HEVC_SLICE_B)) {
         int ret = pred_weight_table(sh, s->avctx, sps, gb);
         if(ret < 0)
           return ret;
   ...
       }
     }
   }
   ...
   ret = get_bits1(gb);
   if(!ret) {
   ...
   }
}

CALLEES (22):
  get_bits1 (libavcodec/get_bits.h:388 (1 of 2 definitions)): reads s; writes s*; returns return result;
  get_ue_golomb_long (libavcodec/golomb.h:104): reads gb; writes -; returns return get_bits_long(gb, log + 1)- 1;
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  get_bitsz (libavcodec/get_bits.h:351 (1 of 2 definitions)): reads n, s; writes -; returns return n ? get_bits(s, n): 0;
  get_se_golomb (libavcodec/golomb.h:239 (1 of 3 definitions)): reads gb; writes gb*; returns return ff_se_golomb_vlc_code[buf]; | return buf; | return ff_se_golomb_vlc_code[buf]; | return buf;
  pred_weight_table (libavcodec/hevc/hevcdec.c:170 (1 of 2 definitions)): reads gb, logctx, sh, sps; writes sh*; returns return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;
  get_bits (libavcodec/get_bits.h:335 (1 of 3 definitions)): reads n, s; writes s*; returns return tmp;
  ff_hevc_frame_nb_refs (libavcodec/hevc/refs.c:483): reads pps, sh; writes -; returns return ret;
  get_ue_golomb_31 (libavcodec/golomb.h:120): reads gb; writes gb*; returns return ff_ue_golomb_vlc_code[buf];
  get_bits_left (libavcodec/get_bits.h:695 (1 of 2 definitions)): reads gb; writes -; returns return gb->size_in_bits - get_bits_count(gb);
  decode_lt_rps (libavcodec/hevc/hevcdec.c:287): reads cur_poc, gb, poc_lsb, rps, sps; writes rps*; returns return 0; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return 0;
  ff_hevc_decode_short_term_rps (libavcodec/hevc/ps.c:89): reads avctx, gb, is_slice_header, rps, sps; writes rps*; returns return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;
  ff_hevc_compute_poc (libavcodec/hevc/ps.c:2382): reads nal_unit_type, pocTid0, poc_lsb, sps; writes -; returns return poc_msb + poc_lsb;
  skip_bits (libavcodec/get_bits.h:381 (1 of 2 definitions)): reads n, s; writes s*; returns -
  get_bits_long (libavcodec/get_bits.h:421 (1 of 2 definitions)): reads n, s; writes s*; returns return 0; | return get_bits(s, n); | return tmp; | return ret |(get_bits(s, n - 16)<< 16); | return ret | get_bits(s, n - 16);
  av_malloc_array (libavutil/mem.c:209 (1 of 2 definitions)): reads nmemb, size; writes -; returns return NULL; | return av_malloc(result);
  av_freep (libavutil/mem.c:247 (1 of 2 definitions)): reads arg; writes arg*; returns -
  align_get_bits (libavcodec/get_bits.h:561 (1 of 2 definitions)): reads s; writes -; returns return s->buffer +(s->index >> 3);
  IS_IRAP [macro (1 of 2 definitions)]: #define IS_IRAP(s) ((s)->nal_unit_type >= HEVC_NAL_BLA_W_LP && (s)->nal_unit_type <= HEVC_NAL_RSV_IRAP_VCL23)
  av_ceil_log2 [macro]: # define av_ceil_log2 av_ceil_log2_c
  IS_IDR [macro (1 of 3 definitions)]: #define IS_IDR(s) ((s)->nal_unit_type == HEVC_NAL_IDR_W_RADL || (s)->nal_unit_type == HEVC_NAL_IDR_N_LP)
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)

CALLERS (1):
  decode_slice (libavcodec/hevc/hevcdec.c:3218): ret = hls_slice_header(&s->sh, s, gb);
```

- `get_context_at(file=libavcodec/nvdec_hevc.c, line=191)` →

```
nvdec_hevc_start_frame — libavcodec/nvdec_hevc.c:72 [function] static int nvdec_hevc_start_frame(AVCodecContext *avctx, const uint8_t *buffer, uint32_t size)
  reads: avctx; writes: avctx*; returns: return ret; | return AVERROR(ENOSYS); | return AVERROR(ENOSYS); | return AVERROR(ENOSYS); | return AVERROR_INVALIDDATA; | return 0;

SLICE around line 191 (def-use, level 2; '>' marks the seed):
static int nvdec_hevc_start_frame(AVCodecContext *avctx, const uint8_t *buffer, uint32_t size) {
   const HEVCContext *s = avctx->priv_data;
   ...
   const HEVCPPS *pps = s->pps;
   const HEVCSPS *sps = pps->sps;
   NVDECContext *ctx = avctx->internal->hwaccel_priv_data;
   CUVIDPICPARAMS *pp = &ctx->pic_params;
   ...
   FrameDecodeData *fdd;
   NVDECFrame *cf;
   ...
   fdd =(FrameDecodeData*)s->cur_frame->f->private_ref->data;
   cf =(NVDECFrame*)fdd->hwaccel_priv;
>  *pp =(CUVIDPICPARAMS){ .PicWidthInMbs = sps->width / 16, .FrameHeightInMbs = sps->height / 16, .CurrPicIdx = cf->idx, .ref_pic_flag = 1, .intra_pic_flag = IS_IRAP(s), .CodecSpecific.hevc = { .pic_width_in_luma_samples = sps->width, .pic_height_in_luma_samples = sps->height, .log2_min_luma_coding_block_size_minus3 = sps->log2_min_cb_size - 3, .log2_diff_max_min_luma_coding_block_size = sps->log2_diff_max_min_coding_block_size, .log2_min_transform_block_size_minus2 = sps->log2_min_tb_size - 2, .log2_diff_max_min_transform_block_size = sps->log2_max_trafo_size - sps->log2_min_tb_size, .pcm_enabled_flag = sps->pcm_enabled, .log2_min_pcm_luma_coding_block_size_minus3 = sps->pcm_enabled ? sps->pcm.log2_min_pcm_cb_size - 3 : 0, .log2_diff_max_min_pcm_luma_coding_block_size = sps->pcm.log2_max_pcm_cb_size - sps->pcm.log2_min_pcm_cb_size, .pcm_sample_bit_depth_luma_minus1 = sps->pcm_enabled ? sps->pcm.bit_depth - 1 : 0, .pcm_sample_bit_depth_chroma_minus1 = sps->pcm_enabled ? sps->pcm.bit_depth_chroma - 1 : 0, #if NVDECAPI_CHECK_VERSION(8, 1).log2_max_transform_skip_block_size_minus2 = pps->log2_max_transform_skip_block_size - 2, .log2_sao_offset_scale_luma = pps->log2_sao_offset_scale_luma, .log2_sao_offset_scale_chroma = pps->log2_sao_offset_scale_chroma, .high_precision_offsets_enabled_flag = sps->high_precision_offsets_enabled, #endif .pcm_loop_filter_disabled_flag = sps->pcm_loop_filter_disabled, .strong_intra_smoothing_enabled_flag = sps->strong_intra_smoothing_enabled, .max_transform_hierarchy_depth_intra = sps->max_transform_hierarchy_depth_intra, .max_transform_hierarchy_depth_inter = sps->max_transform_hierarchy_depth_inter, .amp_enabled_flag = sps->amp_enabled, .separate_colour_plane_flag = sps->separate_colour_plane, .log2_max_pic_order_cnt_lsb_minus4 = sps->log2_max_poc_lsb - 4, .num_short_term_ref_pic_sets = sps->nb_st_rps, .long_term_ref_pics_present_flag = sps->long_term_ref_pics_present, .num_long_term_ref_pics_sps = sps->num_long_term_ref_pics_sps, .sps_temporal_mvp_enabled_flag = sps->temporal_mvp_enabled, .sample_adaptive_offset_enabled_flag = sps->sao_enabled, .scaling_list_enable_flag = sps->scaling_list_enabled, .IrapPicFlag = IS_IRAP(s), .IdrPicFlag = IS_IDR(s), .bit_depth_luma_minus8 = sps->bit_depth - 8, .bit_depth_chroma_minus8 = sps->bit_depth - 8, #if NVDECAPI_CHECK_VERSION(9, 0).sps_range_extension_flag = sps->range_extension, .transform_skip_rotation_enabled_flag = sps->transform_skip_rotation_enabled, .transform_skip_context_enabled_flag = sps->transform_skip_context_enabled, .implicit_rdpcm_enabled_flag = sps->implicit_rdpcm_enabled, .explicit_rdpcm_enabled_flag = sps->explicit_rdpcm_enabled, .extended_precision_processing_flag = sps->extended_precision_processing, .intra_smoothing_disabled_flag = sps->intra_smoothing_disabled, .persistent_rice_adaptation_enabled_flag = sps->persistent_rice_adaptation_enabled, .cabac_bypass_alignment_enabled_flag = sps->cabac_bypass_alignment_enabled, #endif .dependent_slice_segments_enabled_flag = pps->dependent_slice_segments_enabled_flag, .slice_segment_header_extension_present_flag = pps->slice_header_extension_present_flag, .sign_data_hiding_enabled_flag = pps->sign_data_hiding_flag, .cu_qp_delta_enabled_flag = pps->cu_qp_delta_enabled_flag, .diff_cu_qp_delta_depth = pps->diff_cu_qp_delta_depth, .init_qp_minus26 = pps->pic_init_qp_minus26, .pps_cb_qp_offset = pps->cb_qp_offset, .pps_cr_qp_offset = pps->cr_qp_offset, .constrained_intra_pred_flag = pps->constrained_intra_pred_flag, .weighted_pred_flag = pps->weighted_pred_flag, .weighted_bipred_flag = pps->weighted_bipred_flag, .transform_skip_enabled_flag = pps->transform_skip_enabled_flag, .transquant_bypass_enabled_flag = pps->transquant_bypass_enable_flag, .entropy_coding_sync_enabled_flag = pps->entropy_coding_sync_enabled_flag, .log2_parallel_merge_level_minus2 = pps->log2_parallel_merge_level - 2, .num_extra_slice_header_bits = pps->num_extra_slice_header_bits, .loop_filter_across_tiles_enabled_flag = pps->loop_filter_across_tiles_enabled_flag, .loop_filter_across_slices_enabled_flag = pps->seq_loop_filter_across_slices_enabled_flag, .output_flag_present_flag = pps->output_flag_present_flag, .num_ref_idx_l0_default_active_minus1 = pps->num_ref_idx_l0_default_active - 1, .num_ref_idx_l1_default_active_minus1 = pps->num_ref_idx_l1_default_active - 1, .lists_modification_present_flag = pps->lists_modification_present_flag, .cabac_init_present_flag = pps->cabac_init_present_flag, .pps_slice_chroma_qp_offsets_present_flag = pps->pic_slice_level_chroma_qp_offsets_present_flag, .deblocking_filter_override_enabled_flag = pps->deblocking_filter_override_enabled_flag, .pps_deblocking_filter_disabled_flag = pps->disable_dbf, .pps_beta_offset_div2 = pps->beta_offset / 2, .pps_tc_offset_div2 = pps->tc_offset / 2, .tiles_enabled_flag = pps->tiles_enabled_flag, .uniform_spacing_flag = pps->uniform_spacing_flag, .num_tile_columns_minus1 = pps->num_tile_columns - 1, .num_tile_rows_minus1 = pps->num_tile_rows - 1, #if NVDECAPI_CHECK_VERSION(9, 0).pps_range_extension_flag = pps->pps_range_extensions_flag, .cross_component_prediction_enabled_flag = pps->cross_component_prediction_enabled_flag, .chroma_qp_offset_list_enabled_flag = pps->chroma_qp_offset_list_enabled_flag, .diff_cu_chroma_qp_offset_depth = pps->diff_cu_chroma_qp_offset_depth, .chroma_qp_offset_list_len_minus1 = pps->chroma_qp_offset_list_len_minus1, #endif .NumBitsForShortTermRPSInSlice = s->sh.short_term_rps ? s->sh.short_term_ref_pic_set_size : 0, .NumDeltaPocsOfRefRpsIdx = s->sh.short_term_rps ? s->sh.short_term_rps->rps_idx_num_delta_pocs : 0, .NumPocTotalCurr = ff_hevc_frame_nb_refs(&s->sh, pps), .NumPocStCurrBefore = s->rps[ST_CURR_BEF].nb_refs, .NumPocStCurrAfter = s->rps[ST_CURR_AFT].nb_refs, .NumPocLtCurr = s->rps[LT_CURR].nb_refs, .CurrPicOrderCntVal = s->cur_frame->poc, }, };
   ...
}

CALLEES (10):
  ff_nvdec_start_frame (libavcodec/nvdec.c:561): reads avctx, frame; writes avctx*, frame*; returns return 0; | return AVERROR(ENOMEM); | return 0; | return ret;
  ff_hevc_frame_nb_refs (libavcodec/hevc/refs.c:483): reads pps, sh; writes -; returns return ret;
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  dpb_add (libavcodec/nvdec_h264.c:34 (1 of 3 definitions)): reads dst, frame_idx, src; writes dst*; returns -
  fill_scaling_lists (libavcodec/nvdec_hevc.c:45): reads ppc, s; writes ppc*; returns -
  NVDECAPI_CHECK_VERSION [macro (1 of 2 definitions)]: # define NVDECAPI_CHECK_VERSION(major, minor) \
  IS_IDR [macro (1 of 3 definitions)]: #define IS_IDR(s) ((s)->nal_unit_type == HEVC_NAL_IDR_W_RADL || (s)->nal_unit_type == HEVC_NAL_IDR_N_LP)
  IS_IRAP [macro (1 of 2 definitions)]: #define IS_IRAP(s) ((s)->nal_unit_type >= HEVC_NAL_BLA_W_LP && (s)->nal_unit_type <= HEVC_NAL_RSV_IRAP_VCL23)
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)
  FF_ARRAY_ELEMS [macro (1 of 3 definitions)]: #define FF_ARRAY_ELEMS(a) (sizeof(a) / sizeof((a)[0]))

CALLERS (0):
```

- `get_context_at(file=libavcodec/vdpau_hevc.c, line=209)` →

```
vdpau_hevc_start_frame — libavcodec/vdpau_hevc.c:34 [function] static int vdpau_hevc_start_frame(AVCodecContext *avctx, const uint8_t *buffer, uint32_t size)
  reads: avctx, buffer, size; writes: avctx*; returns: return ff_vdpau_common_start_frame(pic_ctx, buffer, size);

SLICE around line 209 (def-use, level 2; '>' marks the seed):
static int vdpau_hevc_start_frame(AVCodecContext *avctx, const uint8_t *buffer, uint32_t size) {
   HEVCContext *h = avctx->priv_data;
   ...
   HEVCFrame *pic = h->cur_frame;
   struct vdpau_picture_context *pic_ctx = pic->hwaccel_picture_private;
   VdpPictureInfoHEVC *info = &pic_ctx->info.hevc;
   ...
   const HEVCPPS *pps = h->pps;
   ...
>  info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
   ...
}

CALLEES (7):
  ff_hevc_frame_nb_refs (libavcodec/hevc/refs.c:483): reads pps, sh; writes -; returns return ret;
  ff_vdpau_get_surface_id (libavcodec/vdpau_internal.h:38): reads pic; writes -; returns return(uintptr_t)pic->data[3];
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_vdpau_common_start_frame (libavcodec/vdpau.c:331): reads pic_ctx; writes pic_ctx*; returns return 0;
  IS_IDR [macro (1 of 3 definitions)]: #define IS_IDR(s) ((s)->nal_unit_type == HEVC_NAL_IDR_W_RADL || (s)->nal_unit_type == HEVC_NAL_IDR_N_LP)
  IS_IRAP [macro (1 of 2 definitions)]: #define IS_IRAP(s) ((s)->nal_unit_type >= HEVC_NAL_BLA_W_LP && (s)->nal_unit_type <= HEVC_NAL_RSV_IRAP_VCL23)
  FF_ARRAY_ELEMS [macro (1 of 3 definitions)]: #define FF_ARRAY_ELEMS(a) (sizeof(a) / sizeof((a)[0]))

CALLERS (0):

TYPES (1):
  vdpau_picture_context — libavcodec/vdpau_internal.h:98
    struct vdpau_picture_context {
        union VDPAUPictureInfo info;
        int bitstream_buffers_allocated;
        int bitstream_buffers_used;
        VdpBitstreamBuffer *bitstream_buffers;
    }
```

### Turn 3  _(tok 9822+403, stop=tool_use)_

**Reasoning:** All three confirmed. Also verify there's no other reference (e.g., in hevc_mvs.c or an assembly file). grep was repo-wide with 5 matches, so complete.

Also check for any usage via a macro alias like `#define nb_refs ff_hevc_frame_nb_refs` — grep already covers all textual occurrences of the name.

Submit.


**Says:** 

All three call sites are confirmed (grep across the whole repo found only the 3 call sites plus the prototype in `hevcdec.h` and the definition in `refs.c`):

| Function | File | Call site |
|---|---|---|
| `hls_slice_header` | `libavcodec/hevc/hevcdec.c` | line 787 — `nb_refs = ff_hevc_frame_nb_refs(sh, pps);` |
| `nvdec_hevc_start_frame` | `libavcodec/nvdec_hevc.c` | line 191 — `.NumPocTotalCurr = ff_hevc_frame_nb_refs(&s->sh, pps),` |
| `vdpau_hevc_start_frame` | `libavcodec/vdpau_hevc.c` | line 209 — `info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);` |



- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2355+218, stop=tool_use)_

**Reasoning:** Let me use the tools to find callers of `ff_hevc_frame_nb_refs`.

The task requires listing every function that calls `ff_hevc_frame_nb_refs`. There's a risk of indirect/macro-wrapped calls, calls through function pointers, or calls in files not indexed. Let me start.

Also note the hint: "Also check for macro-wrapped calls (e.g., `#define M(x) ff_hevc_frame_nb_refs(x)`), conditional compilation (`#ifdef` branches), and indirect calls via function pointers — these are easy to miss with grep alone."

Let me do the investigation.


**Says:** 

I'll start by resolving the symbol and getting its callers.




- `resolve_symbol(name=ff_hevc_frame_nb_refs)` →

```
{
  "resolved": true,
  "name": "ff_hevc_frame_nb_refs",
  "version": "old",
  "file": "libavcodec/hevc/refs.c",
  "line": 483,
  "kind": "function",
  "signature": "int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

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

### Turn 2  _(tok 2840+168, stop=tool_use)_

**Reasoning:** Let me verify with get_neighborhood, and also check the definition source and any macro wrappers.

Let me check the neighborhood of ff_hevc_frame_nb_refs.

Also I should look for macros that wrap it. There's no grep, but I can check the definition source and look at related headers. Let me check get_neighborhood which lists callers and callees.

Additionally, I should consider indirect calls via function pointers — e.g., a table of function pointers. Let me check whether there's any other name resolution. Let me also check the "new"/"work" versions to see if callers differ.

Let me do a few calls in parallel.


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

### Turn 3  _(tok 3224+770, stop=tool_use)_

**Reasoning:** Now, let me check for macro-wrapped calls. The hint says to check for macros that wrap it, conditional compilation branches, and function pointers.

Possible places: 
- libavcodec/hevc/hevcdec.c — the multi-threaded variant? There's also `libavcodec/hevc/hevc_mvs.c`. 
- There may be a `hevc_parse_slice_header` or similar.
- Also there could be a `ff_hevc_frame_nb_refs` usage in `libavcodec/hevc/refs.c` itself (self-call) — no.

Let me check for other HEVC decoders: `libavcodec/hevcdec.c` (old location)? The repo layout has `libavcodec/hevc/hevcdec.c`. 

Potential macro wrappers: In FFmpeg, there's `#define NB_REFS ...`. Hmm.

Let me check the function source to see what it does, and check for any similar functions. Also check callers in other versions ("work", "new").

Let me think about what could be missed. Common candidates in FFmpeg:
1. `libavcodec/hevc/hevcdec.c` — `hls_slice_header` (found).
2. `libavcodec/hevc/hevcdec.c` — maybe also in `hls_slice_data` or `ff_hevc_output_frame`? Not found.
3. `libavcodec/vaapi_hevc.c` — VAAPI HEVC decode uses `vaapi_hevc_start_frame`; does it call ff_hevc_frame_nb_refs? In upstream FFmpeg, `vaapi_hevc.c` computes NumPocTotalCurr itself... Actually in upstream FFmpeg, `vaapi_hevc_start_frame` does call `ff_hevc_frame_nb_refs`. Let me check.

Upstream libavcodec/vaapi_hevc.c:
```c
static int vaapi_hevc_start_frame(AVCodecContext          *avctx,
                                  av_unused const uint8_t *buffer,
                                  av_unused uint32_t       size)
{
    HEVCContext         *h = avctx->priv_data;
    HEVCVAAPIContext     *ctx = avctx->internal->hwaccel_priv_data;
    const HEVCPPS       *pps = h->ps.pps;
    const HEVCSPS       *sps = pps->sps;
    ...
    pic_param.NumPocTotalCurr = ff_hevc_frame_nb_refs(h->sh, pps); // hmm
```
Actually I recall in vaapi_hevc.c:
```c
    pic_param->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```
Hmm, but actually I think vaapi_hevc.c has its own loop. Let me check by resolving symbols.

Also `libavcodec/v4l2_m2m_dec.c`? No.

Also there might be a `hevc_v4l2_request.c` in newer FFmpeg which calls `ff_hevc_frame_nb_refs`.

Also `libavcodec/hevc/hevc_sei.c`? no.

Let me also consider that gtags might not index all files (e.g., files excluded). Let me check whether vaapi_hevc.c exists and search within it. I don't have grep, but I can use get_context_at on a line, or get_function_source of `vaapi_hevc_start_frame`.

Let me resolve those symbols.

- `resolve_symbol(name=vaapi_hevc_start_frame)` →

```
{
  "resolved": true,
  "name": "vaapi_hevc_start_frame",
  "version": "old",
  "file": "libavcodec/vaapi_hevc.c",
  "line": 124,
  "kind": "function",
  "signature": "static int vaapi_hevc_start_frame(AVCodecContext *avctx, av_unused const uint8_t *buffer, av_unused uint32_t size)",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 4  _(tok 4131+163, stop=tool_use)_

**Reasoning:** Let me get its source to see if it calls ff_hevc_frame_nb_refs (perhaps through a macro or directly but gtags missed it).

Also check other HEVC hwaccels: `libavcodec/hevc_v4l2_request.c`? Let me resolve `v4l2_request_hevc_start_frame` or similar. And `libavcodec/dxva2_hevc.c`, `libavcodec/d3d11va_hevc.c`? Actually there's `libavcodec/dxva2_hevc.c` with `dxva2_hevc_start_frame`.

Let me do parallel calls.


- `get_function_source(name=vaapi_hevc_start_frame)` →

```
vaapi_hevc_start_frame (function, old version) — libavcodec/vaapi_hevc.c:124-344
  124| static int vaapi_hevc_start_frame(AVCodecContext          *avctx,
  125|                                   av_unused const uint8_t *buffer,
  126|                                   av_unused uint32_t       size)
  127| {
  128|     const HEVCContext        *h = avctx->priv_data;
  129|     const HEVCLayerContext   *l = &h->layers[h->cur_layer];
  130|     VAAPIDecodePictureHEVC *pic = h->cur_frame->hwaccel_picture_private;
  131|     const HEVCPPS          *pps = h->pps;
  132|     const HEVCSPS          *sps = pps->sps;
  133| 
  134|     const ScalingList *scaling_list = NULL;
  135|     int pic_param_size, err, i;
  136| 
  137| #if VA_CHECK_VERSION(1, 2, 0)
  138|     int num_comps, pre_palette_size;
  139| #endif
  140| 
  141|     VAPictureParameterBufferHEVC *pic_param = (VAPictureParameterBufferHEVC *)&pic->pic_param;
  142| 
  143|     pic->pic.output_surface = ff_vaapi_get_surface_id(h->cur_frame->f);
  144| 
  145|     *pic_param = (VAPictureParameterBufferHEVC) {
  146|         .pic_width_in_luma_samples                    = sps->width,
  147|         .pic_height_in_luma_samples                   = sps->height,
  148|         .log2_min_luma_coding_block_size_minus3       = sps->log2_min_cb_size - 3,
  149|         .sps_max_dec_pic_buffering_minus1             = sps->temporal_layer[sps->max_sub_layers - 1].max_dec_pic_buffering - 1,
  150|         .log2_diff_max_min_luma_coding_block_size     = sps->log2_diff_max_min_coding_block_size,
  151|         .log2_min_transform_block_size_minus2         = sps->log2_min_tb_size - 2,
  152|         .log2_diff_max_min_transform_block_size       = sps->log2_max_trafo_size  - sps->log2_min_tb_size,
  153|         .max_transform_hierarchy_depth_inter          = sps->max_transform_hierarchy_depth_inter,
  154|         .max_transform_hierarchy_depth_intra          = sps->max_transform_hierarchy_depth_intra,
  155|         .num_short_term_ref_pic_sets                  = sps->nb_st_rps,
  156|         .num_long_term_ref_pic_sps                    = sps->num_long_term_ref_pics_sps,
  157|         .num_ref_idx_l0_default_active_minus1         = pps->num_ref_idx_l0_default_active - 1,
  158|         .num_ref_idx_l1_default_active_minus1         = pps->num_ref_idx_l1_default_active - 1,
  159|         .init_qp_minus26                              = pps->pic_init_qp_minus26,
  160|         .pps_cb_qp_offset                             = pps->cb_qp_offset,
  161|         .pps_cr_qp_offset                             = pps->cr_qp_offset,
  162|         .pcm_sample_bit_depth_luma_minus1             = sps->pcm.bit_depth - 1,
  163|         .pcm_sample_bit_depth_chroma_minus1           = sps->pcm.bit_depth_chroma - 1,
  164|         .log2_min_pcm_luma_coding_block_size_minus3   = sps->pcm.log2_min_pcm_cb_size - 3,
  165|         .log2_diff_max_min_pcm_luma_coding_block_size = sps->pcm.log2_max_pcm_cb_size - sps->pcm.log2_min_pcm_cb_size,
  166|         .diff_cu_qp_delta_depth                       = pps->diff_cu_qp_delta_depth,
  167|         .pps_beta_offset_div2                         = pps->beta_offset / 2,
  168|         .pps_tc_offset_div2                           = pps->tc_offset / 2,
  169|         .log2_parallel_merge_level_minus2             = pps->log2_parallel_merge_level - 2,
  170|         .bit_depth_luma_minus8                        = sps->bit_depth - 8,
  171|         .bit_depth_chroma_minus8                      = sps->bit_depth - 8,
  172|         .log2_max_pic_order_cnt_lsb_minus4            = sps->log2_max_poc_lsb - 4,
  173|         .num_extra_slice_header_bits                  = pps->num_extra_slice_header_bits,
  174|         .pic_fields.bits = {
  175|             .chroma_format_idc                          = sps->chroma_format_idc,
  176|             .tiles_enabled_flag                         = pps->tiles_enabled_flag,
  177|             .separate_colour_plane_flag                 = sps->separate_colour_plane,
  178|             .pcm_enabled_flag                           = sps->pcm_enabled,
  179|             .scaling_list_enabled_flag                  = sps->scaling_list_enabled,
  180|             .transform_skip_enabled_flag                = pps->transform_skip_enabled_flag,
  181|             .amp_enabled_flag                           = sps->amp_enabled,
  182|             .strong_intra_smoothing_enabled_flag        = sps->strong_intra_smoothing_enabled,
  183|             .sign_data_hiding_enabled_flag              = pps->sign_data_hiding_flag,
  184|             .constrained_intra_pred_flag                = pps->constrained_intra_pred_flag,
  185|             .cu_qp_delta_enabled_flag                   = pps->cu_qp_delta_enabled_flag,
  186|             .weighted_pred_flag                         = pps->weighted_pred_flag,
  187|             .weighted_bipred_flag                       = pps->weighted_bipred_flag,
  188|             .transquant_bypass_enabled_flag             = pps->transquant_bypass_enable_flag,
  189|             .entropy_coding_sync_enabled_flag           = pps->entropy_coding_sync_enabled_flag,
  190|             .pps_loop_filter_across_slices_enabled_flag = pps->seq_loop_filter_across_slices_enabled_flag,
  191|             .loop_filter_across_tiles_enabled_flag      = pps->loop_filter_across_tiles_enabled_flag,
  192|             .pcm_loop_filter_disabled_flag              = sps->pcm_loop_filter_disabled,
  193|         },
  194|         .slice_parsing_fields.bits = {
  195|             .lists_modification_present_flag             = pps->lists_modification_present_flag,
  196|             .long_term_ref_pics_present_flag             = sps->long_term_ref_pics_present,
  197|             .sps_temporal_mvp_enabled_flag               = sps->temporal_mvp_enabled,
  198|             .cabac_init_present_flag                     = pps->cabac_init_present_flag,
  199|             .output_flag_present_flag                    = pps->output_flag_present_flag,
  200|             .dependent_slice_segments_enabled_flag       = pps->dependent_slice_segments_enabled_flag,
  201|             .pps_slice_chroma_qp_offsets_present_flag    = pps->pic_slice_level_chroma_qp_offsets_present_flag,
  202|             .sample_adaptive_offset_enabled_flag         = sps->sao_enabled,
  203|             .deblocking_filter_override_enabled_flag     = pps->deblocking_filter_override_enabled_flag,
  204|             .pps_disable_deblocking_filter_flag          = pps->disable_dbf,
  205|             .slice_segment_header_extension_present_flag = pps->slice_header_extension_present_flag,
  206|             .RapPicFlag                                  = IS_IRAP(h),
  207|             .IdrPicFlag                                  = IS_IDR(h),
  208|             .IntraPicFlag                                = IS_IRAP(h),
  209|         },
  210|     };
  211| 
  212|     fill_vaapi_pic(&pic_param->CurrPic, h->cur_frame, 0);
  213|     fill_vaapi_reference_frames(h, l, pic_param);
  214| 
  215|     if (pps->tiles_enabled_flag) {
  216|         pic_param->num_tile_columns_minus1 = pps->num_tile_columns - 1;
  217|         pic_param->num_tile_rows_minus1    = pps->num_tile_rows - 1;
  218| 
  219|         for (i = 0; i < pps->num_tile_columns; i++)
  220|             pic_param->column_width_minus1[i] = pps->column_width[i] - 1;
  221| 
  222|         for (i = 0; i < pps->num_tile_rows; i++)
  223|             pic_param->row_height_minus1[i] = pps->row_height[i] - 1;
  224|     }
  225| 
  226|     if (h->sh.short_term_ref_pic_set_sps_flag == 0 && h->sh.short_term_rps) {
  227|         pic_param->st_rps_bits = h->sh.short_term_ref_pic_set_size;
  228|     } else {
  229|         pic_param->st_rps_bits = 0;
  230|     }
  231| 
  232| #if VA_CHECK_VERSION(1, 2, 0)
  233|     if (avctx->profile == AV_PROFILE_HEVC_REXT ||
  234|         avctx->profile == AV_PROFILE_HEVC_SCC) {
  235|         pic->pic_param.rext = (VAPictureParameterBufferHEVCRext) {
  236|             .range_extension_pic_fields.bits  = {
  237|                 .transform_skip_rotation_enabled_flag       = sps->transform_skip_rotation_enabled,
  238|                 .transform_skip_context_enabled_flag        = sps->transform_skip_context_enabled,
  239|                 .implicit_rdpcm_enabled_flag                = sps->implicit_rdpcm_enabled,
  240|                 .explicit_rdpcm_enabled_flag                = sps->explicit_rdpcm_enabled,
  241|                 .extended_precision_processing_flag         = sps->extended_precision_processing,
  242|                 .intra_smoothing_disabled_flag              = sps->intra_smoothing_disabled,
  243|                 .high_precision_offsets_enabled_flag        = sps->high_precision_offsets_enabled,
  244|                 .persistent_rice_adaptation_enabled_flag    = sps->persistent_rice_adaptation_enabled,
  245|                 .cabac_bypass_alignment_enabled_flag        = sps->cabac_bypass_alignment_enabled,
  246|                 .cross_component_prediction_enabled_flag    = pps->cross_component_prediction_enabled_flag,
  247|                 .chroma_qp_offset_list_enabled_flag         = pps->chroma_qp_offset_list_enabled_flag,
  248|             },
  249|             .diff_cu_chroma_qp_offset_depth                 = pps->diff_cu_chroma_qp_offset_depth,
  250|             .chroma_qp_offset_list_len_minus1               = pps->chroma_qp_offset_list_len_minus1,
  251|             .log2_sao_offset_scale_luma                     = pps->log2_sao_offset_scale_luma,
  252|             .log2_sao_offset_scale_chroma                   = pps->log2_sao_offset_scale_chroma,
  253|             .log2_max_transform_skip_block_size_minus2      = pps->log2_max_transform_skip_block_size - 2,
  254|         };
  255| 
  256|         for (i = 0; i < 6; i++)
  257|             pic->pic_param.rext.cb_qp_offset_list[i]        = pps->cb_qp_offset_list[i];
  258|         for (i = 0; i < 6; i++)
  259|             pic->pic_param.rext.cr_qp_offset_list[i]        = pps->cr_qp_offset_list[i];
  260|     }
  261| 
  262|     pre_palette_size = pps->pps_palette_predictor_initializers_present_flag ?
  263|                        pps->pps_num_palette_predictor_initializers :
  264|                        (sps->palette_predictor_initializers_present ?
  265|                        sps->sps_num_palette_predictor_initializers :
  266|                        0);
  267| 
  268|     if (avctx->profile == AV_PROFILE_HEVC_SCC) {
  269|         pic->pic_param.scc = (VAPictureParameterBufferHEVCScc) {
  270|             .screen_content_pic_fields.bits = {
  271|                 .pps_curr_pic_ref_enabled_flag              = pps->pps_curr_pic_ref_enabled_flag,
  272|                 .palette_mode_enabled_flag                  = sps->palette_mode_enabled,
  273|                 .motion_vector_resolution_control_idc       = sps->motion_vector_resolution_control_idc,
  274|                 .intra_boundary_filtering_disabled_flag     = sps->intra_boundary_filtering_disabled,
  275|                 .residual_adaptive_colour_transform_enabled_flag
  276|                                                             = pps->residual_adaptive_colour_transform_enabled_flag,
  277|                 .pps_slice_act_qp_offsets_present_flag      = pps->pps_slice_act_qp_offsets_present_flag,
  278|             },
  279|             .palette_max_size                               = sps->palette_max_size,
  280|             .delta_palette_max_predictor_size               = sps->delta_palette_max_predictor_size,
  281|             .predictor_palette_size                         = pre_palette_size,
  282|             .pps_act_y_qp_offset_plus5                      = pps->residual_adaptive_colour_transform_enabled_flag ?
  283|                                                               pps->pps_act_y_qp_offset + 5 : 0,
  284|             .pps_act_cb_qp_offset_plus5                     = pps->residual_adaptive_colour_transform_enabled_flag ?
  285|                                                               pps->pps_act_cb_qp_offset + 5 : 0,
  286|             .pps_act_cr_qp_offset_plus3                     = pps->residual_adaptive_colour_transform_enabled_flag ?
  287|                                                               pps->pps_act_cr_qp_offset + 3 : 0,
  288|         };
  289| 
  290|         num_comps = pps->monochrome_palette_flag ? 1 : 3;
  291|         for (int comp = 0; comp < num_comps; comp++)
  292|             for (int j = 0; j < pre_palette_size; j++)
  293|                 pic->pic_param.scc.predictor_palette_entries[comp][j] =
  294|                     pps->pps_palette_predictor_initializers_present_flag ?
  295|                     pps->pps_palette_predictor_initializer[comp][j]:
  296|                     sps->sps_palette_predictor_initializer[comp][j];
  297|     }
  298| 
  299| #endif
  300|     pic_param_size = avctx->profile >= AV_PROFILE_HEVC_REXT ?
  301|                             sizeof(pic->pic_param) : sizeof(VAPictureParameterBufferHEVC);
  302| 
  303|     err = ff_vaapi_decode_make_param_buffer(avctx, &pic->pic,
  304|                                             VAPictureParameterBufferType,
  305|                                             &pic->pic_param, pic_param_size);
  306|     if (err < 0)
  307|         goto fail;
  308| 
  309|     if (pps->scaling_list_data_present_flag)
  310|         scaling_list = &pps->scaling_list;
  311|     else if (sps->scaling_list_enabled)
  312|         scaling_list = &sps->scaling_list;
  313| 
  314|     if (scaling_list) {
  315|         VAIQMatrixBufferHEVC iq_matrix;
  316|         int j;
  317| 
  318|         for (i = 0; i < 6; i++) {
  319|             for (j = 0; j < 16; j++)
  320|                 iq_matrix.ScalingList4x4[i][j] = scaling_list->sl[0][i][j];
  321|             for (j = 0; j < 64; j++) {
  322|                 iq_matrix.ScalingList8x8[i][j]   = scaling_list->sl[1][i][j];
  323|                 iq_matrix.ScalingList16x16[i][j] = scaling_list->sl[2][i][j];
  324|                 if (i < 2)
  325|                     iq_matrix.ScalingList32x32[i][j] = scaling_list->sl[3][i * 3][j];
  326|             }
  327|             iq_matrix.ScalingListDC16x16[i] = scaling_list->sl_dc[0][i];
  328|             if (i < 2)
  329|                 iq_matrix.ScalingListDC32x32[i] = scaling_list->sl_dc[1][i * 3];
  330|         }
  331| 
  332|         err = ff_vaapi_decode_make_param_buffer(avctx, &pic->pic,
  333|                                                 VAIQMatrixBufferType,
  334|                                                 &iq_matrix, sizeof(iq_matrix));
  335|         if (err < 0)
  336|             goto fail;
  337|     }
  338| 
  339|     return 0;
  340| 
  341| fail:
  342|     ff_vaapi_decode_cancel(avctx, &pic->pic);
  343|     return err;
  344| }
```

### Turn 5  _(tok 9017+127, stop=tool_use)_

**Reasoning:** vaapi_hevc_start_frame does not call ff_hevc_frame_nb_refs in this version. But it calls fill_vaapi_reference_frames, which might compute NumPocTotalCurr. Let me check fill_vaapi_reference_frames.

Actually in this version, the pic_param doesn't set NumPocTotalCurr at all? Hmm, VAPictureParameterBufferHEVC requires NumPocTotalCurr. Maybe fill_vaapi_reference_frames sets it. Let me check.

- `get_function_source(name=fill_vaapi_reference_frames)` →

```
fill_vaapi_reference_frames (function, old version) — libavcodec/vaapi_hevc.c:99-122
   99| static void fill_vaapi_reference_frames(const HEVCContext *h, const HEVCLayerContext *l,
  100|                                         VAPictureParameterBufferHEVC *pp)
  101| {
  102|     const HEVCFrame *current_picture = h->cur_frame;
  103|     int i, j, rps_type;
  104| 
  105|     for (i = 0, j = 0; i < FF_ARRAY_ELEMS(pp->ReferenceFrames); i++) {
  106|         const HEVCFrame *frame = NULL;
  107| 
  108|         while (!frame && j < FF_ARRAY_ELEMS(l->DPB)) {
  109|             if ((&l->DPB[j] != current_picture || h->pps->pps_curr_pic_ref_enabled_flag) &&
  110|                 (l->DPB[j].flags & (HEVC_FRAME_FLAG_LONG_REF | HEVC_FRAME_FLAG_SHORT_REF)))
  111|                 frame = &l->DPB[j];
  112|             j++;
  113|         }
  114| 
  115|         init_vaapi_pic(&pp->ReferenceFrames[i]);
  116| 
  117|         if (frame) {
  118|             rps_type = find_frame_rps_type(h, frame);
  119|             fill_vaapi_pic(&pp->ReferenceFrames[i], frame, rps_type);
  120|         }
  121|     }
  122| }
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 7860+189, stop=tool_use, forced)_

**Reasoning:** Budget exhausted. Based on evidence: 3 callers found by gtags: hls_slice_header (hevcdec.c), nvdec_hevc_start_frame (nvdec_hevc.c), vdpau_hevc_start_frame (vdpau_hevc.c). I checked vaapi_hevc.c and it doesn't call it. Submit.


- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

