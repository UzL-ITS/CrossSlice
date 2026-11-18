# Impact-analysis transcript — ffmpeg @ 545724f61e65 — openrouter:deepseek/deepseek-v4-pro

- target: `ff_mpeg4_get_video_packet_prefix_length` (libavcodec/mpeg4video.c), arity 1->3
- truth: [['libavcodec/mpeg4videodec.c', 'ff_mpeg4_decode_video_packet_header'], ['libavcodec/mpeg4videodec.c', 'mpeg4_is_resync'], ['libavcodec/mpeg4videoenc.c', 'ff_mpeg4_encode_video_packet_header']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1044+105, stop=tool_use)_

**Reasoning:** The user wants me to find every call site of `ff_mpeg4_get_video_packet_prefix_length` in the repository. Let me use the find_references tool to find all references, then determine the enclosing functions for each reference.

- `find_references(name=ff_mpeg4_get_video_packet_prefix_length)` →

```
4 references
ff_mpeg4_get_video_packet_prefix_length   31 libavcodec/mpeg4video.h int ff_mpeg4_get_video_packet_prefix_length(MpegEncContext *s);
ff_mpeg4_get_video_packet_prefix_length  424 libavcodec/mpeg4videodec.c             if (len >= ff_mpeg4_get_video_packet_prefix_length(s))
ff_mpeg4_get_video_packet_prefix_length  717 libavcodec/mpeg4videodec.c     if (len != ff_mpeg4_get_video_packet_prefix_length(s)) {
ff_mpeg4_get_video_packet_prefix_length 1396 libavcodec/mpeg4videoenc.c     put_bits(&s->pb, ff_mpeg4_get_video_packet_prefix_length(&s->c), 0);
```

### Turn 2  _(tok 1337+367, stop=tool_use)_

**Reasoning:** Let me identify the enclosing functions for each call site:

1. `libavcodec/mpeg4video.h:31` - This is a prototype/declaration, not a call site. Skip.
2. `libavcodec/mpeg4videodec.c:424` - Need to find the enclosing function.
3. `libavcodec/mpeg4videodec.c:717` - Need to find the enclosing function.
4. `libavcodec/mpeg4videoenc.c:1396` - Need to find the enclosing function.

Let me read the relevant areas to find the enclosing functions

- `read_file(path=libavcodec/mpeg4videodec.c, start_line=410, end_line=435)` →

```
libavcodec/mpeg4videodec.c lines 410-435 of 4004
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
```

- `read_file(path=libavcodec/mpeg4videodec.c, start_line=700, end_line=730)` →

```
libavcodec/mpeg4videodec.c lines 700-730 of 4004
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

- `read_file(path=libavcodec/mpeg4videoenc.c, start_line=1380, end_line=1410)` →

```
libavcodec/mpeg4videoenc.c lines 1380-1410 of 1442
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

### Turn 3  _(tok 3184+114, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing function for line 424. Let me scroll up from there to find the function definition

- `read_file(end_line=410, path=libavcodec/mpeg4videodec.c, start_line=370)` →

```
libavcodec/mpeg4videodec.c lines 370-410 of 4004
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
```

### Turn 4  _(tok 3897+377, stop=tool_use)_

**Reasoning:** Now I have all the information:

1. `libavcodec/mpeg4videodec.c:424` — inside `mpeg4_is_resync` (starts at line 377)
2. `libavcodec/mpeg4videodec.c:717` — inside `ff_mpeg4_decode_video_packet_header` (starts at line 702)
3. `libavcodec/mpeg4videoenc.c:1396` — inside `ff_mpeg4_encode_video_packet_header` (starts at line 1392)

Line 31 in `mpeg4video.h` is a prototype, not a call site.

So the callers are:
- `mpeg4_is_resync` in `libavcodec/mpeg4videodec.c`
- `ff_mpeg4_decode_video_packet_header` in `libavcodec/mpeg4videodec.c`
- `ff_mpeg4_encode_video_packet_header` in `libavcodec/mpeg4videoenc.c`

- **submit_callers** → `{"callers": [{"function": "mpeg4_is_resync", "file": "libavcodec/mpeg4videodec.c"}, {"function": "ff_mpeg4_decode_video_packet_header", "file": "libavcodec/mpeg4videodec.c"}, {"function": "ff_mpeg4_encode_video_packet_header", "file": "libavcodec/mpeg4videoenc.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

