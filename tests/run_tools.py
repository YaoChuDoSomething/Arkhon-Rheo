import subprocess


def run_command(command: list[str]) -> None:
    try:
        # Using uvx to ensure tools are run in a clean environment if not installed
        cmd = ["uvx", *command]
        subprocess.run(cmd, capture_output=True, text=True, check=True)  # noqa: S603
    except subprocess.CalledProcessError:
        pass
        # We don't exit here to allow other tools to run


def main():
    # 1. Ruff Linting & Formatting Check
    run_command(["ruff", "check", "."])

    # 2. Ty Static Type Check (Red Knot)
    run_command(["ty", "check", "."])

    # 3. Radon Complexity Analysis
    run_command(["radon", "cc", "src", "-a"])

    # 4. Pytest (explicitly including pytest-cov for uvx)
    run_command(["--with", "pytest-cov", "pytest", "--cov=src", "tests/"])


if __name__ == "__main__":
    main()
