# Impact-analysis transcript — qemu @ 5202861b20d7 — anthropic:claude-sonnet-5-5

- target: `semihosting_enabled` (include/semihosting/semihost.h), arity 0->1
- truth: [['softmmu/vl.c', 'qemu_apply_machine_options'], ['target/arm/translate-a64.c', 'disas_exc'], ['target/arm/translate.c', 'gen_hlt'], ['target/arm/translate.c', 'trans_BKPT'], ['target/arm/translate.c', 'trans_SVC'], ['target/m68k/op_helper.c', 'cf_interrupt_all'], ['target/mips/tcg/translate.c', 'is_uhi'], ['target/nios2/translate.c', 'gen_break'], ['target/xtensa/translate.c', 'test_exceptions_simcall'], ['target/xtensa/translate.c', 'translate_simcall']]

## Self-navigation arm

### Turn 1  _(tok 1218+99, stop=tool_use)_

- `grep(pattern=semihosting_enabled, version=old, max_results=200)` →

```
15 matches
include/semihosting/semihost.h:30:static inline bool semihosting_enabled(void)
include/semihosting/semihost.h:55:bool semihosting_enabled(void);
semihosting/config.c:62:bool semihosting_enabled(void)
softmmu/vl.c:1825:    if (semihosting_enabled() && !semihosting_get_argc()) {
stubs/semihost.c:26:bool semihosting_enabled(void)
target/arm/translate-a64.c:2222:        if (semihosting_enabled() && imm16 == 0xf000) {
target/arm/translate.c:1172:    if (semihosting_enabled() &&
target/arm/translate.c:6559:        semihosting_enabled() &&
target/arm/translate.c:8767:    if (!arm_dc_feature(s, ARM_FEATURE_M) && semihosting_enabled() &&
target/m68k/op_helper.c:206:            if (semihosting_enabled()
target/mips/tcg/translate.c:12090:    return semihosting_enabled() && sdbbp_code == 1;
target/nios2/translate.c:821:    if (semihosting_enabled() && instr.imm5 == 1) {
target/xtensa/translate.c:2369:    bool ill = dc->config->hw_version <= 250002 && !semihosting_enabled();
target/xtensa/translate.c:2371:    if (ill || !semihosting_enabled()) {
target/xtensa/translate.c:2381:    if (semihosting_enabled()) {
```

### Turn 2  _(tok 1847+666, stop=tool_use)_

**Reasoning:** I need to find the functions that enclose this code. I'm also wondering whether it gets used elsewhere through macros, so I'll go through each use site one by one.



- `grep(pattern=^[a-z].*\(|^\{, version=old, path_glob=target/xtensa/translate.c, max_results=400)` →

```
530 matches (showing 200)
target/xtensa/translate.c:99:void xtensa_collect_sr_names(const XtensaConfig *config)
target/xtensa/translate.c:100:{
target/xtensa/translate.c:131:void xtensa_translate_init(void)
target/xtensa/translate.c:132:{
target/xtensa/translate.c:237:void **xtensa_get_regfile_by_name(const char *name, int entries, int bits)
target/xtensa/translate.c:238:{
target/xtensa/translate.c:278:static inline bool option_enabled(DisasContext *dc, int opt)
target/xtensa/translate.c:279:{
target/xtensa/translate.c:283:static void init_sar_tracker(DisasContext *dc)
target/xtensa/translate.c:284:{
target/xtensa/translate.c:290:static void reset_sar_tracker(DisasContext *dc)
target/xtensa/translate.c:291:{
target/xtensa/translate.c:297:static void gen_right_shift_sar(DisasContext *dc, TCGv_i32 sa)
target/xtensa/translate.c:298:{
target/xtensa/translate.c:307:static void gen_left_shift_sar(DisasContext *dc, TCGv_i32 sa)
target/xtensa/translate.c:308:{
target/xtensa/translate.c:319:static void gen_exception(DisasContext *dc, int excp)
target/xtensa/translate.c:320:{
target/xtensa/translate.c:324:static void gen_exception_cause(DisasContext *dc, uint32_t cause)
target/xtensa/translate.c:325:{
target/xtensa/translate.c:334:static void gen_debug_exception(DisasContext *dc, uint32_t cause)
target/xtensa/translate.c:335:{
target/xtensa/translate.c:343:static bool gen_check_privilege(DisasContext *dc)
target/xtensa/translate.c:344:{
target/xtensa/translate.c:355:static bool gen_check_cpenable(DisasContext *dc, uint32_t cp_mask)
target/xtensa/translate.c:356:{
target/xtensa/translate.c:367:static int gen_postprocess(DisasContext *dc, int slot);
target/xtensa/translate.c:369:static void gen_jump_slot(DisasContext *dc, TCGv dest, int slot)
target/xtensa/translate.c:370:{
target/xtensa/translate.c:387:static void gen_jump(DisasContext *dc, TCGv dest)
target/xtensa/translate.c:388:{
target/xtensa/translate.c:392:static int adjust_jump_slot(DisasContext *dc, uint32_t dest, int slot)
target/xtensa/translate.c:393:{
target/xtensa/translate.c:397:static void gen_jumpi(DisasContext *dc, uint32_t dest, int slot)
target/xtensa/translate.c:398:{
target/xtensa/translate.c:403:static void gen_callw_slot(DisasContext *dc, int callinc, TCGv_i32 dest,
target/xtensa/translate.c:405:{
target/xtensa/translate.c:413:static bool gen_check_loop_end(DisasContext *dc, int slot)
target/xtensa/translate.c:414:{
target/xtensa/translate.c:432:static void gen_jumpi_check_loop_end(DisasContext *dc, int slot)
target/xtensa/translate.c:433:{
target/xtensa/translate.c:439:static void gen_brcond(DisasContext *dc, TCGCond cond,
target/xtensa/translate.c:441:{
target/xtensa/translate.c:450:static void gen_brcondi(DisasContext *dc, TCGCond cond,
target/xtensa/translate.c:452:{
target/xtensa/translate.c:456:static uint32_t test_exceptions_sr(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:458:{
target/xtensa/translate.c:462:static uint32_t test_exceptions_ccompare(DisasContext *dc,
target/xtensa/translate.c:465:{
target/xtensa/translate.c:474:static uint32_t test_exceptions_dbreak(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:476:{
target/xtensa/translate.c:491:static uint32_t test_exceptions_ibreak(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:493:{
target/xtensa/translate.c:502:static uint32_t test_exceptions_hpi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:504:{
target/xtensa/translate.c:522:static MemOp gen_load_store_alignment(DisasContext *dc, MemOp mop,
target/xtensa/translate.c:524:{
target/xtensa/translate.c:538:static bool gen_window_check(DisasContext *dc, uint32_t mask)
target/xtensa/translate.c:539:{
target/xtensa/translate.c:553:static TCGv_i32 gen_mac16_m(TCGv_i32 v, bool hi, bool is_unsigned)
target/xtensa/translate.c:554:{
target/xtensa/translate.c:565:static void gen_zero_check(DisasContext *dc, const OpcodeArg arg[])
target/xtensa/translate.c:566:{
target/xtensa/translate.c:574:static inline unsigned xtensa_op0_insn_len(DisasContext *dc, uint8_t op0)
target/xtensa/translate.c:575:{
target/xtensa/translate.c:579:static int gen_postprocess(DisasContext *dc, int slot)
target/xtensa/translate.c:580:{
target/xtensa/translate.c:627:static uint32_t encode_resource(enum resource_type r, unsigned g, unsigned n)
target/xtensa/translate.c:628:{
target/xtensa/translate.c:633:static enum resource_type get_resource_type(uint32_t resource)
target/xtensa/translate.c:634:{
target/xtensa/translate.c:642:static bool op_depends_on(const struct slot_prop *a,
target/xtensa/translate.c:644:{
target/xtensa/translate.c:673:static bool break_dependency(struct slot_prop *a,
target/xtensa/translate.c:677:{
target/xtensa/translate.c:719:static bool tsort(struct slot_prop *slot,
target/xtensa/translate.c:724:{
target/xtensa/translate.c:804:static void opcode_add_resource(struct slot_prop *op,
target/xtensa/translate.c:807:{
target/xtensa/translate.c:829:static int resource_compare(const void *a, const void *b)
target/xtensa/translate.c:830:{
target/xtensa/translate.c:838:static int arg_copy_compare(const void *a, const void *b)
target/xtensa/translate.c:839:{
target/xtensa/translate.c:847:static void disas_xtensa_insn(CPUXtensaState *env, DisasContext *dc)
target/xtensa/translate.c:848:{
target/xtensa/translate.c:1139:static inline unsigned xtensa_insn_len(CPUXtensaState *env, DisasContext *dc)
target/xtensa/translate.c:1140:{
target/xtensa/translate.c:1145:static void gen_ibreak_check(CPUXtensaState *env, DisasContext *dc)
target/xtensa/translate.c:1146:{
target/xtensa/translate.c:1158:static void xtensa_tr_init_disas_context(DisasContextBase *dcbase,
target/xtensa/translate.c:1160:{
target/xtensa/translate.c:1185:static void xtensa_tr_tb_start(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1186:{
target/xtensa/translate.c:1194:static void xtensa_tr_insn_start(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1195:{
target/xtensa/translate.c:1199:static void xtensa_tr_translate_insn(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1200:{
target/xtensa/translate.c:1246:static void xtensa_tr_tb_stop(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1247:{
target/xtensa/translate.c:1266:static void xtensa_tr_disas_log(const DisasContextBase *dcbase,
target/xtensa/translate.c:1268:{
target/xtensa/translate.c:1282:void gen_intermediate_code(CPUState *cpu, TranslationBlock *tb, int max_insns,
target/xtensa/translate.c:1284:{
target/xtensa/translate.c:1290:void xtensa_cpu_dump_state(CPUState *cs, FILE *f, int flags)
target/xtensa/translate.c:1291:{
target/xtensa/translate.c:1358:void restore_state_to_opc(CPUXtensaState *env, TranslationBlock *tb,
target/xtensa/translate.c:1360:{
target/xtensa/translate.c:1364:static void translate_abs(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1366:{
target/xtensa/translate.c:1370:static void translate_add(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1372:{
target/xtensa/translate.c:1376:static void translate_addi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1378:{
target/xtensa/translate.c:1382:static void translate_addx(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1384:{
target/xtensa/translate.c:1391:static void translate_all(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1393:{
target/xtensa/translate.c:1411:static void translate_and(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1413:{
target/xtensa/translate.c:1417:static void translate_ball(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1419:{
target/xtensa/translate.c:1426:static void translate_bany(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1428:{
target/xtensa/translate.c:1435:static void translate_b(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1437:{
target/xtensa/translate.c:1441:static void translate_bb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1443:{
target/xtensa/translate.c:1462:static void translate_bbi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1464:{
target/xtensa/translate.c:1475:static void translate_bi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1477:{
target/xtensa/translate.c:1481:static void translate_bz(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1483:{
target/xtensa/translate.c:1495:static void translate_boolean(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1497:{
target/xtensa/translate.c:1517:static void translate_bp(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1519:{
target/xtensa/translate.c:1527:static void translate_call0(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1529:{
target/xtensa/translate.c:1534:static void translate_callw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1536:{
target/xtensa/translate.c:1542:static void translate_callx0(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1544:{
target/xtensa/translate.c:1552:static void translate_callxw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1554:{
target/xtensa/translate.c:1562:static void translate_clamps(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1564:{
target/xtensa/translate.c:1574:static void translate_clrb_expstate(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1576:{
target/xtensa/translate.c:1581:static void translate_clrex(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1583:{
target/xtensa/translate.c:1587:static void translate_const16(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1589:{
target/xtensa/translate.c:1596:static void translate_dcache(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1598:{
target/xtensa/translate.c:1608:static void translate_depbits(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1610:{
target/xtensa/translate.c:1615:static void translate_diwbuip(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1617:{
target/xtensa/translate.c:1621:static uint32_t test_exceptions_entry(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1623:{
target/xtensa/translate.c:1633:static uint32_t test_overflow_entry(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1635:{
target/xtensa/translate.c:1639:static void translate_entry(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1641:{
target/xtensa/translate.c:1648:static void translate_extui(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1650:{
target/xtensa/translate.c:1659:static void translate_getex(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1661:{
target/xtensa/translate.c:1670:static void translate_icache(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1672:{
target/xtensa/translate.c:1683:static void translate_itlb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1685:{
target/xtensa/translate.c:1693:static void translate_j(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1695:{
target/xtensa/translate.c:1699:static void translate_jx(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1701:{
target/xtensa/translate.c:1705:static void translate_l32e(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1707:{
target/xtensa/translate.c:1718:static void gen_check_exclusive(DisasContext *dc, TCGv_i32 addr, bool is_write)
target/xtensa/translate.c:1719:{
target/xtensa/translate.c:1722:static void gen_check_exclusive(DisasContext *dc, TCGv_i32 addr, bool is_write)
target/xtensa/translate.c:1723:{
target/xtensa/translate.c:1733:static void translate_l32ex(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1735:{
target/xtensa/translate.c:1748:static void translate_ldst(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1750:{
target/xtensa/translate.c:1771:static void translate_lct(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1773:{
target/xtensa/translate.c:1777:static void translate_l32r(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1779:{
target/xtensa/translate.c:1792:static void translate_loop(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1794:{
target/xtensa/translate.c:1829:static void translate_mac16(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1831:{
target/xtensa/translate.c:1890:static void translate_memw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1892:{
target/xtensa/translate.c:1896:static void translate_smin(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1898:{
target/xtensa/translate.c:1902:static void translate_umin(DisasContext *dc, const OpcodeArg arg[],
```

- `read_file(path=softmmu/vl.c, start_line=1800, end_line=1826, version=old)` →

```
softmmu/vl.c lines 1800-1826 of 3593
 1800|         g_str_equal(type, "filter-mirror") ||
 1801|         g_str_equal(type, "filter-redirector") ||
 1802|         g_str_equal(type, "colo-compare") ||
 1803|         g_str_equal(type, "filter-rewriter") ||
 1804|         g_str_equal(type, "filter-replay")) {
 1805|         return false;
 1806|     }
 1807| 
 1808|     /*
 1809|      * Allocation of large amounts of memory may delay
 1810|      * chardev initialization for too long, and trigger timeouts
 1811|      * on software that waits for a monitor socket to be created
 1812|      * (e.g. libvirt).
 1813|      */
 1814|     if (g_str_has_prefix(type, "memory-backend-")) {
 1815|         return false;
 1816|     }
 1817| 
 1818|     return true;
 1819| }
 1820| 
 1821| static void qemu_apply_machine_options(QDict *qdict)
 1822| {
 1823|     object_set_properties_from_keyval(OBJECT(current_machine), qdict, false, &error_fatal);
 1824| 
 1825|     if (semihosting_enabled() && !semihosting_get_argc()) {
 1826|         /* fall back to the -kernel/-append */
```

- `read_file(path=target/m68k/op_helper.c, start_line=190, end_line=210, version=old)` →

```
target/m68k/op_helper.c lines 190-210 of 1128
  190|     uint32_t sp;
  191|     uint32_t sr;
  192|     uint32_t fmt;
  193|     uint32_t retaddr;
  194|     uint32_t vector;
  195| 
  196|     fmt = 0;
  197|     retaddr = env->pc;
  198| 
  199|     if (!is_hw) {
  200|         switch (cs->exception_index) {
  201|         case EXCP_RTE:
  202|             /* Return from an exception.  */
  203|             cf_rte(env);
  204|             return;
  205|         case EXCP_HALT_INSN:
  206|             if (semihosting_enabled()
  207|                     && (env->sr & SR_S) != 0
  208|                     && (env->pc & 3) == 0
  209|                     && cpu_lduw_code(env, env->pc - 4) == 0x4e71
  210|                     && cpu_ldl_code(env, env->pc) == 0x4e7bf000) {
```

- `read_file(path=target/mips/tcg/translate.c, start_line=12085, end_line=12091, version=old)` →

```
target/mips/tcg/translate.c lines 12085-12091 of 16247
12085| static inline bool is_uhi(int sdbbp_code)
12086| {
12087| #ifdef CONFIG_USER_ONLY
12088|     return false;
12089| #else
12090|     return semihosting_enabled() && sdbbp_code == 1;
12091| #endif
```

- `grep(pattern=^[a-z_].*\(, version=old, path_glob=target/arm/translate.c, max_results=400)` →

```
475 matches (showing 200)
target/arm/translate.c:69:void arm_translate_init(void)
target/arm/translate.c:91:uint64_t asimd_imm_const(uint32_t imm, int cmode, int op)
target/arm/translate.c:162:void arm_gen_condlabel(DisasContext *s)
target/arm/translate.c:186:void store_cpu_offset(TCGv_i32 var, int offset, int size)
target/arm/translate.c:202:static void disas_set_da_iss(DisasContext *s, MemOp memop, ISSInfo issinfo)
target/arm/translate.c:232:static inline int get_a32_user_mem_index(DisasContext *s)
target/arm/translate.c:268:static uint32_t read_pc(DisasContext *s)
target/arm/translate.c:274:void load_reg_var(DisasContext *s, TCGv_i32 var, int reg)
target/arm/translate.c:302:void store_reg(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:327:static void store_sp_checked(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:346:void gen_set_cpsr(TCGv_i32 var, uint32_t mask)
target/arm/translate.c:351:static void gen_rebuild_hflags(DisasContext *s, bool new_el)
target/arm/translate.c:371:static void gen_exception_internal(int excp)
target/arm/translate.c:377:static void gen_singlestep_exception(DisasContext *s)
target/arm/translate.c:393:void clear_eci_state(DisasContext *s)
target/arm/translate.c:405:static void gen_smul_dual(TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:421:void gen_rev16(TCGv_i32 dest, TCGv_i32 var)
target/arm/translate.c:434:static void gen_revsh(TCGv_i32 dest, TCGv_i32 var)
target/arm/translate.c:446:static void gen_add16(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:459:static inline void gen_logic_CC(TCGv_i32 var)
target/arm/translate.c:466:static void gen_add_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:473:static void gen_sub_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:481:static void gen_add_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:495:static void gen_adc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:523:static void gen_sub_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:538:static void gen_sbc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:547:static void gen_##name(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)       \
target/arm/translate.c:563:static void gen_sar(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:573:static void shifter_out_im(TCGv_i32 var, int shift)
target/arm/translate.c:579:static inline void gen_arm_shift_im(TCGv_i32 var, int shiftop,
target/arm/translate.c:628:static inline void gen_arm_shift_reg(TCGv_i32 var, int shiftop,
target/arm/translate.c:660:void arm_test_cc(DisasCompare *cmp, int cc)
target/arm/translate.c:746:void arm_free_cc(DisasCompare *cmp)
target/arm/translate.c:753:void arm_jump_cc(DisasCompare *cmp, TCGLabel *label)
target/arm/translate.c:758:void arm_gen_test_cc(int cc, TCGLabel *label)
target/arm/translate.c:766:void gen_set_condexec(DisasContext *s)
target/arm/translate.c:775:void gen_set_pc_im(DisasContext *s, target_ulong val)
target/arm/translate.c:781:static inline void gen_bx(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:811:static inline void gen_bx_excret(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:825:static inline void gen_bx_excret_final_code(DisasContext *s)
target/arm/translate.c:863:static inline void gen_bxns(DisasContext *s, int rm)
target/arm/translate.c:882:static inline void gen_blxns(DisasContext *s, int rm)
target/arm/translate.c:899:static inline void store_reg_bx(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:912:static inline void store_reg_from_load(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:951:static TCGv gen_aa32_addr(DisasContext *s, TCGv_i32 a32, MemOp op)
target/arm/translate.c:967:void gen_aa32_ld_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:975:void gen_aa32_st_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:983:void gen_aa32_ld_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:997:void gen_aa32_st_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:1014:void gen_aa32_ld_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1020:void gen_aa32_st_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1026:void gen_aa32_ld_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1032:void gen_aa32_st_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1052:static inline void gen_hvc(DisasContext *s, int imm16)
target/arm/translate.c:1070:static inline void gen_smc(DisasContext *s)
target/arm/translate.c:1081:static void gen_exception_internal_insn(DisasContext *s, uint32_t pc, int excp)
target/arm/translate.c:1089:static void gen_exception_el_v(int excp, uint32_t syndrome, TCGv_i32 tcg_el)
target/arm/translate.c:1095:static void gen_exception_el(int excp, uint32_t syndrome, uint32_t target_el)
target/arm/translate.c:1100:static void gen_exception(int excp, uint32_t syndrome)
target/arm/translate.c:1106:static void gen_exception_insn_el_v(DisasContext *s, uint64_t pc, int excp,
target/arm/translate.c:1119:void gen_exception_insn_el(DisasContext *s, uint64_t pc, int excp,
target/arm/translate.c:1125:void gen_exception_insn(DisasContext *s, uint64_t pc, int excp, uint32_t syn)
target/arm/translate.c:1137:static void gen_exception_bkpt_insn(DisasContext *s, uint32_t syn)
target/arm/translate.c:1145:void unallocated_encoding(DisasContext *s)
target/arm/translate.c:1152:void gen_lookup_tb(DisasContext *s)
target/arm/translate.c:1158:static inline void gen_hlt(DisasContext *s, int imm)
target/arm/translate.c:1187:long neon_full_reg_offset(unsigned reg)
target/arm/translate.c:1196:long neon_element_offset(int reg, int element, MemOp memop)
target/arm/translate.c:1213:long vfp_reg_offset(bool dp, unsigned reg)
target/arm/translate.c:1222:void read_neon_element32(TCGv_i32 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1248:void read_neon_element64(TCGv_i64 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1267:void write_neon_element32(TCGv_i32 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1286:void write_neon_element64(TCGv_i64 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1304:static inline void iwmmxt_load_reg(TCGv_i64 var, int reg)
target/arm/translate.c:1309:static inline void iwmmxt_store_reg(TCGv_i64 var, int reg)
target/arm/translate.c:1314:static inline TCGv_i32 iwmmxt_load_creg(int reg)
target/arm/translate.c:1321:static inline void iwmmxt_store_creg(int reg, TCGv_i32 var)
target/arm/translate.c:1327:static inline void gen_op_iwmmxt_movq_wRn_M0(int rn)
target/arm/translate.c:1332:static inline void gen_op_iwmmxt_movq_M0_wRn(int rn)
target/arm/translate.c:1337:static inline void gen_op_iwmmxt_orq_M0_wRn(int rn)
target/arm/translate.c:1343:static inline void gen_op_iwmmxt_andq_M0_wRn(int rn)
target/arm/translate.c:1349:static inline void gen_op_iwmmxt_xorq_M0_wRn(int rn)
target/arm/translate.c:1356:static inline void gen_op_iwmmxt_##name##_M0_wRn(int rn) \
target/arm/translate.c:1363:static inline void gen_op_iwmmxt_##name##_M0_wRn(int rn) \
target/arm/translate.c:1375:static inline void gen_op_iwmmxt_##name##_M0(void) \
target/arm/translate.c:1435:static void gen_op_iwmmxt_set_mup(void)
target/arm/translate.c:1443:static void gen_op_iwmmxt_set_cup(void)
target/arm/translate.c:1451:static void gen_op_iwmmxt_setpsr_nz(void)
target/arm/translate.c:1458:static inline void gen_op_iwmmxt_addl_M0_wRn(int rn)
target/arm/translate.c:1465:static inline int gen_iwmmxt_address(DisasContext *s, uint32_t insn,
target/arm/translate.c:1500:static inline int gen_iwmmxt_shift(uint32_t insn, uint32_t mask, TCGv_i32 dest)
target/arm/translate.c:1524:static int disas_iwmmxt_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:2524:static int disas_dsp_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:2591:static void gen_goto_ptr(void)
target/arm/translate.c:2600:static void gen_goto_tb(DisasContext *s, int n, target_ulong dest)
target/arm/translate.c:2614:static inline void gen_jmp_tb(DisasContext *s, uint32_t dest, int tbno)
target/arm/translate.c:2657:static inline void gen_jmp(DisasContext *s, uint32_t dest)
target/arm/translate.c:2662:static inline void gen_mulxy(TCGv_i32 t0, TCGv_i32 t1, int x, int y)
target/arm/translate.c:2676:static uint32_t msr_mask(DisasContext *s, int flags, int spsr)
target/arm/translate.c:2709:static int gen_set_psr(DisasContext *s, uint32_t mask, int spsr, TCGv_i32 t0)
target/arm/translate.c:2731:static int gen_set_psr_im(DisasContext *s, uint32_t mask, int spsr, uint32_t val)
target/arm/translate.c:2739:static bool msr_banked_access_decode(DisasContext *s, int r, int sysm, int rn,
target/arm/translate.c:2901:static void gen_msr_banked(DisasContext *s, int r, int sysm, int rn)
target/arm/translate.c:2921:static void gen_mrs_banked(DisasContext *s, int r, int sysm, int rn)
target/arm/translate.c:2945:static void store_pc_exc_ret(DisasContext *s, TCGv_i32 pc)
target/arm/translate.c:2952:static void gen_rfe(DisasContext *s, TCGv_i32 pc, TCGv_i32 cpsr)
target/arm/translate.c:2969:static void gen_exception_return(DisasContext *s, TCGv_i32 pc)
target/arm/translate.c:2974:static void gen_gvec_fn3_qc(uint32_t rd_ofs, uint32_t rn_ofs, uint32_t rm_ofs,
target/arm/translate.c:2986:void gen_gvec_sqrdmlah_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:2996:void gen_gvec_sqrdmlsh_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3059:static void gen_ssra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3065:static void gen_ssra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3071:static void gen_ssra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3077:static void gen_ssra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3083:static void gen_ssra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3089:void gen_gvec_ssra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3135:static void gen_usra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3141:static void gen_usra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3147:static void gen_usra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3153:static void gen_usra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3159:static void gen_usra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3165:void gen_gvec_usra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3221:static void gen_srshr8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3232:static void gen_srshr16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3243:static void gen_srshr32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3259:static void gen_srshr64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3269:static void gen_srshr_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3284:void gen_gvec_srshr(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3331:static void gen_srsra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3340:static void gen_srsra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3349:static void gen_srsra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3358:static void gen_srsra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3367:static void gen_srsra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3376:void gen_gvec_srsra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3428:static void gen_urshr8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3439:static void gen_urshr16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3450:static void gen_urshr32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3466:static void gen_urshr64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3476:static void gen_urshr_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t shift)
target/arm/translate.c:3491:void gen_gvec_urshr(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3537:static void gen_ursra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3550:static void gen_ursra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3563:static void gen_ursra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3576:static void gen_ursra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3589:static void gen_ursra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3602:void gen_gvec_ursra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3643:static void gen_shr8_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3655:static void gen_shr16_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3667:static void gen_shr32_ins_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3673:static void gen_shr64_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3679:static void gen_shr_ins_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3693:void gen_gvec_sri(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3738:static void gen_shl8_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3750:static void gen_shl16_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3762:static void gen_shl32_ins_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3767:static void gen_shl64_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3772:static void gen_shl_ins_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3786:void gen_gvec_sli(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3829:static void gen_mla8_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3835:static void gen_mls8_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3841:static void gen_mla16_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3847:static void gen_mls16_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3853:static void gen_mla32_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3859:static void gen_mls32_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3865:static void gen_mla64_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3871:static void gen_mls64_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3877:static void gen_mla_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3883:static void gen_mls_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3892:void gen_gvec_mla(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3924:void gen_gvec_mls(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3957:static void gen_cmtst_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3964:void gen_cmtst_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3971:static void gen_cmtst_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3978:void gen_gvec_cmtst(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4004:void gen_ushl_i32(TCGv_i32 dst, TCGv_i32 src, TCGv_i32 shift)
target/arm/translate.c:4031:void gen_ushl_i64(TCGv_i64 dst, TCGv_i64 src, TCGv_i64 shift)
target/arm/translate.c:4058:static void gen_ushl_vec(unsigned vece, TCGv_vec dst,
target/arm/translate.c:4116:void gen_gvec_ushl(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4144:void gen_sshl_i32(TCGv_i32 dst, TCGv_i32 src, TCGv_i32 shift)
target/arm/translate.c:4172:void gen_sshl_i64(TCGv_i64 dst, TCGv_i64 src, TCGv_i64 shift)
target/arm/translate.c:4200:static void gen_sshl_vec(unsigned vece, TCGv_vec dst,
target/arm/translate.c:4250:void gen_gvec_sshl(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4278:static void gen_uqadd_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4289:void gen_gvec_uqadd_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4321:static void gen_sqadd_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4332:void gen_gvec_sqadd_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4364:static void gen_uqsub_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4375:void gen_gvec_uqsub_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4407:static void gen_sqsub_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4418:void gen_gvec_sqsub_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4450:static void gen_sabd_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4460:static void gen_sabd_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:4470:static void gen_sabd_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:4480:void gen_gvec_sabd(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4510:static void gen_uabd_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4520:static void gen_uabd_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:4530:static void gen_uabd_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:4540:void gen_gvec_uabd(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4570:static void gen_saba_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4578:static void gen_saba_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
```

### Turn 3  _(tok 19746+443, stop=tool_use)_

**Reasoning:** I'm trying to avoid wasteful reads, so I'll use targeted ones. The ARM translate.c hit is at line 1172 inside gen_hlt, which starts at 1158. Lines 6559 and 8767 still need a lookup, and I'll check the xtensa range 2369 to 2381.



- `grep(pattern=^(static )?[a-z_].*\(.*(\)|,)$, version=old, path_glob=target/arm/translate.c, max_results=500)` →

```
461 matches (showing 200)
target/arm/translate.c:69:void arm_translate_init(void)
target/arm/translate.c:91:uint64_t asimd_imm_const(uint32_t imm, int cmode, int op)
target/arm/translate.c:162:void arm_gen_condlabel(DisasContext *s)
target/arm/translate.c:186:void store_cpu_offset(TCGv_i32 var, int offset, int size)
target/arm/translate.c:202:static void disas_set_da_iss(DisasContext *s, MemOp memop, ISSInfo issinfo)
target/arm/translate.c:232:static inline int get_a32_user_mem_index(DisasContext *s)
target/arm/translate.c:268:static uint32_t read_pc(DisasContext *s)
target/arm/translate.c:274:void load_reg_var(DisasContext *s, TCGv_i32 var, int reg)
target/arm/translate.c:302:void store_reg(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:327:static void store_sp_checked(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:346:void gen_set_cpsr(TCGv_i32 var, uint32_t mask)
target/arm/translate.c:351:static void gen_rebuild_hflags(DisasContext *s, bool new_el)
target/arm/translate.c:371:static void gen_exception_internal(int excp)
target/arm/translate.c:377:static void gen_singlestep_exception(DisasContext *s)
target/arm/translate.c:393:void clear_eci_state(DisasContext *s)
target/arm/translate.c:405:static void gen_smul_dual(TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:421:void gen_rev16(TCGv_i32 dest, TCGv_i32 var)
target/arm/translate.c:434:static void gen_revsh(TCGv_i32 dest, TCGv_i32 var)
target/arm/translate.c:446:static void gen_add16(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:459:static inline void gen_logic_CC(TCGv_i32 var)
target/arm/translate.c:466:static void gen_add_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:473:static void gen_sub_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:481:static void gen_add_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:495:static void gen_adc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:523:static void gen_sub_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:538:static void gen_sbc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:563:static void gen_sar(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:573:static void shifter_out_im(TCGv_i32 var, int shift)
target/arm/translate.c:579:static inline void gen_arm_shift_im(TCGv_i32 var, int shiftop,
target/arm/translate.c:628:static inline void gen_arm_shift_reg(TCGv_i32 var, int shiftop,
target/arm/translate.c:660:void arm_test_cc(DisasCompare *cmp, int cc)
target/arm/translate.c:746:void arm_free_cc(DisasCompare *cmp)
target/arm/translate.c:753:void arm_jump_cc(DisasCompare *cmp, TCGLabel *label)
target/arm/translate.c:758:void arm_gen_test_cc(int cc, TCGLabel *label)
target/arm/translate.c:766:void gen_set_condexec(DisasContext *s)
target/arm/translate.c:775:void gen_set_pc_im(DisasContext *s, target_ulong val)
target/arm/translate.c:781:static inline void gen_bx(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:811:static inline void gen_bx_excret(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:825:static inline void gen_bx_excret_final_code(DisasContext *s)
target/arm/translate.c:863:static inline void gen_bxns(DisasContext *s, int rm)
target/arm/translate.c:882:static inline void gen_blxns(DisasContext *s, int rm)
target/arm/translate.c:899:static inline void store_reg_bx(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:912:static inline void store_reg_from_load(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:951:static TCGv gen_aa32_addr(DisasContext *s, TCGv_i32 a32, MemOp op)
target/arm/translate.c:967:void gen_aa32_ld_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:975:void gen_aa32_st_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:983:void gen_aa32_ld_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:997:void gen_aa32_st_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:1014:void gen_aa32_ld_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1020:void gen_aa32_st_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1026:void gen_aa32_ld_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1032:void gen_aa32_st_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1052:static inline void gen_hvc(DisasContext *s, int imm16)
target/arm/translate.c:1070:static inline void gen_smc(DisasContext *s)
target/arm/translate.c:1081:static void gen_exception_internal_insn(DisasContext *s, uint32_t pc, int excp)
target/arm/translate.c:1089:static void gen_exception_el_v(int excp, uint32_t syndrome, TCGv_i32 tcg_el)
target/arm/translate.c:1095:static void gen_exception_el(int excp, uint32_t syndrome, uint32_t target_el)
target/arm/translate.c:1100:static void gen_exception(int excp, uint32_t syndrome)
target/arm/translate.c:1106:static void gen_exception_insn_el_v(DisasContext *s, uint64_t pc, int excp,
target/arm/translate.c:1119:void gen_exception_insn_el(DisasContext *s, uint64_t pc, int excp,
target/arm/translate.c:1125:void gen_exception_insn(DisasContext *s, uint64_t pc, int excp, uint32_t syn)
target/arm/translate.c:1137:static void gen_exception_bkpt_insn(DisasContext *s, uint32_t syn)
target/arm/translate.c:1145:void unallocated_encoding(DisasContext *s)
target/arm/translate.c:1152:void gen_lookup_tb(DisasContext *s)
target/arm/translate.c:1158:static inline void gen_hlt(DisasContext *s, int imm)
target/arm/translate.c:1187:long neon_full_reg_offset(unsigned reg)
target/arm/translate.c:1196:long neon_element_offset(int reg, int element, MemOp memop)
target/arm/translate.c:1213:long vfp_reg_offset(bool dp, unsigned reg)
target/arm/translate.c:1222:void read_neon_element32(TCGv_i32 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1248:void read_neon_element64(TCGv_i64 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1267:void write_neon_element32(TCGv_i32 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1286:void write_neon_element64(TCGv_i64 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1304:static inline void iwmmxt_load_reg(TCGv_i64 var, int reg)
target/arm/translate.c:1309:static inline void iwmmxt_store_reg(TCGv_i64 var, int reg)
target/arm/translate.c:1314:static inline TCGv_i32 iwmmxt_load_creg(int reg)
target/arm/translate.c:1321:static inline void iwmmxt_store_creg(int reg, TCGv_i32 var)
target/arm/translate.c:1327:static inline void gen_op_iwmmxt_movq_wRn_M0(int rn)
target/arm/translate.c:1332:static inline void gen_op_iwmmxt_movq_M0_wRn(int rn)
target/arm/translate.c:1337:static inline void gen_op_iwmmxt_orq_M0_wRn(int rn)
target/arm/translate.c:1343:static inline void gen_op_iwmmxt_andq_M0_wRn(int rn)
target/arm/translate.c:1349:static inline void gen_op_iwmmxt_xorq_M0_wRn(int rn)
target/arm/translate.c:1435:static void gen_op_iwmmxt_set_mup(void)
target/arm/translate.c:1443:static void gen_op_iwmmxt_set_cup(void)
target/arm/translate.c:1451:static void gen_op_iwmmxt_setpsr_nz(void)
target/arm/translate.c:1458:static inline void gen_op_iwmmxt_addl_M0_wRn(int rn)
target/arm/translate.c:1465:static inline int gen_iwmmxt_address(DisasContext *s, uint32_t insn,
target/arm/translate.c:1500:static inline int gen_iwmmxt_shift(uint32_t insn, uint32_t mask, TCGv_i32 dest)
target/arm/translate.c:1524:static int disas_iwmmxt_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:2524:static int disas_dsp_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:2591:static void gen_goto_ptr(void)
target/arm/translate.c:2600:static void gen_goto_tb(DisasContext *s, int n, target_ulong dest)
target/arm/translate.c:2614:static inline void gen_jmp_tb(DisasContext *s, uint32_t dest, int tbno)
target/arm/translate.c:2657:static inline void gen_jmp(DisasContext *s, uint32_t dest)
target/arm/translate.c:2662:static inline void gen_mulxy(TCGv_i32 t0, TCGv_i32 t1, int x, int y)
target/arm/translate.c:2676:static uint32_t msr_mask(DisasContext *s, int flags, int spsr)
target/arm/translate.c:2709:static int gen_set_psr(DisasContext *s, uint32_t mask, int spsr, TCGv_i32 t0)
target/arm/translate.c:2731:static int gen_set_psr_im(DisasContext *s, uint32_t mask, int spsr, uint32_t val)
target/arm/translate.c:2739:static bool msr_banked_access_decode(DisasContext *s, int r, int sysm, int rn,
target/arm/translate.c:2901:static void gen_msr_banked(DisasContext *s, int r, int sysm, int rn)
target/arm/translate.c:2921:static void gen_mrs_banked(DisasContext *s, int r, int sysm, int rn)
target/arm/translate.c:2945:static void store_pc_exc_ret(DisasContext *s, TCGv_i32 pc)
target/arm/translate.c:2952:static void gen_rfe(DisasContext *s, TCGv_i32 pc, TCGv_i32 cpsr)
target/arm/translate.c:2969:static void gen_exception_return(DisasContext *s, TCGv_i32 pc)
target/arm/translate.c:2974:static void gen_gvec_fn3_qc(uint32_t rd_ofs, uint32_t rn_ofs, uint32_t rm_ofs,
target/arm/translate.c:2986:void gen_gvec_sqrdmlah_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:2996:void gen_gvec_sqrdmlsh_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3059:static void gen_ssra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3065:static void gen_ssra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3071:static void gen_ssra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3077:static void gen_ssra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3083:static void gen_ssra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3089:void gen_gvec_ssra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3135:static void gen_usra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3141:static void gen_usra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3147:static void gen_usra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3153:static void gen_usra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3159:static void gen_usra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3165:void gen_gvec_usra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3221:static void gen_srshr8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3232:static void gen_srshr16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3243:static void gen_srshr32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3259:static void gen_srshr64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3269:static void gen_srshr_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3284:void gen_gvec_srshr(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3331:static void gen_srsra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3340:static void gen_srsra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3349:static void gen_srsra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3358:static void gen_srsra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3367:static void gen_srsra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3376:void gen_gvec_srsra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3428:static void gen_urshr8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3439:static void gen_urshr16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3450:static void gen_urshr32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3466:static void gen_urshr64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3476:static void gen_urshr_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t shift)
target/arm/translate.c:3491:void gen_gvec_urshr(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3537:static void gen_ursra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3550:static void gen_ursra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3563:static void gen_ursra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3576:static void gen_ursra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3589:static void gen_ursra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3602:void gen_gvec_ursra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3643:static void gen_shr8_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3655:static void gen_shr16_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3667:static void gen_shr32_ins_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3673:static void gen_shr64_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3679:static void gen_shr_ins_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3693:void gen_gvec_sri(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3738:static void gen_shl8_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3750:static void gen_shl16_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3762:static void gen_shl32_ins_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3767:static void gen_shl64_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3772:static void gen_shl_ins_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3786:void gen_gvec_sli(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3829:static void gen_mla8_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3835:static void gen_mls8_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3841:static void gen_mla16_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3847:static void gen_mls16_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3853:static void gen_mla32_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3859:static void gen_mls32_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3865:static void gen_mla64_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3871:static void gen_mls64_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3877:static void gen_mla_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3883:static void gen_mls_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3892:void gen_gvec_mla(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3924:void gen_gvec_mls(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3957:static void gen_cmtst_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3964:void gen_cmtst_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3971:static void gen_cmtst_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3978:void gen_gvec_cmtst(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4004:void gen_ushl_i32(TCGv_i32 dst, TCGv_i32 src, TCGv_i32 shift)
target/arm/translate.c:4031:void gen_ushl_i64(TCGv_i64 dst, TCGv_i64 src, TCGv_i64 shift)
target/arm/translate.c:4058:static void gen_ushl_vec(unsigned vece, TCGv_vec dst,
target/arm/translate.c:4116:void gen_gvec_ushl(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4144:void gen_sshl_i32(TCGv_i32 dst, TCGv_i32 src, TCGv_i32 shift)
target/arm/translate.c:4172:void gen_sshl_i64(TCGv_i64 dst, TCGv_i64 src, TCGv_i64 shift)
target/arm/translate.c:4200:static void gen_sshl_vec(unsigned vece, TCGv_vec dst,
target/arm/translate.c:4250:void gen_gvec_sshl(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4278:static void gen_uqadd_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4289:void gen_gvec_uqadd_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4321:static void gen_sqadd_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4332:void gen_gvec_sqadd_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4364:static void gen_uqsub_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4375:void gen_gvec_uqsub_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4407:static void gen_sqsub_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4418:void gen_gvec_sqsub_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4450:static void gen_sabd_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4460:static void gen_sabd_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:4470:static void gen_sabd_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:4480:void gen_gvec_sabd(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4510:static void gen_uabd_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4520:static void gen_uabd_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:4530:static void gen_uabd_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:4540:void gen_gvec_uabd(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4570:static void gen_saba_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4578:static void gen_saba_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:4586:static void gen_saba_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:4594:void gen_gvec_saba(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4629:static void gen_uaba_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4637:static void gen_uaba_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
```

- `read_file(path=target/xtensa/translate.c, start_line=2355, end_line=2385, version=old)` →

```
target/xtensa/translate.c lines 2355-2385 of 7852
 2355|         tcg_gen_shli_i32(tmp, arg[1].in, shift);
 2356|         tcg_gen_sari_i32(arg[0].out, tmp, shift);
 2357|         tcg_temp_free(tmp);
 2358|     }
 2359| }
 2360| 
 2361| static uint32_t test_exceptions_simcall(DisasContext *dc,
 2362|                                         const OpcodeArg arg[],
 2363|                                         const uint32_t par[])
 2364| {
 2365| #ifdef CONFIG_USER_ONLY
 2366|     bool ill = true;
 2367| #else
 2368|     /* Between RE.2 and RE.3 simcall opcode's become nop for the hardware. */
 2369|     bool ill = dc->config->hw_version <= 250002 && !semihosting_enabled();
 2370| #endif
 2371|     if (ill || !semihosting_enabled()) {
 2372|         qemu_log_mask(LOG_GUEST_ERROR, "SIMCALL but semihosting is disabled\n");
 2373|     }
 2374|     return ill ? XTENSA_OP_ILL : 0;
 2375| }
 2376| 
 2377| static void translate_simcall(DisasContext *dc, const OpcodeArg arg[],
 2378|                               const uint32_t par[])
 2379| {
 2380| #ifndef CONFIG_USER_ONLY
 2381|     if (semihosting_enabled()) {
 2382|         gen_helper_simcall(cpu_env);
 2383|     }
 2384| #endif
 2385| }
```

- `grep(pattern=^[a-z_].*\(, version=old, path_glob=target/nios2/translate.c)` →

```
85 matches (showing 60)
target/nios2/translate.c:73:typedef target_ulong ImmFromIType(const InstrIType *);
target/nios2/translate.c:75:static target_ulong imm_unsigned(const InstrIType *i)
target/nios2/translate.c:80:static target_ulong imm_signed(const InstrIType *i)
target/nios2/translate.c:85:static target_ulong imm_shifted(const InstrIType *i)
target/nios2/translate.c:122:typedef void GenFn2i(TCGv, TCGv, target_long);
target/nios2/translate.c:123:typedef void GenFn3(TCGv, TCGv, TCGv);
target/nios2/translate.c:124:typedef void GenFn4(TCGv, TCGv, TCGv, TCGv);
target/nios2/translate.c:147:static uint8_t get_opcode(uint32_t code)
target/nios2/translate.c:153:static uint8_t get_opxcode(uint32_t code)
target/nios2/translate.c:159:static TCGv load_gpr(DisasContext *dc, unsigned reg)
target/nios2/translate.c:181:static TCGv dest_gpr(DisasContext *dc, unsigned reg)
target/nios2/translate.c:205:static void t_gen_helper_raise_exception(DisasContext *dc, uint32_t index)
target/nios2/translate.c:213:static void gen_goto_tb(DisasContext *dc, int n, uint32_t dest)
target/nios2/translate.c:228:static void gen_jumpr(DisasContext *dc, int regno, bool is_call)
target/nios2/translate.c:251:static void gen_excp(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:256:static bool gen_check_supervisor(DisasContext *dc)
target/nios2/translate.c:270:static void nop(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:278:static void jmpi(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:284:static void call(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:294:static void gen_ldx(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:307:static void gen_stx(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:319:static void br(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:326:static void gen_bxx(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:338:static void do_i_cmpxx(DisasContext *dc, uint32_t insn,
target/nios2/translate.c:350:gen_i_cmpxx(gen_cmpxxsi, imm_signed)
target/nios2/translate.c:351:gen_i_cmpxx(gen_cmpxxui, imm_unsigned)
target/nios2/translate.c:354:static void do_i_math_logic(DisasContext *dc, uint32_t insn,
target/nios2/translate.c:380:gen_i_math_logic(addi,  addi, 1, imm_signed)
target/nios2/translate.c:381:gen_i_math_logic(muli,  muli, 0, imm_signed)
target/nios2/translate.c:383:gen_i_math_logic(andi,  andi, 0, imm_unsigned)
target/nios2/translate.c:384:gen_i_math_logic(ori,   ori,  1, imm_unsigned)
target/nios2/translate.c:385:gen_i_math_logic(xori,  xori, 1, imm_unsigned)
target/nios2/translate.c:387:gen_i_math_logic(andhi, andi, 0, imm_shifted)
target/nios2/translate.c:388:gen_i_math_logic(orhi , ori,  1, imm_shifted)
target/nios2/translate.c:389:gen_i_math_logic(xorhi, xori, 1, imm_shifted)
target/nios2/translate.c:392:static void rdprs(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:413:static void handle_r_type_instr(DisasContext *dc, uint32_t code,
target/nios2/translate.c:490:static void eret(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:512:static void ret(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:521:static void bret(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:540:static void jmp(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:548:static void nextpc(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:559:static void callr(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:567:static void rdctl(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:612:static void wrctl(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:677:static void wrprs(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:707:static void gen_cmpxx(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:715:static void do_ri_math_logic(DisasContext *dc, uint32_t insn, GenFn2i *fn)
target/nios2/translate.c:721:static void do_rr_math_logic(DisasContext *dc, uint32_t insn, GenFn3 *fn)
target/nios2/translate.c:735:gen_rr_math_logic(add,  add)
target/nios2/translate.c:736:gen_rr_math_logic(sub,  sub)
target/nios2/translate.c:737:gen_rr_math_logic(mul,  mul)
target/nios2/translate.c:739:gen_rr_math_logic(and,  and)
target/nios2/translate.c:740:gen_rr_math_logic(or,   or)
target/nios2/translate.c:741:gen_rr_math_logic(xor,  xor)
target/nios2/translate.c:742:gen_rr_math_logic(nor,  nor)
target/nios2/translate.c:744:gen_ri_math_logic(srai, sari)
target/nios2/translate.c:745:gen_ri_math_logic(srli, shri)
target/nios2/translate.c:746:gen_ri_math_logic(slli, shli)
target/nios2/translate.c:747:gen_ri_math_logic(roli, rotli)
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 4  _(tok 33300+2321, stop=tool_use, forced)_

**Reasoning:** I'm still trying to pin down a few line references in the Arm and Nios2 sources. For the Arm A64 file at line 2222, I'm guessing it's the disas_exc function. The line 6559 in the 32-bit translate file might be a halt or breakpoint handler, but I'm not sure yet.

I'm now recalling that in the 32-bit Arm translator, line 6559 looks like the SVC handler, where semihosting is checked against an immediate value that differs between Thumb and Arm modes. The 8767 reference seems to be a similar semihosting check tied to the Thumb instruction path, though I'm still working out which function it sits in.

I'm now wondering whether line 6559 is actually trans_SVC, since the semihosting check there sits right after an arm_dc_feature condition, which fits that function's layout in the 6.1 source. Line 8767 is a single-line version of the same check, and I'm not sure which function holds it yet.

I'm now weighing whether the 8767 check belongs to trans_SVC or to a separate thumb path, since the M-profile condition in that line points away from the function I'd assumed. I'm still unsure which of the two sites is the SVC handler and which is the other semihosting check.

I'm still going back and forth on whether 6559 is trans_SVC, since its semihosting check sits right after an arm_dc_feature condition, which matches that function's layout. The 8767 site looks like a separate check on the non-M path, and I'm not sure which function holds it, so I'll leave that one open for now.

I'm still going back and forth on whether 6559 is trans_BKPT or trans_SVC, since the lone semihosting condition there doesn't settle it. The 8767 check looks like a single-line version I'd expect to sit later in the file, so I'm leaning toward trans_SVC for that one, but I haven't confirmed it.

I'm still weighing whether line 6559 is trans_BKPT or trans_SVC, and the lone semihosting condition there doesn't settle it. Line 2222 in the A64 file looks like disas_exc, and for the Nios2 site at 821 I'm considering a trap or break handler that checks imm5 against 1.

I'm now leaning toward the Nios2 site at line 821 being the `trap` handler, which checks `instr.imm5 == 1` for semihosting calls.



- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "m68k_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "trap", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "low"}`

**Score (self):** `{"n_pred": 10, "n_truth": 10, "tp": 8, "precision": 0.8, "recall": 0.8, "f1": 0.8000000000000002}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1387+150, stop=tool_use)_

- `find_references(name=semihosting_enabled)` →

```
12 references
semihosting_enabled   55 include/semihosting/semihost.h bool semihosting_enabled(void);
semihosting_enabled 1825 softmmu/vl.c         if (semihosting_enabled() && !semihosting_get_argc()) {
semihosting_enabled 2222 target/arm/translate-a64.c         if (semihosting_enabled() && imm16 == 0xf000) {
semihosting_enabled 1172 target/arm/translate.c     if (semihosting_enabled() &&
semihosting_enabled 6559 target/arm/translate.c         semihosting_enabled() &&
semihosting_enabled 8767 target/arm/translate.c     if (!arm_dc_feature(s, ARM_FEATURE_M) && semihosting_enabled() &&
semihosting_enabled  206 target/m68k/op_helper.c             if (semihosting_enabled()
semihosting_enabled 12090 target/mips/tcg/translate.c     return semihosting_enabled() && sdbbp_code == 1;
semihosting_enabled  821 target/nios2/translate.c     if (semihosting_enabled() && instr.imm5 == 1) {
semihosting_enabled 2369 target/xtensa/translate.c     bool ill = dc->config->hw_version <= 250002 && !semihosting_enabled();
semihosting_enabled 2371 target/xtensa/translate.c     if (ill || !semihosting_enabled()) {
semihosting_enabled 2381 target/xtensa/translate.c     if (semihosting_enabled()) {
```

- `grep(pattern=semihosting_enabled, version=old, max_results=200)` →

```
15 matches
include/semihosting/semihost.h:30:static inline bool semihosting_enabled(void)
include/semihosting/semihost.h:55:bool semihosting_enabled(void);
semihosting/config.c:62:bool semihosting_enabled(void)
softmmu/vl.c:1825:    if (semihosting_enabled() && !semihosting_get_argc()) {
stubs/semihost.c:26:bool semihosting_enabled(void)
target/arm/translate-a64.c:2222:        if (semihosting_enabled() && imm16 == 0xf000) {
target/arm/translate.c:1172:    if (semihosting_enabled() &&
target/arm/translate.c:6559:        semihosting_enabled() &&
target/arm/translate.c:8767:    if (!arm_dc_feature(s, ARM_FEATURE_M) && semihosting_enabled() &&
target/m68k/op_helper.c:206:            if (semihosting_enabled()
target/mips/tcg/translate.c:12090:    return semihosting_enabled() && sdbbp_code == 1;
target/nios2/translate.c:821:    if (semihosting_enabled() && instr.imm5 == 1) {
target/xtensa/translate.c:2369:    bool ill = dc->config->hw_version <= 250002 && !semihosting_enabled();
target/xtensa/translate.c:2371:    if (ill || !semihosting_enabled()) {
target/xtensa/translate.c:2381:    if (semihosting_enabled()) {
```

### Turn 2  _(tok 2654+402, stop=tool_use)_

**Reasoning:** I need to find the enclosing functions, so I'm checking each one in turn.



- `grep(pattern=^[a-z_].*\(|^\{, version=old, path_glob=target/xtensa/translate.c, max_results=400)` →

```
530 matches (showing 200)
target/xtensa/translate.c:99:void xtensa_collect_sr_names(const XtensaConfig *config)
target/xtensa/translate.c:100:{
target/xtensa/translate.c:131:void xtensa_translate_init(void)
target/xtensa/translate.c:132:{
target/xtensa/translate.c:237:void **xtensa_get_regfile_by_name(const char *name, int entries, int bits)
target/xtensa/translate.c:238:{
target/xtensa/translate.c:278:static inline bool option_enabled(DisasContext *dc, int opt)
target/xtensa/translate.c:279:{
target/xtensa/translate.c:283:static void init_sar_tracker(DisasContext *dc)
target/xtensa/translate.c:284:{
target/xtensa/translate.c:290:static void reset_sar_tracker(DisasContext *dc)
target/xtensa/translate.c:291:{
target/xtensa/translate.c:297:static void gen_right_shift_sar(DisasContext *dc, TCGv_i32 sa)
target/xtensa/translate.c:298:{
target/xtensa/translate.c:307:static void gen_left_shift_sar(DisasContext *dc, TCGv_i32 sa)
target/xtensa/translate.c:308:{
target/xtensa/translate.c:319:static void gen_exception(DisasContext *dc, int excp)
target/xtensa/translate.c:320:{
target/xtensa/translate.c:324:static void gen_exception_cause(DisasContext *dc, uint32_t cause)
target/xtensa/translate.c:325:{
target/xtensa/translate.c:334:static void gen_debug_exception(DisasContext *dc, uint32_t cause)
target/xtensa/translate.c:335:{
target/xtensa/translate.c:343:static bool gen_check_privilege(DisasContext *dc)
target/xtensa/translate.c:344:{
target/xtensa/translate.c:355:static bool gen_check_cpenable(DisasContext *dc, uint32_t cp_mask)
target/xtensa/translate.c:356:{
target/xtensa/translate.c:367:static int gen_postprocess(DisasContext *dc, int slot);
target/xtensa/translate.c:369:static void gen_jump_slot(DisasContext *dc, TCGv dest, int slot)
target/xtensa/translate.c:370:{
target/xtensa/translate.c:387:static void gen_jump(DisasContext *dc, TCGv dest)
target/xtensa/translate.c:388:{
target/xtensa/translate.c:392:static int adjust_jump_slot(DisasContext *dc, uint32_t dest, int slot)
target/xtensa/translate.c:393:{
target/xtensa/translate.c:397:static void gen_jumpi(DisasContext *dc, uint32_t dest, int slot)
target/xtensa/translate.c:398:{
target/xtensa/translate.c:403:static void gen_callw_slot(DisasContext *dc, int callinc, TCGv_i32 dest,
target/xtensa/translate.c:405:{
target/xtensa/translate.c:413:static bool gen_check_loop_end(DisasContext *dc, int slot)
target/xtensa/translate.c:414:{
target/xtensa/translate.c:432:static void gen_jumpi_check_loop_end(DisasContext *dc, int slot)
target/xtensa/translate.c:433:{
target/xtensa/translate.c:439:static void gen_brcond(DisasContext *dc, TCGCond cond,
target/xtensa/translate.c:441:{
target/xtensa/translate.c:450:static void gen_brcondi(DisasContext *dc, TCGCond cond,
target/xtensa/translate.c:452:{
target/xtensa/translate.c:456:static uint32_t test_exceptions_sr(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:458:{
target/xtensa/translate.c:462:static uint32_t test_exceptions_ccompare(DisasContext *dc,
target/xtensa/translate.c:465:{
target/xtensa/translate.c:474:static uint32_t test_exceptions_dbreak(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:476:{
target/xtensa/translate.c:491:static uint32_t test_exceptions_ibreak(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:493:{
target/xtensa/translate.c:502:static uint32_t test_exceptions_hpi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:504:{
target/xtensa/translate.c:522:static MemOp gen_load_store_alignment(DisasContext *dc, MemOp mop,
target/xtensa/translate.c:524:{
target/xtensa/translate.c:538:static bool gen_window_check(DisasContext *dc, uint32_t mask)
target/xtensa/translate.c:539:{
target/xtensa/translate.c:553:static TCGv_i32 gen_mac16_m(TCGv_i32 v, bool hi, bool is_unsigned)
target/xtensa/translate.c:554:{
target/xtensa/translate.c:565:static void gen_zero_check(DisasContext *dc, const OpcodeArg arg[])
target/xtensa/translate.c:566:{
target/xtensa/translate.c:574:static inline unsigned xtensa_op0_insn_len(DisasContext *dc, uint8_t op0)
target/xtensa/translate.c:575:{
target/xtensa/translate.c:579:static int gen_postprocess(DisasContext *dc, int slot)
target/xtensa/translate.c:580:{
target/xtensa/translate.c:627:static uint32_t encode_resource(enum resource_type r, unsigned g, unsigned n)
target/xtensa/translate.c:628:{
target/xtensa/translate.c:633:static enum resource_type get_resource_type(uint32_t resource)
target/xtensa/translate.c:634:{
target/xtensa/translate.c:642:static bool op_depends_on(const struct slot_prop *a,
target/xtensa/translate.c:644:{
target/xtensa/translate.c:673:static bool break_dependency(struct slot_prop *a,
target/xtensa/translate.c:677:{
target/xtensa/translate.c:719:static bool tsort(struct slot_prop *slot,
target/xtensa/translate.c:724:{
target/xtensa/translate.c:804:static void opcode_add_resource(struct slot_prop *op,
target/xtensa/translate.c:807:{
target/xtensa/translate.c:829:static int resource_compare(const void *a, const void *b)
target/xtensa/translate.c:830:{
target/xtensa/translate.c:838:static int arg_copy_compare(const void *a, const void *b)
target/xtensa/translate.c:839:{
target/xtensa/translate.c:847:static void disas_xtensa_insn(CPUXtensaState *env, DisasContext *dc)
target/xtensa/translate.c:848:{
target/xtensa/translate.c:1139:static inline unsigned xtensa_insn_len(CPUXtensaState *env, DisasContext *dc)
target/xtensa/translate.c:1140:{
target/xtensa/translate.c:1145:static void gen_ibreak_check(CPUXtensaState *env, DisasContext *dc)
target/xtensa/translate.c:1146:{
target/xtensa/translate.c:1158:static void xtensa_tr_init_disas_context(DisasContextBase *dcbase,
target/xtensa/translate.c:1160:{
target/xtensa/translate.c:1185:static void xtensa_tr_tb_start(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1186:{
target/xtensa/translate.c:1194:static void xtensa_tr_insn_start(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1195:{
target/xtensa/translate.c:1199:static void xtensa_tr_translate_insn(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1200:{
target/xtensa/translate.c:1246:static void xtensa_tr_tb_stop(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1247:{
target/xtensa/translate.c:1266:static void xtensa_tr_disas_log(const DisasContextBase *dcbase,
target/xtensa/translate.c:1268:{
target/xtensa/translate.c:1282:void gen_intermediate_code(CPUState *cpu, TranslationBlock *tb, int max_insns,
target/xtensa/translate.c:1284:{
target/xtensa/translate.c:1290:void xtensa_cpu_dump_state(CPUState *cs, FILE *f, int flags)
target/xtensa/translate.c:1291:{
target/xtensa/translate.c:1358:void restore_state_to_opc(CPUXtensaState *env, TranslationBlock *tb,
target/xtensa/translate.c:1360:{
target/xtensa/translate.c:1364:static void translate_abs(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1366:{
target/xtensa/translate.c:1370:static void translate_add(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1372:{
target/xtensa/translate.c:1376:static void translate_addi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1378:{
target/xtensa/translate.c:1382:static void translate_addx(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1384:{
target/xtensa/translate.c:1391:static void translate_all(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1393:{
target/xtensa/translate.c:1411:static void translate_and(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1413:{
target/xtensa/translate.c:1417:static void translate_ball(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1419:{
target/xtensa/translate.c:1426:static void translate_bany(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1428:{
target/xtensa/translate.c:1435:static void translate_b(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1437:{
target/xtensa/translate.c:1441:static void translate_bb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1443:{
target/xtensa/translate.c:1462:static void translate_bbi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1464:{
target/xtensa/translate.c:1475:static void translate_bi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1477:{
target/xtensa/translate.c:1481:static void translate_bz(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1483:{
target/xtensa/translate.c:1495:static void translate_boolean(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1497:{
target/xtensa/translate.c:1517:static void translate_bp(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1519:{
target/xtensa/translate.c:1527:static void translate_call0(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1529:{
target/xtensa/translate.c:1534:static void translate_callw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1536:{
target/xtensa/translate.c:1542:static void translate_callx0(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1544:{
target/xtensa/translate.c:1552:static void translate_callxw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1554:{
target/xtensa/translate.c:1562:static void translate_clamps(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1564:{
target/xtensa/translate.c:1574:static void translate_clrb_expstate(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1576:{
target/xtensa/translate.c:1581:static void translate_clrex(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1583:{
target/xtensa/translate.c:1587:static void translate_const16(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1589:{
target/xtensa/translate.c:1596:static void translate_dcache(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1598:{
target/xtensa/translate.c:1608:static void translate_depbits(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1610:{
target/xtensa/translate.c:1615:static void translate_diwbuip(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1617:{
target/xtensa/translate.c:1621:static uint32_t test_exceptions_entry(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1623:{
target/xtensa/translate.c:1633:static uint32_t test_overflow_entry(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1635:{
target/xtensa/translate.c:1639:static void translate_entry(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1641:{
target/xtensa/translate.c:1648:static void translate_extui(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1650:{
target/xtensa/translate.c:1659:static void translate_getex(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1661:{
target/xtensa/translate.c:1670:static void translate_icache(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1672:{
target/xtensa/translate.c:1683:static void translate_itlb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1685:{
target/xtensa/translate.c:1693:static void translate_j(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1695:{
target/xtensa/translate.c:1699:static void translate_jx(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1701:{
target/xtensa/translate.c:1705:static void translate_l32e(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1707:{
target/xtensa/translate.c:1718:static void gen_check_exclusive(DisasContext *dc, TCGv_i32 addr, bool is_write)
target/xtensa/translate.c:1719:{
target/xtensa/translate.c:1722:static void gen_check_exclusive(DisasContext *dc, TCGv_i32 addr, bool is_write)
target/xtensa/translate.c:1723:{
target/xtensa/translate.c:1733:static void translate_l32ex(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1735:{
target/xtensa/translate.c:1748:static void translate_ldst(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1750:{
target/xtensa/translate.c:1771:static void translate_lct(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1773:{
target/xtensa/translate.c:1777:static void translate_l32r(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1779:{
target/xtensa/translate.c:1792:static void translate_loop(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1794:{
target/xtensa/translate.c:1829:static void translate_mac16(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1831:{
target/xtensa/translate.c:1890:static void translate_memw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1892:{
target/xtensa/translate.c:1896:static void translate_smin(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1898:{
target/xtensa/translate.c:1902:static void translate_umin(DisasContext *dc, const OpcodeArg arg[],
```

- `read_file(path=target/arm/translate.c, version=old, start_line=1160, end_line=1175)` →

```
target/arm/translate.c lines 1160-1175 of 9927
 1160|     /* HLT. This has two purposes.
 1161|      * Architecturally, it is an external halting debug instruction.
 1162|      * Since QEMU doesn't implement external debug, we treat this as
 1163|      * it is required for halting debug disabled: it will UNDEF.
 1164|      * Secondly, "HLT 0x3C" is a T32 semihosting trap instruction,
 1165|      * and "HLT 0xF000" is an A32 semihosting syscall. These traps
 1166|      * must trigger semihosting even for ARMv7 and earlier, where
 1167|      * HLT was an undefined encoding.
 1168|      * In system mode, we don't allow userspace access to
 1169|      * semihosting, to provide some semblance of security
 1170|      * (and for consistency with our 32-bit semihosting).
 1171|      */
 1172|     if (semihosting_enabled() &&
 1173| #ifndef CONFIG_USER_ONLY
 1174|         s->current_el != 0 &&
 1175| #endif
```

- `read_file(path=target/mips/tcg/translate.c, version=old, start_line=12080, end_line=12092)` →

```
target/mips/tcg/translate.c lines 12080-12092 of 16247
12080|     gen_helper_cache(cpu_env, t1, t0);
12081|     tcg_temp_free(t1);
12082|     tcg_temp_free_i32(t0);
12083| }
12084| 
12085| static inline bool is_uhi(int sdbbp_code)
12086| {
12087| #ifdef CONFIG_USER_ONLY
12088|     return false;
12089| #else
12090|     return semihosting_enabled() && sdbbp_code == 1;
12091| #endif
12092| }
```

### Turn 3  _(tok 9934+750, stop=tool_use)_

**Says:** Need enclosing functions for the others.

- `read_file(path=target/xtensa/translate.c, version=old, start_line=2360, end_line=2385)` →

```
target/xtensa/translate.c lines 2360-2385 of 7852
 2360| 
 2361| static uint32_t test_exceptions_simcall(DisasContext *dc,
 2362|                                         const OpcodeArg arg[],
 2363|                                         const uint32_t par[])
 2364| {
 2365| #ifdef CONFIG_USER_ONLY
 2366|     bool ill = true;
 2367| #else
 2368|     /* Between RE.2 and RE.3 simcall opcode's become nop for the hardware. */
 2369|     bool ill = dc->config->hw_version <= 250002 && !semihosting_enabled();
 2370| #endif
 2371|     if (ill || !semihosting_enabled()) {
 2372|         qemu_log_mask(LOG_GUEST_ERROR, "SIMCALL but semihosting is disabled\n");
 2373|     }
 2374|     return ill ? XTENSA_OP_ILL : 0;
 2375| }
 2376| 
 2377| static void translate_simcall(DisasContext *dc, const OpcodeArg arg[],
 2378|                               const uint32_t par[])
 2379| {
 2380| #ifndef CONFIG_USER_ONLY
 2381|     if (semihosting_enabled()) {
 2382|         gen_helper_simcall(cpu_env);
 2383|     }
 2384| #endif
 2385| }
```

- `grep(pattern=^[a-z_].*\(, version=old, path_glob=target/arm/translate.c, max_results=400)` →

```
475 matches (showing 200)
target/arm/translate.c:69:void arm_translate_init(void)
target/arm/translate.c:91:uint64_t asimd_imm_const(uint32_t imm, int cmode, int op)
target/arm/translate.c:162:void arm_gen_condlabel(DisasContext *s)
target/arm/translate.c:186:void store_cpu_offset(TCGv_i32 var, int offset, int size)
target/arm/translate.c:202:static void disas_set_da_iss(DisasContext *s, MemOp memop, ISSInfo issinfo)
target/arm/translate.c:232:static inline int get_a32_user_mem_index(DisasContext *s)
target/arm/translate.c:268:static uint32_t read_pc(DisasContext *s)
target/arm/translate.c:274:void load_reg_var(DisasContext *s, TCGv_i32 var, int reg)
target/arm/translate.c:302:void store_reg(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:327:static void store_sp_checked(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:346:void gen_set_cpsr(TCGv_i32 var, uint32_t mask)
target/arm/translate.c:351:static void gen_rebuild_hflags(DisasContext *s, bool new_el)
target/arm/translate.c:371:static void gen_exception_internal(int excp)
target/arm/translate.c:377:static void gen_singlestep_exception(DisasContext *s)
target/arm/translate.c:393:void clear_eci_state(DisasContext *s)
target/arm/translate.c:405:static void gen_smul_dual(TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:421:void gen_rev16(TCGv_i32 dest, TCGv_i32 var)
target/arm/translate.c:434:static void gen_revsh(TCGv_i32 dest, TCGv_i32 var)
target/arm/translate.c:446:static void gen_add16(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:459:static inline void gen_logic_CC(TCGv_i32 var)
target/arm/translate.c:466:static void gen_add_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:473:static void gen_sub_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:481:static void gen_add_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:495:static void gen_adc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:523:static void gen_sub_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:538:static void gen_sbc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:547:static void gen_##name(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)       \
target/arm/translate.c:563:static void gen_sar(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:573:static void shifter_out_im(TCGv_i32 var, int shift)
target/arm/translate.c:579:static inline void gen_arm_shift_im(TCGv_i32 var, int shiftop,
target/arm/translate.c:628:static inline void gen_arm_shift_reg(TCGv_i32 var, int shiftop,
target/arm/translate.c:660:void arm_test_cc(DisasCompare *cmp, int cc)
target/arm/translate.c:746:void arm_free_cc(DisasCompare *cmp)
target/arm/translate.c:753:void arm_jump_cc(DisasCompare *cmp, TCGLabel *label)
target/arm/translate.c:758:void arm_gen_test_cc(int cc, TCGLabel *label)
target/arm/translate.c:766:void gen_set_condexec(DisasContext *s)
target/arm/translate.c:775:void gen_set_pc_im(DisasContext *s, target_ulong val)
target/arm/translate.c:781:static inline void gen_bx(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:811:static inline void gen_bx_excret(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:825:static inline void gen_bx_excret_final_code(DisasContext *s)
target/arm/translate.c:863:static inline void gen_bxns(DisasContext *s, int rm)
target/arm/translate.c:882:static inline void gen_blxns(DisasContext *s, int rm)
target/arm/translate.c:899:static inline void store_reg_bx(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:912:static inline void store_reg_from_load(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:951:static TCGv gen_aa32_addr(DisasContext *s, TCGv_i32 a32, MemOp op)
target/arm/translate.c:967:void gen_aa32_ld_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:975:void gen_aa32_st_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:983:void gen_aa32_ld_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:997:void gen_aa32_st_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:1014:void gen_aa32_ld_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1020:void gen_aa32_st_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1026:void gen_aa32_ld_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1032:void gen_aa32_st_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1052:static inline void gen_hvc(DisasContext *s, int imm16)
target/arm/translate.c:1070:static inline void gen_smc(DisasContext *s)
target/arm/translate.c:1081:static void gen_exception_internal_insn(DisasContext *s, uint32_t pc, int excp)
target/arm/translate.c:1089:static void gen_exception_el_v(int excp, uint32_t syndrome, TCGv_i32 tcg_el)
target/arm/translate.c:1095:static void gen_exception_el(int excp, uint32_t syndrome, uint32_t target_el)
target/arm/translate.c:1100:static void gen_exception(int excp, uint32_t syndrome)
target/arm/translate.c:1106:static void gen_exception_insn_el_v(DisasContext *s, uint64_t pc, int excp,
target/arm/translate.c:1119:void gen_exception_insn_el(DisasContext *s, uint64_t pc, int excp,
target/arm/translate.c:1125:void gen_exception_insn(DisasContext *s, uint64_t pc, int excp, uint32_t syn)
target/arm/translate.c:1137:static void gen_exception_bkpt_insn(DisasContext *s, uint32_t syn)
target/arm/translate.c:1145:void unallocated_encoding(DisasContext *s)
target/arm/translate.c:1152:void gen_lookup_tb(DisasContext *s)
target/arm/translate.c:1158:static inline void gen_hlt(DisasContext *s, int imm)
target/arm/translate.c:1187:long neon_full_reg_offset(unsigned reg)
target/arm/translate.c:1196:long neon_element_offset(int reg, int element, MemOp memop)
target/arm/translate.c:1213:long vfp_reg_offset(bool dp, unsigned reg)
target/arm/translate.c:1222:void read_neon_element32(TCGv_i32 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1248:void read_neon_element64(TCGv_i64 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1267:void write_neon_element32(TCGv_i32 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1286:void write_neon_element64(TCGv_i64 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1304:static inline void iwmmxt_load_reg(TCGv_i64 var, int reg)
target/arm/translate.c:1309:static inline void iwmmxt_store_reg(TCGv_i64 var, int reg)
target/arm/translate.c:1314:static inline TCGv_i32 iwmmxt_load_creg(int reg)
target/arm/translate.c:1321:static inline void iwmmxt_store_creg(int reg, TCGv_i32 var)
target/arm/translate.c:1327:static inline void gen_op_iwmmxt_movq_wRn_M0(int rn)
target/arm/translate.c:1332:static inline void gen_op_iwmmxt_movq_M0_wRn(int rn)
target/arm/translate.c:1337:static inline void gen_op_iwmmxt_orq_M0_wRn(int rn)
target/arm/translate.c:1343:static inline void gen_op_iwmmxt_andq_M0_wRn(int rn)
target/arm/translate.c:1349:static inline void gen_op_iwmmxt_xorq_M0_wRn(int rn)
target/arm/translate.c:1356:static inline void gen_op_iwmmxt_##name##_M0_wRn(int rn) \
target/arm/translate.c:1363:static inline void gen_op_iwmmxt_##name##_M0_wRn(int rn) \
target/arm/translate.c:1375:static inline void gen_op_iwmmxt_##name##_M0(void) \
target/arm/translate.c:1435:static void gen_op_iwmmxt_set_mup(void)
target/arm/translate.c:1443:static void gen_op_iwmmxt_set_cup(void)
target/arm/translate.c:1451:static void gen_op_iwmmxt_setpsr_nz(void)
target/arm/translate.c:1458:static inline void gen_op_iwmmxt_addl_M0_wRn(int rn)
target/arm/translate.c:1465:static inline int gen_iwmmxt_address(DisasContext *s, uint32_t insn,
target/arm/translate.c:1500:static inline int gen_iwmmxt_shift(uint32_t insn, uint32_t mask, TCGv_i32 dest)
target/arm/translate.c:1524:static int disas_iwmmxt_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:2524:static int disas_dsp_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:2591:static void gen_goto_ptr(void)
target/arm/translate.c:2600:static void gen_goto_tb(DisasContext *s, int n, target_ulong dest)
target/arm/translate.c:2614:static inline void gen_jmp_tb(DisasContext *s, uint32_t dest, int tbno)
target/arm/translate.c:2657:static inline void gen_jmp(DisasContext *s, uint32_t dest)
target/arm/translate.c:2662:static inline void gen_mulxy(TCGv_i32 t0, TCGv_i32 t1, int x, int y)
target/arm/translate.c:2676:static uint32_t msr_mask(DisasContext *s, int flags, int spsr)
target/arm/translate.c:2709:static int gen_set_psr(DisasContext *s, uint32_t mask, int spsr, TCGv_i32 t0)
target/arm/translate.c:2731:static int gen_set_psr_im(DisasContext *s, uint32_t mask, int spsr, uint32_t val)
target/arm/translate.c:2739:static bool msr_banked_access_decode(DisasContext *s, int r, int sysm, int rn,
target/arm/translate.c:2901:static void gen_msr_banked(DisasContext *s, int r, int sysm, int rn)
target/arm/translate.c:2921:static void gen_mrs_banked(DisasContext *s, int r, int sysm, int rn)
target/arm/translate.c:2945:static void store_pc_exc_ret(DisasContext *s, TCGv_i32 pc)
target/arm/translate.c:2952:static void gen_rfe(DisasContext *s, TCGv_i32 pc, TCGv_i32 cpsr)
target/arm/translate.c:2969:static void gen_exception_return(DisasContext *s, TCGv_i32 pc)
target/arm/translate.c:2974:static void gen_gvec_fn3_qc(uint32_t rd_ofs, uint32_t rn_ofs, uint32_t rm_ofs,
target/arm/translate.c:2986:void gen_gvec_sqrdmlah_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:2996:void gen_gvec_sqrdmlsh_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3059:static void gen_ssra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3065:static void gen_ssra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3071:static void gen_ssra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3077:static void gen_ssra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3083:static void gen_ssra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3089:void gen_gvec_ssra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3135:static void gen_usra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3141:static void gen_usra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3147:static void gen_usra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3153:static void gen_usra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3159:static void gen_usra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3165:void gen_gvec_usra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3221:static void gen_srshr8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3232:static void gen_srshr16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3243:static void gen_srshr32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3259:static void gen_srshr64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3269:static void gen_srshr_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3284:void gen_gvec_srshr(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3331:static void gen_srsra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3340:static void gen_srsra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3349:static void gen_srsra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3358:static void gen_srsra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3367:static void gen_srsra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3376:void gen_gvec_srsra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3428:static void gen_urshr8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3439:static void gen_urshr16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3450:static void gen_urshr32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3466:static void gen_urshr64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3476:static void gen_urshr_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t shift)
target/arm/translate.c:3491:void gen_gvec_urshr(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3537:static void gen_ursra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3550:static void gen_ursra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3563:static void gen_ursra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3576:static void gen_ursra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3589:static void gen_ursra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3602:void gen_gvec_ursra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3643:static void gen_shr8_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3655:static void gen_shr16_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3667:static void gen_shr32_ins_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3673:static void gen_shr64_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3679:static void gen_shr_ins_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3693:void gen_gvec_sri(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3738:static void gen_shl8_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3750:static void gen_shl16_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3762:static void gen_shl32_ins_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3767:static void gen_shl64_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3772:static void gen_shl_ins_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3786:void gen_gvec_sli(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3829:static void gen_mla8_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3835:static void gen_mls8_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3841:static void gen_mla16_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3847:static void gen_mls16_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3853:static void gen_mla32_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3859:static void gen_mls32_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3865:static void gen_mla64_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3871:static void gen_mls64_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3877:static void gen_mla_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3883:static void gen_mls_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3892:void gen_gvec_mla(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3924:void gen_gvec_mls(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3957:static void gen_cmtst_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3964:void gen_cmtst_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3971:static void gen_cmtst_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3978:void gen_gvec_cmtst(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4004:void gen_ushl_i32(TCGv_i32 dst, TCGv_i32 src, TCGv_i32 shift)
target/arm/translate.c:4031:void gen_ushl_i64(TCGv_i64 dst, TCGv_i64 src, TCGv_i64 shift)
target/arm/translate.c:4058:static void gen_ushl_vec(unsigned vece, TCGv_vec dst,
target/arm/translate.c:4116:void gen_gvec_ushl(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4144:void gen_sshl_i32(TCGv_i32 dst, TCGv_i32 src, TCGv_i32 shift)
target/arm/translate.c:4172:void gen_sshl_i64(TCGv_i64 dst, TCGv_i64 src, TCGv_i64 shift)
target/arm/translate.c:4200:static void gen_sshl_vec(unsigned vece, TCGv_vec dst,
target/arm/translate.c:4250:void gen_gvec_sshl(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4278:static void gen_uqadd_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4289:void gen_gvec_uqadd_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4321:static void gen_sqadd_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4332:void gen_gvec_sqadd_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4364:static void gen_uqsub_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4375:void gen_gvec_uqsub_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4407:static void gen_sqsub_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4418:void gen_gvec_sqsub_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4450:static void gen_sabd_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4460:static void gen_sabd_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:4470:static void gen_sabd_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:4480:void gen_gvec_sabd(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4510:static void gen_uabd_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4520:static void gen_uabd_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:4530:static void gen_uabd_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:4540:void gen_gvec_uabd(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4570:static void gen_saba_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4578:static void gen_saba_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
```

- `grep(pattern=^[a-z_].*\(, version=old, path_glob=target/arm/translate-a64.c, max_results=400)` →

```
248 matches (showing 200)
target/arm/translate-a64.c:62:typedef void AArch64DecodeFn(DisasContext *s, uint32_t insn);
target/arm/translate-a64.c:71:void a64_translate_init(void)
target/arm/translate-a64.c:91:static int get_a64_user_mem_index(DisasContext *s)
target/arm/translate-a64.c:129:static void set_btype_raw(int val)
target/arm/translate-a64.c:135:static void set_btype(DisasContext *s, int val)
target/arm/translate-a64.c:143:static void reset_btype(DisasContext *s)
target/arm/translate-a64.c:151:void gen_a64_set_pc_im(uint64_t val)
target/arm/translate-a64.c:169:static void gen_top_byte_ignore(DisasContext *s, TCGv_i64 dst,
target/arm/translate-a64.c:200:static void gen_a64_set_pc(DisasContext *s, TCGv_i64 src)
target/arm/translate-a64.c:233:static void gen_address_with_allocation_tag0(TCGv_i64 dst, TCGv_i64 src)
target/arm/translate-a64.c:238:static void gen_probe_access(DisasContext *s, TCGv_i64 ptr,
target/arm/translate-a64.c:253:static TCGv_i64 gen_mte_check1_mmuidx(DisasContext *s, TCGv_i64 addr,
target/arm/translate-a64.c:312:static void a64_test_cc(DisasCompare64 *c64, int cc)
target/arm/translate-a64.c:327:static void a64_free_cc(DisasCompare64 *c64)
target/arm/translate-a64.c:332:static void gen_rebuild_hflags(DisasContext *s)
target/arm/translate-a64.c:337:static void gen_exception_internal(int excp)
target/arm/translate-a64.c:343:static void gen_exception_internal_insn(DisasContext *s, uint64_t pc, int excp)
target/arm/translate-a64.c:350:static void gen_exception_bkpt_insn(DisasContext *s, uint32_t syndrome)
target/arm/translate-a64.c:357:static void gen_step_complete_exception(DisasContext *s)
target/arm/translate-a64.c:373:static inline bool use_goto_tb(DisasContext *s, uint64_t dest)
target/arm/translate-a64.c:381:static inline void gen_goto_tb(DisasContext *s, int n, uint64_t dest)
target/arm/translate-a64.c:399:static void init_tmp_a64_array(DisasContext *s)
target/arm/translate-a64.c:407:static void free_tmp_a64(DisasContext *s)
target/arm/translate-a64.c:500:static inline int fp_reg_offset(DisasContext *s, int regno, MemOp size)
target/arm/translate-a64.c:506:static inline int fp_reg_hi_offset(DisasContext *s, int regno)
target/arm/translate-a64.c:517:static TCGv_i64 read_fp_dreg(DisasContext *s, int reg)
target/arm/translate-a64.c:525:static TCGv_i32 read_fp_sreg(DisasContext *s, int reg)
target/arm/translate-a64.c:533:static TCGv_i32 read_fp_hreg(DisasContext *s, int reg)
target/arm/translate-a64.c:544:static void clear_vec_high(DisasContext *s, bool is_q, int rd)
target/arm/translate-a64.c:553:void write_fp_dreg(DisasContext *s, int reg, TCGv_i64 v)
target/arm/translate-a64.c:561:static void write_fp_sreg(DisasContext *s, int reg, TCGv_i32 v)
target/arm/translate-a64.c:571:static void gen_gvec_fn2(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:581:static void gen_gvec_fn2i(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:589:static void gen_gvec_fn3(DisasContext *s, bool is_q, int rd, int rn, int rm,
target/arm/translate-a64.c:597:static void gen_gvec_fn4(DisasContext *s, bool is_q, int rd, int rn, int rm,
target/arm/translate-a64.c:606:static void gen_gvec_op2_ool(DisasContext *s, bool is_q, int rd,
target/arm/translate-a64.c:615:static void gen_gvec_op3_ool(DisasContext *s, bool is_q, int rd,
target/arm/translate-a64.c:627:static void gen_gvec_op3_fpst(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:640:static void gen_gvec_op3_qc(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:654:static void gen_gvec_op4_ool(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:668:static void gen_gvec_op4_fpst(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:684:static inline void gen_set_NZ64(TCGv_i64 result)
target/arm/translate-a64.c:691:static inline void gen_logic_CC(int sf, TCGv_i64 result)
target/arm/translate-a64.c:704:static void gen_add_CC(int sf, TCGv_i64 dest, TCGv_i64 t0, TCGv_i64 t1)
target/arm/translate-a64.c:751:static void gen_sub_CC(int sf, TCGv_i64 dest, TCGv_i64 t0, TCGv_i64 t1)
target/arm/translate-a64.c:798:static void gen_adc(int sf, TCGv_i64 dest, TCGv_i64 t0, TCGv_i64 t1)
target/arm/translate-a64.c:812:static void gen_adc_CC(int sf, TCGv_i64 dest, TCGv_i64 t0, TCGv_i64 t1)
target/arm/translate-a64.c:868:static void do_gpr_st_memidx(DisasContext *s, TCGv_i64 source,
target/arm/translate-a64.c:891:static void do_gpr_st(DisasContext *s, TCGv_i64 source,
target/arm/translate-a64.c:904:static void do_gpr_ld_memidx(DisasContext *s, TCGv_i64 dest, TCGv_i64 tcg_addr,
target/arm/translate-a64.c:931:static void do_gpr_ld(DisasContext *s, TCGv_i64 dest, TCGv_i64 tcg_addr,
target/arm/translate-a64.c:943:static void do_fp_st(DisasContext *s, int srcidx, TCGv_i64 tcg_addr, int size)
target/arm/translate-a64.c:978:static void do_fp_ld(DisasContext *s, int destidx, TCGv_i64 tcg_addr, int size)
target/arm/translate-a64.c:1027:static void read_vec_element(DisasContext *s, TCGv_i64 tcg_dest, int srcidx,
target/arm/translate-a64.c:1059:static void read_vec_element_i32(DisasContext *s, TCGv_i32 tcg_dest, int srcidx,
target/arm/translate-a64.c:1086:static void write_vec_element(DisasContext *s, TCGv_i64 tcg_src, int destidx,
target/arm/translate-a64.c:1108:static void write_vec_element_i32(DisasContext *s, TCGv_i32 tcg_src,
target/arm/translate-a64.c:1128:static void do_vec_st(DisasContext *s, int srcidx, int element,
target/arm/translate-a64.c:1140:static void do_vec_ld(DisasContext *s, int destidx, int element,
target/arm/translate-a64.c:1158:static bool fp_access_check_only(DisasContext *s)
target/arm/translate-a64.c:1173:static bool fp_access_check(DisasContext *s)
target/arm/translate-a64.c:1191:bool sve_access_check(DisasContext *s)
target/arm/translate-a64.c:1218:static bool sme_access_check(DisasContext *s)
target/arm/translate-a64.c:1230:bool sme_enabled_check(DisasContext *s)
target/arm/translate-a64.c:1245:bool sme_enabled_check_with_svcr(DisasContext *s, unsigned req)
target/arm/translate-a64.c:1268:static void ext_and_shift_reg(TCGv_i64 tcg_out, TCGv_i64 tcg_in,
target/arm/translate-a64.c:1311:static inline void gen_check_sp_alignment(DisasContext *s)
target/arm/translate-a64.c:1335:static inline AArch64DecodeFn *lookup_disas_fn(const AArch64DecodeTable *table,
target/arm/translate-a64.c:1363:static void disas_uncond_b_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:1383:static void disas_comp_b_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:1413:static void disas_test_b_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:1444:static void disas_cond_b_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:1471:static void handle_hint(DisasContext *s, uint32_t insn,
target/arm/translate-a64.c:1599:static void gen_clrex(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:1605:static void handle_sync(DisasContext *s, uint32_t insn,
target/arm/translate-a64.c:1662:static void gen_xaflag(void)
target/arm/translate-a64.c:1692:static void gen_axflag(void)
target/arm/translate-a64.c:1705:static void handle_msr_i(DisasContext *s, uint32_t insn,
target/arm/translate-a64.c:1853:static void gen_get_nzcv(TCGv_i64 tcg_rt)
target/arm/translate-a64.c:1875:static void gen_set_nzcv(TCGv_i64 tcg_rt)
target/arm/translate-a64.c:1896:static void gen_sysreg_undef(DisasContext *s, bool isread,
target/arm/translate-a64.c:1926:static void handle_sys(DisasContext *s, uint32_t insn, bool isread,
target/arm/translate-a64.c:2112:static void disas_system(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:2154:static void disas_exc(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:2258:static void disas_uncond_b_reg(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:2443:static void disas_b_exc_sys(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:2490:static void gen_load_exclusive(DisasContext *s, int rt, int rt2,
target/arm/translate-a64.c:2533:static void gen_store_exclusive(DisasContext *s, int rd, int rt, int rt2,
target/arm/translate-a64.c:2610:static void gen_compare_and_swap(DisasContext *s, int rs, int rt,
target/arm/translate-a64.c:2626:static void gen_compare_and_swap_pair(DisasContext *s, int rs, int rt,
target/arm/translate-a64.c:2718:static bool disas_ldst_compute_iss_sf(int size, bool is_signed, int opc)
target/arm/translate-a64.c:2744:static void disas_ldst_excl(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:2892:static void disas_ld_lit(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:2962:static void disas_ldst_pair(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:3128:static void disas_ldst_reg_imm9(DisasContext *s, uint32_t insn,
target/arm/translate-a64.c:3260:static void disas_ldst_reg_roffset(DisasContext *s, uint32_t insn,
target/arm/translate-a64.c:3352:static void disas_ldst_reg_unsigned_imm(DisasContext *s, uint32_t insn,
target/arm/translate-a64.c:3433:static void disas_ldst_atomic(DisasContext *s, uint32_t insn,
target/arm/translate-a64.c:3542:static void disas_ldst_pac(DisasContext *s, uint32_t insn,
target/arm/translate-a64.c:3604:static void disas_ldst_ldapr_stlr(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:3676:static void disas_ldst_reg(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:3730:static void disas_ldst_multiple_struct(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:3901:static void disas_ldst_single_struct(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4024:static void disas_ldst_tag(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4219:static void disas_ldst(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4263:static void disas_pc_rel_adr(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4298:static void disas_add_sub_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4351:static void disas_add_sub_imm_with_tags(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4390:static uint64_t bitfield_replicate(uint64_t mask, unsigned int e)
target/arm/translate-a64.c:4401:static inline uint64_t bitmask64(unsigned int length)
target/arm/translate-a64.c:4412:bool logic_imm_decode_wmask(uint64_t *result, unsigned int immn,
target/arm/translate-a64.c:4479:static void disas_logic_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4557:static void disas_movw_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4601:static void disas_bitfield(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4679:static void disas_extract(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4736:static void disas_data_proc_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4771:static void shift_reg(TCGv_i64 dst, TCGv_i64 src, int sf,
target/arm/translate-a64.c:4816:static void shift_reg_imm(TCGv_i64 dst, TCGv_i64 src, int sf,
target/arm/translate-a64.c:4834:static void disas_logic_reg(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:4935:static void disas_add_sub_ext_reg(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:5006:static void disas_add_sub_reg(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:5063:static void disas_data_proc_3src(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:5161:static void disas_adc_sbc(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:5197:static void disas_rotate_right_into_flags(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:5242:static void disas_evaluate_into_flags(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:5275:static void disas_cc(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:5379:static void disas_cond_select(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:5429:static void handle_clz(DisasContext *s, unsigned int sf,
target/arm/translate-a64.c:5447:static void handle_cls(DisasContext *s, unsigned int sf,
target/arm/translate-a64.c:5465:static void handle_rbit(DisasContext *s, unsigned int sf,
target/arm/translate-a64.c:5484:static void handle_rev64(DisasContext *s, unsigned int sf,
target/arm/translate-a64.c:5497:static void handle_rev32(DisasContext *s, unsigned int sf,
target/arm/translate-a64.c:5512:static void handle_rev16(DisasContext *s, unsigned int sf,
target/arm/translate-a64.c:5535:static void disas_data_proc_1src(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:5730:static void handle_div(DisasContext *s, bool is_signed, unsigned int sf,
target/arm/translate-a64.c:5758:static void handle_shift_reg(DisasContext *s,
target/arm/translate-a64.c:5772:static void handle_crc32(DisasContext *s,
target/arm/translate-a64.c:5823:static void disas_data_proc_2src(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:5936:static void disas_data_proc_reg(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:6009:static void handle_fp_compare(DisasContext *s, int size,
target/arm/translate-a64.c:6079:static void disas_fp_compare(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:6128:static void disas_fp_ccomp(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:6192:static void disas_fp_csel(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:6252:static void handle_fp_1src_half(DisasContext *s, int opcode, int rd, int rn)
target/arm/translate-a64.c:6310:static void handle_fp_1src_single(DisasContext *s, int opcode, int rd, int rn)
target/arm/translate-a64.c:6387:static void handle_fp_1src_double(DisasContext *s, int opcode, int rd, int rn)
target/arm/translate-a64.c:6463:static void handle_fp_fcvt(DisasContext *s, int opcode,
target/arm/translate-a64.c:6548:static void disas_fp_1src(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:6637:static void handle_fp_2src_single(DisasContext *s, int opcode,
target/arm/translate-a64.c:6690:static void handle_fp_2src_double(DisasContext *s, int opcode,
target/arm/translate-a64.c:6743:static void handle_fp_2src_half(DisasContext *s, int opcode,
target/arm/translate-a64.c:6803:static void disas_fp_2src(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:6846:static void handle_fp_3src_single(DisasContext *s, bool o0, bool o1,
target/arm/translate-a64.c:6884:static void handle_fp_3src_double(DisasContext *s, bool o0, bool o1,
target/arm/translate-a64.c:6922:static void handle_fp_3src_half(DisasContext *s, bool o0, bool o1,
target/arm/translate-a64.c:6965:static void disas_fp_3src(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:7015:static void disas_fp_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:7061:static void handle_fpfpcvt(DisasContext *s, int rd, int rn, int opcode,
target/arm/translate-a64.c:7238:static void disas_fp_fixed_conv(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:7290:static void handle_fmov(DisasContext *s, int rd, int rn, int type, bool itof)
target/arm/translate-a64.c:7353:static void handle_fjcvtzs(DisasContext *s, int rd, int rn)
target/arm/translate-a64.c:7377:static void disas_fp_int_conv(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:7469:static void disas_data_proc_fp(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:7518:static void do_ext64(DisasContext *s, TCGv_i64 tcg_left, TCGv_i64 tcg_right,
target/arm/translate-a64.c:7543:static void disas_simd_ext(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:7618:static void disas_simd_tb(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:7650:static void disas_simd_zip_trn(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:7747:static TCGv_i32 do_reduction_op(DisasContext *s, int fpopcode, int rn,
target/arm/translate-a64.c:7815:static void disas_simd_across_lanes(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:7973:static void handle_simd_dupe(DisasContext *s, int is_q, int rd, int rn,
target/arm/translate-a64.c:8000:static void handle_simd_dupes(DisasContext *s, int rd, int rn,
target/arm/translate-a64.c:8036:static void handle_simd_dupg(DisasContext *s, int is_q, int rd, int rn,
target/arm/translate-a64.c:8068:static void handle_simd_inse(DisasContext *s, int rd, int rn,
target/arm/translate-a64.c:8109:static void handle_simd_insg(DisasContext *s, int rd, int rn, int imm5)
target/arm/translate-a64.c:8142:static void handle_simd_umov_smov(DisasContext *s, int is_q, int is_signed,
target/arm/translate-a64.c:8183:static void disas_simd_copy(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:8243:static void disas_simd_mod_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:8294:static void disas_simd_scalar_copy(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:8317:static void disas_simd_scalar_pairwise(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:8476:static void handle_shri_with_rndacc(TCGv_i64 tcg_res, TCGv_i64 tcg_src,
target/arm/translate-a64.c:8558:static void handle_scalar_simd_shri(DisasContext *s,
target/arm/translate-a64.c:8626:static void handle_scalar_simd_shli(DisasContext *s, bool insert,
target/arm/translate-a64.c:8662:static void handle_vec_simd_sqshrn(DisasContext *s, bool is_scalar, bool is_q,
target/arm/translate-a64.c:8749:static void handle_simd_qshl(DisasContext *s, bool scalar, bool is_q,
target/arm/translate-a64.c:8863:static void handle_simd_intfp_conv(DisasContext *s, int rd, int rn,
target/arm/translate-a64.c:8964:static void handle_simd_shift_intfp_conv(DisasContext *s, bool is_scalar,
target/arm/translate-a64.c:9008:static void handle_simd_shift_fpint_conv(DisasContext *s, bool is_scalar,
target/arm/translate-a64.c:9119:static void disas_simd_scalar_shift_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:9192:static void disas_simd_scalar_three_reg_diff(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:9291:static void handle_3same_64(DisasContext *s, int opcode, bool u,
target/arm/translate-a64.c:9379:static void handle_3same_float(DisasContext *s, int size, int elements,
target/arm/translate-a64.c:9569:static void disas_simd_scalar_three_reg_same(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:9737:static void disas_simd_scalar_three_reg_same_fp16(DisasContext *s,
target/arm/translate-a64.c:9830:static void disas_simd_scalar_three_reg_same_extra(DisasContext *s,
target/arm/translate-a64.c:9907:static void handle_2misc_64(DisasContext *s, int opcode, bool u,
target/arm/translate-a64.c:10010:static void handle_2misc_fcmp_zero(DisasContext *s, int opcode,
target/arm/translate-a64.c:10144:static void handle_2misc_reciprocal(DisasContext *s, int opcode,
target/arm/translate-a64.c:10222:static void handle_2misc_narrow(DisasContext *s, bool scalar,
target/arm/translate-a64.c:10338:static void handle_2misc_satacc(DisasContext *s, bool is_scalar, bool is_u,
target/arm/translate-a64.c:10429:static void disas_simd_scalar_two_reg_misc(DisasContext *s, uint32_t insn)
```

- `grep(pattern=^[a-z_].*\(, version=old, path_glob=target/m68k/op_helper.c)` →

```
37 matches
target/m68k/op_helper.c:29:static void cf_rte(CPUM68KState *env)
target/m68k/op_helper.c:43:static void m68k_rte(CPUM68KState *env)
target/m68k/op_helper.c:82:static const char *m68k_exception_name(int index)
target/m68k/op_helper.c:187:static void cf_interrupt_all(CPUM68KState *env, int is_hw)
target/m68k/op_helper.c:256:static inline void do_stack_frame(CPUM68KState *env, uint32_t *sp,
target/m68k/op_helper.c:286:static void m68k_interrupt_all(CPUM68KState *env, int is_hw)
target/m68k/op_helper.c:434:static void do_interrupt_all(CPUM68KState *env, int is_hw)
target/m68k/op_helper.c:443:void m68k_cpu_do_interrupt(CPUState *cs)
target/m68k/op_helper.c:451:static inline void do_interrupt_m68k_hardirq(CPUM68KState *env)
target/m68k/op_helper.c:456:void m68k_cpu_transaction_failed(CPUState *cs, hwaddr physaddr, vaddr addr,
target/m68k/op_helper.c:513:bool m68k_cpu_exec_interrupt(CPUState *cs, int interrupt_request)
target/m68k/op_helper.c:536:raise_exception_ra(CPUM68KState *env, int tt, uintptr_t raddr)
target/m68k/op_helper.c:549:void HELPER(raise_exception)(CPUM68KState *env, uint32_t tt)
target/m68k/op_helper.c:555:raise_exception_format2(CPUM68KState *env, int tt, int ilen, uintptr_t raddr)
target/m68k/op_helper.c:577:void HELPER(divuw)(CPUM68KState *env, int destr, uint32_t den, int ilen)
target/m68k/op_helper.c:605:void HELPER(divsw)(CPUM68KState *env, int destr, int32_t den, int ilen)
target/m68k/op_helper.c:634:void HELPER(divul)(CPUM68KState *env, int numr, int regr,
target/m68k/op_helper.c:664:void HELPER(divsl)(CPUM68KState *env, int numr, int regr,
target/m68k/op_helper.c:694:void HELPER(divull)(CPUM68KState *env, int numr, int regr,
target/m68k/op_helper.c:731:void HELPER(divsll)(CPUM68KState *env, int numr, int regr,
target/m68k/op_helper.c:769:void HELPER(cas2w)(CPUM68KState *env, uint32_t regs, uint32_t a1, uint32_t a2)
target/m68k/op_helper.c:801:static void do_cas2l(CPUM68KState *env, uint32_t regs, uint32_t a1, uint32_t a2,
target/m68k/op_helper.c:863:void HELPER(cas2l)(CPUM68KState *env, uint32_t regs, uint32_t a1, uint32_t a2)
target/m68k/op_helper.c:868:void HELPER(cas2l_parallel)(CPUM68KState *env, uint32_t regs, uint32_t a1,
target/m68k/op_helper.c:881:static struct bf_data bf_prep(uint32_t addr, int32_t ofs, uint32_t len)
target/m68k/op_helper.c:942:static uint64_t bf_load(CPUM68KState *env, uint32_t addr, int blen,
target/m68k/op_helper.c:960:static void bf_store(CPUM68KState *env, uint32_t addr, int blen,
target/m68k/op_helper.c:982:uint32_t HELPER(bfexts_mem)(CPUM68KState *env, uint32_t addr,
target/m68k/op_helper.c:992:uint64_t HELPER(bfextu_mem)(CPUM68KState *env, uint32_t addr,
target/m68k/op_helper.c:1010:uint32_t HELPER(bfins_mem)(CPUM68KState *env, uint32_t addr, uint32_t val,
target/m68k/op_helper.c:1026:uint32_t HELPER(bfchg_mem)(CPUM68KState *env, uint32_t addr,
target/m68k/op_helper.c:1039:uint32_t HELPER(bfclr_mem)(CPUM68KState *env, uint32_t addr,
target/m68k/op_helper.c:1052:uint32_t HELPER(bfset_mem)(CPUM68KState *env, uint32_t addr,
target/m68k/op_helper.c:1065:uint32_t HELPER(bfffo_reg)(uint32_t n, uint32_t ofs, uint32_t len)
target/m68k/op_helper.c:1070:uint64_t HELPER(bfffo_mem)(CPUM68KState *env, uint32_t addr,
target/m68k/op_helper.c:1088:void HELPER(chk)(CPUM68KState *env, int32_t val, int32_t ub)
target/m68k/op_helper.c:1108:void HELPER(chk2)(CPUM68KState *env, int32_t val, int32_t lb, int32_t ub)
```

- `grep(pattern=^[a-z_].*\(, version=old, path_glob=target/nios2/translate.c)` →

```
85 matches (showing 60)
target/nios2/translate.c:73:typedef target_ulong ImmFromIType(const InstrIType *);
target/nios2/translate.c:75:static target_ulong imm_unsigned(const InstrIType *i)
target/nios2/translate.c:80:static target_ulong imm_signed(const InstrIType *i)
target/nios2/translate.c:85:static target_ulong imm_shifted(const InstrIType *i)
target/nios2/translate.c:122:typedef void GenFn2i(TCGv, TCGv, target_long);
target/nios2/translate.c:123:typedef void GenFn3(TCGv, TCGv, TCGv);
target/nios2/translate.c:124:typedef void GenFn4(TCGv, TCGv, TCGv, TCGv);
target/nios2/translate.c:147:static uint8_t get_opcode(uint32_t code)
target/nios2/translate.c:153:static uint8_t get_opxcode(uint32_t code)
target/nios2/translate.c:159:static TCGv load_gpr(DisasContext *dc, unsigned reg)
target/nios2/translate.c:181:static TCGv dest_gpr(DisasContext *dc, unsigned reg)
target/nios2/translate.c:205:static void t_gen_helper_raise_exception(DisasContext *dc, uint32_t index)
target/nios2/translate.c:213:static void gen_goto_tb(DisasContext *dc, int n, uint32_t dest)
target/nios2/translate.c:228:static void gen_jumpr(DisasContext *dc, int regno, bool is_call)
target/nios2/translate.c:251:static void gen_excp(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:256:static bool gen_check_supervisor(DisasContext *dc)
target/nios2/translate.c:270:static void nop(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:278:static void jmpi(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:284:static void call(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:294:static void gen_ldx(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:307:static void gen_stx(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:319:static void br(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:326:static void gen_bxx(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:338:static void do_i_cmpxx(DisasContext *dc, uint32_t insn,
target/nios2/translate.c:350:gen_i_cmpxx(gen_cmpxxsi, imm_signed)
target/nios2/translate.c:351:gen_i_cmpxx(gen_cmpxxui, imm_unsigned)
target/nios2/translate.c:354:static void do_i_math_logic(DisasContext *dc, uint32_t insn,
target/nios2/translate.c:380:gen_i_math_logic(addi,  addi, 1, imm_signed)
target/nios2/translate.c:381:gen_i_math_logic(muli,  muli, 0, imm_signed)
target/nios2/translate.c:383:gen_i_math_logic(andi,  andi, 0, imm_unsigned)
target/nios2/translate.c:384:gen_i_math_logic(ori,   ori,  1, imm_unsigned)
target/nios2/translate.c:385:gen_i_math_logic(xori,  xori, 1, imm_unsigned)
target/nios2/translate.c:387:gen_i_math_logic(andhi, andi, 0, imm_shifted)
target/nios2/translate.c:388:gen_i_math_logic(orhi , ori,  1, imm_shifted)
target/nios2/translate.c:389:gen_i_math_logic(xorhi, xori, 1, imm_shifted)
target/nios2/translate.c:392:static void rdprs(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:413:static void handle_r_type_instr(DisasContext *dc, uint32_t code,
target/nios2/translate.c:490:static void eret(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:512:static void ret(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:521:static void bret(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:540:static void jmp(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:548:static void nextpc(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:559:static void callr(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:567:static void rdctl(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:612:static void wrctl(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:677:static void wrprs(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:707:static void gen_cmpxx(DisasContext *dc, uint32_t code, uint32_t flags)
target/nios2/translate.c:715:static void do_ri_math_logic(DisasContext *dc, uint32_t insn, GenFn2i *fn)
target/nios2/translate.c:721:static void do_rr_math_logic(DisasContext *dc, uint32_t insn, GenFn3 *fn)
target/nios2/translate.c:735:gen_rr_math_logic(add,  add)
target/nios2/translate.c:736:gen_rr_math_logic(sub,  sub)
target/nios2/translate.c:737:gen_rr_math_logic(mul,  mul)
target/nios2/translate.c:739:gen_rr_math_logic(and,  and)
target/nios2/translate.c:740:gen_rr_math_logic(or,   or)
target/nios2/translate.c:741:gen_rr_math_logic(xor,  xor)
target/nios2/translate.c:742:gen_rr_math_logic(nor,  nor)
target/nios2/translate.c:744:gen_ri_math_logic(srai, sari)
target/nios2/translate.c:745:gen_ri_math_logic(srli, shri)
target/nios2/translate.c:746:gen_ri_math_logic(slli, shli)
target/nios2/translate.c:747:gen_ri_math_logic(roli, rotli)
```

- `grep(pattern=^[a-z_].*\(, version=old, path_glob=softmmu/vl.c, max_results=300)` →

```
90 matches
softmmu/vl.c:147:typedef QSIMPLEQ_HEAD(, BlockdevOptionsQueueEntry) BlockdevOptionsQueue;
softmmu/vl.c:168:static QTAILQ_HEAD(, ObjectOption) object_opts = QTAILQ_HEAD_INITIALIZER(object_opts);
softmmu/vl.c:169:static QTAILQ_HEAD(, DeviceOption) device_opts = QTAILQ_HEAD_INITIALIZER(device_opts);
softmmu/vl.c:173:static QemuPluginList plugin_list = QTAILQ_HEAD_INITIALIZER(plugin_list);
softmmu/vl.c:174:static BlockdevOptionsQueue bdo_queue = QSIMPLEQ_HEAD_INITIALIZER(bdo_queue);
softmmu/vl.c:505:const char *qemu_get_vm_name(void)
softmmu/vl.c:510:static void default_driver_disable(const char *driver)
softmmu/vl.c:525:static int default_driver_check(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:533:static void default_driver_check_json(void)
softmmu/vl.c:543:static int parse_name(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:560:bool defaults_enabled(void)
softmmu/vl.c:566:static int parse_add_fd(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:623:static int cleanup_add_fd(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:644:static int drive_init_func(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:651:static int drive_enable_snapshot(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:659:static void default_drive(int enable, int snapshot, BlockInterfaceType type,
softmmu/vl.c:679:static void configure_blockdev(BlockdevOptionsQueue *bdo_queue,
softmmu/vl.c:752:static void realtime_init(void)
softmmu/vl.c:763:static void configure_msg(QemuOpts *opts)
softmmu/vl.c:773:static int usb_device_add(const char *devname)
softmmu/vl.c:788:static int usb_parse(const char *cmdline)
softmmu/vl.c:801:static MachineClass *find_machine(const char *name, GSList *machines)
softmmu/vl.c:816:static MachineClass *find_default_machine(GSList *machines)
softmmu/vl.c:833:static void version(void)
softmmu/vl.c:839:static void help(int exitcode)
softmmu/vl.c:947:static bool vga_interface_available(VGAInterfaceType t)
softmmu/vl.c:958:get_default_vga_model(const MachineClass *machine_class)
softmmu/vl.c:971:static void select_vgahw(const MachineClass *machine_class, const char *p)
softmmu/vl.c:1023:static void parse_display_qapi(const char *optarg)
softmmu/vl.c:1042:static void parse_display(const char *p)
softmmu/vl.c:1067:static inline bool nonempty_str(const char *str)
softmmu/vl.c:1072:static int parse_fw_cfg(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:1133:static int device_help_func(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:1138:static int device_init_func(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:1152:static int chardev_init_func(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:1167:static int fsdev_init_func(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:1173:static int mon_init_func(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:1178:static void monitor_parse(const char *optarg, const char *mode, bool pretty)
softmmu/vl.c:1222:static QTAILQ_HEAD(, device_config) device_configs =
softmmu/vl.c:1225:static void add_device_config(int type, const char *cmdline)
softmmu/vl.c:1236:static int foreach_device_config(int type, int (*func)(const char *cmdline))
softmmu/vl.c:1254:static void qemu_disable_default_devices(void)
softmmu/vl.c:1290:static void qemu_create_default_devices(void)
softmmu/vl.c:1365:static int serial_parse(const char *devname)
softmmu/vl.c:1394:static int parallel_parse(const char *devname)
softmmu/vl.c:1416:static int debugcon_parse(const char *devname)
softmmu/vl.c:1434:static gint machine_class_cmp(gconstpointer a, gconstpointer b)
softmmu/vl.c:1468:static void machine_help_func(const QDict *qdict)
softmmu/vl.c:1496:machine_merge_property(const char *propname, QDict *prop, Error **errp)
softmmu/vl.c:1509:machine_parse_property_opt(QemuOptsList *opts_list, const char *propname,
softmmu/vl.c:1531:static void qemu_unlink_pidfile(Notifier *n, void *data)
softmmu/vl.c:1539:static const QEMUOption *lookup_opt(int argc, char **argv,
softmmu/vl.c:1579:static MachineClass *select_machine(QDict *qdict, Error **errp)
softmmu/vl.c:1607:static int object_parse_property_opt(Object *obj,
softmmu/vl.c:1623:static void keyval_dashify(QDict *qdict, Error **errp)
softmmu/vl.c:1651:static void qemu_apply_legacy_machine_options(QDict *qdict)
softmmu/vl.c:1709:static void object_option_foreach_add(bool (*type_opt_predicate)(const char *))
softmmu/vl.c:1724:static void object_option_add_visitor(Visitor *v)
softmmu/vl.c:1731:static void object_option_parse(const char *optarg)
softmmu/vl.c:1771:static bool object_create_early(const char *type)
softmmu/vl.c:1821:static void qemu_apply_machine_options(QDict *qdict)
softmmu/vl.c:1837:static void qemu_create_early_backends(void)
softmmu/vl.c:1898:static bool object_create_late(const char *type)
softmmu/vl.c:1903:static void qemu_create_late_backends(void)
softmmu/vl.c:1931:static void qemu_resolve_machine_memdev(void)
softmmu/vl.c:1952:static void parse_memory_options(void)
softmmu/vl.c:1989:static void qemu_create_machine(QDict *qdict)
softmmu/vl.c:2032:static int global_init_func(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:2048:static bool is_qemuopts_group(const char *group)
softmmu/vl.c:2059:static void qemu_record_config_group(const char *group, QDict *dict,
softmmu/vl.c:2086:static void qemu_parse_config_group(const char *group, QDict *qdict,
softmmu/vl.c:2112:static void qemu_read_default_config_file(Error **errp)
softmmu/vl.c:2127:static void qemu_set_option(const char *str, Error **errp)
softmmu/vl.c:2155:static void user_register_global_props(void)
softmmu/vl.c:2161:static int do_configure_icount(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:2167:static int accelerator_set_property(void *opaque,
softmmu/vl.c:2174:static int do_configure_accelerator(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:2210:static void configure_accelerators(const char *progname)
softmmu/vl.c:2282:static void qemu_validate_options(const QDict *machine_opts)
softmmu/vl.c:2318:static void qemu_process_sugar_options(void)
softmmu/vl.c:2345:static int process_runstate_actions(void *opaque, QemuOpts *opts, Error **errp)
softmmu/vl.c:2360:static void qemu_process_early_options(void)
softmmu/vl.c:2401:static void qemu_process_help_options(void)
softmmu/vl.c:2426:static void qemu_maybe_daemonize(const char *pid_file)
softmmu/vl.c:2459:static void qemu_init_displays(void)
softmmu/vl.c:2481:static void qemu_init_board(void)
softmmu/vl.c:2499:static void qemu_create_cli_devices(void)
softmmu/vl.c:2535:static void qemu_machine_creation_done(void)
softmmu/vl.c:2576:void qmp_x_exit_preconfig(Error **errp)
softmmu/vl.c:2608:void qemu_init(int argc, char **argv, char **envp)
```

### Turn 4  _(tok 38111+350, stop=tool_use)_

**Reasoning:** I'm checking the vl.c machine options function around line 1825, then looking up the Arm translate functions behind lines 6559 and 8767, along with the a64 handler near 2222 and the m68k one near 206. I still need to track down the nios2 function at line 821.



- `grep(pattern=^[a-z_].*\(, version=old, path_glob=target/arm/translate.c, max_results=500)` →

```
475 matches (showing 200)
target/arm/translate.c:69:void arm_translate_init(void)
target/arm/translate.c:91:uint64_t asimd_imm_const(uint32_t imm, int cmode, int op)
target/arm/translate.c:162:void arm_gen_condlabel(DisasContext *s)
target/arm/translate.c:186:void store_cpu_offset(TCGv_i32 var, int offset, int size)
target/arm/translate.c:202:static void disas_set_da_iss(DisasContext *s, MemOp memop, ISSInfo issinfo)
target/arm/translate.c:232:static inline int get_a32_user_mem_index(DisasContext *s)
target/arm/translate.c:268:static uint32_t read_pc(DisasContext *s)
target/arm/translate.c:274:void load_reg_var(DisasContext *s, TCGv_i32 var, int reg)
target/arm/translate.c:302:void store_reg(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:327:static void store_sp_checked(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:346:void gen_set_cpsr(TCGv_i32 var, uint32_t mask)
target/arm/translate.c:351:static void gen_rebuild_hflags(DisasContext *s, bool new_el)
target/arm/translate.c:371:static void gen_exception_internal(int excp)
target/arm/translate.c:377:static void gen_singlestep_exception(DisasContext *s)
target/arm/translate.c:393:void clear_eci_state(DisasContext *s)
target/arm/translate.c:405:static void gen_smul_dual(TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:421:void gen_rev16(TCGv_i32 dest, TCGv_i32 var)
target/arm/translate.c:434:static void gen_revsh(TCGv_i32 dest, TCGv_i32 var)
target/arm/translate.c:446:static void gen_add16(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:459:static inline void gen_logic_CC(TCGv_i32 var)
target/arm/translate.c:466:static void gen_add_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:473:static void gen_sub_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:481:static void gen_add_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:495:static void gen_adc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:523:static void gen_sub_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:538:static void gen_sbc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:547:static void gen_##name(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)       \
target/arm/translate.c:563:static void gen_sar(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:573:static void shifter_out_im(TCGv_i32 var, int shift)
target/arm/translate.c:579:static inline void gen_arm_shift_im(TCGv_i32 var, int shiftop,
target/arm/translate.c:628:static inline void gen_arm_shift_reg(TCGv_i32 var, int shiftop,
target/arm/translate.c:660:void arm_test_cc(DisasCompare *cmp, int cc)
target/arm/translate.c:746:void arm_free_cc(DisasCompare *cmp)
target/arm/translate.c:753:void arm_jump_cc(DisasCompare *cmp, TCGLabel *label)
target/arm/translate.c:758:void arm_gen_test_cc(int cc, TCGLabel *label)
target/arm/translate.c:766:void gen_set_condexec(DisasContext *s)
target/arm/translate.c:775:void gen_set_pc_im(DisasContext *s, target_ulong val)
target/arm/translate.c:781:static inline void gen_bx(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:811:static inline void gen_bx_excret(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:825:static inline void gen_bx_excret_final_code(DisasContext *s)
target/arm/translate.c:863:static inline void gen_bxns(DisasContext *s, int rm)
target/arm/translate.c:882:static inline void gen_blxns(DisasContext *s, int rm)
target/arm/translate.c:899:static inline void store_reg_bx(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:912:static inline void store_reg_from_load(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:951:static TCGv gen_aa32_addr(DisasContext *s, TCGv_i32 a32, MemOp op)
target/arm/translate.c:967:void gen_aa32_ld_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:975:void gen_aa32_st_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:983:void gen_aa32_ld_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:997:void gen_aa32_st_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:1014:void gen_aa32_ld_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1020:void gen_aa32_st_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1026:void gen_aa32_ld_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1032:void gen_aa32_st_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1052:static inline void gen_hvc(DisasContext *s, int imm16)
target/arm/translate.c:1070:static inline void gen_smc(DisasContext *s)
target/arm/translate.c:1081:static void gen_exception_internal_insn(DisasContext *s, uint32_t pc, int excp)
target/arm/translate.c:1089:static void gen_exception_el_v(int excp, uint32_t syndrome, TCGv_i32 tcg_el)
target/arm/translate.c:1095:static void gen_exception_el(int excp, uint32_t syndrome, uint32_t target_el)
target/arm/translate.c:1100:static void gen_exception(int excp, uint32_t syndrome)
target/arm/translate.c:1106:static void gen_exception_insn_el_v(DisasContext *s, uint64_t pc, int excp,
target/arm/translate.c:1119:void gen_exception_insn_el(DisasContext *s, uint64_t pc, int excp,
target/arm/translate.c:1125:void gen_exception_insn(DisasContext *s, uint64_t pc, int excp, uint32_t syn)
target/arm/translate.c:1137:static void gen_exception_bkpt_insn(DisasContext *s, uint32_t syn)
target/arm/translate.c:1145:void unallocated_encoding(DisasContext *s)
target/arm/translate.c:1152:void gen_lookup_tb(DisasContext *s)
target/arm/translate.c:1158:static inline void gen_hlt(DisasContext *s, int imm)
target/arm/translate.c:1187:long neon_full_reg_offset(unsigned reg)
target/arm/translate.c:1196:long neon_element_offset(int reg, int element, MemOp memop)
target/arm/translate.c:1213:long vfp_reg_offset(bool dp, unsigned reg)
target/arm/translate.c:1222:void read_neon_element32(TCGv_i32 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1248:void read_neon_element64(TCGv_i64 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1267:void write_neon_element32(TCGv_i32 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1286:void write_neon_element64(TCGv_i64 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1304:static inline void iwmmxt_load_reg(TCGv_i64 var, int reg)
target/arm/translate.c:1309:static inline void iwmmxt_store_reg(TCGv_i64 var, int reg)
target/arm/translate.c:1314:static inline TCGv_i32 iwmmxt_load_creg(int reg)
target/arm/translate.c:1321:static inline void iwmmxt_store_creg(int reg, TCGv_i32 var)
target/arm/translate.c:1327:static inline void gen_op_iwmmxt_movq_wRn_M0(int rn)
target/arm/translate.c:1332:static inline void gen_op_iwmmxt_movq_M0_wRn(int rn)
target/arm/translate.c:1337:static inline void gen_op_iwmmxt_orq_M0_wRn(int rn)
target/arm/translate.c:1343:static inline void gen_op_iwmmxt_andq_M0_wRn(int rn)
target/arm/translate.c:1349:static inline void gen_op_iwmmxt_xorq_M0_wRn(int rn)
target/arm/translate.c:1356:static inline void gen_op_iwmmxt_##name##_M0_wRn(int rn) \
target/arm/translate.c:1363:static inline void gen_op_iwmmxt_##name##_M0_wRn(int rn) \
target/arm/translate.c:1375:static inline void gen_op_iwmmxt_##name##_M0(void) \
target/arm/translate.c:1435:static void gen_op_iwmmxt_set_mup(void)
target/arm/translate.c:1443:static void gen_op_iwmmxt_set_cup(void)
target/arm/translate.c:1451:static void gen_op_iwmmxt_setpsr_nz(void)
target/arm/translate.c:1458:static inline void gen_op_iwmmxt_addl_M0_wRn(int rn)
target/arm/translate.c:1465:static inline int gen_iwmmxt_address(DisasContext *s, uint32_t insn,
target/arm/translate.c:1500:static inline int gen_iwmmxt_shift(uint32_t insn, uint32_t mask, TCGv_i32 dest)
target/arm/translate.c:1524:static int disas_iwmmxt_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:2524:static int disas_dsp_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:2591:static void gen_goto_ptr(void)
target/arm/translate.c:2600:static void gen_goto_tb(DisasContext *s, int n, target_ulong dest)
target/arm/translate.c:2614:static inline void gen_jmp_tb(DisasContext *s, uint32_t dest, int tbno)
target/arm/translate.c:2657:static inline void gen_jmp(DisasContext *s, uint32_t dest)
target/arm/translate.c:2662:static inline void gen_mulxy(TCGv_i32 t0, TCGv_i32 t1, int x, int y)
target/arm/translate.c:2676:static uint32_t msr_mask(DisasContext *s, int flags, int spsr)
target/arm/translate.c:2709:static int gen_set_psr(DisasContext *s, uint32_t mask, int spsr, TCGv_i32 t0)
target/arm/translate.c:2731:static int gen_set_psr_im(DisasContext *s, uint32_t mask, int spsr, uint32_t val)
target/arm/translate.c:2739:static bool msr_banked_access_decode(DisasContext *s, int r, int sysm, int rn,
target/arm/translate.c:2901:static void gen_msr_banked(DisasContext *s, int r, int sysm, int rn)
target/arm/translate.c:2921:static void gen_mrs_banked(DisasContext *s, int r, int sysm, int rn)
target/arm/translate.c:2945:static void store_pc_exc_ret(DisasContext *s, TCGv_i32 pc)
target/arm/translate.c:2952:static void gen_rfe(DisasContext *s, TCGv_i32 pc, TCGv_i32 cpsr)
target/arm/translate.c:2969:static void gen_exception_return(DisasContext *s, TCGv_i32 pc)
target/arm/translate.c:2974:static void gen_gvec_fn3_qc(uint32_t rd_ofs, uint32_t rn_ofs, uint32_t rm_ofs,
target/arm/translate.c:2986:void gen_gvec_sqrdmlah_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:2996:void gen_gvec_sqrdmlsh_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3059:static void gen_ssra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3065:static void gen_ssra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3071:static void gen_ssra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3077:static void gen_ssra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3083:static void gen_ssra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3089:void gen_gvec_ssra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3135:static void gen_usra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3141:static void gen_usra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3147:static void gen_usra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3153:static void gen_usra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3159:static void gen_usra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3165:void gen_gvec_usra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3221:static void gen_srshr8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3232:static void gen_srshr16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3243:static void gen_srshr32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3259:static void gen_srshr64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3269:static void gen_srshr_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3284:void gen_gvec_srshr(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3331:static void gen_srsra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3340:static void gen_srsra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3349:static void gen_srsra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3358:static void gen_srsra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3367:static void gen_srsra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3376:void gen_gvec_srsra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3428:static void gen_urshr8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3439:static void gen_urshr16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3450:static void gen_urshr32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3466:static void gen_urshr64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3476:static void gen_urshr_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t shift)
target/arm/translate.c:3491:void gen_gvec_urshr(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3537:static void gen_ursra8_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3550:static void gen_ursra16_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3563:static void gen_ursra32_i32(TCGv_i32 d, TCGv_i32 a, int32_t sh)
target/arm/translate.c:3576:static void gen_ursra64_i64(TCGv_i64 d, TCGv_i64 a, int64_t sh)
target/arm/translate.c:3589:static void gen_ursra_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3602:void gen_gvec_ursra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3643:static void gen_shr8_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3655:static void gen_shr16_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3667:static void gen_shr32_ins_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3673:static void gen_shr64_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3679:static void gen_shr_ins_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3693:void gen_gvec_sri(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3738:static void gen_shl8_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3750:static void gen_shl16_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3762:static void gen_shl32_ins_i32(TCGv_i32 d, TCGv_i32 a, int32_t shift)
target/arm/translate.c:3767:static void gen_shl64_ins_i64(TCGv_i64 d, TCGv_i64 a, int64_t shift)
target/arm/translate.c:3772:static void gen_shl_ins_vec(unsigned vece, TCGv_vec d, TCGv_vec a, int64_t sh)
target/arm/translate.c:3786:void gen_gvec_sli(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3829:static void gen_mla8_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3835:static void gen_mls8_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3841:static void gen_mla16_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3847:static void gen_mls16_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3853:static void gen_mla32_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3859:static void gen_mls32_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3865:static void gen_mla64_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3871:static void gen_mls64_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3877:static void gen_mla_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3883:static void gen_mls_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3892:void gen_gvec_mla(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3924:void gen_gvec_mls(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3957:static void gen_cmtst_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:3964:void gen_cmtst_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3971:static void gen_cmtst_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:3978:void gen_gvec_cmtst(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4004:void gen_ushl_i32(TCGv_i32 dst, TCGv_i32 src, TCGv_i32 shift)
target/arm/translate.c:4031:void gen_ushl_i64(TCGv_i64 dst, TCGv_i64 src, TCGv_i64 shift)
target/arm/translate.c:4058:static void gen_ushl_vec(unsigned vece, TCGv_vec dst,
target/arm/translate.c:4116:void gen_gvec_ushl(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4144:void gen_sshl_i32(TCGv_i32 dst, TCGv_i32 src, TCGv_i32 shift)
target/arm/translate.c:4172:void gen_sshl_i64(TCGv_i64 dst, TCGv_i64 src, TCGv_i64 shift)
target/arm/translate.c:4200:static void gen_sshl_vec(unsigned vece, TCGv_vec dst,
target/arm/translate.c:4250:void gen_gvec_sshl(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4278:static void gen_uqadd_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4289:void gen_gvec_uqadd_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4321:static void gen_sqadd_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4332:void gen_gvec_sqadd_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4364:static void gen_uqsub_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4375:void gen_gvec_uqsub_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4407:static void gen_sqsub_vec(unsigned vece, TCGv_vec t, TCGv_vec sat,
target/arm/translate.c:4418:void gen_gvec_sqsub_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4450:static void gen_sabd_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4460:static void gen_sabd_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:4470:static void gen_sabd_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:4480:void gen_gvec_sabd(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4510:static void gen_uabd_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4520:static void gen_uabd_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:4530:static void gen_uabd_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:4540:void gen_gvec_uabd(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4570:static void gen_saba_i32(TCGv_i32 d, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:4578:static void gen_saba_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
```

- `read_file(path=target/nios2/translate.c, version=old, start_line=800, end_line=825)` →

```
target/nios2/translate.c lines 800-825 of 1118
  800| 
  801| static void trap(DisasContext *dc, uint32_t code, uint32_t flags)
  802| {
  803| #ifdef CONFIG_USER_ONLY
  804|     /*
  805|      * The imm5 field is not stored anywhere on real hw; the kernel
  806|      * has to load the insn and extract the field.  But we can make
  807|      * things easier for cpu_loop if we pop this into env->error_code.
  808|      */
  809|     R_TYPE(instr, code);
  810|     tcg_gen_st_i32(tcg_constant_i32(instr.imm5), cpu_env,
  811|                    offsetof(CPUNios2State, error_code));
  812| #endif
  813|     t_gen_helper_raise_exception(dc, EXCP_TRAP);
  814| }
  815| 
  816| static void gen_break(DisasContext *dc, uint32_t code, uint32_t flags)
  817| {
  818| #ifndef CONFIG_USER_ONLY
  819|     /* The semihosting instruction is "break 1".  */
  820|     R_TYPE(instr, code);
  821|     if (semihosting_enabled() && instr.imm5 == 1) {
  822|         t_gen_helper_raise_exception(dc, EXCP_SEMIHOST);
  823|         return;
  824|     }
  825| #endif
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 48979+909, stop=tool_use, forced)_

**Reasoning:** I'm trying to recall the functions at lines 6559 and 8767 of QEMU's arm translate.c, and I don't know them offhand. My guess is that 6559 might be trans_SVC, which I remember has a semihosting check gated on semihosting_enabled().

I'm now recalling that line 8767 is the trans_SVC handler, the one with the semihosting check, so that part is settled. For 6559, the function that fits is trans_BKPT: it gates on ARM_FEATURE_M, semihosting_enabled(), and the 0xab immediate before raising the semihost exception. That's my best reconstruction, so I'll say so when I answer.



- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3753+173, stop=tool_use)_

- `get_callers(name=semihosting_enabled, limit=200)` →

```
{
  "name": "semihosting_enabled",
  "version": "old",
  "callers": [
    {
      "caller": "qemu_apply_machine_options",
      "file": "softmmu/vl.c",
      "line": 1825
    },
    {
      "caller": "disas_exc",
      "file": "target/arm/translate-a64.c",
      "line": 2222
    },
    {
      "caller": "gen_hlt",
      "file": "target/arm/translate.c",
      "line": 1172
    },
    {
      "caller": "trans_BKPT",
      "file": "target/arm/translate.c",
      "line": 6559
    },
    {
      "caller": "trans_SVC",
      "file": "target/arm/translate.c",
      "line": 8767
    },
    {
      "caller": "cf_interrupt_all",
      "file": "target/m68k/op_helper.c",
      "line": 206
    },
    {
      "caller": "is_uhi",
      "file": "target/mips/tcg/translate.c",
      "line": 12090
    },
    {
      "caller": "gen_break",
      "file": "target/nios2/translate.c",
      "line": 821
    },
    {
      "caller": "test_exceptions_simcall",
      "file": "target/xtensa/translate.c",
      "line": 2369
    },
    {
      "caller": "test_exceptions_simcall",
      "file": "target/xtensa/translate.c",
      "line": 2371
    },
    {
      "caller": "translate_simcall",
      "file": "target/xtensa/translate.c",
      "line": 2381
    }
  ]
}
```

- `grep(pattern=semihosting_enabled, version=old, max_results=200)` →

```
15 matches
include/semihosting/semihost.h:30:static inline bool semihosting_enabled(void)
include/semihosting/semihost.h:55:bool semihosting_enabled(void);
semihosting/config.c:62:bool semihosting_enabled(void)
softmmu/vl.c:1825:    if (semihosting_enabled() && !semihosting_get_argc()) {
stubs/semihost.c:26:bool semihosting_enabled(void)
target/arm/translate-a64.c:2222:        if (semihosting_enabled() && imm16 == 0xf000) {
target/arm/translate.c:1172:    if (semihosting_enabled() &&
target/arm/translate.c:6559:        semihosting_enabled() &&
target/arm/translate.c:8767:    if (!arm_dc_feature(s, ARM_FEATURE_M) && semihosting_enabled() &&
target/m68k/op_helper.c:206:            if (semihosting_enabled()
target/mips/tcg/translate.c:12090:    return semihosting_enabled() && sdbbp_code == 1;
target/nios2/translate.c:821:    if (semihosting_enabled() && instr.imm5 == 1) {
target/xtensa/translate.c:2369:    bool ill = dc->config->hw_version <= 250002 && !semihosting_enabled();
target/xtensa/translate.c:2371:    if (ill || !semihosting_enabled()) {
target/xtensa/translate.c:2381:    if (semihosting_enabled()) {
```

### Turn 2  _(tok 5056+361, stop=tool_use)_

- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3205+132, stop=tool_use)_

- `get_callers(name=semihosting_enabled, limit=200)` →

```
{
  "name": "semihosting_enabled",
  "version": "old",
  "callers": [
    {
      "caller": "qemu_apply_machine_options",
      "file": "softmmu/vl.c",
      "line": 1825
    },
    {
      "caller": "disas_exc",
      "file": "target/arm/translate-a64.c",
      "line": 2222
    },
    {
      "caller": "gen_hlt",
      "file": "target/arm/translate.c",
      "line": 1172
    },
    {
      "caller": "trans_BKPT",
      "file": "target/arm/translate.c",
      "line": 6559
    },
    {
      "caller": "trans_SVC",
      "file": "target/arm/translate.c",
      "line": 8767
    },
    {
      "caller": "cf_interrupt_all",
      "file": "target/m68k/op_helper.c",
      "line": 206
    },
    {
      "caller": "is_uhi",
      "file": "target/mips/tcg/translate.c",
      "line": 12090
    },
    {
      "caller": "gen_break",
      "file": "target/nios2/translate.c",
      "line": 821
    },
    {
      "caller": "test_exceptions_simcall",
      "file": "target/xtensa/translate.c",
      "line": 2369
    },
    {
      "caller": "test_exceptions_simcall",
      "file": "target/xtensa/translate.c",
      "line": 2371
    },
    {
      "caller": "translate_simcall",
      "file": "target/xtensa/translate.c",
      "line": 2381
    }
  ]
}
```

- `resolve_symbol(name=semihosting_enabled)` →

```
{
  "resolved": true,
  "name": "semihosting_enabled",
  "version": "old",
  "file": "include/semihosting/semihost.h",
  "line": 30,
  "kind": "function",
  "signature": "static inline bool semihosting_enabled(void)",
  "resolution_method": "priority_fallback",
  "ambiguous": true,
  "definitions": 3,
  "alternatives": [
    {
      "file": "semihosting/config.c",
      "line": 62,
      "kind": "function"
    },
    {
      "file": "stubs/semihost.c",
      "line": 26,
      "kind": "function"
    }
  ],
  "hint": "several definitions share this name; the chosen one is ranked by resolution_method (functions over macros, real code over stubs). get_context_at(file, line) looks at another definition."
}
```

### Turn 2  _(tok 4231+422, stop=tool_use)_

**Reasoning:** I'm thinking there may be other callers in places like target/riscv and hw. The tool might be incomplete, but I'll accept that for now. I'm wondering whether to check the "work" version, and whether the default is still the old one, so I'll try the rev and move on.



- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

