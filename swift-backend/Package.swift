// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "NineCircBackend",
    platforms: [.macOS(.v13)],
    products: [
        .executable(name: "ninecirc-server", targets: ["NineCircServer"]),
        .library(name: "NineCircBackendCore", targets: ["NineCircBackendCore"])
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", from: "4.110.0")
    ],
    targets: [
        .target(
            name: "NineCircBackendCore",
            dependencies: [.product(name: "Vapor", package: "vapor")]
        ),
        .executableTarget(
            name: "NineCircServer",
            dependencies: ["NineCircBackendCore", .product(name: "Vapor", package: "vapor")]
        ),
        .testTarget(name: "NineCircBackendCoreTests", dependencies: ["NineCircBackendCore"])
    ],
    swiftLanguageModes: [.v6]
)
