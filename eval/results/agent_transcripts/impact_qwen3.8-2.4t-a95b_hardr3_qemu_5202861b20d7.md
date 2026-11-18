# Impact-analysis transcript — qemu @ 5202861b20d7 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `semihosting_enabled` (include/semihosting/semihost.h), arity 0->1
- truth: [['softmmu/vl.c', 'qemu_apply_machine_options'], ['target/arm/translate-a64.c', 'disas_exc'], ['target/arm/translate.c', 'gen_hlt'], ['target/arm/translate.c', 'trans_BKPT'], ['target/arm/translate.c', 'trans_SVC'], ['target/m68k/op_helper.c', 'cf_interrupt_all'], ['target/mips/tcg/translate.c', 'is_uhi'], ['target/nios2/translate.c', 'gen_break'], ['target/xtensa/translate.c', 'test_exceptions_simcall'], ['target/xtensa/translate.c', 'translate_simcall']]

## Self-navigation arm

### Turn 1  _(tok 908+69, stop=tool_use)_

**Reasoning:** I'm searching for where semihosting_enabled is used.

- `grep(pattern=semihosting_enabled, version=old, max_results=100)` →

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

### Turn 2  _(tok 1386+350, stop=tool_use)_

**Reasoning:** We need to find the function that contains each call site. Let's read around each location.

1. softmmu/vl.c:1825
2. target/arm/translate-a64.c:2222
3. target/arm/translate.c:1172
4. target/arm/translate.c:6559
5. target/arm/translate.c:8767
6. target/m68k/op_helper.c:206
7. target/mips/tcg/translate.c:12090
8. target/nios2/translate.c:821
9. target/xtensa/translate.c:2369, 2371, 2381

Let's read each of them.


**Says:** Found 15 matches. Excluding the definitions/prototypes, I need to identify the enclosing function for each call site. Let me read each location.



- `read_file(path=softmmu/vl.c, start_line=1780, end_line=1840, version=old)` →

```
softmmu/vl.c lines 1780-1840 of 3593
 1780|         g_str_equal(type, "qtest")) {
 1781|         return false;
 1782|     }
 1783| 
 1784| #if defined(CONFIG_VHOST_USER) && defined(CONFIG_LINUX)
 1785|     /* Reason: cryptodev-vhost-user property "chardev" */
 1786|     if (g_str_equal(type, "cryptodev-vhost-user")) {
 1787|         return false;
 1788|     }
 1789| #endif
 1790| 
 1791|     /* Reason: vhost-user-blk-server property "node-name" */
 1792|     if (g_str_equal(type, "vhost-user-blk-server")) {
 1793|         return false;
 1794|     }
 1795|     /*
 1796|      * Reason: filter-* property "netdev" etc.
 1797|      */
 1798|     if (g_str_equal(type, "filter-buffer") ||
 1799|         g_str_equal(type, "filter-dump") ||
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
 1831|         Error *blocker = NULL;
 1832|         error_setg(&blocker, QERR_REPLAY_NOT_SUPPORTED, "smp");
 1833|         replay_add_blocker(blocker);
 1834|     }
 1835| }
 1836| 
 1837| static void qemu_create_early_backends(void)
 1838| {
 1839|     MachineClass *machine_class = MACHINE_GET_CLASS(current_machine);
 1840| #if defined(CONFIG_SDL)
```

- `read_file(path=target/arm/translate-a64.c, start_line=2180, end_line=2240, version=old)` →

```
target/arm/translate-a64.c lines 2180-2240 of 15028
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
 2224|             /* In system mode, don't allow userspace access to semihosting,
 2225|              * to provide some semblance of security (and for consistency
 2226|              * with our 32-bit semihosting).
 2227|              */
 2228|             if (s->current_el == 0) {
 2229|                 unallocated_encoding(s);
 2230|                 break;
 2231|             }
 2232| #endif
 2233|             gen_exception_internal_insn(s, s->pc_curr, EXCP_SEMIHOST);
 2234|         } else {
 2235|             unallocated_encoding(s);
 2236|         }
 2237|         break;
 2238|     case 5:
 2239|         if (op2_ll < 1 || op2_ll > 3) {
 2240|             unallocated_encoding(s);
```

### Turn 3  _(tok 3654+138, stop=tool_use)_

**Reasoning:** I need to find the function containing line 2222 in translate-a64.c. This is inside something related to exception handling — probably `handle_sys`. Let me search backwards.

- `grep(max_results=50, path_glob=target/arm/translate-a64.c, pattern=^(static )?(void|bool|target_.*|int|DisasCompare) [a-zA-Z_0-, version=old)` →

```
232 matches (showing 50)
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
```

### Turn 4  _(tok 5621+128, stop=tool_use)_

**Reasoning:** I need to find the function that includes line 2222. Let me try grepping for function definitions around lines 2000–2222. I'll read around lines 2100–2160.

- `read_file(end_line=2160, path=target/arm/translate-a64.c, start_line=2090, version=old)` →

```
target/arm/translate-a64.c lines 2090-2160 of 15028
 2090|     }
 2091|     if (!isread && !(ri->type & ARM_CP_SUPPRESS_TB_END)) {
 2092|         /*
 2093|          * A write to any coprocessor regiser that ends a TB
 2094|          * must rebuild the hflags for the next TB.
 2095|          */
 2096|         gen_rebuild_hflags(s);
 2097|         /*
 2098|          * We default to ending the TB on a coprocessor register write,
 2099|          * but allow this to be suppressed by the register definition
 2100|          * (usually only necessary to work around guest bugs).
 2101|          */
 2102|         s->base.is_jmp = DISAS_UPDATE_EXIT;
 2103|     }
 2104| }
 2105| 
 2106| /* System
 2107|  *  31                 22 21  20 19 18 16 15   12 11    8 7   5 4    0
 2108|  * +---------------------+---+-----+-----+-------+-------+-----+------+
 2109|  * | 1 1 0 1 0 1 0 1 0 0 | L | op0 | op1 |  CRn  |  CRm  | op2 |  Rt  |
 2110|  * +---------------------+---+-----+-----+-------+-------+-----+------+
 2111|  */
 2112| static void disas_system(DisasContext *s, uint32_t insn)
 2113| {
 2114|     unsigned int l, op0, op1, crn, crm, op2, rt;
 2115|     l = extract32(insn, 21, 1);
 2116|     op0 = extract32(insn, 19, 2);
 2117|     op1 = extract32(insn, 16, 3);
 2118|     crn = extract32(insn, 12, 4);
 2119|     crm = extract32(insn, 8, 4);
 2120|     op2 = extract32(insn, 5, 3);
 2121|     rt = extract32(insn, 0, 5);
 2122| 
 2123|     if (op0 == 0) {
 2124|         if (l || rt != 31) {
 2125|             unallocated_encoding(s);
 2126|             return;
 2127|         }
 2128|         switch (crn) {
 2129|         case 2: /* HINT (including allocated hints like NOP, YIELD, etc) */
 2130|             handle_hint(s, insn, op1, op2, crm);
 2131|             break;
 2132|         case 3: /* CLREX, DSB, DMB, ISB */
 2133|             handle_sync(s, insn, op1, op2, crm);
 2134|             break;
 2135|         case 4: /* MSR (immediate) */
 2136|             handle_msr_i(s, insn, op1, op2, crm);
 2137|             break;
 2138|         default:
 2139|             unallocated_encoding(s);
 2140|             break;
 2141|         }
 2142|         return;
 2143|     }
 2144|     handle_sys(s, insn, l, op0, op1, op2, crn, crm, rt);
 2145| }
 2146| 
 2147| /* Exception generation
 2148|  *
 2149|  *  31             24 23 21 20                     5 4   2 1  0
 2150|  * +-----------------+-----+------------------------+-----+----+
 2151|  * | 1 1 0 1 0 1 0 0 | opc |          imm16         | op2 | LL |
 2152|  * +-----------------------+------------------------+----------+
 2153|  */
 2154| static void disas_exc(DisasContext *s, uint32_t insn)
 2155| {
 2156|     int opc = extract32(insn, 21, 3);
 2157|     int op2_ll = extract32(insn, 0, 5);
 2158|     int imm16 = extract32(insn, 5, 16);
 2159| 
 2160|     switch (opc) {
```

### Turn 5  _(tok 7077+157, stop=tool_use)_

**Reasoning:** Line 2222 is inside `disas_exc` (starts at line 2154).

Next, target/arm/translate.c: 1172, 6559, 8767. Let's take a look at each one.

**Says:** Line 2222 is in `disas_exc`. Now let's check the ARM translate.c call sites.



- `read_file(end_line=1180, path=target/arm/translate.c, start_line=1130, version=old)` →

```
target/arm/translate.c lines 1130-1180 of 9927
 1130|         gen_set_condexec(s);
 1131|         gen_set_pc_im(s, pc);
 1132|     }
 1133|     gen_exception(excp, syn);
 1134|     s->base.is_jmp = DISAS_NORETURN;
 1135| }
 1136| 
 1137| static void gen_exception_bkpt_insn(DisasContext *s, uint32_t syn)
 1138| {
 1139|     gen_set_condexec(s);
 1140|     gen_set_pc_im(s, s->pc_curr);
 1141|     gen_helper_exception_bkpt_insn(cpu_env, tcg_constant_i32(syn));
 1142|     s->base.is_jmp = DISAS_NORETURN;
 1143| }
 1144| 
 1145| void unallocated_encoding(DisasContext *s)
 1146| {
 1147|     /* Unallocated and reserved encodings are uncategorized */
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

### Turn 6  _(tok 8113+105, stop=tool_use)_

**Reasoning:** Line 1172 is inside `gen_hlt` (starts at line 1158). Next is line 6559.


- `read_file(end_line=6570, path=target/arm/translate.c, start_line=6500, version=old)` →

```
target/arm/translate.c lines 6500-6570 of 9927
 6500| 
 6501| static bool trans_BLXNS(DisasContext *s, arg_BLXNS *a)
 6502| {
 6503|     if (!s->v8m_secure || IS_USER_ONLY) {
 6504|         unallocated_encoding(s);
 6505|     } else {
 6506|         gen_blxns(s, a->rm);
 6507|     }
 6508|     return true;
 6509| }
 6510| 
 6511| static bool trans_CLZ(DisasContext *s, arg_CLZ *a)
 6512| {
 6513|     TCGv_i32 tmp;
 6514| 
 6515|     if (!ENABLE_ARCH_5) {
 6516|         return false;
 6517|     }
 6518|     tmp = load_reg(s, a->rm);
 6519|     tcg_gen_clzi_i32(tmp, tmp, 32);
 6520|     store_reg(s, a->rd, tmp);
 6521|     return true;
 6522| }
 6523| 
 6524| static bool trans_ERET(DisasContext *s, arg_ERET *a)
 6525| {
 6526|     TCGv_i32 tmp;
 6527| 
 6528|     if (!arm_dc_feature(s, ARM_FEATURE_V7VE)) {
 6529|         return false;
 6530|     }
 6531|     if (IS_USER(s)) {
 6532|         unallocated_encoding(s);
 6533|         return true;
 6534|     }
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
 6563|         (a->imm == 0xab)) {
 6564|         gen_exception_internal_insn(s, s->pc_curr, EXCP_SEMIHOST);
 6565|     } else {
 6566|         gen_exception_bkpt_insn(s, syn_aa32_bkpt(a->imm, false));
 6567|     }
 6568|     return true;
 6569| }
 6570| 
```

_(budget of 20,000 tokens exhausted — forcing submission)_

