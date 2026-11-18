# Impact-analysis transcript — qemu @ aeaafb1e59f8 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `migration_is_running` (migration/migration.c), arity 1->0
- truth: [['migration/migration.c', 'migrate_fd_cancel'], ['migration/migration.c', 'migrate_prepare'], ['migration/options.c', 'migrate_cap_set'], ['migration/options.c', 'qmp_migrate_set_capabilities'], ['migration/savevm.c', 'qemu_savevm_state'], ['system/dirtylimit.c', 'dirtylimit_is_allowed'], ['target/riscv/kvm/kvm-cpu.c', 'kvm_riscv_put_regs_timer']]

## Self-navigation arm

### Turn 1  _(tok 901+69, stop=tool_use)_

**Reasoning:** I'm searching through the repo for references to migration_is_running.

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

### Turn 2  _(tok 1188+496, stop=tool_use)_

**Reasoning:** There are 9 matches in total. The ones to exclude are the definition at migration/migration.c:1106 and the prototype at migration/migration.h:482. So that leaves 7 call sites. For each one, I need to identify the enclosing function. Let me read the surrounding context of each line to find the function name.

- `read_file(path=migration/migration.c, start_line=1440, end_line=1485, version=old)` →

```
migration/migration.c lines 1440-1485 of 3838
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
```

- `read_file(path=migration/migration.c, start_line=1930, end_line=1970, version=old)` →

```
migration/migration.c lines 1930-1970 of 3838
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

- `read_file(path=migration/options.c, start_line=660, end_line=735, version=old)` →

```
migration/options.c lines 660-735 of 1579
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

- `read_file(path=migration/savevm.c, start_line=1680, end_line=1715, version=old)` →

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

- `read_file(path=system/dirtylimit.c, start_line=425, end_line=460, version=old)` →

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

- `read_file(path=target/riscv/kvm/kvm-cpu.c, start_line=700, end_line=740, version=old)` →

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

### Turn 3  _(tok 5712+135, stop=tool_use)_

**Reasoning:** Let's try to identify the function enclosing line 1965 of migration/migration.c. That's inside the code that handles `resume` — this is probably inside `qmp_migrate` or a function like `migrate_prepare`. Let me try searching backwards from line 1965.


- `read_file(path=migration/migration.c, start_line=1900, end_line=1932, version=old)` →

```
migration/migration.c lines 1900-1932 of 3838
 1900|     }
 1901| 
 1902|     error_setg(errp, "migrate-pause is currently only supported "
 1903|                "during postcopy-active or postcopy-recover state");
 1904| }
 1905| 
 1906| bool migration_is_blocked(Error **errp)
 1907| {
 1908|     GSList *blockers = migration_blockers[migrate_mode()];
 1909| 
 1910|     if (qemu_savevm_state_blocked(errp)) {
 1911|         return true;
 1912|     }
 1913| 
 1914|     if (blockers) {
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
```

### Turn 4  _(tok 6314+627, stop=tool_use)_

**Reasoning:** Call site at migration/migration.c:1965 is inside `migrate_prepare`.

So the complete list of callers is as follows:
1. `migrate_fd_cancel` — migration/migration.c (line 1480)
2. `migrate_prepare` — migration/migration.c (line 1965)
3. `migrate_cap_set` — migration/options.c (line 684)
4. `qmp_migrate_set_capabilities` — migration/options.c (line 728)
5. `qemu_savevm_state` — migration/savevm.c (line 1709)
6. `dirtylimit_is_allowed` — system/dirtylimit.c (line 454)
7. `kvm_riscv_put_regs_timer` — target/riscv/kvm/kvm-cpu.c (line 732)

There are no other matches (grep shows all 9 matches: 1 definition, 1 prototype, 7 call sites). All verified. Submitting.

**Says:** All call sites verified. The grep found 9 matches total: 1 definition (migration/migration.c:1106), 1 prototype (migration/migration.h:482), and 7 call sites. For each call site I read the surrounding code to identify the enclosing function:

| Call site | Enclosing function |
|---|---|
| migration/migration.c:1480 | `migrate_fd_cancel` |
| migration/migration.c:1965 | `migrate_prepare` |
| migration/options.c:684 | `migrate_cap_set` |
| migration/options.c:728 | `qmp_migrate_set_capabilities` |
| migration/savevm.c:1709 | `qemu_savevm_state` |
| system/dirtylimit.c:454 | `dirtylimit_is_allowed` |
| target/riscv/kvm/kvm-cpu.c:732 | `kvm_riscv_put_regs_timer` |



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1030+80, stop=tool_use)_

**Reasoning:** Let me search for references to `migration_is_running`.

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

### Turn 2  _(tok 1550+510, stop=tool_use)_

**Reasoning:** grep found 9 matches (1 definition + 1 prototype + 7 call sites), and find_references found 7 call sites + prototype (definition is excluded). Next, I need to identify the enclosing function for each call site. Let me read the surrounding context of each call site.

**Says:** Both searches agree: 7 call sites (plus the definition and prototype). Now I need to find the enclosing function for each call site.



- `read_file(path=migration/migration.c, start_line=1440, end_line=1485, version=old)` →

```
migration/migration.c lines 1440-1485 of 3838
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
```

- `read_file(path=migration/migration.c, start_line=1930, end_line=1970, version=old)` →

```
migration/migration.c lines 1930-1970 of 3838
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

- `read_file(path=migration/options.c, start_line=660, end_line=735, version=old)` →

```
migration/options.c lines 660-735 of 1579
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

- `read_file(path=migration/savevm.c, start_line=1690, end_line=1712, version=old)` →

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

- `read_file(path=system/dirtylimit.c, start_line=430, end_line=460, version=old)` →

```
system/dirtylimit.c lines 430-460 of 682
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

- `read_file(path=target/riscv/kvm/kvm-cpu.c, start_line=700, end_line=740, version=old)` →

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

### Turn 3  _(tok 5879+130, stop=tool_use)_

**Reasoning:** Alright, let me verify the function enclosing line 1965 of migration/migration.c — need to confirm the function name. Reading backwards from line 1965.

**Says:** Now I need to identify the function enclosing line 1965 in migration/migration.c.



- `read_file(path=migration/migration.c, start_line=1895, end_line=1935, version=old)` →

```
migration/migration.c lines 1895-1935 of 3838
 1895|         ret = qemu_file_shutdown(mis->from_src_file);
 1896|         if (ret) {
 1897|             error_setg(errp, "Failed to pause destination migration");
 1898|         }
 1899|         return;
 1900|     }
 1901| 
 1902|     error_setg(errp, "migrate-pause is currently only supported "
 1903|                "during postcopy-active or postcopy-recover state");
 1904| }
 1905| 
 1906| bool migration_is_blocked(Error **errp)
 1907| {
 1908|     GSList *blockers = migration_blockers[migrate_mode()];
 1909| 
 1910|     if (qemu_savevm_state_blocked(errp)) {
 1911|         return true;
 1912|     }
 1913| 
 1914|     if (blockers) {
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

### Turn 4  _(tok 6584+616, stop=tool_use)_

**Reasoning:** All 7 call sites and their corresponding enclosing functions have been confirmed:

1. migration/migration.c:1480 → `migrate_fd_cancel`
2. migration/migration.c:1965 → `migrate_prepare`
3. migration/options.c:684 → `migrate_cap_set`
4. migration/options.c:728 → `qmp_migrate_set_capabilities`
5. migration/savevm.c:1709 → `qemu_savevm_state`
6. system/dirtylimit.c:454 → `dirtylimit_is_allowed`
7. target/riscv/kvm/kvm-cpu.c:732 → `kvm_riscv_put_regs_timer`

Submitting.

**Says:** I've located all 7 call sites of `migration_is_running` (excluding the definition at migration.c:1106 and the prototype at migration.h:482) and confirmed the enclosing function for each:

1. **migration/migration.c:1480** — inside `migrate_fd_cancel` (starts at line 1465)
2. **migration/migration.c:1965** — inside `migrate_prepare` (starts at line 1923)
3. **migration/options.c:684** — inside `migrate_cap_set` (starts at line 679)
4. **migration/options.c:728** — inside `qmp_migrate_set_capabilities` (starts at line 721)
5. **migration/savevm.c:1709** — inside `qemu_savevm_state` (starts at line 1703)
6. **system/dirtylimit.c:454** — inside `dirtylimit_is_allowed` (starts at line 450)
7. **target/riscv/kvm/kvm-cpu.c:732** — inside `kvm_riscv_put_regs_timer` (starts at line 705)



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 2730+125, stop=tool_use)_

**Reasoning:** I need to investigate this further. Let me check the details.

Let me find all the call sites of `migration_is_running`.


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

### Turn 2  _(tok 3395+412, stop=tool_use)_

**Reasoning:** The grep results confirm there are 7 call sites matching the semantic tool's caller list. Excluding the definition (migration.c:1106) and the prototype (migration.h:482), the call sites are as follows:

1. migrate_fd_cancel — migration/migration.c:1480
2. migrate_prepare — migration/migration.c:1965
3. migrate_cap_set — migration/options.c:684
4. qmp_migrate_set_capabilities — migration/options.c:728
5. qemu_savevm_state — migration/savevm.c:1709
6. dirtylimit_is_allowed — system/dirtylimit.c:454
7. kvm_riscv_put_regs_timer — target/riscv/kvm/kvm-cpu.c:732

The grep and the semantic tool match completely. Done.

**Says:** The grep results (7 call sites) match the semantic caller list exactly, excluding the definition itself (`migration/migration.c:1106`) and the header prototype (`migration/migration.h:482`).



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 2307+50, stop=tool_use)_

**Reasoning:** Let's get the callers.

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

### Turn 2  _(tok 2678+100, stop=tool_use)_

**Reasoning:** Verify completeness — maybe there are callers that gtags missed, like via macros or in other files. Let me resolve and recheck, and expand the callers. Or maybe just accept it as is. To reconfirm the list is complete, let me run expand_function with levels=1.


- `expand_function(name=migration_is_running, levels=1)` →

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

### Turn 3  _(tok 3415+339, stop=tool_use)_

**Reasoning:** The two sources match. Sending 7 callers.


**Says:** Both the callers index and the on-demand graph agree on the same complete set of 7 call sites:

| Caller function | File |
|---|---|
| `migrate_fd_cancel` | migration/migration.c |
| `migrate_prepare` | migration/migration.c |
| `migrate_cap_set` | migration/options.c |
| `qmp_migrate_set_capabilities` | migration/options.c |
| `qemu_savevm_state` | migration/savevm.c |
| `dirtylimit_is_allowed` | system/dirtylimit.c |
| `kvm_riscv_put_regs_timer` | target/riscv/kvm/kvm-cpu.c |



- **submit_callers** → `{"callers": [{"function": "migrate_fd_cancel", "file": "migration/migration.c"}, {"function": "migrate_prepare", "file": "migration/migration.c"}, {"function": "migrate_cap_set", "file": "migration/options.c"}, {"function": "qmp_migrate_set_capabilities", "file": "migration/options.c"}, {"function": "qemu_savevm_state", "file": "migration/savevm.c"}, {"function": "dirtylimit_is_allowed", "file": "system/dirtylimit.c"}, {"function": "kvm_riscv_put_regs_timer", "file": "target/riscv/kvm/kvm-cpu.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 7, "n_truth": 7, "tp": 7, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

