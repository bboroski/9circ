# 9circ security and data model

## Default trust posture

9circ runs as the current desktop user and does not request administrator/root privileges. The audit is local and read-only. The app does not install a daemon, scheduled task, kernel module, driver, browser extension, or service.

## Data handled

The app stores paths to folders explicitly selected by the user, display names and profile labels, short event messages, timestamps, and audit findings. The repository scanner inventories names and metadata; it does not read source contents. A system snapshot is collected only when the user opens or refreshes the System Profile. No network transmission is implemented.

The registry and activity log are stored under the current user's application data directory. POSIX permissions are restricted on a best-effort basis. Protect the OS account and backups as usual.

## Allowed operations

- Read directory entries and file metadata in a selected repository.
- Skip dependency, VCS, and generated-output folders.
- Display basic host metadata collected on demand.
- Write the app's own registry and local activity log.
- Export a report to a user-selected path.

## Forbidden by design

- Automatic edits to repository source files.
- Running commands, build scripts, package hooks, or downloaded code during an audit.
- Writing to OS registry, system directories, kernel, drivers, firmware, boot configuration, services, or security controls.
- Installing, updating, or uninstalling applications.
- Remote execution, credential harvesting, stealth, persistence, or background network telemetry.
- Automatic merge, release signing, deployment, or self-granted permissions.

## Approval protocol for future change features

Any future patch workflow must identify the exact repository, branch, and base commit; create an isolated proposal; show the full diff and affected paths; state tests, side effects, and rollback; require explicit approval for that exact proposal; verify tests; and record the result. Approval for one proposal never authorizes a different diff or later action.

## Threat assumptions

A selected repository may contain untrusted filenames, malformed metadata, symlinks, large directory trees, or hostile build scripts. The scanner avoids symlink traversal, does not execute repository code, and enforces inventory limits. Future parsers must treat repository content as untrusted input.
