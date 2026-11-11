import Foundation

public struct IPCHeader: Equatable, Sendable {
    public static let byteCount = 32
    public static let currentVersion: UInt16 = 1

    public let version: UInt16
    public let type: UInt16
    public let sequence: UInt64
    public let payloadLength: UInt32
    public let crc32: UInt32
    public let monotonicNanoseconds: UInt64

    public init(type: UInt16, sequence: UInt64, payloadLength: UInt32,
                crc32: UInt32, monotonicNanoseconds: UInt64) {
        version = Self.currentVersion
        self.type = type
        self.sequence = sequence
        self.payloadLength = payloadLength
        self.crc32 = crc32
        self.monotonicNanoseconds = monotonicNanoseconds
    }

    public func encode() -> [UInt8] {
        var bytes = [UInt8](repeating: 0, count: Self.byteCount)
        bytes[0] = 0x39
        bytes[1] = 0x43
        bytes[2] = 0x49
        bytes[3] = 0x52
        Self.store(version, into: &bytes, at: 4)
        Self.store(type, into: &bytes, at: 6)
        Self.store(sequence, into: &bytes, at: 8)
        Self.store(payloadLength, into: &bytes, at: 16)
        Self.store(crc32, into: &bytes, at: 20)
        Self.store(monotonicNanoseconds, into: &bytes, at: 24)
        return bytes
    }

    public static func decode(_ bytes: [UInt8]) throws -> IPCHeader {
        guard bytes.count >= byteCount,
              Array(bytes[0..<4]) == [0x39, 0x43, 0x49, 0x52] else {
            throw RingBufferError.systemCallFailed("invalid IPC header")
        }
        let version: UInt16 = load(bytes, at: 4)
        guard version == currentVersion else {
            throw RingBufferError.systemCallFailed("unsupported IPC version")
        }
        return IPCHeader(
            version: version,
            type: load(bytes, at: 6),
            sequence: load(bytes, at: 8),
            payloadLength: load(bytes, at: 16),
            crc32: load(bytes, at: 20),
            monotonicNanoseconds: load(bytes, at: 24)
        )
    }

    private init(version: UInt16, type: UInt16, sequence: UInt64,
                 payloadLength: UInt32, crc32: UInt32, monotonicNanoseconds: UInt64) {
        self.version = version
        self.type = type
        self.sequence = sequence
        self.payloadLength = payloadLength
        self.crc32 = crc32
        self.monotonicNanoseconds = monotonicNanoseconds
    }

    private static func store<T: FixedWidthInteger>(_ value: T, into bytes: inout [UInt8], at offset: Int) {
        var little = value.littleEndian
        withUnsafeBytes(of: &little) { raw in
            for index in 0..<raw.count { bytes[offset + index] = raw[index] }
        }
    }

    private static func load<T: FixedWidthInteger>(_ bytes: [UInt8], at offset: Int) -> T {
        var value: T = 0
        withUnsafeMutableBytes(of: &value) { raw in
            for index in 0..<raw.count { raw[index] = bytes[offset + index] }
        }
        return T(littleEndian: value)
    }
}
