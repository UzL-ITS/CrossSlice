# Impact-analysis transcript — qemu @ 5202861b20d7 — openrouter:qwen/qwen3.8-2.4t-a95b

- target: `semihosting_enabled` (include/semihosting/semihost.h), arity 0->1
- truth: [['softmmu/vl.c', 'qemu_apply_machine_options'], ['target/arm/translate-a64.c', 'disas_exc'], ['target/arm/translate.c', 'gen_hlt'], ['target/arm/translate.c', 'trans_BKPT'], ['target/arm/translate.c', 'trans_SVC'], ['target/m68k/op_helper.c', 'cf_interrupt_all'], ['target/mips/tcg/translate.c', 'is_uhi'], ['target/nios2/translate.c', 'gen_break'], ['target/xtensa/translate.c', 'test_exceptions_simcall'], ['target/xtensa/translate.c', 'translate_simcall']]

## Self-navigation arm

### Turn 1  _(tok 908+79, stop=tool_use)_

**Reasoning:** I'm searching through the codebase for all the places where `semihosting_enabled` is being called.

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

### Turn 2  _(tok 1396+300, stop=tool_use)_

**Reasoning:** I need to identify which functions contain each call site. I'm reviewing the locations across several source files: softmmu/vl.c at line 1825, target/arm/translate-a64.c at line 2222, multiple locations in target/arm/translate.c, target/m68k/op_helper.c at line 206, and target/mips/tcg/transl.

c at line 12090, along with target/nios2/translate.c at line 821 and target/xtensa/translate.c at lines 2369, 2371, and 2381.

**Says:** Now let me find the enclosing function for each call site.



- `read_file(path=softmmu/vl.c, start_line=1790, end_line=1835, version=old)` →

```
softmmu/vl.c lines 1790-1835 of 3593
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
```

- `read_file(path=target/arm/translate-a64.c, start_line=2190, end_line=2230, version=old)` →

```
target/arm/translate-a64.c lines 2190-2230 of 15028
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
```

### Turn 3  _(tok 3107+142, stop=tool_use)_

**Reasoning:** I need to find the function that surrounds line 2222 within translate-a64.c. Let's search backwards for the function definition. I'll try grepping for something around "handle_a64".

- `grep(pattern=^(static )?(void|bool|DisasJumpType|TCGv) [a-z_0-9]+\(, path_glob=target/arm/translate-a64.c, version=old, max_results=100)` →

```
226 matches (showing 100)
target/arm/translate-a64.c:71:void a64_translate_init(void)
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
target/arm/translate-a64.c:798:static void gen_adc(int sf, TCGv_i64 dest, TCGv_i64 t0, TCGv_i64 t1)
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
```

### Turn 4  _(tok 6747+173, stop=tool_use)_

**Reasoning:** In translate-a64.c, line 2222 is inside `disas_exc` (lines 2154–2257). Confirmed.

Next, the call sites in target/arm/translate.c: line 1172, line 6559, line 8767. Search for the functions containing them.


**Says:** Confirmed `disas_exc` in translate-a64.c. Now the target/arm/translate.c sites:



- `read_file(path=target/arm/translate.c, start_line=1140, end_line=1190, version=old)` →

```
target/arm/translate.c lines 1140-1190 of 9927
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
 1181|     unallocated_encoding(s);
 1182| }
 1183| 
 1184| /*
 1185|  * Return the offset of a "full" NEON Dreg.
 1186|  */
 1187| long neon_full_reg_offset(unsigned reg)
 1188| {
 1189|     return offsetof(CPUARMState, vfp.zregs[reg >> 1].d[reg & 1]);
 1190| }
```

### Turn 5  _(tok 7789+134, stop=tool_use)_

**Reasoning:** Line 1172 is inside `gen_hlt`. Next up are line 6559 and line 8767 of translate.c.


**Says:** Line 1172 is in `gen_hlt`. Now lines 6559 and 8767:



- `read_file(path=target/arm/translate.c, start_line=6520, end_line=6590, version=old)` →

```
target/arm/translate.c lines 6520-6590 of 9927
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
 6571| static bool trans_HVC(DisasContext *s, arg_HVC *a)
 6572| {
 6573|     if (!ENABLE_ARCH_7 || arm_dc_feature(s, ARM_FEATURE_M)) {
 6574|         return false;
 6575|     }
 6576|     if (IS_USER(s)) {
 6577|         unallocated_encoding(s);
 6578|     } else {
 6579|         gen_hvc(s, a->imm);
 6580|     }
 6581|     return true;
 6582| }
 6583| 
 6584| static bool trans_SMC(DisasContext *s, arg_SMC *a)
 6585| {
 6586|     if (!ENABLE_ARCH_6K || arm_dc_feature(s, ARM_FEATURE_M)) {
 6587|         return false;
 6588|     }
 6589|     if (IS_USER(s)) {
 6590|         unallocated_encoding(s);
```

_(budget of 20,000 tokens exhausted — forcing submission)_

