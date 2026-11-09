# Impact-analysis transcript — ffmpeg @ 75914b582280 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_hevc_frame_nb_refs` (libavcodec/hevc/refs.c), arity 2->3
- truth: [['libavcodec/hevc/hevcdec.c', 'hls_slice_header'], ['libavcodec/nvdec_hevc.c', 'nvdec_hevc_start_frame'], ['libavcodec/vdpau_hevc.c', 'vdpau_hevc_start_frame']]

## Self-navigation arm

### Turn 1  _(tok 949+115, stop=tool_use)_

**Reasoning:** Let me search the repository for `ff_hevc_frame_nb_refs`.


- `grep(pattern=ff_hevc_frame_nb_refs, version=old, max_results=200)` →

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

### Turn 2  _(tok 1627+307, stop=tool_use)_

**Reasoning:** The grep found only 5 matches; the grep seems reliable (git grep). Now I need the enclosing functions.

1. libavcodec/hevc/hevcdec.c:787 — find the enclosing function.
2. libavcodec/nvdec_hevc.c:191
3. libavcodec/vdpau_hevc.c:209

Let me read around these lines.


- `read_file(path=libavcodec/hevc/hevcdec.c, version=old, start_line=700, end_line=800)` →

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

- `read_file(path=libavcodec/nvdec_hevc.c, version=old, start_line=130, end_line=210)` →

```
libavcodec/nvdec_hevc.c lines 130-210 of 336
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

- `read_file(path=libavcodec/vdpau_hevc.c, version=old, start_line=150, end_line=225)` →

```
libavcodec/vdpau_hevc.c lines 150-225 of 559
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
  216|     /* Section 7.6.3.1 of the H.265/HEVC Specification defines the syntax of
  217|        the slice_segment_header. This header contains information that
  218|        some VDPAU implementations may choose to skip. The VDPAU API
  219|        requires client applications to track the number of bits used in the
  220|        slice header for structures associated with short term and long term
  221|        reference pictures. First, VDPAU requires the number of bits used by
  222|        the short_term_ref_pic_set array in the slice_segment_header. */
  223|     info->NumShortTermPictureSliceHeaderBits = sh->short_term_ref_pic_set_size;
  224|     /* Second, VDPAU requires the number of bits used for long term reference
  225|        pictures in the slice_segment_header. This is equal to the number
```

### Turn 3  _(tok 7523+163, stop=tool_use)_

**Reasoning:** Now find enclosing function names:

- hevcdec.c:787 → hls_slice_header (need to confirm start line).
- nvdec_hevc.c:191 → nvdec_hevc_start_frame (probably).
- vdpau_hevc.c:209 → vdpau_hevc_start_frame.

Let me grep function definitions.


- `grep(path_glob=libavcodec/hevc/hevcdec.c, pattern=^[a-zA-Z_].*\(|^static .*\(, version=old, max_results=200)` →

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

### Turn 4  _(tok 9386+128, stop=tool_use)_

**Reasoning:** Line 787 falls in hls_slice_header (583 - 1022). Confirmed.

Now nvdec_hevc.c and vdpau_hevc.c function boundaries.


- `grep(max_results=100, path_glob=libavcodec/nvdec_hevc.c, pattern=^[a-zA-Z_].*\(|^static .*\(, version=old)` →

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

### Turn 5  _(tok 9350+260, stop=tool_use, forced)_

**Reasoning:** nvdec_hevc.c:191 → nvdec_hevc_start_frame (72-273).

vdpau_hevc.c:209 → vdpau_hevc_start_frame (typical name). I haven't confirmed, but likely. Let me just submit with best knowledge.

Actually I should be careful about the vdpau one. The typical FFmpeg vdpau_hevc.c has `static int vdpau_hevc_start_frame(AVCodecContext *avctx, uint8_t *buffer, uint32_t buffer_size)`. Yes, that's the standard name. Line 209 within that function.

Submit.


- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2778+120, stop=tool_use)_

**Reasoning:** Let me find all call sites of `ff_hevc_frame_nb_refs`.


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

### Turn 2  _(tok 3272+292, stop=tool_use)_

**Reasoning:** The grep confirms only 5 matches total: one prototype, one definition, three call sites. But let me double check whether there are call sites through macros or wrapper functions, or in other versions. Let me check "work"/new version too — but the question asks about the current repository. The tools list_files etc. use version "old" for repository listing. Let's also check if there's any other reference e.g. via function pointer. Grep found all matches already. Let me verify the enclosing functions by checking the context at those lines.


- `get_context_at(file=libavcodec/hevc/hevcdec.c, line=787, rev=old)` →

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

- `get_context_at(file=libavcodec/nvdec_hevc.c, line=191, rev=old)` →

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

- `get_context_at(file=libavcodec/vdpau_hevc.c, line=209, rev=old)` →

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

### Turn 3  _(tok 9846+257, stop=tool_use)_

**Reasoning:** All three confirmed. Grep shows only 5 matches total (no other hidden calls, e.g., in hevcdec.c there's only one). Also check whether there might be calls via a wrapper macro. No.

Also double-check for any other file directories like libavcodec/hevc/hevcdec.c only. Also check that grep is case-sensitive with exact name — yes.

Submit.


**Says:** 

All call sites confirmed — grep found only 5 occurrences of the symbol total: the prototype (`hevcdec.h:618`), the definition (`refs.c:483`), and 3 real call sites, all verified via context analysis.



- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2355+90, stop=tool_use)_

**Reasoning:** Let me start by resolving the symbol and getting callers.


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

### Turn 2  _(tok 2750+180, stop=tool_use)_

**Reasoning:** Now let me verify the callers by checking the call sites. Also check for other potential callers, e.g., in vaapi_hevc.c, videotoolbox, or hevc_mvs... Let me check the neighborhood to see callers.

Let's check get_neighborhood for the function to see the caller list.

Also, potential callers via macro aliases? Let's check if there's a macro or inline wrapper. Let me look at the call sites in nvdec_hevc.c and vdpau_hevc.c to confirm.

Also there might be callers in libavcodec/hevc/hevcdec.c's hls_slice_header only, plus maybe in libavcodec/hevc/parser? Let me check neighborhood.


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

### Turn 3  _(tok 3145+399, stop=tool_use)_

**Reasoning:** Only 3 callers per gtags. But we should double check for other places, e.g., libavcodec/vaapi_hevc.c which computes NumPocTotalCurr — it may have its own helper. Let me verify with the work version as well and check vaapi_hevc.c. There's no grep. Let me expand function levels 1 to see if there's more.

Let me check other hwaccels: vaapi_hevc.c, videotoolbox, d3d12va_hevc.c, mediacodec? These might call it too. Let me check via get_callers on version "work" too, and also resolve for any macro named ff_hevc_frame_nb_refs.

Actually the tool returned version "old" by default apparently (rev defaults to server's commit). Let me try version work by passing rev=HEAD? Hmm, get_callers doesn't take a version param directly but takes rev. The default said "old" — odd. Anyway, both should be same.

To be thorough, let me check whether vaapi_hevc.c calls it. I can look at nvdec_hevc_start_frame's neighborhood... no. Better: check functions in vaapi_hevc.c that might call it. Let me resolve_symbol "vaapi_hevc_start_frame" and get its neighborhood to see callees.

Let me do that for a few hwaccel files: vaapi_hevc_start_frame, videotoolbox (vt_hevc_start_frame), d3d12va_hevc_start_frame, d3d11va_hevc_start_frame, and hevc_parser maybe.


- `get_neighborhood(name=vaapi_hevc_start_frame)` →

```
vaapi_hevc_start_frame — libavcodec/vaapi_hevc.c:124 [function] static int vaapi_hevc_start_frame(AVCodecContext *avctx, av_unused const uint8_t *buffer, av_unused uint32_t size)
  reads: avctx; writes: avctx*; returns: return 0; | return err;

CALLEES (8):
  ff_vaapi_get_surface_id (libavcodec/vaapi_decode.h:30): reads pic; writes -; returns return(uintptr_t)pic->data[3];
  fill_vaapi_pic (libavcodec/vaapi_h264.c:55 (1 of 2 definitions)): reads pic, pic_structure, va_pic; writes va_pic*; returns -
  fill_vaapi_reference_frames (libavcodec/vaapi_hevc.c:99): reads h, l, pp; writes pp*; returns -
  ff_vaapi_decode_make_param_buffer (libavcodec/vaapi_decode.c:34): reads avctx, data, pic, size, type; writes -; returns return AVERROR(EIO); | return 0;
  ff_vaapi_decode_cancel (libavcodec/vaapi_decode.c:233): reads avctx, pic; writes pic*; returns return 0;
  IS_IRAP [macro (1 of 2 definitions)]: #define IS_IRAP(s) ((s)->nal_unit_type >= HEVC_NAL_BLA_W_LP && (s)->nal_unit_type <= HEVC_NAL_RSV_IRAP_VCL23)
  IS_IDR [macro (1 of 3 definitions)]: #define IS_IDR(s) ((s)->nal_unit_type == HEVC_NAL_IDR_W_RADL || (s)->nal_unit_type == HEVC_NAL_IDR_N_LP)
  not defined in this repository: VA_CHECK_VERSION

CALLERS (0):
```

- `get_neighborhood(name=hls_slice_header)` →

```
hls_slice_header — libavcodec/hevc/hevcdec.c:583 [function] static int hls_slice_header(SliceHeader *sh, const HEVCContext *s, GetBitContext *gb)
  reads: gb, s, sh; writes: s*, sh*; returns: return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;

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

### Turn 4  _(tok 5159+252, stop=tool_use)_

**Reasoning:** OK. So gtags reports exactly 3 callers. Let me verify by checking videotoolbox and d3d12va / d3d11va hevc start frames, because they might also compute NumPocTotalCurr via ff_hevc_frame_nb_refs. In FFmpeg, d3d12va_hevc.c, d3d11va_hevc.c, videotoolbox (actually videotoolbox doesn't use NumPocTotalCurr), and mediacodec. Actually nvdec, vdpau use it; d3d11va_hevc.c also has NumPocTotalCurr in its fill_picture_parameters. Let me check whether those use ff_hevc_frame_nb_refs or compute on their own.

Let me check d3d11va_hevc_start_frame and d3d12va_hevc_start_frame neighborhoods.

- `get_neighborhood(name=d3d11va_hevc_start_frame)` →

```
{
  "error": "d3d11va_hevc_start_frame: no in-repo definition in old version"
}
```

- `get_neighborhood(name=d3d12va_hevc_start_frame)` →

```
d3d12va_hevc_start_frame — libavcodec/d3d12va_hevc.c:52 [function] static int d3d12va_hevc_start_frame(AVCodecContext *avctx, av_unused const uint8_t *buffer, av_unused uint32_t size)
  reads: avctx; writes: avctx*; returns: return -1; | return 0;

CALLEES (4):
  ff_dxva2_hevc_fill_picture_parameters (libavcodec/dxva2_hevc.c:60): reads avctx, ctx, pp; writes pp*; returns -
  ff_dxva2_hevc_fill_scaling_lists (libavcodec/dxva2_hevc.c:205): reads avctx, qm; writes qm*; returns -
  D3D12VA_DECODE_CONTEXT [macro]: #define D3D12VA_DECODE_CONTEXT(avctx) ((D3D12VADecodeContext *)((avctx)->internal->hwaccel_priv_data))
  av_assert0 [macro]: #define av_assert0(cond) do { \

CALLERS (0):
```

### Turn 5  _(tok 5760+92, stop=tool_use)_

**Reasoning:** dxva2_hevc fill_picture_parameters - does it call ff_hevc_frame_nb_refs? Let me check ff_dxva2_hevc_fill_picture_parameters callees.

Also check videotoolbox hevc: vt_hevc_start_frame.

Let me check both.


- `get_neighborhood(name=ff_dxva2_hevc_fill_picture_parameters)` →

```
ff_dxva2_hevc_fill_picture_parameters — libavcodec/dxva2_hevc.c:60 [function] void ff_dxva2_hevc_fill_picture_parameters(const AVCodecContext *avctx, AVDXVAContext *ctx, DXVA_PicParams_HEVC *pp)
  reads: avctx, ctx, pp; writes: pp*; returns: -

CALLEES (7):
  fill_picture_entry (libavcodec/dxva2_h264.c:44 (1 of 3 definitions)): reads flag, index, pic; writes pic*; returns -
  ff_dxva2_get_surface_index (libavcodec/dxva2.c:771): reads avctx, ctx, curr, frame; writes -; returns return ff_d3d12va_get_surface_index(avctx, (D3D12VADecodeContext *)ctx, frame, curr); | return(intptr_t)frame->data[1]; | return viewDesc.Texture2D.ArraySlice; | return i; | return 0;
  IS_IRAP [macro (1 of 2 definitions)]: #define IS_IRAP(s) ((s)->nal_unit_type >= HEVC_NAL_BLA_W_LP && (s)->nal_unit_type <= HEVC_NAL_RSV_IRAP_VCL23)
  IS_IDR [macro (1 of 3 definitions)]: #define IS_IDR(s) ((s)->nal_unit_type == HEVC_NAL_IDR_W_RADL || (s)->nal_unit_type == HEVC_NAL_IDR_N_LP)
  FF_ARRAY_ELEMS [macro (1 of 3 definitions)]: #define FF_ARRAY_ELEMS(a) (sizeof(a) / sizeof((a)[0]))
  DO_REF_LIST [macro]: #define DO_REF_LIST(ref_idx, ref_list) { \
  DXVA_CONTEXT_REPORT_ID [macro]: #define DXVA_CONTEXT_REPORT_ID(avctx, ctx) (*ff_dxva2_get_report_id(avctx, ctx))

CALLERS (2):
  d3d12va_hevc_start_frame (libavcodec/d3d12va_hevc.c:65): ff_dxva2_hevc_fill_picture_parameters(avctx, (AVDXVAContext *)ctx, &ctx_pic->pp);
  dxva2_hevc_start_frame (libavcodec/dxva2_hevc.c:378): ff_dxva2_hevc_fill_picture_parameters(avctx, ctx, &ctx_pic->pp);
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 4635+137, stop=tool_use, forced)_

**Reasoning:** dxva2 doesn't call it. So the 3 callers stand. Submit.


- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

