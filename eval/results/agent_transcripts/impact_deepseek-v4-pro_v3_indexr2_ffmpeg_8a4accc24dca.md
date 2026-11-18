# Impact-analysis transcript — ffmpeg @ 8a4accc24dca — openrouter:deepseek/deepseek-v4-pro

- target: `mpeg_get_qscale` (libavcodec/mpegvideodec.h), arity 1->2
- truth: [['libavcodec/mpeg12dec.c', 'ipu_decode_frame'], ['libavcodec/mpeg12dec.c', 'mpeg_decode_mb'], ['libavcodec/mpeg12dec.c', 'mpeg_decode_slice'], ['libavcodec/mpeg4videodec.c', 'ff_mpeg4_decode_studio_slice_header'], ['libavcodec/mpeg4videodec.c', 'mpeg4_decode_studio_mb']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1033+89, stop=tool_use)_

**Reasoning:** The user wants me to find every call site of `mpeg_get_qscale` in the repository. Let me start by using `find_references` to find all references to this function.

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

### Turn 2  _(tok 1354+739, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing functions for each of these references. Let me look at the lines around each reference to determine the enclosing function. Let me read the files at those lines.

For libavcodec/mpeg12dec.c: lines 482, 540, 561, 1373, 2808
For libavcodec/mpeg4videodec.c: lines 826, 2371

Let me read the context around each of these.

- `read_file(path=libavcodec/mpeg12dec.c, start_line=470, end_line=495, version=old)` →

```
libavcodec/mpeg12dec.c lines 470-495 of 2882
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
```

- `read_file(path=libavcodec/mpeg12dec.c, start_line=528, end_line=555, version=old)` →

```
libavcodec/mpeg12dec.c lines 528-555 of 2882
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
```

- `read_file(path=libavcodec/mpeg12dec.c, start_line=550, end_line=575, version=old)` →

```
libavcodec/mpeg12dec.c lines 550-575 of 2882
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
```

- `read_file(path=libavcodec/mpeg12dec.c, start_line=1360, end_line=1390, version=old)` →

```
libavcodec/mpeg12dec.c lines 1360-1390 of 2882
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
```

- `read_file(path=libavcodec/mpeg12dec.c, start_line=2795, end_line=2825, version=old)` →

```
libavcodec/mpeg12dec.c lines 2795-2825 of 2882
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
```

- `read_file(path=libavcodec/mpeg4videodec.c, start_line=814, end_line=840, version=old)` →

```
libavcodec/mpeg4videodec.c lines 814-840 of 4109
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

- `read_file(path=libavcodec/mpeg4videodec.c, start_line=2358, end_line=2385, version=old)` →

```
libavcodec/mpeg4videodec.c lines 2358-2385 of 4109
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

### Turn 3  _(tok 5232+368, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing function for each reference. Let me search for function definitions that contain these lines. Let me look at the context around each reference to find the function name.

For mpeg12dec.c:
- Line 482: I need to find the enclosing function. Let me look upwards for a function definition.
- Line 540: same
- Line 561: same
- Line 1373: same
- Line 2808: same

For mpeg4videodec.c:
- Line 826: same
- Line 2371: same

Let me search for function definitions in these files.

Let me find the enclosing functions by looking at the function definitions near these lines.

- `grep(pattern=^(static\s+)?\w+\s+\w+\(, path_glob=libavcodec/mpeg12dec.c, max_results=50, version=old)` →

```
24 matches
libavcodec/mpeg12dec.c:98:static int mpeg_decode_motion(MpegEncContext *s, int fcode, int pred)
libavcodec/mpeg12dec.c:398:static int mpeg_decode_mb(MPVContext *const s)
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
libavcodec/mpeg12dec.c:2755:static int ipu_decode_frame(AVCodecContext *avctx, AVFrame *frame,
```

- `grep(pattern=^(static\s+)?\w+\s+\w+\(, path_glob=libavcodec/mpeg4videodec.c, max_results=50, version=old)` →

```
38 matches
libavcodec/mpeg4videodec.c:90:static void gmc1_motion(MpegEncContext *s, const Mpeg4DecContext *ctx,
libavcodec/mpeg4videodec.c:187:static void gmc_motion(MpegEncContext *s, const Mpeg4DecContext *ctx,
libavcodec/mpeg4videodec.c:245:void ff_mpeg4_mcsel_motion(MpegEncContext *s,
libavcodec/mpeg4videodec.c:260:void ff_mpeg4_decode_studio(MpegEncContext *s, uint8_t *dest_y, uint8_t *dest_cb,
libavcodec/mpeg4videodec.c:328:void ff_mpeg4_pred_ac(H263DecContext *const h, int16_t *block, int n, int dir)
libavcodec/mpeg4videodec.c:437:static int mpeg4_decode_sprite_trajectory(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:693:static int decode_new_pred(Mpeg4DecContext *ctx, GetBitContext *gb) {
libavcodec/mpeg4videodec.c:708:int ff_mpeg4_decode_video_packet_header(H263DecContext *const h)
libavcodec/mpeg4videodec.c:795:static void reset_studio_dc_predictors(Mpeg4DecContext *const ctx)
libavcodec/mpeg4videodec.c:808:int ff_mpeg4_decode_studio_slice_header(H263DecContext *const h)
libavcodec/mpeg4videodec.c:1031:static int mpeg4_decode_partition_a(Mpeg4DecContext *ctx)
libavcodec/mpeg4videodec.c:1223:static int mpeg4_decode_partition_b(H263DecContext *const h, int mb_count)
libavcodec/mpeg4videodec.c:1316:int ff_mpeg4_decode_partitions(H263DecContext *const h)
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
libavcodec/mpeg4videodec.c:3097:void ff_mpeg4_workaround_bugs(AVCodecContext *avctx)
libavcodec/mpeg4videodec.c:3210:static int decode_vop_header(Mpeg4DecContext *ctx, GetBitContext *gb,
libavcodec/mpeg4videodec.c:3490:static void decode_smpte_tc(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:3509:static int decode_studio_vop_header(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:3555:static int decode_studiovisualobject(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:3582:int ff_mpeg4_parse_picture_header(Mpeg4DecContext *ctx, GetBitContext *gb,
libavcodec/mpeg4videodec.c:3739:int ff_mpeg4_decode_picture_header(H263DecContext *const h)
libavcodec/mpeg4videodec.c:3774:int ff_mpeg4_frame_end(AVCodecContext *avctx, const AVPacket *pkt)
libavcodec/mpeg4videodec.c:3877:static int mpeg4_update_thread_context(AVCodecContext *dst,
libavcodec/mpeg4videodec.c:3931:static int mpeg4_update_thread_context_for_user(AVCodecContext *dst,
```

### Turn 4  _(tok 7758+573, stop=tool_use)_

**Reasoning:** Now let me match up the references with their enclosing functions:

For libavcodec/mpeg12dec.c:
- Lines 470-495: `mpeg_decode_mb` starts at 398, let me verify. Let me also check the other references.

Let me look at the function bounds:

1. Line 482: Between `mpeg_decode_mb` (line 398) and `mpeg_decode_postinit` (line 853). So it's in `mpeg_decode_mb`.

2. Line 540: Same, between 398 and 853 → `mpeg_decode_mb`.

3. Line 561: Same, between 398 and 853 → `mpeg_decode_mb`.

4. Line 1373: Between `mpeg_decode_slice` (line 1350) and `slice_decode_thread` (line 1627). Let me verify 1350 is indeed the function start.

5. Line 2808: Between `ipu_decode_frame` (line 2755) and end of file. Let me verify.

For libavcodec/mpeg4videodec.c:
- Line 826: Between `ff_mpeg4_decode_studio_slice_header` (line 808) and `mpeg4_decode_partition_a` (line 1031). So it's `ff_mpeg4_decode_studio_slice_header`.

- Line 2371: Between `mpeg4_decode_studio_mb` (line 2356) and `mpeg4_decode_gop_header` (line 2404). So it's `mpeg4_decode_studio_mb`.

Let me verify the mpeg12dec.c function bounds.

For line 1373: `mpeg_decode_slice` starts at line 1350. Let me check what function encloses this. I see `mpeg_decode_slice` at 1350, then `slice_decode_thread` at 1627, so line 1373 is in `mpeg_decode_slice`.

For line 2808: `ipu_decode_frame` starts at 2755. The next function... looking at the grep results, there's nothing after 2755 listed. Let me check if there are more functions.

- `read_file(end_line=2760, path=libavcodec/mpeg12dec.c, start_line=2750, version=old)` →

```
libavcodec/mpeg12dec.c lines 2750-2760 of 2882
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
```

### Turn 5  _(tok 8511+168, stop=tool_use)_

**Reasoning:** Good. So line 2808 is within `ipu_decode_frame` which starts at 2755 and likely extends to the end of file at 2882.

Now let me verify the mpeg4videodec.c references:

Line 826: Let me check the function start at line 808.

- `read_file(end_line=815, path=libavcodec/mpeg4videodec.c, start_line=805, version=old)` →

```
libavcodec/mpeg4videodec.c lines 805-815 of 4109
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
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 8884+705, stop=tool_use, forced)_

**Reasoning:** Let me verify the last function before submitting. Let me check the mpeg4videodec.c line 2356:

- `mpeg4_decode_studio_mb` at line 2356 → contains line 2371.

For mpeg12dec.c:
- `mpeg_decode_mb` (398) → lines 482, 540, 561
- `mpeg_decode_slice` (1350) → line 1373
- `ipu_decode_frame` (2755) → line 2808

For mpeg4videodec.c:
- `ff_mpeg4_decode_studio_slice_header` (808) → line 826
- `mpeg4_decode_studio_mb` (2356) → line 2371

Wait, I should double-check that line 2808 in mpeg12dec.c is indeed inside `ipu_decode_frame`. Let me also verify: there is a function `mpeg_decode_postinit` at 853 and `mpeg1_decode_picture` at 968, etc. Lines 482, 540, 561 are all between 398 and 853, so they're in `mpeg_decode_mb`.

Line 1373 is between 1350 (`mpeg_decode_slice`) and 1627 (`slice_decode_thread`), so it's in `mpeg_decode_slice`.

Line 2808 is after 2755 (`ipu_decode_frame`), and there are no more function definitions listed after that, so it's in `ipu_decode_frame`.

Now I'm confident. Let me submit.

Summary:
- `mpeg_decode_mb` in `libavcodec/mpeg12dec.c` (lines 482, 540, 561)
- `mpeg_decode_slice` in `libavcodec/mpeg12dec.c` (line 1373)
- `ipu_decode_frame` in `libavcodec/mpeg12dec.c` (line 2808)
- `ff_mpeg4_decode_studio_slice_header` in `libavcodec/mpeg4videodec.c` (line 826)
- `mpeg4_decode_studio_mb` in `libavcodec/mpeg4videodec.c` (line 2371)

All five are unique functions, 3 from mpeg12dec.c and 2 from mpeg4videodec.c.

- **submit_callers** → `{"callers": [{"function": "mpeg_decode_mb", "file": "libavcodec/mpeg12dec.c"}, {"function": "mpeg_decode_slice", "file": "libavcodec/mpeg12dec.c"}, {"function": "ipu_decode_frame", "file": "libavcodec/mpeg12dec.c"}, {"function": "ff_mpeg4_decode_studio_slice_header", "file": "libavcodec/mpeg4videodec.c"}, {"function": "mpeg4_decode_studio_mb", "file": "libavcodec/mpeg4videodec.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 5, "n_truth": 5, "tp": 5, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

