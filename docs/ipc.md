# 9circ shared-memory IPC v1

All language runtimes use the same 32-byte little-endian metadata header. The payload starts immediately after the header and is kept in shared memory.

| Offset | Size | Field | Meaning |
|---:|---:|---|---|
| 0 | 4 | magic | ASCII 9CIR |
| 4 | 2 | version | 1 |
| 6 | 2 | type | Message type |
| 8 | 8 | sequence | Monotonic producer sequence |
| 16 | 4 | payload_length | Number of payload bytes |
| 20 | 4 | crc32 | CRC-32 of payload |
| 24 | 8 | monotonic_ns | Producer monotonic timestamp |

The header is intentionally fixed width and does not contain pointers. A receiver must validate magic, version, length against the mapped segment capacity, sequence ordering and checksum before exposing payload bytes to another module.

## Ownership and synchronization

The producer owns a slot until the consumer acknowledges its sequence. A slot may not be overwritten while leased by a consumer. Use process-shared atomics or a platform-supported process-shared synchronization primitive around slot state; language-local mutexes alone do not synchronize separate processes.

The Swift ring buffer currently serializes access within one process with NSLock. Before using it across processes, add a process-shared synchronization implementation and define crash recovery for abandoned slots. The header codec is cross-language; the synchronization protocol is an explicit deployment prerequisite.

## Compatibility

A breaking field change requires a new header version. Readers must reject unknown versions instead of guessing. Keep payload endianness and numeric encoding specified per message type. The initial v1 codec carries only metadata and does not serialize payload vectors.
