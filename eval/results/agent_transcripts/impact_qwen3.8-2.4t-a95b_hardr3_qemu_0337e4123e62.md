# Impact-analysis transcript — qemu @ 0337e4123e62 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `qemu_input_is_absolute` (ui/input.c), arity 0->1
- truth: [['ui/cocoa.m', 'cocoa_refresh'], ['ui/dbus-console.c', 'dbus_mouse_rel_motion'], ['ui/dbus-console.c', 'dbus_mouse_set_pos'], ['ui/dbus-console.c', 'dbus_mouse_update_is_absolute'], ['ui/gtk.c', 'gd_button_event'], ['ui/gtk.c', 'gd_motion_event'], ['ui/gtk.c', 'gd_mouse_mode_change'], ['ui/gtk.c', 'gd_mouse_set'], ['ui/gtk.c', 'gd_update_cursor'], ['ui/input.c', 'qemu_input_check_mode_change'], ['ui/sdl2.c', 'handle_mousebutton'], ['ui/sdl2.c', 'handle_mousemotion'], ['ui/sdl2.c', 'handle_windowevent'], ['ui/sdl2.c', 'sdl_grab_start'], ['ui/sdl2.c', 'sdl_hide_cursor'], ['ui/sdl2.c', 'sdl_mouse_define'], ['ui/sdl2.c', 'sdl_mouse_mode_change'], ['ui/sdl2.c', 'sdl_mouse_warp'], ['ui/sdl2.c', 'sdl_send_mouse_event'], ['ui/sdl2.c', 'sdl_show_cursor'], ['ui/spice-input.c', 'mouse_mode_notifier'], ['ui/vnc.c', 'check_pointer_type_change']]

## Self-navigation arm

### Turn 1  _(tok 904+69, stop=tool_use)_

**Reasoning:** I'll try searching for the function within the repository.


- `grep(pattern=qemu_input_is_absolute, version=old, max_results=100)` →

```
29 matches
include/ui/input.h:60:bool qemu_input_is_absolute(void);
ui/cocoa.m:327: * isAbsoluteEnabled tracks qemu_input_is_absolute() [ie "is the emulated
ui/cocoa.m:2004:    if (qemu_input_is_absolute()) {
ui/dbus-console.c:389:    if (qemu_input_is_absolute()) {
ui/dbus-console.c:456:    if (!qemu_input_is_absolute()) {
ui/dbus-console.c:517:                 "is-absolute", qemu_input_is_absolute(),
ui/gtk.c:207:    if (s->full_screen || qemu_input_is_absolute() || s->ptr_owner == vc) {
ui/gtk.c:456:        qemu_input_is_absolute()) {
ui/gtk.c:692:    if (qemu_input_is_absolute() && s->ptr_owner) {
ui/gtk.c:906:    if (qemu_input_is_absolute()) {
ui/gtk.c:926:    if (!qemu_input_is_absolute() && s->ptr_owner == vc) {
ui/gtk.c:968:        !qemu_input_is_absolute() && s->ptr_owner != vc) {
ui/input.c:497:bool qemu_input_is_absolute(void)
ui/input.c:591:    is_absolute = qemu_input_is_absolute();
ui/sdl2.c:206:    if (!qemu_input_is_absolute()) {
ui/sdl2.c:217:    if (!qemu_input_is_absolute()) {
ui/sdl2.c:222:        (gui_grab || qemu_input_is_absolute() || absolute_enabled)) {
ui/sdl2.c:248:        if (!qemu_input_is_absolute() && !absolute_enabled) {
ui/sdl2.c:283:    if (qemu_input_is_absolute()) {
ui/sdl2.c:314:    if (qemu_input_is_absolute()) {
ui/sdl2.c:500:    if (qemu_input_is_absolute() || absolute_enabled) {
ui/sdl2.c:516:    if (gui_grab || qemu_input_is_absolute() || absolute_enabled) {
ui/sdl2.c:533:    if (!gui_grab && !qemu_input_is_absolute()) {
ui/sdl2.c:606:        if (!gui_grab && (qemu_input_is_absolute() || absolute_enabled)) {
ui/sdl2.c:736:        if (gui_grab || qemu_input_is_absolute() || absolute_enabled) {
ui/sdl2.c:738:            if (!qemu_input_is_absolute() && !absolute_enabled) {
ui/sdl2.c:776:        (gui_grab || qemu_input_is_absolute() || absolute_enabled)) {
ui/spice-input.c:227:    bool is_absolute  = qemu_input_is_absolute();
ui/vnc.c:1774:    int absolute = qemu_input_is_absolute();
```

### Turn 2  _(tok 1673+394, stop=tool_use)_

**Reasoning:** I need to identify the function that contains each call site. Let's check each file:

1. ui/cocoa.m:2004
2. ui/dbus-console.c:389, 456, 517
3. ui/gtk.c:207, 456, 692, 906, 926, 968
4. ui/input.c:591 (a call within input.c itself — need to identify the containing function)
5. ui/sdl2.c:206, 217, 222, 248, 283, 314, 500, 516, 533, 606, 736, 738, 776
6. ui/spice-input.c:227
7. ui/vnc.c:1774

Let's read around each location to identify the containing function. I'll do this for each file.


**Says:** Found the call sites. Now I need to identify the enclosing function for each. Let me examine each file.



- `read_file(path=ui/cocoa.m, start_line=1985, end_line=2010, version=old)` →

```
ui/cocoa.m lines 1985-2010 of 2101
 1985|     // The DisplaySurface will be freed as soon as this callback returns.
 1986|     // We take a reference to the underlying pixman image here so it does
 1987|     // not disappear from under our feet; the switchSurface method will
 1988|     // deref the old image when it is done with it.
 1989|     pixman_image_ref(image);
 1990| 
 1991|     dispatch_async(dispatch_get_main_queue(), ^{
 1992|         [cocoaView updateUIInfo];
 1993|         [cocoaView switchSurface:image];
 1994|     });
 1995| }
 1996| 
 1997| static void cocoa_refresh(DisplayChangeListener *dcl)
 1998| {
 1999|     NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
 2000| 
 2001|     COCOA_DEBUG("qemu_cocoa: cocoa_refresh\n");
 2002|     graphic_hw_update(NULL);
 2003| 
 2004|     if (qemu_input_is_absolute()) {
 2005|         dispatch_async(dispatch_get_main_queue(), ^{
 2006|             if (![cocoaView isAbsoluteEnabled]) {
 2007|                 if ([cocoaView isMouseGrabbed]) {
 2008|                     [cocoaView ungrabMouse];
 2009|                 }
 2010|             }
```

- `read_file(path=ui/dbus-console.c, start_line=370, end_line=530, version=old)` →

```
ui/dbus-console.c lines 370-530 of 625
  370| 
  371|     return DBUS_METHOD_INVOCATION_HANDLED;
  372| }
  373| 
  374| static void
  375| dbus_kbd_qemu_leds_updated(void *data, int ledstate)
  376| {
  377|     DBusDisplayConsole *ddc = DBUS_DISPLAY_CONSOLE(data);
  378| 
  379|     qemu_dbus_display1_keyboard_set_modifiers(ddc->iface_kbd, ledstate);
  380| }
  381| 
  382| static gboolean
  383| dbus_mouse_rel_motion(DBusDisplayConsole *ddc,
  384|                       GDBusMethodInvocation *invocation,
  385|                       int dx, int dy)
  386| {
  387|     trace_dbus_mouse_rel_motion(dx, dy);
  388| 
  389|     if (qemu_input_is_absolute()) {
  390|         g_dbus_method_invocation_return_error(
  391|             invocation, DBUS_DISPLAY_ERROR,
  392|             DBUS_DISPLAY_ERROR_INVALID,
  393|             "Mouse is not relative");
  394|         return DBUS_METHOD_INVOCATION_HANDLED;
  395|     }
  396| 
  397|     qemu_input_queue_rel(ddc->dcl.con, INPUT_AXIS_X, dx);
  398|     qemu_input_queue_rel(ddc->dcl.con, INPUT_AXIS_Y, dy);
  399|     qemu_input_event_sync();
  400| 
  401|     qemu_dbus_display1_mouse_complete_rel_motion(ddc->iface_mouse,
  402|                                                     invocation);
  403| 
  404|     return DBUS_METHOD_INVOCATION_HANDLED;
  405| }
  406| 
  407| static gboolean
  408| dbus_touch_send_event(DBusDisplayConsole *ddc,
  409|                       GDBusMethodInvocation *invocation,
  410|                       guint kind, uint64_t num_slot,
  411|                       double x, double y)
  412| {
  413|     Error *error = NULL;
  414|     int width, height;
  415|     trace_dbus_touch_send_event(kind, num_slot, x, y);
  416| 
  417|     if (kind != INPUT_MULTI_TOUCH_TYPE_BEGIN &&
  418|         kind != INPUT_MULTI_TOUCH_TYPE_UPDATE &&
  419|         kind != INPUT_MULTI_TOUCH_TYPE_CANCEL &&
  420|         kind != INPUT_MULTI_TOUCH_TYPE_END)
  421|     {
  422|         g_dbus_method_invocation_return_error(
  423|             invocation, DBUS_DISPLAY_ERROR,
  424|             DBUS_DISPLAY_ERROR_INVALID,
  425|             "Invalid touch event kind");
  426|         return DBUS_METHOD_INVOCATION_HANDLED;
  427|     }
  428|     width = qemu_console_get_width(ddc->dcl.con, 0);
  429|     height = qemu_console_get_height(ddc->dcl.con, 0);
  430| 
  431|     console_handle_touch_event(ddc->dcl.con, touch_slots,
  432|                                num_slot, width, height,
  433|                                x, y, kind, &error);
  434|     if (error != NULL) {
  435|         g_dbus_method_invocation_return_error(
  436|             invocation, DBUS_DISPLAY_ERROR,
  437|             DBUS_DISPLAY_ERROR_INVALID,
  438|             error_get_pretty(error), NULL);
  439|         error_free(error);
  440|     } else {
  441|         qemu_dbus_display1_multi_touch_complete_send_event(ddc->iface_touch,
  442|                                                            invocation);
  443|     }
  444|     return DBUS_METHOD_INVOCATION_HANDLED;
  445| }
  446| 
  447| static gboolean
  448| dbus_mouse_set_pos(DBusDisplayConsole *ddc,
  449|                    GDBusMethodInvocation *invocation,
  450|                    guint x, guint y)
  451| {
  452|     int width, height;
  453| 
  454|     trace_dbus_mouse_set_pos(x, y);
  455| 
  456|     if (!qemu_input_is_absolute()) {
  457|         g_dbus_method_invocation_return_error(
  458|             invocation, DBUS_DISPLAY_ERROR,
  459|             DBUS_DISPLAY_ERROR_INVALID,
  460|             "Mouse is not absolute");
  461|         return DBUS_METHOD_INVOCATION_HANDLED;
  462|     }
  463| 
  464|     width = qemu_console_get_width(ddc->dcl.con, 0);
  465|     height = qemu_console_get_height(ddc->dcl.con, 0);
  466|     if (x >= width || y >= height) {
  467|         g_dbus_method_invocation_return_error(
  468|             invocation, DBUS_DISPLAY_ERROR,
  469|             DBUS_DISPLAY_ERROR_INVALID,
  470|             "Invalid mouse position");
  471|         return DBUS_METHOD_INVOCATION_HANDLED;
  472|     }
  473|     qemu_input_queue_abs(ddc->dcl.con, INPUT_AXIS_X, x, 0, width);
  474|     qemu_input_queue_abs(ddc->dcl.con, INPUT_AXIS_Y, y, 0, height);
  475|     qemu_input_event_sync();
  476| 
  477|     qemu_dbus_display1_mouse_complete_set_abs_position(ddc->iface_mouse,
  478|                                                           invocation);
  479| 
  480|     return DBUS_METHOD_INVOCATION_HANDLED;
  481| }
  482| 
  483| static gboolean
  484| dbus_mouse_press(DBusDisplayConsole *ddc,
  485|                  GDBusMethodInvocation *invocation,
  486|                  guint button)
  487| {
  488|     trace_dbus_mouse_press(button);
  489| 
  490|     qemu_input_queue_btn(ddc->dcl.con, button, true);
  491|     qemu_input_event_sync();
  492| 
  493|     qemu_dbus_display1_mouse_complete_press(ddc->iface_mouse, invocation);
  494| 
  495|     return DBUS_METHOD_INVOCATION_HANDLED;
  496| }
  497| 
  498| static gboolean
  499| dbus_mouse_release(DBusDisplayConsole *ddc,
  500|                    GDBusMethodInvocation *invocation,
  501|                    guint button)
  502| {
  503|     trace_dbus_mouse_release(button);
  504| 
  505|     qemu_input_queue_btn(ddc->dcl.con, button, false);
  506|     qemu_input_event_sync();
  507| 
  508|     qemu_dbus_display1_mouse_complete_release(ddc->iface_mouse, invocation);
  509| 
  510|     return DBUS_METHOD_INVOCATION_HANDLED;
  511| }
  512| 
  513| static void
  514| dbus_mouse_update_is_absolute(DBusDisplayConsole *ddc)
  515| {
  516|     g_object_set(ddc->iface_mouse,
  517|                  "is-absolute", qemu_input_is_absolute(),
  518|                  NULL);
  519| }
  520| 
  521| static void
  522| dbus_mouse_mode_change(Notifier *notify, void *data)
  523| {
  524|     DBusDisplayConsole *ddc =
  525|         container_of(notify, DBusDisplayConsole, mouse_mode_notifier);
  526| 
  527|     dbus_mouse_update_is_absolute(ddc);
  528| }
  529| 
  530| int dbus_display_console_get_index(DBusDisplayConsole *ddc)
```

### Turn 3  _(tok 4750+350, stop=tool_use)_

**Reasoning:** dbus-console.c:
- 389: dbus_mouse_rel_motion
- 456: dbus_mouse_set_pos
- 517: dbus_mouse_update_is_absolute

Next up is gtk.c: lines 207, 456, 692, 906, 926, 968.


- `read_file(path=ui/gtk.c, start_line=190, end_line=215, version=old)` →

```
ui/gtk.c lines 190-215 of 2531
  190| }
  191| 
  192| static void gd_update_cursor(VirtualConsole *vc)
  193| {
  194|     GtkDisplayState *s = vc->s;
  195|     GdkWindow *window;
  196| 
  197|     if (vc->type != GD_VC_GFX ||
  198|         !qemu_console_is_graphic(vc->gfx.dcl.con)) {
  199|         return;
  200|     }
  201| 
  202|     if (!gtk_widget_get_realized(vc->gfx.drawing_area)) {
  203|         return;
  204|     }
  205| 
  206|     window = gtk_widget_get_window(GTK_WIDGET(vc->gfx.drawing_area));
  207|     if (s->full_screen || qemu_input_is_absolute() || s->ptr_owner == vc) {
  208|         gdk_window_set_cursor(window, s->null_cursor);
  209|     } else {
  210|         gdk_window_set_cursor(window, NULL);
  211|     }
  212| }
  213| 
  214| static void gd_update_caption(GtkDisplayState *s)
  215| {
```

- `read_file(path=ui/gtk.c, start_line=435, end_line=470, version=old)` →

```
ui/gtk.c lines 435-470 of 2531
  435|                                mx + x1, my + y1, (x2 - x1), (y2 - y1));
  436| }
  437| 
  438| static void gd_refresh(DisplayChangeListener *dcl)
  439| {
  440|     graphic_hw_update(dcl->con);
  441| }
  442| 
  443| static GdkDevice *gd_get_pointer(GdkDisplay *dpy)
  444| {
  445|     return gdk_seat_get_pointer(gdk_display_get_default_seat(dpy));
  446| }
  447| 
  448| static void gd_mouse_set(DisplayChangeListener *dcl,
  449|                          int x, int y, int visible)
  450| {
  451|     VirtualConsole *vc = container_of(dcl, VirtualConsole, gfx.dcl);
  452|     GdkDisplay *dpy;
  453|     gint x_root, y_root;
  454| 
  455|     if (!gtk_widget_get_realized(vc->gfx.drawing_area) ||
  456|         qemu_input_is_absolute()) {
  457|         return;
  458|     }
  459| 
  460|     dpy = gtk_widget_get_display(vc->gfx.drawing_area);
  461|     gdk_window_get_root_coords(gtk_widget_get_window(vc->gfx.drawing_area),
  462|                                x, y, &x_root, &y_root);
  463|     gdk_device_warp(gd_get_pointer(dpy),
  464|                     gtk_widget_get_screen(vc->gfx.drawing_area),
  465|                     x_root, y_root);
  466|     vc->s->last_x = x;
  467|     vc->s->last_y = y;
  468| }
  469| 
  470| static void gd_cursor_define(DisplayChangeListener *dcl,
```

- `read_file(path=ui/gtk.c, start_line=670, end_line=700, version=old)` →

```
ui/gtk.c lines 670-700 of 2531
  670|     .dpy_gl_ctx_make_current = gd_egl_make_current,
  671| };
  672| #endif
  673| 
  674| #endif /* CONFIG_OPENGL */
  675| 
  676| /** QEMU Events **/
  677| 
  678| static void gd_change_runstate(void *opaque, bool running, RunState state)
  679| {
  680|     GtkDisplayState *s = opaque;
  681| 
  682|     gd_update_caption(s);
  683| }
  684| 
  685| static void gd_mouse_mode_change(Notifier *notify, void *data)
  686| {
  687|     GtkDisplayState *s;
  688|     int i;
  689| 
  690|     s = container_of(notify, GtkDisplayState, mouse_mode_notifier);
  691|     /* release the grab at switching to absolute mode */
  692|     if (qemu_input_is_absolute() && s->ptr_owner) {
  693|         if (!s->ptr_owner->window) {
  694|             gtk_check_menu_item_set_active(GTK_CHECK_MENU_ITEM(s->grab_item),
  695|                                            FALSE);
  696|         } else {
  697|             gd_ungrab_pointer(s);
  698|         }
  699|     }
  700|     for (i = 0; i < s->nb_vcs; i++) {
```

- `read_file(path=ui/gtk.c, start_line=890, end_line=980, version=old)` →

```
ui/gtk.c lines 890-980 of 2531
  890| 
  891|     ww = gtk_widget_get_allocated_width(widget);
  892|     wh = gtk_widget_get_allocated_height(widget);
  893|     ws = gtk_widget_get_scale_factor(widget);
  894| 
  895|     mx = my = 0;
  896|     if (ww > fbw) {
  897|         mx = (ww - fbw) / 2;
  898|     }
  899|     if (wh > fbh) {
  900|         my = (wh - fbh) / 2;
  901|     }
  902| 
  903|     x = (motion->x - mx) / vc->gfx.scale_x * ws;
  904|     y = (motion->y - my) / vc->gfx.scale_y * ws;
  905| 
  906|     if (qemu_input_is_absolute()) {
  907|         if (x < 0 || y < 0 ||
  908|             x >= surface_width(vc->gfx.ds) ||
  909|             y >= surface_height(vc->gfx.ds)) {
  910|             return TRUE;
  911|         }
  912|         qemu_input_queue_abs(vc->gfx.dcl.con, INPUT_AXIS_X, x,
  913|                              0, surface_width(vc->gfx.ds));
  914|         qemu_input_queue_abs(vc->gfx.dcl.con, INPUT_AXIS_Y, y,
  915|                              0, surface_height(vc->gfx.ds));
  916|         qemu_input_event_sync();
  917|     } else if (s->last_set && s->ptr_owner == vc) {
  918|         qemu_input_queue_rel(vc->gfx.dcl.con, INPUT_AXIS_X, x - s->last_x);
  919|         qemu_input_queue_rel(vc->gfx.dcl.con, INPUT_AXIS_Y, y - s->last_y);
  920|         qemu_input_event_sync();
  921|     }
  922|     s->last_x = x;
  923|     s->last_y = y;
  924|     s->last_set = TRUE;
  925| 
  926|     if (!qemu_input_is_absolute() && s->ptr_owner == vc) {
  927|         GdkScreen *screen = gtk_widget_get_screen(vc->gfx.drawing_area);
  928|         GdkDisplay *dpy = gtk_widget_get_display(widget);
  929|         GdkWindow *win = gtk_widget_get_window(widget);
  930|         GdkMonitor *monitor = gdk_display_get_monitor_at_window(dpy, win);
  931|         GdkRectangle geometry;
  932| 
  933|         int xr = (int)motion->x_root;
  934|         int yr = (int)motion->y_root;
  935| 
  936|         gdk_monitor_get_geometry(monitor, &geometry);
  937| 
  938|         /* In relative mode check to see if client pointer hit
  939|          * one of the monitor edges, and if so move it back to the
  940|          * center of the monitor. This is important because the pointer
  941|          * in the server doesn't correspond 1-for-1, and so
  942|          * may still be only half way across the screen. Without
  943|          * this warp, the server pointer would thus appear to hit
  944|          * an invisible wall */
  945|         if (xr <= geometry.x || xr - geometry.x >= geometry.width - 1 ||
  946|             yr <= geometry.y || yr - geometry.y >= geometry.height - 1) {
  947|             GdkDevice *dev = gdk_event_get_device((GdkEvent *)motion);
  948|             xr = geometry.x + geometry.width / 2;
  949|             yr = geometry.y + geometry.height / 2;
  950| 
  951|             gdk_device_warp(dev, screen, xr, yr);
  952|             s->last_set = FALSE;
  953|             return FALSE;
  954|         }
  955|     }
  956|     return TRUE;
  957| }
  958| 
  959| static gboolean gd_button_event(GtkWidget *widget, GdkEventButton *button,
  960|                                 void *opaque)
  961| {
  962|     VirtualConsole *vc = opaque;
  963|     GtkDisplayState *s = vc->s;
  964|     InputButton btn;
  965| 
  966|     /* implicitly grab the input at the first click in the relative mode */
  967|     if (button->button == 1 && button->type == GDK_BUTTON_PRESS &&
  968|         !qemu_input_is_absolute() && s->ptr_owner != vc) {
  969|         if (!vc->window) {
  970|             gtk_check_menu_item_set_active(GTK_CHECK_MENU_ITEM(s->grab_item),
  971|                                            TRUE);
  972|         } else {
  973|             gd_grab_pointer(vc, "relative-mode-click");
  974|         }
  975|         return TRUE;
  976|     }
  977| 
  978|     if (button->button == 1) {
  979|         btn = INPUT_BUTTON_LEFT;
  980|     } else if (button->button == 2) {
```

### Turn 4  _(tok 7992+122, stop=tool_use)_

**Reasoning:** gtk.c's 906 and 926 are inside a function that I need to check the beginning of — probably gd_motion_event. Let me check just before line 890. And 968 is inside gd_button_event.

- `read_file(path=ui/gtk.c, start_line=860, end_line=890, version=old)` →

```
ui/gtk.c lines 860-890 of 2531
  860|        behaviour of drawing the rectangle from right to left
  861|        to cut out the whole */
  862|     cairo_rectangle(cr, mx + fbw, my,
  863|                     -1 * fbw, fbh);
  864|     cairo_fill(cr);
  865| 
  866|     cairo_scale(cr, vc->gfx.scale_x, vc->gfx.scale_y);
  867|     cairo_set_source_surface(cr, vc->gfx.surface,
  868|                              mx / vc->gfx.scale_x, my / vc->gfx.scale_y);
  869|     cairo_paint(cr);
  870| 
  871|     return TRUE;
  872| }
  873| 
  874| static gboolean gd_motion_event(GtkWidget *widget, GdkEventMotion *motion,
  875|                                 void *opaque)
  876| {
  877|     VirtualConsole *vc = opaque;
  878|     GtkDisplayState *s = vc->s;
  879|     int x, y;
  880|     int mx, my;
  881|     int fbh, fbw;
  882|     int ww, wh, ws;
  883| 
  884|     if (!vc->gfx.ds) {
  885|         return TRUE;
  886|     }
  887| 
  888|     fbw = surface_width(vc->gfx.ds) * vc->gfx.scale_x;
  889|     fbh = surface_height(vc->gfx.ds) * vc->gfx.scale_y;
  890| 
```

### Turn 5  _(tok 8586+163, stop=tool_use)_

**Reasoning:** GTK.C:
- 207: gd_update_cursor
- 456: gd_mouse_set
- 692: gd_mouse_mode_change
- 906, 926: gd_motion_event
- 968: gd_button_event

Next, at ui/input.c:591 — check the function that contains it.


**Says:** Now ui/input.c:591 and ui/sdl2.c.



- `read_file(path=ui/input.c, start_line=560, end_line=600, version=old)` →

```
ui/input.c lines 560-600 of 663
  560|         .u.mtt.data = &mtt,
  561|     };
  562| 
  563|     qemu_input_event_send(src, &evt);
  564| }
  565| 
  566| void qemu_input_queue_mtt_abs(QemuConsole *src, InputAxis axis, int value,
  567|                               int min_in, int max_in, int slot, int tracking_id)
  568| {
  569|     InputMultiTouchEvent mtt = {
  570|         .type = INPUT_MULTI_TOUCH_TYPE_DATA,
  571|         .slot = slot,
  572|         .tracking_id = tracking_id,
  573|         .axis = axis,
  574|         .value = qemu_input_scale_axis(value, min_in, max_in,
  575|                                        INPUT_EVENT_ABS_MIN,
  576|                                        INPUT_EVENT_ABS_MAX),
  577|     };
  578|     InputEvent evt = {
  579|         .type = INPUT_EVENT_KIND_MTT,
  580|         .u.mtt.data = &mtt,
  581|     };
  582| 
  583|     qemu_input_event_send(src, &evt);
  584| }
  585| 
  586| void qemu_input_check_mode_change(void)
  587| {
  588|     static int current_is_absolute;
  589|     int is_absolute;
  590| 
  591|     is_absolute = qemu_input_is_absolute();
  592| 
  593|     if (is_absolute != current_is_absolute) {
  594|         trace_input_mouse_mode(is_absolute);
  595|         notifier_list_notify(&mouse_mode_notifiers, NULL);
  596|     }
  597| 
  598|     current_is_absolute = is_absolute;
  599| }
  600| 
```

_(budget of 20,000 tokens exhausted — forcing submission)_

