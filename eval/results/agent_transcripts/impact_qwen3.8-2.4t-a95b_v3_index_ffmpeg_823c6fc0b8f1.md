# Impact-analysis transcript — ffmpeg @ 823c6fc0b8f1 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_attach_decode_data` (libavcodec/decode.c), arity 1->2
- truth: [['libavcodec/amfdec.c', 'amf_amfsurface_to_avframe'], ['libavcodec/decode.c', 'ff_get_buffer'], ['libavcodec/qsvdec.c', 'qsv_get_continuous_buffer'], ['libavcodec/videotoolbox.c', 'ff_videotoolbox_alloc_frame']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1072+108, stop=tool_use)_

**Reasoning:** Let me find references to ff_attach_decode_data.

Note: the tools mention version "old" for repository tools. find_references doesn't take version. Let's use it.


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

### Turn 2  _(tok 1483+304, stop=tool_use)_

**Reasoning:** Now I need enclosing functions. Let's read around each call site.


- `read_file(path=libavcodec/amfdec.c, start_line=300, end_line=370, version=old)` →

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

- `read_file(path=libavcodec/decode.c, start_line=1760, end_line=1840, version=old)` →

```
libavcodec/decode.c lines 1760-1840 of 2484
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
 1831| 
 1832|     return ret;
 1833| }
 1834| 
 1835| static int reget_buffer_internal(AVCodecContext *avctx, AVFrame *frame, int flags)
 1836| {
 1837|     AVFrame *tmp;
 1838|     int ret;
 1839| 
 1840|     av_assert0(avctx->codec_type == AVMEDIA_TYPE_VIDEO);
```

- `read_file(path=libavcodec/qsvdec.c, start_line=120, end_line=200, version=old)` →

```
libavcodec/qsvdec.c lines 120-200 of 1309
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
  196|         q->gpu_copy = MFX_GPUCOPY_OFF;
  197|     }
  198|     if (session) {
  199|         q->session = session;
  200|     } else if (hw_frames_ref) {
```

- `read_file(path=libavcodec/videotoolbox.c, start_line=100, end_line=180, version=old)` →

```
libavcodec/videotoolbox.c lines 100-180 of 1454
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
  176| 
  177|     return 0;
  178| }
  179| 
  180| #define AV_W8(p, v) *(p) = (v)
```

### Turn 3  _(tok 6850+108, stop=tool_use)_

**Reasoning:** Now for decode.c line 1811, need enclosing function name. Let me look above around line 1730-1760.


- `read_file(path=libavcodec/decode.c, start_line=1700, end_line=1765, version=old)` →

```
libavcodec/decode.c lines 1700-1765 of 2484
 1700|     return 0;
 1701| }
 1702| 
 1703| static int attach_post_process_data(AVCodecContext *avctx, AVFrame *frame)
 1704| {
 1705| #if CONFIG_LIBLCEVC_DEC
 1706|     AVCodecInternal    *avci = avctx->internal;
 1707|     DecodeContext        *dc = decode_ctx(avci);
 1708| 
 1709|     if (dc->lcevc.frame) {
 1710|         FrameDecodeData *fdd = frame->private_ref;
 1711|         FFLCEVCFrame *frame_ctx;
 1712|         int ret;
 1713| 
 1714|         if (fdd->post_process || !dc->lcevc.width || !dc->lcevc.height) {
 1715|             dc->lcevc.frame = 0;
 1716|             return 0;
 1717|         }
 1718| 
 1719|         frame_ctx = av_mallocz(sizeof(*frame_ctx));
 1720|         if (!frame_ctx)
 1721|             return AVERROR(ENOMEM);
 1722| 
 1723|         frame_ctx->frame = av_frame_alloc();
 1724|         if (!frame_ctx->frame) {
 1725|             av_free(frame_ctx);
 1726|             return AVERROR(ENOMEM);
 1727|         }
 1728| 
 1729|         frame_ctx->lcevc = av_refstruct_ref(dc->lcevc.ctx);
 1730|         frame_ctx->frame->width  = dc->lcevc.width;
 1731|         frame_ctx->frame->height = dc->lcevc.height;
 1732|         frame_ctx->frame->format = frame->format;
 1733| 
 1734|         frame->width  = dc->lcevc.base_width;
 1735|         frame->height = dc->lcevc.base_height;
 1736| 
 1737|         ret = avctx->get_buffer2(avctx, frame_ctx->frame, 0);
 1738|         if (ret < 0) {
 1739|             ff_lcevc_unref(frame_ctx);
 1740|             return ret;
 1741|         }
 1742| 
 1743|         validate_avframe_allocation(avctx, frame_ctx->frame);
 1744| 
 1745|         fdd->post_process_opaque = frame_ctx;
 1746|         fdd->post_process_opaque_free = ff_lcevc_unref;
 1747|         fdd->post_process = ff_lcevc_process;
 1748|     }
 1749|     dc->lcevc.frame = 0;
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
```

### Turn 4  _(tok 8021+615, stop=tool_use)_

**Reasoning:** So decode.c line 1811 is inside `ff_get_buffer`.

Wait — is it? ff_get_buffer starts at 1755 and ends at 1833. Yes.

Now, amfdec.c line 352 is inside `amf_amfsurface_to_avframe`.

qsvdec.c line 179 inside `qsv_get_continuous_buffer`.

videotoolbox.c line 155 inside `ff_videotoolbox_alloc_frame`.

Also I should check whether there's any macro-wrapped usage or a function pointer assignment. The grep found 6 matches total (definition, prototype, 4 calls). Let me double-check there isn't an indirect usage through a macro like a #define renaming. Let's grep for "attach_decode_data" more loosely (already did). Maybe there's a variant in some other branch of the repository? The tool only has "old" version.

Let me verify the amfdec function's definition line and also double check nothing else in amfdec.c. Grep showed only one match in amfdec.c.

All good. Confidence high.


**Says:** 

I found all references and identified each enclosing function:

| Call site | File | Enclosing function |
|---|---|---|
| `ret = ff_attach_decode_data(frame);` (line 352) | `libavcodec/amfdec.c` | `amf_amfsurface_to_avframe` |
| `ret = ff_attach_decode_data(frame);` (line 1811) | `libavcodec/decode.c` | `ff_get_buffer` (starts at line 1755) |
| `ret = ff_attach_decode_data(frame);` (line 179) | `libavcodec/qsvdec.c` | `qsv_get_continuous_buffer` |
| `int ret = ff_attach_decode_data(frame);` (line 155) | `libavcodec/videotoolbox.c` | `ff_videotoolbox_alloc_frame` |

Excluded: the definition at `libavcodec/decode.c:1658` and the prototype at `libavcodec/decode.h:89`.



- **submit_callers** → `{"callers": [{"function": "amf_amfsurface_to_avframe", "file": "libavcodec/amfdec.c"}, {"function": "ff_get_buffer", "file": "libavcodec/decode.c"}, {"function": "qsv_get_continuous_buffer", "file": "libavcodec/qsvdec.c"}, {"function": "ff_videotoolbox_alloc_frame", "file": "libavcodec/videotoolbox.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 4, "n_truth": 4, "tp": 4, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

