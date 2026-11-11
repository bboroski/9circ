import Foundation
import Testing
@testable import NineCircBackendCore

@Test func healthStatusIsCodableAndSendableValue() throws {
    let status = HealthStatus(status: "ok", version: "1.2.3")
    let encoded = try JSONEncoder().encode(status)
    let decoded = try JSONDecoder().decode(HealthStatus.self, from: encoded)

    #expect(decoded == status)
    #expect(decoded.service == "9circ")
}

@Test func backendConfigurationAcceptsValidPort() throws {
    let configuration = try BackendConfiguration(
        host: "127.0.0.1",
        port: 8080,
        version: "1.0.0"
    )
    #expect(configuration.port == 8080)
}

@Test func backendConfigurationRejectsInvalidPort() {
    #expect(throws: BackendConfigurationError.invalidPort(70_000)) {
        try BackendConfiguration(host: "127.0.0.1", port: 70_000, version: "1.0.0")
    }
}

@Test func backendConfigurationRejectsEmptyVersion() {
    #expect(throws: BackendConfigurationError.emptyVersion) {
        try BackendConfiguration(host: "127.0.0.1", port: 8080, version: "  ")
    }
}
