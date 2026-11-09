# Impact-analysis transcript — ffmpeg @ 545724f61e65 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_mpeg4_get_video_packet_prefix_length` (libavcodec/mpeg4video.c), arity 1->3
- truth: [['libavcodec/mpeg4videodec.c', 'ff_mpeg4_decode_video_packet_header'], ['libavcodec/mpeg4videodec.c', 'mpeg4_is_resync'], ['libavcodec/mpeg4videoenc.c', 'ff_mpeg4_encode_video_packet_header']]

## Self-navigation arm

### Turn 1  _(tok 955+149, stop=tool_use)_

**Reasoning:** Let me search for the function name in the repository.

Note: the tools have a "version" parameter with enum "old". Let me just use "old".


- `grep(pattern=ff_mpeg4_get_video_packet_prefix_length, version=old, max_results=200)` →

```
5 matches
libavcodec/mpeg4video.c:42:int ff_mpeg4_get_video_packet_prefix_length(MpegEncContext *s)
libavcodec/mpeg4video.h:31:int ff_mpeg4_get_video_packet_prefix_length(MpegEncContext *s);
libavcodec/mpeg4videodec.c:424:            if (len >= ff_mpeg4_get_video_packet_prefix_length(s))
libavcodec/mpeg4videodec.c:717:    if (len != ff_mpeg4_get_video_packet_prefix_length(s)) {
libavcodec/mpeg4videoenc.c:1396:    put_bits(&s->pb, ff_mpeg4_get_video_packet_prefix_length(&s->c), 0);
```

- `list_files(version=old, path=libavcodec, pattern=mpeg4)` →

```
33 files
libavcodec/mpeg4audio.c	5691
libavcodec/mpeg4audio.h	6520
libavcodec/mpeg4audio_copy_pce.h	2579
libavcodec/mpeg4audio_sample_rates.c	965
libavcodec/mpeg4audio_sample_rates.h	1395
libavcodec/mpeg4data.h	17422
libavcodec/mpeg4video.c	6957
libavcodec/mpeg4video.h	2421
libavcodec/mpeg4video_parser.c	5045
libavcodec/mpeg4videodata.h	2113
libavcodec/mpeg4videodec.c	153246
libavcodec/mpeg4videodec.h	4176
libavcodec/mpeg4videodefs.h	2044
libavcodec/mpeg4videodsp.c	4522
libavcodec/mpeg4videodsp.h	1813
libavcodec/mpeg4videoenc.c	53276
libavcodec/mpeg4videoenc.h	1366
libavcodec/msmpeg4.c	10127
libavcodec/msmpeg4.h	1352
libavcodec/msmpeg4_vc1_data.c	14283
libavcodec/msmpeg4_vc1_data.h	1754
libavcodec/msmpeg4data.c	65480
libavcodec/msmpeg4data.h	2287
libavcodec/msmpeg4dec.c	31310
libavcodec/msmpeg4dec.h	1973
libavcodec/msmpeg4enc.c	24865
libavcodec/msmpeg4enc.h	1876
libavcodec/nvdec_mpeg4.c	5089
libavcodec/vaapi_mpeg4.c	8515
libavcodec/vdpau_mpeg4.c	4962
libavcodec/bsf/mpeg4_unpack_bframes.c	5613
libavcodec/ppc/mpeg4videodsp.c	5400
libavcodec/x86/mpeg4videodsp.c	6223
```

### Turn 2  _(tok 1780+299, stop=tool_use)_

**Reasoning:** I need to identify the function names surrounding each call site:

1. libavcodec/mpeg4videodec.c:424
2. libavcodec/mpeg4videodec.c:717
3. libavcodec/mpeg4videoenc.c:1396

Let's try reading around each of those lines.

- `read_file(version=old, path=libavcodec/mpeg4videodec.c, start_line=380, end_line=440)` →

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

- `read_file(version=old, path=libavcodec/mpeg4videodec.c, start_line=680, end_line=730)` →

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

- `read_file(version=old, path=libavcodec/mpeg4videoenc.c, start_line=1350, end_line=1410)` →

```
libavcodec/mpeg4videoenc.c lines 1350-1410 of 1442
 1350|     return 0;
 1351| }
 1352| 
 1353| void ff_mpeg4_init_partitions(MPVEncContext *const s)
 1354| {
 1355|     uint8_t *start = put_bits_ptr(&s->pb);
 1356|     uint8_t *end   = s->pb.buf_end;
 1357|     int size       = end - start;
 1358|     int pb_size    = (((intptr_t)start + size / 3) & (~3)) - (intptr_t)start;
 1359|     int tex_size   = (size - 2 * pb_size) & (~3);
 1360| 
 1361|     set_put_bits_buffer_size(&s->pb, pb_size);
 1362|     init_put_bits(&s->tex_pb, start + pb_size, tex_size);
 1363|     init_put_bits(&s->pb2, start + pb_size + tex_size, pb_size);
 1364| }
 1365| 
 1366| void ff_mpeg4_merge_partitions(MPVEncContext *const s)
 1367| {
 1368|     const int pb2_len    = put_bits_count(&s->pb2);
 1369|     const int tex_pb_len = put_bits_count(&s->tex_pb);
 1370|     const int bits       = put_bits_count(&s->pb);
 1371| 
 1372|     if (s->c.pict_type == AV_PICTURE_TYPE_I) {
 1373|         put_bits(&s->pb, 19, DC_MARKER);
 1374|         s->misc_bits  += 19 + pb2_len + bits - s->last_bits;
 1375|         s->i_tex_bits += tex_pb_len;
 1376|     } else {
 1377|         put_bits(&s->pb, 17, MOTION_MARKER);
 1378|         s->misc_bits  += 17 + pb2_len;
 1379|         s->mv_bits    += bits - s->last_bits;
 1380|         s->p_tex_bits += tex_pb_len;
 1381|     }
 1382| 
 1383|     flush_put_bits(&s->pb2);
 1384|     flush_put_bits(&s->tex_pb);
 1385| 
 1386|     set_put_bits_buffer_size(&s->pb, s->pb2.buf_end - s->pb.buf);
 1387|     ff_copy_bits(&s->pb, s->pb2.buf, pb2_len);
 1388|     ff_copy_bits(&s->pb, s->tex_pb.buf, tex_pb_len);
 1389|     s->last_bits = put_bits_count(&s->pb);
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
 1401|     put_bits(&s->pb, 1, 0); /* no HEC */
 1402| }
 1403| 
 1404| #define OFFSET(x) offsetof(MPVEncContext, c.x)
 1405| #define VE AV_OPT_FLAG_VIDEO_PARAM | AV_OPT_FLAG_ENCODING_PARAM
 1406| static const AVOption options[] = {
 1407|     { "data_partitioning", "Use data partitioning.",      OFFSET(data_partitioning), AV_OPT_TYPE_BOOL, { .i64 = 0 }, 0, 1, VE },
 1408|     { "alternate_scan",    "Enable alternate scantable.", OFFSET(alternate_scan),    AV_OPT_TYPE_BOOL, { .i64 = 0 }, 0, 1, VE },
 1409|     { "mpeg_quant",        "Use MPEG quantizers instead of H.263",
 1410|       OFFSET(mpeg_quant), AV_OPT_TYPE_INT, {.i64 = 0 }, 0, 1, VE },
```

### Turn 3  _(tok 5243+147, stop=tool_use)_

**Reasoning:** Next, identify the function that contains mpeg4videodec.c:424. Check before line 380 to confirm the enclosing function name. It looked like `mpeg4_find_resync_marker` — let's confirm.

- `grep(max_results=20, path_glob=libavcodec/mpeg4videodec.c, pattern=^(static [a-zA-Z0-9_]+|int|void|static|int64_t)[^(]*\(, version=old)` →

```
49 matches (showing 20)
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
```

### Turn 4  _(tok 6148+458, stop=tool_use)_

**Reasoning:** So, the call site at mpeg4videodec.c:424 is inside `mpeg4_is_resync` (lines 377-429). The call at line 717 is inside `ff_mpeg4_decode_video_packet_header`. The call at mpeg4videoenc.c:1396 is inside `ff_mpeg4_encode_video_packet_header`.

So, the callers are:
1. `mpeg4_is_resync` in libavcodec/mpeg4videodec.c
2. `ff_mpeg4_decode_video_packet_header` in libavcodec/mpeg4videodec.c
3. `ff_mpeg4_encode_video_packet_header` in libavcodec/mpeg4videoenc.c

That's all of them. There were only 5 matches: the definition, the prototype in the header, and 3 call sites. Done.


**Says:** I found all references. Excluding the definition and the header prototype, there are exactly 3 call sites:

- `libavcodec/mpeg4videodec.c:424` — inside `mpeg4_is_resync` (lines 377–429)
- `libavcodec/mpeg4videodec.c:717` — inside `ff_mpeg4_decode_video_packet_header` (starting at line 702)
- `libavcodec/mpeg4videoenc.c:1396` — inside `ff_mpeg4_encode_video_packet_header` (lines 1392–1402)



- **submit_callers** → `{"callers": [{"file": "libavcodec/mpeg4videodec.c", "function": "mpeg4_is_resync"}, {"file": "libavcodec/mpeg4videodec.c", "function": "ff_mpeg4_decode_video_packet_header"}, {"file": "libavcodec/mpeg4videoenc.c", "function": "ff_mpeg4_encode_video_packet_header"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2784+180, stop=tool_use)_

**Reasoning:** Let me search for callers.

Note: resolve_symbol has version param "work"/"old"/"new"? Actually the tool description says `version`: "work" (files on disk), "old" (parent of `rev`) or "new" (`rev`). But the required args only include name. Let's use grep first.


- `grep(pattern=ff_mpeg4_get_video_packet_prefix_length, version=old, max_results=100)` →

```
5 matches
libavcodec/mpeg4video.c:42:int ff_mpeg4_get_video_packet_prefix_length(MpegEncContext *s)
libavcodec/mpeg4video.h:31:int ff_mpeg4_get_video_packet_prefix_length(MpegEncContext *s);
libavcodec/mpeg4videodec.c:424:            if (len >= ff_mpeg4_get_video_packet_prefix_length(s))
libavcodec/mpeg4videodec.c:717:    if (len != ff_mpeg4_get_video_packet_prefix_length(s)) {
libavcodec/mpeg4videoenc.c:1396:    put_bits(&s->pb, ff_mpeg4_get_video_packet_prefix_length(&s->c), 0);
```

- `get_callers(name=ff_mpeg4_get_video_packet_prefix_length, limit=100)` →

```
{
  "name": "ff_mpeg4_get_video_packet_prefix_length",
  "version": "old",
  "callers": [
    {
      "caller": "mpeg4_is_resync",
      "file": "libavcodec/mpeg4videodec.c",
      "line": 424
    },
    {
      "caller": "ff_mpeg4_decode_video_packet_header",
      "file": "libavcodec/mpeg4videodec.c",
      "line": 717
    },
    {
      "caller": "ff_mpeg4_encode_video_packet_header",
      "file": "libavcodec/mpeg4videoenc.c",
      "line": 1396
    }
  ]
}
```

### Turn 2  _(tok 3299+159, stop=tool_use)_

**Reasoning:** Let me verify the enclosing functions by reading context around those lines.

- `get_context_at(file=libavcodec/mpeg4videodec.c, line=424)` →

```
mpeg4_is_resync — libavcodec/mpeg4videodec.c:377 [function] static inline int mpeg4_is_resync(Mpeg4DecContext *ctx)
  reads: ctx; writes: ctx*; returns: return 0; | return s->mb_num; | return mb_num; | return 0;

SLICE around line 424 (def-use, level 2; '>' marks the seed):
static inline int mpeg4_is_resync(Mpeg4DecContext *ctx) {
   MpegEncContext *s = &ctx->m;
   ...
   while(v <= 0xFF) {
   ...
     bits_count += 8 + s->pict_type;
   ...
   }
   if(bits_count + 8 >= s->gb.size_in_bits) {
   ...
     v |= 0x7F >>(7 -(bits_count & 7));
   ...
   } else {
     static const uint16_t mpeg4_resync_prefix[8] = { 0x7F00, 0x7E00, 0x7C00, 0x7800, 0x7000, 0x6000, 0x4000, 0x0000 };
     if(v == mpeg4_resync_prefix[bits_count & 7]) {
       int len, mb_num;
       int mb_num_bits = av_log2(s->mb_num - 1)+ 1;
       GetBitContext gb = s->gb;
   ...
       for(len = 0; len < 32; len++)
   ...
       mb_num = get_bits(&s->gb, mb_num_bits);
       if(!mb_num || mb_num > s->mb_num || get_bits_count(&s->gb)+6 > s->gb.size_in_bits)
         mb_num= -1;
       s->gb = gb;
>      if(len >= ff_mpeg4_get_video_packet_prefix_length(s))
         return mb_num;
   ...
     }
   }
}

CALLEES (8):
  get_bits_count (libavcodec/get_bits.h:249 (1 of 2 definitions)): reads s; writes -; returns return s->index;
  show_bits (libavcodec/get_bits.h:354 (1 of 2 definitions)): reads n, s; writes -; returns return tmp;
  skip_bits (libavcodec/get_bits.h:364 (1 of 2 definitions)): reads n, s; writes s*; returns -
  ff_mpeg4_get_video_packet_prefix_length (libavcodec/mpeg4video.c:42): reads s; writes -; returns return 16; | return s->f_code + 15; | return FFMAX3(s->f_code, s->b_code, 2)+ 15; | return -1;
  get_bits (libavcodec/get_bits.h:318 (1 of 3 definitions)): reads n, s; writes s*; returns return tmp;
  get_bits1 (libavcodec/get_bits.h:371 (1 of 2 definitions)): reads s; writes s*; returns return result;
  align_get_bits (libavcodec/get_bits.h:544 (1 of 2 definitions)): reads s; writes -; returns return s->buffer +(s->index >> 3);
  av_log2 (libavutil/intmath.c:26 (1 of 2 definitions)): reads v; writes -; returns return ff_log2(v);

CALLERS (3):
  mpeg4_decode_partitioned_mb (libavcodec/mpeg4videodec.c:1682): if (mpeg4_is_resync(ctx))
  mpeg4_decode_partitioned_mb (libavcodec/mpeg4videodec.c:1687): if (mpeg4_is_resync(ctx)) {
  mpeg4_decode_mb (libavcodec/mpeg4videodec.c:2052): next = mpeg4_is_resync(ctx);
```

- `get_context_at(file=libavcodec/mpeg4videodec.c, line=717)` →

```
ff_mpeg4_decode_video_packet_header — libavcodec/mpeg4videodec.c:702 [function] int ff_mpeg4_decode_video_packet_header(Mpeg4DecContext *ctx)
  reads: ctx; writes: ctx*; returns: return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return 0;

SLICE around line 717 (def-use, level 2; '>' marks the seed):
int ff_mpeg4_decode_video_packet_header(Mpeg4DecContext *ctx) {
   MpegEncContext *s = &ctx->m;
   ...
   for(len = 0; len < 32; len++)
   ...
>  if(len != ff_mpeg4_get_video_packet_prefix_length(s)) {
     av_log(s->avctx, AV_LOG_ERROR, "marker does not match f_code\n");
     return AVERROR_INVALIDDATA;
   ...
   }
}

CALLEES (10):
  av_log2 (libavutil/intmath.c:26 (1 of 2 definitions)): reads v; writes -; returns return ff_log2(v);
  get_bits_count (libavcodec/get_bits.h:249 (1 of 2 definitions)): reads s; writes -; returns return s->index;
  get_bits1 (libavcodec/get_bits.h:371 (1 of 2 definitions)): reads s; writes s*; returns return result;
  av_log (libavutil/log.c:441 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_mpeg4_get_video_packet_prefix_length (libavcodec/mpeg4video.c:42): reads s; writes -; returns return 16; | return s->f_code + 15; | return FFMAX3(s->f_code, s->b_code, 2)+ 15; | return -1;
  get_bits (libavcodec/get_bits.h:318 (1 of 3 definitions)): reads n, s; writes s*; returns return tmp;
  mpeg4_decode_sprite_trajectory (libavcodec/mpeg4videodec.c:431): reads ctx, gb; writes ctx*; returns return AVERROR_INVALIDDATA; | return 0; | return AVERROR_PATCHWELCOME;
  skip_bits (libavcodec/get_bits.h:364 (1 of 2 definitions)): reads n, s; writes s*; returns -
  check_marker (libavcodec/mpegvideodec.h:81): reads logctx, msg, s; writes -; returns return bit;
  decode_new_pred (libavcodec/mpeg4videodec.c:686): reads ctx, gb; writes -; returns return 0;

CALLERS (2):
  ff_h263_resync (libavcodec/ituh263dec.c:243): ret= ff_mpeg4_decode_video_packet_header(s->avctx->priv_data);
  ff_h263_resync (libavcodec/ituh263dec.c:260): ret= ff_mpeg4_decode_video_packet_header(s->avctx->priv_data);
```

- `get_context_at(file=libavcodec/mpeg4videoenc.c, line=1396)` →

```
ff_mpeg4_encode_video_packet_header — libavcodec/mpeg4videoenc.c:1392 [function] void ff_mpeg4_encode_video_packet_header(MPVEncContext *const s)
  reads: s; writes: s*; returns: -

SLICE around line 1396 (def-use, level 2; '>' marks the seed):
void ff_mpeg4_encode_video_packet_header(MPVEncContext *const s) {
   ...
>  put_bits(&s->pb, ff_mpeg4_get_video_packet_prefix_length(&s->c), 0);
   ...
}

CALLEES (3):
  av_log2 (libavutil/intmath.c:26 (1 of 2 definitions)): reads v; writes -; returns return ff_log2(v);
  put_bits (libavcodec/j2kenc.c:223 (1 of 2 definitions)): reads n, s, val; writes s*; returns -
  ff_mpeg4_get_video_packet_prefix_length (libavcodec/mpeg4video.c:42): reads s; writes -; returns return 16; | return s->f_code + 15; | return FFMAX3(s->f_code, s->b_code, 2)+ 15; | return -1;

CALLERS (1):
  encode_thread (libavcodec/mpegvideo_enc.c:3133): ff_mpeg4_encode_video_packet_header(s);
```

### Turn 3  _(tok 5458+281, stop=tool_use)_

**Reasoning:** All three confirmed. Grep found 5 matches total: definition, prototype, and 3 call sites. No function-pointer usage. Also check for any usage in other directories (grep covered whole repo). Confident.


**Says:** All three call sites verified via grep and semantic context (no function-pointer uses; the other two grep hits are the definition and the prototype).

| Enclosing function | File |
|---|---|
| `mpeg4_is_resync` | libavcodec/mpeg4videodec.c |
| `ff_mpeg4_decode_video_packet_header` | libavcodec/mpeg4videodec.c |
| `ff_mpeg4_encode_video_packet_header` | libavcodec/mpeg4videoenc.c |



- **submit_callers** → `{"callers": [{"function": "mpeg4_is_resync", "file": "libavcodec/mpeg4videodec.c"}, {"function": "ff_mpeg4_decode_video_packet_header", "file": "libavcodec/mpeg4videodec.c"}, {"function": "ff_mpeg4_encode_video_packet_header", "file": "libavcodec/mpeg4videoenc.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2361+96, stop=tool_use)_

**Reasoning:** Let me start by getting the callers of the function.


- `get_callers(name=ff_mpeg4_get_video_packet_prefix_length, limit=100)` →

```
{
  "name": "ff_mpeg4_get_video_packet_prefix_length",
  "version": "old",
  "callers": [
    {
      "caller": "mpeg4_is_resync",
      "file": "libavcodec/mpeg4videodec.c",
      "line": 424
    },
    {
      "caller": "ff_mpeg4_decode_video_packet_header",
      "file": "libavcodec/mpeg4videodec.c",
      "line": 717
    },
    {
      "caller": "ff_mpeg4_encode_video_packet_header",
      "file": "libavcodec/mpeg4videoenc.c",
      "line": 1396
    }
  ]
}
```

- `resolve_symbol(name=ff_mpeg4_get_video_packet_prefix_length)` →

```
{
  "resolved": true,
  "name": "ff_mpeg4_get_video_packet_prefix_length",
  "version": "old",
  "file": "libavcodec/mpeg4video.c",
  "line": 42,
  "kind": "function",
  "signature": "int ff_mpeg4_get_video_packet_prefix_length(MpegEncContext *s)",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 2  _(tok 2770+151, stop=tool_use)_

**Reasoning:** Let's confirm the callers by inspecting each call site context. Also check whether there are other calls in mpeg4videoenc.c (e.g., ff_mpeg4_encode_video_packet_header may call twice) or in mpeg4videodec.c. Let me use expand_function to see callers/callees and also check the source at those lines.

Also, there could be a call in mpeg4video.c itself? The definition is there. Let's check expand_function for callers.


- `expand_function(name=ff_mpeg4_get_video_packet_prefix_length, levels=2)` →

```
{"name":"ff_mpeg4_get_video_packet_prefix_length","version":"old","levels":2,"node":{"name":"ff_mpeg4_get_video_packet_prefix_length","file":"libavcodec/mpeg4video.c","line":42,"kind":"function","state":"analyzed"},"callees":[{"name":"FFMAX3","file":"libavutil/macros.h","line":48,"kind":"macro","state":"analyzed","call_lines":[51]}],"callers":[{"name":"mpeg4_is_resync","file":"libavcodec/mpeg4videodec.c","line":377,"kind":"function","state":"analyzed","call_lines":[424]},{"name":"ff_mpeg4_decode_video_packet_header","file":"libavcodec/mpeg4videodec.c","line":702,"kind":"function","state":"analyzed","call_lines":[717]},{"name":"ff_mpeg4_encode_video_packet_header","file":"libavcodec/mpeg4videoenc.c","line":1392,"kind":"function","state":"analyzed","call_lines":[1396]}],"rings":[{"level":1,"count":4,"nodes":["FFMAX3 libavutil/macros.h:48 <- ff_mpeg4_get_video_packet_prefix_length","ff_mpeg4_decode_video_packet_header libavcodec/mpeg4videodec.c:702 -> ff_mpeg4_get_video_packet_prefix_length","ff_mpeg4_encode_video_packet_header libavcodec/mpeg4videoenc.c:1392 -> ff_mpeg4_get_video_packet_prefix_length","mpeg4_is_resync libavcodec/mpeg4videodec.c:377 -> ff_mpeg4_get_video_packet_prefix_length"]},{"level":2,"count":54,"nodes":["ff_h263_resync libavcodec/ituh263dec.c:217 -> ff_mpeg4_decode_video_packet_header","encode_thread libavcodec/mpegvideo_enc.c:2974 -> ff_mpeg4_encode_video_packet_header","mpeg4_decode_mb libavcodec/mpeg4videodec.c:1696 -> mpeg4_is_resync","mpeg4_decode_partitioned_mb libavcodec/mpeg4videodec.c:1606 -> mpeg4_is_resync","av_log libavutil/log.c:441 <- ff_mpeg4_decode_video_packet_header","check_marker libavcodec/mpegvideodec.h:81 <- ff_mpeg4_decode_video_packet_header","decode_new_pred libavcodec/mpeg4videodec.c:686 <- ff_mpeg4_decode_video_packet_header","mpeg4_decode_sprite_trajectory libavcodec/mpeg4videodec.c:431 <- ff_mpeg4_decode_video_packet_header","put_bits libavcodec/j2kenc.c:223 <- ff_mpeg4_encode_video_packet_header","align_get_bits libavcodec/get_bits.h:544 <- mpeg4_is_resync","av_log2 libavutil/intmath.c:26 <- mpeg4_is_resync","get_bits libavcodec/get_bits.h:318 <- mpeg4_is_resync","get_bits1 libavcodec/get_bits.h:371 <- mpeg4_is_resync","get_bits_count libavcodec/get_bits.h:249 <- mpeg4_is_resync","show_bits libavcodec/get_bits.h:354 <- mpeg4_is_resync","skip_bits libavcodec/get_bits.h:364 <- mpeg4_is_resync","decode_frame_headers libavcodec/indeo3.c:900 -> FFMAX3","dirac_decode_data_unit libavcodec/diracdec.c:2122 -> FFMAX3","ff_ffv1_compute_bits_per_plane libavcodec/ffv1.c:222 -> FFMAX3","float2rgbe libavcodec/hdrenc.c:56 -> FFMAX3","h264_slice_init libavcodec/h264_slice.c:1914 -> FFMAX3","jpeg2000_decode_ht_cleanup_segment libavcodec/jpeg2000htdec.c:548 -> FFMAX3","long_term_filter libavcodec/g729postfilter.c:113 -> FFMAX3","mux_fixup_ts fftools/ffmpeg_mux.c:138 -> FFMAX3","search_for_quantizers_twoloop libavcodec/aaccoder_twoloop.h:65 -> FFMAX3","verify_md5 libavcodec/hevc/hevcdec.c:3415 -> FFMAX3","avcodec_align_dimensions libavcodec/utils.c:351 -> FFMAX3","avfilter_graph_dump_to_buf libavfilter/graphdump.c:64 -> FFMAX3","cas_slice16 libavfilter/vf_cas.c:113 -> FFMAX3","cas_slice8 libavfilter/vf_cas.c:47 -> FFMAX3","color_balance16 libavfilter/vf_colorbalance.c:308 -> FFMAX3","color_balance16_p libavfilter/vf_colorbalance.c:203 -> FFMAX3","color_balance8 libavfilter/vf_colorbalance.c:257 -> FFMAX3","color_balance8_p libavfilter/vf_colorbalance.c:150 -> FFMAX3","compute_box_stats libavfilter/vf_palettegen.c:176 -> FFMAX3","draw_text libavfilter/vf_drawtext.c:1553 -> FFMAX3","encode_picture libavcodec/mpegvideo_enc.c:3696 -> FFMAX3","ff_mjpeg_decode_frame_from_buf libavcodec/mjpegdec.c:2374 -> FFMAX3","fill_in_tongue libavfilter/vf_ciescope.c:1119 -> FFMAX3","filter_frame libavfilter/vf_histeq.c:124 -> FFMAX3","init libavfilter/vf_hqx.c:504 -> FFMAX3","init_video_param libavcodec/qsvenc.c:774 -> FFMAX3","load_data libavfilter/af_sofalizer.c:718 -> FFMAX3","mjpegb_decode_frame libavcodec/mjpegbdec.c:43 -> FFMAX3","normalize libavfilter/vf_normalize.c:290 -> FFMAX3","preserve_color libavfilter/preserve_color.h:53 -> FFMAX3","preservel libavfilter/vf_colorbalance.c:117 -> FFMAX3","tonemap libavfilter/vf_tonemap.c:109 -> FFMAX3","update_bitrate libavcodec/qsvenc.c:2408 -> FFMAX3","update_needed_crop libavfilter/vf_deshake_opencl.c:989 -> FFMAX3","vibrance_slice16 libavfilter/vf_vibrance.c:133 -> FFMAX3","vibrance_slice8 libavfilter/vf_vibrance.c:58 -> FFMAX3","vibrance_slice8p libavfilter/vf_vibrance.c:210 -> FFMAX3","xyz_to_tetrahedron libavfilter/vf_v360.c:3345 -> FFMAX3"]}],"rings_format":"name file:line <- via (callee of via) | name file:line -> via (caller of via); ordered: callers of callers, callees of callees, then the rest; at most 10 per via"}
```

### Turn 3  _(tok 4565+261, stop=tool_use)_

**Reasoning:** Three callers. Let me verify the call sites by checking the source context at those lines, and also verify no additional call sites exist (e.g., in ff_mpeg4_encode_video_packet_header maybe two calls — but that doesn't change the list of functions). Also I should double-check whether there might be callers in files the index doesn't cover, or macros that wrap it. Let me check the source of each caller to confirm.

Also worth checking: is there any macro that expands to this function? Let's check the neighborhoods of the three callers quickly.


- `get_context_at(file=libavcodec/mpeg4videodec.c, line=424)` →

```
mpeg4_is_resync — libavcodec/mpeg4videodec.c:377 [function] static inline int mpeg4_is_resync(Mpeg4DecContext *ctx)
  reads: ctx; writes: ctx*; returns: return 0; | return s->mb_num; | return mb_num; | return 0;

SLICE around line 424 (def-use, level 2; '>' marks the seed):
static inline int mpeg4_is_resync(Mpeg4DecContext *ctx) {
   MpegEncContext *s = &ctx->m;
   ...
   while(v <= 0xFF) {
   ...
     bits_count += 8 + s->pict_type;
   ...
   }
   if(bits_count + 8 >= s->gb.size_in_bits) {
   ...
     v |= 0x7F >>(7 -(bits_count & 7));
   ...
   } else {
     static const uint16_t mpeg4_resync_prefix[8] = { 0x7F00, 0x7E00, 0x7C00, 0x7800, 0x7000, 0x6000, 0x4000, 0x0000 };
     if(v == mpeg4_resync_prefix[bits_count & 7]) {
       int len, mb_num;
       int mb_num_bits = av_log2(s->mb_num - 1)+ 1;
       GetBitContext gb = s->gb;
   ...
       for(len = 0; len < 32; len++)
   ...
       mb_num = get_bits(&s->gb, mb_num_bits);
       if(!mb_num || mb_num > s->mb_num || get_bits_count(&s->gb)+6 > s->gb.size_in_bits)
         mb_num= -1;
       s->gb = gb;
>      if(len >= ff_mpeg4_get_video_packet_prefix_length(s))
         return mb_num;
   ...
     }
   }
}

CALLEES (8):
  get_bits_count (libavcodec/get_bits.h:249 (1 of 2 definitions)): reads s; writes -; returns return s->index;
  show_bits (libavcodec/get_bits.h:354 (1 of 2 definitions)): reads n, s; writes -; returns return tmp;
  skip_bits (libavcodec/get_bits.h:364 (1 of 2 definitions)): reads n, s; writes s*; returns -
  ff_mpeg4_get_video_packet_prefix_length (libavcodec/mpeg4video.c:42): reads s; writes -; returns return 16; | return s->f_code + 15; | return FFMAX3(s->f_code, s->b_code, 2)+ 15; | return -1;
  get_bits (libavcodec/get_bits.h:318 (1 of 3 definitions)): reads n, s; writes s*; returns return tmp;
  get_bits1 (libavcodec/get_bits.h:371 (1 of 2 definitions)): reads s; writes s*; returns return result;
  align_get_bits (libavcodec/get_bits.h:544 (1 of 2 definitions)): reads s; writes -; returns return s->buffer +(s->index >> 3);
  av_log2 (libavutil/intmath.c:26 (1 of 2 definitions)): reads v; writes -; returns return ff_log2(v);

CALLERS (3):
  mpeg4_decode_partitioned_mb (libavcodec/mpeg4videodec.c:1682): if (mpeg4_is_resync(ctx))
  mpeg4_decode_partitioned_mb (libavcodec/mpeg4videodec.c:1687): if (mpeg4_is_resync(ctx)) {
  mpeg4_decode_mb (libavcodec/mpeg4videodec.c:2052): next = mpeg4_is_resync(ctx);
```

- `get_context_at(file=libavcodec/mpeg4videodec.c, line=717)` →

```
ff_mpeg4_decode_video_packet_header — libavcodec/mpeg4videodec.c:702 [function] int ff_mpeg4_decode_video_packet_header(Mpeg4DecContext *ctx)
  reads: ctx; writes: ctx*; returns: return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return 0;

SLICE around line 717 (def-use, level 2; '>' marks the seed):
int ff_mpeg4_decode_video_packet_header(Mpeg4DecContext *ctx) {
   MpegEncContext *s = &ctx->m;
   ...
   for(len = 0; len < 32; len++)
   ...
>  if(len != ff_mpeg4_get_video_packet_prefix_length(s)) {
     av_log(s->avctx, AV_LOG_ERROR, "marker does not match f_code\n");
     return AVERROR_INVALIDDATA;
   ...
   }
}

CALLEES (10):
  av_log2 (libavutil/intmath.c:26 (1 of 2 definitions)): reads v; writes -; returns return ff_log2(v);
  get_bits_count (libavcodec/get_bits.h:249 (1 of 2 definitions)): reads s; writes -; returns return s->index;
  get_bits1 (libavcodec/get_bits.h:371 (1 of 2 definitions)): reads s; writes s*; returns return result;
  av_log (libavutil/log.c:441 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_mpeg4_get_video_packet_prefix_length (libavcodec/mpeg4video.c:42): reads s; writes -; returns return 16; | return s->f_code + 15; | return FFMAX3(s->f_code, s->b_code, 2)+ 15; | return -1;
  get_bits (libavcodec/get_bits.h:318 (1 of 3 definitions)): reads n, s; writes s*; returns return tmp;
  mpeg4_decode_sprite_trajectory (libavcodec/mpeg4videodec.c:431): reads ctx, gb; writes ctx*; returns return AVERROR_INVALIDDATA; | return 0; | return AVERROR_PATCHWELCOME;
  skip_bits (libavcodec/get_bits.h:364 (1 of 2 definitions)): reads n, s; writes s*; returns -
  check_marker (libavcodec/mpegvideodec.h:81): reads logctx, msg, s; writes -; returns return bit;
  decode_new_pred (libavcodec/mpeg4videodec.c:686): reads ctx, gb; writes -; returns return 0;

CALLERS (2):
  ff_h263_resync (libavcodec/ituh263dec.c:243): ret= ff_mpeg4_decode_video_packet_header(s->avctx->priv_data);
  ff_h263_resync (libavcodec/ituh263dec.c:260): ret= ff_mpeg4_decode_video_packet_header(s->avctx->priv_data);
```

- `get_context_at(file=libavcodec/mpeg4videoenc.c, line=1396)` →

```
ff_mpeg4_encode_video_packet_header — libavcodec/mpeg4videoenc.c:1392 [function] void ff_mpeg4_encode_video_packet_header(MPVEncContext *const s)
  reads: s; writes: s*; returns: -

SLICE around line 1396 (def-use, level 2; '>' marks the seed):
void ff_mpeg4_encode_video_packet_header(MPVEncContext *const s) {
   ...
>  put_bits(&s->pb, ff_mpeg4_get_video_packet_prefix_length(&s->c), 0);
   ...
}

CALLEES (3):
  av_log2 (libavutil/intmath.c:26 (1 of 2 definitions)): reads v; writes -; returns return ff_log2(v);
  put_bits (libavcodec/j2kenc.c:223 (1 of 2 definitions)): reads n, s, val; writes s*; returns -
  ff_mpeg4_get_video_packet_prefix_length (libavcodec/mpeg4video.c:42): reads s; writes -; returns return 16; | return s->f_code + 15; | return FFMAX3(s->f_code, s->b_code, 2)+ 15; | return -1;

CALLERS (1):
  encode_thread (libavcodec/mpegvideo_enc.c:3133): ff_mpeg4_encode_video_packet_header(s);
```

### Turn 4  _(tok 6825+392, stop=tool_use)_

**Reasoning:** All three call sites confirmed. Note that ff_mpeg4_encode_video_packet_header passes &s->c (MPVEncContext) — meaning the signature may be changing. That confirms relevance.

Is there any possibility of another caller not captured (e.g., in a header inline function or macro)? gtags-unique resolution and get_callers found 3. Let me double-check with a broader search — maybe there's a macro alias. I can't grep. The get_callers result with limit 100 returned 3 callers. That's likely complete.

Let me submit.


**Says:** 

All three call sites verified (definition at `libavcodec/mpeg4video.c:42`; no macro wrappers or additional call sites found):

1. `mpeg4_is_resync` — `libavcodec/mpeg4videodec.c:424`
2. `ff_mpeg4_decode_video_packet_header` — `libavcodec/mpeg4videodec.c:717`
3. `ff_mpeg4_encode_video_packet_header` — `libavcodec/mpeg4videoenc.c:1396` (passes `&s->c` from an `MPVEncContext`, so this site matters most for a signature change)



- **submit_callers** → `{"callers": [{"function": "mpeg4_is_resync", "file": "libavcodec/mpeg4videodec.c"}, {"function": "ff_mpeg4_decode_video_packet_header", "file": "libavcodec/mpeg4videodec.c"}, {"function": "ff_mpeg4_encode_video_packet_header", "file": "libavcodec/mpeg4videoenc.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

