# 9circ native ABI

ABI version: 1. Exported symbols: `ninecirc_abi_version`, `ninecirc_scan`. Calling convention: C / cdecl. Integer encoding: little-endian. Result size: exactly 48 bytes.

```c
uint32_t ninecirc_abi_version(void);
int32_t ninecirc_scan(const uint8_t *input, size_t length, uint8_t *output);
```

The scanner accepts a null input pointer only when length is zero. The output pointer must refer to at least 48 writable bytes. Return value 0 indicates success; negative values indicate invalid arguments.

| Offset | Width | Field |
|---:|---:|---|
| 0 | 4 | status: signed 32-bit |
| 4 | 4 | flags: unsigned 32-bit |
| 8 | 8 | byte count: unsigned 64-bit |
| 16 | 8 | zero-byte count: unsigned 64-bit |
| 24 | 8 | LF newline count: unsigned 64-bit |
| 32 | 8 | FNV-1a-64 checksum: unsigned 64-bit |
| 40 | 8 | longest consecutive zero-byte run: unsigned 64-bit |

Flag bits: bit 0 valid UTF-8, bit 1 at least one NUL byte, bit 2 empty input. Unknown bits must be ignored.

FNV-1a is for diagnostics only, not cryptographic identity. The SHA-256 report field is calculated by the host. Consumers must check the ABI version before invoking the scanner. ABI changes require coordinated updates to every host, tests, and this document. Never read the result buffer after a failed call.
