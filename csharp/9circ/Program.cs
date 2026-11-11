using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text.Json;

namespace Ninecirc;

[StructLayout(LayoutKind.Explicit, Size = 48)]
internal struct NativeResult
{
    [FieldOffset(0)] public int Status;
    [FieldOffset(4)] public uint Flags;
    [FieldOffset(8)] public ulong ByteCount;
    [FieldOffset(16)] public ulong ZeroBytes;
    [FieldOffset(24)] public ulong LineCount;
    [FieldOffset(32)] public ulong Fnv64;
    [FieldOffset(40)] public ulong LongestZeroRun;
}

public readonly record struct ScanMetrics(
    ulong ByteCount, ulong ZeroBytes, ulong LineCount,
    ulong LongestZeroRun, ulong Fnv64, bool Utf8Valid, bool ContainsNul);

public static class NativeScanner
{
    private const uint RequiredAbiVersion = 1;

    [DllImport("ninecirc_core", EntryPoint = "ninecirc_abi_version", CallingConvention = CallingConvention.Cdecl)]
    private static extern uint AbiVersion();

    [DllImport("ninecirc_core", EntryPoint = "ninecirc_scan", CallingConvention = CallingConvention.Cdecl)]
    private static extern unsafe int ScanNative(byte* input, nuint length, byte* output);

    public static unsafe ScanMetrics Scan(ReadOnlySpan<byte> bytes)
    {
        uint version;
        try
        {
            version = AbiVersion();
        }
        catch (DllNotFoundException exception)
        {
            throw new InvalidOperationException(
                "The 9circ native library is missing. Build the Swift native product and configure the OS library loader.",
                exception);
        }

        if (version != RequiredAbiVersion)
            throw new InvalidOperationException("Unsupported 9circ native ABI version: " + version);

        Span<byte> resultBuffer = stackalloc byte[48];
        fixed (byte* input = bytes)
        fixed (byte* output = resultBuffer)
        {
            int status = ScanNative(input, (nuint)bytes.Length, output);
            if (status != 0)
                throw new InvalidOperationException("9circ native scan failed with code " + status);
        }

        NativeResult result = MemoryMarshal.Read<NativeResult>(resultBuffer);
        if (result.Status != 0)
            throw new InvalidOperationException("9circ native result contains status " + result.Status);

        return new ScanMetrics(
            result.ByteCount, result.ZeroBytes, result.LineCount,
            result.LongestZeroRun, result.Fnv64,
            (result.Flags & 1) != 0, (result.Flags & 2) != 0);
    }
}

public static class ProjectAnalyzer
{
    public const int MaximumInputBytes = 64 * 1024 * 1024;

    public static object Analyze(string inputName, ReadOnlySpan<byte> bytes)
    {
        ScanMetrics metrics = NativeScanner.Scan(bytes);
        string classification = metrics.ContainsNul || !metrics.Utf8Valid ? "binary" : "text";
        string digest = Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
        var diagnostics = new List<object>();

        if (metrics.ByteCount == 0)
        {
            diagnostics.Add(new {
                id = "9circ-empty-input", category = "Structural Defects", severity = "warning",
                description = "The input file is empty.", cause = "The file contains zero bytes.",
                recommendation = "Review whether an empty artifact is intentional.",
                verification = "Re-scan after the expected source content is restored."
            });
        }
        if (metrics.ContainsNul)
        {
            diagnostics.Add(new {
                id = "9circ-binary-content", category = "Content Classification", severity = "info",
                description = "The input contains NUL bytes and is classified as binary.",
                cause = "At least one byte has the value 0x00.",
                recommendation = "Use a format-aware binary verifier before interpreting this artifact as source code.",
                verification = "Compare the detected format with the declared input type."
            });
        }
        else if (!metrics.Utf8Valid)
        {
            diagnostics.Add(new {
                id = "9circ-invalid-utf8", category = "Structural Defects", severity = "warning",
                description = "The input is not valid UTF-8 text.",
                cause = "The byte sequence cannot be decoded as UTF-8.",
                recommendation = "Confirm the declared text encoding; do not rewrite bytes automatically.",
                verification = "Validate the file with its documented encoding."
            });
        }
        if (metrics.LongestZeroRun >= 4096)
        {
            diagnostics.Add(new {
                id = "9circ-zero-run", category = "Resource Constraints", severity = "warning",
                description = "A long contiguous run of zero bytes was detected.",
                cause = "At least 4096 consecutive bytes are zero.",
                recommendation = "Inspect the relevant binary section or padding boundary.",
                verification = "Re-scan and compare the zero-run metric after an approved change."
            });
        }

        return new {
            schemaVersion = 1,
            product = "9circ",
            input = inputName,
            sha256 = digest,
            classification,
            metrics = new {
                byteCount = metrics.ByteCount,
                zeroBytes = metrics.ZeroBytes,
                lineCount = metrics.LineCount,
                longestZeroRun = metrics.LongestZeroRun,
                fnv64 = metrics.Fnv64.ToString("x16"),
                utf8Valid = metrics.Utf8Valid
            },
            diagnostics,
            stages = new[] { "Import", "Identification", "Analysis", "Verification", "Diagnosis", "Report" }
        };
    }
}

internal static class Program
{
    private static int Main(string[] args)
    {
        if (args.Length != 2 || args[0] != "scan")
        {
            Console.Error.WriteLine("Usage: 9circ scan <file>");
            return 64;
        }

        try
        {
            string path = Path.GetFullPath(args[1]);
            var info = new FileInfo(path);
            if (!info.Exists)
                throw new FileNotFoundException("Input file was not found.", path);
            if (info.Length > ProjectAnalyzer.MaximumInputBytes)
                throw new IOException("Input exceeds the 64 MiB safety limit.");

            byte[] bytes;
            using (var stream = new FileStream(
                path, FileMode.Open, FileAccess.Read, FileShare.Read,
                64 * 1024, FileOptions.SequentialScan))
            {
                bytes = GC.AllocateUninitializedArray<byte>(checked((int)stream.Length));
                stream.ReadExactly(bytes.AsSpan());
            }

            object report = ProjectAnalyzer.Analyze(Path.GetFileName(path), bytes);
            Console.WriteLine(System.Text.Json.JsonSerializer.Serialize(
                report, new JsonSerializerOptions { WriteIndented = true }));
            return 0;
        }
        catch (Exception exception)
        {
            Console.Error.WriteLine("9circ: " + exception.Message);
            return 1;
        }
    }
}
