"""Tk desktop interface for 9circ."""
from __future__ import annotations

import json
import tkinter as tk
from datetime import datetime, timezone
from tkinter import filedialog, messagebox, ttk
from typing import Any

from . import __version__
from .audit import build_triadic_matrix, scan_repository
from .store import LocalStore
from .system import system_snapshot

BG, PANEL, PANEL_ALT, LINE = "#050505", "#121212", "#171717", "#1F1F1F"
GREEN, TEXT, SECONDARY, MUTED = "#006442", "#F4F4F4", "#C8C8C8", "#929292"
RED, YELLOW = "#FF1E1E", "#F2C94C"


class NineCircApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.store = LocalStore()
        self.last_audit: dict[str, Any] | None = None
        self.system = system_snapshot()
        self.current_view = "overview"
        self.repo_tree: ttk.Treeview | None = None
        root.title("9circ — Local Optimization Studio")
        root.geometry("1320x860")
        root.minsize(1080, 700)
        root.configure(bg=BG)
        self.style = ttk.Style(root)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self._styles()
        self._shell()
        self.show_view("overview")

    def _styles(self) -> None:
        self.style.configure(".", background=BG, foreground=TEXT, fieldbackground=PANEL, bordercolor=LINE, font=("Segoe UI", 10))
        self.style.configure("TButton", padding=(12, 9), background=PANEL_ALT, foreground=TEXT, borderwidth=1, relief="flat")
        self.style.map("TButton", background=[("active", "#242424"), ("pressed", GREEN)], foreground=[("disabled", MUTED)])
        self.style.configure("Primary.TButton", padding=(14, 10), background=GREEN, foreground=TEXT, borderwidth=0)
        self.style.map("Primary.TButton", background=[("active", "#087A55"), ("pressed", "#004B32")])
        self.style.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=TEXT, rowheight=34, borderwidth=0)
        self.style.configure("Treeview.Heading", background="#202020", foreground=SECONDARY, padding=(8, 8), relief="flat")
        self.style.map("Treeview", background=[("selected", "#174B3B")], foreground=[("selected", TEXT)])

    def _shell(self) -> None:
        shell = tk.Frame(self.root, bg=BG)
        shell.pack(fill="both", expand=True)
        self.sidebar = tk.Frame(shell, bg=PANEL, width=230, highlightthickness=1, highlightbackground=LINE)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        brand = tk.Frame(self.sidebar, bg=PANEL)
        brand.pack(fill="x", padx=22, pady=(24, 34))
        tk.Label(brand, text="9circ", bg=PANEL, fg=TEXT, font=("Segoe UI", 24, "bold")).pack(anchor="w")
        tk.Label(brand, text="LOCAL OPTIMIZATION STUDIO", bg=PANEL, fg=GREEN, font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(2, 0))
        self.nav_buttons: dict[str, ttk.Button] = {}
        for key, label in [
            ("overview", "Overview"), ("repositories", "Repositories"),
            ("matrix", "Triadic matrix"), ("system", "System profile"),
            ("activity", "Activity log"),
        ]:
            button = ttk.Button(self.sidebar, text=label, command=lambda view=key: self.show_view(view))
            button.pack(fill="x", padx=14, pady=4)
            self.nav_buttons[key] = button
        tk.Frame(self.sidebar, bg=LINE, height=1).pack(fill="x", padx=18, pady=(28, 14))
        tk.Label(self.sidebar, text="LOCAL • READ ONLY", bg=PANEL, fg=GREEN, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=22)
        tk.Label(self.sidebar, text=f"Version {__version__}", bg=PANEL, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=22, pady=(5, 0))
        self.main = tk.Frame(shell, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

    def _header(self, title: str, subtitle: str) -> tk.Frame:
        header = tk.Frame(self.main, bg=BG)
        header.pack(fill="x", padx=30, pady=(26, 20))
        left = tk.Frame(header, bg=BG)
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text=title, bg=BG, fg=TEXT, font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(left, text=subtitle, bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(5, 0))
        return header

    def _content(self) -> tk.Frame:
        frame = tk.Frame(self.main, bg=BG)
        frame.pack(fill="both", expand=True, padx=30, pady=(0, 28))
        return frame

    def _card(self, parent: tk.Widget, title: str, value: str, detail: str) -> tk.Frame:
        card = tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=16, pady=15)
        tk.Label(card, text=title.upper(), bg=PANEL, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(card, text=value, bg=PANEL, fg=TEXT, font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(10, 2))
        tk.Label(card, text=detail, bg=PANEL, fg=GREEN, font=("Segoe UI", 9)).pack(anchor="w")
        return card

    def _section(self, parent: tk.Widget, title: str, detail: str = "") -> None:
        tk.Label(parent, text=title, bg=BG, fg=TEXT, font=("Segoe UI", 13, "bold")).pack(anchor="w")
        if detail:
            tk.Label(parent, text=detail, bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(3, 10))

    def _clear(self) -> None:
        for child in self.main.winfo_children():
            child.destroy()
        self.repo_tree = None

    def show_view(self, view: str) -> None:
        self.current_view = view
        for key, button in self.nav_buttons.items():
            button.configure(style="Primary.TButton" if key == view else "TButton")
        self._clear()
        {
            "overview": self._overview, "repositories": self._repositories,
            "matrix": self._matrix, "system": self._system, "activity": self._activity,
        }.get(view, self._overview)()

    def _overview(self) -> None:
        header = self._header("Overview", "A local control room for repository evidence and safe improvement planning.")
        ttk.Button(header, text="Run repository audit", style="Primary.TButton", command=self.run_audit).pack(side="right")
        content = self._content()
        repos = self.store.repositories
        cards = tk.Frame(content, bg=BG)
        cards.pack(fill="x")
        values = [
            ("Tracked repositories", str(len(repos)), "Explicitly selected folders"),
            ("Matrix stages", "03", "Observe · Evaluate · Propose"),
            ("Host operating system", self.system["os"], self.system["os_release"]),
            ("Execution mode", "LOCAL", "No remote calls or background agent"),
        ]
        for index, item in enumerate(values):
            self._card(cards, *item).grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 8, 0), pady=2)
            cards.grid_columnconfigure(index, weight=1, uniform="metric")
        self._section(content, "Operating boundary", "The app observes and proposes; it does not autonomously apply changes.")
        boundary = tk.Frame(content, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=18, pady=16)
        boundary.pack(fill="x", pady=(0, 20))
        for number, title, detail in [
            ("01", "READ-ONLY INVENTORY", "No source files are changed during an audit."),
            ("02", "NO PRIVILEGED OPERATIONS", "No registry, kernel, driver, service, or firmware writes."),
            ("03", "HUMAN APPROVAL", "Future patches must be previewed, tested, and explicitly approved."),
        ]:
            row = tk.Frame(boundary, bg=PANEL)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=number, bg=PANEL, fg=GREEN, width=4, font=("Consolas", 10, "bold")).pack(side="left")
            info = tk.Frame(row, bg=PANEL)
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=title, bg=PANEL, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(anchor="w")
            tk.Label(info, text=detail, bg=PANEL, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))
        self._section(content, "Repository profiles", "Each repository keeps its own identity and local path.")
        if not repos:
            self._empty(content, "No repositories registered", "Add a local repository folder to start its first triadic audit.")
        else:
            for repo in repos[:5]:
                line = tk.Frame(content, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=12, pady=10)
                line.pack(fill="x", pady=3)
                tk.Label(line, text=repo["name"], bg=PANEL, fg=TEXT, font=("Segoe UI", 10, "bold")).pack(anchor="w")
                tk.Label(line, text=repo["path"], bg=PANEL, fg=MUTED, font=("Consolas", 8)).pack(anchor="w", pady=(3, 0))

    def _repositories(self) -> None:
        header = self._header("Repositories", "Choose the folders that 9circ is allowed to inspect.")
        ttk.Button(header, text="Add folder", style="Primary.TButton", command=self.add_repository).pack(side="right")
        content = self._content()
        self._section(content, "Local registry", "Removing a profile never deletes the selected folder.")
        table = tk.Frame(content, bg=PANEL, highlightthickness=1, highlightbackground=LINE)
        table.pack(fill="both", expand=True)
        tree = ttk.Treeview(table, columns=("name", "role", "path"), show="headings", selectmode="browse")
        for key, label, width in [("name", "REPOSITORY", 180), ("role", "PROFILE", 190), ("path", "LOCAL PATH", 600)]:
            tree.heading(key, text=label)
            tree.column(key, width=width, minwidth=120)
        tree.pack(fill="both", expand=True, padx=1, pady=1)
        self.repo_tree = tree
        for repo in self.store.repositories:
            tree.insert("", "end", iid=repo["path"], values=(repo["name"], repo.get("role", "Independent repository"), repo["path"]))
        actions = tk.Frame(content, bg=BG)
        actions.pack(fill="x", pady=(14, 0))
        ttk.Button(actions, text="Audit selected", command=self.run_audit).pack(side="left")
        ttk.Button(actions, text="Remove profile", command=self.remove_repository).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Export report", command=self.export_report).pack(side="right")

    def _matrix(self) -> None:
        header = self._header("Triadic matrix", "Three stages × three axes. Evidence first, change approval last.")
        ttk.Button(header, text="Run selected audit", style="Primary.TButton", command=self.run_audit).pack(side="right")
        content = self._content()
        if self.last_audit is None:
            self._empty(content, "No audit report yet", "Select a repository and run a read-only audit to generate its matrix.")
            return
        snapshot, matrix = self.last_audit["snapshot"], self.last_audit["matrix"]
        summary = tk.Frame(content, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=16, pady=14)
        summary.pack(fill="x", pady=(0, 16))
        tk.Label(summary, text=snapshot["repository"], bg=PANEL, fg=TEXT, font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(summary, text=snapshot["path"], bg=PANEL, fg=MUTED, font=("Consolas", 8)).pack(anchor="w", pady=(3, 7))
        tk.Label(summary, text=f"Matrix score  {matrix['score']} / 9     •     {snapshot['file_count']} files     •     {snapshot['source_count']} source files",
                 bg=PANEL, fg=GREEN, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        stages = tk.Frame(content, bg=BG)
        stages.pack(fill="x")
        for index, stage in enumerate(matrix["stages"]):
            card = tk.Frame(stages, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=14, pady=14)
            card.grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 8, 0))
            stages.grid_columnconfigure(index, weight=1, uniform="stage")
            tk.Label(card, text=stage["id"], bg=PANEL, fg=GREEN, font=("Consolas", 10, "bold")).pack(anchor="w")
            tk.Label(card, text=stage["title"], bg=PANEL, fg=TEXT, font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(5, 0))
            tk.Label(card, text=stage["subtitle"], bg=PANEL, fg=MUTED, font=("Segoe UI", 8), wraplength=260, justify="left").pack(anchor="w", pady=(3, 10))
            for axis in stage["axes"]:
                self._axis_row(card, axis)
        self._section(content, "Evidence-based findings", "Recommendations only — no changes were executed.")
        for finding in matrix.get("findings", []):
            self._finding(content, finding)
        ttk.Button(content, text="Export JSON report", command=self.export_report).pack(anchor="e", pady=(12, 0))

    def _axis_row(self, parent: tk.Widget, axis: dict[str, str]) -> None:
        color = GREEN if axis["state"] == "READY" else YELLOW if axis["state"] == "REVIEW" else RED
        row = tk.Frame(parent, bg=PANEL, pady=7)
        row.pack(fill="x")
        tk.Label(row, text=axis["name"], bg=PANEL, fg=SECONDARY, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(row, text=axis["state"], bg=PANEL, fg=color, font=("Consolas", 9, "bold")).pack(anchor="w", pady=(2, 0))
        tk.Label(row, text=axis["detail"], bg=PANEL, fg=MUTED, font=("Segoe UI", 8), wraplength=260, justify="left").pack(anchor="w", pady=(2, 0))
        tk.Frame(parent, bg=LINE, height=1).pack(fill="x")

    def _finding(self, parent: tk.Widget, item: dict[str, str]) -> None:
        color = YELLOW if item.get("severity") == "REVIEW" else MUTED
        row = tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=12, pady=10)
        row.pack(fill="x", pady=3)
        top = tk.Frame(row, bg=PANEL)
        top.pack(fill="x")
        tk.Label(top, text=item.get("severity", "INFO"), bg=PANEL, fg=color, font=("Consolas", 8, "bold")).pack(side="left")
        tk.Label(top, text=item.get("title", "Finding"), bg=PANEL, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(10, 0))
        tk.Label(row, text=item.get("detail", ""), bg=PANEL, fg=MUTED, font=("Segoe UI", 9), wraplength=940, justify="left").pack(anchor="w", pady=(5, 0))

    def _system(self) -> None:
        header = self._header("System profile", "A one-time local snapshot. No monitoring service is installed.")
        ttk.Button(header, text="Refresh snapshot", command=self.refresh_system).pack(side="right")
        content = self._content()
        self._section(content, "Host overview", "System information remains on this device.")
        fields = [
            ("Operating system", "os"), ("Release", "os_release"), ("Architecture", "architecture"),
            ("Processor", "processor"), ("Logical CPUs", "logical_cpus"), ("Installed memory", "memory_total"),
            ("Free disk space", "disk_free"), ("Collection", "collection"), ("Execution mode", "mode"),
        ]
        grid = tk.Frame(content, bg=BG)
        grid.pack(fill="x")
        for index, (label, key) in enumerate(fields):
            card = tk.Frame(grid, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=14, pady=13)
            card.grid(row=index // 3, column=index % 3, sticky="nsew", padx=(0 if index % 3 == 0 else 8, 0), pady=4)
            grid.grid_columnconfigure(index % 3, weight=1, uniform="system")
            tk.Label(card, text=label.upper(), bg=PANEL, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
            tk.Label(card, text=str(self.system.get(key) or "Not reported"), bg=PANEL, fg=TEXT,
                     font=("Segoe UI", 11, "bold"), wraplength=260, justify="left").pack(anchor="w", pady=(8, 0))
        warning = tk.Frame(content, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=14, pady=12)
        warning.pack(fill="x", pady=(18, 0))
        tk.Label(warning, text="NO OS OPTIMIZATION IS APPLIED", bg=PANEL, fg=GREEN, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(warning, text="9circ does not edit the registry, change services, install packages, patch drivers, or modify kernel settings.",
                 bg=PANEL, fg=SECONDARY, font=("Segoe UI", 9), wraplength=920, justify="left").pack(anchor="w", pady=(5, 0))

    def _activity(self) -> None:
        header = self._header("Activity log", "Local audit events. No remote telemetry or account sync.")
        content = self._content()
        events = list(reversed(self.store.read_events(100)))
        self._section(content, f"{len(events)} recent events", "The log is stored in the current user's application data directory.")
        if not events:
            self._empty(content, "No activity recorded", "A local event appears after the first repository audit.")
            return
        for event in events:
            row = tk.Frame(content, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=12, pady=9)
            row.pack(fill="x", pady=3)
            line = tk.Frame(row, bg=PANEL)
            line.pack(fill="x")
            tk.Label(line, text=str(event.get("type", "EVENT")).upper(), bg=PANEL, fg=GREEN, font=("Consolas", 8, "bold")).pack(side="left")
            tk.Label(line, text=event.get("timestamp", ""), bg=PANEL, fg=MUTED, font=("Consolas", 8)).pack(side="right")
            tk.Label(row, text=event.get("message", ""), bg=PANEL, fg=TEXT, font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 0))
            if event.get("repository"):
                tk.Label(row, text=event["repository"], bg=PANEL, fg=MUTED, font=("Consolas", 8)).pack(anchor="w", pady=(3, 0))

    def _empty(self, parent: tk.Widget, title: str, detail: str) -> None:
        panel = tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=22, pady=24)
        panel.pack(fill="x", pady=(5, 12))
        tk.Label(panel, text=title, bg=PANEL, fg=TEXT, font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(panel, text=detail, bg=PANEL, fg=MUTED, font=("Segoe UI", 9), wraplength=820, justify="left").pack(anchor="w", pady=(6, 12))
        if self.current_view in {"overview", "repositories", "matrix"}:
            ttk.Button(panel, text="Add local repository", style="Primary.TButton", command=self.add_repository).pack(anchor="w")

    def add_repository(self) -> None:
        selected = filedialog.askdirectory(title="Select a local repository folder", mustexist=True)
        if not selected:
            return
        try:
            profile = self.store.add_repository(selected)
            self.store.append_event("repository-added", f"Registered {profile['name']}", repository=profile["path"])
        except (OSError, ValueError) as error:
            messagebox.showerror("Could not add repository", str(error))
            return
        self.show_view("repositories")

    def _selected_repository(self) -> dict[str, str] | None:
        if self.repo_tree is not None:
            selection = self.repo_tree.selection()
            if selection:
                selected_path = selection[0]
                return next((repo for repo in self.store.repositories if repo["path"] == selected_path), None)
        rows = self.store.repositories
        return rows[0] if rows else None

    def remove_repository(self) -> None:
        repo = self._selected_repository()
        if not repo:
            messagebox.showinfo("No selection", "Select a repository profile first.")
            return
        if not messagebox.askyesno("Remove profile", f"Remove {repo['name']} from the registry?\n\nThe folder will not be deleted."):
            return
        self.store.remove_repository(repo["path"])
        self.store.append_event("repository-removed", f"Removed profile {repo['name']}")
        self.show_view("repositories")

    def run_audit(self) -> None:
        repo = self._selected_repository()
        if not repo:
            messagebox.showinfo("No repository", "Add a local repository folder before starting an audit.")
            self.show_view("repositories")
            return
        try:
            snapshot = scan_repository(repo["path"])
            matrix = build_triadic_matrix(snapshot)
        except (OSError, ValueError, PermissionError) as error:
            messagebox.showerror("Audit failed", str(error))
            return
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self.last_audit = {"timestamp": timestamp, "snapshot": snapshot, "matrix": matrix}
        self.store.append_event("audit-completed",
            f"Read-only triadic audit: {snapshot['file_count']} files, score {matrix['score']}/9",
            repository=snapshot["path"])
        self.show_view("matrix")

    def refresh_system(self) -> None:
        self.system = system_snapshot()
        self.store.append_event("system-snapshot", "On-demand local system snapshot refreshed")
        self.show_view("system")

    def export_report(self) -> None:
        if self.last_audit is None:
            messagebox.showinfo("No report", "Run a repository audit before exporting.")
            return
        destination = filedialog.asksaveasfilename(
            title="Export 9circ audit report", defaultextension=".json",
            filetypes=[("JSON report", "*.json")], initialfile="9circ-audit-report.json",
        )
        if not destination:
            return
        try:
            with open(destination, "w", encoding="utf-8") as handle:
                json.dump(self.last_audit, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
        except OSError as error:
            messagebox.showerror("Export failed", str(error))
            return
        self.store.append_event("report-exported", "Audit report exported to a user-selected file")
        messagebox.showinfo("Report exported", "The JSON report was saved.")

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    root = tk.Tk()
    NineCircApp(root).run()


if __name__ == "__main__":
    main()
