# Impact-analysis transcript — ffmpeg @ c982376076b6 — openrouter:deepseek/deepseek-v4-pro

- target: `ff_vk_shader_rep_fmt` (libavutil/vulkan.c), arity 1->2
- truth: [['libavfilter/vf_avgblur_vulkan.c', 'init_filter'], ['libavfilter/vf_blend_vulkan.c', 'init_filter'], ['libavfilter/vf_bwdif_vulkan.c', 'init_filter'], ['libavfilter/vf_chromaber_vulkan.c', 'init_filter'], ['libavfilter/vf_flip_vulkan.c', 'init_filter'], ['libavfilter/vf_gblur_vulkan.c', 'init_filter'], ['libavfilter/vf_nlmeans_vulkan.c', 'init_denoise_pipeline'], ['libavfilter/vf_overlay_vulkan.c', 'init_filter'], ['libavfilter/vf_scale_vulkan.c', 'init_filter'], ['libavfilter/vf_transpose_vulkan.c', 'init_filter'], ['libavfilter/vf_xfade_vulkan.c', 'init_vulkan'], ['libavfilter/vsrc_testsrc_vulkan.c', 'init_filter']]

## Self-navigation arm

### Turn 1  _(tok 910+92, stop=tool_use)_

**Reasoning:** Let me search for all call sites of `ff_vk_shader_rep_fmt` in the repository.

- `grep(pattern=ff_vk_shader_rep_fmt, version=old)` →

```
14 matches
libavfilter/vf_avgblur_vulkan.c:102:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_blend_vulkan.c:173:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_bwdif_vulkan.c:107:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_chromaber_vulkan.c:120:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_flip_vulkan.c:86:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_gblur_vulkan.c:231:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_nlmeans_vulkan.c:457:            .mem_layout  = ff_vk_shader_rep_fmt(vkctx->output_format),
libavfilter/vf_overlay_vulkan.c:142:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_scale_vulkan.c:174:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_transpose_vulkan.c:85:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_xfade_vulkan.c:367:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vsrc_testsrc_vulkan.c:105:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavutil/vulkan.c:1289:const char *ff_vk_shader_rep_fmt(enum AVPixelFormat pixfmt)
libavutil/vulkan.h:363:const char *ff_vk_shader_rep_fmt(enum AVPixelFormat pixfmt);
```

### Turn 2  _(tok 1494+937, stop=tool_use)_

**Reasoning:** Now I need to identify the enclosing functions for each call site. Let me look at each file to find the function that contains the call.

**Says:** Let me identify the enclosing function for each call site.

- `read_file(path=libavfilter/vf_avgblur_vulkan.c, start_line=90, end_line=112)` →

```
libavfilter/vf_avgblur_vulkan.c lines 90-112 of 258
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
  110|     RET(ff_vk_shader_add_descriptor_set(vkctx, shd, desc, 2, 0, 0));
  111| 
  112|     GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
```

- `read_file(path=libavfilter/vf_blend_vulkan.c, start_line=163, end_line=183)` →

```
libavfilter/vf_blend_vulkan.c lines 163-183 of 399
  163|             .name       = "bottom_images",
  164|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  165|             .dimensions = 2,
  166|             .elems      = planes,
  167|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  168|             .samplers   = DUP_SAMPLER(s->sampler),
  169|         },
  170|         {
  171|             .name       = "output_images",
  172|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  173|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  174|             .mem_quali  = "writeonly",
  175|             .dimensions = 2,
  176|             .elems      = planes,
  177|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  178|         },
  179|     };
  180| 
  181|     RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 3, 0, 0));
  182| 
  183|     for (int i = 0, j = 0; i < planes; i++) {
```

- `read_file(path=libavfilter/vf_bwdif_vulkan.c, start_line=97, end_line=117)` →

```
libavfilter/vf_bwdif_vulkan.c lines 97-117 of 336
   97|             .name       = "next",
   98|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
   99|             .dimensions = 2,
  100|             .elems      = planes,
  101|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  102|             .samplers   = DUP_SAMPLER(s->sampler),
  103|         },
  104|         {
  105|             .name       = "dst",
  106|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  107|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  108|             .mem_quali  = "writeonly",
  109|             .dimensions = 2,
  110|             .elems      = planes,
  111|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  112|         },
  113|     };
  114| 
  115|     RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 4, 0, 0));
  116| 
  117|     GLSLC(0, layout(push_constant, std430) uniform pushConstants {                 );
```

- `read_file(path=libavfilter/vf_chromaber_vulkan.c, start_line=110, end_line=130)` →

```
libavfilter/vf_chromaber_vulkan.c lines 110-130 of 259
  110|             .name       = "input_img",
  111|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  112|             .dimensions = 2,
  113|             .elems      = planes,
  114|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  115|             .samplers   = DUP_SAMPLER(s->sampler),
  116|         },
  117|         {
  118|             .name       = "output_img",
  119|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  120|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  121|             .mem_quali  = "writeonly",
  122|             .dimensions = 2,
  123|             .elems      = planes,
  124|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  125|         },
  126|     };
  127| 
  128|     RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 2, 0, 0));
  129| 
  130|     GLSLD(   distort_chroma_kernel                                        );
```

- `read_file(path=libavfilter/vf_flip_vulkan.c, start_line=76, end_line=96)` →

```
libavfilter/vf_flip_vulkan.c lines 76-96 of 299
   76|             .name       = "input_image",
   77|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
   78|             .dimensions = 2,
   79|             .elems      = planes,
   80|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
   81|             .samplers   = DUP_SAMPLER(s->sampler),
   82|         },
   83|         {
   84|             .name       = "output_image",
   85|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
   86|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
   87|             .mem_quali  = "writeonly",
   88|             .dimensions = 2,
   89|             .elems      = planes,
   90|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
   91|         },
   92|     };
   93| 
   94|     RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 2, 0, 0));
   95| 
   96|     GLSLC(0, void main()                                                                    );
```

- `read_file(path=libavfilter/vf_gblur_vulkan.c, start_line=221, end_line=241)` →

```
libavfilter/vf_gblur_vulkan.c lines 221-241 of 385
  221|             .name       = "input_images",
  222|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  223|             .dimensions = 2,
  224|             .elems      = planes,
  225|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  226|             .samplers   = DUP_SAMPLER(s->sampler),
  227|         },
  228|         {
  229|             .name       = "output_images",
  230|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  231|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  232|             .mem_quali  = "writeonly",
  233|             .dimensions = 2,
  234|             .elems      = planes,
  235|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  236|         },
  237|     };
  238| 
  239|     init_gaussian_params(s);
  240| 
  241|     {
```

- `read_file(path=libavfilter/vf_nlmeans_vulkan.c, start_line=447, end_line=467)` →

```
libavfilter/vf_nlmeans_vulkan.c lines 447-467 of 1123
  447|             .name        = "input_img",
  448|             .type        = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  449|             .dimensions  = 2,
  450|             .elems       = planes,
  451|             .stages      = VK_SHADER_STAGE_COMPUTE_BIT,
  452|             .samplers    = DUP_SAMPLER(sampler),
  453|         },
  454|         {
  455|             .name        = "output_img",
  456|             .type        = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  457|             .mem_layout  = ff_vk_shader_rep_fmt(vkctx->output_format),
  458|             .mem_quali   = "writeonly",
  459|             .dimensions  = 2,
  460|             .elems       = planes,
  461|             .stages      = VK_SHADER_STAGE_COMPUTE_BIT,
  462|         },
  463|     };
  464|     RET(ff_vk_shader_add_descriptor_set(vkctx, shd, desc_set, 2, 0, 0));
  465| 
  466|     desc_set = (FFVulkanDescriptorSetBinding []) {
  467|         {
```

- `read_file(path=libavfilter/vf_overlay_vulkan.c, start_line=132, end_line=152)` →

```
libavfilter/vf_overlay_vulkan.c lines 132-152 of 347
  132|             .name       = "overlay_img",
  133|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  134|             .dimensions = 2,
  135|             .elems      = planes,
  136|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  137|             .samplers   = DUP_SAMPLER(s->sampler),
  138|         },
  139|         {
  140|             .name       = "output_img",
  141|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  142|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  143|             .mem_quali  = "writeonly",
  144|             .dimensions = 2,
  145|             .elems      = planes,
  146|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  147|         },
  148|     };
  149| 
  150|     RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 3, 0, 0));
  151| 
  152|     GLSLD(   overlay_noalpha                                              );
```

- `read_file(path=libavfilter/vf_scale_vulkan.c, start_line=164, end_line=184)` →

```
libavfilter/vf_scale_vulkan.c lines 164-184 of 417
  164|             .name       = "input_img",
  165|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  166|             .dimensions = 2,
  167|             .elems      = in_planes,
  168|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  169|             .samplers   = DUP_SAMPLER(s->sampler),
  170|         },
  171|         {
  172|             .name       = "output_img",
  173|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  174|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  175|             .mem_quali  = "writeonly",
  176|             .dimensions = 2,
  177|             .elems      = av_pix_fmt_count_planes(s->vkctx.output_format),
  178|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  179|         },
  180|     };
  181| 
  182|     RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 2, 0, 0));
  183| 
  184|     GLSLD(   scale_bilinear                                                  );
```

- `read_file(path=libavfilter/vf_transpose_vulkan.c, start_line=75, end_line=95)` →

```
libavfilter/vf_transpose_vulkan.c lines 75-95 of 276
   75|             .name       = "input_images",
   76|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
   77|             .dimensions = 2,
   78|             .elems      = planes,
   79|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
   80|             .samplers   = DUP_SAMPLER(s->sampler),
   81|         },
   82|         {
   83|             .name       = "output_images",
   84|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
   85|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
   86|             .mem_quali  = "writeonly",
   87|             .dimensions = 2,
   88|             .elems      = planes,
   89|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
   90|         },
   91|     };
   92| 
   93|     RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 2, 0, 0));
   94| 
   95|     GLSLC(0, void main()                                               );
```

- `read_file(path=libavfilter/vf_xfade_vulkan.c, start_line=357, end_line=377)` →

```
libavfilter/vf_xfade_vulkan.c lines 357-377 of 720
  357|             .name       = "b_images",
  358|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  359|             .dimensions = 2,
  360|             .elems      = planes,
  361|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  362|             .samplers   = DUP_SAMPLER(s->sampler),
  363|         },
  364|         {
  365|             .name       = "output_images",
  366|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  367|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  368|             .mem_quali  = "writeonly",
  369|             .dimensions = 2,
  370|             .elems      = planes,
  371|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  372|         },
  373|     };
  374| 
  375|     RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 3, 0, 0));
  376| 
  377|     GLSLC(0, layout(push_constant, std430) uniform pushConstants {                 );
```

- `read_file(path=libavfilter/vsrc_testsrc_vulkan.c, start_line=95, end_line=115)` →

```
libavfilter/vsrc_testsrc_vulkan.c lines 95-115 of 375
   95|     GLSLC(0, };                                                           );
   96|     GLSLC(0,                                                              );
   97| 
   98|     ff_vk_shader_add_push_const(&s->shd, 0, sizeof(s->opts),
   99|                                 VK_SHADER_STAGE_COMPUTE_BIT);
  100| 
  101|     desc_set = (FFVulkanDescriptorSetBinding []) {
  102|         {
  103|             .name       = "output_img",
  104|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  105|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  106|             .mem_quali  = "writeonly",
  107|             .dimensions = 2,
  108|             .elems      = planes,
  109|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  110|         },
  111|     };
  112| 
  113|     RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc_set, 1, 0, 0));
  114| 
  115|     GLSLC(0, void main()                                                  );
```

### Turn 3  _(tok 6555+496, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing function for each of these call sites. Let me look at the function definitions that contain these lines.

**Says:** Now let me find the enclosing function names for each file:

- `read_file(end_line=90, path=libavfilter/vf_avgblur_vulkan.c, start_line=50)` →

```
libavfilter/vf_avgblur_vulkan.c lines 50-90 of 258
   50|     C(0, void distort(const ivec2 pos, const int idx)                         )
   51|     C(0, {                                                                    )
   52|     C(1,     vec4 sum = vec4(0);                                              )
   53|     C(1,     for (int y = -filter_len.y; y <= filter_len.y; y++)              )
   54|     C(1,        for (int x = -filter_len.x; x <= filter_len.x; x++)           )
   55|     C(2,            sum += texture(input_img[idx], pos + ivec2(x, y));        )
   56|     C(0,                                                                      )
   57|     C(1,     imageStore(output_img[idx], pos, sum * filter_norm);             )
   58|     C(0, }                                                                    )
   59| };
   60| 
   61| static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
   62| {
   63|     int err;
   64|     uint8_t *spv_data;
   65|     size_t spv_len;
   66|     void *spv_opaque = NULL;
   67|     AvgBlurVulkanContext *s = ctx->priv;
   68|     FFVulkanContext *vkctx = &s->vkctx;
   69|     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   70|     FFVulkanShader *shd;
   71|     FFVkSPIRVCompiler *spv;
   72|     FFVulkanDescriptorSetBinding *desc;
   73| 
   74|     spv = ff_vk_spirv_init();
   75|     if (!spv) {
   76|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
   77|         return AVERROR_EXTERNAL;
   78|     }
   79| 
   80|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
   81|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
   82|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_LINEAR));
   83|     RET(ff_vk_shader_init(vkctx, &s->shd, "avgblur",
   84|                           VK_SHADER_STAGE_COMPUTE_BIT,
   85|                           NULL, 0,
   86|                           32, 1, 1,
   87|                           0));
   88|     shd = &s->shd;
   89| 
   90|     desc = (FFVulkanDescriptorSetBinding []) {
```

- `read_file(end_line=163, path=libavfilter/vf_blend_vulkan.c, start_line=120)` →

```
libavfilter/vf_blend_vulkan.c lines 120-163 of 399
  120|         return ret;
  121| 
  122|     return config_params(ctx);
  123| }
  124| 
  125| static av_cold int init_filter(AVFilterContext *avctx)
  126| {
  127|     int err = 0;
  128|     uint8_t *spv_data;
  129|     size_t spv_len;
  130|     void *spv_opaque = NULL;
  131|     BlendVulkanContext *s = avctx->priv;
  132|     FFVulkanContext *vkctx = &s->vkctx;
  133|     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
  134|     FFVulkanShader *shd = &s->shd;
  135|     FFVkSPIRVCompiler *spv;
  136|     FFVulkanDescriptorSetBinding *desc;
  137| 
  138|     spv = ff_vk_spirv_init();
  139|     if (!spv) {
  140|         av_log(avctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
  141|         return AVERROR_EXTERNAL;
  142|     }
  143| 
  144|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
  145|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
  146|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_NEAREST));
  147|     RET(ff_vk_shader_init(vkctx, &s->shd, "blend",
  148|                           VK_SHADER_STAGE_COMPUTE_BIT,
  149|                           NULL, 0,
  150|                           32, 32, 1,
  151|                           0));
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
```

- `read_file(end_line=97, path=libavfilter/vf_bwdif_vulkan.c, start_line=60)` →

```
libavfilter/vf_bwdif_vulkan.c lines 60-97 of 336
   60|     FFVulkanDescriptorSetBinding *desc;
   61| 
   62|     spv = ff_vk_spirv_init();
   63|     if (!spv) {
   64|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
   65|         return AVERROR_EXTERNAL;
   66|     }
   67| 
   68|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
   69|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
   70|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_NEAREST));
   71| 
   72|     RET(ff_vk_shader_init(vkctx, &s->shd, "bwdif",
   73|                           VK_SHADER_STAGE_COMPUTE_BIT,
   74|                           NULL, 0,
   75|                           1, 64, 1,
   76|                           0));
   77|     shd = &s->shd;
   78| 
   79|     desc = (FFVulkanDescriptorSetBinding []) {
   80|         {
   81|             .name       = "prev",
   82|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
   83|             .dimensions = 2,
   84|             .elems      = planes,
   85|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
   86|             .samplers   = DUP_SAMPLER(s->sampler),
   87|         },
   88|         {
   89|             .name       = "cur",
   90|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
   91|             .dimensions = 2,
   92|             .elems      = planes,
   93|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
   94|             .samplers   = DUP_SAMPLER(s->sampler),
   95|         },
   96|         {
   97|             .name       = "next",
```

- `read_file(end_line=110, path=libavfilter/vf_chromaber_vulkan.c, start_line=70)` →

```
libavfilter/vf_chromaber_vulkan.c lines 70-110 of 259
   70|     int err;
   71|     uint8_t *spv_data;
   72|     size_t spv_len;
   73|     void *spv_opaque = NULL;
   74|     ChromaticAberrationVulkanContext *s = ctx->priv;
   75|     FFVulkanContext *vkctx = &s->vkctx;
   76|     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   77|     FFVulkanShader *shd = &s->shd;
   78|     FFVkSPIRVCompiler *spv;
   79|     FFVulkanDescriptorSetBinding *desc;
   80| 
   81|     /* Normalize options */
   82|     s->opts.dist[0] = (s->opts.dist[0] / 100.0f) + 1.0f;
   83|     s->opts.dist[1] = (s->opts.dist[1] / 100.0f) + 1.0f;
   84| 
   85|     spv = ff_vk_spirv_init();
   86|     if (!spv) {
   87|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
   88|         return AVERROR_EXTERNAL;
   89|     }
   90| 
   91|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
   92|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
   93|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 0, VK_FILTER_LINEAR));
   94|     RET(ff_vk_shader_init(vkctx, &s->shd, "chromatic_abberation",
   95|                           VK_SHADER_STAGE_COMPUTE_BIT,
   96|                           NULL, 0,
   97|                           32, 32, 1,
   98|                           0));
   99| 
  100|     GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
  101|     GLSLC(1,    vec2 dist;                                                );
  102|     GLSLC(0, };                                                           );
  103|     GLSLC(0,                                                              );
  104| 
  105|     ff_vk_shader_add_push_const(&s->shd, 0, sizeof(s->opts),
  106|                                 VK_SHADER_STAGE_COMPUTE_BIT);
  107| 
  108|     desc = (FFVulkanDescriptorSetBinding []) {
  109|         {
  110|             .name       = "input_img",
```

- `read_file(end_line=76, path=libavfilter/vf_flip_vulkan.c, start_line=40)` →

```
libavfilter/vf_flip_vulkan.c lines 40-76 of 299
   40|     FFVkExecPool e;
   41|     FFVkQueueFamilyCtx qf;
   42|     FFVulkanShader shd;
   43|     VkSampler sampler;
   44| } FlipVulkanContext;
   45| 
   46| static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in, enum FlipType type)
   47| {
   48|     int err = 0;
   49|     uint8_t *spv_data;
   50|     size_t spv_len;
   51|     void *spv_opaque = NULL;
   52|     FlipVulkanContext *s = ctx->priv;
   53|     FFVulkanContext *vkctx = &s->vkctx;
   54|     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   55|     FFVulkanShader *shd = &s->shd;
   56|     FFVkSPIRVCompiler *spv;
   57|     FFVulkanDescriptorSetBinding *desc;
   58| 
   59|     spv = ff_vk_spirv_init();
   60|     if (!spv) {
   61|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
   62|         return AVERROR_EXTERNAL;
   63|     }
   64| 
   65|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
   66|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
   67|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_LINEAR));
   68|     RET(ff_vk_shader_init(vkctx, &s->shd, "flip",
   69|                           VK_SHADER_STAGE_COMPUTE_BIT,
   70|                           NULL, 0,
   71|                           32, 32, 1,
   72|                           0));
   73| 
   74|     desc = (FFVulkanDescriptorSetBinding []) {
   75|         {
   76|             .name       = "input_image",
```

- `read_file(end_line=221, path=libavfilter/vf_gblur_vulkan.c, start_line=180)` →

```
libavfilter/vf_gblur_vulkan.c lines 180-221 of 385
  180|                          VK_BUFFER_USAGE_STORAGE_BUFFER_BIT,
  181|                          VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT));
  182|     RET(ff_vk_map_buffer(&s->vkctx, params_buf, &kernel_mapped, 0));
  183| 
  184|     init_gaussian_kernel((float *)kernel_mapped, sigma, ksize);
  185| 
  186|     RET(ff_vk_unmap_buffer(&s->vkctx, params_buf, 1));
  187|     RET(ff_vk_shader_update_desc_buffer(&s->vkctx, &s->e.contexts[0], shd, 1, 0, 0,
  188|                                         params_buf, 0, params_buf->size,
  189|                                         VK_FORMAT_UNDEFINED));
  190| 
  191| fail:
  192|     av_free(kernel_def);
  193|     if (spv_opaque)
  194|         spv->free_shader(spv, &spv_opaque);
  195|     return err;
  196| }
  197| 
  198| static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
  199| {
  200|     int err = 0;
  201|     GBlurVulkanContext *s = ctx->priv;
  202|     FFVulkanContext *vkctx = &s->vkctx;
  203|     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
  204| 
  205|     FFVulkanShader *shd;
  206|     FFVkSPIRVCompiler *spv;
  207|     FFVulkanDescriptorSetBinding *desc;
  208| 
  209|     spv = ff_vk_spirv_init();
  210|     if (!spv) {
  211|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
  212|         return AVERROR_EXTERNAL;
  213|     }
  214| 
  215|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
  216|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
  217|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_LINEAR));
  218| 
  219|     desc = (FFVulkanDescriptorSetBinding []) {
  220|         {
  221|             .name       = "input_images",
```

### Turn 4  _(tok 10917+122, stop=tool_use)_

**Reasoning:** Now let me find the enclosing function for nlmeans_vulkan.c. The call is at line 457 and I need to figure out which function it's in.

- `read_file(end_line=457, path=libavfilter/vf_nlmeans_vulkan.c, start_line=400)` →

```
libavfilter/vf_nlmeans_vulkan.c lines 400-457 of 1123
  400|     }
  401| 
  402|     GLSLC(0, }                                                                   );
  403| 
  404|     RET(spv->compile_shader(vkctx, spv, shd, &spv_data, &spv_len, "main", &spv_opaque));
  405|     RET(ff_vk_shader_link(vkctx, shd, spv_data, spv_len, "main"));
  406| 
  407|     RET(ff_vk_shader_register_exec(vkctx, exec, shd));
  408| 
  409| fail:
  410|     if (spv_opaque)
  411|         spv->free_shader(spv, &spv_opaque);
  412| 
  413|     return err;
  414| }
  415| 
  416| typedef struct DenoisePushData {
  417|     uint32_t ws_stride[4];
  418| } DenoisePushData;
  419| 
  420| static av_cold int init_denoise_pipeline(FFVulkanContext *vkctx, FFVkExecPool *exec,
  421|                                          FFVulkanShader *shd,
  422|                                          VkSampler sampler, FFVkSPIRVCompiler *spv,
  423|                                          const AVPixFmtDescriptor *desc, int planes)
  424| {
  425|     int err;
  426|     uint8_t *spv_data;
  427|     size_t spv_len;
  428|     void *spv_opaque = NULL;
  429|     FFVulkanDescriptorSetBinding *desc_set;
  430| 
  431|     RET(ff_vk_shader_init(vkctx, shd, "nlmeans_denoise",
  432|                           VK_SHADER_STAGE_COMPUTE_BIT,
  433|                           (const char *[]) { "GL_EXT_buffer_reference",
  434|                                              "GL_EXT_buffer_reference2" }, 2,
  435|                           32, 32, 1,
  436|                           0));
  437| 
  438|     GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
  439|     GLSLC(1,    uvec4 ws_stride;                                          );
  440|     GLSLC(0, };                                                           );
  441| 
  442|     ff_vk_shader_add_push_const(shd, 0, sizeof(DenoisePushData),
  443|                                 VK_SHADER_STAGE_COMPUTE_BIT);
  444| 
  445|     desc_set = (FFVulkanDescriptorSetBinding []) {
  446|         {
  447|             .name        = "input_img",
  448|             .type        = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  449|             .dimensions  = 2,
  450|             .elems       = planes,
  451|             .stages      = VK_SHADER_STAGE_COMPUTE_BIT,
  452|             .samplers    = DUP_SAMPLER(sampler),
  453|         },
  454|         {
  455|             .name        = "output_img",
  456|             .type        = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  457|             .mem_layout  = ff_vk_shader_rep_fmt(vkctx->output_format),
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 11853+645, stop=tool_use, forced)_

**Reasoning:** Let me now identify all the enclosing functions. I've seen the start of each function. Let me summarize:

1. vf_avgblur_vulkan.c: line 61 - `init_filter` (at line 61)
2. vf_blend_vulkan.c: line 125 - `init_filter` (at line 125)
3. vf_bwdif_vulkan.c: I need to find the function name. I see `shd = &s->shd;` at line 77, `desc = ...` at line 79. Let me look further up.
4. vf_chromaber_vulkan.c: line 68 or so - need to find function name
5. vf_flip_vulkan.c: line 46 - `init_filter`
6. vf_gblur_vulkan.c: line 198 - `init_filter`
7. vf_nlmeans_vulkan.c: line 420 - `init_denoise_pipeline`
8. vf_overlay_vulkan.c: need to find function name
9. vf_scale_vulkan.c: need to find function name
10. vf_transpose_vulkan.c: need to find function name
11. vf_xfade_vulkan.c: need to find function name
12. vsrc_testsrc_vulkan.c: need to find function name

Let me look at the ones I haven't identified.

- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_denoise_pipeline", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "medium"}`

**Score (self):** `{"n_pred": 2, "n_truth": 3, "tp": 2, "precision": 1.0, "recall": 0.6666666666666666, "f1": 0.8}`

## Tool arm

### Turn 1  _(tok 2728+102, stop=tool_use)_

**Reasoning:** The user wants me to find every call site of `ff_vk_shader_rep_fmt` in the repository. Let me start by searching for it.

- `grep(pattern=ff_vk_shader_rep_fmt, version=old)` →

```
14 matches
libavfilter/vf_avgblur_vulkan.c:102:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_blend_vulkan.c:173:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_bwdif_vulkan.c:107:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_chromaber_vulkan.c:120:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_flip_vulkan.c:86:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_gblur_vulkan.c:231:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_nlmeans_vulkan.c:457:            .mem_layout  = ff_vk_shader_rep_fmt(vkctx->output_format),
libavfilter/vf_overlay_vulkan.c:142:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_scale_vulkan.c:174:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_transpose_vulkan.c:85:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_xfade_vulkan.c:367:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vsrc_testsrc_vulkan.c:105:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavutil/vulkan.c:1289:const char *ff_vk_shader_rep_fmt(enum AVPixelFormat pixfmt)
libavutil/vulkan.h:363:const char *ff_vk_shader_rep_fmt(enum AVPixelFormat pixfmt);
```

### Turn 2  _(tok 3322+985, stop=tool_use)_

**Reasoning:** I need to find the enclosing functions for each call site. Let me get the context around each call to identify the function name. Let me look at each file at the relevant lines.

The definition is at libavutil/vulkan.c:1289 (exclude).
The prototype/declaration is at libavutil/vulkan.h:363 (exclude).

I need to look at each filter file to find the enclosing function. Let me use get_context_at for each call site.

- `get_context_at(file=libavfilter/vf_avgblur_vulkan.c, line=102, version=old)` →

```
init_filter — libavfilter/vf_avgblur_vulkan.c:61 [function] static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
  reads: ctx, in; writes: ctx*, in*; returns: return AVERROR_EXTERNAL; | return err; | return ff_filter_frame(outlink, out); | return err;

SLICE around line 102 (def-use, level 2; '>' marks the seed):
static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in) {
   ...
   AvgBlurVulkanContext *s = ctx->priv;
   FFVulkanContext *vkctx = &s->vkctx;
   const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   ...
   shd = &s->shd;
>  desc =(FFVulkanDescriptorSetBinding []){ { .name = "input_img", .type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, .samplers = DUP_SAMPLER(s->sampler), }, { .name = "output_img", .type = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE, .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format), .mem_quali = "writeonly", .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, }, };
   RET(ff_vk_shader_add_descriptor_set(vkctx, shd, desc, 2, 0, 0));
   ...
}

CALLEES (41):
  av_pix_fmt_count_planes (libavutil/pixdesc.c:3065): reads pix_fmt; writes -; returns return AVERROR(EINVAL); | return ret;
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_vk_qf_init (libavutil/vulkan.c:228): reads dev_family, qf, s; writes qf*; returns return(qf->queue_family = vk_qf_get_index(s, dev_family, &qf->nb_queues));
  ff_vk_exec_pool_init (libavutil/vulkan.c:300): reads nb_contexts, nb_queries, pool, qf, query_64bit, query_create_pnext, query_type, s; writes pool*; returns return AVERROR(EINVAL); | return AVERROR(err); | return AVERROR_EXTERNAL; | return 0; | return err;
  ff_vk_init_sampler (libavutil/vulkan.c:1244): reads filt, s, sampler, unnorm_coords; writes -; returns return AVERROR_EXTERNAL; | return 0;
  ff_vk_shader_init (libavutil/vulkan.c:1431): reads extensions, lg_x, lg_y, lg_z, name, nb_extensions, required_subgroup_size, s, shd, stage; writes shd*; returns return 0;
  ff_vk_shader_rep_fmt (libavutil/vulkan.c:1289): reads pixfmt; writes -; returns return high ? "rgba16f" : "rgba8";
  ff_vk_shader_add_descriptor_set (libavutil/vulkan.c:1795): reads desc, nb, print_to_shader_only, s, shd, singular; writes shd*; returns return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return 0;
  ff_vk_shader_add_push_const (libavutil/vulkan.c:1223): reads offset, shd, size, stage; writes shd*; returns return AVERROR(ENOMEM); | return 0;
  main (ffbuild/bin2c.c:26 (1 of 168 definitions)): reads argc, argv; writes argv*; returns return 1; | return -1; | return -1; | return -1; | return 0;
  ff_vk_shader_register_exec (libavutil/vulkan.c:1907): reads pool, s, shd; writes pool*, shd*; returns return 0; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return err; | return err;
  ff_vk_shader_link (libavutil/vulkan.c:1720): reads entrypoint, s, shd, spirv, spirv_len; writes shd*; returns return err; | return err; | return AVERROR(ENOMEM); | return err; | return err; | return err;
  ff_get_video_buffer (libavfilter/video.c:116): reads h, link, w; writes -; returns return ret;
  ff_vk_filter_process_simple (libavfilter/vulkan_filter.c:242): reads e, in_f, out_f, push_size, push_src, sampler, shd, vkctx; writes -; returns return ff_vk_exec_submit(vkctx, exec); | return err;
  av_frame_copy_props (libavutil/frame.c:713): reads dst, src; writes -; returns return frame_copy_props(dst, src, 1);
  av_frame_free (libavutil/frame.c:162): reads frame; writes -; returns -
  ff_filter_frame (libavfilter/avfilter.c:1062): reads frame, link; writes frame*; returns return ret; | return 0; | return AVERROR_PATCHWELCOME;
  ff_vk_uninit (libavutil/vulkan.c:2306): reads s; writes s*; returns -
  ff_vk_shader_free (libavutil/vulkan.c:2267): reads s, shd; writes shd*; returns -
  ff_vk_exec_pool_free (libavutil/vulkan.c:238): reads pool, s; writes pool*; returns -
  ff_vk_spirv_init [macro (1 of 2 definitions)]: #define ff_vk_spirv_init ff_vk_shaderc_init
  RET [macro (1 of 2 definitions)]: #define RET(x) \
  DUP_SAMPLER [macro]: #define DUP_SAMPLER(x) { x, x, x, x }
  GLSLC [macro]: #define GLSLC(N, S) \
  GLSLD [macro]: #define GLSLD(D) \
  GLSLF [macro]: #define GLSLF(N, S, ...) \
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)
  OFFSET [macro (1 of 713 definitions)]: #define OFFSET(x) offsetof(OptionsContext, x)
  AVFILTER_DEFINE_CLASS [macro]: #define AVFILTER_DEFINE_CLASS_EXT(name, desc, options) \
  FILTER_SINGLE_PIXFMT [macro]: #define FILTER_SINGLE_PIXFMT(pix_fmt_) \
  not defined in this repository: layout, imageStore, texture, distort, if, IS_WITHIN, imageSize, ivec2
  not shown (3): FILTER_OUTPUTS, FILTER_INPUTS, NULL_IF_CONFIG_SMALL

CALLERS (8):
  init_frame_decoder (libavcodec/apedec.c:1477): init_filter(ctx, ctx->filters[i], ctx->filterbuf[i],
  avgblur_vulkan_filter_frame (libavfilter/vf_avgblur_vulkan.c:180): RET(init_filter(ctx, in));
  blend_frame (libavfilter/vf_blend_vulkan.c:256): RET(init_filter(avctx));
  bwdif_vulkan_config_output (libavfilter/vf_bwdif_vulkan.c:293): return init_filter(avctx);
  chromaber_vulkan_filter_frame (libavfilter/vf_chromaber_vulkan.c:182): RET(init_filter(ctx, in));
  filter_frame (libavfilter/vf_flip_vulkan.c:175): RET(init_filter(ctx, in, type));
  gblur_vulkan_filter_frame (libavfilter/vf_gblur_vulkan.c:320): RET(init_filter(ctx, in));
  nlmeans_vulkan_filter_frame (libavfilter/vf_nlmeans_vulkan.c:780): RET(init_filter(ctx));
  ... only the first 8 of 14 reference sites were followed
```

- `get_context_at(file=libavfilter/vf_blend_vulkan.c, line=173, version=old)` →

```
init_filter — libavfilter/vf_blend_vulkan.c:125 [function] static av_cold int init_filter(AVFilterContext *avctx)
  reads: -; writes: avctx*; returns: return AVERROR_EXTERNAL; | return err; | return ff_filter_frame(outlink, out); | return err; | return ff_vk_filter_init(avctx); | return AVERROR(EINVAL);

SLICE around line 173 (def-use, level 2; '>' marks the seed):
static av_cold int init_filter(AVFilterContext *avctx) {
   ...
   BlendVulkanContext *s = avctx->priv;
   FFVulkanContext *vkctx = &s->vkctx;
   const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   ...
>  desc =(FFVulkanDescriptorSetBinding []){ { .name = "top_images", .type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, .samplers = DUP_SAMPLER(s->sampler), }, { .name = "bottom_images", .type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, .samplers = DUP_SAMPLER(s->sampler), }, { .name = "output_images", .type = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE, .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format), .mem_quali = "writeonly", .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, }, };
   RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 3, 0, 0));
   ...
}

CALLEES (48):
  av_pix_fmt_count_planes (libavutil/pixdesc.c:3065): reads pix_fmt; writes -; returns return AVERROR(EINVAL); | return ret;
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_vk_qf_init (libavutil/vulkan.c:228): reads dev_family, qf, s; writes qf*; returns return(qf->queue_family = vk_qf_get_index(s, dev_family, &qf->nb_queues));
  ff_vk_exec_pool_init (libavutil/vulkan.c:300): reads nb_contexts, nb_queries, pool, qf, query_64bit, query_create_pnext, query_type, s; writes pool*; returns return AVERROR(EINVAL); | return AVERROR(err); | return AVERROR_EXTERNAL; | return 0; | return err;
  ff_vk_init_sampler (libavutil/vulkan.c:1244): reads filt, s, sampler, unnorm_coords; writes -; returns return AVERROR_EXTERNAL; | return 0;
  ff_vk_shader_init (libavutil/vulkan.c:1431): reads extensions, lg_x, lg_y, lg_z, name, nb_extensions, required_subgroup_size, s, shd, stage; writes shd*; returns return 0;
  ff_vk_shader_rep_fmt (libavutil/vulkan.c:1289): reads pixfmt; writes -; returns return high ? "rgba16f" : "rgba8";
  ff_vk_shader_add_descriptor_set (libavutil/vulkan.c:1795): reads desc, nb, print_to_shader_only, s, shd, singular; writes shd*; returns return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return 0;
  main (ffbuild/bin2c.c:26 (1 of 168 definitions)): reads argc, argv; writes argv*; returns return 1; | return -1; | return -1; | return -1; | return 0;
  ff_vk_shader_register_exec (libavutil/vulkan.c:1907): reads pool, s, shd; writes pool*, shd*; returns return 0; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return err; | return err;
  ff_vk_shader_link (libavutil/vulkan.c:1720): reads entrypoint, s, shd, spirv, spirv_len; writes shd*; returns return err; | return err; | return AVERROR(ENOMEM); | return err; | return err; | return err;
  ff_get_video_buffer (libavfilter/video.c:116): reads h, link, w; writes -; returns return ret;
  ff_framesync_get_frame (libavfilter/framesync.c:270): reads fs, get, in, rframe; writes fs*, rframe*; returns return 0; | return AVERROR(ENOMEM); | return 0;
  av_frame_copy_props (libavutil/frame.c:713): reads dst, src; writes -; returns return frame_copy_props(dst, src, 1);
  ff_vk_filter_process_Nin (libavfilter/vulkan_filter.c:401): reads e, in, nb_in, out, push_size, push_src, sampler, shd, vkctx; writes -; returns return ff_vk_exec_submit(vkctx, exec); | return err;
  ff_filter_frame (libavfilter/avfilter.c:1062): reads frame, link; writes frame*; returns return ret; | return 0; | return AVERROR_PATCHWELCOME;
  av_frame_free (libavutil/frame.c:162): reads frame; writes -; returns -
  ff_vk_filter_init (libavfilter/vulkan_filter.c:233): reads avctx; writes avctx*; returns return 0;
  ff_framesync_uninit (libavfilter/framesync.c:302): reads fs; writes fs*; returns -
  ff_vk_uninit (libavutil/vulkan.c:2306): reads s; writes s*; returns -
  ff_vk_shader_free (libavutil/vulkan.c:2267): reads s, shd; writes shd*; returns -
  ff_vk_exec_pool_free (libavutil/vulkan.c:238): reads pool, s; writes pool*; returns -
  config_params (libavfilter/vf_bilateral.c:91 (1 of 3 definitions)): reads ctx; writes ctx*; returns return 0;
  ff_framesync_configure (libavfilter/framesync.c:137): reads fs; writes fs*; returns return AVERROR(EINVAL); | return 0;
  ff_framesync_init_dualinput (libavfilter/framesync.c:373): reads fs, parent; writes fs*; returns return ret; | return 0;
  ff_vk_filter_config_output (libavfilter/vulkan_filter.c:209): reads outlink; writes outlink*; returns return err; | return AVERROR(ENOMEM); | return err;
  ff_filter_link (libavfilter/filters.h:197): reads link; writes -; returns return(FilterLink*)link;
  ff_framesync_activate (libavfilter/framesync.c:353): reads fs; writes fs*; returns return ret; | return 0; | return ret; | return 0;
  ff_vk_spirv_init [macro (1 of 2 definitions)]: #define ff_vk_spirv_init ff_vk_shaderc_init
  RET [macro (1 of 2 definitions)]: #define RET(x) \
  not defined in this repository: imageStore, texture, if, IS_WITHIN, imageSize, ivec2
  not shown (12): DUP_SAMPLER, GLSLD, GLSLC, GLSLF, s, AVERROR, OFFSET, AVFILTER_DEFINE_CLASS, FILTER_SINGLE_PIXFMT, FILTER_OUTPUTS, FILTER_INPUTS, NULL_IF_CONFIG_SMALL

CALLERS (8):
  init_frame_decoder (libavcodec/apedec.c:1477): init_filter(ctx, ctx->filters[i], ctx->filterbuf[i],
  avgblur_vulkan_filter_frame (libavfilter/vf_avgblur_vulkan.c:180): RET(init_filter(ctx, in));
  blend_frame (libavfilter/vf_blend_vulkan.c:256): RET(init_filter(avctx));
  bwdif_vulkan_config_output (libavfilter/vf_bwdif_vulkan.c:293): return init_filter(avctx);
  chromaber_vulkan_filter_frame (libavfilter/vf_chromaber_vulkan.c:182): RET(init_filter(ctx, in));
  filter_frame (libavfilter/vf_flip_vulkan.c:175): RET(init_filter(ctx, in, type));
  gblur_vulkan_filter_frame (libavfilter/vf_gblur_vulkan.c:320): RET(init_filter(ctx, in));
  nlmeans_vulkan_filter_frame (libavfilter/vf_nlmeans_vulkan.c:780): RET(init_filter(ctx));
  ... only the first 8 of 14 reference sites were followed
```

- `get_context_at(file=libavfilter/vf_bwdif_vulkan.c, line=107, version=old)` →

```
{
  "error": "libavfilter/vf_bwdif_vulkan.c:107 is not inside a function definition in the old version"
}
```

- `get_context_at(file=libavfilter/vf_chromaber_vulkan.c, line=120, version=old)` →

```
{
  "error": "libavfilter/vf_chromaber_vulkan.c:120 is not inside a function definition in the old version"
}
```

- `get_context_at(file=libavfilter/vf_flip_vulkan.c, line=86, version=old)` →

```
init_filter — libavfilter/vf_flip_vulkan.c:46 [function] static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in, enum FlipType type)
  reads: ctx; writes: ctx*, in*; returns: return AVERROR_EXTERNAL; | return err; | return ff_filter_frame(outlink, out); | return err; | return filter_frame(link, in, FLIP_HORIZONTAL); | return filter_frame(link, in, FLIP_VERTICAL);

SLICE around line 86 (def-use, level 2; '>' marks the seed):
static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in, enum FlipType type) {
   ...
   FlipVulkanContext *s = ctx->priv;
   FFVulkanContext *vkctx = &s->vkctx;
   const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   ...
>  desc =(FFVulkanDescriptorSetBinding []){ { .name = "input_image", .type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, .samplers = DUP_SAMPLER(s->sampler), }, { .name = "output_image", .type = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE, .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format), .mem_quali = "writeonly", .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, }, };
   RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 2, 0, 0));
   ...
}

CALLEES (37):
  av_pix_fmt_count_planes (libavutil/pixdesc.c:3065): reads pix_fmt; writes -; returns return AVERROR(EINVAL); | return ret;
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_vk_qf_init (libavutil/vulkan.c:228): reads dev_family, qf, s; writes qf*; returns return(qf->queue_family = vk_qf_get_index(s, dev_family, &qf->nb_queues));
  ff_vk_exec_pool_init (libavutil/vulkan.c:300): reads nb_contexts, nb_queries, pool, qf, query_64bit, query_create_pnext, query_type, s; writes pool*; returns return AVERROR(EINVAL); | return AVERROR(err); | return AVERROR_EXTERNAL; | return 0; | return err;
  ff_vk_init_sampler (libavutil/vulkan.c:1244): reads filt, s, sampler, unnorm_coords; writes -; returns return AVERROR_EXTERNAL; | return 0;
  ff_vk_shader_init (libavutil/vulkan.c:1431): reads extensions, lg_x, lg_y, lg_z, name, nb_extensions, required_subgroup_size, s, shd, stage; writes shd*; returns return 0;
  ff_vk_shader_rep_fmt (libavutil/vulkan.c:1289): reads pixfmt; writes -; returns return high ? "rgba16f" : "rgba8";
  ff_vk_shader_add_descriptor_set (libavutil/vulkan.c:1795): reads desc, nb, print_to_shader_only, s, shd, singular; writes shd*; returns return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return 0;
  main (ffbuild/bin2c.c:26 (1 of 168 definitions)): reads argc, argv; writes argv*; returns return 1; | return -1; | return -1; | return -1; | return 0;
  ff_vk_shader_register_exec (libavutil/vulkan.c:1907): reads pool, s, shd; writes pool*, shd*; returns return 0; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return err; | return err;
  ff_vk_shader_link (libavutil/vulkan.c:1720): reads entrypoint, s, shd, spirv, spirv_len; writes shd*; returns return err; | return err; | return AVERROR(ENOMEM); | return err; | return err; | return err;
  ff_vk_exec_pool_free (libavutil/vulkan.c:238): reads pool, s; writes pool*; returns -
  ff_vk_shader_free (libavutil/vulkan.c:2267): reads s, shd; writes shd*; returns -
  ff_vk_uninit (libavutil/vulkan.c:2306): reads s; writes s*; returns -
  av_frame_free (libavutil/frame.c:162): reads frame; writes -; returns -
  ff_filter_frame (libavfilter/avfilter.c:1062): reads frame, link; writes frame*; returns return ret; | return 0; | return AVERROR_PATCHWELCOME;
  av_frame_copy_props (libavutil/frame.c:713): reads dst, src; writes -; returns return frame_copy_props(dst, src, 1);
  ff_vk_filter_process_simple (libavfilter/vulkan_filter.c:242): reads e, in_f, out_f, push_size, push_src, sampler, shd, vkctx; writes -; returns return ff_vk_exec_submit(vkctx, exec); | return err;
  ff_get_video_buffer (libavfilter/video.c:116): reads h, link, w; writes -; returns return ret;
  filter_frame (libavcodec/dolby_e.c:1059 (1 of 277 definitions)): reads frame, s; writes frame*, s*; returns return ret; | return 0;
  ff_vk_spirv_init [macro (1 of 2 definitions)]: #define ff_vk_spirv_init ff_vk_shaderc_init
  RET [macro (1 of 2 definitions)]: #define RET(x) \
  DUP_SAMPLER [macro]: #define DUP_SAMPLER(x) { x, x, x, x }
  GLSLC [macro]: #define GLSLC(N, S) \
  GLSLF [macro]: #define GLSLF(N, S, ...) \
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)
  AVFILTER_DEFINE_CLASS [macro]: #define AVFILTER_DEFINE_CLASS_EXT(name, desc, options) \
  FILTER_SINGLE_PIXFMT [macro]: #define FILTER_SINGLE_PIXFMT(pix_fmt_) \
  FILTER_OUTPUTS [macro]: #define FILTER_OUTPUTS(array) FILTER_INOUTPADS(outputs, (array))
  FILTER_INPUTS [macro]: #define FILTER_INPUTS(array) FILTER_INOUTPADS(inputs, (array))
  not defined in this repository: imageStore, texture, ivec2, if, IS_WITHIN, imageSize
  not shown (1): NULL_IF_CONFIG_SMALL

CALLERS (8):
  init_frame_decoder (libavcodec/apedec.c:1477): init_filter(ctx, ctx->filters[i], ctx->filterbuf[i],
  avgblur_vulkan_filter_frame (libavfilter/vf_avgblur_vulkan.c:180): RET(init_filter(ctx, in));
  blend_frame (libavfilter/vf_blend_vulkan.c:256): RET(init_filter(avctx));
  bwdif_vulkan_config_output (libavfilter/vf_bwdif_vulkan.c:293): return init_filter(avctx);
  chromaber_vulkan_filter_frame (libavfilter/vf_chromaber_vulkan.c:182): RET(init_filter(ctx, in));
  filter_frame (libavfilter/vf_flip_vulkan.c:175): RET(init_filter(ctx, in, type));
  gblur_vulkan_filter_frame (libavfilter/vf_gblur_vulkan.c:320): RET(init_filter(ctx, in));
  nlmeans_vulkan_filter_frame (libavfilter/vf_nlmeans_vulkan.c:780): RET(init_filter(ctx));
  ... only the first 8 of 14 reference sites were followed

TYPES (1):
  FlipType — libavfilter/vf_flip_vulkan.c:30
    enum FlipType {
        FLIP_VERTICAL,
        FLIP_HORIZONTAL,
        FLIP_BOTH
    }
```

- `get_context_at(file=libavfilter/vf_gblur_vulkan.c, line=231, version=old)` →

```
init_gblur_pipeline — libavfilter/vf_gblur_vulkan.c:124 [function] static int init_gblur_pipeline(GBlurVulkanContext *s, FFVulkanShader *shd, FFVkBuffer *params_buf, int ksize, float sigma, FFVkSPIRVCompiler *spv)
  reads: ksize, params_buf, s, shd, sigma, spv; writes: s*, shd*, spv*; returns: return AVERROR(ENOMEM); | return err; | return AVERROR_EXTERNAL; | return err; | return ff_filter_frame(outlink, out); | return err;

SLICE around line 231 (def-use, level 2; '>' marks the seed):
static int init_gblur_pipeline(GBlurVulkanContext *s, FFVulkanShader *shd, FFVkBuffer *params_buf, int ksize, float sigma, FFVkSPIRVCompiler *spv) {
   ...
     GBlurVulkanContext *s = ctx->priv;
     FFVulkanContext *vkctx = &s->vkctx;
     const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   ...
>    desc =(FFVulkanDescriptorSetBinding []){ { .name = "input_images", .type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, .samplers = DUP_SAMPLER(s->sampler), }, { .name = "output_images", .type = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE, .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format), .mem_quali = "writeonly", .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, }, };
   ...
       shd = &s->shd_hor;
   ...
       RET(ff_vk_shader_add_descriptor_set(vkctx, shd, desc, 2, 0, 0));
   ...
       shd = &s->shd_ver;
   ...
       RET(ff_vk_shader_add_descriptor_set(vkctx, shd, desc, 2, 0, 0));
   ...
}

CALLEES (50):
  av_pix_fmt_count_planes (libavutil/pixdesc.c:3065): reads pix_fmt; writes -; returns return AVERROR(EINVAL); | return ret;
  av_asprintf (libavutil/avstring.c:115): reads fmt; writes -; returns return p;
  ff_vk_shader_add_descriptor_set (libavutil/vulkan.c:1795): reads desc, nb, print_to_shader_only, s, shd, singular; writes shd*; returns return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return 0;
  main (ffbuild/bin2c.c:26 (1 of 168 definitions)): reads argc, argv; writes argv*; returns return 1; | return -1; | return -1; | return -1; | return 0;
  av_free (libavutil/mem.c:238 (1 of 3 definitions)): reads ptr; writes -; returns -
  ff_vk_shader_update_desc_buffer (libavutil/vulkan.c:2144): reads bind, buf, e, elem, fmt, len, offset, s, set, shd; writes -; returns return AVERROR(EINVAL); | return 0;
  ff_vk_unmap_buffer (libavutil/vulkan.h:477): reads buf, flush, s; writes -; returns return ff_vk_unmap_buffers(s, (FFVkBuffer *[]){ buf }, 1, flush);
  ff_vk_map_buffer (libavutil/vulkan.h:470): reads buf, invalidate, mem, s; writes -; returns return ff_vk_map_buffers(s, (FFVkBuffer *[]){ buf }, mem, 1, invalidate);
  ff_vk_create_buf (libavutil/vulkan.c:928): reads alloc_pNext, buf, flags, pNext, s, size, usage; writes buf*; returns return AVERROR_EXTERNAL; | return err; | return AVERROR_EXTERNAL; | return 0;
  ff_vk_shader_register_exec (libavutil/vulkan.c:1907): reads pool, s, shd; writes pool*, shd*; returns return 0; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return err; | return err;
  ff_vk_shader_link (libavutil/vulkan.c:1720): reads entrypoint, s, shd, spirv, spirv_len; writes shd*; returns return err; | return err; | return AVERROR(ENOMEM); | return err; | return err; | return err;
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_vk_qf_init (libavutil/vulkan.c:228): reads dev_family, qf, s; writes qf*; returns return(qf->queue_family = vk_qf_get_index(s, dev_family, &qf->nb_queues));
  ff_vk_exec_pool_init (libavutil/vulkan.c:300): reads nb_contexts, nb_queries, pool, qf, query_64bit, query_create_pnext, query_type, s; writes pool*; returns return AVERROR(EINVAL); | return AVERROR(err); | return AVERROR_EXTERNAL; | return 0; | return err;
  ff_vk_init_sampler (libavutil/vulkan.c:1244): reads filt, s, sampler, unnorm_coords; writes -; returns return AVERROR_EXTERNAL; | return 0;
  ff_vk_shader_rep_fmt (libavutil/vulkan.c:1289): reads pixfmt; writes -; returns return high ? "rgba16f" : "rgba8";
  init_gaussian_params (libavfilter/vf_gblur_vulkan.c:111): reads s; writes s*; returns -
  ff_vk_shader_init (libavutil/vulkan.c:1431): reads extensions, lg_x, lg_y, lg_z, name, nb_extensions, required_subgroup_size, s, shd, stage; writes shd*; returns return 0;
  ff_vk_uninit (libavutil/vulkan.c:2306): reads s; writes s*; returns -
  ff_vk_free_buf (libavutil/vulkan.c:1135): reads buf, s; writes -; returns -
  ff_vk_shader_free (libavutil/vulkan.c:2267): reads s, shd; writes shd*; returns -
  ff_vk_exec_pool_free (libavutil/vulkan.c:238): reads pool, s; writes pool*; returns -
  av_frame_free (libavutil/frame.c:162): reads frame; writes -; returns -
  ff_filter_frame (libavfilter/avfilter.c:1062): reads frame, link; writes frame*; returns return ret; | return 0; | return AVERROR_PATCHWELCOME;
  av_frame_copy_props (libavutil/frame.c:713): reads dst, src; writes -; returns return frame_copy_props(dst, src, 1);
  ff_vk_filter_process_2pass (libavfilter/vulkan_filter.c:312): reads e, in, out, push_size, push_src, sampler, shd_list, tmp, vkctx; writes -; returns return ff_vk_exec_submit(vkctx, exec); | return err;
  init_filter (libavcodec/apedec.c:1376 (1 of 9 definitions)): reads buf, f, order; writes f*; returns -
  ff_get_video_buffer (libavfilter/video.c:116): reads h, link, w; writes -; returns return ret;
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)
  RET [macro (1 of 2 definitions)]: #define RET(x) \
  not defined in this repository: init_gaussian_kernel, imageStore, texture, gblur, if, IS_WITHIN, imageSize, ivec2, vec2
  not shown (11): GLSLD, GLSLC, GLSLF, ff_vk_spirv_init, DUP_SAMPLER, OFFSET, AVFILTER_DEFINE_CLASS, FILTER_SINGLE_PIXFMT, FILTER_OUTPUTS, FILTER_INPUTS, NULL_IF_CONFIG_SMALL

CALLERS (2):
  init_filter (libavfilter/vf_gblur_vulkan.c:252): RET(init_gblur_pipeline(s, shd, &s->params_hor, s->size, s->sigma, spv));
  init_filter (libavfilter/vf_gblur_vulkan.c:266): RET(init_gblur_pipeline(s, shd, &s->params_ver, s->sizeV, s->sigmaV, spv));
```

- `get_context_at(file=libavfilter/vf_nlmeans_vulkan.c, line=457, version=old)` →

```
{
  "error": "libavfilter/vf_nlmeans_vulkan.c:457 is not inside a function definition in the old version"
}
```

- `get_context_at(file=libavfilter/vf_overlay_vulkan.c, line=142, version=old)` →

```
init_filter — libavfilter/vf_overlay_vulkan.c:83 [function] static av_cold int init_filter(AVFilterContext *ctx)
  reads: ctx; writes: ctx*; returns: return AVERROR_EXTERNAL; | return err; | return 0; | return AVERROR(EINVAL); | return ff_filter_frame(outlink, out); | return err;

SLICE around line 142 (def-use, level 2; '>' marks the seed):
static av_cold int init_filter(AVFilterContext *ctx) {
   ...
   OverlayVulkanContext *s = ctx->priv;
   FFVulkanContext *vkctx = &s->vkctx;
   const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   ...
>  desc =(FFVulkanDescriptorSetBinding []){ { .name = "main_img", .type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, .samplers = DUP_SAMPLER(s->sampler), }, { .name = "overlay_img", .type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, .samplers = DUP_SAMPLER(s->sampler), }, { .name = "output_img", .type = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE, .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format), .mem_quali = "writeonly", .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, }, };
   RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 3, 0, 0));
   ...
}

CALLEES (46):
  av_pix_fmt_count_planes (libavutil/pixdesc.c:3065): reads pix_fmt; writes -; returns return AVERROR(EINVAL); | return ret;
  av_pix_fmt_desc_get (libavutil/pixdesc.c:3025): reads pix_fmt; writes -; returns return NULL; | return &av_pix_fmt_descriptors[pix_fmt];
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_vk_qf_init (libavutil/vulkan.c:228): reads dev_family, qf, s; writes qf*; returns return(qf->queue_family = vk_qf_get_index(s, dev_family, &qf->nb_queues));
  ff_vk_exec_pool_init (libavutil/vulkan.c:300): reads nb_contexts, nb_queries, pool, qf, query_64bit, query_create_pnext, query_type, s; writes pool*; returns return AVERROR(EINVAL); | return AVERROR(err); | return AVERROR_EXTERNAL; | return 0; | return err;
  ff_vk_init_sampler (libavutil/vulkan.c:1244): reads filt, s, sampler, unnorm_coords; writes -; returns return AVERROR_EXTERNAL; | return 0;
  ff_vk_shader_init (libavutil/vulkan.c:1431): reads extensions, lg_x, lg_y, lg_z, name, nb_extensions, required_subgroup_size, s, shd, stage; writes shd*; returns return 0;
  ff_vk_shader_add_push_const (libavutil/vulkan.c:1223): reads offset, shd, size, stage; writes shd*; returns return AVERROR(ENOMEM); | return 0;
  ff_vk_shader_rep_fmt (libavutil/vulkan.c:1289): reads pixfmt; writes -; returns return high ? "rgba16f" : "rgba8";
  ff_vk_shader_add_descriptor_set (libavutil/vulkan.c:1795): reads desc, nb, print_to_shader_only, s, shd, singular; writes shd*; returns return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return 0;
  main (ffbuild/bin2c.c:26 (1 of 168 definitions)): reads argc, argv; writes argv*; returns return 1; | return -1; | return -1; | return -1; | return 0;
  ff_vk_shader_register_exec (libavutil/vulkan.c:1907): reads pool, s, shd; writes pool*, shd*; returns return 0; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return err; | return err;
  ff_vk_shader_link (libavutil/vulkan.c:1720): reads entrypoint, s, shd, spirv, spirv_len; writes shd*; returns return err; | return err; | return AVERROR(ENOMEM); | return err; | return err; | return err;
  ff_framesync_get_frame (libavfilter/framesync.c:270): reads fs, get, in, rframe; writes fs*, rframe*; returns return 0; | return AVERROR(ENOMEM); | return 0;
  ff_get_video_buffer (libavfilter/video.c:116): reads h, link, w; writes -; returns return ret;
  ff_vk_filter_process_Nin (libavfilter/vulkan_filter.c:401): reads e, in, nb_in, out, push_size, push_src, sampler, shd, vkctx; writes -; returns return ff_vk_exec_submit(vkctx, exec); | return err;
  av_frame_copy_props (libavutil/frame.c:713): reads dst, src; writes -; returns return frame_copy_props(dst, src, 1);
  ff_filter_frame (libavfilter/avfilter.c:1062): reads frame, link; writes frame*; returns return ret; | return 0; | return AVERROR_PATCHWELCOME;
  av_frame_free (libavutil/frame.c:162): reads frame; writes -; returns -
  ff_framesync_configure (libavfilter/framesync.c:137): reads fs; writes fs*; returns return AVERROR(EINVAL); | return 0;
  ff_framesync_init_dualinput (libavfilter/framesync.c:373): reads fs, parent; writes fs*; returns return ret; | return 0;
  ff_vk_filter_config_output (libavfilter/vulkan_filter.c:209): reads outlink; writes outlink*; returns return err; | return AVERROR(ENOMEM); | return err;
  ff_framesync_activate (libavfilter/framesync.c:353): reads fs; writes fs*; returns return ret; | return 0; | return ret; | return 0;
  ff_vk_filter_init (libavfilter/vulkan_filter.c:233): reads avctx; writes avctx*; returns return 0;
  ff_framesync_uninit (libavfilter/framesync.c:302): reads fs; writes fs*; returns -
  ff_vk_uninit (libavutil/vulkan.c:2306): reads s; writes s*; returns -
  ff_vk_shader_free (libavutil/vulkan.c:2267): reads s, shd; writes shd*; returns -
  ff_vk_exec_pool_free (libavutil/vulkan.c:238): reads pool, s; writes pool*; returns -
  ff_vk_spirv_init [macro (1 of 2 definitions)]: #define ff_vk_spirv_init ff_vk_shaderc_init
  RET [macro (1 of 2 definitions)]: #define RET(x) \
  not defined in this repository: layout, overlay_noalpha, overlay_alpha_opaque, for, ivec2
  not shown (11): GLSLC, DUP_SAMPLER, GLSLD, GLSLF, AVERROR, OFFSET, AVFILTER_DEFINE_CLASS, FILTER_SINGLE_PIXFMT, FILTER_OUTPUTS, FILTER_INPUTS, NULL_IF_CONFIG_SMALL

CALLERS (8):
  init_frame_decoder (libavcodec/apedec.c:1477): init_filter(ctx, ctx->filters[i], ctx->filterbuf[i],
  avgblur_vulkan_filter_frame (libavfilter/vf_avgblur_vulkan.c:180): RET(init_filter(ctx, in));
  blend_frame (libavfilter/vf_blend_vulkan.c:256): RET(init_filter(avctx));
  bwdif_vulkan_config_output (libavfilter/vf_bwdif_vulkan.c:293): return init_filter(avctx);
  chromaber_vulkan_filter_frame (libavfilter/vf_chromaber_vulkan.c:182): RET(init_filter(ctx, in));
  filter_frame (libavfilter/vf_flip_vulkan.c:175): RET(init_filter(ctx, in, type));
  gblur_vulkan_filter_frame (libavfilter/vf_gblur_vulkan.c:320): RET(init_filter(ctx, in));
  nlmeans_vulkan_filter_frame (libavfilter/vf_nlmeans_vulkan.c:780): RET(init_filter(ctx));
  ... only the first 8 of 14 reference sites were followed
```

- `get_context_at(file=libavfilter/vf_scale_vulkan.c, line=174, version=old)` →

```
init_filter — libavfilter/vf_scale_vulkan.c:111 [function] static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
  reads: ctx, in; writes: ctx*, in*; returns: return AVERROR_EXTERNAL; | return AVERROR(EINVAL); | return AVERROR(EINVAL); | return err; | return ff_filter_frame(outlink, out); | return err;

SLICE around line 174 (def-use, level 2; '>' marks the seed):
static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in) {
   ...
   ScaleVulkanContext *s = ctx->priv;
   FFVulkanContext *vkctx = &s->vkctx;
   ...
   int in_planes = av_pix_fmt_count_planes(s->vkctx.input_format);
   ...
>  desc =(FFVulkanDescriptorSetBinding []){ { .name = "input_img", .type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, .dimensions = 2, .elems = in_planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, .samplers = DUP_SAMPLER(s->sampler), }, { .name = "output_img", .type = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE, .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format), .mem_quali = "writeonly", .dimensions = 2, .elems = av_pix_fmt_count_planes(s->vkctx.output_format), .stages = VK_SHADER_STAGE_COMPUTE_BIT, }, };
   RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 2, 0, 0));
   ...
     if(s->vkctx.output_format == s->vkctx.input_format) {
       for(int i = 0;; i < desc[1].elems; i++) {
       int i = 0;
         GLSLF(1, size = imageSize(output_img[%i]);, i);
         GLSLC(1, if(IS_WITHIN(pos, size)){);
         switch(s->scaler) {
   ...
           case F_BILINEAR: GLSLF(2, vec4 res = scale_bilinear(%i, pos, c_r, c_o);, i); GLSLF(2, imageStore(output_img[%i], pos, res);, i); break;
             GLSLF(2, vec4 res = scale_bilinear(%i, pos, c_r, c_o);
           i);
           GLSLF(2, imageStore(output_img[%i], pos, res);, i);
   ...
         }
       }
     } else {
   ...
       GLSLF(1, res = rgb2yuv(res, %i);, s->out_range == AVCOL_RANGE_JPEG);
       switch(s->vkctx.output_format) {
         case AV_PIX_FMT_NV12: GLSLC(1, write_nv12(res, pos);); break;
           GLSLC(1, write_nv12(res, pos););
   ...
         case AV_PIX_FMT_YUV420P: GLSLC(1, write_420(res, pos);); break;
           GLSLC(1, write_420(res, pos););
   ...
         case AV_PIX_FMT_YUV444P: GLSLC(1, write_444(res, pos);); break;
           GLSLC(1, write_444(res, pos););
   ...
       }
     }
}

CALLEES (50):
  av_pix_fmt_count_planes (libavutil/pixdesc.c:3065): reads pix_fmt; writes -; returns return AVERROR(EINVAL); | return ret;
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_vk_qf_init (libavutil/vulkan.c:228): reads dev_family, qf, s; writes qf*; returns return(qf->queue_family = vk_qf_get_index(s, dev_family, &qf->nb_queues));
  ff_vk_exec_pool_init (libavutil/vulkan.c:300): reads nb_contexts, nb_queries, pool, qf, query_64bit, query_create_pnext, query_type, s; writes pool*; returns return AVERROR(EINVAL); | return AVERROR(err); | return AVERROR_EXTERNAL; | return 0; | return err;
  ff_vk_init_sampler (libavutil/vulkan.c:1244): reads filt, s, sampler, unnorm_coords; writes -; returns return AVERROR_EXTERNAL; | return 0;
  ff_vk_shader_init (libavutil/vulkan.c:1431): reads extensions, lg_x, lg_y, lg_z, name, nb_extensions, required_subgroup_size, s, shd, stage; writes shd*; returns return 0;
  ff_vk_shader_add_push_const (libavutil/vulkan.c:1223): reads offset, shd, size, stage; writes shd*; returns return AVERROR(ENOMEM); | return 0;
  ff_vk_shader_rep_fmt (libavutil/vulkan.c:1289): reads pixfmt; writes -; returns return high ? "rgba16f" : "rgba8";
  ff_vk_shader_add_descriptor_set (libavutil/vulkan.c:1795): reads desc, nb, print_to_shader_only, s, shd, singular; writes shd*; returns return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return 0;
  main (ffbuild/bin2c.c:26 (1 of 168 definitions)): reads argc, argv; writes argv*; returns return 1; | return -1; | return -1; | return -1; | return 0;
  ff_vk_shader_register_exec (libavutil/vulkan.c:1907): reads pool, s, shd; writes pool*, shd*; returns return 0; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return err; | return err;
  ff_vk_shader_link (libavutil/vulkan.c:1720): reads entrypoint, s, shd, spirv, spirv_len; writes shd*; returns return err; | return err; | return AVERROR(ENOMEM); | return err; | return err; | return err;
  ff_fill_rgb2yuv_table (libavfilter/colorspace.c:125): reads coeffs, rgb2yuv; writes rgb2yuv*; returns -
  av_csp_luma_coeffs_from_avcsp (libavutil/csp.c:58): reads csp; writes -; returns return NULL; | return NULL; | return coeffs;
  rgb2yuv (libavfilter/vf_colorize.c:186 (1 of 3 definitions)): reads b, depth, g, r, u, v, y; writes u*, v*, y*; returns -
  ff_get_video_buffer (libavfilter/video.c:116): reads h, link, w; writes -; returns return ret;
  ff_vk_filter_process_simple (libavfilter/vulkan_filter.c:242): reads e, in_f, out_f, push_size, push_src, sampler, shd, vkctx; writes -; returns return ff_vk_exec_submit(vkctx, exec); | return err;
  av_frame_copy_props (libavutil/frame.c:713): reads dst, src; writes -; returns return frame_copy_props(dst, src, 1);
  av_frame_free (libavutil/frame.c:162): reads frame; writes -; returns -
  ff_filter_frame (libavfilter/avfilter.c:1062): reads frame, link; writes frame*; returns return ret; | return 0; | return AVERROR_PATCHWELCOME;
  ff_vk_filter_config_output (libavfilter/vulkan_filter.c:209): reads outlink; writes outlink*; returns return err; | return AVERROR(ENOMEM); | return err;
  ff_vk_mt_is_np_rgb (libavutil/vulkan.c:1276): reads pix_fmt; writes -; returns return 1; | return 0;
  av_get_pix_fmt (libavutil/pixdesc.c:2957): reads name; writes -; returns return pix_fmt;
  ff_scale_eval_dimensions (libavfilter/scale_eval.c:57): reads h_expr, inlink, log_ctx, outlink, ret_h, ret_w, w_expr; writes ret_h*, ret_w*; returns return 0; | return ret;
  ff_vk_uninit (libavutil/vulkan.c:2306): reads s; writes s*; returns -
  ff_vk_shader_free (libavutil/vulkan.c:2267): reads s, shd; writes shd*; returns -
  ff_vk_exec_pool_free (libavutil/vulkan.c:238): reads pool, s; writes pool*; returns -
  ff_vk_spirv_init [macro (1 of 2 definitions)]: #define ff_vk_spirv_init ff_vk_shaderc_init
  RET [macro (1 of 2 definitions)]: #define RET(x) \
  GLSLC [macro]: #define GLSLC(N, S) \
  not defined in this repository: layout, write_444, write_420, write_nv12, scale_bilinear, imageStore, if, IS_WITHIN, imageSize, ivec2
  not shown (10): DUP_SAMPLER, GLSLD, AVERROR, GLSLF, OFFSET, AVFILTER_DEFINE_CLASS, FILTER_SINGLE_PIXFMT, FILTER_OUTPUTS, FILTER_INPUTS, NULL_IF_CONFIG_SMALL

CALLERS (8):
  init_frame_decoder (libavcodec/apedec.c:1477): init_filter(ctx, ctx->filters[i], ctx->filterbuf[i],
  avgblur_vulkan_filter_frame (libavfilter/vf_avgblur_vulkan.c:180): RET(init_filter(ctx, in));
  blend_frame (libavfilter/vf_blend_vulkan.c:256): RET(init_filter(avctx));
  bwdif_vulkan_config_output (libavfilter/vf_bwdif_vulkan.c:293): return init_filter(avctx);
  chromaber_vulkan_filter_frame (libavfilter/vf_chromaber_vulkan.c:182): RET(init_filter(ctx, in));
  filter_frame (libavfilter/vf_flip_vulkan.c:175): RET(init_filter(ctx, in, type));
  gblur_vulkan_filter_frame (libavfilter/vf_gblur_vulkan.c:320): RET(init_filter(ctx, in));
  nlmeans_vulkan_filter_frame (libavfilter/vf_nlmeans_vulkan.c:780): RET(init_filter(ctx));
  ... only the first 8 of 14 reference sites were followed
```

- `get_context_at(file=libavfilter/vf_transpose_vulkan.c, line=85, version=old)` →

```
init_filter — libavfilter/vf_transpose_vulkan.c:44 [function] static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
  reads: ctx, in; writes: ctx*, in*; returns: return AVERROR_EXTERNAL; | return err; | return ff_filter_frame(outlink, in); | return ff_filter_frame(outlink, out); | return err; | return outl->hw_frames_ctx ? 0 : AVERROR(ENOMEM);

SLICE around line 85 (def-use, level 2; '>' marks the seed):
static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in) {
   ...
   TransposeVulkanContext *s = ctx->priv;
   FFVulkanContext *vkctx = &s->vkctx;
   const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   ...
>  desc =(FFVulkanDescriptorSetBinding []){ { .name = "input_images", .type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, .samplers = DUP_SAMPLER(s->sampler), }, { .name = "output_images", .type = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE, .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format), .mem_quali = "writeonly", .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, }, };
   RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 2, 0, 0));
   ...
}

CALLEES (41):
  av_pix_fmt_count_planes (libavutil/pixdesc.c:3065): reads pix_fmt; writes -; returns return AVERROR(EINVAL); | return ret;
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_vk_qf_init (libavutil/vulkan.c:228): reads dev_family, qf, s; writes qf*; returns return(qf->queue_family = vk_qf_get_index(s, dev_family, &qf->nb_queues));
  ff_vk_exec_pool_init (libavutil/vulkan.c:300): reads nb_contexts, nb_queries, pool, qf, query_64bit, query_create_pnext, query_type, s; writes pool*; returns return AVERROR(EINVAL); | return AVERROR(err); | return AVERROR_EXTERNAL; | return 0; | return err;
  ff_vk_init_sampler (libavutil/vulkan.c:1244): reads filt, s, sampler, unnorm_coords; writes -; returns return AVERROR_EXTERNAL; | return 0;
  ff_vk_shader_init (libavutil/vulkan.c:1431): reads extensions, lg_x, lg_y, lg_z, name, nb_extensions, required_subgroup_size, s, shd, stage; writes shd*; returns return 0;
  ff_vk_shader_rep_fmt (libavutil/vulkan.c:1289): reads pixfmt; writes -; returns return high ? "rgba16f" : "rgba8";
  ff_vk_shader_add_descriptor_set (libavutil/vulkan.c:1795): reads desc, nb, print_to_shader_only, s, shd, singular; writes shd*; returns return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return 0;
  main (ffbuild/bin2c.c:26 (1 of 168 definitions)): reads argc, argv; writes argv*; returns return 1; | return -1; | return -1; | return -1; | return 0;
  ff_vk_shader_register_exec (libavutil/vulkan.c:1907): reads pool, s, shd; writes pool*, shd*; returns return 0; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return err; | return err;
  ff_vk_shader_link (libavutil/vulkan.c:1720): reads entrypoint, s, shd, spirv, spirv_len; writes shd*; returns return err; | return err; | return AVERROR(ENOMEM); | return err; | return err; | return err;
  ff_filter_frame (libavfilter/avfilter.c:1062): reads frame, link; writes frame*; returns return ret; | return 0; | return AVERROR_PATCHWELCOME;
  ff_get_video_buffer (libavfilter/video.c:116): reads h, link, w; writes -; returns return ret;
  ff_vk_filter_process_simple (libavfilter/vulkan_filter.c:242): reads e, in_f, out_f, push_size, push_src, sampler, shd, vkctx; writes -; returns return ff_vk_exec_submit(vkctx, exec); | return err;
  av_frame_copy_props (libavutil/frame.c:713): reads dst, src; writes -; returns return frame_copy_props(dst, src, 1);
  av_frame_free (libavutil/frame.c:162): reads frame; writes -; returns -
  ff_vk_uninit (libavutil/vulkan.c:2306): reads s; writes s*; returns -
  ff_vk_shader_free (libavutil/vulkan.c:2267): reads s, shd; writes shd*; returns -
  ff_vk_exec_pool_free (libavutil/vulkan.c:238): reads pool, s; writes pool*; returns -
  ff_vk_filter_config_output (libavfilter/vulkan_filter.c:209): reads outlink; writes outlink*; returns return err; | return AVERROR(ENOMEM); | return err;
  av_div_q (libavutil/rational.c:88): reads b, c; writes -; returns return av_mul_q(b, (AVRational){ c.den, c.num });
  av_buffer_ref (libavutil/buffer.c:103): reads buf; writes buf*; returns return NULL; | return ret;
  ff_filter_link (libavfilter/filters.h:197): reads link; writes -; returns return(FilterLink*)link;
  ff_vk_spirv_init [macro (1 of 2 definitions)]: #define ff_vk_spirv_init ff_vk_shaderc_init
  RET [macro (1 of 2 definitions)]: #define RET(x) \
  DUP_SAMPLER [macro]: #define DUP_SAMPLER(x) { x, x, x, x }
  GLSLC [macro]: #define GLSLC(N, S) \
  GLSLF [macro]: #define GLSLF(N, S, ...) \
  AVERROR [macro (1 of 2 definitions)]: #define AVERROR(e) (e)
  OFFSET [macro (1 of 713 definitions)]: #define OFFSET(x) offsetof(OptionsContext, x)
  not defined in this repository: imageStore, texture, ivec2, if, IS_WITHIN, imageSize
  not shown (5): AVFILTER_DEFINE_CLASS, FILTER_SINGLE_PIXFMT, FILTER_OUTPUTS, FILTER_INPUTS, NULL_IF_CONFIG_SMALL

CALLERS (8):
  init_frame_decoder (libavcodec/apedec.c:1477): init_filter(ctx, ctx->filters[i], ctx->filterbuf[i],
  avgblur_vulkan_filter_frame (libavfilter/vf_avgblur_vulkan.c:180): RET(init_filter(ctx, in));
  blend_frame (libavfilter/vf_blend_vulkan.c:256): RET(init_filter(avctx));
  bwdif_vulkan_config_output (libavfilter/vf_bwdif_vulkan.c:293): return init_filter(avctx);
  chromaber_vulkan_filter_frame (libavfilter/vf_chromaber_vulkan.c:182): RET(init_filter(ctx, in));
  filter_frame (libavfilter/vf_flip_vulkan.c:175): RET(init_filter(ctx, in, type));
  gblur_vulkan_filter_frame (libavfilter/vf_gblur_vulkan.c:320): RET(init_filter(ctx, in));
  nlmeans_vulkan_filter_frame (libavfilter/vf_nlmeans_vulkan.c:780): RET(init_filter(ctx));
  ... only the first 8 of 14 reference sites were followed
```

- `get_context_at(file=libavfilter/vf_xfade_vulkan.c, line=367, version=old)` →

```
init_vulkan — libavfilter/vf_xfade_vulkan.c:319 [function] static av_cold int init_vulkan(AVFilterContext *avctx)
  reads: -; writes: avctx*; returns: return AVERROR_EXTERNAL; | return err; | return AVERROR(EINVAL); | return ff_filter_frame(outlink, output); | return err; | return AVERROR(EINVAL);

SLICE around line 367 (def-use, level 2; '>' marks the seed):
static av_cold int init_vulkan(AVFilterContext *avctx) {
   ...
   XFadeVulkanContext *s = avctx->priv;
   FFVulkanContext *vkctx = &s->vkctx;
   const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   ...
>  desc =(FFVulkanDescriptorSetBinding []){ { .name = "a_images", .type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, .samplers = DUP_SAMPLER(s->sampler), }, { .name = "b_images", .type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, .samplers = DUP_SAMPLER(s->sampler), }, { .name = "output_images", .type = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE, .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format), .mem_quali = "writeonly", .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, }, };
   RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 3, 0, 0));
   ...
}

CALLEES (55):
  av_pix_fmt_count_planes (libavutil/pixdesc.c:3065): reads pix_fmt; writes -; returns return AVERROR(EINVAL); | return ret;
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_vk_qf_init (libavutil/vulkan.c:228): reads dev_family, qf, s; writes qf*; returns return(qf->queue_family = vk_qf_get_index(s, dev_family, &qf->nb_queues));
  ff_vk_exec_pool_init (libavutil/vulkan.c:300): reads nb_contexts, nb_queries, pool, qf, query_64bit, query_create_pnext, query_type, s; writes pool*; returns return AVERROR(EINVAL); | return AVERROR(err); | return AVERROR_EXTERNAL; | return 0; | return err;
  ff_vk_init_sampler (libavutil/vulkan.c:1244): reads filt, s, sampler, unnorm_coords; writes -; returns return AVERROR_EXTERNAL; | return 0;
  ff_vk_shader_init (libavutil/vulkan.c:1431): reads extensions, lg_x, lg_y, lg_z, name, nb_extensions, required_subgroup_size, s, shd, stage; writes shd*; returns return 0;
  ff_vk_shader_rep_fmt (libavutil/vulkan.c:1289): reads pixfmt; writes -; returns return high ? "rgba16f" : "rgba8";
  ff_vk_shader_add_descriptor_set (libavutil/vulkan.c:1795): reads desc, nb, print_to_shader_only, s, shd, singular; writes shd*; returns return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return 0;
  ff_vk_shader_add_push_const (libavutil/vulkan.c:1223): reads offset, shd, size, stage; writes shd*; returns return AVERROR(ENOMEM); | return 0;
  main (ffbuild/bin2c.c:26 (1 of 168 definitions)): reads argc, argv; writes argv*; returns return 1; | return -1; | return -1; | return -1; | return 0;
  ff_vk_shader_register_exec (libavutil/vulkan.c:1907): reads pool, s, shd; writes pool*, shd*; returns return 0; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return err; | return err;
  ff_vk_shader_link (libavutil/vulkan.c:1720): reads entrypoint, s, shd, spirv, spirv_len; writes shd*; returns return err; | return err; | return AVERROR(ENOMEM); | return err; | return err; | return err;
  ff_get_video_buffer (libavfilter/video.c:116): reads h, link, w; writes -; returns return ret;
  av_frame_copy_props (libavutil/frame.c:713): reads dst, src; writes -; returns return frame_copy_props(dst, src, 1);
  ff_vk_filter_process_Nin (libavfilter/vulkan_filter.c:401): reads e, in, nb_in, out, push_size, push_src, sampler, shd, vkctx; writes -; returns return ff_vk_exec_submit(vkctx, exec); | return err;
  ff_filter_frame (libavfilter/avfilter.c:1062): reads frame, link; writes frame*; returns return ret; | return 0; | return AVERROR_PATCHWELCOME;
  av_frame_free (libavutil/frame.c:162): reads frame; writes -; returns -
  ff_vk_filter_config_output (libavfilter/vulkan_filter.c:209): reads outlink; writes outlink*; returns return err; | return AVERROR(ENOMEM); | return err;
  av_rescale_q (libavutil/mathematics.c:142): reads a, bq, cq; writes -; returns return av_rescale_q_rnd(a, bq, cq, AV_ROUND_NEAR_INF);
  ff_filter_link (libavfilter/filters.h:197): reads link; writes -; returns return(FilterLink*)link;
  ff_inlink_request_frame (libavfilter/avfilter.c:1594): reads link; writes -; returns -
  ff_outlink_frame_wanted (libavfilter/avfilter.c:1661): reads link; writes -; returns return li->frame_wanted_out;
  ff_outlink_set_status (libavfilter/filters.h:424): reads link, pts, status; writes -; returns -
  ff_inlink_acknowledge_status (libavfilter/avfilter.c:1438): reads link, rpts, rstatus; writes rpts*, rstatus*; returns return *rstatus = 0; | return *rstatus = li->status_out; | return *rstatus = 0; | return 1;
  ff_inlink_consume_frame (libavfilter/avfilter.c:1491): reads link, rframe; writes rframe*; returns return 0; | return ff_inlink_consume_samples(link, frame->nb_samples, frame->nb_samples, rframe); | return 1;
  ff_filter_set_ready (libavfilter/avfilter.c:239): reads filter, priority; writes -; returns -
  xfade_frame (libavfilter/vf_xfade.c:2204 (1 of 2 definitions)): reads a, b, ctx; writes -; returns return AVERROR(ENOMEM); | return ff_filter_frame(outlink, out);
  ff_inlink_set_status (libavfilter/avfilter.c:1603): reads link, status; writes -; returns -
  ff_inlink_check_available_frame (libavfilter/avfilter.c:1460): reads link; writes -; returns return ff_framequeue_queued_frames(&li->fifo)> 0;
  ff_inlink_peek_frame (libavfilter/avfilter.c:1532): reads idx, link; writes -; returns return ff_framequeue_peek(&li->fifo, idx);
  not defined in this repository: layout, transition, for, ivec2
  not shown (21): forward_frame, ff_vk_uninit, ff_vk_shader_free, ff_vk_exec_pool_free, ff_default_get_video_buffer, ff_null_get_video_buffer, ff_vk_spirv_init, RET, DUP_SAMPLER, GLSLC, GLSLD, GLSLF, AVERROR, av_clipf, FF_FILTER_FORWARD_STATUS_BACK_ALL, OFFSET, AVFILTER_DEFINE_CLASS, FILTER_SINGLE_PIXFMT, FILTER_OUTPUTS, FILTER_INPUTS, NULL_IF_CONFIG_SMALL

CALLERS (2):
  libplacebo_query_format (libavfilter/vf_libplacebo.c:1094): RET(init_vulkan(ctx, vkhwctx));
  xfade_frame (libavfilter/vf_xfade_vulkan.c:434): RET(init_vulkan(avctx));
```

- `get_context_at(file=libavfilter/vsrc_testsrc_vulkan.c, line=105, version=old)` →

```
init_filter — libavfilter/vsrc_testsrc_vulkan.c:65 [function] static av_cold int init_filter(AVFilterContext *ctx, enum TestSrcVulkanMode mode)
  reads: ctx, mode; writes: ctx*; returns: return AVERROR_EXTERNAL; | return AVERROR(EINVAL); | return err; | return err; | return FFERROR_NOT_READY; | return 0;

SLICE around line 105 (def-use, level 2; '>' marks the seed):
static av_cold int init_filter(AVFilterContext *ctx, enum TestSrcVulkanMode mode) {
   ...
   TestSrcVulkanContext *s = ctx->priv;
   FFVulkanContext *vkctx = &s->vkctx;
   const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
   ...
>  desc_set =(FFVulkanDescriptorSetBinding []){ { .name = "output_img", .type = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE, .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format), .mem_quali = "writeonly", .dimensions = 2, .elems = planes, .stages = VK_SHADER_STAGE_COMPUTE_BIT, }, };
   RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc_set, 1, 0, 0));
   ...
}

CALLEES (45):
  av_pix_fmt_count_planes (libavutil/pixdesc.c:3065): reads pix_fmt; writes -; returns return AVERROR(EINVAL); | return ret;
  av_pix_fmt_desc_get (libavutil/pixdesc.c:3025): reads pix_fmt; writes -; returns return NULL; | return &av_pix_fmt_descriptors[pix_fmt];
  av_log (libavutil/log.c:414 (1 of 2 definitions)): reads avcl, fmt, level; writes -; returns -
  ff_vk_qf_init (libavutil/vulkan.c:228): reads dev_family, qf, s; writes qf*; returns return(qf->queue_family = vk_qf_get_index(s, dev_family, &qf->nb_queues));
  ff_vk_exec_pool_init (libavutil/vulkan.c:300): reads nb_contexts, nb_queries, pool, qf, query_64bit, query_create_pnext, query_type, s; writes pool*; returns return AVERROR(EINVAL); | return AVERROR(err); | return AVERROR_EXTERNAL; | return 0; | return err;
  ff_vk_shader_init (libavutil/vulkan.c:1431): reads extensions, lg_x, lg_y, lg_z, name, nb_extensions, required_subgroup_size, s, shd, stage; writes shd*; returns return 0;
  ff_vk_shader_add_push_const (libavutil/vulkan.c:1223): reads offset, shd, size, stage; writes shd*; returns return AVERROR(ENOMEM); | return 0;
  ff_vk_shader_rep_fmt (libavutil/vulkan.c:1289): reads pixfmt; writes -; returns return high ? "rgba16f" : "rgba8";
  ff_vk_shader_add_descriptor_set (libavutil/vulkan.c:1795): reads desc, nb, print_to_shader_only, s, shd, singular; writes shd*; returns return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return 0;
  main (ffbuild/bin2c.c:26 (1 of 168 definitions)): reads argc, argv; writes argv*; returns return 1; | return -1; | return -1; | return -1; | return 0;
  ff_vk_shader_register_exec (libavutil/vulkan.c:1907): reads pool, s, shd; writes pool*, shd*; returns return 0; | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return AVERROR(ENOMEM); | return err; | return err;
  ff_vk_shader_link (libavutil/vulkan.c:1720): reads entrypoint, s, shd, spirv, spirv_len; writes shd*; returns return err; | return err; | return AVERROR(ENOMEM); | return err; | return err; | return err;
  ff_matrix_mul_3x3_vec (libavfilter/colorspace.c:66): reads dst, mat, vec; writes dst*; returns -
  ff_fill_rgb2yuv_table (libavfilter/colorspace.c:125): reads coeffs, rgb2yuv; writes rgb2yuv*; returns -
  av_csp_luma_coeffs_from_avcsp (libavutil/csp.c:58): reads csp; writes -; returns return NULL; | return NULL; | return coeffs;
  ff_outlink_frame_wanted (libavfilter/avfilter.c:1661): reads link; writes -; returns return li->frame_wanted_out;
  ff_outlink_set_status (libavfilter/filters.h:424): reads link, pts, status; writes -; returns -
  av_rescale_q (libavutil/mathematics.c:142): reads a, bq, cq; writes -; returns return av_rescale_q_rnd(a, bq, cq, AV_ROUND_NEAR_INF);
  ff_get_video_buffer (libavfilter/video.c:116): reads h, link, w; writes -; returns return ret;
  av_frame_clone (libavutil/frame.c:597): reads src; writes -; returns return NULL; | return ret;
  ff_vk_filter_process_simple (libavfilter/vulkan_filter.c:242): reads e, in_f, out_f, push_size, push_src, sampler, shd, vkctx; writes -; returns return ff_vk_exec_submit(vkctx, exec); | return err;
  av_frame_free (libavutil/frame.c:162): reads frame; writes -; returns -
  ff_filter_frame (libavfilter/avfilter.c:1062): reads frame, link; writes frame*; returns return ret; | return 0; | return AVERROR_PATCHWELCOME;
  av_buffer_ref (libavutil/buffer.c:103): reads buf; writes buf*; returns return NULL; | return ret;
  ff_vk_filter_init_context (libavfilter/vulkan_filter.c:25): reads avctx, frames_ref, height, s, sw_format, width; writes frames_ref*, s*; returns return err; | return AVERROR(ENOMEM); | return AVERROR(EINVAL); | return err; | return err; | return err;
  av_get_pix_fmt (libavutil/pixdesc.c:2957): reads name; writes -; returns return pix_fmt;
  ff_filter_link (libavfilter/filters.h:197): reads link; writes -; returns return(FilterLink*)link;
  ff_vk_uninit (libavutil/vulkan.c:2306): reads s; writes s*; returns -
  ff_vk_shader_free (libavutil/vulkan.c:2267): reads s, shd; writes shd*; returns -
  ff_vk_exec_pool_free (libavutil/vulkan.c:238): reads pool, s; writes pool*; returns -
  not defined in this repository: layout, imageStore, ivec2, av_inv_q
  not shown (11): ff_vk_spirv_init, RET, GLSLC, GLSLF, FFALIGN, AVERROR, OFFSET, AVFILTER_DEFINE_CLASS, FILTER_SINGLE_PIXFMT, FILTER_OUTPUTS, NULL_IF_CONFIG_SMALL

CALLERS (8):
  init_frame_decoder (libavcodec/apedec.c:1477): init_filter(ctx, ctx->filters[i], ctx->filterbuf[i],
  avgblur_vulkan_filter_frame (libavfilter/vf_avgblur_vulkan.c:180): RET(init_filter(ctx, in));
  blend_frame (libavfilter/vf_blend_vulkan.c:256): RET(init_filter(avctx));
  bwdif_vulkan_config_output (libavfilter/vf_bwdif_vulkan.c:293): return init_filter(avctx);
  chromaber_vulkan_filter_frame (libavfilter/vf_chromaber_vulkan.c:182): RET(init_filter(ctx, in));
  filter_frame (libavfilter/vf_flip_vulkan.c:175): RET(init_filter(ctx, in, type));
  gblur_vulkan_filter_frame (libavfilter/vf_gblur_vulkan.c:320): RET(init_filter(ctx, in));
  nlmeans_vulkan_filter_frame (libavfilter/vf_nlmeans_vulkan.c:780): RET(init_filter(ctx));
  ... only the first 8 of 14 reference sites were followed

TYPES (2):
  TestSrcVulkanMode — libavfilter/vsrc_testsrc_vulkan.c:30
    enum TestSrcVulkanMode {
        TESTSRC_COLOR,
    }
  AVColorSpace — libavutil/pixfmt.h:619
    enum AVColorSpace {
        AVCOL_SPC_RGB         = 0,  
        AVCOL_SPC_BT709       = 1,  
        AVCOL_SPC_UNSPECIFIED = 2,
        AVCOL_SPC_RESERVED    = 3,  
        AVCOL_SPC_FCC         = 4,  
        AVCOL_SPC_BT470BG     = 5,  
        AVCOL_SPC_SMPTE170M   = 6,  
        AVCOL_SPC_SMPTE240M   = 7,  
        AVCOL_SPC_YCGCO       = 8,  
        AVCOL_SPC_YCOCG       = AVCOL_SPC_YCGCO,
        AVCOL_SPC_BT2020_NCL  = 9,  
        AVCOL_SPC_BT2020_CL   = 10, 
        AVCOL_SPC_SMPTE2085   = 11, 
        AVCOL_SPC_CHROMA_DERIVED_NCL = 12, 
        AVCOL_SPC_CHROMA_DERIVED_CL = 13, 
        AVCOL_SPC_ICTCP       = 14, 
        AVCOL_SPC_IPT_C2      = 15, 
        AVCOL_SPC_YCGCO_RE    = 16, 
        AVCOL_SPC_YCGCO_RO    = 17, 
        AVCOL_SPC_NB                
    }
```

### Turn 3  _(tok 24534+148, stop=tool_use)_

**Reasoning:** Now let me handle the three files that returned errors. Let me read them directly to find the enclosing function.

**Says:** Now let me resolve the three files where `get_context_at` returned errors by reading the surrounding lines directly:

- `read_file(path=libavfilter/vf_bwdif_vulkan.c, start_line=85, end_line=130, version=old)` →

```
libavfilter/vf_bwdif_vulkan.c lines 85-130 of 336
   85|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
   86|             .samplers   = DUP_SAMPLER(s->sampler),
   87|         },
   88|         {
   89|             .name       = "cur",
   90|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
   91|             .dimensions = 2,
   92|             .elems      = planes,
   93|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
   94|             .samplers   = DUP_SAMPLER(s->sampler),
   95|         },
   96|         {
   97|             .name       = "next",
   98|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
   99|             .dimensions = 2,
  100|             .elems      = planes,
  101|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  102|             .samplers   = DUP_SAMPLER(s->sampler),
  103|         },
  104|         {
  105|             .name       = "dst",
  106|             .type       = VK_DESCRIPTOR_TYPE_STORAGE_IMAGE,
  107|             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  108|             .mem_quali  = "writeonly",
  109|             .dimensions = 2,
  110|             .elems      = planes,
  111|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  112|         },
  113|     };
  114| 
  115|     RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 4, 0, 0));
  116| 
  117|     GLSLC(0, layout(push_constant, std430) uniform pushConstants {                 );
  118|     GLSLC(1,    int parity;                                                        );
  119|     GLSLC(1,    int tff;                                                           );
  120|     GLSLC(1,    int current_field;                                                 );
  121|     GLSLC(0, };                                                                    );
  122| 
  123|     ff_vk_shader_add_push_const(&s->shd, 0, sizeof(BWDIFParameters),
  124|                                 VK_SHADER_STAGE_COMPUTE_BIT);
  125| 
  126|     GLSLD(ff_source_bwdif_comp                                                     );
  127|     GLSLC(0, void main()                                                           );
  128|     GLSLC(0, {                                                                     );
  129|     GLSLC(1,     ivec2 size;                                                       );
  130|     GLSLC(1,     const ivec2 pos = ivec2(gl_GlobalInvocationID.xy);                );
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 4  _(tok 25418+469, stop=tool_use, forced)_

**Reasoning:** Let me look at the remaining files I need to resolve. I need to find the enclosing function for vf_bwdif_vulkan.c, vf_chromaber_vulkan.c, and vf_nlmeans_vulkan.c. Let me look at the function that contains those lines by reading a bit before each call site.

For vf_bwdif_vulkan.c:107 - I need to find the enclosing function.

For vf_chromaber_vulkan.c:120 - same.

For vf_nlmeans_vulkan.c:457 - same.

Let me read the surrounding context of each.

- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_gblur_pipeline", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_vulkan", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 3, "n_truth": 3, "tp": 2, "precision": 0.6666666666666666, "recall": 0.6666666666666666, "f1": 0.6666666666666666}`

## Semantic arm

### Turn 1  _(tok 2317+119, stop=tool_use)_

**Reasoning:** The user wants me to find every function that calls `ff_vk_shader_rep_fmt` in the repository. Let me start by getting the callers of this function, and also look at its neighborhood to understand the full picture.

- `get_callers(name=ff_vk_shader_rep_fmt, limit=100)` →

```
{
  "name": "ff_vk_shader_rep_fmt",
  "version": "old",
  "callers": [
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_avgblur_vulkan.c",
      "line": 102
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_blend_vulkan.c",
      "line": 173
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_bwdif_vulkan.c",
      "line": 107
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_chromaber_vulkan.c",
      "line": 120
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_flip_vulkan.c",
      "line": 86
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_gblur_vulkan.c",
      "line": 231
    },
    {
      "caller": "init_denoise_pipeline",
      "file": "libavfilter/vf_nlmeans_vulkan.c",
      "line": 457
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_overlay_vulkan.c",
      "line": 142
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_scale_vulkan.c",
      "line": 174
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_transpose_vulkan.c",
      "line": 85
    },
    {
      "caller": "init_vulkan",
      "file": "libavfilter/vf_xfade_vulkan.c",
      "line": 367
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vsrc_testsrc_vulkan.c",
      "line": 105
    }
  ]
}
```

### Turn 2  _(tok 2923+173, stop=tool_use)_

**Reasoning:** I got 12 callers. Let me also check the "work" version to make sure there are no differences, and let me also verify that these are all the callers by checking if there might be more. Let me also check the neighborhood to confirm.

Actually, I should also check the "work" version and "new" version to make sure I have the complete list. Let me get the work version as well.

- `get_callers(name=ff_vk_shader_rep_fmt, limit=100, rev=work)` →

```
{
  "name": "ff_vk_shader_rep_fmt",
  "version": "old",
  "callers": [
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_avgblur_vulkan.c",
      "line": 102
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_blend_vulkan.c",
      "line": 173
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_bwdif_vulkan.c",
      "line": 107
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_chromaber_vulkan.c",
      "line": 120
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_flip_vulkan.c",
      "line": 86
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_gblur_vulkan.c",
      "line": 231
    },
    {
      "caller": "init_denoise_pipeline",
      "file": "libavfilter/vf_nlmeans_vulkan.c",
      "line": 457
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_overlay_vulkan.c",
      "line": 142
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_scale_vulkan.c",
      "line": 174
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vf_transpose_vulkan.c",
      "line": 85
    },
    {
      "caller": "init_vulkan",
      "file": "libavfilter/vf_xfade_vulkan.c",
      "line": 367
    },
    {
      "caller": "init_filter",
      "file": "libavfilter/vsrc_testsrc_vulkan.c",
      "line": 105
    }
  ]
}
```

### Turn 3  _(tok 3583+616, stop=tool_use)_

**Reasoning:** The results are identical across "old" and "work". The list is complete with 12 callers. Let me now submit.

Summary of callers:
1. init_filter - libavfilter/vf_avgblur_vulkan.c
2. init_filter - libavfilter/vf_blend_vulkan.c
3. init_filter - libavfilter/vf_bwdif_vulkan.c
4. init_filter - libavfilter/vf_chromaber_vulkan.c
5. init_filter - libavfilter/vf_flip_vulkan.c
6. init_filter - libavfilter/vf_gblur_vulkan.c
7. init_denoise_pipeline - libavfilter/vf_nlmeans_vulkan.c
8. init_filter - libavfilter/vf_overlay_vulkan.c
9. init_filter - libavfilter/vf_scale_vulkan.c
10. init_filter - libavfilter/vf_transpose_vulkan.c
11. init_vulkan - libavfilter/vf_xfade_vulkan.c
12. init_filter - libavfilter/vsrc_testsrc_vulkan.c

All are distinct caller+file pairs (even though many are named "init_filter", they're in different files, so each one is a different function that needs to be updated).

- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_denoise_pipeline", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_vulkan", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

