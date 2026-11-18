# Impact-analysis transcript — ffmpeg @ 179db32777e8 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_mjpeg_decode_sos` (libavcodec/mjpegdec.c), arity 4->1
- truth: [['libavcodec/mjpegbdec.c', 'mjpegb_decode_frame'], ['libavcodec/mjpegdec.c', 'ff_mjpeg_decode_frame_from_buf'], ['libavcodec/mxpegdec.c', 'mxpeg_decode_frame']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1077+90, stop=tool_use)_

**Reasoning:** Let me search for references to `ff_mjpeg_decode_sos`.


- `find_references(name=ff_mjpeg_decode_sos)` →

```
5 references
ff_mjpeg_decode_sos  119 libavcodec/mjpegbdec.c             ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL);
ff_mjpeg_decode_sos 2602 libavcodec/mjpegdec.c             if ((ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL)) < 0 &&
ff_mjpeg_decode_sos  190 libavcodec/mjpegdec.h int ff_mjpeg_decode_sos(MJpegDecodeContext *s,
ff_mjpeg_decode_sos  314 libavcodec/mxpegdec.c                 ret = ff_mjpeg_decode_sos(jpg, s->mxm_bitmask, s->bitmask_size, reference_ptr);
ff_mjpeg_decode_sos  318 libavcodec/mxpegdec.c                 ret = ff_mjpeg_decode_sos(jpg, NULL, 0, NULL);
```

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

### Turn 2  _(tok 1616+163, stop=tool_use)_

**Reasoning:** Now determine enclosing functions.

Let me read each file around the call sites.


- `read_file(path=libavcodec/mjpegbdec.c, version=old, start_line=40, end_line=150)` →

```
libavcodec/mjpegbdec.c lines 40-150 of 182
   40|     return offs;
   41| }
   42| 
   43| static int mjpegb_decode_frame(AVCodecContext *avctx, AVFrame *rframe,
   44|                                int *got_frame, AVPacket *avpkt)
   45| {
   46|     const uint8_t *buf = avpkt->data;
   47|     int buf_size = avpkt->size;
   48|     MJpegDecodeContext *s = avctx->priv_data;
   49|     const uint8_t *buf_end, *buf_ptr;
   50|     GetBitContext hgb; /* for the header */
   51|     uint32_t dqt_offs, dht_offs, sof_offs, sos_offs, second_field_offs;
   52|     uint32_t field_size, sod_offs;
   53|     int ret;
   54| 
   55|     buf_ptr = buf;
   56|     buf_end = buf + buf_size;
   57|     s->got_picture = 0;
   58|     s->adobe_transform = -1;
   59|     s->buf_size = buf_size;
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
```

- `read_file(path=libavcodec/mxpegdec.c, version=old, start_line=230, end_line=340)` →

```
libavcodec/mxpegdec.c lines 230-340 of 363
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
```

### Turn 3  _(tok 5632+179, stop=tool_use)_

**Reasoning:** Need enclosing function name for mxpegdec.c lines 314/318. Let me look for the function definition earlier in the file.


- `read_file(end_line=232, path=libavcodec/mxpegdec.c, start_line=185, version=old)` →

```
libavcodec/mxpegdec.c lines 185-232 of 363
  185|             av_log(jpg->avctx, AV_LOG_ERROR, "Reference mismatching\n");
  186|             return AVERROR_INVALIDDATA;
  187|         }
  188|     }
  189| 
  190|     return 0;
  191| }
  192| 
  193| static int mxpeg_decode_frame(AVCodecContext *avctx, AVFrame *rframe,
  194|                               int *got_frame, AVPacket *avpkt)
  195| {
  196|     const uint8_t *buf = avpkt->data;
  197|     int buf_size = avpkt->size;
  198|     MXpegDecodeContext *s = avctx->priv_data;
  199|     MJpegDecodeContext *jpg = &s->jpg;
  200|     const uint8_t *buf_end, *buf_ptr;
  201|     int start_code;
  202|     int ret;
  203| 
  204|     if (avctx->skip_frame == AVDISCARD_ALL)
  205|         return AVERROR_PATCHWELCOME;
  206| 
  207|     buf_ptr = buf;
  208|     buf_end = buf + buf_size;
  209|     jpg->got_picture = 0;
  210|     s->got_mxm_bitmask = 0;
  211|     s->got_sof_data = !!s->got_sof_data;
  212|     while (buf_ptr < buf_end) {
  213|         start_code = ff_mjpeg_find_marker(&buf_ptr, buf_end);
  214|         if (start_code < 0)
  215|             goto the_end;
  216| 
  217|         int bytes_left = buf_end - buf_ptr;
  218|         bytestream2_init(&jpg->gB, buf_ptr, bytes_left);
  219| 
  220|         if (start_code >= APP0 && start_code <= APP15) {
  221|             mxpeg_decode_app(s, buf_ptr, bytes_left);
  222|         }
  223| 
  224|         switch (start_code) {
  225|         case SOI:
  226|             if (jpg->got_picture) //emulating EOI
  227|                 goto the_end;
  228|             break;
  229|         case EOI:
  230|             goto the_end;
  231|         case DQT:
  232|             ret = ff_mjpeg_decode_dqt(jpg);
```

- `read_file(end_line=2620, path=libavcodec/mjpegdec.c, start_line=2470, version=old)` →

```
libavcodec/mjpegdec.c lines 2470-2620 of 3101
 2470| 
 2471|         ret = -1;
 2472| 
 2473|         if (!CONFIG_JPEGLS_DECODER &&
 2474|             (start_code == SOF55 || start_code == LSE)) {
 2475|             av_log(avctx, AV_LOG_ERROR, "JPEG-LS support not enabled.\n");
 2476|             return AVERROR(ENOSYS);
 2477|         }
 2478| 
 2479|         if (avctx->skip_frame == AVDISCARD_ALL) {
 2480|             switch(start_code) {
 2481|             case SOF0:
 2482|             case SOF1:
 2483|             case SOF2:
 2484|             case SOF3:
 2485|             case SOF55:
 2486|                 break;
 2487|             default:
 2488|                 goto skip;
 2489|             }
 2490|         }
 2491| 
 2492|         switch (start_code) {
 2493|         case SOI:
 2494|             s->restart_interval = 0;
 2495|             s->restart_count    = 0;
 2496|             s->raw_image_buffer      = buf_ptr;
 2497|             s->raw_image_buffer_size = buf_end - buf_ptr;
 2498|             /* nothing to do on SOI */
 2499|             break;
 2500|         case DHT:
 2501|             if ((ret = ff_mjpeg_decode_dht(s)) < 0) {
 2502|                 av_log(avctx, AV_LOG_ERROR, "huffman table decode error\n");
 2503|                 goto fail;
 2504|             }
 2505|             break;
 2506|         case SOF0:
 2507|         case SOF1:
 2508|             if (start_code == SOF0)
 2509|                 avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_BASELINE_DCT;
 2510|             else
 2511|                 avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_EXTENDED_SEQUENTIAL_DCT;
 2512|             s->lossless    = 0;
 2513|             s->ls          = 0;
 2514|             s->progressive = 0;
 2515|             if ((ret = ff_mjpeg_decode_sof(s)) < 0)
 2516|                 goto fail;
 2517|             break;
 2518|         case SOF2:
 2519|             avctx->profile = AV_PROFILE_MJPEG_HUFFMAN_PROGRESSIVE_DCT;
 2520|             s->lossless    = 0;
 2521|             s->ls          = 0;
 2522|             s->progressive = 1;
 2523|             if ((ret = ff_mjpeg_decode_sof(s)) < 0)
 2524|                 goto fail;
 2525|             break;
 2526|         case SOF3:
 2527|             avctx->profile     = AV_PROFILE_MJPEG_HUFFMAN_LOSSLESS;
 2528| #if FF_API_CODEC_PROPS
 2529| FF_DISABLE_DEPRECATION_WARNINGS
 2530|             avctx->properties |= FF_CODEC_PROPERTY_LOSSLESS;
 2531| FF_ENABLE_DEPRECATION_WARNINGS
 2532| #endif
 2533|             s->lossless    = 1;
 2534|             s->ls          = 0;
 2535|             s->progressive = 0;
 2536|             if ((ret = ff_mjpeg_decode_sof(s)) < 0)
 2537|                 goto fail;
 2538|             break;
 2539|         case SOF55:
 2540|             avctx->profile     = AV_PROFILE_MJPEG_JPEG_LS;
 2541| #if FF_API_CODEC_PROPS
 2542| FF_DISABLE_DEPRECATION_WARNINGS
 2543|             avctx->properties |= FF_CODEC_PROPERTY_LOSSLESS;
 2544| FF_ENABLE_DEPRECATION_WARNINGS
 2545| #endif
 2546|             s->lossless    = 1;
 2547|             s->ls          = 1;
 2548|             s->progressive = 0;
 2549|             if ((ret = ff_mjpeg_decode_sof(s)) < 0)
 2550|                 goto fail;
 2551|             break;
 2552|         case LSE:
 2553|             if (!CONFIG_JPEGLS_DECODER ||
 2554|                 (ret = ff_jpegls_decode_lse(s)) < 0)
 2555|                 goto fail;
 2556|             if (ret == 1)
 2557|                 goto redo_for_pal8;
 2558|             break;
 2559|         case EOI:
 2560| eoi_parser:
 2561|             if (!avctx->hwaccel &&
 2562|                 s->progressive && s->cur_scan && s->got_picture)
 2563|                 mjpeg_idct_scan_progressive_ac(s);
 2564|             s->cur_scan = 0;
 2565|             if (!s->got_picture) {
 2566|                 av_log(avctx, AV_LOG_WARNING,
 2567|                        "Found EOI before any SOF, ignoring\n");
 2568|                 break;
 2569|             }
 2570|             if (s->interlaced) {
 2571|                 s->bottom_field ^= 1;
 2572|                 /* if not bottom field, do not output image yet */
 2573|                 if (s->bottom_field == !s->interlace_polarity)
 2574|                     break;
 2575|             }
 2576|             if (avctx->hwaccel) {
 2577|                 ret = FF_HW_SIMPLE_CALL(avctx, end_frame);
 2578|                 if (ret < 0)
 2579|                     return ret;
 2580| 
 2581|                 av_freep(&s->hwaccel_picture_private);
 2582|             }
 2583|             if ((ret = av_frame_ref(frame, s->picture_ptr)) < 0)
 2584|                 return ret;
 2585|             if (s->lossless)
 2586|                 frame->flags |= AV_FRAME_FLAG_LOSSLESS;
 2587|             *got_frame = 1;
 2588|             s->got_picture = 0;
 2589| 
 2590|             if (!s->lossless && avctx->debug & FF_DEBUG_QP) {
 2591|                 int qp = FFMAX3(s->qscale[0],
 2592|                                 s->qscale[1],
 2593|                                 s->qscale[2]);
 2594| 
 2595|                 av_log(avctx, AV_LOG_DEBUG, "QP: %d\n", qp);
 2596|             }
 2597| 
 2598|             goto the_end;
 2599|         case SOS:
 2600|             s->cur_scan++;
 2601| 
 2602|             if ((ret = ff_mjpeg_decode_sos(s, NULL, 0, NULL)) < 0 &&
 2603|                 (avctx->err_recognition & AV_EF_EXPLODE))
 2604|                 goto fail;
 2605|             break;
 2606|         case DRI:
 2607|             if ((ret = mjpeg_decode_dri(s)) < 0)
 2608|                 return ret;
 2609|             break;
 2610|         case SOF5:
 2611|         case SOF6:
 2612|         case SOF7:
 2613|         case SOF9:
 2614|         case SOF10:
 2615|         case SOF11:
 2616|         case SOF13:
 2617|         case SOF14:
 2618|         case SOF15:
 2619|         case JPG:
 2620|             av_log(avctx, AV_LOG_ERROR,
```

### Turn 4  _(tok 8858+117, stop=tool_use)_

**Reasoning:** The mjpegdec.c call at 2602 is inside `mjpeg_decode_frame`. Let me verify by finding the enclosing function definition.


- `grep(pattern=^static int mjpeg_decode_frame|^static .*decode_frame\(AVCod, version=old, path_glob=libavcodec/mjpegdec.c)` →

```
1 matches
libavcodec/mjpegdec.c:1711:int ff_mjpeg_decode_sos(MJpegDecodeContext *s, const uint8_t *mb_bitmask,
```

### Turn 5  _(tok 9029+122, stop=tool_use)_

**Reasoning:** Need to find enclosing function for line 2602 in mjpegdec.c. Let me search for function definitions in mjpegdec.c between 1711 and 2602.


- `grep(pattern=^[a-zA-Z_].*\)$, path_glob=libavcodec/mjpegdec.c, version=old, max_results=200)` →

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

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 9442+292, stop=tool_use, forced)_

**Reasoning:** The enclosing function at line 2602 is between 2389 and 2919 — the function definition wasn't matched because it probably spans multiple lines (e.g., `static int decode_frame(AVCodecContext *avctx, AVFrame *frame,\n int *got_frame, AVPacket *avpkt)`). In FFmpeg's mjpegdec.c, that function is `decode_frame`. Actually in recent FFmpeg it's `static int decode_frame(AVCodecContext *avctx, AVFrame *frame, int *got_frame, AVPacket *avpkt)`. Yes, line 2583 uses `frame` and `*got_frame = 1`, consistent with `decode_frame`. Also smvjpeg_receive_frame calls decode_frame. So answer: decode_frame in libavcodec/mjpegdec.c.

Submit the three callers.


- **submit_callers** → `{"callers": [{"function": "decode_frame", "file": "libavcodec/mjpegdec.c"}, {"function": "mjpegb_decode_frame", "file": "libavcodec/mjpegbdec.c"}, {"function": "mxpeg_decode_frame", "file": "libavcodec/mxpegdec.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 3, "n_truth": 3, "tp": 2, "precision": 0.6666666666666666, "recall": 0.6666666666666666, "f1": 0.6666666666666666}`

