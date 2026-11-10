# Evaluation harness and results

This directory holds the harness, the case files and the result files of the
CrossSlice paper (ICPC 2027 tool track). Everything was produced on one machine (Intel Core
i7-7700, 4 cores at 3.6 GHz, 62 GB RAM, Linux) with the tool at `ANALYSIS_VERSION 2026-11-03.10`.

## Environment

| component | version used |
|---|---|
| Python / uv | the project's `pyproject.toml` via `uv run` |
| GNU Global (gtags) | 6.6.14 |
| GumTree | 4.0.0-beta3 (`GUMTREE_PATH`, default `/opt/gumtree/gumtree-4.0.0-beta3/bin/gumtree`) |
| Java | OpenJDK 21 (for GumTree and Joern) |
| clangd | 22.1.3 |
| Joern | 4.0.671 (`joern`, `joern-parse` on `PATH`; baselines only) |
| cscope | 15.9 (baselines only) |

`eval/_env.py` reads `.env` at the repository root. Variables: `GUMTREE_PATH`, `ANTHROPIC_API_KEY`
(Claude agents and the repair judge), `OPENROUTER_API_KEY` (open-weight agents).

Subject repositories are plain clones under `data/repos/<name>` (git-ignored): zlib, libexpat,
acpica, ffmpeg, php-src and qemu from their GitHub mirrors. The case files pin every revision by
full SHA. The repair cases (`cases_fix_large.txt`) name their repositories by URL and
`agent_probe` clones them itself.

## Case files

| file | content |
|---|---|
| `results/bench_h100.sample.txt` | H100: 20 non-merge commits per project touching a `.c`/`.h` file, drawn uniformly (seed 42) from the last 3,000 such commits |
| `cases_impact_all_v2.jsonl` | I18: 18 commits of FFmpeg and php-src that change the parameter list of a function and edit at least three of its call sites in two files. Truth: the call lines the commit edited, 135 sites in 120 functions with 102 distinct names (`truth_sites.py`), reviewed by hand. `truth_grep.py` run on the same cases yields the same 135 sites |
| `cases_impact_hard_v3.jsonl` | H16: 16 signature changes in php-src and QEMU whose function name has several definitions or more than twice as many references as edited call sites (`impact.py mine --hard`, candidates in `cases_impact_hard_raw.jsonl`). Truth: every call of the function at the parent revision, 159 sites, from a repository-wide search (`truth_grep.py`) |
| `cases_impact_hard_review.txt` | the review sheet of H16: every occurrence of each function name at the parent revision with its class (call, declaration, comment, macro body, reference) and enclosing function, checked by hand |
| `cases_fix_large.txt` | R15: 15 hand-labeled vulnerability fixes in large C projects (`<repo url> <sha>`) |
| `examples/` | the worked example of the paper (`kvstore`), produced by `make_example.py` |

The H16 truth distinguishes required and optional caller names. Required are the functions that
contain a call. Optional names are accepted in an answer but neither required nor counted as
errors: a macro whose body calls the function, the functions that use such a macro, the function
that holds a non-call reference (a function pointer), and the function itself when it is recursive.
A `static` definition in a `.c` file is scoped to that file. Names are matched alias-aware
(`impact.aliases`): `PHP_METHOD(C, m)` ~ `zim_C_m` ~ `C::m`, `PHP_FUNCTION(f)` ~ `zif_f` ~ `f`,
`ZEND_VM_HANDLER(n, OP, ...)` ~ `OP`, and `NAME(PARAMS)` ~ `NAME`.

## Experiments and commands

All commands run from the repository root. Each writes a JSONL file with one record per commit or
case, and a report step prints the summary that is stored under `results/summaries/`.

**Q1 latency and output size, Q2 resolution.**
```
uv run python -m eval.benchmark --commits eval/results/bench_h100.sample.txt --out eval/results/bench_h100.jsonl
uv run python -m eval.benchmark --aggregate eval/results/bench_h100.jsonl           # -> summaries/bench_h100.txt
```
Each commit is enriched twice, cold and then warm with the cache of the first pass. The pass was
run three times (`bench_h100.jsonl`, `bench_h100_r2.jsonl`, `bench_h100_r3.jsonl`).
`bench_h100.texts/` holds the enriched outputs whose sizes and cold/warm stability are reported.

**Q2 audit of the resolution with clangd.** The audit repeats every resolution of a function with
clangd as the oracle, using compile databases generated from each project's own configure step
(no build), and covers all four resolution steps:
```
# once per project: configure, then a dry-run make captured by compiledb (pip install compiledb)
(cd data/repos/zlib && ./configure && compiledb -n -o ../../../eval/compiledb/zlib.json make)
(cd data/repos/ffmpeg && ./configure --disable-x86asm --disable-doc && compiledb -n -o ../../../eval/compiledb/ffmpeg.json make)
(cd data/repos/acpica/generate/unix && compiledb -n -o ../../../../../eval/compiledb/acpica.json make)
(cd data/repos/libexpat/expat && ./buildconf.sh && ./configure && compiledb -n -o ../../../../eval/compiledb/libexpat.json make)
(cd data/repos/php-src && ./buildconf --force && ./configure --disable-all && compiledb -n -o ../../../eval/compiledb/php-src.json make)
CROSSSLICE_AUDIT_COMPILE_DB_MAP=eval/compiledb/map.json uv run python -m eval.benchmark --commits eval/results/bench_h100.sample.txt --audit-lsp --no-warm --no-texts --out eval/results/bench_h100_audit_realdb.jsonl
uv run python -m eval.audit_report eval/results/bench_h100_audit_realdb.jsonl          # -> summaries/audit_realdb_report.txt
```
`eval/compiledb/map.example.json` shows the map format (repository root to database). The
generated databases are machine-specific and are not shipped. The resolver queries clangd with
them only in audit mode, so the audited decisions are the tool's own. `audit_report.py` inspects
what clangd pointed at for every decision and reports, per resolution step, agreement, another
definition, the system library, a declaration only, another symbol, and no answer.

**Q3 incremental maintenance.**
```
uv run python -m eval.replay --repo zlib --n 40 --out eval/results/replay_zlib_v3.jsonl     # likewise libexpat, acpica (40), ffmpeg, php-src (30)
uv run python -m eval.replay --aggregate eval/results/replay_zlib_v3.jsonl                  # -> summaries/replay_zlib_v3.txt
```

**Q4 agents listing the callers of a changed function (Table I).**
```
uv run python -m eval.impact run --model anthropic:claude-haiku-5-5 --budget 20000 --cases eval/cases_impact_all_v2.jsonl --out eval/results/impact_haiku-5-5_v3.jsonl
uv run python -m eval.impact run --model anthropic:claude-haiku-5-5 --budget 20000 --arms index --cases eval/cases_impact_all_v2.jsonl --out eval/results/impact_haiku-5-5_v3_index.jsonl
uv run python -m eval.impact run --model anthropic:claude-haiku-5-5 --budget 20000 --arms self,index,tool,semantic --cases eval/cases_impact_hard_v3.jsonl --out eval/results/impact_haiku-5-5_hard.jsonl
uv run python -m eval.impact run --model openrouter:qwen/qwen3.8-2.4t-a95b --budget 20000 --cases eval/cases_impact_all_v2.jsonl --out eval/results/impact_qwen3.8-2.4t-a95b_v3.jsonl
uv run python -m eval.impact report eval/results/impact_haiku-5-5_hard.jsonl
```
Arms: `self` (list, read, grep), `index` (the same plus `find_references`, a GNU Global lookup),
`tool` (list, read, grep and the MCP tools), `semantic` (the MCP tools only). Every configuration
was run three times; the second and third runs carry the suffixes `r2` and `r3`. Open-weight
models run over OpenRouter, `--provider` pins the provider order, and the result records list the
providers that served each arm.

**Q4 repair task.**
```
uv run python -m eval.agent_probe run --task fix --cases eval/cases_fix_large.txt --model anthropic:claude-haiku-5-5 --budget 40000 --hint function --seed-source --arms self,tool,semantic --effort high --out eval/results/agent_fix_haiku-5-5_v2.jsonl
uv run python -m eval.relevant_sets --cases eval/cases_fix_large.txt --out eval/results/relevant_sets_v3.json
uv run python -m eval.coverage eval/results/agent_fix_haiku-5-5_v2.jsonl --sets eval/results/relevant_sets_v3.json
```
`--seed-source` puts the source of the vulnerable function into the first prompt of every arm, so
the arms differ only in the tools available. The judge defaults to `anthropic:claude-sonnet-5-5`.
The task was run three times for Haiku and Sonnet (`agent_fix_<model>_v2.jsonl`, `_v3.jsonl`,
`_v3r2.jsonl`; coverage `coverage_v3.txt`, `_v4.txt`, `_v5.txt`) and once for Qwen3.8.
Full transcripts of every agent run are in `results/agent_transcripts/`.

**Q5 callers found by each tool (Table II).**
```
uv run python -m eval.baselines crossslice-callers --cold --cases eval/cases_impact_all_v2.jsonl --out eval/results/callers_crossslice_cold.jsonl
uv run python -m eval.baselines joern-callers   --cases eval/cases_impact_all_v2.jsonl --out eval/results/callers_joern_v2.jsonl
uv run python -m eval.baselines global-callers  --cases eval/cases_impact_all_v2.jsonl --out eval/results/callers_global_v2.jsonl
uv run python -m eval.baselines cscope-callers  --cases eval/cases_impact_all_v2.jsonl --out eval/results/callers_cscope_v2.jsonl
uv run python -m eval.baselines report --ours eval/results/callers_crossslice_cold.jsonl --joern eval/results/callers_joern_v2.jsonl --global eval/results/callers_global_v2.jsonl --cscope eval/results/callers_cscope_v2.jsonl
```
The same four commands with `--cases eval/cases_impact_hard_v3.jsonl` produce the
`callers_*_hard.jsonl` files. `--cold` gives the tool an empty cache per case, so its index build
is timed like the fresh `gtags` and `cscope` runs of the baselines.

## Where each number in the paper comes from

| paper | raw file | summary |
|---|---|---|
| Q1 latency and output size | `results/bench_h100.jsonl` (+ `_r2`, `_r3`) | `summaries/bench_h100.txt` (+ `_r2`, `_r3`) |
| Q2 resolution rate and steps | `results/bench_h100.jsonl` | `summaries/bench_h100.txt` |
| Q2 audit | `results/bench_h100_audit_realdb.jsonl` | `summaries/audit_realdb_report.txt` |
| Q3 incremental graph | `replay_<repo>_v3.jsonl` | `summaries/replay_<repo>_v3.txt` |
| Table I, I18 | `impact_<model>_v3.jsonl`, `_v3r2.jsonl`, `_v3r3.jsonl`, `impact_<model>_v3_index{,r2,r3}.jsonl` | `summaries/impact_agents_v3.txt`, `impact_agents_openweight_v3.txt`, `impact_agents_index_v3.txt` |
| Table I, H16 | `impact_<model>_hard{,r2,r3}.jsonl` | `summaries/impact_agents_hard.txt` |
| Q4 repair and retrieval | `agent_fix_{haiku,sonnet}-5-5_v2.jsonl`, `_v3.jsonl`, `_v3r2.jsonl`, `agent_fix_qwen3.8-2.4t-a95b_v3.jsonl`, `relevant_sets_v3.json` | `summaries/agent_fix_*.txt`, `coverage_v3.txt`, `_v4.txt`, `_v5.txt` |
| Table II, I18 | `callers_crossslice_cold.jsonl`, `callers_{joern,global,cscope}_v2.jsonl`, `impact_tool_v2_all.jsonl` | `summaries/baselines_v3.txt`, `impact_tool_v2_all.txt` |
| Table II, H16 | `callers_{crossslice,joern,global,cscope}_hard.jsonl`, `impact_tool_hard.jsonl` | `summaries/baselines_hard.txt` |

File-name suffixes `_v2` and `_v3` are harness revisions, `r2` and `r3` are repeated runs.
Agent results are subject to model non-determinism; the stored transcripts are the record of what
the models did.
