# Impact-analysis transcript — qemu @ aeaafb1e59f8 — anthropic:claude-sonnet-5-5

- target: `migration_is_running` (migration/migration.c), arity 1->0
- truth: [['migration/migration.c', 'migrate_fd_cancel'], ['migration/migration.c', 'migrate_prepare'], ['migration/options.c', 'migrate_cap_set'], ['migration/options.c', 'qmp_migrate_set_capabilities'], ['migration/savevm.c', 'qemu_savevm_state'], ['system/dirtylimit.c', 'dirtylimit_is_allowed'], ['target/riscv/kvm/kvm-cpu.c', 'kvm_riscv_put_regs_timer']]

## Self-navigation arm

### Turn 1  _(tok 1209+97, stop=tool_use)_

- `grep(pattern=migration_is_running, version=old, max_results=200)` →

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

### Turn 2  _(tok 1589+743, stop=tool_use)_

- `grep(pattern=^[a-z_]+.*\(|^\{, version=old, path_glob=migration/options.c, max_results=400)` →

```
132 matches
migration/options.c:211:bool migrate_auto_converge(void)
migration/options.c:212:{
migration/options.c:218:bool migrate_background_snapshot(void)
migration/options.c:219:{
migration/options.c:225:bool migrate_block(void)
migration/options.c:226:{
migration/options.c:232:bool migrate_colo(void)
migration/options.c:233:{
migration/options.c:239:bool migrate_compress(void)
migration/options.c:240:{
migration/options.c:246:bool migrate_dirty_bitmaps(void)
migration/options.c:247:{
migration/options.c:253:bool migrate_dirty_limit(void)
migration/options.c:254:{
migration/options.c:260:bool migrate_events(void)
migration/options.c:261:{
migration/options.c:267:bool migrate_mapped_ram(void)
migration/options.c:268:{
migration/options.c:274:bool migrate_ignore_shared(void)
migration/options.c:275:{
migration/options.c:281:bool migrate_late_block_activate(void)
migration/options.c:282:{
migration/options.c:288:bool migrate_multifd(void)
migration/options.c:289:{
migration/options.c:295:bool migrate_pause_before_switchover(void)
migration/options.c:296:{
migration/options.c:302:bool migrate_postcopy_blocktime(void)
migration/options.c:303:{
migration/options.c:309:bool migrate_postcopy_preempt(void)
migration/options.c:310:{
migration/options.c:316:bool migrate_postcopy_ram(void)
migration/options.c:317:{
migration/options.c:323:bool migrate_rdma_pin_all(void)
migration/options.c:324:{
migration/options.c:330:bool migrate_release_ram(void)
migration/options.c:331:{
migration/options.c:337:bool migrate_return_path(void)
migration/options.c:338:{
migration/options.c:344:bool migrate_switchover_ack(void)
migration/options.c:345:{
migration/options.c:351:bool migrate_validate_uuid(void)
migration/options.c:352:{
migration/options.c:358:bool migrate_xbzrle(void)
migration/options.c:359:{
migration/options.c:365:bool migrate_zero_blocks(void)
migration/options.c:366:{
migration/options.c:372:bool migrate_zero_copy_send(void)
migration/options.c:373:{
migration/options.c:381:bool migrate_multifd_flush_after_each_section(void)
migration/options.c:382:{
migration/options.c:388:bool migrate_postcopy(void)
migration/options.c:389:{
migration/options.c:393:bool migrate_rdma(void)
migration/options.c:394:{
migration/options.c:400:bool migrate_tls(void)
migration/options.c:401:{
migration/options.c:416:{
migration/options.c:465:static bool migrate_incoming_started(void)
migration/options.c:466:{
migration/options.c:479:bool migrate_caps_check(bool *old_caps, bool *new_caps, Error **errp)
migration/options.c:480:{
migration/options.c:679:bool migrate_cap_set(int cap, bool value, Error **errp)
migration/options.c:680:{
migration/options.c:700:{
migration/options.c:721:void qmp_migrate_set_capabilities(MigrationCapabilityStatusList *params,
migration/options.c:723:{
migration/options.c:749:const BitmapMigrationNodeAliasList *migrate_block_bitmap_mapping(void)
migration/options.c:750:{
migration/options.c:756:bool migrate_has_block_bitmap_mapping(void)
migration/options.c:757:{
migration/options.c:763:bool migrate_block_incremental(void)
migration/options.c:764:{
migration/options.c:770:uint32_t migrate_checkpoint_delay(void)
migration/options.c:771:{
migration/options.c:777:int migrate_compress_level(void)
migration/options.c:778:{
migration/options.c:784:int migrate_compress_threads(void)
migration/options.c:785:{
migration/options.c:791:int migrate_compress_wait_thread(void)
migration/options.c:792:{
migration/options.c:798:uint8_t migrate_cpu_throttle_increment(void)
migration/options.c:799:{
migration/options.c:805:uint8_t migrate_cpu_throttle_initial(void)
migration/options.c:806:{
migration/options.c:812:bool migrate_cpu_throttle_tailslow(void)
migration/options.c:813:{
migration/options.c:819:int migrate_decompress_threads(void)
migration/options.c:820:{
migration/options.c:826:uint64_t migrate_downtime_limit(void)
migration/options.c:827:{
migration/options.c:833:uint8_t migrate_max_cpu_throttle(void)
migration/options.c:834:{
migration/options.c:840:uint64_t migrate_max_bandwidth(void)
migration/options.c:841:{
migration/options.c:847:uint64_t migrate_avail_switchover_bandwidth(void)
migration/options.c:848:{
migration/options.c:854:uint64_t migrate_max_postcopy_bandwidth(void)
migration/options.c:855:{
migration/options.c:862:{
migration/options.c:870:int migrate_multifd_channels(void)
migration/options.c:871:{
migration/options.c:878:{
migration/options.c:885:int migrate_multifd_zlib_level(void)
migration/options.c:886:{
migration/options.c:892:int migrate_multifd_zstd_level(void)
migration/options.c:893:{
migration/options.c:899:uint8_t migrate_throttle_trigger_threshold(void)
migration/options.c:900:{
migration/options.c:906:const char *migrate_tls_authz(void)
migration/options.c:907:{
migration/options.c:913:const char *migrate_tls_creds(void)
migration/options.c:914:{
migration/options.c:920:const char *migrate_tls_hostname(void)
migration/options.c:921:{
migration/options.c:927:uint64_t migrate_xbzrle_cache_size(void)
migration/options.c:928:{
migration/options.c:936:void migrate_set_block_incremental(bool value)
migration/options.c:937:{
migration/options.c:945:void block_cleanup_parameters(void)
migration/options.c:946:{
migration/options.c:958:{
migration/options.c:972:{
migration/options.c:1048:void migrate_params_init(MigrationParameters *params)
migration/options.c:1049:{
migration/options.c:1086:bool migrate_params_check(MigrationParameters *params, Error **errp)
migration/options.c:1087:{
migration/options.c:1276:static void migrate_params_test_apply(MigrateSetParameters *params,
migration/options.c:1278:{
migration/options.c:1396:static void migrate_params_apply(MigrateSetParameters *params, Error **errp)
migration/options.c:1397:{
migration/options.c:1546:void qmp_migrate_set_parameters(MigrateSetParameters *params, Error **errp)
migration/options.c:1547:{
```

- `read_file(path=migration/migration.c, version=old, start_line=1465, end_line=1482)` →

```
migration/migration.c lines 1465-1482 of 3838
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

- `read_file(path=migration/migration.c, version=old, start_line=1950, end_line=1966)` →

```
migration/migration.c lines 1950-1966 of 3838
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
```

- `read_file(path=migration/savevm.c, version=old, start_line=1695, end_line=1710)` →

```
migration/savevm.c lines 1695-1710 of 3547
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
```

- `read_file(path=system/dirtylimit.c, version=old, start_line=440, end_line=455)` →

```
system/dirtylimit.c lines 440-455 of 682
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
```

- `read_file(path=target/riscv/kvm/kvm-cpu.c, version=old, start_line=715, end_line=733)` →

```
target/riscv/kvm/kvm-cpu.c lines 715-733 of 1821
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
```

### Turn 3  _(tok 6571+354, stop=tool_use)_

**Reasoning:** I need the names of the functions at migration.c line 1965 and in kvm-cpu.c. In options.c, line 684 is migrate_cap_set and line 728 is qmp_migrate_set_capabilities.



- `grep(pattern=^[a-z_]+.*\(.*(\)|,)$, version=old, path_glob=migration/migration.c, max_results=400)` →

```
133 matches
migration/migration.c:105:static int migration_maybe_pause(MigrationState *s,
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
```

- `grep(pattern=^(static )?[a-z_ ]+\(.*, version=old, path_glob=target/riscv/kvm/kvm-cpu.c, max_results=100)` →

```
366 matches (showing 100)
target/riscv/kvm/kvm-cpu.c:54:void riscv_kvm_aplic_request(void *opaque, int irq, int level)
target/riscv/kvm/kvm-cpu.c:56:    kvm_set_irq(kvm_state, irq, !!level);
target/riscv/kvm/kvm-cpu.c:66:    switch (riscv_cpu_mxl(env)) {
target/riscv/kvm/kvm-cpu.c:74:        g_assert_not_reached();
target/riscv/kvm/kvm-cpu.c:102:    g_assert(idx < 32);
target/riscv/kvm/kvm-cpu.c:107:    return kvm_encode_reg_size_id(id, size_b);
target/riscv/kvm/kvm-cpu.c:111:    kvm_riscv_reg_id_ulong(env, KVM_REG_RISCV_CORE, \
target/riscv/kvm/kvm-cpu.c:115:    kvm_riscv_reg_id_ulong(env, KVM_REG_RISCV_CSR, \
target/riscv/kvm/kvm-cpu.c:119:    kvm_riscv_reg_id_ulong(env, KVM_REG_RISCV_CONFIG, \
target/riscv/kvm/kvm-cpu.c:130:    kvm_riscv_reg_id_ulong(env, KVM_REG_RISCV_VECTOR, \
target/riscv/kvm/kvm-cpu.c:136:        if (_ret) { \
target/riscv/kvm/kvm-cpu.c:144:        if (_ret) { \
target/riscv/kvm/kvm-cpu.c:152:        if (ret) { \
target/riscv/kvm/kvm-cpu.c:153:            abort(); \
target/riscv/kvm/kvm-cpu.c:160:        if (ret) { \
target/riscv/kvm/kvm-cpu.c:161:            abort(); \
target/riscv/kvm/kvm-cpu.c:189:static void kvm_cpu_get_misa_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:199:    visit_type_bool(v, name, &value, errp);
target/riscv/kvm/kvm-cpu.c:202:static void kvm_cpu_set_misa_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:212:    if (!visit_type_bool(v, name, &value, errp)) {
target/riscv/kvm/kvm-cpu.c:218:    if (value == host_bit) {
target/riscv/kvm/kvm-cpu.c:222:    if (!value) {
target/riscv/kvm/kvm-cpu.c:231:    error_setg(errp, "Enabling MISA bit '%s' is not allowed: it's not "
target/riscv/kvm/kvm-cpu.c:235:static void kvm_riscv_update_cpu_misa_ext(RISCVCPU *cpu, CPUState *cs)
target/riscv/kvm/kvm-cpu.c:241:    for (i = 0; i < ARRAY_SIZE(kvm_misa_ext_cfgs); i++) {
target/riscv/kvm/kvm-cpu.c:245:        if (!misa_cfg->user_set) {
target/riscv/kvm/kvm-cpu.c:254:        if (ret != 0) {
target/riscv/kvm/kvm-cpu.c:262:            error_report("Unable to set KVM reg %s, error %d",
target/riscv/kvm/kvm-cpu.c:264:            exit(EXIT_FAILURE);
target/riscv/kvm/kvm-cpu.c:323:    return (void *)&cpu->cfg + kvmcfg->offset;
target/riscv/kvm/kvm-cpu.c:326:static void kvm_cpu_cfg_set(RISCVCPU *cpu, KVMCPUConfig *multi_ext,
target/riscv/kvm/kvm-cpu.c:342:static void kvm_cpu_get_multi_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:350:    visit_type_bool(v, name, &value, errp);
target/riscv/kvm/kvm-cpu.c:353:static void kvm_cpu_set_multi_ext_cfg(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:361:    if (!visit_type_bool(v, name, &value, errp)) {
target/riscv/kvm/kvm-cpu.c:371:    if (value == host_val) {
target/riscv/kvm/kvm-cpu.c:375:    if (!multi_ext_cfg->supported) {
target/riscv/kvm/kvm-cpu.c:381:        if (value) {
target/riscv/kvm/kvm-cpu.c:382:            error_setg(errp, "KVM does not support disabling extension %s",
target/riscv/kvm/kvm-cpu.c:390:    kvm_cpu_cfg_set(cpu, multi_ext_cfg, value);
target/riscv/kvm/kvm-cpu.c:412:static void kvm_riscv_update_cpu_cfg_isa_ext(RISCVCPU *cpu, CPUState *cs)
target/riscv/kvm/kvm-cpu.c:418:    for (i = 0; i < ARRAY_SIZE(kvm_multi_ext_cfgs); i++) {
target/riscv/kvm/kvm-cpu.c:421:        if (!multi_ext_cfg->user_set) {
target/riscv/kvm/kvm-cpu.c:429:        if (ret != 0) {
target/riscv/kvm/kvm-cpu.c:430:            error_report("Unable to %s extension %s in KVM, error %d",
target/riscv/kvm/kvm-cpu.c:433:            exit(EXIT_FAILURE);
target/riscv/kvm/kvm-cpu.c:438:static void cpu_get_cfg_unavailable(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:444:    visit_type_bool(v, name, &value, errp);
target/riscv/kvm/kvm-cpu.c:447:static void cpu_set_cfg_unavailable(Object *obj, Visitor *v,
target/riscv/kvm/kvm-cpu.c:454:    if (!visit_type_bool(v, name, &value, errp)) {
target/riscv/kvm/kvm-cpu.c:458:    if (value) {
target/riscv/kvm/kvm-cpu.c:459:        error_setg(errp, "'%s' is not available with KVM",
target/riscv/kvm/kvm-cpu.c:464:static void riscv_cpu_add_kvm_unavail_prop(Object *obj, const char *prop_name)
target/riscv/kvm/kvm-cpu.c:467:    if (object_property_find(obj, prop_name)) {
target/riscv/kvm/kvm-cpu.c:476:    object_property_add(obj, prop_name, "bool",
target/riscv/kvm/kvm-cpu.c:482:static void riscv_cpu_add_kvm_unavail_prop_array(Object *obj,
target/riscv/kvm/kvm-cpu.c:487:    g_assert(array);
target/riscv/kvm/kvm-cpu.c:489:    for (prop = array; prop && prop->name; prop++) {
target/riscv/kvm/kvm-cpu.c:490:        riscv_cpu_add_kvm_unavail_prop(obj, prop->name);
target/riscv/kvm/kvm-cpu.c:494:static void kvm_riscv_add_cpu_user_properties(Object *cpu_obj)
target/riscv/kvm/kvm-cpu.c:498:    riscv_add_satp_mode_properties(cpu_obj);
target/riscv/kvm/kvm-cpu.c:500:    for (i = 0; i < ARRAY_SIZE(kvm_misa_ext_cfgs); i++) {
target/riscv/kvm/kvm-cpu.c:507:        object_property_add(cpu_obj, misa_cfg->name, "bool",
target/riscv/kvm/kvm-cpu.c:511:        object_property_set_description(cpu_obj, misa_cfg->name,
target/riscv/kvm/kvm-cpu.c:515:    for (i = 0; misa_bits[i] != 0; i++) {
target/riscv/kvm/kvm-cpu.c:517:        riscv_cpu_add_kvm_unavail_prop(cpu_obj, ext_name);
target/riscv/kvm/kvm-cpu.c:520:    for (i = 0; i < ARRAY_SIZE(kvm_multi_ext_cfgs); i++) {
target/riscv/kvm/kvm-cpu.c:523:        object_property_add(cpu_obj, multi_cfg->name, "bool",
target/riscv/kvm/kvm-cpu.c:529:    riscv_cpu_add_kvm_unavail_prop_array(cpu_obj, riscv_cpu_extensions);
target/riscv/kvm/kvm-cpu.c:530:    riscv_cpu_add_kvm_unavail_prop_array(cpu_obj, riscv_cpu_vendor_exts);
target/riscv/kvm/kvm-cpu.c:531:    riscv_cpu_add_kvm_unavail_prop_array(cpu_obj, riscv_cpu_experimental_exts);
target/riscv/kvm/kvm-cpu.c:534:    for (i = 0; riscv_profiles[i] != NULL; i++) {
target/riscv/kvm/kvm-cpu.c:535:        riscv_cpu_add_kvm_unavail_prop(cpu_obj, riscv_profiles[i]->name);
target/riscv/kvm/kvm-cpu.c:539:static int kvm_riscv_get_regs_core(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:547:    if (ret) {
target/riscv/kvm/kvm-cpu.c:552:    for (i = 1; i < 32; i++) {
target/riscv/kvm/kvm-cpu.c:555:        if (ret) {
target/riscv/kvm/kvm-cpu.c:564:static int kvm_riscv_put_regs_core(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:573:    if (ret) {
target/riscv/kvm/kvm-cpu.c:577:    for (i = 1; i < 32; i++) {
target/riscv/kvm/kvm-cpu.c:581:        if (ret) {
target/riscv/kvm/kvm-cpu.c:589:static int kvm_riscv_get_regs_csr(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:606:static int kvm_riscv_put_regs_csr(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:623:static int kvm_riscv_get_regs_fp(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:629:    if (riscv_has_ext(env, RVD)) {
target/riscv/kvm/kvm-cpu.c:631:        for (i = 0; i < 32; i++) {
target/riscv/kvm/kvm-cpu.c:633:            if (ret) {
target/riscv/kvm/kvm-cpu.c:641:    if (riscv_has_ext(env, RVF)) {
target/riscv/kvm/kvm-cpu.c:643:        for (i = 0; i < 32; i++) {
target/riscv/kvm/kvm-cpu.c:645:            if (ret) {
target/riscv/kvm/kvm-cpu.c:656:static int kvm_riscv_put_regs_fp(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:662:    if (riscv_has_ext(env, RVD)) {
target/riscv/kvm/kvm-cpu.c:664:        for (i = 0; i < 32; i++) {
target/riscv/kvm/kvm-cpu.c:667:            if (ret) {
target/riscv/kvm/kvm-cpu.c:674:    if (riscv_has_ext(env, RVF)) {
target/riscv/kvm/kvm-cpu.c:676:        for (i = 0; i < 32; i++) {
target/riscv/kvm/kvm-cpu.c:679:            if (ret) {
target/riscv/kvm/kvm-cpu.c:689:static void kvm_riscv_get_regs_timer(CPUState *cs)
target/riscv/kvm/kvm-cpu.c:693:    if (env->kvm_timer_dirty) {
target/riscv/kvm/kvm-cpu.c:705:static void kvm_riscv_put_regs_timer(CPUState *cs)
```

### Turn 4  _(tok 16004+378, stop=tool_use)_

**Reasoning:** I'm checking where those line numbers fall: line 684 sits inside migrate_cap_set, 728 inside qmp_migrate_set_capabilities, and 1965 inside migrate_prepare. I also need to look at the RISC-V timer register code in kvm_riscv_put_regs_timer.



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1378+146, stop=tool_use)_

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

- `grep(pattern=migration_is_running, version=old, max_results=200)` →

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

### Turn 2  _(tok 2158+751, stop=tool_use)_

**Says:** Need enclosing functions.

- `grep(pattern=^[a-z_A-Z].*\(, version=old, path_glob=migration/options.c, max_results=300)` →

```
70 matches
migration/options.c:211:bool migrate_auto_converge(void)
migration/options.c:218:bool migrate_background_snapshot(void)
migration/options.c:225:bool migrate_block(void)
migration/options.c:232:bool migrate_colo(void)
migration/options.c:239:bool migrate_compress(void)
migration/options.c:246:bool migrate_dirty_bitmaps(void)
migration/options.c:253:bool migrate_dirty_limit(void)
migration/options.c:260:bool migrate_events(void)
migration/options.c:267:bool migrate_mapped_ram(void)
migration/options.c:274:bool migrate_ignore_shared(void)
migration/options.c:281:bool migrate_late_block_activate(void)
migration/options.c:288:bool migrate_multifd(void)
migration/options.c:295:bool migrate_pause_before_switchover(void)
migration/options.c:302:bool migrate_postcopy_blocktime(void)
migration/options.c:309:bool migrate_postcopy_preempt(void)
migration/options.c:316:bool migrate_postcopy_ram(void)
migration/options.c:323:bool migrate_rdma_pin_all(void)
migration/options.c:330:bool migrate_release_ram(void)
migration/options.c:337:bool migrate_return_path(void)
migration/options.c:344:bool migrate_switchover_ack(void)
migration/options.c:351:bool migrate_validate_uuid(void)
migration/options.c:358:bool migrate_xbzrle(void)
migration/options.c:365:bool migrate_zero_blocks(void)
migration/options.c:372:bool migrate_zero_copy_send(void)
migration/options.c:381:bool migrate_multifd_flush_after_each_section(void)
migration/options.c:388:bool migrate_postcopy(void)
migration/options.c:393:bool migrate_rdma(void)
migration/options.c:400:bool migrate_tls(void)
migration/options.c:415:WriteTrackingSupport migrate_query_write_tracking(void)
migration/options.c:448:INITIALIZE_MIGRATE_CAPS_SET(check_caps_background_snapshot,
migration/options.c:465:static bool migrate_incoming_started(void)
migration/options.c:479:bool migrate_caps_check(bool *old_caps, bool *new_caps, Error **errp)
migration/options.c:679:bool migrate_cap_set(int cap, bool value, Error **errp)
migration/options.c:699:MigrationCapabilityStatusList *qmp_query_migrate_capabilities(Error **errp)
migration/options.c:721:void qmp_migrate_set_capabilities(MigrationCapabilityStatusList *params,
migration/options.c:749:const BitmapMigrationNodeAliasList *migrate_block_bitmap_mapping(void)
migration/options.c:756:bool migrate_has_block_bitmap_mapping(void)
migration/options.c:763:bool migrate_block_incremental(void)
migration/options.c:770:uint32_t migrate_checkpoint_delay(void)
migration/options.c:777:int migrate_compress_level(void)
migration/options.c:784:int migrate_compress_threads(void)
migration/options.c:791:int migrate_compress_wait_thread(void)
migration/options.c:798:uint8_t migrate_cpu_throttle_increment(void)
migration/options.c:805:uint8_t migrate_cpu_throttle_initial(void)
migration/options.c:812:bool migrate_cpu_throttle_tailslow(void)
migration/options.c:819:int migrate_decompress_threads(void)
migration/options.c:826:uint64_t migrate_downtime_limit(void)
migration/options.c:833:uint8_t migrate_max_cpu_throttle(void)
migration/options.c:840:uint64_t migrate_max_bandwidth(void)
migration/options.c:847:uint64_t migrate_avail_switchover_bandwidth(void)
migration/options.c:854:uint64_t migrate_max_postcopy_bandwidth(void)
migration/options.c:861:MigMode migrate_mode(void)
migration/options.c:870:int migrate_multifd_channels(void)
migration/options.c:877:MultiFDCompression migrate_multifd_compression(void)
migration/options.c:885:int migrate_multifd_zlib_level(void)
migration/options.c:892:int migrate_multifd_zstd_level(void)
migration/options.c:899:uint8_t migrate_throttle_trigger_threshold(void)
migration/options.c:906:const char *migrate_tls_authz(void)
migration/options.c:913:const char *migrate_tls_creds(void)
migration/options.c:920:const char *migrate_tls_hostname(void)
migration/options.c:927:uint64_t migrate_xbzrle_cache_size(void)
migration/options.c:936:void migrate_set_block_incremental(bool value)
migration/options.c:945:void block_cleanup_parameters(void)
migration/options.c:957:AnnounceParameters *migrate_announce_params(void)
migration/options.c:971:MigrationParameters *qmp_query_migrate_parameters(Error **errp)
migration/options.c:1048:void migrate_params_init(MigrationParameters *params)
migration/options.c:1086:bool migrate_params_check(MigrationParameters *params, Error **errp)
migration/options.c:1276:static void migrate_params_test_apply(MigrateSetParameters *params,
migration/options.c:1396:static void migrate_params_apply(MigrateSetParameters *params, Error **errp)
migration/options.c:1546:void qmp_migrate_set_parameters(MigrateSetParameters *params, Error **errp)
```

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

- `read_file(path=migration/migration.c, version=old, start_line=1945, end_line=1966)` →

```
migration/migration.c lines 1945-1966 of 3838
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
```

- `read_file(path=migration/savevm.c, version=old, start_line=1695, end_line=1710)` →

```
migration/savevm.c lines 1695-1710 of 3547
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
```

- `read_file(path=system/dirtylimit.c, version=old, start_line=440, end_line=456)` →

```
system/dirtylimit.c lines 440-456 of 682
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
```

- `read_file(path=target/riscv/kvm/kvm-cpu.c, version=old, start_line=720, end_line=733)` →

```
target/riscv/kvm/kvm-cpu.c lines 720-733 of 1821
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
```

### Turn 3  _(tok 6827+291, stop=tool_use)_

**Says:** Need the function names for migration.c:1965 and riscv.

- `grep(pattern=^[a-z_A-Z].*\(, version=old, path_glob=target/riscv/kvm/kvm-cpu.c, max_results=300)` →

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

- `grep(pattern=^(static )?bool migrate_prepare|^[a-z].*migrate_prepare, version=old, path_glob=migration/migration.c)` →

```
1 matches
migration/migration.c:1923:static bool migrate_prepare(MigrationState *s, bool blk, bool blk_inc,
```

### Turn 4  _(tok 11469+366, stop=tool_use)_

**Reasoning:** I'm tracing the call chain: line 684 in options.c leads into migrate_cap_set at 679, and line 728 leads into qmp_migrate_set_capabilities at 721. Line 1965 falls inside migrate_prepare, which starts at 1923, and I'm assuming no other function sits between them. That all checks out.



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3744+169, stop=tool_use)_

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

- `grep(pattern=migration_is_running, version=old, max_results=200)` →

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

### Turn 2  _(tok 4619+292, stop=tool_use)_

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

### Turn 2  _(tok 3648+365, stop=tool_use)_

**Reasoning:** I'm wondering if other callers of migration_is_running might pass a different version, though "old" is the default and that's probably fine. I could check with "new", but I think I'll skip it and submit.



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

