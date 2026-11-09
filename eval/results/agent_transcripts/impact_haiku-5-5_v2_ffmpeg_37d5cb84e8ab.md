# Impact-analysis transcript — ffmpeg @ 37d5cb84e8ab — anthropic:claude-haiku-5-5

- target: `ff_vk_exec_get` (libavutil/vulkan.c), arity 1->2
- truth: [['libavcodec/vulkan_decode.c', 'ff_vk_decode_flush'], ['libavcodec/vulkan_decode.c', 'ff_vk_decode_frame'], ['libavcodec/vulkan_encode.c', 'vulkan_encode_issue'], ['libavfilter/vf_nlmeans_vulkan.c', 'nlmeans_vulkan_filter_frame'], ['libavfilter/vulkan_filter.c', 'ff_vk_filter_process_2pass'], ['libavfilter/vulkan_filter.c', 'ff_vk_filter_process_Nin'], ['libavfilter/vulkan_filter.c', 'ff_vk_filter_process_simple'], ['libavutil/hwcontext_vulkan.c', 'prepare_frame'], ['libavutil/hwcontext_vulkan.c', 'vulkan_map_from_drm_frame_sync'], ['libavutil/hwcontext_vulkan.c', 'vulkan_transfer_frame']]

## Self-navigation arm

### Turn 1  _(tok 1221+105, stop=tool_use)_

**Reasoning:** I'll search the repo for references to ff_vk_exec_get to see where it's used.



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

### Turn 2  _(tok 2132+1544, stop=tool_use)_

**Reasoning:** I need to refine my search to match the exact function name boundary, since the broader pattern was also catching ff_vk_exec_get_query. Filtering for exact matches turns up calls in vulkan_decode.c, vulkan_encode.c, vf_nlmeans_vulkan.c, vulkan_filter.c, and hwcontext_vulkan.c.

Now I should check each call site's surrounding code to identify the enclosing function names.



**Says:** The grep matched 16 lines, including `ff_vk_exec_get_query` (a different function) and the definition and prototype. I need the enclosing function for each real call site.

- `read_file(path=libavcodec/vulkan_decode.c, version=old, start_line=280, end_line=350)` →

```
libavcodec/vulkan_decode.c lines 280-350 of 1249
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
  301|     vk->CmdBeginVideoCodingKHR(cmd_buf, &decode_start);
  302|     vk->CmdControlVideoCodingKHR(cmd_buf, &decode_ctrl);
  303|     vk->CmdEndVideoCodingKHR(cmd_buf, &decode_end);
  304|     ff_vk_exec_submit(&ctx->s, exec);
  305| 
  306|     /* If this is the very first time this context is used, then remove the
  307|      * had_submission flag to indicate that no query result is available,
  308|      * as no decode command was issued. */
  309|     exec->had_submission = had_submission;
  310| }
  311| 
  312| int ff_vk_decode_frame(AVCodecContext *avctx,
  313|                        AVFrame *pic,    FFVulkanDecodePicture *vp,
  314|                        AVFrame *rpic[], FFVulkanDecodePicture *rvkp[])
  315| {
  316|     int err;
  317|     VkResult ret;
  318|     VkCommandBuffer cmd_buf;
  319|     FFVkBuffer *sd_buf;
  320| 
  321|     FFVulkanDecodeContext *dec = avctx->internal->hwaccel_priv_data;
  322|     FFVulkanDecodeShared *ctx = dec->shared_ctx;
  323|     FFVulkanFunctions *vk = &ctx->s.vkfn;
  324| 
  325|     /* Output */
  326|     AVVkFrame *vkf = (AVVkFrame *)pic->buf[0]->data;
  327| 
  328|     /* Quirks */
  329|     const int layered_dpb = ctx->common.layered_dpb;
  330| 
  331|     VkVideoSessionParametersKHR *par = (VkVideoSessionParametersKHR *)dec->session_params->data;
  332|     VkVideoBeginCodingInfoKHR decode_start = {
  333|         .sType = VK_STRUCTURE_TYPE_VIDEO_BEGIN_CODING_INFO_KHR,
  334|         .videoSession = ctx->common.session,
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

- `read_file(path=libavfilter/vf_nlmeans_vulkan.c, version=old, start_line=815, end_line=842)` →

```
libavfilter/vf_nlmeans_vulkan.c lines 815-842 of 1123
  815|                                   VK_BUFFER_USAGE_TRANSFER_DST_BIT |
  816|                                   VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT,
  817|                                   NULL,
  818|                                   ws_total_size * 2,
  819|                                   VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT);
  820|     if (err < 0)
  821|         return err;
  822|     ws_vk = (FFVkBuffer *)ws_buf->data;
  823| 
  824|     weights_offs[0] = 0;
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

- `read_file(path=libavfilter/vulkan_filter.c, version=old, start_line=240, end_line=256)` →

```
libavfilter/vulkan_filter.c lines 240-256 of 473
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
  256|                                  VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
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

- `read_file(path=libavfilter/vulkan_filter.c, version=old, start_line=398, end_line=414)` →

```
libavfilter/vulkan_filter.c lines 398-414 of 473
  398| 
  399| int ff_vk_filter_process_Nin(FFVulkanContext *vkctx, FFVkExecPool *e,
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

- `read_file(path=libavutil/hwcontext_vulkan.c, version=old, start_line=3175, end_line=3195)` →

```
libavutil/hwcontext_vulkan.c lines 3175-3195 of 4378
 3175|                 .sType = VK_STRUCTURE_TYPE_IMPORT_SEMAPHORE_FD_INFO_KHR,
 3176|                 .handleType = VK_EXTERNAL_SEMAPHORE_HANDLE_TYPE_SYNC_FD_BIT,
 3177|                 .flags = VK_SEMAPHORE_IMPORT_TEMPORARY_BIT,
 3178|                 .semaphore = drm_sync_sem[i],
 3179|                 .fd = implicit_fd_info.fd,
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

- `read_file(path=libavutil/hwcontext_vulkan.c, version=old, start_line=4080, end_line=4103)` →

```
libavutil/hwcontext_vulkan.c lines 4080-4103 of 4378
 4080| 
 4081|     /* Setup buffers first */
 4082|     if (p->vkctx.extensions & FF_VK_EXT_EXTERNAL_HOST_MEMORY) {
 4083|         err = host_map_frame(hwfc, bufs, &nb_bufs, swf, region, upload);
 4084|         if (err >= 0)
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

### Turn 3  _(tok 9199+797, stop=tool_use)_

**Reasoning:** I still need to identify the enclosing functions for several spots in hwcontext_vulkan.c and the vulkan_decode/encode and nlmeans files, so I'm planning to grep for function definition lines in those files to locate them.



**Says:** I have the call lines. Next I need the enclosing function names for the ones not yet identified, so I'll pull the function headers from those files.

- `grep(pattern=^[A-Za-z_].*\(|^\{?$, path_glob=libavcodec/vulkan_decode.c, version=old, max_results=300)` →

```
238 matches (showing 200)
libavcodec/vulkan_decode.c:18:
libavcodec/vulkan_decode.c:26:
libavcodec/vulkan_decode.c:36:
libavcodec/vulkan_decode.c:48:
libavcodec/vulkan_decode.c:49:static const FFVulkanDecodeDescriptor *get_codecdesc(enum AVCodecID codec_id)
libavcodec/vulkan_decode.c:50:{
libavcodec/vulkan_decode.c:57:
libavcodec/vulkan_decode.c:58:static const VkVideoProfileInfoKHR *get_video_profile(FFVulkanDecodeShared *ctx, enum AVCodecID codec_id)
libavcodec/vulkan_decode.c:59:{
libavcodec/vulkan_decode.c:61:
libavcodec/vulkan_decode.c:67:
libavcodec/vulkan_decode.c:72:
libavcodec/vulkan_decode.c:76:
libavcodec/vulkan_decode.c:79:
libavcodec/vulkan_decode.c:80:int ff_vk_update_thread_context(AVCodecContext *dst, const AVCodecContext *src)
libavcodec/vulkan_decode.c:81:{
libavcodec/vulkan_decode.c:85:
libavcodec/vulkan_decode.c:88:
libavcodec/vulkan_decode.c:94:
libavcodec/vulkan_decode.c:104:
libavcodec/vulkan_decode.c:106:
libavcodec/vulkan_decode.c:112:
libavcodec/vulkan_decode.c:116:
libavcodec/vulkan_decode.c:119:
libavcodec/vulkan_decode.c:120:int ff_vk_params_invalidate(AVCodecContext *avctx, int t, const uint8_t *b, uint32_t s)
libavcodec/vulkan_decode.c:121:{
libavcodec/vulkan_decode.c:126:
libavcodec/vulkan_decode.c:127:static AVFrame *vk_get_dpb_pool(FFVulkanDecodeShared *ctx)
libavcodec/vulkan_decode.c:128:{
libavcodec/vulkan_decode.c:133:
libavcodec/vulkan_decode.c:137:
libavcodec/vulkan_decode.c:140:
libavcodec/vulkan_decode.c:141:int ff_vk_decode_prepare_frame(FFVulkanDecodeContext *dec, AVFrame *pic,
libavcodec/vulkan_decode.c:144:{
libavcodec/vulkan_decode.c:148:
libavcodec/vulkan_decode.c:150:
libavcodec/vulkan_decode.c:155:
libavcodec/vulkan_decode.c:160:
libavcodec/vulkan_decode.c:163:
libavcodec/vulkan_decode.c:170:
libavcodec/vulkan_decode.c:174:
libavcodec/vulkan_decode.c:181:
libavcodec/vulkan_decode.c:184:
libavcodec/vulkan_decode.c:188:
libavcodec/vulkan_decode.c:195:
libavcodec/vulkan_decode.c:201:
libavcodec/vulkan_decode.c:204:
libavcodec/vulkan_decode.c:205:int ff_vk_decode_add_slice(AVCodecContext *avctx, FFVulkanDecodePicture *vp,
libavcodec/vulkan_decode.c:208:{
libavcodec/vulkan_decode.c:211:
libavcodec/vulkan_decode.c:218:
libavcodec/vulkan_decode.c:222:
libavcodec/vulkan_decode.c:227:
libavcodec/vulkan_decode.c:230:
libavcodec/vulkan_decode.c:236:
libavcodec/vulkan_decode.c:239:
libavcodec/vulkan_decode.c:243:
libavcodec/vulkan_decode.c:250:
libavcodec/vulkan_decode.c:252:
libavcodec/vulkan_decode.c:258:
libavcodec/vulkan_decode.c:263:
libavcodec/vulkan_decode.c:266:
libavcodec/vulkan_decode.c:269:
libavcodec/vulkan_decode.c:272:
libavcodec/vulkan_decode.c:275:
libavcodec/vulkan_decode.c:276:void ff_vk_decode_flush(AVCodecContext *avctx)
libavcodec/vulkan_decode.c:277:{
libavcodec/vulkan_decode.c:280:
libavcodec/vulkan_decode.c:294:
libavcodec/vulkan_decode.c:300:
libavcodec/vulkan_decode.c:305:
libavcodec/vulkan_decode.c:311:
libavcodec/vulkan_decode.c:312:int ff_vk_decode_frame(AVCodecContext *avctx,
libavcodec/vulkan_decode.c:315:{
libavcodec/vulkan_decode.c:320:
libavcodec/vulkan_decode.c:324:
libavcodec/vulkan_decode.c:327:
libavcodec/vulkan_decode.c:330:
libavcodec/vulkan_decode.c:342:
libavcodec/vulkan_decode.c:347:
libavcodec/vulkan_decode.c:349:
libavcodec/vulkan_decode.c:356:
libavcodec/vulkan_decode.c:366:
libavcodec/vulkan_decode.c:372:
libavcodec/vulkan_decode.c:374:
libavcodec/vulkan_decode.c:384:
libavcodec/vulkan_decode.c:392:
libavcodec/vulkan_decode.c:396:
libavcodec/vulkan_decode.c:402:
libavcodec/vulkan_decode.c:408:
libavcodec/vulkan_decode.c:413:
libavcodec/vulkan_decode.c:419:
libavcodec/vulkan_decode.c:424:
libavcodec/vulkan_decode.c:448:
libavcodec/vulkan_decode.c:457:
libavcodec/vulkan_decode.c:460:
libavcodec/vulkan_decode.c:465:
libavcodec/vulkan_decode.c:471:
libavcodec/vulkan_decode.c:479:
libavcodec/vulkan_decode.c:482:
libavcodec/vulkan_decode.c:515:
libavcodec/vulkan_decode.c:523:
libavcodec/vulkan_decode.c:526:
libavcodec/vulkan_decode.c:530:
libavcodec/vulkan_decode.c:532:
libavcodec/vulkan_decode.c:536:
libavcodec/vulkan_decode.c:538:
libavcodec/vulkan_decode.c:542:
libavcodec/vulkan_decode.c:543:void ff_vk_decode_free_frame(AVHWDeviceContext *dev_ctx, FFVulkanDecodePicture *vp)
libavcodec/vulkan_decode.c:544:{
libavcodec/vulkan_decode.c:546:
libavcodec/vulkan_decode.c:553:
libavcodec/vulkan_decode.c:559:
libavcodec/vulkan_decode.c:562:
libavcodec/vulkan_decode.c:566:
libavcodec/vulkan_decode.c:570:
libavcodec/vulkan_decode.c:573:
libavcodec/vulkan_decode.c:574:static void free_common(FFRefStructOpaque unused, void *obj)
libavcodec/vulkan_decode.c:575:{
libavcodec/vulkan_decode.c:579:
libavcodec/vulkan_decode.c:582:
libavcodec/vulkan_decode.c:588:
libavcodec/vulkan_decode.c:590:
libavcodec/vulkan_decode.c:592:
libavcodec/vulkan_decode.c:595:
libavcodec/vulkan_decode.c:596:static int vulkan_decode_bootstrap(AVCodecContext *avctx, AVBufferRef *frames_ref)
libavcodec/vulkan_decode.c:597:{
libavcodec/vulkan_decode.c:604:
libavcodec/vulkan_decode.c:607:
libavcodec/vulkan_decode.c:612:
libavcodec/vulkan_decode.c:614:
libavcodec/vulkan_decode.c:617:
libavcodec/vulkan_decode.c:624:
libavcodec/vulkan_decode.c:630:
libavcodec/vulkan_decode.c:633:
libavcodec/vulkan_decode.c:634:static VkResult vulkan_setup_profile(AVCodecContext *avctx,
libavcodec/vulkan_decode.c:645:{
libavcodec/vulkan_decode.c:649:
libavcodec/vulkan_decode.c:653:
libavcodec/vulkan_decode.c:657:
libavcodec/vulkan_decode.c:662:
libavcodec/vulkan_decode.c:667:
libavcodec/vulkan_decode.c:684:
libavcodec/vulkan_decode.c:687:
libavcodec/vulkan_decode.c:694:
libavcodec/vulkan_decode.c:698:
libavcodec/vulkan_decode.c:704:
libavcodec/vulkan_decode.c:708:
libavcodec/vulkan_decode.c:709:static int vulkan_decode_get_profile(AVCodecContext *avctx, AVBufferRef *frames_ref,
libavcodec/vulkan_decode.c:713:{
libavcodec/vulkan_decode.c:723:
libavcodec/vulkan_decode.c:727:
libavcodec/vulkan_decode.c:730:
libavcodec/vulkan_decode.c:740:
libavcodec/vulkan_decode.c:747:
libavcodec/vulkan_decode.c:753:
libavcodec/vulkan_decode.c:759:
libavcodec/vulkan_decode.c:784:
libavcodec/vulkan_decode.c:802:
libavcodec/vulkan_decode.c:807:
libavcodec/vulkan_decode.c:849:
libavcodec/vulkan_decode.c:856:
libavcodec/vulkan_decode.c:860:
libavcodec/vulkan_decode.c:877:
libavcodec/vulkan_decode.c:881:
libavcodec/vulkan_decode.c:889:
libavcodec/vulkan_decode.c:894:
libavcodec/vulkan_decode.c:907:
libavcodec/vulkan_decode.c:911:
libavcodec/vulkan_decode.c:914:
libavcodec/vulkan_decode.c:928:
libavcodec/vulkan_decode.c:933:
libavcodec/vulkan_decode.c:941:
libavcodec/vulkan_decode.c:945:
libavcodec/vulkan_decode.c:950:
libavcodec/vulkan_decode.c:952:
libavcodec/vulkan_decode.c:960:
libavcodec/vulkan_decode.c:963:
libavcodec/vulkan_decode.c:965:
libavcodec/vulkan_decode.c:968:
libavcodec/vulkan_decode.c:969:static void free_profile_data(AVHWFramesContext *hwfc)
libavcodec/vulkan_decode.c:970:{
libavcodec/vulkan_decode.c:973:
libavcodec/vulkan_decode.c:974:int ff_vk_frame_params(AVCodecContext *avctx, AVBufferRef *hw_frames_ctx)
libavcodec/vulkan_decode.c:975:{
libavcodec/vulkan_decode.c:983:
libavcodec/vulkan_decode.c:985:
libavcodec/vulkan_decode.c:989:
libavcodec/vulkan_decode.c:993:
libavcodec/vulkan_decode.c:1001:
libavcodec/vulkan_decode.c:1004:
libavcodec/vulkan_decode.c:1008:
libavcodec/vulkan_decode.c:1015:
libavcodec/vulkan_decode.c:1018:
libavcodec/vulkan_decode.c:1023:
libavcodec/vulkan_decode.c:1026:
libavcodec/vulkan_decode.c:1027:static void vk_decode_free_params(void *opaque, uint8_t *data)
libavcodec/vulkan_decode.c:1028:{
libavcodec/vulkan_decode.c:1036:
libavcodec/vulkan_decode.c:1037:int ff_vk_decode_create_params(AVBufferRef **par_ref, void *logctx, FFVulkanDecodeShared *ctx,
```

- `grep(pattern=^[A-Za-z_].*\(, path_glob=libavcodec/vulkan_encode.c, version=old, max_results=300)` →

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

- `grep(pattern=^[A-Za-z_].*\(, path_glob=libavfilter/vf_nlmeans_vulkan.c, version=old, max_results=300)` →

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

- `grep(pattern=^[A-Za-z_].*\(, path_glob=libavutil/hwcontext_vulkan.c, version=old, max_results=300)` →

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

### Turn 4  _(tok 19764+1442, stop=tool_use)_

**Reasoning:** I'm mapping each flagged line number to its enclosing function across the codebase—confirming vulkan_decode's flush and frame functions, vulkan_encode's issue function, and now checking vf_nlmeans for the same.

I continue tracing other files: nlmeans_vulkan's filter_frame, vulkan_filter's process variants, and hwcontext_vulkan's prepare_frame, map_from_drm_frame_sync, and transfer_frame functions, verifying each call site falls within the right boundaries. I'm also confirming the git grep search covered all tracked files so I'm not missing any call sites, then tallying up the total count of functions and call sites found.



**Says:** I found 10 call sites across 4 files and resolved each one's enclosing function from the function headers. The grep matched `ff_vk_exec_get` as a substring, so I excluded `ff_vk_exec_get_query` (a different function), the definition in `vulkan.c`, and the prototype in `vulkan.h`.

- **submit_callers** → `{"callers": [{"function": "ff_vk_decode_flush", "file": "libavcodec/vulkan_decode.c"}, {"function": "ff_vk_decode_frame", "file": "libavcodec/vulkan_decode.c"}, {"function": "vulkan_encode_issue", "file": "libavcodec/vulkan_encode.c"}, {"function": "nlmeans_vulkan_filter_frame", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "ff_vk_filter_process_simple", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_2pass", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_Nin", "file": "libavfilter/vulkan_filter.c"}, {"function": "prepare_frame", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_map_from_drm_frame_sync", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_transfer_frame", "file": "libavutil/hwcontext_vulkan.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3756+236, stop=tool_use)_

**Reasoning:** I'll check the callers of ff_vk_exec_get and also grep for it directly to confirm all usages.



- `get_callers(name=ff_vk_exec_get, version=old, limit=200)` →

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

### Turn 2  _(tok 5456+744, stop=tool_use)_

**Reasoning:** The grep finds 10 call sites across vulkan_decode.c, vulkan_encode.c, vf_nlmeans, vulkan_filter, and hwcontext, which matches the callers list exactly—ff_vk_exec_get_query was just a substring match and gets excluded. Now I'm considering whether to verify the enclosing function.

I'll trust the tool's attribution that line 3193 belongs to vulkan_map_from_drm_frame_sync, and since the grep covers all textual references with no macros or function pointers to worry about, I'm confident this is complete and ready to submit.



- **submit_callers** → `{"callers": [{"function": "ff_vk_decode_flush", "file": "libavcodec/vulkan_decode.c"}, {"function": "ff_vk_decode_frame", "file": "libavcodec/vulkan_decode.c"}, {"function": "vulkan_encode_issue", "file": "libavcodec/vulkan_encode.c"}, {"function": "nlmeans_vulkan_filter_frame", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "ff_vk_filter_process_simple", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_2pass", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_Nin", "file": "libavfilter/vulkan_filter.c"}, {"function": "prepare_frame", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_map_from_drm_frame_sync", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_transfer_frame", "file": "libavutil/hwcontext_vulkan.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3208+112, stop=tool_use)_

**Reasoning:** I'll start by checking who calls ff_vk_exec_get, using a high limit to make sure I catch everything.



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

### Turn 2  _(tok 3932+275, stop=tool_use)_

**Reasoning:** I notice the "old" version seems to default to the parent of the server's commit, but the callers list I need is for the current working tree, so I should query the "work" version instead to confirm.



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

### Turn 3  _(tok 5479+662, stop=tool_use)_

**Reasoning:** It's odd that the results keep reporting "old" consistently, even when I specify rev HEAD — it seems the version might default to the parent commit rather than the given rev. I want to verify this by checking what happens for the new version instead.

Since there's no explicit version parameter and the tool only exposes rev, I'm not confident I can isolate the "work" (current) state versus the parent commit. It might be worth cross-checking the call graph with get_neighborhood on the current definition, since the indexed callers could be incomplete anyway — missing function-pointer calls or macro-based invocations.



- `get_neighborhood(name=ff_vk_exec_get, rev=HEAD)` →

```
ff_vk_exec_get — libavutil/vulkan.c:485 [function] FFVkExecContext *ff_vk_exec_get(FFVkExecPool *pool)
  reads: pool; writes: pool*; returns: return &pool->contexts[idx];

CALLEES (0):

CALLERS (8):
  ff_vk_decode_flush (libavcodec/vulkan_decode.c:296): FFVkExecContext *exec = ff_vk_exec_get(&dec->exec_pool);
  ff_vk_decode_frame (libavcodec/vulkan_decode.c:348): FFVkExecContext *exec = ff_vk_exec_get(&dec->exec_pool);
  vulkan_encode_issue (libavcodec/vulkan_encode.c:342): exec = vp->exec = ff_vk_exec_get(&ctx->enc_pool);
  nlmeans_vulkan_filter_frame (libavfilter/vf_nlmeans_vulkan.c:839): exec = ff_vk_exec_get(&s->e);
  ff_vk_filter_process_simple (libavfilter/vulkan_filter.c:252): FFVkExecContext *exec = ff_vk_exec_get(e);
  ff_vk_filter_process_2pass (libavfilter/vulkan_filter.c:324): FFVkExecContext *exec = ff_vk_exec_get(e);
  ff_vk_filter_process_Nin (libavfilter/vulkan_filter.c:412): FFVkExecContext *exec = ff_vk_exec_get(e);
  prepare_frame (libavutil/hwcontext_vulkan.c:2256): FFVkExecContext *exec = ff_vk_exec_get(ectx);
  ... only the first 8 of 11 reference sites were followed
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

### Turn 4  _(tok 6963+737, stop=tool_use)_

**Reasoning:** I'm counting 10 unique caller functions but 11 reference sites total, so one function likely calls it twice — maybe vulkan_map_from_drm_frame_sync or vulkan_transfer_frame has a duplicate call site.



- `get_function_source(name=vulkan_transfer_frame, rev=HEAD)` →

```
vulkan_transfer_frame (function, old version) — libavutil/hwcontext_vulkan.c:4041-4175
 4041| static int vulkan_transfer_frame(AVHWFramesContext *hwfc,
 4042|                                  AVFrame *swf, AVFrame *hwf,
 4043|                                  int upload)
 4044| {
 4045|     int err;
 4046|     VulkanFramesPriv *fp = hwfc->hwctx;
 4047|     VulkanDevicePriv *p = hwfc->device_ctx->hwctx;
 4048|     FFVulkanFunctions *vk = &p->vkctx.vkfn;
 4049| 
 4050|     int host_mapped = 0;
 4051| 
 4052|     AVVkFrame *hwf_vk = (AVVkFrame *)hwf->data[0];
 4053|     VkBufferImageCopy region[AV_NUM_DATA_POINTERS]; // always one per plane
 4054| 
 4055|     const int planes = av_pix_fmt_count_planes(swf->format);
 4056|     const AVPixFmtDescriptor *desc = av_pix_fmt_desc_get(swf->format);
 4057|     const int nb_images = ff_vk_count_images(hwf_vk);
 4058|     static const VkImageAspectFlags plane_aspect[] = { VK_IMAGE_ASPECT_COLOR_BIT,
 4059|                                                        VK_IMAGE_ASPECT_PLANE_0_BIT,
 4060|                                                        VK_IMAGE_ASPECT_PLANE_1_BIT,
 4061|                                                        VK_IMAGE_ASPECT_PLANE_2_BIT, };
 4062| 
 4063|     VkImageMemoryBarrier2 img_bar[AV_NUM_DATA_POINTERS];
 4064|     int nb_img_bar = 0;
 4065| 
 4066|     AVBufferRef *bufs[AV_NUM_DATA_POINTERS];
 4067|     int nb_bufs = 0;
 4068| 
 4069|     VkCommandBuffer cmd_buf;
 4070|     FFVkExecContext *exec;
 4071| 
 4072|     /* Sanity checking */
 4073|     if ((swf->format != AV_PIX_FMT_NONE && !av_vkfmt_from_pixfmt(swf->format))) {
 4074|         av_log(hwfc, AV_LOG_ERROR, "Unsupported software frame pixel format!\n");
 4075|         return AVERROR(EINVAL);
 4076|     }
 4077| 
 4078|     if (swf->width > hwfc->width || swf->height > hwfc->height)
 4079|         return AVERROR(EINVAL);
 4080| 
 4081|     /* Setup buffers first */
 4082|     if (p->vkctx.extensions & FF_VK_EXT_EXTERNAL_HOST_MEMORY) {
 4083|         err = host_map_frame(hwfc, bufs, &nb_bufs, swf, region, upload);
 4084|         if (err >= 0)
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
 4104|     ff_vk_exec_start(&p->vkctx, exec);
 4105| 
 4106|     /* Prep destination Vulkan frame */
 4107|     err = ff_vk_exec_add_dep_frame(&p->vkctx, exec, hwf,
 4108|                                    VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
 4109|                                    VK_PIPELINE_STAGE_2_TRANSFER_BIT);
 4110|     if (err < 0)
 4111|         goto end;
 4112| 
 4113|     /* No need to declare buf deps for synchronous transfers */
 4114|     if (upload) {
 4115|         err = ff_vk_exec_add_dep_buf(&p->vkctx, exec, bufs, nb_bufs, 1);
 4116|         if (err < 0) {
 4117|             ff_vk_exec_discard_deps(&p->vkctx, exec);
 4118|             goto end;
 4119|         }
 4120|     }
 4121| 
 4122|     ff_vk_frame_barrier(&p->vkctx, exec, hwf, img_bar, &nb_img_bar,
 4123|                         VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
 4124|                         VK_PIPELINE_STAGE_2_TRANSFER_BIT_KHR,
 4125|                         upload ? VK_ACCESS_TRANSFER_WRITE_BIT :
 4126|                                  VK_ACCESS_TRANSFER_READ_BIT,
 4127|                         upload ? VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL :
 4128|                                  VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,
 4129|                         VK_QUEUE_FAMILY_IGNORED);
 4130| 
 4131|     vk->CmdPipelineBarrier2(cmd_buf, &(VkDependencyInfo) {
 4132|             .sType = VK_STRUCTURE_TYPE_DEPENDENCY_INFO,
 4133|             .pImageMemoryBarriers = img_bar,
 4134|             .imageMemoryBarrierCount = nb_img_bar,
 4135|     });
 4136| 
 4137|     for (int i = 0; i < planes; i++) {
 4138|         int buf_idx = FFMIN(i, (nb_bufs - 1));
 4139|         int img_idx = FFMIN(i, (nb_images - 1));
 4140|         FFVkBuffer *vkbuf = (FFVkBuffer *)bufs[buf_idx]->data;
 4141| 
 4142|         uint32_t orig_stride = region[i].bufferRowLength;
 4143|         region[i].bufferRowLength /= desc->comp[i].step;
 4144|         region[i].imageSubresource.aspectMask = plane_aspect[(planes != nb_images) +
 4145|                                                              i*(planes != nb_images)];
 4146| 
 4147|         if (upload)
 4148|             vk->CmdCopyBufferToImage(cmd_buf, vkbuf->buf,
 4149|                                      hwf_vk->img[img_idx],
 4150|                                      img_bar[img_idx].newLayout,
 4151|                                      1, &region[i]);
 4152|         else
 4153|             vk->CmdCopyImageToBuffer(cmd_buf, hwf_vk->img[img_idx],
 4154|                                      img_bar[img_idx].newLayout,
 4155|                                      vkbuf->buf,
 4156|                                      1, &region[i]);
 4157| 
 4158|         region[i].bufferRowLength = orig_stride;
 4159|     }
 4160| 
 4161|     err = ff_vk_exec_submit(&p->vkctx, exec);
 4162|     if (err < 0) {
 4163|         ff_vk_exec_discard_deps(&p->vkctx, exec);
 4164|     } else if (!upload) {
 4165|         ff_vk_exec_wait(&p->vkctx, exec);
 4166|         if (!host_mapped)
 4167|             err = copy_buffer_data(hwfc, bufs[0], swf, region, planes, 0);
 4168|     }
 4169| 
 4170| end:
 4171|     for (int i = 0; i < nb_bufs; i++)
 4172|         av_buffer_unref(&bufs[i]);
 4173| 
 4174|     return err;
 4175| }
```

- `get_function_source(name=vulkan_map_from_drm_frame_sync, rev=HEAD)` →

```
vulkan_map_from_drm_frame_sync (function, old version) — libavutil/hwcontext_vulkan.c:3117-3242
 3117| static int vulkan_map_from_drm_frame_sync(AVHWFramesContext *hwfc, AVFrame *dst,
 3118|                                           const AVFrame *src, int flags)
 3119| {
 3120|     int err;
 3121|     VkResult ret;
 3122|     AVHWDeviceContext *ctx = hwfc->device_ctx;
 3123|     VulkanDevicePriv *p = ctx->hwctx;
 3124|     VulkanFramesPriv *fp = hwfc->hwctx;
 3125|     AVVulkanDeviceContext *hwctx = &p->p;
 3126|     FFVulkanFunctions *vk = &p->vkctx.vkfn;
 3127| 
 3128|     const AVDRMFrameDescriptor *desc = (AVDRMFrameDescriptor *)src->data[0];
 3129| 
 3130| #ifdef DMA_BUF_IOCTL_EXPORT_SYNC_FILE
 3131|     if (p->vkctx.extensions & FF_VK_EXT_EXTERNAL_FD_SEM) {
 3132|         VkCommandBuffer cmd_buf;
 3133|         FFVkExecContext *exec;
 3134|         VkImageMemoryBarrier2 img_bar[AV_NUM_DATA_POINTERS];
 3135|         VkSemaphore drm_sync_sem[AV_DRM_MAX_PLANES] = { 0 };
 3136|         int nb_img_bar = 0;
 3137| 
 3138|         for (int i = 0; i < desc->nb_objects; i++) {
 3139|             VkSemaphoreTypeCreateInfo sem_type_info = {
 3140|                 .sType         = VK_STRUCTURE_TYPE_SEMAPHORE_TYPE_CREATE_INFO,
 3141|                 .semaphoreType = VK_SEMAPHORE_TYPE_BINARY,
 3142|             };
 3143|             VkSemaphoreCreateInfo sem_spawn = {
 3144|                 .sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO,
 3145|                 .pNext = &sem_type_info,
 3146|             };
 3147|             VkImportSemaphoreFdInfoKHR import_info;
 3148|             struct dma_buf_export_sync_file implicit_fd_info = {
 3149|                 .flags = DMA_BUF_SYNC_READ,
 3150|                 .fd = -1,
 3151|             };
 3152| 
 3153|             if (ioctl(desc->objects[i].fd, DMA_BUF_IOCTL_EXPORT_SYNC_FILE,
 3154|                       &implicit_fd_info)) {
 3155|                 err = AVERROR(errno);
 3156|                 av_log(hwctx, AV_LOG_ERROR, "Failed to retrieve implicit DRM sync file: %s\n",
 3157|                        av_err2str(err));
 3158|                 for (; i >= 0; i--)
 3159|                     vk->DestroySemaphore(hwctx->act_dev, drm_sync_sem[i], hwctx->alloc);
 3160|                 return err;
 3161|             }
 3162| 
 3163|             ret = vk->CreateSemaphore(hwctx->act_dev, &sem_spawn,
 3164|                                       hwctx->alloc, &drm_sync_sem[i]);
 3165|             if (ret != VK_SUCCESS) {
 3166|                 av_log(hwctx, AV_LOG_ERROR, "Failed to create semaphore: %s\n",
 3167|                        ff_vk_ret2str(ret));
 3168|                 err = AVERROR_EXTERNAL;
 3169|                 for (; i >= 0; i--)
 3170|                     vk->DestroySemaphore(hwctx->act_dev, drm_sync_sem[i], hwctx->alloc);
 3171|                 return err;
 3172|             }
 3173| 
 3174|             import_info = (VkImportSemaphoreFdInfoKHR) {
 3175|                 .sType = VK_STRUCTURE_TYPE_IMPORT_SEMAPHORE_FD_INFO_KHR,
 3176|                 .handleType = VK_EXTERNAL_SEMAPHORE_HANDLE_TYPE_SYNC_FD_BIT,
 3177|                 .flags = VK_SEMAPHORE_IMPORT_TEMPORARY_BIT,
 3178|                 .semaphore = drm_sync_sem[i],
 3179|                 .fd = implicit_fd_info.fd,
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
 3196|         ff_vk_exec_start(&p->vkctx, exec);
 3197| 
 3198|         /* Ownership of semaphores is passed */
 3199|         err = ff_vk_exec_add_dep_bool_sem(&p->vkctx, exec,
 3200|                                           drm_sync_sem, desc->nb_objects,
 3201|                                           VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT, 1);
 3202|         if (err < 0)
 3203|             return err;
 3204| 
 3205|         err = ff_vk_exec_add_dep_frame(&p->vkctx, exec, dst,
 3206|                                        VK_PIPELINE_STAGE_2_NONE,
 3207|                                        VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT);
 3208|         if (err < 0)
 3209|             return err;
 3210| 
 3211|         ff_vk_frame_barrier(&p->vkctx, exec, dst, img_bar, &nb_img_bar,
 3212|                             VK_PIPELINE_STAGE_2_NONE,
 3213|                             VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
 3214|                             ((flags & AV_HWFRAME_MAP_READ) ?
 3215|                              VK_ACCESS_2_SHADER_SAMPLED_READ_BIT : 0x0) |
 3216|                             ((flags & AV_HWFRAME_MAP_WRITE) ?
 3217|                              VK_ACCESS_2_SHADER_STORAGE_WRITE_BIT : 0x0),
 3218|                             VK_IMAGE_LAYOUT_GENERAL,
 3219|                             VK_QUEUE_FAMILY_IGNORED);
 3220| 
 3221|         vk->CmdPipelineBarrier2(cmd_buf, &(VkDependencyInfo) {
 3222|                 .sType = VK_STRUCTURE_TYPE_DEPENDENCY_INFO,
 3223|                 .pImageMemoryBarriers = img_bar,
 3224|                 .imageMemoryBarrierCount = nb_img_bar,
 3225|             });
 3226| 
 3227|         err = ff_vk_exec_submit(&p->vkctx, exec);
 3228|         if (err < 0)
 3229|             return err;
 3230|     } else
 3231| #endif
 3232|     {
 3233|         AVVkFrame *f = (AVVkFrame *)dst->data[0];
 3234|         av_log(hwctx, AV_LOG_WARNING, "No support for synchronization when importing DMA-BUFs, "
 3235|                                       "image may be corrupted.\n");
 3236|         err = prepare_frame(hwfc, &fp->compute_exec, f, PREP_MODE_EXTERNAL_IMPORT);
 3237|         if (err)
 3238|             return err;
 3239|     }
 3240| 
 3241|     return 0;
 3242| }
```

- `get_function_source(name=prepare_frame, rev=HEAD)` →

```
prepare_frame (function, old version) — libavutil/hwcontext_vulkan.c:2230-2318
 2230| static int prepare_frame(AVHWFramesContext *hwfc, FFVkExecPool *ectx,
 2231|                          AVVkFrame *frame, enum PrepMode pmode)
 2232| {
 2233|     int err;
 2234|     VulkanDevicePriv *p = hwfc->device_ctx->hwctx;
 2235|     FFVulkanFunctions *vk = &p->vkctx.vkfn;
 2236|     VkImageMemoryBarrier2 img_bar[AV_NUM_DATA_POINTERS];
 2237|     int nb_img_bar = 0;
 2238| 
 2239|     uint32_t dst_qf = VK_QUEUE_FAMILY_IGNORED;
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
 2259| 
 2260|     err = ff_vk_exec_add_dep_frame(&p->vkctx, exec, &tmp_frame,
 2261|                                    VK_PIPELINE_STAGE_2_NONE,
 2262|                                    VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT);
 2263|     if (err < 0)
 2264|         return err;
 2265| 
 2266|     switch (pmode) {
 2267|     case PREP_MODE_GENERAL:
 2268|         new_layout = VK_IMAGE_LAYOUT_GENERAL;
 2269|         new_access = VK_ACCESS_TRANSFER_WRITE_BIT;
 2270|         break;
 2271|     case PREP_MODE_WRITE:
 2272|         new_layout = VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL;
 2273|         new_access = VK_ACCESS_TRANSFER_WRITE_BIT;
 2274|         break;
 2275|     case PREP_MODE_EXTERNAL_IMPORT:
 2276|         new_layout = VK_IMAGE_LAYOUT_GENERAL;
 2277|         new_access = VK_ACCESS_MEMORY_READ_BIT | VK_ACCESS_MEMORY_WRITE_BIT;
 2278|         break;
 2279|     case PREP_MODE_EXTERNAL_EXPORT:
 2280|         new_layout = VK_IMAGE_LAYOUT_GENERAL;
 2281|         new_access = VK_ACCESS_MEMORY_READ_BIT | VK_ACCESS_MEMORY_WRITE_BIT;
 2282|         dst_qf     = VK_QUEUE_FAMILY_EXTERNAL_KHR;
 2283|         src_stage  = VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT;
 2284|         break;
 2285|     case PREP_MODE_DECODING_DST:
 2286|         new_layout = VK_IMAGE_LAYOUT_VIDEO_DECODE_DST_KHR;
 2287|         new_access = VK_ACCESS_TRANSFER_WRITE_BIT;
 2288|         break;
 2289|     case PREP_MODE_DECODING_DPB:
 2290|         new_layout = VK_IMAGE_LAYOUT_VIDEO_DECODE_DPB_KHR;
 2291|         new_access = VK_ACCESS_TRANSFER_READ_BIT | VK_ACCESS_TRANSFER_WRITE_BIT;
 2292|         break;
 2293|     case PREP_MODE_ENCODING_DPB:
 2294|         new_layout = VK_IMAGE_LAYOUT_VIDEO_ENCODE_DPB_KHR;
 2295|         new_access = VK_ACCESS_TRANSFER_READ_BIT | VK_ACCESS_TRANSFER_WRITE_BIT;
 2296|         break;
 2297|     }
 2298| 
 2299|     ff_vk_frame_barrier(&p->vkctx, exec, &tmp_frame, img_bar, &nb_img_bar,
 2300|                         src_stage,
 2301|                         VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
 2302|                         new_access, new_layout, dst_qf);
 2303| 
 2304|     vk->CmdPipelineBarrier2(cmd_buf, &(VkDependencyInfo) {
 2305|             .sType = VK_STRUCTURE_TYPE_DEPENDENCY_INFO,
 2306|             .pImageMemoryBarriers = img_bar,
 2307|             .imageMemoryBarrierCount = nb_img_bar,
 2308|         });
 2309| 
 2310|     err = ff_vk_exec_submit(&p->vkctx, exec);
 2311|     if (err < 0)
 2312|         return err;
 2313| 
 2314|     /* We can do this because there are no real dependencies */
 2315|     ff_vk_exec_discard_deps(&p->vkctx, exec);
 2316| 
 2317|     return 0;
 2318| }
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 16243+475, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "ff_vk_decode_flush", "file": "libavcodec/vulkan_decode.c"}, {"function": "ff_vk_decode_frame", "file": "libavcodec/vulkan_decode.c"}, {"function": "vulkan_encode_issue", "file": "libavcodec/vulkan_encode.c"}, {"function": "nlmeans_vulkan_filter_frame", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "ff_vk_filter_process_simple", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_2pass", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_Nin", "file": "libavfilter/vulkan_filter.c"}, {"function": "prepare_frame", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_map_from_drm_frame_sync", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_transfer_frame", "file": "libavutil/hwcontext_vulkan.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

