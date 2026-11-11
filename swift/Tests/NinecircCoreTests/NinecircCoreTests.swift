import Foundation
import XCTest
@testable import NinecircCore

final class NinecircCoreTests: XCTestCase {
    func testEmptyInputMetrics() throws {
        let result = try scan(Data())
        XCTAssertEqual(result.byteCount, 0)
        XCTAssertEqual(result.zeroBytes, 0)
        XCTAssertEqual(result.lineCount, 0)
        XCTAssertTrue(result.utf8Valid)
        XCTAssertFalse(result.containsNul)
    }

    func testBinaryMetrics() throws {
        let result = try scan(Data([0x41, 0x00, 0x42, 0x0A]))
        XCTAssertEqual(result.byteCount, 4)
        XCTAssertEqual(result.zeroBytes, 1)
        XCTAssertEqual(result.lineCount, 1)
        XCTAssertTrue(result.containsNul)
        XCTAssertEqual(result.longestZeroRun, 1)
    }

    func testInvalidUtf8() throws {
        let result = try scan(Data([0xC3, 0x28]))
        XCTAssertFalse(result.utf8Valid)
    }

    func testSha256KnownVector() {
        XCTAssertEqual(
            sha256Hex(Data("abc".utf8)),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        )
    }
}
