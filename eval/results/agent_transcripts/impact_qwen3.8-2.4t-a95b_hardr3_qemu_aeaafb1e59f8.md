# Impact-analysis transcript — qemu @ aeaafb1e59f8 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `migration_is_running` (migration/migration.c), arity 1->0
- truth: [['migration/migration.c', 'migrate_fd_cancel'], ['migration/migration.c', 'migrate_prepare'], ['migration/options.c', 'migrate_cap_set'], ['migration/options.c', 'qmp_migrate_set_capabilities'], ['migration/savevm.c', 'qemu_savevm_state'], ['system/dirtylimit.c', 'dirtylimit_is_allowed'], ['target/riscv/kvm/kvm-cpu.c', 'kvm_riscv_put_regs_timer']]

## Self-navigation arm

### Turn 1  _(tok 901+77, stop=tool_use)_

**Reasoning:** To find the call sites of `migration_is_running`, let's try searching for all occurrences of it.

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

### Turn 2  _(tok 1196+294, stop=tool_use)_

**Reasoning:** Now, I need to identify the enclosing function at each call site. Excluding the definition (migration/migration.c:1106) and the prototype (migration/migration.h:482), the call sites are as follows:

1. migration/migration.c:1480
2. migration/migration.c:1965
3. migration/options.c:684
4. migration/options.c:728
5. migration/savevm.c:1709
6. system/dirtylimit.c:454
7. target/riscv/kvm/kvm-cpu.c:732

To identify the enclosing function, let me try reading around each of these lines.

- `read_file(path=migration/migration.c, start_line=1400, end_line=1490, version=old)` →

```
migration/migration.c lines 1400-1490 of 3838
 1400|         qemu_mutex_unlock(&s->qemu_file_lock);
 1401|         /*
 1402|          * Close the file handle without the lock to make sure the
 1403|          * critical section won't block for long.
 1404|          */
 1405|         migration_ioc_unregister_yank_from_file(tmp);
 1406|         qemu_fclose(tmp);
 1407|     }
 1408| 
 1409|     assert(!migration_is_active());
 1410| 
 1411|     if (s->state == MIGRATION_STATUS_CANCELLING) {
 1412|         migrate_set_state(&s->state, MIGRATION_STATUS_CANCELLING,
 1413|                           MIGRATION_STATUS_CANCELLED);
 1414|     }
 1415| 
 1416|     if (s->error) {
 1417|         /* It is used on info migrate.  We can't free it */
 1418|         error_report_err(error_copy(s->error));
 1419|     }
 1420|     type = migration_has_failed(s) ? MIG_EVENT_PRECOPY_FAILED :
 1421|                                      MIG_EVENT_PRECOPY_DONE;
 1422|     migration_call_notifiers(s, type, NULL);
 1423|     block_cleanup_parameters();
 1424|     yank_unregister_instance(MIGRATION_YANK_INSTANCE);
 1425| }
 1426| 
 1427| static void migrate_fd_cleanup_bh(void *opaque)
 1428| {
 1429|     migrate_fd_cleanup(opaque);
 1430| }
 1431| 
 1432| void migrate_set_error(MigrationState *s, const Error *error)
 1433| {
 1434|     QEMU_LOCK_GUARD(&s->error_mutex);
 1435|     if (!s->error) {
 1436|         s->error = error_copy(error);
 1437|     }
 1438| }
 1439| 
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

### Turn 3  _(tok 3564+83, stop=tool_use)_

**Reasoning:** migration.c:1965 is inside `migrate_prepare`.

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

### Turn 4  _(tok 4879+101, stop=tool_use)_

**Reasoning:** options.c:684 → `migrate_cap_set`
options.c:728 → `qmp_migrate_set_capabilities`

- `read_file(path=migration/savevm.c, start_line=1670, end_line=1715, version=old)` →

```
migration/savevm.c lines 1670-1715 of 3547
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

### Turn 5  _(tok 5647+87, stop=tool_use)_

**Reasoning:** savevm.c:1709 → `qemu_savevm_state`


- `read_file(path=system/dirtylimit.c, start_line=420, end_line=460, version=old)` →

```
system/dirtylimit.c lines 420-460 of 682
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
```

### Turn 6  _(tok 6257+91, stop=tool_use)_

**Reasoning:** dirtylimit.c:454 → `dirtylimit_is_allowed`

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

_(budget of 20,000 tokens exhausted — forcing submission)_

