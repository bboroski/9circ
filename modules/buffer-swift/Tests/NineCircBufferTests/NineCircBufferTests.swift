import Foundation
import XCTest
@testable import NineCircBuffer

final class NineCircBufferTests: XCTestCase {
    func testRingBufferWrapAround() throws {
        let path = FileManager.default.temporaryDirectory
            .appendingPathComponent(UUID().uuidString).path
        defer { try? FileManager.default.removeItem(atPath: path) }

        let ring = try MappedRingBuffer(path: path, capacity: 8)
        let input: [UInt8] = Array("abcdef".utf8)
        let written = input.withUnsafeBytes { ring.write($0) }
        XCTAssertEqual(written, 6)

        var first = [UInt8](repeating: 0, count: 4)
        let firstRead = first.withUnsafeMutableBytes { ring.read(into: $0) }
        XCTAssertEqual(firstRead, 4)
        XCTAssertEqual(Array(first.prefix(firstRead)), Array("abcd".utf8))

        let tail: [UInt8] = Array("WXYZ".utf8)
        XCTAssertEqual(tail.withUnsafeBytes { ring.write($0) }, 4)

        var second = [UInt8](repeating: 0, count: 8)
        let secondRead = second.withUnsafeMutableBytes { ring.read(into: $0) }
        XCTAssertEqual(Array(second.prefix(secondRead)), Array("efWXYZ".utf8))
        XCTAssertEqual(ring.occupancy, 0)
    }

    func testSharedIPCHeader() throws {
        let source = IPCHeader(type: 5, sequence: 0x102030405, payloadLength: 256,
                               crc32: 0xAABBCCDD, monotonicNanoseconds: 1234)
        XCTAssertEqual(try IPCHeader.decode(source.encode()), source)
    }
}
