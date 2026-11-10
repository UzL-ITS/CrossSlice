# Impact-analysis transcript — qemu @ 0337e4123e62 — anthropic:claude-haiku-5-5

- target: `qemu_input_is_absolute` (ui/input.c), arity 0->1
- truth: [['ui/cocoa.m', 'cocoa_refresh'], ['ui/dbus-console.c', 'dbus_mouse_rel_motion'], ['ui/dbus-console.c', 'dbus_mouse_set_pos'], ['ui/dbus-console.c', 'dbus_mouse_update_is_absolute'], ['ui/gtk.c', 'gd_button_event'], ['ui/gtk.c', 'gd_motion_event'], ['ui/gtk.c', 'gd_mouse_mode_change'], ['ui/gtk.c', 'gd_mouse_set'], ['ui/gtk.c', 'gd_update_cursor'], ['ui/input.c', 'qemu_input_check_mode_change'], ['ui/sdl2.c', 'handle_mousebutton'], ['ui/sdl2.c', 'handle_mousemotion'], ['ui/sdl2.c', 'handle_windowevent'], ['ui/sdl2.c', 'sdl_grab_start'], ['ui/sdl2.c', 'sdl_hide_cursor'], ['ui/sdl2.c', 'sdl_mouse_define'], ['ui/sdl2.c', 'sdl_mouse_mode_change'], ['ui/sdl2.c', 'sdl_mouse_warp'], ['ui/sdl2.c', 'sdl_send_mouse_event'], ['ui/sdl2.c', 'sdl_show_cursor'], ['ui/spice-input.c', 'mouse_mode_notifier'], ['ui/vnc.c', 'check_pointer_type_change']]

## Self-navigation arm

### Turn 1  _(tok 1218+130, stop=tool_use)_

**Reasoning:** I'm going to search the repo for every use of qemu_input_is_absolute to see where it's referenced.



- `grep(pattern=qemu_input_is_absolute, version=old, max_results=300)` →

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

### Turn 2  _(tok 2410+951, stop=tool_use)_

**Reasoning:** I need to find the function that encloses each of these call sites. I'll read around each line, since there are many files: cocoa.m, dbus-console.c, gtk.c, input.c, sdl2.c, spice-input.c, and vnc.c. I also want to check whether macros or function pointers could hide a caller, though the grep already covers all git-tracked files.

I'll look up the surrounding code for each call site, perhaps by grepping for function definitions rather than reading each file, though reading around the lines seems simpler. I'll issue several reads at once.



**Says:** The grep found 29 matches. Next I need the enclosing function for each call site, so I'll read the surrounding code.

- `read_file(path=ui/cocoa.m, version=old, start_line=1985, end_line=2010)` →

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

- `read_file(path=ui/dbus-console.c, version=old, start_line=375, end_line=525)` →

```
ui/dbus-console.c lines 375-525 of 625
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
```

- `read_file(path=ui/gtk.c, version=old, start_line=195, end_line=215)` →

```
ui/gtk.c lines 195-215 of 2531
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

- `read_file(path=ui/gtk.c, version=old, start_line=440, end_line=470)` →

```
ui/gtk.c lines 440-470 of 2531
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

- `read_file(path=ui/gtk.c, version=old, start_line=680, end_line=700)` →

```
ui/gtk.c lines 680-700 of 2531
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

- `read_file(path=ui/gtk.c, version=old, start_line=895, end_line=975)` →

```
ui/gtk.c lines 895-975 of 2531
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
```

### Turn 3  _(tok 9722+704, stop=tool_use)_

**Reasoning:** I need the name of the function that contains lines 906 and 926, which starts before line 895. My guess is gd_motion_event, so I'll search gtk.c for function definitions near there and read lines 870 to 895 first.



**Says:** I still need the function name for the gtk.c lines 906 and 926, so I'll read above them and also check the other files.

- `read_file(path=ui/gtk.c, version=old, start_line=870, end_line=895)` →

```
ui/gtk.c lines 870-895 of 2531
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
  891|     ww = gtk_widget_get_allocated_width(widget);
  892|     wh = gtk_widget_get_allocated_height(widget);
  893|     ws = gtk_widget_get_scale_factor(widget);
  894| 
  895|     mx = my = 0;
```

- `read_file(path=ui/input.c, version=old, start_line=570, end_line=600)` →

```
ui/input.c lines 570-600 of 663
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

- `read_file(path=ui/spice-input.c, version=old, start_line=215, end_line=235)` →

```
ui/spice-input.c lines 215-235 of 261
  215|     .base.description   = "tablet",
  216|     .base.major_version = SPICE_INTERFACE_TABLET_MAJOR,
  217|     .base.minor_version = SPICE_INTERFACE_TABLET_MINOR,
  218|     .set_logical_size   = tablet_set_logical_size,
  219|     .position           = tablet_position,
  220|     .wheel              = tablet_wheel,
  221|     .buttons            = tablet_buttons,
  222| };
  223| 
  224| static void mouse_mode_notifier(Notifier *notifier, void *data)
  225| {
  226|     QemuSpicePointer *pointer = container_of(notifier, QemuSpicePointer, mouse_mode);
  227|     bool is_absolute  = qemu_input_is_absolute();
  228| 
  229|     if (pointer->absolute == is_absolute) {
  230|         return;
  231|     }
  232| 
  233|     if (is_absolute) {
  234|         qemu_spice.add_interface(&pointer->tablet.base);
  235|     } else {
```

- `read_file(path=ui/vnc.c, version=old, start_line=1760, end_line=1785)` →

```
ui/vnc.c lines 1760-1785 of 4301
 1760| {
 1761|     return (int32_t)((data[offset] << 24) | (data[offset + 1] << 16) |
 1762|                      (data[offset + 2] << 8) | data[offset + 3]);
 1763| }
 1764| 
 1765| uint32_t read_u32(uint8_t *data, size_t offset)
 1766| {
 1767|     return ((data[offset] << 24) | (data[offset + 1] << 16) |
 1768|             (data[offset + 2] << 8) | data[offset + 3]);
 1769| }
 1770| 
 1771| static void check_pointer_type_change(Notifier *notifier, void *data)
 1772| {
 1773|     VncState *vs = container_of(notifier, VncState, mouse_mode_notifier);
 1774|     int absolute = qemu_input_is_absolute();
 1775| 
 1776|     if (vnc_has_feature(vs, VNC_FEATURE_POINTER_TYPE_CHANGE) && vs->absolute != absolute) {
 1777|         vnc_lock_output(vs);
 1778|         vnc_write_u8(vs, VNC_MSG_SERVER_FRAMEBUFFER_UPDATE);
 1779|         vnc_write_u8(vs, 0);
 1780|         vnc_write_u16(vs, 1);
 1781|         vnc_framebuffer_update(vs, absolute, 0,
 1782|                                pixman_image_get_width(vs->vd->server),
 1783|                                pixman_image_get_height(vs->vd->server),
 1784|                                VNC_ENCODING_POINTER_TYPE_CHANGE);
 1785|         vnc_unlock_output(vs);
```

- `read_file(path=ui/sdl2.c, version=old, start_line=190, end_line=330)` →

```
ui/sdl2.c lines 190-330 of 974
  190|     }
  191| 
  192|     if (scon->real_window) {
  193|         SDL_SetWindowTitle(scon->real_window, win_title);
  194|     }
  195| }
  196| 
  197| static void sdl_hide_cursor(struct sdl2_console *scon)
  198| {
  199|     if (scon->opts->has_show_cursor && scon->opts->show_cursor) {
  200|         return;
  201|     }
  202| 
  203|     SDL_ShowCursor(SDL_DISABLE);
  204|     SDL_SetCursor(sdl_cursor_hidden);
  205| 
  206|     if (!qemu_input_is_absolute()) {
  207|         SDL_SetRelativeMouseMode(SDL_TRUE);
  208|     }
  209| }
  210| 
  211| static void sdl_show_cursor(struct sdl2_console *scon)
  212| {
  213|     if (scon->opts->has_show_cursor && scon->opts->show_cursor) {
  214|         return;
  215|     }
  216| 
  217|     if (!qemu_input_is_absolute()) {
  218|         SDL_SetRelativeMouseMode(SDL_FALSE);
  219|     }
  220| 
  221|     if (guest_cursor &&
  222|         (gui_grab || qemu_input_is_absolute() || absolute_enabled)) {
  223|         SDL_SetCursor(guest_sprite);
  224|     } else {
  225|         SDL_SetCursor(sdl_cursor_normal);
  226|     }
  227| 
  228|     SDL_ShowCursor(SDL_ENABLE);
  229| }
  230| 
  231| static void sdl_grab_start(struct sdl2_console *scon)
  232| {
  233|     QemuConsole *con = scon ? scon->dcl.con : NULL;
  234| 
  235|     if (!con || !qemu_console_is_graphic(con)) {
  236|         return;
  237|     }
  238|     /*
  239|      * If the application is not active, do not try to enter grab state. This
  240|      * prevents 'SDL_WM_GrabInput(SDL_GRAB_ON)' from blocking all the
  241|      * application (SDL bug).
  242|      */
  243|     if (!(SDL_GetWindowFlags(scon->real_window) & SDL_WINDOW_INPUT_FOCUS)) {
  244|         return;
  245|     }
  246|     if (guest_cursor) {
  247|         SDL_SetCursor(guest_sprite);
  248|         if (!qemu_input_is_absolute() && !absolute_enabled) {
  249|             SDL_WarpMouseInWindow(scon->real_window, guest_x, guest_y);
  250|         }
  251|     } else {
  252|         sdl_hide_cursor(scon);
  253|     }
  254|     SDL_SetWindowGrab(scon->real_window, SDL_TRUE);
  255|     gui_grab = 1;
  256|     win32_kbd_set_grab(true);
  257|     sdl_update_caption(scon);
  258| }
  259| 
  260| static void sdl_grab_end(struct sdl2_console *scon)
  261| {
  262|     SDL_SetWindowGrab(scon->real_window, SDL_FALSE);
  263|     gui_grab = 0;
  264|     win32_kbd_set_grab(false);
  265|     sdl_show_cursor(scon);
  266|     sdl_update_caption(scon);
  267| }
  268| 
  269| static void absolute_mouse_grab(struct sdl2_console *scon)
  270| {
  271|     int mouse_x, mouse_y;
  272|     int scr_w, scr_h;
  273|     SDL_GetMouseState(&mouse_x, &mouse_y);
  274|     SDL_GetWindowSize(scon->real_window, &scr_w, &scr_h);
  275|     if (mouse_x > 0 && mouse_x < scr_w - 1 &&
  276|         mouse_y > 0 && mouse_y < scr_h - 1) {
  277|         sdl_grab_start(scon);
  278|     }
  279| }
  280| 
  281| static void sdl_mouse_mode_change(Notifier *notify, void *data)
  282| {
  283|     if (qemu_input_is_absolute()) {
  284|         if (!absolute_enabled) {
  285|             absolute_enabled = 1;
  286|             SDL_SetRelativeMouseMode(SDL_FALSE);
  287|             absolute_mouse_grab(&sdl2_console[0]);
  288|         }
  289|     } else if (absolute_enabled) {
  290|         if (!gui_fullscreen) {
  291|             sdl_grab_end(&sdl2_console[0]);
  292|         }
  293|         absolute_enabled = 0;
  294|     }
  295| }
  296| 
  297| static void sdl_send_mouse_event(struct sdl2_console *scon, int dx, int dy,
  298|                                  int x, int y, int state)
  299| {
  300|     static uint32_t bmap[INPUT_BUTTON__MAX] = {
  301|         [INPUT_BUTTON_LEFT]       = SDL_BUTTON(SDL_BUTTON_LEFT),
  302|         [INPUT_BUTTON_MIDDLE]     = SDL_BUTTON(SDL_BUTTON_MIDDLE),
  303|         [INPUT_BUTTON_RIGHT]      = SDL_BUTTON(SDL_BUTTON_RIGHT),
  304|         [INPUT_BUTTON_SIDE]       = SDL_BUTTON(SDL_BUTTON_X1),
  305|         [INPUT_BUTTON_EXTRA]      = SDL_BUTTON(SDL_BUTTON_X2)
  306|     };
  307|     static uint32_t prev_state;
  308| 
  309|     if (prev_state != state) {
  310|         qemu_input_update_buttons(scon->dcl.con, bmap, prev_state, state);
  311|         prev_state = state;
  312|     }
  313| 
  314|     if (qemu_input_is_absolute()) {
  315|         qemu_input_queue_abs(scon->dcl.con, INPUT_AXIS_X,
  316|                              x, 0, surface_width(scon->surface));
  317|         qemu_input_queue_abs(scon->dcl.con, INPUT_AXIS_Y,
  318|                              y, 0, surface_height(scon->surface));
  319|     } else {
  320|         if (guest_cursor) {
  321|             x -= guest_x;
  322|             y -= guest_y;
  323|             guest_x += x;
  324|             guest_y += y;
  325|             dx = x;
  326|             dy = y;
  327|         }
  328|         qemu_input_queue_rel(scon->dcl.con, INPUT_AXIS_X, dx);
  329|         qemu_input_queue_rel(scon->dcl.con, INPUT_AXIS_Y, dy);
  330|     }
```

### Turn 4  _(tok 14962+241, stop=tool_use)_

- `read_file(path=ui/sdl2.c, version=old, start_line=490, end_line=620)` →

```
ui/sdl2.c lines 490-620 of 974
  490| 
  491| static void handle_mousemotion(SDL_Event *ev)
  492| {
  493|     int max_x, max_y;
  494|     struct sdl2_console *scon = get_scon_from_window(ev->motion.windowID);
  495| 
  496|     if (!scon || !qemu_console_is_graphic(scon->dcl.con)) {
  497|         return;
  498|     }
  499| 
  500|     if (qemu_input_is_absolute() || absolute_enabled) {
  501|         int scr_w, scr_h;
  502|         SDL_GetWindowSize(scon->real_window, &scr_w, &scr_h);
  503|         max_x = scr_w - 1;
  504|         max_y = scr_h - 1;
  505|         if (gui_grab && !gui_fullscreen
  506|             && (ev->motion.x == 0 || ev->motion.y == 0 ||
  507|                 ev->motion.x == max_x || ev->motion.y == max_y)) {
  508|             sdl_grab_end(scon);
  509|         }
  510|         if (!gui_grab &&
  511|             (ev->motion.x > 0 && ev->motion.x < max_x &&
  512|              ev->motion.y > 0 && ev->motion.y < max_y)) {
  513|             sdl_grab_start(scon);
  514|         }
  515|     }
  516|     if (gui_grab || qemu_input_is_absolute() || absolute_enabled) {
  517|         sdl_send_mouse_event(scon, ev->motion.xrel, ev->motion.yrel,
  518|                              ev->motion.x, ev->motion.y, ev->motion.state);
  519|     }
  520| }
  521| 
  522| static void handle_mousebutton(SDL_Event *ev)
  523| {
  524|     int buttonstate = SDL_GetMouseState(NULL, NULL);
  525|     SDL_MouseButtonEvent *bev;
  526|     struct sdl2_console *scon = get_scon_from_window(ev->button.windowID);
  527| 
  528|     if (!scon || !qemu_console_is_graphic(scon->dcl.con)) {
  529|         return;
  530|     }
  531| 
  532|     bev = &ev->button;
  533|     if (!gui_grab && !qemu_input_is_absolute()) {
  534|         if (ev->type == SDL_MOUSEBUTTONUP && bev->button == SDL_BUTTON_LEFT) {
  535|             /* start grabbing all events */
  536|             sdl_grab_start(scon);
  537|         }
  538|     } else {
  539|         if (ev->type == SDL_MOUSEBUTTONDOWN) {
  540|             buttonstate |= SDL_BUTTON(bev->button);
  541|         } else {
  542|             buttonstate &= ~SDL_BUTTON(bev->button);
  543|         }
  544|         sdl_send_mouse_event(scon, 0, 0, bev->x, bev->y, buttonstate);
  545|     }
  546| }
  547| 
  548| static void handle_mousewheel(SDL_Event *ev)
  549| {
  550|     struct sdl2_console *scon = get_scon_from_window(ev->wheel.windowID);
  551|     SDL_MouseWheelEvent *wev = &ev->wheel;
  552|     InputButton btn;
  553| 
  554|     if (!scon || !qemu_console_is_graphic(scon->dcl.con)) {
  555|         return;
  556|     }
  557| 
  558|     if (wev->y > 0) {
  559|         btn = INPUT_BUTTON_WHEEL_UP;
  560|     } else if (wev->y < 0) {
  561|         btn = INPUT_BUTTON_WHEEL_DOWN;
  562|     } else if (wev->x < 0) {
  563|         btn = INPUT_BUTTON_WHEEL_RIGHT;
  564|     } else if (wev->x > 0) {
  565|         btn = INPUT_BUTTON_WHEEL_LEFT;
  566|     } else {
  567|         return;
  568|     }
  569| 
  570|     qemu_input_queue_btn(scon->dcl.con, btn, true);
  571|     qemu_input_event_sync();
  572|     qemu_input_queue_btn(scon->dcl.con, btn, false);
  573|     qemu_input_event_sync();
  574| }
  575| 
  576| static void handle_windowevent(SDL_Event *ev)
  577| {
  578|     struct sdl2_console *scon = get_scon_from_window(ev->window.windowID);
  579|     bool allow_close = true;
  580| 
  581|     if (!scon) {
  582|         return;
  583|     }
  584| 
  585|     switch (ev->window.event) {
  586|     case SDL_WINDOWEVENT_RESIZED:
  587|         {
  588|             QemuUIInfo info;
  589|             memset(&info, 0, sizeof(info));
  590|             info.width = ev->window.data1;
  591|             info.height = ev->window.data2;
  592|             dpy_set_ui_info(scon->dcl.con, &info, true);
  593|         }
  594|         sdl2_redraw(scon);
  595|         break;
  596|     case SDL_WINDOWEVENT_EXPOSED:
  597|         sdl2_redraw(scon);
  598|         break;
  599|     case SDL_WINDOWEVENT_FOCUS_GAINED:
  600|         win32_kbd_set_grab(gui_grab);
  601|         if (qemu_console_is_graphic(scon->dcl.con)) {
  602|             win32_kbd_set_window(sdl2_win32_get_hwnd(scon));
  603|         }
  604|         /* fall through */
  605|     case SDL_WINDOWEVENT_ENTER:
  606|         if (!gui_grab && (qemu_input_is_absolute() || absolute_enabled)) {
  607|             absolute_mouse_grab(scon);
  608|         }
  609|         /* If a new console window opened using a hotkey receives the
  610|          * focus, SDL sends another KEYDOWN event to the new window,
  611|          * closing the console window immediately after.
  612|          *
  613|          * Work around this by ignoring further hotkey events until a
  614|          * key is released.
  615|          */
  616|         scon->ignore_hotkeys = get_mod_state();
  617|         break;
  618|     case SDL_WINDOWEVENT_FOCUS_LOST:
  619|         if (qemu_console_is_graphic(scon->dcl.con)) {
  620|             win32_kbd_set_window(NULL);
```

- `read_file(path=ui/sdl2.c, version=old, start_line=715, end_line=785)` →

```
ui/sdl2.c lines 715-785 of 974
  715|             }
  716|         }
  717|     } else {
  718|         scon->idle_counter = 0;
  719|         scon->dcl.update_interval = SDL2_REFRESH_INTERVAL_BUSY;
  720|     }
  721| }
  722| 
  723| static void sdl_mouse_warp(DisplayChangeListener *dcl,
  724|                            int x, int y, int on)
  725| {
  726|     struct sdl2_console *scon = container_of(dcl, struct sdl2_console, dcl);
  727| 
  728|     if (!qemu_console_is_graphic(scon->dcl.con)) {
  729|         return;
  730|     }
  731| 
  732|     if (on) {
  733|         if (!guest_cursor) {
  734|             sdl_show_cursor(scon);
  735|         }
  736|         if (gui_grab || qemu_input_is_absolute() || absolute_enabled) {
  737|             SDL_SetCursor(guest_sprite);
  738|             if (!qemu_input_is_absolute() && !absolute_enabled) {
  739|                 SDL_WarpMouseInWindow(scon->real_window, x, y);
  740|             }
  741|         }
  742|     } else if (gui_grab) {
  743|         sdl_hide_cursor(scon);
  744|     }
  745|     guest_cursor = on;
  746|     guest_x = x, guest_y = y;
  747| }
  748| 
  749| static void sdl_mouse_define(DisplayChangeListener *dcl,
  750|                              QEMUCursor *c)
  751| {
  752| 
  753|     if (guest_sprite) {
  754|         SDL_FreeCursor(guest_sprite);
  755|     }
  756| 
  757|     if (guest_sprite_surface) {
  758|         SDL_FreeSurface(guest_sprite_surface);
  759|     }
  760| 
  761|     guest_sprite_surface =
  762|         SDL_CreateRGBSurfaceFrom(c->data, c->width, c->height, 32, c->width * 4,
  763|                                  0xff0000, 0x00ff00, 0xff, 0xff000000);
  764| 
  765|     if (!guest_sprite_surface) {
  766|         fprintf(stderr, "Failed to make rgb surface from %p\n", c);
  767|         return;
  768|     }
  769|     guest_sprite = SDL_CreateColorCursor(guest_sprite_surface,
  770|                                          c->hot_x, c->hot_y);
  771|     if (!guest_sprite) {
  772|         fprintf(stderr, "Failed to make color cursor from %p\n", c);
  773|         return;
  774|     }
  775|     if (guest_cursor &&
  776|         (gui_grab || qemu_input_is_absolute() || absolute_enabled)) {
  777|         SDL_SetCursor(guest_sprite);
  778|     }
  779| }
  780| 
  781| static void sdl_cleanup(void)
  782| {
  783|     if (guest_sprite) {
  784|         SDL_FreeCursor(guest_sprite);
  785|     }
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 18899+706, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "cocoa_refresh", "file": "ui/cocoa.m"}, {"function": "dbus_mouse_rel_motion", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_set_pos", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_update_is_absolute", "file": "ui/dbus-console.c"}, {"function": "gd_update_cursor", "file": "ui/gtk.c"}, {"function": "gd_mouse_set", "file": "ui/gtk.c"}, {"function": "gd_mouse_mode_change", "file": "ui/gtk.c"}, {"function": "gd_motion_event", "file": "ui/gtk.c"}, {"function": "gd_button_event", "file": "ui/gtk.c"}, {"function": "qemu_input_check_mode_change", "file": "ui/input.c"}, {"function": "mouse_mode_notifier", "file": "ui/spice-input.c"}, {"function": "check_pointer_type_change", "file": "ui/vnc.c"}, {"function": "sdl_hide_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_show_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_grab_start", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_mode_change", "file": "ui/sdl2.c"}, {"function": "sdl_send_mouse_event", "file": "ui/sdl2.c"}, {"function": "handle_mousemotion", "file": "ui/sdl2.c"}, {"function": "handle_mousebutton", "file": "ui/sdl2.c"}, {"function": "handle_windowevent", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_warp", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_define", "file": "ui/sdl2.c"}], "confidence_overall": "medium"}`

**Score (self):** `{"n_pred": 22, "n_truth": 22, "tp": 22, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1387+158, stop=tool_use)_

**Reasoning:** I'm going to start by calling find_references on qemu_input_is_absolute to see where it's used.



- `find_references(name=qemu_input_is_absolute)` →

```
26 references
qemu_input_is_absolute   60 include/ui/input.h bool qemu_input_is_absolute(void);
qemu_input_is_absolute  389 ui/dbus-console.c     if (qemu_input_is_absolute()) {
qemu_input_is_absolute  456 ui/dbus-console.c     if (!qemu_input_is_absolute()) {
qemu_input_is_absolute  517 ui/dbus-console.c                  "is-absolute", qemu_input_is_absolute(),
qemu_input_is_absolute  207 ui/gtk.c             if (s->full_screen || qemu_input_is_absolute() || s->ptr_owner == vc) {
qemu_input_is_absolute  456 ui/gtk.c                 qemu_input_is_absolute()) {
qemu_input_is_absolute  692 ui/gtk.c             if (qemu_input_is_absolute() && s->ptr_owner) {
qemu_input_is_absolute  906 ui/gtk.c             if (qemu_input_is_absolute()) {
qemu_input_is_absolute  926 ui/gtk.c             if (!qemu_input_is_absolute() && s->ptr_owner == vc) {
qemu_input_is_absolute  968 ui/gtk.c                 !qemu_input_is_absolute() && s->ptr_owner != vc) {
qemu_input_is_absolute  591 ui/input.c           is_absolute = qemu_input_is_absolute();
qemu_input_is_absolute  206 ui/sdl2.c            if (!qemu_input_is_absolute()) {
qemu_input_is_absolute  217 ui/sdl2.c            if (!qemu_input_is_absolute()) {
qemu_input_is_absolute  222 ui/sdl2.c                (gui_grab || qemu_input_is_absolute() || absolute_enabled)) {
qemu_input_is_absolute  248 ui/sdl2.c                if (!qemu_input_is_absolute() && !absolute_enabled) {
qemu_input_is_absolute  283 ui/sdl2.c            if (qemu_input_is_absolute()) {
qemu_input_is_absolute  314 ui/sdl2.c            if (qemu_input_is_absolute()) {
qemu_input_is_absolute  500 ui/sdl2.c            if (qemu_input_is_absolute() || absolute_enabled) {
qemu_input_is_absolute  516 ui/sdl2.c            if (gui_grab || qemu_input_is_absolute() || absolute_enabled) {
qemu_input_is_absolute  533 ui/sdl2.c            if (!gui_grab && !qemu_input_is_absolute()) {
qemu_input_is_absolute  606 ui/sdl2.c                if (!gui_grab && (qemu_input_is_absolute() || absolute_enabled)) {
qemu_input_is_absolute  736 ui/sdl2.c                if (gui_grab || qemu_input_is_absolute() || absolute_enabled) {
qemu_input_is_absolute  738 ui/sdl2.c                    if (!qemu_input_is_absolute() && !absolute_enabled) {
qemu_input_is_absolute  776 ui/sdl2.c                (gui_grab || qemu_input_is_absolute() || absolute_enabled)) {
qemu_input_is_absolute  227 ui/spice-input.c     bool is_absolute  = qemu_input_is_absolute();
qemu_input_is_absolute 1774 ui/vnc.c             int absolute = qemu_input_is_absolute();
```

- `grep(pattern=qemu_input_is_absolute, version=old)` →

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

### Turn 2  _(tok 3896+1245, stop=tool_use)_

**Reasoning:** The grep turned up cocoa.m, which find_references had missed. Next I need the enclosing function for each hit, so I'll read the code around every listed line across the affected files.

I'm grepping each file for lines that look like function headers, so I can map the flagged lines to the functions that contain them.



**Says:** The grep found a `ui/cocoa.m` call that the GNU Global index missed. To map each call to its enclosing function, I'll pull the top-level function headers from every file that has a call.

- `grep(pattern=^[A-Za-z_].*\(, path_glob=ui/cocoa.m, version=old, max_results=400)` →

```
28 matches
ui/cocoa.m:84:static void cocoa_update(DisplayChangeListener *dcl,
ui/cocoa.m:87:static void cocoa_switch(DisplayChangeListener *dcl,
ui/cocoa.m:90:static void cocoa_refresh(DisplayChangeListener *dcl);
ui/cocoa.m:117:typedef void (^CodeBlock)(void);
ui/cocoa.m:118:typedef bool (^BoolCodeBlock)(void);
ui/cocoa.m:120:static void with_iothread_lock(CodeBlock block)
ui/cocoa.m:132:static bool bool_with_iothread_lock(BoolCodeBlock block)
ui/cocoa.m:272:static int cocoa_keycode_to_qemu(int keycode)
ui/cocoa.m:282:static void QEMU_Alert(NSString *message)
ui/cocoa.m:291:static void handleAnyDeviceErrors(Error * err)
ui/cocoa.m:344:static CGEventRef handleTapEvent(CGEventTapProxy proxy, CGEventType type, CGEventRef cgEvent, void *userInfo)
ui/cocoa.m:1630:static void create_initial_menus(void)
ui/cocoa.m:1722:static NSString * getConsoleName(QemuConsole * console)
ui/cocoa.m:1730:static void add_console_menu_entries(void)
ui/cocoa.m:1752:static void addRemovableDevicesMenuItems(void)
ui/cocoa.m:1849:static void cocoa_clipboard_notify(Notifier *notifier, void *data);
ui/cocoa.m:1850:static void cocoa_clipboard_request(QemuClipboardInfo *info,
ui/cocoa.m:1859:static void cocoa_clipboard_update_info(QemuClipboardInfo *info)
ui/cocoa.m:1876:static void cocoa_clipboard_notify(Notifier *notifier, void *data)
ui/cocoa.m:1890:static void cocoa_clipboard_request(QemuClipboardInfo *info,
ui/cocoa.m:1924:static void *call_qemu_main(void *opaque)
ui/cocoa.m:1937:static int cocoa_main(void)
ui/cocoa.m:1958:static void cocoa_update(DisplayChangeListener *dcl,
ui/cocoa.m:1978:static void cocoa_switch(DisplayChangeListener *dcl,
ui/cocoa.m:1997:static void cocoa_refresh(DisplayChangeListener *dcl)
ui/cocoa.m:2029:static void cocoa_display_init(DisplayState *ds, DisplayOptions *opts)
ui/cocoa.m:2095:static void register_cocoa(void)
ui/cocoa.m:2100:type_init(register_cocoa);
```

- `grep(pattern=^[A-Za-z_].*\(, path_glob=ui/dbus-console.c, version=old, max_results=400)` →

```
27 matches
ui/dbus-console.c:58:G_DEFINE_TYPE(DBusDisplayConsole,
ui/dbus-console.c:63:dbus_display_console_set_size(DBusDisplayConsole *ddc,
ui/dbus-console.c:73:dbus_gfx_switch(DisplayChangeListener *dcl,
ui/dbus-console.c:84:dbus_gfx_update(DisplayChangeListener *dcl,
ui/dbus-console.c:90:dbus_gl_scanout_disable(DisplayChangeListener *dcl)
ui/dbus-console.c:95:dbus_gl_scanout_texture(DisplayChangeListener *dcl,
ui/dbus-console.c:110:dbus_gl_scanout_dmabuf(DisplayChangeListener *dcl,
ui/dbus-console.c:121:dbus_gl_scanout_update(DisplayChangeListener *dcl,
ui/dbus-console.c:138:dbus_display_console_init(DBusDisplayConsole *object)
ui/dbus-console.c:148:dbus_display_console_dispose(GObject *object)
ui/dbus-console.c:164:dbus_display_console_class_init(DBusDisplayConsoleClass *klass)
ui/dbus-console.c:172:listener_vanished_cb(DBusDisplayListener *listener)
ui/dbus-console.c:184:dbus_console_set_ui_info(DBusDisplayConsole *ddc,
ui/dbus-console.c:217:dbus_win32_import_socket(GDBusMethodInvocation *invocation,
ui/dbus-console.c:251:dbus_console_register_listener(DBusDisplayConsole *ddc,
ui/dbus-console.c:343:dbus_kbd_press(DBusDisplayConsole *ddc,
ui/dbus-console.c:359:dbus_kbd_release(DBusDisplayConsole *ddc,
ui/dbus-console.c:375:dbus_kbd_qemu_leds_updated(void *data, int ledstate)
ui/dbus-console.c:383:dbus_mouse_rel_motion(DBusDisplayConsole *ddc,
ui/dbus-console.c:408:dbus_touch_send_event(DBusDisplayConsole *ddc,
ui/dbus-console.c:448:dbus_mouse_set_pos(DBusDisplayConsole *ddc,
ui/dbus-console.c:484:dbus_mouse_press(DBusDisplayConsole *ddc,
ui/dbus-console.c:499:dbus_mouse_release(DBusDisplayConsole *ddc,
ui/dbus-console.c:514:dbus_mouse_update_is_absolute(DBusDisplayConsole *ddc)
ui/dbus-console.c:522:dbus_mouse_mode_change(Notifier *notify, void *data)
ui/dbus-console.c:530:int dbus_display_console_get_index(DBusDisplayConsole *ddc)
ui/dbus-console.c:536:dbus_display_console_new(DBusDisplay *display, QemuConsole *con)
```

- `grep(pattern=^[A-Za-z_].*\(, path_glob=ui/gtk.c, version=old, max_results=400)` →

```
104 matches
ui/gtk.c:130:DECLARE_INSTANCE_CHECKER(VCChardev, VC_CHARDEV,
ui/gtk.c:137:static void gd_grab_pointer(VirtualConsole *vc, const char *reason);
ui/gtk.c:138:static void gd_ungrab_pointer(GtkDisplayState *s);
ui/gtk.c:139:static void gd_grab_keyboard(VirtualConsole *vc, const char *reason);
ui/gtk.c:140:static void gd_ungrab_keyboard(GtkDisplayState *s);
ui/gtk.c:144:static VirtualConsole *gd_vc_find_by_menu(GtkDisplayState *s)
ui/gtk.c:159:static VirtualConsole *gd_vc_find_by_page(GtkDisplayState *s, gint page)
ui/gtk.c:174:static VirtualConsole *gd_vc_find_current(GtkDisplayState *s)
ui/gtk.c:182:static bool gd_is_grab_active(GtkDisplayState *s)
ui/gtk.c:187:static bool gd_grab_on_hover(GtkDisplayState *s)
ui/gtk.c:192:static void gd_update_cursor(VirtualConsole *vc)
ui/gtk.c:214:static void gd_update_caption(GtkDisplayState *s)
ui/gtk.c:262:static void gd_update_geometry_hints(VirtualConsole *vc)
ui/gtk.c:329:void gd_update_windowsize(VirtualConsole *vc)
ui/gtk.c:341:static void gd_update_full_redraw(VirtualConsole *vc)
ui/gtk.c:356:static void gtk_release_modifiers(GtkDisplayState *s)
ui/gtk.c:367:static void gd_widget_reparent(GtkWidget *from, GtkWidget *to,
ui/gtk.c:376:static void *gd_win32_get_hwnd(VirtualConsole *vc)
ui/gtk.c:388:static void gd_update(DisplayChangeListener *dcl,
ui/gtk.c:438:static void gd_refresh(DisplayChangeListener *dcl)
ui/gtk.c:443:static GdkDevice *gd_get_pointer(GdkDisplay *dpy)
ui/gtk.c:448:static void gd_mouse_set(DisplayChangeListener *dcl,
ui/gtk.c:470:static void gd_cursor_define(DisplayChangeListener *dcl,
ui/gtk.c:493:static void gd_switch(DisplayChangeListener *dcl,
ui/gtk.c:569:static bool gd_has_dmabuf(DisplayChangeListener *dcl)
ui/gtk.c:582:static void gd_gl_release_dmabuf(DisplayChangeListener *dcl,
ui/gtk.c:595:void gd_hw_gl_flushed(void *vcon)
ui/gtk.c:626:gd_gl_area_is_compatible_dcl(DisplayGLCtx *dgc,
ui/gtk.c:660:gd_egl_is_compatible_dcl(DisplayGLCtx *dgc,
ui/gtk.c:678:static void gd_change_runstate(void *opaque, bool running, RunState state)
ui/gtk.c:685:static void gd_mouse_mode_change(Notifier *notify, void *data)
ui/gtk.c:708:static gboolean gd_window_close(GtkWidget *widget, GdkEvent *event,
ui/gtk.c:725:static void gd_set_ui_refresh_rate(VirtualConsole *vc, int refresh_rate)
ui/gtk.c:734:static void gd_set_ui_size(VirtualConsole *vc, gint width, gint height)
ui/gtk.c:746:static gboolean gd_render_event(GtkGLArea *area, GdkGLContext *context,
ui/gtk.c:757:static void gd_resize_event(GtkGLArea *area,
ui/gtk.c:767:void gd_update_monitor_refresh_rate(VirtualConsole *vc, GtkWidget *widget)
ui/gtk.c:790:static gboolean gd_draw_event(GtkWidget *widget, cairo_t *cr, void *opaque)
ui/gtk.c:874:static gboolean gd_motion_event(GtkWidget *widget, GdkEventMotion *motion,
ui/gtk.c:959:static gboolean gd_button_event(GtkWidget *widget, GdkEventButton *button,
ui/gtk.c:1002:static gboolean gd_scroll_event(GtkWidget *widget, GdkEventScroll *scroll,
ui/gtk.c:1067:static gboolean gd_touch_event(GtkWidget *widget, GdkEventTouch *touch,
ui/gtk.c:1097:static const guint16 *gd_get_keymap(size_t *maplen)
ui/gtk.c:1155:static int gd_map_keycode(int scancode)
ui/gtk.c:1167:static int gd_get_keycode(GdkEventKey *key)
ui/gtk.c:1186:static gboolean gd_text_key_down(GtkWidget *widget,
ui/gtk.c:1203:static gboolean gd_key_event(GtkWidget *widget, GdkEventKey *key, void *opaque)
ui/gtk.c:1246:static gboolean gd_grab_broken_event(GtkWidget *widget,
ui/gtk.c:1265:static gboolean gd_event(GtkWidget *widget, GdkEvent *event, void *opaque)
ui/gtk.c:1275:static void gd_menu_pause(GtkMenuItem *item, void *opaque)
ui/gtk.c:1289:static void gd_menu_reset(GtkMenuItem *item, void *opaque)
ui/gtk.c:1294:static void gd_menu_powerdown(GtkMenuItem *item, void *opaque)
ui/gtk.c:1299:static void gd_menu_quit(GtkMenuItem *item, void *opaque)
ui/gtk.c:1304:static void gd_menu_switch_vc(GtkMenuItem *item, void *opaque)
ui/gtk.c:1319:static void gd_accel_switch_vc(void *opaque)
ui/gtk.c:1326:static void gd_menu_show_tabs(GtkMenuItem *item, void *opaque)
ui/gtk.c:1339:static gboolean gd_tab_window_close(GtkWidget *widget, GdkEvent *event,
ui/gtk.c:1364:static gboolean gd_win_grab(void *opaque)
ui/gtk.c:1377:static void gd_menu_untabify(GtkMenuItem *item, void *opaque)
ui/gtk.c:1420:static void gd_menu_show_menubar(GtkMenuItem *item, void *opaque)
ui/gtk.c:1438:static void gd_accel_show_menubar(void *opaque)
ui/gtk.c:1444:static void gd_menu_full_screen(GtkMenuItem *item, void *opaque)
ui/gtk.c:1475:static void gd_accel_full_screen(void *opaque)
ui/gtk.c:1481:static void gd_menu_zoom_in(GtkMenuItem *item, void *opaque)
ui/gtk.c:1495:static void gd_accel_zoom_in(void *opaque)
ui/gtk.c:1501:static void gd_menu_zoom_out(GtkMenuItem *item, void *opaque)
ui/gtk.c:1518:static void gd_menu_zoom_fixed(GtkMenuItem *item, void *opaque)
ui/gtk.c:1529:static void gd_menu_zoom_fit(GtkMenuItem *item, void *opaque)
ui/gtk.c:1546:static void gd_grab_update(VirtualConsole *vc, bool kbd, bool ptr)
ui/gtk.c:1570:static void gd_grab_keyboard(VirtualConsole *vc, const char *reason)
ui/gtk.c:1587:static void gd_ungrab_keyboard(GtkDisplayState *s)
ui/gtk.c:1602:static void gd_grab_pointer(VirtualConsole *vc, const char *reason)
ui/gtk.c:1622:static void gd_ungrab_pointer(GtkDisplayState *s)
ui/gtk.c:1641:static void gd_menu_grab_input(GtkMenuItem *item, void *opaque)
ui/gtk.c:1657:static void gd_change_page(GtkNotebook *nb, gpointer arg1, guint arg2,
ui/gtk.c:1692:static gboolean gd_enter_event(GtkWidget *widget, GdkEventCrossing *crossing,
ui/gtk.c:1704:static gboolean gd_leave_event(GtkWidget *widget, GdkEventCrossing *crossing,
ui/gtk.c:1716:static gboolean gd_focus_in_event(GtkWidget *widget,
ui/gtk.c:1725:static gboolean gd_focus_out_event(GtkWidget *widget,
ui/gtk.c:1736:static gboolean gd_configure(GtkWidget *widget,
ui/gtk.c:1747:static GSList *gd_vc_menu_init(GtkDisplayState *s, VirtualConsole *vc,
ui/gtk.c:1766:static void gd_menu_copy(GtkMenuItem *item, void *opaque)
ui/gtk.c:1779:static void gd_vc_adjustment_changed(GtkAdjustment *adjustment, void *opaque)
ui/gtk.c:1791:static void gd_vc_send_chars(VirtualConsole *vc)
ui/gtk.c:1808:static int gd_vc_chr_write(Chardev *chr, const uint8_t *buf, int len)
ui/gtk.c:1817:static void gd_vc_chr_accept_input(Chardev *chr)
ui/gtk.c:1827:static void gd_vc_chr_set_echo(Chardev *chr, bool echo)
ui/gtk.c:1841:static void gd_vc_open(Chardev *chr,
ui/gtk.c:1859:static void char_gd_vc_class_init(ObjectClass *oc, void *data)
ui/gtk.c:1876:static gboolean gd_vc_in(VteTerminal *terminal, gchar *text, guint size,
ui/gtk.c:1907:static GSList *gd_vc_vte_init(GtkDisplayState *s, VirtualConsole *vc,
ui/gtk.c:1976:static void gd_vcs_init(GtkDisplayState *s, GSList *group,
ui/gtk.c:1991:static void gd_connect_vc_gfx_signals(VirtualConsole *vc)
ui/gtk.c:2038:static void gd_connect_signals(GtkDisplayState *s)
ui/gtk.c:2078:static GtkWidget *gd_create_menu_machine(GtkDisplayState *s)
ui/gtk.c:2112:static void gl_area_realize(GtkGLArea *area, VirtualConsole *vc)
ui/gtk.c:2123:static GSList *gd_vc_gfx_init(GtkDisplayState *s, VirtualConsole *vc,
ui/gtk.c:2220:static GtkWidget *gd_create_menu_view(GtkDisplayState *s, DisplayOptions *opts)
ui/gtk.c:2330:static void gd_create_menus(GtkDisplayState *s, DisplayOptions *opts)
ui/gtk.c:2358:static void gtk_display_init(DisplayState *ds, DisplayOptions *opts)
ui/gtk.c:2458:static void early_gtk_display_init(DisplayOptions *opts)
ui/gtk.c:2521:static void register_gtk(void)
ui/gtk.c:2526:type_init(register_gtk);
ui/gtk.c:2529:module_dep("ui-opengl");
```

- `grep(pattern=^[A-Za-z_].*\(, path_glob=ui/sdl2.c, version=old, max_results=400)` →

```
34 matches
ui/sdl2.c:66:static void sdl_update_caption(struct sdl2_console *scon);
ui/sdl2.c:68:static struct sdl2_console *get_scon_from_window(uint32_t window_id)
ui/sdl2.c:79:void sdl2_window_create(struct sdl2_console *scon)
ui/sdl2.c:125:void sdl2_window_destroy(struct sdl2_console *scon)
ui/sdl2.c:143:void sdl2_window_resize(struct sdl2_console *scon)
ui/sdl2.c:154:static void sdl2_redraw(struct sdl2_console *scon)
ui/sdl2.c:165:static void sdl_update_caption(struct sdl2_console *scon)
ui/sdl2.c:197:static void sdl_hide_cursor(struct sdl2_console *scon)
ui/sdl2.c:211:static void sdl_show_cursor(struct sdl2_console *scon)
ui/sdl2.c:231:static void sdl_grab_start(struct sdl2_console *scon)
ui/sdl2.c:260:static void sdl_grab_end(struct sdl2_console *scon)
ui/sdl2.c:269:static void absolute_mouse_grab(struct sdl2_console *scon)
ui/sdl2.c:281:static void sdl_mouse_mode_change(Notifier *notify, void *data)
ui/sdl2.c:297:static void sdl_send_mouse_event(struct sdl2_console *scon, int dx, int dy,
ui/sdl2.c:334:static void toggle_full_screen(struct sdl2_console *scon)
ui/sdl2.c:351:static int get_mod_state(void)
ui/sdl2.c:365:static void *sdl2_win32_get_hwnd(struct sdl2_console *scon)
ui/sdl2.c:378:static void handle_keydown(SDL_Event *ev)
ui/sdl2.c:465:static void handle_keyup(SDL_Event *ev)
ui/sdl2.c:477:static void handle_textinput(SDL_Event *ev)
ui/sdl2.c:491:static void handle_mousemotion(SDL_Event *ev)
ui/sdl2.c:522:static void handle_mousebutton(SDL_Event *ev)
ui/sdl2.c:548:static void handle_mousewheel(SDL_Event *ev)
ui/sdl2.c:576:static void handle_windowevent(SDL_Event *ev)
ui/sdl2.c:655:void sdl2_poll_events(struct sdl2_console *scon)
ui/sdl2.c:723:static void sdl_mouse_warp(DisplayChangeListener *dcl,
ui/sdl2.c:749:static void sdl_mouse_define(DisplayChangeListener *dcl,
ui/sdl2.c:781:static void sdl_cleanup(void)
ui/sdl2.c:815:sdl2_gl_is_compatible_dcl(DisplayGLCtx *dgc,
ui/sdl2.c:829:static void sdl2_display_early_init(DisplayOptions *o)
ui/sdl2.c:839:static void sdl2_display_init(DisplayState *ds, DisplayOptions *o)
ui/sdl2.c:964:static void register_sdl1(void)
ui/sdl2.c:969:type_init(register_sdl1);
ui/sdl2.c:972:module_dep("ui-opengl");
```

- `grep(pattern=^[A-Za-z_].*\(, path_glob=ui/input.c, version=old, max_results=400)` →

```
39 matches
ui/input.c:21:typedef QTAILQ_HEAD(QemuInputEventQueueHead, QemuInputEventQueue)
ui/input.c:37:static QTAILQ_HEAD(, QemuInputHandlerState) handlers =
ui/input.c:42:static QemuInputEventQueueHead kbd_queue = QTAILQ_HEAD_INITIALIZER(kbd_queue);
ui/input.c:48:QemuInputHandlerState *qemu_input_handler_register(DeviceState *dev,
ui/input.c:63:void qemu_input_handler_activate(QemuInputHandlerState *s)
ui/input.c:70:void qemu_input_handler_deactivate(QemuInputHandlerState *s)
ui/input.c:77:void qemu_input_handler_unregister(QemuInputHandlerState *s)
ui/input.c:84:void qemu_input_handler_bind(QemuInputHandlerState *s,
ui/input.c:101:qemu_input_find_handler(uint32_t mask, QemuConsole *con)
ui/input.c:125:void qmp_input_send_event(const char *device,
ui/input.c:177:static int qemu_input_transform_invert_abs_value(int value)
ui/input.c:182:static void qemu_input_transform_abs_rotate(InputEvent *evt)
ui/input.c:208:static void qemu_input_event_trace(QemuConsole *src, InputEvent *evt)
ui/input.c:265:static void qemu_input_queue_process(void *opaque)
ui/input.c:298:static void qemu_input_queue_delay(QemuInputEventQueueHead *queue,
ui/input.c:316:static void qemu_input_queue_event(QemuInputEventQueueHead *queue,
ui/input.c:328:static void qemu_input_queue_sync(QemuInputEventQueueHead *queue)
ui/input.c:337:void qemu_input_event_send_impl(QemuConsole *src, InputEvent *evt)
ui/input.c:357:void qemu_input_event_send(QemuConsole *src, InputEvent *evt)
ui/input.c:385:void qemu_input_event_sync_impl(void)
ui/input.c:402:void qemu_input_event_sync(void)
ui/input.c:411:static InputEvent *qemu_input_event_new_key(KeyValue *key, bool down)
ui/input.c:421:void qemu_input_event_send_key(QemuConsole *src, KeyValue *key, bool down)
ui/input.c:437:void qemu_input_event_send_key_number(QemuConsole *src, int num, bool down)
ui/input.c:443:void qemu_input_event_send_key_qcode(QemuConsole *src, QKeyCode q, bool down)
ui/input.c:451:void qemu_input_event_send_key_delay(uint32_t delay_ms)
ui/input.c:468:void qemu_input_queue_btn(QemuConsole *src, InputButton btn, bool down)
ui/input.c:482:void qemu_input_update_buttons(QemuConsole *src, uint32_t *button_map,
ui/input.c:497:bool qemu_input_is_absolute(void)
ui/input.c:506:int qemu_input_scale_axis(int value,
ui/input.c:519:void qemu_input_queue_rel(QemuConsole *src, InputAxis axis, int value)
ui/input.c:533:void qemu_input_queue_abs(QemuConsole *src, InputAxis axis, int value,
ui/input.c:550:void qemu_input_queue_mtt(QemuConsole *src, InputMultiTouchType type,
ui/input.c:566:void qemu_input_queue_mtt_abs(QemuConsole *src, InputAxis axis, int value,
ui/input.c:586:void qemu_input_check_mode_change(void)
ui/input.c:601:void qemu_add_mouse_mode_change_notifier(Notifier *notify)
ui/input.c:606:void qemu_remove_mouse_mode_change_notifier(Notifier *notify)
ui/input.c:611:MouseInfoList *qmp_query_mice(Error **errp)
ui/input.c:637:bool qemu_mouse_set(int index, Error **errp)
```

- `grep(pattern=^[A-Za-z_].*\(, path_glob=ui/spice-input.c, version=old, max_results=400)` →

```
14 matches
ui/spice-input.c:37:static void kbd_push_key(SpiceKbdInstance *sin, uint8_t frag);
ui/spice-input.c:38:static uint8_t kbd_get_leds(SpiceKbdInstance *sin);
ui/spice-input.c:49:static void kbd_push_key(SpiceKbdInstance *sin, uint8_t scancode)
ui/spice-input.c:82:static uint8_t kbd_get_leds(SpiceKbdInstance *sin)
ui/spice-input.c:88:static void kbd_leds(void *opaque, int ledstate)
ui/spice-input.c:116:static void spice_update_buttons(QemuSpicePointer *pointer,
ui/spice-input.c:143:static void mouse_motion(SpiceMouseInstance *sin, int dx, int dy, int dz,
ui/spice-input.c:153:static void mouse_buttons(SpiceMouseInstance *sin, uint32_t buttons_state)
ui/spice-input.c:169:static void tablet_set_logical_size(SpiceTabletInstance* sin, int width, int height)
ui/spice-input.c:183:static void tablet_position(SpiceTabletInstance* sin, int x, int y,
ui/spice-input.c:195:static void tablet_wheel(SpiceTabletInstance* sin, int wheel,
ui/spice-input.c:204:static void tablet_buttons(SpiceTabletInstance *sin,
ui/spice-input.c:224:static void mouse_mode_notifier(Notifier *notifier, void *data)
ui/spice-input.c:241:void qemu_spice_input_init(void)
```

- `grep(pattern=^[A-Za-z_].*\(, path_glob=ui/vnc.c, version=old, max_results=400)` →

```
139 matches
ui/vnc.c:68:static QTAILQ_HEAD(, VncDisplay) vnc_displays =
ui/vnc.c:71:static int vnc_cursor_define(VncState *vs);
ui/vnc.c:72:static void vnc_update_throttle_offset(VncState *vs);
ui/vnc.c:74:static void vnc_set_share_mode(VncState *vs, VncShareMode mode)
ui/vnc.c:120:static void vnc_init_basic_info(SocketAddress *addr,
ui/vnc.c:153:static void vnc_init_basic_info_from_server_addr(QIOChannelSocket *ioc,
ui/vnc.c:173:static void vnc_init_basic_info_from_remote_addr(QIOChannelSocket *ioc,
ui/vnc.c:188:static const char *vnc_auth_name(VncDisplay *vd) {
ui/vnc.c:235:static VncServerInfo *vnc_server_info_get(VncDisplay *vd)
ui/vnc.c:256:static void vnc_client_cache_auth(VncState *client)
ui/vnc.c:274:static void vnc_client_cache_addr(VncState *client)
ui/vnc.c:290:static void vnc_qmp_event(VncState *vs, QAPIEvent event)
ui/vnc.c:320:static VncClientInfo *qmp_query_vnc_client(const VncState *client)
ui/vnc.c:350:static VncDisplay *vnc_display_find(const char *id)
ui/vnc.c:365:static VncClientInfoList *qmp_query_client_list(VncDisplay *vd)
ui/vnc.c:376:VncInfo *qmp_query_vnc(Error **errp)
ui/vnc.c:438:static void qmp_query_auth(int auth, int subauth,
ui/vnc.c:443:static VncServerInfo2List *qmp_query_server_entry(QIOChannelSocket *ioc,
ui/vnc.c:475:static void qmp_query_auth(int auth, int subauth,
ui/vnc.c:545:VncInfo2List *qmp_query_vnc_servers(Error **errp)
ui/vnc.c:580:bool vnc_display_reload_certs(const char *id, Error **errp)
ui/vnc.c:615:static int vnc_update_client(VncState *vs, int has_dirty);
ui/vnc.c:616:static void vnc_disconnect_start(VncState *vs);
ui/vnc.c:618:static void vnc_colordepth(VncState *vs);
ui/vnc.c:619:static void framebuffer_update_request(VncState *vs, int incremental,
ui/vnc.c:622:static void vnc_refresh(DisplayChangeListener *dcl);
ui/vnc.c:623:static int vnc_refresh_server_surface(VncDisplay *vd);
ui/vnc.c:625:static int vnc_width(VncDisplay *vd)
ui/vnc.c:631:static int vnc_true_width(VncDisplay *vd)
ui/vnc.c:636:static int vnc_height(VncDisplay *vd)
ui/vnc.c:641:static void vnc_set_area_dirty(DECLARE_BITMAP(dirty[VNC_MAX_HEIGHT],
ui/vnc.c:665:static void vnc_dpy_update(DisplayChangeListener *dcl,
ui/vnc.c:674:void vnc_framebuffer_update(VncState *vs, int x, int y, int w, int h,
ui/vnc.c:685:static void vnc_desktop_resize_ext(VncState *vs, int reject_reason)
ui/vnc.c:713:static void vnc_desktop_resize(VncState *vs)
ui/vnc.c:749:static void vnc_abort_display_jobs(VncDisplay *vd)
ui/vnc.c:774:int vnc_server_fb_stride(VncDisplay *vd)
ui/vnc.c:779:void *vnc_server_fb_ptr(VncDisplay *vd, int x, int y)
ui/vnc.c:789:static void vnc_update_server_surface(VncDisplay *vd)
ui/vnc.c:812:static bool vnc_check_pageflip(DisplaySurface *s1,
ui/vnc.c:823:static void vnc_dpy_switch(DisplayChangeListener *dcl,
ui/vnc.c:870:static void vnc_write_pixels_copy(VncState *vs,
ui/vnc.c:877:void vnc_convert_pixel(VncState *vs, uint8_t *buf, uint32_t v)
ui/vnc.c:921:static void vnc_write_pixels_generic(VncState *vs,
ui/vnc.c:937:int vnc_raw_send_framebuffer_update(VncState *vs, int x, int y, int w, int h)
ui/vnc.c:951:int vnc_send_framebuffer_update(VncState *vs, int x, int y, int w, int h)
ui/vnc.c:983:static void vnc_mouse_set(DisplayChangeListener *dcl,
ui/vnc.c:989:static int vnc_cursor_define(VncState *vs)
ui/vnc.c:1026:static void vnc_dpy_cursor_define(DisplayChangeListener *dcl,
ui/vnc.c:1042:static int find_and_clear_dirty_height(VncState *vs,
ui/vnc.c:1067:static void vnc_update_throttle_offset(VncState *vs)
ui/vnc.c:1107:static bool vnc_should_update(VncState *vs)
ui/vnc.c:1144:static int vnc_update_client(VncState *vs, int has_dirty)
ui/vnc.c:1215:static void audio_capture_notify(void *opaque, audcnotification_e cmd)
ui/vnc.c:1243:static void audio_capture_destroy(void *opaque)
ui/vnc.c:1247:static void audio_capture(void *opaque, const void *buf, int size)
ui/vnc.c:1267:static void audio_add(VncState *vs)
ui/vnc.c:1286:static void audio_del(VncState *vs)
ui/vnc.c:1294:static void vnc_disconnect_start(VncState *vs)
ui/vnc.c:1309:void vnc_disconnect_finish(VncState *vs)
ui/vnc.c:1370:size_t vnc_client_io_error(VncState *vs, ssize_t ret, Error *err)
ui/vnc.c:1389:void vnc_client_error(VncState *vs)
ui/vnc.c:1411:size_t vnc_client_write_buf(VncState *vs, const uint8_t *data, size_t datalen)
ui/vnc.c:1431:static size_t vnc_client_write_plain(VncState *vs)
ui/vnc.c:1486:static void vnc_client_write_locked(VncState *vs)
ui/vnc.c:1500:static void vnc_client_write(VncState *vs)
ui/vnc.c:1517:void vnc_read_when(VncState *vs, VncReadEvent *func, size_t expecting)
ui/vnc.c:1539:size_t vnc_client_read_buf(VncState *vs, uint8_t *data, size_t datalen)
ui/vnc.c:1558:static size_t vnc_client_read_plain(VncState *vs)
ui/vnc.c:1571:static void vnc_jobs_bh(void *opaque)
ui/vnc.c:1585:static int vnc_client_read(VncState *vs)
ui/vnc.c:1622:gboolean vnc_client_io(QIOChannel *ioc G_GNUC_UNUSED,
ui/vnc.c:1663:void vnc_write(VncState *vs, const void *data, size_t len)
ui/vnc.c:1702:void vnc_write_s32(VncState *vs, int32_t value)
ui/vnc.c:1707:void vnc_write_u32(VncState *vs, uint32_t value)
ui/vnc.c:1719:void vnc_write_u16(VncState *vs, uint16_t value)
ui/vnc.c:1729:void vnc_write_u8(VncState *vs, uint8_t value)
ui/vnc.c:1734:void vnc_flush(VncState *vs)
ui/vnc.c:1749:static uint8_t read_u8(uint8_t *data, size_t offset)
ui/vnc.c:1754:static uint16_t read_u16(uint8_t *data, size_t offset)
ui/vnc.c:1759:static int32_t read_s32(uint8_t *data, size_t offset)
ui/vnc.c:1765:uint32_t read_u32(uint8_t *data, size_t offset)
ui/vnc.c:1771:static void check_pointer_type_change(Notifier *notifier, void *data)
ui/vnc.c:1791:static void pointer_event(VncState *vs, int button_mask, int x, int y)
ui/vnc.c:1826:static void press_key(VncState *vs, QKeyCode qcode)
ui/vnc.c:1832:static void vnc_led_state_change(VncState *vs)
ui/vnc.c:1848:static void kbd_leds(void *opaque, int ledstate)
ui/vnc.c:1868:static void do_key_event(VncState *vs, int down, int keycode, int sym)
ui/vnc.c:2037:static const char *code2name(int keycode)
ui/vnc.c:2042:static void key_event(VncState *vs, int down, uint32_t sym)
ui/vnc.c:2057:static void ext_key_event(VncState *vs, int down,
ui/vnc.c:2069:static void framebuffer_update_request(VncState *vs, int incremental,
ui/vnc.c:2085:static void send_ext_key_event_ack(VncState *vs)
ui/vnc.c:2099:static void send_ext_audio_ack(VncState *vs)
ui/vnc.c:2113:static void send_xvp_message(VncState *vs, int code)
ui/vnc.c:2124:static void set_encodings(VncState *vs, int32_t *encodings, size_t n_encodings)
ui/vnc.c:2235:static void set_pixel_conversion(VncState *vs)
ui/vnc.c:2248:static void send_color_map(VncState *vs)
ui/vnc.c:2268:static void set_pixel_format(VncState *vs, int bits_per_pixel,
ui/vnc.c:2321:static void pixel_format_message (VncState *vs) {
ui/vnc.c:2347:static void vnc_colordepth(VncState *vs)
ui/vnc.c:2367:static int protocol_client_msg(VncState *vs, uint8_t *data, size_t len)
ui/vnc.c:2609:static int protocol_client_init(VncState *vs, uint8_t *data, size_t len)
ui/vnc.c:2710:void start_client_init(VncState *vs)
ui/vnc.c:2715:static void authentication_failed(VncState *vs)
ui/vnc.c:2728:vnc_munge_des_rfb_key(unsigned char *key, size_t nkey)
ui/vnc.c:2740:static int protocol_client_auth_vnc(VncState *vs, uint8_t *data, size_t len)
ui/vnc.c:2810:void start_auth_vnc(VncState *vs)
ui/vnc.c:2830:static int protocol_client_auth(VncState *vs, uint8_t *data, size_t len)
ui/vnc.c:2871:static int protocol_version(VncState *vs, uint8_t *version, size_t len)
ui/vnc.c:2931:static VncRectStat *vnc_stat_rect(VncDisplay *vd, int x, int y)
ui/vnc.c:2938:void vnc_sent_lossy_rect(VncState *vs, int x, int y, int w, int h)
ui/vnc.c:2954:static int vnc_refresh_lossy_rect(VncDisplay *vd, int x, int y)
ui/vnc.c:2988:static int vnc_update_stats(VncDisplay *vd,  struct timeval * tv)
ui/vnc.c:3045:double vnc_update_freq(VncState *vs, int x, int y, int w, int h)
ui/vnc.c:3068:static void vnc_rect_updated(VncDisplay *vd, int x, int y, struct timeval * tv)
ui/vnc.c:3081:static int vnc_refresh_server_surface(VncDisplay *vd)
ui/vnc.c:3184:static void vnc_refresh(DisplayChangeListener *dcl)
ui/vnc.c:3223:static void vnc_connect(VncDisplay *vd, QIOChannelSocket *sioc,
ui/vnc.c:3337:void vnc_start_protocol(VncState *vs)
ui/vnc.c:3347:static void vnc_listen_io(QIONetListener *listener,
ui/vnc.c:3370:void vnc_display_init(const char *id, Error **errp)
ui/vnc.c:3409:static void vnc_display_close(VncDisplay *vd)
ui/vnc.c:3454:int vnc_display_password(const char *id, const char *password)
ui/vnc.c:3473:int vnc_display_pw_expire(const char *id, time_t expires)
ui/vnc.c:3485:static void vnc_display_print_local_addr(VncDisplay *vd)
ui/vnc.c:3586:vnc_display_setup_auth(int *auth,
ui/vnc.c:3697:static int vnc_display_get_address(const char *addrstr,
ui/vnc.c:3814:static int vnc_display_get_addresses(QemuOpts *opts,
ui/vnc.c:3906:static int vnc_display_connect(VncDisplay *vd,
ui/vnc.c:3935:static int vnc_display_listen(VncDisplay *vd,
ui/vnc.c:3975:bool vnc_display_update(DisplayUpdateOptionsVNC *arg, Error **errp)
ui/vnc.c:3999:void vnc_display_open(const char *id, Error **errp)
ui/vnc.c:4230:void vnc_display_add_client(const char *id, int csock, bool skipauth)
ui/vnc.c:4247:static void vnc_auto_assign_id(QemuOptsList *olist, QemuOpts *opts)
ui/vnc.c:4260:void vnc_parse(const char *str)
ui/vnc.c:4277:int vnc_init_func(void *opaque, QemuOpts *opts, Error **errp)
ui/vnc.c:4296:static void vnc_register_config(void)
ui/vnc.c:4300:opts_init(vnc_register_config);
```

### Turn 3  _(tok 20069+2591, stop=tool_use)_

**Reasoning:** I'm matching each line number to the function that contains it: the cocoa.m line falls in cocoa_refresh, and the three dbus-console.c lines fall in dbus_mouse_rel_motion, dbus_mouse_set_pos, and dbus_mouse_update_is_absolute. Now I'm starting on gtk.c.

Now I'm mapping the gtk.c lines to their enclosing functions: 207 falls in gd_update_cursor, 456 in gd_mouse_set, 692 in gd_mouse_mode_change, and both 906 and 926 in gd_motion_event, with 968 in gd_button_event. Moving on to the input.c and sdl2.c hits.

Checking the remaining hits: spice-input.c line 227 falls in mouse_mode_notifier, and vnc.c line 1774 falls in check_pointer_type_change. For the sdl2.c ambiguous ones, 206 is inside sdl_hide_cursor and 217 is inside sdl_show_cursor, since sdl_hide_cursor ends before sdl_show_cursor begins.

I'm checking the sdl2.c hit at 222, which sits inside sdl_show_cursor, and I'm noting that the cocoa.m comment at line 327 doesn't count. The grep covered every tracked file, so the list of call sites is complete.

I'm working through the unique callers list now, having already confirmed the dbus-console.c and gtk.c lines fall inside their enclosing functions. The list so far covers cocoa_refresh, the three dbus-console.c functions, and the first gtk.c functions, with gd_motion_event still being matched to its file.

I'm now going through the unique callers list, with the gtk.c entries done and the input.c, sdl2.c, spice-input.c, and vnc.c ones still to confirm. I'm also rechecking the sdl2.c line 283 match against sdl_mouse_mode_change.

I'm checking the gtk.c line 456 against gd_mouse_set, which spans 448 to 469, so it falls inside. I'm also settling on a confidence level for the whole line-to-function mapping: it's inferred from function start lines, which is reliable for C files, so I'd rate it high.



- **submit_callers** → `{"callers": [{"function": "cocoa_refresh", "file": "ui/cocoa.m"}, {"function": "dbus_mouse_rel_motion", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_set_pos", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_update_is_absolute", "file": "ui/dbus-console.c"}, {"function": "gd_update_cursor", "file": "ui/gtk.c"}, {"function": "gd_mouse_set", "file": "ui/gtk.c"}, {"function": "gd_mouse_mode_change", "file": "ui/gtk.c"}, {"function": "gd_motion_event", "file": "ui/gtk.c"}, {"function": "gd_button_event", "file": "ui/gtk.c"}, {"function": "qemu_input_check_mode_change", "file": "ui/input.c"}, {"function": "sdl_hide_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_show_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_grab_start", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_mode_change", "file": "ui/sdl2.c"}, {"function": "sdl_send_mouse_event", "file": "ui/sdl2.c"}, {"function": "handle_mousemotion", "file": "ui/sdl2.c"}, {"function": "handle_mousebutton", "file": "ui/sdl2.c"}, {"function": "handle_windowevent", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_warp", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_define", "file": "ui/sdl2.c"}, {"function": "mouse_mode_notifier", "file": "ui/spice-input.c"}, {"function": "check_pointer_type_change", "file": "ui/vnc.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 22, "n_truth": 22, "tp": 22, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3753+222, stop=tool_use)_

**Reasoning:** I'm going to call get_callers and run a grep at the same time.



- `get_callers(name=qemu_input_is_absolute, limit=200, version=old)` →

```
{
  "name": "qemu_input_is_absolute",
  "version": "old",
  "callers": [
    {
      "caller": "dbus_mouse_rel_motion",
      "file": "ui/dbus-console.c",
      "line": 389
    },
    {
      "caller": "dbus_mouse_set_pos",
      "file": "ui/dbus-console.c",
      "line": 456
    },
    {
      "caller": "dbus_mouse_update_is_absolute",
      "file": "ui/dbus-console.c",
      "line": 517
    },
    {
      "caller": "gd_update_cursor",
      "file": "ui/gtk.c",
      "line": 207
    },
    {
      "caller": "gd_mouse_set",
      "file": "ui/gtk.c",
      "line": 456
    },
    {
      "caller": "gd_mouse_mode_change",
      "file": "ui/gtk.c",
      "line": 692
    },
    {
      "caller": "gd_motion_event",
      "file": "ui/gtk.c",
      "line": 906
    },
    {
      "caller": "gd_motion_event",
      "file": "ui/gtk.c",
      "line": 926
    },
    {
      "caller": "gd_button_event",
      "file": "ui/gtk.c",
      "line": 968
    },
    {
      "caller": "qemu_input_check_mode_change",
      "file": "ui/input.c",
      "line": 591
    },
    {
      "caller": "sdl_hide_cursor",
      "file": "ui/sdl2.c",
      "line": 206
    },
    {
      "caller": "sdl_show_cursor",
      "file": "ui/sdl2.c",
      "line": 217
    },
    {
      "caller": "sdl_show_cursor",
      "file": "ui/sdl2.c",
      "line": 222
    },
    {
      "caller": "sdl_grab_start",
      "file": "ui/sdl2.c",
      "line": 248
    },
    {
      "caller": "sdl_mouse_mode_change",
      "file": "ui/sdl2.c",
      "line": 283
    },
    {
      "caller": "sdl_send_mouse_event",
      "file": "ui/sdl2.c",
      "line": 314
    },
    {
      "caller": "handle_mousemotion",
      "file": "ui/sdl2.c",
      "line": 500
    },
    {
      "caller": "handle_mousemotion",
      "file": "ui/sdl2.c",
      "line": 516
    },
    {
      "caller": "handle_mousebutton",
      "file": "ui/sdl2.c",
      "line": 533
    },
    {
      "caller": "handle_windowevent",
      "file": "ui/sdl2.c",
      "line": 606
    },
    {
      "caller": "sdl_mouse_warp",
      "file": "ui/sdl2.c",
      "line": 736
    },
    {
      "caller": "sdl_mouse_warp",
      "file": "ui/sdl2.c",
      "line": 738
    },
    {
      "caller": "sdl_mouse_define",
      "file": "ui/sdl2.c",
      "line": 776
    },
    {
      "caller": "mouse_mode_notifier",
      "file": "ui/spice-input.c",
      "line": 227
    },
    {
      "caller": "check_pointer_type_change",
      "file": "ui/vnc.c",
      "line": 1774
    }
  ]
}
```

- `grep(pattern=qemu_input_is_absolute, version=old, max_results=500)` →

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

### Turn 2  _(tok 6284+722, stop=tool_use)_

**Reasoning:** The grep turned up a match at cocoa.m:2004 that get_callers didn't report, probably because the file isn't C and the parser missed it. I need to find the function that encloses that line in cocoa.m. Of the 29 grep matches, I'll check whether they are all accounted for.

The count comes out to 26 grep call lines, and get_callers returned 25 of them, so the cocoa.m:2004 hit is the one it dropped. Next I need the function that encloses line 2004 in cocoa.m.



**Says:** The grep found one call site, in `ui/cocoa.m:2004`, that `get_callers` did not report. I need its enclosing function.

- `get_context_at(file=ui/cocoa.m, line=2004, version=old)` →

```
{
  "error": "get_context_at failed: NotImplementedError: File is not a C/C++ file: /tmp/cce_wt_atfu7t1e/wt/ui/cocoa.m"
}
```

### Turn 3  _(tok 7079+124, stop=tool_use)_

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

### Turn 4  _(tok 7723+1178, stop=tool_use)_

**Reasoning:** I'm checking the enclosing function, cocoa_refresh in ui/cocoa.m, and whether any call outside git grep's reach could matter, such as untracked files or headers with inline calls. I think it's fine, so I'll submit. I'm also compiling the callers in ui/dbus-console.c: dbus_mouse_rel_motion, dbus_mouse_set_pos, and dbus_mouse_update_is_absolute.

I'm adding the rest of the callers to the list: the GTK, input, SDL2, SPICE, and VNC handlers, plus cocoa_refresh in ui/cocoa.m. The .m file is Objective-C, but it's still a call site in the repo, so I'm including it.



- **submit_callers** → `{"callers": [{"function": "dbus_mouse_rel_motion", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_set_pos", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_update_is_absolute", "file": "ui/dbus-console.c"}, {"function": "gd_update_cursor", "file": "ui/gtk.c"}, {"function": "gd_mouse_set", "file": "ui/gtk.c"}, {"function": "gd_mouse_mode_change", "file": "ui/gtk.c"}, {"function": "gd_motion_event", "file": "ui/gtk.c"}, {"function": "gd_button_event", "file": "ui/gtk.c"}, {"function": "qemu_input_check_mode_change", "file": "ui/input.c"}, {"function": "sdl_hide_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_show_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_grab_start", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_mode_change", "file": "ui/sdl2.c"}, {"function": "sdl_send_mouse_event", "file": "ui/sdl2.c"}, {"function": "handle_mousemotion", "file": "ui/sdl2.c"}, {"function": "handle_mousebutton", "file": "ui/sdl2.c"}, {"function": "handle_windowevent", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_warp", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_define", "file": "ui/sdl2.c"}, {"function": "mouse_mode_notifier", "file": "ui/spice-input.c"}, {"function": "check_pointer_type_change", "file": "ui/vnc.c"}, {"function": "cocoa_refresh", "file": "ui/cocoa.m"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 22, "n_truth": 22, "tp": 22, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3205+80, stop=tool_use)_

- `get_callers(name=qemu_input_is_absolute, limit=200)` →

```
{
  "name": "qemu_input_is_absolute",
  "version": "old",
  "callers": [
    {
      "caller": "dbus_mouse_rel_motion",
      "file": "ui/dbus-console.c",
      "line": 389
    },
    {
      "caller": "dbus_mouse_set_pos",
      "file": "ui/dbus-console.c",
      "line": 456
    },
    {
      "caller": "dbus_mouse_update_is_absolute",
      "file": "ui/dbus-console.c",
      "line": 517
    },
    {
      "caller": "gd_update_cursor",
      "file": "ui/gtk.c",
      "line": 207
    },
    {
      "caller": "gd_mouse_set",
      "file": "ui/gtk.c",
      "line": 456
    },
    {
      "caller": "gd_mouse_mode_change",
      "file": "ui/gtk.c",
      "line": 692
    },
    {
      "caller": "gd_motion_event",
      "file": "ui/gtk.c",
      "line": 906
    },
    {
      "caller": "gd_motion_event",
      "file": "ui/gtk.c",
      "line": 926
    },
    {
      "caller": "gd_button_event",
      "file": "ui/gtk.c",
      "line": 968
    },
    {
      "caller": "qemu_input_check_mode_change",
      "file": "ui/input.c",
      "line": 591
    },
    {
      "caller": "sdl_hide_cursor",
      "file": "ui/sdl2.c",
      "line": 206
    },
    {
      "caller": "sdl_show_cursor",
      "file": "ui/sdl2.c",
      "line": 217
    },
    {
      "caller": "sdl_show_cursor",
      "file": "ui/sdl2.c",
      "line": 222
    },
    {
      "caller": "sdl_grab_start",
      "file": "ui/sdl2.c",
      "line": 248
    },
    {
      "caller": "sdl_mouse_mode_change",
      "file": "ui/sdl2.c",
      "line": 283
    },
    {
      "caller": "sdl_send_mouse_event",
      "file": "ui/sdl2.c",
      "line": 314
    },
    {
      "caller": "handle_mousemotion",
      "file": "ui/sdl2.c",
      "line": 500
    },
    {
      "caller": "handle_mousemotion",
      "file": "ui/sdl2.c",
      "line": 516
    },
    {
      "caller": "handle_mousebutton",
      "file": "ui/sdl2.c",
      "line": 533
    },
    {
      "caller": "handle_windowevent",
      "file": "ui/sdl2.c",
      "line": 606
    },
    {
      "caller": "sdl_mouse_warp",
      "file": "ui/sdl2.c",
      "line": 736
    },
    {
      "caller": "sdl_mouse_warp",
      "file": "ui/sdl2.c",
      "line": 738
    },
    {
      "caller": "sdl_mouse_define",
      "file": "ui/sdl2.c",
      "line": 776
    },
    {
      "caller": "mouse_mode_notifier",
      "file": "ui/spice-input.c",
      "line": 227
    },
    {
      "caller": "check_pointer_type_change",
      "file": "ui/vnc.c",
      "line": 1774
    }
  ]
}
```

### Turn 2  _(tok 4486+334, stop=tool_use)_

**Reasoning:** The default version came back as "old", which seems to be the parent of the server's commit. Since the change is going into the working tree, I want to see the work version as well, so I'll call the tool again with version "work".



**Says:** The default lookup reported the `old` version. I'll also check the working tree, since that is the code about to change.

- `get_callers(name=qemu_input_is_absolute, limit=200, rev=HEAD)` →

```
{
  "name": "qemu_input_is_absolute",
  "version": "old",
  "callers": [
    {
      "caller": "dbus_mouse_rel_motion",
      "file": "ui/dbus-console.c",
      "line": 389
    },
    {
      "caller": "dbus_mouse_set_pos",
      "file": "ui/dbus-console.c",
      "line": 456
    },
    {
      "caller": "dbus_mouse_update_is_absolute",
      "file": "ui/dbus-console.c",
      "line": 517
    },
    {
      "caller": "gd_update_cursor",
      "file": "ui/gtk.c",
      "line": 207
    },
    {
      "caller": "gd_mouse_set",
      "file": "ui/gtk.c",
      "line": 456
    },
    {
      "caller": "gd_mouse_mode_change",
      "file": "ui/gtk.c",
      "line": 692
    },
    {
      "caller": "gd_motion_event",
      "file": "ui/gtk.c",
      "line": 906
    },
    {
      "caller": "gd_motion_event",
      "file": "ui/gtk.c",
      "line": 926
    },
    {
      "caller": "gd_button_event",
      "file": "ui/gtk.c",
      "line": 968
    },
    {
      "caller": "qemu_input_check_mode_change",
      "file": "ui/input.c",
      "line": 591
    },
    {
      "caller": "sdl_hide_cursor",
      "file": "ui/sdl2.c",
      "line": 206
    },
    {
      "caller": "sdl_show_cursor",
      "file": "ui/sdl2.c",
      "line": 217
    },
    {
      "caller": "sdl_show_cursor",
      "file": "ui/sdl2.c",
      "line": 222
    },
    {
      "caller": "sdl_grab_start",
      "file": "ui/sdl2.c",
      "line": 248
    },
    {
      "caller": "sdl_mouse_mode_change",
      "file": "ui/sdl2.c",
      "line": 283
    },
    {
      "caller": "sdl_send_mouse_event",
      "file": "ui/sdl2.c",
      "line": 314
    },
    {
      "caller": "handle_mousemotion",
      "file": "ui/sdl2.c",
      "line": 500
    },
    {
      "caller": "handle_mousemotion",
      "file": "ui/sdl2.c",
      "line": 516
    },
    {
      "caller": "handle_mousebutton",
      "file": "ui/sdl2.c",
      "line": 533
    },
    {
      "caller": "handle_windowevent",
      "file": "ui/sdl2.c",
      "line": 606
    },
    {
      "caller": "sdl_mouse_warp",
      "file": "ui/sdl2.c",
      "line": 736
    },
    {
      "caller": "sdl_mouse_warp",
      "file": "ui/sdl2.c",
      "line": 738
    },
    {
      "caller": "sdl_mouse_define",
      "file": "ui/sdl2.c",
      "line": 776
    },
    {
      "caller": "mouse_mode_notifier",
      "file": "ui/spice-input.c",
      "line": 227
    },
    {
      "caller": "check_pointer_type_change",
      "file": "ui/vnc.c",
      "line": 1774
    }
  ]
}
```

- `resolve_symbol(name=qemu_input_is_absolute)` →

```
{
  "resolved": true,
  "name": "qemu_input_is_absolute",
  "version": "old",
  "file": "ui/input.c",
  "line": 497,
  "kind": "function",
  "signature": "bool qemu_input_is_absolute(void)",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 3  _(tok 6196+245, stop=tool_use)_

**Reasoning:** Resolve is reporting the "old" version, so I want to confirm against the "work" version before trusting that. I'll run get_callers with the work version.



**Says:** The tool keeps reporting `old`, so I'll query the working-tree version explicitly.

- `get_callers(name=qemu_input_is_absolute, limit=200, rev=work)` →

```
{
  "name": "qemu_input_is_absolute",
  "version": "old",
  "callers": [
    {
      "caller": "dbus_mouse_rel_motion",
      "file": "ui/dbus-console.c",
      "line": 389
    },
    {
      "caller": "dbus_mouse_set_pos",
      "file": "ui/dbus-console.c",
      "line": 456
    },
    {
      "caller": "dbus_mouse_update_is_absolute",
      "file": "ui/dbus-console.c",
      "line": 517
    },
    {
      "caller": "gd_update_cursor",
      "file": "ui/gtk.c",
      "line": 207
    },
    {
      "caller": "gd_mouse_set",
      "file": "ui/gtk.c",
      "line": 456
    },
    {
      "caller": "gd_mouse_mode_change",
      "file": "ui/gtk.c",
      "line": 692
    },
    {
      "caller": "gd_motion_event",
      "file": "ui/gtk.c",
      "line": 906
    },
    {
      "caller": "gd_motion_event",
      "file": "ui/gtk.c",
      "line": 926
    },
    {
      "caller": "gd_button_event",
      "file": "ui/gtk.c",
      "line": 968
    },
    {
      "caller": "qemu_input_check_mode_change",
      "file": "ui/input.c",
      "line": 591
    },
    {
      "caller": "sdl_hide_cursor",
      "file": "ui/sdl2.c",
      "line": 206
    },
    {
      "caller": "sdl_show_cursor",
      "file": "ui/sdl2.c",
      "line": 217
    },
    {
      "caller": "sdl_show_cursor",
      "file": "ui/sdl2.c",
      "line": 222
    },
    {
      "caller": "sdl_grab_start",
      "file": "ui/sdl2.c",
      "line": 248
    },
    {
      "caller": "sdl_mouse_mode_change",
      "file": "ui/sdl2.c",
      "line": 283
    },
    {
      "caller": "sdl_send_mouse_event",
      "file": "ui/sdl2.c",
      "line": 314
    },
    {
      "caller": "handle_mousemotion",
      "file": "ui/sdl2.c",
      "line": 500
    },
    {
      "caller": "handle_mousemotion",
      "file": "ui/sdl2.c",
      "line": 516
    },
    {
      "caller": "handle_mousebutton",
      "file": "ui/sdl2.c",
      "line": 533
    },
    {
      "caller": "handle_windowevent",
      "file": "ui/sdl2.c",
      "line": 606
    },
    {
      "caller": "sdl_mouse_warp",
      "file": "ui/sdl2.c",
      "line": 736
    },
    {
      "caller": "sdl_mouse_warp",
      "file": "ui/sdl2.c",
      "line": 738
    },
    {
      "caller": "sdl_mouse_define",
      "file": "ui/sdl2.c",
      "line": 776
    },
    {
      "caller": "mouse_mode_notifier",
      "file": "ui/spice-input.c",
      "line": 227
    },
    {
      "caller": "check_pointer_type_change",
      "file": "ui/vnc.c",
      "line": 1774
    }
  ]
}
```

- `resolve_symbol(name=qemu_input_is_absolute, rev=work)` →

```
{
  "resolved": true,
  "name": "qemu_input_is_absolute",
  "version": "old",
  "file": "ui/input.c",
  "line": 497,
  "kind": "function",
  "signature": "bool qemu_input_is_absolute(void)",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 4  _(tok 7817+1070, stop=tool_use)_

**Reasoning:** I'm confirming the results are consistent and listing the unique callers. I'll keep qemu_input_check_mode_change from input.c since it's a calling function in the repo, then dedupe the remaining names, covering the dbus_mouse and gd_ handlers down to qemu.

I'm checking whether the list is complete. The callers tool might miss function pointer uses, but that seems acceptable, so I'll submit.



- **submit_callers** → `{"callers": [{"function": "dbus_mouse_rel_motion", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_set_pos", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_update_is_absolute", "file": "ui/dbus-console.c"}, {"function": "gd_update_cursor", "file": "ui/gtk.c"}, {"function": "gd_mouse_set", "file": "ui/gtk.c"}, {"function": "gd_mouse_mode_change", "file": "ui/gtk.c"}, {"function": "gd_motion_event", "file": "ui/gtk.c"}, {"function": "gd_button_event", "file": "ui/gtk.c"}, {"function": "qemu_input_check_mode_change", "file": "ui/input.c"}, {"function": "sdl_hide_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_show_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_grab_start", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_mode_change", "file": "ui/sdl2.c"}, {"function": "sdl_send_mouse_event", "file": "ui/sdl2.c"}, {"function": "handle_mousemotion", "file": "ui/sdl2.c"}, {"function": "handle_mousebutton", "file": "ui/sdl2.c"}, {"function": "handle_windowevent", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_warp", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_define", "file": "ui/sdl2.c"}, {"function": "mouse_mode_notifier", "file": "ui/spice-input.c"}, {"function": "check_pointer_type_change", "file": "ui/vnc.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 21, "n_truth": 22, "tp": 21, "precision": 1.0, "recall": 0.9545454545454546, "f1": 0.9767441860465117}`

