#!/usr/bin/env python3
import ast
import os
import subprocess


def get_changed_files(target_branch="origin/main"):
    """Get list of changed files compared to target branch or local master."""
    try:
        # We look for files changed in the current session (Phase 3)
        # Using git log or diff to find what was modified in recent commits
        cmd = ["git", "diff", "--name-only", "main"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        files = result.stdout.strip().split("\n")

        return [f for f in files if f.endswith(".py") and os.path.exists(f)]
    except Exception as e:
        print(f"Error fetching changed files: {e}")
        return []


def get_imports(file_path):
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
    except Exception:
        pass
    return list(imports)


def generate_context(files):
    context = "# Code Context (Phase 3 Review)\n\n"
    context += "Changed Files:\n"
    for f in files:
        context += f"- `{f}`\n"
        context += "```python\n"
        with open(f, "r") as src:
            context += src.read()
        context += "\n```\n\n"

    return context


def main():
    files = get_changed_files()
    if not files:
        print("No files detected for review.")
        return

    context_md = generate_context(files)
    os.makedirs(".agent", exist_ok=True)
    with open(".agent/context_pack.md", "w") as f:
        f.write(context_md)
    print(f"Context packed for {len(files)} files into .agent/context_pack.md")


if __name__ == "__main__":
    main()
