import Foundation
import Vapor
import NineCircBackendCore

@main
enum NineCircServer {
    static func main() async throws {
        let environment = Environment.detect()
        let app = try await Application.make(environment)

        do {
            let port = Int(Environment.get("PORT") ?? "8080") ?? 8080
            let host = Environment.get("HOST") ?? "0.0.0.0"
            let version = Environment.get("SERVICE_VERSION") ?? "0.1.0"
            let configuration = try BackendConfiguration(
                host: host,
                port: port,
                version: version
            )

            app.http.server.configuration.hostname = configuration.host
            app.http.server.configuration.port = configuration.port

            app.get("health") { _ async -> HealthStatus in
                HealthStatus(status: "ok", version: configuration.version)
            }

            app.get("ready") { _ async -> HealthStatus in
                // Readiness is intentionally local until concrete dependency
                // probes (PostgreSQL/Redis) are configured and verified.
                HealthStatus(status: "ready", version: configuration.version)
            }

            app.get("v1", "health") { _ async -> HealthStatus in
                HealthStatus(status: "ok", version: configuration.version)
            }

            app.logger.info("9circ Swift backend starting", metadata: [
                "host": .string(configuration.host),
                "port": .stringConvertible(configuration.port),
                "version": .string(configuration.version)
            ])

            try await app.execute()
            try await app.asyncShutdown()
        } catch {
            app.logger.report(error: error)
            try? await app.asyncShutdown()
            throw error
        }
    }
}
