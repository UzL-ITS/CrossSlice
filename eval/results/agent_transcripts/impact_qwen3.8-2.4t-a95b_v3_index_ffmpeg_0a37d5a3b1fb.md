# Impact-analysis transcript — ffmpeg @ 0a37d5a3b1fb — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ff_vk_shader_init` (libavutil/vulkan.c), arity 5->10
- truth: [['libavfilter/vf_avgblur_vulkan.c', 'init_filter'], ['libavfilter/vf_blend_vulkan.c', 'init_filter'], ['libavfilter/vf_bwdif_vulkan.c', 'init_filter'], ['libavfilter/vf_chromaber_vulkan.c', 'init_filter'], ['libavfilter/vf_flip_vulkan.c', 'init_filter'], ['libavfilter/vf_gblur_vulkan.c', 'init_filter'], ['libavfilter/vf_nlmeans_vulkan.c', 'init_denoise_pipeline'], ['libavfilter/vf_nlmeans_vulkan.c', 'init_weights_pipeline'], ['libavfilter/vf_overlay_vulkan.c', 'init_filter'], ['libavfilter/vf_scale_vulkan.c', 'init_filter'], ['libavfilter/vf_transpose_vulkan.c', 'init_filter'], ['libavfilter/vf_xfade_vulkan.c', 'init_vulkan'], ['libavfilter/vsrc_testsrc_vulkan.c', 'init_filter']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1072+111, stop=tool_use)_

**Reasoning:** Let me search for references to ff_vk_shader_init.


- `find_references(name=ff_vk_shader_init, max_results=200)` →

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

- `grep(pattern=ff_vk_shader_init, version=old, max_results=200)` →

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

### Turn 2  _(tok 2451+339, stop=tool_use)_

**Reasoning:** Now I need to determine the enclosing function for each call site. Let me read each file around those lines.

Let's read them in parallel.


**Says:** 

Now let me determine the enclosing function for each call site.






- `read_file(path=libavfilter/vf_avgblur_vulkan.c, start_line=55, end_line=95, version=old)` →

```
libavfilter/vf_avgblur_vulkan.c lines 55-95 of 260
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
```

- `read_file(path=libavfilter/vf_blend_vulkan.c, start_line=110, end_line=160, version=old)` →

```
libavfilter/vf_blend_vulkan.c lines 110-160 of 401
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
```

- `read_file(path=libavfilter/vf_bwdif_vulkan.c, start_line=95, end_line=130, version=old)` →

```
libavfilter/vf_bwdif_vulkan.c lines 95-130 of 416
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

- `read_file(path=libavfilter/vf_chromaber_vulkan.c, start_line=75, end_line=105, version=old)` →

```
libavfilter/vf_chromaber_vulkan.c lines 75-105 of 261
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
```

### Turn 3  _(tok 5737+122, stop=tool_use)_

**Reasoning:** Need the function definition line for chromaber (line ~72). Let me check line 70-75. Also flip, gblur, nlmeans, overlay, scale, transpose, xfade, testsrc.


- `read_file(path=libavfilter/vf_chromaber_vulkan.c, start_line=65, end_line=75, version=old)` →

```
libavfilter/vf_chromaber_vulkan.c lines 65-75 of 261
   65|     C(1,     imageStore(output_img[idx], pos, res);                            )
   66|     C(0, }                                                                     )
   67| };
   68| 
   69| static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
   70| {
   71|     int err;
   72|     uint8_t *spv_data;
   73|     size_t spv_len;
   74|     void *spv_opaque = NULL;
   75|     ChromaticAberrationVulkanContext *s = ctx->priv;
```

### Turn 4  _(tok 6056+163, stop=tool_use)_

**Reasoning:** Wait — line 93/94/95 belong to init_filter defined at line 69. Yes.

Now flip, gblur, nlmeans (two sites), overlay, scale, transpose, xfade, testsrc. Also bwdif — need the enclosing function name; the function starts around line 93-94. Let me check bwdif lines 90-95.


- `read_file(path=libavfilter/vf_bwdif_vulkan.c, start_line=88, end_line=96, version=old)` →

```
libavfilter/vf_bwdif_vulkan.c lines 88-96 of 416
   88|     C(1,     vec4 interpol = mix(interpolate_cur, interpolate_all, interpolate_cnd1);                 )
   89|     C(1,     interpol = clamp(interpol, fd - diff, fd + diff);                                        )
   90|     C(1,     return mix(interpol, fd, diff_mask);                                                     )
   91|     C(0, }                                                                                            )
   92| };
   93| 
   94| static av_cold int init_filter(AVFilterContext *ctx)
   95| {
   96|     int err;
```

### Turn 5  _(tok 6404+162, stop=tool_use)_

**Reasoning:** Wait — bwdif init_filter is defined at line 94, and the call at line 116. Good.

Now flip (69), gblur (222, 224), nlmeans (244, 431), overlay (108), scale (149), transpose (68), xfade (342), testsrc (88).


- `read_file(path=libavfilter/vf_flip_vulkan.c, start_line=45, end_line=80, version=old)` →

```
libavfilter/vf_flip_vulkan.c lines 45-80 of 301
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

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 6718+1613, stop=tool_use, forced)_

**Reasoning:** I need to make a decision. Remaining unknown enclosing functions: gblur (222,224), nlmeans (244, 431), overlay (108), scale (149), transpose (68), xfade (342), testsrc (88).

Based on FFmpeg conventions:
- vf_gblur_vulkan.c: `init_filter(AVFilterContext *ctx)` — yes, gblur has init_filter.
- vf_nlmeans_vulkan.c: line 244 is inside a helper function — in FFmpeg master, vf_nlmeans_vulkan.c has `init_pipeline_...`? Let me recall. The nlmeans vulkan filter was added in 2024. Functions: `nlmeans_vulkan_init_weights`? Actually in the code:

```c
static int init_weights_pipeline(FFVkSPIRVShader *shd, FFVulkanPipeline *pl, ...)
```
Hmm. Let me think. The actual code around line 244 in vf_nlmeans_vulkan.c:

```c
static int nlmeans_weights_init(FFVulkanPipeline *pl, FFVkSPIRVShader *shd, ...)
```

Hmm, I recall in nlmeans_vulkan there's:

```c
static int init_weights_pl(FFVulkanPipeline *pl, FFVkSPIRVShader *shd, int planes, int p, int r)
```

And at line 431, `static av_cold int init_filter(AVFilterContext *ctx)`.

Actually I recall the nlmeans vulkan code structure from FFmpeg:

```c
static int init_weights_pipeline(FFVulkanContext *vkctx, FFVkExecPool *exec,
                                 FFVkQueueFamilyCtx *qf, FFVulkanPipeline *pl,
                                 FFVkSPIRVShader *shd, ...)
```

Hmm, hard to be sure. And there's `init_pipeline`? Let me think about what I know of the file: functions include `nlmeans_vulkan_init`, `filter_frame`, `config_props`, `uninit`, `init_filter`, and helpers `init_weights_pipeline` / `free_weights_pipeline`.

Actually the code I recall:

```c
static int init_weights_pl(FFVulkanPipeline *pl, FFVkSPIRVShader *shd, ...)
```

Hmm. Given uncertainty, I could give best guess. The task says "call submit_callers now with your best decision".

Let me reason more carefully about nlmeans_vulkan.c. I believe the file contains:

```c
static int init_weights_pipeline(FFVkSPIRVShader *shd, FFVulkanPipeline *pl,
                                 FFVulkanContext *vkctx, FFVkExecPool *exec,
                                 FFVkQueueFamilyCtx *qf, int planes, int p, int r)
```

Hmm, but signature at call site is `ff_vk_shader_init(pl, shd, "nlmeans_weights", ...)` — pl and shd are pointers passed in, so it's a helper function taking FFVulkanPipeline *pl and FFVkSPIRVShader *shd.

In FFmpeg master, vf_nlmeans_vulkan.c has:

```c
static int init_weights_pipeline(FFVulkanPipeline *pl, FFVkSPIRVShader *shd,
                                 FFVulkanContext *vkctx, FFVkExecPool *exec,
                                 FFVkQueueFamilyCtx *qf, int planes,
                                 int p, int r)
```

I'm fairly confident the helper is named `init_weights_pipeline` and there's a matching `free_weights_pipeline`. And the second call at line 431 is inside `init_filter`.

Hmm, actually I have some memory of the nlmeans vulkan filter code:

```c
static av_cold int init_filter(AVFilterContext *ctx)
```
Yes.

For overlay_vulkan.c: `init_filter(AVFilterContext *avctx)`. Yes — overlay vulkan has `static av_cold int init_filter(AVFilterContext *avctx)`.

scale_vulkan.c: `static av_cold int config_props(AVFilterLink *outlink)` — In vf_scale_vulkan.c, the shader init happens inside `config_props`. Yes! In scale_vulkan, init happens in config_props (line ~149). Indeed vf_scale_vulkan.c's `config_props` does all the pipeline setup. Correct.

transpose_vulkan.c: `static av_cold int init_filter(AVFilterContext *ctx)`. Yes.

xfade_vulkan.c: `static av_cold int init_filter(AVFilterContext *avctx)` — hmm, in vf_xfade_vulkan.c there's `static av_cold int init_filter(AVFilterContext *avctx, int mode)`? Let me think. vf_xfade_vulkan.c has functions: `xfade_frame`, `config_output`, `init_filter`. Line 342 — the file is ~800 lines with transition shader strings. `init_filter` likely around line 300s. I'll say `init_filter`.

vsrc_testsrc_vulkan.c: `static av_cold int init_filter(AVFilterContext *avctx)`? Hmm, testsrc vulkan: functions are `config_props`, `init_filter`, `testsrc_frame`. Line 88 — probably in `init_filter`. Actually vsrc_testsrc_vulkan.c: I recall `static av_cold int init_filter(AVFilterContext *avctx, AVFrame *frame)`? Hmm. There's `config_props` and `init_filter`. Let me guess `init_filter`.

gblur_vulkan.c: `static av_cold int init_filter(AVFilterContext *ctx)` — yes, two calls at 222 and 224 both in init_filter.

I'll submit these.

Note also: the gblur file — I'm fairly confident it's init_filter.

Overall confidence: medium.


- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_weights_pipeline", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "config_props", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 3, "n_truth": 4, "tp": 2, "precision": 0.6666666666666666, "recall": 0.5, "f1": 0.5714285714285715}`

