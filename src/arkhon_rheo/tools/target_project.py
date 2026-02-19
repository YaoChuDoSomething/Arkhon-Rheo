"""TargetProject — Sandboxed file and shell interface for the DEV-TARGET project.

All file writes and shell commands are validated against the constraints
defined in :class:`~arkhon_rheo.config.schema.ConstraintsConfig` before
execution.  This is the single chokepoint for all agent-initiated side
effects on the target project directory.

Observability:
    Every operation is instrumented with ``structlog`` and a
    ``prometheus_client`` counter so that the ``observability-engineer``
    skill can surface them in dashboards.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import structlog
from prometheus_client import Counter

from arkhon_rheo.config.schema import ConstraintsConfig, TargetProjectConfig

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Observability counters (prometheus-client, already in deps)
# ---------------------------------------------------------------------------

_OP_COUNTER = Counter(
    "arkhon_target_project_ops_total",
    "Total operations performed on the target project.",
    ["operation", "status"],
)


class WriteGuardError(PermissionError):
    """Raised when an agent attempts a write outside ``allowed_write_dirs``."""


class ShellGuardError(PermissionError):
    """Raised when an agent attempts to execute a non-whitelisted command."""


class TargetProject:
    """Sandboxed interface to the DEV-TARGET project directory.

    Attributes:
        root: Resolved absolute path to the target project root.
        constraints: Operational constraints from ``config/workflow_context.yaml``.
    """

    def __init__(
        self,
        project_config: TargetProjectConfig,
        constraints: ConstraintsConfig,
        base_dir: Path | None = None,
    ) -> None:
        """Initialise the interface.

        Args:
            project_config: Target project metadata (name, path).
            constraints: Write-dir whitelist and shell whitelist.
            base_dir: Resolve relative ``target_path`` relative to this directory.
                      Defaults to ``Path.cwd()``.
        """
        base = base_dir or Path.cwd()
        self.root: Path = (base / project_config.target_path).resolve()
        self.constraints = constraints
        self._log = logger.bind(target_root=str(self.root))

        if not self.root.exists():
            self._log.warning("target_root_missing", path=str(self.root))

    # ------------------------------------------------------------------
    # File operations
    # ------------------------------------------------------------------

    def read_file(self, relative_path: str) -> str:
        """Read a file from the target project.

        Args:
            relative_path: Path relative to ``self.root``.

        Returns:
            File contents as a UTF-8 string.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        full = self._resolve(relative_path)
        self._log.info("read_file", path=relative_path)
        _OP_COUNTER.labels(operation="read", status="ok").inc()
        return full.read_text(encoding="utf-8")

    def write_file(self, relative_path: str, content: str) -> Path:
        """Write content to a file in the target project.

        The target directory is validated against ``allowed_write_dirs``
        before any write occurs.

        Args:
            relative_path: Path relative to ``self.root``.
            content: UTF-8 content to write.

        Returns:
            The resolved absolute :class:`~pathlib.Path` that was written.

        Raises:
            WriteGuardError: If the path is outside ``allowed_write_dirs``.
        """
        full = self._resolve(relative_path)
        self._check_write_allowed(relative_path)

        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")

        self._log.info("write_file", path=relative_path)
        _OP_COUNTER.labels(operation="write", status="ok").inc()
        return full

    def list_files(self, relative_dir: str = "") -> list[str]:
        """List files under a directory in the target project.

        Args:
            relative_dir: Directory relative to ``self.root`` (empty = root).

        Returns:
            Sorted list of file paths relative to ``self.root``.
        """
        base = self._resolve(relative_dir) if relative_dir else self.root
        if not base.is_dir():
            return []
        files = [str(p.relative_to(self.root)) for p in base.rglob("*") if p.is_file()]
        _OP_COUNTER.labels(operation="list", status="ok").inc()
        return sorted(files)

    # ------------------------------------------------------------------
    # Shell execution
    # ------------------------------------------------------------------

    def run_command(self, command: str, *, cwd: str | None = None) -> str:
        """Run a whitelisted shell command in the target project directory.

        Args:
            command: The shell command string to execute.
            cwd: Override working directory (default: ``self.root``).

        Returns:
            Combined stdout + stderr output.

        Raises:
            ShellGuardError: If the command is not in ``shell_whitelist``.
            subprocess.CalledProcessError: If the command exits with non-zero.
        """
        self._check_command_allowed(command)
        work_dir = Path(cwd).resolve() if cwd else self.root

        self._log.info("run_command", command=command, cwd=str(work_dir))
        try:
            result = subprocess.run(
                command,
                shell=True,  # noqa: S602
                capture_output=True,
                text=True,
                cwd=work_dir,
                check=True,
            )
            _OP_COUNTER.labels(operation="shell", status="ok").inc()
            return result.stdout + result.stderr
        except subprocess.CalledProcessError as exc:
            _OP_COUNTER.labels(operation="shell", status="error").inc()
            self._log.error("command_failed", command=command, returncode=exc.returncode)
            raise

    # ------------------------------------------------------------------
    # Guards
    # ------------------------------------------------------------------

    def _resolve(self, relative: str) -> Path:
        return (self.root / relative).resolve()

    def _check_write_allowed(self, relative_path: str) -> None:
        allowed = self.constraints.allowed_write_dirs
        if not any(relative_path.startswith(d) for d in allowed):
            _OP_COUNTER.labels(operation="write", status="denied").inc()
            raise WriteGuardError(f"Write denied: '{relative_path}' is not under allowed_write_dirs={allowed}")

    def _check_command_allowed(self, command: str) -> None:
        whitelist = self.constraints.shell_whitelist
        if not any(command.startswith(w) for w in whitelist):
            _OP_COUNTER.labels(operation="shell", status="denied").inc()
            raise ShellGuardError(f"Command denied: '{command}' not in shell_whitelist={whitelist}")
