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
`CROSSSLICE_DEFUSE=scalar` selects the scalar def-use engine for the ablation (default `fields`).

Subject repositories are plain clones under `data/repos/<name>` (git-ignored):
zlib, libexpat, acpica, ffmpeg, php-src from their GitHub mirrors. The sample files pin every
revision by full SHA, so the clones only need to contain those commits. The repair cases
(`cases_fix_large.txt`) name their repositories by URL; `agent_probe` clones them itself.

## Case files

| file | content |
|---|---|
| `results/bench_h100.sample.txt` | H100: 20 non-merge commits per project touching a `.c`/`.h` file, drawn uniformly (seed 42) from the last 3,000 such commits |
| `results/bench_d45.sample.txt` | S64: 64 commits of the labeled security-patch dataset, balanced vfc / non-vfc per project (seed 42) |
| `cases_impact_all_v2.jsonl` | I18: 18 signature-changing commits of FFmpeg and php-src with the ground truth (135 call sites in 102 enclosing functions), built by `truth_sites.py` from the diff and the parent files and reviewed by hand |
| `cases_fix_large.txt` | R15: 15 hand-labeled vulnerability fixes in large C projects (`<repo url> <sha>`) |
| `examples/` | the worked example of the paper (`kvstore`), produced by `make_example.py` |

## Experiments and commands

All commands run from the repository root. Each writes a JSONL file with one record per commit or
case, and an `--aggregate` / `report` step prints the summary that is stored under `results/summaries/`.

**Q1 latency and output size, Q2 resolution (Table II, Fig. 4, Section IV-B/C).**
```
uv run python -m eval.benchmark --commits eval/results/bench_h100.sample.txt --out eval/results/bench_h100.jsonl
uv run python -m eval.benchmark --aggregate eval/results/bench_h100.jsonl           # -> summaries/bench_h100.txt
CROSSSLICE_DEFUSE=scalar uv run python -m eval.benchmark --commits eval/results/bench_h100.sample.txt --out eval/results/bench_h100_scalar.jsonl
uv run python -m eval.benchmark --commits eval/results/bench_h100.sample.txt --audit-lsp --out eval/results/bench_h100_audit.jsonl
uv run python -m eval.benchmark --commits eval/results/bench_d45.sample.txt --out eval/results/bench_d45.jsonl
```
Each commit is enriched twice (cold, then warm with the cache of the first pass); `--audit-lsp`
repeats every tag-based function resolution with clangd as the oracle, using the heuristic compile
database the tool itself builds. A second audit uses compile databases generated from each project's
own configure step (no build) and covers all four tiers:
```
# once per project: configure, then a dry-run make captured by compiledb (pip install compiledb)
(cd data/repos/zlib && ./configure && compiledb -n -o ../../../eval/compiledb/zlib.json make)
(cd data/repos/ffmpeg && ./configure --disable-x86asm --disable-doc && compiledb -n -o ../../../eval/compiledb/ffmpeg.json make)
(cd data/repos/acpica/generate/unix && compiledb -n -o ../../../../../eval/compiledb/acpica.json make)
(cd data/repos/libexpat/expat && ./buildconf.sh && ./configure && compiledb -n -o ../../../../eval/compiledb/libexpat.json make)
(cd data/repos/php-src && ./buildconf --force && ./configure --disable-all && compiledb -n -o ../../../eval/compiledb/php-src.json make)
CROSSSLICE_AUDIT_COMPILE_DB_MAP=eval/compiledb/map.json uv run python -m eval.benchmark --commits eval/results/bench_h100.sample.txt --audit-lsp --no-warm --no-texts --out eval/results/bench_h100_audit_realdb.jsonl
```
`eval/compiledb/map.example.json` shows the map format (repository root to database); the generated
databases are machine-specific and are not shipped. The resolver rewrites their paths to each worktree
and queries clangd with them only in audit mode, so the resolution decisions being audited are the
tool's own. The audit records are the `audit` list of each record (`method`, `verdict`, `db`).

The latency pass was repeated three times (`bench_h100.jsonl`, `bench_h100_r2.jsonl`, `bench_h100_r3.jsonl`). The `.texts/` directories hold the
enriched outputs whose sizes and cold/warm stability are reported.

**Q3 incremental maintenance (Table III).**
```
uv run python -m eval.replay --repo zlib --n 40 --out eval/results/replay_zlib_v3.jsonl     # likewise libexpat, acpica (40), ffmpeg, php-src (30)
uv run python -m eval.replay --aggregate eval/results/replay_zlib_v3.jsonl                  # -> summaries/replay_zlib_v3.txt
```

**Q4 agents, impact analysis (Table IV).**
```
uv run python -m eval.impact tool-eval --cases eval/cases_impact_all_v2.jsonl               # the tool alone
uv run python -m eval.impact run --model anthropic:claude-haiku-5-5 --budget 20000 --cases eval/cases_impact_all_v2.jsonl --out eval/results/impact_haiku-5-5_v3.jsonl
uv run python -m eval.impact run --model openrouter:qwen/qwen3.8-2.4t-a95b --budget 20000 --cases eval/cases_impact_all_v2.jsonl --out eval/results/impact_qwen3.8-2.4t-a95b_v3.jsonl
uv run python -m eval.impact report
```
Each model was run three times; the files are `impact_<model>_v3.jsonl`, `_v3r2.jsonl`, `_v3r3.jsonl`.
Open-weight models run over OpenRouter; `--provider` pins the provider order, and the result records
list the providers that served each arm.

**Q4 agents, repair (Section IV-E) and context coverage.**
```
uv run python -m eval.agent_probe run --task fix --cases eval/cases_fix_large.txt --model anthropic:claude-haiku-5-5 --budget 40000 --hint function --seed-source --arms self,tool,semantic --effort high --out eval/results/agent_fix_haiku-5-5_v2.jsonl
uv run python -m eval.relevant_sets --cases eval/cases_fix_large.txt --out eval/results/relevant_sets_v3.json
uv run python -m eval.coverage eval/results/agent_fix_haiku-5-5_v2.jsonl --sets eval/results/relevant_sets_v3.json
```
`--seed-source` puts the source of the vulnerable function into the first prompt of every arm, so the arms differ only in the tools available; the judge defaults to `anthropic:claude-sonnet-5-5`. The repair task was run three times for Haiku and Sonnet (`agent_fix_<model>_v2.jsonl`, `_v3.jsonl`,
`_v3r2.jsonl` are runs 1 to 3; coverage `coverage_v3.txt`, `_v4.txt`, `_v5.txt`). Full transcripts of every agent run
are in `results/agent_transcripts/`.

**Q5 baselines (Table V).**
```
uv run python -m eval.baselines joern-time --out eval/results/joern_time.jsonl
uv run python -m eval.baselines joern-callers   --cases eval/cases_impact_all_v2.jsonl --out eval/results/callers_joern_v2.jsonl
uv run python -m eval.baselines global-callers  --cases eval/cases_impact_all_v2.jsonl --out eval/results/callers_global_v2.jsonl
uv run python -m eval.baselines cscope-callers  --cases eval/cases_impact_all_v2.jsonl --out eval/results/callers_cscope_v2.jsonl
uv run python -m eval.baselines crossslice-callers --cases eval/cases_impact_all_v2.jsonl --out eval/results/callers_crossslice_v3.jsonl
uv run python -m eval.baselines report --cases eval/cases_impact_all_v2.jsonl             # -> summaries/baselines_v3.txt
```

## Source of number in the paper

| paper | raw file | summary |
|---|---|---|
| Table I (subjects) | `summaries/baselines_v3.txt` (files, kLOC) | |
| Table II, Fig. 4, Section IV-B | `results/bench_h100.jsonl` (+ `_r2`, `_r3`), `bench_d45.jsonl` | `summaries/bench_h100.txt`, `bench_d45.txt` |
| Section IV-C (resolution, audits, scalar ablation) | `bench_h100_audit.jsonl` (heuristic DB), `bench_h100_audit_realdb.jsonl` (project DBs), `bench_h100_scalar.jsonl` | `summaries/bench_h100_audit.txt`, `bench_h100_audit_realdb.txt`, `bench_h100_scalar.txt` |
| Table III | `replay_<repo>_v3.jsonl` | `summaries/replay_<repo>_v3.txt` |
| Table IV | `impact_<model>_v3.jsonl`, `_v3r2.jsonl`, `_v3r3.jsonl`, `impact_tool_v2_all.jsonl` | `summaries/impact_agents_v3.txt`, `impact_agents_openweight_v3.txt`, `impact_tool_v2_all.txt` |
| Section IV-E (repair, coverage) | `agent_fix_{haiku,sonnet}-5-5_v2.jsonl`, `_v3.jsonl`, `_v3r2.jsonl` (runs 1 to 3), `agent_fix_qwen3.8-2.4t-a95b_v3.jsonl`, `relevant_sets_v3.json` | `summaries/agent_fix_*.txt`, `coverage_v3.txt`, `_v4.txt`, `_v5.txt` (runs 1 to 3) |
| Table V | `callers_*.jsonl` | `summaries/baselines_v3.txt` |

File-name suffixes `_v2` and `_v3` are harness revisions, `_r2` and `_r3` are repeated runs.

Timings and agent results come from three runs each; the paper reports the first run and the ranges.
Agent results are subject to model non-determinism; the stored transcripts are the record of what the
models did.
