# Impact-analysis transcript — ffmpeg @ 0a37d5a3b1fb — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_vk_shader_init` (libavutil/vulkan.c), arity 5->10
- truth: [['libavfilter/vf_avgblur_vulkan.c', 'init_filter'], ['libavfilter/vf_blend_vulkan.c', 'init_filter'], ['libavfilter/vf_bwdif_vulkan.c', 'init_filter'], ['libavfilter/vf_chromaber_vulkan.c', 'init_filter'], ['libavfilter/vf_flip_vulkan.c', 'init_filter'], ['libavfilter/vf_gblur_vulkan.c', 'init_filter'], ['libavfilter/vf_nlmeans_vulkan.c', 'init_denoise_pipeline'], ['libavfilter/vf_nlmeans_vulkan.c', 'init_weights_pipeline'], ['libavfilter/vf_overlay_vulkan.c', 'init_filter'], ['libavfilter/vf_scale_vulkan.c', 'init_filter'], ['libavfilter/vf_transpose_vulkan.c', 'init_filter'], ['libavfilter/vf_xfade_vulkan.c', 'init_vulkan'], ['libavfilter/vsrc_testsrc_vulkan.c', 'init_filter']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1034+111, stop=tool_use)_

**Reasoning:** I need to investigate this further. Let me check the details.

Let's find all references to `ff_vk_shader_init`.

- `find_references(name=ff_vk_shader_init)` →

```
15 references
ff_vk_shader_init   84 libavfilter/vf_avgblur_vulkan.c     RET(ff_vk_shader_init(&s->pl, &s->shd, "avgblur_compute",
ff_vk_shader_init  148 libavfilter/vf_blend_vulkan.c     RET(ff_vk_shader_init(&s->pl, &s->shd, "blend_compute",
ff_vk_shader_init  116 libavfilter/vf_bwdif_vulkan.c     RET(ff_vk_shader_init(&s->pl, &s->shd, "bwdif_compute",
ff_vk_shader_init   95 libavfilter/vf_chromaber_vulkan.c     RET(ff_vk_shader_init(&s->pl, &s->shd, "chromaber_compute",
ff_vk_shader_init   69 libavfilter/vf_flip_vulkan.c     RET(ff_vk_shader_init(&s->pl, &s->shd, "flip_compute",
ff_vk_shader_init  222 libavfilter/vf_gblur_vulkan.c     RET(ff_vk_shader_init(&s->pl_hor, &s->shd_hor, "gblur_hor_compute",
ff_vk_shader_init  224 libavfilter/vf_gblur_vulkan.c     RET(ff_vk_shader_init(&s->pl_ver, &s->shd_ver, "gblur_ver_compute",
ff_vk_shader_init  244 libavfilter/vf_nlmeans_vulkan.c     RET(ff_vk_shader_init(pl, shd, "nlmeans_weights", VK_SHADER_STAGE_COMPUTE_BIT, 0));
ff_vk_shader_init  431 libavfilter/vf_nlmeans_vulkan.c     RET(ff_vk_shader_init(pl, shd, "nlmeans_denoise",
ff_vk_shader_init  108 libavfilter/vf_overlay_vulkan.c     RET(ff_vk_shader_init(&s->pl, &s->shd, "overlay_compute",
ff_vk_shader_init  149 libavfilter/vf_scale_vulkan.c     RET(ff_vk_shader_init(&s->pl, &s->shd, "scale_compute",
ff_vk_shader_init   68 libavfilter/vf_transpose_vulkan.c     RET(ff_vk_shader_init(&s->pl, &s->shd, "transpose_compute",
ff_vk_shader_init  342 libavfilter/vf_xfade_vulkan.c     RET(ff_vk_shader_init(&s->pl, &s->shd, "xfade_compute",
ff_vk_shader_init   88 libavfilter/vsrc_testsrc_vulkan.c     RET(ff_vk_shader_init(&s->pl, &s->shd, "testsrc_compute",
ff_vk_shader_init  477 libavutil/vulkan.h int ff_vk_shader_init(FFVulkanPipeline *pl, FFVkSPIRVShader *shd, const char *name,
```

- `grep(pattern=ff_vk_shader_init, version=old, max_results=100)` →

```
16 matches
libavfilter/vf_avgblur_vulkan.c:84:    RET(ff_vk_shader_init(&s->pl, &s->shd, "avgblur_compute",
libavfilter/vf_blend_vulkan.c:148:    RET(ff_vk_shader_init(&s->pl, &s->shd, "blend_compute",
libavfilter/vf_bwdif_vulkan.c:116:    RET(ff_vk_shader_init(&s->pl, &s->shd, "bwdif_compute",
libavfilter/vf_chromaber_vulkan.c:95:    RET(ff_vk_shader_init(&s->pl, &s->shd, "chromaber_compute",
libavfilter/vf_flip_vulkan.c:69:    RET(ff_vk_shader_init(&s->pl, &s->shd, "flip_compute",
libavfilter/vf_gblur_vulkan.c:222:    RET(ff_vk_shader_init(&s->pl_hor, &s->shd_hor, "gblur_hor_compute",
libavfilter/vf_gblur_vulkan.c:224:    RET(ff_vk_shader_init(&s->pl_ver, &s->shd_ver, "gblur_ver_compute",
libavfilter/vf_nlmeans_vulkan.c:244:    RET(ff_vk_shader_init(pl, shd, "nlmeans_weights", VK_SHADER_STAGE_COMPUTE_BIT, 0));
libavfilter/vf_nlmeans_vulkan.c:431:    RET(ff_vk_shader_init(pl, shd, "nlmeans_denoise",
libavfilter/vf_overlay_vulkan.c:108:    RET(ff_vk_shader_init(&s->pl, &s->shd, "overlay_compute",
libavfilter/vf_scale_vulkan.c:149:    RET(ff_vk_shader_init(&s->pl, &s->shd, "scale_compute",
libavfilter/vf_transpose_vulkan.c:68:    RET(ff_vk_shader_init(&s->pl, &s->shd, "transpose_compute",
libavfilter/vf_xfade_vulkan.c:342:    RET(ff_vk_shader_init(&s->pl, &s->shd, "xfade_compute",
libavfilter/vsrc_testsrc_vulkan.c:88:    RET(ff_vk_shader_init(&s->pl, &s->shd, "testsrc_compute",
libavutil/vulkan.c:1400:int ff_vk_shader_init(FFVulkanPipeline *pl, FFVkSPIRVShader *shd, const char *name,
libavutil/vulkan.h:477:int ff_vk_shader_init(FFVulkanPipeline *pl, FFVkSPIRVShader *shd, const char *name,
```

### Turn 2  _(tok 2452+334, stop=tool_use)_

**Reasoning:** Now I need to determine the enclosing function for each call site. Let me read the relevant areas.

Let's read each file around the lines. I'll do multiple parallel reads.


- `read_file(path=libavfilter/vf_avgblur_vulkan.c, start_line=50, end_line=110, version=old)` →

```
libavfilter/vf_avgblur_vulkan.c lines 50-110 of 260
   50| static const char blur_kernel[] = {
   51|     C(0, void distort(const ivec2 pos, const int idx)                         )
   52|     C(0, {                                                                    )
   53|     C(1,     vec4 sum = vec4(0);                                              )
   54|     C(1,     for (int y = -filter_len.y; y <= filter_len.y; y++)              )
   55|     C(1,        for (int x = -filter_len.x; x <= filter_len.x; x++)           )
   56|     C(2,            sum += texture(input_img[idx], pos + ivec2(x, y));        )
   57|     C(0,                                                                      )
   58|     C(1,     imageStore(output_img[idx], pos, sum * filter_norm);             )
   59|     C(0, }                                                                    )
   60| };
   61| 
   62| static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
   63| {
   64|     int err;
   65|     uint8_t *spv_data;
   66|     size_t spv_len;
   67|     void *spv_opaque = NULL;
   68|     AvgBlurVulkanContext *s = ctx->priv;
   69|     FFVulkanContext *vkctx = &s->vkctx;
   70|     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   71|     FFVkSPIRVShader *shd;
   72|     FFVkSPIRVCompiler *spv;
   73|     FFVulkanDescriptorSetBinding *desc;
   74| 
   75|     spv = ff_vk_spirv_init();
   76|     if (!spv) {
   77|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
   78|         return AVERROR_EXTERNAL;
   79|     }
   80| 
   81|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
   82|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
   83|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_LINEAR));
   84|     RET(ff_vk_shader_init(&s->pl, &s->shd, "avgblur_compute",
   85|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
   86|     shd = &s->shd;
   87| 
   88|     ff_vk_shader_set_compute_sizes(shd, 32, 1, 1);
   89| 
   90|     desc = (FFVulkanDescriptorSetBinding []) {
   91|         {
   92|             .name       = "input_img",
   93|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
   94|             .dimensions = 2,
   95|             .elems      = planes,
   96|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
   97|             .samplers   = DUP_SAMPLER(s->sampler),
   98|         },
   99|         {
  100|             .name       = "output_img",
  101|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  102|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  103|             .mem_quali  = "writeonly",
  104|             .dimensions = 2,
  105|             .elems      = planes,
  106|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  107|         },
  108|     };
  109| 
  110|     RET(ff_vk_pipeline_descriptor_set_add(vkctx, &s->pl, shd, desc, 2, 0, 0));
```

- `read_file(path=libavfilter/vf_blend_vulkan.c, start_line=110, end_line=165, version=old)` →

```
libavfilter/vf_blend_vulkan.c lines 110-165 of 401
  110|         }
  111|     }
  112| 
  113|     return 0;
  114| }
  115| 
  116| static int process_command(AVFilterContext *ctx, const char *cmd, const char *args,
  117|                            char *res, int res_len, int flags)
  118| {
  119|     int ret = ff_filter_process_command(ctx, cmd, args, res, res_len, flags);
  120|     if (ret < 0)
  121|         return ret;
  122| 
  123|     return config_params(ctx);
  124| }
  125| 
  126| static av_cold int init_filter(AVFilterContext *avctx)
  127| {
  128|     int err = 0;
  129|     uint8_t *spv_data;
  130|     size_t spv_len;
  131|     void *spv_opaque = NULL;
  132|     BlendVulkanContext *s = avctx->priv;
  133|     FFVulkanContext *vkctx = &s->vkctx;
  134|     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
  135|     FFVkSPIRVShader *shd = &s->shd;
  136|     FFVkSPIRVCompiler *spv;
  137|     FFVulkanDescriptorSetBinding *desc;
  138| 
  139|     spv = ff_vk_spirv_init();
  140|     if (!spv) {
  141|         av_log(avctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
  142|         return AVERROR_EXTERNAL;
  143|     }
  144| 
  145|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
  146|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
  147|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_NEAREST));
  148|     RET(ff_vk_shader_init(&s->pl, &s->shd, "blend_compute",
  149|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
  150| 
  151|     ff_vk_shader_set_compute_sizes(&s->shd, 32, 32, 1);
  152| 
  153|     desc = (FFVulkanDescriptorSetBinding []) {
  154|         {
  155|             .name       = "top_images",
  156|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  157|             .dimensions = 2,
  158|             .elems      = planes,
  159|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  160|             .samplers   = DUP_SAMPLER(s->sampler),
  161|         },
  162|         {
  163|             .name       = "bottom_images",
  164|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  165|             .dimensions = 2,
```

- `read_file(path=libavfilter/vf_bwdif_vulkan.c, start_line=90, end_line=130, version=old)` →

```
libavfilter/vf_bwdif_vulkan.c lines 90-130 of 416
   90|     C(1,     return mix(interpol, fd, diff_mask);                                                     )
   91|     C(0, }                                                                                            )
   92| };
   93| 
   94| static av_cold int init_filter(AVFilterContext *ctx)
   95| {
   96|     int err;
   97|     uint8_t *spv_data;
   98|     size_t spv_len;
   99|     void *spv_opaque = NULL;
  100|     BWDIFVulkanContext *s = ctx->priv;
  101|     FFVulkanContext *vkctx = &s->vkctx;
  102|     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
  103|     FFVkSPIRVShader *shd;
  104|     FFVkSPIRVCompiler *spv;
  105|     FFVulkanDescriptorSetBinding *desc;
  106| 
  107|     spv = ff_vk_spirv_init();
  108|     if (!spv) {
  109|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
  110|         return AVERROR_EXTERNAL;
  111|     }
  112| 
  113|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
  114|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
  115|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_NEAREST));
  116|     RET(ff_vk_shader_init(&s->pl, &s->shd, "bwdif_compute",
  117|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
  118|     shd = &s->shd;
  119| 
  120|     ff_vk_shader_set_compute_sizes(shd, 1, 64, 1);
  121| 
  122|     desc = (FFVulkanDescriptorSetBinding []) {
  123|         {
  124|             .name       = "prev",
  125|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  126|             .dimensions = 2,
  127|             .elems      = planes,
  128|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  129|             .samplers   = DUP_SAMPLER(s->sampler),
  130|         },
```

- `read_file(path=libavfilter/vf_chromaber_vulkan.c, start_line=70, end_line=110, version=old)` →

```
libavfilter/vf_chromaber_vulkan.c lines 70-110 of 261
   70| {
   71|     int err;
   72|     uint8_t *spv_data;
   73|     size_t spv_len;
   74|     void *spv_opaque = NULL;
   75|     ChromaticAberrationVulkanContext *s = ctx->priv;
   76|     FFVulkanContext *vkctx = &s->vkctx;
   77|     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   78|     FFVkSPIRVShader *shd = &s->shd;
   79|     FFVkSPIRVCompiler *spv;
   80|     FFVulkanDescriptorSetBinding *desc;
   81| 
   82|     /* Normalize options */
   83|     s->opts.dist[0] = (s->opts.dist[0] / 100.0f) + 1.0f;
   84|     s->opts.dist[1] = (s->opts.dist[1] / 100.0f) + 1.0f;
   85| 
   86|     spv = ff_vk_spirv_init();
   87|     if (!spv) {
   88|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
   89|         return AVERROR_EXTERNAL;
   90|     }
   91| 
   92|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
   93|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
   94|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 0, VK_FILTER_LINEAR));
   95|     RET(ff_vk_shader_init(&s->pl, &s->shd, "chromaber_compute",
   96|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
   97| 
   98|     ff_vk_shader_set_compute_sizes(&s->shd, 32, 32, 1);
   99| 
  100|     GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
  101|     GLSLC(1,    vec2 dist;                                                );
  102|     GLSLC(0, };                                                           );
  103|     GLSLC(0,                                                              );
  104| 
  105|     ff_vk_add_push_constant(&s->pl, 0, sizeof(s->opts),
  106|                              VK_SHADER_STAGE_COMPUTE_BIT);
  107| 
  108|     desc = (FFVulkanDescriptorSetBinding []) {
  109|         {
  110|             .name       = "input_img",
```

### Turn 3  _(tok 6352+98, stop=tool_use)_

**Reasoning:** Need to see line 66-70 for function name.

Let me read a bit above.


- `read_file(path=libavfilter/vf_chromaber_vulkan.c, start_line=60, end_line=72, version=old)` →

```
libavfilter/vf_chromaber_vulkan.c lines 60-72 of 261
   60|     C(0, {                                                                     )
   61|     C(1,     vec2 p = ((vec2(pos)/vec2(size)) - 0.5f)*2.0f;                    )
   62|     C(1,     float d = sqrt(p.x*p.x + p.y*p.y);                                )
   63|     C(1,     p *= d / (d*dist);                                                )
   64|     C(1,     vec4 res = texture(input_img[idx], (p/2.0f) + 0.5f);              )
   65|     C(1,     imageStore(output_img[idx], pos, res);                            )
   66|     C(0, }                                                                     )
   67| };
   68| 
   69| static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
   70| {
   71|     int err;
   72|     uint8_t *spv_data;
```

### Turn 4  _(tok 6738+180, stop=tool_use)_

**Reasoning:** Now vf_flip_vulkan.c line 69, vf_gblur_vulkan.c lines 222, 224, vf_nlmeans_vulkan.c lines 244 and 431, vf_overlay_vulkan.c line 108, vf_scale_vulkan.c 149, vf_transpose_vulkan.c 68, vf_xfade_vulkan.c 342, vsrc_testsrc_vulkan.c 88.

Let me read each in parallel.


- `read_file(path=libavfilter/vf_flip_vulkan.c, start_line=40, end_line=80, version=old)` →

```
libavfilter/vf_flip_vulkan.c lines 40-80 of 301
   40|     FFVulkanPipeline pl;
   41|     FFVkExecPool e;
   42|     FFVkQueueFamilyCtx qf;
   43|     FFVkSPIRVShader shd;
   44|     VkSampler sampler;
   45| } FlipVulkanContext;
   46| 
   47| static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in, enum FlipType type)
   48| {
   49|     int err = 0;
   50|     uint8_t *spv_data;
   51|     size_t spv_len;
   52|     void *spv_opaque = NULL;
   53|     FlipVulkanContext *s = ctx->priv;
   54|     FFVulkanContext *vkctx = &s->vkctx;
   55|     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   56|     FFVkSPIRVShader *shd = &s->shd;
   57|     FFVkSPIRVCompiler *spv;
   58|     FFVulkanDescriptorSetBinding *desc;
   59| 
   60|     spv = ff_vk_spirv_init();
   61|     if (!spv) {
   62|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
   63|         return AVERROR_EXTERNAL;
   64|     }
   65| 
   66|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
   67|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
   68|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_LINEAR));
   69|     RET(ff_vk_shader_init(&s->pl, &s->shd, "flip_compute",
   70|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
   71| 
   72|     ff_vk_shader_set_compute_sizes(&s->shd, 32, 32, 1);
   73| 
   74|     desc = (FFVulkanDescriptorSetBinding []) {
   75|         {
   76|             .name       = "input_image",
   77|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
   78|             .dimensions = 2,
   79|             .elems      = planes,
   80|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
```

### Turn 5  _(tok 7635+135, stop=tool_use)_

**Reasoning:** Note vf_flip_vulkan.c has init_filter which may be called from hflip_init and vflip_init. But the caller of ff_vk_shader_init is init_filter only. The task asks: list every function that calls ff_vk_shader_init. So init_filter.

Now gblur.


- `read_file(path=libavfilter/vf_gblur_vulkan.c, start_line=180, end_line=240, version=old)` →

```
libavfilter/vf_gblur_vulkan.c lines 180-240 of 387
  180| 
  181|     RET(ff_vk_create_buf(&s->vkctx, params_buf, sizeof(float) * ksize, NULL, NULL,
  182|                          VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT |
  183|                          VK_BUFFER_USAGE_STORAGE_BUFFER_BIT,
  184|                          VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT));
  185|     RET(ff_vk_map_buffer(&s->vkctx, params_buf, &kernel_mapped, 0));
  186| 
  187|     init_gaussian_kernel((float *)kernel_mapped, sigma, ksize);
  188| 
  189|     RET(ff_vk_unmap_buffer(&s->vkctx, params_buf, 1));
  190| 
  191|     RET(ff_vk_set_descriptor_buffer(&s->vkctx, pl, NULL, 1, 0, 0,
  192|                                     params_buf, 0, params_buf->size,
  193|                                     VK_FORMAT_UNDEFINED));
  194| 
  195| fail:
  196|     av_free(kernel_def);
  197|     if (spv_opaque)
  198|         spv->free_shader(spv, &spv_opaque);
  199|     return err;
  200| }
  201| 
  202| static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
  203| {
  204|     int err = 0;
  205|     GBlurVulkanContext *s = ctx->priv;
  206|     FFVulkanContext *vkctx = &s->vkctx;
  207|     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
  208| 
  209|     FFVkSPIRVShader *shd;
  210|     FFVkSPIRVCompiler *spv;
  211|     FFVulkanDescriptorSetBinding *desc;
  212| 
  213|     spv = ff_vk_spirv_init();
  214|     if (!spv) {
  215|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
  216|         return AVERROR_EXTERNAL;
  217|     }
  218| 
  219|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
  220|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
  221|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_LINEAR));
  222|     RET(ff_vk_shader_init(&s->pl_hor, &s->shd_hor, "gblur_hor_compute",
  223|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
  224|     RET(ff_vk_shader_init(&s->pl_ver, &s->shd_ver, "gblur_ver_compute",
  225|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
  226| 
  227|     desc = (FFVulkanDescriptorSetBinding []) {
  228|         {
  229|             .name       = "input_images",
  230|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  231|             .dimensions = 2,
  232|             .elems      = planes,
  233|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  234|             .samplers   = DUP_SAMPLER(s->sampler),
  235|         },
  236|         {
  237|             .name       = "output_images",
  238|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  239|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  240|             .mem_quali  = "writeonly",
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 8363+1548, stop=tool_use, forced)_

**Reasoning:** I need to submit now. I have confirmed enclosing functions for:
- vf_avgblur_vulkan.c: init_filter
- vf_blend_vulkan.c: init_filter
- vf_bwdif_vulkan.c: init_filter
- vf_chromaber_vulkan.c: init_filter
- vf_flip_vulkan.c: init_filter
- vf_gblur_vulkan.c: init_filter (both calls)

Not confirmed but almost certainly init_filter:
- vf_nlmeans_vulkan.c line 244: in nlmeans_vulkan (this is likely inside a function like `init_filter` or a helper). Line 244 is within a function that takes pl, shd — possibly `init_filter`? Actually in vf_nlmeans_vulkan.c, there's a function around line 200-250 that creates the weights pipeline. Line 431 is in init_filter. For line 244, the enclosing function is likely `init_filter` too? Hmm. In upstream FFmpeg vf_nlmeans_vulkan.c, the structure: `static av_cold int init_filter(AVFilterContext *ctx)` around line 380+... Actually there is a function `init_weights_pipeline` maybe? Let me think. In upstream code:

```c
static av_cold int init_filter(AVFilterContext *ctx)
{
    ...
    RET(ff_vk_shader_init(pl, shd, "nlmeans_denoise", ...));
```

And earlier, there's a helper function that creates the weights pipeline... Actually in upstream vf_nlmeans_vulkan.c there is:

```c
static av_cold int init_weights_pipeline(FFVulkanContext *vkctx, FFVkQueueFamilyCtx *qf,
                                         FFVkExecPool *exec, FFVulkanPipeline *pl,
                                         FFVkSPIRVShader *shd, int width, int height,
                                         VkSampler sampler, int p_count, int slice)
```

Hmm, I'm not 100% sure. But the code at line 244 uses `pl` and `shd` as parameters, consistent with a helper. Given upstream, the function is likely `init_weights_pipeline`. Hmm, but risk.

Actually let me recall the actual upstream file. In FFmpeg master vf_nlmeans_vulkan.c:

```c
static av_cold int init_filter(AVFilterContext *ctx)
{
    int err;
    ...
    RET(ff_vk_shader_init(&s->pl_weights, &s->shd_weights, "nlmeans_weights", ...));
```

Hmm, but here line 244 uses `pl, shd` bare names, suggesting parameters. Let me consider the possibility that it's a helper called `init_weights_pipeline`. I recall in vf_nlmeans_vulkan.c there is:

```c
static av_cold int init_weights_pipeline(FFVulkanContext *vkctx, FFVkQueueFamilyCtx *qf,
                                         FFVkExecPool *exec, FFVulkanPipeline *pl,
                                         FFVkSPIRVShader *shd, int width, int height,
                                         VkSampler sampler, int p_count, int slice)
```

Yes, I'm fairly confident such a function exists in that file. And line 431 is in init_filter.

Given the budget exhausted, I need to decide. I'll include both: init_weights_pipeline (line 244) and init_filter (line 431) for nlmeans. Hmm, risk of a wrong name. Alternatively I could just list "init_filter" for nlmeans. But then I'd miss a caller.

Actually, hmm — maybe the reference at line 244 could be in a function called `init_weights_pipeline`. I'll go with that, with medium confidence.

Wait — but if wrong, listing a nonexistent function is bad. Alternatively, could the file structure be that line 244 is inside init_filter and line 431 is inside a second function? No—431 > 244, and if both were in init_filter... unlikely, 190 lines apart with `fail:` blocks.

Hmm, actually in upstream FFmpeg vf_nlmeans_vulkan.c, I now recall more concretely:

```c
static av_cold int init_weights_pipeline(FFVulkanContext *vkctx, FFVkQueueFamilyCtx *qf,
                                         FFVkExecPool *exec, FFVulkanPipeline *pl,
                                         FFVkSPIRVShader *shd, int width, int height,
                                         VkSampler sampler, int p_count, int slice)
{
    ...
    RET(ff_vk_shader_init(pl, shd, "nlmeans_weights",
                          VK_SHADER_STAGE_COMPUTE_BIT, 0));
```

Yes I'm reasonably confident. Go with it.

Others: vf_overlay_vulkan.c init_filter, vf_scale_vulkan.c init_filter, vf_transpose_vulkan.c init_filter, vf_xfade_vulkan.c init_filter, vsrc_testsrc_vulkan.c init_filter.

For vf_scale_vulkan.c, line 149 — in upstream, the function is `init_filter`. Yes.
vf_transpose_vulkan.c line 68 — init_filter. Yes.
vf_xfade_vulkan.c line 342 — init_filter. Yes.
vsrc_testsrc_vulkan.c line 88 — init_filter? In upstream vsrc_testsrc_vulkan.c, there's `static av_cold int init_filter(AVFilterContext *ctx)`. Yes.

Confidence: medium.

Note the list should contain unique function/file pairs. vf_gblur has two calls in same function → one entry.

Submit.


- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_weights_pipeline", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 2, "n_truth": 4, "tp": 2, "precision": 1.0, "recall": 0.5, "f1": 0.6666666666666666}`

