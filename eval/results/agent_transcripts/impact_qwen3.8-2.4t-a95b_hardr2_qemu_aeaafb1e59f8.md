# Impact-analysis transcript — qemu @ aeaafb1e59f8 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `migration_is_running` (migration/migration.c), arity 1->0
- truth: [['migration/migration.c', 'migrate_fd_cancel'], ['migration/migration.c', 'migrate_prepare'], ['migration/options.c', 'migrate_cap_set'], ['migration/options.c', 'qmp_migrate_set_capabilities'], ['migration/savevm.c', 'qemu_savevm_state'], ['system/dirtylimit.c', 'dirtylimit_is_allowed'], ['target/riscv/kvm/kvm-cpu.c', 'kvm_riscv_put_regs_timer']]

## Self-navigation arm

### Turn 1  _(tok 901+70, stop=tool_use)_

**Reasoning:** Let's try searching for `migration_is_running` within the repository.


- `grep(pattern=migration_is_running, version=old, max_results=100)` →

```
9 matches
migration/migration.c:1106:bool migration_is_running(int state)
migration/migration.c:1480:        if (!migration_is_running(old_state)) {
migration/migration.c:1965:    if (migration_is_running(s->state)) {
migration/migration.h:482:bool migration_is_running(int state);
migration/options.c:684:    if (migration_is_running(s->state)) {
migration/options.c:728:    if (migration_is_running(s->state) || migration_in_colo_state()) {
migration/savevm.c:1709:    if (migration_is_running(ms->state)) {
system/dirtylimit.c:454:    if (migration_is_running(ms->state) &&
target/riscv/kvm/kvm-cpu.c:732:    if (migration_is_running(migrate_get_current()->state)) {
```

### Turn 2  _(tok 1189+609, stop=tool_use)_

**Reasoning:** 8 call sites (excluding the definition on line 1106 and the prototype on line 482 of migration.h). Need to identify the enclosing function at each call site:

1. migration/migration.c:1480
2. migration/migration.c:1965
3. migration/options.c:684
4. migration/options.c:728
5. migration/savevm.c:1709
6. system/dirtylimit.c:454
7. target/riscv/kvm/kvm-cpu.c:732

Let me try reading around each line to identify the enclosing function.

**Says:** Found 8 matches; one is the definition (migration.c:1106) and one is the prototype (migration.h:482), leaving 7 call sites. Now let me identify the enclosing function for each.



- `read_file(path=migration/migration.c, version=old, start_line=1440, end_line=1490)` →

```
migration/migration.c lines 1440-1490 of 3838
 1440| bool migrate_has_error(MigrationState *s)
 1441| {
 1442|     /* The lock is not helpful here, but still follow the rule */
 1443|     QEMU_LOCK_GUARD(&s->error_mutex);
 1444|     return qatomic_read(&s->error);
 1445| }
 1446| 
 1447| static void migrate_error_free(MigrationState *s)
 1448| {
 1449|     QEMU_LOCK_GUARD(&s->error_mutex);
 1450|     if (s->error) {
 1451|         error_free(s->error);
 1452|         s->error = NULL;
 1453|     }
 1454| }
 1455| 
 1456| static void migrate_fd_error(MigrationState *s, const Error *error)
 1457| {
 1458|     trace_migrate_fd_error(error_get_pretty(error));
 1459|     assert(s->to_dst_file == NULL);
 1460|     migrate_set_state(&s->state, MIGRATION_STATUS_SETUP,
 1461|                       MIGRATION_STATUS_FAILED);
 1462|     migrate_set_error(s, error);
 1463| }
 1464| 
 1465| static void migrate_fd_cancel(MigrationState *s)
 1466| {
 1467|     int old_state ;
 1468| 
 1469|     trace_migrate_fd_cancel();
 1470| 
 1471|     WITH_QEMU_LOCK_GUARD(&s->qemu_file_lock) {
 1472|         if (s->rp_state.from_dst_file) {
 1473|             /* shutdown the rp socket, so causing the rp thread to shutdown */
 1474|             qemu_file_shutdown(s->rp_state.from_dst_file);
 1475|         }
 1476|     }
 1477| 
 1478|     do {
 1479|         old_state = s->state;
 1480|         if (!migration_is_running(old_state)) {
 1481|             break;
 1482|         }
 1483|         /* If the migration is paused, kick it out of the pause */
 1484|         if (old_state == MIGRATION_STATUS_PRE_SWITCHOVER) {
 1485|             qemu_sem_post(&s->pause_sem);
 1486|         }
 1487|         migrate_set_state(&s->state, old_state, MIGRATION_STATUS_CANCELLING);
 1488|     } while (s->state != MIGRATION_STATUS_CANCELLING);
 1489| 
 1490|     /*
```

- `read_file(path=migration/migration.c, version=old, start_line=1930, end_line=1975)` →

```
migration/migration.c lines 1930-1975 of 3838
 1930| 
 1931|     if (blk) {
 1932|         warn_report("parameter 'blk' is deprecated;"
 1933|                     " use blockdev-mirror with NBD instead");
 1934|     }
 1935| 
 1936|     if (resume) {
 1937|         if (s->state != MIGRATION_STATUS_POSTCOPY_PAUSED) {
 1938|             error_setg(errp, "Cannot resume if there is no "
 1939|                        "paused migration");
 1940|             return false;
 1941|         }
 1942| 
 1943|         /*
 1944|          * Postcopy recovery won't work well with release-ram
 1945|          * capability since release-ram will drop the page buffer as
 1946|          * long as the page is put into the send buffer.  So if there
 1947|          * is a network failure happened, any page buffers that have
 1948|          * not yet reached the destination VM but have already been
 1949|          * sent from the source VM will be lost forever.  Let's refuse
 1950|          * the client from resuming such a postcopy migration.
 1951|          * Luckily release-ram was designed to only be used when src
 1952|          * and destination VMs are on the same host, so it should be
 1953|          * fine.
 1954|          */
 1955|         if (migrate_release_ram()) {
 1956|             error_setg(errp, "Postcopy recovery cannot work "
 1957|                        "when release-ram capability is set");
 1958|             return false;
 1959|         }
 1960| 
 1961|         /* This is a resume, skip init status */
 1962|         return true;
 1963|     }
 1964| 
 1965|     if (migration_is_running(s->state)) {
 1966|         error_setg(errp, QERR_MIGRATION_ACTIVE);
 1967|         return false;
 1968|     }
 1969| 
 1970|     if (runstate_check(RUN_STATE_INMIGRATE)) {
 1971|         error_setg(errp, "Guest is waiting for an incoming migration");
 1972|         return false;
 1973|     }
 1974| 
 1975|     if (runstate_check(RUN_STATE_POSTMIGRATE)) {
```

- `read_file(path=migration/options.c, version=old, start_line=655, end_line=735)` →

```
migration/options.c lines 655-735 of 1579
  655| 
  656|     if (new_caps[MIGRATION_CAPABILITY_MAPPED_RAM]) {
  657|         if (new_caps[MIGRATION_CAPABILITY_XBZRLE]) {
  658|             error_setg(errp,
  659|                        "Mapped-ram migration is incompatible with xbzrle");
  660|             return false;
  661|         }
  662| 
  663|         if (new_caps[MIGRATION_CAPABILITY_COMPRESS]) {
  664|             error_setg(errp,
  665|                        "Mapped-ram migration is incompatible with compression");
  666|             return false;
  667|         }
  668| 
  669|         if (new_caps[MIGRATION_CAPABILITY_POSTCOPY_RAM]) {
  670|             error_setg(errp,
  671|                        "Mapped-ram migration is incompatible with postcopy");
  672|             return false;
  673|         }
  674|     }
  675| 
  676|     return true;
  677| }
  678| 
  679| bool migrate_cap_set(int cap, bool value, Error **errp)
  680| {
  681|     MigrationState *s = migrate_get_current();
  682|     bool new_caps[MIGRATION_CAPABILITY__MAX];
  683| 
  684|     if (migration_is_running(s->state)) {
  685|         error_setg(errp, QERR_MIGRATION_ACTIVE);
  686|         return false;
  687|     }
  688| 
  689|     memcpy(new_caps, s->capabilities, sizeof(new_caps));
  690|     new_caps[cap] = value;
  691| 
  692|     if (!migrate_caps_check(s->capabilities, new_caps, errp)) {
  693|         return false;
  694|     }
  695|     s->capabilities[cap] = value;
  696|     return true;
  697| }
  698| 
  699| MigrationCapabilityStatusList *qmp_query_migrate_capabilities(Error **errp)
  700| {
  701|     MigrationCapabilityStatusList *head = NULL, **tail = &head;
  702|     MigrationCapabilityStatus *caps;
  703|     MigrationState *s = migrate_get_current();
  704|     int i;
  705| 
  706|     for (i = 0; i < MIGRATION_CAPABILITY__MAX; i++) {
  707| #ifndef CONFIG_LIVE_BLOCK_MIGRATION
  708|         if (i == MIGRATION_CAPABILITY_BLOCK) {
  709|             continue;
  710|         }
  711| #endif
  712|         caps = g_malloc0(sizeof(*caps));
  713|         caps->capability = i;
  714|         caps->state = s->capabilities[i];
  715|         QAPI_LIST_APPEND(tail, caps);
  716|     }
  717| 
  718|     return head;
  719| }
  720| 
  721| void qmp_migrate_set_capabilities(MigrationCapabilityStatusList *params,
  722|                                   Error **errp)
  723| {
  724|     MigrationState *s = migrate_get_current();
  725|     MigrationCapabilityStatusList *cap;
  726|     bool new_caps[MIGRATION_CAPABILITY__MAX];
  727| 
  728|     if (migration_is_running(s->state) || migration_in_colo_state()) {
  729|         error_setg(errp, QERR_MIGRATION_ACTIVE);
  730|         return;
  731|     }
  732| 
  733|     memcpy(new_caps, s->capabilities, sizeof(new_caps));
  734|     for (cap = params; cap; cap = cap->next) {
  735|         new_caps[cap->value->capability] = cap->value->state;
```

- `read_file(path=migration/savevm.c, version=old, start_line=1680, end_line=1715)` →

```
migration/savevm.c lines 1680-1715 of 3547
 1680|             }
 1681|         }
 1682|         se->ops->state_pending_exact(se->opaque, must_precopy, can_postcopy);
 1683|     }
 1684| }
 1685| 
 1686| void qemu_savevm_state_cleanup(void)
 1687| {
 1688|     SaveStateEntry *se;
 1689|     Error *local_err = NULL;
 1690| 
 1691|     if (precopy_notify(PRECOPY_NOTIFY_CLEANUP, &local_err)) {
 1692|         error_report_err(local_err);
 1693|     }
 1694| 
 1695|     trace_savevm_state_cleanup();
 1696|     QTAILQ_FOREACH(se, &savevm_state.handlers, entry) {
 1697|         if (se->ops && se->ops->save_cleanup) {
 1698|             se->ops->save_cleanup(se->opaque);
 1699|         }
 1700|     }
 1701| }
 1702| 
 1703| static int qemu_savevm_state(QEMUFile *f, Error **errp)
 1704| {
 1705|     int ret;
 1706|     MigrationState *ms = migrate_get_current();
 1707|     MigrationStatus status;
 1708| 
 1709|     if (migration_is_running(ms->state)) {
 1710|         error_setg(errp, QERR_MIGRATION_ACTIVE);
 1711|         return -EINVAL;
 1712|     }
 1713| 
 1714|     if (migrate_block()) {
 1715|         error_setg(errp, "Block migration and snapshots are incompatible");
```

- `read_file(path=system/dirtylimit.c, version=old, start_line=425, end_line=460)` →

```
system/dirtylimit.c lines 425-460 of 682
  425| 
  426|         dirtylimit_state_unlock();
  427|     }
  428| }
  429| 
  430| static void dirtylimit_init(void)
  431| {
  432|     dirtylimit_state_initialize();
  433|     dirtylimit_change(true);
  434|     vcpu_dirty_rate_stat_initialize();
  435|     vcpu_dirty_rate_stat_start();
  436| }
  437| 
  438| static void dirtylimit_cleanup(void)
  439| {
  440|     vcpu_dirty_rate_stat_stop();
  441|     vcpu_dirty_rate_stat_finalize();
  442|     dirtylimit_change(false);
  443|     dirtylimit_state_finalize();
  444| }
  445| 
  446| /*
  447|  * dirty page rate limit is not allowed to set if migration
  448|  * is running with dirty-limit capability enabled.
  449|  */
  450| static bool dirtylimit_is_allowed(void)
  451| {
  452|     MigrationState *ms = migrate_get_current();
  453| 
  454|     if (migration_is_running(ms->state) &&
  455|         (!qemu_thread_is_self(&ms->thread)) &&
  456|         migrate_dirty_limit() &&
  457|         dirtylimit_in_service()) {
  458|         return false;
  459|     }
  460|     return true;
```

- `read_file(path=target/riscv/kvm/kvm-cpu.c, version=old, start_line=700, end_line=740)` →

```
target/riscv/kvm/kvm-cpu.c lines 700-740 of 1821
  700|     KVM_RISCV_GET_TIMER(cs, frequency, env->kvm_timer_frequency);
  701| 
  702|     env->kvm_timer_dirty = true;
  703| }
  704| 
  705| static void kvm_riscv_put_regs_timer(CPUState *cs)
  706| {
  707|     uint64_t reg;
  708|     CPURISCVState *env = &RISCV_CPU(cs)->env;
  709| 
  710|     if (!env->kvm_timer_dirty) {
  711|         return;
  712|     }
  713| 
  714|     KVM_RISCV_SET_TIMER(cs, time, env->kvm_timer_time);
  715|     KVM_RISCV_SET_TIMER(cs, compare, env->kvm_timer_compare);
  716| 
  717|     /*
  718|      * To set register of RISCV_TIMER_REG(state) will occur a error from KVM
  719|      * on env->kvm_timer_state == 0, It's better to adapt in KVM, but it
  720|      * doesn't matter that adaping in QEMU now.
  721|      * TODO If KVM changes, adapt here.
  722|      */
  723|     if (env->kvm_timer_state) {
  724|         KVM_RISCV_SET_TIMER(cs, state, env->kvm_timer_state);
  725|     }
  726| 
  727|     /*
  728|      * For now, migration will not work between Hosts with different timer
  729|      * frequency. Therefore, we should check whether they are the same here
  730|      * during the migration.
  731|      */
  732|     if (migration_is_running(migrate_get_current()->state)) {
  733|         KVM_RISCV_GET_TIMER(cs, frequency, reg);
  734|         if (reg != env->kvm_timer_frequency) {
  735|             error_report("Dst Hosts timer frequency != Src Hosts");
  736|         }
  737|     }
  738| 
  739|     env->kvm_timer_dirty = false;
  740| }
```

### Turn 3  _(tok 6060+168, stop=tool_use)_

**Reasoning:** All call sites have been identified. The function containing migration.c:1965 is still needed — let's confirm. Looking at the context, it references `resume`, `blk`, and `s->state` — it's probably `migrate_prepare` or `qmp_migrate`. Let's check.


**Says:** I need to confirm the enclosing function for migration.c:1965.



- `grep(pattern=^(static )?(bool|void|int|MigrationState)[a-zA-Z_* ]*\(, version=old, path_glob=migration/migration.c, max_results=200)` →

```
129 matches
migration/migration.c:104:static bool migration_object_check(MigrationState *ms, Error **errp);
migration/migration.c:105:static int migration_maybe_pause(MigrationState *s,
migration/migration.c:108:static void migrate_fd_cancel(MigrationState *s);
migration/migration.c:109:static bool close_return_path_on_source(MigrationState *s);
migration/migration.c:110:static void migration_completion_end(MigrationState *s);
migration/migration.c:112:static void migration_downtime_start(MigrationState *s)
migration/migration.c:118:static void migration_downtime_end(MigrationState *s)
migration/migration.c:133:static bool migration_needs_multiple_sockets(void)
migration/migration.c:138:static bool transport_supports_multi_channels(MigrationAddress *addr)
migration/migration.c:157:static bool migration_needs_seekable_channel(void)
migration/migration.c:162:static bool transport_supports_seeking(MigrationAddress *addr)
migration/migration.c:206:static int migration_stop_vm(MigrationState *s, RunState state)
migration/migration.c:223:void migration_object_init(void)
migration/migration.c:263:static void migration_bh_dispatch_bh(void *opaque)
migration/migration.c:279:void migration_bh_schedule(QEMUBHFunc *cb, void *opaque)
migration/migration.c:298:void migration_cancel(const Error *error)
migration/migration.c:309:void migration_shutdown(void)
migration/migration.c:339:MigrationState *migrate_get_current(void)
migration/migration.c:352:void migration_incoming_transport_cleanup(MigrationIncomingState *mis)
migration/migration.c:365:void migration_incoming_state_destroy(void)
migration/migration.c:406:static void migrate_generate_event(int new_state)
migration/migration.c:417:static int migrate_send_rp_message(MigrationIncomingState *mis,
migration/migration.c:446:int migrate_send_rp_message_req_pages(MigrationIncomingState *mis,
migration/migration.c:483:int migrate_send_rp_req_pages(MigrationIncomingState *mis,
migration/migration.c:515:bool migration_incoming_colo_enabled(void)
migration/migration.c:520:void migration_incoming_disable_colo(void)
migration/migration.c:526:int migration_incoming_enable_colo(void)
migration/migration.c:548:void migrate_add_address(SocketAddress *address)
migration/migration.c:556:bool migrate_uri_parse(const char *uri, MigrationChannel **channel,
migration/migration.c:611:static void qemu_start_incoming_migration(const char *uri, bool has_channels,
migration/migration.c:686:static void process_incoming_migration_bh(void *opaque)
migration/migration.c:827:static void migration_incoming_setup(QEMUFile *f)
migration/migration.c:837:void migration_incoming_process(void)
migration/migration.c:844:static bool postcopy_try_recover(void)
migration/migration.c:876:void migration_fd_process_incoming(QEMUFile *f)
migration/migration.c:889:static bool migration_should_start_incoming(bool main_channel)
migration/migration.c:910:void migration_ioc_process_incoming(QIOChannel *ioc, Error **errp)
migration/migration.c:982:bool migration_has_all_channels(void)
migration/migration.c:1001:int migrate_send_rp_switchover_ack(MigrationIncomingState *mis)
migration/migration.c:1011:void migrate_send_rp_shut(MigrationIncomingState *mis,
migration/migration.c:1024:void migrate_send_rp_pong(MigrationIncomingState *mis,
migration/migration.c:1033:void migrate_send_rp_recv_bitmap(MigrationIncomingState *mis,
migration/migration.c:1072:void migrate_send_rp_resume_ack(MigrationIncomingState *mis, uint32_t value)
migration/migration.c:1084:bool migration_is_setup_or_active(void)
migration/migration.c:1106:bool migration_is_running(int state)
migration/migration.c:1126:static bool migrate_show_downtime(MigrationState *s)
migration/migration.c:1131:static void populate_time_info(MigrationInfo *info, MigrationState *s)
migration/migration.c:1155:static void populate_ram_info(MigrationInfo *info, MigrationState *s)
migration/migration.c:1215:static void populate_disk_info(MigrationInfo *info)
migration/migration.c:1225:static void fill_source_migration_info(MigrationInfo *info)
migration/migration.c:1297:static void fill_destination_migration_info(MigrationInfo *info)
migration/migration.c:1339:void qmp_migrate_start_postcopy(Error **errp)
migration/migration.c:1363:void migrate_set_state(int *state, int old_state, int new_state)
migration/migration.c:1372:static void migrate_fd_cleanup(MigrationState *s)
migration/migration.c:1427:static void migrate_fd_cleanup_bh(void *opaque)
migration/migration.c:1432:void migrate_set_error(MigrationState *s, const Error *error)
migration/migration.c:1440:bool migrate_has_error(MigrationState *s)
migration/migration.c:1447:static void migrate_error_free(MigrationState *s)
migration/migration.c:1456:static void migrate_fd_error(MigrationState *s, const Error *error)
migration/migration.c:1465:static void migrate_fd_cancel(MigrationState *s)
migration/migration.c:1514:void migration_add_notifier_mode(NotifierWithReturn *notify,
migration/migration.c:1521:void migration_add_notifier(NotifierWithReturn *notify,
migration/migration.c:1527:void migration_remove_notifier(NotifierWithReturn *notify)
migration/migration.c:1535:int migration_call_notifiers(MigrationState *s, MigrationEventType type,
migration/migration.c:1549:bool migration_in_setup(MigrationState *s)
migration/migration.c:1554:bool migration_has_finished(MigrationState *s)
migration/migration.c:1559:bool migration_has_failed(MigrationState *s)
migration/migration.c:1565:bool migration_in_postcopy(void)
migration/migration.c:1579:bool migration_postcopy_is_alive(int state)
migration/migration.c:1590:bool migration_in_incoming_postcopy(void)
migration/migration.c:1597:bool migration_incoming_postcopy_advised(void)
migration/migration.c:1604:bool migration_in_bg_snapshot(void)
migration/migration.c:1610:bool migration_is_idle(void)
migration/migration.c:1640:bool migration_is_active(void)
migration/migration.c:1648:bool migrate_mode_is_cpr(MigrationState *s)
migration/migration.c:1653:int migrate_init(MigrationState *s, Error **errp)
migration/migration.c:1699:static bool is_busy(Error **reasonp, Error **errp)
migration/migration.c:1714:static bool is_only_migratable(Error **reasonp, Error **errp, int modes)
migration/migration.c:1728:static int get_modes(MigMode mode, va_list ap)
migration/migration.c:1743:static int add_blockers(Error **reasonp, Error **errp, int modes)
migration/migration.c:1754:int migrate_add_blocker(Error **reasonp, Error **errp)
migration/migration.c:1759:int migrate_add_blocker_normal(Error **reasonp, Error **errp)
migration/migration.c:1764:int migrate_add_blocker_modes(Error **reasonp, Error **errp, MigMode mode, ...)
migration/migration.c:1781:int migrate_add_blocker_internal(Error **reasonp, Error **errp)
migration/migration.c:1791:void migrate_del_blocker(Error **reasonp)
migration/migration.c:1803:void qmp_migrate_incoming(const char *uri, bool has_channels,
migration/migration.c:1833:void qmp_migrate_recover(const char *uri, Error **errp)
migration/migration.c:1861:void qmp_migrate_pause(Error **errp)
migration/migration.c:1906:bool migration_is_blocked(Error **errp)
migration/migration.c:1923:static bool migrate_prepare(MigrationState *s, bool blk, bool blk_inc,
migration/migration.c:2047:void qmp_migrate(const char *uri, bool has_channels,
migration/migration.c:2136:void qmp_migrate_cancel(Error **errp)
migration/migration.c:2141:void qmp_migrate_continue(MigrationStatus state, Error **errp)
migration/migration.c:2152:int migration_rp_wait(MigrationState *s)
migration/migration.c:2169:void migration_rp_kick(MigrationState *s)
migration/migration.c:2216:static bool migrate_handle_rp_recv_bitmap(MigrationState *s, char *block_name,
migration/migration.c:2231:static bool migrate_handle_rp_resume_ack(MigrationState *s,
migration/migration.c:2255:static void migration_release_dst_files(MigrationState *ms)
migration/migration.c:2287:static void *source_return_path_thread(void *opaque)
migration/migration.c:2448:static int open_return_path_on_source(MigrationState *ms)
migration/migration.c:2467:static bool close_return_path_on_source(MigrationState *ms)
migration/migration.c:2507:static int postcopy_start(MigrationState *ms, Error **errp)
migration/migration.c:2684:static int migration_maybe_pause(MigrationState *s,
migration/migration.c:2722:static int migration_completion_precopy(MigrationState *s,
migration/migration.c:2755:static void migration_completion_postcopy(MigrationState *s)
migration/migration.c:2774:static void migration_completion_failed(MigrationState *s,
migration/migration.c:2805:static void migration_completion(MigrationState *s)
migration/migration.c:2851:static void bg_migration_completion(MigrationState *s)
migration/migration.c:2890:static int postcopy_resume_handshake(MigrationState *s)
migration/migration.c:2908:static int postcopy_do_resume(MigrationState *s)
migration/migration.c:3075:static void migration_completion_end(MigrationState *s)
migration/migration.c:3099:static void update_iteration_initial_status(MigrationState *s)
migration/migration.c:3110:static void migration_update_counters(MigrationState *s,
migration/migration.c:3171:static bool migration_can_switchover(MigrationState *s)
migration/migration.c:3235:static void migration_iteration_finish(MigrationState *s)
migration/migration.c:3274:static void bg_migration_iteration_finish(MigrationState *s)
migration/migration.c:3319:void migration_make_urgent_request(void)
migration/migration.c:3324:void migration_consume_urgent_request(void)
migration/migration.c:3330:bool migration_rate_limit(void)
migration/migration.c:3369:static void qemu_savevm_wait_unplug(MigrationState *s, int old_state,
migration/migration.c:3406:static void *migration_thread(void *opaque)
migration/migration.c:3505:static void bg_migration_vm_start_bh(void *opaque)
migration/migration.c:3528:static void *bg_migration_thread(void *opaque)
migration/migration.c:3651:void migrate_fd_connect(MigrationState *s, Error *error_in)
migration/migration.c:3753:static void migration_class_init(ObjectClass *klass, void *data)
migration/migration.c:3761:static void migration_instance_finalize(Object *obj)
migration/migration.c:3777:static void migration_instance_init(Object *obj)
migration/migration.c:3802:static bool migration_object_check(MigrationState *ms, Error **errp)
migration/migration.c:3832:static void register_migration_types(void)
```

### Turn 4  _(tok 9130+450, stop=tool_use)_

**Reasoning:** I've verified all 7 call sites and their containing functions:

1. migration/migration.c:1480 → `migrate_fd_cancel` (starts at line 1465, ends around line 1513)
2. migration/migration.c:1965 → `migrate_prepare` (starts at line 1923, ends before line 2047)
3. migration/options.c:684 → `migrate_cap_set` (line 679)
4. migration/options.c:728 → `qmp_migrate_set_capabilities` (line 721)
5. migration/savevm.c:1709 → `qemu_savevm_state` (line 1703)
6. system/dirtylimit.c:454 → `dirtylimit_is_allowed` (line 450)
7. target/riscv/kvm/kvm-cpu.c:732 → `kvm_riscv_put_regs_timer` (line 705)

I've confirmed that grep detected all occurrences of `migration_is_running` (9 total: 7 call sites + 1 definition + 1 header prototype). Nothing more is needed.

- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1030+122, stop=tool_use)_

**Reasoning:** I need to look into this further. Let me check the details. Let's find all references to `migration_is_running`.

- `find_references(name=migration_is_running, max_results=100)` →

```
8 references
migration_is_running 1480 migration/migration.c         if (!migration_is_running(old_state)) {
migration_is_running 1965 migration/migration.c     if (migration_is_running(s->state)) {
migration_is_running  482 migration/migration.h bool migration_is_running(int state);
migration_is_running  684 migration/options.c     if (migration_is_running(s->state)) {
migration_is_running  728 migration/options.c     if (migration_is_running(s->state) || migration_in_colo_state()) {
migration_is_running 1709 migration/savevm.c     if (migration_is_running(ms->state)) {
migration_is_running  454 system/dirtylimit.c     if (migration_is_running(ms->state) &&
migration_is_running  732 target/riscv/kvm/kvm-cpu.c     if (migration_is_running(migrate_get_current()->state)) {
```

- `grep(pattern=migration_is_running, version=old, max_results=100)` →

```
9 matches
migration/migration.c:1106:bool migration_is_running(int state)
migration/migration.c:1480:        if (!migration_is_running(old_state)) {
migration/migration.c:1965:    if (migration_is_running(s->state)) {
migration/migration.h:482:bool migration_is_running(int state);
migration/options.c:684:    if (migration_is_running(s->state)) {
migration/options.c:728:    if (migration_is_running(s->state) || migration_in_colo_state()) {
migration/savevm.c:1709:    if (migration_is_running(ms->state)) {
system/dirtylimit.c:454:    if (migration_is_running(ms->state) &&
target/riscv/kvm/kvm-cpu.c:732:    if (migration_is_running(migrate_get_current()->state)) {
```

### Turn 2  _(tok 1592+459, stop=tool_use)_

**Reasoning:** The grep results match find_references (8 references + 1 definition). Next, I need to find the outer function for each call site. Let me try reading around each line.


- `read_file(path=migration/migration.c, start_line=1440, end_line=1490, version=old)` →

```
migration/migration.c lines 1440-1490 of 3838
 1440| bool migrate_has_error(MigrationState *s)
 1441| {
 1442|     /* The lock is not helpful here, but still follow the rule */
 1443|     QEMU_LOCK_GUARD(&s->error_mutex);
 1444|     return qatomic_read(&s->error);
 1445| }
 1446| 
 1447| static void migrate_error_free(MigrationState *s)
 1448| {
 1449|     QEMU_LOCK_GUARD(&s->error_mutex);
 1450|     if (s->error) {
 1451|         error_free(s->error);
 1452|         s->error = NULL;
 1453|     }
 1454| }
 1455| 
 1456| static void migrate_fd_error(MigrationState *s, const Error *error)
 1457| {
 1458|     trace_migrate_fd_error(error_get_pretty(error));
 1459|     assert(s->to_dst_file == NULL);
 1460|     migrate_set_state(&s->state, MIGRATION_STATUS_SETUP,
 1461|                       MIGRATION_STATUS_FAILED);
 1462|     migrate_set_error(s, error);
 1463| }
 1464| 
 1465| static void migrate_fd_cancel(MigrationState *s)
 1466| {
 1467|     int old_state ;
 1468| 
 1469|     trace_migrate_fd_cancel();
 1470| 
 1471|     WITH_QEMU_LOCK_GUARD(&s->qemu_file_lock) {
 1472|         if (s->rp_state.from_dst_file) {
 1473|             /* shutdown the rp socket, so causing the rp thread to shutdown */
 1474|             qemu_file_shutdown(s->rp_state.from_dst_file);
 1475|         }
 1476|     }
 1477| 
 1478|     do {
 1479|         old_state = s->state;
 1480|         if (!migration_is_running(old_state)) {
 1481|             break;
 1482|         }
 1483|         /* If the migration is paused, kick it out of the pause */
 1484|         if (old_state == MIGRATION_STATUS_PRE_SWITCHOVER) {
 1485|             qemu_sem_post(&s->pause_sem);
 1486|         }
 1487|         migrate_set_state(&s->state, old_state, MIGRATION_STATUS_CANCELLING);
 1488|     } while (s->state != MIGRATION_STATUS_CANCELLING);
 1489| 
 1490|     /*
```

- `read_file(path=migration/migration.c, start_line=1920, end_line=1970, version=old)` →

```
migration/migration.c lines 1920-1970 of 3838
 1920| }
 1921| 
 1922| /* Returns true if continue to migrate, or false if error detected */
 1923| static bool migrate_prepare(MigrationState *s, bool blk, bool blk_inc,
 1924|                             bool resume, Error **errp)
 1925| {
 1926|     if (blk_inc) {
 1927|         warn_report("parameter 'inc' is deprecated;"
 1928|                     " use blockdev-mirror with NBD instead");
 1929|     }
 1930| 
 1931|     if (blk) {
 1932|         warn_report("parameter 'blk' is deprecated;"
 1933|                     " use blockdev-mirror with NBD instead");
 1934|     }
 1935| 
 1936|     if (resume) {
 1937|         if (s->state != MIGRATION_STATUS_POSTCOPY_PAUSED) {
 1938|             error_setg(errp, "Cannot resume if there is no "
 1939|                        "paused migration");
 1940|             return false;
 1941|         }
 1942| 
 1943|         /*
 1944|          * Postcopy recovery won't work well with release-ram
 1945|          * capability since release-ram will drop the page buffer as
 1946|          * long as the page is put into the send buffer.  So if there
 1947|          * is a network failure happened, any page buffers that have
 1948|          * not yet reached the destination VM but have already been
 1949|          * sent from the source VM will be lost forever.  Let's refuse
 1950|          * the client from resuming such a postcopy migration.
 1951|          * Luckily release-ram was designed to only be used when src
 1952|          * and destination VMs are on the same host, so it should be
 1953|          * fine.
 1954|          */
 1955|         if (migrate_release_ram()) {
 1956|             error_setg(errp, "Postcopy recovery cannot work "
 1957|                        "when release-ram capability is set");
 1958|             return false;
 1959|         }
 1960| 
 1961|         /* This is a resume, skip init status */
 1962|         return true;
 1963|     }
 1964| 
 1965|     if (migration_is_running(s->state)) {
 1966|         error_setg(errp, QERR_MIGRATION_ACTIVE);
 1967|         return false;
 1968|     }
 1969| 
 1970|     if (runstate_check(RUN_STATE_INMIGRATE)) {
```

- `read_file(path=migration/options.c, start_line=650, end_line=735, version=old)` →

```
migration/options.c lines 650-735 of 1579
  650|         if (new_caps[MIGRATION_CAPABILITY_XBZRLE]) {
  651|             error_setg(errp, "Compression is not compatible with xbzrle");
  652|             return false;
  653|         }
  654|     }
  655| 
  656|     if (new_caps[MIGRATION_CAPABILITY_MAPPED_RAM]) {
  657|         if (new_caps[MIGRATION_CAPABILITY_XBZRLE]) {
  658|             error_setg(errp,
  659|                        "Mapped-ram migration is incompatible with xbzrle");
  660|             return false;
  661|         }
  662| 
  663|         if (new_caps[MIGRATION_CAPABILITY_COMPRESS]) {
  664|             error_setg(errp,
  665|                        "Mapped-ram migration is incompatible with compression");
  666|             return false;
  667|         }
  668| 
  669|         if (new_caps[MIGRATION_CAPABILITY_POSTCOPY_RAM]) {
  670|             error_setg(errp,
  671|                        "Mapped-ram migration is incompatible with postcopy");
  672|             return false;
  673|         }
  674|     }
  675| 
  676|     return true;
  677| }
  678| 
  679| bool migrate_cap_set(int cap, bool value, Error **errp)
  680| {
  681|     MigrationState *s = migrate_get_current();
  682|     bool new_caps[MIGRATION_CAPABILITY__MAX];
  683| 
  684|     if (migration_is_running(s->state)) {
  685|         error_setg(errp, QERR_MIGRATION_ACTIVE);
  686|         return false;
  687|     }
  688| 
  689|     memcpy(new_caps, s->capabilities, sizeof(new_caps));
  690|     new_caps[cap] = value;
  691| 
  692|     if (!migrate_caps_check(s->capabilities, new_caps, errp)) {
  693|         return false;
  694|     }
  695|     s->capabilities[cap] = value;
  696|     return true;
  697| }
  698| 
  699| MigrationCapabilityStatusList *qmp_query_migrate_capabilities(Error **errp)
  700| {
  701|     MigrationCapabilityStatusList *head = NULL, **tail = &head;
  702|     MigrationCapabilityStatus *caps;
  703|     MigrationState *s = migrate_get_current();
  704|     int i;
  705| 
  706|     for (i = 0; i < MIGRATION_CAPABILITY__MAX; i++) {
  707| #ifndef CONFIG_LIVE_BLOCK_MIGRATION
  708|         if (i == MIGRATION_CAPABILITY_BLOCK) {
  709|             continue;
  710|         }
  711| #endif
  712|         caps = g_malloc0(sizeof(*caps));
  713|         caps->capability = i;
  714|         caps->state = s->capabilities[i];
  715|         QAPI_LIST_APPEND(tail, caps);
  716|     }
  717| 
  718|     return head;
  719| }
  720| 
  721| void qmp_migrate_set_capabilities(MigrationCapabilityStatusList *params,
  722|                                   Error **errp)
  723| {
  724|     MigrationState *s = migrate_get_current();
  725|     MigrationCapabilityStatusList *cap;
  726|     bool new_caps[MIGRATION_CAPABILITY__MAX];
  727| 
  728|     if (migration_is_running(s->state) || migration_in_colo_state()) {
  729|         error_setg(errp, QERR_MIGRATION_ACTIVE);
  730|         return;
  731|     }
  732| 
  733|     memcpy(new_caps, s->capabilities, sizeof(new_caps));
  734|     for (cap = params; cap; cap = cap->next) {
  735|         new_caps[cap->value->capability] = cap->value->state;
```

- `read_file(path=migration/savevm.c, start_line=1660, end_line=1715, version=old)` →

```
migration/savevm.c lines 1660-1715 of 3547
 1660|         }
 1661|         se->ops->state_pending_estimate(se->opaque, must_precopy, can_postcopy);
 1662|     }
 1663| }
 1664| 
 1665| void qemu_savevm_state_pending_exact(uint64_t *must_precopy,
 1666|                                      uint64_t *can_postcopy)
 1667| {
 1668|     SaveStateEntry *se;
 1669| 
 1670|     *must_precopy = 0;
 1671|     *can_postcopy = 0;
 1672| 
 1673|     QTAILQ_FOREACH(se, &savevm_state.handlers, entry) {
 1674|         if (!se->ops || !se->ops->state_pending_exact) {
 1675|             continue;
 1676|         }
 1677|         if (se->ops->is_active) {
 1678|             if (!se->ops->is_active(se->opaque)) {
 1679|                 continue;
 1680|             }
 1681|         }
 1682|         se->ops->state_pending_exact(se->opaque, must_precopy, can_postcopy);
 1683|     }
 1684| }
 1685| 
 1686| void qemu_savevm_state_cleanup(void)
 1687| {
 1688|     SaveStateEntry *se;
 1689|     Error *local_err = NULL;
 1690| 
 1691|     if (precopy_notify(PRECOPY_NOTIFY_CLEANUP, &local_err)) {
 1692|         error_report_err(local_err);
 1693|     }
 1694| 
 1695|     trace_savevm_state_cleanup();
 1696|     QTAILQ_FOREACH(se, &savevm_state.handlers, entry) {
 1697|         if (se->ops && se->ops->save_cleanup) {
 1698|             se->ops->save_cleanup(se->opaque);
 1699|         }
 1700|     }
 1701| }
 1702| 
 1703| static int qemu_savevm_state(QEMUFile *f, Error **errp)
 1704| {
 1705|     int ret;
 1706|     MigrationState *ms = migrate_get_current();
 1707|     MigrationStatus status;
 1708| 
 1709|     if (migration_is_running(ms->state)) {
 1710|         error_setg(errp, QERR_MIGRATION_ACTIVE);
 1711|         return -EINVAL;
 1712|     }
 1713| 
 1714|     if (migrate_block()) {
 1715|         error_setg(errp, "Block migration and snapshots are incompatible");
```

- `read_file(path=system/dirtylimit.c, start_line=420, end_line=465, version=old)` →

```
system/dirtylimit.c lines 420-465 of 682
  420|                     cpu->throttle_us_per_full);
  421| 
  422|             g_usleep(cpu->throttle_us_per_full);
  423|             return;
  424|         }
  425| 
  426|         dirtylimit_state_unlock();
  427|     }
  428| }
  429| 
  430| static void dirtylimit_init(void)
  431| {
  432|     dirtylimit_state_initialize();
  433|     dirtylimit_change(true);
  434|     vcpu_dirty_rate_stat_initialize();
  435|     vcpu_dirty_rate_stat_start();
  436| }
  437| 
  438| static void dirtylimit_cleanup(void)
  439| {
  440|     vcpu_dirty_rate_stat_stop();
  441|     vcpu_dirty_rate_stat_finalize();
  442|     dirtylimit_change(false);
  443|     dirtylimit_state_finalize();
  444| }
  445| 
  446| /*
  447|  * dirty page rate limit is not allowed to set if migration
  448|  * is running with dirty-limit capability enabled.
  449|  */
  450| static bool dirtylimit_is_allowed(void)
  451| {
  452|     MigrationState *ms = migrate_get_current();
  453| 
  454|     if (migration_is_running(ms->state) &&
  455|         (!qemu_thread_is_self(&ms->thread)) &&
  456|         migrate_dirty_limit() &&
  457|         dirtylimit_in_service()) {
  458|         return false;
  459|     }
  460|     return true;
  461| }
  462| 
  463| void qmp_cancel_vcpu_dirty_limit(bool has_cpu_index,
  464|                                  int64_t cpu_index,
  465|                                  Error **errp)
```

- `read_file(path=target/riscv/kvm/kvm-cpu.c, start_line=690, end_line=740, version=old)` →

```
target/riscv/kvm/kvm-cpu.c lines 690-740 of 1821
  690| {
  691|     CPURISCVState *env = &RISCV_CPU(cs)->env;
  692| 
  693|     if (env->kvm_timer_dirty) {
  694|         return;
  695|     }
  696| 
  697|     KVM_RISCV_GET_TIMER(cs, time, env->kvm_timer_time);
  698|     KVM_RISCV_GET_TIMER(cs, compare, env->kvm_timer_compare);
  699|     KVM_RISCV_GET_TIMER(cs, state, env->kvm_timer_state);
  700|     KVM_RISCV_GET_TIMER(cs, frequency, env->kvm_timer_frequency);
  701| 
  702|     env->kvm_timer_dirty = true;
  703| }
  704| 
  705| static void kvm_riscv_put_regs_timer(CPUState *cs)
  706| {
  707|     uint64_t reg;
  708|     CPURISCVState *env = &RISCV_CPU(cs)->env;
  709| 
  710|     if (!env->kvm_timer_dirty) {
  711|         return;
  712|     }
  713| 
  714|     KVM_RISCV_SET_TIMER(cs, time, env->kvm_timer_time);
  715|     KVM_RISCV_SET_TIMER(cs, compare, env->kvm_timer_compare);
  716| 
  717|     /*
  718|      * To set register of RISCV_TIMER_REG(state) will occur a error from KVM
  719|      * on env->kvm_timer_state == 0, It's better to adapt in KVM, but it
  720|      * doesn't matter that adaping in QEMU now.
  721|      * TODO If KVM changes, adapt here.
  722|      */
  723|     if (env->kvm_timer_state) {
  724|         KVM_RISCV_SET_TIMER(cs, state, env->kvm_timer_state);
  725|     }
  726| 
  727|     /*
  728|      * For now, migration will not work between Hosts with different timer
  729|      * frequency. Therefore, we should check whether they are the same here
  730|      * during the migration.
  731|      */
  732|     if (migration_is_running(migrate_get_current()->state)) {
  733|         KVM_RISCV_GET_TIMER(cs, frequency, reg);
  734|         if (reg != env->kvm_timer_frequency) {
  735|             error_report("Dst Hosts timer frequency != Src Hosts");
  736|         }
  737|     }
  738| 
  739|     env->kvm_timer_dirty = false;
  740| }
```

### Turn 3  _(tok 7031+373, stop=tool_use)_

**Reasoning:** All call sites verified:

1. `migrate_fd_cancel` in migration/migration.c (line 1480)
2. `migrate_prepare` in migration/migration.c (line 1965)
3. `migrate_cap_set` in migration/options.c (line 684)
4. `qmp_migrate_set_capabilities` in migration/options.c (line 728)
5. `qemu_savevm_state` in migration/savevm.c (line 1709)
6. `dirtylimit_is_allowed` in system/dirtylimit.c (line 454)
7. `kvm_riscv_put_regs_timer` in target/riscv/kvm/kvm-cpu.c (line 732)

The grep results match find_references perfectly (7 call sites + definition + prototype). Complete. Submitting.

- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2730+109, stop=tool_use)_

**Reasoning:** Let's find all call sites of migration_is_running.

- `get_callers(name=migration_is_running, limit=100)` →

```
{
  "name": "migration_is_running",
  "version": "old",
  "callers": [
    {
      "caller": "migrate_fd_cancel",
      "file": "migration/migration.c",
      "line": 1480
    },
    {
      "caller": "migrate_prepare",
      "file": "migration/migration.c",
      "line": 1965
    },
    {
      "caller": "migrate_cap_set",
      "file": "migration/options.c",
      "line": 684
    },
    {
      "caller": "qmp_migrate_set_capabilities",
      "file": "migration/options.c",
      "line": 728
    },
    {
      "caller": "qemu_savevm_state",
      "file": "migration/savevm.c",
      "line": 1709
    },
    {
      "caller": "dirtylimit_is_allowed",
      "file": "system/dirtylimit.c",
      "line": 454
    },
    {
      "caller": "kvm_riscv_put_regs_timer",
      "file": "target/riscv/kvm/kvm-cpu.c",
      "line": 732
    }
  ]
}
```

- `grep(pattern=migration_is_running, version=old, max_results=100)` →

```
9 matches
migration/migration.c:1106:bool migration_is_running(int state)
migration/migration.c:1480:        if (!migration_is_running(old_state)) {
migration/migration.c:1965:    if (migration_is_running(s->state)) {
migration/migration.h:482:bool migration_is_running(int state);
migration/options.c:684:    if (migration_is_running(s->state)) {
migration/options.c:728:    if (migration_is_running(s->state) || migration_in_colo_state()) {
migration/savevm.c:1709:    if (migration_is_running(ms->state)) {
system/dirtylimit.c:454:    if (migration_is_running(ms->state) &&
target/riscv/kvm/kvm-cpu.c:732:    if (migration_is_running(migrate_get_current()->state)) {
```

### Turn 2  _(tok 3379+443, stop=tool_use)_

**Reasoning:** Grep has confirmed 7 call sites (lines 1480, 1965, 684, 728, 1709, 454, 732), which matches the callers tool. I'll submit.

**Says:** Grep confirms exactly 7 call sites (excluding the definition at migration.c:1106 and the prototype at migration.h:482), matching the caller graph:

| Caller | File | Line |
|---|---|---|
| `migrate_fd_cancel` | migration/migration.c | 1480 |
| `migrate_prepare` | migration/migration.c | 1965 |
| `migrate_cap_set` | migration/options.c | 684 |
| `qmp_migrate_set_capabilities` | migration/options.c | 728 |
| `qemu_savevm_state` | migration/savevm.c | 1709 |
| `dirtylimit_is_allowed` | system/dirtylimit.c | 454 |
| `kvm_riscv_put_regs_timer` | target/riscv/kvm/kvm-cpu.c | 732 |



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2307+86, stop=tool_use)_

**Reasoning:** Let's start by finding all the callers of `migration_is_running`.

- `get_callers(name=migration_is_running, limit=100)` →

```
{
  "name": "migration_is_running",
  "version": "old",
  "callers": [
    {
      "caller": "migrate_fd_cancel",
      "file": "migration/migration.c",
      "line": 1480
    },
    {
      "caller": "migrate_prepare",
      "file": "migration/migration.c",
      "line": 1965
    },
    {
      "caller": "migrate_cap_set",
      "file": "migration/options.c",
      "line": 684
    },
    {
      "caller": "qmp_migrate_set_capabilities",
      "file": "migration/options.c",
      "line": 728
    },
    {
      "caller": "qemu_savevm_state",
      "file": "migration/savevm.c",
      "line": 1709
    },
    {
      "caller": "dirtylimit_is_allowed",
      "file": "system/dirtylimit.c",
      "line": 454
    },
    {
      "caller": "kvm_riscv_put_regs_timer",
      "file": "target/riscv/kvm/kvm-cpu.c",
      "line": 732
    }
  ]
}
```

- `resolve_symbol(name=migration_is_running)` →

```
{
  "resolved": true,
  "name": "migration_is_running",
  "version": "old",
  "file": "migration/migration.c",
  "line": 1106,
  "kind": "function",
  "signature": "bool migration_is_running(int state)",
  "resolution_method": "gtags_unique",
  "ambiguous": false
}
```

### Turn 2  _(tok 2819+497, stop=tool_use)_

**Reasoning:** Let me verify that each caller is genuine (not a comment, prototype, or the definition itself). I'll check each call site with get_context_at to confirm it's an actual call inside a function body.

Call sites:
1. migrate_fd_cancel at migration/migration.c:1480
2. migrate_prepare at migration/migration.c:1965
3. migrate_cap_set at migration/options.c:684
4. qmp_migrate_set_capabilities at migration/options.c:728
5. qemu_savevm_state at migration/savevm.c:1709
6. dirtylimit_is_allowed at system/dirtylimit.c:454
7. kvm_riscv_put_regs_timer at target/riscv/kvm/kvm-cpu.c:732

I'll check each one to make sure they are real calls. I can use get_context_at for each line.


- `get_context_at(file=migration/migration.c, line=1480)` →

```
migrate_fd_cancel — migration/migration.c:1465 [function] static void migrate_fd_cancel(MigrationState *s)
  reads: s; writes: s*; returns: -

SLICE around line 1480 (def-use, level 2; '>' marks the seed):
static void migrate_fd_cancel(MigrationState *s) {
   int old_state ;
   ...
   do {
     old_state = s->state;
>    if(!migration_is_running(old_state)) {
       break;
   ...
     }
   } while(s->state != MIGRATION_STATUS_CANCELLING);
}

CALLEES (8):
  qemu_file_shutdown (migration/qemu-file.c:64): reads f; writes -; returns return -ENOSYS; | return -EIO; | return 0;
  migrate_set_state (migration/migration.c:1363): reads new_state, old_state, state; writes -; returns -
  qemu_sem_post (util/qemu-thread-posix.c:273 (1 of 2 definitions)): reads sem; writes sem*; returns -
  migration_is_running (migration/migration.c:1106): reads state; writes -; returns return true; | return false;
  error_report_err (util/error.c:232): reads err; writes -; returns -
  bdrv_activate_all (block.c:6896): reads errp; writes -; returns -
  WITH_QEMU_LOCK_GUARD [macro]: #define WITH_QEMU_LOCK_GUARD(x) \
  not defined in this repository: trace_migrate_fd_cancel

CALLERS (1):
  migration_cancel (migration/migration.c:306): migrate_fd_cancel(current_migration);
```

- `get_context_at(file=migration/migration.c, line=1965)` →

```
migrate_prepare — migration/migration.c:1923 [function] static bool migrate_prepare(MigrationState *s, bool blk, bool blk_inc, bool resume, Error **errp)
  reads: blk, blk_inc, errp, resume, s; writes: s*; returns: return false; | return false; | return true; | return false; | return false; | return false;

SLICE around line 1965 (def-use, level 2; '>' marks the seed):
static bool migrate_prepare(MigrationState *s, bool blk, bool blk_inc, bool resume, Error **errp) {
   ...
>  if(migration_is_running(s->state)) {
     error_setg(errp, QERR_MIGRATION_ACTIVE);
     return false;
   ...
   }
}

CALLEES (19):
  warn_report (util/error-report.c:286): reads fmt; writes -; returns -
  migrate_release_ram (migration/options.c:330): reads -; writes -; returns return s->capabilities[MIGRATION_CAPABILITY_RELEASE_RAM];
  migration_is_running (migration/migration.c:1106): reads state; writes -; returns return true; | return false;
  runstate_check (system/runstate.c:187 (1 of 2 definitions)): reads state; writes -; returns return current_run_state == state;
  kvm_hwpoisoned_mem (accel/kvm/kvm-all.c:1160 (1 of 2 definitions)): reads -; writes -; returns return !QLIST_EMPTY(&hwpoison_page_list);
  migration_is_blocked (migration/migration.c:1906): reads errp; writes -; returns return true; | return true; | return false;
  migrate_multifd_compression (migration/options.c:877): reads -; writes -; returns return s->parameters.multifd_compression;
  migrate_tls (migration/options.c:400): reads -; writes -; returns return s->parameters.tls_creds && *s->parameters.tls_creds;
  migrate_mapped_ram (migration/options.c:267): reads -; writes -; returns return s->capabilities[MIGRATION_CAPABILITY_MAPPED_RAM];
  migrate_colo (migration/options.c:232): reads -; writes -; returns return s->capabilities[MIGRATION_CAPABILITY_X_COLO];
  migrate_background_snapshot (migration/options.c:218): reads -; writes -; returns return s->capabilities[MIGRATION_CAPABILITY_BACKGROUND_SNAPSHOT];
  migrate_postcopy (migration/options.c:388): reads -; writes -; returns return migrate_postcopy_ram()|| migrate_dirty_bitmaps();
  migrate_mode_is_cpr (migration/migration.c:1648): reads s; writes -; returns return s->parameters.mode == MIG_MODE_CPR_REBOOT;
  migrate_cap_set (migration/options.c:679): reads cap, errp, value; writes -; returns return false; | return false; | return true;
  migrate_block_incremental (migration/options.c:763): reads -; writes -; returns return s->parameters.block_incremental;
  migrate_block (migration/options.c:225): reads -; writes -; returns return s->capabilities[MIGRATION_CAPABILITY_BLOCK];
  migrate_set_block_incremental (migration/options.c:936): reads value; writes -; returns -
  migrate_init (migration/migration.c:1653): reads errp, s; writes s*; returns return ret; | return 0;
  error_setg [macro]: #define error_setg(errp, fmt, ...) \

CALLERS (1):
  qmp_migrate (migration/migration.c:2089): if (!migrate_prepare(s, has_blk && blk, has_inc && inc,
```

- `get_context_at(file=migration/options.c, line=684)` →

```
migrate_cap_set — migration/options.c:679 [function] bool migrate_cap_set(int cap, bool value, Error **errp)
  reads: cap, errp, value; writes: -; returns: return false; | return false; | return true;

SLICE around line 684 (def-use, level 2; '>' marks the seed):
bool migrate_cap_set(int cap, bool value, Error **errp) {
   MigrationState *s = migrate_get_current();
   ...
>  if(migration_is_running(s->state)) {
     error_setg(errp, QERR_MIGRATION_ACTIVE);
     return false;
   ...
   }
}

CALLEES (4):
  migrate_get_current (migration/migration.c:339): reads -; writes -; returns return current_migration;
  migration_is_running (migration/migration.c:1106): reads state; writes -; returns return true; | return false;
  migrate_caps_check (migration/options.c:479): reads errp, new_caps, old_caps; writes -; returns return false; | return false; | return false; | return false; | return false; | return false;
  error_setg [macro]: #define error_setg(errp, fmt, ...) \

CALLERS (2):
  migrate_prepare (migration/migration.c:2030): if (!migrate_cap_set(MIGRATION_CAPABILITY_BLOCK, true, errp)) {
  block_cleanup_parameters (migration/options.c:951): migrate_cap_set(MIGRATION_CAPABILITY_BLOCK, false, &error_abort);
```

- `get_context_at(file=migration/options.c, line=728)` →

```
qmp_migrate_set_capabilities — migration/options.c:721 [function] void qmp_migrate_set_capabilities(MigrationCapabilityStatusList *params, Error **errp)
  reads: errp, params; writes: -; returns: -

SLICE around line 728 (def-use, level 2; '>' marks the seed):
void qmp_migrate_set_capabilities(MigrationCapabilityStatusList *params, Error **errp) {
   MigrationState *s = migrate_get_current();
   ...
>  if(migration_is_running(s->state)|| migration_in_colo_state()) {
     error_setg(errp, QERR_MIGRATION_ACTIVE);
     return;
   ...
   }
}

CALLEES (5):
  migrate_get_current (migration/migration.c:339): reads -; writes -; returns return current_migration;
  migration_in_colo_state (migration/colo.c:47 (1 of 2 definitions)): reads -; writes -; returns return(s->state == MIGRATION_STATUS_COLO);
  migration_is_running (migration/migration.c:1106): reads state; writes -; returns return true; | return false;
  migrate_caps_check (migration/options.c:479): reads errp, new_caps, old_caps; writes -; returns return false; | return false; | return false; | return false; | return false; | return false;
  error_setg [macro]: #define error_setg(errp, fmt, ...) \

CALLERS (1):
  hmp_migrate_set_capability (migration/migration-hmp-cmds.c:509): qmp_migrate_set_capabilities(caps, &err);
```

- `get_context_at(file=migration/savevm.c, line=1709)` →

```
qemu_savevm_state — migration/savevm.c:1703 [function] static int qemu_savevm_state(QEMUFile *f, Error **errp)
  reads: errp, f; writes: -; returns: return -EINVAL; | return -EINVAL; | return ret; | return ret;

SLICE around line 1709 (def-use, level 2; '>' marks the seed):
static int qemu_savevm_state(QEMUFile *f, Error **errp) {
   ...
   MigrationState *ms = migrate_get_current();
   ...
>  if(migration_is_running(ms->state)) {
     error_setg(errp, QERR_MIGRATION_ACTIVE);
     return -EINVAL;
   ...
   }
}

CALLEES (13):
  migrate_get_current (migration/migration.c:339): reads -; writes -; returns return current_migration;
  migration_is_running (migration/migration.c:1106): reads state; writes -; returns return true; | return false;
  migrate_block (migration/options.c:225): reads -; writes -; returns return s->capabilities[MIGRATION_CAPABILITY_BLOCK];
  migrate_init (migration/migration.c:1653): reads errp, s; writes s*; returns return ret; | return 0;
  qemu_savevm_state_header (migration/savevm.c:1251): reads f; writes -; returns -
  qemu_savevm_state_setup (migration/savevm.c:1315): reads f; writes -; returns -
  qemu_savevm_state_iterate (migration/savevm.c:1394): reads f, postcopy; writes -; returns return 0; | return ret; | return all_finished;
  qemu_file_get_error (migration/qemu-file.c:209): reads f; writes -; returns return f->last_error;
  qemu_savevm_state_complete_precopy (migration/savevm.c:1604): reads f, inactivate_disks, iterable_only; writes -; returns return ret; | return ret; | return qemu_fflush(f);
  qemu_savevm_state_cleanup (migration/savevm.c:1686): reads -; writes -; returns -
  migrate_set_state (migration/migration.c:1363): reads new_state, old_state, state; writes -; returns -
  error_setg [macro]: #define error_setg(errp, fmt, ...) \
  error_setg_errno [macro]: #define error_setg_errno(errp, os_error, fmt, ...) \

CALLERS (1):
  save_snapshot (migration/savevm.c:3124): ret = qemu_savevm_state(f, errp);
```

- `get_context_at(file=system/dirtylimit.c, line=454)` →

```
dirtylimit_is_allowed — system/dirtylimit.c:450 [function] static bool dirtylimit_is_allowed(void)
  reads: -; writes: -; returns: return false; | return true;

SLICE around line 454 (def-use, level 2; '>' marks the seed):
static bool dirtylimit_is_allowed(void) {
   MigrationState *ms = migrate_get_current();
>  if(migration_is_running(ms->state)&&(!qemu_thread_is_self(&ms->thread))&& migrate_dirty_limit()&& dirtylimit_in_service()) {
     return false;
   ...
   }
}

CALLEES (5):
  migrate_get_current (migration/migration.c:339): reads -; writes -; returns return current_migration;
  dirtylimit_in_service (system/dirtylimit.c:231): reads -; writes -; returns return !!dirtylimit_state;
  migrate_dirty_limit (migration/options.c:253): reads -; writes -; returns return s->capabilities[MIGRATION_CAPABILITY_DIRTY_LIMIT];
  qemu_thread_is_self (util/qemu-thread-posix.c:666 (1 of 2 definitions)): reads thread; writes -; returns return pthread_equal(pthread_self(), thread->thread);
  migration_is_running (migration/migration.c:1106): reads state; writes -; returns return true; | return false;

CALLERS (2):
  qmp_cancel_vcpu_dirty_limit (system/dirtylimit.c:476): if (!dirtylimit_is_allowed()) {
  qmp_set_vcpu_dirty_limit (system/dirtylimit.c:532): if (!dirtylimit_is_allowed()) {
```

- `get_context_at(file=target/riscv/kvm/kvm-cpu.c, line=732)` →

```
kvm_riscv_put_regs_timer — target/riscv/kvm/kvm-cpu.c:705 [function] static void kvm_riscv_put_regs_timer(CPUState *cs)
  reads: cs; writes: -; returns: -

SLICE around line 732 (def-use, level 2; '>' marks the seed):
static void kvm_riscv_put_regs_timer(CPUState *cs) {
   uint64_t reg;
   CPURISCVState *env = &RISCV_CPU(cs)->env;
   ...
>  if(migration_is_running(migrate_get_current()->state)) {
     KVM_RISCV_GET_TIMER(cs, frequency, reg);
     if(reg != env->kvm_timer_frequency) {
   ...
     }
   }
}

CALLEES (6):
  error_report (util/error-report.c:271): reads fmt; writes -; returns -
  migration_is_running (migration/migration.c:1106): reads state; writes -; returns return true; | return false;
  migrate_get_current (migration/migration.c:339): reads -; writes -; returns return current_migration;
  KVM_RISCV_SET_TIMER [macro]: #define KVM_RISCV_SET_TIMER(cs, name, reg) \
  KVM_RISCV_GET_TIMER [macro]: #define KVM_RISCV_GET_TIMER(cs, name, reg) \
  not defined in this repository: RISCV_CPU

CALLERS (1):
  kvm_riscv_vm_state_change (target/riscv/kvm/kvm-cpu.c:1269): kvm_riscv_put_regs_timer(cs);
```

### Turn 3  _(tok 6737+381, stop=tool_use)_

**Reasoning:** All 7 call sites have been verified as actual calls within function bodies:

1. migrate_fd_cancel — migration/migration.c:1480 ✓
2. migrate_prepare — migration/migration.c:1965 ✓
3. migrate_cap_set — migration/options.c:684 ✓
4. qmp_migrate_set_capabilities — migration/options.c:728 ✓
5. qemu_savevm_state — migration/savevm.c:1709 ✓
6. dirtylimit_is_allowed — system/dirtylimit.c:454 ✓
7. kvm_riscv_put_regs_timer — target/riscv/kvm/kvm-cpu.c:732 ✓

None of them are prototypes, comments, or the definition itself. I'm confident. I'll submit.


**Says:** All seven call sites are verified as genuine calls inside function bodies (none are prototypes, comments, or the definition itself). Submitting the complete list.



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

