#!/usr/bin/env python3
"""Arkhon-Rheo Full Test Suite Runner.

This script executes the complete validation pipeline:
1. Pytest (Unit & Integration)
2. Ty (Static Type Checking)
3. Ruff (Linting & Style)
4. Radon (Cyclomatic Complexity)

Returns 0 only if all checks pass.
"""

import logging
import subprocess
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def run_command(command: list[str], label: str) -> bool:
    """Runs a shell command and returns True if successful."""
    logger.info(f"Running: {label}...")
    try:
        # Use uv run to ensure dependencies from pyproject.toml are used
        full_cmd = ["uv", "run", *command]
        # Safe as command is a list of strings and shell=False
        result = subprocess.run(full_cmd, capture_output=False, check=False)  # noqa: S603

        if result.returncode == 0:
            logger.info(f"{GREEN}✓ {label} Passed{RESET}")
            return True
        logger.error(f"{RED}✗ {label} Failed{RESET}")
        return False
    except FileNotFoundError:
        logger.error(f"{RED}✗ {label} Failed (Command not found){RESET}")
        return False


def main():
    # Correct paths: arkhon_rheo (with underscore)
    src_dir = Path("src/arkhon_rheo/")
    tests_dir = Path("tests/")

    # Define test stages
    stages = [
        (["pytest", "--tb=short", "-q"], "Pytest"),
        (["ty", "check", str(src_dir)], f"Type Check ({src_dir})"),
        (["ty", "check", str(tests_dir)], f"Type Check ({tests_dir})"),
        (["ruff", "check", str(src_dir)], f"Linter ({src_dir})"),
        (["ruff", "check", str(tests_dir)], f"Linter ({tests_dir})"),
        (["radon", "cc", "-s", str(src_dir)], f"Complexity ({src_dir})"),
        (["radon", "cc", "-s", str(tests_dir)], f"Complexity ({tests_dir})"),
    ]

    all_passed = True
    failed_stages = []

    for cmd, label in stages:
        if not run_command(cmd, label):
            all_passed = False
            failed_stages.append(label)

    if all_passed:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
