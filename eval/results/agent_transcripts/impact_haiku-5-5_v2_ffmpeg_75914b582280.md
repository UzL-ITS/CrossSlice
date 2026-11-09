# Impact-analysis transcript — ffmpeg @ 75914b582280 — anthropic:claude-haiku-5-5

- target: `ff_hevc_frame_nb_refs` (libavcodec/hevc/refs.c), arity 2->3
- truth: [['libavcodec/hevc/hevcdec.c', 'hls_slice_header'], ['libavcodec/nvdec_hevc.c', 'nvdec_hevc_start_frame'], ['libavcodec/vdpau_hevc.c', 'vdpau_hevc_start_frame']]

## Self-navigation arm

### Turn 1  _(tok 1234+103, stop=tool_use)_

**Reasoning:** I'll search the repo for that function name to see where it's used.



- `grep(pattern=ff_hevc_frame_nb_refs, version=old)` →

```
5 matches
libavcodec/hevc/hevcdec.c:787:            nb_refs = ff_hevc_frame_nb_refs(sh, pps);
libavcodec/hevc/hevcdec.h:618:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
libavcodec/hevc/refs.c:483:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)
libavcodec/nvdec_hevc.c:191:            .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
libavcodec/vdpau_hevc.c:209:    info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

### Turn 2  _(tok 1634+467, stop=tool_use)_

**Reasoning:** I need to locate the enclosing functions, so I'm checking hevcdec.c near line 787, nvdec_hevc.c near line 191, and vdpau_hevc.c near line 209.



**Says:** The grep gives three call sites outside the definition and prototype. I need the enclosing function for each.

- `read_file(path=libavcodec/hevc/hevcdec.c, version=old, start_line=740, end_line=800)` →

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

- `read_file(path=libavcodec/nvdec_hevc.c, version=old, start_line=150, end_line=200)` →

```
libavcodec/nvdec_hevc.c lines 150-200 of 336
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

- `read_file(path=libavcodec/vdpau_hevc.c, version=old, start_line=160, end_line=215)` →

```
libavcodec/vdpau_hevc.c lines 160-215 of 559
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

### Turn 3  _(tok 7059+457, stop=tool_use)_

**Reasoning:** I need to find the enclosing function names, so I'll search upward from these lines for the relevant function definitions.



**Says:** I still need the enclosing function names, so I'll search upward from each call site for the function headers.

- `grep(pattern=^[a-zA-Z_].*\(|^\{|^\}, version=old, path_glob=libavcodec/hevc/hevcdec.c, max_results=400)` →

```
148 matches
libavcodec/hevc/hevcdec.c:69:static void pic_arrays_free(HEVCLayerContext *l)
libavcodec/hevc/hevcdec.c:70:{
libavcodec/hevc/hevcdec.c:95:}
libavcodec/hevc/hevcdec.c:98:static int pic_arrays_init(HEVCLayerContext *l, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:99:{
libavcodec/hevc/hevcdec.c:168:}
libavcodec/hevc/hevcdec.c:170:static int pred_weight_table(SliceHeader *sh, void *logctx,
libavcodec/hevc/hevcdec.c:172:{
libavcodec/hevc/hevcdec.c:285:}
libavcodec/hevc/hevcdec.c:287:static int decode_lt_rps(const HEVCSPS *sps, LongTermRPS *rps,
libavcodec/hevc/hevcdec.c:289:{
libavcodec/hevc/hevcdec.c:342:}
libavcodec/hevc/hevcdec.c:344:static void export_stream_params(HEVCContext *s, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:345:{
libavcodec/hevc/hevcdec.c:398:}
libavcodec/hevc/hevcdec.c:400:static int export_stream_params_from_sei(HEVCContext *s)
libavcodec/hevc/hevcdec.c:401:{
libavcodec/hevc/hevcdec.c:418:}
libavcodec/hevc/hevcdec.c:420:static enum AVPixelFormat get_format(HEVCContext *s, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:421:{
libavcodec/hevc/hevcdec.c:551:}
libavcodec/hevc/hevcdec.c:553:static int set_sps(HEVCContext *s, HEVCLayerContext *l, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:554:{
libavcodec/hevc/hevcdec.c:581:}
libavcodec/hevc/hevcdec.c:583:static int hls_slice_header(SliceHeader *sh, const HEVCContext *s, GetBitContext *gb)
libavcodec/hevc/hevcdec.c:584:{
libavcodec/hevc/hevcdec.c:1006:}
libavcodec/hevc/hevcdec.c:1020:} while (0)
libavcodec/hevc/hevcdec.c:1022:static void hls_sao_param(HEVCLocalContext *lc, const HEVCLayerContext *l,
libavcodec/hevc/hevcdec.c:1025:{
libavcodec/hevc/hevcdec.c:1093:}
libavcodec/hevc/hevcdec.c:1098:static int hls_cross_component_pred(HEVCLocalContext *lc, int idx)
libavcodec/hevc/hevcdec.c:1099:{
libavcodec/hevc/hevcdec.c:1112:}
libavcodec/hevc/hevcdec.c:1114:static int hls_transform_unit(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1121:{
libavcodec/hevc/hevcdec.c:1324:}
libavcodec/hevc/hevcdec.c:1326:static void set_deblocking_bypass(uint8_t *is_pcm, const HEVCSPS *sps,
libavcodec/hevc/hevcdec.c:1328:{
libavcodec/hevc/hevcdec.c:1340:}
libavcodec/hevc/hevcdec.c:1342:static int hls_transform_tree(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1350:{
libavcodec/hevc/hevcdec.c:1424:} while (0)
libavcodec/hevc/hevcdec.c:1468:}
libavcodec/hevc/hevcdec.c:1470:static int hls_pcm_sample(HEVCLocalContext *lc, const HEVCLayerContext *l,
libavcodec/hevc/hevcdec.c:1472:{
libavcodec/hevc/hevcdec.c:1511:}
libavcodec/hevc/hevcdec.c:1529:static void luma_mc_uni(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1534:{
libavcodec/hevc/hevcdec.c:1575:}
libavcodec/hevc/hevcdec.c:1593:static void luma_mc_bi(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1599:{
libavcodec/hevc/hevcdec.c:1668:}
libavcodec/hevc/hevcdec.c:1687:static void chroma_mc_uni(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1693:{
libavcodec/hevc/hevcdec.c:1738:}
libavcodec/hevc/hevcdec.c:1757:static void chroma_mc_bi(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1762:{
libavcodec/hevc/hevcdec.c:1848:}
libavcodec/hevc/hevcdec.c:1850:static void hevc_await_progress(const HEVCContext *s, const HEVCFrame *ref,
libavcodec/hevc/hevcdec.c:1852:{
libavcodec/hevc/hevcdec.c:1858:}
libavcodec/hevc/hevcdec.c:1860:static void hevc_luma_mv_mvp_mode(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1865:{
libavcodec/hevc/hevcdec.c:1905:}
libavcodec/hevc/hevcdec.c:1907:static void hls_prediction_unit(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1912:{
libavcodec/hevc/hevcdec.c:2031:}
libavcodec/hevc/hevcdec.c:2036:static int luma_intra_pred_mode(HEVCLocalContext *lc, const HEVCLayerContext *l,
libavcodec/hevc/hevcdec.c:2040:{
libavcodec/hevc/hevcdec.c:2116:}
libavcodec/hevc/hevcdec.c:2118:static av_always_inline void set_ct_depth(const HEVCSPS *sps, uint8_t *tab_ct_depth,
libavcodec/hevc/hevcdec.c:2121:{
libavcodec/hevc/hevcdec.c:2130:}
libavcodec/hevc/hevcdec.c:2136:static void intra_prediction_unit(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:2140:{
libavcodec/hevc/hevcdec.c:2204:}
libavcodec/hevc/hevcdec.c:2206:static void intra_prediction_unit_default_value(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:2211:{
libavcodec/hevc/hevcdec.c:2229:}
libavcodec/hevc/hevcdec.c:2231:static int hls_coding_unit(HEVCLocalContext *lc, const HEVCContext *s,
libavcodec/hevc/hevcdec.c:2235:{
libavcodec/hevc/hevcdec.c:2416:}
libavcodec/hevc/hevcdec.c:2418:static int hls_coding_quadtree(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:2423:{
libavcodec/hevc/hevcdec.c:2509:}
libavcodec/hevc/hevcdec.c:2511:static void hls_decode_neighbour(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:2515:{
libavcodec/hevc/hevcdec.c:2560:}
libavcodec/hevc/hevcdec.c:2562:static int hls_decode_entry(HEVCContext *s, GetBitContext *gb)
libavcodec/hevc/hevcdec.c:2563:{
libavcodec/hevc/hevcdec.c:2614:}
libavcodec/hevc/hevcdec.c:2616:static int hls_decode_entry_wpp(AVCodecContext *avctx, void *hevc_lclist,
libavcodec/hevc/hevcdec.c:2618:{
libavcodec/hevc/hevcdec.c:2705:}
libavcodec/hevc/hevcdec.c:2707:static int hls_slice_data_wpp(HEVCContext *s, const H2645NAL *nal)
libavcodec/hevc/hevcdec.c:2708:{
libavcodec/hevc/hevcdec.c:2807:}
libavcodec/hevc/hevcdec.c:2809:static int decode_slice_data(HEVCContext *s, const HEVCLayerContext *l,
libavcodec/hevc/hevcdec.c:2811:{
libavcodec/hevc/hevcdec.c:2861:}
libavcodec/hevc/hevcdec.c:2863:static int set_side_data(HEVCContext *s)
libavcodec/hevc/hevcdec.c:2864:{
libavcodec/hevc/hevcdec.c:2949:}
libavcodec/hevc/hevcdec.c:2951:static int hevc_frame_start(HEVCContext *s, HEVCLayerContext *l)
libavcodec/hevc/hevcdec.c:2952:{
libavcodec/hevc/hevcdec.c:3096:}
libavcodec/hevc/hevcdec.c:3098:static int verify_md5(HEVCContext *s, AVFrame *frame)
libavcodec/hevc/hevcdec.c:3099:{
libavcodec/hevc/hevcdec.c:3167:static int hevc_frame_end(HEVCContext *s)
libavcodec/hevc/hevcdec.c:3168:{
libavcodec/hevc/hevcdec.c:3211:}
libavcodec/hevc/hevcdec.c:3213:static int decode_slice(HEVCContext *s, HEVCLayerContext *l,
libavcodec/hevc/hevcdec.c:3215:{
libavcodec/hevc/hevcdec.c:3259:}
libavcodec/hevc/hevcdec.c:3261:static int decode_nal_unit(HEVCContext *s, const H2645NAL *nal)
libavcodec/hevc/hevcdec.c:3262:{
libavcodec/hevc/hevcdec.c:3346:}
libavcodec/hevc/hevcdec.c:3348:static int decode_nal_units(HEVCContext *s, const uint8_t *buf, int length)
libavcodec/hevc/hevcdec.c:3349:{
libavcodec/hevc/hevcdec.c:3440:}
libavcodec/hevc/hevcdec.c:3442:static int hevc_decode_extradata(HEVCContext *s, uint8_t *buf, int length, int first)
libavcodec/hevc/hevcdec.c:3443:{
libavcodec/hevc/hevcdec.c:3467:}
libavcodec/hevc/hevcdec.c:3469:static int hevc_receive_frame(AVCodecContext *avctx, AVFrame *frame)
libavcodec/hevc/hevcdec.c:3470:{
libavcodec/hevc/hevcdec.c:3526:}
libavcodec/hevc/hevcdec.c:3528:static int hevc_ref_frame(HEVCFrame *dst, const HEVCFrame *src)
libavcodec/hevc/hevcdec.c:3529:{
libavcodec/hevc/hevcdec.c:3557:}
libavcodec/hevc/hevcdec.c:3559:static av_cold int hevc_decode_free(AVCodecContext *avctx)
libavcodec/hevc/hevcdec.c:3560:{
libavcodec/hevc/hevcdec.c:3599:}
libavcodec/hevc/hevcdec.c:3601:static av_cold int hevc_init_context(AVCodecContext *avctx)
libavcodec/hevc/hevcdec.c:3602:{
libavcodec/hevc/hevcdec.c:3641:}
libavcodec/hevc/hevcdec.c:3644:static int hevc_update_thread_context(AVCodecContext *dst,
libavcodec/hevc/hevcdec.c:3646:{
libavcodec/hevc/hevcdec.c:3719:}
libavcodec/hevc/hevcdec.c:3722:static av_cold int hevc_decode_init(AVCodecContext *avctx)
libavcodec/hevc/hevcdec.c:3723:{
libavcodec/hevc/hevcdec.c:3762:}
libavcodec/hevc/hevcdec.c:3764:static void hevc_decode_flush(AVCodecContext *avctx)
libavcodec/hevc/hevcdec.c:3765:{
libavcodec/hevc/hevcdec.c:3775:}
libavcodec/hevc/hevcdec.c:3786:};
libavcodec/hevc/hevcdec.c:3793:};
libavcodec/hevc/hevcdec.c:3843:};
```

- `grep(pattern=^[a-zA-Z_].*\(|^\{|^\}, version=old, path_glob=libavcodec/nvdec_hevc.c)` →

```
18 matches
libavcodec/nvdec_hevc.c:35:static void dpb_add(CUVIDHEVCPICPARAMS *pp, int idx, const HEVCFrame *src)
libavcodec/nvdec_hevc.c:36:{
libavcodec/nvdec_hevc.c:43:}
libavcodec/nvdec_hevc.c:45:static void fill_scaling_lists(CUVIDHEVCPICPARAMS *ppc, const HEVCContext *s)
libavcodec/nvdec_hevc.c:46:{
libavcodec/nvdec_hevc.c:70:}
libavcodec/nvdec_hevc.c:72:static int nvdec_hevc_start_frame(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:74:{
libavcodec/nvdec_hevc.c:271:}
libavcodec/nvdec_hevc.c:273:static int nvdec_hevc_decode_slice(AVCodecContext *avctx, const uint8_t *buffer,
libavcodec/nvdec_hevc.c:275:{
libavcodec/nvdec_hevc.c:298:}
libavcodec/nvdec_hevc.c:300:static int nvdec_hevc_frame_params(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:302:{
libavcodec/nvdec_hevc.c:306:}
libavcodec/nvdec_hevc.c:308:static int nvdec_hevc_decode_init(AVCodecContext *avctx) {
libavcodec/nvdec_hevc.c:321:}
libavcodec/nvdec_hevc.c:335:};
```

- `grep(pattern=^[a-zA-Z_].*\(|^\{|^\}, version=old, path_glob=libavcodec/vdpau_hevc.c)` →

```
19 matches
libavcodec/vdpau_hevc.c:34:static int vdpau_hevc_start_frame(AVCodecContext *avctx,
libavcodec/vdpau_hevc.c:36:{
libavcodec/vdpau_hevc.c:399:}
libavcodec/vdpau_hevc.c:403:static int vdpau_hevc_decode_slice(AVCodecContext *avctx,
libavcodec/vdpau_hevc.c:405:{
libavcodec/vdpau_hevc.c:419:}
libavcodec/vdpau_hevc.c:421:static int vdpau_hevc_end_frame(AVCodecContext *avctx)
libavcodec/vdpau_hevc.c:422:{
libavcodec/vdpau_hevc.c:432:}
libavcodec/vdpau_hevc.c:436:static int ptl_convert(const PTLCommon *general_ptl, H265RawProfileTierLevel *h265_raw_ptl)
libavcodec/vdpau_hevc.c:437:{
libavcodec/vdpau_hevc.c:465:}
libavcodec/vdpau_hevc.c:470:static int vdpau_hevc_parse_rext_profile(AVCodecContext *avctx, VdpDecoderProfile *vdp_profile)
libavcodec/vdpau_hevc.c:471:{
libavcodec/vdpau_hevc.c:513:}
libavcodec/vdpau_hevc.c:516:static int vdpau_hevc_init(AVCodecContext *avctx)
libavcodec/vdpau_hevc.c:517:{
libavcodec/vdpau_hevc.c:542:}
libavcodec/vdpau_hevc.c:558:};
```

### Turn 4  _(tok 13565+865, stop=tool_use)_

**Reasoning:** I'm checking which functions enclose each flagged line: hls_slice_header for hevcdec.c, nvdec_hevc_start_frame for nvdec_hevc.c, and for vdpau_hevc.c I'm double-checking whether line 209 falls inside vdpau_hevc_start_frame or a separate helper function defined earlier in the file.

I confirm all five grep matches were captured since the search stayed under truncation limits, and there's no indication of calls hidden behind macros or function pointers in untracked files. I'm satisfied line 787 lands within hls_slice_header's 583–1006 range.



**Says:** The grep found five occurrences of `ff_hevc_frame_nb_refs`. Two are the prototype and the definition, which are excluded. The three real call sites are:

- `libavcodec/hevc/hevcdec.c:787`, inside `hls_slice_header` (lines 583–1006).
- `libavcodec/nvdec_hevc.c:191`, inside `nvdec_hevc_start_frame` (lines 72–271).
- `libavcodec/vdpau_hevc.c:209`, inside `vdpau_hevc_start_frame` (lines 34–399).

Each caller's enclosing function was confirmed from the function-boundary listing.

- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3769+250, stop=tool_use)_

**Reasoning:** I'll start by checking who calls ff_hevc_frame_nb_refs, then grep to confirm.



- `get_callers(name=ff_hevc_frame_nb_refs, limit=200, rev=None)` →

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

- `grep(pattern=ff_hevc_frame_nb_refs, version=old, max_results=200)` →

```
5 matches
libavcodec/hevc/hevcdec.c:787:            nb_refs = ff_hevc_frame_nb_refs(sh, pps);
libavcodec/hevc/hevcdec.h:618:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
libavcodec/hevc/refs.c:483:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)
libavcodec/nvdec_hevc.c:191:            .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
libavcodec/vdpau_hevc.c:209:    info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

### Turn 2  _(tok 4577+317, stop=tool_use)_

**Reasoning:** The grep results confirm five matches: the prototype, definition, and three call sites, matching the callers I identified in nvdec_hevc_start_frame and vdpau_hevc_start_frame. That covers everything, so I'm ready to submit.



- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3221+146, stop=tool_use)_

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

### Turn 2  _(tok 3793+339, stop=tool_use)_

**Reasoning:** The tool shows "old" version results for the callers, but since the signature is about to change, I should check against the "work" version instead to get accurate current data.



**Says:** The callers tool reported the "old" version (the parent of the server's commit). I'll check the working tree too, in case the call sites differ.

- `get_callers(name=ff_hevc_frame_nb_refs, limit=200, rev=HEAD)` →

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

- `get_callers(name=ff_hevc_frame_nb_refs, limit=200, rev=work)` →

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

### Turn 3  _(tok 4610+476, stop=tool_use)_

**Reasoning:** The tool keeps reporting "old" regardless of revision, so I suspect it isn't honoring the work version properly. I should verify directly by checking get_context_at on the work version for each of the three call sites to confirm the calls to nvdec and vdpau actually exist there.



**Says:** All three queries return the same three callers. To confirm the call sites still exist in the working tree, I'll check each one directly.

- `get_context_at(file=libavcodec/hevc/hevcdec.c, line=787, rev=work)` →

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

- `get_context_at(file=libavcodec/nvdec_hevc.c, line=191, rev=work)` →

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

- `get_context_at(file=libavcodec/vdpau_hevc.c, line=209, rev=work)` →

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

### Turn 4  _(tok 15404+318, stop=tool_use)_

**Reasoning:** All three are confirmed in the work tree, with callers hls_slice_header, nvdec_hevc_start_frame, and vdpau_hevc_start_frame — the nvdec one is nested in a struct initializer but still counts as a call. I'm ready to submit.



**Says:** All three call sites are confirmed in the working tree. The call graph has no other callers, and the definition itself is excluded.

- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

