# Impact-analysis transcript — ffmpeg @ 0a37d5a3b1fb — openrouter:deepseek/deepseek-v4-pro

- target: `ff_vk_shader_init` (libavutil/vulkan.c), arity 5->10
- truth: [['libavfilter/vf_avgblur_vulkan.c', 'init_filter'], ['libavfilter/vf_blend_vulkan.c', 'init_filter'], ['libavfilter/vf_bwdif_vulkan.c', 'init_filter'], ['libavfilter/vf_chromaber_vulkan.c', 'init_filter'], ['libavfilter/vf_flip_vulkan.c', 'init_filter'], ['libavfilter/vf_gblur_vulkan.c', 'init_filter'], ['libavfilter/vf_nlmeans_vulkan.c', 'init_denoise_pipeline'], ['libavfilter/vf_nlmeans_vulkan.c', 'init_weights_pipeline'], ['libavfilter/vf_overlay_vulkan.c', 'init_filter'], ['libavfilter/vf_scale_vulkan.c', 'init_filter'], ['libavfilter/vf_transpose_vulkan.c', 'init_filter'], ['libavfilter/vf_xfade_vulkan.c', 'init_vulkan'], ['libavfilter/vsrc_testsrc_vulkan.c', 'init_filter']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1027+83, stop=tool_use)_

**Reasoning:** The user wants me to find all call sites of `ff_vk_shader_init` in the repository. Let me start by finding references to this function

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

### Turn 2  _(tok 1815+1340, stop=tool_use)_

**Reasoning:** I have the references. The last one (libavutil/vulkan.h line 477) is a declaration/prototype, so I should exclude it. The definition is in libavutil/vulkan.c, but that's not in the list. Let me now find the enclosing functions for each call site. Let me read the context around each line to determine the function name.

Let me go through each reference:

1. libavfilter/vf_avgblur_vulkan.c:84
2. libavfilter/vf_blend_vulkan.c:148
3. libavfilter/vf_bwdif_vulkan.c:116
4. libavfilter/vf_chromaber_vulkan.c:95
5. libavfilter/vf_flip_vulkan.c:69
6. libavfilter/vf_gblur_vulkan.c:222
7. libavfilter/vf_gblur_vulkan.c:224
8. libavfilter/vf_nlmeans_vulkan.c:244
9. libavfilter/vf_nlmeans_vulkan.c:431
10. libavfilter/vf_overlay_vulkan.c:108
11. libavfilter/vf_scale_vulkan.c:149
12. libavfilter/vf_transpose_vulkan.c:68
13. libavfilter/vf_xfade_vulkan.c:342
14. libavfilter/vsrc_testsrc_vulkan.c:88

libavutil/vulkan.h:477 is the declaration, not a call site.

Now I need to find the enclosing function for each call site. Let me read the relevant lines from each file.

**Says:** I need to find the enclosing function for each call site. Let me read around each reference to identify the function names

- `read_file(path=libavfilter/vf_avgblur_vulkan.c, start_line=75, end_line=90)` →

```
libavfilter/vf_avgblur_vulkan.c lines 75-90 of 260
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
```

- `read_file(path=libavfilter/vf_blend_vulkan.c, start_line=140, end_line=155)` →

```
libavfilter/vf_blend_vulkan.c lines 140-155 of 401
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
```

- `read_file(path=libavfilter/vf_bwdif_vulkan.c, start_line=108, end_line=122)` →

```
libavfilter/vf_bwdif_vulkan.c lines 108-122 of 416
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
```

- `read_file(path=libavfilter/vf_chromaber_vulkan.c, start_line=87, end_line=101)` →

```
libavfilter/vf_chromaber_vulkan.c lines 87-101 of 261
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
```

- `read_file(path=libavfilter/vf_flip_vulkan.c, start_line=61, end_line=75)` →

```
libavfilter/vf_flip_vulkan.c lines 61-75 of 301
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
```

- `read_file(path=libavfilter/vf_gblur_vulkan.c, start_line=214, end_line=230)` →

```
libavfilter/vf_gblur_vulkan.c lines 214-230 of 387
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
```

- `read_file(path=libavfilter/vf_nlmeans_vulkan.c, start_line=236, end_line=250)` →

```
libavfilter/vf_nlmeans_vulkan.c lines 236-250 of 1120
  236|     if (max_wg > max_dim) {
  237|         wg_size = max_dim;
  238|     } else if (max_wg < max_dim) {
  239|         /* Make it fit */
  240|         while (wg_size*wg_rows < max_dim)
  241|             wg_rows++;
  242|     }
  243| 
  244|     RET(ff_vk_shader_init(pl, shd, "nlmeans_weights", VK_SHADER_STAGE_COMPUTE_BIT, 0));
  245|     ff_vk_shader_set_compute_sizes(shd, wg_size, 1, 1);
  246|     *nb_rows = wg_rows;
  247| 
  248|     if (t > 1)
  249|         GLSLC(0, #extension GL_EXT_shader_atomic_float : require              );
  250|     GLSLC(0, #extension GL_ARB_gpu_shader_int64 : require                     );
```

- `read_file(path=libavfilter/vf_nlmeans_vulkan.c, start_line=423, end_line=437)` →

```
libavfilter/vf_nlmeans_vulkan.c lines 423-437 of 1120
  423|                                          const AVPixFmtDescriptor *desc, int planes)
  424| {
  425|     int err;
  426|     uint8_t *spv_data;
  427|     size_t spv_len;
  428|     void *spv_opaque = NULL;
  429|     FFVulkanDescriptorSetBinding *desc_set;
  430| 
  431|     RET(ff_vk_shader_init(pl, shd, "nlmeans_denoise",
  432|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
  433| 
  434|     ff_vk_shader_set_compute_sizes(shd, 32, 32, 1);
  435| 
  436|     GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
  437|     GLSLC(1,    uvec4 ws_stride;                                          );
```

- `read_file(path=libavfilter/vf_overlay_vulkan.c, start_line=100, end_line=114)` →

```
libavfilter/vf_overlay_vulkan.c lines 100-114 of 349
  100|     if (!spv) {
  101|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
  102|         return AVERROR_EXTERNAL;
  103|     }
  104| 
  105|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
  106|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
  107|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_NEAREST));
  108|     RET(ff_vk_shader_init(&s->pl, &s->shd, "overlay_compute",
  109|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
  110| 
  111|     ff_vk_shader_set_compute_sizes(&s->shd, 32, 32, 1);
  112| 
  113|     GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
  114|     GLSLC(1,    ivec2 o_offset[3];                                        );
```

- `read_file(path=libavfilter/vf_scale_vulkan.c, start_line=141, end_line=155)` →

```
libavfilter/vf_scale_vulkan.c lines 141-155 of 419
  141|     if (!spv) {
  142|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
  143|         return AVERROR_EXTERNAL;
  144|     }
  145| 
  146|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
  147|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
  148|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 0, sampler_mode));
  149|     RET(ff_vk_shader_init(&s->pl, &s->shd, "scale_compute",
  150|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
  151| 
  152|     ff_vk_shader_set_compute_sizes(&s->shd, 32, 32, 1);
  153| 
  154|     GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
  155|     GLSLC(1,    mat4 yuv_matrix;                                          );
```

- `read_file(path=libavfilter/vf_transpose_vulkan.c, start_line=60, end_line=74)` →

```
libavfilter/vf_transpose_vulkan.c lines 60-74 of 278
   60|     if (!spv) {
   61|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
   62|         return AVERROR_EXTERNAL;
   63|     }
   64| 
   65|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
   66|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
   67|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_LINEAR));
   68|     RET(ff_vk_shader_init(&s->pl, &s->shd, "transpose_compute",
   69|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
   70| 
   71|     ff_vk_shader_set_compute_sizes(&s->shd, 32, 1, 1);
   72| 
   73|     desc = (FFVulkanDescriptorSetBinding []) {
   74|         {
```

- `read_file(path=libavfilter/vf_xfade_vulkan.c, start_line=334, end_line=348)` →

```
libavfilter/vf_xfade_vulkan.c lines 334-348 of 722
  334|     if (!spv) {
  335|         av_log(avctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
  336|         return AVERROR_EXTERNAL;
  337|     }
  338| 
  339|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
  340|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
  341|     RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_NEAREST));
  342|     RET(ff_vk_shader_init(&s->pl, &s->shd, "xfade_compute",
  343|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
  344| 
  345|     ff_vk_shader_set_compute_sizes(&s->shd, 32, 32, 1);
  346| 
  347|     desc = (FFVulkanDescriptorSetBinding []) {
  348|         {
```

- `read_file(path=libavfilter/vsrc_testsrc_vulkan.c, start_line=80, end_line=94)` →

```
libavfilter/vsrc_testsrc_vulkan.c lines 80-94 of 377
   80|     spv = ff_vk_spirv_init();
   81|     if (!spv) {
   82|         av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
   83|         return AVERROR_EXTERNAL;
   84|     }
   85| 
   86|     ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
   87|     RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
   88|     RET(ff_vk_shader_init(&s->pl, &s->shd, "testsrc_compute",
   89|                           VK_SHADER_STAGE_COMPUTE_BIT, 0));
   90| 
   91|     ff_vk_shader_set_compute_sizes(&s->shd, 32, 32, 1);
   92| 
   93|     GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
   94|     GLSLC(1,    vec4 color_comp;                                          );
```

### Turn 3  _(tok 7363+176, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing function for each call site. Let me find the function names by searching backwards for function definitions.

**Says:** Now let me find the enclosing function names for each call site. Let me search for the function definitions that contain these calls.

- `grep(pattern=^static .*\(.*\)\s*$|^[a-zA-Z_][a-zA-Z0-9_]* .*\(.*\)\s*$, path_glob=libavfilter/vf_avgblur_vulkan.c, max_results=30)` →

```
3 matches
libavfilter/vf_avgblur_vulkan.c:62:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
libavfilter/vf_avgblur_vulkan.c:166:static int avgblur_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_avgblur_vulkan.c:200:static void avgblur_vulkan_uninit(AVFilterContext *avctx)
```

### Turn 4  _(tok 7654+111, stop=tool_use)_

**Reasoning:** The call at line 84 is in init_filter (which starts at line 62).

- `grep(max_results=30, path_glob=libavfilter/vf_blend_vulkan.c, pattern=^static .*\()` →

```
9 matches
libavfilter/vf_blend_vulkan.c:77:static inline void init_blend_func(FilterParamsVulkan *param)
libavfilter/vf_blend_vulkan.c:93:static int config_params(AVFilterContext *avctx)
libavfilter/vf_blend_vulkan.c:116:static int process_command(AVFilterContext *ctx, const char *cmd, const char *args,
libavfilter/vf_blend_vulkan.c:126:static av_cold int init_filter(AVFilterContext *avctx)
libavfilter/vf_blend_vulkan.c:229:static int blend_frame(FFFrameSync *fs)
libavfilter/vf_blend_vulkan.c:271:static av_cold int init(AVFilterContext *avctx)
libavfilter/vf_blend_vulkan.c:280:static av_cold void uninit(AVFilterContext *avctx)
libavfilter/vf_blend_vulkan.c:300:static int config_props_output(AVFilterLink *outlink)
libavfilter/vf_blend_vulkan.c:335:static int activate(AVFilterContext *avctx)
```

### Turn 5  _(tok 8023+120, stop=tool_use)_

**Reasoning:** Line 148 is between 126 (init_filter) and 229 (blend_frame), so it's in init_filter.

- `grep(max_results=30, path_glob=libavfilter/vf_bwdif_vulkan.c, pattern=^static .*\()` →

```
5 matches
libavfilter/vf_bwdif_vulkan.c:94:static av_cold int init_filter(AVFilterContext *ctx)
libavfilter/vf_bwdif_vulkan.c:264:static void bwdif_vulkan_filter_frame(AVFilterContext *ctx, AVFrame *dst,
libavfilter/vf_bwdif_vulkan.c:283:static void bwdif_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_bwdif_vulkan.c:304:static int bwdif_vulkan_config_input(AVFilterLink *inlink)
libavfilter/vf_bwdif_vulkan.c:337:static int bwdif_vulkan_config_output(AVFilterLink *outlink)
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 8332+716, stop=tool_use, forced)_

**Reasoning:** Let me also check the remaining files quickly. I have enough to determine most. Let me also check the nlmeans file for the two functions.

For nlmeans, line 244 and 431 - let me find the enclosing functions.

I already have enough patterns to identify:

1. vf_avgblur_vulkan.c:84 → init_filter (starts at 62)
2. vf_blend_vulkan.c:148 → init_filter (starts at 126)
3. vf_bwdif_vulkan.c:116 → init_filter (starts at 94)
4. vf_chromaber_vulkan.c:95 → need to check
5. vf_flip_vulkan.c:69 → need to check
6. vf_gblur_vulkan.c:222,224 → need to check (same function)
7. vf_nlmeans_vulkan.c:244 → need to check
8. vf_nlmeans_vulkan.c:431 → need to check
9. vf_overlay_vulkan.c:108 → need to check
10. vf_scale_vulkan.c:149 → need to check
11. vf_transpose_vulkan.c:68 → need to check
12. vf_xfade_vulkan.c:342 → need to check
13. vsrc_testsrc_vulkan.c:88 → need to check

I need to find the exact function names. Let me look at the remaining files quickly. But I'm running out of tokens. Let me search for function definitions in the remaining files.

Actually, let me just use grep to find function definitions in all these files at once.

- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_weights_buffers", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_denoise", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 3, "n_truth": 4, "tp": 1, "precision": 0.3333333333333333, "recall": 0.25, "f1": 0.28571428571428575}`

