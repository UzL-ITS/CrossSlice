# Impact-analysis transcript — ffmpeg @ 823c6fc0b8f1 — anthropic:claude-haiku-5-5

- target: `ff_attach_decode_data` (libavcodec/decode.c), arity 1->2
- truth: [['libavcodec/amfdec.c', 'amf_amfsurface_to_avframe'], ['libavcodec/decode.c', 'ff_get_buffer'], ['libavcodec/qsvdec.c', 'qsv_get_continuous_buffer'], ['libavcodec/videotoolbox.c', 'ff_videotoolbox_alloc_frame']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1389+83, stop=tool_use)_

**Reasoning:** I'm going to search the codebase for every place ff_attach_decode_data is referenced, using find_references.



- `find_references(name=ff_attach_decode_data)` →

```
5 references
ff_attach_decode_data  352 libavcodec/amfdec.c         ret = ff_attach_decode_data(frame);
ff_attach_decode_data 1811 libavcodec/decode.c     ret = ff_attach_decode_data(frame);
ff_attach_decode_data   89 libavcodec/decode.h int ff_attach_decode_data(AVFrame *frame);
ff_attach_decode_data  179 libavcodec/qsvdec.c     ret = ff_attach_decode_data(frame);
ff_attach_decode_data  155 libavcodec/videotoolbox.c     int ret = ff_attach_decode_data(frame);
```

### Turn 2  _(tok 1704+617, stop=tool_use)_

**Reasoning:** I need to find the enclosing functions, so I'll read each file around the referenced lines. I also want to grep for any other references, since GNU Global might miss some.



- `grep(pattern=ff_attach_decode_data, version=old)` →

```
6 matches
libavcodec/amfdec.c:352:        ret = ff_attach_decode_data(frame);
libavcodec/decode.c:1658:int ff_attach_decode_data(AVFrame *frame)
libavcodec/decode.c:1811:    ret = ff_attach_decode_data(frame);
libavcodec/decode.h:89:int ff_attach_decode_data(AVFrame *frame);
libavcodec/qsvdec.c:179:    ret = ff_attach_decode_data(frame);
libavcodec/videotoolbox.c:155:    int ret = ff_attach_decode_data(frame);
```

- `read_file(path=libavcodec/amfdec.c, version=old, start_line=320, end_line=360)` →

```
libavcodec/amfdec.c lines 320-360 of 664
  320|         res = object->pVtbl->GetProperty(object, name, &var);
  321|         if (res == AMF_OK) {
  322|             if (var.type == AMF_VARIANT_INTERFACE) {
  323|                 AMFGuid guid_AMFBuffer = IID_AMFBuffer();
  324|                 AMFInterface *amf_interface = AMFVariantInterface(&var);
  325|                 res = amf_interface->pVtbl->QueryInterface(amf_interface, &guid_AMFBuffer, (void**)val);
  326|             } else {
  327|                 res = AMF_INVALID_DATA_TYPE;
  328|             }
  329|         }
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

- `read_file(path=libavcodec/decode.c, version=old, start_line=1780, end_line=1830)` →

```
libavcodec/decode.c lines 1780-1830 of 2484
 1780|             goto fail;
 1781|         }
 1782|     } else if (avctx->codec_type == AVMEDIA_TYPE_AUDIO) {
 1783|         if (frame->nb_samples * (int64_t)avctx->ch_layout.nb_channels > avctx->max_samples) {
 1784|             av_log(avctx, AV_LOG_ERROR, "samples per frame %d, exceeds max_samples %"PRId64"\n", frame->nb_samples, avctx->max_samples);
 1785|             ret = AVERROR(EINVAL);
 1786|             goto fail;
 1787|         }
 1788|     }
 1789|     ret = ff_decode_frame_props(avctx, frame);
 1790|     if (ret < 0)
 1791|         goto fail;
 1792| 
 1793|     if (hwaccel) {
 1794|         if (hwaccel->alloc_frame) {
 1795|             ret = hwaccel->alloc_frame(avctx, frame);
 1796|             goto end;
 1797|         }
 1798|     } else {
 1799|         avctx->sw_pix_fmt = avctx->pix_fmt;
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
 1821|         !(ffcodec(avctx->codec)->caps_internal & FF_CODEC_CAP_EXPORTS_CROPPING)) {
 1822|         frame->width  = avctx->width;
 1823|         frame->height = avctx->height;
 1824|     }
 1825| 
 1826| fail:
 1827|     if (ret < 0) {
 1828|         av_log(avctx, AV_LOG_ERROR, "get_buffer() failed\n");
 1829|         av_frame_unref(frame);
 1830|     }
```

- `read_file(path=libavcodec/qsvdec.c, version=old, start_line=140, end_line=190)` →

```
libavcodec/qsvdec.c lines 140-190 of 1309
  140|     frame->width       = avctx->coded_width;
  141|     frame->height      = avctx->coded_height;
  142| 
  143|     switch (avctx->pix_fmt) {
  144|     case AV_PIX_FMT_NV12:
  145|         frame->linesize[0] = FFALIGN(avctx->coded_width, 128);
  146|         break;
  147|     case AV_PIX_FMT_P010:
  148|     case AV_PIX_FMT_P012:
  149|     case AV_PIX_FMT_YUYV422:
  150|         frame->linesize[0] = 2 * FFALIGN(avctx->coded_width, 128);
  151|         break;
  152|     case AV_PIX_FMT_Y210:
  153|     case AV_PIX_FMT_VUYX:
  154|     case AV_PIX_FMT_XV30:
  155|     case AV_PIX_FMT_Y212:
  156|         frame->linesize[0] = 4 * FFALIGN(avctx->coded_width, 128);
  157|         break;
  158|     case AV_PIX_FMT_XV36:
  159|         frame->linesize[0] = 8 * FFALIGN(avctx->coded_width, 128);
  160|         break;
  161|     default:
  162|         av_log(avctx, AV_LOG_ERROR, "Unsupported pixel format.\n");
  163|         return AVERROR(EINVAL);
  164|     }
  165| 
  166|     frame->buf[0]      = av_buffer_pool_get(pool);
  167|     if (!frame->buf[0])
  168|         return AVERROR(ENOMEM);
  169| 
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

- `read_file(path=libavcodec/videotoolbox.c, version=old, start_line=130, end_line=170)` →

```
libavcodec/videotoolbox.c lines 130-170 of 1454
  130|     frame->crop_right = 0;
  131|     frame->crop_left = 0;
  132|     frame->crop_top = 0;
  133|     frame->crop_bottom = 0;
  134| 
  135|     if ((ret = av_vt_pixbuf_set_attachments(avctx, ref->pixbuf, frame)) < 0)
  136|         return ret;
  137| 
  138|     frame->data[3] = (uint8_t*)ref->pixbuf;
  139| 
  140|     if (ref->hw_frames_ctx) {
  141|         av_buffer_unref(&frame->hw_frames_ctx);
  142|         frame->hw_frames_ctx = av_buffer_ref(ref->hw_frames_ctx);
  143|         if (!frame->hw_frames_ctx)
  144|             return AVERROR(ENOMEM);
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
  166|         return AVERROR(ENOMEM);
  167|     }
  168|     frame->buf[0] = buf;
  169| 
  170|     fdd = frame->private_ref;
```

### Turn 3  _(tok 6091+575, stop=tool_use)_

**Reasoning:** I need the names of the functions that enclose these lines. In amfdec.c, the code around line 335 sits inside amf_amfsurface_to_avframe, which runs past line 360. For decode.c line 1811, I suspect it's ff_get_buffer or get_buffer_internal, so I'll check the function start somewhere in the 1700–1780 range. In qsvdec.c I need to find the start of whatever function contains line 179, likely something like qsv_get_buffer. I'll grep for the function definitions to confirm.



- `grep(pattern=^(static |int |av_cold )?[a-zA-Z_].*\(.*\)?$, version=old, path_glob=libavcodec/decode.c, max_results=200)` →

```
76 matches
libavcodec/decode.c:109:static DecodeContext *decode_ctx(AVCodecInternal *avci)
libavcodec/decode.c:114:static int apply_param_change(AVCodecContext *avctx, const AVPacket *avpkt)
libavcodec/decode.c:175:static int extract_packet_props(AVCodecInternal *avci, const AVPacket *pkt)
libavcodec/decode.c:186:static int decode_bsfs_init(AVCodecContext *avctx)
libavcodec/decode.c:226:static int decode_get_packet(AVCodecContext *avctx, AVPacket *pkt)
libavcodec/decode.c:251:int ff_decode_get_packet(AVCodecContext *avctx, AVPacket *pkt)
libavcodec/decode.c:293:static int64_t guess_correct_pts(DecodeContext *dc,
libavcodec/decode.c:319:static int discard_samples(AVCodecContext *avctx, AVFrame *frame, int64_t *discarded_samples)
libavcodec/decode.c:417:static inline int decode_simple_internal(AVCodecContext *avctx, AVFrame *frame, int64_t *discarded_samples)
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
libavcodec/decode.c:995:enum AVPixelFormat avcodec_default_get_format(struct AVCodecContext *avctx,
libavcodec/decode.c:1058:int ff_decode_get_hw_frames_ctx(AVCodecContext *avctx,
libavcodec/decode.c:1109:int avcodec_get_hw_frames_parameters(AVCodecContext *avctx,
libavcodec/decode.c:1171:static int hwaccel_init(AVCodecContext *avctx,
libavcodec/decode.c:1206:void ff_hwaccel_uninit(AVCodecContext *avctx)
libavcodec/decode.c:1218:int ff_get_format(AVCodecContext *avctx, const enum AVPixelFormat *fmt)
libavcodec/decode.c:1357:packet_side_data_get(const AVPacketSideData *sd, int nb_sd,
libavcodec/decode.c:1367:const AVPacketSideData *ff_get_coded_side_data(const AVCodecContext *avctx,
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
libavcodec/decode.c:1961:enum ThreadingStatus ff_thread_sync_ref(AVCodecContext *avctx, size_t offset)
libavcodec/decode.c:1967:static av_cold int progress_frame_pool_init_cb(AVRefStructOpaque opaque, void *obj)
libavcodec/decode.c:1984:static void progress_frame_pool_reset_cb(AVRefStructOpaque unused, void *obj)
libavcodec/decode.c:1992:static av_cold void progress_frame_pool_free_entry_cb(AVRefStructOpaque opaque, void *obj)
libavcodec/decode.c:2000:av_cold int ff_decode_preinit(AVCodecContext *avctx)
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
libavcodec/decode.c:2336:av_cold void ff_decode_flush_buffers(AVCodecContext *avctx)
libavcodec/decode.c:2354:av_cold AVCodecInternal *ff_decode_internal_alloc(void)
libavcodec/decode.c:2359:av_cold void ff_decode_internal_sync(AVCodecContext *dst, const AVCodecContext *src)
libavcodec/decode.c:2374:av_cold void ff_decode_internal_uninit(AVCodecContext *avctx)
libavcodec/decode.c:2384:static int attach_displaymatrix(AVCodecContext *avctx, AVFrame *frame, int orientation)
libavcodec/decode.c:2405:static int exif_attach_ifd(AVCodecContext *avctx, AVFrame *frame, const AVExifMetadata *ifd, AVBufferRef **pbuf)
libavcodec/decode.c:2460:int ff_decode_exif_attach_ifd(AVCodecContext *avctx, AVFrame *frame, const AVExifMetadata *ifd)
libavcodec/decode.c:2466:int ff_decode_exif_attach_buffer(AVCodecContext *avctx, AVFrame *frame, AVBufferRef **pbuf,
```

- `grep(pattern=^[a-zA-Z_].*\(, version=old, path_glob=libavcodec/qsvdec.c, max_results=200)` →

```
29 matches
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
libavcodec/qsvdec.c:1265:DEFINE_QSV_DECODER_WITH_OPTION(hevc, HEVC, "hevc_mp4toannexb", hevc_options)
libavcodec/qsvdec.c:1279:DEFINE_QSV_DECODER(h264, H264, "h264_mp4toannexb")
libavcodec/qsvdec.c:1283:DEFINE_QSV_DECODER(mpeg2, MPEG2VIDEO, NULL)
libavcodec/qsvdec.c:1287:DEFINE_QSV_DECODER(vc1, VC1, NULL)
libavcodec/qsvdec.c:1291:DEFINE_QSV_DECODER(mjpeg, MJPEG, NULL)
libavcodec/qsvdec.c:1295:DEFINE_QSV_DECODER(vp8, VP8, NULL)
libavcodec/qsvdec.c:1299:DEFINE_QSV_DECODER(vp9, VP9, NULL)
libavcodec/qsvdec.c:1303:DEFINE_QSV_DECODER(av1, AV1, NULL)
libavcodec/qsvdec.c:1307:DEFINE_QSV_DECODER(vvc, VVC, "vvc_mp4toannexb")
```

- `grep(pattern=^[a-zA-Z_].*\(, version=old, path_glob=libavcodec/amfdec.c, max_results=200)` →

```
17 matches
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
libavcodec/amfdec.c:660:DEFINE_AMF_DECODER(h264, H264, "h264_mp4toannexb")
libavcodec/amfdec.c:661:DEFINE_AMF_DECODER(hevc, HEVC, NULL)
libavcodec/amfdec.c:662:DEFINE_AMF_DECODER(vp9, VP9, NULL)
libavcodec/amfdec.c:663:DEFINE_AMF_DECODER(av1, AV1, NULL)
```

### Turn 4  _(tok 12804+442, stop=tool_use)_

**Reasoning:** I'm checking the enclosing functions for each match: amf_amfsurface_to_avframe in amfdec.c, ff_get_buffer in decode.c, qsv_get_continuous_buffer in qsvdec.c, and ff_videotoolbox_alloc_frame in videotoolbox.c.

I'm confirming the grep turned up the definition and prototype, and that find_references agrees with five matches, so the count is consistent. Since the search ran across the whole repo with git grep, I'm treating non-C files as covered and moving on to submit.



- **submit_callers** → `{"callers": [{"function": "amf_amfsurface_to_avframe", "file": "libavcodec/amfdec.c"}, {"function": "ff_get_buffer", "file": "libavcodec/decode.c"}, {"function": "qsv_get_continuous_buffer", "file": "libavcodec/qsvdec.c"}, {"function": "ff_videotoolbox_alloc_frame", "file": "libavcodec/videotoolbox.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 4, "n_truth": 4, "tp": 4, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

