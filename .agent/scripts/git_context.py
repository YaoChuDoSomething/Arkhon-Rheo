#!/usr/bin/env python3
"""
git_context.py
Smart Context Packer for APE Reviewer.

Extracts changed files from git, identifies imports (using simple AST),
and prepares a context block for Repomix or direct LLM injection.
"""

import subprocess
import sys
import os
import ast
from pathlib import Path


def get_changed_files(target_branch="origin/dev"):
    """Get list of changed files compared to target branch (or local changes)."""
    try:
        # Check for staged/unstaged changes
        cmd = ["git", "diff", "--name-only", "HEAD"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        files = result.stdout.strip().split("\n")

        # If no local changes, check against upstream
        if not files or files == [""]:
            cmd = ["git", "diff", "--name-only", target_branch]
            result = subprocess.run(cmd, capture_output=True, text=True)
            files = result.stdout.strip().split("\n")

        return [f for f in files if f.endswith(".py") and os.path.exists(f)]
    except subprocess.CalledProcessError:
        print("Error: Not a git repository or git command failed.")
        return []


def get_imports(file_path):
    """Parse a python file and return a list of imported modules."""
    imports = set()
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read(), filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
    except Exception as e:
        print(f"Warning: Could not parse {file_path}: {e}")

    return list(imports)


def generate_context(files):
    """Generate a markdown context block."""
    context = "# Code Context\n\n"
    context += "The following files have changed:\n"
    for f in files:
        context += f"- `{f}`\n"

    context += "\n## Dependencies Detected\n"
    all_imports = set()
    for f in files:
        all_imports.update(get_imports(f))

    # Filter for internal modules (simple heuristic: if folder exists)
    internal_modules = [
        m for m in all_imports if os.path.exists(m) or os.path.exists(f"{m}.py")
    ]

    if internal_modules:
        context += "Internal modules referenced:\n"
        for m in internal_modules:
            context += f"- `{m}`\n"
    else:
        context += "No local internal modules detected in imports.\n"

    return context


def main():
    changed_files = get_changed_files()
    if not changed_files:
        print("No python files changed.")
        sys.exit(0)

    print(f"Detected changes in: {changed_files}")
    context_md = generate_context(changed_files)

    output_path = ".agent/context_pack.md"
    with open(output_path, "w") as f:
        f.write(context_md)

    print(f"Context written to {output_path}")


if __name__ == "__main__":
    main()
