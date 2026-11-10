# Impact-analysis transcript — qemu @ aeaafb1e59f8 — anthropic:claude-haiku-5-5

- target: `migration_is_running` (migration/migration.c), arity 1->0
- truth: [['migration/migration.c', 'migrate_fd_cancel'], ['migration/migration.c', 'migrate_prepare'], ['migration/options.c', 'migrate_cap_set'], ['migration/options.c', 'qmp_migrate_set_capabilities'], ['migration/savevm.c', 'qemu_savevm_state'], ['system/dirtylimit.c', 'dirtylimit_is_allowed'], ['target/riscv/kvm/kvm-cpu.c', 'kvm_riscv_put_regs_timer']]

## Self-navigation arm

### Turn 1  _(tok 1209+120, stop=tool_use)_

**Reasoning:** I'm going to search the whole repo for every occurrence of migration_is_running to see where it's used.



- `grep(pattern=migration_is_running, version=old, max_results=300)` →

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

### Turn 2  _(tok 1612+870, stop=tool_use)_

**Reasoning:** I need the enclosing function name for each call site, so I'll read the code around each one. The sites are migration/migration.c at lines 1480 and 1965, options.c at 684 and 728, savevm.c at 1709, dirtylimit.c at 454, and kvm-cpu.c at 732. The grep already covered every file, so I don't think I'm missing any usages.



- `read_file(path=migration/migration.c, version=old, start_line=1460, end_line=1490)` →

```
migration/migration.c lines 1460-1490 of 3838
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

- `read_file(path=migration/migration.c, version=old, start_line=1950, end_line=1975)` →

```
migration/migration.c lines 1950-1975 of 3838
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

- `read_file(path=migration/options.c, version=old, start_line=670, end_line=740)` →

```
migration/options.c lines 670-740 of 1579
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
  736|     }
  737| 
  738|     if (!migrate_caps_check(s->capabilities, new_caps, errp)) {
  739|         return;
  740|     }
```

- `read_file(path=migration/savevm.c, version=old, start_line=1695, end_line=1720)` →

```
migration/savevm.c lines 1695-1720 of 3547
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
 1716|         return -EINVAL;
 1717|     }
 1718| 
 1719|     ret = migrate_init(ms, errp);
 1720|     if (ret) {
```

- `read_file(path=system/dirtylimit.c, version=old, start_line=440, end_line=465)` →

```
system/dirtylimit.c lines 440-465 of 682
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

- `read_file(path=target/riscv/kvm/kvm-cpu.c, version=old, start_line=715, end_line=745)` →

```
target/riscv/kvm/kvm-cpu.c lines 715-745 of 1821
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
  741| 
  742| static int kvm_riscv_get_regs_vector(CPUState *cs)
  743| {
  744|     RISCVCPU *cpu = RISCV_CPU(cs);
  745|     CPURISCVState *env = &cpu->env;
```

### Turn 3  _(tok 6171+523, stop=tool_use)_

**Reasoning:** I'm looking for the function that encloses migration.c line 1965, probably migrate_prepare or migrate_init_check. I also need the enclosing functions for the other call sites: options.c at 684 and 728, savevm at 1709, dirtylimit at 454, and the kvm-cpu code near line 700.

I still need the enclosing function for kvm-cpu.c line 732.



**Says:** I need the enclosing function for two sites whose headers I haven't seen yet: `migration/migration.c:1965` and `target/riscv/kvm/kvm-cpu.c:732`.

- `grep(pattern=^[a-z_].*\(|^static .*\(|^[A-Za-z].*\($, version=old, path_glob=migration/migration.c, max_results=300)` →

```
138 matches
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
migration/migration.c:181:migration_channels_and_transport_compatible(MigrationAddress *addr,
migration/migration.c:199:static gint page_request_addr_cmp(gconstpointer ap, gconstpointer bp)
migration/migration.c:206:static int migration_stop_vm(MigrationState *s, RunState state)
migration/migration.c:223:void migration_object_init(void)
migration/migration.c:263:static void migration_bh_dispatch_bh(void *opaque)
migration/migration.c:279:void migration_bh_schedule(QEMUBHFunc *cb, void *opaque)
migration/migration.c:298:void migration_cancel(const Error *error)
migration/migration.c:309:void migration_shutdown(void)
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
migration/migration.c:749:process_incoming_migration_co(void *opaque)
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
migration/migration.c:2195:migrate_handle_rp_req_pages(MigrationState *ms, const char* rbname,
migration/migration.c:2216:static bool migrate_handle_rp_recv_bitmap(MigrationState *s, char *block_name,
migration/migration.c:2231:static bool migrate_handle_rp_resume_ack(MigrationState *s,
migration/migration.c:2255:static void migration_release_dst_files(MigrationState *ms)
migration/migration.c:2287:static void *source_return_path_thread(void *opaque)
migration/migration.c:2448:static int open_return_path_on_source(MigrationState *ms)
migration/migration.c:2467:static bool close_return_path_on_source(MigrationState *ms)
migration/migration.c:2497:migration_wait_main_channel(MigrationState *ms)
migration/migration.c:2507:static int postcopy_start(MigrationState *ms, Error **errp)
migration/migration.c:2684:static int migration_maybe_pause(MigrationState *s,
migration/migration.c:2722:static int migration_completion_precopy(MigrationState *s,
migration/migration.c:2755:static void migration_completion_postcopy(MigrationState *s)
migration/migration.c:2774:static void migration_completion_failed(MigrationState *s,
migration/migration.c:2805:static void migration_completion(MigrationState *s)
migration/migration.c:2851:static void bg_migration_completion(MigrationState *s)
migration/migration.c:2890:static int postcopy_resume_handshake(MigrationState *s)
migration/migration.c:2908:static int postcopy_do_resume(MigrationState *s)
migration/migration.c:2955:static MigThrError postcopy_pause(MigrationState *s)
migration/migration.c:3025:static MigThrError migration_detect_error(MigrationState *s)
migration/migration.c:3075:static void migration_completion_end(MigrationState *s)
migration/migration.c:3099:static void update_iteration_initial_status(MigrationState *s)
migration/migration.c:3110:static void migration_update_counters(MigrationState *s,
migration/migration.c:3171:static bool migration_can_switchover(MigrationState *s)
migration/migration.c:3196:static MigIterateState migration_iteration_run(MigrationState *s)
migration/migration.c:3235:static void migration_iteration_finish(MigrationState *s)
migration/migration.c:3274:static void bg_migration_iteration_finish(MigrationState *s)
migration/migration.c:3306:static MigIterateState bg_migration_iteration_run(MigrationState *s)
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
migration/migration.c:3837:type_init(register_migration_types);
```

- `grep(pattern=^[a-zA-Z_].*\(, version=old, path_glob=target/riscv/kvm/kvm-cpu.c, max_results=300)` →

```
78 matches
target/riscv/kvm/kvm-cpu.c:54:void riscv_kvm_aplic_request(void *opaque, int irq, int level)
target/riscv/kvm/kvm-cpu.c:61:static uint64_t kvm_riscv_reg_id_ulong(CPURISCVState *env, uint64_t type,
target/riscv/kvm/kvm-cpu.c:79:static uint64_t kvm_riscv_reg_id_u32(uint64_t type, uint64_t idx)
target/riscv/kvm/kvm-cpu.c:84:static uint64_t kvm_riscv_reg_id_u64(uint64_t type, uint64_t idx)
target/riscv/kvm/kvm-cpu.c:89:static uint64_t kvm_encode_reg_size_id(uint64_t id, size_t size_b)
target/riscv/kvm/kvm-cpu.c:96:static uint64_t kvm_riscv_vector_reg_id(RISCVCPU *cpu,
target/riscv/kvm/kvm-cpu.c:189:static void kvm_cpu_get_misa_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:202:static void kvm_cpu_set_misa_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:235:static void kvm_riscv_update_cpu_misa_ext(RISCVCPU *cpu, CPUState *cs)
target/riscv/kvm/kvm-cpu.c:321:static void *kvmconfig_get_cfg_addr(RISCVCPU *cpu, KVMCPUConfig *kvmcfg)
target/riscv/kvm/kvm-cpu.c:326:static void kvm_cpu_cfg_set(RISCVCPU *cpu, KVMCPUConfig *multi_ext,
target/riscv/kvm/kvm-cpu.c:334:static uint32_t kvm_cpu_cfg_get(RISCVCPU *cpu,
target/riscv/kvm/kvm-cpu.c:342:static void kvm_cpu_get_multi_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:353:static void kvm_cpu_set_multi_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:412:static void kvm_riscv_update_cpu_cfg_isa_ext(RISCVCPU *cpu, CPUState *cs)
target/riscv/kvm/kvm-cpu.c:438:static void cpu_get_cfg_unavailable(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:447:static void cpu_set_cfg_unavailable(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:464:static void riscv_cpu_add_kvm_unavail_prop(Object *obj, const char *prop_name)
target/riscv/kvm/kvm-cpu.c:482:static void riscv_cpu_add_kvm_unavail_prop_array(Object *obj,
target/riscv/kvm/kvm-cpu.c:494:static void kvm_riscv_add_cpu_user_properties(Object *cpu_obj)
target/riscv/kvm/kvm-cpu.c:539:static int kvm_riscv_get_regs_core(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:564:static int kvm_riscv_put_regs_core(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:589:static int kvm_riscv_get_regs_csr(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:606:static int kvm_riscv_put_regs_csr(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:623:static int kvm_riscv_get_regs_fp(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:656:static int kvm_riscv_put_regs_fp(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:689:static void kvm_riscv_get_regs_timer(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:705:static void kvm_riscv_put_regs_timer(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:742:static int kvm_riscv_get_regs_vector(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:798:static int kvm_riscv_put_regs_vector(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:861:static bool kvm_riscv_create_scratch_vcpu(KVMScratchCPU *scratch)
target/riscv/kvm/kvm-cpu.c:900:static void kvm_riscv_destroy_scratch_vcpu(KVMScratchCPU *scratch)
target/riscv/kvm/kvm-cpu.c:907:static void kvm_riscv_init_machine_ids(RISCVCPU *cpu, KVMScratchCPU *kvmcpu)
target/riscv/kvm/kvm-cpu.c:935:static void kvm_riscv_init_misa_ext_mask(RISCVCPU *cpu,
target/riscv/kvm/kvm-cpu.c:956:static void kvm_riscv_read_cbomz_blksize(RISCVCPU *cpu, KVMScratchCPU *kvmcpu,
target/riscv/kvm/kvm-cpu.c:974:static void kvm_riscv_read_multiext_legacy(RISCVCPU *cpu,
target/riscv/kvm/kvm-cpu.c:1015:static int uint64_cmp(const void *a, const void *b)
target/riscv/kvm/kvm-cpu.c:1031:static void kvm_riscv_read_vlenb(RISCVCPU *cpu, KVMScratchCPU *kvmcpu,
target/riscv/kvm/kvm-cpu.c:1058:static void kvm_riscv_init_multiext_cfg(RISCVCPU *cpu, KVMScratchCPU *kvmcpu)
target/riscv/kvm/kvm-cpu.c:1138:static void riscv_init_kvm_registers(Object *cpu_obj)
target/riscv/kvm/kvm-cpu.c:1158:int kvm_arch_get_registers(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1185:int kvm_riscv_sync_mpstate_to_kvm(RISCVCPU *cpu, int state)
target/riscv/kvm/kvm-cpu.c:1203:int kvm_arch_put_registers(CPUState *cs, int level)
target/riscv/kvm/kvm-cpu.c:1242:int kvm_arch_release_virq_post(int virq)
target/riscv/kvm/kvm-cpu.c:1247:int kvm_arch_fixup_msi_route(struct kvm_irq_routing_entry *route,
target/riscv/kvm/kvm-cpu.c:1253:int kvm_arch_destroy_vcpu(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1258:unsigned long kvm_arch_vcpu_id(CPUState *cpu)
target/riscv/kvm/kvm-cpu.c:1263:static void kvm_riscv_vm_state_change(void *opaque, bool running,
target/riscv/kvm/kvm-cpu.c:1275:void kvm_arch_init_irq_routing(KVMState *s)
target/riscv/kvm/kvm-cpu.c:1279:static int kvm_vcpu_set_machine_ids(RISCVCPU *cpu, CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1310:int kvm_arch_init_vcpu(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1330:int kvm_arch_msi_data_to_gsi(uint32_t data)
target/riscv/kvm/kvm-cpu.c:1335:int kvm_arch_add_msi_route_post(struct kvm_irq_routing_entry *route,
target/riscv/kvm/kvm-cpu.c:1341:int kvm_arch_get_default_type(MachineState *ms)
target/riscv/kvm/kvm-cpu.c:1346:int kvm_arch_init(MachineState *ms, KVMState *s)
target/riscv/kvm/kvm-cpu.c:1352:int kvm_arch_irqchip_create(KVMState *s)
target/riscv/kvm/kvm-cpu.c:1365:int kvm_arch_process_async_events(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1370:void kvm_arch_pre_run(CPUState *cs, struct kvm_run *run)
target/riscv/kvm/kvm-cpu.c:1374:MemTxAttrs kvm_arch_post_run(CPUState *cs, struct kvm_run *run)
target/riscv/kvm/kvm-cpu.c:1379:bool kvm_arch_stop_on_emulation_error(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1384:static int kvm_riscv_handle_sbi(CPUState *cs, struct kvm_run *run)
target/riscv/kvm/kvm-cpu.c:1412:int kvm_arch_handle_exit(CPUState *cs, struct kvm_run *run)
target/riscv/kvm/kvm-cpu.c:1428:void kvm_riscv_reset_vcpu(RISCVCPU *cpu)
target/riscv/kvm/kvm-cpu.c:1452:void kvm_riscv_set_irq(RISCVCPU *cpu, int irq, int level)
target/riscv/kvm/kvm-cpu.c:1469:bool kvm_arch_cpu_check_are_resettable(void)
target/riscv/kvm/kvm-cpu.c:1476:static const char *kvm_aia_mode_str(uint64_t mode)
target/riscv/kvm/kvm-cpu.c:1489:static char *riscv_get_kvm_aia(Object *obj, Error **errp)
target/riscv/kvm/kvm-cpu.c:1494:static void riscv_set_kvm_aia(Object *obj, const char *val, Error **errp)
target/riscv/kvm/kvm-cpu.c:1508:void kvm_arch_accel_class_init(ObjectClass *oc)
target/riscv/kvm/kvm-cpu.c:1520:void kvm_riscv_aia_create(MachineState *machine, uint64_t group_shift,
target/riscv/kvm/kvm-cpu.c:1665:static void kvm_cpu_instance_init(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1681:static bool kvm_cpu_realize(CPUState *cs, Error **errp)
target/riscv/kvm/kvm-cpu.c:1698:void riscv_kvm_cpu_finalize_features(RISCVCPU *cpu, Error **errp)
target/riscv/kvm/kvm-cpu.c:1780:static void kvm_cpu_accel_class_init(ObjectClass *oc, void *data)
target/riscv/kvm/kvm-cpu.c:1795:static void kvm_cpu_accel_register_types(void)
target/riscv/kvm/kvm-cpu.c:1799:type_init(kvm_cpu_accel_register_types);
target/riscv/kvm/kvm-cpu.c:1801:static void riscv_host_cpu_class_init(ObjectClass *c, void *data)
target/riscv/kvm/kvm-cpu.c:1820:DEFINE_TYPES(riscv_kvm_cpu_type_infos)
```

### Turn 4  _(tok 15584+626, stop=tool_use)_

**Reasoning:** I'm confirming that the line at migration.c:1965 falls inside migrate_prepare, which runs from 1923 to 2047, and that the KVM line at kvm-cpu.c:732 sits in kvm_riscv_put_regs_timer. Now I'm listing the callers, starting with migrate_fd_cancel and migrate_prepare in migration.c.

I'm going through the rest of the callers, including the options.c capability setters, savevm's state save, the dirty-limit check, and the RISC-V KVM timer register path. I'm also deciding whether the git grep over tracked files already covers non-C sources and header macros, which I think it does.



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1378+142, stop=tool_use)_

**Reasoning:** I'll look up the references with find_references and then search the codebase with grep.



- `find_references(name=migration_is_running)` →

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

- `grep(pattern=migration_is_running, version=old)` →

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

### Turn 2  _(tok 2154+765, stop=tool_use)_

**Reasoning:** I need the enclosing functions for each line, so I'll read the code around each one.



**Says:** I have the call sites. Now I need the enclosing function for each one.

- `read_file(path=migration/migration.c, version=old, start_line=1455, end_line=1482)` →

```
migration/migration.c lines 1455-1482 of 3838
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
```

- `read_file(path=migration/migration.c, version=old, start_line=1945, end_line=1968)` →

```
migration/migration.c lines 1945-1968 of 3838
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
```

- `read_file(path=migration/options.c, version=old, start_line=670, end_line=735)` →

```
migration/options.c lines 670-735 of 1579
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

- `read_file(path=migration/savevm.c, version=old, start_line=1690, end_line=1712)` →

```
migration/savevm.c lines 1690-1712 of 3547
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
```

- `read_file(path=system/dirtylimit.c, version=old, start_line=440, end_line=460)` →

```
system/dirtylimit.c lines 440-460 of 682
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

- `read_file(path=target/riscv/kvm/kvm-cpu.c, version=old, start_line=715, end_line=740)` →

```
target/riscv/kvm/kvm-cpu.c lines 715-740 of 1821
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

### Turn 3  _(tok 6254+525, stop=tool_use)_

**Reasoning:** I'm pinning down which function encloses each of the flagged source lines, starting with migration.c:1480, options.c:684 and 728, savevm.c:1709, dirtylimit.c:454, and then the two spots whose enclosing function I still have to locate.

I still need the enclosing function for migration.c line 1965 and for kvm-cpu.c line 732.



**Says:** Most enclosing functions are now clear. Two still need their definitions located: the call at `migration/migration.c:1965` and the one at `target/riscv/kvm/kvm-cpu.c:732`.

- `grep(pattern=^[a-z_A-Z].*\(, version=old, path_glob=migration/migration.c, max_results=400)` →

```
141 matches
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
migration/migration.c:181:migration_channels_and_transport_compatible(MigrationAddress *addr,
migration/migration.c:199:static gint page_request_addr_cmp(gconstpointer ap, gconstpointer bp)
migration/migration.c:206:static int migration_stop_vm(MigrationState *s, RunState state)
migration/migration.c:223:void migration_object_init(void)
migration/migration.c:263:static void migration_bh_dispatch_bh(void *opaque)
migration/migration.c:279:void migration_bh_schedule(QEMUBHFunc *cb, void *opaque)
migration/migration.c:298:void migration_cancel(const Error *error)
migration/migration.c:309:void migration_shutdown(void)
migration/migration.c:339:MigrationState *migrate_get_current(void)
migration/migration.c:346:MigrationIncomingState *migration_incoming_get_current(void)
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
migration/migration.c:749:process_incoming_migration_co(void *opaque)
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
migration/migration.c:1329:MigrationInfo *qmp_query_migrate(Error **errp)
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
migration/migration.c:2195:migrate_handle_rp_req_pages(MigrationState *ms, const char* rbname,
migration/migration.c:2216:static bool migrate_handle_rp_recv_bitmap(MigrationState *s, char *block_name,
migration/migration.c:2231:static bool migrate_handle_rp_resume_ack(MigrationState *s,
migration/migration.c:2255:static void migration_release_dst_files(MigrationState *ms)
migration/migration.c:2287:static void *source_return_path_thread(void *opaque)
migration/migration.c:2448:static int open_return_path_on_source(MigrationState *ms)
migration/migration.c:2467:static bool close_return_path_on_source(MigrationState *ms)
migration/migration.c:2497:migration_wait_main_channel(MigrationState *ms)
migration/migration.c:2507:static int postcopy_start(MigrationState *ms, Error **errp)
migration/migration.c:2684:static int migration_maybe_pause(MigrationState *s,
migration/migration.c:2722:static int migration_completion_precopy(MigrationState *s,
migration/migration.c:2755:static void migration_completion_postcopy(MigrationState *s)
migration/migration.c:2774:static void migration_completion_failed(MigrationState *s,
migration/migration.c:2805:static void migration_completion(MigrationState *s)
migration/migration.c:2851:static void bg_migration_completion(MigrationState *s)
migration/migration.c:2890:static int postcopy_resume_handshake(MigrationState *s)
migration/migration.c:2908:static int postcopy_do_resume(MigrationState *s)
migration/migration.c:2955:static MigThrError postcopy_pause(MigrationState *s)
migration/migration.c:3025:static MigThrError migration_detect_error(MigrationState *s)
migration/migration.c:3075:static void migration_completion_end(MigrationState *s)
migration/migration.c:3099:static void update_iteration_initial_status(MigrationState *s)
migration/migration.c:3110:static void migration_update_counters(MigrationState *s,
migration/migration.c:3171:static bool migration_can_switchover(MigrationState *s)
migration/migration.c:3196:static MigIterateState migration_iteration_run(MigrationState *s)
migration/migration.c:3235:static void migration_iteration_finish(MigrationState *s)
migration/migration.c:3274:static void bg_migration_iteration_finish(MigrationState *s)
migration/migration.c:3306:static MigIterateState bg_migration_iteration_run(MigrationState *s)
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
migration/migration.c:3837:type_init(register_migration_types);
```

- `grep(pattern=^[a-z_A-Z].*\(, version=old, path_glob=target/riscv/kvm/kvm-cpu.c, max_results=400)` →

```
78 matches
target/riscv/kvm/kvm-cpu.c:54:void riscv_kvm_aplic_request(void *opaque, int irq, int level)
target/riscv/kvm/kvm-cpu.c:61:static uint64_t kvm_riscv_reg_id_ulong(CPURISCVState *env, uint64_t type,
target/riscv/kvm/kvm-cpu.c:79:static uint64_t kvm_riscv_reg_id_u32(uint64_t type, uint64_t idx)
target/riscv/kvm/kvm-cpu.c:84:static uint64_t kvm_riscv_reg_id_u64(uint64_t type, uint64_t idx)
target/riscv/kvm/kvm-cpu.c:89:static uint64_t kvm_encode_reg_size_id(uint64_t id, size_t size_b)
target/riscv/kvm/kvm-cpu.c:96:static uint64_t kvm_riscv_vector_reg_id(RISCVCPU *cpu,
target/riscv/kvm/kvm-cpu.c:189:static void kvm_cpu_get_misa_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:202:static void kvm_cpu_set_misa_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:235:static void kvm_riscv_update_cpu_misa_ext(RISCVCPU *cpu, CPUState *cs)
target/riscv/kvm/kvm-cpu.c:321:static void *kvmconfig_get_cfg_addr(RISCVCPU *cpu, KVMCPUConfig *kvmcfg)
target/riscv/kvm/kvm-cpu.c:326:static void kvm_cpu_cfg_set(RISCVCPU *cpu, KVMCPUConfig *multi_ext,
target/riscv/kvm/kvm-cpu.c:334:static uint32_t kvm_cpu_cfg_get(RISCVCPU *cpu,
target/riscv/kvm/kvm-cpu.c:342:static void kvm_cpu_get_multi_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:353:static void kvm_cpu_set_multi_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:412:static void kvm_riscv_update_cpu_cfg_isa_ext(RISCVCPU *cpu, CPUState *cs)
target/riscv/kvm/kvm-cpu.c:438:static void cpu_get_cfg_unavailable(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:447:static void cpu_set_cfg_unavailable(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:464:static void riscv_cpu_add_kvm_unavail_prop(Object *obj, const char *prop_name)
target/riscv/kvm/kvm-cpu.c:482:static void riscv_cpu_add_kvm_unavail_prop_array(Object *obj,
target/riscv/kvm/kvm-cpu.c:494:static void kvm_riscv_add_cpu_user_properties(Object *cpu_obj)
target/riscv/kvm/kvm-cpu.c:539:static int kvm_riscv_get_regs_core(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:564:static int kvm_riscv_put_regs_core(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:589:static int kvm_riscv_get_regs_csr(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:606:static int kvm_riscv_put_regs_csr(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:623:static int kvm_riscv_get_regs_fp(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:656:static int kvm_riscv_put_regs_fp(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:689:static void kvm_riscv_get_regs_timer(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:705:static void kvm_riscv_put_regs_timer(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:742:static int kvm_riscv_get_regs_vector(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:798:static int kvm_riscv_put_regs_vector(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:861:static bool kvm_riscv_create_scratch_vcpu(KVMScratchCPU *scratch)
target/riscv/kvm/kvm-cpu.c:900:static void kvm_riscv_destroy_scratch_vcpu(KVMScratchCPU *scratch)
target/riscv/kvm/kvm-cpu.c:907:static void kvm_riscv_init_machine_ids(RISCVCPU *cpu, KVMScratchCPU *kvmcpu)
target/riscv/kvm/kvm-cpu.c:935:static void kvm_riscv_init_misa_ext_mask(RISCVCPU *cpu,
target/riscv/kvm/kvm-cpu.c:956:static void kvm_riscv_read_cbomz_blksize(RISCVCPU *cpu, KVMScratchCPU *kvmcpu,
target/riscv/kvm/kvm-cpu.c:974:static void kvm_riscv_read_multiext_legacy(RISCVCPU *cpu,
target/riscv/kvm/kvm-cpu.c:1015:static int uint64_cmp(const void *a, const void *b)
target/riscv/kvm/kvm-cpu.c:1031:static void kvm_riscv_read_vlenb(RISCVCPU *cpu, KVMScratchCPU *kvmcpu,
target/riscv/kvm/kvm-cpu.c:1058:static void kvm_riscv_init_multiext_cfg(RISCVCPU *cpu, KVMScratchCPU *kvmcpu)
target/riscv/kvm/kvm-cpu.c:1138:static void riscv_init_kvm_registers(Object *cpu_obj)
target/riscv/kvm/kvm-cpu.c:1158:int kvm_arch_get_registers(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1185:int kvm_riscv_sync_mpstate_to_kvm(RISCVCPU *cpu, int state)
target/riscv/kvm/kvm-cpu.c:1203:int kvm_arch_put_registers(CPUState *cs, int level)
target/riscv/kvm/kvm-cpu.c:1242:int kvm_arch_release_virq_post(int virq)
target/riscv/kvm/kvm-cpu.c:1247:int kvm_arch_fixup_msi_route(struct kvm_irq_routing_entry *route,
target/riscv/kvm/kvm-cpu.c:1253:int kvm_arch_destroy_vcpu(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1258:unsigned long kvm_arch_vcpu_id(CPUState *cpu)
target/riscv/kvm/kvm-cpu.c:1263:static void kvm_riscv_vm_state_change(void *opaque, bool running,
target/riscv/kvm/kvm-cpu.c:1275:void kvm_arch_init_irq_routing(KVMState *s)
target/riscv/kvm/kvm-cpu.c:1279:static int kvm_vcpu_set_machine_ids(RISCVCPU *cpu, CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1310:int kvm_arch_init_vcpu(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1330:int kvm_arch_msi_data_to_gsi(uint32_t data)
target/riscv/kvm/kvm-cpu.c:1335:int kvm_arch_add_msi_route_post(struct kvm_irq_routing_entry *route,
target/riscv/kvm/kvm-cpu.c:1341:int kvm_arch_get_default_type(MachineState *ms)
target/riscv/kvm/kvm-cpu.c:1346:int kvm_arch_init(MachineState *ms, KVMState *s)
target/riscv/kvm/kvm-cpu.c:1352:int kvm_arch_irqchip_create(KVMState *s)
target/riscv/kvm/kvm-cpu.c:1365:int kvm_arch_process_async_events(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1370:void kvm_arch_pre_run(CPUState *cs, struct kvm_run *run)
target/riscv/kvm/kvm-cpu.c:1374:MemTxAttrs kvm_arch_post_run(CPUState *cs, struct kvm_run *run)
target/riscv/kvm/kvm-cpu.c:1379:bool kvm_arch_stop_on_emulation_error(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1384:static int kvm_riscv_handle_sbi(CPUState *cs, struct kvm_run *run)
target/riscv/kvm/kvm-cpu.c:1412:int kvm_arch_handle_exit(CPUState *cs, struct kvm_run *run)
target/riscv/kvm/kvm-cpu.c:1428:void kvm_riscv_reset_vcpu(RISCVCPU *cpu)
target/riscv/kvm/kvm-cpu.c:1452:void kvm_riscv_set_irq(RISCVCPU *cpu, int irq, int level)
target/riscv/kvm/kvm-cpu.c:1469:bool kvm_arch_cpu_check_are_resettable(void)
target/riscv/kvm/kvm-cpu.c:1476:static const char *kvm_aia_mode_str(uint64_t mode)
target/riscv/kvm/kvm-cpu.c:1489:static char *riscv_get_kvm_aia(Object *obj, Error **errp)
target/riscv/kvm/kvm-cpu.c:1494:static void riscv_set_kvm_aia(Object *obj, const char *val, Error **errp)
target/riscv/kvm/kvm-cpu.c:1508:void kvm_arch_accel_class_init(ObjectClass *oc)
target/riscv/kvm/kvm-cpu.c:1520:void kvm_riscv_aia_create(MachineState *machine, uint64_t group_shift,
target/riscv/kvm/kvm-cpu.c:1665:static void kvm_cpu_instance_init(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:1681:static bool kvm_cpu_realize(CPUState *cs, Error **errp)
target/riscv/kvm/kvm-cpu.c:1698:void riscv_kvm_cpu_finalize_features(RISCVCPU *cpu, Error **errp)
target/riscv/kvm/kvm-cpu.c:1780:static void kvm_cpu_accel_class_init(ObjectClass *oc, void *data)
target/riscv/kvm/kvm-cpu.c:1795:static void kvm_cpu_accel_register_types(void)
target/riscv/kvm/kvm-cpu.c:1799:type_init(kvm_cpu_accel_register_types);
target/riscv/kvm/kvm-cpu.c:1801:static void riscv_host_cpu_class_init(ObjectClass *c, void *data)
target/riscv/kvm/kvm-cpu.c:1820:DEFINE_TYPES(riscv_kvm_cpu_type_infos)
```

### Turn 4  _(tok 15766+808, stop=tool_use)_

**Reasoning:** I'm checking that line 1965 falls inside migrate_prepare, which runs from 1923 to 2046, and it does since the next function starts at 2047. Line 732 also sits inside kvm_riscv_put_regs_timer, which spans 705 to 741, so that one checks out too. Next I'm wondering whether any macros or function pointers reference migration_is_running.

Now I'm confirming that the callers list is complete: the grep covered the whole repo, and there are 7 callers once the header prototype is excluded.



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3744+250, stop=tool_use)_

**Reasoning:** I'm going to call get_callers on migration_is_running with a high limit first. I also want to run a grep, since get_callers might miss indirect uses like function pointers or macros.



- `get_callers(name=migration_is_running, limit=500, rev=None)` →

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

- `grep(pattern=migration_is_running, version=old, max_results=500)` →

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

### Turn 2  _(tok 4700+495, stop=tool_use)_

**Reasoning:** I've got 9 grep matches: the definition, the prototype, and 7 call sites. I'll check the enclosing function names for each, starting with whether the call at line 1480 really sits inside migrate_fd_cancel, and confirm it with get_context_at on a couple of them.

I'll spot-check the riscv call and the dirtylimit one with get_context_at, since either could be inside a macro or another function. It's a quick check, so it's worth doing.



- `get_context_at(file=target/riscv/kvm/kvm-cpu.c, line=732, version=old)` →

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

- `get_context_at(file=system/dirtylimit.c, line=454, version=old)` →

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

- `get_context_at(file=migration/migration.c, line=1480, version=old)` →

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

### Turn 3  _(tok 7021+428, stop=tool_use)_

**Reasoning:** I'm checking the seven call sites against the function names. Listing them out, I count seven distinct functions, so the earlier six-function guess was wrong.



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3196+102, stop=tool_use)_

**Reasoning:** I'm going to call get_callers on migration_is_running with a high limit to see every call site.



- `get_callers(name=migration_is_running, limit=200)` →

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

### Turn 2  _(tok 3675+170, stop=tool_use)_

**Reasoning:** I'm checking whether the tool's default version is "old" (the parent of rev) rather than the server commit, since the output shows that. The task most likely concerns the current repo, so I'll re-run the check with version "work" to confirm.



- `get_callers(name=migration_is_running, limit=200, version=work)` →

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

### Turn 3  _(tok 4222+416, stop=tool_use)_

**Reasoning:** Both versions report "old", which is odd, so the server's state might be off. I'm now weighing whether to check callers and call sites through the "work" version too, since the tool might miss macros or function pointer uses.

I'm going to check the code at migration/migration.c line 1480 in the work version, since the version field keeps reporting "old" and I want to confirm the change is really there.



- `get_context_at(file=migration/migration.c, line=1480, version=work)` →

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

- `get_neighborhood(name=migration_is_running, version=work)` →

```
migration_is_running — migration/migration.c:1106 [function] bool migration_is_running(int state)
  reads: state; writes: -; returns: return true; | return false;

CALLEES (0):

CALLERS (7):
  migrate_fd_cancel (migration/migration.c:1480): if (!migration_is_running(old_state)) {
  migrate_prepare (migration/migration.c:1965): if (migration_is_running(s->state)) {
  migrate_cap_set (migration/options.c:684): if (migration_is_running(s->state)) {
  qmp_migrate_set_capabilities (migration/options.c:728): if (migration_is_running(s->state) || migration_in_colo_state()) {
  qemu_savevm_state (migration/savevm.c:1709): if (migration_is_running(ms->state)) {
  dirtylimit_is_allowed (system/dirtylimit.c:454): if (migration_is_running(ms->state) &&
  kvm_riscv_put_regs_timer (target/riscv/kvm/kvm-cpu.c:732): if (migration_is_running(migrate_get_current()->state)) {
```

### Turn 4  _(tok 5653+352, stop=tool_use)_

**Reasoning:** The results line up, so I'll submit this with the 7 callers. My confidence is fairly high, though the tool may be missing calls made through function pointers.



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

