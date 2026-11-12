"""On-demand, local-only system information snapshot."""
from __future__ import annotations

import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Any


def _memory_total_bytes() -> int | None:
    if sys.platform == "win32":
        try:
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(MemoryStatus)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return int(status.ullTotalPhys)
        except (AttributeError, OSError, TypeError):
            return None
        return None
    if hasattr(os, "sysconf"):
        try:
            pages = os.sysconf("SC_PHYS_PAGES")
            page_size = os.sysconf("SC_PAGE_SIZE")
            if pages > 0 and page_size > 0:
                return int(pages * page_size)
        except (OSError, ValueError):
            return None
    return None


def _human_bytes(value: int | None) -> str:
    if value is None:
        return "Not available"
    units = ("B", "KB", "MB", "GB", "TB")
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.1f} {unit}"
        amount /= 1024
    return "Not available"


def system_snapshot() -> dict[str, Any]:
    """Return a point-in-time host summary; does not monitor or modify the OS."""
    try:
        disk_free = shutil.disk_usage(Path.home()).free
    except OSError:
        disk_free = None
    processor = platform.processor() or os.environ.get("PROCESSOR_IDENTIFIER") or "Not reported"
    memory = _memory_total_bytes()
    return {
        "os": platform.system() or "Unknown",
        "os_release": platform.release() or "Unknown",
        "os_version": platform.version() or "Not reported",
        "architecture": platform.machine() or "Unknown",
        "processor": processor,
        "logical_cpus": os.cpu_count(),
        "memory_total_bytes": memory,
        "memory_total": _human_bytes(memory),
        "disk_free_bytes": disk_free,
        "disk_free": _human_bytes(disk_free),
        "collection": "On demand",
        "mode": "Local / read-only",
    }
