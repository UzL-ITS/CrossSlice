"""
Class to handle gtags related operations.

Reference for the global flags used here:
  -d  locate definitions
  -r  locate references
  -x  cxref-style detailed output
  -a  absolute path names
  -u  incremental index update (gtags/global)

Line numbers reported by global are 1-based; the *_detailed methods keep them
1-based (matching the old resolver code), the tuple-returning methods convert
to 0-based (matching the diff pipeline convention).
"""

import json
import os
import subprocess

GTAGS_FILES = ("GPATH", "GRTAGS", "GTAGS")
MANIFEST = "crossslice-files.json"          # {rel path: [mtime_ns, size]} of every source file the index saw
SOURCE_EXT = (".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx")


def check_if_gtags_files_exist(root_dir):
    """Checks if the GPATH, GRTAGS, and GTAGS files exist in root_dir"""
    return all(os.path.exists(os.path.join(root_dir, f)) for f in GTAGS_FILES)


class GtagsHandler:
    """
    Wrapper around gtags/global for a single repository checkout.

    keep_index=True leaves the GTAGS files in place on exit so repeated
    analyses of the same (repo, commit) reuse the index; incremental updates
    via update() make switching commits cheap compared to a full regenerate.
    """

    def __init__(self, root_dir, language="c", keep_index=True, cache_dir=None,
                 dbpath=None):
        self.root_dir = root_dir
        # Where the GTAGS/GRTAGS/GPATH files live. Default: the source root
        # (fine for throwaway worktrees). For a user's checkout, CrossSlice
        # passes a directory in its cache so the repository stays untouched;
        # global then finds the index through GTAGSROOT/GTAGSDBPATH.
        self.dbpath = os.path.abspath(dbpath) if dbpath else root_dir
        self._env = None
        if dbpath:
            os.makedirs(self.dbpath, exist_ok=True)
            self._env = dict(os.environ, GTAGSROOT=os.path.abspath(root_dir),
                             GTAGSDBPATH=self.dbpath)
        self.language = language
        self.keep_index = keep_index
        self.original_head = None
        # Optional directory holding a previously built index of exactly this
        # tree (e.g. keyed by commit). The GTAGS files are relocatable between
        # checkouts of the same tree, so restoring them skips the build.
        self.cache_dir = cache_dir
        self._restored = False

    def _run(self, cmd, **kw):
        """Run gtags/global; a missing binary becomes a MissingTool with install hints."""
        try:
            return subprocess.run(cmd, cwd=self.root_dir, capture_output=True, text=True, **kw)
        except FileNotFoundError:
            from crossslice.paths import MissingTool
            raise MissingTool(
                f"GNU Global is not installed ({cmd[0]} not found). Install it with "
                "`apt install global`, `brew install global` or scripts/setup_tools.sh, or use "
                "the Docker image. `crossslice check` shows what is installed.") from None

    # ---- lifecycle -------------------------------------------------------

    def __enter__(self):
        self.original_head = self._get_current_head()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        """Restore git state; drop the index unless keep_index is set"""
        self.restore_original_head()
        if not self.keep_index:
            self.clean_gtags_files()

    # ---- git state -------------------------------------------------------

    def _get_current_head(self):
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.root_dir, capture_output=True, text=True,
        )
        return result.stdout.strip() if result.returncode == 0 else None

    def checkout_commit(self, commit_hash):
        """Checkout specific commit"""
        try:
            subprocess.run(
                ["git", "checkout", commit_hash],
                cwd=self.root_dir, capture_output=True, text=True, check=True,
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to checkout commit {commit_hash}: {e}")
            return False

    def restore_original_head(self):
        if self.original_head:
            try:
                subprocess.run(
                    ["git", "checkout", self.original_head],
                    cwd=self.root_dir, capture_output=True, text=True, check=True,
                )
            except subprocess.CalledProcessError as e:
                print(f"Failed to restore original head {self.original_head}: {e}")

    # ---- index management ------------------------------------------------

    def check_gtags(self):
        return check_if_gtags_files_exist(self.dbpath)

    def _gtags_cmd(self, *flags):
        cmd = ["gtags", *flags]
        if self.dbpath != self.root_dir:
            cmd.append(self.dbpath)
        return cmd

    def generate_gtags(self):
        """Generate the gtags index from scratch"""
        self.clean_gtags_files()
        result = self._run(self._gtags_cmd())
        if result.returncode != 0:
            print(f"gtags failed: {result.stderr.strip()}")
            return False
        self._save_manifest()
        return True

    # ---- change detection for the incremental update ---------------------
    # `gtags -i` picks files by mtime with one-second granularity and misses a
    # file edited in the same second as the previous index write (a replay
    # loop or an editor save right after a query). The handler therefore keeps
    # its own manifest of (mtime_ns, size) per source file next to the index
    # and re-indexes every file whose signature changed with --single-update.

    def _manifest_path(self):
        return os.path.join(self.dbpath, MANIFEST)

    def _scan_tree(self):
        """{rel path: [mtime_ns, size]} of every C/C++ source file under the root."""
        root = os.path.abspath(self.root_dir)
        skip = {os.path.abspath(self.dbpath)} if self.dbpath != self.root_dir else set()
        out = {}
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d != ".git" and os.path.join(dirpath, d) not in skip]
            for fn in filenames:
                if fn.endswith(SOURCE_EXT):
                    path = os.path.join(dirpath, fn)
                    try:
                        st = os.stat(path)
                    except OSError:
                        continue
                    out[os.path.relpath(path, root)] = [st.st_mtime_ns, st.st_size]
        return out

    def _save_manifest(self, files=None):
        try:
            with open(self._manifest_path(), "w") as fh:
                json.dump(files if files is not None else self._scan_tree(), fh)
        except OSError:
            pass

    def _changed_since_manifest(self, now):
        """Files whose (mtime_ns, size) differ from the manifest; None without one."""
        try:
            with open(self._manifest_path()) as fh:
                old = json.load(fh)
        except (OSError, ValueError):
            return None
        return [rel for rel, sig in now.items() if old.get(rel) != sig]

    def update(self, changed_files=None):
        """Incrementally update an existing index (falls back to full generate).
        `changed_files` (repo-relative) are re-indexed explicitly, as is every
        file whose (mtime_ns, size) changed since the manifest was written."""
        if not self.check_gtags():
            return self.generate_gtags()
        now = self._scan_tree()
        changed = set(changed_files or ())
        scanned = self._changed_since_manifest(now)
        if scanned is not None:
            changed |= set(scanned)
        result = self._run(self._gtags_cmd("-i"))
        if result.returncode != 0:
            return self.generate_gtags()
        for rel in sorted(changed):
            if rel in now and self._run(self._gtags_cmd("--single-update", rel)).returncode != 0:
                return self.generate_gtags()
        self._save_manifest(now)
        return True

    def _cache_has_index(self):
        # the marker is written last, after an atomic directory rename, so a
        # cache another process is still writing is never picked up half-done
        return bool(self.cache_dir) and os.path.exists(
            os.path.join(self.cache_dir, "COMPLETE")) and all(
            os.path.exists(os.path.join(self.cache_dir, f)) for f in GTAGS_FILES)

    def _restore_from_cache(self):
        import shutil
        for f in GTAGS_FILES:
            shutil.copy2(os.path.join(self.cache_dir, f), os.path.join(self.dbpath, f))
        self._restored = True
        self._save_manifest()

    def _save_to_cache(self):
        import shutil
        import tempfile
        if not self.cache_dir or self._cache_has_index():
            return
        parent = os.path.dirname(self.cache_dir.rstrip(os.sep))
        os.makedirs(parent, exist_ok=True)
        tmp = tempfile.mkdtemp(prefix=".partial_", dir=parent)
        try:
            for f in GTAGS_FILES:
                shutil.copy2(os.path.join(self.dbpath, f), os.path.join(tmp, f))
            open(os.path.join(tmp, "COMPLETE"), "w").close()
            if os.path.exists(self.cache_dir):      # another process won the race
                shutil.rmtree(tmp, ignore_errors=True)
                return
            os.rename(tmp, self.cache_dir)            # atomic publish
        except Exception:
            shutil.rmtree(tmp, ignore_errors=True)

    def ensure_index(self):
        """Make sure a current index exists: restore it from the per-tree cache
        when available (no update needed — same tree), else build and cache."""
        if self.check_gtags():
            return True if self._restored else self.update()
        if self._cache_has_index():
            self._restore_from_cache()
            return True
        ok = self.generate_gtags()
        if ok:
            self._save_to_cache()
        return ok

    def clean_gtags_files(self):
        for f in GTAGS_FILES:
            file_path = os.path.join(self.dbpath, f)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"Failed to remove {file_path}: {e}")

    # ---- queries ---------------------------------------------------------

    def _query(self, flags, symbol):
        cmd = ["global", "--result", "grep", "-x", "-a", *flags, symbol]
        result = self._run(cmd, env=self._env)
        if result.returncode > 1:  # 1 = no match, >1 = real error
            print(f"global failed: {result.stderr.strip()}")
            return []
        entries = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split(":", 2)
            if len(parts) >= 3:
                file_path, lineno, code_line = parts
                entries.append((file_path, int(lineno), code_line))
        return entries

    def suggest(self, name, limit=8):
        """Defined symbols that look like `name`, best first (for "did you mean"):
        prefix completions (global -c) and case-insensitive substring matches."""
        import difflib
        import re
        cands = set()
        for prefix in {name[:4], name[:3], name[:2]}:
            if len(prefix) < 2:
                continue
            r = self._run(["global", "-c", prefix], env=self._env)
            cands.update(l.strip() for l in r.stdout.splitlines() if l.strip())
        core = max(re.split(r"[^A-Za-z0-9]+", name), key=len, default=name)
        if len(core) >= 3:
            r = self._run(["global", "-i", "-d", "-x", f".*{re.escape(core)}.*"], env=self._env)
            cands.update(l.split()[0] for l in r.stdout.splitlines() if l.strip())
        cands.discard(name)
        low_name = name.lower()

        def score(c):
            low = c.lower()
            return (low_name in low or low in low_name,
                    difflib.SequenceMatcher(None, low_name, low).ratio())
        ranked = [c for c in cands if len(c) >= 3]
        ranked = [c for c in ranked if score(c)[0] or score(c)[1] >= 0.5]   # drop `me` for memcpy
        return sorted(ranked, key=lambda c: (-score(c)[0], -score(c)[1], c))[:limit]  # ties: by name

    def find_function_definition(self, function_name):
        """All definitions as (file_path, line_number, declaration), 0-based lines"""
        return [(f, ln - 1, code) for f, ln, code in self._query(["-d"], function_name)]

    def find_function_definition_detailed(self, function_name):
        """All definitions as dicts, 1-based lines (resolver convention)"""
        return [
            {
                "symbol": function_name,
                "line_number": ln,
                "file_path": f,
                "code_line": code.strip(),
            }
            for f, ln, code in self._query(["-d"], function_name)
        ]

    def find_function_callers(self, function_name):
        """All reference sites as (file_path, line_number, statement), 0-based lines.

        Note: gtags references are name-based; whether a site is a real call
        (vs. address-taken use etc.) is decided later by tree-sitter/LSP.
        """
        return [(f, ln - 1, code) for f, ln, code in self._query(["-r"], function_name)]

    def find_function_callers_detailed(self, function_name):
        """All reference sites as dicts, 1-based lines"""
        return [
            {
                "symbol": function_name,
                "line_number": ln,
                "file_path": f,
                "code_line": code.strip(),
            }
            for f, ln, code in self._query(["-r"], function_name)
        ]

    def get_function_context(self, function_name):
        """Definitions and references for a symbol"""
        return {
            "function_name": function_name,
            "definitions": self.find_function_definition_detailed(function_name),
            "references": self.find_function_callers_detailed(function_name),
        }
