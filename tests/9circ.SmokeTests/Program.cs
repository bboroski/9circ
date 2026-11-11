using NineCirc.Core.Clustering;
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

var matrix = new float[] { 1f, float.NaN, 3f, float.NaN, 5f, float.NaN };
FeatureSpaceUpscaler.InterpolateMissing(matrix, 3, 2);
Check(matrix.SequenceEqual(new float[] { 1f, 0f, 3f, 0f, 5f, 0f }), "Feature interpolation fills all-missing columns");
var vector = new float[] { 3f, 4f };
Check(FeatureSpaceUpscaler.NormalizeL2(vector) && Math.Abs(vector[0] - 0.6f) < 0.0001f, "L2 normalization");

Span<byte> headerBytes = stackalloc byte[SharedMemoryProtocol.HeaderSize];
var header = new IpcFrameHeader(1, 7, 42, 128, 0xAABBCCDD, 99);
SharedMemoryProtocol.Write(headerBytes, header);
var parsed = SharedMemoryProtocol.Read(headerBytes);
Check(parsed == header, "Shared-memory header round-trips");

var graph = new MotivationGraph();
graph.AddNode("cluster");
graph.AddNode("buffer", 0.5);
graph.AddDependency("cluster", "buffer", 0.4);
graph.RecordExecution("cluster");
graph.ApplyFeedback(new RuntimeFeedback(500, 0.2, 0.3, 0.01, 12));
Check(graph.Snapshot().Length == 2 && graph.GetPriority("cluster") >= 0, "Motivation graph accepts bounded runtime feedback");

Console.WriteLine("9circ smoke tests passed.");
