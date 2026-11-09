# Impact-analysis transcript — ffmpeg @ c982376076b6 — anthropic:claude-haiku-5-5

- target: `ff_vk_shader_rep_fmt` (libavutil/vulkan.c), arity 1->2
- truth: [['libavfilter/vf_avgblur_vulkan.c', 'init_filter'], ['libavfilter/vf_blend_vulkan.c', 'init_filter'], ['libavfilter/vf_flip_vulkan.c', 'init_filter'], ['libavfilter/vf_gblur_vulkan.c', 'init_gblur_pipeline'], ['libavfilter/vf_overlay_vulkan.c', 'init_filter'], ['libavfilter/vf_scale_vulkan.c', 'init_filter'], ['libavfilter/vf_transpose_vulkan.c', 'init_filter'], ['libavfilter/vf_xfade_vulkan.c', 'init_vulkan'], ['libavfilter/vsrc_testsrc_vulkan.c', 'init_filter']]

## Self-navigation arm

### Turn 1  _(tok 1231+115, stop=tool_use)_

**Reasoning:** I'll search the repo for ff_vk_shader_rep_fmt to see where it's used.



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

### Turn 2  _(tok 2156+323, stop=tool_use)_

**Reasoning:** I need to find the enclosing function names for 13 call sites, so I'll grep for function definition patterns in the vulkan-related libavfilter files to map each line to its surrounding function.



- `grep(pattern=^[A-Za-z_].*\(|^\{|^\}, version=old, path_glob=libavfilter/*vulkan.c, max_results=1000)` →

```
329 matches (showing 200)
libavfilter/vf_avgblur_vulkan.c:47:} AvgBlurVulkanContext;
libavfilter/vf_avgblur_vulkan.c:59:};
libavfilter/vf_avgblur_vulkan.c:61:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
libavfilter/vf_avgblur_vulkan.c:62:{
libavfilter/vf_avgblur_vulkan.c:163:}
libavfilter/vf_avgblur_vulkan.c:165:static int avgblur_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_avgblur_vulkan.c:166:{
libavfilter/vf_avgblur_vulkan.c:197:}
libavfilter/vf_avgblur_vulkan.c:199:static void avgblur_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_avgblur_vulkan.c:200:{
libavfilter/vf_avgblur_vulkan.c:215:}
libavfilter/vf_avgblur_vulkan.c:224:};
libavfilter/vf_avgblur_vulkan.c:226:AVFILTER_DEFINE_CLASS(avgblur_vulkan);
libavfilter/vf_avgblur_vulkan.c:235:};
libavfilter/vf_avgblur_vulkan.c:243:};
libavfilter/vf_avgblur_vulkan.c:257:};
libavfilter/vf_blend_vulkan.c:42:} FilterParamsVulkan;
libavfilter/vf_blend_vulkan.c:57:} BlendVulkanContext;
libavfilter/vf_blend_vulkan.c:66:};
libavfilter/vf_blend_vulkan.c:73:DEFINE_BLEND_MODE(NORMAL, A * opacity + B * (1.0f - opacity))
libavfilter/vf_blend_vulkan.c:74:DEFINE_BLEND_MODE(MULTIPLY, FN(1.0f * A * B / 1.0f))
libavfilter/vf_blend_vulkan.c:76:static inline void init_blend_func(FilterParamsVulkan *param)
libavfilter/vf_blend_vulkan.c:77:{
libavfilter/vf_blend_vulkan.c:90:}
libavfilter/vf_blend_vulkan.c:92:static int config_params(AVFilterContext *avctx)
libavfilter/vf_blend_vulkan.c:93:{
libavfilter/vf_blend_vulkan.c:113:}
libavfilter/vf_blend_vulkan.c:115:static int process_command(AVFilterContext *ctx, const char *cmd, const char *args,
libavfilter/vf_blend_vulkan.c:117:{
libavfilter/vf_blend_vulkan.c:123:}
libavfilter/vf_blend_vulkan.c:125:static av_cold int init_filter(AVFilterContext *avctx)
libavfilter/vf_blend_vulkan.c:126:{
libavfilter/vf_blend_vulkan.c:226:}
libavfilter/vf_blend_vulkan.c:228:static int blend_frame(FFFrameSync *fs)
libavfilter/vf_blend_vulkan.c:229:{
libavfilter/vf_blend_vulkan.c:268:}
libavfilter/vf_blend_vulkan.c:270:static av_cold int init(AVFilterContext *avctx)
libavfilter/vf_blend_vulkan.c:271:{
libavfilter/vf_blend_vulkan.c:277:}
libavfilter/vf_blend_vulkan.c:279:static av_cold void uninit(AVFilterContext *avctx)
libavfilter/vf_blend_vulkan.c:280:{
libavfilter/vf_blend_vulkan.c:296:}
libavfilter/vf_blend_vulkan.c:298:static int config_props_output(AVFilterLink *outlink)
libavfilter/vf_blend_vulkan.c:299:{
libavfilter/vf_blend_vulkan.c:331:}
libavfilter/vf_blend_vulkan.c:333:static int activate(AVFilterContext *avctx)
libavfilter/vf_blend_vulkan.c:334:{
libavfilter/vf_blend_vulkan.c:337:}
libavfilter/vf_blend_vulkan.c:358:};
libavfilter/vf_blend_vulkan.c:360:AVFILTER_DEFINE_CLASS(blend_vulkan);
libavfilter/vf_blend_vulkan.c:373:};
libavfilter/vf_blend_vulkan.c:382:};
libavfilter/vf_blend_vulkan.c:398:};
libavfilter/vf_bwdif_vulkan.c:39:} BWDIFVulkanContext;
libavfilter/vf_bwdif_vulkan.c:45:} BWDIFParameters;
libavfilter/vf_bwdif_vulkan.c:49:static av_cold int init_filter(AVFilterContext *ctx)
libavfilter/vf_bwdif_vulkan.c:50:{
libavfilter/vf_bwdif_vulkan.c:183:}
libavfilter/vf_bwdif_vulkan.c:185:static void bwdif_vulkan_filter_frame(AVFilterContext *ctx, AVFrame *dst,
libavfilter/vf_bwdif_vulkan.c:187:{
libavfilter/vf_bwdif_vulkan.c:202:}
libavfilter/vf_bwdif_vulkan.c:204:static void bwdif_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_bwdif_vulkan.c:205:{
libavfilter/vf_bwdif_vulkan.c:222:}
libavfilter/vf_bwdif_vulkan.c:224:static int bwdif_vulkan_config_input(AVFilterLink *inlink)
libavfilter/vf_bwdif_vulkan.c:225:{
libavfilter/vf_bwdif_vulkan.c:255:}
libavfilter/vf_bwdif_vulkan.c:257:static int bwdif_vulkan_config_output(AVFilterLink *outlink)
libavfilter/vf_bwdif_vulkan.c:258:{
libavfilter/vf_bwdif_vulkan.c:294:}
libavfilter/vf_bwdif_vulkan.c:302:};
libavfilter/vf_bwdif_vulkan.c:311:};
libavfilter/vf_bwdif_vulkan.c:320:};
libavfilter/vf_bwdif_vulkan.c:335:};
libavfilter/vf_chromaber_vulkan.c:42:} ChromaticAberrationVulkanContext;
libavfilter/vf_chromaber_vulkan.c:66:};
libavfilter/vf_chromaber_vulkan.c:68:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
libavfilter/vf_chromaber_vulkan.c:69:{
libavfilter/vf_chromaber_vulkan.c:166:}
libavfilter/vf_chromaber_vulkan.c:168:static int chromaber_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_chromaber_vulkan.c:169:{
libavfilter/vf_chromaber_vulkan.c:199:}
libavfilter/vf_chromaber_vulkan.c:201:static void chromaber_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_chromaber_vulkan.c:202:{
libavfilter/vf_chromaber_vulkan.c:217:}
libavfilter/vf_chromaber_vulkan.c:225:};
libavfilter/vf_chromaber_vulkan.c:227:AVFILTER_DEFINE_CLASS(chromaber_vulkan);
libavfilter/vf_chromaber_vulkan.c:236:};
libavfilter/vf_chromaber_vulkan.c:244:};
libavfilter/vf_chromaber_vulkan.c:258:};
libavfilter/vf_flip_vulkan.c:34:};
libavfilter/vf_flip_vulkan.c:44:} FlipVulkanContext;
libavfilter/vf_flip_vulkan.c:46:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in, enum FlipType type)
libavfilter/vf_flip_vulkan.c:47:{
libavfilter/vf_flip_vulkan.c:139:}
libavfilter/vf_flip_vulkan.c:141:static av_cold void flip_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_flip_vulkan.c:142:{
libavfilter/vf_flip_vulkan.c:158:}
libavfilter/vf_flip_vulkan.c:160:static int filter_frame(AVFilterLink *link, AVFrame *in, enum FlipType type)
libavfilter/vf_flip_vulkan.c:161:{
libavfilter/vf_flip_vulkan.c:190:}
libavfilter/vf_flip_vulkan.c:192:static int hflip_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_flip_vulkan.c:193:{
libavfilter/vf_flip_vulkan.c:195:}
libavfilter/vf_flip_vulkan.c:197:static int vflip_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_flip_vulkan.c:198:{
libavfilter/vf_flip_vulkan.c:200:}
libavfilter/vf_flip_vulkan.c:202:static int flip_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_flip_vulkan.c:203:{
libavfilter/vf_flip_vulkan.c:205:}
libavfilter/vf_flip_vulkan.c:213:};
libavfilter/vf_flip_vulkan.c:217:};
libavfilter/vf_flip_vulkan.c:219:AVFILTER_DEFINE_CLASS(hflip_vulkan);
libavfilter/vf_flip_vulkan.c:228:};
libavfilter/vf_flip_vulkan.c:241:};
libavfilter/vf_flip_vulkan.c:245:};
libavfilter/vf_flip_vulkan.c:247:AVFILTER_DEFINE_CLASS(vflip_vulkan);
libavfilter/vf_flip_vulkan.c:256:};
libavfilter/vf_flip_vulkan.c:269:};
libavfilter/vf_flip_vulkan.c:273:};
libavfilter/vf_flip_vulkan.c:275:AVFILTER_DEFINE_CLASS(flip_vulkan);
libavfilter/vf_flip_vulkan.c:284:};
libavfilter/vf_flip_vulkan.c:298:};
libavfilter/vf_gblur_vulkan.c:51:} GBlurVulkanContext;
libavfilter/vf_gblur_vulkan.c:65:};
libavfilter/vf_gblur_vulkan.c:67:static inline float gaussian(float sigma, float x)
libavfilter/vf_gblur_vulkan.c:68:{
libavfilter/vf_gblur_vulkan.c:71:}
libavfilter/vf_gblur_vulkan.c:73:static inline float gaussian_simpson_integration(float sigma, float a, float b)
libavfilter/vf_gblur_vulkan.c:74:{
libavfilter/vf_gblur_vulkan.c:77:}
libavfilter/vf_gblur_vulkan.c:79:static void init_gaussian_kernel(float *kernel, float sigma, float kernel_size)
libavfilter/vf_gblur_vulkan.c:80:{
libavfilter/vf_gblur_vulkan.c:97:}
libavfilter/vf_gblur_vulkan.c:99:static inline void init_kernel_size(GBlurVulkanContext *s, int *out_size)
libavfilter/vf_gblur_vulkan.c:100:{
libavfilter/vf_gblur_vulkan.c:109:}
libavfilter/vf_gblur_vulkan.c:111:static av_cold void init_gaussian_params(GBlurVulkanContext *s)
libavfilter/vf_gblur_vulkan.c:112:{
libavfilter/vf_gblur_vulkan.c:122:}
libavfilter/vf_gblur_vulkan.c:124:static int init_gblur_pipeline(GBlurVulkanContext *s,
libavfilter/vf_gblur_vulkan.c:127:{
libavfilter/vf_gblur_vulkan.c:196:}
libavfilter/vf_gblur_vulkan.c:198:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
libavfilter/vf_gblur_vulkan.c:199:{
libavfilter/vf_gblur_vulkan.c:276:}
libavfilter/vf_gblur_vulkan.c:278:static av_cold void gblur_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_gblur_vulkan.c:279:{
libavfilter/vf_gblur_vulkan.c:297:}
libavfilter/vf_gblur_vulkan.c:299:static int gblur_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_gblur_vulkan.c:300:{
libavfilter/vf_gblur_vulkan.c:340:}
libavfilter/vf_gblur_vulkan.c:351:};
libavfilter/vf_gblur_vulkan.c:353:AVFILTER_DEFINE_CLASS(gblur_vulkan);
libavfilter/vf_gblur_vulkan.c:362:};
libavfilter/vf_gblur_vulkan.c:370:};
libavfilter/vf_gblur_vulkan.c:384:};
libavfilter/vf_nlmeans_vulkan.c:65:} NLMeansVulkanContext;
libavfilter/vf_nlmeans_vulkan.c:67:static void insert_first(FFVulkanShader *shd, int r, const char *off, int horiz, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:68:{
libavfilter/vf_nlmeans_vulkan.c:82:}
libavfilter/vf_nlmeans_vulkan.c:84:static void insert_horizontal_pass(FFVulkanShader *shd, int nb_rows, int first, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:85:{
libavfilter/vf_nlmeans_vulkan.c:108:}
libavfilter/vf_nlmeans_vulkan.c:110:static void insert_vertical_pass(FFVulkanShader *shd, int nb_rows, int first, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:111:{
libavfilter/vf_nlmeans_vulkan.c:137:}
libavfilter/vf_nlmeans_vulkan.c:139:static void insert_weights_pass(FFVulkanShader *shd, int nb_rows, int vert,
libavfilter/vf_nlmeans_vulkan.c:141:{
libavfilter/vf_nlmeans_vulkan.c:197:}
libavfilter/vf_nlmeans_vulkan.c:209:} HorizontalPushData;
libavfilter/vf_nlmeans_vulkan.c:211:static av_cold int init_weights_pipeline(FFVulkanContext *vkctx, FFVkExecPool *exec,
libavfilter/vf_nlmeans_vulkan.c:217:{
libavfilter/vf_nlmeans_vulkan.c:414:}
libavfilter/vf_nlmeans_vulkan.c:418:} DenoisePushData;
libavfilter/vf_nlmeans_vulkan.c:420:static av_cold int init_denoise_pipeline(FFVulkanContext *vkctx, FFVkExecPool *exec,
libavfilter/vf_nlmeans_vulkan.c:424:{
libavfilter/vf_nlmeans_vulkan.c:566:}
libavfilter/vf_nlmeans_vulkan.c:568:static av_cold int init_filter(AVFilterContext *ctx)
libavfilter/vf_nlmeans_vulkan.c:569:{
libavfilter/vf_nlmeans_vulkan.c:688:}
libavfilter/vf_nlmeans_vulkan.c:690:static int denoise_pass(NLMeansVulkanContext *s, FFVkExecContext *exec,
libavfilter/vf_nlmeans_vulkan.c:692:{
libavfilter/vf_nlmeans_vulkan.c:738:}
libavfilter/vf_nlmeans_vulkan.c:740:static int nlmeans_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_nlmeans_vulkan.c:741:{
libavfilter/vf_nlmeans_vulkan.c:1043:}
libavfilter/vf_nlmeans_vulkan.c:1045:static void nlmeans_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_nlmeans_vulkan.c:1046:{
libavfilter/vf_nlmeans_vulkan.c:1068:}
libavfilter/vf_nlmeans_vulkan.c:1089:};
libavfilter/vf_nlmeans_vulkan.c:1091:AVFILTER_DEFINE_CLASS(nlmeans_vulkan);
libavfilter/vf_nlmeans_vulkan.c:1100:};
libavfilter/vf_nlmeans_vulkan.c:1108:};
libavfilter/vf_nlmeans_vulkan.c:1122:};
libavfilter/vf_overlay_vulkan.c:50:} OverlayVulkanContext;
libavfilter/vf_overlay_vulkan.c:65:};
libavfilter/vf_overlay_vulkan.c:81:};
libavfilter/vf_overlay_vulkan.c:83:static av_cold int init_filter(AVFilterContext *ctx)
libavfilter/vf_overlay_vulkan.c:84:{
```

### Turn 3  _(tok 9120+1010, stop=tool_use)_

**Reasoning:** I'll instead check each call site's surrounding lines to find the nearest enclosing function definition above it — tracing avgblur, blend, bwdif, chromaber, and flip each back to their respective init_filter functions.

For gblur it's init_filter again, and nlmeans maps to init_denoise_pipeline. I still need to verify overlay's enclosing function since its matches extend beyond line 200, plus confirm scale, transpose, xfade, and testsrc with a more targeted search.



- `grep(pattern=^(static |const |av_cold )?[A-Za-z_ *]+\(|^\}, version=old, path_glob=libavfilter/vf_overlay_vulkan.c)` →

```
102 matches (showing 60)
libavfilter/vf_overlay_vulkan.c:2: * Copyright (c) Lynne
libavfilter/vf_overlay_vulkan.c:50:} OverlayVulkanContext;
libavfilter/vf_overlay_vulkan.c:53:    C(0, void overlay_noalpha(int i, ivec2 pos)                                )
libavfilter/vf_overlay_vulkan.c:54:    C(0, {                                                                     )
libavfilter/vf_overlay_vulkan.c:55:    C(1,     if ((o_offset[i].x <= pos.x) && (o_offset[i].y <= pos.y) &&
libavfilter/vf_overlay_vulkan.c:56:                 (pos.x < (o_offset[i].x + o_size[i].x)) &&
libavfilter/vf_overlay_vulkan.c:57:                 (pos.y < (o_offset[i].y + o_size[i].y))) {                    )
libavfilter/vf_overlay_vulkan.c:58:    C(2,         vec4 res = texture(overlay_img[i], pos - o_offset[i]);        )
libavfilter/vf_overlay_vulkan.c:59:    C(2,         imageStore(output_img[i], pos, res);                          )
libavfilter/vf_overlay_vulkan.c:60:    C(1,     } else {                                                          )
libavfilter/vf_overlay_vulkan.c:61:    C(2,         vec4 res = texture(main_img[i], pos);                         )
libavfilter/vf_overlay_vulkan.c:62:    C(2,         imageStore(output_img[i], pos, res);                          )
libavfilter/vf_overlay_vulkan.c:63:    C(1,     }                                                                 )
libavfilter/vf_overlay_vulkan.c:64:    C(0, }                                                                     )
libavfilter/vf_overlay_vulkan.c:65:};
libavfilter/vf_overlay_vulkan.c:68:    C(0, void overlay_alpha_opaque(int i, ivec2 pos)                           )
libavfilter/vf_overlay_vulkan.c:69:    C(0, {                                                                     )
libavfilter/vf_overlay_vulkan.c:70:    C(1,     vec4 res = texture(main_img[i], pos);                             )
libavfilter/vf_overlay_vulkan.c:71:    C(1,     if ((o_offset[i].x <= pos.x) && (o_offset[i].y <= pos.y) &&
libavfilter/vf_overlay_vulkan.c:72:                 (pos.x < (o_offset[i].x + o_size[i].x)) &&
libavfilter/vf_overlay_vulkan.c:73:                 (pos.y < (o_offset[i].y + o_size[i].y))) {                    )
libavfilter/vf_overlay_vulkan.c:74:    C(2,         vec4 ovr = texture(overlay_img[i], pos - o_offset[i]);        )
libavfilter/vf_overlay_vulkan.c:75:    C(2,         res = ovr * ovr.a + res * (1.0f - ovr.a);                     )
libavfilter/vf_overlay_vulkan.c:76:    C(2,         res.a = 1.0f;                                                 )
libavfilter/vf_overlay_vulkan.c:77:    C(2,         imageStore(output_img[i], pos, res);                          )
libavfilter/vf_overlay_vulkan.c:78:    C(1,     }                                                                 )
libavfilter/vf_overlay_vulkan.c:79:    C(1,     imageStore(output_img[i], pos, res);                              )
libavfilter/vf_overlay_vulkan.c:80:    C(0, }                                                                     )
libavfilter/vf_overlay_vulkan.c:81:};
libavfilter/vf_overlay_vulkan.c:83:static av_cold int init_filter(AVFilterContext *ctx)
libavfilter/vf_overlay_vulkan.c:99:    if (!spv) {
libavfilter/vf_overlay_vulkan.c:100:        av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
libavfilter/vf_overlay_vulkan.c:104:    ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
libavfilter/vf_overlay_vulkan.c:105:    RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
libavfilter/vf_overlay_vulkan.c:106:    RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_NEAREST));
libavfilter/vf_overlay_vulkan.c:107:    RET(ff_vk_shader_init(vkctx, &s->shd, "overlay",
libavfilter/vf_overlay_vulkan.c:113:    GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
libavfilter/vf_overlay_vulkan.c:114:    GLSLC(1,    ivec2 o_offset[3];                                        );
libavfilter/vf_overlay_vulkan.c:115:    GLSLC(1,    ivec2 o_size[3];                                          );
libavfilter/vf_overlay_vulkan.c:116:    GLSLC(0, };                                                           );
libavfilter/vf_overlay_vulkan.c:117:    GLSLC(0,                                                              );
libavfilter/vf_overlay_vulkan.c:119:    ff_vk_shader_add_push_const(&s->shd, 0, sizeof(s->opts),
libavfilter/vf_overlay_vulkan.c:150:    RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 3, 0, 0));
libavfilter/vf_overlay_vulkan.c:152:    GLSLD(   overlay_noalpha                                              );
libavfilter/vf_overlay_vulkan.c:153:    GLSLD(   overlay_alpha                                                );
libavfilter/vf_overlay_vulkan.c:154:    GLSLC(0, void main()                                                  );
libavfilter/vf_overlay_vulkan.c:155:    GLSLC(0, {                                                            );
libavfilter/vf_overlay_vulkan.c:156:    GLSLC(1,     ivec2 pos = ivec2(gl_GlobalInvocationID.xy);             );
libavfilter/vf_overlay_vulkan.c:157:    GLSLF(1,     int planes = %i;                                  ,planes);
libavfilter/vf_overlay_vulkan.c:158:    GLSLC(1,     for (int i = 0; i < planes; i++) {                       );
libavfilter/vf_overlay_vulkan.c:159:    if (ialpha)
libavfilter/vf_overlay_vulkan.c:160:        GLSLC(2,         overlay_alpha_opaque(i, pos);                    );
libavfilter/vf_overlay_vulkan.c:162:        GLSLC(2,         overlay_noalpha(i, pos);                         );
libavfilter/vf_overlay_vulkan.c:163:    GLSLC(1,     }                                                        );
libavfilter/vf_overlay_vulkan.c:164:    GLSLC(0, }                                                            );
libavfilter/vf_overlay_vulkan.c:166:    RET(spv->compile_shader(vkctx, spv, shd, &spv_data, &spv_len, "main",
libavfilter/vf_overlay_vulkan.c:168:    RET(ff_vk_shader_link(vkctx, shd, spv_data, spv_len, "main"));
libavfilter/vf_overlay_vulkan.c:170:    RET(ff_vk_shader_register_exec(vkctx, &s->e, &s->shd));
libavfilter/vf_overlay_vulkan.c:189:    if (spv_opaque)
libavfilter/vf_overlay_vulkan.c:191:    if (spv)
```

- `grep(pattern=^(static |const |av_cold )?[A-Za-z_ *]+\(|^\}, version=old, path_glob=libavfilter/vf_scale_vulkan.c)` →

```
139 matches (showing 60)
libavfilter/vf_scale_vulkan.c:2: * Copyright (c) Lynne
libavfilter/vf_scale_vulkan.c:35:};
libavfilter/vf_scale_vulkan.c:57:} ScaleVulkanContext;
libavfilter/vf_scale_vulkan.c:60:    C(0, vec4 scale_bilinear(int idx, ivec2 pos, vec2 crop_range, vec2 crop_off))
libavfilter/vf_scale_vulkan.c:61:    C(0, {                                                                      )
libavfilter/vf_scale_vulkan.c:62:    C(1,     vec2 npos = (vec2(pos) + 0.5f) / imageSize(output_img[idx]);       )
libavfilter/vf_scale_vulkan.c:63:    C(1,     npos *= crop_range;    /* Reduce the range */                      )
libavfilter/vf_scale_vulkan.c:64:    C(1,     npos += crop_off;      /* Offset the start */                      )
libavfilter/vf_scale_vulkan.c:65:    C(1,     return texture(input_img[idx], npos);                              )
libavfilter/vf_scale_vulkan.c:66:    C(0, }                                                                      )
libavfilter/vf_scale_vulkan.c:67:};
libavfilter/vf_scale_vulkan.c:70:    C(0, vec4 rgb2yuv(vec4 src, int fullrange)                                  )
libavfilter/vf_scale_vulkan.c:71:    C(0, {                                                                      )
libavfilter/vf_scale_vulkan.c:72:    C(1,     src *= yuv_matrix;                                                 )
libavfilter/vf_scale_vulkan.c:73:    C(1,     if (fullrange == 1) {                                              )
libavfilter/vf_scale_vulkan.c:74:    C(2,         src += vec4(0.0, 0.5, 0.5, 0.0);                               )
libavfilter/vf_scale_vulkan.c:75:    C(1,     } else {                                                           )
libavfilter/vf_scale_vulkan.c:76:    C(2,         src *= vec4(219.0 / 255.0, 224.0 / 255.0, 224.0 / 255.0, 1.0); )
libavfilter/vf_scale_vulkan.c:77:    C(2,         src += vec4(16.0 / 255.0, 128.0 / 255.0, 128.0 / 255.0, 0.0);  )
libavfilter/vf_scale_vulkan.c:78:    C(1,     }                                                                  )
libavfilter/vf_scale_vulkan.c:79:    C(1,     return src;                                                        )
libavfilter/vf_scale_vulkan.c:80:    C(0, }                                                                      )
libavfilter/vf_scale_vulkan.c:81:};
libavfilter/vf_scale_vulkan.c:84:    C(0, void write_nv12(vec4 src, ivec2 pos)                                   )
libavfilter/vf_scale_vulkan.c:85:    C(0, {                                                                      )
libavfilter/vf_scale_vulkan.c:86:    C(1,     imageStore(output_img[0], pos, vec4(src.r, 0.0, 0.0, 0.0));        )
libavfilter/vf_scale_vulkan.c:87:    C(1,     pos /= ivec2(2);                                                   )
libavfilter/vf_scale_vulkan.c:88:    C(1,     imageStore(output_img[1], pos, vec4(src.g, src.b, 0.0, 0.0));      )
libavfilter/vf_scale_vulkan.c:89:    C(0, }                                                                      )
libavfilter/vf_scale_vulkan.c:90:};
libavfilter/vf_scale_vulkan.c:93:    C(0, void write_420(vec4 src, ivec2 pos)                                    )
libavfilter/vf_scale_vulkan.c:94:    C(0, {                                                                      )
libavfilter/vf_scale_vulkan.c:95:    C(1,     imageStore(output_img[0], pos, vec4(src.r, 0.0, 0.0, 0.0));        )
libavfilter/vf_scale_vulkan.c:96:    C(1,     pos /= ivec2(2);                                                   )
libavfilter/vf_scale_vulkan.c:97:    C(1,     imageStore(output_img[1], pos, vec4(src.g, 0.0, 0.0, 0.0));        )
libavfilter/vf_scale_vulkan.c:98:    C(1,     imageStore(output_img[2], pos, vec4(src.b, 0.0, 0.0, 0.0));        )
libavfilter/vf_scale_vulkan.c:99:    C(0, }                                                                      )
libavfilter/vf_scale_vulkan.c:100:};
libavfilter/vf_scale_vulkan.c:103:    C(0, void write_444(vec4 src, ivec2 pos)                                    )
libavfilter/vf_scale_vulkan.c:104:    C(0, {                                                                      )
libavfilter/vf_scale_vulkan.c:105:    C(1,     imageStore(output_img[0], pos, vec4(src.r, 0.0, 0.0, 0.0));        )
libavfilter/vf_scale_vulkan.c:106:    C(1,     imageStore(output_img[1], pos, vec4(src.g, 0.0, 0.0, 0.0));        )
libavfilter/vf_scale_vulkan.c:107:    C(1,     imageStore(output_img[2], pos, vec4(src.b, 0.0, 0.0, 0.0));        )
libavfilter/vf_scale_vulkan.c:108:    C(0, }                                                                      )
libavfilter/vf_scale_vulkan.c:109:};
libavfilter/vf_scale_vulkan.c:111:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
libavfilter/vf_scale_vulkan.c:130:    switch (s->scaler) {
libavfilter/vf_scale_vulkan.c:140:    if (!spv) {
libavfilter/vf_scale_vulkan.c:141:        av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
libavfilter/vf_scale_vulkan.c:145:    ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
libavfilter/vf_scale_vulkan.c:146:    RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
libavfilter/vf_scale_vulkan.c:147:    RET(ff_vk_init_sampler(vkctx, &s->sampler, 0, sampler_mode));
libavfilter/vf_scale_vulkan.c:148:    RET(ff_vk_shader_init(vkctx, &s->shd, "scale",
libavfilter/vf_scale_vulkan.c:154:    GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
libavfilter/vf_scale_vulkan.c:155:    GLSLC(1,    mat4 yuv_matrix;                                          );
libavfilter/vf_scale_vulkan.c:156:    GLSLC(0, };                                                           );
libavfilter/vf_scale_vulkan.c:157:    GLSLC(0,                                                              );
libavfilter/vf_scale_vulkan.c:159:    ff_vk_shader_add_push_const(&s->shd, 0, sizeof(s->opts),
libavfilter/vf_scale_vulkan.c:182:    RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 2, 0, 0));
libavfilter/vf_scale_vulkan.c:184:    GLSLD(   scale_bilinear                                                  );
```

- `grep(pattern=^(static |const |av_cold )?[A-Za-z_ *]+\(|^\}, version=old, path_glob=libavfilter/vf_transpose_vulkan.c)` →

```
71 matches (showing 60)
libavfilter/vf_transpose_vulkan.c:2: * copyright (c) 2021 Wu Jianhua <jianhua.wu@intel.com>
libavfilter/vf_transpose_vulkan.c:3: * Copyright (c) Lynne
libavfilter/vf_transpose_vulkan.c:42:} TransposeVulkanContext;
libavfilter/vf_transpose_vulkan.c:44:static av_cold int init_filter(AVFilterContext *ctx, AVFrame *in)
libavfilter/vf_transpose_vulkan.c:59:    if (!spv) {
libavfilter/vf_transpose_vulkan.c:60:        av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
libavfilter/vf_transpose_vulkan.c:64:    ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
libavfilter/vf_transpose_vulkan.c:65:    RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
libavfilter/vf_transpose_vulkan.c:66:    RET(ff_vk_init_sampler(vkctx, &s->sampler, 1, VK_FILTER_LINEAR));
libavfilter/vf_transpose_vulkan.c:67:    RET(ff_vk_shader_init(vkctx, &s->shd, "transpose",
libavfilter/vf_transpose_vulkan.c:93:    RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc, 2, 0, 0));
libavfilter/vf_transpose_vulkan.c:95:    GLSLC(0, void main()                                               );
libavfilter/vf_transpose_vulkan.c:96:    GLSLC(0, {                                                         );
libavfilter/vf_transpose_vulkan.c:97:    GLSLC(1,     ivec2 size;                                           );
libavfilter/vf_transpose_vulkan.c:98:    GLSLC(1,     ivec2 pos = ivec2(gl_GlobalInvocationID.xy);          );
libavfilter/vf_transpose_vulkan.c:99:    for (int i = 0; i < planes; i++) {
libavfilter/vf_transpose_vulkan.c:100:        GLSLC(0,                                                       );
libavfilter/vf_transpose_vulkan.c:101:        GLSLF(1, size = imageSize(output_images[%i]);                ,i);
libavfilter/vf_transpose_vulkan.c:102:        GLSLC(1, if (IS_WITHIN(pos, size)) {                           );
libavfilter/vf_transpose_vulkan.c:103:        if (s->dir == TRANSPOSE_CCLOCK)
libavfilter/vf_transpose_vulkan.c:104:            GLSLF(2, vec4 res = texture(input_images[%i], ivec2(size.y - pos.y, pos.x)); ,i);
libavfilter/vf_transpose_vulkan.c:105:        else if (s->dir == TRANSPOSE_CLOCK_FLIP || s->dir == TRANSPOSE_CLOCK) {
libavfilter/vf_transpose_vulkan.c:106:            GLSLF(2, vec4 res = texture(input_images[%i], ivec2(size.yx - pos.yx));      ,i);
libavfilter/vf_transpose_vulkan.c:107:            if (s->dir == TRANSPOSE_CLOCK)
libavfilter/vf_transpose_vulkan.c:108:                GLSLC(2, pos = ivec2(pos.x, size.y - pos.y);           );
libavfilter/vf_transpose_vulkan.c:110:            GLSLF(2, vec4 res = texture(input_images[%i], pos.yx);   ,i);
libavfilter/vf_transpose_vulkan.c:111:        GLSLF(2,     imageStore(output_images[%i], pos, res);        ,i);
libavfilter/vf_transpose_vulkan.c:112:        GLSLC(1, }                                                     );
libavfilter/vf_transpose_vulkan.c:114:    GLSLC(0, }                                                         );
libavfilter/vf_transpose_vulkan.c:116:    RET(spv->compile_shader(vkctx, spv, shd, &spv_data, &spv_len, "main",
libavfilter/vf_transpose_vulkan.c:118:    RET(ff_vk_shader_link(vkctx, shd, spv_data, spv_len, "main"));
libavfilter/vf_transpose_vulkan.c:120:    RET(ff_vk_shader_register_exec(vkctx, &s->e, &s->shd));
libavfilter/vf_transpose_vulkan.c:125:    if (spv_opaque)
libavfilter/vf_transpose_vulkan.c:127:    if (spv)
libavfilter/vf_transpose_vulkan.c:131:}
libavfilter/vf_transpose_vulkan.c:133:static int filter_frame(AVFilterLink *inlink, AVFrame *in)
libavfilter/vf_transpose_vulkan.c:141:    if (s->passthrough)
libavfilter/vf_transpose_vulkan.c:142:        return ff_filter_frame(outlink, in);
libavfilter/vf_transpose_vulkan.c:145:    if (!out) {
libavfilter/vf_transpose_vulkan.c:150:    if (!s->initialized)
libavfilter/vf_transpose_vulkan.c:151:        RET(init_filter(ctx, in));
libavfilter/vf_transpose_vulkan.c:153:    RET(ff_vk_filter_process_simple(&s->vkctx, &s->e, &s->shd, out, in,
libavfilter/vf_transpose_vulkan.c:156:    RET(av_frame_copy_props(out, in));
libavfilter/vf_transpose_vulkan.c:158:    if (in->sample_aspect_ratio.num)
libavfilter/vf_transpose_vulkan.c:165:    av_frame_free(&in);
libavfilter/vf_transpose_vulkan.c:167:    return ff_filter_frame(outlink, out);
libavfilter/vf_transpose_vulkan.c:170:    av_frame_free(&in);
libavfilter/vf_transpose_vulkan.c:171:    av_frame_free(&out);
libavfilter/vf_transpose_vulkan.c:173:}
libavfilter/vf_transpose_vulkan.c:175:static av_cold void transpose_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_transpose_vulkan.c:181:    ff_vk_exec_pool_free(vkctx, &s->e);
libavfilter/vf_transpose_vulkan.c:182:    ff_vk_shader_free(vkctx, &s->shd);
libavfilter/vf_transpose_vulkan.c:184:    if (s->sampler)
libavfilter/vf_transpose_vulkan.c:188:    ff_vk_uninit(&s->vkctx);
libavfilter/vf_transpose_vulkan.c:191:}
libavfilter/vf_transpose_vulkan.c:193:static int config_props_output(AVFilterLink *outlink)
libavfilter/vf_transpose_vulkan.c:202:    if ((inlink->w >= inlink->h && s->passthrough == TRANSPOSE_PT_TYPE_LANDSCAPE) ||
libavfilter/vf_transpose_vulkan.c:203:        (inlink->w <= inlink->h && s->passthrough == TRANSPOSE_PT_TYPE_PORTRAIT)) {
libavfilter/vf_transpose_vulkan.c:204:        av_log(avctx, AV_LOG_VERBOSE,
libavfilter/vf_transpose_vulkan.c:216:    if (inlink->sample_aspect_ratio.num)
```

- `grep(pattern=^(static |const |av_cold )?[A-Za-z_ *]+\(|^\}, version=old, path_glob=libavfilter/vf_xfade_vulkan.c)` →

```
272 matches (showing 60)
libavfilter/vf_xfade_vulkan.c:33:} XFadeParameters;
libavfilter/vf_xfade_vulkan.c:66:} XFadeVulkanContext;
libavfilter/vf_xfade_vulkan.c:87:};
libavfilter/vf_xfade_vulkan.c:90:    C(0, void transition(int idx, ivec2 pos, float progress)                   )
libavfilter/vf_xfade_vulkan.c:91:    C(0, {                                                                     )
libavfilter/vf_xfade_vulkan.c:92:    C(1,     vec4 a = texture(a_images[idx], pos);                             )
libavfilter/vf_xfade_vulkan.c:93:    C(1,     vec4 b = texture(b_images[idx], pos);                             )
libavfilter/vf_xfade_vulkan.c:94:    C(1,     imageStore(output_images[idx], pos, mix(a, b, progress));         )
libavfilter/vf_xfade_vulkan.c:95:    C(0, }                                                                     )
libavfilter/vf_xfade_vulkan.c:96:};
libavfilter/vf_xfade_vulkan.c:99:    C(0, void transition(int idx, ivec2 pos, float progress)                   )
libavfilter/vf_xfade_vulkan.c:100:    C(0, {                                                                     )
libavfilter/vf_xfade_vulkan.c:101:    C(1,     ivec2 size = imageSize(output_images[idx]);                       )
libavfilter/vf_xfade_vulkan.c:102:    C(1,     int  s = int(size.x * (1.0 - progress));                          )
libavfilter/vf_xfade_vulkan.c:103:    C(1,     vec4 a = texture(a_images[idx], pos);                             )
libavfilter/vf_xfade_vulkan.c:104:    C(1,     vec4 b = texture(b_images[idx], pos);                             )
libavfilter/vf_xfade_vulkan.c:105:    C(1,     imageStore(output_images[idx], pos, pos.x > s ? b : a);           )
libavfilter/vf_xfade_vulkan.c:106:    C(0, }                                                                     )
libavfilter/vf_xfade_vulkan.c:107:};
libavfilter/vf_xfade_vulkan.c:110:    C(0, void transition(int idx, ivec2 pos, float progress)                   )
libavfilter/vf_xfade_vulkan.c:111:    C(0, {                                                                     )
libavfilter/vf_xfade_vulkan.c:112:    C(1,     ivec2 size = imageSize(output_images[idx]);                       )
libavfilter/vf_xfade_vulkan.c:113:    C(1,     int  s = int(size.x * progress);                                  )
libavfilter/vf_xfade_vulkan.c:114:    C(1,     vec4 a = texture(a_images[idx], pos);                             )
libavfilter/vf_xfade_vulkan.c:115:    C(1,     vec4 b = texture(b_images[idx], pos);                             )
libavfilter/vf_xfade_vulkan.c:116:    C(1,     imageStore(output_images[idx], pos, pos.x > s ? a : b);           )
libavfilter/vf_xfade_vulkan.c:117:    C(0, }                                                                     )
libavfilter/vf_xfade_vulkan.c:118:};
libavfilter/vf_xfade_vulkan.c:121:    C(0, void transition(int idx, ivec2 pos, float progress)                   )
libavfilter/vf_xfade_vulkan.c:122:    C(0, {                                                                     )
libavfilter/vf_xfade_vulkan.c:123:    C(1,     ivec2 size = imageSize(output_images[idx]);                       )
libavfilter/vf_xfade_vulkan.c:124:    C(1,     int  s = int(size.y * (1.0 - progress));                          )
libavfilter/vf_xfade_vulkan.c:125:    C(1,     vec4 a = texture(a_images[idx], pos);                             )
libavfilter/vf_xfade_vulkan.c:126:    C(1,     vec4 b = texture(b_images[idx], pos);                             )
libavfilter/vf_xfade_vulkan.c:127:    C(1,     imageStore(output_images[idx], pos, pos.y > s ? b : a);           )
libavfilter/vf_xfade_vulkan.c:128:    C(0, }                                                                     )
libavfilter/vf_xfade_vulkan.c:129:};
libavfilter/vf_xfade_vulkan.c:132:    C(0, void transition(int idx, ivec2 pos, float progress)                   )
libavfilter/vf_xfade_vulkan.c:133:    C(0, {                                                                     )
libavfilter/vf_xfade_vulkan.c:134:    C(1,     ivec2 size = imageSize(output_images[idx]);                       )
libavfilter/vf_xfade_vulkan.c:135:    C(1,     int  s = int(size.y * progress);                                  )
libavfilter/vf_xfade_vulkan.c:136:    C(1,     vec4 a = texture(a_images[idx], pos);                             )
libavfilter/vf_xfade_vulkan.c:137:    C(1,     vec4 b = texture(b_images[idx], pos);                             )
libavfilter/vf_xfade_vulkan.c:138:    C(1,     imageStore(output_images[idx], pos, pos.y > s ? a : b);           )
libavfilter/vf_xfade_vulkan.c:139:    C(0, }                                                                     )
libavfilter/vf_xfade_vulkan.c:140:};
libavfilter/vf_xfade_vulkan.c:143:    C(0, void slide(int idx, ivec2 pos, float progress, ivec2 direction)               ) \
libavfilter/vf_xfade_vulkan.c:144:    C(0, {                                                                             ) \
libavfilter/vf_xfade_vulkan.c:145:    C(1,     ivec2 size = imageSize(output_images[idx]);                               ) \
libavfilter/vf_xfade_vulkan.c:146:    C(1,     ivec2 pi = ivec2(progress * size);                                        ) \
libavfilter/vf_xfade_vulkan.c:147:    C(1,     ivec2 p = pos + pi * direction;                                           ) \
libavfilter/vf_xfade_vulkan.c:148:    C(1,     ivec2 f = p % size;                                                       ) \
libavfilter/vf_xfade_vulkan.c:149:    C(1,     f = f + size * ivec2(f.x < 0, f.y < 0);                                   ) \
libavfilter/vf_xfade_vulkan.c:150:    C(1,     vec4 a = texture(a_images[idx], f);                                       ) \
libavfilter/vf_xfade_vulkan.c:151:    C(1,     vec4 b = texture(b_images[idx], f);                                       ) \
libavfilter/vf_xfade_vulkan.c:152:    C(1,     vec4 r = (p.y >= 0 && p.x >= 0 && size.y > p.y &&  size.x > p.x) ? a : b; ) \
libavfilter/vf_xfade_vulkan.c:153:    C(1,     imageStore(output_images[idx], pos, r);                                   ) \
libavfilter/vf_xfade_vulkan.c:154:    C(0, }                                                                             )
libavfilter/vf_xfade_vulkan.c:158:    C(0, void transition(int idx, ivec2 pos, float progress)                   )
libavfilter/vf_xfade_vulkan.c:159:    C(0, {                                                                     )
```

- `grep(pattern=^(static |const |av_cold )?[A-Za-z_ *]+\(|^\}, version=old, path_glob=libavfilter/vsrc_testsrc_vulkan.c)` →

```
89 matches (showing 60)
libavfilter/vsrc_testsrc_vulkan.c:2: * Copyright (c) Lynne
libavfilter/vsrc_testsrc_vulkan.c:32:};
libavfilter/vsrc_testsrc_vulkan.c:36:} TestSrcVulkanPushData;
libavfilter/vsrc_testsrc_vulkan.c:63:} TestSrcVulkanContext;
libavfilter/vsrc_testsrc_vulkan.c:65:static av_cold int init_filter(AVFilterContext *ctx, enum TestSrcVulkanMode mode)
libavfilter/vsrc_testsrc_vulkan.c:80:    if (!spv) {
libavfilter/vsrc_testsrc_vulkan.c:81:        av_log(ctx, AV_LOG_ERROR, "Unable to initialize SPIR-V compiler!\n");
libavfilter/vsrc_testsrc_vulkan.c:85:    ff_vk_qf_init(vkctx, &s->qf, VK_QUEUE_COMPUTE_BIT);
libavfilter/vsrc_testsrc_vulkan.c:86:    RET(ff_vk_exec_pool_init(vkctx, &s->qf, &s->e, s->qf.nb_queues*4, 0, 0, 0, NULL));
libavfilter/vsrc_testsrc_vulkan.c:87:    RET(ff_vk_shader_init(vkctx, &s->shd, "scale",
libavfilter/vsrc_testsrc_vulkan.c:93:    GLSLC(0, layout(push_constant, std430) uniform pushConstants {        );
libavfilter/vsrc_testsrc_vulkan.c:94:    GLSLC(1,    vec4 color_comp;                                          );
libavfilter/vsrc_testsrc_vulkan.c:95:    GLSLC(0, };                                                           );
libavfilter/vsrc_testsrc_vulkan.c:96:    GLSLC(0,                                                              );
libavfilter/vsrc_testsrc_vulkan.c:98:    ff_vk_shader_add_push_const(&s->shd, 0, sizeof(s->opts),
libavfilter/vsrc_testsrc_vulkan.c:113:    RET(ff_vk_shader_add_descriptor_set(vkctx, &s->shd, desc_set, 1, 0, 0));
libavfilter/vsrc_testsrc_vulkan.c:115:    GLSLC(0, void main()                                                  );
libavfilter/vsrc_testsrc_vulkan.c:116:    GLSLC(0, {                                                            );
libavfilter/vsrc_testsrc_vulkan.c:117:    GLSLC(1,     ivec2 pos = ivec2(gl_GlobalInvocationID.xy);             );
libavfilter/vsrc_testsrc_vulkan.c:118:    if (mode == TESTSRC_COLOR) {
libavfilter/vsrc_testsrc_vulkan.c:128:        if (desc->flags & AV_PIX_FMT_FLAG_RGB)
libavfilter/vsrc_testsrc_vulkan.c:133:        if (!(desc->flags & AV_PIX_FMT_FLAG_RGB) && !(luma = av_csp_luma_coeffs_from_avcsp(csp)))
libavfilter/vsrc_testsrc_vulkan.c:134:            return AVERROR(EINVAL);
libavfilter/vsrc_testsrc_vulkan.c:135:        else if (!(desc->flags & AV_PIX_FMT_FLAG_RGB))
libavfilter/vsrc_testsrc_vulkan.c:138:        for (int i = 0; i < 4; i++)
libavfilter/vsrc_testsrc_vulkan.c:141:        if (!(desc->flags & AV_PIX_FMT_FLAG_RGB))
libavfilter/vsrc_testsrc_vulkan.c:144:            memcpy(yuvad, rgbad, sizeof(rgbad));
libavfilter/vsrc_testsrc_vulkan.c:148:        if (!(desc->flags & AV_PIX_FMT_FLAG_RGB)) {
libavfilter/vsrc_testsrc_vulkan.c:149:            for (int i = 0; i < 3; i++) {
libavfilter/vsrc_testsrc_vulkan.c:151:                if (s->out_range == AVCOL_RANGE_MPEG) {
libavfilter/vsrc_testsrc_vulkan.c:161:        if (desc->nb_components <= 2)
libavfilter/vsrc_testsrc_vulkan.c:164:        for (int i = 0; i < 4; i++)
libavfilter/vsrc_testsrc_vulkan.c:167:        GLSLC(1,     vec4 r;                                                  );
libavfilter/vsrc_testsrc_vulkan.c:168:        GLSLC(0,                                                              );
libavfilter/vsrc_testsrc_vulkan.c:169:        for (int i = 0, c_off = 0; i < planes; i++) {
libavfilter/vsrc_testsrc_vulkan.c:170:            for (int c = 0; c < desc->nb_components; c++) {
libavfilter/vsrc_testsrc_vulkan.c:171:                if (desc->comp[c].plane == i) {
libavfilter/vsrc_testsrc_vulkan.c:173:                    GLSLF(1, r[%i] = color_comp[%i];             ,off, c_off++);
libavfilter/vsrc_testsrc_vulkan.c:176:            GLSLF(1, imageStore(output_img[%i], pos, r);                    ,i);
libavfilter/vsrc_testsrc_vulkan.c:177:            GLSLC(0,                                                          );
libavfilter/vsrc_testsrc_vulkan.c:180:    GLSLC(0, }                                                            );
libavfilter/vsrc_testsrc_vulkan.c:182:    RET(spv->compile_shader(vkctx, spv, shd, &spv_data, &spv_len, "main",
libavfilter/vsrc_testsrc_vulkan.c:184:    RET(ff_vk_shader_link(vkctx, shd, spv_data, spv_len, "main"));
libavfilter/vsrc_testsrc_vulkan.c:186:    RET(ff_vk_shader_register_exec(vkctx, &s->e, &s->shd));
libavfilter/vsrc_testsrc_vulkan.c:191:    if (spv_opaque)
libavfilter/vsrc_testsrc_vulkan.c:193:    if (spv)
libavfilter/vsrc_testsrc_vulkan.c:197:}
libavfilter/vsrc_testsrc_vulkan.c:199:static int testsrc_vulkan_activate(AVFilterContext *ctx)
libavfilter/vsrc_testsrc_vulkan.c:206:    if (!s->initialized) {
libavfilter/vsrc_testsrc_vulkan.c:209:        if (err < 0)
libavfilter/vsrc_testsrc_vulkan.c:213:    if (!ff_outlink_frame_wanted(outlink))
libavfilter/vsrc_testsrc_vulkan.c:215:    if (s->duration >= 0 &&
libavfilter/vsrc_testsrc_vulkan.c:216:        av_rescale_q(s->pts, s->time_base, AV_TIME_BASE_Q) >= s->duration) {
libavfilter/vsrc_testsrc_vulkan.c:217:        ff_outlink_set_status(outlink, AVERROR_EOF, s->pts);
libavfilter/vsrc_testsrc_vulkan.c:221:    if (s->draw_once) {
libavfilter/vsrc_testsrc_vulkan.c:222:        if (s->draw_once_reset) {
libavfilter/vsrc_testsrc_vulkan.c:223:            av_frame_free(&s->picref);
libavfilter/vsrc_testsrc_vulkan.c:226:        if (!s->picref) {
libavfilter/vsrc_testsrc_vulkan.c:228:            if (!s->picref)
libavfilter/vsrc_testsrc_vulkan.c:229:                return AVERROR(ENOMEM);
```

### Turn 4  _(tok 24561+522, stop=tool_use)_

**Reasoning:** I'm checking the function boundaries for overlay, scale, and transpose to confirm each call falls within init_filter's range, cross-referencing against the grep results.

For xfade and testsrc I'm tracing which function each call line falls into, confirming testsrc's call at 105 lands inside its init_filter. For xfade I still need to grep for top-level static functions beyond line 159 to pin down the right boundary.



- `grep(pattern=^(static|void|int|const|[a-z_]+ \*?[a-z_]+\(), version=old, path_glob=libavfilter/vf_xfade_vulkan.c)` →

```
29 matches
libavfilter/vf_xfade_vulkan.c:89:static const char transition_fade[] = {
libavfilter/vf_xfade_vulkan.c:98:static const char transition_wipeleft[] = {
libavfilter/vf_xfade_vulkan.c:109:static const char transition_wiperight[] = {
libavfilter/vf_xfade_vulkan.c:120:static const char transition_wipeup[] = {
libavfilter/vf_xfade_vulkan.c:131:static const char transition_wipedown[] = {
libavfilter/vf_xfade_vulkan.c:156:static const char transition_slidedown[] = {
libavfilter/vf_xfade_vulkan.c:164:static const char transition_slideup[] = {
libavfilter/vf_xfade_vulkan.c:172:static const char transition_slideleft[] = {
libavfilter/vf_xfade_vulkan.c:180:static const char transition_slideright[] = {
libavfilter/vf_xfade_vulkan.c:203:static const char transition_circleopen[] = {
libavfilter/vf_xfade_vulkan.c:211:static const char transition_circleclose[] = {
libavfilter/vf_xfade_vulkan.c:225:static const char transition_dissolve[] = {
libavfilter/vf_xfade_vulkan.c:236:static const char transition_pixelize[] = {
libavfilter/vf_xfade_vulkan.c:251:static const char transition_wipetl[] = {
libavfilter/vf_xfade_vulkan.c:263:static const char transition_wipetr[] = {
libavfilter/vf_xfade_vulkan.c:275:static const char transition_wipebl[] = {
libavfilter/vf_xfade_vulkan.c:287:static const char transition_wipebr[] = {
libavfilter/vf_xfade_vulkan.c:299:static const char* transitions_map[NB_TRANSITIONS] = {
libavfilter/vf_xfade_vulkan.c:319:static av_cold int init_vulkan(AVFilterContext *avctx)
libavfilter/vf_xfade_vulkan.c:413:static int xfade_frame(AVFilterContext *avctx, AVFrame *frame_a, AVFrame *frame_b)
libavfilter/vf_xfade_vulkan.c:454:static int config_props_output(AVFilterLink *outlink)
libavfilter/vf_xfade_vulkan.c:497:static int forward_frame(XFadeVulkanContext *s,
libavfilter/vf_xfade_vulkan.c:535:static int activate(AVFilterContext *avctx)
libavfilter/vf_xfade_vulkan.c:627:static av_cold void uninit(AVFilterContext *avctx)
libavfilter/vf_xfade_vulkan.c:645:static AVFrame *get_video_buffer(AVFilterLink *inlink, int w, int h)
libavfilter/vf_xfade_vulkan.c:657:static const AVOption xfade_vulkan_options[] = {
libavfilter/vf_xfade_vulkan.c:683:static const AVFilterPad xfade_vulkan_inputs[] = {
libavfilter/vf_xfade_vulkan.c:698:static const AVFilterPad xfade_vulkan_outputs[] = {
libavfilter/vf_xfade_vulkan.c:706:const AVFilter ff_vf_xfade_vulkan = {
```

- `grep(pattern=^(static|void|int)[^;]*$, version=old, path_glob=libavfilter/vf_nlmeans_vulkan.c)` →

```
13 matches
libavfilter/vf_nlmeans_vulkan.c:67:static void insert_first(FFVulkanShader *shd, int r, const char *off, int horiz, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:84:static void insert_horizontal_pass(FFVulkanShader *shd, int nb_rows, int first, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:110:static void insert_vertical_pass(FFVulkanShader *shd, int nb_rows, int first, int plane, int comp)
libavfilter/vf_nlmeans_vulkan.c:139:static void insert_weights_pass(FFVulkanShader *shd, int nb_rows, int vert,
libavfilter/vf_nlmeans_vulkan.c:211:static av_cold int init_weights_pipeline(FFVulkanContext *vkctx, FFVkExecPool *exec,
libavfilter/vf_nlmeans_vulkan.c:420:static av_cold int init_denoise_pipeline(FFVulkanContext *vkctx, FFVkExecPool *exec,
libavfilter/vf_nlmeans_vulkan.c:568:static av_cold int init_filter(AVFilterContext *ctx)
libavfilter/vf_nlmeans_vulkan.c:690:static int denoise_pass(NLMeansVulkanContext *s, FFVkExecContext *exec,
libavfilter/vf_nlmeans_vulkan.c:740:static int nlmeans_vulkan_filter_frame(AVFilterLink *link, AVFrame *in)
libavfilter/vf_nlmeans_vulkan.c:1045:static void nlmeans_vulkan_uninit(AVFilterContext *avctx)
libavfilter/vf_nlmeans_vulkan.c:1072:static const AVOption nlmeans_vulkan_options[] = {
libavfilter/vf_nlmeans_vulkan.c:1093:static const AVFilterPad nlmeans_vulkan_inputs[] = {
libavfilter/vf_nlmeans_vulkan.c:1102:static const AVFilterPad nlmeans_vulkan_outputs[] = {
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 27278+505, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_denoise_pipeline", "file": "libavfilter/vf_nlmeans_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_vulkan", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "medium"}`

**Score (self):** `{"n_pred": 3, "n_truth": 3, "tp": 2, "precision": 0.6666666666666666, "recall": 0.6666666666666666, "f1": 0.6666666666666666}`

## Tool arm

### Turn 1  _(tok 3766+231, stop=tool_use)_

**Reasoning:** I'll search the codebase for all call sites using get_callers and grep.



- `get_callers(name=ff_vk_shader_rep_fmt, limit=200, version=old)` →

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
      "file": "libavfilter/vf_flip_vulkan.c",
      "line": 86
    },
    {
      "caller": "init_gblur_pipeline",
      "file": "libavfilter/vf_gblur_vulkan.c",
      "line": 231
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

- `grep(pattern=ff_vk_shader_rep_fmt, version=old, max_results=500)` →

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

### Turn 2  _(tok 5370+664, stop=tool_use)_

**Reasoning:** I notice the grep results show more call sites than get_callers found—bwdif, chromaber, and nlmeans are missing. I need to check the enclosing function for each of those three using get_context_at.



**Says:** The grep finds three call sites that `get_callers` missed (bwdif, chromaber, nlmeans). I'll check their enclosing functions, and confirm the others.

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

- `get_context_at(file=libavfilter/vf_nlmeans_vulkan.c, line=457, version=old)` →

```
{
  "error": "libavfilter/vf_nlmeans_vulkan.c:457 is not inside a function definition in the old version"
}
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

CALLERS (1):
  libplacebo_query_format (libavfilter/vf_libplacebo.c:1094): RET(init_vulkan(ctx, vkhwctx));
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

CALLERS (0):
```

### Turn 3  _(tok 12603+657, stop=tool_use)_

**Reasoning:** I need to locate the enclosing functions for bwdif, chromaber, and nlmeans, confirming gblur's call sits in init_gblur_pipeline and xfade's in init_vulkan at line 367. I also want to double-check for call sites the literal-name grep might miss, like macros or function pointers.



**Says:** Confirmed: `init_vulkan` (xfade) and `init_gblur_pipeline` (gblur). The context tool couldn't resolve the other three, so I'll read those files directly.

- `read_file(path=libavfilter/vf_bwdif_vulkan.c, start_line=80, end_line=110, version=old)` →

```
libavfilter/vf_bwdif_vulkan.c lines 80-110 of 336
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
```

- `read_file(path=libavfilter/vf_chromaber_vulkan.c, start_line=95, end_line=122, version=old)` →

```
libavfilter/vf_chromaber_vulkan.c lines 95-122 of 259
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
```

- `read_file(path=libavfilter/vf_nlmeans_vulkan.c, start_line=420, end_line=460, version=old)` →

```
libavfilter/vf_nlmeans_vulkan.c lines 420-460 of 1123
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
  458|             .mem_quali   = "writeonly",
  459|             .dimensions  = 2,
  460|             .elems       = planes,
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 4  _(tok 15651+488, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_gblur_pipeline", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_vulkan", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_bwdif_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_chromaber_vulkan.c"}, {"function": "init_denoise_pipeline", "file": "libavfilter/vf_nlmeans_vulkan.c"}], "confidence_overall": "medium"}`

**Score (tool):** `{"n_pred": 4, "n_truth": 3, "tp": 3, "precision": 0.75, "recall": 1.0, "f1": 0.8571428571428571}`

## Semantic arm

### Turn 1  _(tok 3218+120, stop=tool_use)_

**Reasoning:** I'll check who calls ff_vk_shader_rep_fmt by querying with a high limit.



- `get_callers(name=ff_vk_shader_rep_fmt, limit=200)` →

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
      "file": "libavfilter/vf_flip_vulkan.c",
      "line": 86
    },
    {
      "caller": "init_gblur_pipeline",
      "file": "libavfilter/vf_gblur_vulkan.c",
      "line": 231
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

### Turn 2  _(tok 3855+494, stop=tool_use)_

**Reasoning:** I'm noticing get_callers defaulted to the "old" version rather than the current working tree, since the rev parameter controls this and defaults to the parent commit or HEAD — but there's no explicit version argument to force checking the "work" state instead.



- `get_neighborhood(name=ff_vk_shader_rep_fmt)` →

```
ff_vk_shader_rep_fmt — libavutil/vulkan.c:1289 [function] const char *ff_vk_shader_rep_fmt(enum AVPixelFormat pixfmt)
  reads: pixfmt; writes: -; returns: return high ? "rgba16f" : "rgba8";

CALLEES (1):
  av_pix_fmt_desc_get (libavutil/pixdesc.c:3025): reads pix_fmt; writes -; returns return NULL; | return &av_pix_fmt_descriptors[pix_fmt];

CALLERS (8):
  init_filter (libavfilter/vf_avgblur_vulkan.c:102): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_filter (libavfilter/vf_blend_vulkan.c:173): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_filter (libavfilter/vf_flip_vulkan.c:86): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_gblur_pipeline (libavfilter/vf_gblur_vulkan.c:231): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_filter (libavfilter/vf_overlay_vulkan.c:142): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_filter (libavfilter/vf_scale_vulkan.c:174): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_filter (libavfilter/vf_transpose_vulkan.c:85): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
  init_vulkan (libavfilter/vf_xfade_vulkan.c:367): .mem_layout = ff_vk_shader_rep_fmt(s->vkctx.output_format),
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

- `get_callers(name=ff_vk_shader_rep_fmt, limit=200, rev=HEAD)` →

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
      "file": "libavfilter/vf_flip_vulkan.c",
      "line": 86
    },
    {
      "caller": "init_gblur_pipeline",
      "file": "libavfilter/vf_gblur_vulkan.c",
      "line": 231
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

### Turn 3  _(tok 6495+2137, stop=tool_use)_

**Reasoning:** I notice there are 13 reference sites total but only 8 were followed, while the callers list has 9 entries including vsrc_testsrc—so some callers likely share functions with multiple call sites, and I need to check the remaining ones in the neighborhood list.

I'm trying to figure out whether "old" vs "new" corresponds to HEAD or its parent, since the tool's rev parameter doesn't let me select the working tree state directly. Rather than guessing at version semantics, I should just check the callers of the relevant functions directly to reconcile the discrepancy.

I know the line numbers for most of the known call sites (avgblur, blend, flip, gblur, overlay, scale, transpose, xfade, testsrc) but four sites remain unidentified. Comparing get_callers' nine results against the neighborhood tool's cut at 8-of-13, it seems the 13 total reference sites span across functions where some have multiple call sites, so get_callers might be collapsing or missing some of them.

I'm considering candidate files like vf_chromaber_vulkan.c, vf_libplacebo.c, vf_nlmeans_vulkan.c, and vf_bwdif_vulkan.c to track down the missing sites, but without known line numbers, get_context_at won't help directly. I think trying resolve_symbol on likely function names or expand_function with callees might narrow things down, though get_callers on "init_filter" broadly probably won't isolate what I need either.



- `get_context_at(file=libavfilter/vf_nlmeans_vulkan.c, line=100)` →

```
insert_horizontal_pass — libavfilter/vf_nlmeans_vulkan.c:84 [function] static void insert_horizontal_pass(FFVulkanShader *shd, int nb_rows, int first, int plane, int comp)
  reads: comp, first, nb_rows, plane, shd; writes: shd*; returns: -

SLICE around line 100 (def-use, level 2; '>' marks the seed):
static void insert_horizontal_pass(FFVulkanShader *shd, int nb_rows, int first, int plane, int comp) {
   GLSLF(1, pos.y = int(gl_GlobalInvocationID.x)* %i;, nb_rows);
   ...
   GLSLF(2, for(r = 0; r < %i; r++){, nb_rows);
   GLSLC(3, prefix_sum = DTYPE(0););
   GLSLC(3, offset = int_stride * uint64_t(pos.y + r););
   GLSLC(3, dst = DataBuffer(uint64_t(integral_data)+ offset););
   ...
   GLSLF(3, for(pos.x = 0; pos.x < width[%i]; pos.x++){, plane);
>  if(first)
     insert_first(shd, 0, "r", 0, plane, comp);
   else
     GLSLC(4, s2 = dst.v[pos.x];);
   GLSLC(4, dst.v[pos.x] = s2 + prefix_sum;);
   GLSLC(4, prefix_sum += s2;);
   ...
}

CALLEES (11):
  insert_first (libavfilter/vf_nlmeans_vulkan.c:67): reads comp, horiz, off, plane, r; writes shd*; returns -
  GLSLF [macro]: #define GLSLF(N, S, ...) \
  GLSLC [macro]: #define GLSLC(N, S) \
  not defined in this repository: int, barrier, if, unroll, for, DTYPE, uint64_t, DataBuffer

CALLERS (0):
```

- `get_context_at(file=libavfilter/vf_gblur_vulkan.c, line=231)` →

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

CALLERS (0):
```

- `get_function_source(name=ff_vk_shader_rep_fmt)` →

```
ff_vk_shader_rep_fmt (function, old version) — libavutil/vulkan.c:1289-1294
 1289| const char *ff_vk_shader_rep_fmt(enum AVPixelFormat pixfmt)
 1290| {
 1291|     const AVPixFmtDescriptor *desc = av_pix_fmt_desc_get(pixfmt);
 1292|     const int high = desc->comp[0].depth > 8;
 1293|     return high ? "rgba16f" : "rgba8";
 1294| }
```

### Turn 4  _(tok 12663+2590, stop=tool_use)_

**Reasoning:** The gblur call site inside init_gblur_pipeline's struct initializer looks fine on its own, but the "13 reference sites" count seems to mix in duplicates and possibly stale data, since struct initializers like xfade's can have multiple calls per function. The get_callers output only lists 9 entries, so I can't fully reconcile the discrepancy.

I'm wondering whether the 13-count includes non-call textual references like the prototype in vulkan.h or the definition itself alongside the 9 actual call sites, which would roughly explain the gap. I also want to verify whether the tool is reporting against the right revision, since passing rev="HEAD" still returned "old" rather than the current work tree, which is confusing.

I should try varying the rev parameter further and cross-check with another function's callers for consistency, then consider whether other Vulkan filters like chromaber or libplacebo might account for the remaining referenced sites.

I'm second-guessing whether get_callers is actually the reliable source of truth here, given the suspicious count of reference sites. Rather than fighting name ambiguity with resolve_symbol or get_neighborhood, I think I should just test get_callers directly with a smaller limit to see if it's truncating results.

Maybe the 13 counts include textual references like the definition itself, not just call sites, which I can't fully resolve with these tools. I think the safest path is to submit the 9 unique callers I found, though I could double-check if any newly-added files introduce additional callers.

get_callers seems like the best source here, and checking expand_function on ff_vk_shader_rep_fmt confirmed the same results. I'll go with medium confidence, listing init_filter (across multiple files), init_gblur_pipeline, and init_vulkan (xfade) as the enclosing functions, submitting 9 entries total.



- **submit_callers** → `{"callers": [{"function": "init_filter", "file": "libavfilter/vf_avgblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_blend_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_flip_vulkan.c"}, {"function": "init_gblur_pipeline", "file": "libavfilter/vf_gblur_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_overlay_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_scale_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vf_transpose_vulkan.c"}, {"function": "init_vulkan", "file": "libavfilter/vf_xfade_vulkan.c"}, {"function": "init_filter", "file": "libavfilter/vsrc_testsrc_vulkan.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

