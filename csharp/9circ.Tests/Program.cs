using Ninecirc;

static void Require(bool condition, string message)
{
    if (!condition)
        throw new InvalidOperationException(message);
}

var binary = new byte[] { 0x41, 0x00, 0x42, 0x0A };
ScanMetrics result = NativeScanner.Scan(binary);
Require(result.ByteCount == 4, "byte count mismatch");
Require(result.ZeroBytes == 1, "zero-byte count mismatch");
Require(result.LineCount == 1, "line count mismatch");
Require(result.ContainsNul, "NUL flag missing");
Require(result.LongestZeroRun == 1, "zero-run mismatch");

ScanMetrics empty = NativeScanner.Scan(ReadOnlySpan<byte>.Empty);
Require(empty.ByteCount == 0, "empty byte count mismatch");
Require(empty.Utf8Valid, "empty input must be valid UTF-8");

Console.WriteLine("9circ C# native ABI tests passed.");
