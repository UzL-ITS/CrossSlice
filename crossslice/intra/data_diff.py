import copy
import re
import subprocess
import json
import os
import uuid
import hashlib
import bisect
import sys


def decode_bytes_safely(data: bytes) -> str:
    """
    Decode bytes to string, trying multiple encodings.
    Falls back to latin-1 which can decode any byte sequence.

    :param data: Raw bytes to decode
    :return: Decoded string
    """
    # Try common encodings in order of preference
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue

    # Final fallback: decode with replacement characters
    return data.decode('utf-8', errors='replace')


def create_diff(folder_a, folder_b, changed_files):
    """
    Create a diff between two files. (with git diff)

    :param folder_a: The path to the old version of the folder.
    :param folder_b: The path to the new version of the folder.
    """
    diffs = []
    for file in changed_files:
        old_path = os.path.join(folder_a, file)
        new_path = os.path.join(folder_b, file)

        # Handle added file (old_path doesn't exist)
        if not os.path.exists(old_path) and os.path.exists(new_path):
            result = subprocess.run(
                ["git", "diff", "-U0", "--no-index", "/dev/null", new_path],
                capture_output=True
            )
            diffs.append(decode_bytes_safely(result.stdout))

        # Handle deleted file (new_path doesn't exist)
        elif os.path.exists(old_path) and not os.path.exists(new_path):
            result = subprocess.run(
                ["git", "diff", "-U0", "--no-index", old_path, "/dev/null"],
                capture_output=True
            )
            diffs.append(decode_bytes_safely(result.stdout))

        # Modified file
        elif os.path.exists(old_path) and os.path.exists(new_path):
            result = subprocess.run(
                ["git", "diff", "-U0", "--no-index", old_path, new_path],
                capture_output=True
            )
            diffs.append(decode_bytes_safely(result.stdout))

        # Both paths missing — unexpected, skip
        else:
            continue
    return "\n".join(diffs)