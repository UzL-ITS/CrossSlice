# Impact-analysis transcript — qemu @ 5202861b20d7 — anthropic:claude-haiku-5-5

- target: `semihosting_enabled` (include/semihosting/semihost.h), arity 0->1
- truth: [['softmmu/vl.c', 'qemu_apply_machine_options'], ['target/arm/translate-a64.c', 'disas_exc'], ['target/arm/translate.c', 'gen_hlt'], ['target/arm/translate.c', 'trans_BKPT'], ['target/arm/translate.c', 'trans_SVC'], ['target/m68k/op_helper.c', 'cf_interrupt_all'], ['target/mips/tcg/translate.c', 'is_uhi'], ['target/nios2/translate.c', 'gen_break'], ['target/xtensa/translate.c', 'test_exceptions_simcall'], ['target/xtensa/translate.c', 'translate_simcall']]

## Self-navigation arm

### Turn 1  _(tok 1218+101, stop=tool_use)_

**Reasoning:** I'm going to start by searching the repo for every occurrence of semihosting_enabled.



- `grep(pattern=semihosting_enabled, version=old)` →

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

### Turn 2  _(tok 1849+1314, stop=tool_use)_

**Reasoning:** I need the enclosing function name for each of these call sites, so I'll read the surrounding code. A grep for the name should catch multi-line calls and macros too, so I'll check each call site directly.

I'm still looking up the enclosing functions, now for the nios2 call at line 821 and the three xtensa call sites at 2369, 2371 and 2381.



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

- `read_file(path=target/arm/translate-a64.c, version=old, start_line=2200, end_line=2223)` →

```
target/arm/translate-a64.c lines 2200-2223 of 15028
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

- `read_file(path=target/arm/translate.c, version=old, start_line=1155, end_line=1175)` →

```
target/arm/translate.c lines 1155-1175 of 9927
 1155|     s->base.is_jmp = DISAS_EXIT;
 1156| }
 1157| 
 1158| static inline void gen_hlt(DisasContext *s, int imm)
 1159| {
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

- `read_file(path=target/arm/translate.c, version=old, start_line=6540, end_line=6562)` →

```
target/arm/translate.c lines 6540-6562 of 9927
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

- `read_file(path=target/arm/translate.c, version=old, start_line=8750, end_line=8770)` →

```
target/arm/translate.c lines 8750-8770 of 9927
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

- `read_file(path=target/mips/tcg/translate.c, version=old, start_line=12075, end_line=12092)` →

```
target/mips/tcg/translate.c lines 12075-12092 of 16247
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
```

- `read_file(path=target/nios2/translate.c, version=old, start_line=805, end_line=823)` →

```
target/nios2/translate.c lines 805-823 of 1118
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
```

- `read_file(path=target/xtensa/translate.c, version=old, start_line=2355, end_line=2390)` →

```
target/xtensa/translate.c lines 2355-2390 of 7852
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
```

### Turn 3  _(tok 7324+592, stop=tool_use)_

**Reasoning:** I need to confirm which function encloses each of these spots: is_uhi around translate.c line 12090, gen_hlt at 1172, trans_BKPT at 6559, and trans_SVC at 8767 in the ARM file. For translate-a64.c line 2222 I'm not sure yet, so I'll look for the enclosing function, likely disas_exc. The m68k one near line 206 is probably m68k_cpu_do_interrupt or m68k_cpu_do, so I'll grep the function definitions to settle these.

I'm also checking the enclosing function for the nios2 gen_break and the Xtensa simcall spots, which are already confirmed. The stubs/semihost.c and config.c definitions can be set aside, along with the header inline at line 30. Next I'll check the enclosing functions for the a64 and m68k locations.



- `grep(pattern=^(static |void |bool |int )?[a-zA-Z_0-9 *]*\(?[a-z_0-9]+\(.*, version=old, path_glob=target/arm/translate-a64.c, max_results=400)` →

```
2854 matches (showing 200)
target/arm/translate-a64.c:62:typedef void AArch64DecodeFn(DisasContext *s, uint32_t insn);
target/arm/translate-a64.c:71:void a64_translate_init(void)
target/arm/translate-a64.c:76:                                    offsetof(CPUARMState, pc),
target/arm/translate-a64.c:80:                                          offsetof(CPUARMState, xregs[i]),
target/arm/translate-a64.c:85:        offsetof(CPUARMState, exclusive_high), "exclusive_high");
target/arm/translate-a64.c:91:static int get_a64_user_mem_index(DisasContext *s)
target/arm/translate-a64.c:123:            g_assert_not_reached();
target/arm/translate-a64.c:126:    return arm_to_core_mmu_idx(useridx);
target/arm/translate-a64.c:129:static void set_btype_raw(int val)
target/arm/translate-a64.c:131:    tcg_gen_st_i32(tcg_constant_i32(val), cpu_env,
target/arm/translate-a64.c:132:                   offsetof(CPUARMState, btype));
target/arm/translate-a64.c:135:static void set_btype(DisasContext *s, int val)
target/arm/translate-a64.c:138:    tcg_debug_assert(val >= 1 && val <= 3);
target/arm/translate-a64.c:139:    set_btype_raw(val);
target/arm/translate-a64.c:143:static void reset_btype(DisasContext *s)
target/arm/translate-a64.c:146:        set_btype_raw(0);
target/arm/translate-a64.c:151:void gen_a64_set_pc_im(uint64_t val)
target/arm/translate-a64.c:153:    tcg_gen_movi_i64(cpu_pc, val);
target/arm/translate-a64.c:169:static void gen_top_byte_ignore(DisasContext *s, TCGv_i64 dst,
target/arm/translate-a64.c:174:        tcg_gen_mov_i64(dst, src);
target/arm/translate-a64.c:177:        tcg_gen_extract_i64(dst, src, 0, 56);
target/arm/translate-a64.c:180:        tcg_gen_sextract_i64(dst, src, 0, 56);
target/arm/translate-a64.c:185:            tcg_gen_and_i64(dst, dst, src);
target/arm/translate-a64.c:189:            tcg_gen_or_i64(dst, dst, src);
target/arm/translate-a64.c:195:            g_assert_not_reached();
target/arm/translate-a64.c:200:static void gen_a64_set_pc(DisasContext *s, TCGv_i64 src)
target/arm/translate-a64.c:206:    gen_top_byte_ignore(s, cpu_pc, src, s->tbii);
target/arm/translate-a64.c:221:TCGv_i64 clean_data_tbi(DisasContext *s, TCGv_i64 addr)
target/arm/translate-a64.c:225:    gen_top_byte_ignore(s, clean, addr, s->tbid);
target/arm/translate-a64.c:227:    tcg_gen_mov_i64(clean, addr);
target/arm/translate-a64.c:233:static void gen_address_with_allocation_tag0(TCGv_i64 dst, TCGv_i64 src)
target/arm/translate-a64.c:235:    tcg_gen_andi_i64(dst, src, ~MAKE_64BIT_MASK(56, 4));
target/arm/translate-a64.c:238:static void gen_probe_access(DisasContext *s, TCGv_i64 ptr,
target/arm/translate-a64.c:241:    gen_helper_probe_access(cpu_env, ptr,
target/arm/translate-a64.c:242:                            tcg_constant_i32(acc),
target/arm/translate-a64.c:243:                            tcg_constant_i32(get_mem_index(s)),
target/arm/translate-a64.c:244:                            tcg_constant_i32(1 << log2_size));
target/arm/translate-a64.c:253:static TCGv_i64 gen_mte_check1_mmuidx(DisasContext *s, TCGv_i64 addr,
target/arm/translate-a64.c:269:        gen_helper_mte_check(ret, cpu_env, tcg_constant_i32(desc), addr);
target/arm/translate-a64.c:273:    return clean_data_tbi(s, addr);
target/arm/translate-a64.c:276:TCGv_i64 gen_mte_check1(DisasContext *s, TCGv_i64 addr, bool is_write,
target/arm/translate-a64.c:279:    return gen_mte_check1_mmuidx(s, addr, is_write, tag_checked, log2_size,
target/arm/translate-a64.c:300:        gen_helper_mte_check(ret, cpu_env, tcg_constant_i32(desc), addr);
target/arm/translate-a64.c:304:    return clean_data_tbi(s, addr);
target/arm/translate-a64.c:312:static void a64_test_cc(DisasCompare64 *c64, int cc)
target/arm/translate-a64.c:316:    arm_test_cc(&c32, cc);
target/arm/translate-a64.c:322:    tcg_gen_ext_i32_i64(c64->value, c32.value);
target/arm/translate-a64.c:324:    arm_free_cc(&c32);
target/arm/translate-a64.c:327:static void a64_free_cc(DisasCompare64 *c64)
target/arm/translate-a64.c:329:    tcg_temp_free_i64(c64->value);
target/arm/translate-a64.c:332:static void gen_rebuild_hflags(DisasContext *s)
target/arm/translate-a64.c:334:    gen_helper_rebuild_hflags_a64(cpu_env, tcg_constant_i32(s->current_el));
target/arm/translate-a64.c:337:static void gen_exception_internal(int excp)
target/arm/translate-a64.c:339:    assert(excp_is_internal(excp));
target/arm/translate-a64.c:340:    gen_helper_exception_internal(cpu_env, tcg_constant_i32(excp));
target/arm/translate-a64.c:343:static void gen_exception_internal_insn(DisasContext *s, uint64_t pc, int excp)
target/arm/translate-a64.c:345:    gen_a64_set_pc_im(pc);
target/arm/translate-a64.c:346:    gen_exception_internal(excp);
target/arm/translate-a64.c:350:static void gen_exception_bkpt_insn(DisasContext *s, uint32_t syndrome)
target/arm/translate-a64.c:352:    gen_a64_set_pc_im(s->pc_curr);
target/arm/translate-a64.c:353:    gen_helper_exception_bkpt_insn(cpu_env, tcg_constant_i32(syndrome));
target/arm/translate-a64.c:357:static void gen_step_complete_exception(DisasContext *s)
target/arm/translate-a64.c:368:    gen_ss_advance(s);
target/arm/translate-a64.c:369:    gen_swstep_exception(s, 1, s->is_ldex);
target/arm/translate-a64.c:373:static inline bool use_goto_tb(DisasContext *s, uint64_t dest)
target/arm/translate-a64.c:378:    return translator_use_goto_tb(&s->base, dest);
target/arm/translate-a64.c:381:static inline void gen_goto_tb(DisasContext *s, int n, uint64_t dest)
target/arm/translate-a64.c:383:    if (use_goto_tb(s, dest)) {
target/arm/translate-a64.c:384:        tcg_gen_goto_tb(n);
target/arm/translate-a64.c:385:        gen_a64_set_pc_im(dest);
target/arm/translate-a64.c:386:        tcg_gen_exit_tb(s->base.tb, n);
target/arm/translate-a64.c:389:        gen_a64_set_pc_im(dest);
target/arm/translate-a64.c:391:            gen_step_complete_exception(s);
target/arm/translate-a64.c:393:            tcg_gen_lookup_and_goto_ptr();
target/arm/translate-a64.c:399:static void init_tmp_a64_array(DisasContext *s)
target/arm/translate-a64.c:402:    memset(s->tmp_a64, 0, sizeof(s->tmp_a64));
target/arm/translate-a64.c:407:static void free_tmp_a64(DisasContext *s)
target/arm/translate-a64.c:411:        tcg_temp_free_i64(s->tmp_a64[i]);
target/arm/translate-a64.c:413:    init_tmp_a64_array(s);
target/arm/translate-a64.c:416:TCGv_i64 new_tmp_a64(DisasContext *s)
target/arm/translate-a64.c:418:    assert(s->tmp_a64_count < TMP_A64_MAX);
target/arm/translate-a64.c:422:TCGv_i64 new_tmp_a64_local(DisasContext *s)
target/arm/translate-a64.c:424:    assert(s->tmp_a64_count < TMP_A64_MAX);
target/arm/translate-a64.c:428:TCGv_i64 new_tmp_a64_zero(DisasContext *s)
target/arm/translate-a64.c:431:    tcg_gen_movi_i64(t, 0);
target/arm/translate-a64.c:450:TCGv_i64 cpu_reg(DisasContext *s, int reg)
target/arm/translate-a64.c:453:        return new_tmp_a64_zero(s);
target/arm/translate-a64.c:460:TCGv_i64 cpu_reg_sp(DisasContext *s, int reg)
target/arm/translate-a64.c:469:TCGv_i64 read_cpu_reg(DisasContext *s, int reg, int sf)
target/arm/translate-a64.c:474:            tcg_gen_mov_i64(v, cpu_X[reg]);
target/arm/translate-a64.c:476:            tcg_gen_ext32u_i64(v, cpu_X[reg]);
target/arm/translate-a64.c:479:        tcg_gen_movi_i64(v, 0);
target/arm/translate-a64.c:484:TCGv_i64 read_cpu_reg_sp(DisasContext *s, int reg, int sf)
target/arm/translate-a64.c:488:        tcg_gen_mov_i64(v, cpu_X[reg]);
target/arm/translate-a64.c:490:        tcg_gen_ext32u_i64(v, cpu_X[reg]);
target/arm/translate-a64.c:500:static inline int fp_reg_offset(DisasContext *s, int regno, MemOp size)
target/arm/translate-a64.c:502:    return vec_reg_offset(s, regno, 0, size);
target/arm/translate-a64.c:506:static inline int fp_reg_hi_offset(DisasContext *s, int regno)
target/arm/translate-a64.c:508:    return vec_reg_offset(s, regno, 1, MO_64);
target/arm/translate-a64.c:517:static TCGv_i64 read_fp_dreg(DisasContext *s, int reg)
target/arm/translate-a64.c:521:    tcg_gen_ld_i64(v, cpu_env, fp_reg_offset(s, reg, MO_64));
target/arm/translate-a64.c:525:static TCGv_i32 read_fp_sreg(DisasContext *s, int reg)
target/arm/translate-a64.c:529:    tcg_gen_ld_i32(v, cpu_env, fp_reg_offset(s, reg, MO_32));
target/arm/translate-a64.c:533:static TCGv_i32 read_fp_hreg(DisasContext *s, int reg)
target/arm/translate-a64.c:537:    tcg_gen_ld16u_i32(v, cpu_env, fp_reg_offset(s, reg, MO_16));
target/arm/translate-a64.c:544:static void clear_vec_high(DisasContext *s, bool is_q, int rd)
target/arm/translate-a64.c:550:    tcg_gen_gvec_mov(MO_64, ofs, ofs, is_q ? 16 : 8, vsz);
target/arm/translate-a64.c:553:void write_fp_dreg(DisasContext *s, int reg, TCGv_i64 v)
target/arm/translate-a64.c:557:    tcg_gen_st_i64(v, cpu_env, ofs);
target/arm/translate-a64.c:558:    clear_vec_high(s, false, reg);
target/arm/translate-a64.c:561:static void write_fp_sreg(DisasContext *s, int reg, TCGv_i32 v)
target/arm/translate-a64.c:565:    tcg_gen_extu_i32_i64(tmp, v);
target/arm/translate-a64.c:566:    write_fp_dreg(s, reg, tmp);
target/arm/translate-a64.c:567:    tcg_temp_free_i64(tmp);
target/arm/translate-a64.c:571:static void gen_gvec_fn2(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:574:    gvec_fn(vece, vec_full_reg_offset(s, rd), vec_full_reg_offset(s, rn),
target/arm/translate-a64.c:581:static void gen_gvec_fn2i(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:584:    gvec_fn(vece, vec_full_reg_offset(s, rd), vec_full_reg_offset(s, rn),
target/arm/translate-a64.c:589:static void gen_gvec_fn3(DisasContext *s, bool is_q, int rd, int rn, int rm,
target/arm/translate-a64.c:592:    gvec_fn(vece, vec_full_reg_offset(s, rd), vec_full_reg_offset(s, rn),
target/arm/translate-a64.c:593:            vec_full_reg_offset(s, rm), is_q ? 16 : 8, vec_full_reg_size(s));
target/arm/translate-a64.c:597:static void gen_gvec_fn4(DisasContext *s, bool is_q, int rd, int rn, int rm,
target/arm/translate-a64.c:600:    gvec_fn(vece, vec_full_reg_offset(s, rd), vec_full_reg_offset(s, rn),
target/arm/translate-a64.c:601:            vec_full_reg_offset(s, rm), vec_full_reg_offset(s, rx),
target/arm/translate-a64.c:606:static void gen_gvec_op2_ool(DisasContext *s, bool is_q, int rd,
target/arm/translate-a64.c:609:    tcg_gen_gvec_2_ool(vec_full_reg_offset(s, rd),
target/arm/translate-a64.c:610:                       vec_full_reg_offset(s, rn),
target/arm/translate-a64.c:615:static void gen_gvec_op3_ool(DisasContext *s, bool is_q, int rd,
target/arm/translate-a64.c:618:    tcg_gen_gvec_3_ool(vec_full_reg_offset(s, rd),
target/arm/translate-a64.c:619:                       vec_full_reg_offset(s, rn),
target/arm/translate-a64.c:620:                       vec_full_reg_offset(s, rm),
target/arm/translate-a64.c:627:static void gen_gvec_op3_fpst(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:632:    tcg_gen_gvec_3_ptr(vec_full_reg_offset(s, rd),
target/arm/translate-a64.c:633:                       vec_full_reg_offset(s, rn),
target/arm/translate-a64.c:634:                       vec_full_reg_offset(s, rm), fpst,
target/arm/translate-a64.c:636:    tcg_temp_free_ptr(fpst);
target/arm/translate-a64.c:640:static void gen_gvec_op3_qc(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:645:    tcg_gen_addi_ptr(qc_ptr, cpu_env, offsetof(CPUARMState, vfp.qc));
target/arm/translate-a64.c:646:    tcg_gen_gvec_3_ptr(vec_full_reg_offset(s, rd),
target/arm/translate-a64.c:647:                       vec_full_reg_offset(s, rn),
target/arm/translate-a64.c:648:                       vec_full_reg_offset(s, rm), qc_ptr,
target/arm/translate-a64.c:650:    tcg_temp_free_ptr(qc_ptr);
target/arm/translate-a64.c:654:static void gen_gvec_op4_ool(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:657:    tcg_gen_gvec_4_ool(vec_full_reg_offset(s, rd),
target/arm/translate-a64.c:658:                       vec_full_reg_offset(s, rn),
target/arm/translate-a64.c:659:                       vec_full_reg_offset(s, rm),
target/arm/translate-a64.c:660:                       vec_full_reg_offset(s, ra),
target/arm/translate-a64.c:668:static void gen_gvec_op4_fpst(DisasContext *s, bool is_q, int rd, int rn,
target/arm/translate-a64.c:673:    tcg_gen_gvec_4_ptr(vec_full_reg_offset(s, rd),
target/arm/translate-a64.c:674:                       vec_full_reg_offset(s, rn),
target/arm/translate-a64.c:675:                       vec_full_reg_offset(s, rm),
target/arm/translate-a64.c:676:                       vec_full_reg_offset(s, ra), fpst,
target/arm/translate-a64.c:678:    tcg_temp_free_ptr(fpst);
target/arm/translate-a64.c:684:static inline void gen_set_NZ64(TCGv_i64 result)
target/arm/translate-a64.c:686:    tcg_gen_extr_i64_i32(cpu_ZF, cpu_NF, result);
target/arm/translate-a64.c:687:    tcg_gen_or_i32(cpu_ZF, cpu_ZF, cpu_NF);
target/arm/translate-a64.c:694:        gen_set_NZ64(result);
target/arm/translate-a64.c:696:        tcg_gen_extrl_i64_i32(cpu_ZF, result);
target/arm/translate-a64.c:697:        tcg_gen_mov_i32(cpu_NF, cpu_ZF);
target/arm/translate-a64.c:699:    tcg_gen_movi_i32(cpu_CF, 0);
target/arm/translate-a64.c:700:    tcg_gen_movi_i32(cpu_VF, 0);
target/arm/translate-a64.c:712:        tcg_gen_movi_i64(tmp, 0);
target/arm/translate-a64.c:713:        tcg_gen_add2_i64(result, flag, t0, tmp, t1, tmp);
target/arm/translate-a64.c:715:        tcg_gen_extrl_i64_i32(cpu_CF, flag);
target/arm/translate-a64.c:717:        gen_set_NZ64(result);
target/arm/translate-a64.c:719:        tcg_gen_xor_i64(flag, result, t0);
target/arm/translate-a64.c:720:        tcg_gen_xor_i64(tmp, t0, t1);
target/arm/translate-a64.c:721:        tcg_gen_andc_i64(flag, flag, tmp);
target/arm/translate-a64.c:722:        tcg_temp_free_i64(tmp);
target/arm/translate-a64.c:723:        tcg_gen_extrh_i64_i32(cpu_VF, flag);
target/arm/translate-a64.c:725:        tcg_gen_mov_i64(dest, result);
target/arm/translate-a64.c:726:        tcg_temp_free_i64(result);
target/arm/translate-a64.c:727:        tcg_temp_free_i64(flag);
target/arm/translate-a64.c:734:        tcg_gen_movi_i32(tmp, 0);
target/arm/translate-a64.c:735:        tcg_gen_extrl_i64_i32(t0_32, t0);
target/arm/translate-a64.c:736:        tcg_gen_extrl_i64_i32(t1_32, t1);
target/arm/translate-a64.c:737:        tcg_gen_add2_i32(cpu_NF, cpu_CF, t0_32, tmp, t1_32, tmp);
target/arm/translate-a64.c:738:        tcg_gen_mov_i32(cpu_ZF, cpu_NF);
target/arm/translate-a64.c:739:        tcg_gen_xor_i32(cpu_VF, cpu_NF, t0_32);
target/arm/translate-a64.c:740:        tcg_gen_xor_i32(tmp, t0_32, t1_32);
target/arm/translate-a64.c:741:        tcg_gen_andc_i32(cpu_VF, cpu_VF, tmp);
target/arm/translate-a64.c:742:        tcg_gen_extu_i32_i64(dest, cpu_NF);
target/arm/translate-a64.c:744:        tcg_temp_free_i32(tmp);
target/arm/translate-a64.c:745:        tcg_temp_free_i32(t0_32);
target/arm/translate-a64.c:746:        tcg_temp_free_i32(t1_32);
target/arm/translate-a64.c:759:        tcg_gen_sub_i64(result, t0, t1);
target/arm/translate-a64.c:761:        gen_set_NZ64(result);
target/arm/translate-a64.c:763:        tcg_gen_setcond_i64(TCG_COND_GEU, flag, t0, t1);
target/arm/translate-a64.c:764:        tcg_gen_extrl_i64_i32(cpu_CF, flag);
target/arm/translate-a64.c:766:        tcg_gen_xor_i64(flag, result, t0);
target/arm/translate-a64.c:768:        tcg_gen_xor_i64(tmp, t0, t1);
target/arm/translate-a64.c:769:        tcg_gen_and_i64(flag, flag, tmp);
target/arm/translate-a64.c:770:        tcg_temp_free_i64(tmp);
target/arm/translate-a64.c:771:        tcg_gen_extrh_i64_i32(cpu_VF, flag);
target/arm/translate-a64.c:772:        tcg_gen_mov_i64(dest, result);
target/arm/translate-a64.c:773:        tcg_temp_free_i64(flag);
target/arm/translate-a64.c:774:        tcg_temp_free_i64(result);
target/arm/translate-a64.c:781:        tcg_gen_extrl_i64_i32(t0_32, t0);
target/arm/translate-a64.c:782:        tcg_gen_extrl_i64_i32(t1_32, t1);
target/arm/translate-a64.c:783:        tcg_gen_sub_i32(cpu_NF, t0_32, t1_32);
```

- `grep(pattern=^[a-zA-Z_].*\(, version=old, path_glob=target/m68k/op_helper.c, max_results=100)` →

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

### Turn 4  _(tok 18193+257, stop=tool_use)_

**Reasoning:** I've confirmed the m68k match at line 206 sits inside cf_interrupt_all, which runs from about line 187 to 255. Now I need the function that encloses the a64 match at line 2222, so I'll search translate-a64.c for the nearby disas_ function definitions.



- `grep(pattern=^static void disas_(exc|system)\b|^static void handle_hlt|^s, version=old, path_glob=target/arm/translate-a64.c, max_results=400)` →

```
239 matches (showing 200)
target/arm/translate-a64.c:91:static int get_a64_user_mem_index(DisasContext *s)
target/arm/translate-a64.c:129:static void set_btype_raw(int val)
target/arm/translate-a64.c:135:static void set_btype(DisasContext *s, int val)
target/arm/translate-a64.c:143:static void reset_btype(DisasContext *s)
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
target/arm/translate-a64.c:1218:static bool sme_access_check(DisasContext *s)
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
target/arm/translate-a64.c:10624:static void handle_vec_simd_shri(DisasContext *s, bool is_q, bool is_u,
target/arm/translate-a64.c:10685:static void handle_vec_simd_shli(DisasContext *s, bool is_q, bool insert,
target/arm/translate-a64.c:10712:static void handle_vec_simd_wshli(DisasContext *s, bool is_q, bool is_u,
target/arm/translate-a64.c:10749:static void handle_vec_simd_shrn(DisasContext *s, bool is_q,
target/arm/translate-a64.c:10810:static void disas_simd_shift_imm(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:10882:static void gen_neon_addl(int size, bool is_sub, TCGv_i64 tcg_res,
target/arm/translate-a64.c:10897:static void handle_3rd_widening(DisasContext *s, int is_q, int is_u, int size,
target/arm/translate-a64.c:11115:static void handle_3rd_wide(DisasContext *s, int is_q, int is_u, int size,
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 27963+345, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "medium"}`

**Score (self):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1387+80, stop=tool_use)_

**Reasoning:** I'm going to start by using find_references to locate every place semihosting_enabled is referenced.



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

### Turn 2  _(tok 2009+160, stop=tool_use)_

**Reasoning:** GNU Global might miss some references, so I'll grep as well. I need to find the enclosing functions, so I'm reading through the relevant sections now.



**Says:** The index gives 11 call lines. I need the enclosing function for each, and I'll grep as well in case the index missed any.

- `grep(pattern=semihosting_enabled\s*\(, version=old)` →

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

### Turn 3  _(tok 2699+1191, stop=tool_use)_

**Reasoning:** The grep results match what I already had. The `static inline` at line 30 in the header is just the definition, so I can skip it. Next I need the enclosing functions, so I'll read those regions.



**Says:** The grep matches the index. Next I'll read the surrounding code to find each enclosing function.

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

- `read_file(path=target/arm/translate.c, version=old, start_line=6545, end_line=6565)` →

```
target/arm/translate.c lines 6545-6565 of 9927
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

- `read_file(path=target/mips/tcg/translate.c, version=old, start_line=12080, end_line=12095)` →

```
target/mips/tcg/translate.c lines 12080-12095 of 16247
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

- `read_file(path=target/nios2/translate.c, version=old, start_line=810, end_line=825)` →

```
target/nios2/translate.c lines 810-825 of 1118
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

- `read_file(path=target/xtensa/translate.c, version=old, start_line=2355, end_line=2390)` →

```
target/xtensa/translate.c lines 2355-2390 of 7852
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
```

### Turn 4  _(tok 8145+900, stop=tool_use)_

**Reasoning:** I'm working out which functions enclose the spots at translate.c line 1172 and translate-a64.c around line 2222, probably something like disas_exc for the latter. I'll grep for the function names, and also check the m68k location.

I'm now checking the remaining spots: the m68k interrupt handler near op_helper.c line 206, mips is_uhi at line 12090, nios2 gen_break, the xtensa simcall functions, and qemu_apply_machine_options in vl.c. I still need to confirm the enclosing functions for the a64 and arm gen_hlt locations and for m68k, so I'll grep for the function definitions.



**Says:** Most enclosing functions are now clear. Three still need checking: the A64 call at line 2222, the A32/T32 call at line 1172, and the m68k call at line 206. I'll look up their enclosing function definitions.

- `grep(pattern=^(static |void |bool |int )?[a-zA-Z_0-9 \*]*\b(disas_exc|gen, version=old)` →

```
7 matches
target/arm/translate-a64.c:2154:static void disas_exc(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:2467:            disas_exc(s, insn);
target/arm/translate.c:1158:static inline void gen_hlt(DisasContext *s, int imm)
target/arm/translate.c:6547:    gen_hlt(s, a->imm);
target/m68k/cpu.h:177:void m68k_cpu_do_interrupt(CPUState *cpu);
target/m68k/op_helper.c:443:void m68k_cpu_do_interrupt(CPUState *cs)
tools/virtiofsd/fuse_lowlevel.c:1746:static void do_interrupt(fuse_req_t req, fuse_ino_t nodeid,
```

- `read_file(path=target/arm/translate-a64.c, version=old, start_line=2180, end_line=2200)` →

```
target/arm/translate-a64.c lines 2180-2200 of 15028
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

- `read_file(path=target/arm/translate.c, version=old, start_line=1148, end_line=1160)` →

```
target/arm/translate.c lines 1148-1160 of 9927
 1148|     gen_exception_insn(s, s->pc_curr, EXCP_UDEF, syn_uncategorized());
 1149| }
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

- `read_file(path=target/m68k/op_helper.c, version=old, start_line=175, end_line=190)` →

```
target/m68k/op_helper.c lines 175-190 of 1128
  175|     case EXCP_MMU_CONF: /* 68030/68851 only */
  176|         return "MMU Configuration Error";
  177|     case EXCP_MMU_ILLEGAL: /* 68851 only */
  178|         return "MMU Illegal Operation";
  179|     case EXCP_MMU_ACCESS: /* 68851 only */
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

### Turn 5  _(tok 10428+392, stop=tool_use)_

**Reasoning:** I'm checking that the a64 hit at line 2222 falls inside disas_exc, which starts at 2154, and that no other function boundary sits between them. For m68k, line 206 is inside cf_interrupt_all, starting at 187. I'm also checking whether the semihosting_enabled pattern turns up anywhere outside C files or in macros.

I'm wondering whether the function might also be referenced without parentheses, like a function pointer assignment, so I'm going to grep for the name without the trailing parenthesis.



**Says:** The enclosing functions are: `disas_exc` (A64), `gen_hlt` (A32/T32), and `cf_interrupt_all` (m68k). Before submitting, I'll check for uses without an opening parenthesis, such as function-pointer references.

- `grep(pattern=semihosting_enabled([^_(a-zA-Z]|$), version=old)` →

```
0 matches

```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 10991+344, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "high"}`

**Score (index):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Tool arm

### Turn 1  _(tok 3753+228, stop=tool_use)_

**Reasoning:** I'm going to pull the callers of semihosting_enabled with get_callers, and run a grep as well so I don't miss anything.



- `get_callers(name=semihosting_enabled, limit=200, rev=None)` →

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

### Turn 2  _(tok 5111+863, stop=tool_use)_

**Reasoning:** I'm checking the grep hits against the callers list: 15 matches but only 11 entries. The xtensa simcall tests show up at 2369, 2371, and translate_simcall at 2381. Next I'm going through each call site, from vl.c and the a64 disassembler through the translate and m68k entries, and the mips list is cut off there.

I'm checking that the grep covers the call sites, and that the only function duplicated in the list, test_exceptions_simcall, should count once, which brings the unique callers to 10. The git grep only searches tracked files, which is fine here, and the names it returns should catch any function-pointer use too.



- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3205+106, stop=tool_use)_

**Reasoning:** I'm going to pull up the callers of semihosting_enabled, asking for a generous limit so I get the full list.



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

### Turn 2  _(tok 3865+233, stop=tool_use)_

**Reasoning:** The tool reports "version: old," which suggests the default revision is the server's commit, and the results are coming from the old version. The function itself is being changed, but what matters are the call sites in the working tree, so the old results are probably the same. To be safe, I'll check against the working version.



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

### Turn 3  _(tok 4992+254, stop=tool_use)_

**Reasoning:** I'm checking whether the callers list is complete, since macros, function pointers, or work-tree code could be missing from the call graph. The "old" version label looks off even with HEAD, so I'll check the work version to see if it differs.



- `get_callers(name=semihosting_enabled, limit=500, rev=work)` →

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

- `get_neighborhood(name=semihosting_enabled)` →

```
semihosting_enabled — include/semihosting/semihost.h:30 [function] static inline bool semihosting_enabled(void)
  AMBIGUOUS: 3 definitions of this name; this one was chosen by priority_fallback; others: semihosting/config.c:62, stubs/semihost.c:26 — get_context_at(file, line) looks at another one
  reads: -; writes: -; returns: return true;

CALLEES (0):

CALLERS (8):
  qemu_apply_machine_options (softmmu/vl.c:1825): if (semihosting_enabled() && !semihosting_get_argc()) {
  disas_exc (target/arm/translate-a64.c:2222): if (semihosting_enabled() && imm16 == 0xf000) {
  gen_hlt (target/arm/translate.c:1172): if (semihosting_enabled() &&
  trans_BKPT (target/arm/translate.c:6559): semihosting_enabled() &&
  trans_SVC (target/arm/translate.c:8767): if (!arm_dc_feature(s, ARM_FEATURE_M) && semihosting_enabled() &&
  cf_interrupt_all (target/m68k/op_helper.c:206): if (semihosting_enabled()
  is_uhi (target/mips/tcg/translate.c:12090): return semihosting_enabled() && sdbbp_code == 1;
  gen_break (target/nios2/translate.c:821): if (semihosting_enabled() && instr.imm5 == 1) {
  ... only the first 8 of 12 reference sites were followed
```

### Turn 4  _(tok 6391+538, stop=tool_use)_

**Reasoning:** I'm counting the reference sites: the neighborhood reports 12, but the callers list only has 11 entries, with test_exceptions_simcall listed twice. I'm wondering whether the extra site comes from another call inside the definition's file, such as one in semihosting/config.c or the stubs.

I'm now going to look at whether the twelfth reference is a non-call use, like a function pointer assignment, or a caller in a file that isn't indexed. I'll check the callers of the other definitions and expand the function to see what's behind the extra site.



- `expand_function(name=semihosting_enabled, levels=1)` →

```
{
  "name": "semihosting_enabled",
  "version": "old",
  "levels": 1,
  "node": {
    "name": "semihosting_enabled",
    "file": "include/semihosting/semihost.h",
    "line": 30,
    "kind": "function",
    "state": "analyzed",
    "ambiguous": true,
    "definitions": 3,
    "alternatives": [
      "semihosting/config.c:62",
      "stubs/semihost.c:26"
    ]
  },
  "callees": [],
  "callers": [
    {
      "name": "qemu_apply_machine_options",
      "file": "softmmu/vl.c",
      "line": 1821,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1825
      ]
    },
    {
      "name": "disas_exc",
      "file": "target/arm/translate-a64.c",
      "line": 2154,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        2222
      ]
    },
    {
      "name": "gen_hlt",
      "file": "target/arm/translate.c",
      "line": 1158,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        1172
      ]
    },
    {
      "name": "trans_BKPT",
      "file": "target/arm/translate.c",
      "line": 6551,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        6559
      ]
    },
    {
      "name": "trans_SVC",
      "file": "target/arm/translate.c",
      "line": 8763,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        8767
      ]
    },
    {
      "name": "cf_interrupt_all",
      "file": "target/m68k/op_helper.c",
      "line": 187,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        206
      ]
    },
    {
      "name": "is_uhi",
      "file": "target/mips/tcg/translate.c",
      "line": 12085,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        12090
      ]
    },
    {
      "name": "gen_break",
      "file": "target/nios2/translate.c",
      "line": 816,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        821
      ]
    },
    {
      "name": "test_exceptions_simcall",
      "file": "target/xtensa/translate.c",
      "line": 2361,
      "kind": "function",
      "state": "analyzed",
      "call_lines": [
        2369,
        2371
      ]
    },
    {
      "name": "translate_simcall",
      "file": "target/xtensa/translate.c",
      "line": 2377,
      "kind": "function",
      "state": "summarized",
      "call_lines": [
        2381
      ]
    }
  ]
}
```

- `get_context_at(file=semihosting/config.c, line=62)` →

```
semihosting_enabled — semihosting/config.c:62 [function] bool semihosting_enabled(void)
  reads: -; writes: -; returns: return semihosting.enabled;

SLICE around line 62 (def-use, level 2; '>' marks the seed):
bool semihosting_enabled(void) {
>  return semihosting.enabled;
}

CALLEES (0):

CALLERS (8):
  qemu_apply_machine_options (softmmu/vl.c:1825): if (semihosting_enabled() && !semihosting_get_argc()) {
  disas_exc (target/arm/translate-a64.c:2222): if (semihosting_enabled() && imm16 == 0xf000) {
  gen_hlt (target/arm/translate.c:1172): if (semihosting_enabled() &&
  trans_BKPT (target/arm/translate.c:6559): semihosting_enabled() &&
  trans_SVC (target/arm/translate.c:8767): if (!arm_dc_feature(s, ARM_FEATURE_M) && semihosting_enabled() &&
  cf_interrupt_all (target/m68k/op_helper.c:206): if (semihosting_enabled()
  is_uhi (target/mips/tcg/translate.c:12090): return semihosting_enabled() && sdbbp_code == 1;
  gen_break (target/nios2/translate.c:821): if (semihosting_enabled() && instr.imm5 == 1) {
  ... only the first 8 of 12 reference sites were followed
```

- `get_context_at(file=stubs/semihost.c, line=26)` →

```
semihosting_enabled — stubs/semihost.c:26 [function] bool semihosting_enabled(void)
  reads: -; writes: -; returns: return false;

SLICE around line 26 (def-use, level 2; '>' marks the seed):
bool semihosting_enabled(void) {
>  return false;
}

CALLEES (0):

CALLERS (8):
  qemu_apply_machine_options (softmmu/vl.c:1825): if (semihosting_enabled() && !semihosting_get_argc()) {
  disas_exc (target/arm/translate-a64.c:2222): if (semihosting_enabled() && imm16 == 0xf000) {
  gen_hlt (target/arm/translate.c:1172): if (semihosting_enabled() &&
  trans_BKPT (target/arm/translate.c:6559): semihosting_enabled() &&
  trans_SVC (target/arm/translate.c:8767): if (!arm_dc_feature(s, ARM_FEATURE_M) && semihosting_enabled() &&
  cf_interrupt_all (target/m68k/op_helper.c:206): if (semihosting_enabled()
  is_uhi (target/mips/tcg/translate.c:12090): return semihosting_enabled() && sdbbp_code == 1;
  gen_break (target/nios2/translate.c:821): if (semihosting_enabled() && instr.imm5 == 1) {
  ... only the first 8 of 12 reference sites were followed
```

### Turn 5  _(tok 9050+3575, stop=tool_use)_

**Reasoning:** I'm counting the call sites from the callers list: eleven of them, which leaves a twelfth reference I haven't found yet. I'm wondering whether the extra one is the definition itself or some other kind of reference.

I'm now going through the likely places outside the callers list where the twelfth reference could be: arm translate code, a64 exception handling, and the m68k helpers. I'm checking which of these historically call the semihosting check.

I'm checking the remaining candidates in the m68k op_helper and translate code, plus MIPS, Nios2, and Xtensa, where semihosting checks show up in trap or break handling. I'm also wondering whether the Arm bkpt helper or a RISC-V ebreak path might account for the twelfth reference.

I'm now checking the riscv translate code, where an ebreak handler might reference semihosting, and the interrupt path that tests for the semihost exception index. I'm also weighing whether the twelfth reference sits behind a function pointer or inside a macro, since the call graph only followed eight of the twelve sites.

I'm still trying to find the twelfth reference, and it may not be in the callers list at all. The eleven sites already counted don't cover it, so I'm considering a function that the call graph doesn't follow or a site hidden behind a macro.

I'm checking whether the twelfth reference might be in the header that declares semihosting_enabled, or in an inline helper that the call graph reports under its own name. I'm also looking at the QEMU 8.0-era target code for other spots that test it.

I'm listing the remaining QEMU files that might test for semihosting: the config and stub files, the Arm translate code, the m68k op helper, MIPS, Nios2, and Xtensa. I'm also wondering whether an Arm helper file belongs on that list.

I'm now recalling the other QEMU spots that might test for semihosting: the RISC-V translate code, which I'm not sure uses it, and a few less likely files like the m68k translate code and the Arm a64 helper, which I can't confirm either way.

I'm checking the remaining QEMU targets for semihosting checks, including the Arm translate code, the a64 exception path, and the MIPS `is_uhi` helper. I already have a handful of those confirmed, so I'm mostly looking for a spot I haven't counted yet.

I'm checking the remaining QEMU targets for a semihosting check, including m68k translate, riscv translate, and the Arm helper code. I'm also wondering whether the twelfth reference sits in a macro or an inline helper that the call graph doesn't follow.

I'm still hunting for the twelfth reference, so next I'll look at semihosting/config.c and the stubs, plus the header, in case the definition's own file holds another call. The call graph only traced eight sites, so a direct grep-style check of those files seems like the honest next step.

I'm checking whether the twelfth reference is a call inside a function that the call graph only partly traced, so I'll try the riscv and Arm interrupt handlers to see whether either one calls semihosting_enabled.

I'm checking whether the twelfth reference sits in an arm, riscv, or m68k interrupt handler, since any of those would already show up as a callee. I'm running neighborhood lookups on those candidates, plus a helper_bkpt check, to see whether one of them calls semihosting_enabled.



- `get_neighborhood(name=arm_cpu_do_interrupt)` →

```
arm_cpu_do_interrupt — target/arm/helper.c:10022 [function] void arm_cpu_do_interrupt(CPUState *cs)
  reads: cs; writes: cs*; returns: -

CALLEES (20):
  arm_feature (target/arm/cpu.h:2349): reads env, feature; writes -; returns return(env->features &(1ULL << feature))!= 0;
  arm_log_exception (target/arm/helper.c:9094): reads cs; writes -; returns -
  arm_current_el (target/arm/cpu.h:2756): reads env; writes -; returns return arm_v7m_is_handler_mode(env)|| !(env->v7m.control[env->v7m.secure] & 1); | return extract32(env->pstate, 2, 2); | return 0; | return 2; | return 3; | return 3;
  syn_get_ec (target/arm/syndrome.h:85): reads syn; writes -; returns return syn >> ARM_EL_EC_SHIFT;
  excp_is_internal (target/arm/internals.h:42): reads excp; writes -; returns return excp == EXCP_INTERRUPT || excp == EXCP_HLT || excp == EXCP_DEBUG || excp == EXCP_HALTED || excp == EXCP_EXCEPTION_EXIT || excp == EXCP_KERNEL_TRAP || excp == EXCP_SEMIHOST;
  qemu_loglevel_mask (include/qemu/log-for-trace.h:27): reads mask; writes -; returns return(qemu_loglevel & mask)!= 0;
  arm_handle_psci_call (target/arm/internals.h:298 (1 of 2 definitions)): reads -; writes -; returns -
  arm_is_psci_call (target/arm/internals.h:294 (1 of 2 definitions)): reads -; writes -; returns return false;
  handle_semihosting (target/arm/helper.c:9992): reads cs; writes -; returns -
  qemu_mutex_iothread_locked (stubs/iothread-lock.c:4): reads -; writes -; returns return false;
  arm_call_pre_el_change_hook (target/arm/internals.h:630): reads cpu; writes cpu*; returns -
  arm_cpu_do_interrupt_aarch32 (target/arm/helper.c:9519): reads cs; writes -; returns -
  arm_cpu_do_interrupt_aarch64 (target/arm/helper.c:9794): reads cs; writes -; returns -
  arm_el_is_aa64 (target/arm/cpu.h:2442): reads el, env; writes -; returns return aa64; | return aa64; | return aa64;
  arm_call_el_change_hook (target/arm/internals.h:637): reads cpu; writes cpu*; returns -
  assert [macro]: #define assert(x) g_assert(x)
  qemu_log_mask [macro]: #define qemu_log_mask(MASK, FMT, ...) \
  kvm_enabled [macro (1 of 2 definitions)]: #define kvm_enabled() (0)
  not defined in this repository: ARM_CPU, g_assert

CALLERS (3):
  hvf_raise_exception (target/arm/hvf/hvf.c:643): arm_cpu_do_interrupt(cpu);
  kvm_inject_arm_sea (target/arm/kvm64.c:995): arm_cpu_do_interrupt(c);
  kvm_arm_handle_debug (target/arm/kvm64.c:1575): arm_cpu_do_interrupt(cs);
```

- `get_neighborhood(name=riscv_cpu_do_interrupt)` →

```
riscv_cpu_do_interrupt — target/riscv/cpu_helper.c:1571 [function] void riscv_cpu_do_interrupt(CPUState *cs)
  reads: cs; writes: cs*; returns: -

CALLEES (15):
  riscv_cpu_set_mode (target/riscv/cpu_helper.c:665): reads env, newpriv; writes env*; returns -
  set_field (target/cris/mmu.c:97 (1 of 5 definitions)): reads dst, offset, val, width; writes dst*; returns -
  get_field (disas/m68k.c:4675 (1 of 7 definitions)): reads data, len, order, start, total_len; writes -; returns return result;
  riscv_cpu_set_virt_enabled (target/riscv/cpu_helper.c:565): reads enable, env; writes env*; returns -
  riscv_cpu_virt_enabled (target/riscv/cpu_helper.c:556): reads env; writes -; returns return false; | return get_field(env->virt, VIRT_ONOFF);
  riscv_cpu_swap_hypervisor_regs (target/riscv/cpu_helper.c:472): reads env; writes env*; returns -
  riscv_has_ext (target/riscv/cpu.h:510): reads env, ext; writes -; returns return(env->misa_ext & ext)!= 0;
  riscv_cpu_get_trap_name (target/riscv/cpu.c:204): reads async, cause; writes -; returns return(cause < ARRAY_SIZE(riscv_intr_names))? riscv_intr_names[cause] : "(unknown)"; | return(cause < ARRAY_SIZE(riscv_excp_names))? riscv_excp_names[cause] : "(unknown)";
  riscv_cpu_xlen (target/riscv/cpu.h:662): reads env; writes -; returns return 16 << env->xl;
  riscv_transformed_insn (target/riscv/cpu_helper.c:1359): reads env, insn, taddr; writes -; returns return xinsn;
  do_common_semihosting (semihosting/arm-compat-semi.c:361): reads cs; writes cs*; returns -
  qemu_log_mask [macro]: #define qemu_log_mask(MASK, FMT, ...) \
  assert [macro]: #define assert(x) g_assert(x)
  not defined in this repository: trace_riscv_trap, RISCV_CPU

CALLERS (1):
  riscv_cpu_exec_interrupt (target/riscv/cpu_helper.c:439): riscv_cpu_do_interrupt(cs);
```

- `get_neighborhood(name=trans_ebreak)` →

```
{
  "error": "trans_ebreak: no in-repo definition in old version"
}
```

- `get_neighborhood(name=disas_exc)` →

```
disas_exc — target/arm/translate-a64.c:2154 [function] static void disas_exc(DisasContext *s, uint32_t insn)
  reads: insn, s; writes: -; returns: -

CALLEES (16):
  extract32 (include/qemu/bitops.h:336): reads length, start, value; writes -; returns return(value >> start)&(~0U >>(32 - length));
  unallocated_encoding (target/arm/translate.c:1145): reads s; writes -; returns -
  gen_exception_internal_insn (target/arm/translate-a64.c:343 (1 of 2 definitions)): reads excp, pc, s; writes s*; returns -
  semihosting_enabled (include/semihosting/semihost.h:30 (1 of 3 definitions)): reads -; writes -; returns return true;
  gen_exception_bkpt_insn (target/arm/translate-a64.c:350 (1 of 2 definitions)): reads s, syndrome; writes s*; returns -
  syn_aa64_bkpt (target/arm/syndrome.h:136): reads imm16; writes -; returns return(EC_AA64_BKPT << ARM_EL_EC_SHIFT)| ARM_EL_IL |(imm16 & 0xffff);
  gen_exception_insn_el (target/arm/translate.c:1119): reads excp, pc, s, syn, target_el; writes -; returns -
  syn_aa64_smc (target/arm/syndrome.h:115): reads imm16; writes -; returns return(EC_AA64_SMC << ARM_EL_EC_SHIFT)| ARM_EL_IL |(imm16 & 0xffff);
  gen_ss_advance (target/arm/translate.h:322): reads s; writes s*; returns -
  tcg_constant_i32 (include/tcg/tcg.h:1043): reads val; writes -; returns return temp_tcgv_i32(tcg_constant_internal(TCG_TYPE_I32, val));
  gen_a64_set_pc_im (target/arm/translate-a64.c:151 (1 of 2 definitions)): reads val; writes -; returns -
  syn_aa64_hvc (target/arm/syndrome.h:110): reads imm16; writes -; returns return(EC_AA64_HVC << ARM_EL_EC_SHIFT)| ARM_EL_IL |(imm16 & 0xffff);
  gen_exception_insn (target/arm/translate.c:1125): reads excp, pc, s, syn; writes s*; returns -
  syn_aa64_svc (target/arm/syndrome.h:105): reads imm16; writes -; returns return(EC_AA64_SVC << ARM_EL_EC_SHIFT)| ARM_EL_IL |(imm16 & 0xffff);
  not defined in this repository: gen_helper_pre_smc, gen_helper_pre_hvc

CALLERS (1):
  disas_b_exc_sys (target/arm/translate-a64.c:2467): disas_exc(s, insn);
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 16111+345, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

