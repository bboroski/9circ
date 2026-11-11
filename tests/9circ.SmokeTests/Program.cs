using NineCirc.Core.Clustering;
using NineCirc.Core.Creative;
using NineCirc.Core.Ipc;
using NineCirc.Core.Motivation;
using NineCirc.Core.Scaling;

static void Check(bool condition, string message)
{
    if (!condition) throw new InvalidOperationException($"FAIL: {message}");
    Console.WriteLine($"PASS: {message}");
}

var points = new float[] { 0f, 0f, 0.1f, 0.1f, 5f, 5f, 5.1f, 5.1f, 30f, 30f };
var labels = new int[5];
var visited = new byte[5];
var queued = new byte[5];
var queue = new int[5];
var count = Dbscan.Cluster(points, 5, 2, 0.5f, 2, labels, visited, queued, queue);
Check(count == 2, "DBSCAN finds two dense clusters");
Check(labels[0] == labels[1] && labels[2] == labels[3], "DBSCAN groups nearby points");
Check(labels[4] == Dbscan.Noise, "DBSCAN classifies isolated point as noise");

var hierarchicalPoints = new float[] { 0f, 0f, 0.1f, 0.1f, 10f, 10f, 10.1f, 10.1f };
var centroids = new float[hierarchicalPoints.Length];
var sizes = new int[4];
var hierarchicalLabels = new int[4];
var active = new byte[4];
var remap = new int[4];
var hierarchicalCount = HierarchicalClustering.Cluster(
    hierarchicalPoints, 4, 2, 2, centroids, sizes, hierarchicalLabels, active, remap);
Check(hierarchicalCount == 2 && hierarchicalLabels[0] == hierarchicalLabels[1] &&
      hierarchicalLabels[2] == hierarchicalLabels[3], "Hierarchical centroid clustering merges nearest groups");

var matrix = new float[] { 1f, float.NaN, 3f, float.NaN, 5f, float.NaN };
FeatureSpaceUpscaler.InterpolateMissing(matrix, 3, 2);
Check(matrix.SequenceEqual(new float[] { 1f, 0f, 3f, 0f, 5f, 0f }), "Feature interpolation fills all-missing columns");
var vector = new float[] { 3f, 4f };
Check(FeatureSpaceUpscaler.NormalizeL2(vector) && Math.Abs(vector[0] - 0.6f) < 0.0001f, "L2 normalization");

var payload = new byte[] { 1, 2, 3, 4 };
Span<byte> headerBytes = stackalloc byte[SharedMemoryProtocol.HeaderSize];
var header = new IpcFrameHeader(1, 7, 42, (uint)payload.Length,
    SharedMemoryProtocol.ComputeCrc32(payload), 99);
SharedMemoryProtocol.Write(headerBytes, header);
var parsed = SharedMemoryProtocol.Read(headerBytes);
Check(parsed == header && SharedMemoryProtocol.ValidatePayload(parsed, payload),
    "Shared-memory header and CRC validation");

var mappedPath = Path.Combine(Path.GetTempPath(), $"9circ-{Guid.NewGuid():N}.shm");
try
{
    using (var mapped = new SharedMemoryRegion(mappedPath, 64))
    {
        new byte[] { 9, 8, 7, 6 }.CopyTo(mapped.Bytes[..4]);
        mapped.Flush();
    }
    using var reopened = new SharedMemoryRegion(mappedPath, 64);
    Check(reopened.Bytes[..4].SequenceEqual(new byte[] { 9, 8, 7, 6 }),
        "File-backed shared memory persists bytes across mappings");
}
finally
{
    if (File.Exists(mappedPath)) File.Delete(mappedPath);
}

var graph = new MotivationGraph();
graph.AddNode("cluster");
graph.AddNode("buffer", 0.5);
graph.AddDependency("cluster", "buffer", 0.4);
graph.RecordExecution("cluster");
graph.ApplyFeedback(new RuntimeFeedback(500, 0.2, 0.3, 0.01, 12));
Check(graph.Snapshot().Length == 2 && graph.GetPriority("cluster") >= 0, "Motivation graph accepts bounded runtime feedback");
var diagnostics = MotivationDiagnostics.Evaluate(graph.Snapshot(), 0.2, 0.3);
Check(diagnostics.IsBalanced, "Motivation diagnostics accept healthy resource pressure");

var source = new ParsedSource(SourceLanguage.CSharp, new[]
{
    new SyntaxDeclaration("method", "LoadA", 0, 20, "return cache lookup document"),
    new SyntaxDeclaration("method", "LoadB", 21, 40, "return cache lookup document")
});
Check(CodeEvolutionPlanner.Suggest(source).Count == 1, "Creative planner emits review-only similarity proposals");

Console.WriteLine("9circ smoke tests passed.");
