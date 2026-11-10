# Impact-analysis transcript — qemu @ 5202861b20d7 — anthropic:claude-haiku-5-5

- target: `semihosting_enabled` (include/semihosting/semihost.h), arity 0->1
- truth: [['softmmu/vl.c', 'qemu_apply_machine_options'], ['target/arm/translate-a64.c', 'disas_exc'], ['target/arm/translate.c', 'gen_hlt'], ['target/arm/translate.c', 'trans_BKPT'], ['target/arm/translate.c', 'trans_SVC'], ['target/m68k/op_helper.c', 'cf_interrupt_all'], ['target/mips/tcg/translate.c', 'is_uhi'], ['target/nios2/translate.c', 'gen_break'], ['target/xtensa/translate.c', 'test_exceptions_simcall'], ['target/xtensa/translate.c', 'translate_simcall']]

## Self-navigation arm

### Turn 1  _(tok 1218+124, stop=tool_use)_

**Reasoning:** I'm going to grep the repo for `semihosting_enabled` to find where it's used.



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

### Turn 2  _(tok 1872+1303, stop=tool_use)_

**Reasoning:** I need to find the enclosing function for each call site, so I'll read the code around every match. I'm also wondering whether the grep could miss calls split across lines or made through macros or function pointers, though I'll treat that as unlikely for now.



**Says:** Grep found 15 matches. I need the enclosing function for each call site, so I'll read the surrounding code.

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

- `read_file(path=target/nios2/translate.c, version=old, start_line=805, end_line=825)` →

```
target/nios2/translate.c lines 805-825 of 1118
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

- `read_file(path=stubs/semihost.c, version=old)` →

```
stubs/semihost.c lines 1-71 of 71
    1| /*
    2|  * Semihosting Stubs for SoftMMU
    3|  *
    4|  * Copyright (c) 2019 Linaro Ltd
    5|  *
    6|  * Stubs for SoftMMU targets that don't actually do semihosting.
    7|  *
    8|  * SPDX-License-Identifier: GPL-2.0-or-later
    9|  */
   10| 
   11| #include "qemu/osdep.h"
   12| #include "qemu/option.h"
   13| #include "qemu/error-report.h"
   14| #include "semihosting/semihost.h"
   15| 
   16| /* Empty config */
   17| QemuOptsList qemu_semihosting_config_opts = {
   18|     .name = "",
   19|     .head = QTAILQ_HEAD_INITIALIZER(qemu_semihosting_config_opts.head),
   20|     .desc = {
   21|         { /* end of list */ }
   22|     },
   23| };
   24| 
   25| /* Queries to config status default to off */
   26| bool semihosting_enabled(void)
   27| {
   28|     return false;
   29| }
   30| 
   31| SemihostingTarget semihosting_get_target(void)
   32| {
   33|     return SEMIHOSTING_TARGET_AUTO;
   34| }
   35| 
   36| /*
   37|  * All the rest are empty subs. We could g_assert_not_reached() but
   38|  * that adds extra weight to the final binary. Waste not want not.
   39|  */
   40| void qemu_semihosting_enable(void)
   41| {
   42| }
   43| 
   44| int qemu_semihosting_config_options(const char *optarg)
   45| {
   46|     return 1;
   47| }
   48| 
   49| const char *semihosting_get_arg(int i)
   50| {
   51|     return NULL;
   52| }
   53| 
   54| int semihosting_get_argc(void)
   55| {
   56|     return 0;
   57| }
   58| 
   59| const char *semihosting_get_cmdline(void)
   60| {
   61|     return NULL;
   62| }
   63| 
   64| void semihosting_arg_fallback(const char *file, const char *cmd)
   65| {
   66| }
   67| 
   68| void qemu_semihosting_chardev_init(void)
   69| {
   70| }
   71| 
```

### Turn 3  _(tok 8257+758, stop=tool_use)_

**Reasoning:** I need to pin down which function encloses the translate-a64 call at line 2222, probably disas_exc, and verify that. I also want to check the arm translate.c line 1172 (gen_hlt) around 1150, the BKPT and SVC handlers at 6559 and 8767 (the SVC one is already confirmed), the m68k function near line 206 that looks like an interrupt handler, and the Xtensa exception simcall tests near 2369 and 2371.

I'm also checking the other handlers the grep turned up, the nios2 gen_break and the mips is_uhi, and I still need the function headers for the translate-a64 call at 2222, the arm translate.c line 1172, and the m68k line 206.



**Says:** Most enclosing functions are now clear. Three still need their function headers: the A64 HLT site, the A32 `gen_hlt` site, and the m68k exception site.

- `grep(pattern=^(static |void |bool )[a-z_0-9]+\(, version=old, path_glob=target/arm/translate-a64.c, max_results=500)` →

```
8 matches
target/arm/translate-a64.c:71:void a64_translate_init(void)
target/arm/translate-a64.c:151:void gen_a64_set_pc_im(uint64_t val)
target/arm/translate-a64.c:553:void write_fp_dreg(DisasContext *s, int reg, TCGv_i64 v)
target/arm/translate-a64.c:1191:bool sve_access_check(DisasContext *s)
target/arm/translate-a64.c:1230:bool sme_enabled_check(DisasContext *s)
target/arm/translate-a64.c:1245:bool sme_enabled_check_with_svcr(DisasContext *s, unsigned req)
target/arm/translate-a64.c:4412:bool logic_imm_decode_wmask(uint64_t *result, unsigned int immn,
target/arm/translate-a64.c:14234:void gen_gvec_rax1(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
```

- `grep(pattern=^(static |void |bool )[a-zA-Z_0-9]+\(, version=old, path_glob=target/arm/translate.c, max_results=500)` →

```
60 matches
target/arm/translate.c:69:void arm_translate_init(void)
target/arm/translate.c:162:void arm_gen_condlabel(DisasContext *s)
target/arm/translate.c:186:void store_cpu_offset(TCGv_i32 var, int offset, int size)
target/arm/translate.c:274:void load_reg_var(DisasContext *s, TCGv_i32 var, int reg)
target/arm/translate.c:302:void store_reg(DisasContext *s, int reg, TCGv_i32 var)
target/arm/translate.c:346:void gen_set_cpsr(TCGv_i32 var, uint32_t mask)
target/arm/translate.c:393:void clear_eci_state(DisasContext *s)
target/arm/translate.c:421:void gen_rev16(TCGv_i32 dest, TCGv_i32 var)
target/arm/translate.c:660:void arm_test_cc(DisasCompare *cmp, int cc)
target/arm/translate.c:746:void arm_free_cc(DisasCompare *cmp)
target/arm/translate.c:753:void arm_jump_cc(DisasCompare *cmp, TCGLabel *label)
target/arm/translate.c:758:void arm_gen_test_cc(int cc, TCGLabel *label)
target/arm/translate.c:766:void gen_set_condexec(DisasContext *s)
target/arm/translate.c:775:void gen_set_pc_im(DisasContext *s, target_ulong val)
target/arm/translate.c:967:void gen_aa32_ld_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:975:void gen_aa32_st_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:983:void gen_aa32_ld_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:997:void gen_aa32_st_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:1014:void gen_aa32_ld_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1020:void gen_aa32_st_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1026:void gen_aa32_ld_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1032:void gen_aa32_st_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1119:void gen_exception_insn_el(DisasContext *s, uint64_t pc, int excp,
target/arm/translate.c:1125:void gen_exception_insn(DisasContext *s, uint64_t pc, int excp, uint32_t syn)
target/arm/translate.c:1145:void unallocated_encoding(DisasContext *s)
target/arm/translate.c:1152:void gen_lookup_tb(DisasContext *s)
target/arm/translate.c:1222:void read_neon_element32(TCGv_i32 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1248:void read_neon_element64(TCGv_i64 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1267:void write_neon_element32(TCGv_i32 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1286:void write_neon_element64(TCGv_i64 src, int reg, int ele, MemOp memop)
target/arm/translate.c:2986:void gen_gvec_sqrdmlah_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:2996:void gen_gvec_sqrdmlsh_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3089:void gen_gvec_ssra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3165:void gen_gvec_usra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3284:void gen_gvec_srshr(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3376:void gen_gvec_srsra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3491:void gen_gvec_urshr(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3602:void gen_gvec_ursra(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3693:void gen_gvec_sri(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3786:void gen_gvec_sli(unsigned vece, uint32_t rd_ofs, uint32_t rm_ofs,
target/arm/translate.c:3892:void gen_gvec_mla(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3924:void gen_gvec_mls(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:3964:void gen_cmtst_i64(TCGv_i64 d, TCGv_i64 a, TCGv_i64 b)
target/arm/translate.c:3978:void gen_gvec_cmtst(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4004:void gen_ushl_i32(TCGv_i32 dst, TCGv_i32 src, TCGv_i32 shift)
target/arm/translate.c:4031:void gen_ushl_i64(TCGv_i64 dst, TCGv_i64 src, TCGv_i64 shift)
target/arm/translate.c:4116:void gen_gvec_ushl(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4144:void gen_sshl_i32(TCGv_i32 dst, TCGv_i32 src, TCGv_i32 shift)
target/arm/translate.c:4172:void gen_sshl_i64(TCGv_i64 dst, TCGv_i64 src, TCGv_i64 shift)
target/arm/translate.c:4250:void gen_gvec_sshl(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4289:void gen_gvec_uqadd_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4332:void gen_gvec_sqadd_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4375:void gen_gvec_uqsub_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4418:void gen_gvec_sqsub_qc(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4480:void gen_gvec_sabd(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4540:void gen_gvec_uabd(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4594:void gen_gvec_saba(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4653:void gen_gvec_uaba(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:9895:void gen_intermediate_code(CPUState *cpu, TranslationBlock *tb, int max_insns,
target/arm/translate.c:9914:void restore_state_to_opc(CPUARMState *env, TranslationBlock *tb,
```

- `grep(pattern=^[a-z].*\(, version=old, path_glob=target/m68k/op_helper.c, max_results=500)` →

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

### Turn 4  _(tok 14290+677, stop=tool_use)_

**Reasoning:** I'm checking which function the call at line 2222 falls inside, since the grep for static functions in that file came back empty and the signature may have its parameters on the same line as the name.

I'm checking the regex again, since the "static void" pattern wouldn't match when "void" follows "static" in the signature. I'll switch to a different grep for the disas functions, and I still need the gen_hlt function in translate.c.



**Says:** The m68k site is inside `cf_interrupt_all` (line 187). The A64 and A32 sites are still unresolved, so I'll read backwards from them to find their headers.

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

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 5  _(tok 16027+345, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "medium"}`

**Score (self):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Index arm (generic tools + GNU Global references)

### Turn 1  _(tok 1387+80, stop=tool_use)_

**Reasoning:** I'll start by pulling every reference to semihosting_enabled using find_references.



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

### Turn 2  _(tok 2009+165, stop=tool_use)_

**Reasoning:** I'm worried GNU Global might miss some references, so I want to double-check with grep. I'll search across the repo.



**Says:** The index returned 12 references. I'll cross-check with a text search, since GNU Global can miss some uses.

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

### Turn 3  _(tok 2704+1391, stop=tool_use)_

**Reasoning:** The grep also picked up the inline definition in the header at line 30, which is the definition itself rather than a call site. The other matches are the six call sites, in softmmu/vl.c, several target/arm files, and target/m68k/op_helper.c. I still need to find which function encloses each one, so I'll read the surrounding context at each location.

I'm also checking the remaining call sites: the MIPS translator at line 12090, nios2 at line 821, and three xtensa spots around lines 2369 to 2381. I still need the enclosing function for each one.



**Says:** The text search matches the same call sites; the extra hits are the header's inline definition and the stub/config definitions, which are excluded. Now I need the enclosing function for each call site.

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

- `read_file(path=target/nios2/translate.c, version=old, start_line=805, end_line=828)` →

```
target/nios2/translate.c lines 805-828 of 1118
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

### Turn 4  _(tok 8430+501, stop=tool_use)_

**Reasoning:** I need to pin down which function encloses line 1172 in translate.c, and I suspect it's gen_hlt. Reading a bit above line 1160 should confirm the name. The a64 translator's line 2222 probably sits in disas_exc, though I still need to check that. I'll grep for the function definitions to settle both.



**Says:** Most enclosing functions are clear from the context. I still need the function headers for the Arm A64 site at line 2222 and the Arm A32/T32 site at line 1172.

- `grep(pattern=^static (void|bool|int|uint32_t) \w+\(|^(void|bool) \w+\(, version=old, path_glob=target/arm/translate-a64.c, max_results=400)` →

```
232 matches (showing 200)
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
target/arm/translate-a64.c:312:static void a64_test_cc(DisasCompare64 *c64, int cc)
target/arm/translate-a64.c:327:static void a64_free_cc(DisasCompare64 *c64)
target/arm/translate-a64.c:332:static void gen_rebuild_hflags(DisasContext *s)
target/arm/translate-a64.c:337:static void gen_exception_internal(int excp)
target/arm/translate-a64.c:343:static void gen_exception_internal_insn(DisasContext *s, uint64_t pc, int excp)
target/arm/translate-a64.c:350:static void gen_exception_bkpt_insn(DisasContext *s, uint32_t syndrome)
target/arm/translate-a64.c:357:static void gen_step_complete_exception(DisasContext *s)
target/arm/translate-a64.c:399:static void init_tmp_a64_array(DisasContext *s)
target/arm/translate-a64.c:407:static void free_tmp_a64(DisasContext *s)
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
target/arm/translate-a64.c:11150:static void do_narrow_round_high_u32(TCGv_i32 res, TCGv_i64 in)
target/arm/translate-a64.c:11156:static void handle_3rd_narrowing(DisasContext *s, int is_q, int is_u, int size,
target/arm/translate-a64.c:11202:static void disas_simd_three_reg_diff(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:11314:static void disas_simd_3same_logic(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:11364:static void handle_simd_3same_pair(DisasContext *s, int is_q, int u, int opcode,
target/arm/translate-a64.c:11515:static void disas_simd_3same_float(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:11604:static void disas_simd_3same_int(DisasContext *s, uint32_t insn)
target/arm/translate-a64.c:11871:static void disas_simd_three_reg_same(DisasContext *s, uint32_t insn)
```

- `grep(pattern=^static (void|bool|int|uint32_t) \w+\(|^(void|bool) \w+\(, version=old, path_glob=target/arm/translate.c, max_results=400)` →

```
423 matches (showing 200)
target/arm/translate.c:69:void arm_translate_init(void)
target/arm/translate.c:162:void arm_gen_condlabel(DisasContext *s)
target/arm/translate.c:186:void store_cpu_offset(TCGv_i32 var, int offset, int size)
target/arm/translate.c:202:static void disas_set_da_iss(DisasContext *s, MemOp memop, ISSInfo issinfo)
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
target/arm/translate.c:466:static void gen_add_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:473:static void gen_sub_carry(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:481:static void gen_add_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:495:static void gen_adc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:523:static void gen_sub_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:538:static void gen_sbc_CC(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:563:static void gen_sar(TCGv_i32 dest, TCGv_i32 t0, TCGv_i32 t1)
target/arm/translate.c:573:static void shifter_out_im(TCGv_i32 var, int shift)
target/arm/translate.c:660:void arm_test_cc(DisasCompare *cmp, int cc)
target/arm/translate.c:746:void arm_free_cc(DisasCompare *cmp)
target/arm/translate.c:753:void arm_jump_cc(DisasCompare *cmp, TCGLabel *label)
target/arm/translate.c:758:void arm_gen_test_cc(int cc, TCGLabel *label)
target/arm/translate.c:766:void gen_set_condexec(DisasContext *s)
target/arm/translate.c:775:void gen_set_pc_im(DisasContext *s, target_ulong val)
target/arm/translate.c:967:void gen_aa32_ld_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:975:void gen_aa32_st_internal_i32(DisasContext *s, TCGv_i32 val,
target/arm/translate.c:983:void gen_aa32_ld_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:997:void gen_aa32_st_internal_i64(DisasContext *s, TCGv_i64 val,
target/arm/translate.c:1014:void gen_aa32_ld_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1020:void gen_aa32_st_i32(DisasContext *s, TCGv_i32 val, TCGv_i32 a32,
target/arm/translate.c:1026:void gen_aa32_ld_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
target/arm/translate.c:1032:void gen_aa32_st_i64(DisasContext *s, TCGv_i64 val, TCGv_i32 a32,
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
target/arm/translate.c:1222:void read_neon_element32(TCGv_i32 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1248:void read_neon_element64(TCGv_i64 dest, int reg, int ele, MemOp memop)
target/arm/translate.c:1267:void write_neon_element32(TCGv_i32 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1286:void write_neon_element64(TCGv_i64 src, int reg, int ele, MemOp memop)
target/arm/translate.c:1435:static void gen_op_iwmmxt_set_mup(void)
target/arm/translate.c:1443:static void gen_op_iwmmxt_set_cup(void)
target/arm/translate.c:1451:static void gen_op_iwmmxt_setpsr_nz(void)
target/arm/translate.c:1524:static int disas_iwmmxt_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:2524:static int disas_dsp_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:2591:static void gen_goto_ptr(void)
target/arm/translate.c:2600:static void gen_goto_tb(DisasContext *s, int n, target_ulong dest)
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
target/arm/translate.c:4645:static void gen_uaba_vec(unsigned vece, TCGv_vec d, TCGv_vec a, TCGv_vec b)
target/arm/translate.c:4653:void gen_gvec_uaba(unsigned vece, uint32_t rd_ofs, uint32_t rn_ofs,
target/arm/translate.c:4688:static void do_coproc_insn(DisasContext *s, int cpnum, int is64,
target/arm/translate.c:4910:static void disas_xscale_insn(DisasContext *s, uint32_t insn)
target/arm/translate.c:4928:static void gen_storeq_reg(DisasContext *s, int rlow, int rhigh, TCGv_i64 val)
target/arm/translate.c:4940:static void gen_addq(DisasContext *s, TCGv_i64 val, int rlow, int rhigh)
target/arm/translate.c:4958:static void gen_logicq_cc(TCGv_i32 lo, TCGv_i32 hi)
target/arm/translate.c:4970:static void gen_load_exclusive(DisasContext *s, int rt, int rt2,
target/arm/translate.c:5012:static void gen_clrex(DisasContext *s)
target/arm/translate.c:5017:static void gen_store_exclusive(DisasContext *s, int rd, int rt, int rt2,
target/arm/translate.c:5101:static void gen_srs(DisasContext *s,
target/arm/translate.c:5216:static void arm_skip_unless(DisasContext *s, uint32_t cond)
target/arm/translate.c:5228:static int t32_expandimm_rot(DisasContext *s, int x)
target/arm/translate.c:5234:static int t32_expandimm_imm(DisasContext *s, int x)
target/arm/translate.c:5259:static int t32_branch24(DisasContext *s, int x)
target/arm/translate.c:5267:static int t16_setflags(DisasContext *s)
target/arm/translate.c:5272:static int t16_push_list(DisasContext *s, int x)
target/arm/translate.c:5277:static int t16_pop_list(DisasContext *s, int x)
target/arm/translate.c:5291:static bool valid_cp(DisasContext *s, int cp)
target/arm/translate.c:5320:static bool trans_MCR(DisasContext *s, arg_MCR *a)
target/arm/translate.c:5330:static bool trans_MRC(DisasContext *s, arg_MRC *a)
target/arm/translate.c:5340:static bool trans_MCRR(DisasContext *s, arg_MCRR *a)
target/arm/translate.c:5350:static bool trans_MRRC(DisasContext *s, arg_MRRC *a)
target/arm/translate.c:5361:static void gen_rsb(TCGv_i32 dst, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:5366:static void gen_rsb_CC(TCGv_i32 dst, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:5371:static void gen_rsc(TCGv_i32 dest, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:5376:static void gen_rsc_CC(TCGv_i32 dest, TCGv_i32 a, TCGv_i32 b)
target/arm/translate.c:5398:static bool store_reg_kind(DisasContext *s, int rd,
target/arm/translate.c:5429:static bool op_s_rrr_shi(DisasContext *s, arg_s_rrr_shi *a,
target/arm/translate.c:5448:static bool op_s_rxr_shi(DisasContext *s, arg_s_rrr_shi *a,
target/arm/translate.c:5470:static bool op_s_rrr_shr(DisasContext *s, arg_s_rrr_shr *a,
target/arm/translate.c:5490:static bool op_s_rxr_shr(DisasContext *s, arg_s_rrr_shr *a,
target/arm/translate.c:5517:static bool op_s_rri_rot(DisasContext *s, arg_s_rri_rot *a,
target/arm/translate.c:5538:static bool op_s_rxi_rot(DisasContext *s, arg_s_rri_rot *a,
```

### Turn 5  _(tok 28347+447, stop=tool_use)_

**Reasoning:** I'm checking that line 2222 falls inside disas_exc, which runs from 2154 to 2257, so that's fine. In translate.c, gen_lookup_tb sits at line 1152, and the 1160–1175 function comes after it but before read_neon_element32 at 1222, so there's a function in that gap that doesn't match the pattern I'm looking for.

I'm checking whether gen_hlt at line 1160 is the function that sits between gen_lookup_tb and read_neon_element32. I'll read lines 1152 to 1160 to confirm, and I'm also noting that trans_BKPT is near line 6559 and trans_SVC near 8767.



**Says:** Line 2222 in translate-a64.c falls inside `disas_exc` (2154–2257). For translate.c line 1172, the enclosing function is not shown by that grep, so I'll read its header.

- `read_file(path=target/arm/translate.c, version=old, start_line=1150, end_line=1162)` →

```
target/arm/translate.c lines 1150-1162 of 9927
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
 1161|      * Architecturally, it is an external halting debug instruction.
 1162|      * Since QEMU doesn't implement external debug, we treat this as
```

_(budget of 20,000 tokens exhausted — forcing submission)_

### Turn 6  _(tok 29229+371, stop=tool_use, forced)_

- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "do_interrupt_m68k_hwaddr", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "medium"}`

**Score (index):** `{"n_pred": 10, "n_truth": 10, "tp": 9, "precision": 0.9, "recall": 0.9, "f1": 0.9}`

## Tool arm

### Turn 1  _(tok 3753+217, stop=tool_use)_

**Reasoning:** I'm going to pull up every call site, starting with get_callers and then a grep search.



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

### Turn 2  _(tok 5100+833, stop=tool_use)_

**Reasoning:** I'm tallying the grep matches against the callers list, which has duplicates from xtensa, and that leaves 10 unique functions. I'm now checking whether the is_uhi match at line 12090 in target/mips falls within that range.

I'm going to check the enclosing functions for a few of the matches, starting with the mips is_uhi hit at 12090 and the arm trans_BKPT at 6559, to confirm the callers tool's names are right.



- `get_context_at(file=target/mips/tcg/translate.c, line=12090, version=old)` →

```
is_uhi — target/mips/tcg/translate.c:12085 [function] static inline bool is_uhi(int sdbbp_code)
  reads: sdbbp_code; writes: -; returns: return false; | return semihosting_enabled()&& sdbbp_code == 1;

SLICE around line 12090 (def-use, level 2; '>' marks the seed):
static inline bool is_uhi(int sdbbp_code) {
   #ifdef ...
   ...
   #else None
>  return semihosting_enabled()&& sdbbp_code == 1;
   #endif
}

CALLEES (1):
  semihosting_enabled (include/semihosting/semihost.h:30 (1 of 3 definitions)): reads -; writes -; returns return true;

CALLERS (2):
  decode_opc_special_r6 (target/mips/tcg/translate.c:13901): if (is_uhi(extract32(ctx->opcode, 6, 20))) {
  decode_opc_special2_legacy (target/mips/tcg/translate.c:14313): if (is_uhi(extract32(ctx->opcode, 6, 20))) {
```

- `get_context_at(file=target/arm/translate.c, line=6559, version=old)` →

```
{
  "error": "target/arm/translate.c:6559 is not inside a function definition in the old version"
}
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

### Turn 3  _(tok 8744+475, stop=tool_use)_

**Reasoning:** I'm checking whether line 6559 in the arm file sits outside any function, and I'm thinking it might be a macro-generated body like trans_BKPT inside a DEF. I'll open the file around that line to see.



**Says:** The ARM call at line 6559 isn't inside a function according to the tool, so I'll check the source directly.

- `read_file(path=target/arm/translate.c, version=old, start_line=6545, end_line=6570)` →

```
target/arm/translate.c lines 6545-6570 of 9927
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
```

- `read_file(path=target/arm/translate.c, version=old, start_line=8755, end_line=8775)` →

```
target/arm/translate.c lines 8755-8775 of 9927
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

### Turn 4  _(tok 10639+617, stop=tool_use)_

**Reasoning:** I've confirmed that trans_BKPT and trans_SVC are both static bool functions, and the line 6559 lookup failure looks like a quirk of the line-number tool rather than anything real. Line 6559 falls inside trans_BKPT, which spans lines 6551 to 6569. I'm also going to check the callers in translate-a64's disas_exc, since the callers tool already listed them, and the grep's 15 matches all check out across vl.c, a64, and arm.

I'm checking the xtensa match at line 2381 to confirm it sits inside translate_simcall, which the tool already indicated.



- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "high"}`

**Score (tool):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

## Semantic arm

### Turn 1  _(tok 3205+106, stop=tool_use)_

**Reasoning:** I'm calling get_callers on semihosting_enabled, asking for a high limit so I get the full set of callers.



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

### Turn 2  _(tok 3865+345, stop=tool_use)_

**Reasoning:** I'm checking the version field, since the output came back as "old" even though I expected the working copy by default. I'll rerun the call with version "work" to confirm what's on disk, and I also want to look for macros or other callers.

I'm also weighing whether macros or inline header calls could be slipping past the caller search, so I'll query the working version to see what's actually on disk.



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

### Turn 3  _(tok 5104+217, stop=tool_use)_

**Reasoning:** I'm checking whether "old" is just the parent of HEAD, since the default revision seems to be the server's commit or HEAD. That would mean the current working state could be HEAD itself, so I'll look at the "work" and "new" versions next.



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

### Turn 4  _(tok 5875+1756, stop=tool_use)_

**Reasoning:** I'm checking whether "old" is HEAD's parent, since the work version may differ. The query tools only accept a rev parameter, not a version selector, so I can't pull the work tree directly.

I'm trying to pin down which version the tools report, since none of them accept a "work" selector. The rev parameter seems to be the only lever, and "old" appears to be the parent of whatever rev points to. I'm weighing whether I can reach the new state through HEAD or a commit SHA, but I don't have the SHA, and the default version still looks like "old" either way.

I'm testing whether resolve_symbol at HEAD also reports version "old", which would mean the tools don't expose the new state directly. Since the function is a static inline in a header, I'm wondering whether some callers could sit outside what get_callers returns, so I'm weighing whether to check neighboring revisions to see whether the results change.

I'm trying to reach callers beyond what get_callers returned, since some QEMU semihosting checks might live in other architecture backends. I'll trust the tool's results but want to confirm a few known spots like the ARM and RISC-V translators.

I'm settling on the list of unique callers now, since the two call sites in the test file are the same function and should only be counted once. I'll skip any further completeness checks and submit the ten distinct functions.



- **submit_callers** → `{"callers": [{"function": "qemu_apply_machine_options", "file": "softmmu/vl.c"}, {"function": "disas_exc", "file": "target/arm/translate-a64.c"}, {"function": "gen_hlt", "file": "target/arm/translate.c"}, {"function": "trans_BKPT", "file": "target/arm/translate.c"}, {"function": "trans_SVC", "file": "target/arm/translate.c"}, {"function": "cf_interrupt_all", "file": "target/m68k/op_helper.c"}, {"function": "is_uhi", "file": "target/mips/tcg/translate.c"}, {"function": "gen_break", "file": "target/nios2/translate.c"}, {"function": "test_exceptions_simcall", "file": "target/xtensa/translate.c"}, {"function": "translate_simcall", "file": "target/xtensa/translate.c"}], "confidence_overall": "medium"}`

**Score (semantic):** `{"n_pred": 10, "n_truth": 10, "tp": 10, "precision": 1.0, "recall": 1.0, "f1": 1.0}`

