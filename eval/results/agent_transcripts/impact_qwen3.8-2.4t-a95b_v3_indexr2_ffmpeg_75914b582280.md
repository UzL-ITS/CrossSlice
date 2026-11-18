# Impact-analysis transcript — ffmpeg @ 75914b582280 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_hevc_frame_nb_refs` (libavcodec/hevc/refs.c), arity 2->3
- truth: [['libavcodec/hevc/hevcdec.c', 'hls_slice_header'], ['libavcodec/nvdec_hevc.c', 'nvdec_hevc_start_frame'], ['libavcodec/vdpau_hevc.c', 'vdpau_hevc_start_frame']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1040+53, stop=tool_use)_

**Reasoning:** Let me search for all references to `ff_hevc_frame_nb_refs` to find every call site.


- `find_references(name=ff_hevc_frame_nb_refs)` →

```
4 references
ff_hevc_frame_nb_refs  787 libavcodec/hevc/hevcdec.c             nb_refs = ff_hevc_frame_nb_refs(sh, pps);
ff_hevc_frame_nb_refs  618 libavcodec/hevc/hevcdec.h int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
ff_hevc_frame_nb_refs  191 libavcodec/nvdec_hevc.c             .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
ff_hevc_frame_nb_refs  209 libavcodec/vdpau_hevc.c     info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

### Turn 2  _(tok 1315+290, stop=tool_use)_

**Reasoning:** Now I need to find enclosing functions for each call site:
1. libavcodec/hevc/hevcdec.c:787
2. libavcodec/nvdec_hevc.c:191
3. libavcodec/vdpau_hevc.c:209

Let me read around those lines.


- `read_file(path=libavcodec/hevc/hevcdec.c, start_line=700, end_line=800, version=old)` →

```
libavcodec/hevc/hevcdec.c lines 700-800 of 3844
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

- `read_file(path=libavcodec/nvdec_hevc.c, start_line=120, end_line=200, version=old)` →

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

- `read_file(path=libavcodec/vdpau_hevc.c, start_line=150, end_line=215, version=old)` →

```
libavcodec/vdpau_hevc.c lines 150-215 of 559
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

### Turn 3  _(tok 7010+202, stop=tool_use)_

**Reasoning:** Now find enclosing function names. For hevcdec.c:787 — the function containing line 787. Let's search for function definitions before line 787. It's likely `parse_slice_header` or `hls_slice_header`. Let me grep.

For nvdec_hevc.c:191 — likely `nvdec_hevc_start_frame`.
For vdpau_hevc.c:209 — likely `vdpau_hevc_start_frame`.

Let me verify by grepping for function definitions.


- `grep(pattern=^static.*\(|^[a-zA-Z_].*\(.*\)$, path_glob=libavcodec/hevc/hevcdec.c, version=old, max_results=200)` →

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

### Turn 4  _(tok 8912+204, stop=tool_use)_

**Reasoning:** hevcdec.c:787 is within hls_slice_header (starting at 583, next function at 1022). Confirmed.

Now nvdec_hevc.c:191 — find enclosing function.
And vdpau_hevc.c:209.

Let me grep both.


- `grep(path_glob=libavcodec/nvdec_hevc.c, pattern=^static.*\(|^int .*\(, version=old)` →

```
6 matches
libavcodec/nvdec_hevc.c:35:static void dpb_add(CUVIDHEVCPICPARAMS *pp, int idx, const HEVCFrame *src)
libavcodec/nvdec_hevc.c:45:static void fill_scaling_lists(CUVIDHEVCPICPARAMS *ppc, const HEVCContext *s)
libavcodec/nvdec_hevc.c:72:static int nvdec_hevc_start_frame(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:273:static int nvdec_hevc_decode_slice(AVCodecContext *avctx, const uint8_t *buffer,
libavcodec/nvdec_hevc.c:300:static int nvdec_hevc_frame_params(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:308:static int nvdec_hevc_decode_init(AVCodecContext *avctx) {
```

- `grep(path_glob=libavcodec/vdpau_hevc.c, pattern=^static.*\(|^int .*\(, version=old)` →

```
6 matches
libavcodec/vdpau_hevc.c:34:static int vdpau_hevc_start_frame(AVCodecContext *avctx,
libavcodec/vdpau_hevc.c:403:static int vdpau_hevc_decode_slice(AVCodecContext *avctx,
libavcodec/vdpau_hevc.c:421:static int vdpau_hevc_end_frame(AVCodecContext *avctx)
libavcodec/vdpau_hevc.c:436:static int ptl_convert(const PTLCommon *general_ptl, H265RawProfileTierLevel *h265_raw_ptl)
libavcodec/vdpau_hevc.c:470:static int vdpau_hevc_parse_rext_profile(AVCodecContext *avctx, VdpDecoderProfile *vdp_profile)
libavcodec/vdpau_hevc.c:516:static int vdpau_hevc_init(AVCodecContext *avctx)
```

### Turn 5  _(tok 9578+204, stop=tool_use)_

**Reasoning:** All three confirmed:
- hls_slice_header in libavcodec/hevc/hevcdec.c (line 787 within 583-1022)
- nvdec_hevc_start_frame in libavcodec/nvdec_hevc.c (line 191 within 72-273)
- vdpau_hevc_start_frame in libavcodec/vdpau_hevc.c (line 209 within 34-403)

Let me also double-check there aren't other call sites not indexed by GNU Global (e.g., function pointers, or a different grep search). Let me grep across the whole repo for "frame_nb_refs".


- `grep(max_results=100, pattern=frame_nb_refs, version=old)` →

```
5 matches
libavcodec/hevc/hevcdec.c:787:            nb_refs = ff_hevc_frame_nb_refs(sh, pps);
libavcodec/hevc/hevcdec.h:618:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
libavcodec/hevc/refs.c:483:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)
libavcodec/nvdec_hevc.c:191:            .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
libavcodec/vdpau_hevc.c:209:    info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 9476+182, stop=tool_use, forced)_

**Reasoning:** The complete list of callers:
1. hls_slice_header — libavcodec/hevc/hevcdec.c
2. nvdec_hevc_start_frame — libavcodec/nvdec_hevc.c
3. vdpau_hevc_start_frame — libavcodec/vdpau_hevc.c


- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

