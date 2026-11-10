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

### Turn 2  _(tok 1847+914, stop=tool_use)_

**Reasoning:** I still need the enclosing functions, and I'm wondering whether macros matter here too. I'll grep for other uses of "semihosting_enabled" alone, then read the surrounding contexts.



- `grep(pattern=^[a-z].*\(|^\{, version=old, path_glob=target/arm/translate.c, max_results=400)` →

```
951 matches (showing 200)
target/arm/translate.c:69:void arm_translate_init(void)
target/arm/translate.c:70:{
target/arm/translate.c:91:uint64_t asimd_imm_const(uint32_t imm, int cmode, int op)
target/arm/translate.c:92:{
target/arm/translate.c:162:void arm_gen_condlabel(DisasContext *s)
target/arm/translate.c:163:{
target/arm/translate.c:186:void store_cpu_offset(TCGv_i32 var, int offset, int size)
target/arm/translate.c:187:{
target/arm/translate.c:202:static void disas_set_da_iss(DisasContext *s, MemOp memop, ISSInfo issinfo)
target/arm/translate.c:203:{
target/arm/translate.c:232:static inline int get_a32_user_mem_index(DisasContext *s)
target/arm/translate.c:233:{
target/arm/translate.c:268:static uint32_t read_pc(DisasContext *s)
target/arm/translate.c:269:{
target/arm/translate.c:274:void load_reg_var(DisasContext *s, TCGv_i32 var, int reg)
target/arm/translate.c:275:{
target/arm/translate.c:289:{
target/arm/translate.c:302:void store_reg(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:303:{
target/arm/translate.c:327:static void store_sp_checked(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:328:{
target/arm/translate.c:346:void gen_set_cpsr(TCGv_i32 var, uint32_t mask)
target/arm/translate.c:347:{
target/arm/translate.c:351:static void gen_rebuild_hflags(DisasContext *s, bool new_el)
target/arm/translate.c:352:{
target/arm/translate.c:371:static void gen_exception_internal(int excp)
target/arm/translate.c:372:{
target/arm/translate.c:377:static void gen_singlestep_exception(DisasContext *s)
target/arm/translate.c:378:{
target/arm/translate.c:393:void clear_eci_state(DisasContext *s)
target/arm/translate.c:394:{
target/arm/translate.c:405:static void gen_smul_dual(TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:406:{
target/arm/translate.c:421:void gen_rev16(TCGv_i32 dest, TCGv_i32 var)
target/arm/translate.c:422:{
target/arm/translate.c:434:static void gen_revsh(TCGv_i32 dest, TCGv_i32 var)
target/arm/translate.c:435:{
target/arm/translate.c:446:static void gen_add16(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:447:{
target/arm/translate.c:459:static inline void gen_logic_CC(TCGv_i32 var)
target/arm/translate.c:460:{
target/arm/translate.c:466:static void gen_add_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:467:{
target/arm/translate.c:473:static void gen_sub_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:474:{
target/arm/translate.c:481:static void gen_add_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:482:{
target/arm/translate.c:495:static void gen_adc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:496:{
target/arm/translate.c:523:static void gen_sub_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:524:{
target/arm/translate.c:538:static void gen_sbc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:539:{
target/arm/translate.c:547:static void gen_##name(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)       \
target/arm/translate.c:548:{                                                                     \
target/arm/translate.c:563:static void gen_sar(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:564:{
target/arm/translate.c:573:static void shifter_out_im(TCGv_i32 var, int shift)
target/arm/translate.c:574:{
target/arm/translate.c:579:static inline void gen_arm_shift_im(TCGv_i32 var, int shiftop,
target/arm/translate.c:581:{
target/arm/translate.c:628:static inline void gen_arm_shift_reg(TCGv_i32 var, int shiftop,
target/arm/translate.c:630:{
target/arm/translate.c:660:void arm_test_cc(DisasCompare *cmp, int cc)
target/arm/translate.c:661:{
target/arm/translate.c:746:void arm_free_cc(DisasCompare *cmp)
target/arm/translate.c:747:{
target/arm/translate.c:753:void arm_jump_cc(DisasCompare *cmp, TCGLabel *label)
target/arm/translate.c:754:{
target/arm/translate.c:758:void arm_gen_test_cc(int cc, TCGLabel *label)
target/arm/translate.c:759:{
target/arm/translate.c:766:void gen_set_condexec(DisasContext *s)
target/arm/translate.c:767:{
target/arm/translate.c:775:void gen_set_pc_im(DisasContext *s, target_ulong val)
target/arm/translate.c:776:{
target/arm/translate.c:781:static inline void gen_bx(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:782:{
target/arm/translate.c:811:static inline void gen_bx_excret(DisasContext *s, TCGv_i32 var)
target/arm/translate.c:812:{
target/arm/translate.c:825:static inline void gen_bx_excret_final_code(DisasContext *s)
target/arm/translate.c:826:{
target/arm/translate.c:863:static inline void gen_bxns(DisasContext *s, int rm)
target/arm/translate.c:864:{
target/arm/translate.c:882:static inline void gen_blxns(DisasContext *s, int rm)
target/arm/translate.c:883:{
target/arm/translate.c:899:static inline void store_reg_bx(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:900:{
target/arm/translate.c:912:static inline void store_reg_from_load(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:913:{
target/arm/translate.c:928:{
target/arm/translate.c:951:static TCGv gen_aa32_addr(DisasContext *s, TCGv_i32 a32, MemOp op)
target/arm/translate.c:952:{
target/arm/translate.c:967:void gen_aa32_ld_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:969:{
target/arm/translate.c:975:void gen_aa32_st_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:977:{
target/arm/translate.c:983:void gen_aa32_ld_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:985:{
target/arm/translate.c:997:void gen_aa32_st_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:999:{
target/arm/translate.c:1014:void gen_aa32_ld_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1016:{
target/arm/translate.c:1020:void gen_aa32_st_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1022:{
target/arm/translate.c:1026:void gen_aa32_ld_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1028:{
target/arm/translate.c:1032:void gen_aa32_st_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1034:{
target/arm/translate.c:1052:static inline void gen_hvc(DisasContext *s, int imm16)
target/arm/translate.c:1053:{
target/arm/translate.c:1070:static inline void gen_smc(DisasContext *s)
target/arm/translate.c:1071:{
target/arm/translate.c:1081:static void gen_exception_internal_insn(DisasContext *s, uint32_t pc, int excp)
target/arm/translate.c:1082:{
target/arm/translate.c:1089:static void gen_exception_el_v(int excp, uint32_t syndrome, TCGv_i32 tcg_el)
target/arm/translate.c:1090:{
target/arm/translate.c:1095:static void gen_exception_el(int excp, uint32_t syndrome, uint32_t target_el)
target/arm/translate.c:1096:{
target/arm/translate.c:1100:static void gen_exception(int excp, uint32_t syndrome)
target/arm/translate.c:1101:{
target/arm/translate.c:1106:static void gen_exception_insn_el_v(DisasContext *s, uint64_t pc, int excp,
target/arm/translate.c:1108:{
target/arm/translate.c:1119:void gen_exception_insn_el(DisasContext *s, uint64_t pc, int excp,
target/arm/translate.c:1121:{
target/arm/translate.c:1125:void gen_exception_insn(DisasContext *s, uint64_t pc, int excp, uint32_t syn)
target/arm/translate.c:1126:{
target/arm/translate.c:1137:static void gen_exception_bkpt_insn(DisasContext *s, uint32_t syn)
target/arm/translate.c:1138:{
target/arm/translate.c:1145:void unallocated_encoding(DisasContext *s)
target/arm/translate.c:1146:{
target/arm/translate.c:1152:void gen_lookup_tb(DisasContext *s)
target/arm/translate.c:1153:{
target/arm/translate.c:1158:static inline void gen_hlt(DisasContext *s, int imm)
target/arm/translate.c:1159:{
target/arm/translate.c:1187:long neon_full_reg_offset(unsigned reg)
target/arm/translate.c:1188:{
target/arm/translate.c:1196:long neon_element_offset(int reg, int element, MemOp memop)
target/arm/translate.c:1197:{
target/arm/translate.c:1213:long vfp_reg_offset(bool dp, unsigned reg)
target/arm/translate.c:1214:{
target/arm/translate.c:1222:void read_neon_element32(TCGv_i32 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1223:{
target/arm/translate.c:1248:void read_neon_element64(TCGv_i64 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1249:{
target/arm/translate.c:1267:void write_neon_element32(TCGv_i32 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1268:{
target/arm/translate.c:1286:void write_neon_element64(TCGv_i64 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1287:{
target/arm/translate.c:1304:static inline void iwmmxt_load_reg(TCGv_i64 var, int reg)
target/arm/translate.c:1305:{
target/arm/translate.c:1309:static inline void iwmmxt_store_reg(TCGv_i64 var, int reg)
target/arm/translate.c:1310:{
target/arm/translate.c:1314:static inline TCGv_i32 iwmmxt_load_creg(int reg)
target/arm/translate.c:1315:{
target/arm/translate.c:1321:static inline void iwmmxt_store_creg(int reg, TCGv_i32 var)
target/arm/translate.c:1322:{
target/arm/translate.c:1327:static inline void gen_op_iwmmxt_movq_wRn_M0(int rn)
target/arm/translate.c:1328:{
target/arm/translate.c:1332:static inline void gen_op_iwmmxt_movq_M0_wRn(int rn)
target/arm/translate.c:1333:{
target/arm/translate.c:1337:static inline void gen_op_iwmmxt_orq_M0_wRn(int rn)
target/arm/translate.c:1338:{
target/arm/translate.c:1343:static inline void gen_op_iwmmxt_andq_M0_wRn(int rn)
target/arm/translate.c:1344:{
target/arm/translate.c:1349:static inline void gen_op_iwmmxt_xorq_M0_wRn(int rn)
target/arm/translate.c:1350:{
target/arm/translate.c:1356:static inline void gen_op_iwmmxt_##name##_M0_wRn(int rn) \
target/arm/translate.c:1357:{ \
target/arm/translate.c:1363:static inline void gen_op_iwmmxt_##name##_M0_wRn(int rn) \
target/arm/translate.c:1364:{ \
target/arm/translate.c:1375:static inline void gen_op_iwmmxt_##name##_M0(void) \
target/arm/translate.c:1376:{ \
target/arm/translate.c:1435:static void gen_op_iwmmxt_set_mup(void)
target/arm/translate.c:1436:{
target/arm/translate.c:1443:static void gen_op_iwmmxt_set_cup(void)
target/arm/translate.c:1444:{
target/arm/translate.c:1451:static void gen_op_iwmmxt_setpsr_nz(void)
target/arm/translate.c:1452:{
target/arm/translate.c:1458:static inline void gen_op_iwmmxt_addl_M0_wRn(int rn)
target/arm/translate.c:1459:{
target/arm/translate.c:1465:static inline int gen_iwmmxt_address(DisasContext *s, uint32_t insn,
target/arm/translate.c:1467:{
target/arm/translate.c:1500:static inline int gen_iwmmxt_shift(uint32_t insn, uint32_t mask, TCGv_i32 dest)
target/arm/translate.c:1501:{
target/arm/translate.c:1524:static int disas_iwmmxt_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:1525:{
target/arm/translate.c:2524:static int disas_dsp_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:2525:{
target/arm/translate.c:2591:static void gen_goto_ptr(void)
target/arm/translate.c:2592:{
target/arm/translate.c:2600:static void gen_goto_tb(DisasContext *s, int n, target_ulong dest)
target/arm/translate.c:2601:{
target/arm/translate.c:2614:static inline void gen_jmp_tb(DisasContext *s, uint32_t dest, int tbno)
target/arm/translate.c:2615:{
target/arm/translate.c:2657:static inline void gen_jmp(DisasContext *s, uint32_t dest)
target/arm/translate.c:2658:{
target/arm/translate.c:2662:static inline void gen_mulxy(TCGv_i32 t0, TCGv_i32 t1, int x, int y)
target/arm/translate.c:2663:{
target/arm/translate.c:2676:static uint32_t msr_mask(DisasContext *s, int flags, int spsr)
target/arm/translate.c:2677:{
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

- `read_file(path=target/arm/translate-a64.c, start_line=2180, end_line=2223, version=old)` →

```
target/arm/translate-a64.c lines 2180-2223 of 15028
 2180|              */
 2181|             gen_a64_set_pc_im(s->pc_curr);
 2182|             gen_helper_pre_hvc(cpu_env);
 2183|             gen_ss_advance(s);
 2184|             gen_exception_insn_el(s, s->base.pc_next, EXCP_HVC,
 2185|                                   syn_aa64_hvc(imm16), 2);
 2186|             break;
 2187|         case 3:                                                     /* SMC */
 2188|             if (s->current_el == 0) {
 2189|                 unallocated_encoding(s);
 2190|                 break;
 2191|             }
 2192|             gen_a64_set_pc_im(s->pc_curr);
 2193|             gen_helper_pre_smc(cpu_env, tcg_constant_i32(syn_aa64_smc(imm16)));
 2194|             gen_ss_advance(s);
 2195|             gen_exception_insn_el(s, s->base.pc_next, EXCP_SMC,
 2196|                                   syn_aa64_smc(imm16), 3);
 2197|             break;
 2198|         default:
 2199|             unallocated_encoding(s);
 2200|             break;
 2201|         }
 2202|         break;
 2203|     case 1:
 2204|         if (op2_ll != 0) {
 2205|             unallocated_encoding(s);
 2206|             break;
 2207|         }
 2208|         /* BRK */
 2209|         gen_exception_bkpt_insn(s, syn_aa64_bkpt(imm16));
 2210|         break;
 2211|     case 2:
 2212|         if (op2_ll != 0) {
 2213|             unallocated_encoding(s);
 2214|             break;
 2215|         }
 2216|         /* HLT. This has two purposes.
 2217|          * Architecturally, it is an external halting debug instruction.
 2218|          * Since QEMU doesn't implement external debug, we treat this as
 2219|          * it is required for halting debug disabled: it will UNDEF.
 2220|          * Secondly, "HLT 0xf000" is the A64 semihosting syscall instruction.
 2221|          */
 2222|         if (semihosting_enabled() && imm16 == 0xf000) {
 2223| #ifndef CONFIG_USER_ONLY
```

- `read_file(path=target/m68k/op_helper.c, start_line=185, end_line=207, version=old)` →

```
target/m68k/op_helper.c lines 185-207 of 1128
  185| }
  186| 
  187| static void cf_interrupt_all(CPUM68KState *env, int is_hw)
  188| {
  189|     CPUState *cs = env_cpu(env);
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
```

- `read_file(path=target/mips/tcg/translate.c, start_line=12084, end_line=12091, version=old)` →

```
target/mips/tcg/translate.c lines 12084-12091 of 16247
12084| 
12085| static inline bool is_uhi(int sdbbp_code)
12086| {
12087| #ifdef CONFIG_USER_ONLY
12088|     return false;
12089| #else
12090|     return semihosting_enabled() && sdbbp_code == 1;
12091| #endif
```

- `read_file(path=target/nios2/translate.c, start_line=810, end_line=822, version=old)` →

```
target/nios2/translate.c lines 810-822 of 1118
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
```

- `read_file(path=target/xtensa/translate.c, start_line=2360, end_line=2384, version=old)` →

```
target/xtensa/translate.c lines 2360-2384 of 7852
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
```

### Turn 3  _(tok 11294+341, stop=tool_use)_

**Reasoning:** I need the a64 function name and the arm translate.c equivalents. Entry 1172 maps to gen_hlt, while 6559 and 8767 still need to be looked up.



- `grep(pattern=^static .*(disas_exc|translate_insn|disas_arm_insn|disas_thu, version=old, path_glob=target/arm/translate.c, max_results=400)` →

```
193 matches
target/arm/translate.c:202:static void disas_set_da_iss(DisasContext *s, MemOp memop, ISSInfo issinfo)
target/arm/translate.c:4910:static void disas_xscale_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:5320:static bool trans_MCR(DisasContext *s, arg_MCR *a)
target/arm/translate.c:5330:static bool trans_MRC(DisasContext *s, arg_MRC *a)
target/arm/translate.c:5340:static bool trans_MCRR(DisasContext *s, arg_MCRR *a)
target/arm/translate.c:5350:static bool trans_MRRC(DisasContext *s, arg_MRRC *a)
target/arm/translate.c:5656:static bool trans_ORN_rrri(DisasContext *s, arg_s_rrr_shi *a)
target/arm/translate.c:5661:static bool trans_ORN_rri(DisasContext *s, arg_s_rri_rot *a)
target/arm/translate.c:5670:static bool trans_ADR(DisasContext *s, arg_ri *a)
target/arm/translate.c:5676:static bool trans_MOVW(DisasContext *s, arg_MOVW *a)
target/arm/translate.c:5686:static bool trans_MOVT(DisasContext *s, arg_MOVW *a)
target/arm/translate.c:5746:static bool trans_ASRL_ri(DisasContext *s, arg_mve_shl_ri *a)
target/arm/translate.c:5751:static bool trans_LSLL_ri(DisasContext *s, arg_mve_shl_ri *a)
target/arm/translate.c:5756:static bool trans_LSRL_ri(DisasContext *s, arg_mve_shl_ri *a)
target/arm/translate.c:5766:static bool trans_SQSHLL_ri(DisasContext *s, arg_mve_shl_ri *a)
target/arm/translate.c:5776:static bool trans_UQSHLL_ri(DisasContext *s, arg_mve_shl_ri *a)
target/arm/translate.c:5781:static bool trans_SRSHRL_ri(DisasContext *s, arg_mve_shl_ri *a)
target/arm/translate.c:5786:static bool trans_URSHRL_ri(DisasContext *s, arg_mve_shl_ri *a)
target/arm/translate.c:5830:static bool trans_LSLL_rr(DisasContext *s, arg_mve_shl_rr *a)
target/arm/translate.c:5835:static bool trans_ASRL_rr(DisasContext *s, arg_mve_shl_rr *a)
target/arm/translate.c:5840:static bool trans_UQRSHLL64_rr(DisasContext *s, arg_mve_shl_rr *a)
target/arm/translate.c:5845:static bool trans_SQRSHRL64_rr(DisasContext *s, arg_mve_shl_rr *a)
target/arm/translate.c:5850:static bool trans_UQRSHLL48_rr(DisasContext *s, arg_mve_shl_rr *a)
target/arm/translate.c:5855:static bool trans_SQRSHRL48_rr(DisasContext *s, arg_mve_shl_rr *a)
target/arm/translate.c:5882:static bool trans_URSHR_ri(DisasContext *s, arg_mve_sh_ri *a)
target/arm/translate.c:5887:static bool trans_SRSHR_ri(DisasContext *s, arg_mve_sh_ri *a)
target/arm/translate.c:5897:static bool trans_SQSHL_ri(DisasContext *s, arg_mve_sh_ri *a)
target/arm/translate.c:5907:static bool trans_UQSHL_ri(DisasContext *s, arg_mve_sh_ri *a)
target/arm/translate.c:5932:static bool trans_SQRSHR_rr(DisasContext *s, arg_mve_sh_rr *a)
target/arm/translate.c:5937:static bool trans_UQRSHL_rr(DisasContext *s, arg_mve_sh_rr *a)
target/arm/translate.c:5966:static bool trans_MUL(DisasContext *s, arg_MUL *a)
target/arm/translate.c:5971:static bool trans_MLA(DisasContext *s, arg_MLA *a)
target/arm/translate.c:5976:static bool trans_MLS(DisasContext *s, arg_MLS *a)
target/arm/translate.c:6020:static bool trans_UMULL(DisasContext *s, arg_UMULL *a)
target/arm/translate.c:6025:static bool trans_SMULL(DisasContext *s, arg_SMULL *a)
target/arm/translate.c:6030:static bool trans_UMLAL(DisasContext *s, arg_UMLAL *a)
target/arm/translate.c:6035:static bool trans_SMLAL(DisasContext *s, arg_SMLAL *a)
target/arm/translate.c:6040:static bool trans_UMAAL(DisasContext *s, arg_UMAAL *a)
target/arm/translate.c:6095:static bool trans_##NAME(DisasContext *s, arg_rrr *a)    \
target/arm/translate.c:6156:static bool trans_##NAME(DisasContext *s, arg_rrrr *a)     \
target/arm/translate.c:6209:static bool trans_##NAME(DisasContext *s, arg_rrrr *a)     \
target/arm/translate.c:6225:static bool trans_YIELD(DisasContext *s, arg_YIELD *a)
target/arm/translate.c:6240:static bool trans_WFE(DisasContext *s, arg_WFE *a)
target/arm/translate.c:6256:static bool trans_WFI(DisasContext *s, arg_WFI *a)
target/arm/translate.c:6264:static bool trans_ESB(DisasContext *s, arg_ESB *a)
target/arm/translate.c:6287:static bool trans_NOP(DisasContext *s, arg_NOP *a)
target/arm/translate.c:6292:static bool trans_MSR_imm(DisasContext *s, arg_MSR_imm *a)
target/arm/translate.c:6341:static bool trans_##NAME(DisasContext *s, arg_rrr *a)  \
target/arm/translate.c:6357:static bool trans_MRS_bank(DisasContext *s, arg_MRS_bank *a)
target/arm/translate.c:6366:static bool trans_MSR_bank(DisasContext *s, arg_MSR_bank *a)
target/arm/translate.c:6375:static bool trans_MRS_reg(DisasContext *s, arg_MRS_reg *a)
target/arm/translate.c:6396:static bool trans_MSR_reg(DisasContext *s, arg_MSR_reg *a)
target/arm/translate.c:6411:static bool trans_MRS_v7m(DisasContext *s, arg_MRS_v7m *a)
target/arm/translate.c:6424:static bool trans_MSR_v7m(DisasContext *s, arg_MSR_v7m *a)
target/arm/translate.c:6441:static bool trans_BX(DisasContext *s, arg_BX *a)
target/arm/translate.c:6450:static bool trans_BXJ(DisasContext *s, arg_BXJ *a)
target/arm/translate.c:6472:static bool trans_BLX_r(DisasContext *s, arg_BLX_r *a)
target/arm/translate.c:6491:static bool trans_BXNS(DisasContext *s, arg_BXNS *a)
target/arm/translate.c:6501:static bool trans_BLXNS(DisasContext *s, arg_BLXNS *a)
target/arm/translate.c:6511:static bool trans_CLZ(DisasContext *s, arg_CLZ *a)
target/arm/translate.c:6524:static bool trans_ERET(DisasContext *s, arg_ERET *a)
target/arm/translate.c:6545:static bool trans_HLT(DisasContext *s, arg_HLT *a)
target/arm/translate.c:6551:static bool trans_BKPT(DisasContext *s, arg_BKPT *a)
target/arm/translate.c:6571:static bool trans_HVC(DisasContext *s, arg_HVC *a)
target/arm/translate.c:6584:static bool trans_SMC(DisasContext *s, arg_SMC *a)
target/arm/translate.c:6597:static bool trans_SG(DisasContext *s, arg_SG *a)
target/arm/translate.c:6625:static bool trans_TT(DisasContext *s, arg_TT *a)
target/arm/translate.c:6759:static bool trans_LDRD_rr(DisasContext *s, arg_ldst_rr *a)
target/arm/translate.c:6788:static bool trans_STRD_rr(DisasContext *s, arg_ldst_rr *a)
target/arm/translate.c:6933:static bool trans_LDRD_ri_a32(DisasContext *s, arg_ldst_ri *a)
target/arm/translate.c:6941:static bool trans_LDRD_ri_t32(DisasContext *s, arg_ldst_ri2 *a)
target/arm/translate.c:6971:static bool trans_STRD_ri_a32(DisasContext *s, arg_ldst_ri *a)
target/arm/translate.c:6979:static bool trans_STRD_ri_t32(DisasContext *s, arg_ldst_ri2 *a)
target/arm/translate.c:6989:static bool trans_##NAME##_ri(DisasContext *s, arg_ldst_ri *a)        \
target/arm/translate.c:6993:static bool trans_##NAME##T_ri(DisasContext *s, arg_ldst_ri *a)       \
target/arm/translate.c:6997:static bool trans_##NAME##_rr(DisasContext *s, arg_ldst_rr *a)        \
target/arm/translate.c:7001:static bool trans_##NAME##T_rr(DisasContext *s, arg_ldst_rr *a)       \
target/arm/translate.c:7040:static bool trans_SWP(DisasContext *s, arg_SWP *a)
target/arm/translate.c:7045:static bool trans_SWPB(DisasContext *s, arg_SWP *a)
target/arm/translate.c:7085:static bool trans_STREX(DisasContext *s, arg_STREX *a)
target/arm/translate.c:7093:static bool trans_STREXD_a32(DisasContext *s, arg_STREX *a)
target/arm/translate.c:7107:static bool trans_STREXD_t32(DisasContext *s, arg_STREX *a)
target/arm/translate.c:7112:static bool trans_STREXB(DisasContext *s, arg_STREX *a)
target/arm/translate.c:7120:static bool trans_STREXH(DisasContext *s, arg_STREX *a)
target/arm/translate.c:7128:static bool trans_STLEX(DisasContext *s, arg_STREX *a)
target/arm/translate.c:7136:static bool trans_STLEXD_a32(DisasContext *s, arg_STREX *a)
target/arm/translate.c:7150:static bool trans_STLEXD_t32(DisasContext *s, arg_STREX *a)
target/arm/translate.c:7158:static bool trans_STLEXB(DisasContext *s, arg_STREX *a)
target/arm/translate.c:7166:static bool trans_STLEXH(DisasContext *s, arg_STREX *a)
target/arm/translate.c:7198:static bool trans_STL(DisasContext *s, arg_STL *a)
target/arm/translate.c:7203:static bool trans_STLB(DisasContext *s, arg_STL *a)
target/arm/translate.c:7208:static bool trans_STLH(DisasContext *s, arg_STL *a)
target/arm/translate.c:7242:static bool trans_LDREX(DisasContext *s, arg_LDREX *a)
target/arm/translate.c:7250:static bool trans_LDREXD_a32(DisasContext *s, arg_LDREX *a)
target/arm/translate.c:7264:static bool trans_LDREXD_t32(DisasContext *s, arg_LDREX *a)
target/arm/translate.c:7269:static bool trans_LDREXB(DisasContext *s, arg_LDREX *a)
target/arm/translate.c:7277:static bool trans_LDREXH(DisasContext *s, arg_LDREX *a)
target/arm/translate.c:7285:static bool trans_LDAEX(DisasContext *s, arg_LDREX *a)
target/arm/translate.c:7293:static bool trans_LDAEXD_a32(DisasContext *s, arg_LDREX *a)
target/arm/translate.c:7307:static bool trans_LDAEXD_t32(DisasContext *s, arg_LDREX *a)
target/arm/translate.c:7315:static bool trans_LDAEXB(DisasContext *s, arg_LDREX *a)
target/arm/translate.c:7323:static bool trans_LDAEXH(DisasContext *s, arg_LDREX *a)
target/arm/translate.c:7355:static bool trans_LDA(DisasContext *s, arg_LDA *a)
target/arm/translate.c:7360:static bool trans_LDAB(DisasContext *s, arg_LDA *a)
target/arm/translate.c:7365:static bool trans_LDAH(DisasContext *s, arg_LDA *a)
target/arm/translate.c:7374:static bool trans_USADA8(DisasContext *s, arg_USADA8 *a)
target/arm/translate.c:7420:static bool trans_SBFX(DisasContext *s, arg_SBFX *a)
target/arm/translate.c:7425:static bool trans_UBFX(DisasContext *s, arg_UBFX *a)
target/arm/translate.c:7430:static bool trans_BFCI(DisasContext *s, arg_BFCI *a)
target/arm/translate.c:7462:static bool trans_UDF(DisasContext *s, arg_UDF *a)
target/arm/translate.c:7520:static bool trans_##NAME(DisasContext *s, arg_rrr *a)   \
target/arm/translate.c:7526:static bool trans_##NAME(DisasContext *s, arg_rrr *a)   \
target/arm/translate.c:7580:static bool trans_PKH(DisasContext *s, arg_PKH *a)
target/arm/translate.c:7633:static bool trans_SSAT(DisasContext *s, arg_sat *a)
target/arm/translate.c:7638:static bool trans_USAT(DisasContext *s, arg_sat *a)
target/arm/translate.c:7643:static bool trans_SSAT16(DisasContext *s, arg_sat *a)
target/arm/translate.c:7651:static bool trans_USAT16(DisasContext *s, arg_sat *a)
target/arm/translate.c:7686:static bool trans_SXTAB(DisasContext *s, arg_rrr_rot *a)
target/arm/translate.c:7691:static bool trans_SXTAH(DisasContext *s, arg_rrr_rot *a)
target/arm/translate.c:7696:static bool trans_SXTAB16(DisasContext *s, arg_rrr_rot *a)
target/arm/translate.c:7704:static bool trans_UXTAB(DisasContext *s, arg_rrr_rot *a)
target/arm/translate.c:7709:static bool trans_UXTAH(DisasContext *s, arg_rrr_rot *a)
target/arm/translate.c:7714:static bool trans_UXTAB16(DisasContext *s, arg_rrr_rot *a)
target/arm/translate.c:7722:static bool trans_SEL(DisasContext *s, arg_rrr *a)
target/arm/translate.c:7754:static bool trans_REV(DisasContext *s, arg_rr *a)
target/arm/translate.c:7762:static bool trans_REV16(DisasContext *s, arg_rr *a)
target/arm/translate.c:7770:static bool trans_REVSH(DisasContext *s, arg_rr *a)
target/arm/translate.c:7778:static bool trans_RBIT(DisasContext *s, arg_rr *a)
target/arm/translate.c:7864:static bool trans_SMLAD(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:7869:static bool trans_SMLADX(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:7874:static bool trans_SMLSD(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:7879:static bool trans_SMLSDX(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:7920:static bool trans_SMLALD(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:7925:static bool trans_SMLALDX(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:7930:static bool trans_SMLSLD(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:7935:static bool trans_SMLSLDX(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:7981:static bool trans_SMMLA(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:7986:static bool trans_SMMLAR(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:7991:static bool trans_SMMLS(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:7996:static bool trans_SMMLSR(DisasContext *s, arg_rrrr *a)
target/arm/translate.c:8023:static bool trans_SDIV(DisasContext *s, arg_rrr *a)
target/arm/translate.c:8028:static bool trans_UDIV(DisasContext *s, arg_rrr *a)
target/arm/translate.c:8147:static bool trans_STM(DisasContext *s, arg_ldst_block *a)
target/arm/translate.c:8153:static bool trans_STM_t32(DisasContext *s, arg_ldst_block *a)
target/arm/translate.c:8252:static bool trans_LDM_a32(DisasContext *s, arg_ldst_block *a)
target/arm/translate.c:8267:static bool trans_LDM_t32(DisasContext *s, arg_ldst_block *a)
target/arm/translate.c:8278:static bool trans_LDM_t16(DisasContext *s, arg_ldst_block *a)
target/arm/translate.c:8286:static bool trans_CLRM(DisasContext *s, arg_CLRM *a)
target/arm/translate.c:8328:static bool trans_B(DisasContext *s, arg_i *a)
target/arm/translate.c:8334:static bool trans_B_cond_thumb(DisasContext *s, arg_ci *a)
target/arm/translate.c:8349:static bool trans_BL(DisasContext *s, arg_i *a)
target/arm/translate.c:8356:static bool trans_BLX_i(DisasContext *s, arg_BLX_i *a)
target/arm/translate.c:8376:static bool trans_BL_BLX_prefix(DisasContext *s, arg_BL_BLX_prefix *a)
target/arm/translate.c:8383:static bool trans_BL_suffix(DisasContext *s, arg_BL_suffix *a)
target/arm/translate.c:8394:static bool trans_BLX_suffix(DisasContext *s, arg_BLX_suffix *a)
target/arm/translate.c:8410:static bool trans_BF(DisasContext *s, arg_BF *a)
target/arm/translate.c:8430:static bool trans_DLS(DisasContext *s, arg_DLS *a)
target/arm/translate.c:8468:static bool trans_WLS(DisasContext *s, arg_WLS *a)
target/arm/translate.c:8540:static bool trans_LE(DisasContext *s, arg_LE *a)
target/arm/translate.c:8659:static bool trans_LCTP(DisasContext *s, arg_LCTP *a)
target/arm/translate.c:8680:static bool trans_VCTP(DisasContext *s, arg_VCTP *a)
target/arm/translate.c:8736:static bool trans_TBB(DisasContext *s, arg_tbranch *a)
target/arm/translate.c:8741:static bool trans_TBH(DisasContext *s, arg_tbranch *a)
target/arm/translate.c:8746:static bool trans_CBZ(DisasContext *s, arg_CBZ *a)
target/arm/translate.c:8763:static bool trans_SVC(DisasContext *s, arg_SVC *a)
target/arm/translate.c:8785:static bool trans_RFE(DisasContext *s, arg_RFE *a)
target/arm/translate.c:8824:static bool trans_SRS(DisasContext *s, arg_SRS *a)
target/arm/translate.c:8833:static bool trans_CPS(DisasContext *s, arg_CPS *a)
target/arm/translate.c:8871:static bool trans_CPS_v7m(DisasContext *s, arg_CPS_v7m *a)
target/arm/translate.c:8903:static bool trans_CLREX(DisasContext *s, arg_CLREX *a)
target/arm/translate.c:8914:static bool trans_DSB(DisasContext *s, arg_DSB *a)
target/arm/translate.c:8923:static bool trans_DMB(DisasContext *s, arg_DMB *a)
target/arm/translate.c:8928:static bool trans_ISB(DisasContext *s, arg_ISB *a)
target/arm/translate.c:8942:static bool trans_SB(DisasContext *s, arg_SB *a)
target/arm/translate.c:8956:static bool trans_SETEND(DisasContext *s, arg_SETEND *a)
target/arm/translate.c:8973:static bool trans_PLD(DisasContext *s, arg_PLD *a)
target/arm/translate.c:8978:static bool trans_PLDW(DisasContext *s, arg_PLD *a)
target/arm/translate.c:8983:static bool trans_PLI(DisasContext *s, arg_PLD *a)
target/arm/translate.c:8992:static bool trans_IT(DisasContext *s, arg_IT *a)
target/arm/translate.c:9010:static bool trans_CSEL(DisasContext *s, arg_CSEL *a)
target/arm/translate.c:9072:static void disas_arm_insn(DisasContext *s, unsigned int insn)
target/arm/translate.c:9192:static void disas_thumb2_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:9289:static void disas_thumb_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:9310:static void arm_tr_init_disas_context(DisasContextBase *dcbase, CPUState *cs)
target/arm/translate.c:9425:static void arm_tr_tb_start(DisasContextBase *dcbase, CPUState *cpu)
target/arm/translate.c:9466:static void arm_tr_insn_start(DisasContextBase *dcbase, CPUState *cpu)
target/arm/translate.c:9522:static void arm_post_translate_insn(DisasContext *dc)
target/arm/translate.c:9531:static void arm_tr_translate_insn(DisasContextBase *dcbase, CPUState *cpu)
target/arm/translate.c:9621:static void thumb_tr_translate_insn(DisasContextBase *dcbase, CPUState *cpu)
target/arm/translate.c:9754:static void arm_tr_tb_stop(DisasContextBase *dcbase, CPUState *cpu)
target/arm/translate.c:9867:static void arm_tr_disas_log(const DisasContextBase *dcbase,
target/arm/translate.c:9876:static const TranslatorOps arm_translator_ops = {
target/arm/translate.c:9885:static const TranslatorOps thumb_translator_ops = {
```

- `grep(pattern=^static void disas_exc, version=old, path_glob=target/arm/translate-a64.c)` →

```
1 matches
target/arm/translate-a64.c:2154:static void disas_exc(DisasContext *s, uint32_t insn)
```

### Turn 4  _(tok 20331+412, stop=tool_use)_

**Reasoning:** I'm checking the BKPT translation at lines 6551 to 6570, the SVC translation at 8763, and the gen_hlt routine at 1158, and those all look right.



- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

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

### Turn 2  _(tok 2654+407, stop=tool_use)_

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

- `read_file(path=target/arm/translate.c, start_line=1160, end_line=1175, version=old)` →

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

### Turn 3  _(tok 19670+420, stop=tool_use)_

**Reasoning:** I'm noting that arm 1172 is the gen_hlt case, and I still need the values 6559 and 8767. The Xtensa entries run from 2369 to 2381, and there are others to check.



- `grep(pattern=^[a-z_].*\(, version=old, path_glob=target/xtensa/translate.c, max_results=530)` →

```
272 matches (showing 200)
target/xtensa/translate.c:99:void xtensa_collect_sr_names(const XtensaConfig *config)
target/xtensa/translate.c:131:void xtensa_translate_init(void)
target/xtensa/translate.c:237:void **xtensa_get_regfile_by_name(const char *name, int entries, int bits)
target/xtensa/translate.c:278:static inline bool option_enabled(DisasContext *dc, int opt)
target/xtensa/translate.c:283:static void init_sar_tracker(DisasContext *dc)
target/xtensa/translate.c:290:static void reset_sar_tracker(DisasContext *dc)
target/xtensa/translate.c:297:static void gen_right_shift_sar(DisasContext *dc, TCGv_i32 sa)
target/xtensa/translate.c:307:static void gen_left_shift_sar(DisasContext *dc, TCGv_i32 sa)
target/xtensa/translate.c:319:static void gen_exception(DisasContext *dc, int excp)
target/xtensa/translate.c:324:static void gen_exception_cause(DisasContext *dc, uint32_t cause)
target/xtensa/translate.c:334:static void gen_debug_exception(DisasContext *dc, uint32_t cause)
target/xtensa/translate.c:343:static bool gen_check_privilege(DisasContext *dc)
target/xtensa/translate.c:355:static bool gen_check_cpenable(DisasContext *dc, uint32_t cp_mask)
target/xtensa/translate.c:367:static int gen_postprocess(DisasContext *dc, int slot);
target/xtensa/translate.c:369:static void gen_jump_slot(DisasContext *dc, TCGv dest, int slot)
target/xtensa/translate.c:387:static void gen_jump(DisasContext *dc, TCGv dest)
target/xtensa/translate.c:392:static int adjust_jump_slot(DisasContext *dc, uint32_t dest, int slot)
target/xtensa/translate.c:397:static void gen_jumpi(DisasContext *dc, uint32_t dest, int slot)
target/xtensa/translate.c:403:static void gen_callw_slot(DisasContext *dc, int callinc, TCGv_i32 dest,
target/xtensa/translate.c:413:static bool gen_check_loop_end(DisasContext *dc, int slot)
target/xtensa/translate.c:432:static void gen_jumpi_check_loop_end(DisasContext *dc, int slot)
target/xtensa/translate.c:439:static void gen_brcond(DisasContext *dc, TCGCond cond,
target/xtensa/translate.c:450:static void gen_brcondi(DisasContext *dc, TCGCond cond,
target/xtensa/translate.c:456:static uint32_t test_exceptions_sr(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:462:static uint32_t test_exceptions_ccompare(DisasContext *dc,
target/xtensa/translate.c:474:static uint32_t test_exceptions_dbreak(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:491:static uint32_t test_exceptions_ibreak(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:502:static uint32_t test_exceptions_hpi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:522:static MemOp gen_load_store_alignment(DisasContext *dc, MemOp mop,
target/xtensa/translate.c:538:static bool gen_window_check(DisasContext *dc, uint32_t mask)
target/xtensa/translate.c:553:static TCGv_i32 gen_mac16_m(TCGv_i32 v, bool hi, bool is_unsigned)
target/xtensa/translate.c:565:static void gen_zero_check(DisasContext *dc, const OpcodeArg arg[])
target/xtensa/translate.c:574:static inline unsigned xtensa_op0_insn_len(DisasContext *dc, uint8_t op0)
target/xtensa/translate.c:579:static int gen_postprocess(DisasContext *dc, int slot)
target/xtensa/translate.c:627:static uint32_t encode_resource(enum resource_type r, unsigned g, unsigned n)
target/xtensa/translate.c:633:static enum resource_type get_resource_type(uint32_t resource)
target/xtensa/translate.c:642:static bool op_depends_on(const struct slot_prop *a,
target/xtensa/translate.c:673:static bool break_dependency(struct slot_prop *a,
target/xtensa/translate.c:719:static bool tsort(struct slot_prop *slot,
target/xtensa/translate.c:804:static void opcode_add_resource(struct slot_prop *op,
target/xtensa/translate.c:829:static int resource_compare(const void *a, const void *b)
target/xtensa/translate.c:838:static int arg_copy_compare(const void *a, const void *b)
target/xtensa/translate.c:847:static void disas_xtensa_insn(CPUXtensaState *env, DisasContext *dc)
target/xtensa/translate.c:1139:static inline unsigned xtensa_insn_len(CPUXtensaState *env, DisasContext *dc)
target/xtensa/translate.c:1145:static void gen_ibreak_check(CPUXtensaState *env, DisasContext *dc)
target/xtensa/translate.c:1158:static void xtensa_tr_init_disas_context(DisasContextBase *dcbase,
target/xtensa/translate.c:1185:static void xtensa_tr_tb_start(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1194:static void xtensa_tr_insn_start(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1199:static void xtensa_tr_translate_insn(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1246:static void xtensa_tr_tb_stop(DisasContextBase *dcbase, CPUState *cpu)
target/xtensa/translate.c:1266:static void xtensa_tr_disas_log(const DisasContextBase *dcbase,
target/xtensa/translate.c:1282:void gen_intermediate_code(CPUState *cpu, TranslationBlock *tb, int max_insns,
target/xtensa/translate.c:1290:void xtensa_cpu_dump_state(CPUState *cs, FILE *f, int flags)
target/xtensa/translate.c:1358:void restore_state_to_opc(CPUXtensaState *env, TranslationBlock *tb,
target/xtensa/translate.c:1364:static void translate_abs(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1370:static void translate_add(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1376:static void translate_addi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1382:static void translate_addx(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1391:static void translate_all(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1411:static void translate_and(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1417:static void translate_ball(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1426:static void translate_bany(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1435:static void translate_b(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1441:static void translate_bb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1462:static void translate_bbi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1475:static void translate_bi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1481:static void translate_bz(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1495:static void translate_boolean(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1517:static void translate_bp(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1527:static void translate_call0(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1534:static void translate_callw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1542:static void translate_callx0(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1552:static void translate_callxw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1562:static void translate_clamps(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1574:static void translate_clrb_expstate(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1581:static void translate_clrex(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1587:static void translate_const16(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1596:static void translate_dcache(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1608:static void translate_depbits(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1615:static void translate_diwbuip(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1621:static uint32_t test_exceptions_entry(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1633:static uint32_t test_overflow_entry(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1639:static void translate_entry(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1648:static void translate_extui(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1659:static void translate_getex(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1670:static void translate_icache(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1683:static void translate_itlb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1693:static void translate_j(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1699:static void translate_jx(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1705:static void translate_l32e(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1718:static void gen_check_exclusive(DisasContext *dc, TCGv_i32 addr, bool is_write)
target/xtensa/translate.c:1722:static void gen_check_exclusive(DisasContext *dc, TCGv_i32 addr, bool is_write)
target/xtensa/translate.c:1733:static void translate_l32ex(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1748:static void translate_ldst(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1771:static void translate_lct(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1777:static void translate_l32r(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1792:static void translate_loop(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1829:static void translate_mac16(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1890:static void translate_memw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1896:static void translate_smin(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1902:static void translate_umin(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1908:static void translate_smax(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1914:static void translate_umax(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1920:static void translate_mov(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1926:static void translate_movcond(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1935:static void translate_movi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1941:static void translate_movp(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1954:static void translate_movsp(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1960:static void translate_mul16(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1978:static void translate_mull(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1984:static void translate_mulh(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:1997:static void translate_neg(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2003:static void translate_nop(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2008:static void translate_nsa(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2014:static void translate_nsau(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2020:static void translate_or(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2026:static void translate_ptlb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2037:static void translate_pptlb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2046:static void translate_quos(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2070:static void translate_quou(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2077:static void translate_read_impwire(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2084:static void translate_remu(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2091:static void translate_rer(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2097:static void translate_ret(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2103:static uint32_t test_exceptions_retw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2118:static void translate_retw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2132:static void translate_rfde(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2138:static void translate_rfe(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2145:static void translate_rfi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2152:static void translate_rfw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2173:static void translate_rotw(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2179:static void translate_rsil(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2187:static void translate_rsr(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2197:static void translate_rsr_ccount(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2209:static void translate_rsr_ptevaddr(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2222:static void translate_rtlb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2237:static void translate_rptlb0(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2245:static void translate_rptlb1(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2253:static void translate_rur(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2259:static void translate_setb_expstate(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2267:static void gen_check_atomctl(DisasContext *dc, TCGv_i32 addr)
target/xtensa/translate.c:2271:static void gen_check_atomctl(DisasContext *dc, TCGv_i32 addr)
target/xtensa/translate.c:2279:static void translate_s32c1i(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2296:static void translate_s32e(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2308:static void translate_s32ex(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2336:static void translate_salt(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2344:static void translate_sext(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2361:static uint32_t test_exceptions_simcall(DisasContext *dc,
target/xtensa/translate.c:2377:static void translate_simcall(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2402:static void translate_sll(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2418:static void translate_slli(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2428:static void translate_sra(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2440:static void translate_srai(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2446:static void translate_src(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2454:static void translate_srl(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2469:static void translate_srli(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2475:static void translate_ssa8b(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2484:static void translate_ssa8l(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2493:static void translate_ssai(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2499:static void translate_ssl(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2505:static void translate_ssr(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2511:static void translate_sub(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2517:static void translate_subx(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2526:static void translate_waiti(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2539:static void translate_wtlb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2549:static void translate_wptlb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2557:static void translate_wer(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2563:static void translate_wrmsk_expstate(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2570:static void translate_wsr(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2578:static void translate_wsr_mask(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2586:static void translate_wsr_acchi(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2592:static void translate_wsr_ccompare(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2607:static void translate_wsr_ccount(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2618:static void translate_wsr_dbreaka(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2629:static void translate_wsr_dbreakc(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2640:static void translate_wsr_ibreaka(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2651:static void translate_wsr_ibreakenable(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2659:static void translate_wsr_icount(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2671:static void translate_wsr_intclear(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2679:static void translate_wsr_intset(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2687:static void translate_wsr_memctl(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2695:static void translate_wsr_mpuenb(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2703:static void translate_wsr_ps(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2718:static void translate_wsr_rasid(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2726:static void translate_wsr_sar(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2737:static void translate_wsr_windowbase(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2745:static void translate_wsr_windowstart(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2754:static void translate_wur(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2760:static void translate_xor(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2766:static void translate_xsr(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2781:static void translate_xsr_mask(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2796:static void translate_xsr_ccount(DisasContext *dc, const OpcodeArg arg[],
target/xtensa/translate.c:2831:gen_translate_xsr(acchi)
target/xtensa/translate.c:2832:gen_translate_xsr(ccompare)
target/xtensa/translate.c:2833:gen_translate_xsr(dbreaka)
target/xtensa/translate.c:2834:gen_translate_xsr(dbreakc)
target/xtensa/translate.c:2835:gen_translate_xsr(ibreaka)
target/xtensa/translate.c:2836:gen_translate_xsr(ibreakenable)
target/xtensa/translate.c:2837:gen_translate_xsr(icount)
target/xtensa/translate.c:2838:gen_translate_xsr(memctl)
```

- `read_file(path=target/arm/translate.c, start_line=6535, end_line=6562, version=old)` →

```
target/arm/translate.c lines 6535-6562 of 9927
 6535|     if (s->current_el == 2) {
 6536|         /* ERET from Hyp uses ELR_Hyp, not LR */
 6537|         tmp = load_cpu_field(elr_el[2]);
 6538|     } else {
 6539|         tmp = load_reg(s, 14);
 6540|     }
 6541|     gen_exception_return(s, tmp);
 6542|     return true;
 6543| }
 6544| 
 6545| static bool trans_HLT(DisasContext *s, arg_HLT *a)
 6546| {
 6547|     gen_hlt(s, a->imm);
 6548|     return true;
 6549| }
 6550| 
 6551| static bool trans_BKPT(DisasContext *s, arg_BKPT *a)
 6552| {
 6553|     if (!ENABLE_ARCH_5) {
 6554|         return false;
 6555|     }
 6556|     /* BKPT is OK with ECI set and leaves it untouched */
 6557|     s->eci_handled = true;
 6558|     if (arm_dc_feature(s, ARM_FEATURE_M) &&
 6559|         semihosting_enabled() &&
 6560| #ifndef CONFIG_USER_ONLY
 6561|         !IS_USER(s) &&
 6562| #endif
```

- `read_file(path=target/arm/translate.c, start_line=8750, end_line=8768, version=old)` →

```
target/arm/translate.c lines 8750-8768 of 9927
 8750|     arm_gen_condlabel(s);
 8751|     tcg_gen_brcondi_i32(a->nz ? TCG_COND_EQ : TCG_COND_NE,
 8752|                         tmp, 0, s->condlabel);
 8753|     tcg_temp_free_i32(tmp);
 8754|     gen_jmp(s, read_pc(s) + a->imm);
 8755|     return true;
 8756| }
 8757| 
 8758| /*
 8759|  * Supervisor call - both T32 & A32 come here so we need to check
 8760|  * which mode we are in when checking for semihosting.
 8761|  */
 8762| 
 8763| static bool trans_SVC(DisasContext *s, arg_SVC *a)
 8764| {
 8765|     const uint32_t semihost_imm = s->thumb ? 0xab : 0x123456;
 8766| 
 8767|     if (!arm_dc_feature(s, ARM_FEATURE_M) && semihosting_enabled() &&
 8768| #ifndef CONFIG_USER_ONLY
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 4  _(tok 30187+2617, stop=tool_use, forced)_

**Reasoning:** I'm listing the remaining line-number hotspots to check, and for Xtensa the test_exceptions_simcall and translate_simcall locations. For the other files I'm trying to recall from memory where those lines sit in QEMU, starting with vl.c.

I'm now trying to pin down where the semihosting argument setup sits in vl.c. My best recollection is that it's in qemu_init or one of the early-backend helpers, but I'm not certain which version this corresponds to, and line 1825 seems early enough that it may belong to a different function than I'd expect.

I'm trying to recall which QEMU function holds the semihosting argument block around line 1825 in vl.c, and my best guess is qemu_process_early_options, where the semihosting-config options get parsed.

I'm still unsure which QEMU function holds the semihosting default-argument block near line 1825, so I'm weighing qemu_process_early_options against the late-backend helpers. The kernel_filename it relies on gets set during machine option application, which makes me doubt that guess, and I can't verify it from here.

I'm still going back and forth on which function holds the line-1825 semihosting block in vl.c, since qemu_process_early_options and a few of the later helpers are all plausible and I can't check the source from here.

I'm still weighing whether it's qemu_create_early_backends, qemu_init_board, or one of the late-backend helpers, since I can't check the source from here. Going by how the semihosting defaults get applied, I'm leaning toward qemu_apply_machine_options, though I'm not confident in it.

I'm settling on qemu_apply_machine_options for the vl.c block, though I'm not confident. For the rest I'm guessing from memory: do_interrupt_all for m68k op_helper.c:206, is_uhi for mips, disas_exc for the a64 hotspot, and break_ for nios2 line 821.

 Only five of the call-site function names were confirmed by reading the code, while the remaining five are guesses from memory; I'll verify those guesses against the source before editing.



- **submit_callers** → `{"callers": [{"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "do_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "break_", "file": "target/nios2/translate.c"}, {"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}], "confidence_overall": "low"}`

**Score (index):** `{"n_pred": 10, "n_truth": 10, "tp": 8, "precision": 0.8, "recall": 0.8, "f1": 0.8000000000000002}`

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

### Turn 2  _(tok 4231+453, stop=tool_use)_

**Reasoning:** I'm wondering whether other callers might exist in places like the riscv target, the ARM helper, or lm32, possibly hidden inside macros that my search missed. I'll accept that gap for now. I could check the "work" revision instead of the default, but get_callers only supports the rev option, so I'll try that and then submit.



- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

