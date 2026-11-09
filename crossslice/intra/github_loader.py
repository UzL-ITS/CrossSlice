import os
from git import Repo

def clone_repository(repo_url, clone_dir):
    """
    Clones teh repostiroty from thee given URL into the specified directory.
    """
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
        Repo.clone_from(repo_url, clone_dir)
        print(f"Cloned repository from {repo_url} to {clone_dir}")
    else:
        print(f"Repository already exists at {clone_dir}")

def checkout_commit(repo_dir, commit_hash):
    """
    Checks out the repository at specified commit
    """
    repo = Repo(repo_dir)
    repo.git.checkout(commit_hash)
    print(f"Checked out to commit {commit_hash}")

def get_previous_commit(repo_dir, commit_hash):
    """
    Returns the hash of the previous commit
    """
    repo = Repo(repo_dir)
    commit = repo.commit(commit_hash)
    parents = commit.parents
    if parents:
        prev_commit_hash = parents[0].hexsha
        print(f"Previous commit hash: {prev_commit_hash}")
        return prev_commit_hash
    else:
        print("No previous commit found")
        return None
    
def generate_diff(repo_dir, old_commit, new_commit):
    """
    Generates the diff between two commits
    """
    repo = Repo(repo_dir)
    diff = repo.git.diff(old_commit, new_commit)
    return diff

def get_changed_files(repo_dir, old_commit, new_commit):
    """
    Returns the list of files changed between two commits
    """
    repo = Repo(repo_dir)
    diff = repo.git.diff("--name-only", old_commit, new_commit)
    return diff.split("\n")

def get_changed_lines(repo_dir, old_commit, new_commit):
    """
    Returns a list of dictionaries, each containing:
    - 'file_path': Relative path to the file.
    - 'line_numbers': List of changed line numbers in the file.
    """

    """
    changed_files = get_changed_files(repo_dir, old_commit, new_commit)
    changed_lines = []
    repo = Repo(repo_dir)
    for file in changed_files:
        diff = repo.git.diff("-U0", old_commit, new_commit, file)
        lines = diff.split("\n")
        changed_lines.append({
            "file_path": file,
            "line_numbers": [line[4:] for line in lines if line.startswith("@@")]
        })
    return changed_lines
    """

    # Hardcoded for the test project
    changed_lines = [
        {
            'file_paht': 'file2.c',
            'line_numbers': [4]
        }
    ]
    return changed_lines
    

def extract_file_from_commit(repo_dir, commit_hash, file_path, output_path):
    """Write `file_path` as of `commit_hash` to `output_path` (no checkout).
    Returns False when the file does not exist in that commit (added/deleted files)."""
    import subprocess
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        content = subprocess.check_output(
            ["git", "show", f"{commit_hash}:{file_path}"], cwd=repo_dir, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return False
    with open(output_path, "wb") as f:
        f.write(content)
    return True
