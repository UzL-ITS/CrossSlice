"""
Build the per-case "relevant set" for the context-recall measurement: for every
function the real fix touched, the definition spans (file, start, end) of the
function itself, its direct callees and callers, and the project types it uses,
all in the PRE-commit version, measured through the same locked MCP server the
arms use. Writes eval/results/relevant_sets.json keyed by commit sha.

  uv run python -m eval.relevant_sets --cases eval/cases_fix_large.txt
  uv run python -m eval.relevant_sets --results eval/results/agent_fix_claude-opus-4-8.jsonl
"""
import argparse, asyncio, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import eval._env  # noqa
from mcp import ClientSession
from mcp.client.stdio import stdio_client
import eval.llm_classify as base
import eval.agent_probe as ap

OUT = "eval/results/relevant_sets.json"
HDR = re.compile(r"^(\S+) \((function|macro|type_definition|struct_specifier|union_specifier|"
                 r"enum_specifier|preproc_def|preproc_function_def|declaration), old version\) — (.+?):(\d+)-(\d+)")


async def span(session, tool, name):
    r = await asyncio.wait_for(session.call_tool(tool, {"name": name}), timeout=300)
    txt = r.content[0].text if r.content else ""
    m = HDR.match(txt.split("\n", 1)[0])
    if not m:
        return None
    return {"name": name, "kind": m.group(2), "file": m.group(3),
            "start": int(m.group(4)), "end": int(m.group(5))}


async def build(repo_dir, sha, functions):
    params = ap._server_params(repo_dir, sha, lock="old")
    out = {"functions": [], "callees": [], "callers": [], "types": []}
    async with stdio_client(params, errlog=open(os.devnull, "w")) as (r, w):
        async with ClientSession(r, w) as s:
            await asyncio.wait_for(s.initialize(), timeout=60)
            for fn in functions:
                d = await asyncio.wait_for(span(s, "get_function_source", fn), timeout=ap.WARMUP_TIMEOUT)
                if d:
                    out["functions"].append(d)
                nb = (await asyncio.wait_for(s.call_tool("get_neighborhood", {"name": fn}), timeout=300)).content[0].text
                section = None
                for line in nb.split("\n"):
                    if line.startswith("CALLEES"):
                        section = "callees"; continue
                    if line.startswith("CALLERS"):
                        section = "callers"; continue
                    if line.startswith("TYPES"):
                        section = "types"; continue
                    m = re.match(r"  (\w+) ", line)
                    if not (section and m):
                        continue
                    nm = m.group(1)
                    if section == "types" and not re.match(r"  \w+ — ", line):
                        continue
                    if section in ("callees", "callers"):
                        if "no in-repo definition" in line:
                            continue
                        d = await span(s, "get_function_source", nm)
                    else:
                        d = await span(s, "get_type_definition", nm)
                    if d and d not in out[section]:
                        out[section].append(d)
    return out


def main():
    apr = argparse.ArgumentParser()
    apr.add_argument("--cases", default=None)
    apr.add_argument("--results", default=None, help="take cases from a results file")
    apr.add_argument("--out", default=OUT, help="sets file (default eval/results/relevant_sets.json)")
    a = apr.parse_args()
    out_path = a.out
    sets = json.load(open(out_path)) if os.path.exists(out_path) else {}
    cases = []
    if a.cases:
        cases = [(c["repo_dir"], c["commit"], c["functions"]) for c in ap.load_case_list(a.cases)]
    if a.results:
        for rec in map(json.loads, open(a.results)):
            repo_dir = base.resolve_repo(rec["url"], rec["commit"])
            cases.append((repo_dir, rec["commit"], rec["functions"]))
    for repo_dir, sha, fns in cases:
        if sha in sets:
            print(f"{sha[:10]} cached"); continue
        print(f"{sha[:10]} {fns} …", flush=True)
        sets[sha] = asyncio.run(build(repo_dir, sha, fns))
        json.dump(sets, open(out_path, "w"), indent=1)
        s = sets[sha]
        print(f"   functions {len(s['functions'])} callees {len(s['callees'])} "
              f"callers {len(s['callers'])} types {len(s['types'])}")
    print("done")


if __name__ == "__main__":
    main()
