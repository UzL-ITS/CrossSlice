# Impact-analysis transcript — ffmpeg @ 8a4accc24dca — anthropic:claude-haiku-5-5

- target: `mpeg_get_qscale` (libavcodec/mpegvideodec.h), arity 1->2
- truth: [['libavcodec/mpeg12dec.c', 'ipu_decode_frame'], ['libavcodec/mpeg12dec.c', 'mpeg_decode_mb'], ['libavcodec/mpeg12dec.c', 'mpeg_decode_slice'], ['libavcodec/mpeg4videodec.c', 'ff_mpeg4_decode_studio_slice_header'], ['libavcodec/mpeg4videodec.c', 'mpeg4_decode_studio_mb']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1394+150, stop=tool_use)_

**Reasoning:** I'll look up the references with find_references and then run a grep to see where the symbol is used.



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

### Turn 2  _(tok 2299+691, stop=tool_use)_

**Reasoning:** I need the enclosing functions for each call site, so I'll read the lines surrounding them.



**Says:** The index gives line numbers but not enclosing functions, so I'll read the surrounding code at each call site.

- `read_file(path=libavcodec/mpeg12dec.c, version=old, start_line=440, end_line=570)` →

```
libavcodec/mpeg12dec.c lines 440-570 of 2882
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
```

- `read_file(path=libavcodec/mpeg12dec.c, version=old, start_line=1340, end_line=1380)` →

```
libavcodec/mpeg12dec.c lines 1340-1380 of 2882
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
```

- `read_file(path=libavcodec/mpeg12dec.c, version=old, start_line=2780, end_line=2815)` →

```
libavcodec/mpeg12dec.c lines 2780-2815 of 2882
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
```

- `read_file(path=libavcodec/mpeg4videodec.c, version=old, start_line=780, end_line=830)` →

```
libavcodec/mpeg4videodec.c lines 780-830 of 4109
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
```

- `read_file(path=libavcodec/mpeg4videodec.c, version=old, start_line=2340, end_line=2375)` →

```
libavcodec/mpeg4videodec.c lines 2340-2375 of 4109
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
```

### Turn 3  _(tok 8926+620, stop=tool_use)_

**Reasoning:** I need to find the functions that enclose lines 482, 540, and 561 in mpeg12dec.c, which are probably mpeg_decode_mb or one of its variants. I also still have to locate the definitions above line 440 and the function enclosing line 2808.

I'm still trying to pin down which function sits around the 2808 line, and it may belong to a different codec entirely. The 2780s region mentions the scan permutation and intra quantization, so I'll grep mpeg12dec.c for the function definitions to check.



**Says:** I have the call-site lines. Now I need the enclosing function definitions for the mpeg12dec.c call sites.

- `grep(pattern=^[a-zA-Z_][a-zA-Z0-9_ \*]*\(|^static .*\(|^[a-z].*\)$, version=old, path_glob=libavcodec/mpeg12dec.c, max_results=200)` →

```
33 matches
libavcodec/mpeg12dec.c:98:static int mpeg_decode_motion(MpegEncContext *s, int fcode, int pred)
libavcodec/mpeg12dec.c:134:static inline int mpeg1_decode_block_inter(MpegEncContext *s,
libavcodec/mpeg12dec.c:218:static inline int mpeg2_decode_block_non_intra(MpegEncContext *s,
libavcodec/mpeg12dec.c:303:static inline int mpeg2_decode_block_intra(MpegEncContext *s,
libavcodec/mpeg12dec.c:384:static inline int get_dmv(MpegEncContext *s)
libavcodec/mpeg12dec.c:398:static int mpeg_decode_mb(MPVContext *const s)
libavcodec/mpeg12dec.c:760:static av_cold int mpeg_decode_init(AVCodecContext *avctx)
libavcodec/mpeg12dec.c:830:static enum AVPixelFormat mpeg_get_pixelformat(AVCodecContext *avctx)
libavcodec/mpeg12dec.c:853:static int mpeg_decode_postinit(AVCodecContext *avctx)
libavcodec/mpeg12dec.c:968:static int mpeg1_decode_picture(AVCodecContext *avctx, const uint8_t *buf,
libavcodec/mpeg12dec.c:1014:static void mpeg_decode_sequence_extension(Mpeg1Context *const s1,
libavcodec/mpeg12dec.c:1058:static void mpeg_decode_sequence_display_extension(Mpeg1Context *const s1,
libavcodec/mpeg12dec.c:1083:static void mpeg_decode_picture_display_extension(Mpeg1Context *const s1,
libavcodec/mpeg12dec.c:1118:static int load_matrix(MPVContext *const s, GetBitContext *const gb,
libavcodec/mpeg12dec.c:1141:static void mpeg_decode_quant_matrix_extension(MPVContext *const s,
libavcodec/mpeg12dec.c:1156:static int mpeg_decode_picture_coding_extension(Mpeg1Context *const s1,
libavcodec/mpeg12dec.c:1215:static int mpeg_field_start(Mpeg1Context *s1, const uint8_t *buf, int buf_size)
libavcodec/mpeg12dec.c:1350:static int mpeg_decode_slice(MpegEncContext *s, int mb_y,
libavcodec/mpeg12dec.c:1627:static int slice_decode_thread(AVCodecContext *c, void *arg)
libavcodec/mpeg12dec.c:1680:static int slice_end(AVCodecContext *avctx, AVFrame *pict, int *got_output)
libavcodec/mpeg12dec.c:1730:static int mpeg1_decode_sequence(AVCodecContext *avctx,
libavcodec/mpeg12dec.c:1820:static int vcr2_init_sequence(AVCodecContext *avctx)
libavcodec/mpeg12dec.c:1870:static void mpeg_set_cc_format(AVCodecContext *avctx, enum Mpeg2ClosedCaptionsFormat format,
libavcodec/mpeg12dec.c:1890:static int mpeg_decode_a53_cc(AVCodecContext *avctx,
libavcodec/mpeg12dec.c:2095:static void mpeg_decode_user_data(AVCodecContext *avctx,
libavcodec/mpeg12dec.c:2164:static int mpeg_decode_gop(AVCodecContext *avctx,
libavcodec/mpeg12dec.c:2196:static void mpeg12_execute_slice_threads(AVCodecContext *avctx,
libavcodec/mpeg12dec.c:2225:static int decode_chunks(AVCodecContext *avctx, AVFrame *picture,
libavcodec/mpeg12dec.c:2543:static int mpeg_decode_frame(AVCodecContext *avctx, AVFrame *picture,
libavcodec/mpeg12dec.c:2610:static av_cold void flush(AVCodecContext *avctx)
libavcodec/mpeg12dec.c:2621:static av_cold int mpeg_decode_end(AVCodecContext *avctx)
libavcodec/mpeg12dec.c:2755:static int ipu_decode_frame(AVCodecContext *avctx, AVFrame *frame,
libavcodec/mpeg12dec.c:2851:static av_cold int ipu_decode_init(AVCodecContext *avctx)
```

- `grep(pattern=^[a-zA-Z].*\(, version=old, path_glob=libavcodec/mpeg4videodec.c, max_results=200)` →

```
53 matches
libavcodec/mpeg4videodec.c:84:static inline Mpeg4DecContext *h263_to_mpeg4(H263DecContext *h)
libavcodec/mpeg4videodec.c:90:static void gmc1_motion(MpegEncContext *s, const Mpeg4DecContext *ctx,
libavcodec/mpeg4videodec.c:187:static void gmc_motion(MpegEncContext *s, const Mpeg4DecContext *ctx,
libavcodec/mpeg4videodec.c:245:void ff_mpeg4_mcsel_motion(MpegEncContext *s,
libavcodec/mpeg4videodec.c:260:void ff_mpeg4_decode_studio(MpegEncContext *s, uint8_t *dest_y, uint8_t *dest_cb,
libavcodec/mpeg4videodec.c:328:void ff_mpeg4_pred_ac(H263DecContext *const h, int16_t *block, int n, int dir)
libavcodec/mpeg4videodec.c:383:static inline int mpeg4_is_resync(Mpeg4DecContext *ctx)
libavcodec/mpeg4videodec.c:437:static int mpeg4_decode_sprite_trajectory(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:693:static int decode_new_pred(Mpeg4DecContext *ctx, GetBitContext *gb) {
libavcodec/mpeg4videodec.c:708:int ff_mpeg4_decode_video_packet_header(H263DecContext *const h)
libavcodec/mpeg4videodec.c:795:static void reset_studio_dc_predictors(Mpeg4DecContext *const ctx)
libavcodec/mpeg4videodec.c:808:int ff_mpeg4_decode_studio_slice_header(H263DecContext *const h)
libavcodec/mpeg4videodec.c:850:static inline int get_amv(Mpeg4DecContext *ctx, int n)
libavcodec/mpeg4videodec.c:902:static inline int mpeg4_pred_dc(MpegEncContext *s, int n, int *dir_ptr)
libavcodec/mpeg4videodec.c:940:static inline int mpeg4_get_level_dc(MpegEncContext *s, int n, int pred, int level)
libavcodec/mpeg4videodec.c:983:static inline int mpeg4_decode_dc(H263DecContext *const h, int n, int *dir_ptr)
libavcodec/mpeg4videodec.c:1031:static int mpeg4_decode_partition_a(Mpeg4DecContext *ctx)
libavcodec/mpeg4videodec.c:1223:static int mpeg4_decode_partition_b(H263DecContext *const h, int mb_count)
libavcodec/mpeg4videodec.c:1316:int ff_mpeg4_decode_partitions(H263DecContext *const h)
libavcodec/mpeg4videodec.c:1381:static inline int mpeg4_decode_block(Mpeg4DecContext *ctx, int16_t *block,
libavcodec/mpeg4videodec.c:1654:static int mpeg4_decode_partitioned_mb(H263DecContext *const h)
libavcodec/mpeg4videodec.c:1741:static int mpeg4_decode_mb(H263DecContext *const h)
libavcodec/mpeg4videodec.c:2120:static void next_start_code_studio(GetBitContext *gb)
libavcodec/mpeg4videodec.c:2156:static int mpeg4_decode_studio_block(Mpeg4DecContext *const ctx, int32_t block[64], int n)
libavcodec/mpeg4videodec.c:2271:static int mpeg4_decode_dpcm_macroblock(Mpeg4DecContext *const ctx,
libavcodec/mpeg4videodec.c:2356:static int mpeg4_decode_studio_mb(H263DecContext *const h)
libavcodec/mpeg4videodec.c:2404:static int mpeg4_decode_gop_header(MpegEncContext *s, GetBitContext *gb)
libavcodec/mpeg4videodec.c:2426:static int mpeg4_decode_profile_level(MpegEncContext *s, GetBitContext *gb, int *profile, int *level)
libavcodec/mpeg4videodec.c:2440:static int mpeg4_decode_visual_object(MpegEncContext *s, GetBitContext *gb)
libavcodec/mpeg4videodec.c:2472:static void mpeg4_load_default_matrices(MpegEncContext *s)
libavcodec/mpeg4videodec.c:2489:static int read_quant_matrix_ext(MpegEncContext *s, GetBitContext *gb)
libavcodec/mpeg4videodec.c:2538:static void extension_and_user_data(MpegEncContext *s, GetBitContext *gb, int id)
libavcodec/mpeg4videodec.c:2555:static int decode_studio_vol_header(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:2641:static int decode_vol_header(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:3011:static int decode_user_data(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:3068:static av_cold void permute_quant_matrix(uint16_t matrix[64],
libavcodec/mpeg4videodec.c:3079:static av_cold void switch_to_xvid_idct(AVCodecContext *const avctx,
libavcodec/mpeg4videodec.c:3097:void ff_mpeg4_workaround_bugs(AVCodecContext *avctx)
libavcodec/mpeg4videodec.c:3210:static int decode_vop_header(Mpeg4DecContext *ctx, GetBitContext *gb,
libavcodec/mpeg4videodec.c:3490:static void decode_smpte_tc(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:3509:static int decode_studio_vop_header(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:3555:static int decode_studiovisualobject(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:3582:int ff_mpeg4_parse_picture_header(Mpeg4DecContext *ctx, GetBitContext *gb,
libavcodec/mpeg4videodec.c:3739:int ff_mpeg4_decode_picture_header(H263DecContext *const h)
libavcodec/mpeg4videodec.c:3774:int ff_mpeg4_frame_end(AVCodecContext *avctx, const AVPacket *pkt)
libavcodec/mpeg4videodec.c:3824:static av_cold void clear_context(MpegEncContext *s)
libavcodec/mpeg4videodec.c:3859:static av_cold int update_mpvctx(MpegEncContext *s, const MpegEncContext *s1)
libavcodec/mpeg4videodec.c:3877:static int mpeg4_update_thread_context(AVCodecContext *dst,
libavcodec/mpeg4videodec.c:3931:static int mpeg4_update_thread_context_for_user(AVCodecContext *dst,
libavcodec/mpeg4videodec.c:3944:static av_cold void mpeg4_init_static(void)
libavcodec/mpeg4videodec.c:3989:static av_cold int decode_init(AVCodecContext *avctx)
libavcodec/mpeg4videodec.c:4041:static av_cold void mpeg4_flush(AVCodecContext *avctx)
libavcodec/mpeg4videodec.c:4049:static av_cold int mpeg4_close(AVCodecContext *avctx)
```

### Turn 4  _(tok 14075+620, stop=tool_use)_

**Reasoning:** I'm listing which function each line falls inside: several hits in mpeg_decode_mb, one in mpeg_decode_slice, one in ipu_decode_frame, and I'm still checking the mpeg4 one.

I'm checking the remaining hits: the mpeg4 studio slice header sits at line 808, and mpeg4_decode_studio_mb at 2356 covers line 2371. Grep only matched function definitions, including the static ones, and it found no other callers, so I think the list is complete.



- **submit_callers** → `{"callers": [{"function": "mpeg_decode_mb", "file": "libavcodec/mpeg12dec.c"}, {"function": "mpeg_decode_slice", "file": "libavcodec/mpeg12dec.c"}, {"function": "ipu_decode_frame", "file": "libavcodec/mpeg12dec.c"}, {"function": "ff_mpeg4_decode_studio_slice_header", "file": "libavcodec/mpeg4videodec.c"}, {"function": "mpeg4_decode_studio_mb", "file": "libavcodec/mpeg4videodec.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

