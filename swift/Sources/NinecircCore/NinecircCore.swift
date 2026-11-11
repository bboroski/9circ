import Foundation

public struct ScanMetrics: Sendable, Equatable {
    public let byteCount: UInt64
    public let zeroBytes: UInt64
    public let lineCount: UInt64
    public let fnv64: UInt64
    public let longestZeroRun: UInt64
    public let utf8Valid: Bool
    public let containsNul: Bool
}

public enum NinecircCoreError: Error {
    case nativeCallFailed(Int32)
    case abiMismatch(UInt32)
}

@_cdecl("ninecirc_abi_version")
public func ninecirc_abi_version() -> UInt32 { 1 }

@_cdecl("ninecirc_scan")
public func ninecirc_scan(
    _ input: UnsafePointer<UInt8>?,
    _ length: Int,
    _ output: UnsafeMutablePointer<UInt8>?
) -> Int32 {
    guard length >= 0, let output else { return -1 }
    guard length == 0 || input != nil else { return -2 }

    var zeroCount: UInt64 = 0
    var newlineCount: UInt64 = 0
    var longestZeroRun: UInt64 = 0
    var currentZeroRun: UInt64 = 0
    var hash: UInt64 = 14_695_981_039_346_656_037

    if length > 0, let input {
        for index in 0..<length {
            let byte = input[index]
            hash = (hash ^ UInt64(byte)) &* 1_099_511_628_211
            if byte == 0 {
                zeroCount &+= 1
                currentZeroRun &+= 1
                longestZeroRun = max(longestZeroRun, currentZeroRun)
            } else {
                currentZeroRun = 0
            }
            if byte == 0x0A { newlineCount &+= 1 }
        }
    }

    let validUTF8: Bool
    if length == 0 {
        validUTF8 = true
    } else if let input {
        validUTF8 = String(
            bytes: UnsafeBufferPointer(start: input, count: length),
            encoding: .utf8
        ) != nil
    } else {
        validUTF8 = false
    }

    if length > 0, let input, input[length - 1] != 0x0A {
        newlineCount &+= 1
    }

    let flags =
        (validUTF8 ? UInt32(1) : UInt32(0)) |
        (zeroCount > 0 ? UInt32(2) : UInt32(0)) |
        (length == 0 ? UInt32(4) : UInt32(0))

    let raw = UnsafeMutableRawPointer(output)
    raw.storeBytes(of: Int32(0).littleEndian, toByteOffset: 0, as: Int32.self)
    raw.storeBytes(of: flags.littleEndian, toByteOffset: 4, as: UInt32.self)
    raw.storeBytes(of: UInt64(length).littleEndian, toByteOffset: 8, as: UInt64.self)
    raw.storeBytes(of: zeroCount.littleEndian, toByteOffset: 16, as: UInt64.self)
    raw.storeBytes(of: newlineCount.littleEndian, toByteOffset: 24, as: UInt64.self)
    raw.storeBytes(of: hash.littleEndian, toByteOffset: 32, as: UInt64.self)
    raw.storeBytes(of: longestZeroRun.littleEndian, toByteOffset: 40, as: UInt64.self)
    return 0
}

public func scan(_ data: Data) throws -> ScanMetrics {
    let version = ninecirc_abi_version()
    guard version == 1 else { throw NinecircCoreError.abiMismatch(version) }

    var output = [UInt8](repeating: 0, count: 48)
    let status = output.withUnsafeMutableBufferPointer { outputBuffer in
        data.withUnsafeBytes { inputBuffer in
            ninecirc_scan(
                inputBuffer.bindMemory(to: UInt8.self).baseAddress,
                data.count,
                outputBuffer.baseAddress
            )
        }
    }
    guard status == 0 else { throw NinecircCoreError.nativeCallFailed(status) }

    func readUInt32(_ offset: Int) -> UInt32 {
        UInt32(output[offset]) |
        (UInt32(output[offset + 1]) << 8) |
        (UInt32(output[offset + 2]) << 16) |
        (UInt32(output[offset + 3]) << 24)
    }

    func readUInt64(_ offset: Int) -> UInt64 {
        var value: UInt64 = 0
        for index in 0..<8 {
            value |= UInt64(output[offset + index]) << (index * 8)
        }
        return value
    }

    let flags = readUInt32(4)
    return ScanMetrics(
        byteCount: readUInt64(8),
        zeroBytes: readUInt64(16),
        lineCount: readUInt64(24),
        fnv64: readUInt64(32),
        longestZeroRun: readUInt64(40),
        utf8Valid: (flags & 1) != 0,
        containsNul: (flags & 2) != 0
    )
}

public func sha256Hex(_ data: Data) -> String {
    let constants: [UInt32] = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    @inline(__always)
    func rotateRight(_ value: UInt32, _ count: UInt32) -> UInt32 {
        (value >> count) | (value << (32 - count))
    }

    var message = [UInt8](data)
    let bitLength = UInt64(message.count) &* 8
    message.append(0x80)
    while message.count % 64 != 56 { message.append(0) }
    for shift in stride(from: 56, through: 0, by: -8) {
        message.append(UInt8((bitLength >> UInt64(shift)) & 0xff))
    }

    var state: [UInt32] = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    for chunkStart in stride(from: 0, to: message.count, by: 64) {
        var words = [UInt32](repeating: 0, count: 64)
        for index in 0..<16 {
            let offset = chunkStart + index * 4
            words[index] =
                (UInt32(message[offset]) << 24) |
                (UInt32(message[offset + 1]) << 16) |
                (UInt32(message[offset + 2]) << 8) |
                UInt32(message[offset + 3])
        }
        for index in 16..<64 {
            let x = words[index - 15]
            let y = words[index - 2]
            let s0 = rotateRight(x, 7) ^ rotateRight(x, 18) ^ (x >> 3)
            let s1 = rotateRight(y, 17) ^ rotateRight(y, 19) ^ (y >> 10)
            words[index] = words[index - 16] &+ s0 &+ words[index - 7] &+ s1
        }

        var a = state[0]
        var b = state[1]
        var c = state[2]
        var d = state[3]
        var e = state[4]
        var f = state[5]
        var g = state[6]
        var h = state[7]

        for index in 0..<64 {
            let sum1 = rotateRight(e, 6) ^ rotateRight(e, 11) ^ rotateRight(e, 25)
            let choose = (e & f) ^ ((~e) & g)
            let temp1 = h &+ sum1 &+ choose &+ constants[index] &+ words[index]
            let sum0 = rotateRight(a, 2) ^ rotateRight(a, 13) ^ rotateRight(a, 22)
            let majority = (a & b) ^ (a & c) ^ (b & c)
            let temp2 = sum0 &+ majority
            h = g
            g = f
            f = e
            e = d &+ temp1
            d = c
            c = b
            b = a
            a = temp1 &+ temp2
        }

        state[0] = state[0] &+ a
        state[1] = state[1] &+ b
        state[2] = state[2] &+ c
        state[3] = state[3] &+ d
        state[4] = state[4] &+ e
        state[5] = state[5] &+ f
        state[6] = state[6] &+ g
        state[7] = state[7] &+ h
    }

    return state.map { String(format: "%08x", $0) }.joined()
}
