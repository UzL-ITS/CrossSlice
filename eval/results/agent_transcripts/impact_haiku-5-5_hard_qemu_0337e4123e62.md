# Impact-analysis transcript — qemu @ 0337e4123e62 — anthropic:claude-haiku-5-5

- target: `qemu_input_is_absolute` (ui/input.c), arity 0->1
- truth: [['ui/cocoa.m', 'cocoa_refresh'], ['ui/dbus-console.c', 'dbus_mouse_rel_motion'], ['ui/dbus-console.c', 'dbus_mouse_set_pos'], ['ui/dbus-console.c', 'dbus_mouse_update_is_absolute'], ['ui/gtk.c', 'gd_button_event'], ['ui/gtk.c', 'gd_motion_event'], ['ui/gtk.c', 'gd_mouse_mode_change'], ['ui/gtk.c', 'gd_mouse_set'], ['ui/gtk.c', 'gd_update_cursor'], ['ui/input.c', 'qemu_input_check_mode_change'], ['ui/sdl2.c', 'handle_mousebutton'], ['ui/sdl2.c', 'handle_mousemotion'], ['ui/sdl2.c', 'handle_windowevent'], ['ui/sdl2.c', 'sdl_grab_start'], ['ui/sdl2.c', 'sdl_hide_cursor'], ['ui/sdl2.c', 'sdl_mouse_define'], ['ui/sdl2.c', 'sdl_mouse_mode_change'], ['ui/sdl2.c', 'sdl_mouse_warp'], ['ui/sdl2.c', 'sdl_send_mouse_event'], ['ui/sdl2.c', 'sdl_show_cursor'], ['ui/spice-input.c', 'mouse_mode_notifier'], ['ui/vnc.c', 'check_pointer_type_change']]

## Self-navigation arm

### Turn 1  _(tok 1218+107, stop=tool_use)_

**Reasoning:** I'm searching the repo for every place qemu_input_is_absolute is used.



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

### Turn 2  _(tok 2387+349, stop=tool_use)_

**Reasoning:** I need the enclosing function for each of these lines, so I'm going to read the surrounding regions file by file. There are a lot of them, so I'll also try grepping for function definitions to map lines to their functions, which may be quicker than reading each range.

Next I'll try a grep for function-like lines in each file, looking for lines that start at column one, contain an open parenthesis, and don't end in a semicolon, so I can map the line numbers to their enclosing functions.



- `grep(pattern=^[A-Za-z_][A-Za-z0-9_ \*]*\(|^\{|^[a-z_]+\(, version=old, path_glob=ui/*.[cm], max_results=2000)` →

```
2443 matches (showing 200)
ui/clipboard.c:10:void qemu_clipboard_peer_register(QemuClipboardPeer *peer)
ui/clipboard.c:11:{
ui/clipboard.c:15:void qemu_clipboard_peer_unregister(QemuClipboardPeer *peer)
ui/clipboard.c:16:{
ui/clipboard.c:25:bool qemu_clipboard_peer_owns(QemuClipboardPeer *peer,
ui/clipboard.c:27:{
ui/clipboard.c:33:void qemu_clipboard_peer_release(QemuClipboardPeer *peer,
ui/clipboard.c:35:{
ui/clipboard.c:45:bool qemu_clipboard_check_serial(QemuClipboardInfo *info, bool client)
ui/clipboard.c:46:{
ui/clipboard.c:66:void qemu_clipboard_update(QemuClipboardInfo *info)
ui/clipboard.c:67:{
ui/clipboard.c:82:QemuClipboardInfo *qemu_clipboard_info(QemuClipboardSelection selection)
ui/clipboard.c:83:{
ui/clipboard.c:89:QemuClipboardInfo *qemu_clipboard_info_new(QemuClipboardPeer *owner,
ui/clipboard.c:91:{
ui/clipboard.c:101:QemuClipboardInfo *qemu_clipboard_info_ref(QemuClipboardInfo *info)
ui/clipboard.c:102:{
ui/clipboard.c:107:void qemu_clipboard_info_unref(QemuClipboardInfo *info)
ui/clipboard.c:108:{
ui/clipboard.c:126:void qemu_clipboard_request(QemuClipboardInfo *info,
ui/clipboard.c:128:{
ui/clipboard.c:139:void qemu_clipboard_reset_serial(void)
ui/clipboard.c:140:{
ui/clipboard.c:153:void qemu_clipboard_set_data(QemuClipboardPeer *peer,
ui/clipboard.c:159:{
ui/cocoa.m:84:static void cocoa_update(DisplayChangeListener *dcl,
ui/cocoa.m:87:static void cocoa_switch(DisplayChangeListener *dcl,
ui/cocoa.m:90:static void cocoa_refresh(DisplayChangeListener *dcl);
ui/cocoa.m:117:typedef void (^CodeBlock)(void);
ui/cocoa.m:118:typedef bool (^BoolCodeBlock)(void);
ui/cocoa.m:120:static void with_iothread_lock(CodeBlock block)
ui/cocoa.m:121:{
ui/cocoa.m:132:static bool bool_with_iothread_lock(BoolCodeBlock block)
ui/cocoa.m:133:{
ui/cocoa.m:272:static int cocoa_keycode_to_qemu(int keycode)
ui/cocoa.m:273:{
ui/cocoa.m:282:static void QEMU_Alert(NSString *message)
ui/cocoa.m:283:{
ui/cocoa.m:291:static void handleAnyDeviceErrors(Error * err)
ui/cocoa.m:292:{
ui/cocoa.m:306:{
ui/cocoa.m:344:static CGEventRef handleTapEvent(CGEventTapProxy proxy, CGEventType type, CGEventRef cgEvent, void *userInfo)
ui/cocoa.m:345:{
ui/cocoa.m:359:{
ui/cocoa.m:374:{
ui/cocoa.m:391:{
ui/cocoa.m:396:{
ui/cocoa.m:402:{
ui/cocoa.m:436:{
ui/cocoa.m:444:{
ui/cocoa.m:452:{
ui/cocoa.m:517:{
ui/cocoa.m:550:{
ui/cocoa.m:595:{
ui/cocoa.m:614:{
ui/cocoa.m:619:{
ui/cocoa.m:663:{
ui/cocoa.m:694:{
ui/cocoa.m:729:{
ui/cocoa.m:792:{
ui/cocoa.m:799:{
ui/cocoa.m:1137:{
ui/cocoa.m:1152:{
ui/cocoa.m:1184:{
ui/cocoa.m:1200:{
ui/cocoa.m:1223:{
ui/cocoa.m:1268:{
ui/cocoa.m:1277:{
ui/cocoa.m:1283:{
ui/cocoa.m:1300:{
ui/cocoa.m:1306:{
ui/cocoa.m:1312:{
ui/cocoa.m:1317:{
ui/cocoa.m:1323:{
ui/cocoa.m:1341:{
ui/cocoa.m:1352:{
ui/cocoa.m:1357:{
ui/cocoa.m:1364:{
ui/cocoa.m:1372:{
ui/cocoa.m:1398:{
ui/cocoa.m:1406:{
ui/cocoa.m:1417:{
ui/cocoa.m:1423:{
ui/cocoa.m:1434:{
ui/cocoa.m:1445:{
ui/cocoa.m:1458:{
ui/cocoa.m:1464:{
ui/cocoa.m:1472:{
ui/cocoa.m:1482:{
ui/cocoa.m:1503:{
ui/cocoa.m:1544:{
ui/cocoa.m:1559:{
ui/cocoa.m:1587:{
ui/cocoa.m:1622:{
ui/cocoa.m:1630:static void create_initial_menus(void)
ui/cocoa.m:1631:{
ui/cocoa.m:1722:static NSString * getConsoleName(QemuConsole * console)
ui/cocoa.m:1723:{
ui/cocoa.m:1730:static void add_console_menu_entries(void)
ui/cocoa.m:1731:{
ui/cocoa.m:1752:static void addRemovableDevicesMenuItems(void)
ui/cocoa.m:1753:{
ui/cocoa.m:1816:{
ui/cocoa.m:1849:static void cocoa_clipboard_notify(Notifier *notifier, void *data);
ui/cocoa.m:1850:static void cocoa_clipboard_request(QemuClipboardInfo *info,
ui/cocoa.m:1859:static void cocoa_clipboard_update_info(QemuClipboardInfo *info)
ui/cocoa.m:1860:{
ui/cocoa.m:1876:static void cocoa_clipboard_notify(Notifier *notifier, void *data)
ui/cocoa.m:1877:{
ui/cocoa.m:1890:static void cocoa_clipboard_request(QemuClipboardInfo *info,
ui/cocoa.m:1892:{
ui/cocoa.m:1924:static void *call_qemu_main(void *opaque)
ui/cocoa.m:1925:{
ui/cocoa.m:1937:static int cocoa_main(void)
ui/cocoa.m:1938:{
ui/cocoa.m:1958:static void cocoa_update(DisplayChangeListener *dcl,
ui/cocoa.m:1960:{
ui/cocoa.m:1978:static void cocoa_switch(DisplayChangeListener *dcl,
ui/cocoa.m:1980:{
ui/cocoa.m:1997:static void cocoa_refresh(DisplayChangeListener *dcl)
ui/cocoa.m:1998:{
ui/cocoa.m:2029:static void cocoa_display_init(DisplayState *ds, DisplayOptions *opts)
ui/cocoa.m:2030:{
ui/cocoa.m:2095:static void register_cocoa(void)
ui/cocoa.m:2096:{
ui/cocoa.m:2100:type_init(register_cocoa);
ui/console-gl.c:33:bool console_gl_check_format(DisplayChangeListener *dcl,
ui/console-gl.c:35:{
ui/console-gl.c:46:void surface_gl_create_texture(QemuGLShader *gls,
ui/console-gl.c:48:{
ui/console-gl.c:99:void surface_gl_update_texture(QemuGLShader *gls,
ui/console-gl.c:102:{
ui/console-gl.c:120:void surface_gl_render_texture(QemuGLShader *gls,
ui/console-gl.c:122:{
ui/console-gl.c:131:void surface_gl_destroy_texture(QemuGLShader *gls,
ui/console-gl.c:133:{
ui/console-gl.c:141:void surface_gl_setup_viewport(QemuGLShader *gls,
ui/console-gl.c:144:{
ui/console-vc.c:73:OBJECT_DEFINE_TYPE(QemuTextConsole, qemu_text_console, QEMU_TEXT_CONSOLE, QEMU_CONSOLE)
ui/console-vc.c:81:OBJECT_DEFINE_TYPE(QemuFixedTextConsole, qemu_fixed_text_console, QEMU_FIXED_TEXT_CONSOLE, QEMU_TEXT_CONSOLE)
ui/console-vc.c:122:qemu_text_console_get_label(QemuTextConsole *c)
ui/console-vc.c:123:{
ui/console-vc.c:127:static void qemu_console_fill_rect(QemuConsole *con, int posx, int posy,
ui/console-vc.c:129:{
ui/console-vc.c:141:static void qemu_console_bitblt(QemuConsole *con,
ui/console-vc.c:143:{
ui/console-vc.c:152:static void vga_putcharxy(QemuConsole *s, int x, int y, int ch,
ui/console-vc.c:154:{
ui/console-vc.c:175:static void invalidate_xy(QemuTextConsole *s, int x, int y)
ui/console-vc.c:176:{
ui/console-vc.c:190:static void console_show_cursor(QemuTextConsole *s, int show)
ui/console-vc.c:191:{
ui/console-vc.c:219:static void console_refresh(QemuTextConsole *s)
ui/console-vc.c:220:{
ui/console-vc.c:251:static void console_scroll(QemuTextConsole *s, int ydelta)
ui/console-vc.c:252:{
ui/console-vc.c:280:static void kbd_send_chars(QemuTextConsole *s)
ui/console-vc.c:281:{
ui/console-vc.c:298:void qemu_text_console_handle_keysym(QemuTextConsole *s, int keysym)
ui/console-vc.c:299:{
ui/console-vc.c:348:static void text_console_update(void *opaque, console_ch_t *chardata)
ui/console-vc.c:349:{
ui/console-vc.c:377:static void text_console_resize(QemuTextConsole *t)
ui/console-vc.c:378:{
ui/console-vc.c:416:static void vc_put_lf(VCChardev *vc)
ui/console-vc.c:417:{
ui/console-vc.c:465:static void vc_handle_escape(VCChardev *vc)
ui/console-vc.c:466:{
ui/console-vc.c:558:static void vc_update_xy(VCChardev *vc, int x, int y)
ui/console-vc.c:559:{
ui/console-vc.c:585:static void vc_clear_xy(VCChardev *vc, int x, int y)
ui/console-vc.c:586:{
ui/console-vc.c:598:static void vc_put_one(VCChardev *vc, int ch)
ui/console-vc.c:599:{
ui/console-vc.c:616:static void vc_respond_str(VCChardev *vc, const char *buf)
ui/console-vc.c:617:{
ui/console-vc.c:625:static void vc_set_cursor(VCChardev *vc, int x, int y)
ui/console-vc.c:626:{
ui/console-vc.c:646:static void vc_putchar(VCChardev *vc, int ch)
ui/console-vc.c:647:{
ui/console-vc.c:851:DECLARE_INSTANCE_CHECKER(VCChardev, VC_CHARDEV,
ui/console-vc.c:854:static int vc_chr_write(Chardev *chr, const uint8_t *buf, int len)
ui/console-vc.c:855:{
ui/console-vc.c:877:void qemu_text_console_update_cursor(void)
ui/console-vc.c:878:{
ui/console-vc.c:888:cursor_timer_cb(void *opaque)
ui/console-vc.c:889:{
ui/console-vc.c:893:static void text_console_invalidate(void *opaque)
ui/console-vc.c:894:{
ui/console-vc.c:904:qemu_text_console_finalize(Object *obj)
ui/console-vc.c:905:{
ui/console-vc.c:909:qemu_text_console_class_init(ObjectClass *oc, void *data)
ui/console-vc.c:910:{
ui/console-vc.c:922:qemu_text_console_init(Object *obj)
ui/console-vc.c:923:{
ui/console-vc.c:933:qemu_fixed_text_console_finalize(Object *obj)
ui/console-vc.c:934:{
ui/console-vc.c:938:qemu_fixed_text_console_class_init(ObjectClass *oc, void *data)
ui/console-vc.c:939:{
```

### Turn 3  _(tok 7550+949, stop=tool_use)_

**Reasoning:** I'm going to narrow the search instead of reading everything: first I'll pull up the lines around each call site, roughly 40 lines before, and if that gets unwieldy I'll grep for function headers in just ui/gtk.c.



- `grep(pattern=^[a-zA-Z_].*\(|^\{$, version=old, path_glob=ui/gtk.c, max_results=500)` →

```
201 matches (showing 200)
ui/gtk.c:130:DECLARE_INSTANCE_CHECKER(VCChardev, VC_CHARDEV,
ui/gtk.c:137:static void gd_grab_pointer(VirtualConsole *vc, const char *reason);
ui/gtk.c:138:static void gd_ungrab_pointer(GtkDisplayState *s);
ui/gtk.c:139:static void gd_grab_keyboard(VirtualConsole *vc, const char *reason);
ui/gtk.c:140:static void gd_ungrab_keyboard(GtkDisplayState *s);
ui/gtk.c:144:static VirtualConsole *gd_vc_find_by_menu(GtkDisplayState *s)
ui/gtk.c:145:{
ui/gtk.c:159:static VirtualConsole *gd_vc_find_by_page(GtkDisplayState *s, gint page)
ui/gtk.c:160:{
ui/gtk.c:174:static VirtualConsole *gd_vc_find_current(GtkDisplayState *s)
ui/gtk.c:175:{
ui/gtk.c:182:static bool gd_is_grab_active(GtkDisplayState *s)
ui/gtk.c:183:{
ui/gtk.c:187:static bool gd_grab_on_hover(GtkDisplayState *s)
ui/gtk.c:188:{
ui/gtk.c:192:static void gd_update_cursor(VirtualConsole *vc)
ui/gtk.c:193:{
ui/gtk.c:214:static void gd_update_caption(GtkDisplayState *s)
ui/gtk.c:215:{
ui/gtk.c:262:static void gd_update_geometry_hints(VirtualConsole *vc)
ui/gtk.c:263:{
ui/gtk.c:329:void gd_update_windowsize(VirtualConsole *vc)
ui/gtk.c:330:{
ui/gtk.c:341:static void gd_update_full_redraw(VirtualConsole *vc)
ui/gtk.c:342:{
ui/gtk.c:356:static void gtk_release_modifiers(GtkDisplayState *s)
ui/gtk.c:357:{
ui/gtk.c:367:static void gd_widget_reparent(GtkWidget *from, GtkWidget *to,
ui/gtk.c:369:{
ui/gtk.c:376:static void *gd_win32_get_hwnd(VirtualConsole *vc)
ui/gtk.c:377:{
ui/gtk.c:388:static void gd_update(DisplayChangeListener *dcl,
ui/gtk.c:390:{
ui/gtk.c:438:static void gd_refresh(DisplayChangeListener *dcl)
ui/gtk.c:439:{
ui/gtk.c:443:static GdkDevice *gd_get_pointer(GdkDisplay *dpy)
ui/gtk.c:444:{
ui/gtk.c:448:static void gd_mouse_set(DisplayChangeListener *dcl,
ui/gtk.c:450:{
ui/gtk.c:470:static void gd_cursor_define(DisplayChangeListener *dcl,
ui/gtk.c:472:{
ui/gtk.c:493:static void gd_switch(DisplayChangeListener *dcl,
ui/gtk.c:495:{
ui/gtk.c:569:static bool gd_has_dmabuf(DisplayChangeListener *dcl)
ui/gtk.c:570:{
ui/gtk.c:582:static void gd_gl_release_dmabuf(DisplayChangeListener *dcl,
ui/gtk.c:584:{
ui/gtk.c:595:void gd_hw_gl_flushed(void *vcon)
ui/gtk.c:596:{
ui/gtk.c:626:gd_gl_area_is_compatible_dcl(DisplayGLCtx *dgc,
ui/gtk.c:628:{
ui/gtk.c:660:gd_egl_is_compatible_dcl(DisplayGLCtx *dgc,
ui/gtk.c:662:{
ui/gtk.c:678:static void gd_change_runstate(void *opaque, bool running, RunState state)
ui/gtk.c:679:{
ui/gtk.c:685:static void gd_mouse_mode_change(Notifier *notify, void *data)
ui/gtk.c:686:{
ui/gtk.c:708:static gboolean gd_window_close(GtkWidget *widget, GdkEvent *event,
ui/gtk.c:710:{
ui/gtk.c:725:static void gd_set_ui_refresh_rate(VirtualConsole *vc, int refresh_rate)
ui/gtk.c:726:{
ui/gtk.c:734:static void gd_set_ui_size(VirtualConsole *vc, gint width, gint height)
ui/gtk.c:735:{
ui/gtk.c:746:static gboolean gd_render_event(GtkGLArea *area, GdkGLContext *context,
ui/gtk.c:748:{
ui/gtk.c:757:static void gd_resize_event(GtkGLArea *area,
ui/gtk.c:759:{
ui/gtk.c:767:void gd_update_monitor_refresh_rate(VirtualConsole *vc, GtkWidget *widget)
ui/gtk.c:768:{
ui/gtk.c:790:static gboolean gd_draw_event(GtkWidget *widget, cairo_t *cr, void *opaque)
ui/gtk.c:791:{
ui/gtk.c:874:static gboolean gd_motion_event(GtkWidget *widget, GdkEventMotion *motion,
ui/gtk.c:876:{
ui/gtk.c:959:static gboolean gd_button_event(GtkWidget *widget, GdkEventButton *button,
ui/gtk.c:961:{
ui/gtk.c:1002:static gboolean gd_scroll_event(GtkWidget *widget, GdkEventScroll *scroll,
ui/gtk.c:1004:{
ui/gtk.c:1067:static gboolean gd_touch_event(GtkWidget *widget, GdkEventTouch *touch,
ui/gtk.c:1069:{
ui/gtk.c:1097:static const guint16 *gd_get_keymap(size_t *maplen)
ui/gtk.c:1098:{
ui/gtk.c:1155:static int gd_map_keycode(int scancode)
ui/gtk.c:1156:{
ui/gtk.c:1167:static int gd_get_keycode(GdkEventKey *key)
ui/gtk.c:1168:{
ui/gtk.c:1186:static gboolean gd_text_key_down(GtkWidget *widget,
ui/gtk.c:1188:{
ui/gtk.c:1203:static gboolean gd_key_event(GtkWidget *widget, GdkEventKey *key, void *opaque)
ui/gtk.c:1204:{
ui/gtk.c:1246:static gboolean gd_grab_broken_event(GtkWidget *widget,
ui/gtk.c:1248:{
ui/gtk.c:1265:static gboolean gd_event(GtkWidget *widget, GdkEvent *event, void *opaque)
ui/gtk.c:1266:{
ui/gtk.c:1275:static void gd_menu_pause(GtkMenuItem *item, void *opaque)
ui/gtk.c:1276:{
ui/gtk.c:1289:static void gd_menu_reset(GtkMenuItem *item, void *opaque)
ui/gtk.c:1290:{
ui/gtk.c:1294:static void gd_menu_powerdown(GtkMenuItem *item, void *opaque)
ui/gtk.c:1295:{
ui/gtk.c:1299:static void gd_menu_quit(GtkMenuItem *item, void *opaque)
ui/gtk.c:1300:{
ui/gtk.c:1304:static void gd_menu_switch_vc(GtkMenuItem *item, void *opaque)
ui/gtk.c:1305:{
ui/gtk.c:1319:static void gd_accel_switch_vc(void *opaque)
ui/gtk.c:1320:{
ui/gtk.c:1326:static void gd_menu_show_tabs(GtkMenuItem *item, void *opaque)
ui/gtk.c:1327:{
ui/gtk.c:1339:static gboolean gd_tab_window_close(GtkWidget *widget, GdkEvent *event,
ui/gtk.c:1341:{
ui/gtk.c:1364:static gboolean gd_win_grab(void *opaque)
ui/gtk.c:1365:{
ui/gtk.c:1377:static void gd_menu_untabify(GtkMenuItem *item, void *opaque)
ui/gtk.c:1378:{
ui/gtk.c:1420:static void gd_menu_show_menubar(GtkMenuItem *item, void *opaque)
ui/gtk.c:1421:{
ui/gtk.c:1438:static void gd_accel_show_menubar(void *opaque)
ui/gtk.c:1439:{
ui/gtk.c:1444:static void gd_menu_full_screen(GtkMenuItem *item, void *opaque)
ui/gtk.c:1445:{
ui/gtk.c:1475:static void gd_accel_full_screen(void *opaque)
ui/gtk.c:1476:{
ui/gtk.c:1481:static void gd_menu_zoom_in(GtkMenuItem *item, void *opaque)
ui/gtk.c:1482:{
ui/gtk.c:1495:static void gd_accel_zoom_in(void *opaque)
ui/gtk.c:1496:{
ui/gtk.c:1501:static void gd_menu_zoom_out(GtkMenuItem *item, void *opaque)
ui/gtk.c:1502:{
ui/gtk.c:1518:static void gd_menu_zoom_fixed(GtkMenuItem *item, void *opaque)
ui/gtk.c:1519:{
ui/gtk.c:1529:static void gd_menu_zoom_fit(GtkMenuItem *item, void *opaque)
ui/gtk.c:1530:{
ui/gtk.c:1546:static void gd_grab_update(VirtualConsole *vc, bool kbd, bool ptr)
ui/gtk.c:1547:{
ui/gtk.c:1570:static void gd_grab_keyboard(VirtualConsole *vc, const char *reason)
ui/gtk.c:1571:{
ui/gtk.c:1587:static void gd_ungrab_keyboard(GtkDisplayState *s)
ui/gtk.c:1588:{
ui/gtk.c:1602:static void gd_grab_pointer(VirtualConsole *vc, const char *reason)
ui/gtk.c:1603:{
ui/gtk.c:1622:static void gd_ungrab_pointer(GtkDisplayState *s)
ui/gtk.c:1623:{
ui/gtk.c:1641:static void gd_menu_grab_input(GtkMenuItem *item, void *opaque)
ui/gtk.c:1642:{
ui/gtk.c:1657:static void gd_change_page(GtkNotebook *nb, gpointer arg1, guint arg2,
ui/gtk.c:1659:{
ui/gtk.c:1692:static gboolean gd_enter_event(GtkWidget *widget, GdkEventCrossing *crossing,
ui/gtk.c:1694:{
ui/gtk.c:1704:static gboolean gd_leave_event(GtkWidget *widget, GdkEventCrossing *crossing,
ui/gtk.c:1706:{
ui/gtk.c:1716:static gboolean gd_focus_in_event(GtkWidget *widget,
ui/gtk.c:1718:{
ui/gtk.c:1725:static gboolean gd_focus_out_event(GtkWidget *widget,
ui/gtk.c:1727:{
ui/gtk.c:1736:static gboolean gd_configure(GtkWidget *widget,
ui/gtk.c:1738:{
ui/gtk.c:1747:static GSList *gd_vc_menu_init(GtkDisplayState *s, VirtualConsole *vc,
ui/gtk.c:1749:{
ui/gtk.c:1766:static void gd_menu_copy(GtkMenuItem *item, void *opaque)
ui/gtk.c:1767:{
ui/gtk.c:1779:static void gd_vc_adjustment_changed(GtkAdjustment *adjustment, void *opaque)
ui/gtk.c:1780:{
ui/gtk.c:1791:static void gd_vc_send_chars(VirtualConsole *vc)
ui/gtk.c:1792:{
ui/gtk.c:1808:static int gd_vc_chr_write(Chardev *chr, const uint8_t *buf, int len)
ui/gtk.c:1809:{
ui/gtk.c:1817:static void gd_vc_chr_accept_input(Chardev *chr)
ui/gtk.c:1818:{
ui/gtk.c:1827:static void gd_vc_chr_set_echo(Chardev *chr, bool echo)
ui/gtk.c:1828:{
ui/gtk.c:1841:static void gd_vc_open(Chardev *chr,
ui/gtk.c:1845:{
ui/gtk.c:1859:static void char_gd_vc_class_init(ObjectClass *oc, void *data)
ui/gtk.c:1860:{
ui/gtk.c:1876:static gboolean gd_vc_in(VteTerminal *terminal, gchar *text, guint size,
ui/gtk.c:1878:{
ui/gtk.c:1907:static GSList *gd_vc_vte_init(GtkDisplayState *s, VirtualConsole *vc,
ui/gtk.c:1910:{
ui/gtk.c:1976:static void gd_vcs_init(GtkDisplayState *s, GSList *group,
ui/gtk.c:1978:{
ui/gtk.c:1991:static void gd_connect_vc_gfx_signals(VirtualConsole *vc)
ui/gtk.c:1992:{
ui/gtk.c:2038:static void gd_connect_signals(GtkDisplayState *s)
ui/gtk.c:2039:{
ui/gtk.c:2078:static GtkWidget *gd_create_menu_machine(GtkDisplayState *s)
ui/gtk.c:2079:{
ui/gtk.c:2112:static void gl_area_realize(GtkGLArea *area, VirtualConsole *vc)
ui/gtk.c:2113:{
ui/gtk.c:2123:static GSList *gd_vc_gfx_init(GtkDisplayState *s, VirtualConsole *vc,
ui/gtk.c:2126:{
ui/gtk.c:2220:static GtkWidget *gd_create_menu_view(GtkDisplayState *s, DisplayOptions *opts)
ui/gtk.c:2221:{
ui/gtk.c:2330:static void gd_create_menus(GtkDisplayState *s, DisplayOptions *opts)
ui/gtk.c:2331:{
ui/gtk.c:2358:static void gtk_display_init(DisplayState *ds, DisplayOptions *opts)
ui/gtk.c:2359:{
ui/gtk.c:2458:static void early_gtk_display_init(DisplayOptions *opts)
ui/gtk.c:2459:{
ui/gtk.c:2521:static void register_gtk(void)
ui/gtk.c:2522:{
ui/gtk.c:2526:type_init(register_gtk);
```

- `grep(pattern=^[a-zA-Z_].*\(|^\{$, version=old, path_glob=ui/sdl2.c, max_results=500)` →

```
65 matches
ui/sdl2.c:66:static void sdl_update_caption(struct sdl2_console *scon);
ui/sdl2.c:68:static struct sdl2_console *get_scon_from_window(uint32_t window_id)
ui/sdl2.c:69:{
ui/sdl2.c:79:void sdl2_window_create(struct sdl2_console *scon)
ui/sdl2.c:80:{
ui/sdl2.c:125:void sdl2_window_destroy(struct sdl2_console *scon)
ui/sdl2.c:126:{
ui/sdl2.c:143:void sdl2_window_resize(struct sdl2_console *scon)
ui/sdl2.c:144:{
ui/sdl2.c:154:static void sdl2_redraw(struct sdl2_console *scon)
ui/sdl2.c:155:{
ui/sdl2.c:165:static void sdl_update_caption(struct sdl2_console *scon)
ui/sdl2.c:166:{
ui/sdl2.c:197:static void sdl_hide_cursor(struct sdl2_console *scon)
ui/sdl2.c:198:{
ui/sdl2.c:211:static void sdl_show_cursor(struct sdl2_console *scon)
ui/sdl2.c:212:{
ui/sdl2.c:231:static void sdl_grab_start(struct sdl2_console *scon)
ui/sdl2.c:232:{
ui/sdl2.c:260:static void sdl_grab_end(struct sdl2_console *scon)
ui/sdl2.c:261:{
ui/sdl2.c:269:static void absolute_mouse_grab(struct sdl2_console *scon)
ui/sdl2.c:270:{
ui/sdl2.c:281:static void sdl_mouse_mode_change(Notifier *notify, void *data)
ui/sdl2.c:282:{
ui/sdl2.c:297:static void sdl_send_mouse_event(struct sdl2_console *scon, int dx, int dy,
ui/sdl2.c:299:{
ui/sdl2.c:334:static void toggle_full_screen(struct sdl2_console *scon)
ui/sdl2.c:335:{
ui/sdl2.c:351:static int get_mod_state(void)
ui/sdl2.c:352:{
ui/sdl2.c:365:static void *sdl2_win32_get_hwnd(struct sdl2_console *scon)
ui/sdl2.c:366:{
ui/sdl2.c:378:static void handle_keydown(SDL_Event *ev)
ui/sdl2.c:379:{
ui/sdl2.c:465:static void handle_keyup(SDL_Event *ev)
ui/sdl2.c:466:{
ui/sdl2.c:477:static void handle_textinput(SDL_Event *ev)
ui/sdl2.c:478:{
ui/sdl2.c:491:static void handle_mousemotion(SDL_Event *ev)
ui/sdl2.c:492:{
ui/sdl2.c:522:static void handle_mousebutton(SDL_Event *ev)
ui/sdl2.c:523:{
ui/sdl2.c:548:static void handle_mousewheel(SDL_Event *ev)
ui/sdl2.c:549:{
ui/sdl2.c:576:static void handle_windowevent(SDL_Event *ev)
ui/sdl2.c:577:{
ui/sdl2.c:655:void sdl2_poll_events(struct sdl2_console *scon)
ui/sdl2.c:656:{
ui/sdl2.c:723:static void sdl_mouse_warp(DisplayChangeListener *dcl,
ui/sdl2.c:725:{
ui/sdl2.c:749:static void sdl_mouse_define(DisplayChangeListener *dcl,
ui/sdl2.c:751:{
ui/sdl2.c:781:static void sdl_cleanup(void)
ui/sdl2.c:782:{
ui/sdl2.c:815:sdl2_gl_is_compatible_dcl(DisplayGLCtx *dgc,
ui/sdl2.c:817:{
ui/sdl2.c:829:static void sdl2_display_early_init(DisplayOptions *o)
ui/sdl2.c:830:{
ui/sdl2.c:839:static void sdl2_display_init(DisplayState *ds, DisplayOptions *o)
ui/sdl2.c:840:{
ui/sdl2.c:964:static void register_sdl1(void)
ui/sdl2.c:965:{
ui/sdl2.c:969:type_init(register_sdl1);
ui/sdl2.c:972:module_dep("ui-opengl");
```

- `grep(pattern=^[a-zA-Z_].*\(|^\{$, version=old, path_glob=ui/dbus-console.c, max_results=500)` →

```
53 matches
ui/dbus-console.c:58:G_DEFINE_TYPE(DBusDisplayConsole,
ui/dbus-console.c:63:dbus_display_console_set_size(DBusDisplayConsole *ddc,
ui/dbus-console.c:65:{
ui/dbus-console.c:73:dbus_gfx_switch(DisplayChangeListener *dcl,
ui/dbus-console.c:75:{
ui/dbus-console.c:84:dbus_gfx_update(DisplayChangeListener *dcl,
ui/dbus-console.c:86:{
ui/dbus-console.c:90:dbus_gl_scanout_disable(DisplayChangeListener *dcl)
ui/dbus-console.c:91:{
ui/dbus-console.c:95:dbus_gl_scanout_texture(DisplayChangeListener *dcl,
ui/dbus-console.c:103:{
ui/dbus-console.c:110:dbus_gl_scanout_dmabuf(DisplayChangeListener *dcl,
ui/dbus-console.c:112:{
ui/dbus-console.c:121:dbus_gl_scanout_update(DisplayChangeListener *dcl,
ui/dbus-console.c:124:{
ui/dbus-console.c:138:dbus_display_console_init(DBusDisplayConsole *object)
ui/dbus-console.c:139:{
ui/dbus-console.c:148:dbus_display_console_dispose(GObject *object)
ui/dbus-console.c:149:{
ui/dbus-console.c:164:dbus_display_console_class_init(DBusDisplayConsoleClass *klass)
ui/dbus-console.c:165:{
ui/dbus-console.c:172:listener_vanished_cb(DBusDisplayListener *listener)
ui/dbus-console.c:173:{
ui/dbus-console.c:184:dbus_console_set_ui_info(DBusDisplayConsole *ddc,
ui/dbus-console.c:192:{
ui/dbus-console.c:217:dbus_win32_import_socket(GDBusMethodInvocation *invocation,
ui/dbus-console.c:219:{
ui/dbus-console.c:251:dbus_console_register_listener(DBusDisplayConsole *ddc,
ui/dbus-console.c:257:{
ui/dbus-console.c:343:dbus_kbd_press(DBusDisplayConsole *ddc,
ui/dbus-console.c:346:{
ui/dbus-console.c:359:dbus_kbd_release(DBusDisplayConsole *ddc,
ui/dbus-console.c:362:{
ui/dbus-console.c:375:dbus_kbd_qemu_leds_updated(void *data, int ledstate)
ui/dbus-console.c:376:{
ui/dbus-console.c:383:dbus_mouse_rel_motion(DBusDisplayConsole *ddc,
ui/dbus-console.c:386:{
ui/dbus-console.c:408:dbus_touch_send_event(DBusDisplayConsole *ddc,
ui/dbus-console.c:412:{
ui/dbus-console.c:448:dbus_mouse_set_pos(DBusDisplayConsole *ddc,
ui/dbus-console.c:451:{
ui/dbus-console.c:484:dbus_mouse_press(DBusDisplayConsole *ddc,
ui/dbus-console.c:487:{
ui/dbus-console.c:499:dbus_mouse_release(DBusDisplayConsole *ddc,
ui/dbus-console.c:502:{
ui/dbus-console.c:514:dbus_mouse_update_is_absolute(DBusDisplayConsole *ddc)
ui/dbus-console.c:515:{
ui/dbus-console.c:522:dbus_mouse_mode_change(Notifier *notify, void *data)
ui/dbus-console.c:523:{
ui/dbus-console.c:530:int dbus_display_console_get_index(DBusDisplayConsole *ddc)
ui/dbus-console.c:531:{
ui/dbus-console.c:536:dbus_display_console_new(DBusDisplay *display, QemuConsole *con)
ui/dbus-console.c:537:{
```

- `grep(pattern=^[a-zA-Z_].*\(|^\{$, version=old, path_glob=ui/input.c, max_results=500)` →

```
75 matches
ui/input.c:21:typedef QTAILQ_HEAD(QemuInputEventQueueHead, QemuInputEventQueue)
ui/input.c:37:static QTAILQ_HEAD(, QemuInputHandlerState) handlers =
ui/input.c:42:static QemuInputEventQueueHead kbd_queue = QTAILQ_HEAD_INITIALIZER(kbd_queue);
ui/input.c:48:QemuInputHandlerState *qemu_input_handler_register(DeviceState *dev,
ui/input.c:50:{
ui/input.c:63:void qemu_input_handler_activate(QemuInputHandlerState *s)
ui/input.c:64:{
ui/input.c:70:void qemu_input_handler_deactivate(QemuInputHandlerState *s)
ui/input.c:71:{
ui/input.c:77:void qemu_input_handler_unregister(QemuInputHandlerState *s)
ui/input.c:78:{
ui/input.c:84:void qemu_input_handler_bind(QemuInputHandlerState *s,
ui/input.c:87:{
ui/input.c:101:qemu_input_find_handler(uint32_t mask, QemuConsole *con)
ui/input.c:102:{
ui/input.c:125:void qmp_input_send_event(const char *device,
ui/input.c:128:{
ui/input.c:177:static int qemu_input_transform_invert_abs_value(int value)
ui/input.c:178:{
ui/input.c:182:static void qemu_input_transform_abs_rotate(InputEvent *evt)
ui/input.c:183:{
ui/input.c:208:static void qemu_input_event_trace(QemuConsole *src, InputEvent *evt)
ui/input.c:209:{
ui/input.c:265:static void qemu_input_queue_process(void *opaque)
ui/input.c:266:{
ui/input.c:298:static void qemu_input_queue_delay(QemuInputEventQueueHead *queue,
ui/input.c:300:{
ui/input.c:316:static void qemu_input_queue_event(QemuInputEventQueueHead *queue,
ui/input.c:318:{
ui/input.c:328:static void qemu_input_queue_sync(QemuInputEventQueueHead *queue)
ui/input.c:329:{
ui/input.c:337:void qemu_input_event_send_impl(QemuConsole *src, InputEvent *evt)
ui/input.c:338:{
ui/input.c:357:void qemu_input_event_send(QemuConsole *src, InputEvent *evt)
ui/input.c:358:{
ui/input.c:385:void qemu_input_event_sync_impl(void)
ui/input.c:386:{
ui/input.c:402:void qemu_input_event_sync(void)
ui/input.c:403:{
ui/input.c:411:static InputEvent *qemu_input_event_new_key(KeyValue *key, bool down)
ui/input.c:412:{
ui/input.c:421:void qemu_input_event_send_key(QemuConsole *src, KeyValue *key, bool down)
ui/input.c:422:{
ui/input.c:437:void qemu_input_event_send_key_number(QemuConsole *src, int num, bool down)
ui/input.c:438:{
ui/input.c:443:void qemu_input_event_send_key_qcode(QemuConsole *src, QKeyCode q, bool down)
ui/input.c:444:{
ui/input.c:451:void qemu_input_event_send_key_delay(uint32_t delay_ms)
ui/input.c:452:{
ui/input.c:468:void qemu_input_queue_btn(QemuConsole *src, InputButton btn, bool down)
ui/input.c:469:{
ui/input.c:482:void qemu_input_update_buttons(QemuConsole *src, uint32_t *button_map,
ui/input.c:484:{
ui/input.c:497:bool qemu_input_is_absolute(void)
ui/input.c:498:{
ui/input.c:506:int qemu_input_scale_axis(int value,
ui/input.c:509:{
ui/input.c:519:void qemu_input_queue_rel(QemuConsole *src, InputAxis axis, int value)
ui/input.c:520:{
ui/input.c:533:void qemu_input_queue_abs(QemuConsole *src, InputAxis axis, int value,
ui/input.c:535:{
ui/input.c:550:void qemu_input_queue_mtt(QemuConsole *src, InputMultiTouchType type,
ui/input.c:552:{
ui/input.c:566:void qemu_input_queue_mtt_abs(QemuConsole *src, InputAxis axis, int value,
ui/input.c:568:{
ui/input.c:586:void qemu_input_check_mode_change(void)
ui/input.c:587:{
ui/input.c:601:void qemu_add_mouse_mode_change_notifier(Notifier *notify)
ui/input.c:602:{
ui/input.c:606:void qemu_remove_mouse_mode_change_notifier(Notifier *notify)
ui/input.c:607:{
ui/input.c:611:MouseInfoList *qmp_query_mice(Error **errp)
ui/input.c:612:{
ui/input.c:637:bool qemu_mouse_set(int index, Error **errp)
ui/input.c:638:{
```

- `grep(pattern=^[a-zA-Z_].*\(|^\{$, version=old, path_glob=ui/vnc.c, max_results=500)` →

```
265 matches (showing 200)
ui/vnc.c:68:static QTAILQ_HEAD(, VncDisplay) vnc_displays =
ui/vnc.c:71:static int vnc_cursor_define(VncState *vs);
ui/vnc.c:72:static void vnc_update_throttle_offset(VncState *vs);
ui/vnc.c:74:static void vnc_set_share_mode(VncState *vs, VncShareMode mode)
ui/vnc.c:75:{
ui/vnc.c:120:static void vnc_init_basic_info(SocketAddress *addr,
ui/vnc.c:123:{
ui/vnc.c:153:static void vnc_init_basic_info_from_server_addr(QIOChannelSocket *ioc,
ui/vnc.c:156:{
ui/vnc.c:173:static void vnc_init_basic_info_from_remote_addr(QIOChannelSocket *ioc,
ui/vnc.c:176:{
ui/vnc.c:188:static const char *vnc_auth_name(VncDisplay *vd) {
ui/vnc.c:235:static VncServerInfo *vnc_server_info_get(VncDisplay *vd)
ui/vnc.c:236:{
ui/vnc.c:256:static void vnc_client_cache_auth(VncState *client)
ui/vnc.c:257:{
ui/vnc.c:274:static void vnc_client_cache_addr(VncState *client)
ui/vnc.c:275:{
ui/vnc.c:290:static void vnc_qmp_event(VncState *vs, QAPIEvent event)
ui/vnc.c:291:{
ui/vnc.c:320:static VncClientInfo *qmp_query_vnc_client(const VncState *client)
ui/vnc.c:321:{
ui/vnc.c:350:static VncDisplay *vnc_display_find(const char *id)
ui/vnc.c:351:{
ui/vnc.c:365:static VncClientInfoList *qmp_query_client_list(VncDisplay *vd)
ui/vnc.c:366:{
ui/vnc.c:376:VncInfo *qmp_query_vnc(Error **errp)
ui/vnc.c:377:{
ui/vnc.c:438:static void qmp_query_auth(int auth, int subauth,
ui/vnc.c:443:static VncServerInfo2List *qmp_query_server_entry(QIOChannelSocket *ioc,
ui/vnc.c:448:{
ui/vnc.c:475:static void qmp_query_auth(int auth, int subauth,
ui/vnc.c:479:{
ui/vnc.c:545:VncInfo2List *qmp_query_vnc_servers(Error **errp)
ui/vnc.c:546:{
ui/vnc.c:580:bool vnc_display_reload_certs(const char *id, Error **errp)
ui/vnc.c:581:{
ui/vnc.c:615:static int vnc_update_client(VncState *vs, int has_dirty);
ui/vnc.c:616:static void vnc_disconnect_start(VncState *vs);
ui/vnc.c:618:static void vnc_colordepth(VncState *vs);
ui/vnc.c:619:static void framebuffer_update_request(VncState *vs, int incremental,
ui/vnc.c:622:static void vnc_refresh(DisplayChangeListener *dcl);
ui/vnc.c:623:static int vnc_refresh_server_surface(VncDisplay *vd);
ui/vnc.c:625:static int vnc_width(VncDisplay *vd)
ui/vnc.c:626:{
ui/vnc.c:631:static int vnc_true_width(VncDisplay *vd)
ui/vnc.c:632:{
ui/vnc.c:636:static int vnc_height(VncDisplay *vd)
ui/vnc.c:637:{
ui/vnc.c:641:static void vnc_set_area_dirty(DECLARE_BITMAP(dirty[VNC_MAX_HEIGHT],
ui/vnc.c:645:{
ui/vnc.c:665:static void vnc_dpy_update(DisplayChangeListener *dcl,
ui/vnc.c:667:{
ui/vnc.c:674:void vnc_framebuffer_update(VncState *vs, int x, int y, int w, int h,
ui/vnc.c:676:{
ui/vnc.c:685:static void vnc_desktop_resize_ext(VncState *vs, int reject_reason)
ui/vnc.c:686:{
ui/vnc.c:713:static void vnc_desktop_resize(VncState *vs)
ui/vnc.c:714:{
ui/vnc.c:749:static void vnc_abort_display_jobs(VncDisplay *vd)
ui/vnc.c:750:{
ui/vnc.c:774:int vnc_server_fb_stride(VncDisplay *vd)
ui/vnc.c:775:{
ui/vnc.c:779:void *vnc_server_fb_ptr(VncDisplay *vd, int x, int y)
ui/vnc.c:780:{
ui/vnc.c:789:static void vnc_update_server_surface(VncDisplay *vd)
ui/vnc.c:790:{
ui/vnc.c:812:static bool vnc_check_pageflip(DisplaySurface *s1,
ui/vnc.c:814:{
ui/vnc.c:823:static void vnc_dpy_switch(DisplayChangeListener *dcl,
ui/vnc.c:825:{
ui/vnc.c:870:static void vnc_write_pixels_copy(VncState *vs,
ui/vnc.c:872:{
ui/vnc.c:877:void vnc_convert_pixel(VncState *vs, uint8_t *buf, uint32_t v)
ui/vnc.c:878:{
ui/vnc.c:921:static void vnc_write_pixels_generic(VncState *vs,
ui/vnc.c:923:{
ui/vnc.c:937:int vnc_raw_send_framebuffer_update(VncState *vs, int x, int y, int w, int h)
ui/vnc.c:938:{
ui/vnc.c:951:int vnc_send_framebuffer_update(VncState *vs, int x, int y, int w, int h)
ui/vnc.c:952:{
ui/vnc.c:983:static void vnc_mouse_set(DisplayChangeListener *dcl,
ui/vnc.c:985:{
ui/vnc.c:989:static int vnc_cursor_define(VncState *vs)
ui/vnc.c:990:{
ui/vnc.c:1026:static void vnc_dpy_cursor_define(DisplayChangeListener *dcl,
ui/vnc.c:1028:{
ui/vnc.c:1042:static int find_and_clear_dirty_height(VncState *vs,
ui/vnc.c:1044:{
ui/vnc.c:1067:static void vnc_update_throttle_offset(VncState *vs)
ui/vnc.c:1068:{
ui/vnc.c:1107:static bool vnc_should_update(VncState *vs)
ui/vnc.c:1108:{
ui/vnc.c:1144:static int vnc_update_client(VncState *vs, int has_dirty)
ui/vnc.c:1145:{
ui/vnc.c:1215:static void audio_capture_notify(void *opaque, audcnotification_e cmd)
ui/vnc.c:1216:{
ui/vnc.c:1243:static void audio_capture_destroy(void *opaque)
ui/vnc.c:1244:{
ui/vnc.c:1247:static void audio_capture(void *opaque, const void *buf, int size)
ui/vnc.c:1248:{
ui/vnc.c:1267:static void audio_add(VncState *vs)
ui/vnc.c:1268:{
ui/vnc.c:1286:static void audio_del(VncState *vs)
ui/vnc.c:1287:{
ui/vnc.c:1294:static void vnc_disconnect_start(VncState *vs)
ui/vnc.c:1295:{
ui/vnc.c:1309:void vnc_disconnect_finish(VncState *vs)
ui/vnc.c:1310:{
ui/vnc.c:1370:size_t vnc_client_io_error(VncState *vs, ssize_t ret, Error *err)
ui/vnc.c:1371:{
ui/vnc.c:1389:void vnc_client_error(VncState *vs)
ui/vnc.c:1390:{
ui/vnc.c:1411:size_t vnc_client_write_buf(VncState *vs, const uint8_t *data, size_t datalen)
ui/vnc.c:1412:{
ui/vnc.c:1431:static size_t vnc_client_write_plain(VncState *vs)
ui/vnc.c:1432:{
ui/vnc.c:1486:static void vnc_client_write_locked(VncState *vs)
ui/vnc.c:1487:{
ui/vnc.c:1500:static void vnc_client_write(VncState *vs)
ui/vnc.c:1501:{
ui/vnc.c:1517:void vnc_read_when(VncState *vs, VncReadEvent *func, size_t expecting)
ui/vnc.c:1518:{
ui/vnc.c:1539:size_t vnc_client_read_buf(VncState *vs, uint8_t *data, size_t datalen)
ui/vnc.c:1540:{
ui/vnc.c:1558:static size_t vnc_client_read_plain(VncState *vs)
ui/vnc.c:1559:{
ui/vnc.c:1571:static void vnc_jobs_bh(void *opaque)
ui/vnc.c:1572:{
ui/vnc.c:1585:static int vnc_client_read(VncState *vs)
ui/vnc.c:1586:{
ui/vnc.c:1622:gboolean vnc_client_io(QIOChannel *ioc G_GNUC_UNUSED,
ui/vnc.c:1624:{
ui/vnc.c:1663:void vnc_write(VncState *vs, const void *data, size_t len)
ui/vnc.c:1664:{
ui/vnc.c:1702:void vnc_write_s32(VncState *vs, int32_t value)
ui/vnc.c:1703:{
ui/vnc.c:1707:void vnc_write_u32(VncState *vs, uint32_t value)
ui/vnc.c:1708:{
ui/vnc.c:1719:void vnc_write_u16(VncState *vs, uint16_t value)
ui/vnc.c:1720:{
ui/vnc.c:1729:void vnc_write_u8(VncState *vs, uint8_t value)
ui/vnc.c:1730:{
ui/vnc.c:1734:void vnc_flush(VncState *vs)
ui/vnc.c:1735:{
ui/vnc.c:1749:static uint8_t read_u8(uint8_t *data, size_t offset)
ui/vnc.c:1750:{
ui/vnc.c:1754:static uint16_t read_u16(uint8_t *data, size_t offset)
ui/vnc.c:1755:{
ui/vnc.c:1759:static int32_t read_s32(uint8_t *data, size_t offset)
ui/vnc.c:1760:{
ui/vnc.c:1765:uint32_t read_u32(uint8_t *data, size_t offset)
ui/vnc.c:1766:{
ui/vnc.c:1771:static void check_pointer_type_change(Notifier *notifier, void *data)
ui/vnc.c:1772:{
ui/vnc.c:1791:static void pointer_event(VncState *vs, int button_mask, int x, int y)
ui/vnc.c:1792:{
ui/vnc.c:1826:static void press_key(VncState *vs, QKeyCode qcode)
ui/vnc.c:1827:{
ui/vnc.c:1832:static void vnc_led_state_change(VncState *vs)
ui/vnc.c:1833:{
ui/vnc.c:1848:static void kbd_leds(void *opaque, int ledstate)
ui/vnc.c:1849:{
ui/vnc.c:1868:static void do_key_event(VncState *vs, int down, int keycode, int sym)
ui/vnc.c:1869:{
ui/vnc.c:2037:static const char *code2name(int keycode)
ui/vnc.c:2038:{
ui/vnc.c:2042:static void key_event(VncState *vs, int down, uint32_t sym)
ui/vnc.c:2043:{
ui/vnc.c:2057:static void ext_key_event(VncState *vs, int down,
ui/vnc.c:2059:{
ui/vnc.c:2069:static void framebuffer_update_request(VncState *vs, int incremental,
ui/vnc.c:2071:{
ui/vnc.c:2085:static void send_ext_key_event_ack(VncState *vs)
ui/vnc.c:2086:{
ui/vnc.c:2099:static void send_ext_audio_ack(VncState *vs)
ui/vnc.c:2100:{
ui/vnc.c:2113:static void send_xvp_message(VncState *vs, int code)
ui/vnc.c:2114:{
ui/vnc.c:2124:static void set_encodings(VncState *vs, int32_t *encodings, size_t n_encodings)
ui/vnc.c:2125:{
ui/vnc.c:2235:static void set_pixel_conversion(VncState *vs)
ui/vnc.c:2236:{
ui/vnc.c:2248:static void send_color_map(VncState *vs)
ui/vnc.c:2249:{
ui/vnc.c:2268:static void set_pixel_format(VncState *vs, int bits_per_pixel,
ui/vnc.c:2272:{
ui/vnc.c:2321:static void pixel_format_message (VncState *vs) {
ui/vnc.c:2347:static void vnc_colordepth(VncState *vs)
ui/vnc.c:2348:{
ui/vnc.c:2367:static int protocol_client_msg(VncState *vs, uint8_t *data, size_t len)
ui/vnc.c:2368:{
ui/vnc.c:2609:static int protocol_client_init(VncState *vs, uint8_t *data, size_t len)
ui/vnc.c:2610:{
ui/vnc.c:2710:void start_client_init(VncState *vs)
ui/vnc.c:2711:{
ui/vnc.c:2715:static void authentication_failed(VncState *vs)
ui/vnc.c:2716:{
ui/vnc.c:2728:vnc_munge_des_rfb_key(unsigned char *key, size_t nkey)
ui/vnc.c:2729:{
```

- `grep(pattern=^[a-zA-Z_].*\(|^\{$, version=old, path_glob=ui/spice-input.c, max_results=500)` →

```
26 matches
ui/spice-input.c:37:static void kbd_push_key(SpiceKbdInstance *sin, uint8_t frag);
ui/spice-input.c:38:static uint8_t kbd_get_leds(SpiceKbdInstance *sin);
ui/spice-input.c:49:static void kbd_push_key(SpiceKbdInstance *sin, uint8_t scancode)
ui/spice-input.c:50:{
ui/spice-input.c:82:static uint8_t kbd_get_leds(SpiceKbdInstance *sin)
ui/spice-input.c:83:{
ui/spice-input.c:88:static void kbd_leds(void *opaque, int ledstate)
ui/spice-input.c:89:{
ui/spice-input.c:116:static void spice_update_buttons(QemuSpicePointer *pointer,
ui/spice-input.c:118:{
ui/spice-input.c:143:static void mouse_motion(SpiceMouseInstance *sin, int dx, int dy, int dz,
ui/spice-input.c:145:{
ui/spice-input.c:153:static void mouse_buttons(SpiceMouseInstance *sin, uint32_t buttons_state)
ui/spice-input.c:154:{
ui/spice-input.c:169:static void tablet_set_logical_size(SpiceTabletInstance* sin, int width, int height)
ui/spice-input.c:170:{
ui/spice-input.c:183:static void tablet_position(SpiceTabletInstance* sin, int x, int y,
ui/spice-input.c:185:{
ui/spice-input.c:195:static void tablet_wheel(SpiceTabletInstance* sin, int wheel,
ui/spice-input.c:197:{
ui/spice-input.c:204:static void tablet_buttons(SpiceTabletInstance *sin,
ui/spice-input.c:206:{
ui/spice-input.c:224:static void mouse_mode_notifier(Notifier *notifier, void *data)
ui/spice-input.c:225:{
ui/spice-input.c:241:void qemu_spice_input_init(void)
ui/spice-input.c:242:{
```

### Turn 4  _(tok 25115+3509, stop=tool_use)_

**Reasoning:** I'm mapping each call-site line to the function that contains it. The cocoa.m call at line 2004 falls inside cocoa_refresh, which runs from 1997 to 2028, since cocoa_display_init starts at 2029. The dbus-console.c calls at 389, 456 and 517 sit in dbus_mouse_rel_motion (from 383) and dbus_mouse_set_pos (from 448), and I'm now checking the third one.

Now I'm matching the remaining call-site lines to their enclosing functions, mostly across the gtk.c and sdl2.c ranges.

I'm checking the sdl2.c call sites at 736 and 738, which both fall inside sdl_mouse_warp (723-748). The one at 776 looks different: it sits past that range, in sdl_mouse_define (749-780), so I need to read the file to confirm that before I trust it.

Now I'm pinning down the spice-input.c call at 227, which falls in mouse_mode_notifier (224-240), and the vnc.c call at 1774, which sits in check_pointer_type_change (1771-1790). Next I want to re-read a handful of the ambiguous sdl2.c and gtk.c lines against their function ranges, since the grep output alone might be missing some headers.

I'm checking the remaining call-site lines against their enclosing functions, mostly to confirm the sdl2.c and gtk.c boundaries. The grep covered the whole repo, and every match is in ui/, so there are no hidden call sites elsewhere.

I'm confirming that the gtk.c call at 207 belongs to gd_update_cursor, since it sits before gd_update_caption at 214. The sdl2.c call at 776 falls inside sdl_mouse_define (749 to 781), and I'm also checking input.c at 591 against qemu_input_check_mode_change (586 to 600).

I'm settling on the final list of the functions that contain these call sites, one entry per function with its file, and the last entry is still being written.

Still listing the remaining sdl2.c, spice-input.c and vnc.c functions for the final list...

Checking the last few call sites against their function ranges: sdl2.c 283 falls in sdl_mouse_mode_change, 314 in sdl_send_mouse_event, and vnc.c 1774 in check_pointer_type_change. The hide and show cursor boundaries also look right from the grep output.

I'm tallying the call sites: 26 real calls once the definition, prototype and comment are excluded, and checking that the list of enclosing functions covers each one, including the sdl2.c lines in the hide, show, grab, mode-change, mouse-event and window-event handlers.

I'm finishing the tally of call sites by function: the handle_mousemotion lines at 500 and 516 both fall within its range, 533 sits in handle_mousebutton, and 606 in handle_windowevent. Adding it up, the lines come to 26, which matches the expected count.



- **submit_callers** → `{"callers": [{"function": "cocoa_refresh", "file": "ui/cocoa.m"}, {"function": "dbus_mouse_rel_motion", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_set_pos", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_update_is_absolute", "file": "ui/dbus-console.c"}, {"function": "gd_update_cursor", "file": "ui/gtk.c"}, {"function": "gd_mouse_set", "file": "ui/gtk.c"}, {"function": "gd_mouse_mode_change", "file": "ui/gtk.c"}, {"function": "gd_motion_event", "file": "ui/gtk.c"}, {"function": "gd_button_event", "file": "ui/gtk.c"}, {"function": "qemu_input_check_mode_change", "file": "ui/input.c"}, {"function": "sdl_hide_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_show_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_grab_start", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_mode_change", "file": "ui/sdl2.c"}, {"function": "sdl_send_mouse_event", "file": "ui/sdl2.c"}, {"function": "handle_mousemotion", "file": "ui/sdl2.c"}, {"function": "handle_mousebutton", "file": "ui/sdl2.c"}, {"function": "handle_windowevent", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_warp", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_define", "file": "ui/sdl2.c"}, {"function": "mouse_mode_notifier", "file": "ui/spice-input.c"}, {"function": "check_pointer_type_change", "file": "ui/vnc.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 22, "n_truth": 22, "tp": 22, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1387+75, stop=tool_use)_

**Reasoning:** I'm going to start by running find_references on the symbol to see where it's used.



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

### Turn 2  _(tok 2706+1204, stop=tool_use)_

**Reasoning:** I'm going through the reference list now: 26 call sites spread across dbus-console.c, gtk.c, input.c, sdl2.c, spice-input.c, and vnc.c. I need to find the enclosing function for each one, so I'll read the surrounding lines in batches rather than one at a time.

I'm going to search for function definitions in the ui/*.c files so I can map each call site to its enclosing function, rather than reading each range one at a time.



- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ui/dbus-console.c, max_results=500)` →

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

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ui/gtk.c, max_results=500)` →

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

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ui/input.c, max_results=500)` →

```
38 matches
ui/input.c:21:typedef QTAILQ_HEAD(QemuInputEventQueueHead, QemuInputEventQueue)
ui/input.c:37:static QTAILQ_HEAD(, QemuInputHandlerState) handlers =
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

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ui/sdl2.c, max_results=500)` →

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

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ui/spice-input.c, max_results=500)` →

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

- `grep(pattern=^[A-Za-z_][A-Za-z_0-9 \*]*\(, version=old, path_glob=ui/vnc.c, max_results=500)` →

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

### Turn 3  _(tok 17748+1890, stop=tool_use)_

**Reasoning:** I'm mapping each reference in dbus-console.c and gtk.c to the function that encloses it. Line 389 falls inside dbus_mouse_rel_motion, 456 inside dbus_mouse_set_pos, and 517 inside dbus_mouse_update_is_absolute. In gtk.c, 207 is inside gd_update_cursor and 456 inside gd_mouse_set, and I'm still checking the one at 692.

I'm checking the remaining references against their enclosing functions: 692 falls in gd_mouse_mode_change, and the 906 and 926 hits both land in gd_motion_event rather than gd_draw_event, with 968 inside gd_button_event. The input.c reference at 591 sits in qemu_input_check_mode_change, and I'm now matching the sdl2.c line numbers to their functions, starting with 206 in sdl_hide_cursor.

I'm working through the remaining sdl2.c references, matching each line to its enclosing function: 283 falls in sdl_mouse_mode_change, 314 in sdl_send_mouse_event, and 500 and 516 in handle_mousemotion. I'm also placing 533 in handle_mousebutton, 606 in handle_windowevent, 736 and 738 in sdl_mouse_warp, and 776 in sdl_mouse_define, then checking the spice-input.c and vnc.c hits.

I'm double-checking the function boundaries near the edges, since the grep only catches functions whose name sits on the same line as the signature, so a static helper defined across two lines could be missed. The sdl2.c hits around 206 and 222 look clean, but I still need to confirm the vnc.c reference at 1774 falls inside check_pointer_type_change.

I'm going to check the gtk.c region between 874 and 960 for any function header the grep might have missed, since a helper defined across two lines could sit in that gap. The line numbers from the references are fixed, so I'm only confirming that nothing unmatched hides between the known function starts.

I'm checking whether the grep pattern could miss any function definitions, especially ones that start at column 0 without a parenthesis on the same line. The current regex only catches signatures where the return type and name sit together before the opening paren, so an unusual return type could slip past. The references themselves are fixed, though, so I'm mainly asking whether any hidden helper could sit between the known function starts.

I'm going to check whether the index missed any references by grepping the whole repo for qemu_input_is_absolute, since git grep covers all tracked files including any #ifdef'd code.



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

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 4  _(tok 20861+678, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "dbus_mouse_rel_motion", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_set_pos", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_update_is_absolute", "file": "ui/dbus-console.c"}, {"function": "gd_update_cursor", "file": "ui/gtk.c"}, {"function": "gd_mouse_set", "file": "ui/gtk.c"}, {"function": "gd_mouse_mode_change", "file": "ui/gtk.c"}, {"function": "gd_motion_event", "file": "ui/gtk.c"}, {"function": "gd_button_event", "file": "ui/gtk.c"}, {"function": "qemu_input_check_mode_change", "file": "ui/input.c"}, {"function": "sdl_hide_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_show_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_grab_start", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_mode_change", "file": "ui/sdl2.c"}, {"function": "sdl_send_mouse_event", "file": "ui/sdl2.c"}, {"function": "handle_mousemotion", "file": "ui/sdl2.c"}, {"function": "handle_mousebutton", "file": "ui/sdl2.c"}, {"function": "handle_windowevent", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_warp", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_define", "file": "ui/sdl2.c"}, {"function": "mouse_mode_notifier", "file": "ui/spice-input.c"}, {"function": "check_pointer_type_change", "file": "ui/vnc.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 21, "n_truth": 22, "tp": 21, "precision": 1.0, "recall": 0.9545454545454546, "f1": 0.9767441860465117}`

## Tool arm

### Turn 1  _(tok 3753+223, stop=tool_use)_

**Reasoning:** I'm going to call get_callers and grep at the same time.



- `get_callers(name=qemu_input_is_absolute, limit=200, rev=None)` →

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

### Turn 2  _(tok 6285+404, stop=tool_use)_

**Reasoning:** Cocoa.m line 2004 turned up in the grep but get_callers didn't report it, so I need to find which function encloses it. The callers list also has gd_motion_event twice, so I'll dedupe that. I also want to confirm whether sdl2.c line 206 really sits in sdl_hide_cursor, as get_callers says.



**Says:** The grep found a call in `ui/cocoa.m` (line 2004) that the C-only caller index did not return. I need to find its enclosing function.

- `get_context_at(file=ui/cocoa.m, line=2004, rev=None)` →

```
{
  "error": "get_context_at failed: NotImplementedError: File is not a C/C++ file: /tmp/cce_wt_z_cn0h7t/wt/ui/cocoa.m"
}
```

- `grep(pattern=qemu_input_is_absolute|is_absolute, version=old, path_glob=*.m)` →

```
2 matches
ui/cocoa.m:327: * isAbsoluteEnabled tracks qemu_input_is_absolute() [ie "is the emulated
ui/cocoa.m:2004:    if (qemu_input_is_absolute()) {
```

### Turn 3  _(tok 6899+124, stop=tool_use)_

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

### Turn 4  _(tok 7543+1334, stop=tool_use)_

**Reasoning:** I'm going through the callers of gd_motion_event in ui/cocoa.m, which sits inside cocoa_refresh. I'm checking whether any callers exist outside C files or inside macros, and confirming the git grep covered every tracked file. The 29 matches include the definition, the prototype, and a comment in cocoa.m.

I'm listing the callers by file: dbus-console.c, gtk.c, input.c, sdl2.c, spice-input.c, and vnc.c, with the cocoa.m entry for cocoa_refresh. Counting the unique functions across them gives 22, so I'll submit with the one cocoa entry.



- **submit_callers** → `{"callers": [{"function": "dbus_mouse_rel_motion", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_set_pos", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_update_is_absolute", "file": "ui/dbus-console.c"}, {"function": "gd_update_cursor", "file": "ui/gtk.c"}, {"function": "gd_mouse_set", "file": "ui/gtk.c"}, {"function": "gd_mouse_mode_change", "file": "ui/gtk.c"}, {"function": "gd_motion_event", "file": "ui/gtk.c"}, {"function": "gd_button_event", "file": "ui/gtk.c"}, {"function": "qemu_input_check_mode_change", "file": "ui/input.c"}, {"function": "sdl_hide_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_show_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_grab_start", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_mode_change", "file": "ui/sdl2.c"}, {"function": "sdl_send_mouse_event", "file": "ui/sdl2.c"}, {"function": "handle_mousemotion", "file": "ui/sdl2.c"}, {"function": "handle_mousebutton", "file": "ui/sdl2.c"}, {"function": "handle_windowevent", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_warp", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_define", "file": "ui/sdl2.c"}, {"function": "mouse_mode_notifier", "file": "ui/spice-input.c"}, {"function": "check_pointer_type_change", "file": "ui/vnc.c"}, {"function": "cocoa_refresh", "file": "ui/cocoa.m"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 22, "n_truth": 22, "tp": 22, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3205+100, stop=tool_use)_

**Reasoning:** I'm starting by calling get_callers with a high limit to pull up the full list.



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

### Turn 2  _(tok 4506+279, stop=tool_use)_

**Reasoning:** The tool reported the "old" version by default, which I'd expect to be the server's commit rather than the working tree. Since the signature change hasn't happened yet, the working tree is what I actually care about for call sites, so I'll re-run the check with version "work" to be sure.



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

### Turn 3  _(tok 6161+235, stop=tool_use)_

**Reasoning:** The results match what I got before, so the first attempt wasn't a fluke. I'm wondering whether I should also check the "work" version, and I think I will, just to be thorough.



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

### Turn 4  _(tok 8846+1031, stop=tool_use)_

**Reasoning:** I've confirmed the list of enclosing functions is consistent, and I'm now going through the mouse, display and input handlers that set cursor state.

I'm checking whether indirect callers through function pointers or macros could be missing from the call graph. There's no grep here, so I'll skip that and deduplicate the list by function and file, which leaves 21 entries.



- **submit_callers** → `{"callers": [{"function": "dbus_mouse_rel_motion", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_set_pos", "file": "ui/dbus-console.c"}, {"function": "dbus_mouse_update_is_absolute", "file": "ui/dbus-console.c"}, {"function": "gd_update_cursor", "file": "ui/gtk.c"}, {"function": "gd_mouse_set", "file": "ui/gtk.c"}, {"function": "gd_mouse_mode_change", "file": "ui/gtk.c"}, {"function": "gd_motion_event", "file": "ui/gtk.c"}, {"function": "gd_button_event", "file": "ui/gtk.c"}, {"function": "qemu_input_check_mode_change", "file": "ui/input.c"}, {"function": "sdl_hide_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_show_cursor", "file": "ui/sdl2.c"}, {"function": "sdl_grab_start", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_mode_change", "file": "ui/sdl2.c"}, {"function": "sdl_send_mouse_event", "file": "ui/sdl2.c"}, {"function": "handle_mousemotion", "file": "ui/sdl2.c"}, {"function": "handle_mousebutton", "file": "ui/sdl2.c"}, {"function": "handle_windowevent", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_warp", "file": "ui/sdl2.c"}, {"function": "sdl_mouse_define", "file": "ui/sdl2.c"}, {"function": "mouse_mode_notifier", "file": "ui/spice-input.c"}, {"function": "check_pointer_type_change", "file": "ui/vnc.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 21, "n_truth": 22, "tp": 21, "precision": 1.0, "recall": 0.9545454545454546, "f1": 0.9767441860465117}`

