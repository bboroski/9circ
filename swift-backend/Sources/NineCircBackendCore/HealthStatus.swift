import Foundation
import Vapor

public struct HealthStatus: Content, Sendable, Equatable {
    public let service: String
    public let status: String
    public let version: String
    public let timestamp: Date

    public init(
        service: String = "9circ",
        status: String,
        version: String,
        timestamp: Date = Date()
    ) {
        self.service = service
        self.status = status
        self.version = version
        self.timestamp = timestamp
    }
}

public enum BackendConfigurationError: Error, Equatable {
    case invalidPort(Int)
    case emptyVersion
}

public struct BackendConfiguration: Sendable, Equatable {
    public let host: String
    public let port: Int
    public let version: String

    public init(host: String, port: Int, version: String) throws {
        guard (1...65_535).contains(port) else {
            throw BackendConfigurationError.invalidPort(port)
        }
        guard !version.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
            throw BackendConfigurationError.emptyVersion
        }
        self.host = host
        self.port = port
        self.version = version
    }
}
