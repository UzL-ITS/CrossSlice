# Impact-analysis transcript — ffmpeg @ 37d5cb84e8ab — anthropic:claude-haiku-5-5

- target: `ff_vk_exec_get` (libavutil/vulkan.c), arity 1->2
- truth: [['libavcodec/vulkan_decode.c', 'ff_vk_decode_flush'], ['libavcodec/vulkan_decode.c', 'ff_vk_decode_frame'], ['libavcodec/vulkan_encode.c', 'vulkan_encode_issue'], ['libavfilter/vf_nlmeans_vulkan.c', 'nlmeans_vulkan_filter_frame'], ['libavfilter/vulkan_filter.c', 'ff_vk_filter_process_2pass'], ['libavfilter/vulkan_filter.c', 'ff_vk_filter_process_Nin'], ['libavfilter/vulkan_filter.c', 'ff_vk_filter_process_simple'], ['libavutil/hwcontext_vulkan.c', 'prepare_frame'], ['libavutil/hwcontext_vulkan.c', 'vulkan_map_from_drm_frame_sync'], ['libavutil/hwcontext_vulkan.c', 'vulkan_transfer_frame']]

## Self-navigation arm

### Turn 1  _(tok 1221+105, stop=tool_use)_

**Reasoning:** I'm searching the repo for every use of ff_vk_exec_get to see where it's called.



- `grep(pattern=ff_vk_exec_get, version=old)` →

```
16 matches
libavcodec/vulkan_decode.c:296:    FFVkExecContext *exec = ff_vk_exec_get(&dec->exec_pool);
libavcodec/vulkan_decode.c:348:    FFVkExecContext *exec = ff_vk_exec_get(&dec->exec_pool);
libavcodec/vulkan_decode.c:359:        ret = ff_vk_exec_get_query(&ctx->s, exec, (void **)&result,
libavcodec/vulkan_encode.c:342:    exec = vp->exec = ff_vk_exec_get(&ctx->enc_pool);
libavcodec/vulkan_encode.c:473:    ret = ff_vk_exec_get_query(&ctx->s, vp->exec, (void **)&query_data, 0);
libavfilter/vf_nlmeans_vulkan.c:839:    exec = ff_vk_exec_get(&s->e);
libavfilter/vulkan_filter.c:252:    FFVkExecContext *exec = ff_vk_exec_get(e);
libavfilter/vulkan_filter.c:324:    FFVkExecContext *exec = ff_vk_exec_get(e);
libavfilter/vulkan_filter.c:412:    FFVkExecContext *exec = ff_vk_exec_get(e);
libavutil/hwcontext_vulkan.c:2256:    FFVkExecContext *exec = ff_vk_exec_get(ectx);
libavutil/hwcontext_vulkan.c:3193:        exec = ff_vk_exec_get(&fp->compute_exec);
libavutil/hwcontext_vulkan.c:4101:    exec = ff_vk_exec_get(&fp->upload_exec);
libavutil/vulkan.c:457:VkResult ff_vk_exec_get_query(FFVulkanContext *s, FFVkExecContext *e,
libavutil/vulkan.c:485:FFVkExecContext *ff_vk_exec_get(FFVkExecPool *pool)
libavutil/vulkan.h:390:FFVkExecContext *ff_vk_exec_get(FFVkExecPool *pool);
libavutil/vulkan.h:397:VkResult ff_vk_exec_get_query(FFVulkanContext *s, FFVkExecContext *e,
```

### Turn 2  _(tok 2132+1708, stop=tool_use)_

**Reasoning:** I'm checking which of the grep matches are real calls to ff_vk_exec_get, since ff_vk_exec_get_query also matches and those four hits belong to the _query variant. Next up are the remaining call sites, starting with vulkan_decode.c around line 296.

I'm now going through the remaining call sites: the ones in vulkan_decode.c, vulkan_encode.c, the nlmeans and vulkan_filter files, and hwcontext_vulkan.c. The definition in vulkan.c and the prototype in vulkan.h are being set aside, and I still want to check for calls split across lines.



- `read_file(path=libavcodec/vulkan_decode.c, version=old, start_line=280, end_line=300)` →

```
libavcodec/vulkan_decode.c lines 280-300 of 1249
  280| 
  281|     FFVulkanFunctions *vk = &ctx->s.vkfn;
  282|     VkVideoBeginCodingInfoKHR decode_start = {
  283|         .sType = VK_STRUCTURE_TYPE_VIDEO_BEGIN_CODING_INFO_KHR,
  284|         .videoSession = ctx->common.session,
  285|         .videoSessionParameters = ctx->empty_session_params,
  286|     };
  287|     VkVideoCodingControlInfoKHR decode_ctrl = {
  288|         .sType = VK_STRUCTURE_TYPE_VIDEO_CODING_CONTROL_INFO_KHR,
  289|         .flags = VK_VIDEO_CODING_CONTROL_RESET_BIT_KHR,
  290|     };
  291|     VkVideoEndCodingInfoKHR decode_end = {
  292|         .sType = VK_STRUCTURE_TYPE_VIDEO_END_CODING_INFO_KHR,
  293|     };
  294| 
  295|     VkCommandBuffer cmd_buf;
  296|     FFVkExecContext *exec = ff_vk_exec_get(&dec->exec_pool);
  297|     int had_submission = exec->had_submission;
  298|     ff_vk_exec_start(&ctx->s, exec);
  299|     cmd_buf = exec->buf;
  300| 
```

- `read_file(path=libavcodec/vulkan_decode.c, version=old, start_line=335, end_line=350)` →

```
libavcodec/vulkan_decode.c lines 335-350 of 1249
  335|         .videoSessionParameters = *par,
  336|         .referenceSlotCount = vp->decode_info.referenceSlotCount,
  337|         .pReferenceSlots = vp->decode_info.pReferenceSlots,
  338|     };
  339|     VkVideoEndCodingInfoKHR decode_end = {
  340|         .sType = VK_STRUCTURE_TYPE_VIDEO_END_CODING_INFO_KHR,
  341|     };
  342| 
  343|     VkImageMemoryBarrier2 img_bar[37];
  344|     int nb_img_bar = 0;
  345|     size_t data_size = FFALIGN(vp->slices_size,
  346|                                ctx->caps.minBitstreamBufferSizeAlignment);
  347| 
  348|     FFVkExecContext *exec = ff_vk_exec_get(&dec->exec_pool);
  349| 
  350|     /* The current decoding reference has to be bound as an inactive reference */
```

- `read_file(path=libavcodec/vulkan_encode.c, version=old, start_line=320, end_line=345)` →

```
libavcodec/vulkan_encode.c lines 320-345 of 1060
  320|                 filler_data += offset_align;
  321| 
  322|             filler_data -= ctx->codec->filler_header_size;
  323| 
  324|             err = ctx->codec->write_filler(avctx, filler_data,
  325|                                            hdr_dst, &data_size);
  326|             if (err < 0)
  327|                 goto fail;
  328| 
  329|             encode_info.dstBufferOffset += data_size;
  330|             encode_info.dstBufferRange  -= data_size;
  331|         }
  332|     }
  333| 
  334|     vp->slices_offset = encode_info.dstBufferOffset;
  335| 
  336|     /* Align buffer size to the nearest lower alignment requirement. */
  337|     encode_info.dstBufferRange -= size_align;
  338|     encode_info.dstBufferRange = FFALIGN(encode_info.dstBufferRange,
  339|                                          size_align);
  340| 
  341|     /* Start command buffer recording */
  342|     exec = vp->exec = ff_vk_exec_get(&ctx->enc_pool);
  343|     ff_vk_exec_start(&ctx->s, exec);
  344|     cmd_buf = exec->buf;
  345| 
```

- `read_file(path=libavfilter/vf_nlmeans_vulkan.c, version=old, start_line=825, end_line=842)` →

```
libavfilter/vf_nlmeans_vulkan.c lines 825-842 of 1123
  825|     sums_offs[0] = ws_total_size;
  826|     for (int i = 1; i < desc->nb_components; i++) {
  827|         weights_offs[i] = weights_offs[i - 1] + ws_size[i - 1];
  828|         sums_offs[i] = sums_offs[i - 1] + ws_size[i - 1];
  829|     }
  830| 
  831|     /* Output frame */
  832|     out = ff_get_video_buffer(outlink, outlink->w, outlink->h);
  833|     if (!out) {
  834|         err = AVERROR(ENOMEM);
  835|         goto fail;
  836|     }
  837| 
  838|     /* Execution context */
  839|     exec = ff_vk_exec_get(&s->e);
  840|     ff_vk_exec_start(vkctx, exec);
  841| 
  842|     /* Dependencies */
```

- `read_file(path=libavfilter/vulkan_filter.c, version=old, start_line=240, end_line=255)` →

```
libavfilter/vulkan_filter.c lines 240-255 of 473
  240| int ff_vk_filter_process_simple(FFVulkanContext *vkctx, FFVkExecPool *e,
  241|                                 FFVulkanShader *shd, AVFrame *out_f, AVFrame *in_f,
  242|                                 VkSampler sampler, void *push_src, size_t push_size)
  243| {
  244|     int err = 0;
  245|     FFVulkanFunctions *vk = &vkctx->vkfn;
  246|     VkImageView in_views[AV_NUM_DATA_POINTERS];
  247|     VkImageView out_views[AV_NUM_DATA_POINTERS];
  248|     VkImageMemoryBarrier2 img_bar[37];
  249|     int nb_img_bar = 0;
  250| 
  251|     /* Update descriptors and init the exec context */
  252|     FFVkExecContext *exec = ff_vk_exec_get(e);
  253|     ff_vk_exec_start(vkctx, exec);
  254| 
  255|     RET(ff_vk_exec_add_dep_frame(vkctx, exec, out_f,
```

- `read_file(path=libavfilter/vulkan_filter.c, version=old, start_line=310, end_line=326)` →

```
libavfilter/vulkan_filter.c lines 310-326 of 473
  310| int ff_vk_filter_process_2pass(FFVulkanContext *vkctx, FFVkExecPool *e,
  311|                                FFVulkanShader *shd_list[2],
  312|                                AVFrame *out, AVFrame *tmp, AVFrame *in,
  313|                                VkSampler sampler, void *push_src, size_t push_size)
  314| {
  315|     int err = 0;
  316|     FFVulkanFunctions *vk = &vkctx->vkfn;
  317|     VkImageView in_views[AV_NUM_DATA_POINTERS];
  318|     VkImageView tmp_views[AV_NUM_DATA_POINTERS];
  319|     VkImageView out_views[AV_NUM_DATA_POINTERS];
  320|     VkImageMemoryBarrier2 img_bar[37];
  321|     int nb_img_bar = 0;
  322| 
  323|     /* Update descriptors and init the exec context */
  324|     FFVkExecContext *exec = ff_vk_exec_get(e);
  325|     ff_vk_exec_start(vkctx, exec);
  326| 
```

- `read_file(path=libavfilter/vulkan_filter.c, version=old, start_line=400, end_line=414)` →

```
libavfilter/vulkan_filter.c lines 400-414 of 473
  400|                              FFVulkanShader *shd,
  401|                              AVFrame *out, AVFrame *in[], int nb_in,
  402|                              VkSampler sampler, void *push_src, size_t push_size)
  403| {
  404|     int err = 0;
  405|     FFVulkanFunctions *vk = &vkctx->vkfn;
  406|     VkImageView in_views[16][AV_NUM_DATA_POINTERS];
  407|     VkImageView out_views[AV_NUM_DATA_POINTERS];
  408|     VkImageMemoryBarrier2 img_bar[128];
  409|     int nb_img_bar = 0;
  410| 
  411|     /* Update descriptors and init the exec context */
  412|     FFVkExecContext *exec = ff_vk_exec_get(e);
  413|     ff_vk_exec_start(vkctx, exec);
  414| 
```

- `read_file(path=libavutil/hwcontext_vulkan.c, version=old, start_line=2240, end_line=2258)` →

```
libavutil/hwcontext_vulkan.c lines 2240-2258 of 4378
 2240|     VkImageLayout new_layout;
 2241|     VkAccessFlags2 new_access;
 2242|     VkPipelineStageFlagBits2 src_stage = VK_PIPELINE_STAGE_2_NONE;
 2243| 
 2244|     /* This is dirty - but it works. The vulkan.c dependency system doesn't
 2245|      * free non-refcounted frames, and non-refcounted hardware frames cannot
 2246|      * happen anywhere outside of here. */
 2247|     AVBufferRef tmp_ref = {
 2248|         .data = (uint8_t *)hwfc,
 2249|     };
 2250|     AVFrame tmp_frame = {
 2251|         .data[0] = (uint8_t *)frame,
 2252|         .hw_frames_ctx = &tmp_ref,
 2253|     };
 2254| 
 2255|     VkCommandBuffer cmd_buf;
 2256|     FFVkExecContext *exec = ff_vk_exec_get(ectx);
 2257|     cmd_buf = exec->buf;
 2258|     ff_vk_exec_start(&p->vkctx, exec);
```

- `read_file(path=libavutil/hwcontext_vulkan.c, version=old, start_line=3180, end_line=3195)` →

```
libavutil/hwcontext_vulkan.c lines 3180-3195 of 4378
 3180|             };
 3181| 
 3182|             ret = vk->ImportSemaphoreFdKHR(hwctx->act_dev, &import_info);
 3183|             if (ret != VK_SUCCESS) {
 3184|                 av_log(hwctx, AV_LOG_ERROR, "Failed to import semaphore: %s\n",
 3185|                        ff_vk_ret2str(ret));
 3186|                 err = AVERROR_EXTERNAL;
 3187|                 for (; i >= 0; i--)
 3188|                     vk->DestroySemaphore(hwctx->act_dev, drm_sync_sem[i], hwctx->alloc);
 3189|                 return err;
 3190|             }
 3191|         }
 3192| 
 3193|         exec = ff_vk_exec_get(&fp->compute_exec);
 3194|         cmd_buf = exec->buf;
 3195| 
```

- `read_file(path=libavutil/hwcontext_vulkan.c, version=old, start_line=4085, end_line=4103)` →

```
libavutil/hwcontext_vulkan.c lines 4085-4103 of 4378
 4085|             host_mapped = 1;
 4086|     }
 4087| 
 4088|     if (!host_mapped) {
 4089|         err = get_plane_buf(hwfc, &bufs[0], swf, region, upload);
 4090|         if (err < 0)
 4091|             goto end;
 4092|         nb_bufs = 1;
 4093| 
 4094|         if (upload) {
 4095|             err = copy_buffer_data(hwfc, bufs[0], swf, region, planes, 1);
 4096|             if (err < 0)
 4097|                 goto end;
 4098|         }
 4099|     }
 4100| 
 4101|     exec = ff_vk_exec_get(&fp->upload_exec);
 4102|     cmd_buf = exec->buf;
 4103| 
```

### Turn 3  _(tok 8037+858, stop=tool_use)_

**Reasoning:** I need the names of the functions containing each match, so I'll grep each file for column-zero definition lines and work out the enclosing functions from those.



**Says:** Now I need the enclosing function for each call. I'll find the column-0 function definitions in each file.

- `grep(pattern=^[A-Za-z_].*\(|^\{|^\}, version=old, path_glob=libavcodec/vulkan_decode.c, max_results=300)` →

```
61 matches
libavcodec/vulkan_decode.c:47:};
libavcodec/vulkan_decode.c:49:static const FFVulkanDecodeDescriptor *get_codecdesc(enum AVCodecID codec_id)
libavcodec/vulkan_decode.c:50:{
libavcodec/vulkan_decode.c:56:}
libavcodec/vulkan_decode.c:58:static const VkVideoProfileInfoKHR *get_video_profile(FFVulkanDecodeShared *ctx, enum AVCodecID codec_id)
libavcodec/vulkan_decode.c:59:{
libavcodec/vulkan_decode.c:78:}
libavcodec/vulkan_decode.c:80:int ff_vk_update_thread_context(AVCodecContext *dst, const AVCodecContext *src)
libavcodec/vulkan_decode.c:81:{
libavcodec/vulkan_decode.c:118:}
libavcodec/vulkan_decode.c:120:int ff_vk_params_invalidate(AVCodecContext *avctx, int t, const uint8_t *b, uint32_t s)
libavcodec/vulkan_decode.c:121:{
libavcodec/vulkan_decode.c:125:}
libavcodec/vulkan_decode.c:127:static AVFrame *vk_get_dpb_pool(FFVulkanDecodeShared *ctx)
libavcodec/vulkan_decode.c:128:{
libavcodec/vulkan_decode.c:139:}
libavcodec/vulkan_decode.c:141:int ff_vk_decode_prepare_frame(FFVulkanDecodeContext *dec, AVFrame *pic,
libavcodec/vulkan_decode.c:144:{
libavcodec/vulkan_decode.c:203:}
libavcodec/vulkan_decode.c:205:int ff_vk_decode_add_slice(AVCodecContext *avctx, FFVulkanDecodePicture *vp,
libavcodec/vulkan_decode.c:208:{
libavcodec/vulkan_decode.c:274:}
libavcodec/vulkan_decode.c:276:void ff_vk_decode_flush(AVCodecContext *avctx)
libavcodec/vulkan_decode.c:277:{
libavcodec/vulkan_decode.c:310:}
libavcodec/vulkan_decode.c:312:int ff_vk_decode_frame(AVCodecContext *avctx,
libavcodec/vulkan_decode.c:315:{
libavcodec/vulkan_decode.c:541:}
libavcodec/vulkan_decode.c:543:void ff_vk_decode_free_frame(AVHWDeviceContext *dev_ctx, FFVulkanDecodePicture *vp)
libavcodec/vulkan_decode.c:544:{
libavcodec/vulkan_decode.c:572:}
libavcodec/vulkan_decode.c:574:static void free_common(FFRefStructOpaque unused, void *obj)
libavcodec/vulkan_decode.c:575:{
libavcodec/vulkan_decode.c:594:}
libavcodec/vulkan_decode.c:596:static int vulkan_decode_bootstrap(AVCodecContext *avctx, AVBufferRef *frames_ref)
libavcodec/vulkan_decode.c:597:{
libavcodec/vulkan_decode.c:632:}
libavcodec/vulkan_decode.c:634:static VkResult vulkan_setup_profile(AVCodecContext *avctx,
libavcodec/vulkan_decode.c:645:{
libavcodec/vulkan_decode.c:707:}
libavcodec/vulkan_decode.c:709:static int vulkan_decode_get_profile(AVCodecContext *avctx, AVBufferRef *frames_ref,
libavcodec/vulkan_decode.c:713:{
libavcodec/vulkan_decode.c:967:}
libavcodec/vulkan_decode.c:969:static void free_profile_data(AVHWFramesContext *hwfc)
libavcodec/vulkan_decode.c:970:{
libavcodec/vulkan_decode.c:972:}
libavcodec/vulkan_decode.c:974:int ff_vk_frame_params(AVCodecContext *avctx, AVBufferRef *hw_frames_ctx)
libavcodec/vulkan_decode.c:975:{
libavcodec/vulkan_decode.c:1025:}
libavcodec/vulkan_decode.c:1027:static void vk_decode_free_params(void *opaque, uint8_t *data)
libavcodec/vulkan_decode.c:1028:{
libavcodec/vulkan_decode.c:1035:}
libavcodec/vulkan_decode.c:1037:int ff_vk_decode_create_params(AVBufferRef **par_ref, void *logctx, FFVulkanDecodeShared *ctx,
libavcodec/vulkan_decode.c:1039:{
libavcodec/vulkan_decode.c:1064:}
libavcodec/vulkan_decode.c:1066:int ff_vk_decode_uninit(AVCodecContext *avctx)
libavcodec/vulkan_decode.c:1067:{
libavcodec/vulkan_decode.c:1079:}
libavcodec/vulkan_decode.c:1081:int ff_vk_decode_init(AVCodecContext *avctx)
libavcodec/vulkan_decode.c:1082:{
libavcodec/vulkan_decode.c:1248:}
```

- `grep(pattern=^[A-Za-z_].*\(, version=old, path_glob=libavcodec/vulkan_encode.c, max_results=300)` →

```
13 matches
libavcodec/vulkan_encode.c:31:av_cold void ff_vulkan_encode_uninit(FFVulkanEncodeContext *ctx)
libavcodec/vulkan_encode.c:54:static int vulkan_encode_init(AVCodecContext *avctx, FFHWBaseEncodePicture *pic)
libavcodec/vulkan_encode.c:95:static int vulkan_encode_free(AVCodecContext *avctx, FFHWBaseEncodePicture *pic)
libavcodec/vulkan_encode.c:115:static int init_pic_rc(AVCodecContext *avctx, FFHWBaseEncodePicture *pic,
libavcodec/vulkan_encode.c:141:static int vulkan_encode_issue(AVCodecContext *avctx,
libavcodec/vulkan_encode.c:447:static void vulkan_encode_wait(AVCodecContext *avctx,
libavcodec/vulkan_encode.c:462:static int vulkan_encode_output(AVCodecContext *avctx,
libavcodec/vulkan_encode.c:542:int ff_vulkan_encode_receive_packet(AVCodecContext *avctx, AVPacket *pkt)
libavcodec/vulkan_encode.c:548:static int vulkan_encode_create_dpb(AVCodecContext *avctx, FFVulkanEncodeContext *ctx)
libavcodec/vulkan_encode.c:611:static av_cold int init_rc(AVCodecContext *avctx, FFVulkanEncodeContext *ctx)
libavcodec/vulkan_encode.c:672:av_cold int ff_vulkan_write_global_header(AVCodecContext *avctx,
libavcodec/vulkan_encode.c:702:av_cold int ff_vulkan_encode_init(AVCodecContext *avctx, FFVulkanEncodeContext *ctx,
libavcodec/vulkan_encode.c:1027:int ff_vulkan_encode_create_session_params(AVCodecContext *avctx, FFVulkanEncodeContext *ctx,
```

- `grep(pattern=^[A-Za-z_].*\(, version=old, path_glob=libavfilter/vf_nlmeans_vulkan.c, max_results=300)` →

```
11 matches
libavfilter/vf_nlmeans_vulkan.c:69:static void insert_first(FFVulkanShader *shd, int r, const char *off, int horiz, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:86:static void insert_horizontal_pass(FFVulkanShader *shd, int nb_rows, int first, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:112:static void insert_vertical_pass(FFVulkanShader *shd, int nb_rows, int first, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:141:static void insert_weights_pass(FFVulkanShader *shd, int nb_rows, int vert,
libavfilter/vf_nlmeans_vulkan.c:213:static av_cold int init_weights_pipeline(FFVulkanContext *vkctx, FFVkExecPool *exec,
libavfilter/vf_nlmeans_vulkan.c:421:static av_cold int init_denoise_pipeline(FFVulkanContext *vkctx, FFVkExecPool *exec,
libavfilter/vf_nlmeans_vulkan.c:568:static av_cold int init_filter(AVFilterContext *ctx)
libavfilter/vf_nlmeans_vulkan.c:690:static int denoise_pass(NLMeansVulkanContext *s, FFVkExecContext *exec,
libavfilter/vf_nlmeans_vulkan.c:740:static int nlmeans_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_nlmeans_vulkan.c:1045:static void nlmeans_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_nlmeans_vulkan.c:1091:AVFILTER_DEFINE_CLASS(nlmeans_vulkan);
```

- `grep(pattern=^[A-Za-z_].*\(, version=old, path_glob=libavfilter/vulkan_filter.c, max_results=300)` →

```
7 matches
libavfilter/vulkan_filter.c:25:int ff_vk_filter_init_context(AVFilterContext *avctx, FFVulkanContext *s,
libavfilter/vulkan_filter.c:174:int ff_vk_filter_config_input(AVFilterLink *inlink)
libavfilter/vulkan_filter.c:207:int ff_vk_filter_config_output(AVFilterLink *outlink)
libavfilter/vulkan_filter.c:231:int ff_vk_filter_init(AVFilterContext *avctx)
libavfilter/vulkan_filter.c:240:int ff_vk_filter_process_simple(FFVulkanContext *vkctx, FFVkExecPool *e,
libavfilter/vulkan_filter.c:310:int ff_vk_filter_process_2pass(FFVulkanContext *vkctx, FFVkExecPool *e,
libavfilter/vulkan_filter.c:399:int ff_vk_filter_process_Nin(FFVulkanContext *vkctx, FFVkExecPool *e,
```

- `grep(pattern=^[A-Za-z_].*\(, version=old, path_glob=libavutil/hwcontext_vulkan.c, max_results=300)` →

```
66 matches
libavutil/hwcontext_vulkan.c:240:static const int nb_vk_formats_list = FF_ARRAY_ELEMS(vk_formats_list);
libavutil/hwcontext_vulkan.c:242:const VkFormat *av_vkfmt_from_pixfmt(enum AVPixelFormat p)
libavutil/hwcontext_vulkan.c:250:static const struct FFVkFormatEntry *vk_find_format_entry(enum AVPixelFormat p)
libavutil/hwcontext_vulkan.c:285:FN_MAP_TO(VkFormatFeatureFlagBits2, feats, VkImageUsageFlags, usage)
libavutil/hwcontext_vulkan.c:288:FN_MAP_TO(VkImageUsageFlags, usage, VkFormatFeatureFlagBits2, feats)
libavutil/hwcontext_vulkan.c:292:static int vkfmt_from_pixfmt2(AVHWDeviceContext *dev_ctx, enum AVPixelFormat p,
libavutil/hwcontext_vulkan.c:379:static int load_libvulkan(AVHWDeviceContext *ctx)
libavutil/hwcontext_vulkan.c:456:static VkBool32 VKAPI_CALL vk_dbg_callback(VkDebugUtilsMessageSeverityFlagBitsEXT severity,
libavutil/hwcontext_vulkan.c:521:static int check_extensions(AVHWDeviceContext *ctx, int dev, AVDictionary *opts,
libavutil/hwcontext_vulkan.c:660:static int check_layers(AVHWDeviceContext *ctx, AVDictionary *opts,
libavutil/hwcontext_vulkan.c:807:static int create_instance(AVHWDeviceContext *ctx, AVDictionary *opts,
libavutil/hwcontext_vulkan.c:956:static const char *vk_dev_type(enum VkPhysicalDeviceType type)
libavutil/hwcontext_vulkan.c:968:static int find_device(AVHWDeviceContext *ctx, VulkanDeviceSelection *select)
libavutil/hwcontext_vulkan.c:1125:static inline int pick_queue_family(VkQueueFamilyProperties2 *qf, uint32_t num_qf,
libavutil/hwcontext_vulkan.c:1154:static inline int pick_video_queue_family(VkQueueFamilyProperties2 *qf,
libavutil/hwcontext_vulkan.c:1183:static int setup_queue_families(AVHWDeviceContext *ctx, VkDeviceCreateInfo *cd)
libavutil/hwcontext_vulkan.c:1365:static void vulkan_device_free(AVHWDeviceContext *ctx)
libavutil/hwcontext_vulkan.c:1388:static void vulkan_device_uninit(AVHWDeviceContext *ctx)
libavutil/hwcontext_vulkan.c:1401:static int vulkan_device_create_internal(AVHWDeviceContext *ctx,
libavutil/hwcontext_vulkan.c:1624:static void lock_queue(AVHWDeviceContext *ctx, uint32_t queue_family, uint32_t index)
libavutil/hwcontext_vulkan.c:1630:static void unlock_queue(AVHWDeviceContext *ctx, uint32_t queue_family, uint32_t index)
libavutil/hwcontext_vulkan.c:1636:static int vulkan_device_init(AVHWDeviceContext *ctx)
libavutil/hwcontext_vulkan.c:1853:static int vulkan_device_create(AVHWDeviceContext *ctx, const char *device,
libavutil/hwcontext_vulkan.c:1869:static int vulkan_device_derive(AVHWDeviceContext *ctx,
libavutil/hwcontext_vulkan.c:1972:static int vulkan_frames_get_constraints(AVHWDeviceContext *ctx,
libavutil/hwcontext_vulkan.c:2018:static int alloc_mem(AVHWDeviceContext *ctx, VkMemoryRequirements *req,
libavutil/hwcontext_vulkan.c:2076:static void vulkan_free_internal(AVVkFrame *f)
libavutil/hwcontext_vulkan.c:2112:static void vulkan_frame_free(AVHWFramesContext *hwfc, AVVkFrame *f)
libavutil/hwcontext_vulkan.c:2146:static void vulkan_frame_free_cb(void *opaque, uint8_t *data)
libavutil/hwcontext_vulkan.c:2151:static int alloc_bind_mem(AVHWFramesContext *hwfc, AVVkFrame *f,
libavutil/hwcontext_vulkan.c:2230:static int prepare_frame(AVHWFramesContext *hwfc, FFVkExecPool *ectx,
libavutil/hwcontext_vulkan.c:2320:static inline void get_plane_wh(uint32_t *w, uint32_t *h, enum AVPixelFormat format,
libavutil/hwcontext_vulkan.c:2337:static int create_frame(AVHWFramesContext *hwfc, AVVkFrame **frame,
libavutil/hwcontext_vulkan.c:2446:static void try_export_flags(AVHWFramesContext *hwfc,
libavutil/hwcontext_vulkan.c:2508:static AVBufferRef *vulkan_pool_alloc(void *opaque, size_t size)
libavutil/hwcontext_vulkan.c:2578:static void lock_frame(AVHWFramesContext *fc, AVVkFrame *vkf)
libavutil/hwcontext_vulkan.c:2583:static void unlock_frame(AVHWFramesContext *fc, AVVkFrame *vkf)
libavutil/hwcontext_vulkan.c:2588:static void vulkan_frames_uninit(AVHWFramesContext *hwfc)
libavutil/hwcontext_vulkan.c:2606:static int vulkan_frames_init(AVHWFramesContext *hwfc)
libavutil/hwcontext_vulkan.c:2765:static int vulkan_get_buffer(AVHWFramesContext *hwfc, AVFrame *frame)
libavutil/hwcontext_vulkan.c:2779:static int vulkan_transfer_get_formats(AVHWFramesContext *hwfc,
libavutil/hwcontext_vulkan.c:2805:static void vulkan_unmap_from_drm(AVHWFramesContext *hwfc, HWMapDescriptor *hwmap)
libavutil/hwcontext_vulkan.c:2839:static inline VkFormat drm_to_vulkan_fmt(uint32_t drm_fourcc)
libavutil/hwcontext_vulkan.c:2847:static int vulkan_map_from_drm_frame_desc(AVHWFramesContext *hwfc, AVVkFrame **frame,
libavutil/hwcontext_vulkan.c:3117:static int vulkan_map_from_drm_frame_sync(AVHWFramesContext *hwfc, AVFrame *dst,
libavutil/hwcontext_vulkan.c:3244:static int vulkan_map_from_drm(AVHWFramesContext *hwfc, AVFrame *dst,
libavutil/hwcontext_vulkan.c:3278:static int vulkan_map_from_vaapi(AVHWFramesContext *dst_fc,
libavutil/hwcontext_vulkan.c:3314:static int vulkan_export_to_cuda(AVHWFramesContext *hwfc,
libavutil/hwcontext_vulkan.c:3485:static int vulkan_transfer_data_from_cuda(AVHWFramesContext *hwfc,
libavutil/hwcontext_vulkan.c:3576:static int vulkan_map_to(AVHWFramesContext *hwfc, AVFrame *dst,
libavutil/hwcontext_vulkan.c:3607:static void vulkan_unmap_to_drm(AVHWFramesContext *hwfc, HWMapDescriptor *hwmap)
libavutil/hwcontext_vulkan.c:3617:static inline uint32_t vulkan_fmt_to_drm(VkFormat vkfmt)
libavutil/hwcontext_vulkan.c:3625:static int vulkan_map_to_drm(AVHWFramesContext *hwfc, AVFrame *dst,
libavutil/hwcontext_vulkan.c:3736:static int vulkan_map_to_vaapi(AVHWFramesContext *hwfc, AVFrame *dst,
libavutil/hwcontext_vulkan.c:3763:static int vulkan_map_from(AVHWFramesContext *hwfc, AVFrame *dst,
libavutil/hwcontext_vulkan.c:3789:static int copy_buffer_data(AVHWFramesContext *hwfc, AVBufferRef *buf,
libavutil/hwcontext_vulkan.c:3837:static int get_plane_buf(AVHWFramesContext *hwfc, AVBufferRef **dst,
libavutil/hwcontext_vulkan.c:3882:static int create_mapped_buffer(AVHWFramesContext *hwfc,
libavutil/hwcontext_vulkan.c:3930:static void destroy_avvkbuf(void *opaque, uint8_t *data)
libavutil/hwcontext_vulkan.c:3938:static int host_map_frame(AVHWFramesContext *hwfc, AVBufferRef **dst, int *nb_bufs,
libavutil/hwcontext_vulkan.c:4041:static int vulkan_transfer_frame(AVHWFramesContext *hwfc,
libavutil/hwcontext_vulkan.c:4177:static int vulkan_transfer_data_to(AVHWFramesContext *hwfc, AVFrame *dst,
libavutil/hwcontext_vulkan.c:4203:static int vulkan_transfer_data_to_cuda(AVHWFramesContext *hwfc, AVFrame *dst,
libavutil/hwcontext_vulkan.c:4294:static int vulkan_transfer_data_from(AVHWFramesContext *hwfc, AVFrame *dst,
libavutil/hwcontext_vulkan.c:4319:static int vulkan_frames_derive_to(AVHWFramesContext *dst_fc,
libavutil/hwcontext_vulkan.c:4325:AVVkFrame *av_vk_frame_alloc(void)
```

### Turn 4  _(tok 16488+1178, stop=tool_use)_

**Reasoning:** I'm checking which function encloses lines 296 and 348 in vulkan_decode.c. Line 296 falls inside ff_vk_decode_flush, and line 348 falls inside ff_vk_decode_frame.

I'm mapping the remaining call sites to their enclosing functions: the encode issue path, the nlmeans filter frame, the three vulkan_filter process variants, and the hwcontext prepare, map, and transfer functions.



**Says:** I found 13 call sites of `ff_vk_exec_get` (excluding the `ff_vk_exec_get_query` matches, the definition, and the prototype). Each one maps to an enclosing function by line range.

- **submit_callers** → `{"callers": [{"function": "ff_vk_decode_flush", "file": "libavcodec/vulkan_decode.c"}, {"function": "ff_vk_decode_frame", "file": "libavcodec/vulkan_decode.c"}, {"function": "vulkan_encode_issue", "file": "libavcodec/vulkan_encode.c"}, {"function": "nlmeans_vulkan_filter_frame", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "ff_vk_filter_process_simple", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_2pass", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_Nin", "file": "libavfilter/vulkan_filter.c"}, {"function": "prepare_frame", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_map_from_drm_frame_sync", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_transfer_frame", "file": "libavutil/hwcontext_vulkan.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3756+234, stop=tool_use)_

**Reasoning:** I'll pull the callers of ff_vk_exec_get using get_callers, and run a grep alongside it so I don't miss any references.



- `get_callers(name=ff_vk_exec_get, limit=200, rev=None)` →

```
{
  "name": "ff_vk_exec_get",
  "version": "old",
  "callers": [
    {
      "caller": "ff_vk_decode_flush",
      "file": "libavcodec/vulkan_decode.c",
      "line": 296
    },
    {
      "caller": "ff_vk_decode_frame",
      "file": "libavcodec/vulkan_decode.c",
      "line": 348
    },
    {
      "caller": "vulkan_encode_issue",
      "file": "libavcodec/vulkan_encode.c",
      "line": 342
    },
    {
      "caller": "nlmeans_vulkan_filter_frame",
      "file": "libavfilter/vf_nlmeans_vulkan.c",
      "line": 839
    },
    {
      "caller": "ff_vk_filter_process_simple",
      "file": "libavfilter/vulkan_filter.c",
      "line": 252
    },
    {
      "caller": "ff_vk_filter_process_2pass",
      "file": "libavfilter/vulkan_filter.c",
      "line": 324
    },
    {
      "caller": "ff_vk_filter_process_Nin",
      "file": "libavfilter/vulkan_filter.c",
      "line": 412
    },
    {
      "caller": "prepare_frame",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 2256
    },
    {
      "caller": "vulkan_map_from_drm_frame_sync",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 3193
    },
    {
      "caller": "vulkan_transfer_frame",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 4101
    }
  ]
}
```

- `grep(pattern=ff_vk_exec_get, version=old, max_results=500)` →

```
16 matches
libavcodec/vulkan_decode.c:296:    FFVkExecContext *exec = ff_vk_exec_get(&dec->exec_pool);
libavcodec/vulkan_decode.c:348:    FFVkExecContext *exec = ff_vk_exec_get(&dec->exec_pool);
libavcodec/vulkan_decode.c:359:        ret = ff_vk_exec_get_query(&ctx->s, exec, (void **)&result,
libavcodec/vulkan_encode.c:342:    exec = vp->exec = ff_vk_exec_get(&ctx->enc_pool);
libavcodec/vulkan_encode.c:473:    ret = ff_vk_exec_get_query(&ctx->s, vp->exec, (void **)&query_data, 0);
libavfilter/vf_nlmeans_vulkan.c:839:    exec = ff_vk_exec_get(&s->e);
libavfilter/vulkan_filter.c:252:    FFVkExecContext *exec = ff_vk_exec_get(e);
libavfilter/vulkan_filter.c:324:    FFVkExecContext *exec = ff_vk_exec_get(e);
libavfilter/vulkan_filter.c:412:    FFVkExecContext *exec = ff_vk_exec_get(e);
libavutil/hwcontext_vulkan.c:2256:    FFVkExecContext *exec = ff_vk_exec_get(ectx);
libavutil/hwcontext_vulkan.c:3193:        exec = ff_vk_exec_get(&fp->compute_exec);
libavutil/hwcontext_vulkan.c:4101:    exec = ff_vk_exec_get(&fp->upload_exec);
libavutil/vulkan.c:457:VkResult ff_vk_exec_get_query(FFVulkanContext *s, FFVkExecContext *e,
libavutil/vulkan.c:485:FFVkExecContext *ff_vk_exec_get(FFVkExecPool *pool)
libavutil/vulkan.h:390:FFVkExecContext *ff_vk_exec_get(FFVkExecPool *pool);
libavutil/vulkan.h:397:VkResult ff_vk_exec_get_query(FFVulkanContext *s, FFVkExecContext *e,
```

### Turn 2  _(tok 5454+816, stop=tool_use)_

**Reasoning:** I'm counting the matches for ff_vk_exec_get: ten call sites across the listed line numbers, plus the definition and prototype. The ff_vk_exec_get_query hits only share a substring with the pattern, so I'm leaving them out.

I'm checking whether the enclosing function names hold up, and whether any function pointers or macros reference ff_vk_exec_get without a direct call. The grep already covers every occurrence, so nothing else turns up there, and the search is limited to git-tracked files.



- **submit_callers** → `{"callers": [{"function": "ff_vk_decode_flush", "file": "libavcodec/vulkan_decode.c"}, {"function": "ff_vk_decode_frame", "file": "libavcodec/vulkan_decode.c"}, {"function": "vulkan_encode_issue", "file": "libavcodec/vulkan_encode.c"}, {"function": "nlmeans_vulkan_filter_frame", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "ff_vk_filter_process_simple", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_2pass", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_Nin", "file": "libavfilter/vulkan_filter.c"}, {"function": "prepare_frame", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_map_from_drm_frame_sync", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_transfer_frame", "file": "libavutil/hwcontext_vulkan.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3208+114, stop=tool_use)_

**Reasoning:** I'm starting by calling get_callers on ff_vk_exec_get with a high limit to pull in the full set of call sites.



- `get_callers(name=ff_vk_exec_get, limit=200)` →

```
{
  "name": "ff_vk_exec_get",
  "version": "old",
  "callers": [
    {
      "caller": "ff_vk_decode_flush",
      "file": "libavcodec/vulkan_decode.c",
      "line": 296
    },
    {
      "caller": "ff_vk_decode_frame",
      "file": "libavcodec/vulkan_decode.c",
      "line": 348
    },
    {
      "caller": "vulkan_encode_issue",
      "file": "libavcodec/vulkan_encode.c",
      "line": 342
    },
    {
      "caller": "nlmeans_vulkan_filter_frame",
      "file": "libavfilter/vf_nlmeans_vulkan.c",
      "line": 839
    },
    {
      "caller": "ff_vk_filter_process_simple",
      "file": "libavfilter/vulkan_filter.c",
      "line": 252
    },
    {
      "caller": "ff_vk_filter_process_2pass",
      "file": "libavfilter/vulkan_filter.c",
      "line": 324
    },
    {
      "caller": "ff_vk_filter_process_Nin",
      "file": "libavfilter/vulkan_filter.c",
      "line": 412
    },
    {
      "caller": "prepare_frame",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 2256
    },
    {
      "caller": "vulkan_map_from_drm_frame_sync",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 3193
    },
    {
      "caller": "vulkan_transfer_frame",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 4101
    }
  ]
}
```

### Turn 2  _(tok 3934+472, stop=tool_use)_

**Reasoning:** I'm checking which version the callers tool is actually reading, since it reported "old" as the parent of the revision. I want to confirm the current working version before trusting that list, so I'm going to try calling it with the work version set explicitly.

I'm not sure the tools can target the working version directly, since they only accept a rev parameter. I'll try get_callers with rev set to HEAD to see whether that gives me the current state.



- `get_callers(name=ff_vk_exec_get, limit=200, rev=HEAD)` →

```
{
  "name": "ff_vk_exec_get",
  "version": "old",
  "callers": [
    {
      "caller": "ff_vk_decode_flush",
      "file": "libavcodec/vulkan_decode.c",
      "line": 296
    },
    {
      "caller": "ff_vk_decode_frame",
      "file": "libavcodec/vulkan_decode.c",
      "line": 348
    },
    {
      "caller": "vulkan_encode_issue",
      "file": "libavcodec/vulkan_encode.c",
      "line": 342
    },
    {
      "caller": "nlmeans_vulkan_filter_frame",
      "file": "libavfilter/vf_nlmeans_vulkan.c",
      "line": 839
    },
    {
      "caller": "ff_vk_filter_process_simple",
      "file": "libavfilter/vulkan_filter.c",
      "line": 252
    },
    {
      "caller": "ff_vk_filter_process_2pass",
      "file": "libavfilter/vulkan_filter.c",
      "line": 324
    },
    {
      "caller": "ff_vk_filter_process_Nin",
      "file": "libavfilter/vulkan_filter.c",
      "line": 412
    },
    {
      "caller": "prepare_frame",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 2256
    },
    {
      "caller": "vulkan_map_from_drm_frame_sync",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 3193
    },
    {
      "caller": "vulkan_transfer_frame",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 4101
    }
  ]
}
```

- `resolve_symbol(name=ff_vk_exec_get)` →

```
{
  "resolved": true,
  "name": "ff_vk_exec_get",
  "version": "old",
  "file": "libavutil/vulkan.c",
  "line": 485,
  "kind": "function",
  "signature": "FFVkExecContext *ff_vk_exec_get(FFVkExecPool *pool)",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 3  _(tok 5213+618, stop=tool_use)_

**Reasoning:** I'm checking whether the "old" version is a problem, since the question is about the current code. The "old" side is the parent of the revision, so with HEAD as the server's commit it would miss callers added in HEAD itself. I'm considering whether to compare against a different revision or look for a "new" version instead.

The tool only resolves "old" by default, so I'm trying other revisions to reach the "new" side. Calling get_callers with rev="HEAD~1" would just give HEAD~2, which doesn't help. I'm going to try get_neighborhood with rev="HEAD" to see whether a "new" version shows up, and check whether the signature change would affect HEAD's callers.



- `get_function_source(name=ff_vk_exec_get, rev=HEAD)` →

```
ff_vk_exec_get (function, old version) — libavutil/vulkan.c:485-490
  485| FFVkExecContext *ff_vk_exec_get(FFVkExecPool *pool)
  486| {
  487|     uint32_t idx = pool->idx++;
  488|     idx %= pool->pool_size;
  489|     return &pool->contexts[idx];
  490| }
```

- `get_summary(name=ff_vk_exec_get)` →

```
{
  "name": "ff_vk_exec_get",
  "version": "old",
  "params_read": [
    "pool"
  ],
  "params_written": [
    "pool*"
  ],
  "params_rebound": [],
  "returns": [
    "return &pool->contexts[idx];"
  ]
}
```

### Turn 4  _(tok 6125+562, stop=tool_use)_

**Reasoning:** I'm checking whether "old" is just what the tool shows for the parent of HEAD, since the work tree may match HEAD and the commit itself could be the signature change. If so, the callers in the old version are what I need, and I'm considering that setup as a plausible explanation.

I'm weighing whether the callers listed under "old" are enough, since the call graph might miss indirect calls like function pointers or callers in other files such as vulkan_encode.c or hwcontext_vulkan.c. I could run a neighborhood or expand query on ff_vk_exec_get to cross-check the list.



- `expand_function(name=ff_vk_exec_get, levels=1)` →

```
{
  "name": "ff_vk_exec_get",
  "version": "old",
  "levels": 1,
  "node": {
    "name": "ff_vk_exec_get",
    "file": "libavutil/vulkan.c",
    "line": 485,
    "kind": "function",
    "state": "analyzed"
  },
  "callees": [],
  "callers": [
    {
      "name": "ff_vk_decode_flush",
      "file": "libavcodec/vulkan_decode.c",
      "line": 276,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        296
      ]
    },
    {
      "name": "ff_vk_decode_frame",
      "file": "libavcodec/vulkan_decode.c",
      "line": 312,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        348
      ]
    },
    {
      "name": "vulkan_encode_issue",
      "file": "libavcodec/vulkan_encode.c",
      "line": 141,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        342
      ]
    },
    {
      "name": "nlmeans_vulkan_filter_frame",
      "file": "libavfilter/vf_nlmeans_vulkan.c",
      "line": 740,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        839
      ]
    },
    {
      "name": "ff_vk_filter_process_simple",
      "file": "libavfilter/vulkan_filter.c",
      "line": 240,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        252
      ]
    },
    {
      "name": "ff_vk_filter_process_2pass",
      "file": "libavfilter/vulkan_filter.c",
      "line": 310,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        324
      ]
    },
    {
      "name": "ff_vk_filter_process_Nin",
      "file": "libavfilter/vulkan_filter.c",
      "line": 399,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        412
      ]
    },
    {
      "name": "prepare_frame",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 2230,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        2256
      ]
    },
    {
      "name": "vulkan_map_from_drm_frame_sync",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 3117,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        3193
      ]
    },
    {
      "name": "vulkan_transfer_frame",
      "file": "libavutil/hwcontext_vulkan.c",
      "line": 4041,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        4101
      ]
    }
  ]
}
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 7907+475, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "ff_vk_decode_flush", "file": "libavcodec/vulkan_decode.c"}, {"function": "ff_vk_decode_frame", "file": "libavcodec/vulkan_decode.c"}, {"function": "vulkan_encode_issue", "file": "libavcodec/vulkan_encode.c"}, {"function": "nlmeans_vulkan_filter_frame", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "ff_vk_filter_process_simple", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_2pass", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_Nin", "file": "libavfilter/vulkan_filter.c"}, {"function": "prepare_frame", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_map_from_drm_frame_sync", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_transfer_frame", "file": "libavutil/hwcontext_vulkan.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

