# Impact-analysis transcript — ffmpeg @ 8a4accc24dca — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `mpeg_get_qscale` (libavcodec/mpegvideodec.h), arity 1->2
- truth: [['libavcodec/mpeg12dec.c', 'ipu_decode_frame'], ['libavcodec/mpeg12dec.c', 'mpeg_decode_mb'], ['libavcodec/mpeg12dec.c', 'mpeg_decode_slice'], ['libavcodec/mpeg4videodec.c', 'ff_mpeg4_decode_studio_slice_header'], ['libavcodec/mpeg4videodec.c', 'mpeg4_decode_studio_mb']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1075+81, stop=tool_use)_

**Reasoning:** Let me start by looking at the repository.


- `find_references(name=mpeg_get_qscale)` →

```
7 references
mpeg_get_qscale   482 libavcodec/mpeg12dec.c             s->qscale = mpeg_get_qscale(s);
mpeg_get_qscale   540 libavcodec/mpeg12dec.c                 s->qscale = mpeg_get_qscale(s);
mpeg_get_qscale   561 libavcodec/mpeg12dec.c                 s->qscale = mpeg_get_qscale(s);
mpeg_get_qscale  1373 libavcodec/mpeg12dec.c     s->qscale = mpeg_get_qscale(s);
mpeg_get_qscale  2808 libavcodec/mpeg12dec.c                 m->qscale = mpeg_get_qscale(m);
mpeg_get_qscale   826 libavcodec/mpeg4videodec.c             h->c.qscale = mpeg_get_qscale(&h->c);
mpeg_get_qscale  2371 libavcodec/mpeg4videodec.c             h->c.qscale = mpeg_get_qscale(&h->c);
```

- `grep(pattern=mpeg_get_qscale, version=old)` →

```
8 matches
libavcodec/mpeg12dec.c:482:            s->qscale = mpeg_get_qscale(s);
libavcodec/mpeg12dec.c:540:                s->qscale = mpeg_get_qscale(s);
libavcodec/mpeg12dec.c:561:                s->qscale = mpeg_get_qscale(s);
libavcodec/mpeg12dec.c:1373:    s->qscale = mpeg_get_qscale(s);
libavcodec/mpeg12dec.c:2808:                m->qscale = mpeg_get_qscale(m);
libavcodec/mpeg4videodec.c:826:            h->c.qscale = mpeg_get_qscale(&h->c);
libavcodec/mpeg4videodec.c:2371:            h->c.qscale = mpeg_get_qscale(&h->c);
libavcodec/mpegvideodec.h:80:static inline int mpeg_get_qscale(MpegEncContext *s)
```

### Turn 2  _(tok 1667+164, stop=tool_use)_

**Reasoning:** Now let's find enclosing functions. Let's read each region.


- `read_file(path=libavcodec/mpeg12dec.c, start_line=400, end_line=600, version=old)` →

```
libavcodec/mpeg12dec.c lines 400-600 of 2882
  400|     int i, j, k, cbp, val, mb_type, motion_type;
  401|     const int mb_block_count = 4 + (1 << s->chroma_format);
  402|     int ret;
  403| 
  404|     ff_tlog(s->avctx, "decode_mb: x=%d y=%d\n", s->mb_x, s->mb_y);
  405| 
  406|     av_assert2(s->mb_skipped == 0);
  407| 
  408|     if (s->mb_skip_run-- != 0) {
  409|         if (s->pict_type == AV_PICTURE_TYPE_P) {
  410|             s->mb_skipped = 1;
  411|             s->cur_pic.mb_type[s->mb_x + s->mb_y * s->mb_stride] =
  412|                 MB_TYPE_SKIP | MB_TYPE_FORWARD_MV | MB_TYPE_16x16;
  413|         } else {
  414|             int mb_type;
  415| 
  416|             if (s->mb_x)
  417|                 mb_type = s->cur_pic.mb_type[s->mb_x + s->mb_y * s->mb_stride - 1];
  418|             else
  419|                 // FIXME not sure if this is allowed in MPEG at all
  420|                 mb_type = s->cur_pic.mb_type[s->mb_width + (s->mb_y - 1) * s->mb_stride - 1];
  421|             if (IS_INTRA(mb_type)) {
  422|                 av_log(s->avctx, AV_LOG_ERROR, "skip with previntra\n");
  423|                 return AVERROR_INVALIDDATA;
  424|             }
  425|             s->cur_pic.mb_type[s->mb_x + s->mb_y * s->mb_stride] =
  426|                 mb_type | MB_TYPE_SKIP;
  427| 
  428|             if ((s->mv[0][0][0] | s->mv[0][0][1] | s->mv[1][0][0] | s->mv[1][0][1]) == 0)
  429|                 s->mb_skipped = 1;
  430|         }
  431| 
  432|         return 0;
  433|     }
  434| 
  435|     switch (s->pict_type) {
  436|     default:
  437|     case AV_PICTURE_TYPE_I:
  438|         if (get_bits1(&s->gb) == 0) {
  439|             if (get_bits1(&s->gb) == 0) {
  440|                 av_log(s->avctx, AV_LOG_ERROR,
  441|                        "Invalid mb type in I-frame at %d %d\n",
  442|                        s->mb_x, s->mb_y);
  443|                 return AVERROR_INVALIDDATA;
  444|             }
  445|             mb_type = MB_TYPE_QUANT | MB_TYPE_INTRA;
  446|         } else {
  447|             mb_type = MB_TYPE_INTRA;
  448|         }
  449|         break;
  450|     case AV_PICTURE_TYPE_P:
  451|         mb_type = get_vlc2(&s->gb, ff_mb_ptype_vlc, MB_PTYPE_VLC_BITS, 1);
  452|         if (mb_type < 0) {
  453|             av_log(s->avctx, AV_LOG_ERROR,
  454|                    "Invalid mb type in P-frame at %d %d\n", s->mb_x, s->mb_y);
  455|             return AVERROR_INVALIDDATA;
  456|         }
  457|         break;
  458|     case AV_PICTURE_TYPE_B:
  459|         mb_type = get_vlc2(&s->gb, ff_mb_btype_vlc, MB_BTYPE_VLC_BITS, 1);
  460|         if (mb_type < 0) {
  461|             av_log(s->avctx, AV_LOG_ERROR,
  462|                    "Invalid mb type in B-frame at %d %d\n", s->mb_x, s->mb_y);
  463|             return AVERROR_INVALIDDATA;
  464|         }
  465|         break;
  466|     }
  467|     ff_tlog(s->avctx, "mb_type=%x\n", mb_type);
  468| //    motion_type = 0; /* avoid warning */
  469|     if (IS_INTRA(mb_type)) {
  470|         s->bdsp.clear_blocks(s->block[0]);
  471| 
  472|         if (!s->chroma_y_shift)
  473|             s->bdsp.clear_blocks(s->block[6]);
  474| 
  475|         /* compute DCT type */
  476|         // FIXME: add an interlaced_dct coded var?
  477|         if (s->picture_structure == PICT_FRAME &&
  478|             !s->frame_pred_frame_dct)
  479|             s->interlaced_dct = get_bits1(&s->gb);
  480| 
  481|         if (IS_QUANT(mb_type))
  482|             s->qscale = mpeg_get_qscale(s);
  483| 
  484|         if (s->concealment_motion_vectors) {
  485|             /* just parse them */
  486|             if (s->picture_structure != PICT_FRAME)
  487|                 skip_bits1(&s->gb);  /* field select */
  488| 
  489|             s->mv[0][0][0]      =
  490|             s->last_mv[0][0][0] =
  491|             s->last_mv[0][1][0] = mpeg_decode_motion(s, s->mpeg_f_code[0][0],
  492|                                                      s->last_mv[0][0][0]);
  493|             s->mv[0][0][1]      =
  494|             s->last_mv[0][0][1] =
  495|             s->last_mv[0][1][1] = mpeg_decode_motion(s, s->mpeg_f_code[0][1],
  496|                                                      s->last_mv[0][0][1]);
  497| 
  498|             check_marker(s->avctx, &s->gb, "after concealment_motion_vectors");
  499|         } else {
  500|             /* reset mv prediction */
  501|             memset(s->last_mv, 0, sizeof(s->last_mv));
  502|         }
  503|         s->mb_intra = 1;
  504| 
  505|         if (s->codec_id == AV_CODEC_ID_MPEG2VIDEO) {
  506|             for (i = 0; i < mb_block_count; i++)
  507|                 if ((ret = mpeg2_decode_block_intra(s, s->block[i], i)) < 0)
  508|                     return ret;
  509|         } else {
  510|             for (i = 0; i < 6; i++) {
  511|                 ret = ff_mpeg1_decode_block_intra(&s->gb,
  512|                                                   s->intra_matrix,
  513|                                                   s->intra_scantable.permutated,
  514|                                                   s->last_dc, s->block[i],
  515|                                                   i, s->qscale);
  516|                 if (ret < 0) {
  517|                     av_log(s->avctx, AV_LOG_ERROR, "ac-tex damaged at %d %d\n",
  518|                            s->mb_x, s->mb_y);
  519|                     return ret;
  520|                 }
  521|             }
  522|         }
  523|     } else {
  524|         if (mb_type & MB_TYPE_ZERO_MV) {
  525|             av_assert2(mb_type & MB_TYPE_CBP);
  526| 
  527|             s->mv_dir = MV_DIR_FORWARD;
  528|             if (s->picture_structure == PICT_FRAME) {
  529|                 if (s->picture_structure == PICT_FRAME
  530|                     && !s->frame_pred_frame_dct)
  531|                     s->interlaced_dct = get_bits1(&s->gb);
  532|                 s->mv_type = MV_TYPE_16X16;
  533|             } else {
  534|                 s->mv_type            = MV_TYPE_FIELD;
  535|                 mb_type              |= MB_TYPE_INTERLACED;
  536|                 s->field_select[0][0] = s->picture_structure - 1;
  537|             }
  538| 
  539|             if (IS_QUANT(mb_type))
  540|                 s->qscale = mpeg_get_qscale(s);
  541| 
  542|             s->last_mv[0][0][0] = 0;
  543|             s->last_mv[0][0][1] = 0;
  544|             s->last_mv[0][1][0] = 0;
  545|             s->last_mv[0][1][1] = 0;
  546|             s->mv[0][0][0]      = 0;
  547|             s->mv[0][0][1]      = 0;
  548|         } else {
  549|             av_assert2(mb_type & MB_TYPE_BIDIR_MV);
  550|             // FIXME decide if MBs in field pictures are MB_TYPE_INTERLACED
  551|             /* get additional motion vector type */
  552|             if (s->picture_structure == PICT_FRAME && s->frame_pred_frame_dct) {
  553|                 motion_type = MT_FRAME;
  554|             } else {
  555|                 motion_type = get_bits(&s->gb, 2);
  556|                 if (s->picture_structure == PICT_FRAME && HAS_CBP(mb_type))
  557|                     s->interlaced_dct = get_bits1(&s->gb);
  558|             }
  559| 
  560|             if (IS_QUANT(mb_type))
  561|                 s->qscale = mpeg_get_qscale(s);
  562| 
  563|             /* motion vectors */
  564|             s->mv_dir = MB_TYPE_MV_2_MV_DIR(mb_type);
  565|             ff_tlog(s->avctx, "motion_type=%d\n", motion_type);
  566|             switch (motion_type) {
  567|             case MT_FRAME: /* or MT_16X8 */
  568|                 if (s->picture_structure == PICT_FRAME) {
  569|                     mb_type   |= MB_TYPE_16x16;
  570|                     s->mv_type = MV_TYPE_16X16;
  571|                     for (i = 0; i < 2; i++) {
  572|                         if (HAS_MV(mb_type, i)) {
  573|                             /* MT_FRAME */
  574|                             s->mv[i][0][0]      =
  575|                             s->last_mv[i][0][0] =
  576|                             s->last_mv[i][1][0] =
  577|                                 mpeg_decode_motion(s, s->mpeg_f_code[i][0],
  578|                                                    s->last_mv[i][0][0]);
  579|                             s->mv[i][0][1]      =
  580|                             s->last_mv[i][0][1] =
  581|                             s->last_mv[i][1][1] =
  582|                                 mpeg_decode_motion(s, s->mpeg_f_code[i][1],
  583|                                                    s->last_mv[i][0][1]);
  584|                             /* full_pel: only for MPEG-1 */
  585|                             if (s->full_pel[i]) {
  586|                                 s->mv[i][0][0] *= 2;
  587|                                 s->mv[i][0][1] *= 2;
  588|                             }
  589|                         }
  590|                     }
  591|                 } else {
  592|                     mb_type   |= MB_TYPE_16x8 | MB_TYPE_INTERLACED;
  593|                     s->mv_type = MV_TYPE_16X8;
  594|                     for (i = 0; i < 2; i++) {
  595|                         if (HAS_MV(mb_type, i)) {
  596|                             /* MT_16X8 */
  597|                             for (j = 0; j < 2; j++) {
  598|                                 s->field_select[i][j] = get_bits1(&s->gb);
  599|                                 for (k = 0; k < 2; k++) {
  600|                                     val = mpeg_decode_motion(s, s->mpeg_f_code[i][k],
```

- `read_file(path=libavcodec/mpeg12dec.c, start_line=1320, end_line=1400, version=old)` →

```
libavcodec/mpeg12dec.c lines 1320-1400 of 2882
 1320|         }
 1321|     }
 1322| 
 1323|     if (avctx->hwaccel) {
 1324|         if ((ret = FF_HW_CALL(avctx, start_frame, NULL, buf, buf_size)) < 0)
 1325|             return ret;
 1326|     } else if (s->codec_tag == MKTAG('V', 'C', 'R', '2')) {
 1327|         // Exchange UV
 1328|         FFSWAP(uint8_t*,  s->cur_pic.data[1],     s->cur_pic.data[2]);
 1329|         FFSWAP(ptrdiff_t, s->cur_pic.linesize[1], s->cur_pic.linesize[2]);
 1330|         if (!second_field) {
 1331|             FFSWAP(uint8_t*,  s->next_pic.data[1],     s->next_pic.data[2]);
 1332|             FFSWAP(ptrdiff_t, s->next_pic.linesize[1], s->next_pic.linesize[2]);
 1333|             FFSWAP(uint8_t*,  s->last_pic.data[1],     s->last_pic.data[2]);
 1334|             FFSWAP(ptrdiff_t, s->last_pic.linesize[1], s->last_pic.linesize[2]);
 1335|         }
 1336|     }
 1337| 
 1338|     return 0;
 1339| }
 1340| 
 1341| #define DECODE_SLICE_ERROR -1
 1342| #define DECODE_SLICE_OK     0
 1343| 
 1344| /**
 1345|  * Decode a slice.
 1346|  * MpegEncContext.mb_y must be set to the MB row from the startcode.
 1347|  * @return DECODE_SLICE_ERROR if the slice is damaged,
 1348|  *         DECODE_SLICE_OK if this slice is OK
 1349|  */
 1350| static int mpeg_decode_slice(MpegEncContext *s, int mb_y,
 1351|                              const uint8_t **buf, int buf_size)
 1352| {
 1353|     AVCodecContext *avctx = s->avctx;
 1354|     const int lowres      = s->avctx->lowres;
 1355|     const int field_pic   = s->picture_structure != PICT_FRAME;
 1356|     int ret;
 1357| 
 1358|     s->resync_mb_x =
 1359|     s->resync_mb_y = -1;
 1360| 
 1361|     av_assert0(mb_y < s->mb_height);
 1362| 
 1363|     ret = init_get_bits8(&s->gb, *buf, buf_size);
 1364|     if (ret < 0)
 1365|         return ret;
 1366| 
 1367|     if (s->codec_id != AV_CODEC_ID_MPEG1VIDEO && s->mb_height > 2800/16)
 1368|         skip_bits(&s->gb, 3);
 1369| 
 1370|     ff_mpeg1_clean_buffers(s);
 1371|     s->interlaced_dct = 0;
 1372| 
 1373|     s->qscale = mpeg_get_qscale(s);
 1374| 
 1375|     if (s->qscale == 0) {
 1376|         av_log(s->avctx, AV_LOG_ERROR, "qscale == 0\n");
 1377|         return AVERROR_INVALIDDATA;
 1378|     }
 1379| 
 1380|     /* extra slice info */
 1381|     if (skip_1stop_8data_bits(&s->gb) < 0)
 1382|         return AVERROR_INVALIDDATA;
 1383| 
 1384|     s->mb_x = 0;
 1385| 
 1386|     if (mb_y == 0 && s->codec_tag == AV_RL32("SLIF")) {
 1387|         skip_bits1(&s->gb);
 1388|     } else {
 1389|         while (get_bits_left(&s->gb) > 0) {
 1390|             int code = get_vlc2(&s->gb, ff_mbincr_vlc,
 1391|                                 MBINCR_VLC_BITS, 2);
 1392|             if (code < 0) {
 1393|                 av_log(s->avctx, AV_LOG_ERROR, "first mb_incr damaged\n");
 1394|                 return AVERROR_INVALIDDATA;
 1395|             }
 1396|             if (code >= 33) {
 1397|                 if (code == 33)
 1398|                     s->mb_x += 33;
 1399|                 /* otherwise, stuffing, nothing to do */
 1400|             } else {
```

### Turn 3  _(tok 6869+100, stop=tool_use)_

**Reasoning:** Line 1373 is in mpeg_decode_slice.

Now line 2808.


- `read_file(end_line=2830, path=libavcodec/mpeg12dec.c, start_line=2740, version=old)` →

```
libavcodec/mpeg12dec.c lines 2740-2830 of 2882
 2740|     FF_CODEC_DECODE_CB(mpeg_decode_frame),
 2741|     .p.capabilities = AV_CODEC_CAP_DRAW_HORIZ_BAND | AV_CODEC_CAP_DR1 |
 2742|                       AV_CODEC_CAP_DELAY | AV_CODEC_CAP_SLICE_THREADS,
 2743|     .caps_internal  = FF_CODEC_CAP_SKIP_FRAME_FILL_PARAM,
 2744|     .flush          = flush,
 2745|     .p.max_lowres   = 3,
 2746| };
 2747| 
 2748| typedef struct IPUContext {
 2749|     MpegEncContext m;
 2750| 
 2751|     int flags;
 2752|     DECLARE_ALIGNED(32, int16_t, block)[6][64];
 2753| } IPUContext;
 2754| 
 2755| static int ipu_decode_frame(AVCodecContext *avctx, AVFrame *frame,
 2756|                             int *got_frame, AVPacket *avpkt)
 2757| {
 2758|     IPUContext *s = avctx->priv_data;
 2759|     MpegEncContext *m = &s->m;
 2760|     GetBitContext *gb = &m->gb;
 2761|     int ret;
 2762| 
 2763|     // Check for minimal intra MB size (considering mb header, luma & chroma dc VLC, ac EOB VLC)
 2764|     if (avpkt->size*8LL < (avctx->width+15)/16 * ((avctx->height+15)/16) * (2LL + 3*4 + 2*2 + 2*6))
 2765|         return AVERROR_INVALIDDATA;
 2766| 
 2767|     ret = ff_get_buffer(avctx, frame, 0);
 2768|     if (ret < 0)
 2769|         return ret;
 2770| 
 2771|     ret = init_get_bits8(gb, avpkt->data, avpkt->size);
 2772|     if (ret < 0)
 2773|         return ret;
 2774| 
 2775|     s->flags = get_bits(gb, 8);
 2776|     m->intra_dc_precision = s->flags & 3;
 2777|     m->q_scale_type = !!(s->flags & 0x40);
 2778|     m->intra_vlc_format = !!(s->flags & 0x20);
 2779|     m->alternate_scan = !!(s->flags & 0x10);
 2780| 
 2781|     ff_permute_scantable(m->intra_scantable.permutated,
 2782|                          s->flags & 0x10 ? ff_alternate_vertical_scan : ff_zigzag_direct,
 2783|                          m->idsp.idct_permutation);
 2784| 
 2785|     m->last_dc[0] = m->last_dc[1] = m->last_dc[2] = 1 << (7 + (s->flags & 3));
 2786|     m->qscale = 1;
 2787| 
 2788|     for (int y = 0; y < avctx->height; y += 16) {
 2789|         int intraquant;
 2790| 
 2791|         for (int x = 0; x < avctx->width; x += 16) {
 2792|             if (x || y) {
 2793|                 if (!get_bits1(gb))
 2794|                     return AVERROR_INVALIDDATA;
 2795|             }
 2796|             if (get_bits1(gb)) {
 2797|                 intraquant = 0;
 2798|             } else {
 2799|                 if (!get_bits1(gb))
 2800|                     return AVERROR_INVALIDDATA;
 2801|                 intraquant = 1;
 2802|             }
 2803| 
 2804|             if (s->flags & 4)
 2805|                 skip_bits1(gb);
 2806| 
 2807|             if (intraquant)
 2808|                 m->qscale = mpeg_get_qscale(m);
 2809| 
 2810|             memset(s->block, 0, sizeof(s->block));
 2811| 
 2812|             for (int n = 0; n < 6; n++) {
 2813|                 if (s->flags & 0x80) {
 2814|                     ret = ff_mpeg1_decode_block_intra(&m->gb,
 2815|                                                       m->intra_matrix,
 2816|                                                       m->intra_scantable.permutated,
 2817|                                                       m->last_dc, s->block[n],
 2818|                                                       n, m->qscale);
 2819|                 } else {
 2820|                     ret = mpeg2_decode_block_intra(m, s->block[n], n);
 2821|                 }
 2822| 
 2823|                 if (ret < 0)
 2824|                     return ret;
 2825|             }
 2826| 
 2827|             m->idsp.idct_put(frame->data[0] + y * frame->linesize[0] + x,
 2828|                              frame->linesize[0], s->block[0]);
 2829|             m->idsp.idct_put(frame->data[0] + y * frame->linesize[0] + x + 8,
 2830|                              frame->linesize[0], s->block[1]);
```

### Turn 4  _(tok 8555+110, stop=tool_use)_

**Reasoning:** Line 2808 in ipu_decode_frame.

Now mpeg4videodec.c lines 826 and 2371.


- `read_file(end_line=840, path=libavcodec/mpeg4videodec.c, start_line=760, version=old)` →

```
libavcodec/mpeg4videodec.c lines 760-840 of 4109
  760|         skip_bits(&h->c.gb, 2); /* vop coding type */
  761|         // FIXME not rect stuff here
  762| 
  763|         if (ctx->shape != BIN_ONLY_SHAPE) {
  764|             skip_bits(&h->c.gb, 3); /* intra dc vlc threshold */
  765|             // FIXME don't just ignore everything
  766|             if (h->c.pict_type == AV_PICTURE_TYPE_S &&
  767|                 ctx->vol_sprite_usage == GMC_SPRITE) {
  768|                 if (mpeg4_decode_sprite_trajectory(ctx, &h->c.gb) < 0)
  769|                     return AVERROR_INVALIDDATA;
  770|                 av_log(h->c.avctx, AV_LOG_ERROR, "untested\n");
  771|             }
  772| 
  773|             // FIXME reduced res stuff here
  774| 
  775|             if (h->c.pict_type != AV_PICTURE_TYPE_I) {
  776|                 int f_code = get_bits(&h->c.gb, 3);       /* fcode_for */
  777|                 if (f_code == 0)
  778|                     av_log(h->c.avctx, AV_LOG_ERROR,
  779|                            "Error, video packet header damaged (f_code=0)\n");
  780|             }
  781|             if (h->c.pict_type == AV_PICTURE_TYPE_B) {
  782|                 int b_code = get_bits(&h->c.gb, 3);
  783|                 if (b_code == 0)
  784|                     av_log(h->c.avctx, AV_LOG_ERROR,
  785|                            "Error, video packet header damaged (b_code=0)\n");
  786|             }
  787|         }
  788|     }
  789|     if (ctx->new_pred)
  790|         decode_new_pred(ctx, &h->c.gb);
  791| 
  792|     return 0;
  793| }
  794| 
  795| static void reset_studio_dc_predictors(Mpeg4DecContext *const ctx)
  796| {
  797|     MPVContext *const s = &ctx->h.c;
  798|     /* Reset DC Predictors */
  799|     s->last_dc[0] =
  800|     s->last_dc[1] =
  801|     s->last_dc[2] = 1 << (s->avctx->bits_per_raw_sample + ctx->dct_precision + s->intra_dc_precision - 1);
  802| }
  803| 
  804| /**
  805|  * Decode the next video packet.
  806|  * @return <0 if something went wrong
  807|  */
  808| int ff_mpeg4_decode_studio_slice_header(H263DecContext *const h)
  809| {
  810|     Mpeg4DecContext *const ctx = h263_to_mpeg4(h);
  811|     GetBitContext *gb = &h->c.gb;
  812|     unsigned vlc_len;
  813|     uint16_t mb_num;
  814| 
  815|     if (get_bits_left(gb) >= 32 && get_bits_long(gb, 32) == SLICE_STARTCODE) {
  816|         vlc_len = av_log2(h->c.mb_width * h->c.mb_height) + 1;
  817|         mb_num = get_bits(gb, vlc_len);
  818| 
  819|         if (mb_num >= h->c.mb_num)
  820|             return AVERROR_INVALIDDATA;
  821| 
  822|         h->c.mb_x = mb_num % h->c.mb_width;
  823|         h->c.mb_y = mb_num / h->c.mb_width;
  824| 
  825|         if (ctx->shape != BIN_ONLY_SHAPE)
  826|             h->c.qscale = mpeg_get_qscale(&h->c);
  827| 
  828|         if (get_bits1(gb)) {  /* slice_extension_flag */
  829|             skip_bits1(gb);   /* intra_slice */
  830|             skip_bits1(gb);   /* slice_VOP_id_enable */
  831|             skip_bits(gb, 6); /* slice_VOP_id */
  832|             while (get_bits1(gb)) /* extra_bit_slice */
  833|                 skip_bits(gb, 8); /* extra_information_slice */
  834|         }
  835| 
  836|         reset_studio_dc_predictors(ctx);
  837|     }
  838|     else {
  839|         return AVERROR_INVALIDDATA;
  840|     }
```

### Turn 5  _(tok 10041+182, stop=tool_use)_

**Reasoning:** Note: here it's MPVContext... wait, in this repo version, `h->c` is MpegEncContext? Let's check: `reset_studio_dc_predictors` uses `MPVContext *const s = &ctx->h.c;`. Hmm, so `h->c` is MPVContext, and mpeg_get_qscale takes MpegEncContext*. Possibly MPVContext is a typedef/alias. Anyway not important.

Now line 2371.


- `read_file(end_line=2385, path=libavcodec/mpeg4videodec.c, start_line=2300, version=old)` →

```
libavcodec/mpeg4videodec.c lines 2300-2385 of 4109
 2300|     }
 2301| 
 2302|     for (int i = 0; i < height; i++) {
 2303|         output = 1 << (h->c.avctx->bits_per_raw_sample - 1);
 2304|         top = 1 << (h->c.avctx->bits_per_raw_sample - 1);
 2305| 
 2306|         for (j = 0; j < w; j++) {
 2307|             left = output;
 2308|             topleft = top;
 2309| 
 2310|             rice_prefix_code = get_unary(&h->c.gb, 1, 12);
 2311| 
 2312|             /* Escape */
 2313|             if (rice_prefix_code == 11)
 2314|                 dpcm_residual = get_bits(&h->c.gb, h->c.avctx->bits_per_raw_sample);
 2315|             else {
 2316|                 if (rice_prefix_code == 12) {
 2317|                     av_log(h->c.avctx, AV_LOG_ERROR, "Forbidden rice_prefix_code\n");
 2318|                     return AVERROR_INVALIDDATA;
 2319|                 }
 2320|                 rice_suffix_code = get_bitsz(&h->c.gb, rice_parameter);
 2321|                 dpcm_residual = (rice_prefix_code << rice_parameter) + rice_suffix_code;
 2322|             }
 2323| 
 2324|             /* Map to a signed residual */
 2325|             if (dpcm_residual & 1)
 2326|                 dpcm_residual = (-1 * dpcm_residual) >> 1;
 2327|             else
 2328|                 dpcm_residual = (dpcm_residual >> 1);
 2329| 
 2330|             if (i != 0)
 2331|                 top = macroblock[idx-w];
 2332| 
 2333|             p = left + top - topleft;
 2334|             min_left_top = FFMIN(left, top);
 2335|             if (p < min_left_top)
 2336|                 p = min_left_top;
 2337| 
 2338|             max_left_top = FFMAX(left, top);
 2339|             if (p > max_left_top)
 2340|                 p = max_left_top;
 2341| 
 2342|             p2 = (FFMIN(min_left_top, topleft) + FFMAX(max_left_top, topleft)) >> 1;
 2343|             if (p2 == p)
 2344|                 p2 = block_mean;
 2345| 
 2346|             if (p2 > p)
 2347|                 dpcm_residual *= -1;
 2348| 
 2349|             macroblock[idx++] = output = (dpcm_residual + p) & ((1 << h->c.avctx->bits_per_raw_sample) - 1);
 2350|         }
 2351|     }
 2352| 
 2353|     return 0;
 2354| }
 2355| 
 2356| static int mpeg4_decode_studio_mb(H263DecContext *const h)
 2357| {
 2358|     Mpeg4DecContext *const ctx = h263_to_mpeg4(h);
 2359|     int i;
 2360| 
 2361|     ctx->dpcm_direction = 0;
 2362| 
 2363|     /* StudioMacroblock */
 2364|     /* Assumes I-VOP */
 2365|     h->c.mb_intra = 1;
 2366|     if (get_bits1(&h->c.gb)) { /* compression_mode */
 2367|         /* DCT */
 2368|         /* macroblock_type, 1 or 2-bit VLC */
 2369|         if (!get_bits1(&h->c.gb)) {
 2370|             skip_bits1(&h->c.gb);
 2371|             h->c.qscale = mpeg_get_qscale(&h->c);
 2372|         }
 2373| 
 2374|         for (i = 0; i < mpeg4_block_count[h->c.chroma_format]; i++) {
 2375|             if (mpeg4_decode_studio_block(ctx, ctx->block32[i], i) < 0)
 2376|                 return AVERROR_INVALIDDATA;
 2377|         }
 2378|     } else {
 2379|         /* DPCM */
 2380|         check_marker(h->c.avctx, &h->c.gb, "DPCM block start");
 2381|         ctx->dpcm_direction = get_bits1(&h->c.gb) ? -1 : 1;
 2382|         for (i = 0; i < 3; i++) {
 2383|             if (mpeg4_decode_dpcm_macroblock(ctx, ctx->dpcm_macroblock[i], i) < 0)
 2384|                 return AVERROR_INVALIDDATA;
 2385|         }
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 11150+421, stop=tool_use, forced)_

**Reasoning:** We need the enclosing function for line 482, 540, 561 in mpeg12dec.c — that's mpeg_decode_mb (the function starting around line 398). Let me confirm: line 404 references "decode_mb". The function is `static int mpeg_decode_mb(MpegEncContext *s, const uint8_t *buf, int buf_size)`. Yes.

So callers:
- mpeg_decode_mb (libavcodec/mpeg12dec.c) — lines 482, 540, 561
- mpeg_decode_slice (libavcodec/mpeg12dec.c) — 1373
- ipu_decode_frame (libavcodec/mpeg12dec.c) — 2808
- ff_mpeg4_decode_studio_slice_header (libavcodec/mpeg4videodec.c) — 826
- mpeg4_decode_studio_mb (libavcodec/mpeg4videodec.c) — 2371

Should I list duplicates? The list of functions that call it — unique functions. I'll list each unique function once.


- **submit_callers** → `{"callers": [{"function": "mpeg_decode_mb", "file": "libavcodec/mpeg12dec.c"}, {"function": "mpeg_decode_slice", "file": "libavcodec/mpeg12dec.c"}, {"function": "ipu_decode_frame", "file": "libavcodec/mpeg12dec.c"}, {"function": "ff_mpeg4_decode_studio_slice_header", "file": "libavcodec/mpeg4videodec.c"}, {"function": "mpeg4_decode_studio_mb", "file": "libavcodec/mpeg4videodec.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

