# Impact-analysis transcript — qemu @ aeaafb1e59f8 — anthropic:claude-haiku-5-5

- target: `migration_is_running` (migration/migration.c), arity 1->0
- truth: [['migration/migration.c', 'migrate_fd_cancel'], ['migration/migration.c', 'migrate_prepare'], ['migration/options.c', 'migrate_cap_set'], ['migration/options.c', 'qmp_migrate_set_capabilities'], ['migration/savevm.c', 'qemu_savevm_state'], ['system/dirtylimit.c', 'dirtylimit_is_allowed'], ['target/riscv/kvm/kvm-cpu.c', 'kvm_riscv_put_regs_timer']]

## Self-navigation arm

### Turn 1  _(tok 1209+97, stop=tool_use)_

**Reasoning:** I'm going to grep the whole repo for migration_is_running to find every place it's referenced.



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

### Turn 2  _(tok 1589+805, stop=tool_use)_

**Reasoning:** I need the names of the enclosing functions, so I'll read the code around each match. Grep could also miss function pointers or macros, but that's acceptable for now. Next I'm checking those lines.



**Says:** Nine matches. I need the enclosing function for each call site, so I'll read the surrounding code.

- `read_file(path=migration/migration.c, version=old, start_line=1455, end_line=1485)` →

```
migration/migration.c lines 1455-1485 of 3838
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
```

- `read_file(path=migration/migration.c, version=old, start_line=1945, end_line=1970)` →

```
migration/migration.c lines 1945-1970 of 3838
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

- `read_file(path=migration/savevm.c, version=old, start_line=1695, end_line=1715)` →

```
migration/savevm.c lines 1695-1715 of 3547
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

### Turn 3  _(tok 5994+451, stop=tool_use)_

**Reasoning:** I'm hunting for the enclosing function headers: one in migration.c above line 1965 and one in kvm-cpu.c above line 732. The other references (options.c:684, savevm.c:1709, dirtylimit.c:454) are already settled.



**Says:** Most enclosing functions are confirmed. Two still need their headers: the `migration.c:1965` site and the `kvm-cpu.c:732` site.

- `grep(pattern=^[a-z_A-Z].*\(|^\{, version=old, path_glob=migration/migration.c, max_results=400)` →

```
276 matches (showing 200)
migration/migration.c:104:static bool migration_object_check(MigrationState *ms, Error **errp);
migration/migration.c:105:static int migration_maybe_pause(MigrationState *s,
migration/migration.c:108:static void migrate_fd_cancel(MigrationState *s);
migration/migration.c:109:static bool close_return_path_on_source(MigrationState *s);
migration/migration.c:110:static void migration_completion_end(MigrationState *s);
migration/migration.c:112:static void migration_downtime_start(MigrationState *s)
migration/migration.c:113:{
migration/migration.c:118:static void migration_downtime_end(MigrationState *s)
migration/migration.c:119:{
migration/migration.c:133:static bool migration_needs_multiple_sockets(void)
migration/migration.c:134:{
migration/migration.c:138:static bool transport_supports_multi_channels(MigrationAddress *addr)
migration/migration.c:139:{
migration/migration.c:157:static bool migration_needs_seekable_channel(void)
migration/migration.c:158:{
migration/migration.c:162:static bool transport_supports_seeking(MigrationAddress *addr)
migration/migration.c:163:{
migration/migration.c:181:migration_channels_and_transport_compatible(MigrationAddress *addr,
migration/migration.c:183:{
migration/migration.c:199:static gint page_request_addr_cmp(gconstpointer ap, gconstpointer bp)
migration/migration.c:200:{
migration/migration.c:206:static int migration_stop_vm(MigrationState *s, RunState state)
migration/migration.c:207:{
migration/migration.c:223:void migration_object_init(void)
migration/migration.c:224:{
migration/migration.c:263:static void migration_bh_dispatch_bh(void *opaque)
migration/migration.c:264:{
migration/migration.c:279:void migration_bh_schedule(QEMUBHFunc *cb, void *opaque)
migration/migration.c:280:{
migration/migration.c:298:void migration_cancel(const Error *error)
migration/migration.c:299:{
migration/migration.c:309:void migration_shutdown(void)
migration/migration.c:310:{
migration/migration.c:339:MigrationState *migrate_get_current(void)
migration/migration.c:340:{
migration/migration.c:346:MigrationIncomingState *migration_incoming_get_current(void)
migration/migration.c:347:{
migration/migration.c:352:void migration_incoming_transport_cleanup(MigrationIncomingState *mis)
migration/migration.c:353:{
migration/migration.c:365:void migration_incoming_state_destroy(void)
migration/migration.c:366:{
migration/migration.c:406:static void migrate_generate_event(int new_state)
migration/migration.c:407:{
migration/migration.c:417:static int migrate_send_rp_message(MigrationIncomingState *mis,
migration/migration.c:420:{
migration/migration.c:446:int migrate_send_rp_message_req_pages(MigrationIncomingState *mis,
migration/migration.c:448:{
migration/migration.c:483:int migrate_send_rp_req_pages(MigrationIncomingState *mis,
migration/migration.c:485:{
migration/migration.c:515:bool migration_incoming_colo_enabled(void)
migration/migration.c:516:{
migration/migration.c:520:void migration_incoming_disable_colo(void)
migration/migration.c:521:{
migration/migration.c:526:int migration_incoming_enable_colo(void)
migration/migration.c:527:{
migration/migration.c:548:void migrate_add_address(SocketAddress *address)
migration/migration.c:549:{
migration/migration.c:556:bool migrate_uri_parse(const char *uri, MigrationChannel **channel,
migration/migration.c:558:{
migration/migration.c:611:static void qemu_start_incoming_migration(const char *uri, bool has_channels,
migration/migration.c:614:{
migration/migration.c:686:static void process_incoming_migration_bh(void *opaque)
migration/migration.c:687:{
migration/migration.c:749:process_incoming_migration_co(void *opaque)
migration/migration.c:750:{
migration/migration.c:827:static void migration_incoming_setup(QEMUFile *f)
migration/migration.c:828:{
migration/migration.c:837:void migration_incoming_process(void)
migration/migration.c:838:{
migration/migration.c:844:static bool postcopy_try_recover(void)
migration/migration.c:845:{
migration/migration.c:876:void migration_fd_process_incoming(QEMUFile *f)
migration/migration.c:877:{
migration/migration.c:889:static bool migration_should_start_incoming(bool main_channel)
migration/migration.c:890:{
migration/migration.c:910:void migration_ioc_process_incoming(QIOChannel *ioc, Error **errp)
migration/migration.c:911:{
migration/migration.c:982:bool migration_has_all_channels(void)
migration/migration.c:983:{
migration/migration.c:1001:int migrate_send_rp_switchover_ack(MigrationIncomingState *mis)
migration/migration.c:1002:{
migration/migration.c:1011:void migrate_send_rp_shut(MigrationIncomingState *mis,
migration/migration.c:1013:{
migration/migration.c:1024:void migrate_send_rp_pong(MigrationIncomingState *mis,
migration/migration.c:1026:{
migration/migration.c:1033:void migrate_send_rp_recv_bitmap(MigrationIncomingState *mis,
migration/migration.c:1035:{
migration/migration.c:1072:void migrate_send_rp_resume_ack(MigrationIncomingState *mis, uint32_t value)
migration/migration.c:1073:{
migration/migration.c:1084:bool migration_is_setup_or_active(void)
migration/migration.c:1085:{
migration/migration.c:1106:bool migration_is_running(int state)
migration/migration.c:1107:{
migration/migration.c:1126:static bool migrate_show_downtime(MigrationState *s)
migration/migration.c:1127:{
migration/migration.c:1131:static void populate_time_info(MigrationInfo *info, MigrationState *s)
migration/migration.c:1132:{
migration/migration.c:1155:static void populate_ram_info(MigrationInfo *info, MigrationState *s)
migration/migration.c:1156:{
migration/migration.c:1215:static void populate_disk_info(MigrationInfo *info)
migration/migration.c:1216:{
migration/migration.c:1225:static void fill_source_migration_info(MigrationInfo *info)
migration/migration.c:1226:{
migration/migration.c:1297:static void fill_destination_migration_info(MigrationInfo *info)
migration/migration.c:1298:{
migration/migration.c:1329:MigrationInfo *qmp_query_migrate(Error **errp)
migration/migration.c:1330:{
migration/migration.c:1339:void qmp_migrate_start_postcopy(Error **errp)
migration/migration.c:1340:{
migration/migration.c:1363:void migrate_set_state(int *state, int old_state, int new_state)
migration/migration.c:1364:{
migration/migration.c:1372:static void migrate_fd_cleanup(MigrationState *s)
migration/migration.c:1373:{
migration/migration.c:1427:static void migrate_fd_cleanup_bh(void *opaque)
migration/migration.c:1428:{
migration/migration.c:1432:void migrate_set_error(MigrationState *s, const Error *error)
migration/migration.c:1433:{
migration/migration.c:1440:bool migrate_has_error(MigrationState *s)
migration/migration.c:1441:{
migration/migration.c:1447:static void migrate_error_free(MigrationState *s)
migration/migration.c:1448:{
migration/migration.c:1456:static void migrate_fd_error(MigrationState *s, const Error *error)
migration/migration.c:1457:{
migration/migration.c:1465:static void migrate_fd_cancel(MigrationState *s)
migration/migration.c:1466:{
migration/migration.c:1514:void migration_add_notifier_mode(NotifierWithReturn *notify,
migration/migration.c:1516:{
migration/migration.c:1521:void migration_add_notifier(NotifierWithReturn *notify,
migration/migration.c:1523:{
migration/migration.c:1527:void migration_remove_notifier(NotifierWithReturn *notify)
migration/migration.c:1528:{
migration/migration.c:1535:int migration_call_notifiers(MigrationState *s, MigrationEventType type,
migration/migration.c:1537:{
migration/migration.c:1549:bool migration_in_setup(MigrationState *s)
migration/migration.c:1550:{
migration/migration.c:1554:bool migration_has_finished(MigrationState *s)
migration/migration.c:1555:{
migration/migration.c:1559:bool migration_has_failed(MigrationState *s)
migration/migration.c:1560:{
migration/migration.c:1565:bool migration_in_postcopy(void)
migration/migration.c:1566:{
migration/migration.c:1579:bool migration_postcopy_is_alive(int state)
migration/migration.c:1580:{
migration/migration.c:1590:bool migration_in_incoming_postcopy(void)
migration/migration.c:1591:{
migration/migration.c:1597:bool migration_incoming_postcopy_advised(void)
migration/migration.c:1598:{
migration/migration.c:1604:bool migration_in_bg_snapshot(void)
migration/migration.c:1605:{
migration/migration.c:1610:bool migration_is_idle(void)
migration/migration.c:1611:{
migration/migration.c:1640:bool migration_is_active(void)
migration/migration.c:1641:{
migration/migration.c:1648:bool migrate_mode_is_cpr(MigrationState *s)
migration/migration.c:1649:{
migration/migration.c:1653:int migrate_init(MigrationState *s, Error **errp)
migration/migration.c:1654:{
migration/migration.c:1699:static bool is_busy(Error **reasonp, Error **errp)
migration/migration.c:1700:{
migration/migration.c:1714:static bool is_only_migratable(Error **reasonp, Error **errp, int modes)
migration/migration.c:1715:{
migration/migration.c:1728:static int get_modes(MigMode mode, va_list ap)
migration/migration.c:1729:{
migration/migration.c:1743:static int add_blockers(Error **reasonp, Error **errp, int modes)
migration/migration.c:1744:{
migration/migration.c:1754:int migrate_add_blocker(Error **reasonp, Error **errp)
migration/migration.c:1755:{
migration/migration.c:1759:int migrate_add_blocker_normal(Error **reasonp, Error **errp)
migration/migration.c:1760:{
migration/migration.c:1764:int migrate_add_blocker_modes(Error **reasonp, Error **errp, MigMode mode, ...)
migration/migration.c:1765:{
migration/migration.c:1781:int migrate_add_blocker_internal(Error **reasonp, Error **errp)
migration/migration.c:1782:{
migration/migration.c:1791:void migrate_del_blocker(Error **reasonp)
migration/migration.c:1792:{
migration/migration.c:1803:void qmp_migrate_incoming(const char *uri, bool has_channels,
migration/migration.c:1805:{
migration/migration.c:1833:void qmp_migrate_recover(const char *uri, Error **errp)
migration/migration.c:1834:{
migration/migration.c:1861:void qmp_migrate_pause(Error **errp)
migration/migration.c:1862:{
migration/migration.c:1906:bool migration_is_blocked(Error **errp)
migration/migration.c:1907:{
migration/migration.c:1923:static bool migrate_prepare(MigrationState *s, bool blk, bool blk_inc,
migration/migration.c:1925:{
migration/migration.c:2047:void qmp_migrate(const char *uri, bool has_channels,
migration/migration.c:2051:{
migration/migration.c:2136:void qmp_migrate_cancel(Error **errp)
migration/migration.c:2137:{
migration/migration.c:2141:void qmp_migrate_continue(MigrationStatus state, Error **errp)
migration/migration.c:2142:{
migration/migration.c:2152:int migration_rp_wait(MigrationState *s)
migration/migration.c:2153:{
migration/migration.c:2169:void migration_rp_kick(MigrationState *s)
migration/migration.c:2170:{
migration/migration.c:2195:migrate_handle_rp_req_pages(MigrationState *ms, const char* rbname,
migration/migration.c:2197:{
migration/migration.c:2216:static bool migrate_handle_rp_recv_bitmap(MigrationState *s, char *block_name,
migration/migration.c:2218:{
migration/migration.c:2231:static bool migrate_handle_rp_resume_ack(MigrationState *s,
```

- `grep(pattern=^[a-z_A-Z].*\(, version=old, path_glob=target/riscv/kvm/kvm-cpu.c)` →

```
78 matches (showing 60)
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
```

### Turn 4  _(tok 14518+1058, stop=tool_use)_

**Reasoning:** The line at 732 falls inside kvm_riscv_put_regs_timer, which starts at 705, since the next function, get_regs_vector, begins at 742. Next I'm checking migration.c:1965, which is a function.

I'm confirming that migrate_prepare is the enclosing function for line 1965, since it starts at 1923 and the next function, qmp_migrate, begins at 2047. The postcopy recovery logic in that region fits migrate_prepare, and the grep covers all tracked files, so the match list should be complete.



**Says:** I found 7 functions across 5 files. The `migration.c:1965` site is inside `migrate_prepare` (starts at line 1923, next function `qmp_migrate` at 2047), and the `kvm-cpu.c:732` site is inside `kvm_riscv_put_regs_timer` (starts at 705, next function at 742).

- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1378+190, stop=tool_use)_

**Reasoning:** I'll look up the references to this with find_references and then search the codebase with grep.



**Says:** I'll start with the GNU Global reference index, then cross-check with a text search.

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

### Turn 2  _(tok 2202+846, stop=tool_use)_

**Reasoning:** I need to find the enclosing functions around several line numbers: migration.c at lines 1480 and 1965, options.c at 684 and 728, savevm.c at 1709, dirtylimit.c at 454, and kvm-cpu.c at 732. I'll read the code around each one to see which function it sits in.



**Says:** The index and grep agree on 7 call sites (excluding the definition and the header prototype). Next I'll read each site to find its enclosing function.

- `read_file(path=migration/migration.c, version=old, start_line=1455, end_line=1485)` →

```
migration/migration.c lines 1455-1485 of 3838
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
```

- `read_file(path=migration/migration.c, version=old, start_line=1945, end_line=1970)` →

```
migration/migration.c lines 1945-1970 of 3838
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

- `read_file(path=migration/savevm.c, version=old, start_line=1690, end_line=1715)` →

```
migration/savevm.c lines 1690-1715 of 3547
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

### Turn 3  _(tok 6560+380, stop=tool_use)_

**Reasoning:** I need to pin down the enclosing function for line 1480 in migration.c, which is in migrate_fd_cancel, and find the function header above line 1965. I'm also checking which function encloses line 715 in kvm-cpu.c.



**Says:** Most enclosing functions are clear now. Two still need their headers: the `migration.c:1965` site and the `kvm-cpu.c:732` site.

- `read_file(path=migration/migration.c, version=old, start_line=1915, end_line=1935)` →

```
migration/migration.c lines 1915-1935 of 3838
 1915|         error_propagate(errp, error_copy(blockers->data));
 1916|         return true;
 1917|     }
 1918| 
 1919|     return false;
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
```

- `read_file(path=target/riscv/kvm/kvm-cpu.c, version=old, start_line=680, end_line=716)` →

```
target/riscv/kvm/kvm-cpu.c lines 680-716 of 1821
  680|                 return ret;
  681|             }
  682|         }
  683|         return ret;
  684|     }
  685| 
  686|     return ret;
  687| }
  688| 
  689| static void kvm_riscv_get_regs_timer(CPUState *cs)
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
```

### Turn 4  _(tok 7924+862, stop=tool_use)_

**Reasoning:** I'm checking whether any other function sits between 1923 and 1965 in migration.c, since the 1935–1945 stretch is still unclear to me.

I've confirmed the 1945 content sits inside migrate_prepare, so that stretch is settled. The kvm-cpu.c site at 732 falls within kvm_riscv_put_regs_timer, and the grep turned up only the definition and prototype beyond the textual callers. That leaves seven callers, and I'm fairly confident in the list.



**Says:** I've confirmed all seven call sites and their enclosing functions, so I'm submitting the list.

- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3744+230, stop=tool_use)_

**Reasoning:** I'm going to pull up the callers of migration_is_running with a high limit, and run a grep on it as well to cross-check.



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

### Turn 2  _(tok 4680+547, stop=tool_use)_

**Reasoning:** I'm checking the grep results: nine matches in total, covering the definition, the prototype, and seven call sites. Next I want to confirm the enclosing functions for each caller, including whether git grep only searches tracked files.

I'm weighing whether to double-check the enclosing function for line 1480 with a context lookup, but the grep is authoritative for the call sites and the tool supplies the function names, so I'll go ahead and submit.



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3196+75, stop=tool_use)_

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

### Turn 2  _(tok 3648+348, stop=tool_use)_

**Reasoning:** I'm checking which version the tool returned by default, since it came back as "old" even though I didn't pass a version parameter. The server's commit may be pinned so the work state matches HEAD. Since the signature change hasn't landed yet, I want the current call sites, so I'll query with version "work" to be safe.

Next, I'm checking the rest of the request.



**Says:** The result came back labelled as the "old" version, so I'll check the working tree too to make sure nothing is missing.

- `get_callers(name=migration_is_running, limit=200, rev=HEAD)` →

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

### Turn 3  _(tok 4541+281, stop=tool_use)_

**Reasoning:** I'm checking whether the "work" version gives different results, since "old" keeps coming back. The callers lookup doesn't seem to take a version argument, only `rev`, so I'm weighing whether to pass "work" as `rev`. I'll try the neighborhood lookup with the work version to see the caller list instead.



**Says:** The callers tool only takes `rev`, so I'll cross-check against the working tree with the neighborhood tool, which does accept a version.

- `expand_function(name=migration_is_running, levels=1, rev=work)` →

```
{
  "name": "migration_is_running",
  "version": "old",
  "levels": 1,
  "node": {
    "name": "migration_is_running",
    "file": "migration/migration.c",
    "line": 1106,
    "kind": "function",
    "state": "analyzed"
  },
  "callees": [],
  "callers": [
    {
      "name": "migrate_fd_cancel",
      "file": "migration/migration.c",
      "line": 1465,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        1480
      ]
    },
    {
      "name": "migrate_prepare",
      "file": "migration/migration.c",
      "line": 1923,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        1965
      ]
    },
    {
      "name": "migrate_cap_set",
      "file": "migration/options.c",
      "line": 679,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        684
      ]
    },
    {
      "name": "qmp_migrate_set_capabilities",
      "file": "migration/options.c",
      "line": 721,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        728
      ]
    },
    {
      "name": "qemu_savevm_state",
      "file": "migration/savevm.c",
      "line": 1703,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        1709
      ]
    },
    {
      "name": "dirtylimit_is_allowed",
      "file": "system/dirtylimit.c",
      "line": 450,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        454
      ]
    },
    {
      "name": "kvm_riscv_put_regs_timer",
      "file": "target/riscv/kvm/kvm-cpu.c",
      "line": 705,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        732
      ]
    }
  ]
}
```

### Turn 4  _(tok 5535+357, stop=tool_use)_

**Reasoning:** The check looks consistent, and I'm going ahead with submitting it, covering the 7 callers. I'm fairly confident in this, though macros or function pointers might not have shown up in the search.



**Says:** Both lookups agree on the same seven call sites.

- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

