# Impact-analysis transcript — ffmpeg @ 823c6fc0b8f1 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_attach_decode_data` (libavcodec/decode.c), arity 1->2
- truth: [['libavcodec/amfdec.c', 'amf_amfsurface_to_avframe'], ['libavcodec/decode.c', 'ff_get_buffer'], ['libavcodec/qsvdec.c', 'qsv_get_continuous_buffer'], ['libavcodec/videotoolbox.c', 'ff_videotoolbox_alloc_frame']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1072+149, stop=tool_use)_

**Reasoning:** Let me start by finding references to the symbol.

Wait, the tools available: list_files, read_file, grep, find_references, submit_callers. There's no repo_search. Let me use grep and find_references.

Also note the "version" parameter for list_files/read_file/grep — enum ["old"]. Let me use that.

Let's do it.


- `find_references(name=ff_attach_decode_data)` →

```
5 references
ff_attach_decode_data  352 libavcodec/amfdec.c         ret = ff_attach_decode_data(frame);
ff_attach_decode_data 1811 libavcodec/decode.c     ret = ff_attach_decode_data(frame);
ff_attach_decode_data   89 libavcodec/decode.h int ff_attach_decode_data(AVFrame *frame);
ff_attach_decode_data  179 libavcodec/qsvdec.c     ret = ff_attach_decode_data(frame);
ff_attach_decode_data  155 libavcodec/videotoolbox.c     int ret = ff_attach_decode_data(frame);
```

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

### Turn 2  _(tok 1524+305, stop=tool_use)_

**Reasoning:** Both agree: 4 call sites. Now find the enclosing function names.


- `read_file(path=libavcodec/amfdec.c, version=old, start_line=300, end_line=370)` →

```
libavcodec/amfdec.c lines 300-370 of 664
  300|                 avctx->coded_height = 720;
  301|             ret = amf_init_frames_context(avctx, surf_pix_fmt, avctx->coded_width, avctx->coded_height);
  302|             AMF_GOTO_FAIL_IF_FALSE(avctx, ret == 0, ret, "Failed to init frames context (AMF) : %s\n", av_err2str(ret));
  303|         }
  304|         else
  305|             avctx->pix_fmt = surf_pix_fmt;
  306| 
  307|         return 0;
  308|     }
  309| fail:
  310|     amf_decode_close(avctx);
  311|     return ret;
  312| }
  313| 
  314| static AMF_RESULT amf_get_property_buffer(AMFData *object, const wchar_t *name, AMFBuffer **val)
  315| {
  316|     AMF_RESULT res;
  317|     AMFVariantStruct var;
  318|     res = AMFVariantInit(&var);
  319|     if (res == AMF_OK) {
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
  361|                                     AV_BUFFER_FLAG_READONLY);
  362|         AMF_RETURN_IF_FALSE(avctx, !!frame->buf[0], AVERROR(ENOMEM), "av_buffer_create for amf surface failed.");
  363| 
  364|         frame->data[0] = (uint8_t *)surface;
  365|         frame->format =  AV_PIX_FMT_AMF_SURFACE;
  366|         format_amf = surface->pVtbl->GetFormat(surface);
  367|         avctx->sw_pix_fmt = av_amf_to_av_format(format_amf);
  368|         frame->hw_frames_ctx = av_buffer_ref(avctx->hw_frames_ctx);
  369|     } else {
  370|         ret = surface->pVtbl->Convert(surface, AMF_MEMORY_HOST);
```

- `read_file(path=libavcodec/decode.c, version=old, start_line=1750, end_line=1830)` →

```
libavcodec/decode.c lines 1750-1830 of 2484
 1750| #endif
 1751| 
 1752|     return 0;
 1753| }
 1754| 
 1755| int ff_get_buffer(AVCodecContext *avctx, AVFrame *frame, int flags)
 1756| {
 1757|     const FFHWAccel *hwaccel = ffhwaccel(avctx->hwaccel);
 1758|     int override_dimensions = 1;
 1759|     int ret;
 1760| 
 1761|     av_assert0(ff_codec_is_decoder(avctx->codec));
 1762| 
 1763|     if (avctx->codec_type == AVMEDIA_TYPE_VIDEO) {
 1764|         if ((unsigned)avctx->width > INT_MAX - STRIDE_ALIGN ||
 1765|             (ret = av_image_check_size2(FFALIGN(avctx->width, STRIDE_ALIGN), avctx->height, avctx->max_pixels, AV_PIX_FMT_NONE, 0, avctx)) < 0 || avctx->pix_fmt<0) {
 1766|             av_log(avctx, AV_LOG_ERROR, "video_get_buffer: image parameters invalid\n");
 1767|             ret = AVERROR(EINVAL);
 1768|             goto fail;
 1769|         }
 1770| 
 1771|         if (frame->width <= 0 || frame->height <= 0) {
 1772|             frame->width  = FFMAX(avctx->width,  AV_CEIL_RSHIFT(avctx->coded_width,  avctx->lowres));
 1773|             frame->height = FFMAX(avctx->height, AV_CEIL_RSHIFT(avctx->coded_height, avctx->lowres));
 1774|             override_dimensions = 0;
 1775|         }
 1776| 
 1777|         if (frame->data[0] || frame->data[1] || frame->data[2] || frame->data[3]) {
 1778|             av_log(avctx, AV_LOG_ERROR, "pic->data[*]!=NULL in get_buffer_internal\n");
 1779|             ret = AVERROR(EINVAL);
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

- `read_file(path=libavcodec/qsvdec.c, version=old, start_line=120, end_line=195)` →

```
libavcodec/qsvdec.c lines 120-195 of 1309
  120|         .public = {
  121|             .pix_fmt     = AV_PIX_FMT_QSV,
  122|             .methods     = AV_CODEC_HW_CONFIG_METHOD_HW_FRAMES_CTX |
  123|                            AV_CODEC_HW_CONFIG_METHOD_HW_DEVICE_CTX,
  124|             .device_type = AV_HWDEVICE_TYPE_QSV,
  125|         },
  126|         .hwaccel = NULL,
  127|     },
  128|     NULL
  129| };
  130| 
  131| static int qsv_get_continuous_buffer(AVCodecContext *avctx, AVFrame *frame,
  132|                                      AVBufferPool *pool)
  133| {
  134|     int ret = 0;
  135| 
  136|     ret = ff_decode_frame_props(avctx, frame);
  137|     if (ret < 0)
  138|         return ret;
  139| 
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
  191| 
  192|     if (q->gpu_copy == MFX_GPUCOPY_ON &&
  193|         !(q->iopattern & MFX_IOPATTERN_OUT_SYSTEM_MEMORY)) {
  194|         av_log(avctx, AV_LOG_WARNING, "GPU-accelerated memory copy "
  195|                         "only works in system memory mode.\n");
```

- `read_file(path=libavcodec/videotoolbox.c, version=old, start_line=100, end_line=175)` →

```
libavcodec/videotoolbox.c lines 100-175 of 1454
  100|                                  const uint8_t *buffer,
  101|                                  uint32_t size)
  102| {
  103|     void *tmp;
  104| 
  105|     tmp = av_fast_realloc(vtctx->bitstream,
  106|                           &vtctx->allocated_size,
  107|                           vtctx->bitstream_size + size);
  108| 
  109|     if (!tmp)
  110|         return AVERROR(ENOMEM);
  111| 
  112|     vtctx->bitstream = tmp;
  113|     memcpy(vtctx->bitstream + vtctx->bitstream_size, buffer, size);
  114|     vtctx->bitstream_size += size;
  115| 
  116|     return 0;
  117| }
  118| 
  119| static int videotoolbox_postproc_frame(void *avctx, AVFrame *frame)
  120| {
  121|     int ret;
  122|     VTHWFrame *ref = (VTHWFrame *)frame->buf[0]->data;
  123| 
  124|     if (!ref->pixbuf) {
  125|         av_log(avctx, AV_LOG_ERROR, "No frame decoded?\n");
  126|         av_frame_unref(frame);
  127|         return AVERROR_EXTERNAL;
  128|     }
  129| 
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
  171|     fdd->hwaccel_priv_post_process = videotoolbox_postproc_frame;
  172| 
  173|     frame->width  = avctx->width;
  174|     frame->height = avctx->height;
  175|     frame->format = avctx->pix_fmt;
```

### Turn 3  _(tok 6768+400, stop=tool_use)_

**Reasoning:** Now I have all four enclosing functions:

1. `amf_amfsurface_to_avframe` in libavcodec/amfdec.c
2. `ff_get_buffer` in libavcodec/decode.c
3. `qsv_get_continuous_buffer` in libavcodec/qsvdec.c
4. `ff_videotoolbox_alloc_frame` in libavcodec/videotoolbox.c

Let me also double-check there aren't calls via function pointer assignment, or indirect references like `&ff_attach_decode_data`. The grep found 6 matches total, and I've accounted for all: definition, prototype, and 4 call sites. Also check whether there might be call sites in a differently-named pattern such as within a macro. Grep covered everything.

Also, let me check if maybe there are files elsewhere (e.g., tests) that use it — grep covered the entire repo.

Let me verify there's not a second definition or a wrapper with a different name in decode.c that also calls it — no, only line 1811.

Also confirm that amfdec.c line 352 is inside `amf_amfsurface_to_avframe` — yes, defined at line 335, and the call at 352.

Let me double-check whether decode.c's line 1658 definition belongs to ff_attach_decode_data and there's no other caller in decode.c inside another function. Confirmed.

Submit.


**Says:** 

I found all references. Let me verify the full context once more:



- `read_file(end_line=1680, path=libavcodec/decode.c, start_line=1650, version=old)` →

```
libavcodec/decode.c lines 1650-1680 of 2484
 1650| 
 1651|     if (fdd->post_process_opaque_free)
 1652|         fdd->post_process_opaque_free(fdd->post_process_opaque);
 1653| 
 1654|     if (fdd->hwaccel_priv_free)
 1655|         fdd->hwaccel_priv_free(fdd->hwaccel_priv);
 1656| }
 1657| 
 1658| int ff_attach_decode_data(AVFrame *frame)
 1659| {
 1660|     FrameDecodeData *fdd;
 1661| 
 1662|     av_assert1(!frame->private_ref);
 1663|     av_refstruct_unref(&frame->private_ref);
 1664| 
 1665|     fdd = av_refstruct_alloc_ext(sizeof(*fdd), 0, NULL, decode_data_free);
 1666|     if (!fdd)
 1667|         return AVERROR(ENOMEM);
 1668| 
 1669|     frame->private_ref = fdd;
 1670| 
 1671|     return 0;
 1672| }
 1673| 
 1674| static int update_frame_props(AVCodecContext *avctx, AVFrame *frame)
 1675| {
 1676| #if CONFIG_LIBLCEVC_DEC
 1677|     AVCodecInternal    *avci = avctx->internal;
 1678|     DecodeContext        *dc = decode_ctx(avci);
 1679| 
 1680|     dc->lcevc.frame = dc->lcevc.ctx && avctx->codec_type == AVMEDIA_TYPE_VIDEO &&
```

### Turn 4  _(tok 7651+511, stop=tool_use)_

**Reasoning:** All confirmed. There are exactly 4 call sites:

1. `amf_amfsurface_to_avframe` — libavcodec/amfdec.c:352
2. `ff_get_buffer` — libavcodec/decode.c:1811
3. `qsv_get_continuous_buffer` — libavcodec/qsvdec.c:179
4. `ff_videotoolbox_alloc_frame` — libavcodec/videotoolbox.c:155

Submit.


**Says:** 

Analysis complete. Both the GNU Global index and a repo-wide grep agree there are exactly 6 textual occurrences: the definition (`decode.c:1658`), the prototype (`decode.h:89`), and **4 real call sites**, whose enclosing functions I confirmed by reading the surrounding code:

| Call site | Enclosing function | File |
|---|---|---|
| line 352 | `amf_amfsurface_to_avframe` (static, starts at line 335) | `libavcodec/amfdec.c` |
| line 1811 | `ff_get_buffer` (starts at line 1755) | `libavcodec/decode.c` |
| line 179 | `qsv_get_continuous_buffer` (static, starts at line 131) | `libavcodec/qsvdec.c` |
| line 155 | `ff_videotoolbox_alloc_frame` (starts at line 150) | `libavcodec/videotoolbox.c` |

No indirect references (e.g. function-pointer assignment to `ff_attach_decode_data`) exist, and no call sites in tests or other directories.



- **submit_callers** → `{"callers": [{"function": "amf_amfsurface_to_avframe", "file": "libavcodec/amfdec.c"}, {"function": "ff_get_buffer", "file": "libavcodec/decode.c"}, {"function": "qsv_get_continuous_buffer", "file": "libavcodec/qsvdec.c"}, {"function": "ff_videotoolbox_alloc_frame", "file": "libavcodec/videotoolbox.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 4, "n_truth": 4, "tp": 4, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

