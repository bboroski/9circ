// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "NineCircBuffer",
    products: [
        .library(name: "NineCircBuffer", targets: ["NineCircBuffer"])
    ],
    targets: [
        .target(name: "NineCircBuffer"),
        .testTarget(name: "NineCircBufferTests", dependencies: ["NineCircBuffer"])
    ]
)
