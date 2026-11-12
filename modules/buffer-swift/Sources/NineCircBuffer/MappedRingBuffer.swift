import Foundation
#if os(Linux)
import Glibc
#else
import Darwin
#endif

public enum RingBufferError: Error {
    case invalidCapacity
    case invalidTransferCount
    case systemCallFailed(String)
}

/// File-backed shared mapping. Payload moves directly between caller buffers and mmap memory.
/// Access is serialized; callers may wrap multiple reads/writes in their own higher-level protocol.
public final class MappedRingBuffer: @unchecked Sendable {
    private let descriptor: Int32
    private let mapping: UnsafeMutableRawPointer
    public let capacity: Int
    private let lock = NSLock()
    private var readIndex = 0
    private var writeIndex = 0
    private var available = 0

    public init(path: String, capacity: Int) throws {
        guard capacity > 0 else { throw RingBufferError.invalidCapacity }

        let fd = open(path, O_CREAT | O_RDWR, mode_t(0o600))
        guard fd >= 0 else { throw RingBufferError.systemCallFailed("open") }

        guard ftruncate(fd, off_t(capacity)) == 0 else {
            _ = close(fd)
            throw RingBufferError.systemCallFailed("ftruncate")
        }

        let mapped = mmap(nil, capacity, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0)
        guard mapped != MAP_FAILED, let memory = mapped else {
            _ = close(fd)
            throw RingBufferError.systemCallFailed("mmap")
        }

        descriptor = fd
        mapping = memory
        self.capacity = capacity
    }

    deinit {
        _ = munmap(mapping, capacity)
        _ = close(descriptor)
    }

    /// Gives the caller a direct view of the next contiguous writable mmap segment.
    /// The closure must not retain the pointer or re-enter this ring buffer.
    /// Returns the closure result and the number of bytes committed.
    public func withWritableSegment<T>(
        _ body: (UnsafeMutableRawBufferPointer) throws -> (T, Int)
    ) throws -> T {
        lock.lock()
        defer { lock.unlock() }

        let contiguous = min(capacity - available, capacity - writeIndex)
        let segment = UnsafeMutableRawBufferPointer(
            start: mapping.advanced(by: writeIndex), count: contiguous)
        let (result, committed) = try body(segment)
        guard committed >= 0 && committed <= contiguous else {
            throw RingBufferError.invalidTransferCount
        }

        writeIndex = (writeIndex + committed) % capacity
        available += committed
        return result
    }

    /// Gives the caller a direct read-only view of the next contiguous mmap segment.
    /// The closure must not retain the pointer or re-enter this ring buffer.
    /// Returns the closure result and the number of bytes consumed.
    public func withReadableSegment<T>(
        _ body: (UnsafeRawBufferPointer) throws -> (T, Int)
    ) throws -> T {
        lock.lock()
        defer { lock.unlock() }

        let contiguous = min(available, capacity - readIndex)
        let segment = UnsafeRawBufferPointer(
            start: mapping.advanced(by: readIndex), count: contiguous)
        let (result, consumed) = try body(segment)
        guard consumed >= 0 && consumed <= contiguous else {
            throw RingBufferError.invalidTransferCount
        }

        readIndex = (readIndex + consumed) % capacity
        available -= consumed
        return result
    }

    /// Writes as many bytes as fit. The input remains owned by the caller.
    @discardableResult
    public func write(_ source: UnsafeRawBufferPointer) -> Int {
        lock.lock()
        defer { lock.unlock() }

        let amount = min(source.count, capacity - available)
        guard amount > 0, let sourceBase = source.baseAddress else { return 0 }

        let firstChunk = min(amount, capacity - writeIndex)
        _ = memcpy(mapping.advanced(by: writeIndex), sourceBase, firstChunk)
        if amount > firstChunk {
            _ = memcpy(mapping, sourceBase.advanced(by: firstChunk), amount - firstChunk)
        }

        writeIndex = (writeIndex + amount) % capacity
        available += amount
        return amount
    }

    /// Copies bytes from the mapped region into caller-owned storage.
    @discardableResult
    public func read(into destination: UnsafeMutableRawBufferPointer) -> Int {
        lock.lock()
        defer { lock.unlock() }

        let amount = min(destination.count, available)
        guard amount > 0, let destinationBase = destination.baseAddress else { return 0 }

        let firstChunk = min(amount, capacity - readIndex)
        _ = memcpy(destinationBase, mapping.advanced(by: readIndex), firstChunk)
        if amount > firstChunk {
            _ = memcpy(destinationBase.advanced(by: firstChunk), mapping, amount - firstChunk)
        }

        readIndex = (readIndex + amount) % capacity
        available -= amount
        return amount
    }

    public var occupancy: Double {
        lock.lock()
        defer { lock.unlock() }
        return Double(available) / Double(capacity)
    }
}

public enum POSIXStream {
    /// Direct POSIX read(2); retries on EINTR and returns zero at EOF.
    public static func read(fd: Int32, into buffer: UnsafeMutableRawBufferPointer) throws -> Int {
        guard let base = buffer.baseAddress, !buffer.isEmpty else { return 0 }
        while true {
            #if os(Linux)
            let result = Glibc.read(fd, base, buffer.count)
            #else
            let result = Darwin.read(fd, base, buffer.count)
            #endif
            if result >= 0 { return result }
            if errno != EINTR {
                throw RingBufferError.systemCallFailed("read")
            }
        }
    }

    /// Direct POSIX write(2); retries on EINTR and returns the number of bytes written.
    public static func write(fd: Int32, from buffer: UnsafeRawBufferPointer) throws -> Int {
        guard let base = buffer.baseAddress, !buffer.isEmpty else { return 0 }
        while true {
            #if os(Linux)
            let result = Glibc.write(fd, base, buffer.count)
            #else
            let result = Darwin.write(fd, base, buffer.count)
            #endif
            if result >= 0 { return result }
            if errno != EINTR {
                throw RingBufferError.systemCallFailed("write")
            }
        }
    }
}
