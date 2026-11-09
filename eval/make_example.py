"""
Generate a presentation-ready example directory for one commit:

  eval/examples/<repo>_<sha12>/
    README.md            — commit info + size comparison table
    raw_diff_u3.txt      — plain git diff (3 context lines)
    enriched_intra.txt   — intra-procedural enriched diff
    enriched_inter1.txt  — + cross-function ring 1 (sliced bodies)
    enriched_inter2.txt  — + ring 2 (signature/summary stubs)

  uv run python -m eval.make_example ffmpeg 10e9d1f76b4bec7a3c581ab7ac494f55acc6f24d
"""

import contextlib
import io
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# the released package (installed as an editable dependency of this project)
from crossslice.intra.github_loader import (get_previous_commit, get_changed_files,
                                            extract_file_from_commit)
from crossslice.intra.data_diff import create_diff
from crossslice.intra.parse_diff import parse_diff
from crossslice.intra.gen_dataflow import gen_dataflow
from crossslice.cross.enrich import CrossFunctionEnricher


def delete_all_folder_and_files_in_dir(path):
    import shutil
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path, exist_ok=True)

REPOS_DIR = "./data/repos"
WORK_DIR = "./outputs_eval"


def make_example(repo_name, commit, note=""):
    # repo_name is either a name under data/repos/ or a path to any git repo
    if os.sep in repo_name and os.path.isdir(repo_name):
        repo_dir = repo_name
        repo_name = os.path.basename(os.path.normpath(repo_name))
    else:
        repo_dir = os.path.join(REPOS_DIR, repo_name)
    commit = subprocess.run(["git", "rev-parse", commit], cwd=repo_dir,
                            capture_output=True, text=True).stdout.strip()
    out_dir = os.path.join("eval/examples", f"{repo_name}_{commit[:12]}")
    os.makedirs(out_dir, exist_ok=True)
    old_dir = os.path.abspath(os.path.join(WORK_DIR, "old_version"))
    new_dir = os.path.abspath(os.path.join(WORK_DIR, "new_version"))
    os.makedirs(old_dir, exist_ok=True)
    os.makedirs(new_dir, exist_ok=True)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        prev = get_previous_commit(repo_dir, commit)
        files = [f for f in get_changed_files(repo_dir, prev, commit)
                 if f.endswith((".c", ".h"))]
        for f in files:
            extract_file_from_commit(repo_dir, prev, f, os.path.join(old_dir, f))
            extract_file_from_commit(repo_dir, commit, f, os.path.join(new_dir, f))
        diff = create_diff(old_dir, new_dir, files)
        changes = parse_diff(diff, WORK_DIR, old_dir, new_dir,
                             use_hungarian=True, debug_matching=False)
        intra_text, internals = gen_dataflow(changes, old_dir, new_dir,
                                             level=2, collect_internals=True)
        enricher = CrossFunctionEnricher(repo_dir, prev, commit, cross_depth=2)
        cross2_text, cross_json = enricher.enrich(internals)
        cross1_text = enricher.format_text(include_ring2=False)

    u3 = subprocess.run(["git", "diff", "-U3", prev, commit, "--", *files],
                        cwd=repo_dir, capture_output=True, text=True,
                        errors="replace").stdout
    msg = subprocess.run(["git", "log", "-1", "--format=%s%n%n%b", commit],
                         cwd=repo_dir, capture_output=True, text=True,
                         errors="replace").stdout.strip()
    full_fn = sum(len(fn.get("old_code") or "") + len(fn.get("new_code") or "")
                  for d in changes.values() for fn in d.get("functions", {}).values())

    variants = {
        "raw_diff_u3.txt": u3,
        "enriched_intra.txt": intra_text,
        "enriched_inter1.txt": intra_text + "\n" + cross1_text,
        "enriched_inter2.txt": intra_text + "\n" + cross2_text,
    }
    for fname, text in variants.items():
        with open(os.path.join(out_dir, fname), "w") as f:
            f.write(text or "")

    rows = [("raw git diff (-U3)", len(u3)),
            ("full changed functions (old+new)", full_fn),
            ("intra-procedural enriched", len(intra_text or "")),
            ("+ cross-function ring 1", len(variants["enriched_inter1.txt"])),
            ("+ ring 2 summaries", len(variants["enriched_inter2.txt"]))]
    with open(os.path.join(out_dir, "README.md"), "w") as f:
        f.write(f"# {repo_name} @ {commit[:12]}\n\n")
        f.write(f"Repository: {repo_name}\nCommit: `{commit}`\nParent: `{prev}`\n\n")
        f.write(f"Commit message:\n\n```\n{msg}\n```\n\n")
        if note:
            f.write(f"{note}\n\n")
        f.write("## Context size comparison\n\n")
        f.write("| representation | characters | vs full functions |\n|---|---:|---:|\n")
        base = full_fn or 1
        for name, n in rows:
            f.write(f"| {name} | {n:,} | {n / base:.2f}x |\n")
        f.write("\n## Cascade statistics\n\n```json\n")
        f.write(json.dumps(cross_json.get("stats"), indent=2))
        f.write("\n```\n\nFiles: `raw_diff_u3.txt`, `enriched_intra.txt`, "
                "`enriched_inter1.txt`, `enriched_inter2.txt`.\n")

    with contextlib.redirect_stdout(io.StringIO()):
        delete_all_folder_and_files_in_dir(old_dir)
        delete_all_folder_and_files_in_dir(new_dir)
        delete_all_folder_and_files_in_dir(os.path.join(WORK_DIR, "functions_code"))
    print(f"example written to {out_dir} "
          f"(sizes: {', '.join(f'{n}={v:,}' for n, v in rows)})")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('usage: python -m eval.make_example <repo-name> <sha> [out-dir]')
    make_example(sys.argv[1], sys.argv[2],
                 sys.argv[3] if len(sys.argv) > 3 else "")
