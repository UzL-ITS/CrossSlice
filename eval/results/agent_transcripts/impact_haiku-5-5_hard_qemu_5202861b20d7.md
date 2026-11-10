# Impact-analysis transcript — qemu @ 5202861b20d7 — anthropic:claude-haiku-5-5

- target: `semihosting_enabled` (include/semihosting/semihost.h), arity 0->1
- truth: [['softmmu/vl.c', 'qemu_apply_machine_options'], ['target/arm/translate-a64.c', 'disas_exc'], ['target/arm/translate.c', 'gen_hlt'], ['target/arm/translate.c', 'trans_BKPT'], ['target/arm/translate.c', 'trans_SVC'], ['target/m68k/op_helper.c', 'cf_interrupt_all'], ['target/mips/tcg/translate.c', 'is_uhi'], ['target/nios2/translate.c', 'gen_break'], ['target/xtensa/translate.c', 'test_exceptions_simcall'], ['target/xtensa/translate.c', 'translate_simcall']]

## Self-navigation arm

### Turn 1  _(tok 1218+124, stop=tool_use)_

**Reasoning:** I'm searching the repo for every occurrence of semihosting_enabled to see where it's used.



- `grep(pattern=semihosting_enabled, version=old, max_results=500)` →

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

### Turn 2  _(tok 1872+1229, stop=tool_use)_

**Reasoning:** I need the enclosing function name for each match, so I'll read the surrounding code. The grep is searching for the name itself, so it should catch every call, though files outside git's tracked set could still be missed.



**Says:** The grep found 15 matches. I need the enclosing function for each call site, so I'll read the surrounding code.

- `read_file(path=softmmu/vl.c, version=old, start_line=1800, end_line=1830)` →

```
softmmu/vl.c lines 1800-1830 of 3593
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
 1827|         semihosting_arg_fallback(current_machine->kernel_filename, current_machine->kernel_cmdline);
 1828|     }
 1829| 
 1830|     if (current_machine->smp.cpus > 1) {
```

- `read_file(path=target/arm/translate-a64.c, version=old, start_line=2205, end_line=2225)` →

```
target/arm/translate-a64.c lines 2205-2225 of 15028
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
 2224|             /* In system mode, don't allow userspace access to semihosting,
 2225|              * to provide some semblance of security (and for consistency
```

- `read_file(path=target/arm/translate.c, version=old, start_line=1160, end_line=1180)` →

```
target/arm/translate.c lines 1160-1180 of 9927
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
 1176|         (imm == (s->thumb ? 0x3c : 0xf000))) {
 1177|         gen_exception_internal_insn(s, s->pc_curr, EXCP_SEMIHOST);
 1178|         return;
 1179|     }
 1180| 
```

- `read_file(path=target/arm/translate.c, version=old, start_line=6540, end_line=6565)` →

```
target/arm/translate.c lines 6540-6565 of 9927
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
 6563|         (a->imm == 0xab)) {
 6564|         gen_exception_internal_insn(s, s->pc_curr, EXCP_SEMIHOST);
 6565|     } else {
```

- `read_file(path=target/arm/translate.c, version=old, start_line=8750, end_line=8775)` →

```
target/arm/translate.c lines 8750-8775 of 9927
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
 8769|         !IS_USER(s) &&
 8770| #endif
 8771|         (a->imm == semihost_imm)) {
 8772|         gen_exception_internal_insn(s, s->pc_curr, EXCP_SEMIHOST);
 8773|     } else {
 8774|         gen_set_pc_im(s, s->base.pc_next);
 8775|         s->svc_imm = a->imm;
```

- `read_file(path=target/m68k/op_helper.c, version=old, start_line=190, end_line=215)` →

```
target/m68k/op_helper.c lines 190-215 of 1128
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
  211|                 env->pc += 4;
  212|                 do_m68k_semihosting(env, env->dregs[0]);
  213|                 return;
  214|             }
  215|             cs->halted = 1;
```

- `read_file(path=target/mips/tcg/translate.c, version=old, start_line=12075, end_line=12095)` →

```
target/mips/tcg/translate.c lines 12075-12095 of 16247
12075|                                 int16_t offset)
12076| {
12077|     TCGv_i32 t0 = tcg_const_i32(op);
12078|     TCGv t1 = tcg_temp_new();
12079|     gen_base_offset_addr(ctx, t1, base, offset);
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
12093| 
12094| void gen_ldxs(DisasContext *ctx, int base, int index, int rd)
12095| {
```

- `read_file(path=target/nios2/translate.c, version=old, start_line=805, end_line=830)` →

```
target/nios2/translate.c lines 805-830 of 1118
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
  826| 
  827|     t_gen_helper_raise_exception(dc, EXCP_BREAK);
  828| }
  829| 
  830| static const Nios2Instruction r_type_instructions[] = {
```

- `read_file(path=target/xtensa/translate.c, version=old, start_line=2355, end_line=2395)` →

```
target/xtensa/translate.c lines 2355-2395 of 7852
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
 2386| 
 2387| /*
 2388|  * Note: 64 bit ops are used here solely because SAR values
 2389|  * have range 0..63
 2390|  */
 2391| #define gen_shift_reg(cmd, reg) do { \
 2392|                     TCGv_i64 tmp = tcg_temp_new_i64(); \
 2393|                     tcg_gen_extu_i32_i64(tmp, reg); \
 2394|                     tcg_gen_##cmd##_i64(v, v, tmp); \
 2395|                     tcg_gen_extrl_i64_i32(arg[0].out, v); \
```

### Turn 3  _(tok 7832+1109, stop=tool_use)_

**Reasoning:** I need to find the enclosing function for each of these locations. The vl.c one is qemu_apply_machine_options, and the translate.c one at line 1172 looks like gen_hlt, which trans_HLT calls. The a64 line at 2222 I still need to check, probably disas_exc or something close to it, and the translate.c line at 6559 isn't resolved yet.

I've got the enclosing function for the vl.c site, and the translate.c hit at 8767 looks like trans_SVC. Still need to confirm the enclosing names for the a64 site at 2222, the m68k one at 206, and translate.c 1172, and I'll check whether grep covers every file or just tracked ones.



**Says:** Most enclosing functions are clear from the code. Three need confirming: the A64 HLT site, the `gen_hlt` site in translate.c, and the m68k exception helper.

- `grep(pattern=^(static |void |bool |int )?[a-zA-Z_0-9 \*]*\b(disas_exc|gen, version=old, path_glob=target/*.c)` →

```
6 matches
target/arm/translate-a64.c:2154:static void disas_exc(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:2467:            disas_exc(s, insn);
target/arm/translate.c:1158:static inline void gen_hlt(DisasContext *s, int imm)
target/arm/translate.c:6547:    gen_hlt(s, a->imm);
target/m68k/op_helper.c:443:void m68k_cpu_do_interrupt(CPUState *cs)
target/m68k/op_helper.c:513:bool m68k_cpu_exec_interrupt(CPUState *cs, int interrupt_request)
```

- `read_file(path=target/arm/translate-a64.c, version=old, start_line=2170, end_line=2200)` →

```
target/arm/translate-a64.c lines 2170-2200 of 15028
 2170|             gen_exception_insn(s, s->base.pc_next, EXCP_SWI,
 2171|                                syn_aa64_svc(imm16));
 2172|             break;
 2173|         case 2:                                                     /* HVC */
 2174|             if (s->current_el == 0) {
 2175|                 unallocated_encoding(s);
 2176|                 break;
 2177|             }
 2178|             /* The pre HVC helper handles cases when HVC gets trapped
 2179|              * as an undefined insn by runtime configuration.
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
```

- `read_file(path=target/arm/translate.c, version=old, start_line=1150, end_line=1160)` →

```
target/arm/translate.c lines 1150-1160 of 9927
 1150| 
 1151| /* Force a TB lookup after an instruction that changes the CPU state.  */
 1152| void gen_lookup_tb(DisasContext *s)
 1153| {
 1154|     tcg_gen_movi_i32(cpu_R[15], s->base.pc_next);
 1155|     s->base.is_jmp = DISAS_EXIT;
 1156| }
 1157| 
 1158| static inline void gen_hlt(DisasContext *s, int imm)
 1159| {
 1160|     /* HLT. This has two purposes.
```

- `read_file(path=target/m68k/op_helper.c, version=old, start_line=180, end_line=190)` →

```
target/m68k/op_helper.c lines 180-190 of 1128
  180|         return "MMU Access Level Violation";
  181|     case 64 ... 255:
  182|         return "User Defined Vector";
  183|     }
  184|     return "Unassigned";
  185| }
  186| 
  187| static void cf_interrupt_all(CPUM68KState *env, int is_hw)
  188| {
  189|     CPUState *cs = env_cpu(env);
  190|     uint32_t sp;
```

### Turn 4  _(tok 10289+1335, stop=tool_use)_

**Reasoning:** I'm checking whether any other function sits between the m68k hit at line 206 and its start at 187, and the lines shown suggest none does. Next I'm looking at the disas_exc call at 2222 to confirm no function boundary falls between it and the definition at 2154, using a grep for definitions in that range.

I'm confirming the region between 2154 and 2170 has no other function, and that the lines up to 2222 are just switch cases inside disas_exc. I also checked the gen_hlt hit at 1172 and the nios2, xtensa and mips callers, which all sit inside their enclosing functions. That gives an 11-entry list, and I'm working through it now.

I'm tallying the call sites now: the list has ten unique functions, which lines up with eleven call lines once the xtensa pair at 2369 and 2371 is counted as one function.



**Says:** I've confirmed every call site and its enclosing function. The grep returned 15 matches: 4 are the definition/prototype lines (header lines 30 and 55, `semihosting/config.c:62`, `stubs/semihost.c:26`), which are excluded. The remaining 11 call lines fall in 10 functions, because two calls in xtensa's `test_exceptions_simcall` share one function.

- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "high"}`

**Score (self):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1387+172, stop=tool_use)_

**Reasoning:** I'll start by running a find_references lookup on semihosting_enabled to see where it's used.



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

- `grep(pattern=semihosting_enabled, version=old, max_results=500)` →

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

### Turn 2  _(tok 2676+1316, stop=tool_use)_

**Reasoning:** I need to find the functions that enclose these lines, so I'll read the surrounding code in each file: the spots in vl.c, translate-a64.c, translate.c, the m68k op_helper, mips, nios2, and xtensa. I also want to confirm there are no macro-based or function-pointer uses, since the earlier grep should already have covered those.



**Says:** The index and grep agree on 12 hits (plus the definitions in `semihost.h`, `config.c`, and `stubs/semihost.c`, which are excluded). I need the enclosing function for each call site, so I'll read the surrounding code.

- `read_file(path=softmmu/vl.c, version=old, start_line=1800, end_line=1826)` →

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

- `read_file(path=target/arm/translate-a64.c, version=old, start_line=2205, end_line=2223)` →

```
target/arm/translate-a64.c lines 2205-2223 of 15028
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

- `read_file(path=target/arm/translate.c, version=old, start_line=1160, end_line=1173)` →

```
target/arm/translate.c lines 1160-1173 of 9927
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
```

- `read_file(path=target/arm/translate.c, version=old, start_line=6540, end_line=6560)` →

```
target/arm/translate.c lines 6540-6560 of 9927
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
```

- `read_file(path=target/arm/translate.c, version=old, start_line=8750, end_line=8768)` →

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

- `read_file(path=target/m68k/op_helper.c, version=old, start_line=190, end_line=210)` →

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

- `read_file(path=target/nios2/translate.c, version=old, start_line=810, end_line=822)` →

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

- `read_file(path=target/xtensa/translate.c, version=old, start_line=2355, end_line=2385)` →

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

### Turn 3  _(tok 7618+669, stop=tool_use)_

**Reasoning:** I need the enclosing functions for translate.c line 1172, which is probably gen_hlt, and for op_helper.c line 206, which is likely something like m68k_cpu_do_interrupt. I'll look up the function names directly. The xtensa lines 2369 and 2371 sit in test_exceptions_simcall, and 2381 is in translate_simcall, so those are already settled.

I still need the enclosing function for translate-a64 line 2222, which is probably disas_exc, so I'll grep the function definitions to confirm it.



**Says:** Most enclosing functions are now clear. I still need the function names for three sites (`target/arm/translate.c:1172`, `target/m68k/op_helper.c:206`, and `target/arm/translate-a64.c:2222`), so I'll look up their definitions.

- `grep(pattern=^(static )?[a-zA-Z_].*\(|^\{, version=old, path_glob=target/arm/translate.c, max_results=400)` →

```
1096 matches (showing 200)
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
target/arm/translate.c:288:TCGv_i32 add_reg_for_lit(DisasContext *s, int reg, int ofs)
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
target/arm/translate.c:559:GEN_SHIFT(shl)
target/arm/translate.c:560:GEN_SHIFT(shr)
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
target/arm/translate.c:927:MemOp pow2_align(unsigned i)
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
target/arm/translate.c:1370:IWMMXT_OP_ENV(name##b) \
target/arm/translate.c:1371:IWMMXT_OP_ENV(name##w) \
target/arm/translate.c:1372:IWMMXT_OP_ENV(name##l)
target/arm/translate.c:1375:static inline void gen_op_iwmmxt_##name##_M0(void) \
target/arm/translate.c:1376:{ \
target/arm/translate.c:1380:IWMMXT_OP(maddsq)
target/arm/translate.c:1381:IWMMXT_OP(madduq)
target/arm/translate.c:1382:IWMMXT_OP(sadb)
target/arm/translate.c:1383:IWMMXT_OP(sadw)
target/arm/translate.c:1384:IWMMXT_OP(mulslw)
target/arm/translate.c:1385:IWMMXT_OP(mulshw)
target/arm/translate.c:1386:IWMMXT_OP(mululw)
target/arm/translate.c:1387:IWMMXT_OP(muluhw)
target/arm/translate.c:1388:IWMMXT_OP(macsw)
target/arm/translate.c:1389:IWMMXT_OP(macuw)
target/arm/translate.c:1391:IWMMXT_OP_ENV_SIZE(unpackl)
target/arm/translate.c:1392:IWMMXT_OP_ENV_SIZE(unpackh)
target/arm/translate.c:1394:IWMMXT_OP_ENV1(unpacklub)
target/arm/translate.c:1395:IWMMXT_OP_ENV1(unpackluw)
target/arm/translate.c:1396:IWMMXT_OP_ENV1(unpacklul)
target/arm/translate.c:1397:IWMMXT_OP_ENV1(unpackhub)
target/arm/translate.c:1398:IWMMXT_OP_ENV1(unpackhuw)
target/arm/translate.c:1399:IWMMXT_OP_ENV1(unpackhul)
target/arm/translate.c:1400:IWMMXT_OP_ENV1(unpacklsb)
target/arm/translate.c:1401:IWMMXT_OP_ENV1(unpacklsw)
target/arm/translate.c:1402:IWMMXT_OP_ENV1(unpacklsl)
```

- `grep(pattern=^[a-zA-Z_].*\(, version=old, path_glob=target/m68k/op_helper.c)` →

```
38 matches
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
target/m68k/op_helper.c:544:G_NORETURN static void raise_exception(CPUM68KState *env, int tt)
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

- `grep(pattern=^[a-zA-Z_].*\(, version=old, path_glob=target/arm/translate-a64.c, max_results=400)` →

```
258 matches (showing 200)
target/arm/translate-a64.c:62:typedef void AArch64DecodeFn(DisasContext *s, uint32_t insn);
target/arm/translate-a64.c:71:void a64_translate_init(void)
target/arm/translate-a64.c:91:static int get_a64_user_mem_index(DisasContext *s)
target/arm/translate-a64.c:129:static void set_btype_raw(int val)
target/arm/translate-a64.c:135:static void set_btype(DisasContext *s, int val)
target/arm/translate-a64.c:143:static void reset_btype(DisasContext *s)
target/arm/translate-a64.c:151:void gen_a64_set_pc_im(uint64_t val)
target/arm/translate-a64.c:169:static void gen_top_byte_ignore(DisasContext *s, TCGv_i64 dst,
target/arm/translate-a64.c:200:static void gen_a64_set_pc(DisasContext *s, TCGv_i64 src)
target/arm/translate-a64.c:221:TCGv_i64 clean_data_tbi(DisasContext *s, TCGv_i64 addr)
target/arm/translate-a64.c:233:static void gen_address_with_allocation_tag0(TCGv_i64 dst, TCGv_i64 src)
target/arm/translate-a64.c:238:static void gen_probe_access(DisasContext *s, TCGv_i64 ptr,
target/arm/translate-a64.c:253:static TCGv_i64 gen_mte_check1_mmuidx(DisasContext *s, TCGv_i64 addr,
target/arm/translate-a64.c:276:TCGv_i64 gen_mte_check1(DisasContext *s, TCGv_i64 addr, bool is_write,
target/arm/translate-a64.c:286:TCGv_i64 gen_mte_checkN(DisasContext *s, TCGv_i64 addr, bool is_write,
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
target/arm/translate-a64.c:416:TCGv_i64 new_tmp_a64(DisasContext *s)
target/arm/translate-a64.c:422:TCGv_i64 new_tmp_a64_local(DisasContext *s)
target/arm/translate-a64.c:428:TCGv_i64 new_tmp_a64_zero(DisasContext *s)
target/arm/translate-a64.c:450:TCGv_i64 cpu_reg(DisasContext *s, int reg)
target/arm/translate-a64.c:460:TCGv_i64 cpu_reg_sp(DisasContext *s, int reg)
target/arm/translate-a64.c:469:TCGv_i64 read_cpu_reg(DisasContext *s, int reg, int sf)
target/arm/translate-a64.c:484:TCGv_i64 read_cpu_reg_sp(DisasContext *s, int reg, int sf)
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
```

### Turn 4  _(tok 25437+907, stop=tool_use)_

**Reasoning:** Now I'm going through the enclosing functions for each location: qemu_apply_machine_options in vl.c, disas_exc in translate-a64.c, gen_hlt, trans_BKPT and trans_SVC in translate.c, and cf_interrupt_all in the m68k op_helper.c.

I'm confirming the remaining locations: the mips is_uhi, nios2 gen_break, and xtensa test_exceptions_simcall and translate_simcall, and checking the function boundaries I've already mapped.



- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3753+229, stop=tool_use)_

**Reasoning:** I'm going to check callers of semihosting_enabled with get_callers, and grep for it as well to be thorough.



- `get_callers(name=semihosting_enabled, limit=200, version=old)` →

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

- `grep(pattern=semihosting_enabled, version=old, max_results=500)` →

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

### Turn 2  _(tok 5112+718, stop=tool_use)_

**Reasoning:** I'm pulling the callers from the grep: qemu_apply_machine_options, disas_exc, gen_hlt, the trans_BKPT and trans_SVC handlers, and a few others, including test_exceptions_simcall, which shows up twice. Next I want to confirm that line 6559 in translate.c really is trans_BKPT, since that's what get_callers reported.

I'm checking the enclosing functions for a few of the grep hits where the match could be ambiguous, starting with the arm line near 6559 and the m68k one near 206, since get_context_at should be quick for that.



- `get_context_at(file=target/arm/translate.c, line=6559, version=old)` →

```
{
  "error": "target/arm/translate.c:6559 is not inside a function definition in the old version"
}
```

- `get_context_at(file=target/m68k/op_helper.c, line=206, version=old)` →

```
cf_interrupt_all — target/m68k/op_helper.c:187 [function] static void cf_interrupt_all(CPUM68KState *env, int is_hw)
  reads: env, is_hw; writes: env*; returns: -

SLICE around line 206 (def-use, level 2; '>' marks the seed):
static void cf_interrupt_all(CPUM68KState *env, int is_hw) {
   CPUState *cs = env_cpu(env);
   ...
   retaddr = env->pc;
   if(!is_hw) {
     switch(cs->exception_index) {
   ...
       case EXCP_HALT_INSN: if(semihosting_enabled()&&(env->sr & SR_S)!= 0 &&(env->pc & 3)== 0 && cpu_lduw_code(env, env->pc - 4)== 0x4e71 && cpu_ldl_code(env, env->pc)== 0x4e7bf000) {
>      if(semihosting_enabled()&&(env->sr & SR_S)!= 0 &&(env->pc & 3)== 0 && cpu_lduw_code(env, env->pc - 4)== 0x4e71 && cpu_ldl_code(env, env->pc)== 0x4e7bf000) {
         env->pc += 4;
         do_m68k_semihosting(env, env->dregs[0]);
         return;
       }
   ...
       cs->exception_index = EXCP_HLT;
   ...
       }
     }
   }
   vector = cs->exception_index << 2;
   sr = env->sr | cpu_m68k_get_ccr(env);
   if(qemu_loglevel_mask(CPU_LOG_INT)) {
   ...
     qemu_log("INT %6d: %s(%#x)pc=%08x sp=%08x sr=%04x\n", ++count, m68k_exception_name(cs->exception_index), vector, env->pc, env->aregs[7], sr);
   }
   ...
   fmt |= sr;
   env->sr |= SR_S;
   if(is_hw) {
     env->sr =(env->sr & ~SR_I)|(env->pending_level << SR_I_SHIFT);
     env->sr &= ~SR_M;
   }
   m68k_switch_sp(env);
   sp = env->aregs[7];
   fmt |=(sp & 3)<< 28;
   ...
   sp -= 4;
   cpu_stl_mmuidx_ra(env, sp, retaddr, MMU_KERNEL_IDX, 0);
   sp -= 4;
   cpu_stl_mmuidx_ra(env, sp, fmt, MMU_KERNEL_IDX, 0);
   ...
   env->pc = cpu_ldl_mmuidx_ra(env, env->vbr + vector, MMU_KERNEL_IDX, 0);
}

CALLEES (14):
  env_cpu (include/exec/cpu-all.h:463): reads env; writes -; returns return &env_archcpu(env)->parent_obj;
  cpu_loop_exit (accel/tcg/cpu-exec-common.c:64 (1 of 2 definitions)): reads cpu; writes cpu*; returns -
  do_m68k_semihosting (target/m68k/m68k-semi.c:123): reads env, nr; writes env*; returns -
  cpu_ldl_code (accel/tcg/cputlb.c:2584 (1 of 2 definitions)): reads addr, env; writes -; returns return full_ldl_code(env, addr, oi, 0);
  cpu_lduw_code (accel/tcg/cputlb.c:2572 (1 of 2 definitions)): reads addr, env; writes -; returns return full_lduw_code(env, addr, oi, 0);
  semihosting_enabled (include/semihosting/semihost.h:30 (1 of 3 definitions)): reads -; writes -; returns return true;
  cf_rte (target/m68k/op_helper.c:29): reads env; writes env*; returns -
  qemu_log (util/log.c:128): reads fmt; writes -; returns -
  m68k_exception_name (target/m68k/op_helper.c:82): reads index; writes -; returns return "Access Fault"; | return "Address Error"; | return "Illegal Instruction"; | return "Divide by Zero"; | return "CHK/CHK2"; | return "FTRAPcc, TRAPcc, TRAPV";
  qemu_loglevel_mask (include/qemu/log-for-trace.h:27): reads mask; writes -; returns return(qemu_loglevel & mask)!= 0;
  m68k_switch_sp (target/m68k/helper.c:458): reads env; writes env*; returns -
  cpu_stl_mmuidx_ra [macro (1 of 2 definitions)]: # define cpu_stl_mmuidx_ra cpu_stl_le_mmuidx_ra
  cpu_ldl_mmuidx_ra [macro (1 of 2 definitions)]: # define cpu_ldl_mmuidx_ra cpu_ldl_le_mmuidx_ra
  not defined in this repository: cpu_m68k_get_ccr

CALLERS (1):
  do_interrupt_all (target/m68k/op_helper.c:440): cf_interrupt_all(env, is_hw);
```

- `get_context_at(file=target/xtensa/translate.c, line=2369, version=old)` →

```
test_exceptions_simcall — target/xtensa/translate.c:2361 [function] static uint32_t test_exceptions_simcall(DisasContext *dc, const OpcodeArg arg[], const uint32_t par[])
  reads: dc; writes: -; returns: return ill ? XTENSA_OP_ILL : 0;

SLICE around line 2369 (def-use, level 2; '>' marks the seed):
static uint32_t test_exceptions_simcall(DisasContext *dc, const OpcodeArg arg[], const uint32_t par[]) {
   #ifdef ...
   ...
   #else None
>  bool ill = dc->config->hw_version <= 250002 && !semihosting_enabled();
   #endif
   if(ill || !semihosting_enabled()) {
   ...
   }
   return ill ? XTENSA_OP_ILL : 0;
}

CALLEES (2):
  semihosting_enabled (include/semihosting/semihost.h:30 (1 of 3 definitions)): reads -; writes -; returns return true;
  qemu_log_mask [macro]: #define qemu_log_mask(MASK, FMT, ...) \

CALLERS (1):
  gen_translate_xsr (target/xtensa/translate.c:4687): .test_exceptions = test_exceptions_simcall,
```

### Turn 3  _(tok 8230+294, stop=tool_use)_

**Reasoning:** I'm noticing that the tool reports ARM 6559 as outside any function definition, so it might sit inside a macro or an #ifdef block. I'll look at the surrounding code to check.



- `read_file(path=target/arm/translate.c, version=old, start_line=6545, end_line=6575)` →

```
target/arm/translate.c lines 6545-6575 of 9927
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
 6563|         (a->imm == 0xab)) {
 6564|         gen_exception_internal_insn(s, s->pc_curr, EXCP_SEMIHOST);
 6565|     } else {
 6566|         gen_exception_bkpt_insn(s, syn_aa32_bkpt(a->imm, false));
 6567|     }
 6568|     return true;
 6569| }
 6570| 
 6571| static bool trans_HVC(DisasContext *s, arg_HVC *a)
 6572| {
 6573|     if (!ENABLE_ARCH_7 || arm_dc_feature(s, ARM_FEATURE_M)) {
 6574|         return false;
 6575|     }
```

- `read_file(path=target/xtensa/translate.c, version=old, start_line=2358, end_line=2390)` →

```
target/xtensa/translate.c lines 2358-2390 of 7852
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
 2386| 
 2387| /*
 2388|  * Note: 64 bit ops are used here solely because SAR values
 2389|  * have range 0..63
 2390|  */
```

### Turn 4  _(tok 9705+811, stop=tool_use)_

**Reasoning:** I'm checking that the trans_BKPT failure at line 6559 came from my passing a file-level line number, since trans_BKPT is actually inside a function, and the grep and get_callers results agree on that. Next I'm confirming that arms 1172 and 8767 are gen_hlt and trans_SVC, as get_callers reported, and that the grep's 15 matches cover every call site, with the 3 definitions accounted for.

Next I'm checking that is_uhi at line 12090 is a function, since the return statement about semihosting and sdbbp_code likely sits inside it, and get_callers agrees. I'm also going through the final list of ten functions across their files, with the grep coverage already accounted for.



- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3205+106, stop=tool_use)_

**Reasoning:** I'm calling get_callers on semihosting_enabled, asking for a high limit so I get the full list.



- `get_callers(name=semihosting_enabled, limit=500)` →

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

### Turn 2  _(tok 3865+310, stop=tool_use)_

**Reasoning:** I'm checking whether the tool's "old" version is just the parent of the revision it defaults to, and wondering whether the question is really about the repo's current state. I'll call it again with version "work" to see if the files on disk differ, and possibly look for callers through macros as well.



- `get_callers(name=semihosting_enabled, limit=500, rev=HEAD)` →

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

- `get_callers(name=semihosting_enabled, limit=500, version=work)` →

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

### Turn 3  _(tok 5331+321, stop=tool_use)_

**Reasoning:** Everything checks out so far. I'm wondering whether any callers could be missing from the call graph, such as through function pointers or macro expansions. I'll spot-check a few of the listed call sites, but I don't think I need to chase the callers of semihosting_enabled.

I'd like to check the "work" version for a caller in an unindexed file. I'll look up the definition of semihosting_enabled via resolve_symbol, since it may be a macro with other uses.



- `resolve_symbol(name=semihosting_enabled, rev=HEAD)` →

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

### Turn 4  _(tok 5941+592, stop=tool_use)_

**Reasoning:** I'm checking that the list is consistent and that the 11 callers are each unique by function and file. test_exceptions_simcall shows up twice, so I'll list it once and keep going through the callers.

Listing the remaining callers, from the gen_break in target/nios2 through translate_simcall in target/xtensa, with test_exceptions_simcall counted only once.



- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "high"}`

**Score (semantic):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

