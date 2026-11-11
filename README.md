# 9circ

9circ is a native-first engineering verification toolkit implemented in C#, Ruby, and Swift. Its first runtime is deliberately small: a shared Swift C ABI scans raw bytes, while each language exposes the same machine-readable source-inspection report.

## Runtime layout

- `swift/Sources/NinecircCore`: native byte scanner and SHA-256 implementation.
- `swift/Sources/NinecircCLI`: Swift command-line entry point.
- `csharp/9circ`: unsafe .NET command-line host using `Span<byte>`, pinned buffers, and P/Invoke.
- `ruby/lib`: Ruby host using Fiddle and the same native ABI.
- `.github/workflows/ci.yml`: builds the native library and runs all three language test suites.

The ABI is versioned and fixed-width. `ninecirc_scan` receives a byte pointer and byte count and writes a 48-byte little-endian result. See `docs/ABI.md`.

## Build

Requirements: Swift 6, .NET 8 SDK, and Ruby 3.2 or newer.

### Linux

```sh
swift build --package-path swift -c release --product ninecirc_core
export NINECIRC_NATIVE_LIBRARY="$PWD/swift/.build/release/libninecirc_core.so"
export LD_LIBRARY_PATH="$PWD/swift/.build/release:$LD_LIBRARY_PATH"
swift test --package-path swift
dotnet build csharp/9circ/9circ.csproj -c Release
dotnet run --project csharp/9circ/9circ.csproj -c Release -- scan README.md
ruby ruby/bin/9circ scan README.md
ruby ruby/test/test_ninecirc.rb
swift run --package-path swift 9circ-swift scan README.md
dotnet run --project csharp/9circ.Tests/9circ.Tests.csproj -c Release
```

### macOS

Build the Swift product first, set `NINECIRC_NATIVE_LIBRARY` to `swift/.build/release/libninecirc_core.dylib`, and add `swift/.build/release` to `DYLD_LIBRARY_PATH`. The command-line invocations are otherwise the same.

## Commands

Each host currently supports `scan <file>`. The command emits JSON with a stable schema: content classification, SHA-256 source identity, native byte metrics, findings, and the stages actually executed.

## Current verification behavior

The native scanner measures byte count, zero-byte count, newline count, longest zero-byte run, UTF-8 validity, and a non-cryptographic FNV-1a diagnostic checksum. The hosts calculate SHA-256 independently with standard libraries (the Swift host contains a pure-Swift implementation).

Findings are deterministic and explicitly scoped: empty input, binary/NUL content, invalid UTF-8, and unusually long zero-byte runs. A binary classification is not itself a security vulnerability. The scanner never executes imported files and never modifies source material.

## Safety and implementation boundaries

This initial runtime is a working native core and cross-language contract, not a trained neural model, industrial certification system, binary patcher, autonomous production updater, or graphical dashboard. Those capabilities require executable domain modules, representative datasets, trained and evaluated models, hardware safety cases, signed artifacts, and human approval gates. No capability is represented as complete until it has real behavior and tests.

All product naming in this repository uses **9circ**.
