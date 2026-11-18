# Impact-analysis transcript — ffmpeg @ 545724f61e65 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_mpeg4_get_video_packet_prefix_length` (libavcodec/mpeg4video.c), arity 1->3
- truth: [['libavcodec/mpeg4videodec.c', 'ff_mpeg4_decode_video_packet_header'], ['libavcodec/mpeg4videodec.c', 'mpeg4_is_resync'], ['libavcodec/mpeg4videoenc.c', 'ff_mpeg4_encode_video_packet_header']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1046+43, stop=tool_use)_

**Reasoning:** I'll try searching for the symbols.

- `find_references(name=ff_mpeg4_get_video_packet_prefix_length)` →

```
4 references
ff_mpeg4_get_video_packet_prefix_length   31 libavcodec/mpeg4video.h int ff_mpeg4_get_video_packet_prefix_length(MpegEncContext *s);
ff_mpeg4_get_video_packet_prefix_length  424 libavcodec/mpeg4videodec.c             if (len >= ff_mpeg4_get_video_packet_prefix_length(s))
ff_mpeg4_get_video_packet_prefix_length  717 libavcodec/mpeg4videodec.c     if (len != ff_mpeg4_get_video_packet_prefix_length(s)) {
ff_mpeg4_get_video_packet_prefix_length 1396 libavcodec/mpeg4videoenc.c     put_bits(&s->pb, ff_mpeg4_get_video_packet_prefix_length(&s->c), 0);
```

### Turn 2  _(tok 1316+245, stop=tool_use)_

**Reasoning:** Now I need to determine the enclosing functions for each reference. Let me read the relevant portions.


- `read_file(path=libavcodec/mpeg4videodec.c, start_line=390, end_line=440, version=old)` →

```
libavcodec/mpeg4videodec.c lines 390-440 of 4004
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

- `read_file(path=libavcodec/mpeg4videodec.c, start_line=690, end_line=740, version=old)` →

```
libavcodec/mpeg4videodec.c lines 690-740 of 4004
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
  731|         return AVERROR_INVALIDDATA;
  732|     }
  733| 
  734|     s->mb_x = mb_num % s->mb_width;
  735|     s->mb_y = mb_num / s->mb_width;
  736| 
  737|     if (ctx->shape != BIN_ONLY_SHAPE) {
  738|         int qscale = get_bits(&s->gb, ctx->quant_precision);
  739|         if (qscale)
  740|             s->chroma_qscale = s->qscale = qscale;
```

- `read_file(path=libavcodec/mpeg4videoenc.c, start_line=1370, end_line=1410, version=old)` →

```
libavcodec/mpeg4videoenc.c lines 1370-1410 of 1442
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

### Turn 3  _(tok 4148+110, stop=tool_use)_

**Reasoning:** I need to identify the function enclosing line 424 in mpeg4videodec.c. Let me read from around line 370 to confirm.

- `read_file(path=libavcodec/mpeg4videodec.c, start_line=360, end_line=395, version=old)` →

```
libavcodec/mpeg4videodec.c lines 360-395 of 4004
  360|                     block[s->idsp.idct_permutation[i]] += ROUNDED_DIV(ac_val[i + 8] * qscale_table[xy], s->qscale);
  361|             }
  362|         }
  363|     }
  364|     /* left copy */
  365|     for (i = 1; i < 8; i++)
  366|         ac_val1[i] = block[s->idsp.idct_permutation[i << 3]];
  367| 
  368|     /* top copy */
  369|     for (i = 1; i < 8; i++)
  370|         ac_val1[8 + i] = block[s->idsp.idct_permutation[i]];
  371| }
  372| 
  373| /**
  374|  * check if the next stuff is a resync marker or the end.
  375|  * @return 0 if not
  376|  */
  377| static inline int mpeg4_is_resync(Mpeg4DecContext *ctx)
  378| {
  379|     MpegEncContext *s = &ctx->m;
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
```

### Turn 4  _(tok 4905+404, stop=tool_use)_

**Reasoning:** So the call sites are:
1. mpeg4videodec.c:424 — inside `mpeg4_is_resync`
2. mpeg4videodec.c:717 — inside `ff_mpeg4_decode_video_packet_header`
3. mpeg4videoenc.c:1396 — inside `ff_mpeg4_encode_video_packet_header`

Let me confirm that the definition in mpeg4video.c itself doesn't call this function (find_references only found 4 references: the prototype, 2 in mpeg4videodec.c, and 1 in mpeg4videoenc.c). Good, complete.

Let's submit.

**Says:** I've found all references to `ff_mpeg4_get_video_packet_prefix_length`. Excluding the prototype in `mpeg4video.h` and the definition itself, the call sites are:

1. `mpeg4_is_resync` in `libavcodec/mpeg4videodec.c` (line 424)
2. `ff_mpeg4_decode_video_packet_header` in `libavcodec/mpeg4videodec.c` (line 717)
3. `ff_mpeg4_encode_video_packet_header` in `libavcodec/mpeg4videoenc.c` (line 1396)



- **submit_callers** → `{"callers": [{"function": "mpeg4_is_resync", "file": "libavcodec/mpeg4videodec.c"}, {"function": "ff_mpeg4_decode_video_packet_header", "file": "libavcodec/mpeg4videodec.c"}, {"function": "ff_mpeg4_encode_video_packet_header", "file": "libavcodec/mpeg4videoenc.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

