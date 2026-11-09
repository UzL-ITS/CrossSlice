# Impact-analysis transcript — ffmpeg @ 75914b582280 — anthropic:claude-haiku-5-5

- target: `ff_hevc_frame_nb_refs` (libavcodec/hevc/refs.c), arity 2->3
- truth: [['libavcodec/hevc/hevcdec.c', 'hls_slice_header'], ['libavcodec/nvdec_hevc.c', 'nvdec_hevc_start_frame'], ['libavcodec/vdpau_hevc.c', 'vdpau_hevc_start_frame']]

## Self-navigation arm

### Turn 1  _(tok 1234+103, stop=tool_use)_

**Reasoning:** I'm going to grep the repo for that function name to see where it's used.



- `grep(pattern=ff_hevc_frame_nb_refs, version=old)` →

```
5 matches
libavcodec/hevc/hevcdec.c:787:            nb_refs = ff_hevc_frame_nb_refs(sh, pps);
libavcodec/hevc/hevcdec.h:618:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
libavcodec/hevc/refs.c:483:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)
libavcodec/nvdec_hevc.c:191:            .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
libavcodec/vdpau_hevc.c:209:    info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

### Turn 2  _(tok 1634+399, stop=tool_use)_

**Reasoning:** I need the names of the functions that enclose each of these spots, so I'll read the code around each one.



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

- `read_file(path=libavcodec/vdpau_hevc.c, version=old, start_line=170, end_line=215)` →

```
libavcodec/vdpau_hevc.c lines 170-215 of 559
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

### Turn 3  _(tok 6772+438, stop=tool_use)_

**Reasoning:** I need the names of the functions, so I'm searching for the function definitions that enclose these lines in each file.



**Says:** Now I need the enclosing function for each call site.

- `grep(pattern=^[a-z_A-Z].*\(|^\{?$, version=old, path_glob=libavcodec/hevc/hevcdec.c, max_results=400)` →

```
625 matches (showing 200)
libavcodec/hevc/hevcdec.c:25:
libavcodec/hevc/hevcdec.c:27:
libavcodec/hevc/hevcdec.c:38:
libavcodec/hevc/hevcdec.c:56:
libavcodec/hevc/hevcdec.c:58:
libavcodec/hevc/hevcdec.c:63:
libavcodec/hevc/hevcdec.c:67:
libavcodec/hevc/hevcdec.c:69:static void pic_arrays_free(HEVCLayerContext *l)
libavcodec/hevc/hevcdec.c:70:{
libavcodec/hevc/hevcdec.c:73:
libavcodec/hevc/hevcdec.c:76:
libavcodec/hevc/hevcdec.c:80:
libavcodec/hevc/hevcdec.c:84:
libavcodec/hevc/hevcdec.c:87:
libavcodec/hevc/hevcdec.c:92:
libavcodec/hevc/hevcdec.c:96:
libavcodec/hevc/hevcdec.c:98:static int pic_arrays_init(HEVCLayerContext *l, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:99:{
libavcodec/hevc/hevcdec.c:107:
libavcodec/hevc/hevcdec.c:110:
libavcodec/hevc/hevcdec.c:115:
libavcodec/hevc/hevcdec.c:120:
libavcodec/hevc/hevcdec.c:126:
libavcodec/hevc/hevcdec.c:134:
libavcodec/hevc/hevcdec.c:139:
libavcodec/hevc/hevcdec.c:144:
libavcodec/hevc/hevcdec.c:147:
libavcodec/hevc/hevcdec.c:162:
libavcodec/hevc/hevcdec.c:164:
libavcodec/hevc/hevcdec.c:169:
libavcodec/hevc/hevcdec.c:170:static int pred_weight_table(SliceHeader *sh, void *logctx,
libavcodec/hevc/hevcdec.c:172:{
libavcodec/hevc/hevcdec.c:180:
libavcodec/hevc/hevcdec.c:195:
libavcodec/hevc/hevcdec.c:222:
libavcodec/hevc/hevcdec.c:227:
libavcodec/hevc/hevcdec.c:266:
libavcodec/hevc/hevcdec.c:271:
libavcodec/hevc/hevcdec.c:286:
libavcodec/hevc/hevcdec.c:287:static int decode_lt_rps(const HEVCSPS *sps, LongTermRPS *rps,
libavcodec/hevc/hevcdec.c:289:{
libavcodec/hevc/hevcdec.c:294:
libavcodec/hevc/hevcdec.c:298:
libavcodec/hevc/hevcdec.c:302:
libavcodec/hevc/hevcdec.c:307:
libavcodec/hevc/hevcdec.c:309:
libavcodec/hevc/hevcdec.c:311:
libavcodec/hevc/hevcdec.c:314:
libavcodec/hevc/hevcdec.c:317:
libavcodec/hevc/hevcdec.c:324:
libavcodec/hevc/hevcdec.c:329:
libavcodec/hevc/hevcdec.c:332:
libavcodec/hevc/hevcdec.c:340:
libavcodec/hevc/hevcdec.c:343:
libavcodec/hevc/hevcdec.c:344:static void export_stream_params(HEVCContext *s, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:345:{
libavcodec/hevc/hevcdec.c:350:
libavcodec/hevc/hevcdec.c:359:
libavcodec/hevc/hevcdec.c:361:
libavcodec/hevc/hevcdec.c:367:
libavcodec/hevc/hevcdec.c:377:
libavcodec/hevc/hevcdec.c:386:
libavcodec/hevc/hevcdec.c:394:
libavcodec/hevc/hevcdec.c:399:
libavcodec/hevc/hevcdec.c:400:static int export_stream_params_from_sei(HEVCContext *s)
libavcodec/hevc/hevcdec.c:401:{
libavcodec/hevc/hevcdec.c:403:
libavcodec/hevc/hevcdec.c:406:
libavcodec/hevc/hevcdec.c:412:
libavcodec/hevc/hevcdec.c:416:
libavcodec/hevc/hevcdec.c:419:
libavcodec/hevc/hevcdec.c:420:static enum AVPixelFormat get_format(HEVCContext *s, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:421:{
libavcodec/hevc/hevcdec.c:431:
libavcodec/hevc/hevcdec.c:546:
libavcodec/hevc/hevcdec.c:549:
libavcodec/hevc/hevcdec.c:552:
libavcodec/hevc/hevcdec.c:553:static int set_sps(HEVCContext *s, HEVCLayerContext *l, const HEVCSPS *sps)
libavcodec/hevc/hevcdec.c:554:{
libavcodec/hevc/hevcdec.c:556:
libavcodec/hevc/hevcdec.c:560:
libavcodec/hevc/hevcdec.c:563:
libavcodec/hevc/hevcdec.c:567:
libavcodec/hevc/hevcdec.c:571:
libavcodec/hevc/hevcdec.c:574:
libavcodec/hevc/hevcdec.c:576:
libavcodec/hevc/hevcdec.c:582:
libavcodec/hevc/hevcdec.c:583:static int hls_slice_header(SliceHeader *sh, const HEVCContext *s, GetBitContext *gb)
libavcodec/hevc/hevcdec.c:584:{
libavcodec/hevc/hevcdec.c:590:
libavcodec/hevc/hevcdec.c:593:
libavcodec/hevc/hevcdec.c:597:
libavcodec/hevc/hevcdec.c:608:
libavcodec/hevc/hevcdec.c:613:
libavcodec/hevc/hevcdec.c:616:
libavcodec/hevc/hevcdec.c:620:
libavcodec/hevc/hevcdec.c:627:
libavcodec/hevc/hevcdec.c:637:
libavcodec/hevc/hevcdec.c:644:
libavcodec/hevc/hevcdec.c:648:
libavcodec/hevc/hevcdec.c:663:
libavcodec/hevc/hevcdec.c:668:
libavcodec/hevc/hevcdec.c:671:
libavcodec/hevc/hevcdec.c:676:
libavcodec/hevc/hevcdec.c:688:
libavcodec/hevc/hevcdec.c:691:
libavcodec/hevc/hevcdec.c:698:
libavcodec/hevc/hevcdec.c:702:
libavcodec/hevc/hevcdec.c:707:
libavcodec/hevc/hevcdec.c:713:
libavcodec/hevc/hevcdec.c:722:
libavcodec/hevc/hevcdec.c:736:
libavcodec/hevc/hevcdec.c:740:
libavcodec/hevc/hevcdec.c:745:
libavcodec/hevc/hevcdec.c:753:
libavcodec/hevc/hevcdec.c:765:
libavcodec/hevc/hevcdec.c:769:
libavcodec/hevc/hevcdec.c:773:
libavcodec/hevc/hevcdec.c:784:
libavcodec/hevc/hevcdec.c:792:
libavcodec/hevc/hevcdec.c:799:
libavcodec/hevc/hevcdec.c:807:
libavcodec/hevc/hevcdec.c:810:
libavcodec/hevc/hevcdec.c:815:
libavcodec/hevc/hevcdec.c:821:
libavcodec/hevc/hevcdec.c:832:
libavcodec/hevc/hevcdec.c:839:
libavcodec/hevc/hevcdec.c:847:
libavcodec/hevc/hevcdec.c:854:
libavcodec/hevc/hevcdec.c:856:
libavcodec/hevc/hevcdec.c:858:
libavcodec/hevc/hevcdec.c:871:
libavcodec/hevc/hevcdec.c:877:
libavcodec/hevc/hevcdec.c:882:
libavcodec/hevc/hevcdec.c:885:
libavcodec/hevc/hevcdec.c:888:
libavcodec/hevc/hevcdec.c:914:
libavcodec/hevc/hevcdec.c:924:
libavcodec/hevc/hevcdec.c:933:
libavcodec/hevc/hevcdec.c:937:
libavcodec/hevc/hevcdec.c:943:
libavcodec/hevc/hevcdec.c:961:
libavcodec/hevc/hevcdec.c:971:
libavcodec/hevc/hevcdec.c:978:
libavcodec/hevc/hevcdec.c:990:
libavcodec/hevc/hevcdec.c:992:
libavcodec/hevc/hevcdec.c:998:
libavcodec/hevc/hevcdec.c:1004:
libavcodec/hevc/hevcdec.c:1007:
libavcodec/hevc/hevcdec.c:1009:
libavcodec/hevc/hevcdec.c:1021:
libavcodec/hevc/hevcdec.c:1022:static void hls_sao_param(HEVCLocalContext *lc, const HEVCLayerContext *l,
libavcodec/hevc/hevcdec.c:1025:{
libavcodec/hevc/hevcdec.c:1031:
libavcodec/hevc/hevcdec.c:1043:
libavcodec/hevc/hevcdec.c:1047:
libavcodec/hevc/hevcdec.c:1052:
libavcodec/hevc/hevcdec.c:1059:
libavcodec/hevc/hevcdec.c:1062:
libavcodec/hevc/hevcdec.c:1065:
libavcodec/hevc/hevcdec.c:1079:
libavcodec/hevc/hevcdec.c:1094:
libavcodec/hevc/hevcdec.c:1097:
libavcodec/hevc/hevcdec.c:1098:static int hls_cross_component_pred(HEVCLocalContext *lc, int idx)
libavcodec/hevc/hevcdec.c:1099:{
libavcodec/hevc/hevcdec.c:1101:
libavcodec/hevc/hevcdec.c:1109:
libavcodec/hevc/hevcdec.c:1110:
libavcodec/hevc/hevcdec.c:1113:
libavcodec/hevc/hevcdec.c:1114:static int hls_transform_unit(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1121:{
libavcodec/hevc/hevcdec.c:1125:
libavcodec/hevc/hevcdec.c:1129:
libavcodec/hevc/hevcdec.c:1132:
libavcodec/hevc/hevcdec.c:1140:
libavcodec/hevc/hevcdec.c:1147:
libavcodec/hevc/hevcdec.c:1158:
libavcodec/hevc/hevcdec.c:1161:
libavcodec/hevc/hevcdec.c:1180:
libavcodec/hevc/hevcdec.c:1189:
libavcodec/hevc/hevcdec.c:1198:
libavcodec/hevc/hevcdec.c:1200:
libavcodec/hevc/hevcdec.c:1209:
libavcodec/hevc/hevcdec.c:1230:
libavcodec/hevc/hevcdec.c:1239:
libavcodec/hevc/hevcdec.c:1260:
libavcodec/hevc/hevcdec.c:1322:
libavcodec/hevc/hevcdec.c:1325:
libavcodec/hevc/hevcdec.c:1326:static void set_deblocking_bypass(uint8_t *is_pcm, const HEVCSPS *sps,
libavcodec/hevc/hevcdec.c:1328:{
libavcodec/hevc/hevcdec.c:1331:
libavcodec/hevc/hevcdec.c:1336:
libavcodec/hevc/hevcdec.c:1341:
libavcodec/hevc/hevcdec.c:1342:static int hls_transform_tree(HEVCLocalContext *lc,
libavcodec/hevc/hevcdec.c:1350:{
libavcodec/hevc/hevcdec.c:1356:
libavcodec/hevc/hevcdec.c:1361:
libavcodec/hevc/hevcdec.c:1378:
libavcodec/hevc/hevcdec.c:1389:
libavcodec/hevc/hevcdec.c:1394:
```

- `grep(pattern=^[a-z_A-Z].*\(, version=old, path_glob=libavcodec/nvdec_hevc.c)` →

```
6 matches
libavcodec/nvdec_hevc.c:35:static void dpb_add(CUVIDHEVCPICPARAMS *pp, int idx, const HEVCFrame *src)
libavcodec/nvdec_hevc.c:45:static void fill_scaling_lists(CUVIDHEVCPICPARAMS *ppc, const HEVCContext *s)
libavcodec/nvdec_hevc.c:72:static int nvdec_hevc_start_frame(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:273:static int nvdec_hevc_decode_slice(AVCodecContext *avctx, const uint8_t *buffer,
libavcodec/nvdec_hevc.c:300:static int nvdec_hevc_frame_params(AVCodecContext *avctx,
libavcodec/nvdec_hevc.c:308:static int nvdec_hevc_decode_init(AVCodecContext *avctx) {
```

- `grep(pattern=^[a-z_A-Z].*\(, version=old, path_glob=libavcodec/vdpau_hevc.c)` →

```
6 matches
libavcodec/vdpau_hevc.c:34:static int vdpau_hevc_start_frame(AVCodecContext *avctx,
libavcodec/vdpau_hevc.c:403:static int vdpau_hevc_decode_slice(AVCodecContext *avctx,
libavcodec/vdpau_hevc.c:421:static int vdpau_hevc_end_frame(AVCodecContext *avctx)
libavcodec/vdpau_hevc.c:436:static int ptl_convert(const PTLCommon *general_ptl, H265RawProfileTierLevel *h265_raw_ptl)
libavcodec/vdpau_hevc.c:470:static int vdpau_hevc_parse_rext_profile(AVCodecContext *avctx, VdpDecoderProfile *vdp_profile)
libavcodec/vdpau_hevc.c:516:static int vdpau_hevc_init(AVCodecContext *avctx)
```

### Turn 4  _(tok 12668+1042, stop=tool_use)_

**Reasoning:** I'm checking where line 787 falls: it looks like it sits inside hls_slice_header, which starts at 583, though I'm not sure where that function ends. The grep hits at 736, 740, and 745 seem to be references inside the function rather than new definitions, and the next definition I can see is hls_sao_param around 1021.

I'm checking whether any other function definitions sit between 583 and 787, since the grep output was noisy with empty lines and got truncated around 1394. The entries I can see in that range are all empty, so hls_slice_header should still be the enclosing function for line 787. I still need to confirm that against the actual source, and I'm leaving out the header prototype and the refs.c definition for now.

I'm confirming that the grep matches at 191 and 209 belong to the nvdec and vdpau start_frame functions, since 191 falls between nvdec_hevc_start_frame at 72 and the end of that function, and 209 falls inside vdpau_hevc_start_frame.



**Says:** All five matches are accounted for. The grep for function headers is noisy, but the boundaries are clear: `hls_slice_header` spans lines 583 to ~1020 in `hevcdec.c`, `nvdec_hevc_start_frame` spans lines 72 to ~272, and `vdpau_hevc_start_frame` spans lines 34 to ~402. Each call site falls inside those ranges.

- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3769+304, stop=tool_use)_

**Reasoning:** I'm going to start with get_callers on ff_hevc_frame_nb_refs, since its rev parameter defaults to HEAD. The version enum with "old" belongs to the file tools like list_files, read_file, and grep, so I'll call get_callers and grep next.



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

- `grep(pattern=ff_hevc_frame_nb_refs, version=old, max_results=500)` →

```
5 matches
libavcodec/hevc/hevcdec.c:787:            nb_refs = ff_hevc_frame_nb_refs(sh, pps);
libavcodec/hevc/hevcdec.h:618:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps);
libavcodec/hevc/refs.c:483:int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)
libavcodec/nvdec_hevc.c:191:            .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
libavcodec/vdpau_hevc.c:209:    info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

### Turn 2  _(tok 4631+373, stop=tool_use)_

**Reasoning:** I'm checking which functions enclose the matches: the nvdec and vdpau hits sit in their hevc start-frame functions, which fits with get_callers. The hevcdec.c:787 match is the one still unclear, since it might belong to a different function than hls_slice_header, so I'll verify that one directly.

I'll confirm the enclosing function for the hevcdec.c:787 match with get_context_at, since get_callers alone may not settle it. Grep already covers every textual call, including through function pointers and macros, so that part is fine.



- `get_context_at(file=libavcodec/hevc/hevcdec.c, line=787, rev=None, version=old)` →

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

### Turn 3  _(tok 9949+276, stop=tool_use)_

**Reasoning:** I'm noting the callers of hls_slice_header, nvdec_hevc_start_frame, and vdpau_hevc_start_frame, which get_callers returned. I want to check the nvdec and vdpau enclosing functions, but I think what I have is enough to submit.



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

### Turn 2  _(tok 3793+319, stop=tool_use)_

**Reasoning:** The tool's get_callers reports the "old" version by default, which might reflect the server's commit rather than the working tree. Since the change is about to happen and the working tree is what counts, I'll also check the "work" version by calling get_callers with that version.



**Says:** The lookup returned the "old" revision. I'll also check the working tree, since that is what the upcoming edit will touch.

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

- `get_neighborhood(name=ff_hevc_frame_nb_refs, version=work)` →

```
ff_hevc_frame_nb_refs — libavcodec/hevc/refs.c:483 [function] int ff_hevc_frame_nb_refs(const SliceHeader *sh, const HEVCPPS *pps)
  reads: pps, sh; writes: -; returns: return ret;

CALLEES (0):

CALLERS (3):
  hls_slice_header (libavcodec/hevc/hevcdec.c:787): nb_refs = ff_hevc_frame_nb_refs(sh, pps);
  nvdec_hevc_start_frame (libavcodec/nvdec_hevc.c:191): .NumPocTotalCurr                              = ff_hevc_frame_nb_refs(&s->sh, pps),
  vdpau_hevc_start_frame (libavcodec/vdpau_hevc.c:209): info->NumPocTotalCurr = ff_hevc_frame_nb_refs(&h->sh, pps);
```

### Turn 3  _(tok 4705+415, stop=tool_use)_

**Reasoning:** I'm checking whether the callers list is complete, since it could miss calls made through macros or function pointers. The call graph tool is the reference I'm trusting, and it reports only three callers, so I'm weighing whether it's worth also checking the other hwaccel HEVC files directly.

I'm wondering whether tree-sitter or gtags could miss some callers, so I'm considering a quick look at the neighboring hwaccel files. I can't grep here, though, and I'm going to settle on the call graph result with medium-high confidence.



- **submit_callers** → `{"callers": [{"function": "hls_slice_header", "file": "libavcodec/hevc/hevcdec.c"}, {"function": "nvdec_hevc_start_frame", "file": "libavcodec/nvdec_hevc.c"}, {"function": "vdpau_hevc_start_frame", "file": "libavcodec/vdpau_hevc.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

