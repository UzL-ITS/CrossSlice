# Impact-analysis transcript — ffmpeg @ 37d5cb84e8ab — openrouter:deepseek/deepseek-v4-pro

- target: `ff_vk_exec_get` (libavutil/vulkan.c), arity 1->2
- truth: [['libavcodec/vulkan_decode.c', 'ff_vk_decode_flush'], ['libavcodec/vulkan_decode.c', 'ff_vk_decode_frame'], ['libavcodec/vulkan_encode.c', 'vulkan_encode_issue'], ['libavfilter/vf_nlmeans_vulkan.c', 'nlmeans_vulkan_filter_frame'], ['libavfilter/vulkan_filter.c', 'ff_vk_filter_process_2pass'], ['libavfilter/vulkan_filter.c', 'ff_vk_filter_process_Nin'], ['libavfilter/vulkan_filter.c', 'ff_vk_filter_process_simple'], ['libavutil/hwcontext_vulkan.c', 'prepare_frame'], ['libavutil/hwcontext_vulkan.c', 'vulkan_map_from_drm_frame_sync'], ['libavutil/hwcontext_vulkan.c', 'vulkan_transfer_frame']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1108+138, stop=tool_use)_

**Reasoning:** The user wants me to find every function that calls `ff_vk_exec_get`. I need to list all call sites, i.e., the enclosing function name and its file. I'll use `find_references` to find all references to `ff_vk_exec_get`, then determine the enclosing function for each reference. Let me start by finding references.

- `find_references(name=ff_vk_exec_get, max_results=50)` →

```
11 references
ff_vk_exec_get    296 libavcodec/vulkan_decode.c     FFVkExecContext *exec = ff_vk_exec_get(&dec->exec_pool);
ff_vk_exec_get    348 libavcodec/vulkan_decode.c     FFVkExecContext *exec = ff_vk_exec_get(&dec->exec_pool);
ff_vk_exec_get    342 libavcodec/vulkan_encode.c     exec = vp->exec = ff_vk_exec_get(&ctx->enc_pool);
ff_vk_exec_get    839 libavfilter/vf_nlmeans_vulkan.c     exec = ff_vk_exec_get(&s->e);
ff_vk_exec_get    252 libavfilter/vulkan_filter.c     FFVkExecContext *exec = ff_vk_exec_get(e);
ff_vk_exec_get    324 libavfilter/vulkan_filter.c     FFVkExecContext *exec = ff_vk_exec_get(e);
ff_vk_exec_get    412 libavfilter/vulkan_filter.c     FFVkExecContext *exec = ff_vk_exec_get(e);
ff_vk_exec_get   2256 libavutil/hwcontext_vulkan.c     FFVkExecContext *exec = ff_vk_exec_get(ectx);
ff_vk_exec_get   3193 libavutil/hwcontext_vulkan.c         exec = ff_vk_exec_get(&fp->compute_exec);
ff_vk_exec_get   4101 libavutil/hwcontext_vulkan.c     exec = ff_vk_exec_get(&fp->upload_exec);
ff_vk_exec_get    390 libavutil/vulkan.h FFVkExecContext *ff_vk_exec_get(FFVkExecPool *pool);
```

### Turn 2  _(tok 1540+991, stop=tool_use)_

**Reasoning:** I have 11 references. Let me filter:

1. `libavutil/vulkan.h` line 390 - this is likely the declaration/prototype. Not a call site.
2. The rest are call sites. I need to determine the enclosing function for each.

Let me read the relevant files to find the enclosing functions. Let me start by reading around each call site.

Let me go through each:

- `libavcodec/vulkan_decode.c` line 296
- `libavcodec/vulkan_decode.c` line 348
- `libavcodec/vulkan_encode.c` line 342
- `libavfilter/vf_nlmeans_vulkan.c` line 839
- `libavfilter/vulkan_filter.c` line 252
- `libavfilter/vulkan_filter.c` line 324
- `libavfilter/vulkan_filter.c` line 412
- `libavutil/hwcontext_vulkan.c` line 2256
- `libavutil/hwcontext_vulkan.c` line 3193
- `libavutil/hwcontext_vulkan.c` line 4101

I need to find the enclosing function for each. Let me read around each line.

- `read_file(path=libavcodec/vulkan_decode.c, start_line=280, end_line=310)` →

```
libavcodec/vulkan_decode.c lines 280-310 of 1249
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
```

- `read_file(path=libavcodec/vulkan_decode.c, start_line=335, end_line=360)` →

```
libavcodec/vulkan_decode.c lines 335-360 of 1249
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
  351|     VkVideoReferenceSlotInfoKHR *cur_vk_ref;
  352|     cur_vk_ref = (void *)&decode_start.pReferenceSlots[decode_start.referenceSlotCount];
  353|     cur_vk_ref[0] = vp->ref_slot;
  354|     cur_vk_ref[0].slotIndex = -1;
  355|     decode_start.referenceSlotCount++;
  356| 
  357|     if (dec->exec_pool.nb_queries && exec->had_submission) {
  358|         uint32_t *result;
  359|         ret = ff_vk_exec_get_query(&ctx->s, exec, (void **)&result,
  360|                                    VK_QUERY_RESULT_WAIT_BIT);
```

- `read_file(path=libavcodec/vulkan_encode.c, start_line=330, end_line=355)` →

```
libavcodec/vulkan_encode.c lines 330-355 of 1060
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
  346|     /* Output packet buffer */
  347|     err = ff_vk_exec_add_dep_buf(&ctx->s, exec, &vp->pkt_buf, 1, 1);
  348|     if (err < 0)
  349|         goto fail;
  350| 
  351|     /* Source image */
  352|     err = ff_vk_exec_add_dep_frame(&ctx->s, exec, src,
  353|                                    VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
  354|                                    VK_PIPELINE_STAGE_2_VIDEO_ENCODE_BIT_KHR);
  355|     if (err < 0)
```

- `read_file(path=libavfilter/vf_nlmeans_vulkan.c, start_line=825, end_line=850)` →

```
libavfilter/vf_nlmeans_vulkan.c lines 825-850 of 1123
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
  843|     RET(ff_vk_exec_add_dep_frame(vkctx, exec, in,
  844|                                  VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
  845|                                  VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT));
  846|     RET(ff_vk_exec_add_dep_frame(vkctx, exec, out,
  847|                                  VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
  848|                                  VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT));
  849| 
  850|     RET(ff_vk_exec_add_dep_buf(vkctx, exec, &integral_buf, 1, 0));
```

- `read_file(path=libavfilter/vulkan_filter.c, start_line=240, end_line=265)` →

```
libavfilter/vulkan_filter.c lines 240-265 of 473
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
  257|                                  VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT));
  258|     RET(ff_vk_create_imageviews(vkctx, exec, out_views, out_f));
  259|     ff_vk_shader_update_img_array(vkctx, exec, shd, out_f, out_views, 0, !!in_f,
  260|                                   VK_IMAGE_LAYOUT_GENERAL,
  261|                                   VK_NULL_HANDLE);
  262|     if (in_f) {
  263|         RET(ff_vk_exec_add_dep_frame(vkctx, exec, in_f,
  264|                                      VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
  265|                                      VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT));
```

- `read_file(path=libavfilter/vulkan_filter.c, start_line=312, end_line=335)` →

```
libavfilter/vulkan_filter.c lines 312-335 of 473
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
  327|     RET(ff_vk_exec_add_dep_frame(vkctx, exec, in,
  328|                                  VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
  329|                                  VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT));
  330|     RET(ff_vk_exec_add_dep_frame(vkctx, exec, tmp,
  331|                                  VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
  332|                                  VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT));
  333|     RET(ff_vk_exec_add_dep_frame(vkctx, exec, out,
  334|                                  VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
  335|                                  VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT));
```

- `read_file(path=libavfilter/vulkan_filter.c, start_line=398, end_line=425)` →

```
libavfilter/vulkan_filter.c lines 398-425 of 473
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
  415|     /* Add deps and create temporary imageviews */
  416|     RET(ff_vk_exec_add_dep_frame(vkctx, exec, out,
  417|                                  VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
  418|                                  VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT));
  419|     RET(ff_vk_create_imageviews(vkctx, exec, out_views, out));
  420|     for (int i = 0; i < nb_in; i++) {
  421|         RET(ff_vk_exec_add_dep_frame(vkctx, exec, in[i],
  422|                                      VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT,
  423|                                      VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT));
  424|         RET(ff_vk_create_imageviews(vkctx, exec, in_views[i], in[i]));
  425|     }
```

- `read_file(path=libavutil/hwcontext_vulkan.c, start_line=2242, end_line=2270)` →

```
libavutil/hwcontext_vulkan.c lines 2242-2270 of 4378
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
```

- `read_file(path=libavutil/hwcontext_vulkan.c, start_line=3180, end_line=3205)` →

```
libavutil/hwcontext_vulkan.c lines 3180-3205 of 4378
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
```

- `read_file(path=libavutil/hwcontext_vulkan.c, start_line=4088, end_line=4115)` →

```
libavutil/hwcontext_vulkan.c lines 4088-4115 of 4378
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
```

### Turn 3  _(tok 7029+525, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing function for each reference. Let me trace backwards from each line to find the function definition.

For `libavcodec/vulkan_decode.c`:
- Line 296: Let me look backwards for the function definition.
- Line 348: Same.

For `libavcodec/vulkan_encode.c`:
- Line 342.

For `libavfilter/vf_nlmeans_vulkan.c`:
- Line 839.

For `libavfilter/vulkan_filter.c`:
- Line 252: already can see function `ff_vk_filter_process_simple` at line 240.
- Line 324: function `ff_vk_filter_process_2in` at line 312? Wait, line 312 shows `AVFrame *out, AVFrame *tmp, AVFrame *in,` - let me check what function starts around there.
- Line 412: function `ff_vk_filter_process_Nin` at line 399.

For `libavutil/hwcontext_vulkan.c`:
- Line 2256, 3193, 4101.

Let me look at the functions more carefully.

**Says:** Now let me find the enclosing function for each reference by looking backwards for function definitions:

- `grep(pattern=^(static )?[a-zA-Z_][a-zA-Z0-9_* ]+\*?\s*[a-zA-Z_][a-zA-Z0-9, path_glob=libavcodec/vulkan_decode.c, max_results=30)` →

```
20 matches
libavcodec/vulkan_decode.c:49:static const FFVulkanDecodeDescriptor *get_codecdesc(enum AVCodecID codec_id)
libavcodec/vulkan_decode.c:58:static const VkVideoProfileInfoKHR *get_video_profile(FFVulkanDecodeShared *ctx, enum AVCodecID codec_id)
libavcodec/vulkan_decode.c:80:int ff_vk_update_thread_context(AVCodecContext *dst, const AVCodecContext *src)
libavcodec/vulkan_decode.c:120:int ff_vk_params_invalidate(AVCodecContext *avctx, int t, const uint8_t *b, uint32_t s)
libavcodec/vulkan_decode.c:127:static AVFrame *vk_get_dpb_pool(FFVulkanDecodeShared *ctx)
libavcodec/vulkan_decode.c:141:int ff_vk_decode_prepare_frame(FFVulkanDecodeContext *dec, AVFrame *pic,
libavcodec/vulkan_decode.c:205:int ff_vk_decode_add_slice(AVCodecContext *avctx, FFVulkanDecodePicture *vp,
libavcodec/vulkan_decode.c:276:void ff_vk_decode_flush(AVCodecContext *avctx)
libavcodec/vulkan_decode.c:312:int ff_vk_decode_frame(AVCodecContext *avctx,
libavcodec/vulkan_decode.c:543:void ff_vk_decode_free_frame(AVHWDeviceContext *dev_ctx, FFVulkanDecodePicture *vp)
libavcodec/vulkan_decode.c:574:static void free_common(FFRefStructOpaque unused, void *obj)
libavcodec/vulkan_decode.c:596:static int vulkan_decode_bootstrap(AVCodecContext *avctx, AVBufferRef *frames_ref)
libavcodec/vulkan_decode.c:634:static VkResult vulkan_setup_profile(AVCodecContext *avctx,
libavcodec/vulkan_decode.c:709:static int vulkan_decode_get_profile(AVCodecContext *avctx, AVBufferRef *frames_ref,
libavcodec/vulkan_decode.c:969:static void free_profile_data(AVHWFramesContext *hwfc)
libavcodec/vulkan_decode.c:974:int ff_vk_frame_params(AVCodecContext *avctx, AVBufferRef *hw_frames_ctx)
libavcodec/vulkan_decode.c:1027:static void vk_decode_free_params(void *opaque, uint8_t *data)
libavcodec/vulkan_decode.c:1037:int ff_vk_decode_create_params(AVBufferRef **par_ref, void *logctx, FFVulkanDecodeShared *ctx,
libavcodec/vulkan_decode.c:1066:int ff_vk_decode_uninit(AVCodecContext *avctx)
libavcodec/vulkan_decode.c:1081:int ff_vk_decode_init(AVCodecContext *avctx)
```

- `read_file(end_line=296, path=libavcodec/vulkan_decode.c, start_line=260)` →

```
libavcodec/vulkan_decode.c lines 260-296 of 1249
  260|         vkbuf = new_buf;
  261|     }
  262|     slices = vkbuf->mapped_mem;
  263| 
  264|     /* Startcode */
  265|     memcpy(slices + vp->slices_size, startcode_prefix, startcode_len);
  266| 
  267|     /* Slice data */
  268|     memcpy(slices + vp->slices_size + startcode_len, data, size);
  269| 
  270|     *nb_slices = nb + 1;
  271|     vp->slices_size += startcode_len + size;
  272| 
  273|     return 0;
  274| }
  275| 
  276| void ff_vk_decode_flush(AVCodecContext *avctx)
  277| {
  278|     FFVulkanDecodeContext *dec = avctx->internal->hwaccel_priv_data;
  279|     FFVulkanDecodeShared *ctx = dec->shared_ctx;
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
```

- `read_file(end_line=348, path=libavcodec/vulkan_decode.c, start_line=315)` →

```
libavcodec/vulkan_decode.c lines 315-348 of 1249
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
```

### Turn 4  _(tok 9260+111, stop=tool_use)_

**Reasoning:** Line 315 is the open brace of the function. Let me look at line 312-314 for the function signature.

- `read_file(end_line=315, path=libavcodec/vulkan_decode.c, start_line=310)` →

```
libavcodec/vulkan_decode.c lines 310-315 of 1249
  310| }
  311| 
  312| int ff_vk_decode_frame(AVCodecContext *avctx,
  313|                        AVFrame *pic,    FFVulkanDecodePicture *vp,
  314|                        AVFrame *rpic[], FFVulkanDecodePicture *rvkp[])
  315| {
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 9489+921, stop=tool_use, forced)_

**Reasoning:** Let me compile what I've gathered so far:

1. `libavcodec/vulkan_decode.c` line 296 - function `ff_vk_decode_flush` (line 276)
2. `libavcodec/vulkan_decode.c` line 348 - function `ff_vk_decode_frame` (line 312)
3. `libavcodec/vulkan_encode.c` line 342 - I need to find the enclosing function
4. `libavfilter/vf_nlmeans_vulkan.c` line 839 - I need to find the enclosing function
5. `libavfilter/vulkan_filter.c` line 252 - function `ff_vk_filter_process_simple` (line 240)
6. `libavfilter/vulkan_filter.c` line 324 - need to check the function
7. `libavfilter/vulkan_filter.c` line 412 - function `ff_vk_filter_process_Nin` (line 399)
8. `libavutil/hwcontext_vulkan.c` line 2256 - need to find the function
9. `libavutil/hwcontext_vulkan.c` line 3193 - need to find the function
10. `libavutil/hwcontext_vulkan.c` line 4101 - need to find the function

Let me try to confirm the remaining ones.

For vulkan_filter.c line 324: looking at line 312, the function appears to be `ff_vk_filter_process_2in`. Let me check.

For vulkan_encode.c line 342: I saw line 330 `encode_info.dstBufferRange -= data_size;` and line 342 in `ff_vk_exec_get`. Let me look backwards.

For vf_nlmeans_vulkan.c line 839: Let me check.

For hwcontext_vulkan.c lines 2256, 3193, 4101.

I have limited context. Let me try to finalize.

From what I saw:
- vulkan_filter.c line 312-314: `AVFrame *out, AVFrame *tmp, AVFrame *in,` (line 314), the function starts before this. Looking at the function signature pattern, line 310 likely has something like `int ff_vk_filter_process_2in(FFVulkanContext *vkctx, FFVkExecPool *e, FFVulkanShader *shd,` based on the other similar functions.

For vulkan_encode.c, let me check the function around line 342.

For hwcontext_vulkan.c, line 2256 is in some function that starts earlier. Let me look at the patterns.

I think I should try to get more data. But I'm running out of time. Let me use grep to find function definitions more precisely, or read the files.

Actually, let me just try to find the function for vulkan_encode.c line 342 quickly.

- **submit_callers** → `{"callers": [{"function": "ff_vk_decode_flush", "file": "libavcodec/vulkan_decode.c"}, {"function": "ff_vk_decode_frame", "file": "libavcodec/vulkan_decode.c"}, {"function": "ff_vk_encode_video_frame", "file": "libavcodec/vulkan_encode.c"}, {"function": "nlmeans_vulkan_filter_frame", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "ff_vk_filter_process_simple", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_2in", "file": "libavfilter/vulkan_filter.c"}, {"function": "ff_vk_filter_process_Nin", "file": "libavfilter/vulkan_filter.c"}, {"function": "vk_prepare_frame", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_transfer_from_drm", "file": "libavutil/hwcontext_vulkan.c"}, {"function": "vulkan_transfer_to_vulkan", "file": "libavutil/hwcontext_vulkan.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 10, "n_truth": 10, "tp": 5, "precision": 0.5, "recall": 0.5, "f1": 0.5}`

