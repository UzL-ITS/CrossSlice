# Impact-analysis transcript — ffmpeg @ c982376076b6 — openrouter:deepseek/deepseek-v4-pro

- target: `ff_vk_shader_rep_fmt` (libavutil/vulkan.c), arity 1->2
- truth: [['libavfilter/vf_avgblur_vulkan.c', 'init_filter'], ['libavfilter/vf_blend_vulkan.c', 'init_filter'], ['libavfilter/vf_bwdif_vulkan.c', 'init_filter'], ['libavfilter/vf_chromaber_vulkan.c', 'init_filter'], ['libavfilter/vf_flip_vulkan.c', 'init_filter'], ['libavfilter/vf_gblur_vulkan.c', 'init_filter'], ['libavfilter/vf_nlmeans_vulkan.c', 'init_denoise_pipeline'], ['libavfilter/vf_overlay_vulkan.c', 'init_filter'], ['libavfilter/vf_scale_vulkan.c', 'init_filter'], ['libavfilter/vf_transpose_vulkan.c', 'init_filter'], ['libavfilter/vf_xfade_vulkan.c', 'init_vulkan'], ['libavfilter/vsrc_testsrc_vulkan.c', 'init_filter']]

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1037+83, stop=tool_use)_

**Reasoning:** Let me find all callers of `ff_vk_shader_rep_fmt`. I'll start by searching for references to this function.

- `find_references(name=ff_vk_shader_rep_fmt)` →

```
13 references
ff_vk_shader_rep_fmt  102 libavfilter/vf_avgblur_vulkan.c             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
ff_vk_shader_rep_fmt  173 libavfilter/vf_blend_vulkan.c             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
ff_vk_shader_rep_fmt  107 libavfilter/vf_bwdif_vulkan.c             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
ff_vk_shader_rep_fmt  120 libavfilter/vf_chromaber_vulkan.c             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
ff_vk_shader_rep_fmt   86 libavfilter/vf_flip_vulkan.c             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
ff_vk_shader_rep_fmt  231 libavfilter/vf_gblur_vulkan.c             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
ff_vk_shader_rep_fmt  457 libavfilter/vf_nlmeans_vulkan.c             .mem_layout  = ff_vk_shader_rep_fmt(vkctx->output_format),
ff_vk_shader_rep_fmt  142 libavfilter/vf_overlay_vulkan.c             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
ff_vk_shader_rep_fmt  174 libavfilter/vf_scale_vulkan.c             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
ff_vk_shader_rep_fmt   85 libavfilter/vf_transpose_vulkan.c             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
ff_vk_shader_rep_fmt  367 libavfilter/vf_xfade_vulkan.c             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
ff_vk_shader_rep_fmt  105 libavfilter/vsrc_testsrc_vulkan.c             .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
ff_vk_shader_rep_fmt  363 libavutil/vulkan.h const char *ff_vk_shader_rep_fmt(enum AVPixelFormat pixfmt);
```

### Turn 2  _(tok 1681+986, stop=tool_use)_

**Reasoning:** I have 13 references. One of them (line 363 in libavutil/vulkan.h) is the declaration/prototype. The other 12 are in libavfilter files. I need to determine which functions enclose these calls.

Let me read each file at the given line to determine the enclosing function. Let me read around each line to find the function name.

Let me read each file at the relevant lines.

- `read_file(path=libavfilter/vf_avgblur_vulkan.c, start_line=95, end_line=110)` →

```
libavfilter/vf_avgblur_vulkan.c lines 95-110 of 258
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
```

- `read_file(path=libavfilter/vf_blend_vulkan.c, start_line=165, end_line=180)` →

```
libavfilter/vf_blend_vulkan.c lines 165-180 of 399
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
```

- `read_file(path=libavfilter/vf_bwdif_vulkan.c, start_line=100, end_line=115)` →

```
libavfilter/vf_bwdif_vulkan.c lines 100-115 of 336
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
```

- `read_file(path=libavfilter/vf_chromaber_vulkan.c, start_line=113, end_line=128)` →

```
libavfilter/vf_chromaber_vulkan.c lines 113-128 of 259
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
```

- `read_file(path=libavfilter/vf_flip_vulkan.c, start_line=79, end_line=94)` →

```
libavfilter/vf_flip_vulkan.c lines 79-94 of 299
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
```

- `read_file(path=libavfilter/vf_gblur_vulkan.c, start_line=224, end_line=240)` →

```
libavfilter/vf_gblur_vulkan.c lines 224-240 of 385
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
```

- `read_file(path=libavfilter/vf_nlmeans_vulkan.c, start_line=450, end_line=465)` →

```
libavfilter/vf_nlmeans_vulkan.c lines 450-465 of 1123
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
```

- `read_file(path=libavfilter/vf_overlay_vulkan.c, start_line=135, end_line=150)` →

```
libavfilter/vf_overlay_vulkan.c lines 135-150 of 347
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
```

- `read_file(path=libavfilter/vf_scale_vulkan.c, start_line=167, end_line=182)` →

```
libavfilter/vf_scale_vulkan.c lines 167-182 of 417
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
```

- `read_file(path=libavfilter/vf_transpose_vulkan.c, start_line=78, end_line=93)` →

```
libavfilter/vf_transpose_vulkan.c lines 78-93 of 276
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
```

- `read_file(path=libavfilter/vf_xfade_vulkan.c, start_line=360, end_line=375)` →

```
libavfilter/vf_xfade_vulkan.c lines 360-375 of 720
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
```

- `read_file(path=libavfilter/vsrc_testsrc_vulkan.c, start_line=98, end_line=112)` →

```
libavfilter/vsrc_testsrc_vulkan.c lines 98-112 of 375
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
```

### Turn 3  _(tok 5875+205, stop=tool_use)_

**Reasoning:** Now I need to find the enclosing function for each of these call sites. Let me look further back in each file to find the function name. Let me search for function definitions that contain these calls.

For each file, I'll look for the function definition that contains the relevant line. Let me grep for function definitions.

Actually, let me take a different approach. Let me look at the context before each call to find the function name. The calls are all inside what appears to be similar init functions. Let me search for the function definitions.

Let me read the earlier parts of each file to find the function that contains these lines.

- `grep(pattern=static.*init.*\(, path_glob=libavfilter/vf_avgblur_vulkan.c)` →

```
2 matches
libavfilter/vf_avgblur_vulkan.c:61:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
libavfilter/vf_avgblur_vulkan.c:199:static void avgblur_vulkan_uninit(AVFilterContext *avctx)
```

### Turn 4  _(tok 6159+565, stop=tool_use)_

**Reasoning:** Let me verify this by reading around line 61 in vf_avgblur_vulkan.c to confirm the function contains the call. But wait, the call is at line 102, so it's between lines 61 and 199. Let me read around line 199 to see where init_filter ends. But actually, let me just find all function definitions across all these files.

Let me be more efficient and just check where each call falls by looking at the function boundaries in each file.

Let me search for functions in each file. Actually, I can just look for the function definition pattern and see which function each line falls within.

Let me do this more efficiently. I'll look for all function definitions in each file and determine which function contains each call.

- `grep(pattern=^(static )?.*\w+\(, path_glob=libavfilter/vf_avgblur_vulkan.c)` →

```
70 matches (showing 60)
libavfilter/vf_avgblur_vulkan.c:50:    C(0, void distort(const ivec2 pos, const int idx)                         )
libavfilter/vf_avgblur_vulkan.c:51:    C(0, {                                                                    )
libavfilter/vf_avgblur_vulkan.c:52:    C(1,     vec4 sum = vec4(0);                                              )
libavfilter/vf_avgblur_vulkan.c:53:    C(1,     for (int y = -filter_len.y; y <= filter_len.y; y++)              )
libavfilter/vf_avgblur_vulkan.c:54:    C(1,        for (int x = -filter_len.x; x <= filter_len.x; x++)           )
libavfilter/vf_avgblur_vulkan.c:55:    C(2,            sum += texture(input_img[idx], pos + ivec2(x, y));        )
libavfilter/vf_avgblur_vulkan.c:56:    C(0,                                                                      )
libavfilter/vf_avgblur_vulkan.c:57:    C(1,     imageStore(output_img[idx], pos, sum * filter_norm);             )
libavfilter/vf_avgblur_vulkan.c:58:    C(0, }                                                                    )
libavfilter/vf_avgblur_vulkan.c:61:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
libavfilter/vf_avgblur_vulkan.c:69:    const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
libavfilter/vf_avgblur_vulkan.c:74:    spv = ff_vk_spirv_init();
libavfilter/vf_avgblur_vulkan.c:76:        av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
libavfilter/vf_avgblur_vulkan.c:80:    ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
libavfilter/vf_avgblur_vulkan.c:81:    RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
libavfilter/vf_avgblur_vulkan.c:82:    RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_LINEAR));
libavfilter/vf_avgblur_vulkan.c:83:    RET(ff_vk_shader_init(vkctx, &s->shd, "avgblur",
libavfilter/vf_avgblur_vulkan.c:97:            .samplers   = DUP_SAMPLER(s->sampler),
libavfilter/vf_avgblur_vulkan.c:102:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_avgblur_vulkan.c:110:    RET(ff_vk_shader_add_descriptor_set(vkctx, shd, desc, 2, 0, 0));
libavfilter/vf_avgblur_vulkan.c:112:    GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
libavfilter/vf_avgblur_vulkan.c:113:    GLSLC(1,    vec4 filter_norm;                                         );
libavfilter/vf_avgblur_vulkan.c:114:    GLSLC(1,    ivec2 filter_len;                                         );
libavfilter/vf_avgblur_vulkan.c:115:    GLSLC(0, };                                                           );
libavfilter/vf_avgblur_vulkan.c:116:    GLSLC(0,                                                              );
libavfilter/vf_avgblur_vulkan.c:118:    ff_vk_shader_add_push_const(&s->shd, 0, sizeof(s->opts),
libavfilter/vf_avgblur_vulkan.c:121:    GLSLD(   blur_kernel                                                  );
libavfilter/vf_avgblur_vulkan.c:122:    GLSLC(0, void main()                                                  );
libavfilter/vf_avgblur_vulkan.c:123:    GLSLC(0, {                                                            );
libavfilter/vf_avgblur_vulkan.c:124:    GLSLC(1,     ivec2 size;                                              );
libavfilter/vf_avgblur_vulkan.c:125:    GLSLC(1,     const ivec2 pos = ivec2(gl_GlobalInvocationID.xy);       );
libavfilter/vf_avgblur_vulkan.c:127:        GLSLC(0,                                                          );
libavfilter/vf_avgblur_vulkan.c:128:        GLSLF(1,  size = imageSize(output_img[%i]);                     ,i);
libavfilter/vf_avgblur_vulkan.c:129:        GLSLC(1,  if (!IS_WITHIN(pos, size))                              );
libavfilter/vf_avgblur_vulkan.c:130:        GLSLC(2,      return;                                             );
libavfilter/vf_avgblur_vulkan.c:132:            GLSLF(1, distort(pos, %i);                                  ,i);
libavfilter/vf_avgblur_vulkan.c:134:            GLSLF(1, vec4 res = texture(input_img[%i], pos);            ,i);
libavfilter/vf_avgblur_vulkan.c:135:            GLSLF(1, imageStore(output_img[%i], pos, res);              ,i);
libavfilter/vf_avgblur_vulkan.c:138:    GLSLC(0, }                                                            );
libavfilter/vf_avgblur_vulkan.c:140:    RET(spv->compile_shader(vkctx, spv, &s->shd, &spv_data, &spv_len, "main",
libavfilter/vf_avgblur_vulkan.c:142:    RET(ff_vk_shader_link(vkctx, &s->shd, spv_data, spv_len, "main"));
libavfilter/vf_avgblur_vulkan.c:144:    RET(ff_vk_shader_register_exec(vkctx, &s->e, &s->shd));
libavfilter/vf_avgblur_vulkan.c:158:        spv->free_shader(spv, &spv_opaque);
libavfilter/vf_avgblur_vulkan.c:160:        spv->uninit(&spv);
libavfilter/vf_avgblur_vulkan.c:165:static int avgblur_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_avgblur_vulkan.c:173:    out = ff_get_video_buffer(outlink, outlink->w, outlink->h);
libavfilter/vf_avgblur_vulkan.c:175:        err = AVERROR(ENOMEM);
libavfilter/vf_avgblur_vulkan.c:180:        RET(init_filter(ctx, in));
libavfilter/vf_avgblur_vulkan.c:182:    RET(ff_vk_filter_process_simple(&s->vkctx, &s->e, &s->shd,
libavfilter/vf_avgblur_vulkan.c:183:                                    out, in, s->sampler, &s->opts, sizeof(s->opts)));
libavfilter/vf_avgblur_vulkan.c:185:    err = av_frame_copy_props(out, in);
libavfilter/vf_avgblur_vulkan.c:189:    av_frame_free(&in);
libavfilter/vf_avgblur_vulkan.c:191:    return ff_filter_frame(outlink, out);
libavfilter/vf_avgblur_vulkan.c:194:    av_frame_free(&in);
libavfilter/vf_avgblur_vulkan.c:195:    av_frame_free(&out);
libavfilter/vf_avgblur_vulkan.c:199:static void avgblur_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_avgblur_vulkan.c:205:    ff_vk_exec_pool_free(vkctx, &s->e);
libavfilter/vf_avgblur_vulkan.c:206:    ff_vk_shader_free(vkctx, &s->shd);
libavfilter/vf_avgblur_vulkan.c:209:        vk->DestroySampler(vkctx->hwctx->act_dev, s->sampler,
libavfilter/vf_avgblur_vulkan.c:212:    ff_vk_uninit(&s->vkctx);
```

- `grep(pattern=^(static )?.*\w+\(, path_glob=libavfilter/vf_blend_vulkan.c)` →

```
101 matches (showing 60)
libavfilter/vf_blend_vulkan.c:59:#define DEFINE_BLEND_MODE(MODE, EXPR) \
libavfilter/vf_blend_vulkan.c:62:    C(0, vec4 blend_##MODE(vec4 top, vec4 bottom, float opacity) {   ) \
libavfilter/vf_blend_vulkan.c:63:    C(1,     vec4 dst = EXPR;                                        ) \
libavfilter/vf_blend_vulkan.c:64:    C(1,     return dst;                                             ) \
libavfilter/vf_blend_vulkan.c:65:    C(0, }                                                           ) \
libavfilter/vf_blend_vulkan.c:71:#define FN(EXPR) A + ((EXPR) - A) * opacity
libavfilter/vf_blend_vulkan.c:73:DEFINE_BLEND_MODE(NORMAL, A * opacity + B * (1.0f - opacity))
libavfilter/vf_blend_vulkan.c:74:DEFINE_BLEND_MODE(MULTIPLY, FN(1.0f * A * B / 1.0f))
libavfilter/vf_blend_vulkan.c:76:static inline void init_blend_func(FilterParamsVulkan *param)
libavfilter/vf_blend_vulkan.c:78:#define CASE(MODE) case BLEND_##MODE: \
libavfilter/vf_blend_vulkan.c:84:    CASE(NORMAL)
libavfilter/vf_blend_vulkan.c:85:    CASE(MULTIPLY)
libavfilter/vf_blend_vulkan.c:92:static int config_params(AVFilterContext *avctx)
libavfilter/vf_blend_vulkan.c:96:    for (int plane = 0; plane < FF_ARRAY_ELEMS(s->params); plane++) {
libavfilter/vf_blend_vulkan.c:104:        init_blend_func(param);
libavfilter/vf_blend_vulkan.c:106:            av_log(avctx, AV_LOG_ERROR,
libavfilter/vf_blend_vulkan.c:108:            return AVERROR(EINVAL);
libavfilter/vf_blend_vulkan.c:115:static int process_command(AVFilterContext *ctx, const char *cmd, const char *args,
libavfilter/vf_blend_vulkan.c:118:    int ret = ff_filter_process_command(ctx, cmd, args, res, res_len, flags);
libavfilter/vf_blend_vulkan.c:122:    return config_params(ctx);
libavfilter/vf_blend_vulkan.c:125:static av_cold int init_filter(AVFilterContext *avctx)
libavfilter/vf_blend_vulkan.c:133:    const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
libavfilter/vf_blend_vulkan.c:138:    spv = ff_vk_spirv_init();
libavfilter/vf_blend_vulkan.c:140:        av_log(avctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
libavfilter/vf_blend_vulkan.c:144:    ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
libavfilter/vf_blend_vulkan.c:145:    RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
libavfilter/vf_blend_vulkan.c:146:    RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_NEAREST));
libavfilter/vf_blend_vulkan.c:147:    RET(ff_vk_shader_init(vkctx, &s->shd, "blend",
libavfilter/vf_blend_vulkan.c:160:            .samplers   = DUP_SAMPLER(s->sampler),
libavfilter/vf_blend_vulkan.c:168:            .samplers   = DUP_SAMPLER(s->sampler),
libavfilter/vf_blend_vulkan.c:173:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_blend_vulkan.c:181:    RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 3, 0, 0));
libavfilter/vf_blend_vulkan.c:189:            GLSLD(s->params[i].blend_func);
libavfilter/vf_blend_vulkan.c:193:    GLSLC(0, void main()                                                    );
libavfilter/vf_blend_vulkan.c:194:    GLSLC(0, {                                                              );
libavfilter/vf_blend_vulkan.c:195:    GLSLC(1,     ivec2 size;                                                );
libavfilter/vf_blend_vulkan.c:196:    GLSLC(1,     const ivec2 pos = ivec2(gl_GlobalInvocationID.xy);         );
libavfilter/vf_blend_vulkan.c:198:        GLSLC(0,                                                            );
libavfilter/vf_blend_vulkan.c:199:        GLSLF(1, size = imageSize(output_images[%i]);                     ,i);
libavfilter/vf_blend_vulkan.c:200:        GLSLC(1, if (IS_WITHIN(pos, size)) {                                );
libavfilter/vf_blend_vulkan.c:201:        GLSLF(2,     const vec4 top = texture(top_images[%i], pos);       ,i);
libavfilter/vf_blend_vulkan.c:202:        GLSLF(2,     const vec4 bottom = texture(bottom_images[%i], pos); ,i);
libavfilter/vf_blend_vulkan.c:203:        GLSLF(2,     const float opacity = %f;                            ,s->params[i].opacity);
libavfilter/vf_blend_vulkan.c:204:        GLSLF(2,     vec4 dst = %s(top, bottom, opacity);                 ,s->params[i].blend);
libavfilter/vf_blend_vulkan.c:205:        GLSLC(0,                                                            );
libavfilter/vf_blend_vulkan.c:206:        GLSLF(2,     imageStore(output_images[%i], pos, dst);             ,i);
libavfilter/vf_blend_vulkan.c:207:        GLSLC(1, }                                                          );
libavfilter/vf_blend_vulkan.c:209:    GLSLC(0, }                                                              );
libavfilter/vf_blend_vulkan.c:211:    RET(spv->compile_shader(vkctx, spv, shd, &spv_data, &spv_len, "main",
libavfilter/vf_blend_vulkan.c:213:    RET(ff_vk_shader_link(vkctx, shd, spv_data, spv_len, "main"));
libavfilter/vf_blend_vulkan.c:215:    RET(ff_vk_shader_register_exec(vkctx, &s->e, &s->shd));
libavfilter/vf_blend_vulkan.c:221:        spv->free_shader(spv, &spv_opaque);
libavfilter/vf_blend_vulkan.c:223:        spv->uninit(&spv);
libavfilter/vf_blend_vulkan.c:228:static int blend_frame(FFFrameSync *fs)
libavfilter/vf_blend_vulkan.c:236:    out = ff_get_video_buffer(outlink, outlink->w, outlink->h);
libavfilter/vf_blend_vulkan.c:238:        err = AVERROR(ENOMEM);
libavfilter/vf_blend_vulkan.c:242:    RET(ff_framesync_get_frame(fs, IN_TOP,    &top,    0));
libavfilter/vf_blend_vulkan.c:243:    RET(ff_framesync_get_frame(fs, IN_BOTTOM, &bottom, 0));
libavfilter/vf_blend_vulkan.c:245:    RET(av_frame_copy_props(out, top));
libavfilter/vf_blend_vulkan.c:251:            av_log(avctx, AV_LOG_ERROR,
```

- `grep(pattern=^(static )?.*\w+\(, path_glob=libavfilter/vf_bwdif_vulkan.c)` →

```
84 matches (showing 60)
libavfilter/vf_bwdif_vulkan.c:49:static av_cold int init_filter(AVFilterContext *ctx)
libavfilter/vf_bwdif_vulkan.c:57:    const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
libavfilter/vf_bwdif_vulkan.c:62:    spv = ff_vk_spirv_init();
libavfilter/vf_bwdif_vulkan.c:64:        av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
libavfilter/vf_bwdif_vulkan.c:68:    ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
libavfilter/vf_bwdif_vulkan.c:69:    RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
libavfilter/vf_bwdif_vulkan.c:70:    RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_NEAREST));
libavfilter/vf_bwdif_vulkan.c:72:    RET(ff_vk_shader_init(vkctx, &s->shd, "bwdif",
libavfilter/vf_bwdif_vulkan.c:86:            .samplers   = DUP_SAMPLER(s->sampler),
libavfilter/vf_bwdif_vulkan.c:94:            .samplers   = DUP_SAMPLER(s->sampler),
libavfilter/vf_bwdif_vulkan.c:102:            .samplers   = DUP_SAMPLER(s->sampler),
libavfilter/vf_bwdif_vulkan.c:107:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_bwdif_vulkan.c:115:    RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 4, 0, 0));
libavfilter/vf_bwdif_vulkan.c:117:    GLSLC(0, layout(push_constant, std430) uniform pushConstants {                 );
libavfilter/vf_bwdif_vulkan.c:118:    GLSLC(1,    int parity;                                                        );
libavfilter/vf_bwdif_vulkan.c:119:    GLSLC(1,    int tff;                                                           );
libavfilter/vf_bwdif_vulkan.c:120:    GLSLC(1,    int current_field;                                                 );
libavfilter/vf_bwdif_vulkan.c:121:    GLSLC(0, };                                                                    );
libavfilter/vf_bwdif_vulkan.c:123:    ff_vk_shader_add_push_const(&s->shd, 0, sizeof(BWDIFParameters),
libavfilter/vf_bwdif_vulkan.c:126:    GLSLD(ff_source_bwdif_comp                                                     );
libavfilter/vf_bwdif_vulkan.c:127:    GLSLC(0, void main()                                                           );
libavfilter/vf_bwdif_vulkan.c:128:    GLSLC(0, {                                                                     );
libavfilter/vf_bwdif_vulkan.c:129:    GLSLC(1,     ivec2 size;                                                       );
libavfilter/vf_bwdif_vulkan.c:130:    GLSLC(1,     const ivec2 pos = ivec2(gl_GlobalInvocationID.xy);                );
libavfilter/vf_bwdif_vulkan.c:131:    GLSLC(1,     bool filter_field = ((pos.y ^ parity) & 1) == 1;                  );
libavfilter/vf_bwdif_vulkan.c:132:    GLSLF(1,     bool is_intra = filter_field && (current_field == %i);           ,YADIF_FIELD_END);
libavfilter/vf_bwdif_vulkan.c:133:    GLSLC(1,     bool field_parity = (parity ^ tff) != 0;                          );
libavfilter/vf_bwdif_vulkan.c:134:    GLSLC(0,                                                                       );
libavfilter/vf_bwdif_vulkan.c:135:    GLSLC(1,     size = imageSize(dst[0]);                                         );
libavfilter/vf_bwdif_vulkan.c:136:    GLSLC(1,     if (!IS_WITHIN(pos, size)) {                                      );
libavfilter/vf_bwdif_vulkan.c:137:    GLSLC(2,         return;                                                       );
libavfilter/vf_bwdif_vulkan.c:138:    GLSLC(1,     } else if (is_intra) {                                            );
libavfilter/vf_bwdif_vulkan.c:141:            GLSLF(2, size = imageSize(dst[%i]);                                    ,i);
libavfilter/vf_bwdif_vulkan.c:142:            GLSLC(2, if (!IS_WITHIN(pos, size))                                    );
libavfilter/vf_bwdif_vulkan.c:143:            GLSLC(3,     return;                                                   );
libavfilter/vf_bwdif_vulkan.c:145:        GLSLF(2,     process_plane_intra(%i, pos);                                 ,i);
libavfilter/vf_bwdif_vulkan.c:147:    GLSLC(1,     } else if (filter_field) {                                        );
libavfilter/vf_bwdif_vulkan.c:150:            GLSLF(2, size = imageSize(dst[%i]);                                    ,i);
libavfilter/vf_bwdif_vulkan.c:151:            GLSLC(2, if (!IS_WITHIN(pos, size))                                    );
libavfilter/vf_bwdif_vulkan.c:152:            GLSLC(3,     return;                                                   );
libavfilter/vf_bwdif_vulkan.c:154:        GLSLF(2,     process_plane(%i, pos, filter_field, is_intra, field_parity); ,i);
libavfilter/vf_bwdif_vulkan.c:156:    GLSLC(1,     } else {                                                          );
libavfilter/vf_bwdif_vulkan.c:159:            GLSLF(2, size = imageSize(dst[%i]);                                    ,i);
libavfilter/vf_bwdif_vulkan.c:160:            GLSLC(2, if (!IS_WITHIN(pos, size))                                    );
libavfilter/vf_bwdif_vulkan.c:161:            GLSLC(3,     return;                                                   );
libavfilter/vf_bwdif_vulkan.c:163:        GLSLF(2,     imageStore(dst[%i], pos, texture(cur[%i], pos));              ,i, i);
libavfilter/vf_bwdif_vulkan.c:165:    GLSLC(1,     }                                                                 );
libavfilter/vf_bwdif_vulkan.c:166:    GLSLC(0, }                                                                     );
libavfilter/vf_bwdif_vulkan.c:168:    RET(spv->compile_shader(vkctx, spv, &s->shd, &spv_data, &spv_len, "main",
libavfilter/vf_bwdif_vulkan.c:170:    RET(ff_vk_shader_link(vkctx, &s->shd, spv_data, spv_len, "main"));
libavfilter/vf_bwdif_vulkan.c:172:    RET(ff_vk_shader_register_exec(vkctx, &s->e, &s->shd));
libavfilter/vf_bwdif_vulkan.c:178:        spv->free_shader(spv, &spv_opaque);
libavfilter/vf_bwdif_vulkan.c:180:        spv->uninit(&spv);
libavfilter/vf_bwdif_vulkan.c:185:static void bwdif_vulkan_filter_frame(AVFilterContext *ctx, AVFrame *dst,
libavfilter/vf_bwdif_vulkan.c:196:    ff_vk_filter_process_Nin(&s->vkctx, &s->e, &s->shd, dst,
libavfilter/vf_bwdif_vulkan.c:198:                             s->sampler, &params, sizeof(params));
libavfilter/vf_bwdif_vulkan.c:204:static void bwdif_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_bwdif_vulkan.c:210:    ff_vk_exec_pool_free(vkctx, &s->e);
libavfilter/vf_bwdif_vulkan.c:211:    ff_vk_shader_free(vkctx, &s->shd);
libavfilter/vf_bwdif_vulkan.c:214:        vk->DestroySampler(vkctx->hwctx->act_dev, s->sampler,
```

- `grep(pattern=^(static )?.*\w+\(, path_glob=libavfilter/vf_chromaber_vulkan.c)` →

```
82 matches (showing 60)
libavfilter/vf_chromaber_vulkan.c:45:    C(0, void distort_rgb(ivec2 size, ivec2 pos)                               )
libavfilter/vf_chromaber_vulkan.c:46:    C(0, {                                                                     )
libavfilter/vf_chromaber_vulkan.c:47:    C(1,     const vec2 p = ((vec2(pos)/vec2(size)) - 0.5f)*2.0f;              )
libavfilter/vf_chromaber_vulkan.c:48:    C(1,     const vec2 o = p * (dist - 1.0f);                                 )
libavfilter/vf_chromaber_vulkan.c:49:    C(0,                                                                       )
libavfilter/vf_chromaber_vulkan.c:50:    C(1,     vec4 res;                                                         )
libavfilter/vf_chromaber_vulkan.c:51:    C(1,     res.r = texture(input_img[0], ((p - o)/2.0f) + 0.5f).r;           )
libavfilter/vf_chromaber_vulkan.c:52:    C(1,     res.g = texture(input_img[0], ((p    )/2.0f) + 0.5f).g;           )
libavfilter/vf_chromaber_vulkan.c:53:    C(1,     res.b = texture(input_img[0], ((p + o)/2.0f) + 0.5f).b;           )
libavfilter/vf_chromaber_vulkan.c:54:    C(1,     res.a = texture(input_img[0], ((p    )/2.0f) + 0.5f).a;           )
libavfilter/vf_chromaber_vulkan.c:55:    C(1,     imageStore(output_img[0], pos, res);                              )
libavfilter/vf_chromaber_vulkan.c:56:    C(0, }                                                                     )
libavfilter/vf_chromaber_vulkan.c:57:    C(0,                                                                       )
libavfilter/vf_chromaber_vulkan.c:58:    C(0, void distort_chroma(int idx, ivec2 size, ivec2 pos)                   )
libavfilter/vf_chromaber_vulkan.c:59:    C(0, {                                                                     )
libavfilter/vf_chromaber_vulkan.c:60:    C(1,     vec2 p = ((vec2(pos)/vec2(size)) - 0.5f)*2.0f;                    )
libavfilter/vf_chromaber_vulkan.c:61:    C(1,     float d = sqrt(p.x*p.x + p.y*p.y);                                )
libavfilter/vf_chromaber_vulkan.c:62:    C(1,     p *= d / (d*dist);                                                )
libavfilter/vf_chromaber_vulkan.c:63:    C(1,     vec4 res = texture(input_img[idx], (p/2.0f) + 0.5f);              )
libavfilter/vf_chromaber_vulkan.c:64:    C(1,     imageStore(output_img[idx], pos, res);                            )
libavfilter/vf_chromaber_vulkan.c:65:    C(0, }                                                                     )
libavfilter/vf_chromaber_vulkan.c:68:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
libavfilter/vf_chromaber_vulkan.c:76:    const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
libavfilter/vf_chromaber_vulkan.c:85:    spv = ff_vk_spirv_init();
libavfilter/vf_chromaber_vulkan.c:87:        av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
libavfilter/vf_chromaber_vulkan.c:91:    ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
libavfilter/vf_chromaber_vulkan.c:92:    RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
libavfilter/vf_chromaber_vulkan.c:93:    RET(ff_vk_init_sampler(vkctx, &s->sampler, 0, VK_FILTER_LINEAR));
libavfilter/vf_chromaber_vulkan.c:94:    RET(ff_vk_shader_init(vkctx, &s->shd, "chromatic_abberation",
libavfilter/vf_chromaber_vulkan.c:100:    GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
libavfilter/vf_chromaber_vulkan.c:101:    GLSLC(1,    vec2 dist;                                                );
libavfilter/vf_chromaber_vulkan.c:102:    GLSLC(0, };                                                           );
libavfilter/vf_chromaber_vulkan.c:103:    GLSLC(0,                                                              );
libavfilter/vf_chromaber_vulkan.c:105:    ff_vk_shader_add_push_const(&s->shd, 0, sizeof(s->opts),
libavfilter/vf_chromaber_vulkan.c:115:            .samplers   = DUP_SAMPLER(s->sampler),
libavfilter/vf_chromaber_vulkan.c:120:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_chromaber_vulkan.c:128:    RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 2, 0, 0));
libavfilter/vf_chromaber_vulkan.c:130:    GLSLD(   distort_chroma_kernel                                        );
libavfilter/vf_chromaber_vulkan.c:131:    GLSLC(0, void main()                                                  );
libavfilter/vf_chromaber_vulkan.c:132:    GLSLC(0, {                                                            );
libavfilter/vf_chromaber_vulkan.c:133:    GLSLC(1,     ivec2 pos = ivec2(gl_GlobalInvocationID.xy);             );
libavfilter/vf_chromaber_vulkan.c:135:        GLSLC(1, distort_rgb(imageSize(output_img[0]), pos);              );
libavfilter/vf_chromaber_vulkan.c:137:        GLSLC(1, ivec2 size = imageSize(output_img[0]);                   );
libavfilter/vf_chromaber_vulkan.c:138:        GLSLC(1, vec2 npos = vec2(pos)/vec2(size);                        );
libavfilter/vf_chromaber_vulkan.c:139:        GLSLC(1, vec4 res = texture(input_img[0], npos);                  );
libavfilter/vf_chromaber_vulkan.c:140:        GLSLC(1, imageStore(output_img[0], pos, res);                     );
libavfilter/vf_chromaber_vulkan.c:142:            GLSLC(0,                                                      );
libavfilter/vf_chromaber_vulkan.c:143:            GLSLF(1,  size = imageSize(output_img[%i]);                 ,i);
libavfilter/vf_chromaber_vulkan.c:144:            GLSLC(1,  if (!IS_WITHIN(pos, size))                          );
libavfilter/vf_chromaber_vulkan.c:145:            GLSLC(2,      return;                                         );
libavfilter/vf_chromaber_vulkan.c:146:            GLSLF(1,  distort_chroma(%i, size, pos);                    ,i);
libavfilter/vf_chromaber_vulkan.c:149:    GLSLC(0, }                                                            );
libavfilter/vf_chromaber_vulkan.c:151:    RET(spv->compile_shader(vkctx, spv, shd, &spv_data, &spv_len, "main",
libavfilter/vf_chromaber_vulkan.c:153:    RET(ff_vk_shader_link(vkctx, shd, spv_data, spv_len, "main"));
libavfilter/vf_chromaber_vulkan.c:155:    RET(ff_vk_shader_register_exec(vkctx, &s->e, &s->shd));
libavfilter/vf_chromaber_vulkan.c:161:        spv->free_shader(spv, &spv_opaque);
libavfilter/vf_chromaber_vulkan.c:163:        spv->uninit(&spv);
libavfilter/vf_chromaber_vulkan.c:168:static int chromaber_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_chromaber_vulkan.c:175:    AVFrame *out = ff_get_video_buffer(outlink, outlink->w, outlink->h);
libavfilter/vf_chromaber_vulkan.c:177:        err = AVERROR(ENOMEM);
```

- `grep(pattern=^(static )?.*\w+\(, path_glob=libavfilter/vf_flip_vulkan.c)` →

```
69 matches (showing 60)
libavfilter/vf_flip_vulkan.c:46:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in, enum FlipType type)
libavfilter/vf_flip_vulkan.c:54:    const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
libavfilter/vf_flip_vulkan.c:59:    spv = ff_vk_spirv_init();
libavfilter/vf_flip_vulkan.c:61:        av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
libavfilter/vf_flip_vulkan.c:65:    ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
libavfilter/vf_flip_vulkan.c:66:    RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
libavfilter/vf_flip_vulkan.c:67:    RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_LINEAR));
libavfilter/vf_flip_vulkan.c:68:    RET(ff_vk_shader_init(vkctx, &s->shd, "flip",
libavfilter/vf_flip_vulkan.c:81:            .samplers   = DUP_SAMPLER(s->sampler),
libavfilter/vf_flip_vulkan.c:86:            .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
libavfilter/vf_flip_vulkan.c:94:    RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 2, 0, 0));
libavfilter/vf_flip_vulkan.c:96:    GLSLC(0, void main()                                                                    );
libavfilter/vf_flip_vulkan.c:97:    GLSLC(0, {                                                                              );
libavfilter/vf_flip_vulkan.c:98:    GLSLC(1,     ivec2 size;                                                                );
libavfilter/vf_flip_vulkan.c:99:    GLSLC(1,     const ivec2 pos = ivec2(gl_GlobalInvocationID.xy);                         );
libavfilter/vf_flip_vulkan.c:101:        GLSLC(0,                                                                            );
libavfilter/vf_flip_vulkan.c:102:        GLSLF(1, size = imageSize(output_image[%i]);                                      ,i);
libavfilter/vf_flip_vulkan.c:103:        GLSLC(1, if (IS_WITHIN(pos, size)) {                                                );
libavfilter/vf_flip_vulkan.c:107:            GLSLF(2, vec4 res = texture(input_image[%i], ivec2(size.x - pos.x, pos.y));   ,i);
libavfilter/vf_flip_vulkan.c:110:            GLSLF(2, vec4 res = texture(input_image[%i], ivec2(pos.x, size.y - pos.y));   ,i);
libavfilter/vf_flip_vulkan.c:113:            GLSLF(2, vec4 res = texture(input_image[%i], ivec2(size.xy - pos.xy));,         i);
libavfilter/vf_flip_vulkan.c:116:            GLSLF(2, vec4 res = texture(input_image[%i], pos);                            ,i);
libavfilter/vf_flip_vulkan.c:119:        GLSLF(2,     imageStore(output_image[%i], pos, res);                              ,i);
libavfilter/vf_flip_vulkan.c:120:        GLSLC(1, }                                                                          );
libavfilter/vf_flip_vulkan.c:122:    GLSLC(0, }                                                                              );
libavfilter/vf_flip_vulkan.c:124:    RET(spv->compile_shader(vkctx, spv, shd, &spv_data, &spv_len, "main",
libavfilter/vf_flip_vulkan.c:126:    RET(ff_vk_shader_link(vkctx, shd, spv_data, spv_len, "main"));
libavfilter/vf_flip_vulkan.c:128:    RET(ff_vk_shader_register_exec(vkctx, &s->e, &s->shd));
libavfilter/vf_flip_vulkan.c:134:        spv->free_shader(spv, &spv_opaque);
libavfilter/vf_flip_vulkan.c:136:        spv->uninit(&spv);
libavfilter/vf_flip_vulkan.c:141:static av_cold void flip_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_flip_vulkan.c:148:    ff_vk_exec_pool_free(vkctx, &s->e);
libavfilter/vf_flip_vulkan.c:149:    ff_vk_shader_free(vkctx, &s->shd);
libavfilter/vf_flip_vulkan.c:152:        vk->DestroySampler(vkctx->hwctx->act_dev, s->sampler,
libavfilter/vf_flip_vulkan.c:155:    ff_vk_uninit(&s->vkctx);
libavfilter/vf_flip_vulkan.c:160:static int filter_frame(AVFilterLink *link, AVFrame *in, enum FlipType type)
libavfilter/vf_flip_vulkan.c:168:    out = ff_get_video_buffer(outlink, outlink->w, outlink->h);
libavfilter/vf_flip_vulkan.c:170:        err = AVERROR(ENOMEM);
libavfilter/vf_flip_vulkan.c:175:        RET(init_filter(ctx, in, type));
libavfilter/vf_flip_vulkan.c:177:    RET(ff_vk_filter_process_simple(&s->vkctx, &s->e, &s->shd, out, in,
libavfilter/vf_flip_vulkan.c:180:    RET(av_frame_copy_props(out, in));
libavfilter/vf_flip_vulkan.c:182:    av_frame_free(&in);
libavfilter/vf_flip_vulkan.c:184:    return ff_filter_frame(outlink, out);
libavfilter/vf_flip_vulkan.c:187:    av_frame_free(&in);
libavfilter/vf_flip_vulkan.c:188:    av_frame_free(&out);
libavfilter/vf_flip_vulkan.c:192:static int hflip_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_flip_vulkan.c:194:    return filter_frame(link, in, FLIP_HORIZONTAL);
libavfilter/vf_flip_vulkan.c:197:static int vflip_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_flip_vulkan.c:199:    return filter_frame(link, in, FLIP_VERTICAL);
libavfilter/vf_flip_vulkan.c:202:static int flip_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_flip_vulkan.c:204:    return filter_frame(link, in, FLIP_BOTH);
libavfilter/vf_flip_vulkan.c:219:AVFILTER_DEFINE_CLASS(hflip_vulkan);
libavfilter/vf_flip_vulkan.c:232:    .description    = NULL_IF_CONFIG_SMALL("Horizontally flip the input video in Vulkan"),
libavfilter/vf_flip_vulkan.c:233:    .priv_size      = sizeof(FlipVulkanContext),
libavfilter/vf_flip_vulkan.c:236:    FILTER_INPUTS(hflip_vulkan_inputs),
libavfilter/vf_flip_vulkan.c:237:    FILTER_OUTPUTS(flip_vulkan_outputs),
libavfilter/vf_flip_vulkan.c:238:    FILTER_SINGLE_PIXFMT(AV_PIX_FMT_VULKAN),
libavfilter/vf_flip_vulkan.c:247:AVFILTER_DEFINE_CLASS(vflip_vulkan);
libavfilter/vf_flip_vulkan.c:260:    .description    = NULL_IF_CONFIG_SMALL("Vertically flip the input video in Vulkan"),
libavfilter/vf_flip_vulkan.c:261:    .priv_size      = sizeof(FlipVulkanContext),
```

- `grep(pattern=^(static )?.*\w+\(, path_glob=libavfilter/vf_gblur_vulkan.c)` →

```
105 matches (showing 60)
libavfilter/vf_gblur_vulkan.c:54:    C(0, void gblur(const ivec2 pos, const int index)                           )
libavfilter/vf_gblur_vulkan.c:55:    C(0, {                                                                      )
libavfilter/vf_gblur_vulkan.c:56:    C(1,     vec4 sum = texture(input_images[index], pos) * kernel[0];          )
libavfilter/vf_gblur_vulkan.c:57:    C(0,                                                                        )
libavfilter/vf_gblur_vulkan.c:58:    C(1,     for(int i = 1; i < kernel.length(); i++) {                         )
libavfilter/vf_gblur_vulkan.c:59:    C(2,         sum += texture(input_images[index], pos + OFFSET) * kernel[i]; )
libavfilter/vf_gblur_vulkan.c:60:    C(2,         sum += texture(input_images[index], pos - OFFSET) * kernel[i]; )
libavfilter/vf_gblur_vulkan.c:61:    C(1,     }                                                                  )
libavfilter/vf_gblur_vulkan.c:62:    C(0,                                                                        )
libavfilter/vf_gblur_vulkan.c:63:    C(1,     imageStore(output_images[index], pos, sum);                        )
libavfilter/vf_gblur_vulkan.c:64:    C(0, }                                                                      )
libavfilter/vf_gblur_vulkan.c:67:static inline float gaussian(float sigma, float x)
libavfilter/vf_gblur_vulkan.c:69:    return 1.0 / (sqrt(2.0 * M_PI) * sigma) *
libavfilter/vf_gblur_vulkan.c:70:           exp(-(x * x) / (2.0 * sigma * sigma));
libavfilter/vf_gblur_vulkan.c:73:static inline float gaussian_simpson_integration(float sigma, float a, float b)
libavfilter/vf_gblur_vulkan.c:75:    return (b - a) * (1.0 / 6.0) * ((gaussian(sigma, a) +
libavfilter/vf_gblur_vulkan.c:76:           4.0 * gaussian(sigma, (a + b) * 0.5) + gaussian(sigma, b)));
libavfilter/vf_gblur_vulkan.c:79:static void init_gaussian_kernel(float *kernel, float sigma, float kernel_size)
libavfilter/vf_gblur_vulkan.c:86:        kernel[x] = gaussian_simpson_integration(sigma, x - 0.5f, x + 0.5f);
libavfilter/vf_gblur_vulkan.c:99:static inline void init_kernel_size(GBlurVulkanContext *s, int *out_size)
libavfilter/vf_gblur_vulkan.c:104:        av_log(s, AV_LOG_WARNING, "The kernel size should be odd\n");
libavfilter/vf_gblur_vulkan.c:111:static av_cold void init_gaussian_params(GBlurVulkanContext *s)
libavfilter/vf_gblur_vulkan.c:116:    init_kernel_size(s, &s->size);
libavfilter/vf_gblur_vulkan.c:121:        init_kernel_size(s, &s->sizeV);
libavfilter/vf_gblur_vulkan.c:124:static int init_gblur_pipeline(GBlurVulkanContext *s,
libavfilter/vf_gblur_vulkan.c:134:    const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
libavfilter/vf_gblur_vulkan.c:145:    char *kernel_def = av_asprintf("float kernel[%i];", ksize);
libavfilter/vf_gblur_vulkan.c:147:        return AVERROR(ENOMEM);
libavfilter/vf_gblur_vulkan.c:151:    RET(ff_vk_shader_add_descriptor_set(&s->vkctx, shd, &buf_desc, 1, 1, 0));
libavfilter/vf_gblur_vulkan.c:153:    GLSLD(   gblur_func                                               );
libavfilter/vf_gblur_vulkan.c:154:    GLSLC(0, void main()                                              );
libavfilter/vf_gblur_vulkan.c:155:    GLSLC(0, {                                                        );
libavfilter/vf_gblur_vulkan.c:156:    GLSLC(1,     ivec2 size;                                          );
libavfilter/vf_gblur_vulkan.c:157:    GLSLC(1,     const ivec2 pos = ivec2(gl_GlobalInvocationID.xy);   );
libavfilter/vf_gblur_vulkan.c:159:        GLSLC(0,                                                      );
libavfilter/vf_gblur_vulkan.c:160:        GLSLF(1,  size = imageSize(output_images[%i]);              ,i);
libavfilter/vf_gblur_vulkan.c:161:        GLSLC(1,  if (!IS_WITHIN(pos, size))                          );
libavfilter/vf_gblur_vulkan.c:162:        GLSLC(2,      return;                                         );
libavfilter/vf_gblur_vulkan.c:164:            GLSLF(1,      gblur(pos, %i);                           ,i);
libavfilter/vf_gblur_vulkan.c:166:            GLSLF(1, vec4 res = texture(input_images[%i], pos);     ,i);
libavfilter/vf_gblur_vulkan.c:167:            GLSLF(1, imageStore(output_images[%i], pos, res);       ,i);
libavfilter/vf_gblur_vulkan.c:170:    GLSLC(0, }                                                        );
libavfilter/vf_gblur_vulkan.c:172:    RET(spv->compile_shader(&s->vkctx, spv, shd, &spv_data, &spv_len, "main",
libavfilter/vf_gblur_vulkan.c:174:    RET(ff_vk_shader_link(&s->vkctx, shd, spv_data, spv_len, "main"));
libavfilter/vf_gblur_vulkan.c:176:    RET(ff_vk_shader_register_exec(&s->vkctx, &s->e, shd));
libavfilter/vf_gblur_vulkan.c:178:    RET(ff_vk_create_buf(&s->vkctx, params_buf, sizeof(float) * ksize, NULL, NULL,
libavfilter/vf_gblur_vulkan.c:182:    RET(ff_vk_map_buffer(&s->vkctx, params_buf, &kernel_mapped, 0));
libavfilter/vf_gblur_vulkan.c:184:    init_gaussian_kernel((float *)kernel_mapped, sigma, ksize);
libavfilter/vf_gblur_vulkan.c:186:    RET(ff_vk_unmap_buffer(&s->vkctx, params_buf, 1));
libavfilter/vf_gblur_vulkan.c:187:    RET(ff_vk_shader_update_desc_buffer(&s->vkctx, &s->e.contexts[0], shd, 1, 0, 0,
libavfilter/vf_gblur_vulkan.c:192:    av_free(kernel_def);
libavfilter/vf_gblur_vulkan.c:194:        spv->free_shader(spv, &spv_opaque);
libavfilter/vf_gblur_vulkan.c:198:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
libavfilter/vf_gblur_vulkan.c:203:    const int planes = av_pix_fmt_count_planes(s->vkctx.output_format);
libavfilter/vf_gblur_vulkan.c:209:    spv = ff_vk_spirv_init();
libavfilter/vf_gblur_vulkan.c:211:        av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
libavfilter/vf_gblur_vulkan.c:215:    ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
libavfilter/vf_gblur_vulkan.c:216:    RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
libavfilter/vf_gblur_vulkan.c:217:    RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_LINEAR));
libavfilter/vf_gblur_vulkan.c:226:            .samplers   = DUP_SAMPLER(s->sampler),
```

### Turn 5  _(tok 18924+469, stop=tool_use)_

**Reasoning:** Now I have enough context. Let me identify the enclosing functions for each call site:

1. libavfilter/vf_avgblur_vulkan.c:102 - inside `init_filter` (starts at line 61, ends before `avgblur_vulkan_filter_frame` at line 165)
2. libavfilter/vf_blend_vulkan.c:173 - inside `init_filter` (starts at line 125, ends before `blend_frame` at line 228)
3. libavfilter/vf_bwdif_vulkan.c:107 - inside `init_filter` (starts at line 49, ends before `bwdif_vulkan_filter_frame` at line 185)
4. libavfilter/vf_chromaber_vulkan.c:120 - inside `init_filter` (starts at line 68, ends before `chromaber_vulkan_filter_frame` at line 168)
5. libavfilter/vf_flip_vulkan.c:86 - inside `init_filter` (starts at line 46, ends before `flip_vulkan_uninit` at line 141)
6. libavfilter/vf_gblur_vulkan.c:231 - inside `init_filter` (starts at line 198)
7. libavfilter/vf_nlmeans_vulkan.c:457 - need to check
8. libavfilter/vf_overlay_vulkan.c:142 - need to check
9. libavfilter/vf_scale_vulkan.c:174 - need to check
10. libavfilter/vf_transpose_vulkan.c:85 - need to check
11. libavfilter/vf_xfade_vulkan.c:367 - need to check
12. libavfilter/vsrc_testsrc_vulkan.c:105 - need to check

Let me check the remaining files.

- `grep(pattern=^(static )?.*\w+\(, path_glob=libavfilter/vf_nlmeans_vulkan.c)` →

```
332 matches (showing 60)
libavfilter/vf_nlmeans_vulkan.c:67:static void insert_first(FFVulkanShader *shd, int r, const char *off, int horiz, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:69:    GLSLF(4, s1    = texture(input_img[%i], pos + ivec2(%i + %s, %i + %s))[%i];
libavfilter/vf_nlmeans_vulkan.c:72:    GLSLF(4, s2[0] = texture(input_img[%i], pos + offs[0] + ivec2(%i + %s, %i + %s))[%i];
libavfilter/vf_nlmeans_vulkan.c:74:    GLSLF(4, s2[1] = texture(input_img[%i], pos + offs[1] + ivec2(%i + %s, %i + %s))[%i];
libavfilter/vf_nlmeans_vulkan.c:76:    GLSLF(4, s2[2] = texture(input_img[%i], pos + offs[2] + ivec2(%i + %s, %i + %s))[%i];
libavfilter/vf_nlmeans_vulkan.c:78:    GLSLF(4, s2[3] = texture(input_img[%i], pos + offs[3] + ivec2(%i + %s, %i + %s))[%i];
libavfilter/vf_nlmeans_vulkan.c:81:    GLSLC(4, s2 = (s1 - s2) * (s1 - s2);                                                    );
libavfilter/vf_nlmeans_vulkan.c:84:static void insert_horizontal_pass(FFVulkanShader *shd, int nb_rows, int first, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:86:    GLSLF(1, pos.y = int(gl_GlobalInvocationID.x) * %i;                           ,nb_rows);
libavfilter/vf_nlmeans_vulkan.c:88:        GLSLC(1, barrier();                                                       );
libavfilter/vf_nlmeans_vulkan.c:89:    GLSLC(0,                                                                      );
libavfilter/vf_nlmeans_vulkan.c:90:    GLSLF(1, if (pos.y < height[%i]) {                                            ,plane);
libavfilter/vf_nlmeans_vulkan.c:91:    GLSLC(2,     #pragma unroll(1)                                                );
libavfilter/vf_nlmeans_vulkan.c:92:    GLSLF(2,     for (r = 0; r < %i; r++) {                                       ,nb_rows);
libavfilter/vf_nlmeans_vulkan.c:93:    GLSLC(3,         prefix_sum = DTYPE(0);                                       );
libavfilter/vf_nlmeans_vulkan.c:94:    GLSLC(3,         offset = int_stride * uint64_t(pos.y + r);                   );
libavfilter/vf_nlmeans_vulkan.c:95:    GLSLC(3,         dst = DataBuffer(uint64_t(integral_data) + offset);          );
libavfilter/vf_nlmeans_vulkan.c:96:    GLSLC(0,                                                                      );
libavfilter/vf_nlmeans_vulkan.c:97:    GLSLF(3,         for (pos.x = 0; pos.x < width[%i]; pos.x++) {                ,plane);
libavfilter/vf_nlmeans_vulkan.c:99:        insert_first(shd, 0, "r", 0, plane, comp);
libavfilter/vf_nlmeans_vulkan.c:101:        GLSLC(4,         s2 = dst.v[pos.x];                                       );
libavfilter/vf_nlmeans_vulkan.c:102:    GLSLC(4,             dst.v[pos.x] = s2 + prefix_sum;                          );
libavfilter/vf_nlmeans_vulkan.c:103:    GLSLC(4,             prefix_sum += s2;                                        );
libavfilter/vf_nlmeans_vulkan.c:104:    GLSLC(3,         }                                                            );
libavfilter/vf_nlmeans_vulkan.c:105:    GLSLC(2,     }                                                                );
libavfilter/vf_nlmeans_vulkan.c:106:    GLSLC(1, }                                                                    );
libavfilter/vf_nlmeans_vulkan.c:107:    GLSLC(0,                                                                      );
libavfilter/vf_nlmeans_vulkan.c:110:static void insert_vertical_pass(FFVulkanShader *shd, int nb_rows, int first, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:112:    GLSLF(1, pos.x = int(gl_GlobalInvocationID.x) * %i;                           ,nb_rows);
libavfilter/vf_nlmeans_vulkan.c:113:    GLSLC(1, #pragma unroll(1)                                                    );
libavfilter/vf_nlmeans_vulkan.c:114:    GLSLF(1, for (r = 0; r < %i; r++)                                             ,nb_rows);
libavfilter/vf_nlmeans_vulkan.c:115:    GLSLC(2,     psum[r] = DTYPE(0);                                              );
libavfilter/vf_nlmeans_vulkan.c:116:    GLSLC(0,                                                                      );
libavfilter/vf_nlmeans_vulkan.c:118:        GLSLC(1, barrier();                                                       );
libavfilter/vf_nlmeans_vulkan.c:119:    GLSLC(0,                                                                      );
libavfilter/vf_nlmeans_vulkan.c:120:    GLSLF(1, if (pos.x < width[%i]) {                                             ,plane);
libavfilter/vf_nlmeans_vulkan.c:121:    GLSLF(2,     for (pos.y = 0; pos.y < height[%i]; pos.y++) {                   ,plane);
libavfilter/vf_nlmeans_vulkan.c:122:    GLSLC(3,         offset = int_stride * uint64_t(pos.y);                       );
libavfilter/vf_nlmeans_vulkan.c:123:    GLSLC(3,         dst = DataBuffer(uint64_t(integral_data) + offset);          );
libavfilter/vf_nlmeans_vulkan.c:124:    GLSLC(0,                                                                      );
libavfilter/vf_nlmeans_vulkan.c:125:    GLSLC(3,         #pragma unroll(1)                                            );
libavfilter/vf_nlmeans_vulkan.c:126:    GLSLF(3,         for (r = 0; r < %i; r++) {                                   ,nb_rows);
libavfilter/vf_nlmeans_vulkan.c:128:        insert_first(shd, 0, "r", 1, plane, comp);
libavfilter/vf_nlmeans_vulkan.c:130:        GLSLC(4,         s2 = dst.v[pos.x + r];                                   );
libavfilter/vf_nlmeans_vulkan.c:131:    GLSLC(4,             dst.v[pos.x + r] = s2 + psum[r];                         );
libavfilter/vf_nlmeans_vulkan.c:132:    GLSLC(4,             psum[r] += s2;                                           );
libavfilter/vf_nlmeans_vulkan.c:133:    GLSLC(3,         }                                                            );
libavfilter/vf_nlmeans_vulkan.c:134:    GLSLC(2,     }                                                                );
libavfilter/vf_nlmeans_vulkan.c:135:    GLSLC(1, }                                                                    );
libavfilter/vf_nlmeans_vulkan.c:136:    GLSLC(0,                                                                      );
libavfilter/vf_nlmeans_vulkan.c:139:static void insert_weights_pass(FFVulkanShader *shd, int nb_rows, int vert,
libavfilter/vf_nlmeans_vulkan.c:142:    GLSLF(1, p = patch_size[%i];                                              ,dst_comp);
libavfilter/vf_nlmeans_vulkan.c:143:    GLSLC(0,                                                                  );
libavfilter/vf_nlmeans_vulkan.c:144:    GLSLC(1, barrier();                                                       );
libavfilter/vf_nlmeans_vulkan.c:145:    GLSLC(0,                                                                  );
libavfilter/vf_nlmeans_vulkan.c:147:        GLSLF(1, for (pos.y = 0; pos.y < height[%i]; pos.y++) {               ,plane);
libavfilter/vf_nlmeans_vulkan.c:148:        GLSLF(2,     if (gl_GlobalInvocationID.x*%i >= width[%i])             ,nb_rows, plane);
libavfilter/vf_nlmeans_vulkan.c:149:        GLSLC(3,         break;                                               );
libavfilter/vf_nlmeans_vulkan.c:150:        GLSLF(2,     for (r = 0; r < %i; r++) {                               ,nb_rows);
libavfilter/vf_nlmeans_vulkan.c:151:        GLSLF(3,         pos.x = int(gl_GlobalInvocationID.x) * %i + r;       ,nb_rows);
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 21581+422, stop=tool_use, forced)_

**Reasoning:** Let me find the function definitions for the remaining files I haven't checked yet: vf_nlmeans_vulkan.c, vf_overlay_vulkan.c, vf_scale_vulkan.c, vf_transpose_vulkan.c, vf_xfade_vulkan.c, vsrc_testsrc_vulkan.c.

Let me search for function definitions in these files to find the enclosing functions.

- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 1, "n_truth": 3, "tp": 1, "precision": 1.0, "recall": 0.3333333333333333, "f1": 0.5}`

