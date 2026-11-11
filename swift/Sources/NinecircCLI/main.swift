import Foundation
import NinecircCore

@main
struct NinecircCommand {
    private static let maximumInputBytes = 64 * 1024 * 1024

    static func main() {
        let arguments = CommandLine.arguments
        guard arguments.count == 3, arguments[1] == "scan" else {
            FileHandle.standardError.write(Data("Usage: 9circ-swift scan <file>\n".utf8))
            exit(64)
        }

        let path = arguments[2]
        do {
            let attributes = try FileManager.default.attributesOfItem(atPath: path)
            guard let size = attributes[.size] as? NSNumber,
                  size.intValue <= maximumInputBytes else {
                throw CLIError.inputTooLarge
            }
            let data = try Data(contentsOf: URL(fileURLWithPath: path), options: .mappedIfSafe)
            let metrics = try scan(data)
            let diagnostics = buildDiagnostics(metrics)
            let report: [String: Any] = [
                "schemaVersion": 1,
                "product": "9circ",
                "input": URL(fileURLWithPath: path).lastPathComponent,
                "sha256": sha256Hex(data),
                "classification": (metrics.containsNul || !metrics.utf8Valid) ? "binary" : "text",
                "metrics": [
                    "byteCount": metrics.byteCount,
                    "zeroBytes": metrics.zeroBytes,
                    "lineCount": metrics.lineCount,
                    "longestZeroRun": metrics.longestZeroRun,
                    "fnv64": String(format: "%016llx", metrics.fnv64),
                    "utf8Valid": metrics.utf8Valid
                ],
                "diagnostics": diagnostics,
                "stages": ["Import", "Identification", "Analysis", "Verification", "Diagnosis", "Report"]
            ]
            let encoded = try JSONSerialization.data(withJSONObject: report, options: [.prettyPrinted, .sortedKeys])
            FileHandle.standardOutput.write(encoded)
            FileHandle.standardOutput.write(Data([0x0A]))
        } catch {
            FileHandle.standardError.write(Data(("9circ: " + String(describing: error) + "\n").utf8))
            exit(1)
        }
    }

    private static func buildDiagnostics(_ metrics: ScanMetrics) -> [[String: String]] {
        var findings: [[String: String]] = []
        if metrics.byteCount == 0 {
            findings.append(finding(
                "9circ-empty-input", "Structural Defects", "warning",
                "The input file is empty.", "The file contains zero bytes.",
                "Review whether an empty artifact is intentional.",
                "Re-scan after the expected source content is restored."
            ))
        }
        if metrics.containsNul {
            findings.append(finding(
                "9circ-binary-content", "Content Classification", "info",
                "The input contains NUL bytes and is classified as binary.",
                "At least one byte has the value 0x00.",
                "Use a format-aware binary verifier before interpreting this artifact as source code.",
                "Compare the detected format with the declared input type."
            ))
        } else if !metrics.utf8Valid {
            findings.append(finding(
                "9circ-invalid-utf8", "Structural Defects", "warning",
                "The input is not valid UTF-8 text.",
                "The byte sequence cannot be decoded as UTF-8.",
                "Confirm the declared text encoding; do not rewrite bytes automatically.",
                "Validate the file with its documented encoding."
            ))
        }
        if metrics.longestZeroRun >= 4096 {
            findings.append(finding(
                "9circ-zero-run", "Resource Constraints", "warning",
                "A long contiguous run of zero bytes was detected.",
                "At least 4096 consecutive bytes are zero.",
                "Inspect the relevant binary section or padding boundary.",
                "Re-scan and compare the zero-run metric after an approved change."
            ))
        }
        return findings
    }

    private static func finding(
        _ id: String, _ category: String, _ severity: String,
        _ description: String, _ cause: String, _ recommendation: String, _ verification: String
    ) -> [String: String] {
        [
            "id": id, "category": category, "severity": severity,
            "description": description, "cause": cause,
            "recommendation": recommendation, "verification": verification
        ]
    }
}

private enum CLIError: Error {
    case inputTooLarge
}
