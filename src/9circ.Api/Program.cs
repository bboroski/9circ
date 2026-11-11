using System.Buffers;
using NineCirc.Core.Clustering;
using NineCirc.Core.Motivation;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<MotivationGraph>();
var app = builder.Build();

app.MapGet("/healthz", () => Results.Ok(new { service = "9circ-api", status = "healthy" }));
app.MapGet("/readyz", () => Results.Ok(new { service = "9circ-api", status = "ready" }));

app.MapPost("/api/v1/clusters", (ClusterRequest request) =>
{
    if (request.Values is null || request.Dimensions <= 0 ||
        request.Values.Length == 0 || request.Values.Length % request.Dimensions != 0)
        return Results.BadRequest(new { error = "Values must be a non-empty row-major matrix divisible by dimensions." });

    var pointCount = request.Values.Length / request.Dimensions;
    if (pointCount > 100_000 || request.Dimensions > 4096)
        return Results.BadRequest(new { error = "Request exceeds configured safety limits." });

    var labels = ArrayPool<int>.Shared.Rent(pointCount);
    var visited = ArrayPool<byte>.Shared.Rent(pointCount);
    var queued = ArrayPool<byte>.Shared.Rent(pointCount);
    var queue = ArrayPool<int>.Shared.Rent(pointCount);

    try
    {
        var clusterCount = Dbscan.Cluster(
            request.Values, pointCount, request.Dimensions,
            request.Epsilon, request.MinPoints,
            labels.AsSpan(0, pointCount),
            visited.AsSpan(0, pointCount),
            queued.AsSpan(0, pointCount),
            queue.AsSpan(0, pointCount));

        return Results.Ok(new ClusterResponse(
            clusterCount, labels.AsSpan(0, pointCount).ToArray()));
    }
    catch (ArgumentException exception)
    {
        return Results.BadRequest(new { error = exception.Message });
    }
    finally
    {
        ArrayPool<int>.Shared.Return(labels, clearArray: true);
        ArrayPool<byte>.Shared.Return(visited, clearArray: true);
        ArrayPool<byte>.Shared.Return(queued, clearArray: true);
        ArrayPool<int>.Shared.Return(queue, clearArray: true);
    }
});

app.MapGet("/api/v1/motivation", (MotivationGraph graph) => Results.Ok(graph.Snapshot()));
app.Run();

internal sealed record ClusterRequest(float[] Values, int Dimensions, float Epsilon, int MinPoints);
internal sealed record ClusterResponse(int ClusterCount, int[] Labels);
