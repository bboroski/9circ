"""Local repository registry and activity log."""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def default_data_dir() -> Path:
    if os.name == "nt":
        return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "9circ"
    if sys_platform() == "darwin":
        return Path.home() / "Library" / "Application Support" / "9circ"
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "9circ"


def sys_platform() -> str:
    import sys
    return sys.platform


class LocalStore:
    """Persist user-selected paths and short audit summaries on this device."""

    def __init__(self, data_dir: str | os.PathLike[str] | None = None) -> None:
        self.data_dir = Path(data_dir).expanduser() if data_dir else default_data_dir()
        self.registry_path = self.data_dir / "registry.json"
        self.events_path = self.data_dir / "activity.jsonl"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._restrict_permissions(self.data_dir, directory=True)

    @staticmethod
    def _restrict_permissions(path: Path, *, directory: bool = False) -> None:
        if os.name != "nt":
            try:
                path.chmod(0o700 if directory else 0o600)
            except OSError:
                pass

    def _read_registry(self) -> list[dict[str, str]]:
        if not self.registry_path.exists():
            return []
        try:
            data = json.loads(self.registry_path.read_text(encoding="utf-8"))
            rows = data.get("repositories", [])
            if not isinstance(rows, list):
                return []
            return [row for row in rows if isinstance(row, dict) and isinstance(row.get("path"), str)]
        except (OSError, json.JSONDecodeError, AttributeError):
            return []

    @property
    def repositories(self) -> list[dict[str, str]]:
        return self._read_registry()

    def _write_registry(self, rows: list[dict[str, str]]) -> None:
        payload = json.dumps({"schema_version": 1, "repositories": rows}, ensure_ascii=False, indent=2)
        fd, name = tempfile.mkstemp(prefix="registry-", suffix=".tmp", dir=self.data_dir)
        temporary = Path(name)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(payload + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._restrict_permissions(temporary)
            os.replace(temporary, self.registry_path)
            self._restrict_permissions(self.registry_path)
        finally:
            temporary.unlink(missing_ok=True)

    def add_repository(self, repository_path: str | os.PathLike[str]) -> dict[str, str]:
        path = Path(repository_path).expanduser().resolve()
        if not path.is_dir():
            raise ValueError("Choose an existing local folder.")
        rows = self._read_registry()
        normalized = os.path.normcase(str(path))
        for row in rows:
            if os.path.normcase(row["path"]) == normalized:
                return row
        profile = {"name": path.name or str(path), "path": str(path), "role": "Independent repository"}
        rows.append(profile)
        self._write_registry(rows)
        return profile

    def remove_repository(self, repository_path: str) -> bool:
        normalized = os.path.normcase(str(Path(repository_path).expanduser().resolve()))
        rows = self._read_registry()
        filtered = [row for row in rows if os.path.normcase(row.get("path", "")) != normalized]
        if len(filtered) == len(rows):
            return False
        self._write_registry(filtered)
        return True

    def append_event(self, event_type: str, message: str, *, repository: str | None = None) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "type": event_type, "message": message,
        }
        if repository:
            event["repository"] = repository
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
        self._restrict_permissions(self.events_path)

    def read_events(self, limit: int = 100) -> list[dict[str, Any]]:
        if not self.events_path.exists():
            return []
        events: list[dict[str, Any]] = []
        try:
            with self.events_path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    try:
                        value = json.loads(line)
                        if isinstance(value, dict):
                            events.append(value)
                    except json.JSONDecodeError:
                        continue
        except OSError:
            return []
        return events[-max(1, limit):]
