# Impact-analysis transcript — ffmpeg @ 823c6fc0b8f1 — openrouter:deepseek/deepseek-v4-pro

- target: `ff_attach_decode_data` (libavcodec/decode.c), arity 1->2
- truth: [['libavcodec/amfdec.c', 'amf_amfsurface_to_avframe'], ['libavcodec/decode.c', 'ff_get_buffer'], ['libavcodec/qsvdec.c', 'qsv_get_continuous_buffer'], ['libavcodec/videotoolbox.c', 'ff_videotoolbox_alloc_frame']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1030+90, stop=tool_use)_

**Reasoning:** The user wants me to find every call site of `ff_attach_decode_data` in the repository. Let me first find the definition to confirm the function exists, then find all references to it.

- `find_references(name=ff_attach_decode_data)` →

```
5 references
ff_attach_decode_data  352 libavcodec/amfdec.c         ret = ff_attach_decode_data(frame);
ff_attach_decode_data 1811 libavcodec/decode.c     ret = ff_attach_decode_data(frame);
ff_attach_decode_data   89 libavcodec/decode.h int ff_attach_decode_data(AVFrame *frame);
ff_attach_decode_data  179 libavcodec/qsvdec.c     ret = ff_attach_decode_data(frame);
ff_attach_decode_data  155 libavcodec/videotoolbox.c     int ret = ff_attach_decode_data(frame);
```

### Turn 2  _(tok 1348+591, stop=tool_use)_

**Reasoning:** The references show:

1. libavcodec/amfdec.c:352 - call
2. libavcodec/decode.c:1811 - this might be the definition itself, not a call
3. libavcodec/decode.h:89 - prototype/declaration
4. libavcodec/qsvdec.c:179 - call
5. libavcodec/videotoolbox.c:155 - call

I need to determine the enclosing function for each call site. Let me read the relevant lines to get the function names.

For amfdec.c line 352, qsvdec.c line 179, videotoolbox.c line 155. Also need to check decode.c line 1811 - it says "ret = ff_attach_decode_data(frame);" - that might be a call from within some function, but it could be the definition itself? Let me check.

Actually, ff_attach_decode_data is defined in decode.c. The definition would typically be something like:
int ff_attach_decode_data(AVFrame *frame) { ... }

The reference at line 1811 is "ret = ff_attach_decode_data(frame);" - that looks like a call, not a definition. Maybe the definition is elsewhere, or the function calls itself recursively? Let me check the file to understand.

Let me read the relevant sections to get enclosing function names.

- `read_file(path=libavcodec/amfdec.c, start_line=340, end_line=360)` →

```
libavcodec/amfdec.c lines 340-360 of 664
  340|     int                 ret;
  341|     int                 format_amf;
  342| 
  343|     if (avctx->hw_device_ctx && ((AVHWDeviceContext*)avctx->hw_device_ctx->data)->type == AV_HWDEVICE_TYPE_AMF) {
  344|         // prepare frame similar to  ff_get_buffer(avctx, frame, AV_GET_BUFFER_FLAG_REF);
  345| 
  346|         ret = ff_decode_frame_props(avctx, frame);
  347|         if (ret < 0)
  348|             return ret;
  349| 
  350|         avctx->sw_pix_fmt = avctx->pix_fmt;
  351| 
  352|         ret = ff_attach_decode_data(frame);
  353|         if (ret < 0)
  354|             return ret;
  355|         frame->width  = avctx->width;
  356|         frame->height = avctx->height;
  357| 
  358|         ////
  359|         frame->buf[0] = av_buffer_create((uint8_t *)surface, sizeof(surface),
  360|                                     amf_free_amfsurface, (void*)avctx,
```

- `read_file(path=libavcodec/qsvdec.c, start_line=170, end_line=190)` →

```
libavcodec/qsvdec.c lines 170-190 of 1309
  170|     frame->data[0] = frame->buf[0]->data;
  171|     if (avctx->pix_fmt == AV_PIX_FMT_NV12 ||
  172|         avctx->pix_fmt == AV_PIX_FMT_P010 ||
  173|         avctx->pix_fmt == AV_PIX_FMT_P012) {
  174|         frame->linesize[1] = frame->linesize[0];
  175|         frame->data[1] = frame->data[0] +
  176|             frame->linesize[0] * FFALIGN(avctx->coded_height, 64);
  177|     }
  178| 
  179|     ret = ff_attach_decode_data(frame);
  180|     if (ret < 0)
  181|         return ret;
  182| 
  183|     return 0;
  184| }
  185| 
  186| static int qsv_init_session(AVCodecContext *avctx, QSVContext *q, mfxSession session,
  187|                             AVBufferRef *hw_frames_ref, AVBufferRef *hw_device_ref)
  188| {
  189|     int ret;
  190|     mfxIMPL impl;
```

- `read_file(path=libavcodec/videotoolbox.c, start_line=145, end_line=165)` →

```
libavcodec/videotoolbox.c lines 145-165 of 1454
  145|     }
  146| 
  147|     return 0;
  148| }
  149| 
  150| int ff_videotoolbox_alloc_frame(AVCodecContext *avctx, AVFrame *frame)
  151| {
  152|     size_t      size = sizeof(VTHWFrame);
  153|     uint8_t    *data = NULL;
  154|     AVBufferRef *buf = NULL;
  155|     int ret = ff_attach_decode_data(frame);
  156|     FrameDecodeData *fdd;
  157|     if (ret < 0)
  158|         return ret;
  159| 
  160|     data = av_mallocz(size);
  161|     if (!data)
  162|         return AVERROR(ENOMEM);
  163|     buf = av_buffer_create(data, size, videotoolbox_buffer_release, NULL, 0);
  164|     if (!buf) {
  165|         av_freep(&data);
```

- `read_file(path=libavcodec/decode.c, start_line=1800, end_line=1820)` →

```
libavcodec/decode.c lines 1800-1820 of 2484
 1800|         ret = update_frame_props(avctx, frame);
 1801|         if (ret < 0)
 1802|             goto fail;
 1803|     }
 1804| 
 1805|     ret = avctx->get_buffer2(avctx, frame, flags);
 1806|     if (ret < 0)
 1807|         goto fail;
 1808| 
 1809|     validate_avframe_allocation(avctx, frame);
 1810| 
 1811|     ret = ff_attach_decode_data(frame);
 1812|     if (ret < 0)
 1813|         goto fail;
 1814| 
 1815|     ret = attach_post_process_data(avctx, frame);
 1816|     if (ret < 0)
 1817|         goto fail;
 1818| 
 1819| end:
 1820|     if (avctx->codec_type == AVMEDIA_TYPE_VIDEO && !override_dimensions &&
```

### Turn 3  _(tok 3045+124, stop=tool_use)_

**Reasoning:** Let me find the enclosing function names. For amfdec.c, I need to go up to find the function. Let me search for the function containing line 352.

- `grep(pattern=^static |^int |^void |^static int |^static void |^static AV, path_glob=libavcodec/amfdec.c, max_results=50)` →

```
16 matches
libavcodec/amfdec.c:45:static const AVCodecHWConfigInternal *const amf_hw_configs[] = {
libavcodec/amfdec.c:58:static void amf_free_amfsurface(void *opaque, uint8_t *data)
libavcodec/amfdec.c:64:static int amf_legacy_driver_no_bitness_detect(AVAMFDeviceContext    *amf_device_ctx)
libavcodec/amfdec.c:73:static int amf_init_decoder(AVCodecContext *avctx)
libavcodec/amfdec.c:197:static int amf_decode_close(AVCodecContext *avctx)
libavcodec/amfdec.c:213:static int amf_init_frames_context(AVCodecContext *avctx, int sw_format, int new_width, int new_height)
libavcodec/amfdec.c:243:static int amf_decode_init(AVCodecContext *avctx)
libavcodec/amfdec.c:314:static AMF_RESULT amf_get_property_buffer(AMFData *object, const wchar_t *name, AMFBuffer **val)
libavcodec/amfdec.c:335:static int amf_amfsurface_to_avframe(AVCodecContext *avctx, AMFSurface* surface, AVFrame *frame)
libavcodec/amfdec.c:421:static AMF_RESULT amf_receive_frame(AVCodecContext *avctx, AVFrame *frame)
libavcodec/amfdec.c:455:static AMF_RESULT amf_update_buffer_properties(AVCodecContext *avctx, AMFBuffer* buffer, const AVPacket* pkt)
libavcodec/amfdec.c:469:static AMF_RESULT amf_buffer_from_packet(AVCodecContext *avctx, const AVPacket* pkt, AMFBuffer** buffer)
libavcodec/amfdec.c:498:static int amf_decode_frame(AVCodecContext *avctx, struct AVFrame *frame)
libavcodec/amfdec.c:600:static void amf_decode_flush(AVCodecContext *avctx)
libavcodec/amfdec.c:609:static const AVOption options[] = {
libavcodec/amfdec.c:634:static const AVClass amf_decode_class = {
```

### Turn 4  _(tok 3728+138, stop=tool_use)_

**Reasoning:** Line 352 is between 335 (amf_amfsurface_to_avframe) and 421 (amf_receive_frame). So it's in `amf_amfsurface_to_avframe`.

For qsvdec.c, line 179 - let me find the enclosing function.

- `grep(pattern=^static |^int |^void , path_glob=libavcodec/qsvdec.c, max_results=80)` →

```
25 matches
libavcodec/qsvdec.c:62:static const AVRational mfx_tb = { 1, 90000 };
libavcodec/qsvdec.c:118:static const AVCodecHWConfigInternal *const qsv_hw_configs[] = {
libavcodec/qsvdec.c:131:static int qsv_get_continuous_buffer(AVCodecContext *avctx, AVFrame *frame,
libavcodec/qsvdec.c:186:static int qsv_init_session(AVCodecContext *avctx, QSVContext *q, mfxSession session,
libavcodec/qsvdec.c:297:static int qsv_decode_preinit(AVCodecContext *avctx, QSVContext *q, enum AVPixelFormat pix_fmt, mfxVideoParam *param)
libavcodec/qsvdec.c:396:static int qsv_decode_init_context(AVCodecContext *avctx, QSVContext *q, mfxVideoParam *param)
libavcodec/qsvdec.c:425:static int qsv_decode_header(AVCodecContext *avctx, QSVContext *q,
libavcodec/qsvdec.c:494:static int alloc_frame(AVCodecContext *avctx, QSVContext *q, QSVFrame *frame)
libavcodec/qsvdec.c:563:static void qsv_clear_unused_frames(QSVContext *q)
libavcodec/qsvdec.c:575:static int get_surface(AVCodecContext *avctx, QSVContext *q, mfxFrameSurface1 **surf)
libavcodec/qsvdec.c:616:static QSVFrame *find_frame(QSVContext *q, mfxFrameSurface1 *surf)
libavcodec/qsvdec.c:628:static int qsv_export_film_grain(AVCodecContext *avctx, mfxExtAV1FilmGrainParam *ext_param, AVFrame *frame)
libavcodec/qsvdec.c:695:static int qsv_export_hdr_side_data(AVCodecContext *avctx, mfxExtMasteringDisplayColourVolume *mdcv,
libavcodec/qsvdec.c:747:static int qsv_export_hdr_side_data_av1(AVCodecContext *avctx, mfxExtMasteringDisplayColourVolume *mdcv,
libavcodec/qsvdec.c:788:static int qsv_decode(AVCodecContext *avctx, QSVContext *q,
libavcodec/qsvdec.c:964:static void qsv_decode_close_qsvcontext(QSVContext *q)
libavcodec/qsvdec.c:992:static int qsv_process_data(AVCodecContext *avctx, QSVContext *q,
libavcodec/qsvdec.c:1085:static void qsv_clear_buffers(QSVDecContext *s)
libavcodec/qsvdec.c:1094:static av_cold int qsv_decode_close(AVCodecContext *avctx)
libavcodec/qsvdec.c:1107:static av_cold int qsv_decode_init(AVCodecContext *avctx)
libavcodec/qsvdec.c:1157:static int qsv_decode_frame(AVCodecContext *avctx, AVFrame *frame,
libavcodec/qsvdec.c:1207:static void qsv_decode_flush(AVCodecContext *avctx)
libavcodec/qsvdec.c:1221:static const AVClass x##_qsv_class = { \
libavcodec/qsvdec.c:1248:static const AVOption hevc_options[] = {
libavcodec/qsvdec.c:1268:static const AVOption options[] = {
```

### Turn 5  _(tok 4712+135, stop=tool_use)_

**Reasoning:** Line 179 is between 131 (qsv_get_continuous_buffer) and 186 (qsv_init_session). So it's in `qsv_get_continuous_buffer`.

For decode.c line 1811, let me find the enclosing function.

- `grep(pattern=^(static )?int |^(static )?void |^int ff_, path_glob=libavcodec/decode.c, max_results=100)` →

```
62 matches
libavcodec/decode.c:114:static int apply_param_change(AVCodecContext *avctx, const AVPacket *avpkt)
libavcodec/decode.c:175:static int extract_packet_props(AVCodecInternal *avci, const AVPacket *pkt)
libavcodec/decode.c:186:static int decode_bsfs_init(AVCodecContext *avctx)
libavcodec/decode.c:226:static int decode_get_packet(AVCodecContext *avctx, AVPacket *pkt)
libavcodec/decode.c:251:int ff_decode_get_packet(AVCodecContext *avctx, AVPacket *pkt)
libavcodec/decode.c:319:static int discard_samples(AVCodecContext *avctx, AVFrame *frame, int64_t *discarded_samples)
libavcodec/decode.c:514:static int detect_colorspace(AVCodecContext *avctx, AVFrame *frame)
libavcodec/decode.c:557:static int detect_colorspace(av_unused AVCodecContext *c, av_unused AVFrame *f)
libavcodec/decode.c:563:static int fill_frame_props(const AVCodecContext *avctx, AVFrame *frame)
libavcodec/decode.c:598:static int decode_simple_receive_frame(AVCodecContext *avctx, AVFrame *frame)
libavcodec/decode.c:614:int ff_decode_receive_frame_internal(AVCodecContext *avctx, AVFrame *frame)
libavcodec/decode.c:650:static int decode_receive_frame_internal(AVCodecContext *avctx, AVFrame *frame,
libavcodec/decode.c:719:int attribute_align_arg avcodec_send_packet(AVCodecContext *avctx, const AVPacket *avpkt)
libavcodec/decode.c:752:static int apply_cropping(AVCodecContext *avctx, AVFrame *frame)
libavcodec/decode.c:780:static int frame_validate(AVCodecContext *avctx, AVFrame *frame)
libavcodec/decode.c:806:int ff_decode_receive_frame(AVCodecContext *avctx, AVFrame *frame, unsigned flags)
libavcodec/decode.c:837:static void get_subtitle_defaults(AVSubtitle *sub)
libavcodec/decode.c:844:static int recode_subtitle(AVCodecContext *avctx, const AVPacket **outpkt,
libavcodec/decode.c:905:static int utf8_check(const uint8_t *str)
libavcodec/decode.c:924:int avcodec_decode_subtitle2(AVCodecContext *avctx, AVSubtitle *sub,
libavcodec/decode.c:1058:int ff_decode_get_hw_frames_ctx(AVCodecContext *avctx,
libavcodec/decode.c:1109:int avcodec_get_hw_frames_parameters(AVCodecContext *avctx,
libavcodec/decode.c:1171:static int hwaccel_init(AVCodecContext *avctx,
libavcodec/decode.c:1206:void ff_hwaccel_uninit(AVCodecContext *avctx)
libavcodec/decode.c:1218:int ff_get_format(AVCodecContext *avctx, const enum AVPixelFormat *fmt)
libavcodec/decode.c:1373:static int side_data_stereo3d_merge(AVFrameSideData *sd_frame,
libavcodec/decode.c:1409:static int side_data_exif_parse(AVFrame *dst, const AVPacketSideData *sd_pkt)
libavcodec/decode.c:1481:static int side_data_map(AVFrame *dst,
libavcodec/decode.c:1527:static int add_metadata_from_side_data(const AVPacket *avpkt, AVFrame *frame)
libavcodec/decode.c:1539:int ff_decode_frame_props_from_pkt(const AVCodecContext *avctx,
libavcodec/decode.c:1581:int ff_decode_frame_props(AVCodecContext *avctx, AVFrame *frame)
libavcodec/decode.c:1626:static void validate_avframe_allocation(AVCodecContext *avctx, AVFrame *frame)
libavcodec/decode.c:1647:static void decode_data_free(AVRefStructOpaque unused, void *obj)
libavcodec/decode.c:1658:int ff_attach_decode_data(AVFrame *frame)
libavcodec/decode.c:1674:static int update_frame_props(AVCodecContext *avctx, AVFrame *frame)
libavcodec/decode.c:1703:static int attach_post_process_data(AVCodecContext *avctx, AVFrame *frame)
libavcodec/decode.c:1755:int ff_get_buffer(AVCodecContext *avctx, AVFrame *frame, int flags)
libavcodec/decode.c:1835:static int reget_buffer_internal(AVCodecContext *avctx, AVFrame *frame, int flags)
libavcodec/decode.c:1877:int ff_reget_buffer(AVCodecContext *avctx, AVFrame *frame, int flags)
libavcodec/decode.c:1890:static void check_progress_consistency(const ProgressFrame *f)
libavcodec/decode.c:1896:int ff_progress_frame_alloc(AVCodecContext *avctx, ProgressFrame *f)
libavcodec/decode.c:1910:int ff_progress_frame_get_buffer(AVCodecContext *avctx, ProgressFrame *f, int flags)
libavcodec/decode.c:1925:void ff_progress_frame_ref(ProgressFrame *dst, const ProgressFrame *src)
libavcodec/decode.c:1933:void ff_progress_frame_unref(ProgressFrame *f)
libavcodec/decode.c:1940:void ff_progress_frame_replace(ProgressFrame *dst, const ProgressFrame *src)
libavcodec/decode.c:1950:void ff_progress_frame_report(ProgressFrame *f, int n)
libavcodec/decode.c:1955:void ff_progress_frame_await(const ProgressFrame *f, int n)
libavcodec/decode.c:1984:static void progress_frame_pool_reset_cb(AVRefStructOpaque unused, void *obj)
libavcodec/decode.c:2139:static int side_data_pref(const AVCodecContext *avctx, AVFrameSideData ***sd,
libavcodec/decode.c:2155:int ff_frame_new_side_data(const AVCodecContext *avctx, AVFrame *frame,
libavcodec/decode.c:2174:int ff_frame_new_side_data_from_buf_ext(const AVCodecContext *avctx,
libavcodec/decode.c:2193:int ff_frame_new_side_data_from_buf(const AVCodecContext *avctx,
libavcodec/decode.c:2202:int ff_decode_mastering_display_new_ext(const AVCodecContext *avctx,
libavcodec/decode.c:2234:int ff_decode_mastering_display_new(const AVCodecContext *avctx, AVFrame *frame,
libavcodec/decode.c:2247:int ff_decode_content_light_new_ext(const AVCodecContext *avctx,
libavcodec/decode.c:2279:int ff_decode_content_light_new(const AVCodecContext *avctx, AVFrame *frame,
libavcodec/decode.c:2292:int ff_copy_palette(void *dst, const AVPacket *src, void *logctx)
libavcodec/decode.c:2307:int ff_hwaccel_frame_priv_alloc(AVCodecContext *avctx, void **hwaccel_picture_private)
libavcodec/decode.c:2384:static int attach_displaymatrix(AVCodecContext *avctx, AVFrame *frame, int orientation)
libavcodec/decode.c:2405:static int exif_attach_ifd(AVCodecContext *avctx, AVFrame *frame, const AVExifMetadata *ifd, AVBufferRef **pbuf)
libavcodec/decode.c:2460:int ff_decode_exif_attach_ifd(AVCodecContext *avctx, AVFrame *frame, const AVExifMetadata *ifd)
libavcodec/decode.c:2466:int ff_decode_exif_attach_buffer(AVCodecContext *avctx, AVFrame *frame, AVBufferRef **pbuf,
```

### Turn 6  _(tok 6795+279, stop=tool_use)_

**Reasoning:** Line 1811 falls between `ff_get_buffer` (line 1755) and `reget_buffer_internal` (line 1835). So it's in `ff_get_buffer`.

But wait - the definition of `ff_attach_decode_data` is at line 1658. The reference at line 1811 is a call from within `ff_get_buffer`.

So the callers are:

1. `amf_amfsurface_to_avframe` in libavcodec/amfdec.c
2. `qsv_get_continuous_buffer` in libavcodec/qsvdec.c
3. `ff_videotoolbox_alloc_frame` in libavcodec/videotoolbox.c
4. `ff_get_buffer` in libavcodec/decode.c

Let me verify the function boundaries to be absolutely sure.

For amfdec.c, line 335 starts `amf_amfsurface_to_avframe`. Let me check where it ends.

- `read_file(path=libavcodec/amfdec.c, start_line=330, end_line=340)` →

```
libavcodec/amfdec.c lines 330-340 of 664
  330|         AMFVariantClear(&var);
  331|     }
  332|     return res;
  333| }
  334| 
  335| static int amf_amfsurface_to_avframe(AVCodecContext *avctx, AMFSurface* surface, AVFrame *frame)
  336| {
  337|     AMFVariantStruct    var = {0};
  338|     AMFPlane            *plane;
  339|     int                 i;
  340|     int                 ret;
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 7  _(tok 7281+319, stop=tool_use, forced)_

**Reasoning:** Based on my analysis, the four callers (excluding the definition itself) are:

1. `amf_amfsurface_to_avframe` in `libavcodec/amfdec.c`
2. `qsv_get_continuous_buffer` in `libavcodec/qsvdec.c`
3. `ff_videotoolbox_alloc_frame` in `libavcodec/videotoolbox.c`
4. `ff_get_buffer` in `libavcodec/decode.c`

The definition is at decode.c:1658 (`ff_attach_decode_data`), the prototype/declaration is at decode.h:89, and the four actual call sites are above. I'm confident about these.

- **submit_callers** → `{"callers": [{"function": "amf_amfsurface_to_avframe", "file": "libavcodec/amfdec.c"}, {"function": "qsv_get_continuous_buffer", "file": "libavcodec/qsvdec.c"}, {"function": "ff_videotoolbox_alloc_frame", "file": "libavcodec/videotoolbox.c"}, {"function": "ff_get_buffer", "file": "libavcodec/decode.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 4, "n_truth": 4, "tp": 4, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

