// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "9circ",
    products: [
        .library(name: "ninecirc_core", type: .dynamic, targets: ["NinecircCore"]),
        .executable(name: "9circ-swift", targets: ["NinecircCLI"])
    ],
    targets: [
        .target(name: "NinecircCore"),
        .executableTarget(name: "NinecircCLI", dependencies: ["NinecircCore"]),
        .testTarget(name: "NinecircCoreTests", dependencies: ["NinecircCore"])
    ]
)
