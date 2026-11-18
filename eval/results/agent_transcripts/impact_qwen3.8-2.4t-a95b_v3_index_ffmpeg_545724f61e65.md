# Impact-analysis transcript — ffmpeg @ 545724f61e65 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_mpeg4_get_video_packet_prefix_length` (libavcodec/mpeg4video.c), arity 1->3
- truth: [['libavcodec/mpeg4videodec.c', 'ff_mpeg4_decode_video_packet_header'], ['libavcodec/mpeg4videodec.c', 'mpeg4_is_resync'], ['libavcodec/mpeg4videoenc.c', 'ff_mpeg4_encode_video_packet_header']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1046+52, stop=tool_use)_

**Reasoning:** I'll search for references to `ff_mpeg4_get_video_packet_prefix_length`.

- `find_references(name=ff_mpeg4_get_video_packet_prefix_length)` →

```
4 references
ff_mpeg4_get_video_packet_prefix_length   31 libavcodec/mpeg4video.h int ff_mpeg4_get_video_packet_prefix_length(MpegEncContext *s);
ff_mpeg4_get_video_packet_prefix_length  424 libavcodec/mpeg4videodec.c             if (len >= ff_mpeg4_get_video_packet_prefix_length(s))
ff_mpeg4_get_video_packet_prefix_length  717 libavcodec/mpeg4videodec.c     if (len != ff_mpeg4_get_video_packet_prefix_length(s)) {
ff_mpeg4_get_video_packet_prefix_length 1396 libavcodec/mpeg4videoenc.c     put_bits(&s->pb, ff_mpeg4_get_video_packet_prefix_length(&s->c), 0);
```

### Turn 2  _(tok 1325+65, stop=tool_use)_

**Reasoning:** Also check for definition and other callers via grep (in case index is incomplete).


- `grep(pattern=ff_mpeg4_get_video_packet_prefix_length, version=old)` →

```
5 matches
libavcodec/mpeg4video.c:42:int ff_mpeg4_get_video_packet_prefix_length(MpegEncContext *s)
libavcodec/mpeg4video.h:31:int ff_mpeg4_get_video_packet_prefix_length(MpegEncContext *s);
libavcodec/mpeg4videodec.c:424:            if (len >= ff_mpeg4_get_video_packet_prefix_length(s))
libavcodec/mpeg4videodec.c:717:    if (len != ff_mpeg4_get_video_packet_prefix_length(s)) {
libavcodec/mpeg4videoenc.c:1396:    put_bits(&s->pb, ff_mpeg4_get_video_packet_prefix_length(&s->c), 0);
```

### Turn 3  _(tok 1571+188, stop=tool_use)_

**Reasoning:** Now find enclosing functions for lines 424, 717 in mpeg4videodec.c and 1396 in mpeg4videoenc.c.


- `read_file(path=libavcodec/mpeg4videodec.c, start_line=380, end_line=440, version=old)` →

```
libavcodec/mpeg4videodec.c lines 380-440 of 4004
  380|     int bits_count = get_bits_count(&s->gb);
  381|     int v          = show_bits(&s->gb, 16);
  382| 
  383|     if (s->workaround_bugs & FF_BUG_NO_PADDING && !ctx->resync_marker)
  384|         return 0;
  385| 
  386|     while (v <= 0xFF) {
  387|         if (s->pict_type == AV_PICTURE_TYPE_B ||
  388|             (v >> (8 - s->pict_type) != 1) || s->partitioned_frame)
  389|             break;
  390|         skip_bits(&s->gb, 8 + s->pict_type);
  391|         bits_count += 8 + s->pict_type;
  392|         v = show_bits(&s->gb, 16);
  393|     }
  394| 
  395|     if (bits_count + 8 >= s->gb.size_in_bits) {
  396|         v >>= 8;
  397|         v  |= 0x7F >> (7 - (bits_count & 7));
  398| 
  399|         if (v == 0x7F)
  400|             return s->mb_num;
  401|     } else {
  402|         static const uint16_t mpeg4_resync_prefix[8] = {
  403|             0x7F00, 0x7E00, 0x7C00, 0x7800, 0x7000, 0x6000, 0x4000, 0x0000
  404|         };
  405| 
  406|         if (v == mpeg4_resync_prefix[bits_count & 7]) {
  407|             int len, mb_num;
  408|             int mb_num_bits = av_log2(s->mb_num - 1) + 1;
  409|             GetBitContext gb = s->gb;
  410| 
  411|             skip_bits(&s->gb, 1);
  412|             align_get_bits(&s->gb);
  413| 
  414|             for (len = 0; len < 32; len++)
  415|                 if (get_bits1(&s->gb))
  416|                     break;
  417| 
  418|             mb_num = get_bits(&s->gb, mb_num_bits);
  419|             if (!mb_num || mb_num > s->mb_num || get_bits_count(&s->gb)+6 > s->gb.size_in_bits)
  420|                 mb_num= -1;
  421| 
  422|             s->gb = gb;
  423| 
  424|             if (len >= ff_mpeg4_get_video_packet_prefix_length(s))
  425|                 return mb_num;
  426|         }
  427|     }
  428|     return 0;
  429| }
  430| 
  431| static int mpeg4_decode_sprite_trajectory(Mpeg4DecContext *ctx, GetBitContext *gb)
  432| {
  433|     MpegEncContext *s = &ctx->m;
  434|     int a     = 2 << ctx->sprite_warping_accuracy;
  435|     int rho   = 3  - ctx->sprite_warping_accuracy;
  436|     int r     = 16 / a;
  437|     int alpha = 1;
  438|     int beta  = 0;
  439|     int w     = s->width;
  440|     int h     = s->height;
```

- `read_file(path=libavcodec/mpeg4videodec.c, start_line=680, end_line=730, version=old)` →

```
libavcodec/mpeg4videodec.c lines 680-730 of 4004
  680| overflow:
  681|     memset(ctx->sprite_offset, 0, sizeof(ctx->sprite_offset));
  682|     memset(ctx->sprite_delta,  0, sizeof(ctx->sprite_delta));
  683|     return AVERROR_PATCHWELCOME;
  684| }
  685| 
  686| static int decode_new_pred(Mpeg4DecContext *ctx, GetBitContext *gb) {
  687|     MpegEncContext *s = &ctx->m;
  688|     int len = FFMIN(ctx->time_increment_bits + 3, 15);
  689| 
  690|     get_bits(gb, len);
  691|     if (get_bits1(gb))
  692|         get_bits(gb, len);
  693|     check_marker(s->avctx, gb, "after new_pred");
  694| 
  695|     return 0;
  696| }
  697| 
  698| /**
  699|  * Decode the next video packet.
  700|  * @return <0 if something went wrong
  701|  */
  702| int ff_mpeg4_decode_video_packet_header(Mpeg4DecContext *ctx)
  703| {
  704|     MpegEncContext *s = &ctx->m;
  705| 
  706|     int mb_num_bits      = av_log2(s->mb_num - 1) + 1;
  707|     int header_extension = 0, mb_num, len;
  708| 
  709|     /* is there enough space left for a video packet + header */
  710|     if (get_bits_count(&s->gb) > s->gb.size_in_bits - 20)
  711|         return AVERROR_INVALIDDATA;
  712| 
  713|     for (len = 0; len < 32; len++)
  714|         if (get_bits1(&s->gb))
  715|             break;
  716| 
  717|     if (len != ff_mpeg4_get_video_packet_prefix_length(s)) {
  718|         av_log(s->avctx, AV_LOG_ERROR, "marker does not match f_code\n");
  719|         return AVERROR_INVALIDDATA;
  720|     }
  721| 
  722|     if (ctx->shape != RECT_SHAPE) {
  723|         header_extension = get_bits1(&s->gb);
  724|         // FIXME more stuff here
  725|     }
  726| 
  727|     mb_num = get_bits(&s->gb, mb_num_bits);
  728|     if (mb_num >= s->mb_num || !mb_num) {
  729|         av_log(s->avctx, AV_LOG_ERROR,
  730|                "illegal mb_num in video packet (%d %d) \n", mb_num, s->mb_num);
```

### Turn 4  _(tok 3687+106, stop=tool_use)_

**Reasoning:** Now find the enclosing function of line 424 — need the function definition start above line 380.


- `grep(pattern=^[a-zA-Z_].*\(, path_glob=libavcodec/mpeg4videodec.c, max_results=30, version=old)` →

```
49 matches (showing 30)
libavcodec/mpeg4videodec.c:84:static void gmc1_motion(MpegEncContext *s, const Mpeg4DecContext *ctx,
libavcodec/mpeg4videodec.c:181:static void gmc_motion(MpegEncContext *s, const Mpeg4DecContext *ctx,
libavcodec/mpeg4videodec.c:239:void ff_mpeg4_mcsel_motion(MpegEncContext *s,
libavcodec/mpeg4videodec.c:254:void ff_mpeg4_decode_studio(MpegEncContext *s, uint8_t *dest_y, uint8_t *dest_cb,
libavcodec/mpeg4videodec.c:322:void ff_mpeg4_pred_ac(MpegEncContext *s, int16_t *block, int n, int dir)
libavcodec/mpeg4videodec.c:377:static inline int mpeg4_is_resync(Mpeg4DecContext *ctx)
libavcodec/mpeg4videodec.c:431:static int mpeg4_decode_sprite_trajectory(Mpeg4DecContext *ctx, GetBitContext *gb)
libavcodec/mpeg4videodec.c:686:static int decode_new_pred(Mpeg4DecContext *ctx, GetBitContext *gb) {
libavcodec/mpeg4videodec.c:702:int ff_mpeg4_decode_video_packet_header(Mpeg4DecContext *ctx)
libavcodec/mpeg4videodec.c:789:static void reset_studio_dc_predictors(MpegEncContext *s)
libavcodec/mpeg4videodec.c:801:int ff_mpeg4_decode_studio_slice_header(Mpeg4DecContext *ctx)
libavcodec/mpeg4videodec.c:843:static inline int get_amv(Mpeg4DecContext *ctx, int n)
libavcodec/mpeg4videodec.c:890:static inline int mpeg4_get_level_dc(MpegEncContext *s, int n, int pred, int level)
libavcodec/mpeg4videodec.c:933:static inline int mpeg4_decode_dc(MpegEncContext *s, int n, int *dir_ptr)
libavcodec/mpeg4videodec.c:981:static int mpeg4_decode_partition_a(Mpeg4DecContext *ctx)
libavcodec/mpeg4videodec.c:1175:static int mpeg4_decode_partition_b(MpegEncContext *s, int mb_count)
libavcodec/mpeg4videodec.c:1268:int ff_mpeg4_decode_partitions(Mpeg4DecContext *ctx)
libavcodec/mpeg4videodec.c:1333:static inline int mpeg4_decode_block(Mpeg4DecContext *ctx, int16_t *block,
libavcodec/mpeg4videodec.c:1606:static int mpeg4_decode_partitioned_mb(MpegEncContext *s, int16_t block[6][64])
libavcodec/mpeg4videodec.c:1696:static int mpeg4_decode_mb(MpegEncContext *s, int16_t block[6][64])
libavcodec/mpeg4videodec.c:2076:static void next_start_code_studio(GetBitContext *gb)
libavcodec/mpeg4videodec.c:2112:static int mpeg4_decode_studio_block(MpegEncContext *s, int32_t block[64], int n)
libavcodec/mpeg4videodec.c:2227:static int mpeg4_decode_dpcm_macroblock(MpegEncContext *s, int16_t macroblock[256], int n)
libavcodec/mpeg4videodec.c:2310:static int mpeg4_decode_studio_mb(MpegEncContext *s, int16_t block_[12][64])
libavcodec/mpeg4videodec.c:2358:static int mpeg4_decode_gop_header(MpegEncContext *s, GetBitContext *gb)
libavcodec/mpeg4videodec.c:2380:static int mpeg4_decode_profile_level(MpegEncContext *s, GetBitContext *gb, int *profile, int *level)
libavcodec/mpeg4videodec.c:2394:static int mpeg4_decode_visual_object(MpegEncContext *s, GetBitContext *gb)
libavcodec/mpeg4videodec.c:2426:static void mpeg4_load_default_matrices(MpegEncContext *s)
libavcodec/mpeg4videodec.c:2443:static int read_quant_matrix_ext(MpegEncContext *s, GetBitContext *gb)
libavcodec/mpeg4videodec.c:2492:static void extension_and_user_data(MpegEncContext *s, GetBitContext *gb, int id)
```

### Turn 5  _(tok 4948+133, stop=tool_use)_

**Reasoning:** Line 424 is in `mpeg4_is_resync` (line 377). Line 717 in `ff_mpeg4_decode_video_packet_header`.

Now mpeg4videoenc.c line 1396.


- `grep(max_results=40, path_glob=libavcodec/mpeg4videoenc.c, pattern=^[a-zA-Z_].*\(, version=old)` →

```
25 matches
libavcodec/mpeg4videoenc.c:80:static inline Mpeg4EncContext *mainctx_to_mpeg4(MPVMainEncContext *m)
libavcodec/mpeg4videoenc.c:89:static inline int get_block_rate(MPVEncContext *const s, int16_t block[64],
libavcodec/mpeg4videoenc.c:124:static inline void restore_ac_coeffs(MPVEncContext *const s, int16_t block[6][64],
libavcodec/mpeg4videoenc.c:155:static inline int decide_ac_pred(MPVEncContext *const s, int16_t block[6][64],
libavcodec/mpeg4videoenc.c:238:void ff_clean_mpeg4_qscales(MPVEncContext *const s)
libavcodec/mpeg4videoenc.c:281:static inline void mpeg4_encode_dc(PutBitContext *s, int level, int n)
libavcodec/mpeg4videoenc.c:294:static inline int mpeg4_get_dc_length(int level, int n)
libavcodec/mpeg4videoenc.c:306:static inline void mpeg4_encode_block(const MPVEncContext *const s,
libavcodec/mpeg4videoenc.c:367:static int mpeg4_get_block_length(MPVEncContext *const s,
libavcodec/mpeg4videoenc.c:421:static inline void mpeg4_encode_blocks(MPVEncContext *const s,
libavcodec/mpeg4videoenc.c:457:static inline int get_b_cbp(MPVEncContext *const s, int16_t block[6][64],
libavcodec/mpeg4videoenc.c:501:static void mpeg4_encode_mb(MPVEncContext *const s, int16_t block[][64],
libavcodec/mpeg4videoenc.c:884:void ff_mpeg4_stuffing(PutBitContext *pbc)
libavcodec/mpeg4videoenc.c:892:void ff_set_mpeg4_time(MPVEncContext *const s)
libavcodec/mpeg4videoenc.c:902:static void mpeg4_encode_gop_header(MPVMainEncContext *const m)
libavcodec/mpeg4videoenc.c:932:static void mpeg4_encode_visual_object_header(MPVMainEncContext *const m)
libavcodec/mpeg4videoenc.c:975:static void mpeg4_encode_vol_header(Mpeg4EncContext *const m4,
libavcodec/mpeg4videoenc.c:1066:static int mpeg4_encode_picture_header(MPVMainEncContext *const m)
libavcodec/mpeg4videoenc.c:1126:static av_cold void init_uni_dc_tab(void)
libavcodec/mpeg4videoenc.c:1181:static av_cold void init_uni_mpeg4_rl_tab(RLTable *rl, uint32_t *bits_tab,
libavcodec/mpeg4videoenc.c:1276:static av_cold void mpeg4_encode_init_static(void)
libavcodec/mpeg4videoenc.c:1291:static av_cold int encode_init(AVCodecContext *avctx)
libavcodec/mpeg4videoenc.c:1353:void ff_mpeg4_init_partitions(MPVEncContext *const s)
libavcodec/mpeg4videoenc.c:1366:void ff_mpeg4_merge_partitions(MPVEncContext *const s)
libavcodec/mpeg4videoenc.c:1392:void ff_mpeg4_encode_video_packet_header(MPVEncContext *const s)
```

### Turn 6  _(tok 5947+155, stop=tool_use)_

**Reasoning:** Line 1396 is in `ff_mpeg4_encode_video_packet_header` (line 1392). Let me verify.

Also, is there any other file, e.g., in the old version? Grep found only those. Also check whether there are indirect macro wrappers. No.

Let me verify the enclosing of 1396.


- `read_file(end_line=1400, path=libavcodec/mpeg4videoenc.c, start_line=1390, version=old)` →

```
libavcodec/mpeg4videoenc.c lines 1390-1400 of 1442
 1390| }
 1391| 
 1392| void ff_mpeg4_encode_video_packet_header(MPVEncContext *const s)
 1393| {
 1394|     int mb_num_bits = av_log2(s->c.mb_num - 1) + 1;
 1395| 
 1396|     put_bits(&s->pb, ff_mpeg4_get_video_packet_prefix_length(&s->c), 0);
 1397|     put_bits(&s->pb, 1, 1);
 1398| 
 1399|     put_bits(&s->pb, mb_num_bits, s->c.mb_x + s->c.mb_y * s->c.mb_width);
 1400|     put_bits(&s->pb, 5 /* quant_precision */, s->c.qscale);
```

### Turn 7  _(tok 6351+334, stop=tool_use)_

**Reasoning:** All three call sites confirmed:
1. `mpeg4_is_resync` in libavcodec/mpeg4videodec.c
2. `ff_mpeg4_decode_video_packet_header` in libavcodec/mpeg4videodec.c
3. `ff_mpeg4_encode_video_packet_header` in libavcodec/mpeg4videoenc.c

Submit.


**Says:** 

Verified all three call sites (excluding the definition in `mpeg4video.c` and the prototype in `mpeg4video.h`):

| Enclosing function | File | Line |
|---|---|---|
| `mpeg4_is_resync` | libavcodec/mpeg4videodec.c | 424 |
| `ff_mpeg4_decode_video_packet_header` | libavcodec/mpeg4videodec.c | 717 |
| `ff_mpeg4_encode_video_packet_header` | libavcodec/mpeg4videoenc.c | 1396 |



- **submit_callers** → `{"callers": [{"function": "mpeg4_is_resync", "file": "libavcodec/mpeg4videodec.c"}, {"function": "ff_mpeg4_decode_video_packet_header", "file": "libavcodec/mpeg4videodec.c"}, {"function": "ff_mpeg4_encode_video_packet_header", "file": "libavcodec/mpeg4videoenc.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

