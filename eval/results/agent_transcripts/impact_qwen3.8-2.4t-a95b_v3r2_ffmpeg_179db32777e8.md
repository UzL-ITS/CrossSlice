# Impact-analysis transcript — ffmpeg @ 179db32777e8 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_mjpeg_decode_sos` (libavcodec/mjpegdec.c), arity 4->1
- truth: [['libavcodec/mjpegbdec.c', 'mjpegb_decode_frame'], ['libavcodec/mjpegdec.c', 'ff_mjpeg_decode_frame_from_buf'], ['libavcodec/mxpegdec.c', 'mxpeg_decode_frame']]

## Self-navigation arm

### Turn 1  _(tok 948+60, stop=tool_use)_

**Reasoning:** Let me search the repository for `ff_mjpeg_decode_sos`.


- `grep(pattern=ff_mjpeg_decode_sos, version=old)` →

```
6 matches
libavcodec/mjpegbdec.c:119:            ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL);
libavcodec/mjpegdec.c:1711:int ff_mjpeg_decode_sos(MJpegDecodeContext *s, const uint8_t *mb_bitmask,
libavcodec/mjpegdec.c:2602:            if ((ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL)) < 0 &&
libavcodec/mjpegdec.h:190:int ff_mjpeg_decode_sos(MJpegDecodeContext *s,
libavcodec/mxpegdec.c:314:                ret = ff_mjpeg_decode_sos(jpg, s->mxm_bitmask, s->bitmask_size, reference_ptr);
libavcodec/mxpegdec.c:318:                ret = ff_mjpeg_decode_sos(jpg, NULL, 0, NULL);
```

### Turn 2  _(tok 1235+259, stop=tool_use)_

**Reasoning:** Let's look at each call site to find the enclosing function names.

1. libavcodec/mjpegbdec.c:119
2. libavcodec/mjpegdec.c:2602
3. libavcodec/mxpegdec.c:314 and 318

Let me read surrounding code.

Also, there might be indirect callers via function pointers, but let's check. Also check other places in the repo (e.g., mjpegdec.h declares it). Let's read files.


- `read_file(path=libavcodec/mjpegbdec.c, start_line=60, end_line=160, version=old)` →

```
libavcodec/mjpegbdec.c lines 60-160 of 182
   60| 
   61| read_header:
   62|     /* reset on every SOI */
   63|     s->restart_interval = 0;
   64|     s->restart_count = 0;
   65|     s->mjpb_skiptosod = 0;
   66| 
   67|     if ((ret = init_get_bits8(&hgb, buf_ptr, /*buf_size*/(buf_end - buf_ptr))) < 0)
   68|         return ret;
   69| 
   70|     skip_bits(&hgb, 32); /* reserved zeros */
   71| 
   72|     if (get_bits_long(&hgb, 32) != MKBETAG('m','j','p','g')) {
   73|         av_log(avctx, AV_LOG_WARNING, "not mjpeg-b (bad fourcc)\n");
   74|         return AVERROR_INVALIDDATA;
   75|     }
   76| 
   77|     field_size = get_bits_long(&hgb, 32); /* field size */
   78|     av_log(avctx, AV_LOG_DEBUG, "field size: 0x%"PRIx32"\n", field_size);
   79|     skip_bits(&hgb, 32); /* padded field size */
   80|     second_field_offs = read_offs(avctx, &hgb, buf_end - buf_ptr, "second_field_offs is %d and size is %d\n");
   81|     av_log(avctx, AV_LOG_DEBUG, "second field offs: 0x%"PRIx32"\n",
   82|            second_field_offs);
   83| 
   84|     dqt_offs = read_offs(avctx, &hgb, buf_end - buf_ptr, "dqt is %d and size is %d\n");
   85|     av_log(avctx, AV_LOG_DEBUG, "dqt offs: 0x%"PRIx32"\n", dqt_offs);
   86|     if (dqt_offs) {
   87|         bytestream2_init(&s->gB, buf_ptr+dqt_offs, buf_end - (buf_ptr+dqt_offs));
   88|         ret = ff_mjpeg_decode_dqt(s);
   89|         if (ret < 0 && (avctx->err_recognition & AV_EF_EXPLODE))
   90|             return ret;
   91|     }
   92| 
   93|     dht_offs = read_offs(avctx, &hgb, buf_end - buf_ptr, "dht is %d and size is %d\n");
   94|     av_log(avctx, AV_LOG_DEBUG, "dht offs: 0x%"PRIx32"\n", dht_offs);
   95|     if (dht_offs) {
   96|         bytestream2_init(&s->gB, buf_ptr+dht_offs, buf_end - (buf_ptr+dht_offs));
   97|         ff_mjpeg_decode_dht(s);
   98|     }
   99| 
  100|     sof_offs = read_offs(avctx, &hgb, buf_end - buf_ptr, "sof is %d and size is %d\n");
  101|     av_log(avctx, AV_LOG_DEBUG, "sof offs: 0x%"PRIx32"\n", sof_offs);
  102|     if (sof_offs) {
  103|         bytestream2_init(&s->gB, buf_ptr+sof_offs, buf_end - (buf_ptr+sof_offs));
  104|         if ((ret = ff_mjpeg_decode_sof(s)) < 0)
  105|             return ret;
  106|     }
  107| 
  108|     sos_offs = read_offs(avctx, &hgb, buf_end - buf_ptr, "sos is %d and size is %d\n");
  109|     av_log(avctx, AV_LOG_DEBUG, "sos offs: 0x%"PRIx32"\n", sos_offs);
  110|     sod_offs = read_offs(avctx, &hgb, buf_end - buf_ptr, "sof is %d and size is %d\n");
  111|     av_log(avctx, AV_LOG_DEBUG, "sod offs: 0x%"PRIx32"\n", sod_offs);
  112|     if (sos_offs) {
  113|         bytestream2_init(&s->gB, buf_ptr+sos_offs,
  114|                          FFMIN(field_size, buf_end - buf_ptr - sos_offs));
  115|         s->mjpb_skiptosod = (sod_offs - sos_offs - bytestream2_peek_be16(&s->gB));
  116|         if (avctx->skip_frame == AVDISCARD_ALL) {
  117|             bytestream2_skipu(&s->gB, bytestream2_get_bytes_left(&s->gB));
  118|         } else {
  119|             ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL);
  120|             if (ret < 0 && (avctx->err_recognition & AV_EF_EXPLODE))
  121|                 return ret;
  122|         }
  123|     }
  124| 
  125|     if (s->interlaced) {
  126|         s->bottom_field ^= 1;
  127|         /* if not bottom field, do not output image yet */
  128|         if (s->bottom_field != s->interlace_polarity && second_field_offs) {
  129|             buf_ptr = buf + second_field_offs;
  130|             goto read_header;
  131|         }
  132|     }
  133| 
  134|     //XXX FIXME factorize, this looks very similar to the EOI code
  135| 
  136|     if(!s->got_picture) {
  137|         av_log(avctx, AV_LOG_WARNING, "no picture\n");
  138|         return buf_size;
  139|     }
  140|     av_frame_move_ref(rframe, s->picture_ptr);
  141|     s->got_picture = 0;
  142|     if (avctx->skip_frame == AVDISCARD_ALL)
  143|         return buf_size;
  144|     *got_frame = 1;
  145| 
  146|     if (!s->lossless && avctx->debug & FF_DEBUG_QP) {
  147|         av_log(avctx, AV_LOG_DEBUG, "QP: %d\n",
  148|                FFMAX3(s->qscale[0], s->qscale[1], s->qscale[2]));
  149|     }
  150| 
  151|     return buf_size;
  152| }
  153| 
  154| const FFCodec ff_mjpegb_decoder = {
  155|     .p.name         = "mjpegb",
  156|     CODEC_LONG_NAME("Apple MJPEG-B"),
  157|     .p.type         = AVMEDIA_TYPE_VIDEO,
  158|     .p.id           = AV_CODEC_ID_MJPEGB,
  159|     .priv_data_size = sizeof(MJpegDecodeContext),
  160|     .init           = ff_mjpeg_decode_init,
```

- `read_file(path=libavcodec/mxpegdec.c, start_line=230, end_line=360, version=old)` →

```
libavcodec/mxpegdec.c lines 230-360 of 363
  230|             goto the_end;
  231|         case DQT:
  232|             ret = ff_mjpeg_decode_dqt(jpg);
  233|             if (ret < 0) {
  234|                 av_log(avctx, AV_LOG_ERROR,
  235|                        "quantization table decode error\n");
  236|                 return ret;
  237|             }
  238|             break;
  239|         case DHT:
  240|             ret = ff_mjpeg_decode_dht(jpg);
  241|             if (ret < 0) {
  242|                 av_log(avctx, AV_LOG_ERROR,
  243|                        "huffman table decode error\n");
  244|                 return ret;
  245|             }
  246|             break;
  247|         case COM:
  248|             ret = mxpeg_decode_com(s, buf_ptr, bytes_left);
  249|             if (ret < 0)
  250|                 return ret;
  251|             break;
  252|         case SOF0:
  253|             if (s->got_sof_data > 1) {
  254|                 av_log(avctx, AV_LOG_ERROR,
  255|                        "Multiple SOF in a frame\n");
  256|                 return AVERROR_INVALIDDATA;
  257|             }
  258|             ret = ff_mjpeg_decode_sof(jpg);
  259|             if (ret < 0) {
  260|                 av_log(avctx, AV_LOG_ERROR,
  261|                        "SOF data decode error\n");
  262|                 s->got_sof_data = 0;
  263|                 return ret;
  264|             }
  265|             if (jpg->interlaced) {
  266|                 av_log(avctx, AV_LOG_ERROR,
  267|                        "Interlaced mode not supported in MxPEG\n");
  268|                 s->got_sof_data = 0;
  269|                 return AVERROR(EINVAL);
  270|             }
  271|             s->got_sof_data ++;
  272|             break;
  273|         case SOS:
  274|             if (!s->got_sof_data) {
  275|                 av_log(avctx, AV_LOG_WARNING,
  276|                        "Can not process SOS without SOF data, skipping\n");
  277|                 break;
  278|             }
  279|             if (!jpg->got_picture) {
  280|                 if (jpg->first_picture) {
  281|                     av_log(avctx, AV_LOG_WARNING,
  282|                            "First picture has no SOF, skipping\n");
  283|                     break;
  284|                 }
  285|                 if (!s->got_mxm_bitmask){
  286|                     av_log(avctx, AV_LOG_WARNING,
  287|                            "Non-key frame has no MXM, skipping\n");
  288|                     break;
  289|                 }
  290|                 /* use stored SOF data to allocate current picture */
  291|                 av_frame_unref(jpg->picture_ptr);
  292|                 if ((ret = ff_get_buffer(avctx, jpg->picture_ptr,
  293|                                          AV_GET_BUFFER_FLAG_REF)) < 0)
  294|                     return ret;
  295|                 jpg->picture_ptr->pict_type = AV_PICTURE_TYPE_P;
  296|                 jpg->picture_ptr->flags &= ~AV_FRAME_FLAG_KEY;
  297|                 jpg->got_picture = 1;
  298|             } else {
  299|                 jpg->picture_ptr->pict_type = AV_PICTURE_TYPE_I;
  300|                 jpg->picture_ptr->flags |= AV_FRAME_FLAG_KEY;
  301|             }
  302| 
  303|             if (s->got_mxm_bitmask) {
  304|                 AVFrame *reference_ptr = s->picture[s->picture_index ^ 1];
  305|                 if (mxpeg_check_dimensions(s, jpg, reference_ptr) < 0)
  306|                     break;
  307| 
  308|                 /* allocate dummy reference picture if needed */
  309|                 if (!reference_ptr->data[0] &&
  310|                     (ret = ff_get_buffer(avctx, reference_ptr,
  311|                                          AV_GET_BUFFER_FLAG_REF)) < 0)
  312|                     return ret;
  313| 
  314|                 ret = ff_mjpeg_decode_sos(jpg, s->mxm_bitmask, s->bitmask_size, reference_ptr);
  315|                 if (ret < 0 && (avctx->err_recognition & AV_EF_EXPLODE))
  316|                     return ret;
  317|             } else {
  318|                 ret = ff_mjpeg_decode_sos(jpg, NULL, 0, NULL);
  319|                 if (ret < 0 && (avctx->err_recognition & AV_EF_EXPLODE))
  320|                     return ret;
  321|             }
  322| 
  323|             break;
  324|         }
  325| 
  326|         buf_ptr += bytestream2_tell(&jpg->gB);
  327|     }
  328| 
  329| the_end:
  330|     if (jpg->got_picture) {
  331|         int ret = av_frame_ref(rframe, jpg->picture_ptr);
  332|         if (ret < 0)
  333|             return ret;
  334|         *got_frame = 1;
  335| 
  336|         s->picture_index ^= 1;
  337|         jpg->picture_ptr = s->picture[s->picture_index];
  338| 
  339|         if (!s->has_complete_frame) {
  340|             if (!s->got_mxm_bitmask)
  341|                 s->has_complete_frame = 1;
  342|             else
  343|                 *got_frame = 0;
  344|         }
  345|     }
  346| 
  347|     return buf_ptr - buf;
  348| }
  349| 
  350| const FFCodec ff_mxpeg_decoder = {
  351|     .p.name         = "mxpeg",
  352|     CODEC_LONG_NAME("Mobotix MxPEG video"),
  353|     .p.type         = AVMEDIA_TYPE_VIDEO,
  354|     .p.id           = AV_CODEC_ID_MXPEG,
  355|     .priv_data_size = sizeof(MXpegDecodeContext),
  356|     .init           = mxpeg_decode_init,
  357|     .close          = mxpeg_decode_end,
  358|     FF_CODEC_DECODE_CB(mxpeg_decode_frame),
  359|     .p.capabilities = AV_CODEC_CAP_DR1,
  360|     .p.max_lowres   = 3,
```

### Turn 3  _(tok 5495+255, stop=tool_use)_

**Reasoning:** Now the enclosing function names. Let's find function definitions in each file preceding these lines.

For mjpegbdec.c: find function starting before line 60.
For mxpegdec.c: find function containing line 314 — likely mxpeg_decode_frame.
For mjpegdec.c line 2602 — likely ff_mjpeg_decode_frame_internal or mjpeg_decode_app / ff_mjpeg_receive_frame.

Let me grep for function definitions.


- `grep(max_results=50, path_glob=libavcodec/mjpegbdec.c, pattern=^[a-zA-Z_].*\(, version=old)` →

```
2 matches
libavcodec/mjpegbdec.c:34:static uint32_t read_offs(AVCodecContext *avctx, GetBitContext *gb, uint32_t size, const char *err_msg){
libavcodec/mjpegbdec.c:43:static int mjpegb_decode_frame(AVCodecContext *avctx, AVFrame *rframe,
```

- `grep(max_results=50, path_glob=libavcodec/mxpegdec.c, pattern=^[a-zA-Z_].*\(, version=old)` →

```
7 matches
libavcodec/mxpegdec.c:48:static av_cold int mxpeg_decode_end(AVCodecContext *avctx)
libavcodec/mxpegdec.c:65:static av_cold int mxpeg_decode_init(AVCodecContext *avctx)
libavcodec/mxpegdec.c:82:static int mxpeg_decode_app(MXpegDecodeContext *s,
libavcodec/mxpegdec.c:94:static int mxpeg_decode_mxm(MXpegDecodeContext *s,
libavcodec/mxpegdec.c:147:static int mxpeg_decode_com(MXpegDecodeContext *s,
libavcodec/mxpegdec.c:162:static int mxpeg_check_dimensions(MXpegDecodeContext *s, MJpegDecodeContext *jpg,
libavcodec/mxpegdec.c:193:static int mxpeg_decode_frame(AVCodecContext *avctx, AVFrame *rframe,
```

### Turn 4  _(tok 6081+124, stop=tool_use)_

**Reasoning:** Now mjpegdec.c line 2602. Let's look for function definitions in mjpegdec.c around there.


- `grep(max_results=80, path_glob=libavcodec/mjpegdec.c, pattern=^(static\s+)?[a-zA-Z_][a-zA-Z0-9_ \*]*\(.*\)\s*$, version=old)` →

```
25 matches
libavcodec/mjpegdec.c:60:static int init_default_huffman_tables(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:103:static void parse_avid(MJpegDecodeContext *s, uint8_t *buf, int len)
libavcodec/mjpegdec.c:113:static void init_idct(AVCodecContext *avctx)
libavcodec/mjpegdec.c:122:av_cold int ff_mjpeg_decode_init(AVCodecContext *avctx)
libavcodec/mjpegdec.c:192:static int mjpeg_parse_len(MJpegDecodeContext *s, int *plen, const char *name)
libavcodec/mjpegdec.c:204:int ff_mjpeg_decode_dqt(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:247:int ff_mjpeg_decode_dht(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:306:int ff_mjpeg_decode_sof(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:835:static inline int mjpeg_decode_dc(MJpegDecodeContext *s, int dc_index, int *val)
libavcodec/mjpegdec.c:1077:static int handle_rstn(MJpegDecodeContext *s, int nb_components)
libavcodec/mjpegdec.c:1112:static int ljpeg_decode_rgb_scan(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:1288:static int ljpeg_decode_yuv_scan(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:1463:static void shift_output(MJpegDecodeContext *s, uint8_t *ptr, int linesize)
libavcodec/mjpegdec.c:1622:static int mjpeg_decode_scan_progressive_ac(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:1676:static void mjpeg_idct_scan_progressive_ac(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:1856:static int mjpeg_decode_dri(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:1868:static int mjpeg_decode_app(MJpegDecodeContext *s, int start_code)
libavcodec/mjpegdec.c:2168:static int mjpeg_decode_com(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:2212:int ff_mjpeg_find_marker(const uint8_t **pbuf_ptr, const uint8_t *buf_end)
libavcodec/mjpegdec.c:2238:static int mjpeg_unescape_sos(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:2389:static void reset_icc_profile(MJpegDecodeContext *s)
libavcodec/mjpegdec.c:2919:av_cold int ff_mjpeg_decode_end(AVCodecContext *avctx)
libavcodec/mjpegdec.c:2956:static av_cold void decode_flush(AVCodecContext *avctx)
libavcodec/mjpegdec.c:3029:static void smv_process_frame(AVCodecContext *avctx, AVFrame *frame)
libavcodec/mjpegdec.c:3048:static int smvjpeg_receive_frame(AVCodecContext *avctx, AVFrame *frame)
```

### Turn 5  _(tok 6994+150, stop=tool_use)_

**Reasoning:** Line 2602 lies between 2389 (reset_icc_profile) and 2919 (ff_mjpeg_decode_end). So there is a function defined there that doesn't match the grep pattern (perhaps multi-line signature). Let me read around 2400-2450 and around 2602.


- `read_file(end_line=2420, path=libavcodec/mjpegdec.c, start_line=2395, version=old)` →

```
libavcodec/mjpegdec.c lines 2395-2420 of 3101
 2395|             av_freep(&s->iccentries[i].data);
 2396|         av_freep(&s->iccentries);
 2397|     }
 2398| 
 2399|     s->iccread = 0;
 2400|     s->iccnum  = 0;
 2401| }
 2402| 
 2403| int ff_mjpeg_decode_frame_from_buf(AVCodecContext *avctx, AVFrame *frame,
 2404|                                    int *got_frame, const AVPacket *avpkt,
 2405|                                    const uint8_t *buf, const int buf_size)
 2406| {
 2407|     MJpegDecodeContext *s = avctx->priv_data;
 2408|     const uint8_t *buf_end, *buf_ptr;
 2409|     int hshift, vshift;
 2410|     int start_code;
 2411|     int index;
 2412|     int ret = 0;
 2413|     int is16bit;
 2414| 
 2415|     s->force_pal8 = 0;
 2416| 
 2417|     s->buf_size = buf_size;
 2418| 
 2419|     av_exif_free(&s->exif_metadata);
 2420|     av_freep(&s->stereo3d);
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 7170+213, stop=tool_use, forced)_

**Reasoning:** The caller at line 2602 is inside ff_mjpeg_decode_frame_from_buf.

So callers:
- mjpegb_decode_frame in libavcodec/mjpegbdec.c
- ff_mjpeg_decode_frame_from_buf in libavcodec/mjpegdec.c
- mxpeg_decode_frame in libavcodec/mxpegdec.c

Confidence: high (grep found 6 matches; 2 are declaration/definition, 1 is header prototype).


- **submit_callers** → `{"callers": [{"function": "mjpegb_decode_frame", "file": "libavcodec/mjpegbdec.c"}, {"function": "ff_mjpeg_decode_frame_from_buf", "file": "libavcodec/mjpegdec.c"}, {"function": "mxpeg_decode_frame", "file": "libavcodec/mxpegdec.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2777+121, stop=tool_use)_

**Reasoning:** I need to find all call sites of `ff_mjpeg_decode_sos`.


- `grep(pattern=ff_mjpeg_decode_sos, version=old, max_results=100)` →

```
6 matches
libavcodec/mjpegbdec.c:119:            ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL);
libavcodec/mjpegdec.c:1711:int ff_mjpeg_decode_sos(MJpegDecodeContext *s, const uint8_t *mb_bitmask,
libavcodec/mjpegdec.c:2602:            if ((ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL)) < 0 &&
libavcodec/mjpegdec.h:190:int ff_mjpeg_decode_sos(MJpegDecodeContext *s,
libavcodec/mxpegdec.c:314:                ret = ff_mjpeg_decode_sos(jpg, s->mxm_bitmask, s->bitmask_size, reference_ptr);
libavcodec/mxpegdec.c:318:                ret = ff_mjpeg_decode_sos(jpg, NULL, 0, NULL);
```

- `get_callers(name=ff_mjpeg_decode_sos, limit=100)` →

```
{
  "name": "ff_mjpeg_decode_sos",
  "version": "old",
  "callers": [
    {
      "caller": "mjpegb_decode_frame",
      "file": "libavcodec/mjpegbdec.c",
      "line": 119
    },
    {
      "caller": "ff_mjpeg_decode_frame_from_buf",
      "file": "libavcodec/mjpegdec.c",
      "line": 2602
    },
    {
      "caller": "mxpeg_decode_frame",
      "file": "libavcodec/mxpegdec.c",
      "line": 314
    },
    {
      "caller": "mxpeg_decode_frame",
      "file": "libavcodec/mxpegdec.c",
      "line": 318
    }
  ]
}
```

### Turn 2  _(tok 3345+220, stop=tool_use)_

**Reasoning:** Let me verify the enclosing function names by reading context around lines. Let me check mjpegdec.c line 2602 enclosing function, and mxpegdec.c lines 314/318.

Also need to check for calls via function pointers, or macro wrappers. Let's grep for "decode_sos" in general.


- `get_context_at(file=libavcodec/mjpegdec.c, line=2602)` →

```
ff_mjpeg_decode_frame_from_buf — libavcodec/mjpegdec.c:2403 [function] int ff_mjpeg_decode_frame_from_buf(AVCodecContext *avctx, AVFrame *frame, int *got_frame, const AVPacket *avpkt, const uint8_t *buf, const int buf_size)
  reads: avctx, buf, buf_size, frame, got_frame; writes: avctx*, buf*, frame*, got_frame*; returns: return AVERROR_INVALIDDATA; | return ret; | return ret; | return AVERROR(ENOSYS); | return ret; | return ret;

SLICE around line 2602 (def-use, level 2; '>' marks the seed):
int ff_mjpeg_decode_frame_from_buf(AVCodecContext *avctx, AVFrame *frame, int *got_frame, const AVPacket *avpkt, const uint8_t *buf, const int buf_size) {
   MJpegDecodeContext *s = avctx->priv_data;
   const uint8_t *buf_end, *buf_ptr;
   int hshift, vshift;
   ...
   s->force_pal8 = 0;
   s->buf_size = buf_size;
   ...
   s->adobe_transform = -1;
   ...
   buf_ptr = buf;
   buf_end = buf + buf_size;
   while(buf_ptr < buf_end) {
     start_code = ff_mjpeg_find_marker(&buf_ptr, buf_end);
   ...
     switch(start_code) {
       case SOI: s->restart_interval = 0; s->restart_count = 0; s->raw_image_buffer = buf_ptr; s->raw_image_buffer_size = buf_end - buf_ptr; break;
         s->restart_interval = 0;
       s->restart_count = 0;
       s->raw_image_buffer = buf_ptr;
       s->raw_image_buffer_size = buf_end - buf_ptr;
   ...
       case SOF1: if(start_code == SOF0)avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_BASELINE_DCT; else avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_EXTENDED_SEQUENTIAL_DCT; s->lossless = 0; s->ls = 0; s->progressive = 0; if((ret = ff_mjpeg_decode_sof(s))< 0)goto fail; break;
         if(start_code == SOF0)
   ...
         else
           avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_EXTENDED_SEQUENTIAL_DCT;
       s->lossless = 0;
       s->ls = 0;
       s->progressive = 0;
   ...
       case SOF2: avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_PROGRESSIVE_DCT; s->lossless = 0; s->ls = 0; s->progressive = 1; if((ret = ff_mjpeg_decode_sof(s))< 0)goto fail; break;
         avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_PROGRESSIVE_DCT;
       s->lossless = 0;
       s->ls = 0;
       s->progressive = 1;
   ...
       case SOF3:
         avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_LOSSLESS;
   ...
       s->lossless = 1;
       s->ls = 0;
       s->progressive = 0;
   ...
       case SOF55:
         avctx->profile = AV_PROFILE_MJPEG_JPEG_LS;
   ...
       s->lossless = 1;
       s->ls = 1;
       s->progressive = 0;
   ...
       case EOI: eoi_parser: if(!avctx->hwaccel && s->progressive && s->cur_scan && s->got_picture)mjpeg_idct_scan_progressive_ac(s); s->cur_scan = 0; if(!s->got_picture) {
   ...
       s->cur_scan = 0;
   ...
       if(s->interlaced) {
         s->bottom_field ^= 1;
   ...
       }
       if(avctx->hwaccel) {
         ret = FF_HW_SIMPLE_CALL(avctx, end_frame);
   ...
       }
       if((ret = av_frame_ref(frame, s->picture_ptr))< 0)
   ...
       if(s->lossless)
         frame->flags |= AV_FRAME_FLAG_LOSSLESS;
   ...
       s->got_picture = 0;
   ...
       }
       case SOS: s->cur_scan++; if((ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL))< 0 &&(avctx->err_recognition & AV_EF_EXPLODE))goto fail; break;
         s->cur_scan++;
>      if((ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL))< 0 &&(avctx->err_recognition & AV_EF_EXPLODE))
         goto fail;
   ...
       case DRI: if((ret = mjpeg_decode_dri(s))< 0)return ret; break;
         if((ret = mjpeg_decode_dri(s))< 0)
           return ret;
   ...
     }
   }
   ...
   return ret;
   ...
   if(AV_RB32(s->upscale_h)) {
   ...
     ret = av_pix_fmt_get_chroma_sub_sample(avctx->pix_fmt, &hshift, &vshift);
     if(ret)
       return ret;
   ...
   }
   if(AV_RB32(s->upscale_v)) {
   ...
     ret = av_pix_fmt_get_chroma_sub_sample(avctx->pix_fmt, &hshift, &vshift);
     if(ret)
       return ret;
   ...
   }
   if(s->flipped && !s->rgb) {
     ret = av_pix_fmt_get_chroma_sub_sample(avctx->pix_fmt, &hshift, &vshift);
     if(ret)
       return ret;
   ...
     for(index=0; index<s->nb_components; index++) {
   ...
       if(frame->data[index]) {
         frame->data[index] +=(h - 1)* frame->linesize[index];
         frame->linesize[index] *= -1;
       }
     }
   }
   ...
   if(s->iccnum != 0 && s->iccnum == s->iccread) {
     AVFrameSideData *sd;
   ...
     for(int i = 0;; i < s->iccnum; i++)
   ...
       total_size += s->iccentries[i].length;
     ret = ff_frame_new_side_data(avctx, frame, AV_FRAME_DATA_ICC_PROFILE, total_size, &sd);
     if(ret < 0) {
   ...
       return ret;
   ...
     }
   }
   if(s->exif_metadata.entries) {
     ret = ff_decode_exif_attach_ifd(avctx, frame, &s->exif_metadata);
   ...
     if(ret < 0)
   ...
   }
}

CALLEES (32):
  av_exif_free (libavcodec/exif.c:658): reads ifd; writes ifd*; returns -
  av_freep (libavutil/mem.c:247 (1 of 2 definitions)): reads arg; writes arg*; returns -
  reset_icc_profile (libavcodec/mjpegdec.c:2389): reads s; writes s*; returns -
  av_log (libavutil/log.c:443 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  bytestream2_tell (libavcodec/bytestream.h:192): reads g; writes -; returns return(int)(g->buffer - g->buffer_start);
  mjpeg_decode_dri (libavcodec/mjpegdec.c:1856): reads s; writes s*; returns return AVERROR_INVALIDDATA; | return 0;
  ff_mjpeg_decode_sos (libavcodec/mjpegdec.c:1711): reads mb_bitmask, mb_bitmask_size, reference, s; writes s*; returns return AVERROR_INVALIDDATA; | return ret; | return AVERROR_INVALIDDATA; | return AVERROR_PATCHWELCOME; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;
  av_frame_ref (libavutil/frame.c:278): reads dst, src; writes dst*, src*; returns return 0; | return 0; | return ret;
  mjpeg_idct_scan_progressive_ac (libavcodec/mjpegdec.c:1676): reads s; writes -; returns -
  ff_jpegls_decode_lse (libavcodec/jpeglsdec.c:51): reads s; writes s*; returns return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_PATCHWELCOME; | return AVERROR_PATCHWELCOME; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;
  ff_mjpeg_decode_dht (libavcodec/mjpegdec.c:247): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return ret;
  ff_mjpeg_decode_dqt (libavcodec/mjpegdec.c:204): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return 0;
  mjpeg_decode_com (libavcodec/mjpegdec.c:2168): reads s; writes s*; returns return ret; | return 0; | return AVERROR(ENOMEM); | return 0;
  mjpeg_decode_app (libavcodec/mjpegdec.c:1868): reads s, start_code; writes s*; returns return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return 0;
  bytestream2_init (libavcodec/bytestream.h:137): reads buf, buf_size, g; writes g*; returns -
  ff_mjpeg_find_marker (libavcodec/mjpegdec.c:2212): reads buf_end, pbuf_ptr; writes pbuf_ptr*; returns return val;
  av_pix_fmt_desc_get (libavutil/pixdesc.c:3456): reads pix_fmt; writes -; returns return NULL; | return &av_pix_fmt_descriptors[pix_fmt];
  av_pix_fmt_count_planes (libavutil/pixdesc.c:3496): reads pix_fmt; writes -; returns return AVERROR(EINVAL); | return ret;
  av_pix_fmt_get_chroma_sub_sample (libavutil/pixdesc.c:3484): reads h_shift, pix_fmt, v_shift; writes h_shift*, v_shift*; returns return AVERROR(ENOSYS); | return 0;
  av_stereo3d_create_side_data (libavutil/stereo3d.c:54): reads frame; writes -; returns return NULL; | return(AVStereo3D *)side_data->data;
  ff_frame_new_side_data (libavcodec/decode.c:2127): reads avctx, frame, psd, size, type; writes psd*; returns return 0; | return sd ? 0 : AVERROR(ENOMEM);
  ff_decode_exif_attach_ifd (libavcodec/decode.c:2430): reads avctx, frame, ifd; writes -; returns return exif_attach_ifd(avctx, frame, ifd, &dummy);
  FFMAX3 [macro]: #define FFMAX3(a,b,c) FFMAX(FFMAX(a,b),c)
  FF_HW_SIMPLE_CALL [macro]: #define FF_HW_SIMPLE_CALL(avctx, function) \
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)
  av_err2str [macro]: #define av_err2str(errnum) \
  av_assert0 [macro]: #define av_assert0(cond) do { \
  AV_CEIL_RSHIFT [macro]: #define AV_CEIL_RSHIFT(a,b) (!av_builtin_constant_p(b) ? -((-(a)) >> (b)) \
  AV_RB32 [macro (1 of 4 definitions)]: # define AV_RB32(p) AV_RB(32, p)
  FFSWAP [macro (1 of 2 definitions)]: #define FFSWAP(type,a,b) do{type SWAP_tmp= b; b= a; a= SWAP_tmp;}while(0)
  not defined in this repository: ff_mjpeg_decode_sof
  not shown (1): MKTAG

CALLERS (2):
  ff_mjpeg_decode_frame (libavcodec/mjpegdec.c:2912): return ff_mjpeg_decode_frame_from_buf(avctx, frame, got_frame,
  sp5x_decode_frame (libavcodec/sp5xdec.c:88): ret = ff_mjpeg_decode_frame_from_buf(avctx, frame, got_frame,
```

- `get_context_at(file=libavcodec/mxpegdec.c, line=314)` →

```
mxpeg_decode_frame — libavcodec/mxpegdec.c:193 [function] static int mxpeg_decode_frame(AVCodecContext *avctx, AVFrame *rframe, int *got_frame, AVPacket *avpkt)
  reads: avctx, avpkt, got_frame, rframe; writes: avctx*, avpkt*, got_frame*; returns: return AVERROR_PATCHWELCOME; | return ret; | return ret; | return ret; | return AVERROR_INVALIDDATA; | return ret;

SLICE around line 314 (def-use, level 2; '>' marks the seed):
static int mxpeg_decode_frame(AVCodecContext *avctx, AVFrame *rframe, int *got_frame, AVPacket *avpkt) {
   const uint8_t *buf = avpkt->data;
   int buf_size = avpkt->size;
   MXpegDecodeContext *s = avctx->priv_data;
   MJpegDecodeContext *jpg = &s->jpg;
   ...
   buf_ptr = buf;
   buf_end = buf + buf_size;
   jpg->got_picture = 0;
   s->got_mxm_bitmask = 0;
   ...
   while(buf_ptr < buf_end) {
     start_code = ff_mjpeg_find_marker(&buf_ptr, buf_end);
   ...
     switch(start_code) {
   ...
       case SOS: if(!s->got_sof_data) {
   ...
       if(!jpg->got_picture) {
   ...
         jpg->picture_ptr->pict_type = AV_PICTURE_TYPE_P;
         jpg->picture_ptr->flags &= ~AV_FRAME_FLAG_KEY;
         jpg->got_picture = 1;
       } else {
         jpg->picture_ptr->pict_type = AV_PICTURE_TYPE_I;
         jpg->picture_ptr->flags |= AV_FRAME_FLAG_KEY;
       }
       if(s->got_mxm_bitmask) {
         AVFrame *reference_ptr = s->picture[s->picture_index ^ 1];
   ...
>        ret = ff_mjpeg_decode_sos(jpg, s->mxm_bitmask, s->bitmask_size, reference_ptr);
         if(ret < 0 &&(avctx->err_recognition & AV_EF_EXPLODE))
           return ret;
       } else {
         ret = ff_mjpeg_decode_sos(jpg, NULL, 0, NULL);
         if(ret < 0 &&(avctx->err_recognition & AV_EF_EXPLODE))
           return ret;
   ...
       }
       }
     }
   }
}

CALLEES (15):
  bytestream2_tell (libavcodec/bytestream.h:192): reads g; writes -; returns return(int)(g->buffer - g->buffer_start);
  ff_mjpeg_decode_sos (libavcodec/mjpegdec.c:1711): reads mb_bitmask, mb_bitmask_size, reference, s; writes s*; returns return AVERROR_INVALIDDATA; | return ret; | return AVERROR_INVALIDDATA; | return AVERROR_PATCHWELCOME; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;
  ff_get_buffer (libavcodec/decode.c:1729): reads avctx, flags, frame; writes avctx*, frame*; returns return ret;
  mxpeg_check_dimensions (libavcodec/mxpegdec.c:162): reads jpg, reference_ptr, s; writes -; returns return AVERROR(EINVAL); | return AVERROR(EINVAL); | return AVERROR_INVALIDDATA; | return 0;
  av_frame_unref (libavutil/frame.c:496): reads frame; writes frame*; returns -
  av_log (libavutil/log.c:443 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  mxpeg_decode_com (libavcodec/mxpegdec.c:147): reads buf_ptr, buf_size, s; writes s*; returns return 0; | return ret;
  ff_mjpeg_decode_dht (libavcodec/mjpegdec.c:247): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return ret;
  ff_mjpeg_decode_dqt (libavcodec/mjpegdec.c:204): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return 0;
  mxpeg_decode_app (libavcodec/mxpegdec.c:82): reads buf_ptr, buf_size, s; writes s*; returns return 0; | return 0;
  bytestream2_init (libavcodec/bytestream.h:137): reads buf, buf_size, g; writes g*; returns -
  ff_mjpeg_find_marker (libavcodec/mjpegdec.c:2212): reads buf_end, pbuf_ptr; writes pbuf_ptr*; returns return val;
  av_frame_ref (libavutil/frame.c:278): reads dst, src; writes dst*, src*; returns return 0; | return 0; | return ret;
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)
  not defined in this repository: ff_mjpeg_decode_sof

CALLERS (0):
```

- `grep(max_results=100, pattern=decode_sos, version=old)` →

```
10 matches
libavcodec/mjpegbdec.c:119:            ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL);
libavcodec/mjpegdec.c:1711:int ff_mjpeg_decode_sos(MJpegDecodeContext *s, const uint8_t *mb_bitmask,
libavcodec/mjpegdec.c:1732:                                      "decode_sos: nb_components (%d)",
libavcodec/mjpegdec.c:1737:        av_log(s->avctx, AV_LOG_ERROR, "decode_sos: len(%d) mismatch %d components\n", len, s->nb_components_sos);
libavcodec/mjpegdec.c:1749:                   "decode_sos: index(%d) out of components\n", index);
libavcodec/mjpegdec.c:1852:    av_log(s->avctx, AV_LOG_ERROR, "decode_sos: ac/dc index out of range\n");
libavcodec/mjpegdec.c:2602:            if ((ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL)) < 0 &&
libavcodec/mjpegdec.h:190:int ff_mjpeg_decode_sos(MJpegDecodeContext *s,
libavcodec/mxpegdec.c:314:                ret = ff_mjpeg_decode_sos(jpg, s->mxm_bitmask, s->bitmask_size, reference_ptr);
libavcodec/mxpegdec.c:318:                ret = ff_mjpeg_decode_sos(jpg, NULL, 0, NULL);
```

### Turn 3  _(tok 8167+120, stop=tool_use)_

**Reasoning:** Only three distinct calling functions. Verify mjpegbdec.c line 119 enclosing function name is mjpegb_decode_frame.

Also check sp5xdec.c — it calls ff_mjpeg_decode_frame_from_buf, not sos directly. Good.

Submit list of unique functions (dedupe mxpeg two call sites into one entry).


- `get_context_at(file=libavcodec/mjpegbdec.c, line=119)` →

```
mjpegb_decode_frame — libavcodec/mjpegbdec.c:43 [function] static int mjpegb_decode_frame(AVCodecContext *avctx, AVFrame *rframe, int *got_frame, AVPacket *avpkt)
  reads: avctx, avpkt, got_frame, rframe; writes: avctx*, got_frame*; returns: return ret; | return AVERROR_INVALIDDATA; | return ret; | return ret; | return ret; | return buf_size;

SLICE around line 119 (def-use, level 2; '>' marks the seed):
static int mjpegb_decode_frame(AVCodecContext *avctx, AVFrame *rframe, int *got_frame, AVPacket *avpkt) {
   const uint8_t *buf = avpkt->data;
   int buf_size = avpkt->size;
   MJpegDecodeContext *s = avctx->priv_data;
   const uint8_t *buf_end, *buf_ptr;
   GetBitContext hgb;
   ...
   buf_ptr = buf;
   buf_end = buf + buf_size;
   s->got_picture = 0;
   s->adobe_transform = -1;
   s->buf_size = buf_size;
   ...
   s->restart_interval = 0;
   s->restart_count = 0;
   s->mjpb_skiptosod = 0;
   ...
   sos_offs = read_offs(avctx, &hgb, buf_end - buf_ptr, "sos is %d and size is %d\n");
   ...
   sod_offs = read_offs(avctx, &hgb, buf_end - buf_ptr, "sof is %d and size is %d\n");
   ...
   if(sos_offs) {
   ...
     s->mjpb_skiptosod =(sod_offs - sos_offs - bytestream2_peek_be16(&s->gB));
     if(avctx->skip_frame == AVDISCARD_ALL) {
   ...
     } else {
>      ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL);
       if(ret < 0 &&(avctx->err_recognition & AV_EF_EXPLODE))
         return ret;
   ...
     }
   }
}

CALLEES (17):
  init_get_bits8 (libavcodec/get_bits.h:544 (1 of 2 definitions)): reads buffer, byte_size, s; writes -; returns return init_get_bits(s, buffer, byte_size * 8);
  skip_bits (libavcodec/get_bits.h:383 (1 of 2 definitions)): reads n, s; writes s*; returns -
  av_log (libavutil/log.c:443 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  get_bits_long (libavcodec/get_bits.h:424 (1 of 2 definitions)): reads n, s; writes s*; returns return 0; | return get_bits(s, n); | return tmp; | return ret |(get_bits(s, n - 16)<< 16); | return ret | get_bits(s, n - 16);
  read_offs (libavcodec/mjpegbdec.c:34): reads avctx, err_msg, gb, size; writes -; returns return 0; | return offs;
  ff_mjpeg_decode_dqt (libavcodec/mjpegdec.c:204): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return 0;
  bytestream2_init (libavcodec/bytestream.h:137): reads buf, buf_size, g; writes g*; returns -
  ff_mjpeg_decode_dht (libavcodec/mjpegdec.c:247): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return ret;
  ff_mjpeg_decode_sos (libavcodec/mjpegdec.c:1711): reads mb_bitmask, mb_bitmask_size, reference, s; writes s*; returns return AVERROR_INVALIDDATA; | return ret; | return AVERROR_INVALIDDATA; | return AVERROR_PATCHWELCOME; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;
  bytestream2_skipu (libavcodec/bytestream.h:174): reads g, size; writes g*; returns -
  bytestream2_get_bytes_left (libavcodec/bytestream.h:158): reads g; writes -; returns return g->buffer_end - g->buffer;
  av_frame_move_ref (libavutil/frame.c:523): reads dst, src; writes dst*; returns -
  MKBETAG [macro]: #define MKBETAG(a,b,c,d) ((d) | ((c) << 8) | ((b) << 16) | ((unsigned)(a) << 24))
  FFMIN [macro (1 of 4 definitions)]: #define FFMIN(a,b) ((a) > (b) ? (b) : (a))
  FFMAX3 [macro]: #define FFMAX3(a,b,c) FFMAX(FFMAX(a,b),c)
  not defined in this repository: ff_mjpeg_decode_sof, bytestream2_peek_be16

CALLERS (0):
```

### Turn 4  _(tok 9547+315, stop=tool_use)_

**Reasoning:** All three confirmed. Also check whether there's any indirect reference (e.g., function pointer table) — grep found only those. Also check for any files outside libavcodec (e.g., tests) — grep covered whole repo.

Submit.


**Says:** 

All call sites verified — 4 call sites across 3 functions (the declaration in `mjpegdec.h`, the definition in `mjpegdec.c:1711`, and log strings were excluded):

| Function | File | Call site(s) |
|---|---|---|
| `mjpegb_decode_frame` | `libavcodec/mjpegbdec.c` | 119 |
| `ff_mjpeg_decode_frame_from_buf` | `libavcodec/mjpegdec.c` | 2602 |
| `mxpeg_decode_frame` | `libavcodec/mxpegdec.c` | 314, 318 |



- **submit_callers** → `{"callers": [{"function": "mjpegb_decode_frame", "file": "libavcodec/mjpegbdec.c"}, {"function": "ff_mjpeg_decode_frame_from_buf", "file": "libavcodec/mjpegdec.c"}, {"function": "mxpeg_decode_frame", "file": "libavcodec/mxpegdec.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2354+109, stop=tool_use)_

**Reasoning:** Let me start by getting the callers of ff_mjpeg_decode_sos.


**Says:** 

I'll look up the callers of `ff_mjpeg_decode_sos`.




- `get_callers(name=ff_mjpeg_decode_sos, limit=50)` →

```
{
  "name": "ff_mjpeg_decode_sos",
  "version": "old",
  "callers": [
    {
      "caller": "mjpegb_decode_frame",
      "file": "libavcodec/mjpegbdec.c",
      "line": 119
    },
    {
      "caller": "ff_mjpeg_decode_frame_from_buf",
      "file": "libavcodec/mjpegdec.c",
      "line": 2602
    },
    {
      "caller": "mxpeg_decode_frame",
      "file": "libavcodec/mxpegdec.c",
      "line": 314
    },
    {
      "caller": "mxpeg_decode_frame",
      "file": "libavcodec/mxpegdec.c",
      "line": 318
    }
  ]
}
```

- `resolve_symbol(name=ff_mjpeg_decode_sos)` →

```
{
  "resolved": true,
  "name": "ff_mjpeg_decode_sos",
  "version": "old",
  "file": "libavcodec/mjpegdec.c",
  "line": 1711,
  "kind": "function",
  "signature": "int ff_mjpeg_decode_sos(MJpegDecodeContext *s, const uint8_t *mb_bitmask, int mb_bitmask_size, const AVFrame *reference)",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 2  _(tok 2821+365, stop=tool_use)_

**Reasoning:** Now let's check the call sites. Note the version is "old" by default? The description says `version`: "work" (files on disk), "old" (parent of `rev`) or "new" (`rev`); `rev` defaults to the server's commit, else HEAD. The output says "version": "old". Hmm, that's odd — I didn't specify a version. Anyway.

Let me get the work version to compare.

Actually the tools default seems to be reporting "old". Let me try get_callers with the work version... but there's no version param in get_callers schema. The schema only has limit, name, rev. Hmm, no version parameter. The rev defaults to the server's commit. So "old" means parent of rev. Interesting — maybe the tool defaults to old.

Let me pass rev explicitly as something. Actually, let me just verify with other tools. Let me look at the call sites themselves to confirm they're real calls.

Let me check each caller with get_context_at or get_neighborhood.


- `get_context_at(file=libavcodec/mjpegbdec.c, line=119)` →

```
mjpegb_decode_frame — libavcodec/mjpegbdec.c:43 [function] static int mjpegb_decode_frame(AVCodecContext *avctx, AVFrame *rframe, int *got_frame, AVPacket *avpkt)
  reads: avctx, avpkt, got_frame, rframe; writes: avctx*, got_frame*; returns: return ret; | return AVERROR_INVALIDDATA; | return ret; | return ret; | return ret; | return buf_size;

SLICE around line 119 (def-use, level 2; '>' marks the seed):
static int mjpegb_decode_frame(AVCodecContext *avctx, AVFrame *rframe, int *got_frame, AVPacket *avpkt) {
   const uint8_t *buf = avpkt->data;
   int buf_size = avpkt->size;
   MJpegDecodeContext *s = avctx->priv_data;
   const uint8_t *buf_end, *buf_ptr;
   GetBitContext hgb;
   ...
   buf_ptr = buf;
   buf_end = buf + buf_size;
   s->got_picture = 0;
   s->adobe_transform = -1;
   s->buf_size = buf_size;
   ...
   s->restart_interval = 0;
   s->restart_count = 0;
   s->mjpb_skiptosod = 0;
   ...
   sos_offs = read_offs(avctx, &hgb, buf_end - buf_ptr, "sos is %d and size is %d\n");
   ...
   sod_offs = read_offs(avctx, &hgb, buf_end - buf_ptr, "sof is %d and size is %d\n");
   ...
   if(sos_offs) {
   ...
     s->mjpb_skiptosod =(sod_offs - sos_offs - bytestream2_peek_be16(&s->gB));
     if(avctx->skip_frame == AVDISCARD_ALL) {
   ...
     } else {
>      ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL);
       if(ret < 0 &&(avctx->err_recognition & AV_EF_EXPLODE))
         return ret;
   ...
     }
   }
}

CALLEES (17):
  init_get_bits8 (libavcodec/get_bits.h:544 (1 of 2 definitions)): reads buffer, byte_size, s; writes -; returns return init_get_bits(s, buffer, byte_size * 8);
  skip_bits (libavcodec/get_bits.h:383 (1 of 2 definitions)): reads n, s; writes s*; returns -
  av_log (libavutil/log.c:443 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  get_bits_long (libavcodec/get_bits.h:424 (1 of 2 definitions)): reads n, s; writes s*; returns return 0; | return get_bits(s, n); | return tmp; | return ret |(get_bits(s, n - 16)<< 16); | return ret | get_bits(s, n - 16);
  read_offs (libavcodec/mjpegbdec.c:34): reads avctx, err_msg, gb, size; writes -; returns return 0; | return offs;
  ff_mjpeg_decode_dqt (libavcodec/mjpegdec.c:204): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return 0;
  bytestream2_init (libavcodec/bytestream.h:137): reads buf, buf_size, g; writes g*; returns -
  ff_mjpeg_decode_dht (libavcodec/mjpegdec.c:247): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return ret;
  ff_mjpeg_decode_sos (libavcodec/mjpegdec.c:1711): reads mb_bitmask, mb_bitmask_size, reference, s; writes s*; returns return AVERROR_INVALIDDATA; | return ret; | return AVERROR_INVALIDDATA; | return AVERROR_PATCHWELCOME; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;
  bytestream2_skipu (libavcodec/bytestream.h:174): reads g, size; writes g*; returns -
  bytestream2_get_bytes_left (libavcodec/bytestream.h:158): reads g; writes -; returns return g->buffer_end - g->buffer;
  av_frame_move_ref (libavutil/frame.c:523): reads dst, src; writes dst*; returns -
  MKBETAG [macro]: #define MKBETAG(a,b,c,d) ((d) | ((c) << 8) | ((b) << 16) | ((unsigned)(a) << 24))
  FFMIN [macro (1 of 4 definitions)]: #define FFMIN(a,b) ((a) > (b) ? (b) : (a))
  FFMAX3 [macro]: #define FFMAX3(a,b,c) FFMAX(FFMAX(a,b),c)
  not defined in this repository: ff_mjpeg_decode_sof, bytestream2_peek_be16

CALLERS (0):
```

- `get_context_at(file=libavcodec/mjpegdec.c, line=2602)` →

```
ff_mjpeg_decode_frame_from_buf — libavcodec/mjpegdec.c:2403 [function] int ff_mjpeg_decode_frame_from_buf(AVCodecContext *avctx, AVFrame *frame, int *got_frame, const AVPacket *avpkt, const uint8_t *buf, const int buf_size)
  reads: avctx, buf, buf_size, frame, got_frame; writes: avctx*, buf*, frame*, got_frame*; returns: return AVERROR_INVALIDDATA; | return ret; | return ret; | return AVERROR(ENOSYS); | return ret; | return ret;

SLICE around line 2602 (def-use, level 2; '>' marks the seed):
int ff_mjpeg_decode_frame_from_buf(AVCodecContext *avctx, AVFrame *frame, int *got_frame, const AVPacket *avpkt, const uint8_t *buf, const int buf_size) {
   MJpegDecodeContext *s = avctx->priv_data;
   const uint8_t *buf_end, *buf_ptr;
   int hshift, vshift;
   ...
   s->force_pal8 = 0;
   s->buf_size = buf_size;
   ...
   s->adobe_transform = -1;
   ...
   buf_ptr = buf;
   buf_end = buf + buf_size;
   while(buf_ptr < buf_end) {
     start_code = ff_mjpeg_find_marker(&buf_ptr, buf_end);
   ...
     switch(start_code) {
       case SOI: s->restart_interval = 0; s->restart_count = 0; s->raw_image_buffer = buf_ptr; s->raw_image_buffer_size = buf_end - buf_ptr; break;
         s->restart_interval = 0;
       s->restart_count = 0;
       s->raw_image_buffer = buf_ptr;
       s->raw_image_buffer_size = buf_end - buf_ptr;
   ...
       case SOF1: if(start_code == SOF0)avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_BASELINE_DCT; else avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_EXTENDED_SEQUENTIAL_DCT; s->lossless = 0; s->ls = 0; s->progressive = 0; if((ret = ff_mjpeg_decode_sof(s))< 0)goto fail; break;
         if(start_code == SOF0)
   ...
         else
           avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_EXTENDED_SEQUENTIAL_DCT;
       s->lossless = 0;
       s->ls = 0;
       s->progressive = 0;
   ...
       case SOF2: avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_PROGRESSIVE_DCT; s->lossless = 0; s->ls = 0; s->progressive = 1; if((ret = ff_mjpeg_decode_sof(s))< 0)goto fail; break;
         avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_PROGRESSIVE_DCT;
       s->lossless = 0;
       s->ls = 0;
       s->progressive = 1;
   ...
       case SOF3:
         avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_LOSSLESS;
   ...
       s->lossless = 1;
       s->ls = 0;
       s->progressive = 0;
   ...
       case SOF55:
         avctx->profile = AV_PROFILE_MJPEG_JPEG_LS;
   ...
       s->lossless = 1;
       s->ls = 1;
       s->progressive = 0;
   ...
       case EOI: eoi_parser: if(!avctx->hwaccel && s->progressive && s->cur_scan && s->got_picture)mjpeg_idct_scan_progressive_ac(s); s->cur_scan = 0; if(!s->got_picture) {
   ...
       s->cur_scan = 0;
   ...
       if(s->interlaced) {
         s->bottom_field ^= 1;
   ...
       }
       if(avctx->hwaccel) {
         ret = FF_HW_SIMPLE_CALL(avctx, end_frame);
   ...
       }
       if((ret = av_frame_ref(frame, s->picture_ptr))< 0)
   ...
       if(s->lossless)
         frame->flags |= AV_FRAME_FLAG_LOSSLESS;
   ...
       s->got_picture = 0;
   ...
       }
       case SOS: s->cur_scan++; if((ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL))< 0 &&(avctx->err_recognition & AV_EF_EXPLODE))goto fail; break;
         s->cur_scan++;
>      if((ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL))< 0 &&(avctx->err_recognition & AV_EF_EXPLODE))
         goto fail;
   ...
       case DRI: if((ret = mjpeg_decode_dri(s))< 0)return ret; break;
         if((ret = mjpeg_decode_dri(s))< 0)
           return ret;
   ...
     }
   }
   ...
   return ret;
   ...
   if(AV_RB32(s->upscale_h)) {
   ...
     ret = av_pix_fmt_get_chroma_sub_sample(avctx->pix_fmt, &hshift, &vshift);
     if(ret)
       return ret;
   ...
   }
   if(AV_RB32(s->upscale_v)) {
   ...
     ret = av_pix_fmt_get_chroma_sub_sample(avctx->pix_fmt, &hshift, &vshift);
     if(ret)
       return ret;
   ...
   }
   if(s->flipped && !s->rgb) {
     ret = av_pix_fmt_get_chroma_sub_sample(avctx->pix_fmt, &hshift, &vshift);
     if(ret)
       return ret;
   ...
     for(index=0; index<s->nb_components; index++) {
   ...
       if(frame->data[index]) {
         frame->data[index] +=(h - 1)* frame->linesize[index];
         frame->linesize[index] *= -1;
       }
     }
   }
   ...
   if(s->iccnum != 0 && s->iccnum == s->iccread) {
     AVFrameSideData *sd;
   ...
     for(int i = 0;; i < s->iccnum; i++)
   ...
       total_size += s->iccentries[i].length;
     ret = ff_frame_new_side_data(avctx, frame, AV_FRAME_DATA_ICC_PROFILE, total_size, &sd);
     if(ret < 0) {
   ...
       return ret;
   ...
     }
   }
   if(s->exif_metadata.entries) {
     ret = ff_decode_exif_attach_ifd(avctx, frame, &s->exif_metadata);
   ...
     if(ret < 0)
   ...
   }
}

CALLEES (32):
  av_exif_free (libavcodec/exif.c:658): reads ifd; writes ifd*; returns -
  av_freep (libavutil/mem.c:247 (1 of 2 definitions)): reads arg; writes arg*; returns -
  reset_icc_profile (libavcodec/mjpegdec.c:2389): reads s; writes s*; returns -
  av_log (libavutil/log.c:443 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  bytestream2_tell (libavcodec/bytestream.h:192): reads g; writes -; returns return(int)(g->buffer - g->buffer_start);
  mjpeg_decode_dri (libavcodec/mjpegdec.c:1856): reads s; writes s*; returns return AVERROR_INVALIDDATA; | return 0;
  ff_mjpeg_decode_sos (libavcodec/mjpegdec.c:1711): reads mb_bitmask, mb_bitmask_size, reference, s; writes s*; returns return AVERROR_INVALIDDATA; | return ret; | return AVERROR_INVALIDDATA; | return AVERROR_PATCHWELCOME; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;
  av_frame_ref (libavutil/frame.c:278): reads dst, src; writes dst*, src*; returns return 0; | return 0; | return ret;
  mjpeg_idct_scan_progressive_ac (libavcodec/mjpegdec.c:1676): reads s; writes -; returns -
  ff_jpegls_decode_lse (libavcodec/jpeglsdec.c:51): reads s; writes s*; returns return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_PATCHWELCOME; | return AVERROR_PATCHWELCOME; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;
  ff_mjpeg_decode_dht (libavcodec/mjpegdec.c:247): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return ret;
  ff_mjpeg_decode_dqt (libavcodec/mjpegdec.c:204): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return 0;
  mjpeg_decode_com (libavcodec/mjpegdec.c:2168): reads s; writes s*; returns return ret; | return 0; | return AVERROR(ENOMEM); | return 0;
  mjpeg_decode_app (libavcodec/mjpegdec.c:1868): reads s, start_code; writes s*; returns return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return 0;
  bytestream2_init (libavcodec/bytestream.h:137): reads buf, buf_size, g; writes g*; returns -
  ff_mjpeg_find_marker (libavcodec/mjpegdec.c:2212): reads buf_end, pbuf_ptr; writes pbuf_ptr*; returns return val;
  av_pix_fmt_desc_get (libavutil/pixdesc.c:3456): reads pix_fmt; writes -; returns return NULL; | return &av_pix_fmt_descriptors[pix_fmt];
  av_pix_fmt_count_planes (libavutil/pixdesc.c:3496): reads pix_fmt; writes -; returns return AVERROR(EINVAL); | return ret;
  av_pix_fmt_get_chroma_sub_sample (libavutil/pixdesc.c:3484): reads h_shift, pix_fmt, v_shift; writes h_shift*, v_shift*; returns return AVERROR(ENOSYS); | return 0;
  av_stereo3d_create_side_data (libavutil/stereo3d.c:54): reads frame; writes -; returns return NULL; | return(AVStereo3D *)side_data->data;
  ff_frame_new_side_data (libavcodec/decode.c:2127): reads avctx, frame, psd, size, type; writes psd*; returns return 0; | return sd ? 0 : AVERROR(ENOMEM);
  ff_decode_exif_attach_ifd (libavcodec/decode.c:2430): reads avctx, frame, ifd; writes -; returns return exif_attach_ifd(avctx, frame, ifd, &dummy);
  FFMAX3 [macro]: #define FFMAX3(a,b,c) FFMAX(FFMAX(a,b),c)
  FF_HW_SIMPLE_CALL [macro]: #define FF_HW_SIMPLE_CALL(avctx, function) \
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)
  av_err2str [macro]: #define av_err2str(errnum) \
  av_assert0 [macro]: #define av_assert0(cond) do { \
  AV_CEIL_RSHIFT [macro]: #define AV_CEIL_RSHIFT(a,b) (!av_builtin_constant_p(b) ? -((-(a)) >> (b)) \
  AV_RB32 [macro (1 of 4 definitions)]: # define AV_RB32(p) AV_RB(32, p)
  FFSWAP [macro (1 of 2 definitions)]: #define FFSWAP(type,a,b) do{type SWAP_tmp= b; b= a; a= SWAP_tmp;}while(0)
  not defined in this repository: ff_mjpeg_decode_sof
  not shown (1): MKTAG

CALLERS (2):
  ff_mjpeg_decode_frame (libavcodec/mjpegdec.c:2912): return ff_mjpeg_decode_frame_from_buf(avctx, frame, got_frame,
  sp5x_decode_frame (libavcodec/sp5xdec.c:88): ret = ff_mjpeg_decode_frame_from_buf(avctx, frame, got_frame,
```

- `get_context_at(file=libavcodec/mxpegdec.c, line=314)` →

```
mxpeg_decode_frame — libavcodec/mxpegdec.c:193 [function] static int mxpeg_decode_frame(AVCodecContext *avctx, AVFrame *rframe, int *got_frame, AVPacket *avpkt)
  reads: avctx, avpkt, got_frame, rframe; writes: avctx*, avpkt*, got_frame*; returns: return AVERROR_PATCHWELCOME; | return ret; | return ret; | return ret; | return AVERROR_INVALIDDATA; | return ret;

SLICE around line 314 (def-use, level 2; '>' marks the seed):
static int mxpeg_decode_frame(AVCodecContext *avctx, AVFrame *rframe, int *got_frame, AVPacket *avpkt) {
   const uint8_t *buf = avpkt->data;
   int buf_size = avpkt->size;
   MXpegDecodeContext *s = avctx->priv_data;
   MJpegDecodeContext *jpg = &s->jpg;
   ...
   buf_ptr = buf;
   buf_end = buf + buf_size;
   jpg->got_picture = 0;
   s->got_mxm_bitmask = 0;
   ...
   while(buf_ptr < buf_end) {
     start_code = ff_mjpeg_find_marker(&buf_ptr, buf_end);
   ...
     switch(start_code) {
   ...
       case SOS: if(!s->got_sof_data) {
   ...
       if(!jpg->got_picture) {
   ...
         jpg->picture_ptr->pict_type = AV_PICTURE_TYPE_P;
         jpg->picture_ptr->flags &= ~AV_FRAME_FLAG_KEY;
         jpg->got_picture = 1;
       } else {
         jpg->picture_ptr->pict_type = AV_PICTURE_TYPE_I;
         jpg->picture_ptr->flags |= AV_FRAME_FLAG_KEY;
       }
       if(s->got_mxm_bitmask) {
         AVFrame *reference_ptr = s->picture[s->picture_index ^ 1];
   ...
>        ret = ff_mjpeg_decode_sos(jpg, s->mxm_bitmask, s->bitmask_size, reference_ptr);
         if(ret < 0 &&(avctx->err_recognition & AV_EF_EXPLODE))
           return ret;
       } else {
         ret = ff_mjpeg_decode_sos(jpg, NULL, 0, NULL);
         if(ret < 0 &&(avctx->err_recognition & AV_EF_EXPLODE))
           return ret;
   ...
       }
       }
     }
   }
}

CALLEES (15):
  bytestream2_tell (libavcodec/bytestream.h:192): reads g; writes -; returns return(int)(g->buffer - g->buffer_start);
  ff_mjpeg_decode_sos (libavcodec/mjpegdec.c:1711): reads mb_bitmask, mb_bitmask_size, reference, s; writes s*; returns return AVERROR_INVALIDDATA; | return ret; | return AVERROR_INVALIDDATA; | return AVERROR_PATCHWELCOME; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA;
  ff_get_buffer (libavcodec/decode.c:1729): reads avctx, flags, frame; writes avctx*, frame*; returns return ret;
  mxpeg_check_dimensions (libavcodec/mxpegdec.c:162): reads jpg, reference_ptr, s; writes -; returns return AVERROR(EINVAL); | return AVERROR(EINVAL); | return AVERROR_INVALIDDATA; | return 0;
  av_frame_unref (libavutil/frame.c:496): reads frame; writes frame*; returns -
  av_log (libavutil/log.c:443 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  mxpeg_decode_com (libavcodec/mxpegdec.c:147): reads buf_ptr, buf_size, s; writes s*; returns return 0; | return ret;
  ff_mjpeg_decode_dht (libavcodec/mjpegdec.c:247): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return ret;
  ff_mjpeg_decode_dqt (libavcodec/mjpegdec.c:204): reads s; writes s*; returns return ret; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return AVERROR_INVALIDDATA; | return 0;
  mxpeg_decode_app (libavcodec/mxpegdec.c:82): reads buf_ptr, buf_size, s; writes s*; returns return 0; | return 0;
  bytestream2_init (libavcodec/bytestream.h:137): reads buf, buf_size, g; writes g*; returns -
  ff_mjpeg_find_marker (libavcodec/mjpegdec.c:2212): reads buf_end, pbuf_ptr; writes pbuf_ptr*; returns return val;
  av_frame_ref (libavutil/frame.c:278): reads dst, src; writes dst*, src*; returns return 0; | return 0; | return ret;
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)
  not defined in this repository: ff_mjpeg_decode_sof

CALLERS (0):
```

### Turn 3  _(tok 8675+242, stop=tool_use)_

**Reasoning:** All three call sites confirmed (mxpeg has two calls, same function).

Now let me double-check whether there are any other callers that gtags might have missed. Possible candidates:
- libavcodec/sp5xdec.c — calls ff_mjpeg_decode_frame_from_buf, not sos directly.
- libavcodec/mdec.c? No.
- libavcodec/jpeglsdec? 
- libavcodec/tdsc? 
- libavcodec/flashsv?
- Actually there might be a caller in libavcodec/mjpegdec.c itself in `mjpeg_decode_frame`... but that's now ff_mjpeg_decode_frame_from_buf.

Let me also check whether there's an "ipudec" or "mjpeg_decode_sos" (without ff_ prefix) static function. Also let me check the header declaration in mjpegdec.h and see if anything else references.

Let me check with a different approach — expand_function on ff_mjpeg_decode_sos to see callers.


- `expand_function(name=ff_mjpeg_decode_sos)` →

```
{
  "name": "ff_mjpeg_decode_sos",
  "version": "old",
  "levels": 1,
  "node": {
    "name": "ff_mjpeg_decode_sos",
    "file": "libavcodec/mjpegdec.c",
    "line": 1711,
    "kind": "function",
    "state": "analyzed"
  },
  "callees": [
    {
      "name": "av_log",
      "file": "libavutil/log.c",
      "line": 443,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        1719,
        1737,
        1742,
        1748,
        1796,
        1852
      ]
    },
    {
      "name": "bytestream2_skipu",
      "file": "libavcodec/bytestream.h",
      "line": 174,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        1847
      ]
    },
    {
      "name": "av_assert0",
      "file": "libavutil/avassert.h",
      "line": 42,
      "kind": "macro",
      "state": "analyzed",
      "call_lines": [
        1818,
        1833
      ]
    },
    {
      "name": "MKTAG",
      "file": "libavutil/macros.h",
      "line": 55,
      "kind": "macro",
      "state": "analyzed",
      "call_lines": [
        1753
      ]
    },
    {
      "name": "mjpeg_parse_len",
      "file": "libavcodec/mjpegdec.c",
      "line": 192,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1724
      ]
    },
    {
      "name": "avpriv_report_missing_feature",
      "file": "libavutil/log.c",
      "line": 520,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1731
      ]
    },
    {
      "name": "bytestream2_skip",
      "file": "libavcodec/bytestream.h",
      "line": 168,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1804
      ]
    },
    {
      "name": "mjpeg_unescape_sos",
      "file": "libavcodec/mjpegdec.c",
      "line": 2238,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1806
      ]
    },
    {
      "name": "mjpeg_decode_scan",
      "file": "libavcodec/mjpegdec.c",
      "line": 1478,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1837
      ]
    },
    {
      "name": "mjpeg_decode_scan_progressive_ac",
      "file": "libavcodec/mjpegdec.c",
      "line": 1622,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1834
      ]
    },
    {
      "name": "ljpeg_decode_yuv_scan",
      "file": "libavcodec/mjpegdec.c",
      "line": 1288,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1827
      ]
    },
    {
      "name": "ljpeg_decode_rgb_scan",
      "file": "libavcodec/mjpegdec.c",
      "line": 1112,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1824
      ]
    },
    {
      "name": "ff_jpegls_decode_picture",
      "file": "libavcodec/jpeglsdec.c",
      "line": 355,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1820
      ]
    },
    {
      "name": "FF_HW_CALL",
      "file": "libavcodec/hwaccel_internal.h",
      "line": 173,
      "kind": "macro",
      "state": "summarized",
      "call_lines": [
        1811
      ]
    },
    {
      "name": "get_bits_count",
      "file": "libavcodec/get_bits.h",
      "line": 254,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1847
      ]
    }
  ],
  "callers": [
    {
      "name": "mjpegb_decode_frame",
      "file": "libavcodec/mjpegbdec.c",
      "line": 43,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        119
      ]
    },
    {
      "name": "ff_mjpeg_decode_frame_from_buf",
      "file": "libavcodec/mjpegdec.c",
      "line": 2403,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        2602
      ]
    },
    {
      "name": "mxpeg_decode_frame",
      "file": "libavcodec/mxpegdec.c",
      "line": 193,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        314,
        318
      ]
    }
  ]
}
```

### Turn 4  _(tok 10475+826, stop=tool_use)_

**Reasoning:** The list is consistent: three distinct enclosing functions.

Let me sanity-check that there isn't some other file calling it via a function-pointer assignment, e.g. in a struct. That wouldn't be a "call". Also check `libavcodec/mjpegdec.h` for the declaration — that's a prototype, not a call.

One more possibility: a caller in an arch-specific or a different version, e.g., `libavcodec/vaapi_mjpeg.c`? Unlikely.

Let me verify by checking the header declaration and confirming there's no other file. Actually, since there's no grep, I'll rely on gtags. The gtags result resolved uniquely and callers were found across 3 files. That's likely complete.

However, note the "version": "old" — the default. Should I check "work"? The question says "the signature is about to change" so we want the current state. The tools returned version "old" which is parent of rev. Hmm, that's the default behavior. There's no version param on get_callers/expand_function — only `rev`. If rev defaults to the server's commit, then "old" = parent of that commit. That seems like the tool defaults to old always. Let me try passing a rev explicitly to see if it changes... Actually I don't know the commit hash. 

Let me try resolve_symbol with version... resolve_symbol also only has `rev`. Hmm, the description mentions `version` but the schema doesn't have it. So probably it's fixed.

Actually wait — get_function_source has `rev` too. The descriptions mention version but schemas lack it. So the tools operate on a fixed version. Fine.

Let me just double check there is no additional caller that gtags missed due to a weird macro-based call. One way: check `ff_mjpeg_decode_frame_from_buf` callers — no. 

Let me also consider `libavcodec/mjpegdec.c` might have another internal call inside `mjpeg_decode_frame`? Already covered.

I'm reasonably confident. Let me do one more sanity check: look at the header prototype usage — get_type_definition won't help. Let me check get_neighborhood for ff_mjpeg_decode_sos to see if callers list matches (already done via expand).

I'll submit.


**Says:** 

Both query paths (gtags caller index and the on-demand graph) agree, and I verified each call site in context:

- `mjpegb_decode_frame` — `libavcodec/mjpegbdec.c:119` → `ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL);`
- `ff_mjpeg_decode_frame_from_buf` — `libavcodec/mjpegdec.c:2602` → `case SOS: ... ff_mjpeg_decode_sos(s, NULL, 0, NULL)`
- `mxpeg_decode_frame` — `libavcodec/mxpegdec.c:314` and `:318` (two real calls: one with `s->mxm_bitmask`/`reference_ptr`, one with NULLs)

`sp5x_decode_frame` and `ff_mjpeg_decode_frame` only reach it indirectly through `ff_mjpeg_decode_frame_from_buf`, so they are not direct call sites. The `mjpegdec.h` prototype and the definition itself are excluded.



- **submit_callers** → `{"callers": [{"function": "mjpegb_decode_frame", "file": "libavcodec/mjpegbdec.c"}, {"function": "ff_mjpeg_decode_frame_from_buf", "file": "libavcodec/mjpegdec.c"}, {"function": "mxpeg_decode_frame", "file": "libavcodec/mxpegdec.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

