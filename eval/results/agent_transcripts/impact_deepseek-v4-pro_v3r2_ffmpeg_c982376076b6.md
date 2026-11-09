# Impact-analysis transcript — ffmpeg @ c982376076b6 — openrouter:deepseek/deepseek-v4-pro

- target: `ff_vk_shader_rep_fmt` (libavutil/vulkan.c), arity 1->2
- truth: [['libavfilter/vf_avgblur_vulkan.c', 'init_filter'], ['libavfilter/vf_blend_vulkan.c', 'init_filter'], ['libavfilter/vf_bwdif_vulkan.c', 'init_filter'], ['libavfilter/vf_chromaber_vulkan.c', 'init_filter'], ['libavfilter/vf_flip_vulkan.c', 'init_filter'], ['libavfilter/vf_gblur_vulkan.c', 'init_filter'], ['libavfilter/vf_nlmeans_vulkan.c', 'init_denoise_pipeline'], ['libavfilter/vf_overlay_vulkan.c', 'init_filter'], ['libavfilter/vf_scale_vulkan.c', 'init_filter'], ['libavfilter/vf_transpose_vulkan.c', 'init_filter'], ['libavfilter/vf_xfade_vulkan.c', 'init_vulkan'], ['libavfilter/vsrc_testsrc_vulkan.c', 'init_filter']]

## Self-navigation arm

### Turn 1  _(tok 910+91, stop=tool_use)_

**Reasoning:** Let me find all callers of `ff_vk_shader_rep_fmt` in the repository.

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

### Turn 2  _(tok 1493+159, stop=tool_use)_

**Reasoning:** Now I need to identify the enclosing functions for each call site. Let me read a few lines around each match to get the function context.

- `grep(pattern=^(static |int |void |const )?[a-zA-Z_][a-zA-Z0-9_]*\(, path_glob=libavfilter/vf_avgblur_vulkan.c, version=old, max_results=50)` →

```
1 matches
libavfilter/vf_avgblur_vulkan.c:226:AVFILTER_DEFINE_CLASS(avgblur_vulkan);
```

### Turn 3  _(tok 1696+577, stop=tool_use)_

**Reasoning:** Let me read around line 102 of vf_avgblur_vulkan.c to find the enclosing function.

- `read_file(path=libavfilter/vf_avgblur_vulkan.c, start_line=80, end_line=130, version=old)` →

```
libavfilter/vf_avgblur_vulkan.c lines 80-130 of 258
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
  113|     GLSLC(1,    vec4 filter_norm;                                         );
  114|     GLSLC(1,    ivec2 filter_len;                                         );
  115|     GLSLC(0, };                                                           );
  116|     GLSLC(0,                                                              );
  117| 
  118|     ff_vk_shader_add_push_const(&s->shd, 0, sizeof(s->opts),
  119|                                 VK_SHADER_STAGE_COMPUTE_BIT);
  120| 
  121|     GLSLD(   blur_kernel                                                  );
  122|     GLSLC(0, void main()                                                  );
  123|     GLSLC(0, {                                                            );
  124|     GLSLC(1,     ivec2 size;                                              );
  125|     GLSLC(1,     const ivec2 pos = ivec2(gl_GlobalInvocationID.xy);       );
  126|     for (int i = 0; i < planes; i++) {
  127|         GLSLC(0,                                                          );
  128|         GLSLF(1,  size = imageSize(output_img[%i]);                     ,i);
  129|         GLSLC(1,  if (!IS_WITHIN(pos, size))                              );
  130|         GLSLC(2,      return;                                             );
```

- `read_file(path=libavfilter/vf_blend_vulkan.c, start_line=150, end_line=200, version=old)` →

```
libavfilter/vf_blend_vulkan.c lines 150-200 of 399
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
  184|         for (j = 0; j < i; j++)
  185|             if (s->params[i].blend_func == s->params[j].blend_func)
  186|                 break;
  187|         /* note: the bracket is needed, for GLSLD is a macro with multiple statements. */
  188|         if (j == i) {
  189|             GLSLD(s->params[i].blend_func);
  190|         }
  191|     }
  192| 
  193|     GLSLC(0, void main()                                                    );
  194|     GLSLC(0, {                                                              );
  195|     GLSLC(1,     ivec2 size;                                                );
  196|     GLSLC(1,     const ivec2 pos = ivec2(gl_GlobalInvocationID.xy);         );
  197|     for (int i = 0; i < planes; i++) {
  198|         GLSLC(0,                                                            );
  199|         GLSLF(1, size = imageSize(output_images[%i]);                     ,i);
  200|         GLSLC(1, if (IS_WITHIN(pos, size)) {                                );
```

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

- `read_file(path=libavfilter/vf_chromaber_vulkan.c, start_line=100, end_line=145, version=old)` →

```
libavfilter/vf_chromaber_vulkan.c lines 100-145 of 259
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
  131|     GLSLC(0, void main()                                                  );
  132|     GLSLC(0, {                                                            );
  133|     GLSLC(1,     ivec2 pos = ivec2(gl_GlobalInvocationID.xy);             );
  134|     if (planes == 1) {
  135|         GLSLC(1, distort_rgb(imageSize(output_img[0]), pos);              );
  136|     } else {
  137|         GLSLC(1, ivec2 size = imageSize(output_img[0]);                   );
  138|         GLSLC(1, vec2 npos = vec2(pos)/vec2(size);                        );
  139|         GLSLC(1, vec4 res = texture(input_img[0], npos);                  );
  140|         GLSLC(1, imageStore(output_img[0], pos, res);                     );
  141|         for (int i = 1; i < planes; i++) {
  142|             GLSLC(0,                                                      );
  143|             GLSLF(1,  size = imageSize(output_img[%i]);                 ,i);
  144|             GLSLC(1,  if (!IS_WITHIN(pos, size))                          );
  145|             GLSLC(2,      return;                                         );
```

- `read_file(path=libavfilter/vf_flip_vulkan.c, start_line=65, end_line=110, version=old)` →

```
libavfilter/vf_flip_vulkan.c lines 65-110 of 299
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
   97|     GLSLC(0, {                                                                              );
   98|     GLSLC(1,     ivec2 size;                                                                );
   99|     GLSLC(1,     const ivec2 pos = ivec2(gl_GlobalInvocationID.xy);                         );
  100|     for (int i = 0; i < planes; i++) {
  101|         GLSLC(0,                                                                            );
  102|         GLSLF(1, size = imageSize(output_image[%i]);                                      ,i);
  103|         GLSLC(1, if (IS_WITHIN(pos, size)) {                                                );
  104|         switch (type)
  105|         {
  106|         case FLIP_HORIZONTAL:
  107|             GLSLF(2, vec4 res = texture(input_image[%i], ivec2(size.x - pos.x, pos.y));   ,i);
  108|             break;
  109|         case FLIP_VERTICAL:
  110|             GLSLF(2, vec4 res = texture(input_image[%i], ivec2(pos.x, size.y - pos.y));   ,i);
```

- `read_file(path=libavfilter/vf_gblur_vulkan.c, start_line=210, end_line=255, version=old)` →

```
libavfilter/vf_gblur_vulkan.c lines 210-255 of 385
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
  242|         shd = &s->shd_hor;
  243|         RET(ff_vk_shader_init(vkctx, shd, "gblur_hor",
  244|                               VK_SHADER_STAGE_COMPUTE_BIT,
  245|                               NULL, 0,
  246|                               32, 1, 1,
  247|                               0));
  248| 
  249|         RET(ff_vk_shader_add_descriptor_set(vkctx, shd, desc, 2, 0, 0));
  250| 
  251|         GLSLC(0, #define OFFSET (vec2(i, 0.0)));
  252|         RET(init_gblur_pipeline(s, shd, &s->params_hor, s->size, s->sigma, spv));
  253|     }
  254| 
  255|     {
```

### Turn 4  _(tok 6941+105, stop=tool_use)_

- `read_file(path=libavfilter/vf_nlmeans_vulkan.c, start_line=440, end_line=480, version=old)` →

```
libavfilter/vf_nlmeans_vulkan.c lines 440-480 of 1123
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
  468|             .name        = "weights_buffer_0",
  469|             .type        = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,
  470|             .mem_quali   = "readonly",
  471|             .stages      = VK_SHADER_STAGE_COMPUTE_BIT,
  472|             .buf_content = "float weights_0[];",
  473|         },
  474|         {
  475|             .name        = "sums_buffer_0",
  476|             .type        = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,
  477|             .mem_quali   = "readonly",
  478|             .stages      = VK_SHADER_STAGE_COMPUTE_BIT,
  479|             .buf_content = "float sums_0[];",
  480|         },
```

### Turn 5  _(tok 7653+104, stop=tool_use)_

- `read_file(path=libavfilter/vf_overlay_vulkan.c, start_line=122, end_line=165, version=old)` →

```
libavfilter/vf_overlay_vulkan.c lines 122-165 of 347
  122|     desc = (FFVulkanDescriptorSetBinding []) {
  123|         {
  124|             .name       = "main_img",
  125|             .type       = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER,
  126|             .dimensions = 2,
  127|             .elems      = planes,
  128|             .stages     = VK_SHADER_STAGE_COMPUTE_BIT,
  129|             .samplers   = DUP_SAMPLER(s->sampler),
  130|         },
  131|         {
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
  153|     GLSLD(   overlay_alpha                                                );
  154|     GLSLC(0, void main()                                                  );
  155|     GLSLC(0, {                                                            );
  156|     GLSLC(1,     ivec2 pos = ivec2(gl_GlobalInvocationID.xy);             );
  157|     GLSLF(1,     int planes = %i;                                  ,planes);
  158|     GLSLC(1,     for (int i = 0; i < planes; i++) {                       );
  159|     if (ialpha)
  160|         GLSLC(2,         overlay_alpha_opaque(i, pos);                    );
  161|     else
  162|         GLSLC(2,         overlay_noalpha(i, pos);                         );
  163|     GLSLC(1,     }                                                        );
  164|     GLSLC(0, }                                                            );
  165| 
```

### Turn 6  _(tok 8428+104, stop=tool_use)_

- `read_file(path=libavfilter/vf_scale_vulkan.c, start_line=155, end_line=200, version=old)` →

```
libavfilter/vf_scale_vulkan.c lines 155-200 of 417
  155|     GLSLC(1,    mat4 yuv_matrix;                                          );
  156|     GLSLC(0, };                                                           );
  157|     GLSLC(0,                                                              );
  158| 
  159|     ff_vk_shader_add_push_const(&s->shd, 0, sizeof(s->opts),
  160|                                 VK_SHADER_STAGE_COMPUTE_BIT);
  161| 
  162|     desc = (FFVulkanDescriptorSetBinding []) {
  163|         {
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
  185| 
  186|     if (s->vkctx.output_format != s->vkctx.input_format) {
  187|         GLSLD(   rgb2yuv                                                     );
  188|     }
  189| 
  190|     switch (s->vkctx.output_format) {
  191|     case AV_PIX_FMT_NV12:    GLSLD(write_nv12); break;
  192|     case AV_PIX_FMT_YUV420P: GLSLD( write_420); break;
  193|     case AV_PIX_FMT_YUV444P: GLSLD( write_444); break;
  194|     default: break;
  195|     }
  196| 
  197|     GLSLC(0, void main()                                                     );
  198|     GLSLC(0, {                                                               );
  199|     GLSLC(1,     ivec2 size;                                                 );
  200|     GLSLC(1,     ivec2 pos = ivec2(gl_GlobalInvocationID.xy);                );
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 7  _(tok 9248+818, stop=tool_use, forced)_

**Reasoning:** Let me identify the enclosing functions. I need to see the function definitions. Let me find the function names for the remaining files. Let me also check the functions for files I already looked at.

For the ones I've seen:
- vf_avgblur_vulkan.c: line 102 - need to find enclosing function. Let me check the function around line 80.
- vf_blend_vulkan.c: line 173
- vf_bwdif_vulkan.c: line 107
- vf_chromaber_vulkan.c: line 120
- vf_flip_vulkan.c: line 86
- vf_gblur_vulkan.c: line 231
- vf_nlmeans_vulkan.c: line 457
- vf_overlay_vulkan.c: line 142
- vf_scale_vulkan.c: line 174
- vf_transpose_vulkan.c: line 85
- vf_xfade_vulkan.c: line 367
- vsrc_testsrc_vulkan.c: line 105

I need to identify the enclosing function for each. Let me search for function definitions in each file.

From the context I've gathered:
- avgblur: likely `avgblur_vulkan_init` or similar
- blend: likely `blend_vulkan_init`
- bwdif: likely `bwdif_vulkan_init`
- chromaber: likely `chromaber_vulkan_init`
- flip: likely `flip_vulkan_init`
- gblur: likely `gblur_vulkan_init`
- nlmeans: some init function
- overlay: some init function
- scale: some init function
- transpose: some init function
- xfade: some init function
- testsrc: some init function

Let me grep for function definitions in each file. But I'm running out of tokens. Let me just grep for common init function patterns.

Actually, let me just check the function enclosing each call. I'll grep for function definitions in those files.

Let me look at the typical patterns. In FFmpeg Vulkan filters, the init function is usually named `<filter>_vulkan_init` or `init_<filter>_vulkan`. Let me grep for function definitions that contain these calls.

- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "low"}`

**Score (self):** `{"n_pred": 1, "n_truth": 3, "tp": 1, "precision": 1.0, "recall": 0.3333333333333333, "f1": 0.5}`

## Tool arm

### Turn 1  _(tok 2751+196, stop=tool_use)_

**Reasoning:** We need find all call sites of ff_vk_shader_rep_fmt. Need list every function that calls it, enclosing function and file. We must not include definition. Let's search.

- `grep(pattern=ff_vk_shader_rep_fmt, version=old, max_results=100)` →

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

- `get_callers(name=ff_vk_shader_rep_fmt, version=old, limit=100)` →

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

### Turn 2  _(tok 3995+616, stop=tool_use)_

**Reasoning:** get_callers gives 12 call sites across 12 files. Need ensure enclosing function names accurate. But let's verify each line context maybe some are in macros or function dynamic. Also verify no callers missing due repository maybe old vs work? User asks this repository, signature defined libavutil/vulkan.c. grep found 12 usage excluding def/prototype. get_callers matches. But we should verify each call's enclosing function. get_callers already lists. Need maybe there's duplicates in same function? No. Let's check whether all lines are actually inside the function named. Could read context of each? Might be helpful but the tool gives caller. We should call submit exactly once with list. But let's be thorough to ensure no missing calls due macros, indirect, ff_vk_shader_rep_fmt could be called through macro? grep found all textual instances. Only definition and header. So list complete.

Need submit callers exactly once. Format each object function and file. Should we include only unique function/file? The callers list has 12 entries. Note every function called init_filter in different files. Fine. Function names perhaps "init_filter" duplicated. Note vf_nlmeans "init_denoise_pipeline"; vf_xfade "init_vulkan". Need ensure no duplicates in file. submit.

- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_denoise_pipeline", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_vulkan", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2317+114, stop=tool_use)_

**Reasoning:** The user wants me to find all callers of `ff_vk_shader_rep_fmt` in the repository. Let me start by using `get_callers` to find all functions that call this function.

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

### Turn 2  _(tok 2957+438, stop=tool_use)_

**Reasoning:** I got a list of 12 callers. The tool version shows "old" — default to old? The server's commit maybe old. The user says repository currently. I should verify the list is complete. Let me use expand_function perhaps to see callers as well, or use get_callers with version work/new to ensure current files. The `get_callers` returned version "old" although I didn't specify rev. Hmm. The default rev? It says version "work" default? Actually the result says "version": "old" — maybe the server default is old parent of rev? Let me check by calling get_callers with rev maybe not needed, or get_neighborhood. But the user is asking for current repository. I should verify on "work" version. The tool schema default rev null, and description says version "work" (files on disk), "old" (parent of rev), "new" (rev); rev defaults to server's commit. The result reported "old" — maybe because I didn't specify version and default is old? Let me call get_callers with explicit rev? We can't specify version directly, only rev. There's no "work" parameter, rev null should be work? But result says old. Hmm.

Maybe get_callers result name, version "old" indicates default old? Let me examine more. The functions list all in libavfilter vulkan filters. That seems plausible complete.

I should be careful: There may be callers that call via macro or function pointer? The user says "Every function in this repository that calls ff_vk_shader_rep_fmt". get_callers should list. Let me maybe expand to check ring of ff_vk_shader_rep_fmt. Use expand_function to confirm callers.

- `expand_function(name=ff_vk_shader_rep_fmt, levels=1)` →

```
{
  "name": "ff_vk_shader_rep_fmt",
  "version": "old",
  "levels": 1,
  "node": {
    "name": "ff_vk_shader_rep_fmt",
    "file": "libavutil/vulkan.c",
    "line": 1289,
    "kind": "function",
    "state": "analyzed"
  },
  "callees": [
    {
      "name": "av_pix_fmt_desc_get",
      "file": "libavutil/pixdesc.c",
      "line": 3025,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        1291
      ]
    }
  ],
  "callers": [
    {
      "name": "init_filter",
      "file": "libavfilter/vf_avgblur_vulkan.c",
      "line": 61,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        102
      ]
    },
    {
      "name": "init_filter",
      "file": "libavfilter/vf_blend_vulkan.c",
      "line": 125,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        173
      ]
    },
    {
      "name": "init_filter",
      "file": "libavfilter/vf_bwdif_vulkan.c",
      "line": 49,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        107
      ]
    },
    {
      "name": "init_filter",
      "file": "libavfilter/vf_chromaber_vulkan.c",
      "line": 68,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        120
      ]
    },
    {
      "name": "init_filter",
      "file": "libavfilter/vf_flip_vulkan.c",
      "line": 46,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        86
      ]
    },
    {
      "name": "init_filter",
      "file": "libavfilter/vf_gblur_vulkan.c",
      "line": 198,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        231
      ]
    },
    {
      "name": "init_denoise_pipeline",
      "file": "libavfilter/vf_nlmeans_vulkan.c",
      "line": 420,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        457
      ]
    },
    {
      "name": "init_filter",
      "file": "libavfilter/vf_overlay_vulkan.c",
      "line": 83,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        142
      ]
    },
    {
      "name": "init_filter",
      "file": "libavfilter/vf_scale_vulkan.c",
      "line": 111,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        174
      ]
    },
    {
      "name": "init_filter",
      "file": "libavfilter/vf_transpose_vulkan.c",
      "line": 44,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        85
      ]
    },
    {
      "name": "init_vulkan",
      "file": "libavfilter/vf_xfade_vulkan.c",
      "line": 319,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        367
      ]
    },
    {
      "name": "init_filter",
      "file": "libavfilter/vsrc_testsrc_vulkan.c",
      "line": 65,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        105
      ]
    }
  ]
}
```

### Turn 3  _(tok 4285+80, stop=tool_use)_

**Reasoning:** The list is consistent: 12 callers, all confirmed. Let me also double check with get_neighborhood to be thorough:

- `get_neighborhood(name=ff_vk_shader_rep_fmt)` →

```
ff_vk_shader_rep_fmt — libavutil/vulkan.c:1289 [function] const char *ff_vk_shader_rep_fmt(enum AVPixelFormat pixfmt)
  reads: pixfmt; writes: -; returns: return high ? "rgba16f" : "rgba8";

CALLEES (1):
  av_pix_fmt_desc_get (libavutil/pixdesc.c:3025): reads pix_fmt; writes -; returns return NULL; | return &av_pix_fmt_descriptors[pix_fmt];

CALLERS (8):
  init_filter (libavfilter/vf_avgblur_vulkan.c:102): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_filter (libavfilter/vf_blend_vulkan.c:173): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_filter (libavfilter/vf_bwdif_vulkan.c:107): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_filter (libavfilter/vf_chromaber_vulkan.c:120): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_filter (libavfilter/vf_flip_vulkan.c:86): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_filter (libavfilter/vf_gblur_vulkan.c:231): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_denoise_pipeline (libavfilter/vf_nlmeans_vulkan.c:457): .mem_layout  = ff_vk_shader_rep_fmt(vkctx->output_format),
  init_filter (libavfilter/vf_overlay_vulkan.c:142): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  ... only the first 8 of 13 reference sites were followed

TYPES (1):
  AVPixelFormat — libavutil/pixfmt.h:71
    enum AVPixelFormat {
        AV_PIX_FMT_NONE = -1,
        AV_PIX_FMT_YUV420P,   
        AV_PIX_FMT_YUYV422,   
        AV_PIX_FMT_RGB24,     
        AV_PIX_FMT_BGR24,     
        AV_PIX_FMT_YUV422P,   
        AV_PIX_FMT_YUV444P,   
        AV_PIX_FMT_YUV410P,   
        AV_PIX_FMT_YUV411P,   
        AV_PIX_FMT_GRAY8,     
        AV_PIX_FMT_MONOWHITE, 
        AV_PIX_FMT_MONOBLACK, 
        AV_PIX_FMT_PAL8,      
        AV_PIX_FMT_YUVJ420P,  
        AV_PIX_FMT_YUVJ422P,  
        AV_PIX_FMT_YUVJ444P,  
        AV_PIX_FMT_UYVY422,   
        AV_PIX_FMT_UYYVYY411, 
        AV_PIX_FMT_BGR8,      
        AV_PIX_FMT_BGR4,      
        AV_PIX_FMT_BGR4_BYTE, 
        AV_PIX_FMT_RGB8,      
        AV_PIX_FMT_RGB4,      
        AV_PIX_FMT_RGB4_BYTE, 
        AV_PIX_FMT_NV12,      
        AV_PIX_FMT_NV21,      
        AV_PIX_FMT_ARGB,      
        AV_PIX_FMT_RGBA,      
        AV_PIX_FMT_ABGR,      
        AV_PIX_FMT_BGRA,      
        AV_PIX_FMT_GRAY16BE,  
        AV_PIX_FMT_GRAY16LE,  
        AV_PIX_FMT_YUV440P,   
        AV_PIX_FMT_YUVJ440P,  
        AV_PIX_FMT_YUVA420P,  
        AV_PIX_FMT_RGB48BE,   
        AV_PIX_FMT_RGB48LE,   
        AV_PIX_FMT_RGB565BE,  
        AV_PIX_FMT_RGB565LE,  
```

### Turn 4  _(tok 5324+713, stop=tool_use)_

**Reasoning:** The neighborhood shows "only the first 8 of 13 reference sites were followed". But the expand_function showed exactly 12 callers, and get_callers also showed 12 callers. The 13 reference sites probably counts inline or duplicates? But expand_function and get_callers both show 12. The neighborhood truncated but the other 4 we know from expand_function/get_callers: scale_vulkan, transpose_vulkan, xfade_vulkan, testsrc_vulkan.

I'm confident the list is complete. Let me submit:

Callers:
1. init_filter — libavfilter/vf_avgblur_vulkan.c
2. init_filter — libavfilter/vf_blend_vulkan.c
3. init_filter — libavfilter/vf_bwdif_vulkan.c
4. init_filter — libavfilter/vf_chromaber_vulkan.c
5. init_filter — libavfilter/vf_flip_vulkan.c
6. init_filter — libavfilter/vf_gblur_vulkan.c
7. init_denoise_pipeline — libavfilter/vf_nlmeans_vulkan.c
8. init_filter — libavfilter/vf_overlay_vulkan.c
9. init_filter — libavfilter/vf_scale_vulkan.c
10. init_filter — libavfilter/vf_transpose_vulkan.c
11. init_vulkan — libavfilter/vf_xfade_vulkan.c
12. init_filter — libavfilter/vsrc_testsrc_vulkan.c

All 12 confirmed across three different tools. I'll submit.

**Says:** I've confirmed the complete set of callers across three different tools (`get_callers`, `expand_function`, `get_neighborhood`). All 12 call sites are consistent. Submitting now.

- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_denoise_pipeline", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_vulkan", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

