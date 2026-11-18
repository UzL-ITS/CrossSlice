# Impact-analysis transcript — qemu @ 350785d41d8b — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `ramfb_setup` (hw/display/ramfb-stubs.c), arity 1->2
- truth: [['hw/display/ramfb-standalone.c', 'ramfb_realizefn'], ['hw/vfio/display.c', 'vfio_display_dmabuf_init'], ['hw/vfio/display.c', 'vfio_display_region_init']]

## Self-navigation arm

### Turn 1  _(tok 905+66, stop=tool_use)_

**Reasoning:** Let's search the repository for `ramfb_setup`.

- `grep(pattern=ramfb_setup, version=old, max_results=50)` →

```
6 matches
hw/display/ramfb-standalone.c:42:    ramfb->state = ramfb_setup(errp);
hw/display/ramfb-stubs.c:11:RAMFBState *ramfb_setup(Error **errp)
hw/display/ramfb.c:138:RAMFBState *ramfb_setup(Error **errp)
hw/vfio/display.c:368:        vdev->dpy->ramfb = ramfb_setup(errp);
hw/vfio/display.c:497:        vdev->dpy->ramfb = ramfb_setup(errp);
include/hw/display/ramfb.h:9:RAMFBState *ramfb_setup(Error **errp);
```

### Turn 2  _(tok 1144+257, stop=tool_use)_

**Reasoning:** I've found 4 call sites across the codebase in ramfb-standalone.c and vfio/display.c, with the rest being definitions or prototypes. Now I need to identify which functions are enclosing these locations.

- `read_file(path=hw/display/ramfb-standalone.c, start_line=20, end_line=55, version=old)` →

```
hw/display/ramfb-standalone.c lines 20-55 of 91
   20| };
   21| 
   22| static void display_update_wrapper(void *dev)
   23| {
   24|     RAMFBStandaloneState *ramfb = RAMFB(dev);
   25| 
   26|     if (0 /* native driver active */) {
   27|         /* non-standalone device would run native display update here */;
   28|     } else {
   29|         ramfb_display_update(ramfb->con, ramfb->state);
   30|     }
   31| }
   32| 
   33| static const GraphicHwOps wrapper_ops = {
   34|     .gfx_update = display_update_wrapper,
   35| };
   36| 
   37| static void ramfb_realizefn(DeviceState *dev, Error **errp)
   38| {
   39|     RAMFBStandaloneState *ramfb = RAMFB(dev);
   40| 
   41|     ramfb->con = graphic_console_init(dev, 0, &wrapper_ops, dev);
   42|     ramfb->state = ramfb_setup(errp);
   43| }
   44| 
   45| static bool migrate_needed(void *opaque)
   46| {
   47|     RAMFBStandaloneState *ramfb = RAMFB(opaque);
   48| 
   49|     return ramfb->migrate;
   50| }
   51| 
   52| static const VMStateDescription ramfb_dev_vmstate = {
   53|     .name = "ramfb-dev",
   54|     .version_id = 1,
   55|     .minimum_version_id = 1,
```

- `read_file(path=hw/vfio/display.c, start_line=330, end_line=380, version=old)` →

```
hw/vfio/display.c lines 330-380 of 580
  330| 
  331|     if (cursor && cursor->pos_updates) {
  332|         dpy_gl_cursor_position(dpy->con,
  333|                                cursor->pos_x,
  334|                                cursor->pos_y);
  335|         cursor->pos_updates = 0;
  336|     }
  337| 
  338|     dpy_gl_update(dpy->con, 0, 0, width, height);
  339| 
  340|     if (free_bufs) {
  341|         vfio_display_free_dmabufs(vdev);
  342|     }
  343| }
  344| 
  345| static int vfio_display_get_flags(void *opaque)
  346| {
  347|     return GRAPHIC_FLAGS_GL | GRAPHIC_FLAGS_DMABUF;
  348| }
  349| 
  350| static const GraphicHwOps vfio_display_dmabuf_ops = {
  351|     .get_flags  = vfio_display_get_flags,
  352|     .gfx_update = vfio_display_dmabuf_update,
  353|     .ui_info    = vfio_display_edid_ui_info,
  354| };
  355| 
  356| static bool vfio_display_dmabuf_init(VFIOPCIDevice *vdev, Error **errp)
  357| {
  358|     if (!display_opengl) {
  359|         error_setg(errp, "vfio-display-dmabuf: opengl not available");
  360|         return false;
  361|     }
  362| 
  363|     vdev->dpy = g_new0(VFIODisplay, 1);
  364|     vdev->dpy->con = graphic_console_init(DEVICE(vdev), 0,
  365|                                           &vfio_display_dmabuf_ops,
  366|                                           vdev);
  367|     if (vdev->enable_ramfb) {
  368|         vdev->dpy->ramfb = ramfb_setup(errp);
  369|         if (!vdev->dpy->ramfb) {
  370|             return false;
  371|         }
  372|     }
  373|     return vfio_display_edid_init(vdev, errp);
  374| }
  375| 
  376| static void vfio_display_dmabuf_exit(VFIODisplay *dpy)
  377| {
  378|     VFIODMABuf *dmabuf;
  379| 
  380|     if (QTAILQ_EMPTY(&dpy->dmabuf.bufs)) {
```

- `read_file(path=hw/vfio/display.c, start_line=460, end_line=510, version=old)` →

```
hw/vfio/display.c lines 460-510 of 580
  460|             error_report("%s: vfio_region_mmap(%d): %s", __func__,
  461|                          plane.region_index, strerror(-ret));
  462|             goto err;
  463|         }
  464|         assert(dpy->region.buffer.mmaps[0].mmap != NULL);
  465|     }
  466| 
  467|     if (dpy->region.surface == NULL) {
  468|         /* create surface */
  469|         dpy->region.surface = qemu_create_displaysurface_from
  470|             (plane.width, plane.height, format,
  471|              plane.stride, dpy->region.buffer.mmaps[0].mmap);
  472|         dpy_gfx_replace_surface(dpy->con, dpy->region.surface);
  473|     }
  474| 
  475|     /* full screen update */
  476|     dpy_gfx_update(dpy->con, 0, 0,
  477|                    surface_width(dpy->region.surface),
  478|                    surface_height(dpy->region.surface));
  479|     return;
  480| 
  481| err:
  482|     vfio_region_exit(&dpy->region.buffer);
  483|     vfio_region_finalize(&dpy->region.buffer);
  484| }
  485| 
  486| static const GraphicHwOps vfio_display_region_ops = {
  487|     .gfx_update = vfio_display_region_update,
  488| };
  489| 
  490| static bool vfio_display_region_init(VFIOPCIDevice *vdev, Error **errp)
  491| {
  492|     vdev->dpy = g_new0(VFIODisplay, 1);
  493|     vdev->dpy->con = graphic_console_init(DEVICE(vdev), 0,
  494|                                           &vfio_display_region_ops,
  495|                                           vdev);
  496|     if (vdev->enable_ramfb) {
  497|         vdev->dpy->ramfb = ramfb_setup(errp);
  498|         if (!vdev->dpy->ramfb) {
  499|             return false;
  500|         }
  501|     }
  502|     return true;
  503| }
  504| 
  505| static void vfio_display_region_exit(VFIODisplay *dpy)
  506| {
  507|     if (!dpy->region.buffer.size) {
  508|         return;
  509|     }
  510| 
```

### Turn 3  _(tok 3445+247, stop=tool_use)_

**Reasoning:** All the call sites have been identified: 3 functions. Also, confirm that the other matches were definitions (line 138 of ramfb.c is a definition, and line 11 of ramfb-stubs.c is a definition). Furthermore, also check whether there are any other calls via function pointers or aliases. Grep found a total of 6 matches, all of which have been confirmed. Done.


**Says:** All matches are accounted for: the two definitions (`hw/display/ramfb.c`, `hw/display/ramfb-stubs.c`), the prototype in `include/hw/display/ramfb.h`, and three real call sites.



- **submit_callers** → `{"callers": [{"function": "ramfb_realizefn", "file": "hw/display/ramfb-standalone.c"}, {"function": "vfio_display_dmabuf_init", "file": "hw/vfio/display.c"}, {"function": "vfio_display_region_init", "file": "hw/vfio/display.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1034+99, stop=tool_use)_

**Reasoning:** The user is asking me to find all callers of `ramfb_setup` in the repository. Let's start with find_references and checking the file.

- `find_references(name=ramfb_setup)` →

```
4 references
ramfb_setup        42 hw/display/ramfb-standalone.c     ramfb->state = ramfb_setup(errp);
ramfb_setup       368 hw/vfio/display.c         vdev->dpy->ramfb = ramfb_setup(errp);
ramfb_setup       497 hw/vfio/display.c         vdev->dpy->ramfb = ramfb_setup(errp);
ramfb_setup         9 include/hw/display/ramfb.h RAMFBState *ramfb_setup(Error **errp);
```

- `grep(pattern=ramfb_setup, version=old)` →

```
6 matches
hw/display/ramfb-standalone.c:42:    ramfb->state = ramfb_setup(errp);
hw/display/ramfb-stubs.c:11:RAMFBState *ramfb_setup(Error **errp)
hw/display/ramfb.c:138:RAMFBState *ramfb_setup(Error **errp)
hw/vfio/display.c:368:        vdev->dpy->ramfb = ramfb_setup(errp);
hw/vfio/display.c:497:        vdev->dpy->ramfb = ramfb_setup(errp);
include/hw/display/ramfb.h:9:RAMFBState *ramfb_setup(Error **errp);
```

### Turn 2  _(tok 1443+237, stop=tool_use)_

**Reasoning:** The grep results match find_references: the actual call sites are at line 42 of hw/display/ramfb-standalone.c, and at lines 368 and 497 of hw/vfio/display.c. Lines 138 of ramfb.c and 11 of ramfb-stubs.c are definitions, and the header is a prototype.

Next, I need to identify the enclosing functions. Let me try reading these files.

- `read_file(path=hw/display/ramfb-standalone.c, version=old, start_line=1, end_line=70)` →

```
hw/display/ramfb-standalone.c lines 1-70 of 91
    1| #include "qemu/osdep.h"
    2| #include "migration/vmstate.h"
    3| #include "qapi/error.h"
    4| #include "qemu/module.h"
    5| #include "hw/loader.h"
    6| #include "hw/qdev-properties.h"
    7| #include "hw/display/ramfb.h"
    8| #include "ui/console.h"
    9| #include "qom/object.h"
   10| 
   11| typedef struct RAMFBStandaloneState RAMFBStandaloneState;
   12| DECLARE_INSTANCE_CHECKER(RAMFBStandaloneState, RAMFB,
   13|                          TYPE_RAMFB_DEVICE)
   14| 
   15| struct RAMFBStandaloneState {
   16|     SysBusDevice parent_obj;
   17|     QemuConsole *con;
   18|     RAMFBState *state;
   19|     bool migrate;
   20| };
   21| 
   22| static void display_update_wrapper(void *dev)
   23| {
   24|     RAMFBStandaloneState *ramfb = RAMFB(dev);
   25| 
   26|     if (0 /* native driver active */) {
   27|         /* non-standalone device would run native display update here */;
   28|     } else {
   29|         ramfb_display_update(ramfb->con, ramfb->state);
   30|     }
   31| }
   32| 
   33| static const GraphicHwOps wrapper_ops = {
   34|     .gfx_update = display_update_wrapper,
   35| };
   36| 
   37| static void ramfb_realizefn(DeviceState *dev, Error **errp)
   38| {
   39|     RAMFBStandaloneState *ramfb = RAMFB(dev);
   40| 
   41|     ramfb->con = graphic_console_init(dev, 0, &wrapper_ops, dev);
   42|     ramfb->state = ramfb_setup(errp);
   43| }
   44| 
   45| static bool migrate_needed(void *opaque)
   46| {
   47|     RAMFBStandaloneState *ramfb = RAMFB(opaque);
   48| 
   49|     return ramfb->migrate;
   50| }
   51| 
   52| static const VMStateDescription ramfb_dev_vmstate = {
   53|     .name = "ramfb-dev",
   54|     .version_id = 1,
   55|     .minimum_version_id = 1,
   56|     .needed = migrate_needed,
   57|     .fields = (const VMStateField[]) {
   58|         VMSTATE_STRUCT_POINTER(state, RAMFBStandaloneState, ramfb_vmstate, RAMFBState),
   59|         VMSTATE_END_OF_LIST()
   60|     }
   61| };
   62| 
   63| static const Property ramfb_properties[] = {
   64|     DEFINE_PROP_BOOL("x-migrate", RAMFBStandaloneState, migrate,  true),
   65| };
   66| 
   67| static void ramfb_class_initfn(ObjectClass *klass, const void *data)
   68| {
   69|     DeviceClass *dc = DEVICE_CLASS(klass);
   70| 
```

- `read_file(path=hw/vfio/display.c, version=old, start_line=330, end_line=400)` →

```
hw/vfio/display.c lines 330-400 of 580
  330| 
  331|     if (cursor && cursor->pos_updates) {
  332|         dpy_gl_cursor_position(dpy->con,
  333|                                cursor->pos_x,
  334|                                cursor->pos_y);
  335|         cursor->pos_updates = 0;
  336|     }
  337| 
  338|     dpy_gl_update(dpy->con, 0, 0, width, height);
  339| 
  340|     if (free_bufs) {
  341|         vfio_display_free_dmabufs(vdev);
  342|     }
  343| }
  344| 
  345| static int vfio_display_get_flags(void *opaque)
  346| {
  347|     return GRAPHIC_FLAGS_GL | GRAPHIC_FLAGS_DMABUF;
  348| }
  349| 
  350| static const GraphicHwOps vfio_display_dmabuf_ops = {
  351|     .get_flags  = vfio_display_get_flags,
  352|     .gfx_update = vfio_display_dmabuf_update,
  353|     .ui_info    = vfio_display_edid_ui_info,
  354| };
  355| 
  356| static bool vfio_display_dmabuf_init(VFIOPCIDevice *vdev, Error **errp)
  357| {
  358|     if (!display_opengl) {
  359|         error_setg(errp, "vfio-display-dmabuf: opengl not available");
  360|         return false;
  361|     }
  362| 
  363|     vdev->dpy = g_new0(VFIODisplay, 1);
  364|     vdev->dpy->con = graphic_console_init(DEVICE(vdev), 0,
  365|                                           &vfio_display_dmabuf_ops,
  366|                                           vdev);
  367|     if (vdev->enable_ramfb) {
  368|         vdev->dpy->ramfb = ramfb_setup(errp);
  369|         if (!vdev->dpy->ramfb) {
  370|             return false;
  371|         }
  372|     }
  373|     return vfio_display_edid_init(vdev, errp);
  374| }
  375| 
  376| static void vfio_display_dmabuf_exit(VFIODisplay *dpy)
  377| {
  378|     VFIODMABuf *dmabuf;
  379| 
  380|     if (QTAILQ_EMPTY(&dpy->dmabuf.bufs)) {
  381|         return;
  382|     }
  383| 
  384|     while ((dmabuf = QTAILQ_FIRST(&dpy->dmabuf.bufs)) != NULL) {
  385|         vfio_display_free_one_dmabuf(dpy, dmabuf);
  386|     }
  387| }
  388| 
  389| /* ---------------------------------------------------------------------- */
  390| void vfio_display_reset(VFIOPCIDevice *vdev)
  391| {
  392|     if (!vdev || !vdev->dpy || !vdev->dpy->con ||
  393|         !vdev->dpy->dmabuf.primary) {
  394|         return;
  395|     }
  396| 
  397|     dpy_gl_scanout_disable(vdev->dpy->con);
  398|     vfio_display_dmabuf_exit(vdev->dpy);
  399|     dpy_gfx_update_full(vdev->dpy->con);
  400| }
```

### Turn 3  _(tok 3682+99, stop=tool_use)_

**Reasoning:** Line 368 is inside `vfio_display_dmabuf_init`. Next, let's check line 497.

- `read_file(path=hw/vfio/display.c, version=old, start_line=470, end_line=520)` →

```
hw/vfio/display.c lines 470-520 of 580
  470|             (plane.width, plane.height, format,
  471|              plane.stride, dpy->region.buffer.mmaps[0].mmap);
  472|         dpy_gfx_replace_surface(dpy->con, dpy->region.surface);
  473|     }
  474| 
  475|     /* full screen update */
  476|     dpy_gfx_update(dpy->con, 0, 0,
  477|                    surface_width(dpy->region.surface),
  478|                    surface_height(dpy->region.surface));
  479|     return;
  480| 
  481| err:
  482|     vfio_region_exit(&dpy->region.buffer);
  483|     vfio_region_finalize(&dpy->region.buffer);
  484| }
  485| 
  486| static const GraphicHwOps vfio_display_region_ops = {
  487|     .gfx_update = vfio_display_region_update,
  488| };
  489| 
  490| static bool vfio_display_region_init(VFIOPCIDevice *vdev, Error **errp)
  491| {
  492|     vdev->dpy = g_new0(VFIODisplay, 1);
  493|     vdev->dpy->con = graphic_console_init(DEVICE(vdev), 0,
  494|                                           &vfio_display_region_ops,
  495|                                           vdev);
  496|     if (vdev->enable_ramfb) {
  497|         vdev->dpy->ramfb = ramfb_setup(errp);
  498|         if (!vdev->dpy->ramfb) {
  499|             return false;
  500|         }
  501|     }
  502|     return true;
  503| }
  504| 
  505| static void vfio_display_region_exit(VFIODisplay *dpy)
  506| {
  507|     if (!dpy->region.buffer.size) {
  508|         return;
  509|     }
  510| 
  511|     vfio_region_exit(&dpy->region.buffer);
  512|     vfio_region_finalize(&dpy->region.buffer);
  513| }
  514| 
  515| /* ---------------------------------------------------------------------- */
  516| 
  517| bool vfio_display_probe(VFIOPCIDevice *vdev, Error **errp)
  518| {
  519|     struct vfio_device_gfx_plane_info probe;
  520|     int ret;
```

### Turn 4  _(tok 4538+539, stop=tool_use)_

**Reasoning:** Line 497 is inside `vfio_display_region_init`.

Therefore, the call sites are as follows:
1. `ramfb_realizefn` in hw/display/ramfb-standalone.c (line 42)
2. `vfio_display_dmabuf_init` in hw/vfio/display.c (line 368)
3. `vfio_display_region_init` in hw/vfio/display.c (line 497)

Other matches: definitions in hw/display/ramfb-stubs.c and hw/display/ramfb.c, prototypes in include/hw/display/ramfb.h — all excluded.

Double-checking whether there are other call sites, e.g., via macro wrappers. Already found all matches with grep "ramfb_setup". Good. Also checked the possibility of calls through function pointers (unlikely, since it's a simple function).

Confidence: high. Submitting three call sites.


**Says:** All references have been identified and verified:

**Call sites of `ramfb_setup`:**
1. `ramfb_realizefn` — `hw/display/ramfb-standalone.c:42` (`ramfb->state = ramfb_setup(errp);`)
2. `vfio_display_dmabuf_init` — `hw/vfio/display.c:368` (`vdev->dpy->ramfb = ramfb_setup(errp);`)
3. `vfio_display_region_init` — `hw/vfio/display.c:497` (`vdev->dpy->ramfb = ramfb_setup(errp);`)

**Excluded (not calls):**
- `hw/display/ramfb-stubs.c:11` — stub definition
- `hw/display/ramfb.c:138` — actual definition
- `include/hw/display/ramfb.h:9` — prototype

Both grep and the GNU Global index agree there are exactly 3 call sites; no indirect calls via function pointers exist for this symbol.



- **submit_callers** → `{"callers": [{"function": "ramfb_realizefn", "file": "hw/display/ramfb-standalone.c"}, {"function": "vfio_display_dmabuf_init", "file": "hw/vfio/display.c"}, {"function": "vfio_display_region_init", "file": "hw/vfio/display.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2734+85, stop=tool_use)_

**Reasoning:** Let me start by finding all the call sites of `ramfb_setup`.

- `get_callers(name=ramfb_setup)` →

```
{
  "name": "ramfb_setup",
  "version": "old",
  "callers": [
    {
      "caller": "ramfb_realizefn",
      "file": "hw/display/ramfb-standalone.c",
      "line": 42
    },
    {
      "caller": "vfio_display_dmabuf_init",
      "file": "hw/vfio/display.c",
      "line": 368
    },
    {
      "caller": "vfio_display_region_init",
      "file": "hw/vfio/display.c",
      "line": 497
    }
  ]
}
```

- `grep(pattern=ramfb_setup, version=old)` →

```
6 matches
hw/display/ramfb-standalone.c:42:    ramfb->state = ramfb_setup(errp);
hw/display/ramfb-stubs.c:11:RAMFBState *ramfb_setup(Error **errp)
hw/display/ramfb.c:138:RAMFBState *ramfb_setup(Error **errp)
hw/vfio/display.c:368:        vdev->dpy->ramfb = ramfb_setup(errp);
hw/vfio/display.c:497:        vdev->dpy->ramfb = ramfb_setup(errp);
include/hw/display/ramfb.h:9:RAMFBState *ramfb_setup(Error **errp);
```

### Turn 2  _(tok 3164+250, stop=tool_use)_

**Reasoning:** The grep results match get_callers: 3 call sites.
- ramfb_realizefn in hw/display/ramfb-standalone.c
- vfio_display_dmabuf_init in hw/vfio/display.c
- vfio_display_region_init in hw/vfio/display.c

The other matches are the definition (ramfb-stubs.c, ramfb.c) and the prototype (ramfb.h). Confirmed to be complete.


**Says:** The grep confirms exactly 3 call sites, matching the semantic caller analysis. The other occurrences are the two definitions (`ramfb-stubs.c`, `ramfb.c`) and the header prototype, which are excluded.



- **submit_callers** → `{"callers": [{"file": "hw/display/ramfb-standalone.c", "function": "ramfb_realizefn"}, {"file": "hw/vfio/display.c", "function": "vfio_display_dmabuf_init"}, {"file": "hw/vfio/display.c", "function": "vfio_display_region_init"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2312+55, stop=tool_use)_

**Reasoning:** Let me find all callers of `ramfb_setup`.

- `get_callers(name=ramfb_setup, limit=100)` →

```
{
  "name": "ramfb_setup",
  "version": "old",
  "callers": [
    {
      "caller": "ramfb_realizefn",
      "file": "hw/display/ramfb-standalone.c",
      "line": 42
    },
    {
      "caller": "vfio_display_dmabuf_init",
      "file": "hw/vfio/display.c",
      "line": 368
    },
    {
      "caller": "vfio_display_region_init",
      "file": "hw/vfio/display.c",
      "line": 497
    }
  ]
}
```

### Turn 2  _(tok 2538+147, stop=tool_use)_

**Reasoning:** The `get_callers` tool returned 3 callers. Note that the definition itself is in `hw/display/ramfb-stubs.c`, and that's the stub version. It's possible there's another definition in `hw/display/ramfb.c`, but the callers don't change. Let me verify by checking the symbol's resolution and seeing if there are any other callers. The limit of 100 is far more than 3, so it's complete.

Just to be safe, let me verify with resolve_symbol to make sure there's only one symbol.


- `resolve_symbol(name=ramfb_setup)` →

```
{
  "resolved": true,
  "name": "ramfb_setup",
  "version": "old",
  "file": "hw/display/ramfb-stubs.c",
  "line": 11,
  "kind": "function",
  "signature": "RAMFBState *ramfb_setup(Error **errp)",
  "resolution_method": "gtags+ts",
  "ambiguous": false
}
```

### Turn 3  _(tok 2797+321, stop=tool_use)_

**Reasoning:** The symbol resolves unambiguously to `hw/display/ramfb-stubs.c`. The callers are:

1. `ramfb_realizefn` in `hw/display/ramfb-standalone.c`
2. `vfio_display_dmabuf_init` in `hw/vfio/display.c`
3. `vfio_display_region_init` in `hw/vfio/display.c`

With a limit of 100, only 3 callers were returned, so the list is complete. Submitting.


**Says:** The search returned exactly three call sites (well under the limit of 100), and the symbol resolves unambiguously. The complete list of callers is:

1. `ramfb_realizefn` — `hw/display/ramfb-standalone.c`
2. `vfio_display_dmabuf_init` — `hw/vfio/display.c`
3. `vfio_display_region_init` — `hw/vfio/display.c`



- **submit_callers** → `{"callers": [{"function": "ramfb_realizefn", "file": "hw/display/ramfb-standalone.c"}, {"function": "vfio_display_dmabuf_init", "file": "hw/vfio/display.c"}, {"function": "vfio_display_region_init", "file": "hw/vfio/display.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 3, "n_truth": 3, "tp": 3, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

