import subprocess


def run_command(command: list[str], description: str) -> None:
    print(f"\n>>> Running {description}...")
    try:
        # Using uvx to ensure tools are run in a clean environment if not installed
        cmd = ["uvx"] + command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}:")
        print(e.stdout)
        print(e.stderr)
        # We don't exit here to allow other tools to run


def main():
    # 1. Ruff Linting & Formatting Check
    run_command(["ruff", "check", "."], "Ruff Linting")

    # 2. Ty Static Type Check (Red Knot)
    run_command(["ty", "check", "."], "Ty Type Check")

    # 3. Radon Complexity Analysis
    run_command(["radon", "cc", "src", "-a"], "Radon Complexity")

    # 4. Pytest (explicitly including pytest-cov for uvx)
    run_command(
        ["--with", "pytest-cov", "pytest", "--cov=src", "tests/"],
        "Pytest with Coverage",
    )


if __name__ == "__main__":
    main()
